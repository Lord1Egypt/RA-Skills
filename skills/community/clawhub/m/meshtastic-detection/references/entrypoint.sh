#!/usr/bin/env bash
#
# Docker entrypoint — keeps usb_receiver.py running with auto-restart
#
set -uo pipefail

INSTALL_DIR="__INSTALL_DIR__"
SERIAL_PORT="__SERIAL_PORT__"
RESTART_DELAY=10

cd "$INSTALL_DIR"

echo "[entrypoint] Starting Meshtastic USB Receiver"
echo "[entrypoint]   Serial port: $SERIAL_PORT"
echo "[entrypoint]   Install dir: $INSTALL_DIR"

while true; do
  ./venv/bin/python scripts/usb_receiver.py --port "$SERIAL_PORT"
  EXIT_CODE=$?
  echo "[entrypoint] usb_receiver.py exited with code $EXIT_CODE, restarting in ${RESTART_DELAY}s..."
  sleep "$RESTART_DELAY"
done
