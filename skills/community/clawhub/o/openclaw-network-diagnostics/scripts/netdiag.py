#!/usr/bin/env python3
"""OpenClaw advanced network diagnostics for Telegram Bot API connectivity.

Pure network diagnostic utility:
- No LLM calls.
- No token consumption for AI inference.
- Async worker loops for active probing and deep telemetry logging.
"""

from __future__ import annotations

import argparse
import asyncio
import copy
import json
import math
import os
import re
import signal
import socket
import ssl
import subprocess
import sys
import time
import traceback
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any


LEVEL_RANK = {
    "ERROR": 0,
    "WARNING": 1,
    "INFO": 2,
    "DEBUG": 3,
    "TRACE": 4,
}

VERBOSITY_MAX_LEVEL = {
    "normal": LEVEL_RANK["INFO"],
    "debug": LEVEL_RANK["DEBUG"],
    "trace": LEVEL_RANK["TRACE"],
}

DEFAULT_CONFIG: dict[str, Any] = {
    "telegram": {
        "bot_token": "",
        "personal_chat_id": "",
    },
    "network": {
        "telegram_api_host": "api.telegram.org",
        "api_port": 443,
        "ipv4_only": True,
        "proxy_url": "",
        "public_dns_resolvers": ["1.1.1.1", "8.8.8.8"],
    },
    "intervals_sec": {
        "ping": 30,
        "traceroute": 300,
        "dns_reresolve": 300,
        "mtu_test": 900,
    },
    "timeouts_ms": {
        "connect": 4000,
        "request": 10000,
        "delivery_ack": 60000,
        "subprocess": 15000,
    },
    "retry": {
        "max_retries": 2,
        "backoff_base_ms": 500,
    },
    "delivery_verification": {
        "mode": "bot_api_ack",
        "ack_text_prefix": "NETDIAG_ACK",
        "callback_button_text": "Confirm delivery",
        "require_read_hint": False,
        "allow_probe_messages": True,
    },
    "logging": {
        "log_file_path": "./logs/netdiag.jsonl",
        "summary_file_path": "./logs/netdiag-summary.json",
        "max_file_size_mb": 50,
        "max_total_size_mb": 500,
        "verbosity": "normal",
        "redact_sensitive_fields": True,
    },
    "diagnostics": {
        "latency_anomaly_threshold_ms": 1200,
        "packet_loss_probe_count": 4,
        "tcp_keepalive_idle_sec": 30,
        "tcp_keepalive_interval_sec": 10,
        "tcp_keepalive_probe_count": 3,
        "max_response_bytes": 2_000_000,
        "mtu_min_payload": 1200,
        "mtu_max_payload": 1472,
    },
}

SENSITIVE_HEADERS = {
    "authorization",
    "proxy-authorization",
    "cookie",
    "set-cookie",
    "x-telegram-bot-api-secret-token",
}


@dataclass
class ProbeStats:
    started_monotonic: float = field(default_factory=time.monotonic)
    total_pings: int = 0
    failed_pings: int = 0
    latency_sum_ms: float = 0.0
    latency_count: int = 0
    max_latency_ms: float = 0.0
    connection_drops: int = 0
    dns_changes_detected: int = 0
    mtu_changes_detected: int = 0
    anomalies: int = 0
    total_downtime_ms: float = 0.0
    outage_started_monotonic: float | None = None

    def register_ping(self, success: bool, latency_ms: float | None) -> None:
        self.total_pings += 1
        if not success:
            self.failed_pings += 1
        if latency_ms is not None:
            self.latency_sum_ms += latency_ms
            self.latency_count += 1
            if latency_ms > self.max_latency_ms:
                self.max_latency_ms = latency_ms

    @property
    def avg_latency_ms(self) -> float | None:
        if self.latency_count == 0:
            return None
        return self.latency_sum_ms / self.latency_count

    @property
    def runtime_sec(self) -> float:
        return time.monotonic() - self.started_monotonic


def utc_now_iso_ms() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def parse_json_file(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Config root must be a JSON object")
    return data


def _find_default_config_path() -> Path:
    env_cfg = os.getenv("NETDIAG_CONFIG")
    if env_cfg:
        return Path(env_cfg).expanduser().resolve()
    script_dir = Path(__file__).resolve().parent
    candidate = script_dir.parent / "references" / "config.example.json"
    return candidate.resolve()


def _parse_proxy_host_port(proxy_url: str) -> tuple[str, int] | None:
    value = (proxy_url or "").strip()
    if not value:
        return None
    m = re.match(r"^(?:(?:http|https)://)?([A-Za-z0-9._-]+)(?::(\d+))?$", value)
    if not m:
        return None
    host = m.group(1)
    port = int(m.group(2) or 8080)
    return host, port


def validate_config_errors(cfg: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if not cfg.get("telegram", {}).get("bot_token"):
        errors.append("telegram.bot_token is required")
    if not cfg.get("telegram", {}).get("personal_chat_id"):
        errors.append("telegram.personal_chat_id is required")

    mode = cfg.get("delivery_verification", {}).get("mode")
    if mode not in {"bot_api_ack", "user_reply_ack", "callback_ack"}:
        errors.append("delivery_verification.mode must be one of: bot_api_ack, user_reply_ack, callback_ack")

    verbosity = str(cfg.get("logging", {}).get("verbosity"))
    if verbosity not in VERBOSITY_MAX_LEVEL:
        errors.append("logging.verbosity must be one of: normal, debug, trace")

    for section, key in [
        ("intervals_sec", "ping"),
        ("intervals_sec", "traceroute"),
        ("intervals_sec", "dns_reresolve"),
        ("intervals_sec", "mtu_test"),
        ("timeouts_ms", "connect"),
        ("timeouts_ms", "request"),
        ("timeouts_ms", "delivery_ack"),
        ("timeouts_ms", "subprocess"),
    ]:
        try:
            value = int(cfg[section][key])
            if value <= 0:
                errors.append(f"{section}.{key} must be > 0")
        except Exception:
            errors.append(f"{section}.{key} must be an integer > 0")

    try:
        max_total = int(cfg["logging"]["max_total_size_mb"])
        if max_total <= 0:
            errors.append("logging.max_total_size_mb must be > 0")
    except Exception:
        errors.append("logging.max_total_size_mb must be an integer > 0")

    try:
        max_file = int(cfg["logging"]["max_file_size_mb"])
        if max_file <= 0:
            errors.append("logging.max_file_size_mb must be > 0")
    except Exception:
        errors.append("logging.max_file_size_mb must be an integer > 0")
        max_file = None

    if 'max_total' in locals() and 'max_file' in locals() and isinstance(max_total, int) and isinstance(max_file, int):
        if max_file > max_total:
            errors.append("logging.max_file_size_mb must be <= logging.max_total_size_mb")

    proxy_value = str(cfg.get("network", {}).get("proxy_url") or "").strip()
    if proxy_value and _parse_proxy_host_port(proxy_value) is None:
        errors.append("network.proxy_url must be like http://127.0.0.1:1082")

    return errors


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def is_process_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


class JsonRotatingLogger:
    def __init__(
        self,
        log_path: Path,
        max_file_size_mb: int,
        max_total_size_mb: int,
        verbosity: str,
    ) -> None:
        self.log_path = log_path
        self.max_file_size_bytes = max(1, max_file_size_mb) * 1024 * 1024
        self.max_total_size_bytes = max(1, max_total_size_mb) * 1024 * 1024
        self.max_level = VERBOSITY_MAX_LEVEL.get(verbosity, VERBOSITY_MAX_LEVEL["normal"])
        self._lock = Lock()
        ensure_parent(self.log_path)

    def _should_log(self, level: str) -> bool:
        return LEVEL_RANK.get(level, LEVEL_RANK["INFO"]) <= self.max_level

    def _rotated_files(self) -> list[Path]:
        files = []
        if self.log_path.exists():
            files.append(self.log_path)
        prefix = f"{self.log_path.name}."
        for candidate in self.log_path.parent.glob(f"{self.log_path.name}.*"):
            suffix = candidate.name[len(prefix) :]
            if suffix.isdigit():
                files.append(candidate)
        return files

    def _rotation_index(self, path: Path) -> int:
        if path == self.log_path:
            return 0
        suffix = path.name.rsplit(".", 1)[-1]
        if suffix.isdigit():
            return int(suffix)
        return 999999

    def _rotate_if_needed(self, incoming_line_bytes: int) -> None:
        current_size = self.log_path.stat().st_size if self.log_path.exists() else 0
        if current_size + incoming_line_bytes <= self.max_file_size_bytes:
            return

        rotated = [p for p in self._rotated_files() if p != self.log_path]
        rotated.sort(key=self._rotation_index, reverse=True)
        for path in rotated:
            idx = self._rotation_index(path)
            target = self.log_path.parent / f"{self.log_path.name}.{idx + 1}"
            path.rename(target)

        if self.log_path.exists():
            self.log_path.rename(self.log_path.parent / f"{self.log_path.name}.1")

    def _trim_total_size(self) -> None:
        files = self._rotated_files()
        if not files:
            return

        files.sort(key=lambda p: (self._rotation_index(p), p.stat().st_mtime if p.exists() else 0), reverse=True)
        total = sum(path.stat().st_size for path in files if path.exists())
        if total <= self.max_total_size_bytes:
            return

        # Delete oldest rotated files first. Keep active file whenever possible.
        deletable = [p for p in files if p != self.log_path]
        deletable.sort(key=self._rotation_index, reverse=True)
        for path in deletable:
            if total <= self.max_total_size_bytes:
                break
            if path.exists():
                size = path.stat().st_size
                path.unlink(missing_ok=True)
                total -= size

    def log(self, entry: dict[str, Any]) -> None:
        level = str(entry.get("level", "INFO")).upper()
        if not self._should_log(level):
            return

        line = json.dumps(entry, ensure_ascii=True, separators=(",", ":")) + "\n"
        encoded_len = len(line.encode("utf-8"))
        with self._lock:
            self._rotate_if_needed(encoded_len)
            with self.log_path.open("a", encoding="utf-8") as handle:
                handle.write(line)
            self._trim_total_size()


class NetworkDiagnosticWorker:
    def __init__(self, config: dict[str, Any], config_path: Path, pid_file: Path | None = None) -> None:
        self.config = config
        self.config_path = config_path
        self.pid_file = pid_file

        self.telegram_host: str = str(config["network"]["telegram_api_host"])
        self.telegram_port: int = int(config["network"]["api_port"])
        self.proxy_url: str = str(config["network"].get("proxy_url", "") or "").strip()
        self.proxy_endpoint = _parse_proxy_host_port(self.proxy_url)
        self.bot_token: str = str(config["telegram"]["bot_token"])
        self.personal_chat_id: str = str(config["telegram"]["personal_chat_id"])

        self.public_dns_resolvers: list[str] = list(config["network"]["public_dns_resolvers"])
        self.ping_interval_sec: int = int(config["intervals_sec"]["ping"])
        self.traceroute_interval_sec: int = int(config["intervals_sec"]["traceroute"])
        self.dns_interval_sec: int = int(config["intervals_sec"]["dns_reresolve"])
        self.mtu_interval_sec: int = int(config["intervals_sec"]["mtu_test"])

        self.connect_timeout_ms: int = int(config["timeouts_ms"]["connect"])
        self.request_timeout_ms: int = int(config["timeouts_ms"]["request"])
        self.delivery_ack_timeout_ms: int = int(config["timeouts_ms"]["delivery_ack"])
        self.subprocess_timeout_ms: int = int(config["timeouts_ms"]["subprocess"])

        self.max_retries: int = int(config["retry"]["max_retries"])
        self.backoff_base_ms: int = int(config["retry"]["backoff_base_ms"])

        self.delivery_mode: str = str(config["delivery_verification"]["mode"])
        self.ack_text_prefix: str = str(config["delivery_verification"]["ack_text_prefix"])
        self.callback_button_text: str = str(config["delivery_verification"]["callback_button_text"])
        self.require_read_hint: bool = bool(config["delivery_verification"]["require_read_hint"])
        self.allow_probe_messages: bool = bool(config["delivery_verification"]["allow_probe_messages"])

        self.log_path = self._resolve_path(config["logging"]["log_file_path"])
        self.summary_path = self._resolve_path(config["logging"]["summary_file_path"])
        self.redact_sensitive_fields: bool = bool(config["logging"]["redact_sensitive_fields"])

        self.latency_anomaly_threshold_ms: float = float(config["diagnostics"]["latency_anomaly_threshold_ms"])
        self.packet_loss_probe_count: int = int(config["diagnostics"]["packet_loss_probe_count"])
        self.tcp_keepalive_idle_sec: int = int(config["diagnostics"]["tcp_keepalive_idle_sec"])
        self.tcp_keepalive_interval_sec: int = int(config["diagnostics"]["tcp_keepalive_interval_sec"])
        self.tcp_keepalive_probe_count: int = int(config["diagnostics"]["tcp_keepalive_probe_count"])
        self.max_response_bytes: int = int(config["diagnostics"]["max_response_bytes"])
        self.mtu_min_payload: int = int(config["diagnostics"]["mtu_min_payload"])
        self.mtu_max_payload: int = int(config["diagnostics"]["mtu_max_payload"])

        self.logger = JsonRotatingLogger(
            log_path=self.log_path,
            max_file_size_mb=int(config["logging"]["max_file_size_mb"]),
            max_total_size_mb=int(config["logging"]["max_total_size_mb"]),
            verbosity=str(config["logging"]["verbosity"]),
        )

        self.ssl_context = ssl.create_default_context()
        self.stop_event = asyncio.Event()
        self.stats = ProbeStats()

        self.last_dns_snapshot: dict[str, Any] = {
            "host": self.telegram_host,
            "resolved_at_utc": None,
            "system_records": [],
            "public_records": {},
            "selected_ipv4": None,
            "selected_from": None,
        }
        self.last_dns_resolved_monotonic: float | None = None
        self.current_destination_ip: str | None = None
        self.last_dns_fingerprint: tuple[str, ...] = tuple()
        self.last_mtu: int | None = None
        self.last_tls_fingerprint: tuple[str | None, str | None] | None = None

        self.update_offset: int = 0

    def _resolve_path(self, raw_path: str) -> Path:
        path = Path(str(raw_path))
        if path.is_absolute():
            return path
        return (self.config_path.parent / path).resolve()

    def _masked_path(self, path: str) -> str:
        if not self.redact_sensitive_fields:
            return path
        return path.replace(self.bot_token, "<BOT_TOKEN>")

    def _redact_headers(self, headers: dict[str, str]) -> dict[str, str]:
        if not self.redact_sensitive_fields:
            return headers
        redacted: dict[str, str] = {}
        for key, value in headers.items():
            if key.lower() in SENSITIVE_HEADERS:
                redacted[key] = "<REDACTED>"
            else:
                redacted[key] = value
        return redacted

    def _default_log_entry(self, event: str, level: str) -> dict[str, Any]:
        return {
            "timestamp_utc": utc_now_iso_ms(),
            "event": event,
            "level": level,
            "source_ip": None,
            "source_port": None,
            "destination_ip": self.current_destination_ip,
            "destination_port": self.telegram_port,
            "dns_resolution": self.last_dns_snapshot,
            "tls": {
                "version": None,
                "cipher": None,
                "handshake_duration_ms": None,
                "session_reused": None,
                "renegotiation_detected": False,
            },
            "http_request": {
                "method": None,
                "path": None,
                "headers": {},
                "payload_bytes_sent": 0,
            },
            "http_response": {
                "status_code": None,
                "headers": {},
                "payload_bytes_received": 0,
            },
            "payload_bytes": {
                "sent": 0,
                "received": 0,
            },
            "round_trip_latency_ms": None,
            "tcp_state": "unknown",
            "retries": 0,
            "timeout_ms": None,
            "socket_error": None,
            "packet_loss_indicator": None,
            "connection_reset": False,
            "rate_limit": {
                "detected": False,
                "retry_after_sec": None,
                "raw": None,
            },
            "exception_stacktrace": None,
            "details": {},
        }

    def log(self, event: str, level: str = "INFO", **kwargs: Any) -> None:
        entry = self._default_log_entry(event=event, level=level)
        for key, value in kwargs.items():
            entry[key] = value
        self.logger.log(entry)

    async def run(self) -> None:
        self._write_pid_file()
        self._register_signal_handlers()

        self.log(
            "worker_start",
            level="INFO",
            details={
                "config_path": str(self.config_path),
                "log_path": str(self.log_path),
                "summary_path": str(self.summary_path),
                "delivery_mode": self.delivery_mode,
                "proxy_url": self.proxy_url or None,
            },
        )

        await self.resolve_dns(force=True)

        tasks = [
            asyncio.create_task(self.active_monitor_loop(), name="active_monitor_loop"),
            asyncio.create_task(self.dns_loop(), name="dns_loop"),
            asyncio.create_task(self.traceroute_loop(), name="traceroute_loop"),
            asyncio.create_task(self.mtu_loop(), name="mtu_loop"),
        ]

        await self.stop_event.wait()

        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

        summary = self.build_summary()
        self.write_summary(summary)

        print(json.dumps(summary, ensure_ascii=True, indent=2))

        self.log("worker_stop", level="INFO", details={"summary": summary})
        self._cleanup_pid_file()

    def stop(self) -> None:
        self.stop_event.set()

    def _register_signal_handlers(self) -> None:
        loop = asyncio.get_running_loop()

        def _handle_signal(signame: str) -> None:
            self.log("signal_received", level="INFO", details={"signal": signame})
            self.stop_event.set()

        for signame in ("SIGINT", "SIGTERM"):
            if hasattr(signal, signame):
                sig = getattr(signal, signame)
                try:
                    loop.add_signal_handler(sig, _handle_signal, signame)
                except NotImplementedError:
                    pass

    def _write_pid_file(self) -> None:
        if self.pid_file is None:
            return
        ensure_parent(self.pid_file)
        self.pid_file.write_text(str(os.getpid()), encoding="utf-8")

    def _cleanup_pid_file(self) -> None:
        if self.pid_file is None:
            return
        self.pid_file.unlink(missing_ok=True)

    def build_summary(self) -> dict[str, Any]:
        return {
            "timestamp_utc": utc_now_iso_ms(),
            "total_runtime_sec": round(self.stats.runtime_sec, 3),
            "total_pings": self.stats.total_pings,
            "failed_pings": self.stats.failed_pings,
            "average_latency_ms": round(self.stats.avg_latency_ms, 3) if self.stats.avg_latency_ms is not None else None,
            "max_latency_ms": round(self.stats.max_latency_ms, 3) if self.stats.max_latency_ms else None,
            "connection_drops": self.stats.connection_drops,
            "dns_changes_detected": self.stats.dns_changes_detected,
            "mtu_changes_detected": self.stats.mtu_changes_detected,
            "anomalies": self.stats.anomalies,
            "total_downtime_ms": round(self.stats.total_downtime_ms, 3),
            "current_destination_ip": self.current_destination_ip,
            "config_path": str(self.config_path),
            "log_file_path": str(self.log_path),
        }

    def write_summary(self, summary: dict[str, Any]) -> None:
        ensure_parent(self.summary_path)
        self.summary_path.write_text(json.dumps(summary, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")

    async def dns_loop(self) -> None:
        while not self.stop_event.is_set():
            try:
                await self.resolve_dns(force=False)
            except Exception:
                self.log(
                    "dns_loop_error",
                    level="ERROR",
                    exception_stacktrace=traceback.format_exc(),
                )
            await self.sleep_or_stop(self.dns_interval_sec)

    async def traceroute_loop(self) -> None:
        while not self.stop_event.is_set():
            try:
                await self.run_traceroute()
            except Exception:
                self.log(
                    "traceroute_loop_error",
                    level="ERROR",
                    exception_stacktrace=traceback.format_exc(),
                )
            await self.sleep_or_stop(self.traceroute_interval_sec)

    async def mtu_loop(self) -> None:
        while not self.stop_event.is_set():
            try:
                await self.run_mtu_discovery()
            except Exception:
                self.log(
                    "mtu_loop_error",
                    level="ERROR",
                    exception_stacktrace=traceback.format_exc(),
                )
            await self.sleep_or_stop(self.mtu_interval_sec)

    async def active_monitor_loop(self) -> None:
        while not self.stop_event.is_set():
            cycle_started = time.monotonic()
            cycle_id = str(int(time.time() * 1000))

            await self.resolve_dns(force=False)
            ping_success, ping_latency, ping_details = await self.perform_bot_api_ping(cycle_id)
            await self.run_packet_loss_probe(cycle_id)

            delivery_result = None
            if self.allow_probe_messages:
                delivery_result = await self.delivery_verification_cycle(cycle_id)

            self._update_outage_state(ping_success)

            self.stats.register_ping(success=ping_success, latency_ms=ping_latency)
            if ping_latency is not None and ping_latency > self.latency_anomaly_threshold_ms:
                self.stats.anomalies += 1
                self.log(
                    "latency_anomaly",
                    level="WARNING",
                    round_trip_latency_ms=ping_latency,
                    details={
                        "threshold_ms": self.latency_anomaly_threshold_ms,
                        "cycle_id": cycle_id,
                        "ping_details": ping_details,
                    },
                )

            self.log(
                "active_cycle_result",
                level="INFO" if ping_success else "WARNING",
                round_trip_latency_ms=ping_latency,
                retries=ping_details.get("retries", 0) if isinstance(ping_details, dict) else 0,
                details={
                    "cycle_id": cycle_id,
                    "ping_success": ping_success,
                    "delivery_result": delivery_result,
                },
            )

            elapsed = time.monotonic() - cycle_started
            remaining = max(0.0, self.ping_interval_sec - elapsed)
            await self.sleep_or_stop(remaining)

    async def sleep_or_stop(self, seconds: float) -> None:
        if seconds <= 0:
            return
        try:
            await asyncio.wait_for(self.stop_event.wait(), timeout=seconds)
        except asyncio.TimeoutError:
            return

    def _update_outage_state(self, ping_success: bool) -> None:
        now = time.monotonic()
        if ping_success:
            if self.stats.outage_started_monotonic is not None:
                downtime_ms = (now - self.stats.outage_started_monotonic) * 1000.0
                self.stats.total_downtime_ms += downtime_ms
                self.log(
                    "recovery_detected",
                    level="INFO",
                    details={
                        "downtime_ms": round(downtime_ms, 3),
                        "reconnection_attempt_duration_ms": round(downtime_ms, 3),
                    },
                )
                self.stats.outage_started_monotonic = None
        else:
            if self.stats.outage_started_monotonic is None:
                self.stats.outage_started_monotonic = now
                self.stats.connection_drops += 1
                self.log("connectivity_drop", level="WARNING")

    async def resolve_dns(self, force: bool) -> None:
        now = time.monotonic()
        if not force and isinstance(self.last_dns_resolved_monotonic, float):
            if now - self.last_dns_resolved_monotonic < self.dns_interval_sec:
                return

        system_records = await self.run_dig(None)
        public_records: dict[str, list[dict[str, Any]]] = {}
        for resolver in self.public_dns_resolvers:
            public_records[resolver] = await self.run_dig(resolver)

        selected_ip = None
        selected_from = None
        if system_records:
            selected_ip = system_records[0]["ip"]
            selected_from = "system"
        else:
            for resolver in self.public_dns_resolvers:
                if public_records.get(resolver):
                    selected_ip = public_records[resolver][0]["ip"]
                    selected_from = resolver
                    break

        # Fallback without TTL if dig fails.
        if selected_ip is None:
            fallback_ips = await asyncio.to_thread(self.resolve_ipv4_fallback)
            if fallback_ips:
                selected_ip = fallback_ips[0]
                selected_from = "socket_getaddrinfo"
                if not system_records:
                    system_records = [{"ip": ip, "ttl": None, "record_type": "A"} for ip in fallback_ips]

        new_snapshot = {
            "host": self.telegram_host,
            "resolved_at_utc": utc_now_iso_ms(),
            "system_records": system_records,
            "public_records": public_records,
            "selected_ipv4": selected_ip,
            "selected_from": selected_from,
        }

        fingerprint = tuple(sorted({r["ip"] for r in system_records}))
        dns_changed = bool(self.last_dns_fingerprint and fingerprint and fingerprint != self.last_dns_fingerprint)
        if dns_changed:
            self.stats.dns_changes_detected += 1

        self.last_dns_snapshot = new_snapshot
        self.last_dns_resolved_monotonic = now
        self.last_dns_fingerprint = fingerprint
        self.current_destination_ip = selected_ip

        self.log(
            "dns_resolved",
            level="INFO" if selected_ip else "ERROR",
            details={
                "dns_changed": dns_changed,
                "selected_ip": selected_ip,
                "selected_from": selected_from,
                "system_record_count": len(system_records),
                "public_record_count": sum(len(v) for v in public_records.values()),
            },
            dns_resolution={k: v for k, v in new_snapshot.items() if not k.startswith("_")},
        )

    async def run_dig(self, resolver: str | None) -> list[dict[str, Any]]:
        args = ["dig", "+nocmd", "+noall", "+answer"]
        if resolver:
            args.append(f"@{resolver}")
        args.extend([self.telegram_host, "A"])

        result = await self.run_subprocess(args, timeout_ms=self.subprocess_timeout_ms)
        if result["returncode"] != 0:
            return []

        records: list[dict[str, Any]] = []
        for line in result["stdout"].splitlines():
            line = line.strip()
            if not line:
                continue
            parts = re.split(r"\s+", line)
            if len(parts) < 5:
                continue
            try:
                ttl = int(parts[1])
            except ValueError:
                ttl = None
            record_type = parts[3]
            ip = parts[4]
            if record_type != "A":
                continue
            if not self._is_valid_ipv4(ip):
                continue
            records.append({
                "resolver": resolver or "system",
                "ip": ip,
                "ttl": ttl,
                "record_type": record_type,
            })
        return records

    def resolve_ipv4_fallback(self) -> list[str]:
        ips = []
        try:
            infos = socket.getaddrinfo(self.telegram_host, self.telegram_port, socket.AF_INET, socket.SOCK_STREAM)
            for info in infos:
                ip = info[4][0]
                if ip not in ips:
                    ips.append(ip)
        except socket.gaierror:
            return []
        return ips

    def _is_valid_ipv4(self, value: str) -> bool:
        try:
            socket.inet_aton(value)
        except OSError:
            return False
        return value.count(".") == 3

    async def run_traceroute(self) -> None:
        target = self.current_destination_ip or self.telegram_host
        args = ["traceroute", "-n", "-q", "1", "-w", "1", target]
        result = await self.run_subprocess(args, timeout_ms=self.subprocess_timeout_ms)

        hops = []
        for line in result["stdout"].splitlines():
            match = re.match(r"^\s*(\d+)\s+(.*)$", line)
            if not match:
                continue
            hop_no = int(match.group(1))
            payload = match.group(2).strip()
            if payload.startswith("*"):
                hops.append({"hop": hop_no, "ip": None, "latency_ms": None})
                continue
            parts = payload.split()
            ip = parts[0] if parts else None
            latency = None
            latency_match = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*ms", payload)
            if latency_match:
                latency = float(latency_match.group(1))
            hops.append({"hop": hop_no, "ip": ip, "latency_ms": latency})

        self.log(
            "traceroute_result",
            level="INFO" if result["returncode"] == 0 else "WARNING",
            details={
                "target": target,
                "returncode": result["returncode"],
                "stderr": result["stderr"],
                "hop_count": len(hops),
                "hops": hops,
            },
        )

    async def run_mtu_discovery(self) -> None:
        target = self.current_destination_ip or self.telegram_host
        low = self.mtu_min_payload
        high = self.mtu_max_payload
        best = None
        attempts = []

        while low <= high and not self.stop_event.is_set():
            mid = (low + high) // 2
            ok, stdout, stderr = await self.ping_df(target, payload_size=mid)
            attempts.append({
                "payload_size": mid,
                "success": ok,
                "stdout": stdout.strip(),
                "stderr": stderr.strip(),
            })
            if ok:
                best = mid
                low = mid + 1
            else:
                high = mid - 1

        detected_mtu = best + 28 if best is not None else None
        mtu_changed = self.last_mtu is not None and detected_mtu is not None and detected_mtu != self.last_mtu
        if mtu_changed:
            self.stats.mtu_changes_detected += 1

        if detected_mtu is not None:
            self.last_mtu = detected_mtu

        self.log(
            "mtu_discovery",
            level="INFO" if detected_mtu is not None else "WARNING",
            details={
                "target": target,
                "detected_mtu": detected_mtu,
                "changed": mtu_changed,
                "attempts": attempts,
            },
        )

    async def ping_df(self, target: str, payload_size: int) -> tuple[bool, str, str]:
        args = ["ping", "-n", "-D", "-c", "1", "-W", "1000", "-s", str(payload_size), target]
        result = await self.run_subprocess(args, timeout_ms=self.subprocess_timeout_ms)
        return result["returncode"] == 0, result["stdout"], result["stderr"]

    async def run_packet_loss_probe(self, cycle_id: str) -> None:
        target = self.current_destination_ip or self.telegram_host
        args = [
            "ping",
            "-n",
            "-c",
            str(self.packet_loss_probe_count),
            "-W",
            "1000",
            target,
        ]
        result = await self.run_subprocess(args, timeout_ms=self.subprocess_timeout_ms)
        output = (result["stdout"] or "") + "\n" + (result["stderr"] or "")

        packet_loss = None
        avg_latency = None
        loss_match = re.search(r"([0-9]+(?:\.[0-9]+)?)%\s+packet\s+loss", output)
        if loss_match:
            packet_loss = float(loss_match.group(1))

        avg_match = re.search(r"=\s*([0-9]+(?:\.[0-9]+)?)/([0-9]+(?:\.[0-9]+)?)/([0-9]+(?:\.[0-9]+)?)/", output)
        if avg_match:
            avg_latency = float(avg_match.group(2))

        self.log(
            "packet_loss_probe",
            level="INFO" if result["returncode"] == 0 else "WARNING",
            packet_loss_indicator={
                "percent": packet_loss,
                "probe_count": self.packet_loss_probe_count,
                "avg_latency_ms": avg_latency,
            },
            details={
                "cycle_id": cycle_id,
                "target": target,
                "returncode": result["returncode"],
            },
        )

    async def perform_bot_api_ping(self, cycle_id: str) -> tuple[bool, float | None, dict[str, Any]]:
        result = await self.telegram_request(
            method_name="getMe",
            method="GET",
            payload=None,
            cycle_id=cycle_id,
        )
        success = bool(result.get("success") and result.get("telegram_ok"))
        latency = result.get("round_trip_latency_ms")

        return success, latency, {
            "retries": result.get("retries", 0),
            "status_code": result.get("status_code"),
            "error": result.get("error"),
        }

    async def delivery_verification_cycle(self, cycle_id: str) -> dict[str, Any]:
        text = f"[NETDIAG] cycle={cycle_id} mode={self.delivery_mode}"

        reply_markup = None
        if self.delivery_mode == "callback_ack":
            reply_markup = {
                "inline_keyboard": [
                    [
                        {
                            "text": self.callback_button_text,
                            "callback_data": f"ACK:{cycle_id}",
                        }
                    ]
                ]
            }

        payload = {
            "chat_id": self.personal_chat_id,
            "text": text,
            "disable_notification": True,
        }
        if reply_markup is not None:
            payload["reply_markup"] = reply_markup

        send_started = time.monotonic()
        send_result = await self.telegram_request(
            method_name="sendMessage",
            method="POST",
            payload=payload,
            cycle_id=cycle_id,
        )

        if not send_result.get("success") or not send_result.get("telegram_ok"):
            return {
                "mode": self.delivery_mode,
                "sent": False,
                "delivery_confirmed": False,
                "read_hint_detected": False,
                "error": send_result.get("error"),
            }

        send_json = send_result.get("telegram_json") or {}
        message_id = (((send_json.get("result") or {}).get("message_id")) if isinstance(send_json, dict) else None)

        if self.delivery_mode == "bot_api_ack":
            delivery_ms = (time.monotonic() - send_started) * 1000.0
            return {
                "mode": self.delivery_mode,
                "sent": True,
                "delivery_confirmed": True,
                "read_hint_detected": False,
                "delivery_ack_latency_ms": round(delivery_ms, 3),
                "message_id": message_id,
            }

        ack_result = await self.wait_for_delivery_ack(cycle_id=cycle_id, message_id=message_id)
        if ack_result.get("delivery_confirmed"):
            delivery_ms = (time.monotonic() - send_started) * 1000.0
            ack_result["delivery_ack_latency_ms"] = round(delivery_ms, 3)

        if self.require_read_hint and not ack_result.get("read_hint_detected"):
            ack_result["delivery_confirmed"] = False
            ack_result["error"] = "read_hint_required_but_missing"

        return ack_result

    async def wait_for_delivery_ack(self, cycle_id: str, message_id: int | None) -> dict[str, Any]:
        deadline = time.monotonic() + (self.delivery_ack_timeout_ms / 1000.0)

        while time.monotonic() < deadline and not self.stop_event.is_set():
            payload = {
                "timeout": 10,
                "offset": self.update_offset,
                "allowed_updates": ["message", "callback_query"],
            }
            updates_result = await self.telegram_request(
                method_name="getUpdates",
                method="POST",
                payload=payload,
                cycle_id=cycle_id,
            )

            if not updates_result.get("success") or not updates_result.get("telegram_ok"):
                await self.sleep_or_stop(1)
                continue

            updates = (((updates_result.get("telegram_json") or {}).get("result")) if updates_result.get("telegram_json") else [])
            if not isinstance(updates, list):
                updates = []

            for update in updates:
                if not isinstance(update, dict):
                    continue
                update_id = update.get("update_id")
                if isinstance(update_id, int):
                    self.update_offset = max(self.update_offset, update_id + 1)

                if self.delivery_mode == "user_reply_ack":
                    if self._matches_user_reply_ack(update, cycle_id, message_id):
                        return {
                            "mode": self.delivery_mode,
                            "sent": True,
                            "delivery_confirmed": True,
                            "read_hint_detected": True,
                            "message_id": message_id,
                        }

                if self.delivery_mode == "callback_ack":
                    if self._matches_callback_ack(update, cycle_id):
                        return {
                            "mode": self.delivery_mode,
                            "sent": True,
                            "delivery_confirmed": True,
                            "read_hint_detected": True,
                            "message_id": message_id,
                        }

        return {
            "mode": self.delivery_mode,
            "sent": True,
            "delivery_confirmed": False,
            "read_hint_detected": False,
            "message_id": message_id,
            "error": "delivery_ack_timeout",
        }

    def _matches_user_reply_ack(self, update: dict[str, Any], cycle_id: str, message_id: int | None) -> bool:
        message = update.get("message")
        if not isinstance(message, dict):
            return False

        chat = message.get("chat")
        chat_id = str(chat.get("id")) if isinstance(chat, dict) else ""
        if chat_id != self.personal_chat_id:
            return False

        text = str(message.get("text") or "")
        reply_to = message.get("reply_to_message")
        reply_to_id = reply_to.get("message_id") if isinstance(reply_to, dict) else None

        if message_id is not None and reply_to_id == message_id:
            return True

        if self.ack_text_prefix and self.ack_text_prefix in text:
            return True

        return cycle_id in text

    def _matches_callback_ack(self, update: dict[str, Any], cycle_id: str) -> bool:
        callback_query = update.get("callback_query")
        if not isinstance(callback_query, dict):
            return False

        data = str(callback_query.get("data") or "")
        message = callback_query.get("message")
        if not isinstance(message, dict):
            return False

        chat = message.get("chat")
        chat_id = str(chat.get("id")) if isinstance(chat, dict) else ""
        if chat_id != self.personal_chat_id:
            return False

        return data == f"ACK:{cycle_id}"

    async def telegram_request(
        self,
        method_name: str,
        method: str,
        payload: dict[str, Any] | None,
        cycle_id: str,
    ) -> dict[str, Any]:
        retries = 0
        errors: list[str] = []

        for attempt in range(self.max_retries + 1):
            response = await asyncio.to_thread(
                self.http_request_sync,
                method_name,
                method,
                payload,
            )

            status_code = response.get("status_code")
            telegram_json = response.get("telegram_json")
            telegram_ok = bool(isinstance(telegram_json, dict) and telegram_json.get("ok") is True)
            retry_after = self.extract_retry_after(status_code, response.get("response_headers", {}), telegram_json)
            rate_limit_detected = bool(status_code == 429 or retry_after is not None)

            response["retries"] = attempt
            response["telegram_ok"] = telegram_ok
            response["rate_limit"] = {
                "detected": rate_limit_detected,
                "retry_after_sec": retry_after,
                "raw": {
                    "status_code": status_code,
                    "description": (telegram_json or {}).get("description") if isinstance(telegram_json, dict) else None,
                },
            }

            level = "INFO"
            if not response.get("success"):
                level = "ERROR"
            elif status_code and int(status_code) >= 400:
                level = "WARNING"

            self.log(
                "telegram_request",
                level=level,
                source_ip=response.get("source_ip"),
                source_port=response.get("source_port"),
                destination_ip=response.get("destination_ip"),
                destination_port=response.get("destination_port"),
                tls=response.get("tls", self._default_log_entry("x", "INFO")["tls"]),
                http_request=response.get("http_request", self._default_log_entry("x", "INFO")["http_request"]),
                http_response=response.get("http_response", self._default_log_entry("x", "INFO")["http_response"]),
                payload_bytes=response.get("payload_bytes", self._default_log_entry("x", "INFO")["payload_bytes"]),
                round_trip_latency_ms=response.get("round_trip_latency_ms"),
                tcp_state=response.get("tcp_state", "unknown"),
                retries=attempt,
                timeout_ms=self.request_timeout_ms,
                socket_error=response.get("socket_error"),
                connection_reset=response.get("connection_reset", False),
                rate_limit=response.get("rate_limit"),
                exception_stacktrace=response.get("exception_stacktrace"),
                details={
                    "cycle_id": cycle_id,
                    "telegram_method": method_name,
                    "success": response.get("success"),
                    "telegram_ok": telegram_ok,
                    "error": response.get("error"),
                },
            )

            if response.get("success") and telegram_ok:
                response["retries"] = retries
                return response

            retryable = False
            if not response.get("success"):
                retryable = True
            elif status_code in (408, 425, 429) or (status_code is not None and int(status_code) >= 500):
                retryable = True

            if not retryable or attempt >= self.max_retries:
                response["retries"] = retries
                if not response.get("success"):
                    errors.append(str(response.get("error")))
                return response

            retries += 1
            if rate_limit_detected and retry_after is not None:
                sleep_sec = max(0.0, float(retry_after))
            else:
                sleep_sec = (self.backoff_base_ms / 1000.0) * math.pow(2, attempt)
            await self.sleep_or_stop(sleep_sec)
            errors.append(str(response.get("error")))

        return {
            "success": False,
            "error": "unreachable_retry_state",
            "retries": retries,
        }

    def extract_retry_after(
        self,
        status_code: int | None,
        headers: dict[str, str],
        body_json: dict[str, Any] | None,
    ) -> int | None:
        if not isinstance(headers, dict):
            headers = {}
        retry_header = headers.get("Retry-After") or headers.get("retry-after")
        if retry_header:
            try:
                return int(retry_header)
            except ValueError:
                pass

        if isinstance(body_json, dict):
            params = body_json.get("parameters")
            if isinstance(params, dict) and isinstance(params.get("retry_after"), int):
                return int(params["retry_after"])
            if status_code == 429:
                return 1

        return None

    def http_request_sync(
        self,
        method_name: str,
        method: str,
        payload: dict[str, Any] | None,
    ) -> dict[str, Any]:
        path = f"/bot{self.bot_token}/{method_name}"
        headers: dict[str, str] = {
            "Host": self.telegram_host,
            "User-Agent": "OpenClaw-NetDiag/1.0",
            "Accept": "application/json",
            "Accept-Encoding": "identity",
            "Connection": "close",
        }

        if not self.current_destination_ip:
            return {
                "success": False,
                "error": "no_destination_ip",
                "source_ip": None,
                "source_port": None,
                "destination_ip": None,
                "destination_port": self.telegram_port,
                "status_code": None,
                "response_headers": {},
                "telegram_json": None,
                "round_trip_latency_ms": None,
                "tls": self._default_log_entry("x", "INFO")["tls"],
                "http_request": {
                    "method": method.upper(),
                    "path": self._masked_path(path),
                    "headers": self._redact_headers(headers),
                    "payload_bytes_sent": 0,
                },
                "http_response": {
                    "status_code": None,
                    "headers": {},
                    "payload_bytes_received": 0,
                },
                "payload_bytes": {
                    "sent": 0,
                    "received": 0,
                },
                "tcp_state": "dns_unresolved",
                "socket_error": "no_destination_ip",
                "connection_reset": False,
                "exception_stacktrace": None,
            }

        payload_bytes = b""

        if method.upper() == "POST":
            payload_bytes = json.dumps(payload or {}, separators=(",", ":")).encode("utf-8")
            headers["Content-Type"] = "application/json"
            headers["Content-Length"] = str(len(payload_bytes))

        start_total = time.perf_counter()
        tcp_state = "tcp_created"
        source_ip = None
        source_port = None
        destination_ip = self.current_destination_ip
        destination_port = self.telegram_port

        sock: socket.socket | None = None
        tls_sock: ssl.SSLSocket | None = None

        tls_data: dict[str, Any] = {
            "version": None,
            "cipher": None,
            "handshake_duration_ms": None,
            "session_reused": None,
            "renegotiation_detected": False,
            "keepalive": {
                "enabled": False,
                "idle_sec": self.tcp_keepalive_idle_sec,
                "interval_sec": self.tcp_keepalive_interval_sec,
                "probe_count": self.tcp_keepalive_probe_count,
                "set_errors": [],
            },
        }

        raw_request = b""
        raw_response = b""
        status_code = None
        response_headers: dict[str, str] = {}
        response_body = b""

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.connect_timeout_ms / 1000.0)
            tcp_state = "tcp_connecting"
            self.enable_keepalive(sock, tls_data["keepalive"])

            connect_started = time.perf_counter()
            target_host, target_port = destination_ip, destination_port
            if self.proxy_endpoint is not None:
                target_host, target_port = self.proxy_endpoint
            sock.connect((target_host, target_port))
            connect_duration_ms = (time.perf_counter() - connect_started) * 1000.0
            source_ip, source_port = sock.getsockname()
            tcp_state = "tcp_connected"

            if self.proxy_endpoint is not None:
                connect_req = (
                    f"CONNECT {destination_ip}:{destination_port} HTTP/1.1\r\n"
                    f"Host: {destination_ip}:{destination_port}\r\n"
                    f"Proxy-Connection: Keep-Alive\r\n\r\n"
                ).encode("ascii")
                sock.sendall(connect_req)
                proxy_resp = bytearray()
                while b"\r\n\r\n" not in proxy_resp:
                    chunk = sock.recv(4096)
                    if not chunk:
                        raise RuntimeError("proxy_connect_eof")
                    proxy_resp.extend(chunk)
                    if len(proxy_resp) > 65536:
                        raise RuntimeError("proxy_connect_response_too_large")
                first_line = proxy_resp.split(b"\r\n", 1)[0].decode("iso-8859-1", errors="replace")
                if " 200 " not in f" {first_line} ":
                    raise RuntimeError(f"proxy_connect_failed:{first_line}")
                tcp_state = "proxy_tunnel_established"

            tls_sock = self.ssl_context.wrap_socket(
                sock,
                server_hostname=self.telegram_host,
                do_handshake_on_connect=False,
            )
            sock = None
            tls_sock.settimeout(self.request_timeout_ms / 1000.0)

            tcp_state = "tls_handshaking"
            handshake_started = time.perf_counter()
            tls_sock.do_handshake()
            tls_data["handshake_duration_ms"] = round((time.perf_counter() - handshake_started) * 1000.0, 3)
            tls_data["version"] = tls_sock.version()
            cipher_data = tls_sock.cipher()
            tls_data["cipher"] = cipher_data[0] if cipher_data else None
            tls_data["session_reused"] = bool(getattr(tls_sock, "session_reused", False))
            tcp_state = "tls_ready"

            current_fingerprint = (tls_data.get("version"), tls_data.get("cipher"))
            if self.last_tls_fingerprint and current_fingerprint != self.last_tls_fingerprint:
                tls_data["renegotiation_detected"] = True
            self.last_tls_fingerprint = current_fingerprint

            request_line = f"{method.upper()} {path} HTTP/1.1\r\n".encode("ascii")
            header_blob = b"".join(
                f"{key}: {value}\r\n".encode("utf-8")
                for key, value in headers.items()
            )
            raw_request = request_line + header_blob + b"\r\n" + payload_bytes
            tcp_state = "http_request_sent"
            tls_sock.sendall(raw_request)

            status_code, response_headers, response_body, raw_response = self.read_http_response(tls_sock)
            tcp_state = "http_response_received"

            round_trip_latency_ms = round((time.perf_counter() - start_total) * 1000.0, 3)
            body_json = None
            try:
                if response_body:
                    body_json = json.loads(response_body.decode("utf-8", errors="replace"))
            except json.JSONDecodeError:
                body_json = None

            return {
                "success": True,
                "error": None,
                "source_ip": source_ip,
                "source_port": source_port,
                "destination_ip": destination_ip,
                "destination_port": destination_port,
                "status_code": status_code,
                "response_headers": response_headers,
                "telegram_json": body_json,
                "round_trip_latency_ms": round_trip_latency_ms,
                "tcp_connect_duration_ms": round(connect_duration_ms, 3),
                "tls": tls_data,
                "http_request": {
                    "method": method.upper(),
                    "path": self._masked_path(path),
                    "headers": self._redact_headers(headers),
                    "payload_bytes_sent": len(raw_request),
                },
                "http_response": {
                    "status_code": status_code,
                    "headers": self._redact_headers(response_headers),
                    "payload_bytes_received": len(raw_response),
                },
                "payload_bytes": {
                    "sent": len(raw_request),
                    "received": len(raw_response),
                },
                "tcp_state": "tcp_closed",
                "socket_error": None,
                "connection_reset": False,
                "exception_stacktrace": None,
            }

        except Exception as exc:
            connection_reset = isinstance(exc, ConnectionResetError) or "reset" in str(exc).lower()
            is_timeout = isinstance(exc, socket.timeout)
            return {
                "success": False,
                "error": str(exc),
                "source_ip": source_ip,
                "source_port": source_port,
                "destination_ip": destination_ip,
                "destination_port": destination_port,
                "status_code": status_code,
                "response_headers": response_headers,
                "telegram_json": None,
                "round_trip_latency_ms": round((time.perf_counter() - start_total) * 1000.0, 3),
                "tls": tls_data,
                "http_request": {
                    "method": method.upper(),
                    "path": self._masked_path(path),
                    "headers": self._redact_headers(headers),
                    "payload_bytes_sent": len(raw_request),
                },
                "http_response": {
                    "status_code": status_code,
                    "headers": self._redact_headers(response_headers),
                    "payload_bytes_received": len(raw_response),
                },
                "payload_bytes": {
                    "sent": len(raw_request),
                    "received": len(raw_response),
                },
                "tcp_state": tcp_state,
                "socket_error": "timeout" if is_timeout else str(exc),
                "connection_reset": connection_reset,
                "exception_stacktrace": traceback.format_exc(),
            }

        finally:
            if tls_sock is not None:
                try:
                    tls_sock.close()
                except OSError:
                    pass
            if sock is not None:
                try:
                    sock.close()
                except OSError:
                    pass

    def enable_keepalive(self, sock: socket.socket, keepalive_meta: dict[str, Any]) -> None:
        keepalive_meta["enabled"] = False
        errors: list[str] = []
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
            keepalive_meta["enabled"] = True
        except OSError as exc:
            errors.append(f"SO_KEEPALIVE:{exc}")

        # macOS keepalive tuning.
        if hasattr(socket, "TCP_KEEPALIVE"):
            try:
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPALIVE, self.tcp_keepalive_idle_sec)
            except OSError as exc:
                errors.append(f"TCP_KEEPALIVE:{exc}")
        if hasattr(socket, "TCP_KEEPINTVL"):
            try:
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, self.tcp_keepalive_interval_sec)
            except OSError as exc:
                errors.append(f"TCP_KEEPINTVL:{exc}")
        if hasattr(socket, "TCP_KEEPCNT"):
            try:
                sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, self.tcp_keepalive_probe_count)
            except OSError as exc:
                errors.append(f"TCP_KEEPCNT:{exc}")

        keepalive_meta["set_errors"] = errors

    def read_http_response(self, tls_sock: ssl.SSLSocket) -> tuple[int | None, dict[str, str], bytes, bytes]:
        buffer = bytearray()

        while b"\r\n\r\n" not in buffer:
            chunk = tls_sock.recv(4096)
            if not chunk:
                break
            buffer.extend(chunk)
            if len(buffer) > self.max_response_bytes:
                raise RuntimeError("response_headers_too_large")

        header_blob, _, remainder = bytes(buffer).partition(b"\r\n\r\n")
        header_text = header_blob.decode("iso-8859-1", errors="replace")
        lines = header_text.split("\r\n") if header_text else []

        status_code = None
        headers: dict[str, str] = {}
        if lines:
            status_line = lines[0]
            status_match = re.match(r"^HTTP/\d(?:\.\d)?\s+(\d{3})", status_line)
            if status_match:
                status_code = int(status_match.group(1))
            for line in lines[1:]:
                if ":" not in line:
                    continue
                key, value = line.split(":", 1)
                headers[key.strip()] = value.strip()

        body = bytearray(remainder)

        transfer_encoding = headers.get("Transfer-Encoding", "").lower()
        if "chunked" in transfer_encoding:
            body = bytearray(self.read_chunked_body(body, tls_sock))
        elif "Content-Length" in headers:
            try:
                expected = int(headers["Content-Length"])
            except ValueError:
                expected = len(body)
            while len(body) < expected:
                chunk = tls_sock.recv(min(4096, expected - len(body)))
                if not chunk:
                    break
                body.extend(chunk)
                if len(body) > self.max_response_bytes:
                    raise RuntimeError("response_body_too_large")
        else:
            while True:
                chunk = tls_sock.recv(4096)
                if not chunk:
                    break
                body.extend(chunk)
                if len(body) > self.max_response_bytes:
                    raise RuntimeError("response_body_too_large")

        raw_response = header_blob + b"\r\n\r\n" + bytes(body)
        return status_code, headers, bytes(body), raw_response

    def read_chunked_body(self, initial: bytearray, tls_sock: ssl.SSLSocket) -> bytes:
        data = bytearray(initial)
        output = bytearray()

        while True:
            while b"\r\n" not in data:
                chunk = tls_sock.recv(4096)
                if not chunk:
                    raise RuntimeError("unexpected_eof_in_chunked_size")
                data.extend(chunk)

            line, _, rest = data.partition(b"\r\n")
            data = bytearray(rest)
            size_token = line.split(b";", 1)[0]
            try:
                chunk_size = int(size_token, 16)
            except ValueError as exc:
                raise RuntimeError("invalid_chunk_size") from exc

            if chunk_size == 0:
                # Consume trailing CRLF after final chunk.
                while len(data) < 2:
                    chunk = tls_sock.recv(4096)
                    if not chunk:
                        break
                    data.extend(chunk)
                break

            required = chunk_size + 2
            while len(data) < required:
                chunk = tls_sock.recv(4096)
                if not chunk:
                    raise RuntimeError("unexpected_eof_in_chunked_data")
                data.extend(chunk)

            output.extend(data[:chunk_size])
            data = data[required:]

            if len(output) > self.max_response_bytes:
                raise RuntimeError("response_body_too_large")

        return bytes(output)

    async def run_subprocess(self, args: list[str], timeout_ms: int) -> dict[str, Any]:
        started = time.perf_counter()
        try:
            process = await asyncio.create_subprocess_exec(
                *args,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        except FileNotFoundError:
            return {
                "returncode": 127,
                "stdout": "",
                "stderr": f"command_not_found:{args[0]}",
                "duration_ms": round((time.perf_counter() - started) * 1000.0, 3),
            }

        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout_ms / 1000.0)
        except asyncio.TimeoutError:
            process.kill()
            stdout, stderr = await process.communicate()
            return {
                "returncode": -9,
                "stdout": stdout.decode("utf-8", errors="replace"),
                "stderr": stderr.decode("utf-8", errors="replace"),
                "duration_ms": round((time.perf_counter() - started) * 1000.0, 3),
                "timeout": True,
            }

        return {
            "returncode": process.returncode,
            "stdout": stdout.decode("utf-8", errors="replace"),
            "stderr": stderr.decode("utf-8", errors="replace"),
            "duration_ms": round((time.perf_counter() - started) * 1000.0, 3),
            "timeout": False,
        }


def load_config(config_path: Path) -> dict[str, Any]:
    user_cfg = parse_json_file(config_path)
    cfg = deep_merge(DEFAULT_CONFIG, user_cfg)
    errors = validate_config_errors(cfg)
    if errors:
        raise ValueError("; ".join(errors))
    return cfg


async def run_worker(config_path: Path, pid_file: Path | None) -> int:
    try:
        config = load_config(config_path)
    except Exception as exc:
        print(f"Config error: {exc}", file=sys.stderr)
        return 2

    worker = NetworkDiagnosticWorker(config=config, config_path=config_path, pid_file=pid_file)
    await worker.run()
    return 0


def do_start(config_path: Path, pid_file: Path) -> int:
    if pid_file.exists():
        try:
            pid = int(pid_file.read_text(encoding="utf-8").strip())
        except ValueError:
            pid = -1
        if is_process_alive(pid):
            print(f"Already running with pid={pid}")
            return 0
        pid_file.unlink(missing_ok=True)

    cmd = [
        sys.executable,
        str(Path(__file__).resolve()),
        "run",
        "--config",
        str(config_path),
        "--pid-file",
        str(pid_file),
        "--background",
    ]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    print(f"Started background worker pid={process.pid}")
    return 0


def do_stop(pid_file: Path) -> int:
    if not pid_file.exists():
        print("Not running (pid file not found)")
        return 1

    try:
        pid = int(pid_file.read_text(encoding="utf-8").strip())
    except ValueError:
        print("Invalid pid file")
        return 2

    if not is_process_alive(pid):
        pid_file.unlink(missing_ok=True)
        print("Not running (stale pid file removed)")
        return 1

    os.kill(pid, signal.SIGTERM)

    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        if not is_process_alive(pid):
            break
        time.sleep(0.2)

    if is_process_alive(pid):
        print(f"Worker pid={pid} did not stop within timeout")
        return 3

    pid_file.unlink(missing_ok=True)
    print(f"Stopped worker pid={pid}")
    return 0


def do_status(pid_file: Path) -> int:
    if not pid_file.exists():
        print("stopped")
        return 1

    try:
        pid = int(pid_file.read_text(encoding="utf-8").strip())
    except ValueError:
        print("stopped (invalid pid file)")
        return 2

    if is_process_alive(pid):
        print(f"running pid={pid}")
        return 0

    print("stopped (stale pid file)")
    return 1


def do_validate(config_path: Path) -> int:
    try:
        user_cfg = parse_json_file(config_path)
        cfg = deep_merge(DEFAULT_CONFIG, user_cfg)
    except Exception as exc:
        print(f"invalid:\n - failed to parse config: {exc}")
        return 2

    errors = validate_config_errors(cfg)
    if errors:
        print("invalid:")
        for err in errors:
            print(f" - {err}")
        return 2

    print("valid")
    print(json.dumps(cfg, ensure_ascii=True, indent=2))
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="OpenClaw standalone network diagnostics")
    parser.add_argument("--config", help="Path to config JSON (default: NETDIAG_CONFIG or references/config.example.json)")
    parser.add_argument("--proxy", help="Optional HTTP proxy URL for outbound Telegram checks (e.g. http://127.0.0.1:1082)")

    sub = parser.add_subparsers(dest="command", required=True)

    run_parser = sub.add_parser("run", help="Run in foreground until stopped")
    run_parser.add_argument("--config", help="Path to config JSON")
    run_parser.add_argument("--proxy", help="Override proxy URL")
    run_parser.add_argument("--pid-file", default="./logs/netdiag.pid", help="PID file path")
    run_parser.add_argument("--background", action="store_true", help=argparse.SUPPRESS)

    start_parser = sub.add_parser("start", help="Start background worker")
    start_parser.add_argument("--config", help="Path to config JSON")
    start_parser.add_argument("--proxy", help="Override proxy URL")
    start_parser.add_argument("--pid-file", default="./logs/netdiag.pid", help="PID file path")

    stop_parser = sub.add_parser("stop", help="Stop background worker")
    stop_parser.add_argument("--pid-file", default="./logs/netdiag.pid", help="PID file path")

    status_parser = sub.add_parser("status", help="Check background worker status")
    status_parser.add_argument("--pid-file", default="./logs/netdiag.pid", help="PID file path")

    validate_parser = sub.add_parser("validate-config", help="Validate config and print merged config")
    validate_parser.add_argument("--config", help="Path to config JSON")
    validate_parser.add_argument("--proxy", help="Override proxy URL")

    return parser.parse_args()


def resolve_config_path_from_args(args: argparse.Namespace) -> Path:
    raw = getattr(args, "config", None) or _find_default_config_path()
    path = Path(raw).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(
            f"Config file not found: {path}. Pass --config or set NETDIAG_CONFIG."
        )
    return path


def apply_cli_overrides(cfg: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    proxy = getattr(args, "proxy", None)
    if proxy is not None:
        cfg.setdefault("network", {})["proxy_url"] = proxy
    return cfg


def main() -> int:
    args = parse_args()

    if args.command == "run":
        try:
            config_path = resolve_config_path_from_args(args)
            cfg = apply_cli_overrides(load_config(config_path), args)
            if getattr(args, "proxy", None) is not None:
                config_path = config_path.parent / ".netdiag.runtime.config.json"
                config_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as exc:
            print(f"Config error: {exc}", file=sys.stderr)
            return 2
        pid_file = Path(args.pid_file).expanduser().resolve()
        return asyncio.run(run_worker(config_path=config_path, pid_file=pid_file))

    if args.command == "start":
        try:
            config_path = resolve_config_path_from_args(args)
            cfg = apply_cli_overrides(load_config(config_path), args)
            if getattr(args, "proxy", None) is not None:
                config_path = config_path.parent / ".netdiag.runtime.config.json"
                config_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as exc:
            print(f"Config error: {exc}", file=sys.stderr)
            return 2
        pid_file = Path(args.pid_file).expanduser().resolve()
        return do_start(config_path=config_path, pid_file=pid_file)

    if args.command == "stop":
        pid_file = Path(args.pid_file).expanduser().resolve()
        return do_stop(pid_file=pid_file)

    if args.command == "status":
        pid_file = Path(args.pid_file).expanduser().resolve()
        return do_status(pid_file=pid_file)

    if args.command == "validate-config":
        try:
            config_path = resolve_config_path_from_args(args)
        except Exception as exc:
            print(f"invalid:\n - {exc}")
            return 2
        return do_validate(config_path=config_path)

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
