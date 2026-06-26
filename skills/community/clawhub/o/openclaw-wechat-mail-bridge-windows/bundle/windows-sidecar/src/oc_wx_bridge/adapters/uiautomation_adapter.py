from __future__ import annotations

import base64
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import io
import logging
import os
import re
import shutil
import time
from typing import Callable

import requests

from .base import ChatTarget
from ..config import VisualConfig
from ..models import AdapterHealth, IncomingMessage

LOGGER = logging.getLogger(__name__)
_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_CHINESE_TRIGGER_RE = re.compile(r"(查邮箱|监控|邮箱|邮件)")
_SLASH_TRIGGER_RE = re.compile(r"^/(mail|watch|mail-watch|mail-last|mail-health|mail-bind|mail-flush)\b", re.IGNORECASE)

_NOISE_TEXTS = {
    "微信",
    "weixin",
    "wechat",
    "wechat current chat",
}


def _is_noise_text(text: str) -> bool:
    normalized = text.strip().lower()
    if not normalized:
        return True
    if normalized in _NOISE_TEXTS:
        return True
    if len(normalized) <= 1:
        return True
    return False


def _looks_like_message(text: str) -> bool:
    normalized = text.strip()
    if _is_noise_text(normalized):
        return False
    if len(normalized) < 2:
        return False

    compact = normalized.replace(" ", "")
    if compact.lower().startswith("/mail") or normalized.startswith("/"):
        return True
    if _EMAIL_RE.search(normalized):
        return True
    if any("\u4e00" <= char <= "\u9fff" for char in normalized):
        return len(normalized) >= 3
    if "http" in normalized.lower():
        return True
    return False


def _coerce_command_text(text: str) -> str:
    candidate = text.strip()
    candidate = re.sub(r"^/\s*mail\b", "/mail", candidate, flags=re.IGNORECASE)
    candidate = re.sub(r"\s+", " ", candidate).strip()
    return candidate


def _cleanup_lines(raw_text: str, max_chars: int) -> list[str]:
    lines: list[str] = []
    for line in raw_text.replace("\r", "\n").split("\n"):
        cleaned = line.strip().strip("`")
        if not cleaned:
            continue
        lower = cleaned.lower()
        if lower in {"json", "text", "markdown"}:
            continue
        if ":" in cleaned and len(cleaned.split(":", 1)[0]) <= 20:
            prefix, suffix = cleaned.split(":", 1)
            if prefix.strip().lower() in {"message", "latest", "latest message", "text"}:
                cleaned = suffix.strip()
        cleaned = cleaned[:max_chars]
        if cleaned:
            lines.append(cleaned)
    return lines


def _pick_latest_message(candidates: list[str]) -> str | None:
    if not candidates:
        return None

    for candidate in reversed(candidates):
        normalized = _coerce_command_text(candidate)
        compact = normalized.replace(" ", "")
        if compact.lower().startswith("/mail") or normalized.startswith("/"):
            return normalized

    for candidate in reversed(candidates):
        normalized = _coerce_command_text(candidate)
        if _looks_like_message(normalized):
            return normalized

    return None


def _looks_like_low_confidence_ocr(text: str) -> bool:
    normalized = _coerce_command_text(text)
    if not normalized:
        return True
    if _is_noise_text(normalized):
        return True

    if normalized.startswith("/"):
        if _SLASH_TRIGGER_RE.search(normalized):
            if normalized.lower().startswith("/mail") and not _EMAIL_RE.search(normalized):
                return True
            return False
        return True

    if _CHINESE_TRIGGER_RE.search(normalized):
        return not _EMAIL_RE.search(normalized)

    if _EMAIL_RE.search(normalized):
        return True

    if "@" in normalized:
        return True

    if normalized.endswith("."):
        return True

    asciiish = [
        char
        for char in normalized
        if not char.isspace()
    ]
    if not asciiish:
        return True
    accepted = sum(
        1
        for char in asciiish
        if char.isalnum() or char in "/@._%+-:#()[]{}<>?=&" or ("\u4e00" <= char <= "\u9fff")
    )
    return accepted / len(asciiish) < 0.85


def _resolve_tesseract_cmd() -> str | None:
    discovered = shutil.which("tesseract")
    if discovered:
        return discovered
    if os.name != "nt":
        return None

    candidates = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    ]
    for candidate in candidates:
        if os.path.isfile(candidate):
            return candidate
    return None


def _collect_named_nodes(window: object) -> list[str]:
    try:
        root_children = window.GetChildren()  # type: ignore[attr-defined]
    except Exception:
        return []

    queue = list(root_children)
    names: list[str] = []
    visited = 0
    max_nodes = 1200
    while queue and visited < max_nodes:
        node = queue.pop(0)
        visited += 1
        try:
            name = (node.Name or "").strip()  # type: ignore[attr-defined]
        except Exception:
            name = ""
        if name:
            names.append(name)
        try:
            children = node.GetChildren()  # type: ignore[attr-defined]
        except Exception:
            children = []
        if children:
            queue.extend(children)
    return names


@dataclass
class UIAutomationAdapter:
    sidecar_id: str
    watch_poll_interval_sec: float
    visual_config: VisualConfig
    default_chat_name: str = "WeChat Current Chat"
    _last_sent_text: str = ""
    _last_sent_at: float = 0.0

    def health(self) -> AdapterHealth:
        try:
            import uiautomation as auto  # type: ignore

            wechat_window = auto.WindowControl(searchDepth=1, Name="微信")
            if wechat_window.Exists(0, 0):
                return AdapterHealth(ok=True, name="uiautomation", detail="wechat window found")
            return AdapterHealth(ok=False, name="uiautomation", detail="wechat window not found")
        except Exception as error:
            return AdapterHealth(ok=False, name="uiautomation", detail=f"uiautomation not ready: {error}")

    def list_groups(self) -> list[ChatTarget]:
        try:
            import uiautomation as auto  # type: ignore

            wechat_window = auto.WindowControl(searchDepth=1, Name="微信")
            if not wechat_window.Exists(0, 0):
                return []
            candidates: list[ChatTarget] = []
            seen: set[str] = set()
            for child in wechat_window.GetChildren():
                name = (child.Name or "").strip()
                if not name or len(name) > 80:
                    continue
                if name in seen:
                    continue
                seen.add(name)
                candidates.append(ChatTarget(chat_id=name, chat_name=name))
                if len(candidates) >= 100:
                    break
            return candidates
        except Exception as error:
            LOGGER.warning("uiautomation list_groups failed error=%s", error)
            return []

    def _capture_chat_region(self, wechat_window: object) -> object | None:
        try:
            from PIL import ImageGrab  # type: ignore
        except Exception as error:
            LOGGER.debug("visual capture disabled (Pillow missing) error=%s", error)
            return None

        try:
            rect = getattr(wechat_window, "BoundingRectangle", None)
            if rect is None:
                return None
            left = int(getattr(rect, "left", getattr(rect, "Left", 0)))
            top = int(getattr(rect, "top", getattr(rect, "Top", 0)))
            right = int(getattr(rect, "right", getattr(rect, "Right", 0)))
            bottom = int(getattr(rect, "bottom", getattr(rect, "Bottom", 0)))
            if right <= left or bottom <= top:
                return None

            width = right - left
            height = bottom - top
            crop = (
                left + int(width * 0.30),
                top + int(height * 0.15),
                right - int(width * 0.03),
                bottom - int(height * 0.12),
            )
            return ImageGrab.grab(bbox=crop, all_screens=True)
        except Exception as error:
            LOGGER.debug("visual capture failed error=%s", error)
            return None

    def _extract_with_ocr(self, image: object) -> str | None:
        try:
            from PIL import ImageOps  # type: ignore
            import pytesseract  # type: ignore
        except Exception as error:
            LOGGER.debug("ocr dependencies unavailable error=%s", error)
            return None

        try:
            tesseract_cmd = _resolve_tesseract_cmd()
            if not tesseract_cmd:
                LOGGER.debug("ocr unavailable: tesseract executable not found")
                return None
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
            gray = ImageOps.grayscale(image)
            raw = pytesseract.image_to_string(
                gray,
                lang=self.visual_config.ocr_lang,
                config="--psm 6",
            )
            if not raw:
                return None
            return raw[: max(60, self.visual_config.ocr_max_chars * 3)]
        except Exception as error:
            LOGGER.debug("ocr extract failed error=%s", error)
            return None

    def _image_to_base64(self, image: object) -> str:
        max_side = 1200
        image_copy = image.copy()
        width = getattr(image_copy, "width", 0)
        height = getattr(image_copy, "height", 0)
        if width > max_side or height > max_side:
            image_copy.thumbnail((max_side, max_side))
        buffer = io.BytesIO()
        image_copy.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode("ascii")

    def _extract_with_vlm(self, image: object) -> str | None:
        base_url = self.visual_config.vlm_base_url
        api_key = (self.visual_config.vlm_api_key or "").strip()
        if "api.openai.com" in base_url and not api_key:
            return None

        try:
            image_b64 = self._image_to_base64(image)
            payload = {
                "model": self.visual_config.vlm_model,
                "temperature": 0,
                "max_tokens": 100,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Extract only the latest user-authored WeChat message text from the screenshot. "
                            "Prefer the newest actionable command such as /mail, /watch, 查邮箱, or a visible email query. "
                            "Ignore timestamps, chat chrome, previous automation replies, and decorative labels. "
                            "If unreadable, return an empty string."
                        ),
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": (
                                    "Return only the exact raw latest message text, no JSON. "
                                    "If a /mail or /watch command is visible, preserve it verbatim including the email."
                                ),
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/png;base64,{image_b64}"},
                            },
                        ],
                    },
                ],
            }
            headers = {"Content-Type": "application/json"}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"

            response = requests.post(
                f"{base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=12,
            )
            response.raise_for_status()
            data = response.json()
            choices = data.get("choices", [])
            if not choices:
                return None
            content = choices[0].get("message", {}).get("content", "")
            if isinstance(content, list):
                parts: list[str] = []
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        parts.append(str(item.get("text", "")))
                content = "\n".join(parts)
            normalized = str(content).strip()
            return normalized if normalized else None
        except Exception as error:
            LOGGER.debug("vlm extract failed error=%s", error)
            return None

    def _extract_visual_message(self, wechat_window: object) -> str | None:
        if not self.visual_config.enabled or self.visual_config.mode == "off":
            return None

        image = self._capture_chat_region(wechat_window)
        if image is None:
            return None

        mode = self.visual_config.mode
        ocr_candidate: str | None = None
        if mode in {"ocr", "auto"}:
            ocr_raw = self._extract_with_ocr(image)
            if ocr_raw:
                ocr_lines = _cleanup_lines(ocr_raw, self.visual_config.ocr_max_chars)
                picked = _pick_latest_message(ocr_lines)
                if picked:
                    if mode == "ocr":
                        return picked
                    ocr_candidate = picked
                    if not _looks_like_low_confidence_ocr(picked):
                        return picked
                    LOGGER.info("ocr candidate looks low confidence, trying vlm fallback candidate=%s", picked)

        if mode in {"vlm", "auto"}:
            vlm_raw = self._extract_with_vlm(image)
            if vlm_raw:
                vlm_lines = _cleanup_lines(vlm_raw, self.visual_config.ocr_max_chars)
                picked = _pick_latest_message(vlm_lines)
                if picked:
                    return picked
        return ocr_candidate

    def _extract_uia_tree_message(self, wechat_window: object) -> str | None:
        names = _collect_named_nodes(wechat_window)
        if not names:
            return None
        filtered = [item for item in names if not _is_noise_text(item)]
        return _pick_latest_message(filtered)

    def _focus_input_area(self, wechat_window: object) -> None:
        try:
            import uiautomation as auto  # type: ignore

            rect = getattr(wechat_window, "BoundingRectangle", None)
            if rect is None:
                return
            left = int(getattr(rect, "left", getattr(rect, "Left", 0)))
            top = int(getattr(rect, "top", getattr(rect, "Top", 0)))
            right = int(getattr(rect, "right", getattr(rect, "Right", 0)))
            bottom = int(getattr(rect, "bottom", getattr(rect, "Bottom", 0)))
            if right <= left or bottom <= top:
                return

            width = right - left
            height = bottom - top
            auto.Click(left + int(width * 0.68), top + int(height * 0.93), waitTime=0.1)
        except Exception as error:
            LOGGER.debug("focus input area failed error=%s", error)

    def watch(self, handler: Callable[[IncomingMessage], None]) -> None:
        LOGGER.info("uiautomation watch loop started")
        last_fingerprint = ""
        last_visual_probe = 0.0
        try:
            import uiautomation as auto  # type: ignore

            with auto.UIAutomationInitializerInThread():
                while True:
                    try:
                        import uuid

                        wechat_window = auto.WindowControl(searchDepth=1, Name="微信")
                        if wechat_window.Exists(0, 0):
                            latest = self._extract_uia_tree_message(wechat_window)
                            now = time.time()
                            if (
                                not latest
                                and self.visual_config.enabled
                                and self.visual_config.mode != "off"
                                and (now - last_visual_probe) >= self.visual_config.sample_interval_sec
                            ):
                                latest = self._extract_visual_message(wechat_window)
                                last_visual_probe = now

                            if latest and latest != last_fingerprint:
                                if latest == self._last_sent_text and (now - self._last_sent_at) < 4:
                                    last_fingerprint = latest
                                    continue
                                ts = datetime.now(timezone.utc).isoformat()
                                message_id = f"uia_{hashlib.sha1(f'{latest}|{ts}'.encode('utf-8')).hexdigest()[:20]}"
                                handler(
                                    IncomingMessage(
                                        event_id=f"evt_{uuid.uuid4().hex}",
                                        sidecar_id=self.sidecar_id,
                                        chat_id=self.default_chat_name,
                                        chat_name=self.default_chat_name,
                                        sender_display_name="unknown",
                                        message_id=message_id,
                                        message_text=latest,
                                        message_time=ts,
                                        observed_at=ts,
                                    )
                                )
                                last_fingerprint = latest
                    except Exception as error:
                        LOGGER.debug("uiautomation watch tick failed error=%s", error)
                    time.sleep(max(0.2, self.watch_poll_interval_sec))
        except Exception as error:
            LOGGER.warning("uiautomation watch loop stopped error=%s", error)

    def send_text(self, chat_id: str, text: str) -> None:
        try:
            import uiautomation as auto  # type: ignore

            wechat_window = auto.WindowControl(searchDepth=1, Name="微信")
            if not wechat_window.Exists(0, 0):
                raise RuntimeError("wechat window not found")

            wechat_window.SetActive()
            wechat_window.SendKeys("{Ctrl}f", waitTime=0.1)
            wechat_window.SendKeys(chat_id, waitTime=0.1)
            wechat_window.SendKeys("{Enter}", waitTime=0.1)
            time.sleep(0.2)
            self._focus_input_area(wechat_window)
            time.sleep(0.1)
            wechat_window.SendKeys(text, waitTime=0.1)
            wechat_window.SendKeys("{Enter}", waitTime=0.1)
            self._last_sent_text = text
            self._last_sent_at = time.time()
            LOGGER.info("uiautomation send attempted chat_id=%s", chat_id)
        except Exception as error:
            raise RuntimeError(f"uiautomation send_text failed: {error}") from error
