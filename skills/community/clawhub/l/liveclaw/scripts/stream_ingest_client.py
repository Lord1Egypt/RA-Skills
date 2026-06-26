#!/usr/bin/env python3
"""
腾讯云 TRTC StartStreamIngest API 客户端
- 将在线媒体流（mp3/mp4 等）推入 TRTC 房间
- 基于腾讯云 API 签名 v3 (TC3-HMAC-SHA256)
  https://cloud.tencent.com/document/api/647/101872
"""
import hashlib
import hmac
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

if sys.version_info[0] <= 2:
    from httplib import HTTPSConnection
else:
    from http.client import HTTPSConnection

def _log_stream(msg, kind="stream"):
    """打印日志到 stdout + 写入 stream_log.json 供 Viewer System Log 读取"""
    print(f"[STREAM] {msg}")
    try:
        log_file = get_work_dir() / "stream_log.json"
        logs = []
        if log_file.exists():
            try:
                logs = json.loads(log_file.read_text(encoding="utf-8"))
            except Exception:
                logs = []
        from datetime import datetime as _dt
        logs.append({"ts": _dt.now().strftime("%H:%M:%S"), "msg": msg, "kind": kind})
        if len(logs) > 30:
            logs = logs[-30:]
        log_file.write_text(json.dumps(logs, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass

def _emit_bus(kind: str, text: str):
    """直接写入 agent_events.jsonl 上报到 Dashboard（用于关键流程节点）"""
    try:
        from datetime import datetime as _dt
        icons = {"exec": "[EXEC]", "search": "[SRCH]", "info": "[INFO]", "result": "[OK]", "error": "[ERR]"}
        event = {
            "ts": _dt.now().isoformat(),
            "kind": kind,
            "icon": icons.get(kind, "•"),
            "text": text,
            "detail": "",
        }
        bus_file = get_work_dir() / "agent_events.jsonl"
        with open(bus_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
    except Exception:
        pass

try:
    from platform_utils import get_work_dir
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from platform_utils import get_work_dir

try:
    from TLSSigAPIv2 import gen_usersig
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from TLSSigAPIv2 import gen_usersig

# ── 常量 ────────────────────────────────────────────────────
SERVICE = "trtc"
HOST = "trtc.tencentcloudapi.com"
ENDPOINT = f"https://{HOST}"
ACTION = "StartStreamIngest"
VERSION = "2019-07-22"
REGION = "ap-guangzhou"

# 媒体流机器人 UserId 前缀（不能与房间内其他用户重复）
INGEST_BOT_PREFIX = "ingest-bot-"


# ── TC3-HMAC-SHA256 签名 ─────────────────────────────────────
def _sign(key: bytes, msg: str) -> bytes:
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def _load_config() -> dict:
    """从工作目录加载 config.json"""
    work_dir = get_work_dir()
    cfg_path = work_dir / "config.json"
    if cfg_path.exists():
        return json.loads(cfg_path.read_text(encoding="utf-8"))
    return {}


def start_stream_ingest(
    stream_url: str,
    secret_id: str,
    secret_key: str,
    sdkappid: int = None,
    trtc_secret: str = None,
    room_id: str = None,
    user_id: str = None,
    region: str = None,
) -> dict:
    """
    调用腾讯云 TRTC StartStreamIngest API，将在线媒体流推入房间

    Args:
        stream_url:   媒体流 URL（mp3/mp4 等）
        secret_id:    腾讯云 CAM SecretId（用于 API 鉴权）
        secret_key:   腾讯云 CAM SecretKey（用于 API 鉴权）
        sdkappid:     TRTC SDKAppID（可选，默认从 config.json 读取）
        trtc_secret:  TRTC SecretKey（用于生成 UserSig，可选，默认从 config.json 读取）
        room_id:      房间号（可选，默认从 config.json 读取）
        user_id:      机器人 UserId（可选，默认自动生成）
        region:       地域（可选，默认 ap-guangzhou）

    Returns:
        dict: {"task_id": "...", "request_id": "..."} 或 {"error": "..."}
    """
    cfg = _load_config()
    sdkappid = sdkappid or cfg.get("sdkappid")
    trtc_secret = trtc_secret or cfg.get("secret_key")
    room_id = room_id or cfg.get("room_id")
    region = region or REGION

    if not sdkappid or not room_id:
        return {"error": "sdkappid or room_id not configured"}
    if not trtc_secret:
        return {"error": "trtc secret_key not found in config (run setup.py --viewer --secret <KEY>)"}

    # 生成独立的机器人 UserId 和 UserSig
    if not user_id:
        user_id = INGEST_BOT_PREFIX + str(int(time.time() * 1000) % 100000)
    user_sig = gen_usersig(sdkappid, trtc_secret, user_id, 604800)

    # ── 构造请求体 ──
    payload = json.dumps({
        "SdkAppId": sdkappid,
        "RoomId": room_id,
        "RoomIdType": 0,       # 0 = 字符串类型
        "UserId": user_id,
        "UserSig": user_sig,
        "StreamUrl": stream_url,
    })

    timestamp = int(time.time())
    date = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%d")
    algorithm = "TC3-HMAC-SHA256"

    # ************* 步骤 1：拼接规范请求串 *************
    http_request_method = "POST"
    canonical_uri = "/"
    canonical_querystring = ""
    ct = "application/json; charset=utf-8"
    canonical_headers = "content-type:%s\nhost:%s\nx-tc-action:%s\n" % (ct, HOST, ACTION.lower())
    signed_headers = "content-type;host;x-tc-action"
    hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    canonical_request = (http_request_method + "\n" +
                         canonical_uri + "\n" +
                         canonical_querystring + "\n" +
                         canonical_headers + "\n" +
                         signed_headers + "\n" +
                         hashed_request_payload)

    # ************* 步骤 2：拼接待签名字符串 *************
    credential_scope = date + "/" + SERVICE + "/" + "tc3_request"
    hashed_canonical_request = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
    string_to_sign = (algorithm + "\n" +
                      str(timestamp) + "\n" +
                      credential_scope + "\n" +
                      hashed_canonical_request)

    # ************* 步骤 3：计算签名 *************
    secret_date = _sign(("TC3" + secret_key).encode("utf-8"), date)
    secret_service = _sign(secret_date, SERVICE)
    secret_signing = _sign(secret_service, "tc3_request")
    signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"),
                         hashlib.sha256).hexdigest()

    # ************* 步骤 4：拼接 Authorization *************
    authorization = (algorithm + " " +
                     "Credential=" + secret_id + "/" + credential_scope + ", " +
                     "SignedHeaders=" + signed_headers + ", " +
                     "Signature=" + signature)

    # ************* 步骤 5：构造并发起请求 *************
    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json; charset=utf-8",
        "Host": HOST,
        "X-TC-Action": ACTION,
        "X-TC-Timestamp": timestamp,
        "X-TC-Version": VERSION,
        "X-TC-Region": region,
    }

    try:
        req = HTTPSConnection(HOST)
        req.request("POST", "/", headers=headers, body=payload.encode("utf-8"))
        resp = req.getresponse()
        result = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error": f"API request failed: {e}"}

    response = result.get("Response", {})
    if "Error" in response:
        err = response["Error"]
        return {"error": f"{err.get('Code')} - {err.get('Message')}"}

    return {
        "task_id": response.get("TaskId", ""),
        "request_id": response.get("RequestId", ""),
        "user_id": user_id,
    }


# ── TaskId 持久化 ────────────────────────────────────────────

def _save_task(task_id: str, user_id: str = "", stream_url: str = "", song_name: str = "", artist_name: str = "", cover_url: str = ""):
    """保存当前推流任务信息和歌曲信息"""
    try:
        task_file = get_work_dir() / "stream_ingest_task.json"
        data = {"task_id": task_id, "user_id": user_id, "stream_url": stream_url, "ts": time.time()}
        task_file.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        
        # 保存给前端展示用的歌曲状态
        song_file = get_work_dir() / "current_song.json"
        song_data = {
            "playing": True,
            "song_name": song_name,
            "artist_name": artist_name,
            "cover_url": cover_url
        }
        song_file.write_text(json.dumps(song_data, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass

def _load_task() -> dict:
    """读取当前推流任务信息"""
    try:
        task_file = get_work_dir() / "stream_ingest_task.json"
        if task_file.exists():
            return json.loads(task_file.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}

def _clear_task():
    """清除推流任务信息"""
    try:
        task_file = get_work_dir() / "stream_ingest_task.json"
        if task_file.exists():
            task_file.unlink()
            
        # 清除前端展示用的歌曲状态
        song_file = get_work_dir() / "current_song.json"
        if song_file.exists():
            song_data = {"playing": False, "song_name": "", "artist_name": "", "cover_url": ""}
            song_file.write_text(json.dumps(song_data, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


def _call_api(action: str, payload: dict, secret_id: str, secret_key: str, region: str = None) -> dict:
    """通用腾讯云 API 调用（TC3-HMAC-SHA256 签名）"""
    region = region or REGION
    payload_str = json.dumps(payload)
    timestamp = int(time.time())
    date = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%d")
    algorithm = "TC3-HMAC-SHA256"

    ct = "application/json; charset=utf-8"
    canonical_headers = "content-type:%s\nhost:%s\nx-tc-action:%s\n" % (ct, HOST, action.lower())
    signed_headers = "content-type;host;x-tc-action"
    hashed_request_payload = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()
    canonical_request = ("POST\n/\n\n" + canonical_headers + "\n" +
                         signed_headers + "\n" + hashed_request_payload)

    credential_scope = date + "/" + SERVICE + "/" + "tc3_request"
    hashed_canonical_request = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
    string_to_sign = (algorithm + "\n" + str(timestamp) + "\n" +
                      credential_scope + "\n" + hashed_canonical_request)

    secret_date = _sign(("TC3" + secret_key).encode("utf-8"), date)
    secret_service = _sign(secret_date, SERVICE)
    secret_signing = _sign(secret_service, "tc3_request")
    signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"),
                         hashlib.sha256).hexdigest()

    authorization = (algorithm + " " +
                     "Credential=" + secret_id + "/" + credential_scope + ", " +
                     "SignedHeaders=" + signed_headers + ", " +
                     "Signature=" + signature)

    headers = {
        "Authorization": authorization,
        "Content-Type": ct,
        "Host": HOST,
        "X-TC-Action": action,
        "X-TC-Timestamp": timestamp,
        "X-TC-Version": VERSION,
        "X-TC-Region": region,
    }

    try:
        req = HTTPSConnection(HOST)
        req.request("POST", "/", headers=headers, body=payload_str.encode("utf-8"))
        resp = req.getresponse()
        result = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error": f"API request failed: {e}"}

    response = result.get("Response", {})
    if "Error" in response:
        err = response["Error"]
        return {"error": f"{err.get('Code')} - {err.get('Message')}"}
    return response


def update_stream_ingest(
    stream_url: str,
    secret_id: str,
    secret_key: str,
    task_id: str = None,
    sdkappid: int = None,
    region: str = None,
) -> dict:
    """
    调用 UpdateStreamIngest API，更新正在播放的媒体流 URL（切歌）

    Args:
        stream_url:  新的媒体流 URL
        secret_id:   腾讯云 CAM SecretId
        secret_key:  腾讯云 CAM SecretKey
        task_id:     任务 ID（可选，默认从持久化文件读取）
        sdkappid:    TRTC SDKAppID（可选）
        region:      地域（可选）

    Returns:
        dict: {"status": "InProgress", ...} 或 {"error": "..."}
    """
    cfg = _load_config()
    sdkappid = sdkappid or cfg.get("sdkappid")
    if not task_id:
        saved = _load_task()
        task_id = saved.get("task_id")
    if not task_id:
        return {"error": "No active stream ingest task found"}

    payload = {
        "SdkAppId": sdkappid,
        "TaskId": task_id,
        "StreamUrl": stream_url,
    }
    resp = _call_api("UpdateStreamIngest", payload, secret_id, secret_key, region)
    return resp


def stop_stream_ingest(
    task_id: str,
    secret_id: str,
    secret_key: str,
    sdkappid: int = None,
    region: str = None,
) -> dict:
    """停止在线媒体流输入"""
    cfg = _load_config()
    sdkappid = sdkappid or cfg.get("sdkappid")
    if not task_id:
        saved = _load_task()
        task_id = saved.get("task_id")
    if not task_id:
        return {"error": "No active stream ingest task found"}

    _log_stream(f"TRTC StopStreamIngest: TaskId={task_id[:16]}...")
    payload = {
        "SdkAppId": sdkappid,
        "TaskId": task_id,
    }
    resp = _call_api("StopStreamIngest", payload, secret_id, secret_key, region)
    if "error" not in resp:
        _clear_task()
        _log_stream("TRTC StopStreamIngest 成功，音乐播放已停止")
    else:
        _log_stream(f"TRTC StopStreamIngest 失败: {resp.get('error','')}", "error")
    return resp


def describe_stream_ingest(
    task_id: str = None,
    secret_id: str = None,
    secret_key: str = None,
    sdkappid: int = None,
    region: str = None,
) -> dict:
    """查询输入在线媒体流任务状态
    参考: https://cloud.tencent.com/document/api/647/101873

    Returns:
        dict: {"Status": "InProgress"|"NotExist", ...} 或 {"error": "..."}
    """
    cfg = _load_config()
    sdkappid = sdkappid or cfg.get("sdkappid")
    secret_id = secret_id or cfg.get("cam_secret_id") or cfg.get("tts_secret_id") or ""
    secret_key = secret_key or cfg.get("cam_secret_key") or cfg.get("tts_secret_key") or ""
    if not task_id:
        saved = _load_task()
        task_id = saved.get("task_id")
    if not task_id:
        return {"Status": "NotExist", "reason": "no task_id"}
    if not secret_id or not secret_key:
        return {"error": "CAM credentials not configured"}

    payload = {
        "SdkAppId": sdkappid,
        "TaskId": task_id,
    }
    resp = _call_api("DescribeStreamIngest", payload, secret_id, secret_key, region)
    if "error" not in resp:
        status = resp.get("Status", "NotExist")
        # 如果任务已不存在，自动清除本地状态
        if status != "InProgress":
            _clear_task()
        return resp
    return resp


def _check_url_reachable(url: str, timeout: int = 5) -> tuple[bool, str]:
    """用 HTTP HEAD 请求检查 URL 是否可达。返回 (ok, reason)。"""
    try:
        req = Request(url, method='HEAD')
        req.add_header('User-Agent', 'TRTC-StreamIngest/1.0')
        resp = urlopen(req, timeout=timeout)
        status = resp.getcode()
        if 200 <= status < 400:
            return True, f"HTTP {status}"
        return False, f"HTTP {status}"
    except HTTPError as e:
        # 有些 CDN 不允许 HEAD，尝试 GET 并只读少量
        try:
            req2 = Request(url)
            req2.add_header('User-Agent', 'TRTC-StreamIngest/1.0')
            req2.add_header('Range', 'bytes=0-1023')
            resp2 = urlopen(req2, timeout=timeout)
            return True, f"HEAD→{e.code}, GET→{resp2.getcode()}"
        except Exception as e2:
            return False, f"HEAD→{e.code}, GET→{e2}"
    except URLError as e:
        return False, f"URLError: {e.reason}"
    except Exception as e:
        return False, str(e)


def play_music(
    stream_url: str,
    secret_id: str,
    secret_key: str,
    sdkappid: int = None,
    trtc_secret: str = None,
    room_id: str = None,
    region: str = None,
    song_name: str = "",
    artist_name: str = "",
    cover_url: str = "",
) -> dict:
    """
    智能播放：如果已有推流任务则 Update，否则 Start。
    这是推荐的统一入口。

    Returns:
        dict: {"action": "start"|"update", "task_id": "...", ...} 或 {"error": "..."}
    """
    display_name = f"{song_name} - {artist_name}" if song_name else stream_url[:80]

    # 上报 Dashboard：开始推流
    _emit_bus("exec", f"正在推流到TRTC房间: {display_name}")

    # ── 播放前检查 URL 有效性 ──
    _log_stream(f"检查歌曲URL有效性: {stream_url[:120]}")
    url_ok, url_reason = _check_url_reachable(stream_url)
    if not url_ok:
        err_msg = f"歌曲URL无效或不可达: {url_reason}"
        _log_stream(err_msg, "error")
        _emit_bus("error", f"歌曲链接失效: {display_name}")
        return {"error": err_msg}
    _log_stream(f"URL可达 ({url_reason}), 准备推流: {display_name}")

    saved = _load_task()
    if saved.get("task_id"):
        # 已有任务，尝试 Update（切歌）
        _emit_bus("exec", f"切歌: {display_name}")
        _log_stream(f"TRTC UpdateStreamIngest (切歌): {display_name}, TaskId={saved['task_id'][:16]}...")
        resp = update_stream_ingest(stream_url, secret_id, secret_key,
                                     task_id=saved["task_id"], sdkappid=sdkappid, region=region)
        if "error" not in resp and resp.get("Status") != "NotExist":
            _save_task(saved["task_id"], saved.get("user_id", ""), stream_url, song_name, artist_name, cover_url)
            _log_stream(f"TRTC UpdateStreamIngest 成功: {display_name}, Status={resp.get('Status','')}")
            return {"action": "update", "task_id": saved["task_id"],
                    "status": resp.get("Status", ""), "request_id": resp.get("RequestId", "")}
        # 任务不存在，清除后重新 Start
        _log_stream(f"旧任务不存在 (TaskId={saved['task_id'][:16]}...), 重新启动推流")
        _clear_task()

    _log_stream(f"TRTC StartStreamIngest: {display_name}")
    resp = start_stream_ingest(stream_url, secret_id, secret_key,
                                sdkappid=sdkappid, trtc_secret=trtc_secret,
                                room_id=room_id, region=region)
    if "error" not in resp and resp.get("task_id"):
        _save_task(resp["task_id"], resp.get("user_id", ""), stream_url, song_name, artist_name, cover_url)
        _log_stream(f"TRTC StartStreamIngest 成功: {display_name}, TaskId={resp['task_id'][:16]}...")
        return {"action": "start", **resp}

    err_msg = resp.get("error", "Unknown error")
    _log_stream(f"TRTC StartStreamIngest 失败: {err_msg}", "error")
    return resp


# ── CLI ─────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="TRTC StreamIngest — 输入在线媒体流到 TRTC 房间（支持智能切歌）",
        epilog=(
            "示例:\n"
            "  播放: python3 stream_ingest_client.py --url URL --song-name '歌名' --artist-name '歌手'\n"
            "  切歌: python3 stream_ingest_client.py --url NEW_URL --song-name '新歌名'\n"
            "        (自动检测已有任务并 Update，无需手动管理 TaskId)\n"
            "  停止: python3 stream_ingest_client.py --stop\n"
            "\n"
            "  CAM 密钥自动从 config.json 的 cam_secret_id/cam_secret_key 读取。\n"
            "  也可手动指定: --secret-id AKIDxxx --secret-key xxx"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--secret-id", required=False, default=None, help="腾讯云 CAM SecretId（可选，默认从 config.json 读取）")
    parser.add_argument("--secret-key", required=False, default=None, help="腾讯云 CAM SecretKey（可选，默认从 config.json 读取）")
    parser.add_argument("--url", default=None, help="媒体流 URL (mp3/mp4)")
    parser.add_argument("--song-name", default="未知歌曲", help="歌曲名称")
    parser.add_argument("--artist-name", default="Agent Music Search", help="歌手名称")
    parser.add_argument("--cover-url", default="https://images.unsplash.com/photo-1614613535308-eb5fbd3d2c17?q=80&w=100&auto=format&fit=crop", help="封面图片 URL")
    parser.add_argument("--sdkappid", type=int, default=None)
    parser.add_argument("--room", default=None)
    parser.add_argument("--region", default=None)
    parser.add_argument("--stop", action="store_true", help="停止当前播放（自动读取 TaskId）")
    parser.add_argument("--task-id", default=None, help="指定 TaskId（可选，默认自动管理）")

    args = parser.parse_args()

    # 自动从 config.json 读取 CAM 密钥（如果命令行未传入）
    if not args.secret_id or not args.secret_key:
        _cfg = _load_config()
        if not args.secret_id:
            args.secret_id = _cfg.get("cam_secret_id") or _cfg.get("tts_secret_id") or ""
        if not args.secret_key:
            args.secret_key = _cfg.get("cam_secret_key") or _cfg.get("tts_secret_key") or ""
    if not args.secret_id or not args.secret_key:
        print("[ERROR] CAM SecretId/SecretKey not found. Pass --secret-id/--secret-key or configure cam_secret_id/cam_secret_key in config.json")
        sys.exit(1)

    if args.stop:
        result = stop_stream_ingest(
            task_id=args.task_id,
            secret_id=args.secret_id,
            secret_key=args.secret_key,
            sdkappid=args.sdkappid,
            region=args.region,
        )
        if "error" in result:
            print(f"[ERROR] {result['error']}")
        else:
            print(f"[OK] Stream stopped. RequestId: {result.get('RequestId', '')}")
    elif args.url:
        # 智能播放：自动判断 start 或 update
        result = play_music(
            stream_url=args.url,
            secret_id=args.secret_id,
            secret_key=args.secret_key,
            sdkappid=args.sdkappid,
            room_id=args.room,
            region=args.region,
            song_name=args.song_name,
            artist_name=args.artist_name,
            cover_url=args.cover_url
        )
        if "error" in result:
            print(f"[ERROR] {result['error']}")
        else:
            action = result.get("action", "start")
            print(f"[OK] Stream {action}d!")
            if action == "start":
                print(f"  TaskId:    {result.get('task_id', '')}")
                print(f"  UserId:    {result.get('user_id', '')}")
            else:
                print(f"  TaskId:    {result.get('task_id', '')}")
                print(f"  Status:    {result.get('status', '')}")
            print(f"  RequestId: {result.get('request_id', '')}")
    else:
        parser.print_help()
