#!/usr/bin/env python3
"""
OpenClaw Agent Live v10 — 一键配置 & 启停脚本（跨平台版）
Linux:   Xvfb + x11grab + 双 fork 守护
Windows: 桌面 tkinter + gdigrab + pythonw 后台
macOS:   桌面 tkinter + avfoundation + 双 fork 守护

v10 变更:
  - 双向交互从 webhook 改为 timbot 渠道（IM 单聊消息触发 agent turn）
  - 公网 Lighthouse IP 访问方式
  - IM UserSig 复用 TRTC TLSSigAPIv2 生成（同一个 SDKAppID + SecretKey）

用法：
  python3 setup.py --sdkappid <YOUR_SDKAPPID> --secret <YOUR_SECRET_KEY>
  python3 setup.py --sdkappid <ID> --secret <KEY> --cam-secret-id <CAM_ID> --cam-secret-key <CAM_KEY>
  python3 setup.py --start
  python3 setup.py --stop
  python3 setup.py --viewer --lighthouse-ip <YOUR_IP>        # 公网 Lighthouse IP
  python3 setup.py --status

获取 SDKAppID / SecretKey:
  1. 访问 TRTC 控制台 → https://console.cloud.tencent.com/trtc/app
  2. 创建或选择一个应用（体验版/尊享版/旗舰版均可）
  3. 在应用详情页复制 SDKAppID 和 SecretKey
"""
import argparse
import json
import os
import random
import re
import shutil
import string
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

try:
    from platform_utils import (
        get_work_dir, get_python_cmd, get_pythonw_cmd,
        is_windows, is_linux, is_mac, needs_xvfb,
        new_session_kwargs, get_platform_tag,
        find_process_by_script, find_process_by_name,
        kill_process, start_daemon_process,
        get_display_str, get_display_num
    )
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from platform_utils import (
        get_work_dir, get_python_cmd, get_pythonw_cmd,
        is_windows, is_linux, is_mac, needs_xvfb,
        new_session_kwargs, get_platform_tag,
        find_process_by_script, find_process_by_name,
        kill_process, start_daemon_process,
        get_display_str, get_display_num
    )

# 导入官方 TLSSigAPIv2 UserSig 生成算法
try:
    from TLSSigAPIv2 import gen_usersig
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from TLSSigAPIv2 import gen_usersig

WORK_DIR   = get_work_dir()
CONFIG_F   = WORK_DIR / "config.json"

# ── Skill 源目录定位（多路径回退）──────────────────────────
# setup.py 可能在两个位置运行：
#   A. Skill 源目录 <skill>/scripts/setup.py  → parent.parent 即 <skill>
#   B. 工作目录 /tmp/trtc_stream/setup.py    → parent.parent 是 /tmp/（错误）
# 策略：检测 parent.parent 下是否存在 assets/ 和 scripts/，否则从 config.json 恢复
def _resolve_skill_dir() -> Path:
    """多路径回退查找 Skill 源目录"""
    # 方案 1: 经典路径（Skill 源目录内运行）
    candidate = Path(__file__).resolve().parent.parent
    if (candidate / "assets").is_dir() and (candidate / "scripts").is_dir():
        return candidate
    # 方案 2: 从 config.json 中恢复之前记录的源路径
    if CONFIG_F.exists():
        try:
            cfg = json.loads(CONFIG_F.read_text())
            saved = cfg.get("skill_source_dir")
            if saved:
                p = Path(saved)
                if (p / "assets").is_dir():
                    return p
        except Exception:
            pass
    # 方案 3: 回退到经典路径（可能不含 assets，后续逻辑会跳过）
    return candidate

SKILL_DIR  = _resolve_skill_dir()
SCRIPTS    = SKILL_DIR / "scripts"
ASSETS     = SKILL_DIR / "assets"

# ── OpenClaw 容器保留端口（HTTP Server 禁止占用这些端口）──────
# 注意：这是 HTTP Server 端口校验用的黑名单，与 Gateway 端口检测无关
# Gateway 可能运行在 23001 等端口上，自动检测会正确处理
RESERVED_PORTS = {23000, 23001, 22999, 4400, 4401, 4402}

# ── Timbot IM 双向交互配置（v10: 替代 webhook） ──────────────
# v10 使用 IM 单聊消息（C2C）触发 Agent turn，不再需要 webhook token
# IM UserSig 复用 TRTC 同一 SDKAppID + SecretKey 生成
# 机器人 UserID 固定为 @RBT#001（IM 内置智能体机器人前缀）

IM_BOT_USERID = "@RBT#001"  # IM 机器人 UserID（观众发消息给它触发 Agent）

# ── 内置 HTTP Server 端口 ────────────────────────────────────
VIEWER_HTTP_PORT = 19000

# ── 自动生成参数 ─────────────────────────────────────────────
def _random_str(length: int = 6, chars: str = string.ascii_lowercase + string.digits) -> str:
    """生成随机字符串（仅小写字母+数字，符合 TRTC strRoomId 限制）"""
    return "".join(random.choices(chars, k=length))

def auto_room_id() -> str:
    """自动生成房间号: openclaw-live-XXXXXX"""
    return f"openclaw-live-{_random_str(6)}"

def auto_userid() -> str:
    """自动生成推流用户ID: streamer-XXXX"""
    return f"streamer-{_random_str(4)}"

def auto_viewer_userid() -> str:
    """自动生成观看用户ID: viewer-XXXX"""
    return f"viewer-{_random_str(4)}"

def auto_im_userid() -> str:
    """自动生成 IM 聊天用户ID: im-viewer-XXXX（观众登录 IM SDK 用）"""
    return f"im-viewer-{_random_str(4)}"


def build_rtmp_url(sdkappid: int, room_id: str,
                   userid: str, usersig: str) -> str:
    return (
        f"rtmp://rtmp.rtc.qq.com/push/{room_id}"
        f"?sdkappid={sdkappid}"
        f"&userid={userid}"
        f"&usersig={usersig}"
    )


# ── 部署脚本到工作目录 ────────────────────────────────────────
def deploy_scripts(cfg: dict):
    WORK_DIR.mkdir(parents=True, exist_ok=True)

    # 防御：SKILL_DIR == WORK_DIR 时跳过自拷贝（避免 rmtree 删除源 assets、脚本自覆盖等问题）
    _same_dir = False
    try:
        _same_dir = SKILL_DIR.resolve() == WORK_DIR.resolve()
    except Exception:
        pass

    if _same_dir:
        print(f"  [=] SKILL_DIR == WORK_DIR ({WORK_DIR}), skip self-copy")
    else:
        script_files = [
            "platform_utils.py",   # 跨平台工具模块（必须先部署）
            "TLSSigAPIv2.py",      # 官方 UserSig 生成算法
            "agent_bus.py",
            "frame_renderer.py",   # Pillow 帧渲染器（替代 tkinter Dashboard）
            "stream_daemon.py",
            "stream_ingest_client.py",  # 在线媒体流推流客户端
            "supervisor.py",
            "tts_client.py",       # 腾讯云 TTS API 封装
            "tts_worker.py",       # TTS 语音播报守护进程
        ]
        for fname in script_files:
            src = SCRIPTS / fname
            dst = WORK_DIR / fname
            if src.exists() and src.resolve() != dst.resolve():
                shutil.copy2(src, dst)
                print(f"  [+] {fname}")

    # Patch stream_daemon.py with RTMP URL
    # 当 SKILL_DIR == WORK_DIR 时，脚本在 scripts/ 子目录而非根目录
    daemon_path = WORK_DIR / "stream_daemon.py"
    if not daemon_path.exists() and (WORK_DIR / "scripts" / "stream_daemon.py").exists():
        daemon_path = WORK_DIR / "scripts" / "stream_daemon.py"
    if daemon_path.exists():
        code = daemon_path.read_text()
        # 匹配双引号字符串格式: RTMP_URL = "..."
        code = re.sub(
            r'RTMP_URL\s*=\s*"[^"]*"',
            f'RTMP_URL = "{cfg["rtmp_url"]}"',
            code
        )
        daemon_path.write_text(code)

    # 复制整个 assets 目录到工作目录（确保运行时能找到 avatar 视频、icons 图标等资源）
    assets_dst = WORK_DIR / "assets"
    if not _same_dir and ASSETS.is_dir():
        try:
            if ASSETS.resolve() != assets_dst.resolve():
                if assets_dst.exists():
                    shutil.rmtree(assets_dst)
                shutil.copytree(ASSETS, assets_dst)
                asset_count = sum(1 for _ in assets_dst.rglob("*") if _.is_file())
                print(f"  [+] assets/ ({asset_count} files)")
            else:
                print(f"  [=] assets/ already in place (src == dst)")
        except Exception as e:
            print(f"  [!] assets copy failed: {e}")
    elif assets_dst.is_dir():
        asset_count = sum(1 for _ in assets_dst.rglob("*") if _.is_file())
        print(f"  [=] assets/ already in place ({asset_count} files)")

    # 兼容：也在工作目录根放一份 viewer 模板（历史逻辑）
    tmpl_src = ASSETS / "trtc-viewer-template.html"
    tmpl_dst = WORK_DIR / "trtc-viewer-template.html"
    if tmpl_src.exists() and tmpl_src.resolve() != tmpl_dst.resolve():
        shutil.copy2(tmpl_src, tmpl_dst)
        print(f"  [+] trtc-viewer-template.html")

    # 记录 Skill 源目录路径，供后续 --start 时恢复 assets
    cfg["skill_source_dir"] = str(SKILL_DIR)

    # 部署预置 skills（email-skill, music-search, weather）
    skills_src = SKILL_DIR / "skills"
    skills_dst = WORK_DIR / "skills"
    if skills_src.is_dir() and skills_src.resolve() != skills_dst.resolve():
        if skills_dst.exists():
            shutil.rmtree(skills_dst)
        shutil.copytree(skills_src, skills_dst)
        skill_names = [d.name for d in skills_dst.iterdir() if d.is_dir()]
        print(f"  [+] skills/ ({', '.join(skill_names)})")

    # Write config
    CONFIG_F.write_text(json.dumps(cfg, indent=2, ensure_ascii=False))
    print(f"  [+] config.json → {CONFIG_F}")


# ── GitHub Avatar 下载（ClawHub 包不含二进制时的回退方案）─────
AVATAR_GITHUB_BASE = "https://raw.githubusercontent.com/jerryang-cool/LiveClaw/main/assets/avatar"
AVATAR_FILES = [
    "idle_alpha.webm",
    "action_alpha.webm",
    "idle_alpha.mov",
    "action_alpha.mov",
]

def _download_avatar_from_github(assets_dst: Path):
    """从 GitHub raw URL 下载 avatar 视频文件到工作目录"""
    from urllib.request import urlretrieve
    avatar_dst = assets_dst / "avatar"
    avatar_dst.mkdir(parents=True, exist_ok=True)

    downloaded = 0
    for fname in AVATAR_FILES:
        dst_file = avatar_dst / fname
        if dst_file.exists():
            continue
        url = f"{AVATAR_GITHUB_BASE}/{fname}"
        try:
            print(f"  [↓] Downloading {fname} ...")
            urlretrieve(url, str(dst_file))
            size_mb = dst_file.stat().st_size / (1024 * 1024)
            print(f"  [+] {fname} ({size_mb:.1f} MB)")
            downloaded += 1
        except Exception as e:
            print(f"  [!] Failed to download {fname}: {e}")
    if downloaded > 0:
        print(f"  [+] Avatar files downloaded from GitHub ({downloaded} files)")
    elif any((avatar_dst / f).exists() for f in AVATAR_FILES):
        print(f"  [=] Avatar files already present")
    else:
        print(f"  [!] Avatar download failed — viewer will use GitHub URL directly")


# ── 确保 assets 已部署到工作目录 ──────────────────────────────
def _ensure_assets_deployed(cfg: dict):
    """检查工作目录中是否存在 assets/ 及其资源文件。
    如果缺失，从 Skill 源目录（或 config 中记录的路径）重新复制。
    这修复了以下场景：
      - 初次 deploy_scripts() 时 setup.py 已被复制到 WORK_DIR，
        __file__ 指向 /tmp/trtc_stream/setup.py，导致 ASSETS 解析到 /tmp/assets/（不存在）
      - 用户更新 Skill 后 assets 有变化，--start 时自动同步
    """
    assets_dst = WORK_DIR / "assets"
    avatar_dst = assets_dst / "avatar"

    # 快速检查：如果已存在且有 avatar 视频，跳过
    avatar_ok = avatar_dst.is_dir() and any(avatar_dst.glob("*.webm"))
    if avatar_ok:
        vid_count = len(list(avatar_dst.glob("*.webm")))
        print(f"  [=] assets/ already deployed ({vid_count} videos)")
        return

    # 需要复制——查找源 assets 目录
    source_assets = None

    # 候选 1: 全局 ASSETS 变量（_resolve_skill_dir 已做过多路径回退）
    if ASSETS.is_dir() and (ASSETS / "avatar").is_dir():
        source_assets = ASSETS

    # 候选 2: config.json 中记录的 skill_source_dir
    if source_assets is None:
        saved_dir = cfg.get("skill_source_dir")
        if saved_dir:
            p = Path(saved_dir) / "assets"
            if p.is_dir() and (p / "avatar").is_dir():
                source_assets = p

    # 候选 3: 遍历常见 Skill 安装位置
    if source_assets is None:
        common_paths = [
            Path.home() / ".openclaw" / "skills" / "openclaw-agent-live" / "assets",
            Path("/opt/openclaw/skills/openclaw-agent-live/assets"),
        ]
        for cp in common_paths:
            if cp.is_dir() and (cp / "avatar").is_dir():
                source_assets = cp
                break

    if source_assets is None:
        print("  [!] Cannot find local assets/avatar — downloading from GitHub...")
        _download_avatar_from_github(assets_dst)
        return

    # 执行复制（防御 source == dst 的情况）
    try:
        if source_assets.resolve() == assets_dst.resolve():
            print(f"  [=] assets/ source == destination, skip copy")
            return
    except Exception:
        pass

    print(f"  [*] Syncing assets from {source_assets} ...")
    try:
        if assets_dst.exists():
            shutil.rmtree(assets_dst)
        shutil.copytree(source_assets, assets_dst)
        asset_count = sum(1 for _ in assets_dst.rglob("*") if _.is_file())
        print(f"  [+] assets/ deployed ({asset_count} files)")

        # 更新 config 中的源路径记录
        cfg["skill_source_dir"] = str(source_assets.parent)
        CONFIG_F.write_text(json.dumps(cfg, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"  [!] Failed to sync assets: {e}")


def _install_main_skill():
    """将主 SKILL (openclaw-agent-live) 安装到 OpenClaw 全局 skills 目录。
    确保 timbot 等外部渠道的 session 能发现本 SKILL 并执行直播上报规则。
    仅在当前对话 session 中临时加载 SKILL.md 不够——其他渠道看不到。
    """
    skill_name = "openclaw-agent-live"

    # 查找 SKILL.md 源（从 SKILL_DIR 或 WORK_DIR）
    skill_md_src = None
    for candidate in [SKILL_DIR / "SKILL.md", WORK_DIR / "SKILL.md"]:
        if candidate.exists():
            skill_md_src = candidate.parent
            break
    if not skill_md_src:
        print(f"  [!] Cannot find SKILL.md source, skip main skill install")
        return

    # 确定目标目录
    openclaw_skills_dir = None
    candidates = [
        Path(os.environ.get("OPENCLAW_SKILLS_DIR", "")) if os.environ.get("OPENCLAW_SKILLS_DIR") else None,
        Path.home() / ".openclaw" / "workspace" / "skills",
        Path("/projects/.openclaw/skills"),
    ]
    for c in candidates:
        if c and c.is_dir():
            openclaw_skills_dir = c
            break
    if not openclaw_skills_dir:
        try:
            default_dir = Path.home() / ".openclaw" / "workspace" / "skills"
            default_dir.mkdir(parents=True, exist_ok=True)
            openclaw_skills_dir = default_dir
        except Exception:
            print(f"  [!] Cannot find or create OpenClaw skills directory")
            return

    dst = openclaw_skills_dir / skill_name

    # 检查是否已安装且 SKILL.md 存在
    if (dst / "SKILL.md").exists():
        print(f"  [=] Main SKILL already installed: {dst}")
        return

    # 安装（复制核心文件：SKILL.md, SKILL.eval.yaml, scripts/, assets/）
    try:
        dst.mkdir(parents=True, exist_ok=True)
        for item_name in ["SKILL.md", "SKILL.eval.yaml", "scripts", "assets", "skills"]:
            src_item = skill_md_src / item_name
            dst_item = dst / item_name
            if src_item.exists() and not dst_item.exists():
                if src_item.is_dir():
                    shutil.copytree(src_item, dst_item)
                else:
                    shutil.copy2(src_item, dst_item)
        print(f"  [+] Main SKILL installed: {dst}")
    except Exception as e:
        # 回退：尝试软链接
        try:
            if dst.exists():
                shutil.rmtree(dst)
            dst.symlink_to(skill_md_src)
            print(f"  [+] Main SKILL symlinked: {dst} -> {skill_md_src}")
        except Exception as e2:
            print(f"  [!] Main SKILL install failed: {e}, symlink also failed: {e2}")


def _install_bundled_skills(cfg: dict):
    """将预置 skill 自动安装到 OpenClaw 的 skill 目录"""
    bundled_skills = ["email-skill", "music-search", "weather"]

    # 确定 OpenClaw skill 目录（优先级：环境变量 > 标准路径）
    openclaw_skills_dir = None
    candidates = [
        Path(os.environ.get("OPENCLAW_SKILLS_DIR", "")) if os.environ.get("OPENCLAW_SKILLS_DIR") else None,
        Path.home() / ".openclaw" / "workspace" / "skills",
        Path("/projects/.openclaw/skills"),
    ]
    for c in candidates:
        if c and c.is_dir():
            openclaw_skills_dir = c
            break

    if not openclaw_skills_dir:
        # 尝试创建默认路径
        default_dir = Path.home() / ".openclaw" / "workspace" / "skills"
        try:
            default_dir.mkdir(parents=True, exist_ok=True)
            openclaw_skills_dir = default_dir
        except Exception:
            print("  [!] Cannot find or create OpenClaw skills directory, skipping bundled skill install")
            return

    # 查找预置 skill 源目录
    skills_src = WORK_DIR / "skills"
    if not skills_src.is_dir():
        skills_src = SKILL_DIR / "skills"
    if not skills_src.is_dir():
        return

    installed = []
    updated = []
    for skill_name in bundled_skills:
        src = skills_src / skill_name
        dst = openclaw_skills_dir / skill_name
        if not src.is_dir():
            continue
        if dst.exists():
            # 已安装 → 强制更新（确保新版文件覆盖旧版）
            try:
                shutil.rmtree(dst)
                shutil.copytree(src, dst)
                updated.append(skill_name)
            except Exception as e:
                print(f"  [!] Failed to update {skill_name}: {e}")
            continue
        try:
            shutil.copytree(src, dst)
            installed.append(skill_name)
        except Exception as e:
            print(f"  [!] Failed to install {skill_name}: {e}")

    if installed:
        print(f"[+] Bundled skills installed to {openclaw_skills_dir}: {', '.join(installed)}")
    if updated:
        print(f"[↑] Bundled skills updated: {', '.join(updated)}")

    # 子 skill 的 SKILL.md 在包中命名为 SKILL_DOC.md（避免 ClawHub 冲突），安装后恢复
    for skill_name in bundled_skills:
        dst = openclaw_skills_dir / skill_name
        doc = dst / "SKILL_DOC.md"
        target = dst / "SKILL.md"
        if doc.exists() and not target.exists():
            doc.rename(target)

    if not installed and not updated:
        existing = [s for s in bundled_skills if (openclaw_skills_dir / s).is_dir()]
        if existing:
            print(f"[=] Bundled skills up to date: {', '.join(existing)}")


def _ensure_avchatroom(cfg: dict):
    """通过 IM REST API 预创建 AVChatRoom 群，避免观众端创建导致消息接收异常"""
    import urllib.request, urllib.parse
    sdkappid = cfg.get("sdkappid")
    secret = cfg.get("secret_key")
    room_id = cfg.get("room_id")
    if not sdkappid or not secret or not room_id:
        return

    try:
        from TLSSigAPIv2 import gen_usersig
        admin_sig = gen_usersig(sdkappid, secret, "administrator", 86400)

        url = (f"https://console.tim.qq.com/v4/group_open_http_svc/create_group"
               f"?sdkappid={sdkappid}&identifier=administrator"
               f"&usersig={urllib.parse.quote(admin_sig)}"
               f"&random={random.randint(10000000, 99999999)}&contenttype=json")

        body = json.dumps({
            "Type": "AVChatRoom",
            "Name": "OpenClaw Live",
            "GroupId": room_id,
            "Owner_Account": "administrator",
        }).encode()

        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())

        code = data.get("ErrorCode", -1)
        if code == 0:
            print(f"[+] AVChatRoom created: {room_id}")
        elif code == 10021:
            print(f"[=] AVChatRoom already exists: {room_id}")
        else:
            print(f"  [!] AVChatRoom create warning: {data.get('ErrorInfo', 'unknown')} (code={code})")
    except Exception as e:
        print(f"  [!] AVChatRoom create failed: {e} (non-fatal, viewers will create on join)")


def _ensure_im_channel(cfg: dict):
    """自动激活 OpenClaw 的 timbot IM 通道（等效于手动 openclaw onboard 选择 Tencent IM）。

    通过 openclaw CLI 非交互式写入配置，实现 Skill 安装后自动激活双向交互能力。
    幂等操作：已激活且参数一致时跳过，参数变化时覆盖更新。

    所需参数（来自 config.json）：
      - sdkappid: TRTC/IM SDKAppID
      - secret_key: TRTC/IM SecretKey
      - callback_token: IM 控制台配置的回调鉴权 Token
    """
    sdkappid = cfg.get("sdkappid")
    secret = cfg.get("secret_key")
    callback_token = cfg.get("callback_token")

    if not sdkappid or not secret:
        return
    if not callback_token:
        print("  [=] IM channel activation skipped (no --callback-token provided)")
        print("      To enable: python3 setup.py --sdkappid <ID> --secret <KEY> --callback-token <TOKEN>")
        return

    # 检查 openclaw CLI 是否可用
    try:
        result = subprocess.run(["openclaw", "--version"], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            print("  [!] openclaw CLI not available, skip IM channel activation")
            return
        print(f"  [*] {result.stdout.strip()}")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("  [!] openclaw CLI not found, skip IM channel activation")
        return

    # ── 前置检测：timbot 插件是否已安装 + 通道是否已配置且参数一致 ──
    # 如果全部满足，直接跳过，避免不必要的 plugins install / config set / gateway restart
    _plugin_installed = False
    _channel_configured = False

    # 检测 timbot 插件是否已安装
    try:
        result = subprocess.run(
            ["openclaw", "plugins", "list"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            output = result.stdout.strip().lower()
            _plugin_installed = "timbot" in output
            if _plugin_installed:
                print(f"  [=] timbot plugin already installed")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # 检测 channels.timbot 配置是否存在且参数一致
    try:
        result = subprocess.run(
            ["openclaw", "config", "get", "channels.timbot"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            existing = result.stdout.strip()
            has_sdkappid = str(sdkappid) in existing
            has_enabled = '"enabled":true' in existing.lower().replace(" ", "")
            has_token = callback_token and callback_token in existing
            # 关键：检查 sdkAppId 是否为字符串类型（被引号包裹）
            # timbot 插件要求 sdkAppId 是字符串，否则 .trim() 报错
            sdkappid_is_string = f'"sdkAppId":"{sdkappid}"' in existing.replace(" ", "")
            if not sdkappid_is_string and has_sdkappid:
                print(f"  [!] sdkAppId is number type (need string), will re-configure")
            _channel_configured = has_sdkappid and has_enabled and has_token and sdkappid_is_string
            if _channel_configured:
                print(f"  [=] IM channel already activated (sdkAppId={sdkappid}, token matched)")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # 全部已就绪 → 跳过安装/配置/重启，避免 gateway 断连
    if _plugin_installed and _channel_configured:
        print(f"  [=] timbot fully configured — skipping install/activate/gateway restart")
        return

    print(f"  [*] Activating IM channel (timbot)...")

    # 1. 安装 timbot 插件（仅在未安装时执行）
    if not _plugin_installed:
        try:
            result = subprocess.run(
                ["openclaw", "plugins", "install", "timbot"],
                capture_output=True, text=True, timeout=60
            )
            if result.returncode == 0:
                print(f"  [+] timbot plugin installed")
            else:
                stderr = result.stderr.strip()
                if "already" in stderr.lower() or "exists" in stderr.lower():
                    print(f"  [=] timbot plugin already installed")
                else:
                    print(f"  [!] timbot plugin install warning: {stderr[:200]}")
        except (FileNotFoundError, subprocess.TimeoutExpired) as e:
            print(f"  [!] timbot plugin install failed: {e}")
            return

    # 2. 写入 timbot 通道配置
    # 关键：sdkAppId 必须是字符串类型（timbot 插件内部调用 .trim()），
    # 如果存为 number 类型会导致 "merged.sdkAppId?.trim is not a function" 错误
    timbot_config = {
        "enabled": True,
        "sdkAppId": str(sdkappid),
        "secretKey": secret,
        "token": callback_token,
        "botAccount": IM_BOT_USERID,
        "webhookPath": "/timbot",
        "dm": {"policy": "open", "allowFrom": ["*"]},
        "allowFrom": ["*"],
        "streamingMode": "tim_stream",
        "typingText": "正在思考中...",
        "fallbackPolicy": "final_text",
        "overflowPolicy": "split",
    }

    _config_ok = False

    # 方式 1: batch-json（JSON 类型信息完整，sdkAppId 保证是字符串）
    try:
        batch_json = json.dumps({"channels.timbot": timbot_config})
        result = subprocess.run(
            ["openclaw", "config", "set", "--batch-json", batch_json],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            _config_ok = True
            print(f"  [+] IM channel configured via batch-json (sdkAppId={sdkappid})")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    # 方式 2: 整体 JSON 值写入（保留类型）
    if not _config_ok:
        try:
            config_json_str = json.dumps(timbot_config)
            result = subprocess.run(
                ["openclaw", "config", "set", "channels.timbot", config_json_str],
                capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0:
                _config_ok = True
                print(f"  [+] IM channel configured via json-value (sdkAppId={sdkappid})")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

    # 方式 3: 逐字段写入（最后手段，sdkAppId 用 JSON 引号包裹防止 CLI 转数字）
    if not _config_ok:
        _fields = [
            ("channels.timbot.enabled", "true"),
            ("channels.timbot.sdkAppId", json.dumps(str(sdkappid))),  # JSON 字符串: "\"1400796881\""
            ("channels.timbot.secretKey", secret),
            ("channels.timbot.token", callback_token),
            ("channels.timbot.botAccount", IM_BOT_USERID),
            ("channels.timbot.webhookPath", "/timbot"),
            ("channels.timbot.streamingMode", "tim_stream"),
            ("channels.timbot.typingText", "正在思考中..."),
            ("channels.timbot.fallbackPolicy", "final_text"),
            ("channels.timbot.overflowPolicy", "split"),
        ]
        _ok = True
        for path, val in _fields:
            r = subprocess.run(
                ["openclaw", "config", "set", path, val],
                capture_output=True, text=True, timeout=10
            )
            if r.returncode != 0:
                _ok = False
                break
        if _ok:
            _config_ok = True
            print(f"  [+] IM channel configured field-by-field (sdkAppId={sdkappid})")
        else:
            print(f"  [!] IM channel config set failed")
            return

    if not _config_ok:
        print(f"  [!] All config set methods failed")
        return

    # 3. 启用插件
    try:
        subprocess.run(
            ["openclaw", "config", "set", "plugins.entries.timbot.enabled", "true"],
            capture_output=True, text=True, timeout=10
        )
    except Exception:
        pass

    # 4. 设置 gateway 监听公网
    try:
        subprocess.run(
            ["openclaw", "config", "set", "gateway.bind", "lan"],
            capture_output=True, text=True, timeout=10
        )
    except Exception:
        pass

    # 5. 检测 gateway 实际端口（不同 OpenClaw 版本端口可能不同）
    _gw_port = None
    try:
        result = subprocess.run(
            ["openclaw", "config", "get", "gateway.port"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            port_str = result.stdout.strip().split('\n')[-1].strip()
            # 可能返回 "gateway.port = 18789" 或纯数字
            for part in port_str.split():
                if part.isdigit():
                    _gw_port = int(part)
                    break
    except Exception:
        pass

    print(f"  [+] IM channel configured (sdkAppId={sdkappid})")
    if _gw_port:
        print(f"  [*] Gateway port: {_gw_port}")
    print(f"")
    print(f"  ⚠️  需要手动执行以下步骤使 timbot 通道生效：")
    print(f"      1. openclaw gateway restart")
    print(f"      2. netstat -lnpt | grep openclaw    # 确认 gateway 端口监听在 0.0.0.0")
    if _gw_port:
        print(f"      3. 确认 IM 控制台回调 URL 为: http://<公网IP>:{_gw_port}/timbot")
        print(f"      4. 确认 Lighthouse 防火墙已开放端口 {_gw_port}")
    else:
        print(f"      3. 确认 IM 控制台回调 URL 为: http://<公网IP>:<gateway端口>/timbot")
        print(f"         (gateway 端口通过 netstat 或 openclaw config get gateway.port 获取)")


def _send_start_live_msg(cfg: dict):
    """通过 IM REST API v4/openim/sendmsg 静默给 @RBT#001 发送"启动直播"单聊消息。
    参考: https://cloud.tencent.com/document/product/269/2282
    """
    import urllib.request, urllib.parse
    sdkappid = cfg.get("sdkappid")
    secret = cfg.get("secret_key")
    im_bot_userid = cfg.get("im_bot_userid", IM_BOT_USERID)
    if not sdkappid or not secret:
        print(f"  [!] Cannot send start-live msg: sdkappid or secret_key missing")
        return

    try:
        from TLSSigAPIv2 import gen_usersig
        admin_sig = gen_usersig(sdkappid, secret, "administrator", 86400)

        url = (f"https://console.tim.qq.com/v4/openim/sendmsg"
               f"?sdkappid={sdkappid}&identifier=administrator"
               f"&usersig={urllib.parse.quote(admin_sig)}"
               f"&random={random.randint(10000000, 99999999)}&contenttype=json")

        body = json.dumps({
            "SyncOtherMachine": 1,
            "From_Account": "administrator",
            "To_Account": im_bot_userid,
            "MsgLifeTime": 60,
            "MsgRandom": random.randint(1, 999999999),
            "MsgBody": [{
                "MsgType": "TIMTextElem",
                "MsgContent": {"Text": "启动直播"}
            }]
        }).encode()

        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())

        code = data.get("ErrorCode", -1)
        if code == 0:
            print(f"[+] 启动直播消息已发送 → {im_bot_userid}")
            # 写标志文件，HTTP API 不再重复发送
            try:
                flag_file = WORK_DIR / ".start_live_sent"
                flag_file.write_text(str(int(time.time())))
            except Exception:
                pass
        else:
            print(f"  [!] 启动直播消息发送失败: {data.get('ErrorInfo', 'unknown')} (code={code})")
    except Exception as e:
        print(f"  [!] 启动直播消息发送异常: {e}")


def _script_path(name: str) -> str:
    """定位工作目录中的脚本路径（兼容 SKILL_DIR == WORK_DIR 时脚本在 scripts/ 子目录的情况）"""
    p = WORK_DIR / name
    if p.exists():
        return str(p)
    p2 = WORK_DIR / "scripts" / name
    if p2.exists():
        return str(p2)
    return str(p)  # 回退到默认路径（可能不存在，让调用者处理错误）


def cmd_start():
    if not CONFIG_F.exists():
        print("ERROR: No config found. Run with --sdkappid / --secret first.")
        sys.exit(1)

    cfg = json.loads(CONFIG_F.read_text())
    platform_tag = get_platform_tag()
    print(f"[*] Platform: {platform_tag}")
    print(f"[*] Mode: Pillow frame rendering (no Xvfb/tkinter/FFmpeg)")

    # 0-pre. 确保 assets 已部署到工作目录
    _ensure_assets_deployed(cfg)

    # 0-skill-install. 将主 SKILL 安装到全局 skills 目录（确保 timbot 等外部渠道能发现）
    _install_main_skill()

    # 0-skills. 自动安装预置 skill 到 OpenClaw skill 目录
    _install_bundled_skills(cfg)

    # 0-im. 预创建 AVChatRoom 群
    _ensure_avchatroom(cfg)

    # 0-im-channel. timbot IM 通道状态检测（双向交互的前置条件）
    _timbot_ok = False
    if cfg.get("callback_token"):
        # 检测 timbot 是否真正在 gateway 中激活
        try:
            result = subprocess.run(
                ["openclaw", "plugins", "list"],
                capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0 and "timbot" in result.stdout.lower():
                _timbot_ok = True
                print(f"  [✓] timbot IM channel: ACTIVE (callback_token configured, plugin installed)")
            else:
                print(f"  [!] timbot plugin not found in plugins list")
        except Exception:
            pass

        if not _timbot_ok:
            print(f"  [!] timbot may not be active — run: openclaw gateway restart")
    else:
        print(f"")
        print(f"  ╔══════════════════════════════════════════════════════════╗")
        print(f"  ║  ⚠️  双向交互未启用（缺少 --callback-token）           ║")
        print(f"  ║                                                          ║")
        print(f"  ║  观众在 Viewer 页面发送消息将无法触发 Agent 回复！      ║")
        print(f"  ║                                                          ║")
        print(f"  ║  启用方法：                                              ║")
        print(f"  ║  1. 在 IM 控制台配置回调 URL 和 Token                   ║")
        print(f"  ║  2. 重新执行初始化：                                     ║")
        print(f"  ║     python3 setup.py --sdkappid <ID> --secret <KEY> \\   ║")
        print(f"  ║       --callback-token <TOKEN>                          ║")
        print(f"  ║  3. openclaw gateway restart                            ║")
        print(f"  ╚══════════════════════════════════════════════════════════╝")
        print(f"")

    # 0-fonts. 确保 CJK + 符号字体已安装（Linux 自动 apt 安装，macOS/Win 使用系统字体）
    from platform_utils import ensure_fonts_installed
    ensure_fonts_installed(verbose=True)

    # v23: 不再需要 Xvfb、tkinter 预检、Dashboard 窗口
    # 画面由 stream_daemon 内置的 FrameRenderer (Pillow) 直接生成

    # 0-deps. 预检关键 Python 依赖（缺失时 stream_daemon 子进程会静默崩溃）
    _missing_deps = []
    for mod_name, pip_name in [("av", "av"), ("numpy", "numpy"), ("PIL", "Pillow")]:
        try:
            __import__(mod_name)
        except ImportError:
            _missing_deps.append(pip_name)
    if _missing_deps:
        print(f"  [!] Missing Python dependencies: {', '.join(_missing_deps)}")
        print(f"  [*] Auto-installing: pip install {' '.join(_missing_deps)}")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "--quiet"] + _missing_deps,
                capture_output=True, text=True, timeout=120
            )
            if result.returncode == 0:
                print(f"  [+] Dependencies installed: {', '.join(_missing_deps)}")
            else:
                print(f"  [!] pip install failed (exit {result.returncode}): {result.stderr.strip()[:200]}")
                print(f"      Manual fix: pip install {' '.join(_missing_deps)}")
                sys.exit(1)
        except (FileNotFoundError, subprocess.TimeoutExpired) as e:
            print(f"  [!] pip install failed: {e}")
            print(f"      Manual fix: pip install {' '.join(_missing_deps)}")
            sys.exit(1)

    env = {**os.environ}

    # 1. stream_daemon — 带推流就绪检测（内置 Pillow 帧渲染）
    sd_pids = find_process_by_script("stream_daemon.py")
    if not sd_pids:
        pid = start_daemon_process(
            _script_path("stream_daemon.py"),
            log_file=str(WORK_DIR / "daemon.log"),
            env=env
        )
        (WORK_DIR / "daemon.pid").write_text(str(pid))
        print(f"[+] stream_daemon started (PID {pid})")
        _stream_ready = False
        daemon_log = WORK_DIR / "daemon.log"
        for _i in range(40):  # 最多等 20 秒
            time.sleep(0.5)
            if daemon_log.exists():
                content = daemon_log.read_text(errors="ignore")
                if "Streaming started" in content:
                    _stream_ready = True
                    print(f"  [✓] Stream ready ({(_i+1)*0.5:.1f}s)")
                    break
                if "Stream error" in content:
                    print(f"  [!] stream_daemon reported error, check {daemon_log}")
                    break
        if not _stream_ready:
            print(f"  [!] Stream readiness not confirmed after 20s (may still be connecting...)")
    else:
        print(f"[=] stream_daemon already running (PID {sd_pids[0]})")

    # 2. supervisor
    sv_pids = find_process_by_script("supervisor.py")
    if not sv_pids:
        pid = start_daemon_process(
            _script_path("supervisor.py"),
            log_file=str(WORK_DIR / "supervisor.log"),
            env=env
        )
        print(f"[+] supervisor started (PID {pid})")
    else:
        print(f"[=] supervisor already running (PID {sv_pids[0]})")

    # 3. tts_worker（可选，仅在配置了 CAM 密钥时启动）
    cfg_data = json.loads(CONFIG_F.read_text()) if CONFIG_F.exists() else {}
    _has_cam = (cfg_data.get("cam_secret_id") or cfg_data.get("tts_secret_id")) and \
               (cfg_data.get("cam_secret_key") or cfg_data.get("tts_secret_key"))
    if _has_cam:
        tw_pids = find_process_by_script("tts_worker.py")
        if not tw_pids:
            pid = start_daemon_process(
                _script_path("tts_worker.py"),
                log_file=str(WORK_DIR / "tts_worker.log"),
                env=env
            )
            print(f"[+] tts_worker started (PID {pid})")
        else:
            print(f"[=] tts_worker already running (PID {tw_pids[0]})")
    else:
        print(f"[=] tts_worker skipped (no TTS credentials in config.json)")

    # 4. HTTP server（自动启动，确保观看页持续可访问）
    _http_port = VIEWER_HTTP_PORT
    _validate_viewer_port(_http_port)
    import socket as _socket
    _http_running = False
    try:
        _sock = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
        _sock.settimeout(0.5)
        _sock.connect(("127.0.0.1", _http_port))
        _sock.close()
        _http_running = True
    except (OSError, _socket.timeout):
        try:
            _sock.close()
        except Exception:
            pass

    if _http_running:
        print(f"[=] HTTP server already running on port {_http_port}")
    else:
        index_path = WORK_DIR / "index.html"
        if not index_path.exists():
            tmpl_path = WORK_DIR / "trtc-viewer-template.html"
            if not tmpl_path.exists():
                tmpl_path = ASSETS / "trtc-viewer-template.html"
            if tmpl_path.exists() and cfg.get("sdkappid") and cfg.get("viewer_usersig"):
                try:
                    tmpl = tmpl_path.read_text(encoding="utf-8")
                    html = (tmpl
                            .replace("__SDKAPPID__",      str(cfg["sdkappid"]))
                            .replace("__ROOM_ID__",       cfg["room_id"])
                            .replace("__VIEWER_USERID__", cfg["viewer_userid"])
                            .replace("__USERSIG__",       cfg["viewer_usersig"])
                            .replace("__IM_USERID__",     cfg.get("im_userid", ""))
                            .replace("__IM_USERSIG__",    cfg.get("im_usersig", ""))
                            .replace("__IM_BOT_USERID__", cfg.get("im_bot_userid", IM_BOT_USERID))
                            .replace("'__IM_SDKAPPID__'", str(cfg["sdkappid"])))
                    index_path.write_text(html, encoding="utf-8")
                    viewer_out = WORK_DIR / "trtc-viewer.html"
                    if not viewer_out.exists():
                        shutil.copy2(index_path, viewer_out)
                    print(f"  [+] Viewer page auto-generated: {index_path}")
                except Exception as e:
                    print(f"  [!] Failed to auto-generate viewer page: {e}")

        ok = _start_http_server_process(str(WORK_DIR), _http_port)
        if ok:
            print(f"[+] HTTP server started on 0.0.0.0:{_http_port}")
        else:
            print(f"  [!] HTTP server failed to start on port {_http_port}")

    print(f"\n[LIVE] OpenClaw Agent Live is running! ({platform_tag})")
    print(f"  RTMP → {cfg['rtmp_url'][:60]}...")
    print(f"  Room: {cfg['room_id']}")
    print(f"  Mode: Pillow (no Xvfb/tkinter/FFmpeg — 3 processes)")
    print(f"  Run `python3 {__file__} --viewer` to generate viewer page.")

    # 5. 通过 IM REST API 静默发送"启动直播"给 @RBT#001
    _send_start_live_msg(cfg)

    # ── [LIVE MODE ACTIVE] 直播规范提示 ──────────────────────
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  [LIVE MODE ACTIVE] 直播上报规范（当前 session 生效）       ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  直播期间所有回复必须先 emit agent_bus 事件再回复用户：      ║
║                                                              ║
║  路径 A（工具调用）：                                        ║
║    task → think → <kind>(操作) → [工具调用] → result         ║
║                                                              ║
║  路径 B（纯文本回复：故事/笑话/诗歌/聊天/问答等）：         ║
║    task → think → info(正文，可多段) → result                ║
║                                                              ║
║  ⚠️  info 是 Dashboard 和 TTS 显示/播报内容的唯一途径！     ║
║      不上报 info → Dashboard 空白 → TTS 不播报 → 观众无感知 ║
║                                                              ║
║  v10: 双向交互通过 timbot IM 单聊消息触发 Agent turn         ║
║       观众 IM 消息 → @RBT#001 → Agent 执行 → agent_bus 上报 ║
║                                                              ║
║  长文本分段：每段 ≤200 字，多次调用 agent_bus.py info 输出   ║
║  每条消息必须完整走完：task → ... → result/error             ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝""")



# ── 停止 ────────────────────────────────────────────────────
def cmd_stop():
    # 所有守护进程忽略 SIGTERM（抗容器定期清理），--stop 直接 SIGKILL
    procs = ["supervisor.py", "stream_daemon.py", "tts_worker.py"]
    for name in procs:
        pids = find_process_by_script(name)
        for pid in pids:
            kill_process(pid, force=True)
            print(f"  [x] killed {name} (PID {pid})")

    # 终止 HTTP server 子进程（HTTP server 仍响应 SIGTERM）
    http_pid_file = WORK_DIR / "http_server.pid"
    if http_pid_file.exists():
        try:
            http_pid = int(http_pid_file.read_text().strip())
            kill_process(http_pid, force=False)
            time.sleep(1)
            kill_process(http_pid, force=True)
            print(f"  [x] killed http_server (PID {http_pid})")
        except (ValueError, OSError):
            pass
        http_pid_file.unlink(missing_ok=True)

    # 确认清理
    time.sleep(1)
    for name in procs:
        pids = find_process_by_script(name)
        for pid in pids:
            kill_process(pid, force=True)

    print("[STOPPED] All processes stopped.")


# ── 生成 Viewer 页面 ─────────────────────────────────────────

def _validate_viewer_port(port: int) -> None:
    """校验端口号：不能使用 OpenClaw 容器保留端口"""
    if port in RESERVED_PORTS:
        sorted_ports = sorted(RESERVED_PORTS)
        print(f"  [!] 端口 {port} 是 OpenClaw 容器保留端口，禁止使用！")
        print(f"      保留端口列表: {sorted_ports}")
        sys.exit(1)


def _build_lighthouse_url(ip: str, port: int) -> str:
    """构建 Lighthouse 访问地址。

    示例:
      ip = "live.example.com"  → "http://live.example.com"
      ip = "43.136.xxx.xxx"    → "http://43.136.xxx.xxx:19000"
    """
    # 判断是域名还是纯 IP
    parts = ip.replace(":", "").split(".")
    is_domain = any(not p.isdigit() for p in parts)
    if is_domain:
        return f"http://{ip}"
    return f"http://{ip}:{port}"


def _start_http_server_process(directory: str, port: int = VIEWER_HTTP_PORT):
    """以独立守护子进程方式启动 HTTP 服务器（监听 0.0.0.0）。
    v10: 纯静态文件服务（双向交互由前端 IM SDK 直接发单聊消息）。
    """
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(("0.0.0.0", port))
        sock.close()
    except OSError:
        print(f"  [=] Port {port} already in use — HTTP server likely already running")
        return True

    server_script = r'''
import os, json, sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

SERVE_DIR = {directory!r}
PORT = {port}

# Load config for usersig generation
_cfg_path = os.path.join(SERVE_DIR, "config.json")
_cfg = {{}}
if os.path.exists(_cfg_path):
    with open(_cfg_path) as f:
        _cfg = json.load(f)

# Import TLSSigAPIv2 for dynamic usersig generation
sys.path.insert(0, SERVE_DIR)
try:
    from TLSSigAPIv2 import gen_usersig as _gen_usersig
except ImportError:
    _gen_usersig = None

# Import stream_ingest_client for task status verification
try:
    from stream_ingest_client import describe_stream_ingest as _describe_ingest
except ImportError:
    _describe_ingest = None

# Song state verification: throttle DescribeStreamIngest calls (max once per 5s)
import time as _time
_last_ingest_check = 0
_INGEST_CHECK_INTERVAL = 5  # seconds

class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SERVE_DIR, **kwargs)
    def log_message(self, fmt, *a):
        pass
    def do_GET(self):
        if self.path.startswith("/api/gen-usersig"):
            self._handle_gen_usersig()
        elif self.path.startswith("/api/agent-state"):
            self._handle_agent_state()
        elif self.path.startswith("/api/song-state"):
            self._handle_song_state()
        elif self.path.startswith("/api/stream-log"):
            self._handle_stream_log()
        elif self.path.startswith("/api/online-members"):
            self._handle_online_members()
        elif self.path.startswith("/api/send-start-live"):
            self._handle_send_start_live()
        else:
            super().do_GET()

    def do_POST(self):
        if self.path.startswith("/api/emit-task"):
            self._handle_emit_task()
        else:
            self.send_error(404)

    def do_OPTIONS(self):
        """CORS preflight for POST requests"""
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _handle_emit_task(self):
        """Viewer 发消息时预上报 task 事件，Dashboard 瞬间响应"""
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length)) if length > 0 else {{}}
            text = body.get("text", "").strip()
            kind = body.get("kind", "task")
            if not text:
                self._json_response({{"error": "text is required"}}, 400)
                return
            # 允许的 kind 白名单（防止滥用）
            if kind not in ("task", "info"):
                kind = "task"
            # 直接写入 agent_events.jsonl
            import datetime as _dt
            _icon_map = {{"task": "[TASK]", "info": "[INFO]"}}
            event = {{
                "ts": _dt.datetime.now().isoformat(),
                "kind": kind,
                "icon": _icon_map.get(kind, "[TASK]"),
                "text": text,
                "detail": "",
            }}
            bus_file = os.path.join(SERVE_DIR, "agent_events.jsonl")
            with open(bus_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(event, ensure_ascii=False) + "\n")
            # 同时更新 agent_state.json
            state_file = os.path.join(SERVE_DIR, "agent_state.json")
            with open(state_file, "w") as f:
                json.dump({{"current": event, "state": kind, "updated_at": event["ts"]}},
                          f, ensure_ascii=False, indent=2)
            self._json_response({{"ok": True}})
        except Exception as e:
            self._json_response({{"error": str(e)}}, 500)

    def _json_response(self, data, code=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _handle_stream_log(self):
        log_file = os.path.join(SERVE_DIR, "stream_log.json")
        logs = []
        try:
            if os.path.exists(log_file):
                with open(log_file) as f:
                    logs = json.load(f)
        except Exception:
            pass
        body = json.dumps(logs).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def _handle_song_state(self):
        global _last_ingest_check
        song_file = os.path.join(SERVE_DIR, "current_song.json")
        song_state = {{"playing": False, "song_name": "", "artist_name": "", "cover_url": ""}}
        try:
            if os.path.exists(song_file):
                with open(song_file) as f:
                    song_state = json.load(f)
        except Exception:
            pass

        # 如果本地状态显示 playing=true，定期校验 TRTC 推流任务真实状态
        if song_state.get("playing") and _describe_ingest:
            now = _time.time()
            if now - _last_ingest_check >= _INGEST_CHECK_INTERVAL:
                _last_ingest_check = now
                try:
                    result = _describe_ingest()
                    status = result.get("Status", "NotExist")
                    if status != "InProgress":
                        # 任务已结束，重置本地歌曲状态
                        song_state = {{"playing": False, "song_name": "", "artist_name": "", "cover_url": ""}}
                        with open(song_file, "w") as f:
                            json.dump(song_state, f, ensure_ascii=False)
                except Exception:
                    pass

        body = json.dumps(song_state).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def _handle_agent_state(self):
        state_file = os.path.join(SERVE_DIR, "agent_state.json")
        audio_queue_dir = os.path.join(SERVE_DIR, "audio_queue")
        tts_flag_file = os.path.join(SERVE_DIR, "tts_playing.flag")
        state = {{"state": "idle", "tts_playing": False}}
        try:
            if os.path.exists(state_file):
                with open(state_file) as f:
                    state = json.load(f)
            # Check if TTS is playing (with 2s decay to prevent avatar flicker):
            # 1. tts_playing.flag 存储时间戳，2 秒内视为仍在播放
            # 2. audio_queue 有待播文件 = TTS Worker 已合成但尚未被 AudioMixer 消费
            _TTS_DECAY_SEC = 2.0
            tts_playing = False
            if os.path.exists(tts_flag_file):
                try:
                    last_ts = float(open(tts_flag_file).read().strip())
                    if _time.time() - last_ts < _TTS_DECAY_SEC:
                        tts_playing = True
                except (ValueError, OSError):
                    tts_playing = True  # 无法解析时保守视为 playing
            if not tts_playing and os.path.isdir(audio_queue_dir):
                for entry in os.scandir(audio_queue_dir):
                    if entry.is_file() and entry.name.endswith('.npy'):
                        tts_playing = True
                        break
            state["tts_playing"] = tts_playing
        except Exception:
            pass
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(json.dumps(state).encode())
    def _handle_send_start_live(self):
        # 标志文件：整个直播 session 只发一次，后续观众不再触发
        flag_file = os.path.join(SERVE_DIR, ".start_live_sent")
        if os.path.exists(flag_file):
            self._json_resp(200, {{"ok": True, "msg": "already_sent", "skipped": True}})
            return
        import urllib.request, urllib.parse, random as _rnd
        sdkappid = _cfg.get("sdkappid", 0)
        secret = _cfg.get("secret_key", "")
        im_bot_userid = _cfg.get("im_bot_userid", "@RBT#001")
        if not sdkappid or not secret or not _gen_usersig:
            self._json_resp(400, {{"error": "not configured"}})
            return
        try:
            admin_sig = _gen_usersig(sdkappid, secret, "administrator", 86400)
            url = ("https://console.tim.qq.com/v4/openim/sendmsg"
                   "?sdkappid={{}}&identifier=administrator&usersig={{}}&random={{}}&contenttype=json").format(
                   sdkappid, urllib.parse.quote(admin_sig), _rnd.randint(10000000, 99999999))
            body = json.dumps({{
                "SyncOtherMachine": 1,
                "From_Account": "administrator",
                "To_Account": im_bot_userid,
                "MsgLifeTime": 60,
                "MsgRandom": _rnd.randint(1, 999999999),
                "MsgBody": [{{
                    "MsgType": "TIMTextElem",
                    "MsgContent": {{"Text": "启动直播"}}
                }}]
            }}).encode()
            req = urllib.request.Request(url, data=body, headers={{"Content-Type": "application/json"}})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
            code = data.get("ErrorCode", -1)
            if code == 0:
                # 写入标志文件，后续请求不再发送
                try:
                    with open(flag_file, "w") as f:
                        f.write(str(int(_time.time())))
                except Exception:
                    pass
                self._json_resp(200, {{"ok": True, "msg": "启动直播消息已发送"}})
            else:
                self._json_resp(200, {{"ok": False, "error": data.get("ErrorInfo", "unknown"), "code": code}})
        except Exception as e:
            self._json_resp(500, {{"ok": False, "error": str(e)}})
    def _handle_online_members(self):
        import urllib.request, urllib.parse, random as _rnd
        sdkappid = _cfg.get("sdkappid", 0)
        secret = _cfg.get("secret_key", "")
        room_id = _cfg.get("room_id", "")
        if not sdkappid or not secret or not room_id:
            self._json_resp(400, {{"error": "not configured"}})
            return
        try:
            admin_sig = _gen_usersig(sdkappid, secret, "administrator", 86400) if _gen_usersig else ""
            url = ("https://console.tim.qq.com/v4/group_open_avchatroom_http_svc/get_members"
                   "?sdkappid={{}}&identifier=administrator&usersig={{}}&random={{}}&contenttype=json").format(
                   sdkappid, urllib.parse.quote(admin_sig), _rnd.randint(10000000, 99999999))
            body = json.dumps({{"GroupId": room_id, "Timestamp": 0}}).encode()
            req = urllib.request.Request(url, data=body, headers={{"Content-Type": "application/json"}})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode())
            members = data.get("MemberList", [])
            self._json_resp(200, {{"count": len(members), "members": members}})
        except Exception as e:
            self._json_resp(200, {{"count": 0, "members": [], "error": str(e)}})
    def _json_resp(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    def _handle_gen_usersig(self):
        from urllib.parse import urlparse, parse_qs
        qs = parse_qs(urlparse(self.path).query)
        userid = qs.get("userid", [""])[0]
        if not userid or not _gen_usersig or not _cfg.get("secret_key"):
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({{"error": "missing userid or server not configured"}}).encode())
            return
        sdkappid = _cfg.get("sdkappid", 0)
        secret = _cfg["secret_key"]
        usersig = _gen_usersig(sdkappid, secret, userid, 604800)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        resp = {{"userid": userid, "usersig": usersig, "sdkappid": sdkappid, "room_id": _cfg.get("room_id",""), "im_bot_userid": _cfg.get("im_bot_userid","@RBT#001")}}
        self.wfile.write(json.dumps(resp).encode())

os.chdir(SERVE_DIR)
httpd = HTTPServer(("0.0.0.0", PORT), Handler)
print(f"HTTP server PID: {{os.getpid()}}")
httpd.serve_forever()
'''.format(directory=directory, port=port)

    env = {**os.environ}
    cmd = [get_python_cmd(), "-c", server_script]
    proc = subprocess.Popen(
        cmd,
        stdout=open(str(WORK_DIR / "http_server.log"), "w"),
        stderr=subprocess.STDOUT,
        **new_session_kwargs()
    )
    (WORK_DIR / "http_server.pid").write_text(str(proc.pid))
    for _ in range(20):
        time.sleep(0.25)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(("127.0.0.1", port))
            s.close()
            return True
        except OSError:
            s.close()
    print(f"  [!] HTTP server process started but port {port} not ready")
    return False


def cmd_viewer(output_path: str = None,
               lighthouse_ip: str = None, **_kwargs):
    """生成观看页 + 启动 HTTP server（始终非阻塞，立即返回控制权）"""
    if not CONFIG_F.exists():
        print("ERROR: No config found. Run with --sdkappid / --secret first.")
        sys.exit(1)

    cfg = json.loads(CONFIG_F.read_text())

    # 优先从工作目录读取模板（deploy_scripts 已复制），否则从 Skill 原始目录
    tmpl_path = WORK_DIR / "trtc-viewer-template.html"
    if not tmpl_path.exists():
        tmpl_path = ASSETS / "trtc-viewer-template.html"
    tmpl = tmpl_path.read_text(encoding="utf-8")

    html = (tmpl
            .replace("__SDKAPPID__",      str(cfg["sdkappid"]))
            .replace("__ROOM_ID__",       cfg["room_id"])
            .replace("__VIEWER_USERID__", cfg["viewer_userid"])
            .replace("__USERSIG__",       cfg["viewer_usersig"])
            .replace("__IM_USERID__",     cfg.get("im_userid", ""))
            .replace("__IM_USERSIG__",    cfg.get("im_usersig", ""))
            .replace("__IM_BOT_USERID__", cfg.get("im_bot_userid", IM_BOT_USERID))
            .replace("'__IM_SDKAPPID__'", str(cfg["sdkappid"])))

    out = Path(output_path) if output_path else (WORK_DIR / "trtc-viewer.html")
    index_path = WORK_DIR / "index.html"
    out.write_text(html, encoding="utf-8")
    if out != index_path:
        shutil.copy2(out, index_path)
    print(f"[+] Viewer page generated: {out}")

    # 校验端口
    _validate_viewer_port(VIEWER_HTTP_PORT)

    # 启动内置 HTTP server（始终以独立进程方式，避免阻塞 Agent 命令执行器导致超时杀进程）
    print(f"[*] Starting HTTP server on http://0.0.0.0:{VIEWER_HTTP_PORT} ...")
    ok = _start_http_server_process(str(WORK_DIR), VIEWER_HTTP_PORT)
    if ok:
        print(f"[+] HTTP server started on 0.0.0.0:{VIEWER_HTTP_PORT}")

    # ── 公网访问地址 ─────────────────────────────────────────────
    lip = lighthouse_ip or cfg.get("lighthouse_ip")
    viewer_url = None
    if lip:
        viewer_url = _build_lighthouse_url(lip, VIEWER_HTTP_PORT)
        cfg["lighthouse_ip"] = lip
        cfg["viewer_url"] = viewer_url

    # IM 双向交互状态
    im_enabled = bool(cfg.get("im_userid") and cfg.get("im_usersig"))

    # 输出结果
    print(f"\n{'='*60}")
    print(f"  ✅ 观看页面已就绪！")
    if viewer_url:
        print(f"  📺 公网地址: {viewer_url}")
    print(f"  🏠 本地访问地址: http://127.0.0.1:{VIEWER_HTTP_PORT}")
    print(f"  📋 房间号: {cfg['room_id']}")
    if im_enabled:
        print(f"  💬 双向交互: 已启用（timbot IM 单聊触发 Agent）")
        print(f"      IM UserID: {cfg.get('im_userid')}")
        print(f"      IM Bot: {cfg.get('im_bot_userid', IM_BOT_USERID)}")
    else:
        print(f"  💬 双向交互: 未启用（IM UserSig 未生成）")
    print(f"{'='*60}")

    if not viewer_url:
        print(f"\n  💡 如需公网访问，请提供 Lighthouse 公网 IP:")
        print(f"     python3 {__file__} --viewer --lighthouse-ip <YOUR_IP>")

    CONFIG_F.write_text(json.dumps(cfg, indent=2, ensure_ascii=False))


# ── 状态 ────────────────────────────────────────────────────
def cmd_status():
    platform_tag = get_platform_tag()
    print(f"=== OpenClaw Agent Live Status ({platform_tag}, Pillow mode) ===")

    procs = {
        "stream_daemon": "stream_daemon.py",
        "supervisor":    "supervisor.py",
        "tts_worker":    "tts_worker.py",
    }

    for name, script in procs.items():
        pids = find_process_by_script(script)
        status = f"RUNNING (PID {', '.join(map(str, pids))})" if pids else "STOPPED"
        print(f"  {name:20s} {status}")

    if CONFIG_F.exists():
        cfg = json.loads(CONFIG_F.read_text())
        print(f"\n  Room:     {cfg.get('room_id')}")
        print(f"  AppID:    {cfg.get('sdkappid')}")
        expires = cfg.get("usersig_expires", "unknown")
        print(f"  UserSig:  valid until {expires}")

        # 显示公网访问信息
        lip = cfg.get("lighthouse_ip")
        if lip:
            lh_url = _build_lighthouse_url(lip, VIEWER_HTTP_PORT)
            print(f"  Viewer:   {lh_url} (公网)")
        else:
            print(f"  Viewer:   http://127.0.0.1:{VIEWER_HTTP_PORT} (未配置公网访问)")

        # 显示 IM 双向交互状态
        if cfg.get("im_userid") and cfg.get("im_usersig"):
            print(f"  IM Chat:  enabled (im_userid: {cfg.get('im_userid')}, bot: {cfg.get('im_bot_userid', IM_BOT_USERID)})")
        else:
            print(f"  IM Chat:  disabled (IM UserSig not generated)")


# ── CLI ─────────────────────────────────────────────────────
def main():
    p = argparse.ArgumentParser(
        description="OpenClaw Agent Live v10 — 一键配置 & 启停",
        epilog=(
            "获取 SDKAppID / SecretKey:\n"
            "  访问 TRTC 控制台: https://console.cloud.tencent.com/trtc/app\n"
            "  创建或选择一个应用 → 复制 SDKAppID 和 SecretKey"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--sdkappid",  type=int,   help="TRTC SDKAppID（从控制台获取）")
    p.add_argument("--secret",    type=str,   help="TRTC SecretKey（从控制台获取）")
    p.add_argument("--room",      type=str,   default=None,
                   help="房间号（可选，默认自动生成 openclaw-live-XXXXXX）")
    p.add_argument("--userid",    type=str,   default=None,
                   help="推流用户ID（可选，默认自动生成 streamer-XXXX）")
    p.add_argument("--cam-secret-id",  type=str, default=None,
                   help="腾讯云 CAM SecretId（可选，启用 TTS / 音乐推流等云 API 功能）")
    p.add_argument("--cam-secret-key", type=str, default=None,
                   help="腾讯云 CAM SecretKey（可选，启用 TTS / 音乐推流等云 API 功能）")
    p.add_argument("--callback-token", type=str, default=None,
                   help="IM 消息回调鉴权 Token（可选，启用 timbot 双向交互，必须与 IM 控制台回调配置一致）")
    # 兼容旧参数名
    p.add_argument("--tts-secret-id",  type=str, default=None, help=argparse.SUPPRESS)
    p.add_argument("--tts-secret-key", type=str, default=None, help=argparse.SUPPRESS)
    p.add_argument("--start",     action="store_true")
    p.add_argument("--stop",      action="store_true")
    p.add_argument("--viewer",    action="store_true")
    p.add_argument("--status",    action="store_true")
    p.add_argument("--out",       type=str,   help="Viewer output path")
    p.add_argument("--lighthouse-ip", type=str, default=None,
                   help="Lighthouse 公网 IP 地址（如: 43.136.xxx.xxx）")
    args = p.parse_args()

    if args.sdkappid and args.secret:
        # 自动生成 room / userid
        room_id = args.room or auto_room_id()
        streamer_id = args.userid or auto_userid()
        viewer_id = auto_viewer_userid()
        im_userid = auto_im_userid()

        print(f"[*] TRTC SDKAppID:  {args.sdkappid}")
        print(f"[*] Room ID:        {room_id}")
        print(f"[*] Streamer UID:   {streamer_id}")
        print(f"[*] Viewer UID:     {viewer_id}")
        print(f"[*] IM UserID:      {im_userid}")
        print(f"[*] Generating UserSig (official TLSSigAPIv2 algorithm)...")

        usersig = gen_usersig(args.sdkappid, args.secret, streamer_id)
        viewer_usersig = gen_usersig(args.sdkappid, args.secret, viewer_id)
        # IM UserSig 复用同一 SDKAppID + SecretKey（TRTC 和 IM 共享鉴权体系）
        im_usersig = gen_usersig(args.sdkappid, args.secret, im_userid)
        rtmp_url = build_rtmp_url(args.sdkappid, room_id, streamer_id, usersig)
        expires = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
        cfg = {
            "sdkappid":        args.sdkappid,
            "room_id":         room_id,
            "streamer_userid": streamer_id,
            "viewer_userid":   viewer_id,
            "usersig":         usersig,
            "viewer_usersig":  viewer_usersig,
            "usersig_expires": f"(7 days from {expires})",
            "rtmp_url":        rtmp_url,
            # IM 双向交互（timbot 渠道）
            "im_userid":       im_userid,
            "im_usersig":      im_usersig,
            "im_bot_userid":   IM_BOT_USERID,
            "secret_key":      args.secret,
        }
        # 腾讯云 CAM 密钥（项目级，TTS / 音乐推流 / REST API 共用）
        cam_id = getattr(args, 'cam_secret_id', None) or getattr(args, 'tts_secret_id', None)
        cam_key = getattr(args, 'cam_secret_key', None) or getattr(args, 'tts_secret_key', None)
        if cam_id and cam_key:
            cfg["cam_secret_id"] = cam_id
            cfg["cam_secret_key"] = cam_key
            # 兼容旧字段名（tts_worker / tts_client 仍读 tts_secret_id/tts_secret_key）
            cfg["tts_secret_id"] = cam_id
            cfg["tts_secret_key"] = cam_key
            print(f"[*] CAM API Key:    enabled (SecretId: {cam_id[:8]}...)")
            print(f"                    (TTS + Music StreamIngest + REST API)")
        else:
            print(f"[*] CAM API Key:    disabled (add --cam-secret-id/--cam-secret-key to enable)")
            print(f"                    (TTS / 音乐推流等云 API 功能需要 CAM 密钥)")

        # IM 回调 Token（timbot 双向交互激活所需）
        callback_token = getattr(args, 'callback_token', None)
        if callback_token:
            cfg["callback_token"] = callback_token
            print(f"[*] IM Callback:    enabled (token: {callback_token[:8]}...)")
            print(f"                    (--start 时将自动激活 timbot 通道)")
        else:
            print(f"[*] IM Callback:    not set (add --callback-token <TOKEN> to auto-activate timbot)")
            print(f"                    (Token 必须与 IM 控制台回调 URL 中配置的一致)")

        print(f"[*] IM Interactive: enabled (timbot C2C → {IM_BOT_USERID})")

        print("[*] Deploying scripts...")
        deploy_scripts(cfg)

        # IM 通道激活（安装 timbot + 写入配置，不自动重启 gateway）
        if cfg.get("callback_token"):
            print("\n[*] Checking IM channel (timbot)...")
            _ensure_im_channel(cfg)

        print(f"\n[OK] Config ready!")
        print(f"  Next steps:")
        print(f"    1. python3 {__file__} --start     # 启动直播系统")
        print(f"    2. python3 {__file__} --viewer --lighthouse-ip <IP>  # 生成观看页")
        return

    if args.start:
        cmd_start(); return
    if args.stop:
        cmd_stop(); return
    if args.viewer:
        # 如果传了 --secret，写入 config 以启用多人动态签名
        if args.secret and CONFIG_F.exists():
            cfg = json.loads(CONFIG_F.read_text())
            if 'secret_key' not in cfg or cfg['secret_key'] != args.secret:
                cfg['secret_key'] = args.secret
                CONFIG_F.write_text(json.dumps(cfg, indent=2, ensure_ascii=False))
                print(f"[+] secret_key saved to config — multi-viewer mode enabled")
        cmd_viewer(args.out,
                   lighthouse_ip=getattr(args, 'lighthouse_ip', None)); return
    if args.status:
        cmd_status(); return

    p.print_help()


if __name__ == "__main__":
    main()
