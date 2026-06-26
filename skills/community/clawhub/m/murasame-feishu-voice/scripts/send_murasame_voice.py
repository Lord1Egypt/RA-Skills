import json
import os
import random
import re
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path
import urllib.request

# Workspace defaults
WORKSPACE = Path(r"C:\Users\chenxun\.nanobot\workspace")
MURASAME_DIR = WORKSPACE / "murasame-voice" / "audios"

# Simple keyword mapping: category -> list of mp3 filenames
# Expand in references/mapping.json as needed
DEFAULT_MAP = {
    "agree": ["mur314_016.mp3", "mur312_012.mp3"],
    "greet_morning": ["mur002_001.mp3", "mur315_023.mp3", "mur302_001.mp3"],
    "greet_night": ["mur305_166.mp3", "mur314_019.mp3", "mur314_213.mp3"],
    "thanks": ["mur313_093.mp3"],
    "wait": ["mur303_080.mp3", "mur306_055.mp3", "mur311_023.mp3"],
    "rest": ["mur313_037.mp3", "mur312_031.mp3", "mur311_058.mp3"],
    "encourage": ["mur312_045.mp3", "mur313_041.mp3"],
    "explain": ["mur302_097.mp3"],
}

RULES = [
    (re.compile(r"(早上好|早安|早)"), "greet_morning"),
    (re.compile(r"(晚安|晚安啦|睡了|夜)"), "greet_night"),
    (re.compile(r"(谢谢|多谢|感谢)"), "thanks"),
    (re.compile(r"(好|可以|行|OK|没问题)"), "agree"),
    (re.compile(r"(等等|等下|稍等)"), "wait"),
    (re.compile(r"(休息|累|辛苦)"), "rest"),
]


def find_bin(name):
    env_key = f"{name.upper()}_PATH"
    if env_key in os.environ and Path(os.environ[env_key]).exists():
        return os.environ[env_key]
    return name


def run_cmd(cmd, env=None):
    res = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if res.returncode != 0:
        raise RuntimeError(res.stderr.strip() or res.stdout.strip())
    return res.stdout.strip()


def get_token(app_id, app_secret):
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    token = data.get("tenant_access_token")
    if not token:
        raise RuntimeError(f"Token error: {data}")
    return token


def ffprobe_duration(ffprobe, opus_path):
    out = run_cmd([
        ffprobe,
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(opus_path),
    ])
    if not out:
        raise RuntimeError("Failed to read duration")
    return float(out)


def multipart_form(fields, files):
    boundary = "----WebKitFormBoundary" + uuid.uuid4().hex
    lines = []
    for name, value in fields.items():
        lines.append(f"--{boundary}")
        lines.append(f"Content-Disposition: form-data; name=\"{name}\"")
        lines.append("")
        lines.append(str(value))
    for name, (filename, content_type, data) in files.items():
        lines.append(f"--{boundary}")
        lines.append(
            f"Content-Disposition: form-data; name=\"{name}\"; filename=\"{filename}\""
        )
        lines.append(f"Content-Type: {content_type}")
        lines.append("")
        lines.append(data)
    lines.append(f"--{boundary}--")

    body = b""
    for part in lines:
        if isinstance(part, bytes):
            body += part + b"\r\n"
        else:
            body += part.encode("utf-8") + b"\r\n"
    return boundary, body


def upload_audio(token, opus_path, duration_ms):
    url = "https://open.feishu.cn/open-apis/im/v1/files"
    fields = {
        "file_type": "opus",
        "file_name": "voice.opus",
        "duration": str(int(duration_ms)),
    }
    files = {
        "file": ("voice.opus", "audio/opus", Path(opus_path).read_bytes()),
    }
    boundary, body = multipart_form(fields, files)
    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if data.get("code") != 0:
        raise RuntimeError(f"Upload failed: {data}")
    return data["data"]["file_key"]


def send_audio(token, receiver, file_key, duration_ms):
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
    payload = {
        "receive_id": receiver,
        "msg_type": "audio",
        "content": json.dumps({"file_key": file_key, "duration": int(duration_ms)}),
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Send failed (HTTP {e.code}): {err_body}")
    if data.get("code") != 0:
        raise RuntimeError(f"Send failed: {data}")
    return data


def load_mapping():
    mapping_file = Path(__file__).parent.parent / "references" / "mapping.json"
    if mapping_file.exists():
        return json.loads(mapping_file.read_text(encoding="utf-8"))
    return DEFAULT_MAP


def choose_voice(text, mapping):
    # Expect LLM to prepend a category like "[agree]" or "[thanks]" if it can be expressed.
    tag = None
    body = text.strip()
    m = re.match(r"\[(?P<tag>[^\]]+)\]\s*(?P<body>.*)", body)
    if m:
        tag = m.group("tag").strip().lower()
        body = m.group("body").strip()
    if tag and tag in mapping:
        choices = mapping.get(tag)
        if choices:
            return tag, random.choice(choices), body
    # fallback to keyword rules
    for pattern, key in RULES:
        if pattern.search(body):
            choices = mapping.get(key)
            if choices:
                return key, random.choice(choices), body
    return None, None, body


def get_state_file():
    return WORKSPACE / "murasame_voice_state.txt"


def read_state():
    state_file = get_state_file()
    if state_file.exists():
        return state_file.read_text(encoding="utf-8").strip().lower()
    return "on"


def write_state(value: str):
    state_file = get_state_file()
    state_file.write_text(value.strip().lower(), encoding="utf-8")


def main():
    if len(sys.argv) < 2:
        print("Usage: python send_murasame_voice.py <text>")
        sys.exit(1)

    text = sys.argv[1]

    # Only use env var for receiver
    receiver = os.getenv("FEISHU_RECEIVER")
    if not receiver:
        raise SystemExit("Missing FEISHU_RECEIVER")

    # Command toggle
    cmd = text.strip().lower()
    if cmd in {"/murasame on", "/murasame off"}:
        state = "on" if cmd.endswith("on") else "off"
        write_state(state)
        print(f"VOICE_{state.upper()}")
        return

    # Feature toggle (env overrides state file)
    enable = os.getenv("MURASAME_VOICE", "").strip().lower()
    if enable in {"0", "off", "false", "no"}:
        print("VOICE_DISABLED")
        return
    if enable in {"1", "on", "true", "yes"}:
        pass
    else:
        if read_state() in {"0", "off", "false", "no"}:
            print("VOICE_DISABLED")
            return

    mapping = load_mapping()
    key, filename, body = choose_voice(text, mapping)
    if not filename:
        print("NO_VOICE")
        return

    audio_path = MURASAME_DIR / filename
    if not audio_path.exists():
        raise SystemExit(f"Audio not found: {audio_path}")

    # Delegate sending to feishu-voice sender (proven working)
    sender_script = Path(__file__).parent.parent.parent / "feishu-voice" / "scripts" / "send_voice_file.py"
    if not sender_script.exists():
        raise SystemExit(f"Missing sender script: {sender_script}")

    receiver = (receiver or "").strip()

    # Always pass receiver via env
    env = os.environ.copy()
    env["FEISHU_RECEIVER"] = receiver

    # 1) send text first (reduce perceived delay)
    text_sender = Path(__file__).parent.parent / "scripts" / "send_text.py"
    if text_sender.exists():
        env["MURASAME_TEXT"] = body
        run_cmd([
            sys.executable,
            str(text_sender),
            "_",
        ], env=env)

    # 2) send voice (async)
    subprocess.Popen([
        sys.executable,
        str(sender_script),
        str(audio_path),
    ], env=env)

    print(f"OK: sent text+voice (async) for {key}")


if __name__ == "__main__":
    main()
