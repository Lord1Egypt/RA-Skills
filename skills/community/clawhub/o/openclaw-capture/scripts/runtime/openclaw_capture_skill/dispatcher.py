"""Dispatch payloads into the legacy workflow through library or HTTP modes."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import time
import uuid
from urllib import request as urlrequest

from .compat import ensure_legacy_import_path, legacy_scripts_dir
from .config import Settings
from .fallback_renderer import FallbackNoteRenderer
from .local_summary import DeterministicSummaryEngine
from .notifiers import FanoutNotifier, NullNotifier


def normalize_payload(payload: dict) -> dict:
    data = copy.deepcopy(dict(payload))
    if not str(data.get("chat_id", "")).strip():
        raise ValueError("payload missing chat_id")
    if not str(data.get("source_kind", "")).strip():
        raise ValueError("payload missing source_kind")
    data.setdefault("request_id", str(uuid.uuid4()))
    data.setdefault("reply_to_message_id", None)
    data.setdefault("source_url", None)
    data.setdefault("raw_text", None)
    data.setdefault("image_refs", [])
    data.setdefault("platform_hint", None)
    data.setdefault("requested_output_lang", "zh-CN")
    return data


class CaptureDispatcher:
    def __init__(
        self,
        settings: Settings | None = None,
        *,
        extractor_override=None,
        summary_engine=None,
        note_renderer=None,
        fanout_notifier=None,
    ) -> None:
        self.settings = settings or Settings.from_env()
        self.extractor_override = extractor_override
        self.summary_engine = summary_engine
        self.note_renderer = note_renderer
        self.fanout_notifier = fanout_notifier

    def dispatch(self, payload: dict) -> dict:
        normalized = normalize_payload(payload)
        if self.settings.backend_mode == "http":
            return self._dispatch_http(normalized)
        return self._dispatch_library(normalized)

    def _load_legacy_app_config(self):
        legacy_root = ensure_legacy_import_path(self.settings.legacy_project_root)
        from openclaw_capture_workflow.config import (
            AppConfig,
            ExtractorConfig,
            ObsidianConfig,
            SummarizerConfig,
            TelegramConfig,
        )

        config = None
        if self.settings.legacy_config_path and self.settings.legacy_config_path.exists():
            try:
                config = AppConfig.load(str(self.settings.legacy_config_path))
            except Exception:
                config = None
        if config is None:
            config = AppConfig(
                listen_host="127.0.0.1",
                listen_port=8765,
                state_dir=str(self.settings.state_dir),
                obsidian=ObsidianConfig(
                    vault_path=self.settings.vault_path_override or str((Path.home() / "Documents" / "ObsidianVault")),
                    inbox_root="Inbox/OpenClaw",
                    topics_root="Topics",
                    entities_root="Entities",
                    auto_topic_whitelist=["AI", "股票", "GitHub", "产品", "工具", "商业"],
                    auto_topic_blocklist=[
                        "测试",
                        "总结",
                        "结构",
                        "回群",
                        "回执",
                        "路径",
                        "显示",
                        "验证",
                        "本地链接",
                        "wiki",
                        "md",
                        "Telegram",
                        "Obsidian",
                        "OpenClaw",
                    ],
                    auto_entity_pages=False,
                ),
                telegram=TelegramConfig(result_bot_token=self.settings.telegram_bot_token or "disabled"),
                summarizer=SummarizerConfig(
                    api_base_url=self.settings.model_api_base_url,
                    api_key=self.settings.model_api_key or "disabled",
                    model=self.settings.summary_model,
                    timeout_seconds=60,
                ),
                extractors=ExtractorConfig(),
            )
        if self.settings.vault_path_override:
            config.obsidian.vault_path = self.settings.vault_path_override
        config.summarizer.api_base_url = self.settings.model_api_base_url
        if self.settings.model_api_key:
            config.summarizer.api_key = self.settings.model_api_key
        config.summarizer.model = self.settings.summary_model
        if self.settings.telegram_bot_token:
            config.telegram.result_bot_token = self.settings.telegram_bot_token

        scripts_dir = legacy_scripts_dir(legacy_root)
        bridge_script = self.settings.skill_root / "scripts" / "video_audio_bridge.py"
        config.extractors.video_subtitle_command = (
            f'python3 "{scripts_dir / "video_subtitle_extract.py"}" --url "{{url}}" --max-seconds "{{max_seconds}}"'
        )
        config.extractors.video_audio_command = (
            f'python3 "{bridge_script}" --url "{{url}}" --max-seconds "{{max_seconds}}" '
            '--api-key "{api_key}" --api-base-url "{api_base_url}"'
        )
        config.extractors.video_keyframes_command = (
            f'python3 "{scripts_dir / "video_keyframes_extract.py"}" --url "{{url}}" '
            '--output-path "{output_path}" --max-seconds "{max_seconds}"'
        )
        config.video_summary.api_base_url = config.summarizer.api_base_url
        config.video_summary.api_key = config.summarizer.api_key
        config.video_summary.transport = "openai_compat"
        return config

    def _build_fanout_notifier(self, legacy_cfg=None):
        if self.fanout_notifier is not None:
            return self.fanout_notifier
        telegram_token = self.settings.telegram_bot_token
        if not telegram_token and legacy_cfg is not None:
            telegram_token = getattr(legacy_cfg.telegram, "result_bot_token", "")
        return FanoutNotifier(
            outputs=self.settings.outputs,
            telegram_bot_token=telegram_token,
            feishu_webhook=self.settings.feishu_webhook,
            legacy_project_root=self.settings.legacy_project_root,
        )

    def _patch_open_url(self, job: dict) -> None:
        result = job.get("result")
        if not isinstance(result, dict):
            return
        note = result.get("note")
        if isinstance(note, dict):
            obsidian_uri = note.get("obsidian_uri")
            if obsidian_uri:
                result["open_url"] = obsidian_uri

    def _maybe_fanout(self, payload: dict, job: dict, *, skip_outputs: set[str] | None = None, legacy_cfg=None) -> None:
        if payload.get("dry_run"):
            return
        if job.get("status") != "done":
            return
        if not self.settings.outputs:
            return
        try:
            notifier = self._build_fanout_notifier(legacy_cfg=legacy_cfg)
            notifier.send_from_job_result(payload, job, skip_outputs=skip_outputs)
        except Exception as exc:
            job.setdefault("warnings", []).append(f"wrapper_notification_error: {exc}")
            result = job.setdefault("result", {})
            if isinstance(result, dict):
                result["notification_error"] = str(exc)

    def _dispatch_library(self, payload: dict) -> dict:
        config = self._load_legacy_app_config()
        ensure_legacy_import_path(self.settings.legacy_project_root)
        from openclaw_capture_workflow.models import IngestRequest
        from openclaw_capture_workflow.processor import WorkflowProcessor
        from openclaw_capture_workflow.storage import JobStore
        from openclaw_capture_workflow.summarizer import OpenAICompatibleSummarizer

        state_dir = self.settings.state_dir
        (state_dir / "jobs").mkdir(parents=True, exist_ok=True)
        (state_dir / "artifacts").mkdir(parents=True, exist_ok=True)
        jobs = JobStore(state_dir / "jobs")
        if self.summary_engine is not None:
            summarizer = self.summary_engine
        elif payload.get("dry_run"):
            summarizer = DeterministicSummaryEngine()
            config.execution.dry_run_skip_model_call = False
        elif not str(getattr(config.summarizer, "api_key", "") or "").strip() or str(config.summarizer.api_key).strip() == "disabled":
            summarizer = DeterministicSummaryEngine()
            config.execution.dry_run_skip_model_call = False
        else:
            summarizer = OpenAICompatibleSummarizer(config.summarizer)
        processor = WorkflowProcessor(config, jobs, summarizer, state_dir)
        if self.extractor_override is not None:
            processor.extractor = self.extractor_override
        if self.note_renderer is not None:
            processor.writer.renderer = self.note_renderer
        elif processor.writer.renderer is None or not str(getattr(config.summarizer, "api_key", "") or "").strip() or str(config.summarizer.api_key).strip() == "disabled":
            processor.writer.renderer = FallbackNoteRenderer()
        processor.notifier = NullNotifier()
        processor.start()
        try:
            ingest = IngestRequest.from_dict(payload)
            job = processor.enqueue(ingest)
            processor._queue.join()
            stored = jobs.load(job.job_id)
            if stored is None:
                raise RuntimeError(f"job not found after processing: {job.job_id}")
            job_dict = stored.to_dict()
        finally:
            processor.stop()
        self._patch_open_url(job_dict)
        self._maybe_fanout(payload, job_dict, legacy_cfg=config)
        return job_dict

    def _dispatch_http(self, payload: dict) -> dict:
        request = urlrequest.Request(
            f"{self.settings.backend_url.rstrip('/')}/ingest",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlrequest.urlopen(request, timeout=30) as resp:
            accepted = json.loads(resp.read().decode("utf-8"))
        job_id = str(accepted.get("job_id") or payload["request_id"])
        deadline = time.time() + self.settings.poll_timeout_seconds
        while True:
            poll = urlrequest.Request(
                f"{self.settings.backend_url.rstrip('/')}/jobs/{job_id}",
                method="GET",
            )
            with urlrequest.urlopen(poll, timeout=30) as resp:
                job = json.loads(resp.read().decode("utf-8"))
            if str(job.get("status")) in {"done", "failed"}:
                break
            if time.time() >= deadline:
                raise TimeoutError(f"timed out waiting for job {job_id}")
            time.sleep(self.settings.poll_interval_seconds)
        self._patch_open_url(job)
        self._maybe_fanout(payload, job, skip_outputs={"telegram"})
        return job
