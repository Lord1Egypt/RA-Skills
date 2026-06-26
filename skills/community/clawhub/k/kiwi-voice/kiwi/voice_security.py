#!/usr/bin/env python3
"""
Voice Security - Telegram Approval + Dangerous Command Detection

Features:
- Dangerous command detection via regex patterns
- Telegram approval with inline keyboard (approve/deny)
- Caching of pending approvals
- Fallback to log file when Telegram is unavailable
"""

import os
import re
import json
import time
import asyncio
import threading
from typing import Optional, Dict, Tuple, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime

import requests

from kiwi.utils import kiwi_log
from kiwi.i18n import t

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv("KIWI_TELEGRAM_BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("KIWI_TELEGRAM_CHAT_ID") or os.getenv("TELEGRAM_CHAT_ID", "")


class CommandType(Enum):
    """Command types by danger level."""
    SAFE = 0           # Safe commands
    WARNING = 1        # Require attention
    DANGEROUS = 2      # Require approval
    CRITICAL = 3       # Require explicit approval


@dataclass
class PendingApproval:
    """Pending approval."""
    command: str
    speaker_id: str
    speaker_name: str
    timestamp: float
    callback_data: str  # unique ID for callback
    
    def is_expired(self, timeout: int = 60) -> bool:
        """Check if the timeout has expired."""
        return time.time() - self.timestamp > timeout


class DangerousCommandDetector:
    """
    Dangerous command detector based on regular expressions.

    Checks commands before execution and sends them to Telegram
    for approval if it is a dangerous command from a non-Owner.
    """

    # Dangerous command patterns
    DANGEROUS_PATTERNS = [
        # File/folder deletion
        (CommandType.CRITICAL, r"удали?\s+(вс[её]|все|файлы?|папк[уаи]?|директорию|каталог)"),
        (CommandType.CRITICAL, r"delete\s+(all|files?|folder|directory)"),
        (CommandType.CRITICAL, r"rm\s+(-rf|/r|/f|rf)"),
        (CommandType.CRITICAL, r"format\s+[a-zA-Z]:"),
        
        # Shutdown/reboot
        (CommandType.CRITICAL, r"выключи?\s+(компьютер|писи|windows|систему)"),
        (CommandType.CRITICAL, r"shutdown\s+(-h|-s|/s|/h)"),
        (CommandType.CRITICAL, r"перезагруз[и|ка]|restart|reboot"),
        (CommandType.CRITICAL, r"выключи.*сейчас|shutdown\s+now"),
        
        # System commands
        (CommandType.DANGEROUS, r"sudo\s+"),
        (CommandType.DANGEROUS, r"chmod\s+777|chmod\s+-R"),
        (CommandType.DANGEROUS, r"systemctl\s+(stop|disable|kill)"),
        (CommandType.DANGEROUS, r"net\s+stop"),
        
        # Passwords/secrets
        (CommandType.CRITICAL, r"отправь?\s+(пароль|пароли|ключ|токен|секрет|секреты)"),
        (CommandType.CRITICAL, r"покажи?\s+(пароль|ключ|токен)"),
        (CommandType.CRITICAL, r"send\s+(password|key|token|secret)"),
        (CommandType.CRITICAL, r"скажи?\s+(пароль|пароли|код|пин)"),
        
        # Installation of unknown software
        (CommandType.DANGEROUS, r"установи?\s+(неизвест|незнаком)"),
        (CommandType.DANGEROUS, r"install\s+(unknown|untrusted)"),
        (CommandType.DANGEROUS, r"скачай?\s+(исполни|вирус|троян)"),
        
        # System modification
        (CommandType.WARNING, r"измени?\s+(настройк[иа]|конфиг|config)"),
        (CommandType.WARNING, r"настрой?\s+(систему|сервер|nginx|apache)"),
        (CommandType.WARNING, r"change\s+(settings?|config)"),
        
        # Network operations
        (CommandType.WARNING, r"открой?\s+(порты?|port)"),
        (CommandType.WARNING, r"закрыть?\s+(порты?|port|firewall)"),
        (CommandType.WARNING, r"ping\s+-t"),
        
        # File operations
        (CommandType.WARNING, r"перемести?\s+(файл|папку)"),
        (CommandType.WARNING, r"move\s+(file|folder)"),
        (CommandType.WARNING, r"скопируй|copy"),
    ]
    
    def __init__(self):
        self._patterns = []
        locale_patterns = t("security_patterns")
        if isinstance(locale_patterns, dict):
            level_map = {
                "critical": CommandType.CRITICAL,
                "dangerous": CommandType.DANGEROUS,
                "warning": CommandType.WARNING,
            }
            for level_name, patterns in locale_patterns.items():
                level = level_map.get(level_name)
                if level is None:
                    continue
                for p in patterns:
                    try:
                        self._patterns.append((level, re.compile(p, re.IGNORECASE)))
                    except re.error as e:
                        kiwi_log("VOICE_SECURITY", f"Invalid locale pattern '{p}': {e}", level="ERROR")
        else:
            # Fallback to hardcoded patterns
            for cmd_type, pattern in self.DANGEROUS_PATTERNS:
                try:
                    self._patterns.append((cmd_type, re.compile(pattern, re.IGNORECASE)))
                except re.error as e:
                    kiwi_log("VOICE_SECURITY", f"Invalid pattern '{pattern}': {e}", level="ERROR")
    
    def analyze(self, command: str) -> Tuple[CommandType, Optional[str]]:
        """
        Analyze a command for danger level.

        Args:
            command: Command text

        Returns:
            (CommandType, matched_pattern)
        """
        command_lower = command.lower().strip()
        
        for cmd_type, pattern in self._patterns:
            if pattern.search(command_lower):
                return cmd_type, pattern.pattern
        
        return CommandType.SAFE, None
    
    def is_approval_required(self, command_type: CommandType, is_owner: bool) -> bool:
        """
        Check whether approval is required.

        Args:
            command_type: Type of command
            is_owner: Whether the speaker is the owner

        Returns:
            True if approval is required
        """
        if is_owner:
            # Owner can execute critical commands without approval
            return False

        # Non-owner requires approval for DANGEROUS and CRITICAL
        return command_type in (CommandType.DANGEROUS, CommandType.CRITICAL)
    
    def get_warning_message(self, command_type: CommandType) -> str:
        """Return a warning message for the given command type."""
        messages = {
            CommandType.SAFE: t("security.safe"),
            CommandType.WARNING: t("security.warning"),
            CommandType.DANGEROUS: t("security.dangerous"),
            CommandType.CRITICAL: t("security.critical"),
        }
        return messages.get(command_type, t("security.unknown_level"))


class TelegramApprovalClient:
    """
    Client for sending approval requests to Telegram.

    Uses Telegram Bot API with inline keyboard.
    """
    
    API_URL = "https://api.telegram.org/bot{}/".format(TELEGRAM_BOT_TOKEN)
    APPROVAL_TIMEOUT = 60  # seconds
    
    def __init__(self, bot_token: str = None, chat_id: str = None):
        self.bot_token = bot_token or TELEGRAM_BOT_TOKEN
        self.chat_id = chat_id or TELEGRAM_CHAT_ID
        self.pending_approvals: Dict[str, PendingApproval] = {}
        self._lock = threading.Lock()
        self._callbacks: Dict[str, Callable] = {}
        self._running = False
        self._poll_thread: Optional[threading.Thread] = None
        
    def is_configured(self) -> bool:
        """Check if the bot is configured."""
        return bool(self.bot_token) and bool(self.chat_id)
    
    def start(self):
        """Start polling for responses."""
        if not self.is_configured():
            kiwi_log("VOICE_SECURITY", "Telegram not configured, using fallback", level="WARNING")
            return
        
        self._running = True
        self._poll_thread = threading.Thread(target=self._poll_loop, daemon=True)
        self._poll_thread.start()
        kiwi_log("VOICE_SECURITY", "Telegram approval client started")
    
    def stop(self):
        """Stop polling."""
        self._running = False
        if self._poll_thread:
            self._poll_thread.join(timeout=2)
        kiwi_log("VOICE_SECURITY", "Telegram approval client stopped")
    
    def _poll_loop(self):
        """Polling loop to receive callbacks from Inline Keyboard."""
        last_offset = 0
        backoff = 5
        consecutive_errors = 0

        while self._running:
            try:
                url = self.API_URL + "getUpdates"
                params = {
                    "offset": last_offset,
                    "timeout": 30,
                    "allowed_updates": ["callback_query"]
                }

                response = requests.post(url, json=params, timeout=35)
                data = response.json()

                if data.get("ok"):
                    for update in data.get("result", []):
                        last_offset = update["update_id"] + 1

                        callback = update.get("callback_query")
                        if callback:
                            self._handle_callback(callback)

                # Reset backoff on success
                consecutive_errors = 0
                backoff = 5

            except Exception as e:
                consecutive_errors += 1
                if consecutive_errors <= 3:
                    kiwi_log("VOICE_SECURITY", f"Polling error ({consecutive_errors}): {e}", level="ERROR")
                elif consecutive_errors == 4:
                    kiwi_log("VOICE_SECURITY", f"Telegram unreachable after {consecutive_errors} attempts, reducing poll frequency", level="WARNING")
                # Exponential backoff: 5 → 10 → 20 → 40 → ... → max 300s
                time.sleep(backoff)
                backoff = min(backoff * 2, 300)
    
    def _handle_callback(self, callback: dict):
        """Handle a button press callback."""
        callback_data = callback.get("data", "")
        callback_id = callback.get("id", "")
        message_id = callback.get("message", {}).get("message_id")

        # callback_data format: "{key}_approve" or "{key}_deny"
        # where key = "kiwi_{timestamp}".  Split from the RIGHT to
        # separate the action ("approve"/"deny") from the compound key.
        if "_" in callback_data:
            key, action = callback_data.rsplit("_", 1)
        else:
            key, action = callback_data, "deny"

        approved = (action == "approve")

        with self._lock:
            if key in self.pending_approvals:
                approval = self.pending_approvals[key]
                cb = self._callbacks.get(key)

                # Remove from the queue
                del self.pending_approvals[key]
                self._callbacks.pop(key, None)
            else:
                approval = None
                cb = None

        if approval and cb:
            kiwi_log("VOICE_SECURITY",
                     f"Telegram {'approved' if approved else 'denied'}: {approval.command[:60]}",
                     level="INFO")
            try:
                cb(approved, approval)
            except Exception as e:
                kiwi_log("VOICE_SECURITY", f"Callback error: {e}", level="ERROR")
        elif not approval:
            kiwi_log("VOICE_SECURITY",
                     f"Callback for unknown/expired key: {key}", level="WARNING")

        # Answer the callback query so the button stops showing a spinner
        if callback_id:
            try:
                answer_text = t("security.telegram_approved") if approved else t("security.telegram_denied")
                url = f"https://api.telegram.org/bot{self.bot_token}/answerCallbackQuery"
                requests.post(url, json={
                    "callback_query_id": callback_id,
                    "text": answer_text,
                }, timeout=5)
            except Exception:
                pass
    
    def send_approval_request(
        self,
        command: str,
        speaker_id: str,
        speaker_name: str,
        callback: Callable[[bool, PendingApproval], None] = None
    ) -> str:
        """
        Send an approval request to Telegram.

        Args:
            command: Command text
            speaker_id: Speaker ID
            speaker_name: Speaker name
            callback: Callback function (approved, approval_data)

        Returns:
            callback_data for tracking
        """
        # Generate a unique ID
        callback_data = f"kiwi_{int(time.time())}"
        
        # Create a pending record
        approval = PendingApproval(
            command=command,
            speaker_id=speaker_id,
            speaker_name=speaker_name,
            timestamp=time.time(),
            callback_data=callback_data
        )
        
        with self._lock:
            self.pending_approvals[callback_data] = approval
            if callback:
                self._callbacks[callback_data] = callback
        
        # Compose the message
        message = (
            f"{t('security.telegram_request_title')}\n\n"
            f"{t('security.telegram_speaker_label')} {speaker_name}\n"
            f"🆔 ID: `{speaker_id}`\n\n"
            f"{t('security.telegram_command_label')}\n"
            f"```\n{command}\n```\n\n"
            f"{t('security.telegram_confirm')}"
        )
        
        # Send to Telegram
        if self.is_configured():
            self._send_telegram_message(message, callback_data)
        else:
            # Fallback - log it
            kiwi_log("VOICE_SECURITY", f"Approval request (fallback): {speaker_name} -> {command}")
            # Auto-approve after 5 seconds for testing
            if callback:
                time.sleep(0.1)
                callback(True, approval)
        
        return callback_data

    def send_notification(self, message: str):
        """Send a plain Telegram message without inline keyboard buttons (for alerts)."""
        if not self.is_configured():
            kiwi_log("VOICE_SECURITY", f"Notification (fallback): {message}")
            return
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            data = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "Markdown",
            }
            response = requests.post(url, json=data, timeout=10)
            if not response.json().get("ok"):
                kiwi_log("VOICE_SECURITY", f"Telegram notification error: {response.text}", level="ERROR")
        except Exception as e:
            kiwi_log("VOICE_SECURITY", f"Telegram notification error: {e}", level="ERROR")

    def _send_telegram_message(self, message: str, callback_data: str):
        """Send a message with inline keyboard."""
        try:
            url = self.API_URL + "sendMessage"
            data = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "Markdown",
                "reply_markup": json.dumps({
                    "inline_keyboard": [[
                        {"text": t("security.approve_button"), "callback_data": f"{callback_data}_approve"},
                        {"text": t("security.deny_button"), "callback_data": f"{callback_data}_deny"}
                    ]]
                })
            }
            
            response = requests.post(url, json=data, timeout=10)
            if not response.json().get("ok"):
                kiwi_log("VOICE_SECURITY", f"Telegram send error: {response.text}", level="ERROR")
        except Exception as e:
            kiwi_log("VOICE_SECURITY", f"Telegram error: {e}", level="ERROR")
    
    def cleanup_expired(self):
        """Clean up expired approval requests."""
        expired = []
        
        with self._lock:
            for key, approval in self.pending_approvals.items():
                if approval.is_expired(self.APPROVAL_TIMEOUT):
                    expired.append(key)
            
            for key in expired:
                del self.pending_approvals[key]
                if key in self._callbacks:
                    del self._callbacks[key]
        
        if expired:
            kiwi_log("VOICE_SECURITY", f"Cleaned {len(expired)} expired approvals")
    
    def check_pending(self, callback_data: str) -> Optional[PendingApproval]:
        """Check the status of a pending approval."""
        with self._lock:
            return self.pending_approvals.get(callback_data)


class VoiceSecurity:
    """
    Main voice command security class.

    Combines:
    - DangerousCommandDetector
    - TelegramApprovalClient
    """
    
    def __init__(self, bot_token: str = None, chat_id: str = None):
        self.detector = DangerousCommandDetector()
        self.telegram = TelegramApprovalClient(bot_token, chat_id)
        self.telegram.start()
        
        # Cleanup timer
        self._cleanup_timer: Optional[threading.Timer] = None
        self._start_cleanup_timer()
    
    def _start_cleanup_timer(self):
        """Start periodic cleanup."""
        self._cleanup_timer = threading.Timer(30.0, self._cleanup_loop)
        self._cleanup_timer.daemon = True
        self._cleanup_timer.start()
    
    def _cleanup_loop(self):
        """Periodic cleanup."""
        self.telegram.cleanup_expired()
        self._start_cleanup_timer()
    
    def analyze_command(
        self,
        command: str,
        speaker_id: str,
        speaker_name: str = "",
        is_owner: bool = False,
        execute_callback: Callable[[str], None] = None
    ) -> Tuple[bool, str]:
        """
        Analyze a command and request approval if necessary.

        Args:
            command: Command text
            speaker_id: Speaker ID
            speaker_name: Speaker name
            is_owner: Whether the speaker is the owner
            execute_callback: Called on approval (command)

        Returns:
            (should_execute, message)
        """
        # Analyze for danger level
        cmd_type, pattern = self.detector.analyze(command)
        warning = self.detector.get_warning_message(cmd_type)
        
        kiwi_log("VOICE_SECURITY", f"Command analysis: type={cmd_type.name}, pattern={pattern}")
        
        # Owner executes without approval
        if is_owner:
            if cmd_type == CommandType.CRITICAL:
                return True, f"{warning} (Owner - выполнено без подтверждения)"
            elif cmd_type == CommandType.DANGEROUS:
                # Owner can execute, but with a warning
                return True, f"{warning}"
            else:
                return True, warning
        
        # Non-owner requires approval
        if self.detector.is_approval_required(cmd_type, is_owner):
            # Send approval request
            def on_approve(approved: bool, approval: PendingApproval):
                if approved:
                    if execute_callback:
                        execute_callback(command)
                else:
                    kiwi_log("VOICE_SECURITY", f"Command denied by {approval.speaker_name}")
            
            self.telegram.send_approval_request(
                command=command,
                speaker_id=speaker_id,
                speaker_name=speaker_name,
                callback=on_approve
            )
            
            return False, f"{warning}\n{t('security.awaiting_approval')}"
        
        # SAFE commands are executed
        return True, warning
    
    def notify(self, message: str):
        """Send a plain notification to Telegram (no approval buttons)."""
        self.telegram.send_notification(message)

    def stop(self):
        """Stop all processes."""
        if self._cleanup_timer:
            self._cleanup_timer.cancel()
        self.telegram.stop()


# === VOICE MANAGEMENT COMMANDS ===

OWNER_CONTROL_PATTERNS = {
    # Blocking
    r"в чёрный список|заблокируй|запрети.*голос|блокируй.*голос": "block_last",
    r"добавь.*черный список": "block_last",
    
    # Unblocking
    r"разблокируй|убери.*черный список|вычеркни.*списка": "unblock_last",
    r"разблокируй.*голос": "unblock_last",
    
    # Adding a friend
    r"запомни.*как|это мой друг|запомни.*голос": "add_friend",
    r"добавь.*друг": "add_friend",
    
    # Forgetting
    r"забудь.*голос|удали.*профиль": "forget_speaker",
    r"удали.*друг": "forget_speaker",
    
    # Identification
    r"кто.*говорит|кто.*это|who.*is.*speaking": "identify",
    
    # Help/info
    r"какие.*голоса|справка.*по.*голосам|list.*voices": "list_voices",
}


def get_owner_control_patterns() -> dict:
    """Load owner control patterns from i18n locale, falling back to hardcoded defaults."""
    locale_patterns = t("owner_control_patterns")
    if isinstance(locale_patterns, dict):
        return {re.compile(pattern, re.IGNORECASE): action for action, pattern in locale_patterns.items()}
    return {re.compile(k, re.IGNORECASE): v for k, v in OWNER_CONTROL_PATTERNS.items()}


def extract_name_from_command(command: str) -> Optional[str]:
    """Extract a name from a friend-adding command."""
    # Load patterns from locale, fallback to hardcoded
    locale_patterns = t("name_patterns.patterns")
    if isinstance(locale_patterns, list) and locale_patterns:
        patterns = locale_patterns
    else:
        # Fallback to hardcoded patterns
        patterns = [
            r"как\s+(\w+)",
            r"друг\s+(\w+)",
            r"меня\s+зовут\s+(\w+)",
            r"это\s+(\w+)",
        ]

    locale_filter = t("name_patterns.filter_words")
    if isinstance(locale_filter, list) and locale_filter:
        filter_words = [w.lower() for w in locale_filter]
    else:
        # Fallback to hardcoded filter words
        filter_words = ["тебя", "меня", "его", "её", "кто", "что"]

    for pattern in patterns:
        match = re.search(pattern, command, re.IGNORECASE)
        if match:
            name = match.group(1).capitalize()
            # Filter out common words
            if name.lower() not in filter_words:
                return name

    return None


# Testing
if __name__ == "__main__":
    print("[TEST] Voice Security Test")

    security = VoiceSecurity()

    # Detector test
    test_commands = [
        "удали все файлы",
        "выключи компьютер",
        "какая погода",
        "открой браузер",
        "sudo rm -rf /",
    ]
    
    for cmd in test_commands:
        cmd_type, pattern = security.detector.analyze(cmd)
        print(f"  '{cmd}' -> {cmd_type.name}")
    
    security.stop()
