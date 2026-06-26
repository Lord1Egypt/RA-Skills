from __future__ import annotations

import logging
import time

from .adapters.base import WeChatDesktopAdapter
from .bridge_client import BridgeClient

LOGGER = logging.getLogger(__name__)


def process_outbound_once(
    adapter: WeChatDesktopAdapter,
    bridge_client: BridgeClient,
    sidecar_id: str,
    claim_batch_size: int,
    send_max_attempts: int = 2,
) -> None:
    commands = bridge_client.claim_commands(sidecar_id=sidecar_id, limit=claim_batch_size)
    if not commands:
        return

    for command in commands:
        attempts = max(1, send_max_attempts)
        sent = False
        last_error: Exception | None = None

        for attempt in range(1, attempts + 1):
            try:
                adapter.send_text(command.chat_id, command.text)
                sent = True
                break
            except Exception as error:
                last_error = error
                if attempt < attempts:
                    LOGGER.warning(
                        "send failed, will retry command_id=%s attempt=%s/%s error=%s",
                        command.command_id,
                        attempt,
                        attempts,
                        error,
                    )
                    time.sleep(0.2 * attempt)

        if sent:
            try:
                bridge_client.ack_command(
                    command_id=command.command_id,
                    sidecar_id=sidecar_id,
                    status="sent",
                )
            except Exception as ack_error:
                LOGGER.exception(
                    "sent but ack failed command_id=%s ack_error=%s",
                    command.command_id,
                    ack_error,
                )
                continue
            LOGGER.info("sent command_id=%s chat_id=%s", command.command_id, command.chat_id)
            continue

        error_text = str(last_error) if last_error is not None else "unknown_send_error"
        try:
            bridge_client.ack_command(
                command_id=command.command_id,
                sidecar_id=sidecar_id,
                status="failed",
                error_code="send_error",
                error_message=error_text,
            )
        except Exception as ack_error:
            LOGGER.exception(
                "failed to ack failed command command_id=%s ack_error=%s",
                command.command_id,
                ack_error,
            )
        LOGGER.error("failed command_id=%s error=%s", command.command_id, error_text)
