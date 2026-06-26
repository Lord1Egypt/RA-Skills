"""Stream watchdog mixin — detects and recovers from stalled LLM streams."""

import time
import threading
from typing import Optional

from kiwi.state_machine import DialogueState
from kiwi.utils import kiwi_log
from kiwi.i18n import t


class StreamWatchdogMixin:
    """Monitors LLM streaming for stalls and retries or finalises."""

    # ------------------------------------------------------------------
    # Progress bookkeeping
    # ------------------------------------------------------------------

    def _reset_stream_watchdog_progress(self):
        with self._stream_watchdog_lock:
            self._stream_watchdog_first_token_seen = False
            self._stream_watchdog_token_count = 0
            self._stream_watchdog_total_chars = 0
            self._stream_watchdog_last_token_ts = time.time()
            self._stream_watchdog_last_activity_ts = time.time()

    # ------------------------------------------------------------------
    # Start / stop
    # ------------------------------------------------------------------

    def _start_stream_watchdog(self, command: str):
        timeout_s = float(self.config.llm_stream_stall_timeout)
        if timeout_s <= 0:
            return

        self._stop_stream_watchdog()
        with self._stream_watchdog_lock:
            self._stream_watchdog_command = command
            self._stream_watchdog_retry_count = 0
            self._stream_watchdog_retrying = False
            self._stream_watchdog_first_token_seen = False
            self._stream_watchdog_token_count = 0
            self._stream_watchdog_total_chars = 0
            self._stream_watchdog_last_token_ts = time.time()
            self._stream_watchdog_last_activity_ts = time.time()

        self._stream_watchdog_stop_event.clear()
        self._stream_watchdog_thread = threading.Thread(
            target=self._stream_watchdog_loop,
            daemon=True,
            name="kiwi-stream-watchdog",
        )
        self._stream_watchdog_thread.start()
        kiwi_log("STREAM-WATCHDOG", f"Started (stall timeout: {timeout_s:.1f}s)", level="INFO")

    def _stop_stream_watchdog(self):
        self._stream_watchdog_stop_event.set()
        thread = self._stream_watchdog_thread
        if thread and thread.is_alive() and thread is not threading.current_thread():
            thread.join(timeout=1.0)
        self._stream_watchdog_thread = None

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------

    def _stream_watchdog_loop(self):
        timeout_s = max(5.0, float(self.config.llm_stream_stall_timeout))
        no_first_token_timeout = max(timeout_s * 3.0, 45.0)
        low_progress_timeout = max(timeout_s * 2.0, 24.0)
        post_progress_timeout = max(timeout_s * 2.5, 30.0)
        no_processing_since: Optional[float] = None
        while not self._stream_watchdog_stop_event.wait(0.25):
            if timeout_s <= 0:
                return
            if not self.openclaw.is_processing():
                if no_processing_since is None:
                    no_processing_since = time.time()
                elif (time.time() - no_processing_since) >= 2.0:
                    return
                continue
            no_processing_since = None

            with self._stream_watchdog_lock:
                first_token_seen = self._stream_watchdog_first_token_seen
                token_count = self._stream_watchdog_token_count
                total_chars = self._stream_watchdog_total_chars
                now = time.time()
                stalled_for = now - self._stream_watchdog_last_token_ts
                activity_stalled_for = now - self._stream_watchdog_last_activity_ts
                retrying = self._stream_watchdog_retrying

            if not first_token_seen:
                stall_reason = "before first token"
                effective_timeout = no_first_token_timeout
            elif token_count < 3 or total_chars < 16:
                stall_reason = "low token progress"
                effective_timeout = low_progress_timeout
            else:
                stall_reason = "no token progress"
                effective_timeout = post_progress_timeout

            if activity_stalled_for < 5.0:
                effective_timeout = max(effective_timeout, 90.0)

            if stalled_for > timeout_s:
                kiwi_log("STREAM-WATCHDOG",
                    f"Stall check: {stall_reason}, stalled={stalled_for:.1f}s, "
                    f"effective_timeout={effective_timeout:.1f}s, "
                    f"activity_stalled={activity_stalled_for:.1f}s",
                    level="DEBUG")

            if retrying or stalled_for < effective_timeout:
                continue

            try:
                self._handle_streaming_stall(stalled_for, stall_reason)
            except Exception as e:
                kiwi_log("STREAM-WATCHDOG",
                    f"_handle_streaming_stall crashed: {e}", level="ERROR")
                import traceback
                kiwi_log("STREAM-WATCHDOG", traceback.format_exc(), level="ERROR")

    # ------------------------------------------------------------------
    # Accumulated text helper
    # ------------------------------------------------------------------

    def _get_accumulated_stream_text(self) -> str:
        """Return accumulated text from WS client (best effort, non-blocking)."""
        if not hasattr(self.openclaw, "_accumulated_text"):
            return ""

        try:
            lock = getattr(self.openclaw, "_buffer_lock", None)
            if lock is not None:
                acquired = lock.acquire(timeout=2.0)
                if acquired:
                    try:
                        text = getattr(self.openclaw, "_accumulated_text", "") or getattr(self.openclaw, "_full_response", "")
                    finally:
                        lock.release()
                else:
                    kiwi_log("STREAM-WATCHDOG", "Buffer lock timeout (2s), reading without lock", level="WARNING")
                    text = getattr(self.openclaw, "_accumulated_text", "") or getattr(self.openclaw, "_full_response", "")
            else:
                text = getattr(self.openclaw, "_accumulated_text", "") or getattr(self.openclaw, "_full_response", "")
        except Exception:
            text = getattr(self.openclaw, "_accumulated_text", "") or getattr(self.openclaw, "_full_response", "")

        return str(text).strip()

    def _finalize_stalled_stream_from_accumulated(self, stalled_for: float, stall_reason: str) -> bool:
        """Try to finalise a stalled stream from already-accumulated text."""
        accumulated = self._get_accumulated_stream_text()
        if len(accumulated) < 40:
            return False

        kiwi_log(
            "STREAM-WATCHDOG",
            f"Stalled ({stall_reason}) for {stalled_for:.1f}s, "
            f"finalizing from accumulated text ({len(accumulated)} chars)",
            level="WARNING",
        )

        # Suppress stale on_complete callbacks from cancel
        with self._streaming_completion_lock:
            self._streaming_generation = 0

        try:
            self.openclaw.cancel()
        except Exception as e:
            kiwi_log("STREAM-WATCHDOG", f"Cancel before finalize failed: {e}", level="ERROR")

        with self._streaming_completion_lock:
            self._streaming_generation = 1
        self._on_llm_complete(accumulated)
        return True

    # ------------------------------------------------------------------
    # Stall handler
    # ------------------------------------------------------------------

    def _handle_streaming_stall(self, stalled_for: float, stall_reason: str):
        accumulated_now = self._get_accumulated_stream_text()
        has_substantial_text = len(accumulated_now) >= 120
        if has_substantial_text and (
            self._streaming_response_playback_started or self._streaming_tts_manager is not None
        ):
            kiwi_log(
                "STREAM-WATCHDOG",
                f"Stall ({stall_reason}) for {stalled_for:.1f}s with "
                f"{len(accumulated_now)} accumulated chars; finalizing instead of retry",
                level="WARNING",
            )
            if self._finalize_stalled_stream_from_accumulated(stalled_for, stall_reason):
                self._stop_stream_watchdog()
                return

        retry_exhausted = False
        with self._stream_watchdog_lock:
            if self._stream_watchdog_retrying:
                return
            max_retries = max(0, int(self.config.llm_stream_stall_retry_max))
            if self._stream_watchdog_retry_count >= max_retries:
                retry_exhausted = True
            else:
                self._stream_watchdog_retrying = True
                self._stream_watchdog_retry_count += 1
                retry_no = self._stream_watchdog_retry_count
                command = self._stream_watchdog_command

        if retry_exhausted:
            if self._finalize_stalled_stream_from_accumulated(stalled_for, stall_reason):
                self._stop_stream_watchdog()
                return

            kiwi_log(
                "STREAM-WATCHDOG",
                f"Stalled ({stall_reason}) for {stalled_for:.1f}s, "
                "retry budget exhausted and no usable accumulated text",
                level="ERROR",
            )

            self._stop_stream_watchdog()
            # Suppress stale on_complete callbacks from cancel
            with self._streaming_completion_lock:
                self._streaming_generation = 0
            try:
                self.openclaw.cancel()
            except Exception as e:
                kiwi_log("STREAM-WATCHDOG", f"Cancel failed (exhausted path): {e}", level="ERROR")

            if self._streaming_tts_manager:
                self._streaming_tts_manager.stop(graceful=False)
                self._streaming_tts_manager = None
            self._set_state(DialogueState.IDLE)
            self.speak(t("responses.error_stream_stalled"), style="calm")
            return

        kiwi_log(
            "STREAM-WATCHDOG",
            f"Stall ({stall_reason}) for {stalled_for:.1f}s. "
            f"Retrying request ({retry_no}/{self.config.llm_stream_stall_retry_max})",
            level="WARNING",
        )

        try:
            # Suppress stale on_complete callbacks that fire during cancel/reconnect
            kiwi_log("STREAM-WATCHDOG", "Retry step 1/7: suppress stale callbacks", level="DEBUG")
            with self._streaming_completion_lock:
                self._streaming_generation = 0

            kiwi_log("STREAM-WATCHDOG", "Retry step 2/7: cancel", level="DEBUG")
            self.openclaw.cancel()

            kiwi_log("STREAM-WATCHDOG", "Retry step 3/6: stop TTS manager", level="DEBUG")
            if self._streaming_tts_manager:
                self._streaming_tts_manager.stop(graceful=False)
                self._streaming_tts_manager = None

            # Check if WS connection is alive; if dead, reconnect first
            kiwi_log("STREAM-WATCHDOG", "Retry step 4/6: check WS alive", level="DEBUG")
            ws_alive = getattr(self.openclaw, "is_ws_alive", None)
            if callable(ws_alive) and not ws_alive(15.0):
                kiwi_log("STREAM-WATCHDOG",
                    "WS connection appears dead, forcing reconnect before retry",
                    level="WARNING")
                reconnect_fn = getattr(self.openclaw, "force_reconnect", None)
                if callable(reconnect_fn):
                    reconnect_fn("stream stall recovery")

            # Re-arm generation counter for the retry
            kiwi_log("STREAM-WATCHDOG", "Retry step 5/6: re-arm + start streaming runtime", level="DEBUG")
            with self._streaming_completion_lock:
                self._streaming_generation = 1
            self._streaming_response_playback_started = False

            self._start_streaming_runtime(command)
            kiwi_log("STREAM-WATCHDOG", "Retry step 6/6: send_message", level="DEBUG")
            resend_ok = self.openclaw.send_message(command)
            if not resend_ok:
                kiwi_log("STREAM-WATCHDOG", "Retry send failed", level="ERROR")
                self._set_state(DialogueState.IDLE)
                self.speak(t("responses.error_retry_failed"), style="calm")
                self._stop_stream_watchdog()
                return

            self._reset_stream_watchdog_progress()
            kiwi_log("STREAM-WATCHDOG", "Retry sent successfully", level="INFO")
        finally:
            with self._stream_watchdog_lock:
                self._stream_watchdog_retrying = False
