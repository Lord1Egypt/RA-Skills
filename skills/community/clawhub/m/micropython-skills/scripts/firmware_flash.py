#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automatic MicroPython firmware download and flash for ESP devices.

Detects the chip type via esptool, downloads the matching MicroPython
firmware from micropython.org, and flashes it.

Usage:
    python3 firmware_flash.py [--port /dev/ttyACM0] [--chip esp32c3] [--yes]

Requires: esptool (pip install esptool)
"""

import subprocess
import json
import sys
import os
import re
import argparse
import tempfile
import urllib.request
import urllib.error


# Chip -> MicroPython board mapping + flash parameters
FIRMWARE_MAP = {
    "esp32": {
        "board": "ESP32_GENERIC",
        "flash_addr": "0x1000",
        "chip_arg": "esp32",
    },
    "esp32s2": {
        "board": "ESP32_GENERIC_S2",
        "flash_addr": "0x1000",
        "chip_arg": "esp32s2",
    },
    "esp32s3": {
        "board": "ESP32_GENERIC_S3",
        "flash_addr": "0x0",
        "chip_arg": "esp32s3",
    },
    "esp32c3": {
        "board": "ESP32_GENERIC_C3",
        "flash_addr": "0x0",
        "chip_arg": "esp32c3",
    },
    "esp32c6": {
        "board": "ESP32_GENERIC_C6",
        "flash_addr": "0x0",
        "chip_arg": "esp32c6",
    },
}

DOWNLOAD_BASE = "https://micropython.org/download/{board}/"
CACHE_DIR = os.path.join(tempfile.gettempdir(), "micropython-firmware")


def run_cmd(cmd, timeout=60):
    """Run a shell command and return (stdout, stderr, returncode)."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout,
            encoding="utf-8", errors="replace"
        )
        return result.stdout, result.stderr, result.returncode
    except FileNotFoundError:
        return "", f"{cmd[0]} not found", 1
    except subprocess.TimeoutExpired:
        return "", f"Command timed out after {timeout}s", 1


def find_esptool():
    """Find the esptool command name."""
    for name in ["esptool", "esptool.py"]:
        # esptool v5+ uses "version" subcommand, older uses "--version"
        for ver_arg in ["version", "--version"]:
            stdout, _, rc = run_cmd([name, ver_arg], timeout=5)
            if rc == 0:
                return name
    return None


def detect_chip(esptool_cmd, port):
    """Detect chip type via esptool."""
    stdout, stderr, rc = run_cmd(
        [esptool_cmd, "--port", port, "chip_id"], timeout=15
    )
    combined = stdout + stderr

    if "not readable" in combined.lower() or "permission" in combined.lower():
        if sys.platform == "win32":
            return None, f"Permission denied on {port}. Check Device Manager for driver issues."
        return None, f"Permission denied on {port}. Run: sudo chmod 666 {port}"

    chip_match = re.search(r"Chip is (ESP\S+)", combined, re.IGNORECASE)
    if chip_match:
        raw = chip_match.group(1).lower().replace("-", "").replace(" ", "")
        return raw, ""

    if rc != 0:
        return None, (
            f"Cannot connect to {port}. "
            "If the device is not responding, try bootloader mode: "
            "hold BOOT, press RESET, release BOOT."
        )
    return None, f"Could not parse chip type from esptool output"


def get_firmware_url(board):
    """Fetch the latest stable firmware .bin URL from micropython.org."""
    download_page = DOWNLOAD_BASE.format(board=board)

    try:
        req = urllib.request.Request(
            download_page,
            headers={"User-Agent": "micropython-skills/1.0"}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except urllib.error.URLError as e:
        return None, f"Cannot reach {download_page}: {e}"

    # Find .bin download links — micropython.org format:
    # href="/resources/firmware/ESP32_GENERIC-20241025-v1.24.1.bin"
    # We want the first stable release (not unstable/preview)
    bin_links = re.findall(
        r'href="(/resources/firmware/' + re.escape(board) + r'-\d{8}-v[\d.]+\.bin)"',
        html
    )

    if not bin_links:
        # Try broader pattern for different naming
        bin_links = re.findall(
            r'href="(/resources/firmware/' + re.escape(board) + r'[^"]*\.bin)"',
            html
        )

    if not bin_links:
        return None, f"No firmware .bin found on {download_page}"

    # First link is typically the latest stable
    firmware_url = "https://micropython.org" + bin_links[0]
    return firmware_url, ""


def download_firmware(url, chip):
    """Download firmware to cache directory. Returns local path."""
    os.makedirs(CACHE_DIR, exist_ok=True)

    filename = url.split("/")[-1]
    local_path = os.path.join(CACHE_DIR, filename)

    # Use cached version if exists
    if os.path.exists(local_path) and os.path.getsize(local_path) > 10000:
        return local_path, f"Using cached firmware: {filename}"

    print(f"Downloading: {url}")
    print(f"Saving to: {local_path}")

    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "micropython-skills/1.0"}
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
            with open(local_path, "wb") as f:
                f.write(data)
        size_kb = len(data) // 1024
        return local_path, f"Downloaded {filename} ({size_kb} KB)"
    except Exception as e:
        return None, f"Download failed: {e}"


def erase_flash(esptool_cmd, port, chip_arg):
    """Erase entire flash."""
    print("Erasing flash...")
    stdout, stderr, rc = run_cmd(
        [esptool_cmd, "--chip", chip_arg, "--port", port, "erase_flash"],
        timeout=60
    )
    if rc != 0:
        return False, f"Erase failed: {(stderr or stdout)[:300]}"
    return True, "Flash erased successfully"


def write_flash(esptool_cmd, port, chip_arg, flash_addr, firmware_path):
    """Write firmware to flash."""
    print(f"Flashing firmware to {flash_addr}...")
    stdout, stderr, rc = run_cmd(
        [
            esptool_cmd, "--chip", chip_arg, "--port", port,
            "--baud", "460800",
            "write_flash", "-z", flash_addr, firmware_path,
        ],
        timeout=120
    )
    combined = stdout + stderr
    if rc != 0:
        return False, f"Flash failed: {combined[:300]}"

    if "hash of data verified" in combined.lower() or "wrote" in combined.lower():
        return True, "Firmware flashed and verified successfully"
    return True, "Firmware flashed (could not confirm verification)"


def verify_micropython(port):
    """Verify MicroPython is running after flash."""
    # Wait for device to reset
    import time
    time.sleep(2)

    stdout, stderr, rc = run_cmd(
        ["mpremote", "connect", port, "exec",
         "import sys; print('VERIFY:' + sys.platform)"],
        timeout=10
    )
    for line in stdout.splitlines():
        if line.startswith("VERIFY:"):
            return True, f"MicroPython running on {line[len('VERIFY:'):]}"
    return False, "MicroPython verification failed — device may need a manual reset"


def main():
    parser = argparse.ArgumentParser(
        description="Download and flash MicroPython firmware"
    )
    parser.add_argument("--port", help="Serial port (auto-detect if omitted)")
    parser.add_argument("--chip", help="Chip type: esp32, esp32s3, esp32c3, etc. (auto-detect if omitted)")
    parser.add_argument("--version", help="Firmware version (default: latest stable)")
    parser.add_argument("--yes", "-y", action="store_true",
                        help="Skip confirmation prompt")
    parser.add_argument("--download-only", action="store_true",
                        help="Only download firmware, do not flash")
    args = parser.parse_args()

    # Find esptool
    esptool_cmd = find_esptool()
    if not esptool_cmd:
        print(json.dumps({
            "status": "error",
            "error": "esptool not found. Install with: pip install esptool",
        }, indent=2))
        sys.exit(1)

    # Auto-detect port (cross-platform)
    port = args.port
    if not port:
        try:
            from serial.tools import list_ports
            ports = [p.device for p in list_ports.comports()]
        except ImportError:
            import glob
            if sys.platform == "win32":
                # Fallback: use 'mode' command to detect COM ports
                print("WARNING: pyserial not installed. Install with: pip install pyserial", file=sys.stderr)
                try:
                    mode_result = subprocess.run(
                        ["mode"], capture_output=True, text=True, timeout=5
                    )
                    ports = sorted(set(re.findall(r"(COM\d+)", mode_result.stdout)))
                except Exception:
                    ports = []
            elif sys.platform == "darwin":
                ports = sorted(glob.glob("/dev/cu.usbserial-*") + glob.glob("/dev/cu.usbmodem*"))
            else:
                ports = sorted(glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*"))
        if not ports:
            print(json.dumps({
                "status": "error",
                "error": "No serial devices found. Connect an ESP device via USB.",
            }, indent=2))
            sys.exit(1)
        port = ports[0]
        print(f"Auto-detected port: {port}")

    # Auto-detect chip
    chip = args.chip
    if not chip:
        chip, err = detect_chip(esptool_cmd, port)
        if not chip:
            print(json.dumps({
                "status": "error",
                "port": port,
                "error": err,
            }, indent=2))
            sys.exit(1)
        print(f"Detected chip: {chip}")

    # Normalize chip name
    chip = chip.lower().replace("-", "").replace("esp32 ", "esp32").replace(" ", "")
    # Handle variations like "esp32c3(revision v0.4)" -> "esp32c3"
    chip = re.sub(r"\(.*\)", "", chip).strip()

    if chip not in FIRMWARE_MAP:
        print(json.dumps({
            "status": "error",
            "chip": chip,
            "error": f"Unsupported chip: {chip}. Supported: {', '.join(FIRMWARE_MAP.keys())}",
        }, indent=2))
        sys.exit(1)

    fw = FIRMWARE_MAP[chip]
    board = fw["board"]
    flash_addr = fw["flash_addr"]
    chip_arg = fw["chip_arg"]

    # Get firmware download URL
    print(f"Looking up latest MicroPython firmware for {board}...")
    fw_url, err = get_firmware_url(board)
    if not fw_url:
        print(json.dumps({
            "status": "error",
            "chip": chip,
            "board": board,
            "error": err,
        }, indent=2))
        sys.exit(1)

    firmware_version = "unknown"
    version_match = re.search(r"v([\d.]+)", fw_url)
    if version_match:
        firmware_version = "v" + version_match.group(1)

    # Download firmware
    fw_path, msg = download_firmware(fw_url, chip)
    print(msg)
    if not fw_path:
        print(json.dumps({"status": "error", "error": msg}, indent=2))
        sys.exit(1)

    if args.download_only:
        print(json.dumps({
            "status": "downloaded",
            "chip": chip,
            "board": board,
            "version": firmware_version,
            "firmware_path": fw_path,
            "flash_addr": flash_addr,
        }, indent=2))
        return

    # Confirmation
    print(f"\n{'='*60}")
    print(f"  Ready to flash MicroPython to {chip.upper()}")
    print(f"  Port: {port}")
    print(f"  Firmware: {os.path.basename(fw_path)}")
    print(f"  Version: {firmware_version}")
    print(f"  Flash address: {flash_addr}")
    print(f"  WARNING: This will ERASE ALL DATA on the device!")
    print(f"{'='*60}")

    if not args.yes:
        try:
            answer = input("\nProceed? [y/N] ").strip().lower()
            if answer not in ("y", "yes"):
                print("Aborted.")
                sys.exit(0)
        except EOFError:
            print("Non-interactive mode. Use --yes to skip confirmation.")
            sys.exit(1)

    # Erase
    ok, msg = erase_flash(esptool_cmd, port, chip_arg)
    print(msg)
    if not ok:
        print(json.dumps({"status": "error", "step": "erase", "error": msg}, indent=2))
        sys.exit(1)

    # Flash
    ok, msg = write_flash(esptool_cmd, port, chip_arg, flash_addr, fw_path)
    print(msg)
    if not ok:
        print(json.dumps({"status": "error", "step": "flash", "error": msg}, indent=2))
        sys.exit(1)

    # Verify
    ok, msg = verify_micropython(port)
    print(msg)

    result = {
        "status": "ok" if ok else "flashed_unverified",
        "chip": chip,
        "board": board,
        "version": firmware_version,
        "port": port,
        "firmware_path": fw_path,
        "verified": ok,
    }
    print("\n" + json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
