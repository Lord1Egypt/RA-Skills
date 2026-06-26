#!/usr/bin/env python3
"""
macOS CoreLocation location provider.
Uses CoreLocationCLI (installed via brew) for WiFi-based positioning.

Accuracy: ~500m on Mac (no GPS chip, WiFi triangulation via Apple database).
This is the best available on-device location for macOS without external GPS.

Usage:
    loc = get_macos_location()
    if loc:
        print(f"{loc['lat']}, {loc['lon']}")

Returns None if CoreLocationCLI not installed, location services disabled, or
the command fails.
"""

import json
import subprocess

CLI_PATH = subprocess.run(
    ["which", "CoreLocationCLI"],
    capture_output=True, text=True, timeout=5
).stdout.strip() or "/opt/homebrew/bin/CoreLocationCLI"


def get_macos_location(timeout=10):
    """
    Get current location via CoreLocationCLI.

    Returns dict with lat, lon, accuracy, provider, or None on failure.
    """
    try:
        proc = subprocess.run(
            [CLI_PATH, "-json"],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except FileNotFoundError:
        return None
    except subprocess.TimeoutExpired:
        return None
    except Exception:
        return None

    if proc.returncode != 0:
        stderr = (proc.stderr or "").strip()
        # Location services disabled
        if "denied" in stderr.lower() or "disabled" in stderr.lower():
            return None
        return None

    output = proc.stdout.strip()
    if not output:
        return None

    # CoreLocationCLI outputs "lat lon" (space-separated) even with -json flag
    # in some versions. Try to parse as JSON first, then as plain text.
    try:
        data = json.loads(output)
        lat = float(data.get("latitude", data.get("lat", 0)))
        lon = float(data.get("longitude", data.get("lon", data.get("lng", 0))))
        if lat == 0 and lon == 0:
            return None
        return {
            "lat": round(lat, 6),
            "lon": round(lon, 6),
            "accuracy": "wifi",
            "provider": "corelocationcli",
        }
    except json.JSONDecodeError:
        parts = output.split()
        if len(parts) >= 2:
            try:
                lat = float(parts[0])
                lon = float(parts[1])
                return {
                    "lat": round(lat, 6),
                    "lon": round(lon, 6),
                    "accuracy": "wifi",
                    "provider": "corelocationcli",
                }
            except (ValueError, IndexError):
                pass

    return None


if __name__ == "__main__":
    import sys
    result = get_macos_location()
    if result:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("macOS location unavailable", file=sys.stderr)
        sys.exit(1)
