from __future__ import annotations

import argparse
from pathlib import Path
import threading
import time
import logging

from .adapters.mock_adapter import MockAdapter
from .adapters.pywinauto_adapter import PywinautoAdapter
from .adapters.uiautomation_adapter import UIAutomationAdapter
from .bridge_client import BridgeClient
from .config import SidecarConfig, load_config
from .logging_setup import configure_logging
from .message_watch import MessageWatcher
from .send_message import process_outbound_once
from .diagnostics_server import start_diagnostics_server
from .webhook_proxy import start_webhook_proxy

LOGGER = logging.getLogger(__name__)


def build_adapter(config: SidecarConfig):
    if config.adapter == "mock":
        return MockAdapter(config.sidecar_id, config.watch_poll_interval_sec)
    if config.adapter == "pywinauto":
        return PywinautoAdapter(config.sidecar_id, config.watch_poll_interval_sec)
    if config.adapter == "uiautomation":
        default_chat = config.allow_groups[0] if len(config.allow_groups) == 1 else "WeChat Current Chat"
        return UIAutomationAdapter(
            config.sidecar_id,
            config.watch_poll_interval_sec,
            visual_config=config.visual,
            default_chat_name=default_chat,
        )
    raise ValueError(f"unsupported adapter: {config.adapter}")


def main() -> None:
    parser = argparse.ArgumentParser(description="OpenClaw WeChat sidecar")
    parser.add_argument(
        "--config",
        type=Path,
        required=True,
        help="Path to sidecar config TOML",
    )
    parser.add_argument(
        "--health-once",
        action="store_true",
        help="Print adapter and bridge health then exit",
    )
    args = parser.parse_args()

    configure_logging()
    config = load_config(args.config)

    adapter = build_adapter(config)
    bridge_client = BridgeClient(config.bridge)

    health = adapter.health()
    LOGGER.info("adapter health ok=%s name=%s detail=%s", health.ok, health.name, health.detail)
    try:
        bridge_health = bridge_client.health()
        LOGGER.info("bridge health response=%s", bridge_health)
    except Exception as error:
        LOGGER.warning("bridge health check failed error=%s", error)

    try:
        groups = adapter.list_groups()
        LOGGER.info("adapter groups discovered count=%s", len(groups))
    except Exception as error:
        LOGGER.warning("list_groups failed error=%s", error)

    if args.health_once:
        LOGGER.info("health-once completed")
        return

    watcher = MessageWatcher(
        adapter=adapter,
        bridge_client=bridge_client,
        allow_groups=config.allow_groups,
    )

    watch_thread = threading.Thread(target=watcher.run_forever, name="watch-loop", daemon=True)
    watch_thread.start()

    if config.diagnostics.enabled:
        start_diagnostics_server(config.diagnostics, adapter, bridge_client)
        LOGGER.info("diagnostics enabled host=%s port=%s", config.diagnostics.host, config.diagnostics.port)

    if config.webhook_proxy.enabled:
        start_webhook_proxy(config.webhook_proxy, bridge_client)
        LOGGER.info(
            "webhook proxy enabled host=%s port=%s",
            config.webhook_proxy.host,
            config.webhook_proxy.port,
        )

    LOGGER.info("sidecar started sidecar_id=%s adapter=%s", config.sidecar_id, config.adapter)
    last_heartbeat = 0.0
    try:
        while True:
            now = time.time()
            if now - last_heartbeat >= config.bridge.heartbeat_interval_sec:
                try:
                    hb_health = adapter.health()
                    try:
                        hb_groups = adapter.list_groups()
                        hb_groups_payload = [{"chatId": g.chat_id, "chatName": g.chat_name} for g in hb_groups]
                    except Exception:
                        hb_groups_payload = []
                    bridge_client.heartbeat(
                        sidecar_id=config.sidecar_id,
                        adapter_name=hb_health.name,
                        adapter_ok=hb_health.ok,
                        detail=hb_health.detail,
                        groups=hb_groups_payload,
                    )
                    last_heartbeat = now
                except Exception as error:
                    LOGGER.warning("heartbeat failed error=%s", error)

            process_outbound_once(
                adapter=adapter,
                bridge_client=bridge_client,
                sidecar_id=config.sidecar_id,
                claim_batch_size=config.bridge.claim_batch_size,
            )
            time.sleep(config.bridge.send_poll_interval_sec)
    except KeyboardInterrupt:
        LOGGER.info("sidecar shutdown requested")


if __name__ == "__main__":
    main()
