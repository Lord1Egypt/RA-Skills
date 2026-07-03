#!/usr/bin/env python3
"""Feishu long-connection image bot for Go Next Move.

This file is intentionally isolated from the main skill entry points. It reads
chat settings, downloads Feishu image messages, calls scripts/next_move.py, and
replies with the coordinate plus result image. It does not alter the existing
CLI or web server.
"""
from __future__ import annotations

import argparse
import contextlib
import json
import logging
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from collections import deque
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if not (REPO_ROOT / "scripts" / "next_move.py").exists():
    REPO_ROOT = Path.cwd()
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import next_move  # noqa: E402

try:
    import lark_oapi as lark
    from lark_oapi.api.im.v1 import (
        CreateImageRequest,
        CreateImageRequestBody,
        CreateMessageRequest,
        CreateMessageRequestBody,
        GetMessageResourceRequest,
        P2ImMessageReceiveV1,
        ReplyMessageRequest,
        ReplyMessageRequestBody,
    )
except ImportError as exc:  # pragma: no cover - exercised on missing install
    raise SystemExit(
        "Missing Feishu dependencies. Install with: "
        "python3 -m pip install -r integrations/feishu/requirements.txt"
    ) from exc


DEFAULT_SETTINGS_PATH = Path.home() / ".go-next-move" / "feishu-settings.json"
DEFAULT_PROCESSED_PATH = Path.home() / ".go-next-move" / "feishu-processed-messages.json"
DEFAULT_ENV_PATH = REPO_ROOT / ".env.feishu"

SIDE_ALIASES = {
    "b": "black",
    "black": "black",
    "黑": "black",
    "黑棋": "black",
    "w": "white",
    "white": "white",
    "白": "white",
    "白棋": "white",
}
LEVEL_ALIASES = {
    "beginner": "beginner",
    "初": "beginner",
    "初级": "beginner",
    "low": "beginner",
    "intermediate": "intermediate",
    "中": "intermediate",
    "中级": "intermediate",
    "medium": "intermediate",
    "advanced": "advanced",
    "高": "advanced",
    "高级": "advanced",
    "high": "advanced",
    "expert": "expert",
    "special": "expert",
    "特": "expert",
    "特级": "expert",
}
SIDE_LABEL = {"black": "黑棋", "white": "白棋"}
LEVEL_LABEL = {"beginner": "初级", "intermediate": "中级", "advanced": "高级", "expert": "特级"}
LEVEL_VISITS = {"beginner": 100, "intermediate": 200, "advanced": 300, "expert": 400}
FEEDBACK_COMMANDS = {"上报", "报错", "识别错", "反馈"}


@dataclass
class ChatSettings:
    side_to_move: str = "black"
    level: str = "intermediate"
    coordinate_style: str = "gtp"

    def label(self) -> str:
        coord = "GTP坐标" if self.coordinate_style == "gtp" else "连续坐标"
        return f"{SIDE_LABEL[self.side_to_move]} / {LEVEL_LABEL[self.level]} / {coord}"

    def visit_budget(self, default_visits: int) -> int:
        return LEVEL_VISITS.get(self.level, default_visits)


@dataclass
class SettingsPatch:
    side_to_move: str | None = None
    level: str | None = None
    coordinate_style: str | None = None

    def apply(self, current: ChatSettings) -> ChatSettings:
        return ChatSettings(
            side_to_move=self.side_to_move or current.side_to_move,
            level=self.level or current.level,
            coordinate_style=self.coordinate_style or current.coordinate_style,
        )


class SettingsStore:
    def __init__(self, path: Path, default_settings: ChatSettings) -> None:
        self.path = path
        self.default_settings = default_settings
        self._lock = threading.Lock()
        self._data: dict[str, dict[str, str]] = {}
        self._load()

    def get(self, chat_id: str) -> ChatSettings:
        with self._lock:
            raw = self._data.get(chat_id, {})
        return ChatSettings(
            side_to_move=raw.get("side_to_move", self.default_settings.side_to_move),
            level=raw.get("level", self.default_settings.level),
            coordinate_style=raw.get("coordinate_style", self.default_settings.coordinate_style),
        )

    def update(self, chat_id: str, settings: ChatSettings) -> None:
        with self._lock:
            self._data[chat_id] = asdict(settings)
            self._save_locked()

    def _load(self) -> None:
        if not self.path.exists():
            return
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return
        if isinstance(payload, dict):
            chats = payload.get("chats", payload)
            if isinstance(chats, dict):
                self._data = {
                    str(chat_id): value
                    for chat_id, value in chats.items()
                    if isinstance(value, dict)
                }

    def _save_locked(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        tmp.write_text(
            json.dumps({"chats": self._data}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        tmp.replace(self.path)


class ProcessedMessageStore:
    def __init__(self, path: Path, max_items: int = 1000) -> None:
        self.path = path
        self.max_items = max_items
        self._lock = threading.Lock()
        self._ids: set[str] = set()
        self._order: deque[str] = deque()
        self._load()

    def add_if_new(self, message_id: str) -> bool:
        with self._lock:
            if message_id in self._ids:
                return False
            self._ids.add(message_id)
            self._order.append(message_id)
            while len(self._order) > self.max_items:
                old_message_id = self._order.popleft()
                self._ids.discard(old_message_id)
            self._save_locked()
            return True

    def _load(self) -> None:
        if not self.path.exists():
            return
        try:
            payload = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return
        raw_ids = payload.get("message_ids") if isinstance(payload, dict) else payload
        if not isinstance(raw_ids, list):
            return
        for raw_id in raw_ids[-self.max_items :]:
            message_id = str(raw_id)
            if message_id in self._ids:
                continue
            self._ids.add(message_id)
            self._order.append(message_id)

    def _save_locked(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        tmp.write_text(
            json.dumps({"message_ids": list(self._order)}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        tmp.replace(self.path)


@dataclass
class AnalysisSnapshot:
    chat_id: str
    message_id: str
    settings: ChatSettings
    input_image: Path
    output_image: Path
    result: dict[str, Any]
    created_at: float


class KataGoAnalysisEngine:
    def __init__(
        self,
        katago: str,
        model: str,
        config: str,
        skill_config: Path,
        logger: logging.Logger,
    ) -> None:
        self.katago = katago
        self.model = model
        self.config = config
        self.skill_config = skill_config
        self.log = logger
        self._lock = threading.Lock()
        self._proc: subprocess.Popen[str] | None = None
        self._stderr_tail: deque[str] = deque(maxlen=80)
        self._stderr_thread: threading.Thread | None = None

    def analyze(
        self,
        rows: list[str],
        side_to_move: str,
        komi: float,
        visits: int,
        katago: str,
        model: str,
        config: str,
        skill_config: Path,
    ) -> dict[str, Any]:
        del katago, model, config, skill_config
        query = {
            "id": f"go-next-move-{next_move.uuid.uuid4().hex}",
            "initialStones": next_move.board_ascii_to_initial_stones(rows),
            "initialPlayer": side_to_move,
            "moves": [],
            "rules": "chinese",
            "komi": komi,
            "boardXSize": len(rows),
            "boardYSize": len(rows),
            "analyzeTurns": [0],
            "maxVisits": visits,
            "includePVVisits": True,
            "analysisPVLen": 8,
        }
        with self._lock:
            proc = self._ensure_process()
            assert proc.stdin is not None
            assert proc.stdout is not None
            proc.stdin.write(json.dumps(query, ensure_ascii=False) + "\n")
            proc.stdin.flush()

            final_response = None
            warnings = []
            while True:
                line = proc.stdout.readline()
                if line == "":
                    self._proc = None
                    raise RuntimeError(f"KataGo exited before returning analysis. stderr:\n{self._stderr_text()}")
                line = line.strip()
                if not line:
                    continue
                try:
                    payload = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if "error" in payload:
                    raise RuntimeError(f"KataGo returned an error: {payload['error']}")
                if "warning" in payload:
                    warnings.append(payload["warning"])
                    continue
                if payload.get("id") == query["id"] and payload.get("isDuringSearch") is False:
                    final_response = payload
                    break

            if final_response is None:
                raise RuntimeError(f"KataGo returned no final analysis response. stderr:\n{self._stderr_text()}")
            if warnings:
                final_response.setdefault("warnings", []).extend(warnings)
            return final_response

    def _ensure_process(self) -> subprocess.Popen[str]:
        if self._proc is not None and self._proc.poll() is None:
            return self._proc
        if self._proc is not None:
            self.log.warning("restarting exited KataGo analysis process returncode=%s", self._proc.returncode)

        skill_config_arg = self._skill_config_arg()
        command = [
            self.katago,
            "analysis",
            "-model",
            self.model,
            "-config",
            self.config,
            "-config",
            skill_config_arg,
        ]
        self.log.info("starting resident KataGo analysis process")
        self._proc = subprocess.Popen(
            command,
            cwd=REPO_ROOT,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        self._stderr_tail.clear()
        self._stderr_thread = threading.Thread(target=self._drain_stderr, args=(self._proc,), daemon=True)
        self._stderr_thread.start()
        return self._proc

    def _skill_config_arg(self) -> str:
        if not self.skill_config.is_absolute():
            return str(self.skill_config)
        try:
            return str(self.skill_config.relative_to(REPO_ROOT))
        except ValueError as exc:
            raise RuntimeError(
                "KataGo analysis does not accept an absolute project override config path; "
                "pass a path relative to this project"
            ) from exc

    def _drain_stderr(self, proc: subprocess.Popen[str]) -> None:
        if proc.stderr is None:
            return
        for line in proc.stderr:
            self._stderr_tail.append(line.rstrip())

    def _stderr_text(self) -> str:
        return "\n".join(self._stderr_tail)

    def close(self) -> None:
        proc = self._proc
        self._proc = None
        if proc is None or proc.poll() is not None:
            return
        proc.terminate()
        with contextlib.suppress(subprocess.TimeoutExpired):
            proc.wait(timeout=5)
        if proc.poll() is None:
            proc.kill()


@dataclass
class BotConfig:
    app_id: str
    app_secret: str
    settings_path: Path
    default_settings: ChatSettings
    visits: int
    katago: str
    model: str | None
    analysis_config: str | None
    skill_config: str | None
    top_candidates: int
    processed_path: Path
    feedback_dir: Path | None = None
    debug: bool = False


class GoNextMoveFeishuBot:
    def __init__(self, config: BotConfig) -> None:
        self.config = config
        self.store = SettingsStore(config.settings_path, config.default_settings)
        self.processed_messages = ProcessedMessageStore(config.processed_path)
        self._recent_analysis_lock = threading.Lock()
        self._recent_analysis_by_chat: dict[str, AnalysisSnapshot] = {}
        self.log = logging.getLogger("feishu-bot")
        self.started_at_ms = int(time.time() * 1000)
        self.katago_engine = KataGoAnalysisEngine(
            katago=config.katago,
            model=config.model or next_move.DEFAULT_MODEL,
            config=config.analysis_config or next_move.DEFAULT_ANALYSIS_CONFIG,
            skill_config=Path(config.skill_config) if config.skill_config else next_move.DEFAULT_SKILL_CONFIG,
            logger=self.log,
        )
        logging.basicConfig(
            level=logging.DEBUG if config.debug else logging.INFO,
            format="[%(asctime)s] %(levelname)s %(name)s: %(message)s",
        )
        self.client = (
            lark.Client.builder()
            .app_id(config.app_id)
            .app_secret(config.app_secret)
            .build()
        )
        self.event_handler = (
            lark.EventDispatcherHandler.builder("", "")
            .register_p2_im_message_receive_v1(self.handle_message_event)
            .build()
        )
        self.ws_client = lark.ws.Client(
            config.app_id,
            config.app_secret,
            event_handler=self.event_handler,
            log_level=lark.LogLevel.DEBUG if config.debug else lark.LogLevel.INFO,
        )

    def handle_message_event(self, data: P2ImMessageReceiveV1) -> None:
        try:
            message = data.event.message
            if self._is_stale_message(message):
                self.processed_messages.add_if_new(message.message_id)
                self.log.info("skip stale message_id=%s create_time=%s", message.message_id, message.create_time)
                return
            if self._already_seen(message.message_id):
                self.log.info("skip duplicate message_id=%s", message.message_id)
                return
            self.log.info(
                "received message chat_id=%s chat_type=%s message_id=%s message_type=%s",
                message.chat_id,
                message.chat_type,
                message.message_id,
                message.message_type,
            )
            if message.message_type == "text":
                payload = json.loads(message.content or "{}")
                self._handle_text(
                    chat_id=message.chat_id,
                    message_id=message.message_id,
                    chat_type=message.chat_type,
                    text=str(payload.get("text", "")),
                )
                return
            if message.message_type == "image":
                payload = json.loads(message.content or "{}")
                image_key = str(payload.get("image_key", ""))
                if not image_key:
                    self._send_text(
                        message.chat_id,
                        message.message_id,
                        message.chat_type,
                        "没有拿到图片 key，请再发一次棋盘照片。",
                    )
                    return
                threading.Thread(
                    target=self._handle_image_safely,
                    args=(message.chat_id, message.message_id, message.chat_type, image_key),
                    daemon=True,
                ).start()
                return
            self.log.info("ignored unsupported message_type=%s", message.message_type)
        except Exception as exc:
            self.log.exception("failed to handle Feishu message: %s", exc)

    def _is_stale_message(self, message: Any) -> bool:
        create_time_ms = self._message_create_time_ms(message)
        if create_time_ms is None:
            return False
        return create_time_ms < self.started_at_ms - 60_000

    def _message_create_time_ms(self, message: Any) -> int | None:
        try:
            return int(message.create_time)
        except (TypeError, ValueError):
            return None

    def _handle_text(self, chat_id: str, message_id: str, chat_type: str, text: str) -> None:
        command = parse_settings_command(text)
        if command == "help":
            self._send_text(chat_id, message_id, chat_type, help_text(self.store.get(chat_id)))
            return
        if command == "show":
            self._send_text(chat_id, message_id, chat_type, f"当前设置：{self.store.get(chat_id).label()}")
            return
        if command == "feedback":
            self._send_text(chat_id, message_id, chat_type, self._handle_feedback(chat_id, message_id))
            return
        if isinstance(command, SettingsPatch):
            settings = command.apply(self.store.get(chat_id))
            self.store.update(chat_id, settings)
            self._send_text(chat_id, message_id, chat_type, f"已设置：{settings.label()}。之后直接发棋盘照片即可。")
            return
        if looks_like_setting_attempt(text):
            self._send_text(chat_id, message_id, chat_type, "设置格式示例：设置 黑 中级，或 设置 白 特级。")
            return
        self._send_text(chat_id, message_id, chat_type, unsupported_text())

    def _handle_image(self, chat_id: str, message_id: str, chat_type: str, image_key: str) -> None:
        settings = self.store.get(chat_id)
        self._send_text(chat_id, message_id, chat_type, f"收到棋盘图，按当前设置分析：{settings.label()}。")
        started_at = time.monotonic()
        try:
            result = self._analyze_image(message_id, image_key, settings)
        except Exception as exc:
            self._send_text(
                chat_id,
                message_id,
                chat_type,
                f"分析失败：{exc}\n耗时：{format_elapsed(time.monotonic() - started_at)}",
            )
            return

        elapsed_seconds = time.monotonic() - started_at
        self._remember_analysis(chat_id, message_id, settings, result)
        self._send_text(
            chat_id,
            message_id,
            chat_type,
            format_analysis_text(result, settings, elapsed_seconds=elapsed_seconds),
        )
        result_image = result.get("result_image")
        if result_image:
            try:
                self._send_image(chat_id, message_id, chat_type, Path(result_image))
            except Exception as exc:
                self.log.exception("failed to send result image: %s", exc)
                self._send_text(chat_id, message_id, chat_type, f"标注图发送失败：{exc}")
        else:
            self._send_text(chat_id, message_id, chat_type, "没有生成标注图，请查看本地日志。")

    def _handle_image_safely(self, chat_id: str, message_id: str, chat_type: str, image_key: str) -> None:
        try:
            self._handle_image(chat_id, message_id, chat_type, image_key)
        except Exception as exc:
            self.log.exception("failed to handle image message_id=%s: %s", message_id, exc)

    def _already_seen(self, message_id: str) -> bool:
        return not self.processed_messages.add_if_new(message_id)

    def _remember_analysis(
        self,
        chat_id: str,
        message_id: str,
        settings: ChatSettings,
        analysis: dict[str, Any],
    ) -> None:
        input_image = analysis.get("input_image")
        output_image = analysis.get("result_image") or analysis.get("source_result_image")
        if not input_image or not output_image:
            return
        snapshot = AnalysisSnapshot(
            chat_id=chat_id,
            message_id=message_id,
            settings=settings,
            input_image=Path(input_image),
            output_image=Path(output_image),
            result=analysis,
            created_at=time.time(),
        )
        with self._recent_analysis_lock:
            self._recent_analysis_by_chat[chat_id] = snapshot

    def _handle_feedback(self, chat_id: str, report_message_id: str) -> str:
        if self.config.feedback_dir is None:
            return "服务端还没有配置错误上报目录，请先设置 FEISHU_FEEDBACK_DIR。"
        with self._recent_analysis_lock:
            snapshot = self._recent_analysis_by_chat.get(chat_id)
        if snapshot is None:
            return "还没有可上报的最近一次分析。请先发送一张棋盘照片，等我返回结果后再发送“上报”。"
        try:
            sample_dir = self._write_feedback_snapshot(snapshot, report_message_id)
        except Exception as exc:
            self.log.exception("failed to write feedback sample: %s", exc)
            return f"上报失败：{exc}"
        return f"已保存这次错误样本：{sample_dir}"

    def _write_feedback_snapshot(self, snapshot: AnalysisSnapshot, report_message_id: str) -> Path:
        assert self.config.feedback_dir is not None
        if not snapshot.input_image.exists():
            raise RuntimeError(f"输入图片不存在：{snapshot.input_image}")
        if not snapshot.output_image.exists():
            raise RuntimeError(f"输出图片不存在：{snapshot.output_image}")
        timestamp = time.strftime("%Y%m%d-%H%M%S", time.localtime(snapshot.created_at))
        sample_dir = self.config.feedback_dir / f"{timestamp}-{safe_filename(snapshot.message_id)}"
        sample_dir.mkdir(parents=True, exist_ok=True)
        input_path = sample_dir / "input.jpg"
        output_path = sample_dir / "output.jpg"
        shutil.copyfile(snapshot.input_image, input_path)
        shutil.copyfile(snapshot.output_image, output_path)
        metadata = {
            "chat_id": snapshot.chat_id,
            "analysis_message_id": snapshot.message_id,
            "report_message_id": report_message_id,
            "created_at": iso_timestamp(snapshot.created_at),
            "reported_at": iso_timestamp(time.time()),
            "settings": asdict(snapshot.settings),
            "recommendation": snapshot.result.get("recommendation"),
            "timings": snapshot.result.get("timings"),
            "input_image": "input.jpg",
            "output_image": "output.jpg",
            "result": snapshot.result,
        }
        (sample_dir / "metadata.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        self.log.info("saved feedback sample chat_id=%s dir=%s", snapshot.chat_id, sample_dir)
        return sample_dir

    def _analyze_image(self, message_id: str, image_key: str, settings: ChatSettings) -> dict[str, Any]:
        total_started_at = time.monotonic()
        with tempfile.TemporaryDirectory(prefix="go-next-feishu-") as tmp:
            tmp_dir = Path(tmp)
            in_path = tmp_dir / "board.jpg"
            out_path = tmp_dir / "result.jpg"
            download_started_at = time.monotonic()
            self._download_image(message_id, image_key, in_path)
            persisted_input = Path(tempfile.gettempdir()) / f"go-next-feishu-input-{message_id}.jpg"
            persisted_input.write_bytes(in_path.read_bytes())
            download_seconds = time.monotonic() - download_started_at
            katago_seconds = 0.0

            def timed_analysis_runner(*runner_args: Any, **runner_kwargs: Any) -> dict[str, Any]:
                nonlocal katago_seconds
                katago_started_at = time.monotonic()
                try:
                    return self.katago_engine.analyze(*runner_args, **runner_kwargs)
                finally:
                    katago_seconds += time.monotonic() - katago_started_at

            args = argparse.Namespace(
                source=str(in_path),
                input="image",
                side_to_move=settings.side_to_move,
                level=settings.level,
                coordinate_style=settings.coordinate_style,
                move_overlay=[],
                board_size=19,
                komi=7.5,
                visits=settings.visit_budget(self.config.visits),
                top_candidates=self.config.top_candidates,
                warp_size=1200,
                corners=None,
                grid_corners=False,
                overlay=None,
                source_overlay=None,
                result_image=None,
                source_result_image=out_path,
                result_size=1200,
                katago=self.config.katago,
                model=self.config.model or next_move.DEFAULT_MODEL,
                analysis_config=self.config.analysis_config or next_move.DEFAULT_ANALYSIS_CONFIG,
                skill_config=Path(self.config.skill_config) if self.config.skill_config else next_move.DEFAULT_SKILL_CONFIG,
                analysis_runner=timed_analysis_runner,
            )
            build_started_at = time.monotonic()
            analysis = next_move.build_result(args)
            build_seconds = time.monotonic() - build_started_at

            image_path = Path(analysis.get("result_image") or analysis.get("source_result_image") or out_path)
            if image_path.exists():
                persisted = Path(tempfile.gettempdir()) / f"go-next-feishu-result-{message_id}.jpg"
                persisted.write_bytes(image_path.read_bytes())
                analysis["result_image"] = str(persisted)
            analysis["input_image"] = str(persisted_input)
            recognition_and_render_seconds = max(0.0, build_seconds - katago_seconds)
            analysis["timings"] = {
                "download_seconds": round(download_seconds, 3),
                "recognition_and_render_seconds": round(recognition_and_render_seconds, 3),
                "katago_seconds": round(katago_seconds, 3),
                "total_seconds": round(time.monotonic() - total_started_at, 3),
            }
            self.log.info(
                "analysis timings message_id=%s download=%.2fs recognition_render=%.2fs katago=%.2fs total=%.2fs",
                message_id,
                download_seconds,
                recognition_and_render_seconds,
                katago_seconds,
                time.monotonic() - total_started_at,
            )
            return analysis

    def _download_image(self, message_id: str, image_key: str, output_path: Path) -> None:
        request = (
            GetMessageResourceRequest.builder()
            .message_id(message_id)
            .file_key(image_key)
            .type("image")
            .build()
        )
        response = self.client.im.v1.message_resource.get(request)
        if not response.success():
            raise RuntimeError(
                f"图片下载失败：code={response.code}, msg={response.msg}, log_id={response.get_log_id()}"
            )
        output_path.write_bytes(response.file.read())

    def _send_text(self, chat_id: str, message_id: str, chat_type: str, text: str) -> None:
        content = json.dumps({"text": text}, ensure_ascii=False)
        if chat_type == "p2p":
            request = (
                CreateMessageRequest.builder()
                .receive_id_type("chat_id")
                .request_body(
                    CreateMessageRequestBody.builder()
                    .receive_id(chat_id)
                    .msg_type("text")
                    .content(content)
                    .build()
                )
                .build()
            )
            response = self.client.im.v1.message.create(request)
        else:
            request = (
                ReplyMessageRequest.builder()
                .message_id(message_id)
                .request_body(
                    ReplyMessageRequestBody.builder()
                    .msg_type("text")
                    .content(content)
                    .build()
                )
                .build()
            )
            response = self.client.im.v1.message.reply(request)
        if not response.success():
            raise RuntimeError(
                f"发送文字失败：code={response.code}, msg={response.msg}, log_id={response.get_log_id()}"
            )

    def _send_image(self, chat_id: str, message_id: str, chat_type: str, path: Path) -> None:
        with path.open("rb") as image_file:
            upload_request = (
                CreateImageRequest.builder()
                .request_body(
                    CreateImageRequestBody.builder()
                    .image_type("message")
                    .image(image_file)
                    .build()
                )
                .build()
            )
            upload_response = self.client.im.v1.image.create(upload_request)
        if not upload_response.success():
            raise RuntimeError(
                f"上传图片失败：code={upload_response.code}, msg={upload_response.msg}, log_id={upload_response.get_log_id()}"
            )
        content = json.dumps({"image_key": upload_response.data.image_key}, ensure_ascii=False)
        if chat_type == "p2p":
            request = (
                CreateMessageRequest.builder()
                .receive_id_type("chat_id")
                .request_body(
                    CreateMessageRequestBody.builder()
                    .receive_id(chat_id)
                    .msg_type("image")
                    .content(content)
                    .build()
                )
                .build()
            )
            response = self.client.im.v1.message.create(request)
        else:
            request = (
                ReplyMessageRequest.builder()
                .message_id(message_id)
                .request_body(
                    ReplyMessageRequestBody.builder()
                    .msg_type("image")
                    .content(content)
                    .build()
                )
                .build()
            )
            response = self.client.im.v1.message.reply(request)
        if not response.success():
            raise RuntimeError(
                f"发送图片失败：code={response.code}, msg={response.msg}, log_id={response.get_log_id()}"
            )

    def start(self) -> None:
        self.ws_client.start()


def parse_settings_command(text: str) -> SettingsPatch | str | None:
    tokens = normalize_tokens(text)
    if not tokens:
        return None
    if tokens[0] in {"帮助", "help", "/help"}:
        return "help"
    if tokens[0] in FEEDBACK_COMMANDS:
        return "feedback"
    if tokens[0] in {"当前设置", "设置?", "配置?", "status"} or (
        tokens[0] in {"当前", "查看"} and len(tokens) > 1 and tokens[1] in {"设置", "配置"}
    ):
        return "show"
    if tokens[0] not in {"设置", "配置", "set"}:
        return None

    side = None
    level = None
    coordinate_style = None
    for token in tokens[1:]:
        lowered = token.lower()
        if lowered in SIDE_ALIASES:
            side = SIDE_ALIASES[lowered]
        elif lowered in LEVEL_ALIASES:
            level = LEVEL_ALIASES[lowered]
        elif lowered in {"gtp", "标准", "跳过i", "跳过I".lower()}:
            coordinate_style = "gtp"
        elif lowered in {"sequential", "连续", "包含i", "包含I".lower()}:
            coordinate_style = "sequential"

    if side is None and level is None and coordinate_style is None:
        return None
    return SettingsPatch(side_to_move=side, level=level, coordinate_style=coordinate_style)


def normalize_tokens(text: str) -> list[str]:
    cleaned = (
        text.replace("，", " ")
        .replace(",", " ")
        .replace("：", " ")
        .replace(":", " ")
        .replace("\n", " ")
        .strip()
    )
    parts = [item for item in cleaned.split() if item]
    normalized = []
    for item in parts:
        if item.startswith("@") and len(item) > 1:
            continue
        normalized.append(item)
    return normalized


def looks_like_setting_attempt(text: str) -> bool:
    tokens = normalize_tokens(text)
    return bool(tokens and tokens[0] in {"设置", "配置", "set"})


def safe_filename(value: str) -> str:
    cleaned = "".join(char if char.isalnum() or char in {"-", "_", "."} else "_" for char in value)
    return cleaned or "unknown"


def iso_timestamp(timestamp: float) -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime(timestamp))


def help_text(settings: ChatSettings) -> str:
    return (
        f"当前设置：{settings.label()}\n"
        "我不会用 LLM 猜你的意图，只识别明确指令。\n"
        "先发一次设置，例如：设置 黑 中级，或 设置 白 特级。\n"
        "强度四档：初级 100 visits，中级 200，高级 300，特级 400。\n"
        "之后直接发棋盘照片，我会按当前设置推荐下一手。\n"
        "如果发现识别或推荐图不对，发送“上报”保存最近一次分析样本。\n"
        "查看配置：当前设置。\n"
        "获取帮助：帮助。"
    )


def unsupported_text() -> str:
    return (
        "我没有理解这条消息。这个机器人不使用 LLM 自由对话，只识别明确指令。\n"
        "发送“帮助”查看用法，或发送“当前设置”查看配置。"
    )


def format_elapsed(seconds: float) -> str:
    if seconds < 10:
        return f"{seconds:.1f}秒"
    return f"{round(seconds)}秒"


def format_analysis_text(
    result: dict[str, Any],
    settings: ChatSettings,
    elapsed_seconds: float | None = None,
) -> str:
    rec = result.get("recommendation") or {}
    reason = result.get("reason") or {}
    move = rec.get("move") or "未知"
    winrate = rec.get("winrate")
    score_lead = rec.get("scoreLead")
    visits = rec.get("visits")
    bits = [f"推荐：{SIDE_LABEL[settings.side_to_move]}走 {move}"]
    bits.append(f"设置：{settings.label()}")
    if elapsed_seconds is not None:
        bits.append(f"耗时：{format_elapsed(elapsed_seconds)}")
    timings = result.get("timings") or {}
    if timings:
        bits.append(
            "耗时明细："
            f"下载 {format_elapsed(float(timings.get('download_seconds', 0)))}，"
            f"识别/出图 {format_elapsed(float(timings.get('recognition_and_render_seconds', 0)))}，"
            f"KataGo {format_elapsed(float(timings.get('katago_seconds', 0)))}"
        )
    visits_requested = result.get("visits_requested")
    if visits_requested is not None:
        bits.append(f"搜索预算：{visits_requested}")
    if visits is not None:
        bits.append(f"访问数：{visits}")
    if winrate is not None:
        bits.append(f"胜率：{float(winrate) * 100:.1f}%")
    if score_lead is not None:
        bits.append(f"目差：{float(score_lead):+.1f}")
    summary = reason.get("summary")
    if summary:
        bits.append(str(summary))
    return "\n".join(bits)


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if key and key not in os.environ:
            os.environ[key] = value


def parse_args() -> BotConfig:
    load_env_file(DEFAULT_ENV_PATH)
    parser = argparse.ArgumentParser(description="Run a Feishu image bot for Go Next Move.")
    parser.add_argument("--app-id", default=os.getenv("FEISHU_APP_ID"), help="Feishu app id")
    parser.add_argument("--app-secret", default=os.getenv("FEISHU_APP_SECRET"), help="Feishu app secret")
    parser.add_argument("--settings-path", type=Path, default=DEFAULT_SETTINGS_PATH)
    parser.add_argument("--processed-path", type=Path, default=DEFAULT_PROCESSED_PATH)
    parser.add_argument("--side-to-move", choices=["black", "white"], default="black")
    parser.add_argument("--level", choices=["beginner", "intermediate", "advanced", "expert"], default="intermediate")
    parser.add_argument("--coordinate-style", choices=["gtp", "sequential"], default="gtp")
    parser.add_argument("--visits", type=int, default=400)
    parser.add_argument("--top-candidates", type=int, default=20)
    parser.add_argument("--katago", default=os.getenv("KATAGO_PATH") or os.getenv("KATAGO") or "katago")
    parser.add_argument("--model", default=os.getenv("KATAGO_MODEL"))
    parser.add_argument("--analysis-config", default=os.getenv("KATAGO_ANALYSIS_CONFIG"))
    parser.add_argument("--skill-config", default=os.getenv("KATAGO_SKILL_CONFIG"))
    feedback_dir = os.getenv("FEISHU_FEEDBACK_DIR")
    parser.add_argument("--feedback-dir", type=Path, default=Path(feedback_dir) if feedback_dir else None)
    parser.add_argument("--debug", action="store_true", help="Enable verbose bot logs")
    args = parser.parse_args()

    if not args.app_id or not args.app_secret:
        raise SystemExit("Set FEISHU_APP_ID and FEISHU_APP_SECRET, or pass --app-id/--app-secret.")
    if args.visits < 1:
        raise SystemExit("--visits must be at least 1")
    if args.top_candidates < 1:
        raise SystemExit("--top-candidates must be at least 1")
    return BotConfig(
        app_id=args.app_id,
        app_secret=args.app_secret,
        settings_path=args.settings_path,
        default_settings=ChatSettings(args.side_to_move, args.level, args.coordinate_style),
        visits=args.visits,
        katago=args.katago,
        model=args.model,
        analysis_config=args.analysis_config,
        skill_config=args.skill_config,
        top_candidates=args.top_candidates,
        processed_path=args.processed_path,
        feedback_dir=args.feedback_dir,
        debug=args.debug,
    )


def main() -> int:
    config = parse_args()
    bot = GoNextMoveFeishuBot(config)
    sys.stderr.write("[feishu] starting official lark-oapi long-connection bot\n")
    bot.start()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
