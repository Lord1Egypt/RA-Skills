#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import secrets
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
import zipfile
from pathlib import Path


DEFAULT_ROOT = Path.home() / "NapCat.OpenClaw"
DEFAULT_QQ_PACKAGE_ID = "Tencent.QQ.NT"
DEFAULT_NAPCAT_RELEASE_API = "https://api.github.com/repos/NapNeko/NapCatQQ/releases/latest"
DEFAULT_NAPCAT_ASSET = "NapCat.Shell.Windows.Node.zip"
DEFAULT_CONTAINER_IMAGE = "node:23-bookworm"
DEFAULT_BRIDGE_PORT = 3002
DEFAULT_NAPCAT_API_PORT = 3001
DEFAULT_NAPCAT_WS_PORT = 6700
DEFAULT_OPENCLAW_PORT = 18789
DEFAULT_TIMEOUT_SECONDS = 120
SKILL_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = SKILL_DIR / "assets" / "runtime"


def run_command(args: list[str], *, cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    printable = " ".join(shlex.quote(part) for part in args)
    print(f"+ {printable}")
    completed = subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.stdout:
        print(completed.stdout.rstrip())
    if completed.stderr:
        print(completed.stderr.rstrip(), file=sys.stderr)
    if check and completed.returncode != 0:
        raise RuntimeError(f"command failed with exit code {completed.returncode}: {printable}")
    return completed


def run_wsl(distro: str, shell_command: str, *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return run_command(["wsl", "-d", distro, "--", "sh", "-lc", shell_command], check=check)


def read_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def parse_group_ids(raw: str | None) -> list[int] | None:
    if raw is None:
        return None
    values = []
    for piece in raw.split(","):
        piece = piece.strip()
        if not piece:
            continue
        values.append(int(piece))
    return values


def http_json(url: str, *, payload: object | None = None, timeout: int = 10):
    data = None
    headers = {"User-Agent": "napcat-qq-bridge-installer"}
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers, method="POST" if data else "GET")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read().decode("utf-8", errors="replace")
        if not body:
            return {}
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return {"raw": body}


def query_registry_value(key: str, value_name: str) -> str | None:
    completed = run_command(["reg", "query", key, "/v", value_name], check=False)
    if completed.returncode != 0:
        return None
    for line in completed.stdout.splitlines():
        if value_name in line and "REG_" in line:
            parts = line.strip().split(None, 2)
            if len(parts) == 3:
                return parts[2].strip().strip('"')
    return None


def detect_qq_path() -> Path | None:
    keys = [
        r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\QQ",
        r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\QQ",
    ]
    for key in keys:
        uninstall = query_registry_value(key, "UninstallString")
        if not uninstall:
            continue
        candidate = Path(uninstall).parent / "QQ.exe"
        if candidate.exists():
            return candidate
    return None


def ensure_qq_installed(package_id: str) -> Path:
    existing = detect_qq_path()
    if existing:
        return existing
    run_command(
        [
            "winget",
            "install",
            "--id",
            package_id,
            "--exact",
            "--accept-package-agreements",
            "--accept-source-agreements",
        ]
    )
    existing = detect_qq_path()
    if not existing:
        raise RuntimeError("Tencent.QQ.NT appears uninstalled even after winget completed")
    return existing


def fetch_release_payload(url: str) -> dict:
    return http_json(url, timeout=20)


def choose_napcat_asset(release: dict, requested: str | None) -> dict:
    assets = release.get("assets") or []
    if not assets:
        raise RuntimeError("NapCat release API returned no downloadable assets")

    def matches(asset: dict, needle: str) -> bool:
        name = asset.get("name", "")
        return name == needle or needle.lower() in name.lower()

    if requested:
        for asset in assets:
            if matches(asset, requested):
                return asset
        raise RuntimeError(f"NapCat asset not found in latest release: {requested}")

    preferred = [
        DEFAULT_NAPCAT_ASSET,
        "NapCat.Shell.Windows.OneKey.zip",
        "NapCat.Framework.zip",
        "NapCat.Shell.zip",
    ]
    for wanted in preferred:
        for asset in assets:
            if matches(asset, wanted):
                return asset

    for asset in assets:
        if str(asset.get("name", "")).lower().endswith(".zip"):
            return asset
    raise RuntimeError("NapCat release has assets, but none look like a .zip package")


def download_file(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": "napcat-qq-bridge-installer"}),
        timeout=60,
    ) as response:
        with destination.open("wb") as handle:
            shutil.copyfileobj(response, handle)


def locate_runtime_root(extracted_root: Path) -> Path:
    direct_markers = {"napcat.mjs", "NapCatWinBootMain.exe"}
    if any((extracted_root / marker).exists() for marker in direct_markers):
        return extracted_root

    candidates: list[Path] = []
    for path in extracted_root.rglob("*"):
        if not path.is_dir():
            continue
        if any((path / marker).exists() for marker in direct_markers):
            candidates.append(path)
    if not candidates:
        raise RuntimeError("Could not find NapCat runtime files after extracting the downloaded archive")
    candidates.sort(key=lambda item: len(item.parts))
    return candidates[0]


def copy_tree(source: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for entry in source.iterdir():
        target = destination / entry.name
        if entry.is_dir():
            copy_tree(entry, target)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(entry, target)


def install_napcat_runtime(root: Path, asset_name: str | None, force: bool) -> dict:
    napcat_home = root / "napcat"
    release = fetch_release_payload(DEFAULT_NAPCAT_RELEASE_API)
    asset = choose_napcat_asset(release, asset_name)
    with tempfile.TemporaryDirectory(prefix="napcat-skill-") as temp_dir:
        temp_root = Path(temp_dir)
        archive_path = temp_root / asset["name"]
        extract_root = temp_root / "extract"
        print(f"Downloading {asset['name']} from {asset['browser_download_url']}")
        download_file(asset["browser_download_url"], archive_path)
        with zipfile.ZipFile(archive_path) as zip_handle:
            zip_handle.extractall(extract_root)
        runtime_root = locate_runtime_root(extract_root)
        if force and napcat_home.exists():
            for stale in ("bridge.mjs",):
                candidate = napcat_home / stale
                if candidate.exists():
                    candidate.unlink()
        copy_tree(runtime_root, napcat_home)
    return {
        "release": release.get("tag_name"),
        "asset": asset.get("name"),
        "destination": str(napcat_home),
    }


def ensure_openclaw_container(distro: str, container_name: str, openclaw_port: int) -> None:
    quoted = shlex.quote(container_name)
    names = run_wsl(distro, "docker ps -a --format '{{.Names}}'", check=False).stdout.splitlines()
    if container_name not in {name.strip() for name in names}:
        run_wsl(distro, f"docker pull {shlex.quote(DEFAULT_CONTAINER_IMAGE)}")
        create_cmd = (
            "docker create "
            f"--name {quoted} "
            f"-p {openclaw_port}:18789 "
            "-v openclaw-home:/root/.openclaw "
            "-w /root "
            f"{shlex.quote(DEFAULT_CONTAINER_IMAGE)} sleep infinity"
        )
        run_wsl(distro, create_cmd)
    run_wsl(distro, f"docker start {quoted} >/dev/null 2>&1 || true")
    run_wsl(
        distro,
        f"docker exec {quoted} sh -lc \"command -v openclaw >/dev/null 2>&1 || npm install -g openclaw\"",
    )


def load_existing_runtime(root: Path) -> dict:
    napcat_home = root / "napcat"
    config_dir = napcat_home / "config"
    bridge_cfg = read_json(config_dir / "bridge.json", {})
    webui_cfg = read_json(config_dir / "webui.json", {})
    env_cfg = {}
    env_path = config_dir / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                env_cfg[key.strip()] = value.strip()

    onebot_files = sorted(config_dir.glob("onebot11_*.json"))
    onebot_cfg = read_json(onebot_files[0], {}) if onebot_files else {}
    bot_qq = bridge_cfg.get("bot", {}).get("qq")
    if not bot_qq and onebot_files:
        suffix = onebot_files[0].stem.split("_", 1)[-1]
        if suffix.isdigit():
            bot_qq = int(suffix)

    network_cfg = onebot_cfg.get("network", {})
    http_servers = network_cfg.get("httpServers") or [{}]
    ws_servers = network_cfg.get("websocketServers") or [{}]

    return {
        "bot_qq": bot_qq,
        "admin_qq": bridge_cfg.get("bot", {}).get("adminQq"),
        "group_ids": bridge_cfg.get("monitoredGroups"),
        "wsl_distro": bridge_cfg.get("openClaw", {}).get("wslDistro"),
        "container_name": bridge_cfg.get("openClaw", {}).get("container"),
        "bridge_port": bridge_cfg.get("bridge", {}).get("httpPort"),
        "napcat_api_port": http_servers[0].get("port"),
        "napcat_ws_port": ws_servers[0].get("port"),
        "openclaw_port": bridge_cfg.get("openClaw", {}).get("healthUrl", f"http://127.0.0.1:{DEFAULT_OPENCLAW_PORT}/health").rsplit(":", 1)[-1].split("/", 1)[0],
        "api_token": bridge_cfg.get("napcat", {}).get("apiToken"),
        "webui_token": webui_cfg.get("token"),
        "quick_account": webui_cfg.get("autoLoginAccount") or env_cfg.get("NAPCAT_QUICK_ACCOUNT"),
    }


def build_settings(args: argparse.Namespace) -> dict:
    existing = load_existing_runtime(args.Root)
    bot_qq = args.BotQq or existing.get("bot_qq")
    if args.Action in {"install", "repair"} and not bot_qq:
        raise RuntimeError("-BotQq is required when the runtime does not already have a configured QQ account")

    parsed_groups = parse_group_ids(args.GroupIds)
    openclaw_port = args.OpenClawPort or existing.get("openclaw_port") or DEFAULT_OPENCLAW_PORT
    return {
        "root": args.Root,
        "napcat_home": args.Root / "napcat",
        "bot_qq": int(bot_qq) if bot_qq else None,
        "admin_qq": int(args.AdminQq or existing.get("admin_qq") or 0),
        "group_ids": parsed_groups if parsed_groups is not None else (existing.get("group_ids") or []),
        "wsl_distro": args.WslDistro or existing.get("wsl_distro") or "Ubuntu-22.04",
        "container_name": args.ContainerName or existing.get("container_name") or "openclaw-qq-bridge",
        "bridge_port": int(args.BridgePort or existing.get("bridge_port") or DEFAULT_BRIDGE_PORT),
        "napcat_api_port": int(args.NapCatApiPort or existing.get("napcat_api_port") or DEFAULT_NAPCAT_API_PORT),
        "napcat_ws_port": int(args.NapCatWsPort or existing.get("napcat_ws_port") or DEFAULT_NAPCAT_WS_PORT),
        "openclaw_port": int(openclaw_port),
        "api_token": args.ApiToken or existing.get("api_token") or secrets.token_hex(16),
        "webui_token": existing.get("webui_token") or secrets.token_hex(6),
    }


def render_runtime_files(settings: dict) -> dict:
    root = settings["root"]
    napcat_home = settings["napcat_home"]
    config_dir = napcat_home / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    (napcat_home / "logs").mkdir(parents=True, exist_ok=True)
    (napcat_home / "chat-logs").mkdir(parents=True, exist_ok=True)

    shutil.copy2(ASSETS_DIR / "bridge.mjs", napcat_home / "bridge.mjs")

    placeholders = {
        "__BOT_QQ__": str(settings["bot_qq"]),
        "__WSL_DISTRO__": settings["wsl_distro"],
        "__CONTAINER_NAME__": settings["container_name"],
        "__BRIDGE_PORT__": str(settings["bridge_port"]),
        "__NAPCAT_API_PORT__": str(settings["napcat_api_port"]),
        "__NAPCAT_WS_PORT__": str(settings["napcat_ws_port"]),
        "__OPENCLAW_PORT__": str(settings["openclaw_port"]),
    }
    for template_name, destination_name in (
        ("start-all.bat.txt", "start-all.bat"),
        ("stop-all.bat.txt", "stop-all.bat"),
    ):
        content = (ASSETS_DIR / template_name).read_text(encoding="utf-8")
        for key, value in placeholders.items():
            content = content.replace(key, value)
        write_text(root / destination_name, content)

    bridge_config = {
        "bot": {
            "qq": settings["bot_qq"],
            "adminQq": settings["admin_qq"],
            "name": "Assistant",
        },
        "monitoredGroups": settings["group_ids"],
        "humanLike": {
            "enabled": True,
            "typingIndicator": True,
            "randomDelay": True,
            "probabilisticIgnore": True,
            "ignorePatterns": ["^ok$", "^\\.+$", "^emm+$", "^hi$", "^hello$"],
            "ignoreChance": 0.25,
            "minReplyDelayMs": 1200,
            "maxReplyDelayMs": 4000,
            "typingSpeedCps": 5,
        },
        "bridge": {
            "httpPort": settings["bridge_port"],
            "logDir": "./chat-logs",
        },
        "napcat": {
            "apiUrl": f"http://127.0.0.1:{settings['napcat_api_port']}",
            "apiToken": settings["api_token"],
            "wsUrl": f"ws://127.0.0.1:{settings['napcat_ws_port']}",
        },
        "openClaw": {
            "wslDistro": settings["wsl_distro"],
            "container": settings["container_name"],
            "timeoutSeconds": DEFAULT_TIMEOUT_SECONDS,
            "healthUrl": f"http://127.0.0.1:{settings['openclaw_port']}/health",
        },
        "persona": {
            "tone": "calm, restrained, observant, precise, slightly cool, quietly caring",
            "extraRules": "Do not use fixed honorifics or nicknames unless the user does first.",
        },
    }
    write_json(config_dir / "bridge.json", bridge_config)

    onebot_config = {
        "network": {
            "httpServers": [
                {
                    "name": "OpenClawApi",
                    "enable": True,
                    "host": "0.0.0.0",
                    "port": settings["napcat_api_port"],
                    "enableCors": True,
                    "enableWebsocket": False,
                    "messagePostFormat": "array",
                    "token": settings["api_token"],
                    "debug": True,
                }
            ],
            "httpSseServers": [],
            "httpClients": [
                {
                    "name": "OpenClawBridge",
                    "enable": True,
                    "url": f"http://127.0.0.1:{settings['bridge_port']}/",
                    "messagePostFormat": "array",
                    "reportSelfMessage": False,
                    "token": "",
                    "debug": True,
                }
            ],
            "websocketServers": [
                {
                    "name": "OpenClawBridge",
                    "enable": True,
                    "host": "0.0.0.0",
                    "port": settings["napcat_ws_port"],
                    "token": "",
                }
            ],
            "websocketClients": [],
            "plugins": [],
        },
        "musicSignUrl": "",
        "enableLocalFile2Url": False,
        "parseMultMsg": False,
        "imageDownloadProxy": "",
    }
    write_json(config_dir / f"onebot11_{settings['bot_qq']}.json", onebot_config)

    webui_path = config_dir / "webui.json"
    webui_config = read_json(webui_path, {"host": "::", "port": 6099, "loginRate": 10})
    webui_config["token"] = webui_config.get("token") or settings["webui_token"]
    webui_config["autoLoginAccount"] = str(settings["bot_qq"])
    write_json(webui_path, webui_config)

    write_text(config_dir / ".env", f"NAPCAT_QUICK_ACCOUNT={settings['bot_qq']}\n")
    return {
        "bridge_config": str(config_dir / "bridge.json"),
        "onebot_config": str(config_dir / f"onebot11_{settings['bot_qq']}.json"),
        "start_script": str(root / "start-all.bat"),
        "stop_script": str(root / "stop-all.bat"),
    }


def ensure_runtime_core(settings: dict) -> None:
    required = [
        settings["napcat_home"] / "NapCatWinBootMain.exe",
        settings["napcat_home"] / "NapCatWinBootHook.dll",
        settings["napcat_home"] / "napcat.mjs",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise RuntimeError("NapCat runtime is incomplete. Missing: " + ", ".join(missing))


def get_health_snapshot(settings: dict) -> dict:
    root = settings["root"]
    napcat_home = settings["napcat_home"]
    snapshot = {
        "root": str(root),
        "napcat_home": str(napcat_home),
        "bridge_exists": (napcat_home / "bridge.mjs").exists(),
        "start_script_exists": (root / "start-all.bat").exists(),
        "stop_script_exists": (root / "stop-all.bat").exists(),
        "bridge_config_exists": (napcat_home / "config" / "bridge.json").exists(),
        "onebot_config_exists": (napcat_home / "config" / f"onebot11_{settings['bot_qq']}.json").exists() if settings["bot_qq"] else False,
    }
    health_url = f"http://127.0.0.1:{settings['bridge_port']}/health"
    try:
        snapshot["bridge_health"] = http_json(health_url, timeout=5)
    except Exception as exc:  # noqa: BLE001
        snapshot["bridge_health_error"] = str(exc)
    return snapshot


def smoke_test(settings: dict) -> dict:
    result = {"health": get_health_snapshot(settings)}
    try:
        openclaw = run_wsl(
            settings["wsl_distro"],
            " ".join(
                [
                    "docker",
                    "exec",
                    shlex.quote(settings["container_name"]),
                    "sh",
                    "-lc",
                    shlex.quote(
                        "openclaw agent --session-id skill-smoketest "
                        "--message 'Reply with exactly RUNTIME_OK.' --json --timeout 120"
                    ),
                ]
            ),
            check=False,
        )
        result["openclaw_exit_code"] = openclaw.returncode
        if openclaw.stdout.strip():
            result["openclaw_stdout"] = openclaw.stdout.strip()
        if openclaw.stderr.strip():
            result["openclaw_stderr"] = openclaw.stderr.strip()
    except Exception as exc:  # noqa: BLE001
        result["openclaw_error"] = str(exc)

    bridge_health = result["health"].get("bridge_health") or {}
    if settings["admin_qq"] and bridge_health.get("napcat_online"):
        try:
            result["qq_send"] = http_json(
                f"http://127.0.0.1:{settings['bridge_port']}/send_qq",
                payload={
                    "type": "private",
                    "target": settings["admin_qq"],
                    "message": f"[self-test {time.strftime('%Y-%m-%d %H:%M:%S')}] napcat-qq-bridge-installer smoke test.",
                },
                timeout=20,
            )
        except Exception as exc:  # noqa: BLE001
            result["qq_send_error"] = str(exc)
    else:
        result["qq_send_skipped"] = True
    return result


def open_auth_terminal(settings: dict) -> None:
    quoted_distro = settings["wsl_distro"].replace("'", "''")
    quoted_container = settings["container_name"].replace("'", "''")
    command = (
        f"wsl -d '{quoted_distro}' -- docker exec -it '{quoted_container}' "
        "openclaw onboard --auth-choice openai-codex"
    )
    run_command(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            f"Start-Process powershell -ArgumentList '-NoExit','-Command','{command}'",
        ]
    )


def start_runtime(settings: dict) -> None:
    ensure_runtime_core(settings)
    start_script = settings["root"] / "start-all.bat"
    if not start_script.exists():
        raise RuntimeError("start-all.bat is missing; run repair or install first")
    run_command(["cmd", "/c", str(start_script)], cwd=settings["root"])


def stop_runtime(settings: dict) -> None:
    stop_script = settings["root"] / "stop-all.bat"
    if not stop_script.exists():
        raise RuntimeError("stop-all.bat is missing; run repair or install first")
    run_command(["cmd", "/c", str(stop_script)], cwd=settings["root"])


def install_action(settings: dict, args: argparse.Namespace) -> dict:
    qq_path = ensure_qq_installed(args.QqPackageId)
    napcat_info = install_napcat_runtime(settings["root"], args.NapCatAsset, args.Force)
    if args.BootstrapOpenClaw:
        ensure_openclaw_container(settings["wsl_distro"], settings["container_name"], settings["openclaw_port"])
    rendered = render_runtime_files(settings)
    return {
        "qq_path": str(qq_path),
        "napcat": napcat_info,
        "rendered": rendered,
    }


def repair_action(settings: dict) -> dict:
    ensure_runtime_core(settings)
    rendered = render_runtime_files(settings)
    return {
        "rendered": rendered,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install and maintain a local NapCat + OpenClaw QQ bridge")
    parser.add_argument("-Action", dest="Action", required=True, choices=["install", "auth", "start", "stop", "repair", "health", "smoke-test"])
    parser.add_argument("-Root", dest="Root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("-BotQq", dest="BotQq", type=int)
    parser.add_argument("-AdminQq", dest="AdminQq", type=int)
    parser.add_argument("-GroupIds", dest="GroupIds")
    parser.add_argument("-WslDistro", dest="WslDistro")
    parser.add_argument("-ContainerName", dest="ContainerName")
    parser.add_argument("-NapCatAsset", dest="NapCatAsset")
    parser.add_argument("-QqPackageId", dest="QqPackageId", default=DEFAULT_QQ_PACKAGE_ID)
    parser.add_argument("-BridgePort", dest="BridgePort", type=int)
    parser.add_argument("-NapCatApiPort", dest="NapCatApiPort", type=int)
    parser.add_argument("-NapCatWsPort", dest="NapCatWsPort", type=int)
    parser.add_argument("-OpenClawPort", dest="OpenClawPort", type=int)
    parser.add_argument("-ApiToken", dest="ApiToken")
    parser.add_argument("-BootstrapOpenClaw", dest="BootstrapOpenClaw", action="store_true")
    parser.add_argument("-StartAfterInstall", dest="StartAfterInstall", action="store_true")
    parser.add_argument("-Force", dest="Force", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    settings = build_settings(args)
    settings["root"].mkdir(parents=True, exist_ok=True)

    if args.Action == "install":
        result = install_action(settings, args)
        if args.StartAfterInstall:
            start_runtime(settings)
            result["started"] = True
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    if args.Action == "repair":
        print(json.dumps(repair_action(settings), indent=2, ensure_ascii=False))
        return 0

    if args.Action == "auth":
        open_auth_terminal(settings)
        print(json.dumps({"ok": True, "message": "Opened a new PowerShell window for openclaw onboard"}, indent=2))
        return 0

    if args.Action == "start":
        start_runtime(settings)
        return 0

    if args.Action == "stop":
        stop_runtime(settings)
        return 0

    if args.Action == "health":
        print(json.dumps(get_health_snapshot(settings), indent=2, ensure_ascii=False))
        return 0

    if args.Action == "smoke-test":
        print(json.dumps(smoke_test(settings), indent=2, ensure_ascii=False))
        return 0

    raise RuntimeError(f"unsupported action: {args.Action}")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1)
