"""Notification fanout and shared envelope rendering."""

from __future__ import annotations

from types import SimpleNamespace
import json
from pathlib import Path
from typing import Any, Callable
from urllib import parse as urlparse
from urllib import request as urlrequest

from .compat import ensure_legacy_import_path


def _post_urlencoded(url: str, payload: dict[str, Any]) -> None:
    data = urlparse.urlencode(payload).encode("utf-8")
    req = urlrequest.Request(url, data=data, method="POST")
    with urlrequest.urlopen(req, timeout=30) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    if isinstance(body, dict) and body.get("ok") is False:
        raise RuntimeError(f"request failed: {body}")


def _post_json(url: str, payload: dict[str, Any]) -> None:
    req = urlrequest.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlrequest.urlopen(req, timeout=30) as resp:
        raw = resp.read().decode("utf-8").strip()
    if raw:
        try:
            body = json.loads(raw)
        except json.JSONDecodeError:
            return
        if isinstance(body, dict) and body.get("code") not in (None, 0):
            raise RuntimeError(f"request failed: {body}")


def _summary_namespace(data: dict[str, Any]) -> SimpleNamespace:
    payload = {
        "title": data.get("title", ""),
        "primary_topic": data.get("primary_topic", ""),
        "secondary_topics": list(data.get("secondary_topics", [])),
        "entities": list(data.get("entities", [])),
        "conclusion": data.get("conclusion", ""),
        "bullets": list(data.get("bullets", [])),
        "evidence_quotes": list(data.get("evidence_quotes", [])),
        "coverage": data.get("coverage", "partial"),
        "confidence": data.get("confidence", "medium"),
        "note_tags": list(data.get("note_tags", [])),
        "follow_up_actions": list(data.get("follow_up_actions", [])),
        "timeliness": data.get("timeliness", "medium"),
        "effectiveness": data.get("effectiveness", "medium"),
        "recommendation_level": data.get("recommendation_level", "optional"),
        "reader_judgment": data.get("reader_judgment", ""),
    }
    return SimpleNamespace(**payload)


def _ingest_namespace(data: dict[str, Any]) -> SimpleNamespace:
    payload = {
        "chat_id": str(data.get("chat_id", "")),
        "reply_to_message_id": data.get("reply_to_message_id"),
        "request_id": data.get("request_id", ""),
        "source_kind": data.get("source_kind", ""),
        "source_url": data.get("source_url"),
        "raw_text": data.get("raw_text"),
        "image_refs": list(data.get("image_refs", [])),
        "platform_hint": data.get("platform_hint"),
        "requested_output_lang": data.get("requested_output_lang", "zh-CN"),
    }
    return SimpleNamespace(**payload)


def _evidence_namespace(data: dict[str, Any]) -> SimpleNamespace:
    payload = {
        "source_kind": data.get("source_kind", ""),
        "source_url": data.get("source_url"),
        "platform_hint": data.get("platform_hint"),
        "title": data.get("title"),
        "text": data.get("text", ""),
        "evidence_type": data.get("evidence_type", ""),
        "coverage": data.get("coverage", "partial"),
        "transcript": data.get("transcript"),
        "keyframes": list(data.get("keyframes", [])),
        "metadata": dict(data.get("metadata", {})),
    }
    return SimpleNamespace(**payload)


class NullNotifier:
    def send_result(self, *args, **kwargs) -> None:
        return None


class EnvelopeRenderer:
    def __init__(self, legacy_project_root: Path | None) -> None:
        ensure_legacy_import_path(legacy_project_root)
        from openclaw_capture_workflow.telegram import TelegramNotifier

        self._builder = TelegramNotifier("disabled")

    def render_text(
        self,
        ingest,
        summary,
        note_path: str,
        structure_map: str,
        open_url: str,
        evidence=None,
        summary_model: str | None = None,
        summary_elapsed_seconds: float | None = None,
    ) -> str:
        payload = self._builder.build_result_message_payload(
            ingest,
            summary,
            note_path,
            structure_map,
            open_url,
            evidence,
            summary_model,
            summary_elapsed_seconds,
        )
        return str(payload["text"])


class FanoutNotifier:
    def __init__(
        self,
        *,
        outputs: tuple[str, ...],
        telegram_bot_token: str = "",
        feishu_webhook: str = "",
        legacy_project_root: Path | None = None,
        text_renderer: Callable[..., str] | None = None,
        telegram_sender: Callable[[dict[str, Any]], None] | None = None,
        feishu_sender: Callable[[str], None] | None = None,
    ) -> None:
        self.outputs = outputs
        self.telegram_bot_token = telegram_bot_token
        self.feishu_webhook = feishu_webhook
        self._renderer = text_renderer or EnvelopeRenderer(legacy_project_root).render_text
        self._telegram_sender = telegram_sender or self._send_telegram_payload
        self._feishu_sender = feishu_sender or self._send_feishu_text

    def _send_telegram_payload(self, payload: dict[str, Any]) -> None:
        if not self.telegram_bot_token:
            raise RuntimeError("telegram output selected but OPENCLAW_CAPTURE_TELEGRAM_BOT_TOKEN is missing")
        _post_urlencoded(
            f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage",
            payload,
        )

    def _send_feishu_text(self, text: str) -> None:
        if not self.feishu_webhook:
            raise RuntimeError("feishu output selected but OPENCLAW_CAPTURE_FEISHU_WEBHOOK is missing")
        _post_json(
            self.feishu_webhook,
            {
                "msg_type": "text",
                "content": {
                    "text": text,
                },
            },
        )

    def _fanout(
        self,
        ingest,
        summary,
        note_path: str,
        structure_map: str,
        open_url: str,
        evidence=None,
        summary_model: str | None = None,
        summary_elapsed_seconds: float | None = None,
        skip_outputs: set[str] | None = None,
    ) -> str:
        skip_outputs = skip_outputs or set()
        text = self._renderer(
            ingest,
            summary,
            note_path,
            structure_map,
            open_url,
            evidence,
            summary_model,
            summary_elapsed_seconds,
        )
        if "telegram" in self.outputs and "telegram" not in skip_outputs:
            payload: dict[str, Any] = {
                "chat_id": str(getattr(ingest, "chat_id", "")),
                "text": text,
            }
            reply_to_message_id = getattr(ingest, "reply_to_message_id", None)
            if reply_to_message_id not in (None, ""):
                payload["reply_to_message_id"] = str(reply_to_message_id)
            self._telegram_sender(payload)
        if "feishu" in self.outputs and "feishu" not in skip_outputs:
            self._feishu_sender(text)
        return text

    def send_result(
        self,
        ingest,
        summary,
        note_path: str,
        structure_map: str,
        open_url: str,
        evidence=None,
        summary_model: str | None = None,
        summary_elapsed_seconds: float | None = None,
    ) -> None:
        self._fanout(
            ingest,
            summary,
            note_path,
            structure_map,
            open_url,
            evidence,
            summary_model,
            summary_elapsed_seconds,
        )

    def send_from_job_result(
        self,
        ingest_payload: dict[str, Any],
        job: dict[str, Any],
        *,
        skip_outputs: set[str] | None = None,
    ) -> str:
        result = dict(job.get("result", {}))
        note = dict(result.get("note", {}))
        summary = _summary_namespace(dict(result.get("summary", {})))
        evidence = _evidence_namespace(dict(result.get("evidence", {})))
        ingest = _ingest_namespace(ingest_payload)
        note_path = str(note.get("note_path", ""))
        structure_map = str(note.get("structure_map", ""))
        open_url = str(note.get("obsidian_uri") or result.get("open_url") or "")
        return self._fanout(
            ingest,
            summary,
            note_path,
            structure_map,
            open_url,
            evidence,
            result.get("summary_model"),
            result.get("summary_elapsed_seconds"),
            skip_outputs=skip_outputs,
        )

