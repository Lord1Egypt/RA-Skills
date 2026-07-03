from __future__ import annotations

import json
import uuid
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from deepseek_client import DeepSeekClient, StructuredResponseError
from enrich_keywords import enrich_missing_keywords
from match_jobs import match_pending_papers
from models import (
    KeywordGenerationResult,
    MatchClass,
    PaperMatchResult,
    ReplyClass,
)


FIXTURES = Path(__file__).parent / "fixtures"


def settings():
    return SimpleNamespace(
        deepseek_base_url="https://api.deepseek.com",
        deepseek_model="deepseek-v4-pro",
        deepseek_api_key_env="DEEPSEEK_API_KEY",
        thinking_enabled=True,
        reasoning_effort="medium",
        timeout_seconds=30,
        max_attempts=3,
    )


class FakeResponse:
    def __init__(self, content, status_code=200):
        self.status_code = status_code
        self._content = content

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")

    def json(self):
        return {
            "choices": [{"message": {"content": self._content}}],
            "model": "deepseek-v4-pro",
            "usage": {"prompt_tokens": 10, "completion_tokens": 20},
        }


class FakeTransport:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def post(self, url, **kwargs):
        self.calls.append((url, kwargs))
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return FakeResponse(response)


def test_client_reads_api_key_from_environment_and_redacts_it(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "secret-value")
    client = DeepSeekClient(settings(), transport=FakeTransport([]))

    assert client.has_credentials()
    assert "secret-value" not in str(client.safe_settings())


def test_match_request_uses_official_thinking_and_json_parameters(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "secret-value")
    transport = FakeTransport(
        [
            """{
              "classification": "高度匹配",
              "evidence": ["摘要明确包含多模态检索"],
              "matched_requirements": ["多模态"],
              "missing_requirements": [],
              "uncertainties": [],
              "summary": "研究方向与岗位一致"
            }"""
        ]
    )
    client = DeepSeekClient(settings(), transport=transport)

    result = client.match_paper({"title": "Paper", "abstract": "Abstract", "job": {}})

    assert result.classification == MatchClass.HIGH
    request = transport.calls[0][1]["json"]
    assert request["model"] == "deepseek-v4-pro"
    assert request["thinking"] == {"type": "enabled"}
    assert request["reasoning_effort"] == "medium"
    assert request["response_format"] == {"type": "json_object"}
    assert "temperature" not in request


def test_invalid_json_retries_then_raises(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "secret-value")
    transport = FakeTransport(["not-json", "{}", "still-not-valid"])
    client = DeepSeekClient(settings(), transport=transport)

    with pytest.raises(StructuredResponseError, match="3 attempts"):
        client.match_paper({"title": "Paper", "abstract": "Abstract", "job": {}})

    assert len(transport.calls) == 3


def test_reply_classification_rejects_unknown_class(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "secret-value")
    transport = FakeTransport(
        [
            """{
              "classification": "自动录用",
              "evidence_summary": "未知分类",
              "confidence": 0.9,
              "suggested_action": "send",
              "needs_reply": true,
              "reply_body": "test",
              "followup_date": null
            }"""
        ]
        * 3
    )

    with pytest.raises(StructuredResponseError):
        DeepSeekClient(settings(), transport=transport).classify_reply(
            {"messages": [{"body": "hello"}]}
        )

    assert ReplyClass.ADVANCE.value == "积极推进"


def seed_paper(database, *, keywords):
    paper_id = str(uuid.uuid4())
    database.execute(
        """
        INSERT INTO papers (
            id, source_key, source_type, source_record_id, title, normalized_title,
            abstract, original_keywords_json, generated_keywords_json,
            official_url, acceptance_evidence_url, publication_date, collected_at
        ) VALUES (?, 'cvpr', 'conference', ?, 'Paper', 'paper', 'Abstract', ?, '[]',
                  'https://openaccess.thecvf.com/paper', 
                  'https://openaccess.thecvf.com/paper', '2026-01-01', ?)
        """,
        (
            paper_id,
            paper_id,
            json.dumps(keywords, ensure_ascii=False),
            datetime.now(UTC).isoformat(),
        ),
    )
    return paper_id


class FakeWorkflowClient:
    def __init__(self):
        self.keyword_calls = []
        self.match_calls = []

    def generate_keywords(self, payload):
        self.keyword_calls.append(payload)
        return KeywordGenerationResult(
            keywords=("多模态", "视觉语言模型"),
            model="deepseek-v4-pro",
            usage={},
        )

    def match_paper(self, payload):
        self.match_calls.append(payload)
        return PaperMatchResult(
            classification=MatchClass.POSSIBLE,
            evidence=("摘要证据",),
            matched_requirements=("深度学习",),
            missing_requirements=(),
            uncertainties=("缺少工程经历",),
            summary="可能匹配",
            model="deepseek-v4-pro",
            usage={},
        )


def test_original_keywords_are_never_overwritten(initialized_database):
    paper_id = seed_paper(initialized_database, keywords=["视觉语言模型"])
    client = FakeWorkflowClient()

    enriched = enrich_missing_keywords(initialized_database, client)

    row = initialized_database.fetch_one(
        """
        SELECT original_keywords_json, generated_keywords_json
        FROM papers WHERE id = ?
        """,
        (paper_id,),
    )
    assert enriched == 0
    assert json.loads(row["original_keywords_json"]) == ["视觉语言模型"]
    assert json.loads(row["generated_keywords_json"]) == []
    assert client.keyword_calls == []


def test_missing_keywords_store_model_metadata(initialized_database):
    paper_id = seed_paper(initialized_database, keywords=[])
    client = FakeWorkflowClient()

    assert enrich_missing_keywords(initialized_database, client) == 1

    row = initialized_database.fetch_one(
        """
        SELECT generated_keywords_json, keyword_model, keyword_prompt_version,
               keywords_generated_at
        FROM papers WHERE id = ?
        """,
        (paper_id,),
    )
    assert json.loads(row["generated_keywords_json"]) == ["多模态", "视觉语言模型"]
    assert row["keyword_model"] == "deepseek-v4-pro"
    assert row["keyword_prompt_version"] == "keywords-v1"
    assert row["keywords_generated_at"]


def test_each_active_job_gets_an_immutable_snapshot(initialized_database):
    seed_paper(initialized_database, keywords=["深度学习"])
    jobs = yaml.safe_load(
        (FIXTURES / "jobs.yaml").read_text(encoding="utf-8")
    )["jobs"]
    client = FakeWorkflowClient()

    matches = match_pending_papers(initialized_database, jobs, client)

    assert len(matches) == 2
    assert len({match.job_snapshot_id for match in matches}) == 2
    assert initialized_database.fetch_one(
        "SELECT COUNT(*) AS count FROM job_snapshots"
    )["count"] == 2
