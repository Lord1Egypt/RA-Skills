#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""iCalendar Sync - iCloud/OpenClaw calendar operations."""

from __future__ import annotations

import argparse
import base64
import getpass
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import uuid
from datetime import datetime, timedelta, timezone, time as dt_time
from functools import wraps
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence
from urllib.parse import urljoin, urlparse

ICALENDAR_IMPORT_ERROR = ""
iCal = None
iEvent = None
Alarm = None
try:
    from icalendar import Alarm, Calendar as iCal, Event as iEvent
except ImportError as exc:  # pragma: no cover - depends on runtime environment
    ICALENDAR_IMPORT_ERROR = str(exc)

REQUESTS_IMPORT_ERROR = ""
requests = None
RequestException = Exception
SSLError = Exception
ConnectionError = Exception
Timeout = Exception
try:
    import requests
    from requests.exceptions import ConnectionError, RequestException, SSLError, Timeout
except ImportError as exc:  # pragma: no cover - depends on runtime environment
    REQUESTS_IMPORT_ERROR = str(exc)

YAML_IMPORT_ERROR = ""
yaml = None
YAMLError = Exception
try:
    import yaml
    YAMLError = yaml.YAMLError
except ImportError as exc:  # pragma: no cover - depends on runtime environment
    YAML_IMPORT_ERROR = str(exc)

CALDAV_IMPORT_ERROR = ""
caldav = None
DAVClient = None
AuthorizationError = Exception
NotFoundError = Exception
DAVError = Exception
try:
    import caldav
    from caldav.davclient import DAVClient
    from caldav.lib.error import AuthorizationError, DAVError, NotFoundError
except ImportError as exc:  # pragma: no cover - depends on runtime environment
    CALDAV_IMPORT_ERROR = str(exc)

KEYRING_IMPORT_ERROR = ""
keyring = None
KeyringError = Exception
try:
    import keyring
    from keyring.errors import KeyringError
except ImportError as exc:  # pragma: no cover - depends on runtime environment
    KEYRING_IMPORT_ERROR = str(exc)
    class KeyringError(Exception):
        """Fallback keyring error when dependency is unavailable."""

    class _MissingKeyring:
        def get_password(self, service_name: str, username: str) -> Optional[str]:
            raise KeyringError(KEYRING_IMPORT_ERROR or "keyring dependency is unavailable")

        def set_password(self, service_name: str, username: str, password: str) -> None:
            raise KeyringError(KEYRING_IMPORT_ERROR or "keyring dependency is unavailable")

    keyring = _MissingKeyring()

__author__ = "Black_Temple"
__version__ = "2.4"

MAX_CALENDAR_NAME_LENGTH = 255
MAX_SUMMARY_LENGTH = 500
MAX_DESCRIPTION_LENGTH = 5000
MAX_LOCATION_LENGTH = 500
MAX_JSON_FILE_SIZE = 1024 * 1024
MAX_DAYS_AHEAD = 365
MIN_DAYS_AHEAD = 1
MAX_EVENT_UID_LENGTH = 500
RATE_LIMIT_CALLS = 10
RATE_LIMIT_WINDOW = 60
INPUT_TIMEOUT = 30
MAX_CONFIG_FILE_SIZE = 64 * 1024
DEFAULT_CONFIG_PATH = Path.home() / ".openclaw" / "icalendar-sync.yaml"
DEFAULT_USER_AGENT = "macOS/14.0.0 (23A344) CalendarAgent/954"


class SensitiveDataFilter(logging.Filter):
    """Redact potentially sensitive fields from logs."""

    SENSITIVE_PATTERNS = [
        (
            re.compile(r'password["\']?\s*[:=]\s*["\']?([^"\',\s]+)', re.IGNORECASE),
            "password=***",
        ),
        (
            re.compile(r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", re.IGNORECASE),
            "***@***.***",
        ),
        (re.compile(r"(xxxx-xxxx-xxxx-xxxx|\d{4}-\d{4}-\d{4}-\d{4})"), "****-****-****-****"),
    ]

    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = self._sanitize(str(record.msg))
        if record.args:
            record.args = tuple(self._sanitize(str(arg)) for arg in record.args)
        return True

    def _sanitize(self, text: str) -> str:
        for pattern, replacement in self.SENSITIVE_PATTERNS:
            text = pattern.sub(replacement, text)
        return text


def _configure_logging() -> logging.Logger:
    root_logger = logging.getLogger()
    if not root_logger.handlers:
        logging.basicConfig(
            level=os.getenv("LOG_LEVEL", "WARNING"),
            format="%(asctime)s | %(levelname)s | %(message)s",
        )

    app_logger = logging.getLogger(__name__)
    if not any(isinstance(existing, SensitiveDataFilter) for existing in app_logger.filters):
        app_logger.addFilter(SensitiveDataFilter())
    return app_logger


logger = _configure_logging()


class RateLimiter:
    """Simple thread-safe token bucket window limiter."""

    def __init__(self, max_calls: int, window: int):
        self.max_calls = max_calls
        self.window = window
        self.calls: List[float] = []
        self.lock = threading.Lock()

    def acquire(self) -> bool:
        with self.lock:
            now = time.time()
            self.calls = [call_time for call_time in self.calls if now - call_time < self.window]
            if len(self.calls) >= self.max_calls:
                return False
            self.calls.append(now)
            return True

    def wait_if_needed(self) -> None:
        while not self.acquire():
            time.sleep(1)


def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """Retry decorator for transient network/CalDAV failures."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            current_delay = delay
            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                except (RequestException, DAVError):
                    attempt += 1
                    if attempt >= max_attempts:
                        logger.error("Failed after %s attempts", max_attempts)
                        raise
                    logger.warning("Attempt %s failed, retrying in %ss", attempt, current_delay)
                    time.sleep(current_delay)
                    current_delay *= backoff
            return None

        return wrapper

    return decorator


def validate_calendar_name(name: str) -> bool:
    """Validate calendar name and reject path-like payloads."""
    if not name or not isinstance(name, str):
        return False
    if len(name) > MAX_CALENDAR_NAME_LENGTH:
        return False
    if not re.match(r"^[\w\s_-]+$", name, re.UNICODE):
        return False
    if ".." in name or "/" in name or "\\" in name:
        return False
    return True


def validate_email(email: str) -> bool:
    return bool(re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))


def validate_secret_value(value: str) -> bool:
    if not value or not isinstance(value, str):
        return False
    return all(char not in value for char in ("\n", "\r", "\x00"))


def is_truthy_env(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def sanitize_text(text: Any, max_length: int) -> str:
    raw = str(text)
    normalized = "".join(char for char in raw if char.isprintable() or char in "\n\t")
    if len(normalized) > max_length:
        return normalized[: max_length - 3] + "..."
    return normalized


def safe_file_read(file_path: str, max_size: int = MAX_JSON_FILE_SIZE) -> Optional[str]:
    try:
        path = Path(file_path).expanduser().resolve()
        if not path.is_file():
            logger.error("File not found: %s", file_path)
            return None
        stat_result = path.stat()
        if stat_result.st_size > max_size:
            logger.error("File too large: %s bytes", stat_result.st_size)
            return None
        return path.read_text(encoding="utf-8")
    except (OSError, ValueError) as exc:
        logger.error("Error reading file: %s", exc)
        return None


def timed_input(prompt: str, timeout: int = INPUT_TIMEOUT) -> Optional[str]:
    """Input with timeout on Unix-like systems."""
    import signal

    def timeout_handler(signum, frame):  # pragma: no cover - signal callback
        raise TimeoutError("Input timeout")

    try:
        if hasattr(signal, "SIGALRM"):
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(timeout)

        result = input(prompt)

        if hasattr(signal, "SIGALRM"):
            signal.alarm(0)
        return result
    except TimeoutError:
        print("\n⏱️  Input timeout")
        return None
    except Exception:
        return input(prompt)


def resolve_config_path(config_path: Optional[str] = None) -> Path:
    raw_path = config_path or os.getenv("ICALENDAR_SYNC_CONFIG")
    if raw_path:
        return Path(raw_path).expanduser()
    return DEFAULT_CONFIG_PATH


def safe_load_config_credentials(config_path: Optional[str] = None) -> Dict[str, str]:
    path = resolve_config_path(config_path)

    try:
        path = path.resolve()
    except OSError as exc:
        logger.error("Invalid config path: %s", exc)
        return {}

    if not path.is_file():
        return {}

    try:
        stat_result = path.stat()
        if stat_result.st_size > MAX_CONFIG_FILE_SIZE:
            logger.error("Config file too large: %s bytes", stat_result.st_size)
            return {}

        file_mode = stat_result.st_mode & 0o777
        if file_mode & 0o077:
            logger.warning(
                "Config file permissions are too open (%s). Expected 0o600.",
                oct(file_mode),
            )

        if yaml is None:
            logger.error("YAML support is unavailable: %s", YAML_IMPORT_ERROR)
            return {}

        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}

        if not isinstance(data, dict):
            logger.error("Config file must contain a YAML object")
            return {}

        username = data.get("username") or data.get("icloud_username")
        password = data.get("app_password") or data.get("icloud_app_password") or data.get("password")

        username_value = username.strip() if isinstance(username, str) else ""
        password_value = password.strip() if isinstance(password, str) else ""

        if password_value and not validate_secret_value(password_value):
            logger.error("Config password contains invalid control characters")
            return {}

        result: Dict[str, str] = {}
        if username_value:
            result["username"] = username_value
        if password_value:
            result["password"] = password_value
        return result

    except (OSError, YAMLError) as exc:
        logger.error("Failed to read config file: %s", exc)
        return {}


def save_config_credentials(config_path: Optional[str], username: str, password: str) -> Optional[Path]:
    if yaml is None:
        logger.error("YAML support is unavailable: %s", YAML_IMPORT_ERROR)
        return None

    path = resolve_config_path(config_path).expanduser()
    tmp_path: Optional[Path] = None

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(path.parent, 0o700)
        except OSError:
            pass

        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            delete=False,
            dir=path.parent,
        ) as tmp_handle:
            tmp_path = Path(tmp_handle.name)
            yaml.safe_dump(
                {"username": username, "app_password": password},
                tmp_handle,
                sort_keys=False,
                default_flow_style=False,
            )

        os.chmod(tmp_path, 0o600)
        shutil.move(str(tmp_path), str(path))
        os.chmod(path, 0o600)
        return path
    except (OSError, YAMLError) as exc:
        logger.error("Failed to write config file: %s", exc)
        if tmp_path and tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass
        return None


def applescript_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def datetime_to_applescript(var_name: str, dt: datetime) -> List[str]:
    if dt.tzinfo is not None:
        dt = dt.astimezone()

    month_names = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]

    seconds = dt.hour * 3600 + dt.minute * 60 + dt.second
    return [
        f"set {var_name} to (current date)",
        f"set year of {var_name} to {dt.year}",
        f'set month of {var_name} to {month_names[dt.month - 1]}',
        f"set day of {var_name} to {dt.day}",
        f"set time of {var_name} to {seconds}",
    ]


def parse_iso_datetime(value: str) -> datetime:
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed


def _require_icalendar_runtime() -> bool:
    if iCal is None or iEvent is None:
        print("❌ icalendar package is unavailable")
        logger.error("icalendar runtime unavailable: %s", ICALENDAR_IMPORT_ERROR)
        return False
    return True


def _coerce_dt(component_value: Any, fallback_tz: timezone = timezone.utc) -> Optional[datetime]:
    value = getattr(component_value, "dt", component_value)
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=fallback_tz)
        return value
    if value is None:
        return None
    if isinstance(value, dt_time):
        return None
    return datetime.combine(value, dt_time.min).replace(tzinfo=fallback_tz)


class MacOSNativeCalendarManager:
    """Bridge provider: use Calendar.app through AppleScript."""

    def __init__(self):
        if sys.platform != "darwin":
            raise RuntimeError("--provider macos-native is only available on macOS")

    def _run_applescript(self, lines: List[str]) -> Optional[str]:
        script = "\n".join(lines) + "\n"
        try:
            result = subprocess.run(
                ["osascript", "-"],
                input=script,
                text=True,
                capture_output=True,
                check=True,
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as exc:
            stderr_text = sanitize_text((exc.stderr or "").strip(), 500)
            logger.error("AppleScript error: %s", stderr_text)
            print("❌ macOS Calendar bridge error")
            if stderr_text:
                print(f"   {stderr_text}")
            return None

    def list_calendars(self) -> List[str]:
        lines = [
            "set oldTIDs to AppleScript's text item delimiters",
            "set AppleScript's text item delimiters to linefeed",
            'tell application "Calendar"',
            "set calNames to name of every calendar",
            "end tell",
            'set outputText to ""',
            "if (count of calNames) > 0 then set outputText to (calNames as text)",
            "set AppleScript's text item delimiters to oldTIDs",
            "return outputText",
        ]
        output = self._run_applescript(lines)
        if output is None:
            return []

        calendars = [line.strip() for line in output.splitlines() if line.strip()]
        print(f"📅 Available Calendars ({len(calendars)}):\n")
        for name in calendars:
            print(f"  • {name}")
        return calendars

    def get_events(self, calendar_name: str, days_ahead: int = 7) -> List[Dict[str, str]]:
        if not validate_calendar_name(calendar_name):
            print("❌ Invalid calendar name")
            return []
        if not (MIN_DAYS_AHEAD <= days_ahead <= MAX_DAYS_AHEAD):
            print(f"❌ days_ahead must be between {MIN_DAYS_AHEAD} and {MAX_DAYS_AHEAD}")
            return []

        escaped_name = applescript_escape(calendar_name)
        lines = [
            "set oldTIDs to AppleScript's text item delimiters",
            "set AppleScript's text item delimiters to linefeed",
            'tell application "Calendar"',
            f'if not (exists calendar "{escaped_name}") then error "Calendar not found"',
            f'set calRef to calendar "{escaped_name}"',
            "set startDate to current date",
            f"set endDate to startDate + ({days_ahead} * days)",
            "set eventLines to {}",
            "repeat with e in (every event of calRef whose start date ≥ startDate and start date ≤ endDate)",
            "set end of eventLines to ((summary of e as text) & \"|||\" & (id of e as text) & \"|||\" & ((start date of e) as text) & \"|||\" & ((end date of e) as text))",
            "end repeat",
            "end tell",
            'set outputText to ""',
            "if (count of eventLines) > 0 then set outputText to (eventLines as text)",
            "set AppleScript's text item delimiters to oldTIDs",
            "return outputText",
        ]
        output = self._run_applescript(lines)
        if output is None:
            return []

        events: List[Dict[str, str]] = []
        lines_out = [line for line in output.splitlines() if line.strip()]
        print(f"📋 Events in '{calendar_name}' ({len(lines_out)} found):\n")
        for line in lines_out:
            parts = line.split("|||")
            if len(parts) < 4:
                continue
            summary, event_id, start_raw, end_raw = parts[0], parts[1], parts[2], parts[3]
            print(f"  🗓️  {summary}")
            print(f"     Start: {start_raw}")
            print(f"     End: {end_raw}")
            print(f"     UID: {event_id}\n")
            events.append(
                {
                    "summary": summary,
                    "uid": event_id,
                    "dtstart": start_raw,
                    "dtend": end_raw,
                }
            )
        return events

    def create_event(
        self,
        calendar_name: str,
        event_data: Dict[str, Any],
        check_conflicts: bool = True,
        auto_confirm: bool = False,
    ) -> bool:
        del check_conflicts, auto_confirm

        if not validate_calendar_name(calendar_name):
            print("❌ Invalid calendar name")
            return False

        missing_fields = [field for field in ("summary", "dtstart", "dtend") if field not in event_data]
        if missing_fields:
            print(f"❌ Missing required fields: {', '.join(missing_fields)}")
            return False

        dtstart = event_data["dtstart"]
        dtend = event_data["dtend"]
        if not isinstance(dtstart, datetime) or not isinstance(dtend, datetime):
            print("❌ dtstart and dtend must be datetime objects")
            return False
        if dtend <= dtstart:
            print("❌ Event end time must be after start time")
            return False

        summary = applescript_escape(sanitize_text(event_data.get("summary", ""), MAX_SUMMARY_LENGTH))
        description = applescript_escape(sanitize_text(event_data.get("description", ""), MAX_DESCRIPTION_LENGTH))
        location = applescript_escape(sanitize_text(event_data.get("location", ""), MAX_LOCATION_LENGTH))
        escaped_name = applescript_escape(calendar_name)

        lines = []
        lines.extend(datetime_to_applescript("startDate", dtstart))
        lines.extend(datetime_to_applescript("endDate", dtend))
        lines.extend(
            [
                'tell application "Calendar"',
                f'if not (exists calendar "{escaped_name}") then error "Calendar not found"',
                f'set calRef to calendar "{escaped_name}"',
                f'set newEvent to make new event at end of events of calRef with properties {{summary:"{summary}", start date:startDate, end date:endDate}}',
            ]
        )
        if description:
            lines.append(f'set description of newEvent to "{description}"')
        if location:
            lines.append(f'set location of newEvent to "{location}"')
        lines.extend(["set eventId to id of newEvent", "end tell", "return eventId as text"])

        output = self._run_applescript(lines)
        if output is None:
            return False

        print(f"✅ Event '{event_data.get('summary', 'Untitled')}' created successfully")
        if output:
            logger.info("Created native event id=%s", output)
        return True

    def delete_event(self, calendar_name: str, event_uid: str) -> bool:
        if not validate_calendar_name(calendar_name):
            print("❌ Invalid calendar name")
            return False
        if not event_uid or not isinstance(event_uid, str):
            print("❌ Valid event UID required")
            return False

        escaped_name = applescript_escape(calendar_name)
        escaped_uid = applescript_escape(event_uid.strip())
        lines = [
            'tell application "Calendar"',
            f'if not (exists calendar "{escaped_name}") then error "Calendar not found"',
            f'set calRef to calendar "{escaped_name}"',
            f'set matches to (every event of calRef whose id is "{escaped_uid}")',
            'if (count of matches) = 0 then error "Event not found"',
            "delete (item 1 of matches)",
            "end tell",
            'return "ok"',
        ]
        output = self._run_applescript(lines)
        if output is None:
            return False
        print("🗑️  Event deleted successfully")
        return True

    def update_event(
        self,
        calendar_name: str,
        event_uid: str,
        update_data: Dict[str, Any],
        recurrence_id: Optional[str] = None,
        mode: str = "single",
    ) -> bool:
        if not validate_calendar_name(calendar_name):
            print("❌ Invalid calendar name")
            return False
        if not event_uid or not isinstance(event_uid, str):
            print("❌ Valid event UID required")
            return False
        if mode not in ["single", "all", "future"]:
            print("❌ Invalid mode. Must be 'single', 'all', or 'future'")
            return False
        if recurrence_id or mode in ("all", "future"):
            print("⚠️  macOS native provider updates a single event by ID (recurrence mode ignored)")

        escaped_name = applescript_escape(calendar_name)
        escaped_uid = applescript_escape(event_uid.strip())
        lines = [
            'tell application "Calendar"',
            f'if not (exists calendar "{escaped_name}") then error "Calendar not found"',
            f'set calRef to calendar "{escaped_name}"',
            f'set matches to (every event of calRef whose id is "{escaped_uid}")',
            'if (count of matches) = 0 then error "Event not found"',
            "set targetEvent to item 1 of matches",
            "end tell",
        ]

        if "summary" in update_data:
            summary = applescript_escape(sanitize_text(update_data["summary"], MAX_SUMMARY_LENGTH))
            lines.extend(["tell application \"Calendar\"", f'set summary of targetEvent to "{summary}"', "end tell"])
        if "description" in update_data:
            description = applescript_escape(sanitize_text(update_data["description"], MAX_DESCRIPTION_LENGTH))
            lines.extend([
                "tell application \"Calendar\"",
                f'set description of targetEvent to "{description}"',
                "end tell",
            ])
        if "location" in update_data:
            location = applescript_escape(sanitize_text(update_data["location"], MAX_LOCATION_LENGTH))
            lines.extend(["tell application \"Calendar\"", f'set location of targetEvent to "{location}"', "end tell"])
        if "dtstart" in update_data:
            dtstart = update_data["dtstart"]
            if isinstance(dtstart, str):
                dtstart = parse_iso_datetime(dtstart)
            if not isinstance(dtstart, datetime):
                print("❌ Invalid dtstart")
                return False
            lines.extend(datetime_to_applescript("newStartDate", dtstart))
            lines.extend(["tell application \"Calendar\"", "set start date of targetEvent to newStartDate", "end tell"])
        if "dtend" in update_data:
            dtend = update_data["dtend"]
            if isinstance(dtend, str):
                dtend = parse_iso_datetime(dtend)
            if not isinstance(dtend, datetime):
                print("❌ Invalid dtend")
                return False
            lines.extend(datetime_to_applescript("newEndDate", dtend))
            lines.extend(["tell application \"Calendar\"", "set end date of targetEvent to newEndDate", "end tell"])

        lines.append('return "ok"')
        output = self._run_applescript(lines)
        if output is None:
            return False
        print("✅ Event updated successfully")
        return True


class CalendarManager:
    """Manage iCloud Calendar via CalDAV."""

    def __init__(
        self,
        config_path: Optional[str] = None,
        user_agent: Optional[str] = None,
        debug_http: bool = False,
        credential_source: str = "auto",
    ):
        self.config_path = resolve_config_path(config_path)
        self.debug_http = debug_http or is_truthy_env(os.getenv("ICALENDAR_SYNC_DEBUG_HTTP", "0"))
        self.user_agent = (
            user_agent or os.getenv("ICALENDAR_SYNC_USER_AGENT") or DEFAULT_USER_AGENT
        ).strip()
        if credential_source not in ("auto", "keyring", "env", "file", "env-only"):
            logger.warning("Unknown credential source '%s', using auto", credential_source)
            credential_source = "auto"
        self.credential_source = credential_source

        self.base_url = os.getenv("ICALENDAR_SYNC_CALDAV_URL", "https://caldav.icloud.com").strip()
        self._config_credentials = safe_load_config_credentials(str(self.config_path))
        self._last_http_debug: Dict[str, str] = {}
        self.username = self._resolve_username()
        self.password = self._load_password()

        self.client: Optional[DAVClient] = None
        self._connected = False
        self._connection_time: Optional[datetime] = None
        self._cache_timeout = 300
        self._connection_lock = threading.Lock()
        self._rate_limiter = RateLimiter(RATE_LIMIT_CALLS, RATE_LIMIT_WINDOW)

    def _require_caldav_runtime(self) -> bool:
        missing = []
        if DAVClient is None:
            missing.append(f"caldav ({CALDAV_IMPORT_ERROR or 'not installed'})")
        if requests is None:
            missing.append(f"requests ({REQUESTS_IMPORT_ERROR or 'not installed'})")
        if missing:
            print(
                "❌ CalDAV provider is unavailable: "
                + ", ".join(missing)
                + ". Install dependencies from requirements.txt or use --provider macos-native."
            )
            logger.error("CalDAV runtime unavailable: %s", ", ".join(missing))
            return False
        return True

    def _resolve_username(self) -> Optional[str]:
        if self.credential_source in ("env", "env-only"):
            return os.getenv("ICLOUD_USERNAME")
        if self.credential_source == "file":
            return self._config_credentials.get("username")
        return os.getenv("ICLOUD_USERNAME") or self._config_credentials.get("username")

    def _load_password(self) -> Optional[str]:
        username = self.username

        if self.credential_source in ("auto", "keyring") and username and not KEYRING_IMPORT_ERROR:
            try:
                password = keyring.get_password("openclaw-icalendar", username)
                if password:
                    logger.debug("Loaded password from keyring")
                    return password
            except KeyringError:
                pass
        elif self.credential_source == "keyring" and KEYRING_IMPORT_ERROR:
            logger.error("Keyring requested but unavailable: %s", KEYRING_IMPORT_ERROR)
            return None

        if self.credential_source in ("auto", "env", "env-only"):
            env_password = os.getenv("ICLOUD_APP_PASSWORD")
            if env_password:
                if validate_secret_value(env_password):
                    return env_password
                logger.error("Environment password contains invalid control characters")

        if self.credential_source in ("auto", "file"):
            config_password = self._config_credentials.get("password")
            config_username = self._config_credentials.get("username")
            if config_password and validate_secret_value(config_password):
                if not username or not config_username or config_username == username:
                    if not self.username and config_username:
                        self.username = config_username
                    return config_password

        return None

    def _build_request_headers(self, target_url: str) -> Dict[str, str]:
        parsed = urlparse(target_url)
        host = parsed.netloc or "caldav.icloud.com"
        return {
            "User-Agent": self.user_agent,
            "Host": host,
            "Origin": "https://www.icloud.com",
            "Accept": "*/*",
            "Connection": "keep-alive",
        }

    def _capture_response_debug(self, response: Any) -> None:
        debug_data = {
            "status": str(getattr(response, "status_code", "")),
            "reason": str(getattr(response, "reason", "")),
            "url": str(getattr(response, "url", "")),
        }
        headers = getattr(response, "headers", {})
        for key in ("x-apple-request-id", "x-apple-session-token", "www-authenticate", "location"):
            value = headers.get(key) or headers.get(key.title())
            if value:
                debug_data[key] = str(value)

        if self.debug_http:
            body = sanitize_text(getattr(response, "text", "") or "", 2000)
            if body:
                debug_data["body"] = body

        self._last_http_debug = debug_data

    def _debug_string_from_last_response(self) -> str:
        if not self._last_http_debug:
            return ""
        order = [
            "status",
            "reason",
            "url",
            "x-apple-request-id",
            "x-apple-session-token",
            "www-authenticate",
            "location",
            "body",
        ]
        return ", ".join(
            f"{key}={self._last_http_debug[key]}" for key in order if self._last_http_debug.get(key)
        )

    def _resolve_caldav_endpoint(self) -> str:
        current_url = self.base_url
        if not self.username or not self.password or requests is None:
            return current_url

        max_redirects = 5
        timeout = 15
        session = requests.Session()
        auth_header = "Basic " + base64.b64encode(
            f"{self.username}:{self.password}".encode("utf-8")
        ).decode("ascii")

        for _ in range(max_redirects):
            headers = self._build_request_headers(current_url)
            headers["Authorization"] = auth_header

            try:
                response = session.get(
                    current_url,
                    headers=headers,
                    allow_redirects=False,
                    timeout=timeout,
                )
                self._capture_response_debug(response)
            except RequestException as exc:
                if self.debug_http:
                    logger.debug("Endpoint resolution failed: %s", self._format_exception_details(exc))
                break

            if response.status_code in (301, 302, 307, 308):
                location = response.headers.get("Location")
                if not location:
                    break
                next_url = urljoin(current_url, location)
                next_host = (urlparse(next_url).hostname or "").lower()
                if next_host and next_host.endswith("icloud.com"):
                    current_url = next_url
                    continue
                break
            break

        return current_url

    def _format_exception_details(self, exc: Exception) -> str:
        details = [f"type={type(exc).__name__}"]
        for attr in ("status", "reason", "url"):
            value = getattr(exc, attr, None)
            if value:
                details.append(f"{attr}={value}")

        response = getattr(exc, "response", None)
        if response is not None:
            status_code = getattr(response, "status_code", None)
            if status_code:
                details.append(f"http_status={status_code}")
            headers = getattr(response, "headers", {})
            for key in ("x-apple-request-id", "x-apple-session-token"):
                value = headers.get(key) or headers.get(key.title())
                if value:
                    details.append(f"{key}={value}")
            if self.debug_http:
                response_text = getattr(response, "text", "")
                if response_text:
                    details.append(f"response={sanitize_text(response_text, 300)}")

        if self.debug_http and getattr(exc, "args", None):
            details.append(f"args={sanitize_text(str(exc.args), 300)}")

        return ", ".join(details)

    def _is_connection_valid(self) -> bool:
        with self._connection_lock:
            if not self._connected or not self._connection_time:
                return False
            elapsed = (datetime.now(timezone.utc) - self._connection_time).total_seconds()
            return elapsed < self._cache_timeout

    def _iter_principals(self) -> List[Any]:
        principals: List[Any] = []
        try:
            principal = self.client.principal()
        except Exception:
            return principals

        principals.append(principal)

        for attr_name in ("principal", "parent", "owner"):
            ref = getattr(principal, attr_name, None)
            if callable(ref):
                try:
                    nested = ref()
                except Exception:
                    nested = None
                if nested is not None and nested not in principals:
                    principals.append(nested)

        return principals

    def _discover_calendars(self) -> List[Any]:
        if self.client is None:
            return []

        discovered: List[Any] = []
        seen_urls = set()

        def add_calendar(cal: Any) -> None:
            if cal is None:
                return
            candidate_url = None
            for attr in ("url", "canonical_url"):
                value = getattr(cal, attr, None)
                if value:
                    candidate_url = str(value)
                    break
            if candidate_url and candidate_url in seen_urls:
                return
            if candidate_url:
                seen_urls.add(candidate_url)
            discovered.append(cal)

        for principal in self._iter_principals():
            try:
                for cal in principal.calendars() or []:
                    add_calendar(cal)
            except Exception:
                pass

            home_set_getter = getattr(principal, "calendar_home_set", None)
            if callable(home_set_getter):
                try:
                    home_set = home_set_getter()
                    if home_set is not None:
                        for cal in home_set.calendars() or []:
                            add_calendar(cal)
                except Exception:
                    pass

        return discovered

    @retry(max_attempts=3, delay=1.0, backoff=2.0)
    def connect(self) -> bool:
        if self._is_connection_valid():
            logger.debug("Using cached CalDAV connection")
            return True

        if not self._require_caldav_runtime():
            return False

        if not self.username or not self.password:
            print("❌ iCloud credentials not configured")
            logger.error("Missing iCloud credentials")
            return False

        self._rate_limiter.wait_if_needed()

        try:
            with self._connection_lock:
                if self.debug_http:
                    logger.setLevel(logging.DEBUG)
                    logger.debug("CalDAV debug enabled")

                resolved_url = self._resolve_caldav_endpoint()
                headers = self._build_request_headers(resolved_url)
                if self.debug_http:
                    logger.debug(
                        "CalDAV headers prepared: Host=%s Origin=%s User-Agent=%s",
                        headers.get("Host"),
                        headers.get("Origin"),
                        headers.get("User-Agent"),
                    )

                client_kwargs = dict(
                    url=resolved_url,
                    username=self.username,
                    password=self.password,
                    ssl_verify_cert=True,
                    headers=headers,
                )
                try:
                    self.client = DAVClient(**client_kwargs)
                except TypeError:
                    client_kwargs.pop("headers", None)
                    self.client = DAVClient(**client_kwargs)
                    if hasattr(self.client, "session") and hasattr(self.client.session, "headers"):
                        self.client.session.headers.update(headers)

                principal = self.client.principal()
                principal.calendars()

                self._connected = True
                self._connection_time = datetime.now(timezone.utc)
                logger.info("Successfully connected to iCloud CalDAV")
                return True

        except AuthorizationError as exc:
            print("❌ Authentication failed: invalid credentials or blocked iCloud request")
            if self.debug_http and self._debug_string_from_last_response():
                print(f"   Apple response: {self._debug_string_from_last_response()}")
            if self.debug_http:
                print(f"   Debug: {self._format_exception_details(exc)}")
            logger.error("Authentication failed (%s)", self._format_exception_details(exc))
            self._connected = False
            return False
        except SSLError as exc:
            print("❌ TLS/SSL handshake error")
            if self.debug_http and self._debug_string_from_last_response():
                print(f"   Apple response: {self._debug_string_from_last_response()}")
            if self.debug_http:
                print(f"   Debug: {self._format_exception_details(exc)}")
            logger.error("TLS handshake error (%s)", self._format_exception_details(exc))
            self._connected = False
            raise
        except (ConnectionError, Timeout) as exc:
            print("❌ Network error")
            if self.debug_http and self._debug_string_from_last_response():
                print(f"   Apple response: {self._debug_string_from_last_response()}")
            if self.debug_http:
                print(f"   Debug: {self._format_exception_details(exc)}")
            logger.error("Network error (%s)", self._format_exception_details(exc))
            self._connected = False
            raise
        except DAVError as exc:
            print("❌ CalDAV error")
            if self.debug_http and self._debug_string_from_last_response():
                print(f"   Apple response: {self._debug_string_from_last_response()}")
            if self.debug_http:
                print(f"   Debug: {self._format_exception_details(exc)}")
            logger.error("CalDAV error (%s)", self._format_exception_details(exc))
            self._connected = False
            raise
        except Exception as exc:  # pragma: no cover - defensive
            print(f"❌ Unexpected error: {type(exc).__name__}")
            if self.debug_http and self._debug_string_from_last_response():
                print(f"   Apple response: {self._debug_string_from_last_response()}")
            if self.debug_http:
                print(f"   Debug: {self._format_exception_details(exc)}")
            logger.error("Unexpected connection error: %s", self._format_exception_details(exc))
            self._connected = False
            return False

    def list_calendars(self) -> List[str]:
        if not self.connect():
            return []

        self._rate_limiter.wait_if_needed()

        try:
            calendars = self._discover_calendars()

            print(f"📅 Available Calendars ({len(calendars)}):\n")
            names: List[str] = []
            for cal in calendars:
                print(f"  • {cal.name}")
                names.append(cal.name)
                logger.info("Found calendar: %s", cal.name)
            return names
        except NotFoundError:
            print("❌ Calendars not found")
            logger.error("Calendars not found")
            return []
        except DAVError:
            print("❌ CalDAV error")
            logger.error("Error listing calendars")
            return []
        except Exception as exc:
            print("❌ Error listing calendars")
            logger.error("Unexpected error listing calendars: %s", type(exc).__name__)
            return []

    def _check_event_conflicts(
        self,
        calendar: Any,
        start: datetime,
        end: datetime,
        exclude_uid: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        if not _require_icalendar_runtime():
            return []

        try:
            events = calendar.search(
                start=start - timedelta(hours=1),
                end=end + timedelta(hours=1),
                event=True,
                expand=True,
            )

            conflicts: List[Dict[str, Any]] = []
            for event in events:
                parsed_calendar = iCal.from_ical(event.data)
                for component in parsed_calendar.walk():
                    if component.name != "VEVENT":
                        continue

                    evt_uid = str(component.get("uid", ""))
                    if exclude_uid and evt_uid == exclude_uid:
                        continue

                    evt_start = _coerce_dt(component.get("dtstart"), start.tzinfo or timezone.utc)
                    evt_end = _coerce_dt(component.get("dtend"), end.tzinfo or timezone.utc)
                    if not evt_start or not evt_end:
                        continue

                    if not (end <= evt_start or start >= evt_end):
                        conflicts.append(
                            {
                                "summary": str(component.get("summary", "No title")),
                                "start": evt_start,
                                "end": evt_end,
                                "uid": evt_uid,
                            }
                        )

            return conflicts
        except Exception as exc:
            logger.warning("Could not check conflicts: %s", type(exc).__name__)
            return []

    def get_events(self, calendar_name: str, days_ahead: int = 7) -> List[Any]:
        if not validate_calendar_name(calendar_name):
            print("❌ Invalid calendar name")
            logger.error("Invalid calendar name provided")
            return []

        if not (MIN_DAYS_AHEAD <= days_ahead <= MAX_DAYS_AHEAD):
            print(f"❌ days_ahead must be between {MIN_DAYS_AHEAD} and {MAX_DAYS_AHEAD}")
            return []

        if not _require_icalendar_runtime():
            return []

        if not self.connect():
            return []

        self._rate_limiter.wait_if_needed()

        try:
            principal = self.client.principal()
            calendar = principal.calendar(name=calendar_name)

            start = datetime.now(timezone.utc)
            end = start + timedelta(days=days_ahead)
            events = calendar.search(start=start, end=end, event=True, expand=True)

            print(f"📋 Events in '{calendar_name}' ({len(events)} found):\n")
            for event in events:
                parsed_calendar = iCal.from_ical(event.data)
                for component in parsed_calendar.walk():
                    if component.name != "VEVENT":
                        continue
                    summary = component.get("summary", "No title")
                    dtstart = component.get("dtstart")
                    dtend = component.get("dtend")
                    uid = component.get("uid")

                    print(f"  🗓️  {summary}")
                    if dtstart:
                        print(f"     Start: {getattr(dtstart, 'dt', dtstart)}")
                    if dtend:
                        print(f"     End: {getattr(dtend, 'dt', dtend)}")
                    print(f"     UID: {uid}\n")
                    logger.info("Found event: %s", summary)
            return events

        except NotFoundError:
            print(f"❌ Calendar '{calendar_name}' not found")
            logger.error("Calendar not found")
            return []
        except DAVError:
            print("❌ CalDAV error")
            logger.error("Error getting events")
            return []
        except Exception as exc:
            print("❌ Error getting events")
            logger.error("Unexpected error getting events: %s", type(exc).__name__)
            return []

    def create_event(
        self,
        calendar_name: str,
        event_data: Dict[str, Any],
        check_conflicts: bool = True,
        auto_confirm: bool = False,
    ) -> bool:
        if not validate_calendar_name(calendar_name):
            print("❌ Invalid calendar name")
            logger.error("Invalid calendar name provided")
            return False

        if not _require_icalendar_runtime():
            return False

        if not self.connect():
            return False

        required_fields = ["summary", "dtstart", "dtend"]
        missing_fields = [field for field in required_fields if field not in event_data]
        if missing_fields:
            print(f"❌ Missing required fields: {', '.join(missing_fields)}")
            logger.error("Missing required fields: %s", missing_fields)
            return False

        if not isinstance(event_data["dtstart"], datetime):
            print("❌ dtstart must be a datetime object")
            return False
        if not isinstance(event_data["dtend"], datetime):
            print("❌ dtend must be a datetime object")
            return False

        dtstart = event_data["dtstart"]
        dtend = event_data["dtend"]
        if dtstart.tzinfo is None:
            dtstart = dtstart.replace(tzinfo=timezone.utc)
            logger.warning("dtstart had no timezone, assuming UTC")
        if dtend.tzinfo is None:
            dtend = dtend.replace(tzinfo=timezone.utc)
            logger.warning("dtend had no timezone, assuming UTC")

        if dtend <= dtstart:
            print("❌ Event end time must be after start time")
            return False

        summary = sanitize_text(event_data["summary"], MAX_SUMMARY_LENGTH)
        event_data["summary"] = summary
        if "description" in event_data:
            event_data["description"] = sanitize_text(event_data["description"], MAX_DESCRIPTION_LENGTH)
        if "location" in event_data:
            event_data["location"] = sanitize_text(event_data["location"], MAX_LOCATION_LENGTH)

        self._rate_limiter.wait_if_needed()

        try:
            principal = self.client.principal()
            calendar = principal.calendar(name=calendar_name)

            if check_conflicts:
                conflicts = self._check_event_conflicts(calendar, dtstart, dtend)
                if conflicts:
                    print(f"⚠️  Warning: {len(conflicts)} conflicting event(s) found:")
                    for conflict in conflicts:
                        print(f"   - {conflict['summary']} ({conflict['start']} to {conflict['end']})")

                    if not auto_confirm:
                        response = timed_input("Continue anyway? (y/n): ")
                        if response is None or response.lower() != "y":
                            print("Event creation cancelled")
                            return False

            cal = iCal()
            cal.add("prodid", "-//iCalendar Sync//EN")
            cal.add("version", "2.0")

            event = iEvent()
            event.add("uid", str(uuid.uuid4()))
            event.add("dtstamp", datetime.now(timezone.utc))
            event.add("summary", summary)
            event.add("dtstart", dtstart)
            event.add("dtend", dtend)

            if "location" in event_data:
                event.add("location", event_data["location"])
            if "description" in event_data:
                event.add("description", event_data["description"])
            if "status" in event_data:
                event.add("status", event_data["status"])
            if "priority" in event_data and isinstance(event_data["priority"], int):
                event.add("priority", max(0, min(9, event_data["priority"])))

            if Alarm is not None and "alarms" in event_data and isinstance(event_data["alarms"], list):
                for alarm_data in event_data["alarms"]:
                    if isinstance(alarm_data, dict):
                        alarm = Alarm()
                        alarm.add("action", "DISPLAY")
                        minutes = alarm_data.get("minutes", 15)
                        alarm.add("trigger", timedelta(minutes=-abs(minutes)))
                        alarm.add("description", alarm_data.get("description", "Reminder"))
                        event.add_component(alarm)

            if "rrule" in event_data and isinstance(event_data["rrule"], dict):
                rrule_data = event_data["rrule"]
                rrule_dict: Dict[str, Any] = {"FREQ": [rrule_data.get("freq", "WEEKLY")]}

                if "count" in rrule_data and isinstance(rrule_data["count"], int):
                    rrule_dict["COUNT"] = [max(1, rrule_data["count"])]
                if "interval" in rrule_data and isinstance(rrule_data["interval"], int):
                    rrule_dict["INTERVAL"] = [max(1, rrule_data["interval"])]
                if "byday" in rrule_data:
                    rrule_dict["BYDAY"] = rrule_data["byday"]
                if "until" in rrule_data:
                    rrule_dict["UNTIL"] = [rrule_data["until"]]

                event.add("rrule", rrule_dict)

            cal.add_component(event)
            calendar.save_event(cal.to_ical().decode("utf-8"))

            print(f"✅ Event '{summary}' created successfully")
            logger.info("Created event in %s", calendar_name)
            return True

        except NotFoundError:
            print(f"❌ Calendar '{calendar_name}' not found")
            logger.error("Calendar not found")
            return False
        except DAVError:
            print("❌ CalDAV error")
            logger.error("Error creating event")
            return False
        except Exception as exc:
            print("❌ Error creating event")
            logger.error("Unexpected error creating event: %s", type(exc).__name__)
            return False

    def delete_event(self, calendar_name: str, event_uid: str) -> bool:
        if not validate_calendar_name(calendar_name):
            print("❌ Invalid calendar name")
            logger.error("Invalid calendar name provided")
            return False
        if not event_uid or not isinstance(event_uid, str):
            print("❌ Valid event UID required")
            return False

        event_uid = event_uid.strip()
        if len(event_uid) > MAX_EVENT_UID_LENGTH:
            print("❌ Invalid event UID (too long)")
            return False

        if not self.connect():
            return False

        self._rate_limiter.wait_if_needed()

        try:
            principal = self.client.principal()
            calendar = principal.calendar(name=calendar_name)
            event = calendar.event_by_uid(event_uid)
            event.delete()

            print("🗑️  Event deleted successfully")
            logger.info("Deleted event from %s", calendar_name)
            return True
        except NotFoundError:
            print("❌ Event or calendar not found")
            logger.error("Event/calendar not found")
            return False
        except DAVError:
            print("❌ CalDAV error")
            logger.error("Error deleting event")
            return False
        except Exception as exc:
            print("❌ Error deleting event")
            logger.error("Unexpected error deleting event: %s", type(exc).__name__)
            return False

    def update_event(
        self,
        calendar_name: str,
        event_uid: str,
        update_data: Dict[str, Any],
        recurrence_id: Optional[str] = None,
        mode: str = "single",
    ) -> bool:
        if not validate_calendar_name(calendar_name):
            print("❌ Invalid calendar name")
            logger.error("Invalid calendar name provided")
            return False

        if not event_uid or not isinstance(event_uid, str):
            print("❌ Valid event UID required")
            return False

        event_uid = event_uid.strip()
        if len(event_uid) > MAX_EVENT_UID_LENGTH:
            print("❌ Invalid event UID (too long)")
            return False

        if mode not in ["single", "all", "future"]:
            print("❌ Invalid mode. Must be 'single', 'all', or 'future'")
            return False

        if not _require_icalendar_runtime():
            return False

        if not self.connect():
            return False

        self._rate_limiter.wait_if_needed()

        try:
            principal = self.client.principal()
            calendar = principal.calendar(name=calendar_name)

            event_obj = calendar.event_by_uid(event_uid)
            parsed_calendar = iCal.from_ical(event_obj.data)
            event = next((component for component in parsed_calendar.walk() if component.name == "VEVENT"), None)
            if event is None:
                print("❌ Could not parse event data")
                return False

            has_rrule = "RRULE" in event
            if has_rrule and mode == "single" and recurrence_id:
                print(f"📅 Creating exception for instance: {recurrence_id}")
                return self._update_single_instance(calendar, recurrence_id, update_data, event)
            if has_rrule and mode == "future" and recurrence_id:
                print(f"🔮 Updating this and future instances from: {recurrence_id}")
                return self._update_future_instances(calendar, event_uid, recurrence_id, update_data, parsed_calendar, event)
            if has_rrule and mode == "all":
                print("🔁 Updating entire recurrence series")
                return self._update_all_instances(event_obj, update_data, parsed_calendar, event)

            print("✏️  Updating event")
            return self._update_simple(event_obj, update_data, parsed_calendar, event)

        except NotFoundError:
            print("❌ Event or calendar not found")
            logger.error("Event/calendar not found")
            return False
        except DAVError:
            print("❌ CalDAV error")
            logger.error("Error updating event")
            return False
        except Exception as exc:
            print("❌ Error updating event")
            logger.error("Unexpected error updating event: %s: %s", type(exc).__name__, str(exc))
            return False

    def _update_simple(self, event_obj: Any, update_data: Dict[str, Any], parsed_calendar: Any, event: Any) -> bool:
        self._apply_updates_to_event(event, update_data)
        if not self._validate_event_time_range(event):
            return False

        event_obj.data = parsed_calendar.to_ical()
        event_obj.save()

        print("✅ Event updated successfully")
        logger.info("Event updated")
        return True

    def _update_all_instances(self, event_obj: Any, update_data: Dict[str, Any], parsed_calendar: Any, event: Any) -> bool:
        self._apply_updates_to_event(event, update_data)
        if not self._validate_event_time_range(event):
            return False

        event_obj.data = parsed_calendar.to_ical()
        event_obj.save()

        print("✅ All instances updated successfully")
        logger.info("All recurrence instances updated")
        return True

    def _update_single_instance(
        self,
        calendar: Any,
        recurrence_id: str,
        update_data: Dict[str, Any],
        master_event: Any,
    ) -> bool:
        try:
            recurrence_dt = parse_iso_datetime(recurrence_id)

            exception_event = iEvent()
            exception_event.add("uid", master_event["UID"])
            exception_event.add("dtstamp", datetime.now(timezone.utc))
            exception_event.add("recurrence-id", recurrence_dt)

            for key in ["SUMMARY", "LOCATION", "DESCRIPTION", "STATUS", "PRIORITY"]:
                if key in master_event and key.lower() not in update_data:
                    exception_event.add(key.lower(), master_event[key])

            self._apply_updates_to_event(exception_event, update_data)

            if "dtstart" not in update_data:
                exception_event.add("dtstart", recurrence_dt)
            if "dtend" not in update_data:
                master_start = _coerce_dt(master_event["DTSTART"])
                master_end = _coerce_dt(master_event["DTEND"])
                if not master_start or not master_end:
                    print("❌ Could not derive master event duration")
                    return False
                exception_event.add("dtend", recurrence_dt + (master_end - master_start))

            if not self._validate_event_time_range(exception_event):
                return False

            exception_calendar = iCal()
            exception_calendar.add("prodid", "-//iCalendar Sync//EN")
            exception_calendar.add("version", "2.0")
            exception_calendar.add_component(exception_event)
            calendar.save_event(exception_calendar.to_ical().decode("utf-8"))

            print(f"✅ Exception created for instance: {recurrence_id}")
            logger.info("Created exception for recurrence instance")
            return True
        except ValueError as exc:
            print(f"❌ Invalid recurrence_id format: {exc}")
            return False

    def _update_future_instances(
        self,
        calendar: Any,
        event_uid: str,
        recurrence_id: str,
        update_data: Dict[str, Any],
        parsed_calendar: Any,
        master_event: Any,
    ) -> bool:
        try:
            split_dt = parse_iso_datetime(recurrence_id)

            if "RRULE" in master_event:
                # End original series immediately before the split moment.
                rrule = dict(master_event["RRULE"])
                rrule["UNTIL"] = [split_dt - timedelta(seconds=1)]
                master_event["RRULE"] = rrule

            event_obj = calendar.event_by_uid(event_uid)
            event_obj.data = parsed_calendar.to_ical()
            event_obj.save()

            new_calendar = iCal()
            new_calendar.add("prodid", "-//iCalendar Sync//EN")
            new_calendar.add("version", "2.0")

            new_event = iEvent()
            new_event.add("uid", str(uuid.uuid4()))
            new_event.add("dtstamp", datetime.now(timezone.utc))

            for key in ["SUMMARY", "LOCATION", "DESCRIPTION", "STATUS", "PRIORITY", "RRULE"]:
                if key in master_event and key.lower() not in update_data:
                    new_event.add(key.lower(), master_event[key])

            master_start = _coerce_dt(master_event["DTSTART"])
            master_end = _coerce_dt(master_event["DTEND"])
            if not master_start or not master_end:
                print("❌ Could not derive master event duration")
                return False

            duration = master_end - master_start
            new_event.add("dtstart", split_dt)
            new_event.add("dtend", split_dt + duration)

            self._apply_updates_to_event(new_event, update_data)
            if not self._validate_event_time_range(new_event):
                return False

            new_calendar.add_component(new_event)
            calendar.save_event(new_calendar.to_ical().decode("utf-8"))

            print(f"✅ Series split at {recurrence_id}. New series created with updates.")
            logger.info("Split recurrence series and created new series")
            return True
        except ValueError as exc:
            print(f"❌ Invalid recurrence_id format: {exc}")
            return False

    def _apply_updates_to_event(self, event: Any, update_data: Dict[str, Any]) -> None:
        if "summary" in update_data:
            event["SUMMARY"] = sanitize_text(update_data["summary"], MAX_SUMMARY_LENGTH)
        if "description" in update_data:
            event["DESCRIPTION"] = sanitize_text(update_data["description"], MAX_DESCRIPTION_LENGTH)
        if "location" in update_data:
            event["LOCATION"] = sanitize_text(update_data["location"], MAX_LOCATION_LENGTH)

        if "dtstart" in update_data:
            dtstart = update_data["dtstart"]
            if isinstance(dtstart, str):
                dtstart = parse_iso_datetime(dtstart)
            if dtstart.tzinfo is None:
                dtstart = dtstart.replace(tzinfo=timezone.utc)
            event["DTSTART"] = dtstart

        if "dtend" in update_data:
            dtend = update_data["dtend"]
            if isinstance(dtend, str):
                dtend = parse_iso_datetime(dtend)
            if dtend.tzinfo is None:
                dtend = dtend.replace(tzinfo=timezone.utc)
            event["DTEND"] = dtend

        if "status" in update_data:
            event["STATUS"] = update_data["status"]
        if "priority" in update_data and isinstance(update_data["priority"], int):
            event["PRIORITY"] = max(0, min(9, update_data["priority"]))

    def _validate_event_time_range(self, event: Any) -> bool:
        if "DTSTART" not in event or "DTEND" not in event:
            return True

        start_dt = _coerce_dt(event["DTSTART"])
        end_dt = _coerce_dt(event["DTEND"])
        if start_dt is None or end_dt is None:
            return True

        if end_dt <= start_dt:
            print("❌ Event end time must be after start time")
            logger.error("Invalid update: dtend must be after dtstart")
            return False
        return True


def cmd_setup(args: argparse.Namespace) -> None:
    """Interactive or headless setup of credentials."""
    print("\n🔧 iCalendar Sync Setup\n")

    non_interactive = getattr(args, "non_interactive", False)
    username_arg = getattr(args, "username", None)
    storage = getattr(args, "storage", "keyring")
    config_path_arg = getattr(args, "config", None)

    if non_interactive:
        email = (username_arg or os.getenv("ICLOUD_USERNAME") or "").strip()
        password = (os.getenv("ICLOUD_APP_PASSWORD") or "").strip()

        if not email:
            print("❌ ICLOUD_USERNAME is required in non-interactive mode")
            logger.error("Setup: Missing ICLOUD_USERNAME in non-interactive mode")
            return
        if not password:
            print("❌ ICLOUD_APP_PASSWORD is required in non-interactive mode")
            logger.error("Setup: Missing ICLOUD_APP_PASSWORD in non-interactive mode")
            return
        if not validate_secret_value(password):
            print("❌ Invalid ICLOUD_APP_PASSWORD value")
            logger.error("Setup: Invalid ICLOUD_APP_PASSWORD value")
            return
    else:
        print("To use iCalendar Sync, you need to configure your iCloud credentials.")
        print("⚠️  Use an App-Specific Password, NOT your regular Apple ID password.\n")
        print("Get it from: https://appleid.apple.com -> Sign-In & Security -> App-Specific Passwords\n")

        if username_arg:
            email = username_arg.strip()
            print(f"📧 Using provided email: {email}")
        else:
            email = input("📧 iCloud Email: ").strip()

        if not email:
            print("❌ Email cannot be empty")
            return

        if not validate_email(email):
            print("❌ Invalid email format")
            response = timed_input("Continue anyway? (y/n): ")
            if response is None or response.lower() != "y":
                print("Setup cancelled")
                return

        password = getpass.getpass("🔑 App-Specific Password (xxxx-xxxx-xxxx-xxxx): ").strip()
        if not password:
            print("❌ Password cannot be empty")
            return
        if not validate_secret_value(password):
            print("❌ Invalid password value")
            logger.error("Setup: Invalid password value")
            return

        if not all(char.isalnum() or char == "-" for char in password):
            print("⚠️  Password format looks unusual")
            response = timed_input("Are you sure this is correct? (y/n): ")
            if response is None or response.lower() != "y":
                print("Setup cancelled")
                return

    if not validate_email(email):
        logger.error("Setup: Invalid email format")
        print("❌ Invalid email format")
        return

    if storage == "file":
        saved_path = save_config_credentials(config_path_arg, email, password)
        if saved_path is None:
            print("❌ Failed to save credentials to config file")
            return
        print(f"\n✅ Credentials saved to config file: {saved_path}")
        print("   File permissions set to 0600")
        logger.info("Credentials stored in config file: %s", saved_path)
        print("🚀 You can now use iCalendar Sync!\n")
        return

    try:
        keyring.set_password("openclaw-icalendar", email, password)
        print("\n✅ Credentials saved securely to system keyring")
        logger.info("Credentials stored in keyring")
    except (AttributeError, KeyringError):
        logger.error("Setup: Could not access system keyring")
        suggested_path = resolve_config_path(config_path_arg)
        if KEYRING_IMPORT_ERROR:
            print("❌ Keyring backend is not available in this runtime.")
            print(f"   Reason: {KEYRING_IMPORT_ERROR}")
        else:
            print("❌ Could not access system keyring. Credentials were not persisted.")
        print(f"   Use file storage instead: icalendar-sync setup --storage file --config {suggested_path}")
        return

    print("🚀 You can now use iCalendar Sync!\n")


def build_manager(args: argparse.Namespace):
    provider = (getattr(args, "provider", None) or os.getenv("ICALENDAR_SYNC_PROVIDER", "auto")).strip()
    if provider not in ("auto", "caldav", "macos-native"):
        logger.warning("Unknown provider '%s', falling back to auto", provider)
        provider = "auto"

    if provider == "auto":
        provider = "caldav"

    if provider == "macos-native":
        return MacOSNativeCalendarManager()

    raw_storage = getattr(args, "storage", None)
    credential_source = (raw_storage or os.getenv("ICALENDAR_SYNC_STORAGE", "auto")).strip()
    ignore_keyring = bool(getattr(args, "ignore_keyring", False)) or is_truthy_env(os.getenv("ICALENDAR_SYNC_IGNORE_KEYRING", "0"))
    explicit_config = bool(getattr(args, "config", None))
    if ignore_keyring and credential_source in ("auto", "keyring"):
        credential_source = "env-only" if not explicit_config else "file"
    if explicit_config and raw_storage is None and credential_source == "auto":
        credential_source = "file"

    return CalendarManager(
        config_path=getattr(args, "config", None),
        user_agent=getattr(args, "user_agent", None),
        debug_http=getattr(args, "debug_http", False),
        credential_source=credential_source,
    )


def run_with_fallback(args: argparse.Namespace, operation_name: str, *operation_args, **operation_kwargs):
    provider_pref = (getattr(args, "provider", None) or os.getenv("ICALENDAR_SYNC_PROVIDER", "auto")).strip()
    if provider_pref not in ("auto", "caldav", "macos-native"):
        provider_pref = "auto"

    try:
        manager = build_manager(args)
    except RuntimeError as exc:
        if sys.platform == "darwin" and provider_pref in ("auto", "caldav"):
            print("⚠️  CalDAV provider unavailable, switching to macOS native provider")
            logger.warning("CalDAV unavailable, fallback to macOS native: %s", exc)
            manager = MacOSNativeCalendarManager()
        else:
            print(f"❌ {exc}")
            logger.error(str(exc))
            return None

    operation = getattr(manager, operation_name)
    result = operation(*operation_args, **operation_kwargs)

    should_fallback = (
        sys.platform == "darwin"
        and provider_pref == "auto"
        and isinstance(manager, CalendarManager)
        and (result is False or result is None or result == [])
        and not manager._connected
    )
    if should_fallback:
        print("⚠️  CalDAV authentication/connect failed, switching to macOS native provider")
        logger.warning("Fallback from CalDAV to macOS native provider")
        native_manager = MacOSNativeCalendarManager()
        native_operation = getattr(native_manager, operation_name)
        return native_operation(*operation_args, **operation_kwargs)

    return result


def cmd_list(args: argparse.Namespace) -> None:
    run_with_fallback(args, "list_calendars")


def _read_json_payload(value: str) -> Optional[Dict[str, Any]]:
    if os.path.isfile(value):
        content = safe_file_read(value, MAX_JSON_FILE_SIZE)
        if content is None:
            print("❌ Could not read JSON file")
            return None
        return json.loads(content)

    if len(value) > MAX_JSON_FILE_SIZE:
        print("❌ JSON data too large")
        return None
    return json.loads(value)


def cmd_get_events(args: argparse.Namespace) -> None:
    if not args.calendar:
        print("❌ Calendar name required")
        return
    run_with_fallback(args, "get_events", args.calendar, args.days_ahead)


def cmd_create_event(args: argparse.Namespace) -> None:
    if not args.calendar or not args.json:
        print("❌ Calendar and JSON data required")
        return

    try:
        event_data = _read_json_payload(args.json)
        if event_data is None:
            return

        if "dtstart" in event_data and isinstance(event_data["dtstart"], str):
            event_data["dtstart"] = parse_iso_datetime(event_data["dtstart"])
        if "dtend" in event_data and isinstance(event_data["dtend"], str):
            event_data["dtend"] = parse_iso_datetime(event_data["dtend"])

        check_conflicts = not args.no_conflict_check if hasattr(args, "no_conflict_check") else True
        auto_confirm = getattr(args, "yes", False)
        run_with_fallback(
            args,
            "create_event",
            args.calendar,
            event_data,
            check_conflicts=check_conflicts,
            auto_confirm=auto_confirm,
        )
    except json.JSONDecodeError as exc:
        print(f"❌ Invalid JSON: {exc}")
    except ValueError as exc:
        print(f"❌ Invalid datetime format: {exc}")


def cmd_delete_event(args: argparse.Namespace) -> None:
    if not args.calendar or not args.uid:
        print("❌ Calendar and event UID required")
        return
    run_with_fallback(args, "delete_event", args.calendar, args.uid)


def cmd_update_event(args: argparse.Namespace) -> None:
    if not args.calendar or not args.uid or not args.json:
        print("❌ Calendar, event UID, and JSON data required")
        return

    try:
        update_data = _read_json_payload(args.json)
        if update_data is None:
            return

        if "dtstart" in update_data and isinstance(update_data["dtstart"], str):
            update_data["dtstart"] = parse_iso_datetime(update_data["dtstart"])
        if "dtend" in update_data and isinstance(update_data["dtend"], str):
            update_data["dtend"] = parse_iso_datetime(update_data["dtend"])

        mode = getattr(args, "mode", "single")
        recurrence_id = getattr(args, "recurrence_id", None)

        run_with_fallback(
            args,
            "update_event",
            args.calendar,
            args.uid,
            update_data,
            recurrence_id=recurrence_id,
            mode=mode,
        )
    except json.JSONDecodeError as exc:
        print(f"❌ Invalid JSON: {exc}")
    except ValueError as exc:
        print(f"❌ Invalid datetime format: {exc}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="iCalendar Sync - Professional iCloud Calendar for OpenClaw",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  icalendar-sync setup
  icalendar-sync list
  icalendar-sync get --calendar "Work" --days 7
  icalendar-sync create --calendar "Personal" --json '{"summary":"Meeting","dtstart":"2026-02-10T14:00:00+03:00","dtend":"2026-02-10T15:00:00+03:00"}'
  icalendar-sync update --calendar "Work" --uid "event-id" --json '{"summary":"Updated Meeting"}'
  icalendar-sync update --calendar "Work" --uid "event-id" --json data.json --recurrence-id "2026-02-20T10:00:00" --mode single
  icalendar-sync delete --calendar "Work" --uid "event-id"
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    setup_parser = subparsers.add_parser("setup", help="Configure iCloud credentials")
    setup_parser.add_argument("--username", help="Apple ID email (optional in non-interactive mode)")
    setup_parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Non-interactive mode (reads ICLOUD_USERNAME and ICLOUD_APP_PASSWORD)",
    )
    setup_parser.add_argument(
        "--storage",
        choices=["keyring", "file"],
        default="keyring",
        help="Credential storage backend (default: keyring)",
    )
    setup_parser.add_argument(
        "--config",
        help="Path to YAML config with credentials (used for --storage file and runtime lookup)",
    )
    setup_parser.add_argument("--debug-http", action="store_true", help="Show detailed auth/network diagnostics")
    setup_parser.add_argument("--user-agent", help=f"Override CalDAV User-Agent (default: {DEFAULT_USER_AGENT})")
    setup_parser.set_defaults(func=cmd_setup)

    list_parser = subparsers.add_parser("list", help="List calendars")
    list_parser.add_argument("--provider", choices=["auto", "caldav", "macos-native"], default="auto", help="Calendar provider backend")
    list_parser.add_argument("--storage", choices=["auto", "keyring", "env", "file"], default=None, help="Credential source for CalDAV provider (default: auto)")
    list_parser.add_argument("--ignore-keyring", action="store_true", help="Ignore system keyring and use env/config credentials only")
    list_parser.add_argument("--config", help="Path to YAML config with credentials")
    list_parser.add_argument("--debug-http", action="store_true", help="Show detailed auth/network diagnostics")
    list_parser.add_argument("--user-agent", help=f"Override CalDAV User-Agent (default: {DEFAULT_USER_AGENT})")
    list_parser.set_defaults(func=cmd_list)

    get_parser = subparsers.add_parser("get", help="Get calendar events")
    get_parser.add_argument("--calendar", help="Calendar name")
    get_parser.add_argument("--days", type=int, default=7, dest="days_ahead", help=f"Days ahead to retrieve (default: 7, max: {MAX_DAYS_AHEAD})")
    get_parser.add_argument("--provider", choices=["auto", "caldav", "macos-native"], default="auto", help="Calendar provider backend")
    get_parser.add_argument("--storage", choices=["auto", "keyring", "env", "file"], default=None, help="Credential source for CalDAV provider (default: auto)")
    get_parser.add_argument("--ignore-keyring", action="store_true", help="Ignore system keyring and use env/config credentials only")
    get_parser.add_argument("--config", help="Path to YAML config with credentials")
    get_parser.add_argument("--debug-http", action="store_true", help="Show detailed auth/network diagnostics")
    get_parser.add_argument("--user-agent", help=f"Override CalDAV User-Agent (default: {DEFAULT_USER_AGENT})")
    get_parser.set_defaults(func=cmd_get_events)

    create_parser = subparsers.add_parser("create", help="Create calendar event")
    create_parser.add_argument("--calendar", required=True, help="Calendar name")
    create_parser.add_argument("--json", required=True, help="JSON with event data (file path or JSON string)")
    create_parser.add_argument("--no-conflict-check", action="store_true", help="Skip conflict detection")
    create_parser.add_argument("-y", "--yes", action="store_true", help="Auto-confirm without prompts")
    create_parser.add_argument("--provider", choices=["auto", "caldav", "macos-native"], default="auto", help="Calendar provider backend")
    create_parser.add_argument("--storage", choices=["auto", "keyring", "env", "file"], default=None, help="Credential source for CalDAV provider (default: auto)")
    create_parser.add_argument("--ignore-keyring", action="store_true", help="Ignore system keyring and use env/config credentials only")
    create_parser.add_argument("--config", help="Path to YAML config with credentials")
    create_parser.add_argument("--debug-http", action="store_true", help="Show detailed auth/network diagnostics")
    create_parser.add_argument("--user-agent", help=f"Override CalDAV User-Agent (default: {DEFAULT_USER_AGENT})")
    create_parser.set_defaults(func=cmd_create_event)

    update_parser = subparsers.add_parser("update", help="Update calendar event")
    update_parser.add_argument("--calendar", required=True, help="Calendar name")
    update_parser.add_argument("--uid", required=True, help="Event UID")
    update_parser.add_argument("--json", required=True, help="JSON with update data (file path or JSON string)")
    update_parser.add_argument("--recurrence-id", help="ISO datetime of specific instance (for recurring events)")
    update_parser.add_argument(
        "--mode",
        default="single",
        choices=["single", "all", "future"],
        help="Update mode: single instance, all instances, or this and future (default: single)",
    )
    update_parser.add_argument("--provider", choices=["auto", "caldav", "macos-native"], default="auto", help="Calendar provider backend")
    update_parser.add_argument("--storage", choices=["auto", "keyring", "env", "file"], default=None, help="Credential source for CalDAV provider (default: auto)")
    update_parser.add_argument("--ignore-keyring", action="store_true", help="Ignore system keyring and use env/config credentials only")
    update_parser.add_argument("--config", help="Path to YAML config with credentials")
    update_parser.add_argument("--debug-http", action="store_true", help="Show detailed auth/network diagnostics")
    update_parser.add_argument("--user-agent", help=f"Override CalDAV User-Agent (default: {DEFAULT_USER_AGENT})")
    update_parser.set_defaults(func=cmd_update_event)

    delete_parser = subparsers.add_parser("delete", help="Delete calendar event")
    delete_parser.add_argument("--calendar", required=True, help="Calendar name")
    delete_parser.add_argument("--uid", required=True, help="Event UID")
    delete_parser.add_argument("--provider", choices=["auto", "caldav", "macos-native"], default="auto", help="Calendar provider backend")
    delete_parser.add_argument("--storage", choices=["auto", "keyring", "env", "file"], default=None, help="Credential source for CalDAV provider (default: auto)")
    delete_parser.add_argument("--ignore-keyring", action="store_true", help="Ignore system keyring and use env/config credentials only")
    delete_parser.add_argument("--config", help="Path to YAML config with credentials")
    delete_parser.add_argument("--debug-http", action="store_true", help="Show detailed auth/network diagnostics")
    delete_parser.add_argument("--user-agent", help=f"Override CalDAV User-Agent (default: {DEFAULT_USER_AGENT})")
    delete_parser.set_defaults(func=cmd_delete_event)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        raise SystemExit(0)

    args.func(args)


if __name__ == "__main__":
    main()
