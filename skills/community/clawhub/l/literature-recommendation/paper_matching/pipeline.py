"""End-to-end recommendation pipeline."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from .config import Settings
from .fetchers import ArxivFetcher
from .matching import rank_for_member
from .models import MemberProfile, Paper
from .storage import Storage


def _profile_queries(profile: MemberProfile) -> list[str]:
    terms: list[str] = []
    if profile.primary_direction:
        terms.append(profile.primary_direction)
    terms.extend(profile.secondary_directions)
    terms.extend(profile.keywords)
    cleaned = []
    seen = set()
    for term in terms:
        value = term.strip()
        if value and value.lower() not in seen:
            cleaned.append(value)
            seen.add(value.lower())
    return cleaned[:8]


def _resolve_profiles(storage: Storage, settings: Settings, profile_source: str) -> list[MemberProfile]:
    profiles = storage.load_profiles()
    if not profiles:
        raise RuntimeError("No profiles found in database. Please sync profiles first.")
    return profiles


def run_pipeline(
    settings: Settings,
    days: int = 7,
    top_k: int = 5,
    max_results_per_member: int = 20,
    profile_source: str = "auto",
    dry_run: bool = False,
) -> dict[str, Any]:
    settings.output_dir.mkdir(parents=True, exist_ok=True)
    storage = Storage(settings.db_dsn)
    profiles = _resolve_profiles(storage, settings, profile_source)

    fetcher = ArxivFetcher()
    run_id = f"run_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')}_{uuid4().hex[:8]}"
    started_at = datetime.now(timezone.utc).isoformat()
    storage.save_run_status(run_id, "running", started_at)

    all_papers: dict[str, Paper] = {}
    fetch_log: list[dict[str, Any]] = []
    for profile in profiles:
        queries = _profile_queries(profile)
        if not queries:
            continue
        papers = fetcher.fetch_for_keywords(queries, max_results=max_results_per_member)
        fetch_log.append({"record_id": profile.record_id, "queries": queries, "count": len(papers)})
        for paper in papers:
            all_papers[paper.paper_id] = paper

    storage.save_papers(list(all_papers.values()))

    recommendations_by_member: dict[str, list] = {}
    rerank_payload_by_member: dict[str, dict[str, Any]] = {}
    recommendations_to_store = []
    for profile in profiles:
        candidate_top_k = max(top_k, settings.recall_candidate_pool)
        candidate_recommendations = rank_for_member(profile, list(all_papers.values()), top_k=candidate_top_k)
        member_recommendations = candidate_recommendations[:top_k]

        recommendations_by_member[profile.record_id] = member_recommendations
        recommendations_to_store.extend(member_recommendations)
        rerank_payload_by_member[profile.record_id] = {
            "profile": profile.to_dict(),
            "candidates": [
                {
                    "paper_id": rec.paper_id,
                    "rule_score": rec.score,
                    "rule_reason": rec.reason,
                    "paper": all_papers[rec.paper_id].to_dict() if rec.paper_id in all_papers else {},
                }
                for rec in candidate_recommendations
            ],
        }

    storage.save_recommendations(run_id, recommendations_to_store)

    member_payloads = {}
    for profile in profiles:
        member_payloads[profile.record_id] = {
            "profile": profile.to_dict(),
            "recommendations": [rec.to_dict() for rec in recommendations_by_member.get(profile.record_id, [])],
        }

    report = {
        "run_id": run_id,
        "started_at": started_at,
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "days": days,
        "profile_source": profile_source,
        "profiles": [profile.to_dict() for profile in profiles],
        "fetched_papers": [paper.to_dict() for paper in all_papers.values()],
        "fetch_log": fetch_log,
        "openclaw_rerank_payload": {
            "strategy": "hard_rule_recall",
            "note": "OpenClaw should send candidates to LLM and return reranked top_k.",
            "candidate_pool": settings.recall_candidate_pool,
            "llm_reason_contract": {
                "language": "zh-CN",
                "reason_style": "explanatory",
                "required_source": ["paper.title", "paper.abstract", "profile.primary_direction", "profile.keywords"],
                "forbidden": ["title_only_reason"],
                "reason_generation_steps": [
                    "先阅读 paper.abstract 提取论文核心方法/任务",
                    "再对照成员偏好字段判断匹配点",
                    "最后生成一句概括 + 一句匹配说明",
                ],
                "must_include": [
                    "论文核心内容一句话概括",
                    "与该成员偏好匹配的具体点",
                ],
                "max_length": 120,
                "example": "该文聚焦多模态医学影像分割，并提出轻量级跨模态对齐模块；与你关注的医学AI与多模态学习方向高度匹配。",
            },
            "llm_output_schema": {
                "by_member": {
                    "record_id": {
                        "items": [
                            {
                                "paper_id": "string",
                                "keep": "boolean",
                                "rank": "integer",
                                "score": "number",
                                "reason": "string",
                            }
                        ]
                    }
                }
            },
            "by_member": rerank_payload_by_member,
        },
        "member_reports": member_payloads,
        "delivery_payload": _build_delivery_payload(report_context={
            "run_id": run_id,
            "member_reports": member_payloads,
            "fetched_papers": [paper.to_dict() for paper in all_papers.values()],
        }, settings=settings),
    }

    storage.save_run_status(run_id, "finished", started_at, report["finished_at"], notes=f"papers={len(all_papers)}, members={len(profiles)}")

    report_path = settings.output_dir / f"{run_id}.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def _build_delivery_payload(report_context: dict[str, Any], settings: Settings) -> dict[str, Any]:
    run_id = report_context["run_id"]
    paper_by_id = {item["paper_id"]: item for item in report_context["fetched_papers"]}

    personal_cards = []
    for record_id, payload in report_context["member_reports"].items():
        profile = payload["profile"]
        for rec in payload["recommendations"]:
            paper = paper_by_id.get(rec["paper_id"], {})
            title = paper.get("title") or rec["paper_id"]
            abstract = paper.get("abstract") or ""
            raw_url = paper.get("url") or ""

            card = {
                "config": {"wide_screen_mode": True},
                "header": {
                    "template": "blue",
                    "title": {
                        "tag": "plain_text",
                        "content": f"OpenClaw 推荐 · {profile.get('display_name')} · {rec['rank']}",
                    },
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": (
                                f"**{title}**\\n"
                                f"score={rec['score']} | {rec['reason']}\\n"
                                f"[打开论文]({raw_url})"
                            ),
                        },
                    },
                ],
            }

            personal_cards.append(
                {
                    "record_id": record_id,
                    "display_name": profile.get("display_name"),
                    "feishu_user_id": profile.get("feishu_user_id", ""),
                    "paper_id": rec["paper_id"],
                    "rank": rec["rank"],
                    "score": rec["score"],
                    "reason": rec["reason"],
                    "paper_title": title,
                    "paper_abstract": abstract,
                    "paper_url": raw_url,
                    "card": card,
                }
            )

    return {
        "run_id": run_id,
        "personal_cards": personal_cards,
    }
