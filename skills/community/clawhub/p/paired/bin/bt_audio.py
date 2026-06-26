"""
bt_audio.py — Audio routing helpers for the OpenClaw `bluetooth` skill.

Talks to PipeWire/WirePlumber via wpctl + pw-cli to find Bluetooth audio
sinks and sources, set defaults, control volumes, and switch profiles.

Why subprocess wpctl/pw-cli rather than libpipewire bindings? Because
libpipewire C bindings via Python are heavy (gi or ctypes), and wpctl
is the canonical tool with a stable text format. Trade-off: a tiny bit
of parsing fragility against zero new dependencies.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Optional


def _wpctl(*args: str) -> str:
    """Run `wpctl <args>` and return stdout. Raises on failure."""
    p = subprocess.run(["wpctl", *args], capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(
            f"wpctl {' '.join(args)} failed: {p.stderr.strip() or p.stdout.strip()}"
        )
    return p.stdout


def _pwcli(*args: str) -> str:
    p = subprocess.run(["pw-cli", *args], capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(
            f"pw-cli {' '.join(args)} failed: {p.stderr.strip() or p.stdout.strip()}"
        )
    return p.stdout


def mac_to_bluez_name_fragment(mac: str) -> str:
    """AA:BB:CC:DD:EE:FF -> AA_BB_CC_DD_EE_FF  (PipeWire BT object naming)."""
    return mac.upper().replace(":", "_")


# ---------------------------------------------------------------------------
# Status / inventory
# ---------------------------------------------------------------------------
def list_sinks() -> list[dict]:
    """Parse `wpctl status` → list of {id, name, default, kind=sink}."""
    return _list_audio_objects("Sinks")


def list_sources() -> list[dict]:
    return _list_audio_objects("Sources")


def _list_audio_objects(section: str) -> list[dict]:
    """Generic parser. `section` is one of 'Sinks', 'Sources', 'Devices'."""
    out: list[dict] = []
    raw = _wpctl("status")
    in_audio = False
    in_section = False
    for line in raw.splitlines():
        stripped = line.strip()
        if stripped.startswith("Audio"):
            in_audio = True
            in_section = False
            continue
        if in_audio and stripped.startswith("Video"):
            break  # End of Audio block
        if not in_audio:
            continue
        if stripped.startswith(f"\u251c\u2500 {section}") or stripped.startswith(f"\u2514\u2500 {section}") \
                or stripped.startswith(f"├─ {section}") or stripped.startswith(f"└─ {section}"):
            in_section = True
            continue
        if in_section:
            # Format: "│      ID. Name [vol: 1.00]"  or  "│   *  ID. Name [vol: 1.00]"
            # When current default has a `*` prefix.
            m = re.match(r"[\s\u2502│]+(\*\s+)?([0-9]+)\.\s+(.+?)\s*(?:\[[^\]]*\])?\s*$", line)
            if m:
                is_default = bool(m.group(1))
                obj_id = int(m.group(2))
                name = m.group(3).strip()
                out.append({"id": obj_id, "name": name, "default": is_default})
            elif stripped.startswith("├─ ") or stripped.startswith("└─ "):
                in_section = False  # next sub-section
    return out


def find_bluez_sink(mac: str) -> Optional[dict]:
    """Return the wpctl sink dict for a paired+connected BT device, or None.

    PipeWire names BT sinks like
       bluez_output.AA_BB_CC_DD_EE_FF.a2dp-sink
    but `wpctl status` shows the friendly form (e.g. "JBL GO 4 (A2DP Sink)").
    We use `pw-cli list-objects Node` to get the bluez_output object path
    and then map to a wpctl id via the object.serial property.
    """
    frag = mac_to_bluez_name_fragment(mac)
    raw = _pwcli("list-objects", "Node")
    # pw-cli emits stanzas separated by blank lines; each has lines like
    #     id 84, type PipeWire:Interface:Node/3
    #         object.serial = "84"
    #         node.name = "bluez_output.AA_BB_CC_DD_EE_FF.a2dp-sink"
    #         media.class = "Audio/Sink"
    current: dict = {}
    nodes: list[dict] = []
    for line in raw.splitlines():
        if line.startswith("\tid ") or line.startswith("    id "):
            if current:
                nodes.append(current)
            m = re.search(r"id\s+(\d+)", line)
            current = {"id": int(m.group(1)) if m else None, "props": {}}
        elif "=" in line:
            k, _, v = line.strip().partition("=")
            v = v.strip().strip('"')
            current.setdefault("props", {})[k.strip()] = v
    if current:
        nodes.append(current)

    for n in nodes:
        node_name = n.get("props", {}).get("node.name", "")
        media_cls = n.get("props", {}).get("media.class", "")
        if frag in node_name and "Sink" in media_cls and "bluez_output" in node_name:
            return {
                "id": n["id"],
                "node_name": node_name,
                "device_api": n.get("props", {}).get("device.api"),
                "media_class": media_cls,
                "node_description": n.get("props", {}).get("node.description"),
            }
    return None


def find_bluez_source(mac: str) -> Optional[dict]:
    """Find a BT audio source (e.g. phone-as-mic via HFP, or A2DP source mode)."""
    frag = mac_to_bluez_name_fragment(mac)
    raw = _pwcli("list-objects", "Node")
    current: dict = {}
    nodes: list[dict] = []
    for line in raw.splitlines():
        if line.startswith("\tid ") or line.startswith("    id "):
            if current:
                nodes.append(current)
            m = re.search(r"id\s+(\d+)", line)
            current = {"id": int(m.group(1)) if m else None, "props": {}}
        elif "=" in line:
            k, _, v = line.strip().partition("=")
            v = v.strip().strip('"')
            current.setdefault("props", {})[k.strip()] = v
    if current:
        nodes.append(current)
    for n in nodes:
        node_name = n.get("props", {}).get("node.name", "")
        media_cls = n.get("props", {}).get("media.class", "")
        if frag in node_name and "Source" in media_cls and "bluez_input" in node_name:
            return {
                "id": n["id"],
                "node_name": node_name,
                "media_class": media_cls,
                "node_description": n.get("props", {}).get("node.description"),
            }
    return None


# ---------------------------------------------------------------------------
# Defaults / volume / mute
# ---------------------------------------------------------------------------
def set_default_sink(sink_id: int) -> None:
    _wpctl("set-default", str(sink_id))


def set_volume(obj_id: int, level: float) -> None:
    """Set volume 0.0–1.0+ (1.0 = 100 %, 1.5 = 150 % over-amplification)."""
    _wpctl("set-volume", str(obj_id), f"{level:.2f}")


def set_volume_pct(obj_id: int, pct: int) -> None:
    set_volume(obj_id, pct / 100.0)


def set_muted(obj_id: int, muted: bool) -> None:
    _wpctl("set-mute", str(obj_id), "1" if muted else "0")


def get_volume(obj_id: int) -> tuple[float, bool]:
    """Return (volume_0_to_1, muted)."""
    raw = _wpctl("get-volume", str(obj_id))
    # Format: "Volume: 0.85 [MUTED]"
    m = re.search(r"Volume:\s+([\d.]+)", raw)
    vol = float(m.group(1)) if m else 0.0
    muted = "MUTED" in raw
    return vol, muted


# ---------------------------------------------------------------------------
# Profiles (BT devices have multiple profiles: A2DP-sink, HFP-headunit, off)
# ---------------------------------------------------------------------------
def list_profiles_for_bt(mac: str) -> list[dict]:
    """Return the BT device's WirePlumber profiles. Requires the device to be paired+connected."""
    frag = mac_to_bluez_name_fragment(mac)
    # Find the device id (not node id) by walking pw-cli list-objects Device
    raw = _pwcli("list-objects", "Device")
    current: dict = {}
    devices: list[dict] = []
    for line in raw.splitlines():
        if line.startswith("\tid ") or line.startswith("    id "):
            if current:
                devices.append(current)
            m = re.search(r"id\s+(\d+)", line)
            current = {"id": int(m.group(1)) if m else None, "props": {}}
        elif "=" in line:
            k, _, v = line.strip().partition("=")
            v = v.strip().strip('"')
            current.setdefault("props", {})[k.strip()] = v
    if current:
        devices.append(current)

    target = next((d for d in devices if frag in d.get("props", {}).get("device.name", "")), None)
    if target is None:
        return []
    # Use wpctl inspect — profiles are listed under "* Spa:Pod:Object:Param:EnumProfile"
    raw = _wpctl("inspect", str(target["id"]))
    profiles: list[dict] = []
    cur: dict = {}
    in_enum = False
    for line in raw.splitlines():
        if "EnumProfile" in line:
            in_enum = True
            continue
        if not in_enum:
            continue
        if line.strip().startswith("Spa:Pod:Object:Param:Profile:"):
            if cur:
                profiles.append(cur)
            cur = {}
        m = re.match(r"\s+([\w.]+)\s*=\s*(.+)", line)
        if m:
            cur[m.group(1).strip()] = m.group(2).strip().strip('"')
    if cur:
        profiles.append(cur)
    return profiles


def set_bt_profile(mac: str, profile_index: int) -> None:
    """Switch a BT device to a different WirePlumber profile (e.g. A2DP -> HFP)."""
    frag = mac_to_bluez_name_fragment(mac)
    raw = _pwcli("list-objects", "Device")
    current: dict = {}
    devices: list[dict] = []
    for line in raw.splitlines():
        if line.startswith("\tid ") or line.startswith("    id "):
            if current:
                devices.append(current)
            m = re.search(r"id\s+(\d+)", line)
            current = {"id": int(m.group(1)) if m else None, "props": {}}
        elif "=" in line:
            k, _, v = line.strip().partition("=")
            v = v.strip().strip('"')
            current.setdefault("props", {})[k.strip()] = v
    if current:
        devices.append(current)

    target = next((d for d in devices if frag in d.get("props", {}).get("device.name", "")), None)
    if target is None:
        raise RuntimeError(f"BT device with MAC {mac} not present in WirePlumber. Connected?")
    _wpctl("set-profile", str(target["id"]), str(profile_index))


# ---------------------------------------------------------------------------
# Playback
# ---------------------------------------------------------------------------
def play_file(path: str, target_id: Optional[int] = None,
              blocking: bool = True) -> subprocess.Popen | int:
    """Play an audio file via pw-play.

    target_id: a sink object id. If None, uses the system default sink.
    blocking:  if True, run pw-play and wait; return exit code.
               if False, fork pw-play and return the Popen handle.
    """
    if not Path(path).exists():
        raise FileNotFoundError(path)
    cmd = ["pw-play"]
    if target_id is not None:
        cmd += ["--target", str(target_id)]
    cmd.append(path)
    if blocking:
        return subprocess.call(cmd)
    return subprocess.Popen(cmd)


def have_pipewire() -> bool:
    return shutil.which("wpctl") is not None and shutil.which("pw-cli") is not None
