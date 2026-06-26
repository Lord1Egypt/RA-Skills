"""
MeetingOS - 会议录制下载器
功能：从企业微信/飞书/腾讯会议下载录制文件到本地
"""

import os
import re
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# 从环境变量读取配置（只读取，不联网）
WECOM_CORP_ID      = os.getenv("WECOM_CORP_ID", "")
WECOM_AGENT_SECRET = os.getenv("WECOM_AGENT_SECRET", "")
FEISHU_APP_ID      = os.getenv("FEISHU_APP_ID", "")
FEISHU_APP_SECRET  = os.getenv("FEISHU_APP_SECRET", "")

# 下载文件保存目录
DOWNLOAD_DIR = os.getenv("MEETINGOS_DOWNLOAD_DIR", "/tmp/meetingos_recordings")
MAX_FILE_MB  = int(os.getenv("MEETINGOS_MAX_FILE_MB", "2048"))

# 确保下载目录存在（只是创建文件夹，不联网）
Path(DOWNLOAD_DIR).mkdir(parents=True, exist_ok=True)

# 各平台令牌缓存
_wecom_token  = {"token": None, "expires_at": 0.0}
_feishu_token = {"token": None, "expires_at": 0.0}


def _safe_filename(name, max_len=80):
    """把任意文字转成安全的文件名（去掉特殊字符）"""
    return re.sub(r'[\\/:*?"<>|\s]', "_", name)[:max_len]


def _download_file(url, save_path, headers=None):
    """
    下载文件到本地（支持大文件，有进度提示）

    参数：
        url       - 文件下载地址
        save_path - 本地保存路径
        headers   - 可选的请求头（用于需要登录的下载链接）

    返回：保存成功的本地文件路径
    """
    print(f"📥 开始下载：{url[:60]}...")

    response = requests.get(
        url,
        headers=headers or {},
        stream=True,   # 流式下载，支持大文件
        timeout=120,
    )
    response.raise_for_status()

    # 写入文件
    downloaded_bytes = 0
    with open(save_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded_bytes += len(chunk)

    size_mb = downloaded_bytes / 1024 / 1024
    print(f"✅ 下载完成：{save_path}（{size_mb:.1f} MB）")
    return save_path


def _get_wecom_token():
    """获取企业微信令牌"""
    now = time.time()
    if _wecom_token["token"] and now < _wecom_token["expires_at"] - 60:
        return _wecom_token["token"]

    if not WECOM_CORP_ID or not WECOM_AGENT_SECRET:
        raise ValueError("❌ 缺少 WECOM_CORP_ID 或 WECOM_AGENT_SECRET")

    r = requests.get(
        "https://qyapi.weixin.qq.com/cgi-bin/gettoken",
        params={"corpid": WECOM_CORP_ID, "corpsecret": WECOM_AGENT_SECRET},
        timeout=10,
    )
    r.raise_for_status()
    d = r.json()
    _wecom_token["token"]      = d["access_token"]
    _wecom_token["expires_at"] = now + d.get("expires_in", 7200)
    return _wecom_token["token"]


def _get_feishu_token():
    """获取飞书令牌"""
    now = time.time()
    if _feishu_token["token"] and now < _feishu_token["expires_at"] - 60:
        return _feishu_token["token"]

    if not FEISHU_APP_ID or not FEISHU_APP_SECRET:
        raise ValueError("❌ 缺少 FEISHU_APP_ID 或 FEISHU_APP_SECRET")

    r = requests.post(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        json={"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET},
        timeout=10,
    )
    r.raise_for_status()
    d = r.json()
    _feishu_token["token"]      = d["tenant_access_token"]
    _feishu_token["expires_at"] = now + d.get("expire", 7200)
    return _feishu_token["token"]


def download_from_url(url, filename_hint=""):
    """
    通用 URL 下载（支持任意直链）

    参数：
        url           - 文件下载地址
        filename_hint - 文件名提示（不含扩展名）

    示例：
        download_from_url("https://example.com/recording.mp4", "产品周会")
    """
    from urllib.parse import urlparse

    parsed   = urlparse(url)
    url_name = Path(parsed.path).name
    ext      = Path(url_name).suffix or ".mp4"

    if filename_hint:
        filename = _safe_filename(filename_hint) + ext
    elif url_name and "." in url_name:
        filename = _safe_filename(url_name)
    else:
        filename = f"recording_{int(time.time())}{ext}"

    save_path = os.path.join(DOWNLOAD_DIR, filename)
    return _download_file(url, save_path)


def get_wecom_recordings(days=7):
    """
    获取企业微信最近 N 天的会议录制列表

    参数：
        days - 查询最近几天（默认 7 天）

    返回：录制文件信息列表
    """
    start_ts = int(time.time()) - days * 86400
    end_ts   = int(time.time())
    token    = _get_wecom_token()

    r = requests.post(
        "https://qyapi.weixin.qq.com/cgi-bin/meeting/record/list",
        params={"access_token": token},
        json={"start_time": start_ts, "end_time": end_ts, "size": 20, "cursor": ""},
        timeout=15,
    )
    r.raise_for_status()
    d = r.json()

    if d.get("errcode", 0) != 0:
        raise RuntimeError(f"❌ 获取企业微信录制列表失败：{d.get('errmsg')}")

    recordings = d.get("record_meeting_list", [])
    print(f"✅ 发现 {len(recordings)} 场企业微信会议录制")
    return recordings


def download_wecom_recording(record_file, topic="企业微信会议"):
    """
    下载单个企业微信录制文件

    参数：
        record_file - 录制文件信息字典（来自 get_wecom_recordings）
        topic       - 会议主题（用于文件命名）
    """
    url   = record_file.get("download_url", "")
    token = _get_wecom_token()

    if not url:
        raise ValueError("❌ 录制文件缺少下载地址")

    # 企业微信需要在下载链接里加入 access_token
    sep = "&" if "?" in url else "?"
    url = f"{url}{sep}access_token={token}"

    ts        = record_file.get("record_start_time", int(time.time()))
    time_str  = time.strftime("%Y%m%d_%H%M", time.localtime(ts))
    filename  = _safe_filename(f"wecom_{topic}_{time_str}") + ".mp4"
    save_path = os.path.join(DOWNLOAD_DIR, filename)

    return _download_file(url, save_path)


def get_feishu_recording(meeting_id):
    """
    获取飞书指定会议的录制信息

    参数：
        meeting_id - 飞书会议 ID（9 位数字）

    返回：录制信息字典（含下载地址）
    """
    token = _get_feishu_token()
    r = requests.get(
        f"https://open.feishu.cn/open-apis/vc/v1/meetings/{meeting_id}/recording",
        headers={"Authorization": f"Bearer {token}"},
        timeout=15,
    )
    r.raise_for_status()
    d = r.json()

    if d.get("code") != 0:
        raise RuntimeError(f"❌ 获取飞书录制信息失败：{d.get('msg')}")

    return d.get("data", {}).get("recording", {})


def download_feishu_recording(recording, topic_hint="飞书会议"):
    """
    下载飞书会议录制文件

    参数：
        recording   - 录制信息字典（来自 get_feishu_recording）
        topic_hint  - 会议主题备用名称
    """
    token  = _get_feishu_token()
    topic  = recording.get("topic") or topic_hint
    ts     = recording.get("record_start_time", int(time.time()))
    url    = recording.get("url", "")

    if not url:
        raise ValueError("❌ 飞书录制缺少下载链接")

    time_str  = time.strftime("%Y%m%d_%H%M", time.localtime(ts))
    filename  = _safe_filename(f"feishu_{topic}_{time_str}") + ".mp4"
    save_path = os.path.join(DOWNLOAD_DIR, filename)

    return _download_file(
        url, save_path,
        headers={"Authorization": f"Bearer {token}"}
    )


def fetch_recording(source, **kwargs):
    """
    智能录制获取入口：自动识别来源并下载

    参数（source 的值）：
        "wecom"               → 获取最近 N 天企业微信录制
        "feishu:{会议ID}"     → 获取飞书特定会议录制
        "/本地/文件路径.mp4"  → 直接使用本地文件
        "https://..."         → 通用 URL 下载

    其他参数：
        days  = 7   企业微信查询天数
        hint  = ""  URL 下载时的文件名提示

    返回：本地文件路径列表

    示例：
        files = fetch_recording("wecom", days=3)
        files = fetch_recording("feishu:123456789")
        files = fetch_recording("https://example.com/rec.mp4")
        files = fetch_recording("/Users/me/Downloads/meeting.mp4")
    """
    src = str(source).strip()

    # 本地文件：直接返回
    if os.path.exists(src):
        print(f"📂 使用本地文件：{src}")
        return [src]

    # HTTP(S) 链接：通用下载
    if src.startswith(("http://", "https://")):
        path = download_from_url(src, filename_hint=kwargs.get("hint", ""))
        return [path]

    # 企业微信
    if src.lower() == "wecom":
        meetings = get_wecom_recordings(days=kwargs.get("days", 7))
        paths = []
        for meeting in meetings:
            topic = meeting.get("subject", "企业微信会议")
            for rf in meeting.get("record_files", []):
                try:
                    p = download_wecom_recording(rf, topic)
                    paths.append(p)
                except Exception as e:
                    print(f"⚠️ 下载失败：{e}")
        return paths

    # 飞书（带会议 ID）
    if src.lower().startswith("feishu:"):
        meeting_id = src.split(":", 1)[1]
        recording  = get_feishu_recording(meeting_id)
        path       = download_feishu_recording(recording)
        return [path]

    raise ValueError(
        f"❌ 无法识别来源：{src}\n"
        f"支持格式：wecom / feishu:会议ID / 本地路径 / https://链接"
    )


def cleanup_files(file_paths):
    """
    删除临时录制文件（隐私保护，处理完必须调用！）

    参数：
        file_paths - 要删除的文件路径列表

    示例：
        files = fetch_recording("wecom")
        try:
            # 处理文件...
            pass
        finally:
            cleanup_files(files)  # 无论成功失败都删除
    """
    for path in file_paths:
        try:
            if os.path.exists(path):
                os.remove(path)
                print(f"🗑️  已删除：{path}")
        except OSError as e:
            print(f"⚠️  删除失败 [{path}]：{e}")
    print(f"✅ 清理完成，共删除 {len(file_paths)} 个临时文件")


# ══════════════════════════════════════════════
# 测试代码（只有直接运行才执行）
# ══════════════════════════════════════════════
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("使用方法：")
        print("  python meeting_fetcher.py wecom")
        print("  python meeting_fetcher.py feishu:123456789")
        print("  python meeting_fetcher.py https://example.com/rec.mp4")
        print("  python meeting_fetcher.py /path/to/local.mp4")
    else:
        source = sys.argv[1]
        files  = fetch_recording(source)
        print(f"\n共获取 {len(files)} 个文件：")
        for f in files:
            mb = os.path.getsize(f) / 1024 / 1024
            print(f"  {f}（{mb:.1f} MB）")