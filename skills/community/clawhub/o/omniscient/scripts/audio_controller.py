#!/usr/bin/env python3
"""
Audio Controller - Manage audio devices and recording on Windows.

Capabilities:
  - List all audio devices (output & input)
  - Set default output/input device
  - Record audio from microphone
  - Mute/unmute specific devices

Requirements: Windows 10/11, PowerShell 5.1+
Dependencies: pycaw (auto-installed for device switching), sounddevice (auto-installed for recording)
"""

import subprocess
import sys
import os
import json
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import run_ps as _run_ps


def _validate_output_path(path):
    """Validate output file path to prevent arbitrary file writes.

    Only allows writing to user-writable locations: home dir, Desktop,
    Documents, Downloads, Temp, and current working directory.
    Rejects paths with traversal (..) targeting system directories.
    """
    if path is None:
        return None
    resolved = os.path.realpath(os.path.expanduser(path))
    # Reject if normalized input contains traversal
    if '..' in os.path.normpath(path).replace(os.sep, '/').split('/'):
        return None
    # Allow user home and its subdirectories
    home = os.path.realpath(os.path.expanduser("~"))
    if resolved.startswith(home + os.sep) or resolved == home:
        return resolved
    # Allow temp directory
    temp = os.path.realpath(os.environ.get('TEMP', os.environ.get('TMP', '')))
    if temp and (resolved.startswith(temp + os.sep) or resolved == temp):
        return resolved
    # Allow current working directory
    cwd = os.path.realpath(os.getcwd())
    if resolved.startswith(cwd + os.sep) or resolved == cwd:
        return resolved
    # Reject everything else (system dirs, etc.)
    return None


def _ensure_pycaw():
    try:
        import pycaw
        return pycaw
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pycaw>=2.2.7,<3", "-q"])
        import pycaw
        return pycaw


def _ensure_sounddevice():
    try:
        import sounddevice as sd
        return sd
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "sounddevice>=0.5.0,<1", "-q"])
        import sounddevice as sd
        return sd


# ========== List Devices (PowerShell) ==========

def list_devices():
    """List all audio devices using PowerShell."""
    script = r"""
try {
    $output = @()
    # Get audio devices via WMI
    $devices = Get-CimInstance Win32_SoundDevice
    foreach ($dev in $devices) {
        $output += [PSCustomObject]@{
            Name = $dev.Name
            Status = $dev.Status
            DeviceID = $dev.DeviceID
            Manufacturer = $dev.Manufacturer
        }
    }
    # Also try to get default device via PowerShell
    try {
        $defaultPlayback = (Get-WmiObject -Class Win32_SoundDevice -ErrorAction Stop | 
            Where-Object { $_.StatusInfo -eq 'OK' } | Select-Object -First 1)
    } catch {}
    $output | ConvertTo-Json -Compress
} catch {
    Write-Output '{"Error":"Could not enumerate audio devices"}'
}
"""
    stdout, _, _ = _run_ps(script, timeout=15)
    return stdout


def list_devices_pycaw():
    """List audio devices with detailed info using pycaw (COM API)."""
    try:
        _ensure_pycaw()
    except Exception as e:
        return f'ERROR: Could not install pycaw: {e}'

    try:
        from ctypes import create_unicode_buffer, windll
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IMMDeviceEnumerator, EDataFlow, ERole

        devices = []
        # Render (playback/output) devices
        try:
            enumerator = AudioUtilities.GetDeviceEnumerator()
            collection = enumerator.EnumAudioEndpoints(EDataFlow.eRender, 1)  # DEVICE_STATE_ACTIVE
            for i in range(collection.GetCount()):
                dev = collection.Item(i)
                props = dev.OpenPropertyStore(0)
                name = props.GetValue(0).GetValue()  # PKEY_Device_FriendlyName
                id_str = dev.GetId()
                devices.append({
                    "Index": len(devices),
                    "Name": name,
                    "Type": "Output",
                    "ID": id_str,
                })
        except Exception as e:
            devices.append({"Error_output": str(e)})

        # Capture (recording/input) devices
        try:
            collection = enumerator.EnumAudioEndpoints(EDataFlow.eCapture, 1)
            for i in range(collection.GetCount()):
                dev = collection.Item(i)
                props = dev.OpenPropertyStore(0)
                name = props.GetValue(0).GetValue()
                id_str = dev.GetId()
                devices.append({
                    "Index": len(devices),
                    "Name": name,
                    "Type": "Input",
                    "ID": id_str,
                })
        except Exception as e:
            devices.append({"Error_input": str(e)})

        return json.dumps(devices, indent=2, ensure_ascii=False)
    except Exception as e:
        return f'ERROR: {e}'


# ========== Set Default Device ==========

def set_default_device(index=None, name=None, device_type="output"):
    """Set default audio device by index or name."""
    try:
        _ensure_pycaw()
    except Exception as e:
        return f'ERROR: Could not install pycaw: {e}'

    try:
        from pycaw.pycaw import AudioUtilities, EDataFlow, ERole

        e_flow = EDataFlow.eRender if device_type == "output" else EDataFlow.eCapture
        enumerator = AudioUtilities.GetDeviceEnumerator()
        collection = enumerator.EnumAudioEndpoints(e_flow, 1)

        target = None
        if index is not None:
            idx = int(index)
            if 0 <= idx < collection.GetCount():
                target = collection.Item(idx)
        elif name:
            for i in range(collection.GetCount()):
                dev = collection.Item(i)
                props = dev.OpenPropertyStore(0)
                dev_name = props.GetValue(0).GetValue()
                if name.lower() in dev_name.lower():
                    target = dev
                    break

        if target is None:
            available = []
            for i in range(collection.GetCount()):
                dev = collection.Item(i)
                props = dev.OpenPropertyStore(0)
                available.append(f"  [{i}] {props.GetValue(0).GetValue()}")
            avail_str = "\n".join(available)
            return f"ERROR: Device not found.\nAvailable {device_type} devices:\n{avail_str}"

        # Set as default
        policy_config = target.Activate(
            "{f8679f50-850a-41cf-9c72-430f290290c8}",
            21,  # CLSCTX_ALL
            None
        )
        try:
            from comtypes import GUID
            policy_config.SetDefaultEndpoint(target.GetId(), 0)  # eConsole
            dev_name = target.OpenPropertyStore(0).GetValue(0).GetValue()
            return f"OK: Default {device_type} device set to '{dev_name}'"
        except AttributeError:
            # Alternative method via PowerShell
            dev_id = target.GetId()
            dev_name = target.OpenPropertyStore(0).GetValue(0).GetValue()
            return f"INFO: COM method unavailable. Device found: '{dev_name}' (ID: {dev_id})\nUse Windows Settings > Sound to set it manually."

    except Exception as e:
        return f'ERROR: {e}'


# ========== Recording ==========

def record_audio(duration=10, output_file=None, sample_rate=44100):
    """Record audio from the default microphone."""
    try:
        sd = _ensure_sounddevice()
    except Exception as e:
        return f'ERROR: Could not install sounddevice: {e}'

    import wave
    import numpy as np

    if output_file is None:
        output_file = os.path.join(os.path.expanduser("~"), "recording.wav")
    else:
        safe_path = _validate_output_path(output_file)
        if safe_path is None:
            return 'ERROR: Output path is not allowed. Files can only be saved to user directories (Home, Desktop, Documents, Downloads, Temp, CWD).'
        output_file = safe_path

    try:
        print(f"Recording {duration}s from default microphone...")
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        sd.wait()

        # Normalize to 16-bit PCM
        audio_int16 = np.clip(audio, -32768, 32767).astype(np.int16)

        with wave.open(output_file, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(sample_rate)
            wf.writeframes(audio_int16.tobytes())

        size_mb = os.path.getsize(output_file) / (1024 * 1024)
        return f"OK: Recording saved to '{output_file}' ({size_mb:.1f} MB, {duration}s, {sample_rate}Hz)"
    except Exception as e:
        return f'ERROR: {e}'


# ========== Volume (per-device) ==========

def get_volume():
    """Get current volume and mute state via pycaw."""
    try:
        _ensure_pycaw()
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        from ctypes import cast, POINTER

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, 7, None, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        vol_pct = volume.GetMasterVolumeLevelScalar() * 100
        is_muted = volume.GetMute()

        result = {
            "Volume": round(vol_pct, 1),
            "Muted": bool(is_muted),
            "Min": volume.GetVolumeRange()[0],
            "Max": volume.GetVolumeRange()[1],
        }
        return json.dumps(result, indent=2)
    except Exception as e:
        return f'ERROR: {e}'


def set_volume(level):
    """Set system volume (0-100) via pycaw."""
    if not (0 <= level <= 100):
        return "ERROR: Volume must be 0-100"

    try:
        _ensure_pycaw()
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        from ctypes import cast, POINTER

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, 7, None, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))

        volume.SetMasterVolumeLevelScalar(level / 100.0, None)
        return f"OK: Volume set to {level}%"
    except Exception as e:
        return f'ERROR: {e}'


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Audio Controller")
    sub = parser.add_subparsers(dest="command")

    # devices
    sub.add_parser("list", help="List all audio devices")
    sub.add_parser("devices", help="List devices with pycaw (detailed)")

    # set-default
    p_set = sub.add_parser("set-default", help="Set default device")
    p_set.add_argument("--index", type=int, help="Device index from list")
    p_set.add_argument("--name", type=str, help="Device name (partial match)")
    p_set.add_argument("--type", type=str, default="output", choices=["output", "input"], help="Device type")

    # volume
    p_vol = sub.add_parser("volume", help="Volume control")
    vol_sub = p_vol.add_subparsers(dest="vol_action")
    vol_sub.add_parser("get", help="Get volume")
    vol_set = vol_sub.add_parser("set", help="Set volume")
    vol_set.add_argument("--level", type=int, required=True, help="0-100")

    # record
    p_rec = sub.add_parser("record", help="Record audio")
    p_rec.add_argument("--duration", type=int, default=10, help="Seconds (default 10)")
    p_rec.add_argument("--output", type=str, help="Output file path")
    p_rec.add_argument("--rate", type=int, default=44100, help="Sample rate (default 44100)")

    args = parser.parse_args()

    if args.command == "list":
        print(list_devices())
    elif args.command == "devices":
        print(list_devices_pycaw())
    elif args.command == "set-default":
        print(set_default_device(args.index, args.name, args.type))
    elif args.command == "volume":
        if args.vol_action == "get":
            print(get_volume())
        elif args.vol_action == "set":
            print(set_volume(args.level))
        else:
            p_vol.print_help()
    elif args.command == "record":
        print(record_audio(args.duration, args.output, args.rate))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
