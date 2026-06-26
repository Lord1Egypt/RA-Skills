from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib


@dataclass(frozen=True)
class BridgeConfig:
    base_url: str
    shared_secret: str
    auth_mode: str
    request_timeout_sec: int
    claim_batch_size: int
    send_poll_interval_sec: int
    heartbeat_interval_sec: int


@dataclass(frozen=True)
class WebhookProxyConfig:
    enabled: bool
    host: str
    port: int
    shared_secret: str
    inbound_secret: str | None


@dataclass(frozen=True)
class DiagnosticsConfig:
    enabled: bool
    host: str
    port: int


@dataclass(frozen=True)
class VisualConfig:
    enabled: bool
    mode: str
    sample_interval_sec: int
    ocr_lang: str
    ocr_max_chars: int
    vlm_base_url: str
    vlm_api_key: str | None
    vlm_model: str


@dataclass(frozen=True)
class SidecarConfig:
    sidecar_id: str
    adapter: str
    allow_groups: list[str]
    watch_poll_interval_sec: float
    bridge: BridgeConfig
    webhook_proxy: WebhookProxyConfig
    diagnostics: DiagnosticsConfig
    visual: VisualConfig


def load_config(config_path: Path) -> SidecarConfig:
    raw = tomllib.loads(config_path.read_text(encoding="utf-8"))

    bridge_raw = raw.get("bridge", {})
    auth_mode = str(bridge_raw.get("auth_mode", "bearer")).strip().lower()
    if auth_mode not in {"bearer", "hmac"}:
        auth_mode = "bearer"

    bridge = BridgeConfig(
        base_url=str(bridge_raw.get("base_url", "http://127.0.0.1:8787")).rstrip("/"),
        shared_secret=str(bridge_raw.get("shared_secret", "dev-bridge-secret")),
        auth_mode=auth_mode,
        request_timeout_sec=int(bridge_raw.get("request_timeout_sec", 10)),
        claim_batch_size=max(1, int(bridge_raw.get("claim_batch_size", 5))),
        send_poll_interval_sec=max(1, int(bridge_raw.get("send_poll_interval_sec", 2))),
        heartbeat_interval_sec=max(5, int(bridge_raw.get("heartbeat_interval_sec", 15))),
    )
    webhook_raw = raw.get("webhook_proxy", {})
    inbound_secret: str | None
    if "inbound_secret" in webhook_raw:
        incoming = str(webhook_raw.get("inbound_secret", "")).strip()
        inbound_secret = incoming if incoming else None
    else:
        inbound_secret = "local-webhook-secret"
    webhook_proxy = WebhookProxyConfig(
        enabled=bool(webhook_raw.get("enabled", False)),
        host=str(webhook_raw.get("host", "127.0.0.1")),
        port=max(1, int(webhook_raw.get("port", 28761))),
        shared_secret=str(webhook_raw.get("shared_secret", bridge.shared_secret)),
        inbound_secret=inbound_secret,
    )
    diagnostics_raw = raw.get("diagnostics", {})
    diagnostics = DiagnosticsConfig(
        enabled=bool(diagnostics_raw.get("enabled", True)),
        host=str(diagnostics_raw.get("host", "127.0.0.1")),
        port=max(1, int(diagnostics_raw.get("port", 28762))),
    )
    visual_raw = raw.get("visual", {})
    mode = str(visual_raw.get("mode", "auto")).strip().lower()
    if mode not in {"off", "ocr", "vlm", "auto"}:
        mode = "auto"
    visual = VisualConfig(
        enabled=bool(visual_raw.get("enabled", True)),
        mode=mode,
        sample_interval_sec=max(1, int(visual_raw.get("sample_interval_sec", 2))),
        ocr_lang=str(visual_raw.get("ocr_lang", "chi_sim+eng")),
        ocr_max_chars=max(50, int(visual_raw.get("ocr_max_chars", 160))),
        vlm_base_url=str(visual_raw.get("vlm_base_url", "https://api.openai.com/v1")).rstrip("/"),
        vlm_api_key=(
            str(visual_raw.get("vlm_api_key")).strip()
            if visual_raw.get("vlm_api_key") is not None
            else None
        ),
        vlm_model=str(visual_raw.get("vlm_model", "gpt-4.1-mini")),
    )

    return SidecarConfig(
        sidecar_id=str(raw.get("sidecar_id", "winbox-01")),
        adapter=str(raw.get("adapter", "mock")),
        allow_groups=[str(item) for item in raw.get("allow_groups", [])],
        watch_poll_interval_sec=float(raw.get("watch_poll_interval_sec", 1.0)),
        bridge=bridge,
        webhook_proxy=webhook_proxy,
        diagnostics=diagnostics,
        visual=visual,
    )
