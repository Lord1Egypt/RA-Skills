"""LLM callback mixin — token, activity, completion, and exec approval handlers."""

import time
import threading

from kiwi.state_machine import DialogueState
from kiwi.utils import kiwi_log
from kiwi.i18n import t

try:
    from kiwi.event_bus import EventType, get_event_bus
    _EB_AVAILABLE = True
except ImportError:
    _EB_AVAILABLE = False


class LLMCallbacksMixin:
    """WebSocket callback handlers for streaming LLM responses."""

    def _on_llm_token(self, token: str):
        """Callback on each token from the LLM (WebSocket delta event)."""
        if token:
            with self._stream_watchdog_lock:
                first_token = not self._stream_watchdog_first_token_seen
                self._stream_watchdog_first_token_seen = True
                self._stream_watchdog_token_count += 1
                self._stream_watchdog_total_chars += len(token)
                self._stream_watchdog_last_token_ts = time.time()

            # Extend THINKING state timeout while tokens are arriving.
            try:
                with self._state_lock:
                    if self._dialogue_state == DialogueState.THINKING:
                        timeout = self._state_timeouts.get(DialogueState.THINKING, 60.0)
                        self._state_until = time.time() + timeout
            except Exception:
                pass

        if self._streaming_tts_manager:
            self._streaming_tts_manager.on_token(token)

    def _on_agent_activity(self, activity: dict):
        """Callback for intermediate agent activity (tool/lifecycle)."""
        with self._stream_watchdog_lock:
            self._stream_watchdog_last_activity_ts = time.time()

        # Extend THINKING state timeout — agent IS working (tool calls, etc.).
        # Without this, the 60s hard timeout kills long-running tasks like
        # model downloads or code generation.
        try:
            with self._state_lock:
                if self._dialogue_state == DialogueState.THINKING:
                    timeout = self._state_timeouts.get(DialogueState.THINKING, 60.0)
                    self._state_until = time.time() + timeout
        except Exception:
            pass

        message = activity.get("message", "")

        # Flush ElevenLabs WS buffer — agent switched from text to tool work,
        # the last word of the text segment is stuck in the buffer without a
        # trailing space.  flush_wave() is idempotent (no-op if buffer empty).
        if self._streaming_tts_manager and hasattr(self._streaming_tts_manager, 'flush_wave'):
            self._streaming_tts_manager.flush_wave()

    def _on_wave_end(self):
        """lifecycle:end arrived — flush ElevenLabs WS buffer between waves."""
        if self._streaming_tts_manager and hasattr(self._streaming_tts_manager, 'flush_wave'):
            self._streaming_tts_manager.flush_wave()

    def _on_llm_complete(self, full_text: str):
        """Callback when LLM generation is complete (WebSocket final event)."""
        self._stop_stream_watchdog()

        with self._streaming_completion_lock:
            if self._streaming_generation == 0:
                kiwi_log("LLM", "Duplicate/stale completion callback ignored", level="WARNING")
                return
            self._streaming_generation = 0

        # Fallback: use accumulated text if full_text is empty
        if not full_text and hasattr(self.openclaw, '_accumulated_text'):
            accumulated = self.openclaw._accumulated_text
            if accumulated:
                kiwi_log("LLM", f"Generation complete with EMPTY final, using accumulated: {len(accumulated)} chars", level="WARNING")
                full_text = accumulated
            else:
                kiwi_log("LLM", "Generation complete: 0 chars (EMPTY)", level="WARNING")
                # Safety net: don't leave the user in silence
                if not self._streaming_response_playback_started:
                    full_text = t("responses.error_no_response")
        else:
            kiwi_log("LLM", f"Generation complete: {len(full_text)} chars", level="INFO")

        if self._streaming_tts_manager:
            self._streaming_tts_manager.stop()
            self._streaming_tts_manager = None

        # Safety fallback: speak full text only if streaming never started playback.
        # If playback started, audio was delivered — even if the WS later died
        # (idle timeout between waves), the graceful stop drains the queue.
        if not self._streaming_response_playback_started and full_text and full_text.strip():
            kiwi_log("STREAM-TTS", "No playback started for this response, using fallback speak()", level="WARNING")
            self.speak(full_text, style=self._streaming_style)
            if not self._barge_in_requested:
                self._start_idle_timer()
            return

        # Post-playback transition (mirrors _play_audio_interruptible)
        self._is_speaking = False
        self.listener._tts_start_time = time.time()
        self.listener._last_tts_text = full_text or ""
        self.listener._last_tts_time = time.time()
        self.listener.activate_dialog_mode()

        if self.listener.dialog_mode:
            self._set_state(DialogueState.LISTENING)
        else:
            self._set_state(DialogueState.IDLE)

        if not self._barge_in_requested:
            self._start_idle_timer()

    # ------------------------------------------------------------------
    # Exec approval: OpenClaw asks for permission to run a shell command
    # ------------------------------------------------------------------

    def _on_exec_approval_request(self, data: dict):
        """Called from WebSocket thread when OpenClaw requests exec approval.

        Pauses TTS, announces the command to the owner, and waits for
        voice confirmation or Telegram approval. If no response within
        the timeout, the approval is denied.
        """
        approval_id = data.get("id", "")
        command = data.get("command", "")
        expires_at_ms = data.get("expires_at_ms", 0)

        kiwi_log("EXEC-APPROVAL", f"OpenClaw requests approval: '{command[:100]}'", level="INFO")

        # Publish event for dashboard
        if _EB_AVAILABLE:
            try:
                get_event_bus().publish(EventType.EXEC_APPROVAL_REQUESTED,
                    {'id': approval_id, 'command': command},
                    source='exec_approval')
            except Exception:
                pass

        # Store pending approval
        self._pending_exec_approval = {
            "id": approval_id,
            "command": command,
            "timestamp": time.time(),
            "expires_at_ms": expires_at_ms,
        }

        # Announce to owner via voice
        announce = t("responses.exec_approval_request")
        if not announce or announce == "responses.exec_approval_request":
            announce = "OpenClaw wants to run a command: {command}. Should I allow it?"
        self.speak(announce.format(command=command[:100]) if "{command}" in announce else f"{announce} {command[:100]}", style="neutral")

        # Also send via Telegram if configured
        voice_security = getattr(self, '_voice_security', None)
        if voice_security and voice_security.telegram.is_configured():
            voice_security.telegram.send_approval_request(
                command=f"[exec] {command}",
                speaker_id="openclaw-agent",
                speaker_name="OpenClaw Agent",
                callback=self._on_exec_telegram_decision,
            )
            kiwi_log("EXEC-APPROVAL", "Telegram approval request sent", level="INFO")

        # Activate dialog mode to listen for voice response
        self.listener.activate_dialog_mode()

        # Start timeout timer — deny if no response
        timeout_s = 55.0  # OpenClaw default is 60s, leave 5s margin
        if expires_at_ms:
            remaining = (expires_at_ms / 1000.0) - time.time()
            if remaining > 5:
                timeout_s = remaining - 5  # 5s margin

        timer = threading.Timer(timeout_s, self._exec_approval_timeout, args=[approval_id])
        timer.daemon = True
        timer.start()

    def _on_exec_telegram_decision(self, approved, approval_data):
        """Called from Telegram polling thread when owner approves/denies exec."""
        if not self._pending_exec_approval:
            return

        approval_id = self._pending_exec_approval["id"]
        self._pending_exec_approval = None

        decision = "allow-once" if approved else "deny"
        self.openclaw.resolve_exec_approval(approval_id, decision)

        if approved:
            self.speak(t("responses.exec_approved") or "Approved. Running the command.", style="confident")
        else:
            self.speak(t("responses.exec_denied") or "Denied. Command blocked.", style="calm")

    def _exec_approval_timeout(self, approval_id: str):
        """Auto-deny if no response within the timeout."""
        if not self._pending_exec_approval:
            return
        if self._pending_exec_approval.get("id") != approval_id:
            return

        kiwi_log("EXEC-APPROVAL", f"Timeout — auto-denying {approval_id[:12]}", level="WARNING")
        self._pending_exec_approval = None
        self.openclaw.resolve_exec_approval(approval_id, "deny")
        self.speak(t("responses.exec_timeout") or "No response. Command denied.", style="calm")

    def resolve_pending_exec_approval(self, approved: bool) -> bool:
        """Resolve pending exec approval from voice command.

        Called from dialogue pipeline when owner says "allow" / "deny".

        Returns:
            True if there was a pending approval to resolve
        """
        if not self._pending_exec_approval:
            return False

        approval_id = self._pending_exec_approval["id"]
        self._pending_exec_approval = None

        decision = "allow-once" if approved else "deny"
        self.openclaw.resolve_exec_approval(approval_id, decision)

        # Publish event for dashboard
        if _EB_AVAILABLE:
            try:
                get_event_bus().publish(EventType.EXEC_APPROVAL_RESOLVED,
                    {'id': approval_id, 'decision': decision},
                    source='exec_approval')
            except Exception:
                pass

        if approved:
            self.speak(t("responses.exec_approved") or "Approved. Running the command.", style="confident")
        else:
            self.speak(t("responses.exec_denied") or "Denied. Command blocked.", style="calm")
        return True
