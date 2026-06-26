"""Dialogue pipeline mixin — wake-word handler and command stages."""

import re
import time
from dataclasses import dataclass
from typing import Optional, Dict, Any

from kiwi.state_machine import DialogueState
from kiwi.text_processing import quick_completeness_check, detect_emotion
from kiwi.utils import kiwi_log
from kiwi.i18n import t

try:
    from kiwi.event_bus import EventType, get_event_bus
    EVENT_BUS_AVAILABLE = True
except ImportError:
    EVENT_BUS_AVAILABLE = False


@dataclass
class CommandContext:
    """Per-invocation state carried between pipeline stages in _on_wake_word."""
    command: str
    command_lower: str = ""
    timestamp: float = 0.0
    speaker_id: str = "unknown"
    speaker_name: str = ""
    speaker_confidence: float = 0.0
    speaker_music_prob: float = 0.0
    is_owner: bool = False
    owner_profile_ready: bool = False
    approved_command_from_owner: Optional[str] = None
    abort: bool = False

    def __post_init__(self):
        if not self.speaker_name:
            self.speaker_name = t("responses.unknown_speaker")


class DialoguePipelineMixin:
    """Wake-word pipeline stages and speaker/security helpers."""

    # ------------------------------------------------------------------
    # Wake-word entry point
    # ------------------------------------------------------------------

    def _on_wake_word(self, command: str):
        """
        Wake word handler — pipeline orchestrator.
        Each stage receives a CommandContext and may set ctx.abort = True to stop.
        """
        ctx = CommandContext(command=command)
        for stage in [
            self._stage_init_and_dedup,
            self._stage_resolve_speaker,
            self._stage_check_approval,
            self._stage_handle_special_commands,
            self._stage_handle_stop_cancel,
            self._stage_completeness_check,
            self._stage_owner_approval_gate,
            self._stage_homeassistant_routing,
            self._stage_dispatch_to_llm,
        ]:
            stage(ctx)
            if ctx.abort:
                return

    # ------------------------------------------------------------------
    # Pipeline stages
    # ------------------------------------------------------------------

    def _stage_init_and_dedup(self, ctx: CommandContext) -> None:
        """Set PROCESSING, reject duplicates, extend dialog timeout."""
        self._set_state(DialogueState.PROCESSING)

        kiwi_log("KIWI", f"Услышала: {ctx.command}", level="INFO")

        ctx.timestamp = time.time()
        if ctx.command == self._last_command and (ctx.timestamp - self._last_command_time) < self._command_cooldown:
            kiwi_log("DEDUP", f"Ignoring duplicate command within {self._command_cooldown}s", level="INFO")
            self._set_state(DialogueState.IDLE)
            ctx.abort = True
            return

        self._last_command = ctx.command
        self._last_command_time = ctx.timestamp

        if self.listener.dialog_mode:
            self.listener.dialog_until = time.time() + self.listener.dialog_timeout
            kiwi_log("DIALOG", "Extended timeout for processing", level="INFO")

        ctx.command_lower = ctx.command.lower().strip()

    def _stage_resolve_speaker(self, ctx: CommandContext) -> None:
        """Get speaker meta, log, show owner warning once."""
        speaker_meta = self._get_current_speaker_meta()
        ctx.speaker_id = str(speaker_meta.get("speaker_id", "unknown"))
        ctx.speaker_name = str(speaker_meta.get("speaker_name", t("responses.unknown_speaker")))
        ctx.speaker_confidence = float(speaker_meta.get("confidence", 0.0))
        ctx.speaker_music_prob = float(speaker_meta.get("music_probability", 0.0))
        ctx.is_owner = self._is_owner_speaker(speaker_meta)
        ctx.owner_profile_ready = self._owner_profile_registered()

        kiwi_log(
            "SPEAKER",
            f"command from {ctx.speaker_name} ({ctx.speaker_id}), "
            f"owner={ctx.is_owner}, conf={ctx.speaker_confidence:.2f}, music={ctx.speaker_music_prob:.2f}",
            level="INFO",
        )

        # Publish speaker identified event for external consumers
        if EVENT_BUS_AVAILABLE:
            try:
                get_event_bus().publish(EventType.SPEAKER_IDENTIFIED,
                    {'speaker_id': ctx.speaker_id, 'speaker_name': ctx.speaker_name,
                     'priority': int(speaker_meta.get("priority", 2)),
                     'confidence': ctx.speaker_confidence,
                     'is_owner': ctx.is_owner},
                    source='dialogue_pipeline')
            except Exception:
                pass

        if not ctx.owner_profile_ready and not self._owner_profile_warning_shown:
            kiwi_log(
                "APPROVAL",
                f"Owner profile '{self._owner_id}' is not registered yet. "
                f"Using name-based fallback approval; voice enrollment is recommended.",
                level="WARNING",
            )
            self._owner_profile_warning_shown = True

    def _stage_check_approval(self, ctx: CommandContext) -> None:
        """Expire stale approvals, handle owner yes/no (both voice and exec approvals)."""
        # --- OpenClaw exec approval (post-filter) ---
        if self._pending_exec_approval and ctx.is_owner:
            if self._approval_yes(ctx.command_lower):
                kiwi_log("EXEC-APPROVAL", "Approved by owner via voice", level="INFO")
                self.resolve_pending_exec_approval(True)
                ctx.abort = True
                return
            elif self._approval_no(ctx.command_lower):
                kiwi_log("EXEC-APPROVAL", "Denied by owner via voice", level="INFO")
                self.resolve_pending_exec_approval(False)
                ctx.abort = True
                return

        # --- Kiwi voice approval (pre-filter) ---
        if self._pending_owner_approval:
            age = time.time() - float(self._pending_owner_approval.get("timestamp", 0.0))
            if age > self._owner_approval_timeout:
                kiwi_log("APPROVAL", f"Pending request expired ({age:.1f}s)", level="INFO")
                self._pending_owner_approval = None

        if self._pending_owner_approval and ctx.is_owner:
            if self._approval_yes(ctx.command_lower):
                ctx.approved_command_from_owner = str(self._pending_owner_approval.get("command", "")).strip()
                requester = str(self._pending_owner_approval.get("speaker_name", t("responses.unknown_speaker")))
                self._pending_owner_approval = None
                if ctx.approved_command_from_owner:
                    kiwi_log("APPROVAL", f"Approved by owner. Running deferred command from {requester}", level="INFO")
                    self.speak(t("responses.approval_accepted", requester=requester), style="confident")
                    ctx.command = ctx.approved_command_from_owner
                    ctx.command_lower = ctx.command.lower().strip()
            elif self._approval_no(ctx.command_lower):
                requester = str(self._pending_owner_approval.get("speaker_name", t("responses.unknown_speaker")))
                self._pending_owner_approval = None
                kiwi_log("APPROVAL", f"Denied by owner. Requester={requester}", level="INFO")
                self.speak(t("responses.approval_denied", requester=requester), style="calm")
                ctx.abort = True

    def _stage_handle_special_commands(self, ctx: CommandContext) -> None:
        """Reset context, calibrate, voice profile, and soul switching commands."""
        calibrate_words = ['калибровка', 'калибруй', 'перекалибруй', 'обнови профиль']
        reset_prompt_words = ['сбрось контекст', 'новый разговор', 'забудь', 'сбрось системный промпт']

        # Soul switching commands
        if self._soul_manager:
            command_lower = ctx.command_lower

            # "switch to storyteller" / "переключись на рассказчика" etc.
            soul_switch_patterns = t("commands.soul_switch_patterns")
            if isinstance(soul_switch_patterns, list):
                for pattern in soul_switch_patterns:
                    if pattern in command_lower:
                        # Extract soul name after the pattern
                        rest = command_lower.split(pattern, 1)[-1].strip()
                        if rest:
                            soul_id = self._soul_manager.find_soul_by_name(rest)
                            if soul_id:
                                self._soul_manager.switch_soul(soul_id)
                                self._apply_soul_session()
                                soul = self._soul_manager.get_soul(soul_id)
                                self.speak(t("responses.soul_switched", name=soul.name), style="cheerful")
                                ctx.abort = True
                                return
                            else:
                                self.speak(t("responses.soul_not_found"), style="neutral")
                                ctx.abort = True
                                return

            # "nsfw mode" / "режим 18+" / "adult mode"
            nsfw_patterns = t("commands.nsfw_enable_patterns")
            if isinstance(nsfw_patterns, list) and any(p in command_lower for p in nsfw_patterns):
                self._soul_manager.switch_soul("nsfw")
                self._apply_soul_session()
                self.speak(t("responses.nsfw_enabled"), style="neutral")
                ctx.abort = True
                return

            # "default mode" / "обычный режим" / "disable nsfw"
            default_patterns = t("commands.default_mode_patterns")
            if isinstance(default_patterns, list) and any(p in command_lower for p in default_patterns):
                self._soul_manager.switch_to_default()
                self._apply_soul_session()
                self.speak(t("responses.soul_reset"), style="cheerful")
                ctx.abort = True
                return

            # "what modes" / "какие режимы" / "list souls"
            list_patterns = t("commands.soul_list_patterns")
            if isinstance(list_patterns, list) and any(p in command_lower for p in list_patterns):
                souls = self._soul_manager.list_souls()
                names = ", ".join(s.name for s in souls if not s.nsfw)
                active = self._soul_manager.get_active_soul()
                active_name = active.name if active else "none"
                self.speak(t("responses.soul_list", names=names, active=active_name), style="neutral")
                ctx.abort = True
                return

        if any(word in ctx.command_lower for word in reset_prompt_words):
            kiwi_log("KIWI", "Resetting system prompt...", level="INFO")
            self._system_prompt_sent = False
            self.speak(t("responses.context_cleared"), style="neutral")
            ctx.abort = True
            return

        if any(word in ctx.command_lower for word in calibrate_words):
            kiwi_log("KIWI", "Speaker ID calibration requested", level="INFO")
            self._self_profile_created = False
            self.speak(t("responses.calibrating"), style="neutral")
            ctx.abort = True
            return

        # Voice profile commands
        owner_register_words = [
            "запомни мой голос",
            "зарегистрируй мой голос",
            "я хозяин",
        ]
        _on = self._owner_name.lower()
        if _on and _on != "owner":
            owner_register_words.extend([f"это {_on}", f"я {_on}"])
        if any(word in ctx.command_lower for word in owner_register_words):
            if ctx.owner_profile_ready and not ctx.is_owner:
                kiwi_log("SECURITY", f"Non-owner '{ctx.speaker_name}' attempted owner registration — DENIED", level="WARNING")
                self._notify_owner_security_event(
                    t("responses.owner_reregistration_attempt", speaker=ctx.speaker_name, command=ctx.command)
                )
                self.speak(t("responses.owner_already_registered"), style="calm")
                ctx.abort = True
                return
            if hasattr(self.listener, "register_owner_voice"):
                success = self.listener.register_owner_voice(self._owner_name)
                if success:
                    self.speak(t("responses.owner_registered", name=self._owner_name), style="cheerful")
                else:
                    self.speak(t("responses.owner_register_failed"), style="calm")
            else:
                self.speak(t("responses.profiles_unavailable"), style="calm")
            ctx.abort = True
            return

        if "кто говорит" in ctx.command_lower or "кто это говорит" in ctx.command_lower:
            if hasattr(self.listener, "describe_last_speaker"):
                self.speak(self.listener.describe_last_speaker(), style="neutral")
            else:
                self.speak(t("responses.cannot_identify"), style="calm")
            ctx.abort = True
            return

        if "какие голоса" in ctx.command_lower or "список голосов" in ctx.command_lower:
            if hasattr(self.listener, "describe_known_voices"):
                self.speak(self.listener.describe_known_voices(), style="neutral")
            else:
                self.speak(t("responses.voice_list_unavailable"), style="calm")
            ctx.abort = True
            return

        if "запомни меня как" in ctx.command_lower or "это мой друг" in ctx.command_lower:
            if ctx.owner_profile_ready and not ctx.is_owner:
                kiwi_log("SECURITY", f"Non-owner '{ctx.speaker_name}' attempted to add friend — DENIED", level="WARNING")
                self.speak(t("responses.only_owner_can_add"), style="calm")
                ctx.abort = True
                return
            name = self._extract_name_from_voice_command(ctx.command)
            if not name:
                self.speak(t("responses.say_name_prompt"), style="neutral")
                ctx.abort = True
                return
            if hasattr(self.listener, "remember_last_voice_as"):
                success, _sid = self.listener.remember_last_voice_as(name)
                if success:
                    self.speak(t("responses.voice_remembered", name=name), style="cheerful")
                else:
                    self.speak(t("responses.voice_save_failed"), style="calm")
            else:
                self.speak(t("responses.profiles_unavailable"), style="calm")
            ctx.abort = True
            return

    def _stage_handle_stop_cancel(self, ctx: CommandContext) -> None:
        """Stop TTS + barge-in, cancel OpenClaw."""
        stop_words = ['стоп', 'отмена', 'хватит', 'прекрати', 'остановись', 'стой', 'cancel', 'stop']
        if not any(word in ctx.command_lower for word in stop_words):
            return

        kiwi_log("KIWI", "Получена команда отмены!", level="INFO")

        tts_was_active = self.is_speaking() or self._is_streaming or self._streaming_tts_manager is not None
        # Barge-in already stopped TTS before Whisper finished transcribing "stop"
        barge_in_already_stopped = self._barge_in_requested and not tts_was_active
        openclaw_was_processing = self.openclaw.is_processing()

        if tts_was_active:
            self.request_barge_in()
            self._streaming_stop_event.set()
            self._stop_stream_watchdog()
            if self._streaming_tts_manager:
                self._streaming_tts_manager.stop(graceful=False)
                self._streaming_tts_manager = None

        cancelled = self.openclaw.cancel() if openclaw_was_processing else False

        if tts_was_active or barge_in_already_stopped:
            self._is_streaming = False
            self._barge_in_requested = False
            self.listener.activate_dialog_mode()
            self._set_state(DialogueState.LISTENING)
            self._start_idle_timer()
            ctx.abort = True
            return

        if cancelled:
            self.speak(t("responses.stopped"), style="calm")
        else:
            self.speak(t("responses.nothing_to_stop"), style="neutral")
        ctx.abort = True

    def _stage_completeness_check(self, ctx: CommandContext) -> None:
        """Combine pending phrase, check completeness."""
        combined_text = ctx.command
        if self._pending_phrase:
            elapsed = time.time() - self._pending_timestamp
            if elapsed < self._pending_timeout:
                combined_text = f"{self._pending_phrase} {ctx.command}".strip()
                kiwi_log("KIWI", f"Combined with pending: '{self._pending_phrase}' + '{ctx.command}' → '{combined_text}'", level="INFO")
            else:
                kiwi_log("KIWI", f"Pending phrase expired ({elapsed:.1f}s)", level="INFO")
                self._pending_phrase = ""

        quick_complete = quick_completeness_check(combined_text)
        if quick_complete:
            kiwi_log("COMPLETE-CHECK", "Quick check: COMPLETE", level="INFO")
        else:
            kiwi_log("COMPLETE-CHECK", "Quick check: INCOMPLETE - waiting for more", level="INFO")
            self._pending_phrase = combined_text
            self._pending_timestamp = time.time()
            if self.listener.dialog_mode:
                self.listener.dialog_until = time.time() + self._pending_timeout
                kiwi_log("DIALOG", f"Extended timeout for pending phrase ({self._pending_timeout}s)", level="INFO")
            ctx.abort = True
            return

        self._pending_phrase = ""
        ctx.command = combined_text
        ctx.command_lower = ctx.command.lower().strip()

    def _stage_owner_approval_gate(self, ctx: CommandContext) -> None:
        """Defer non-owner actionable tasks."""
        if (
            not ctx.approved_command_from_owner
            and not ctx.is_owner
            and self._looks_like_actionable_task(ctx.command_lower)
            and not self._is_small_talk_or_safe_request(ctx.command_lower)
        ):
            self._pending_owner_approval = {
                "command": ctx.command,
                "speaker_id": ctx.speaker_id,
                "speaker_name": ctx.speaker_name,
                "timestamp": time.time(),
            }
            kiwi_log("APPROVAL", f"Pending owner approval for speaker={ctx.speaker_name}, command='{ctx.command}'", level="INFO")

            # Send Telegram approval request if configured
            voice_security = getattr(self, '_voice_security', None)
            telegram_available = voice_security and voice_security.telegram.is_configured()
            if telegram_available:
                voice_security.telegram.send_approval_request(
                    command=ctx.command,
                    speaker_id=ctx.speaker_id,
                    speaker_name=ctx.speaker_name,
                    callback=self._on_telegram_approval_decision,
                )
                kiwi_log("APPROVAL", "Telegram approval request sent", level="INFO")

            # Build approval hint based on available channels
            if ctx.owner_profile_ready and telegram_available:
                approve_hint = t("responses.approval_prompt_voice_and_telegram")
            elif ctx.owner_profile_ready:
                approve_hint = t("responses.approval_prompt_voice")
            elif telegram_available:
                approve_hint = t("responses.approval_prompt_telegram")
            else:
                approve_hint = t("responses.approval_prompt_register")

            self.speak(
                t("responses.approval_request",
                  owner=self._owner_name,
                  speaker=ctx.speaker_name,
                  command=ctx.command,
                  hint=approve_hint),
                style="neutral",
            )
            self.listener.activate_dialog_mode()
            self._set_state(DialogueState.LISTENING)
            ctx.abort = True

    def _stage_homeassistant_routing(self, ctx: CommandContext) -> None:
        """Route smart-home commands to Home Assistant Conversation API."""
        ha_client = getattr(self, '_ha_client', None)
        if not ha_client or not ha_client.connected:
            return

        command_lower = ctx.command_lower

        # Check if command matches any HA trigger pattern
        ha_patterns = t("commands.ha_trigger_patterns")
        if not isinstance(ha_patterns, list):
            return

        matched = any(pattern in command_lower for pattern in ha_patterns)
        if not matched:
            return

        kiwi_log("HA", f"Routing to Home Assistant: {ctx.command}", level="INFO")

        # Strip HA prefixes (e.g. "smart home turn on lights" -> "turn on lights")
        ha_command = ctx.command
        strip_prefixes = t("commands.ha_strip_prefixes")
        if isinstance(strip_prefixes, list):
            for prefix in strip_prefixes:
                if command_lower.startswith(prefix):
                    ha_command = ctx.command[len(prefix):].strip()
                    break

        if EVENT_BUS_AVAILABLE:
            try:
                get_event_bus().publish(EventType.HA_COMMAND_SENT,
                    {'command': ha_command, 'original': ctx.command},
                    source='dialogue_pipeline')
            except Exception:
                pass

        self.play_beep(async_mode=True)

        # Send to HA Conversation API (blocking call from pipeline thread)
        response = ha_client.process_command(ha_command)

        if response:
            kiwi_log("HA", f"Response: {response[:100]}", level="INFO")
            if EVENT_BUS_AVAILABLE:
                try:
                    get_event_bus().publish(EventType.HA_COMMAND_RESPONSE,
                        {'command': ha_command, 'response': response},
                        source='dialogue_pipeline')
                except Exception:
                    pass
            self.speak(response, style="confident")
        else:
            kiwi_log("HA", "No response from HA", level="WARNING")
            self.speak(t("responses.ha_no_response"), style="calm")

        ctx.abort = True

    def _stage_dispatch_to_llm(self, ctx: CommandContext) -> None:
        """Event, beep, THINKING, streaming/blocking dispatch."""
        if EVENT_BUS_AVAILABLE:
            get_event_bus().publish(
                EventType.COMMAND_RECEIVED,
                {'command': ctx.command, 'source': 'voice'},
                source='kiwi_service'
            )

        self.play_beep(async_mode=True)

        kiwi_log("KIWI", "Думаю...", level="INFO")
        self._set_state(DialogueState.THINKING)

        if self.listener.dialog_mode:
            self.listener.dialog_until = time.time() + self.config.openclaw_timeout + 10
            kiwi_log("DIALOG", f"Extended timeout for LLM response ({self.config.openclaw_timeout + 10}s)", level="INFO")

        self._streaming_style = detect_emotion(ctx.command, "")

        local_qwen_no_streaming = (
            self.tts_provider == "qwen3" and self.tts_qwen_backend == "local"
        )
        use_streaming_flow = (
            self._use_websocket
            and hasattr(self.openclaw, 'send_message')
            and not local_qwen_no_streaming
        )

        if use_streaming_flow:
            self._dispatch_streaming(ctx)
        else:
            self._dispatch_blocking(ctx, local_qwen_no_streaming)

    # ------------------------------------------------------------------
    # Dispatch helpers
    # ------------------------------------------------------------------

    def _apply_soul_session(self):
        """Apply session switch from active soul and reset prompt state."""
        self._system_prompt_sent = False
        if self._soul_manager and hasattr(self, 'openclaw') and self.openclaw:
            session = self._soul_manager.get_session_override()
            self.openclaw.switch_session(session)  # None reverts to default

    def _dispatch_streaming(self, ctx: CommandContext) -> None:
        """Streaming: launch TTS manager and send message via WebSocket."""
        kiwi_log("KIWI", "Using streaming LLM + TTS", level="INFO")
        with self._streaming_completion_lock:
            self._streaming_generation += 1
        self._streaming_response_playback_started = False

        if self.openclaw.is_processing():
            kiwi_log("KIWI", "Cancelling previous OpenClaw request", level="INFO")
            self.openclaw.cancel()
        self._start_streaming_runtime(ctx.command)

        if not self._system_prompt_sent:
            # Compose system prompt with active soul personality
            if self._soul_manager:
                system_prompt = self._soul_manager.get_system_prompt(self.config.voice_system_prompt)
            else:
                system_prompt = self.config.voice_system_prompt

            kiwi_log("KIWI", f"Sending first message with system prompt (soul: {self._soul_manager.active_soul_id if self._soul_manager else 'none'})", level="INFO")
            success = self.openclaw.send_message(
                ctx.command,
                context=system_prompt,
            )
            self._system_prompt_sent = True
        else:
            success = self.openclaw.send_message(ctx.command)

        if not success:
            kiwi_log("KIWI", "Failed to send message via WebSocket", level="ERROR")
            self._stop_stream_watchdog()
            self._streaming_tts_manager.stop(graceful=False)
            self._streaming_tts_manager = None
            self.speak(t("responses.error_send_failed"), style="calm")
            self._set_state(DialogueState.IDLE)
        else:
            self._start_stream_watchdog(ctx.command)

    def _dispatch_blocking(self, ctx: CommandContext, local_qwen_no_streaming: bool) -> None:
        """Blocking flow: CLI or WebSocket without streaming TTS."""
        self._stop_stream_watchdog()
        if self._use_websocket and hasattr(self.openclaw, "chat"):
            if local_qwen_no_streaming:
                kiwi_log("KIWI", "Streaming TTS disabled for local Qwen; using blocking final response", level="INFO")
            else:
                kiwi_log("KIWI", "Using blocking flow (WebSocket mode)", level="INFO")
        else:
            kiwi_log("KIWI", "Using classic blocking flow (CLI mode)", level="INFO")

        if not self._system_prompt_sent:
            # Compose system prompt with active soul personality
            if self._soul_manager:
                system_prompt = self._soul_manager.get_system_prompt(self.config.voice_system_prompt)
            else:
                system_prompt = self.config.voice_system_prompt
            full_command = f"{system_prompt}\n\n{ctx.command}"
            self._system_prompt_sent = True
            kiwi_log("KIWI", f"System prompt added to first message (soul: {self._soul_manager.active_soul_id if self._soul_manager else 'none'})", level="INFO")
        else:
            full_command = ctx.command

        response = self.openclaw.chat(full_command)

        if isinstance(response, list):
            response = "".join(str(r) for r in response)

        if response and response.strip().upper() == "[SILENCE]":
            kiwi_log("KIWI", "Silenced response (likely noise/incomplete)", level="INFO")
            self.listener.dialog_mode = False
            self._set_state(DialogueState.IDLE)
            return

        if response:
            kiwi_log("KIWI", f"Ответ: {response[:100]}...", level="INFO")
            style = detect_emotion(ctx.command, response)
            self.speak(response, style=style)

    # ------------------------------------------------------------------
    # Speaker / security helpers
    # ------------------------------------------------------------------

    def _get_current_speaker_meta(self) -> Dict[str, Any]:
        """Get metadata of the last utterance from listener."""
        default = {
            "speaker_id": "unknown",
            "speaker_name": t("responses.unknown_speaker"),
            "priority": 2,
            "confidence": 0.0,
            "music_probability": 0.0,
            "text": "",
            "timestamp": 0.0,
        }
        if hasattr(self.listener, "get_last_speaker_meta"):
            try:
                meta = self.listener.get_last_speaker_meta()
                if isinstance(meta, dict):
                    return {**default, **meta}
            except Exception as e:
                kiwi_log("SPEAKER", f"Failed to read speaker meta: {e}", level="ERROR")
        return default

    def _is_owner_speaker(self, speaker_meta: Dict[str, Any]) -> bool:
        return str(speaker_meta.get("speaker_id", "")).lower() == str(self._owner_id).lower()

    def _owner_profile_registered(self) -> bool:
        manager = getattr(self.listener, "speaker_manager", None)
        if manager is None:
            return False
        try:
            base = getattr(manager, "base_identifier", None)
            if base is not None and hasattr(base, "profiles"):
                return self._owner_id in base.profiles
        except Exception:
            return False
        return False

    def _is_small_talk_or_safe_request(self, command_lower: str) -> bool:
        """Requests that don't require separate owner approval."""
        safe_markers = [
            "анекдот", "шутк", "сказк", "истори", "поговори", "как дела", "спой",
            "который час", "сколько времени", "время", "дата", "день недели",
            "погода", "новости", "расскажи", "объясни", "кто такой", "что такое",
        ]
        return any(marker in command_lower for marker in safe_markers)

    def _looks_like_actionable_task(self, command_lower: str) -> bool:
        task_markers = [
            "сделай", "выполни", "запусти", "открой", "закрой", "удали", "создай",
            "поставь", "скачай", "установи", "отправь", "напиши", "измени", "перемести",
            "найди", "поищи", "проверь", "зайди", "команд", "в терминале", "shell",
        ]
        return any(marker in command_lower for marker in task_markers)

    def _approval_yes(self, command_lower: str) -> bool:
        yes_markers = ["разрешаю", "подтверждаю", "одобряю", "выполняй", "да, выполняй", "да выполняй"]
        return any(marker in command_lower for marker in yes_markers)

    def _approval_no(self, command_lower: str) -> bool:
        no_markers = ["запрещаю", "отклоняю", "не выполняй", "не надо", "нельзя", "отмена разрешения"]
        return any(marker in command_lower for marker in no_markers)

    def _extract_name_from_voice_command(self, command: str) -> Optional[str]:
        match = re.search(r"(?:запомни меня как|это мой друг|друг)\s+([а-яa-zё\-]{2,30})", command, re.IGNORECASE)
        if not match:
            return None
        name = match.group(1).strip()
        return name[:1].upper() + name[1:]

    def _on_telegram_approval_decision(self, approved, approval_data):
        """Called from Telegram polling thread when owner presses Approve/Deny."""
        if not self._pending_owner_approval:
            return  # Already resolved by voice or expired
        command = self._pending_owner_approval.get("command", "")
        speaker_name = self._pending_owner_approval.get("speaker_name", t("responses.unknown_speaker"))
        self._pending_owner_approval = None
        if approved:
            self.speak(t("responses.telegram_approved", requester=speaker_name), style="confident")
            ctx = CommandContext(command=command)
            ctx.command_lower = command.lower().strip()
            ctx.approved_command_from_owner = command
            self._stage_dispatch_to_llm(ctx)
        else:
            self.speak(t("responses.telegram_denied", requester=speaker_name), style="calm")

    def _notify_owner_security_event(self, message):
        """Send security alerts to Telegram (no approval buttons)."""
        kiwi_log("SECURITY", message, level="WARNING")
        voice_security = getattr(self, '_voice_security', None)
        if voice_security:
            voice_security.notify(f"{t('security.telegram_security_title')}\n\n{message}")
