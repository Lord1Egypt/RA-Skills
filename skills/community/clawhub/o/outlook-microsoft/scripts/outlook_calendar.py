#!/usr/bin/env python3
"""
Microsoft Outlook 日历操作脚本 - 世纪互联版
支持日程查看、创建、修改、删除、忙闲查询
"""

import json
import os
import sys
import io
import requests
from pathlib import Path
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

# 确保 stdout 输出 UTF-8 编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 世纪互联版 Graph API 端点
GRAPH_BASE_URL = "https://microsoftgraph.chinacloudapi.cn"
SCRIPT_DIR = Path(__file__).parent
CONFIG_DIR = Path.home() / ".outlook-microsoft"
CREDS_FILE = CONFIG_DIR / "credentials.json"
ENV_FILE = SCRIPT_DIR / ".env"


def load_env():
    """从 .env 文件加载环境变量"""
    if not ENV_FILE.exists():
        return
    with open(ENV_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                if key and value and not os.getenv(key):
                    os.environ[key] = value


load_env()  # 启动时加载 .env 文件


def load_credentials():
    if not CREDS_FILE.exists():
        return None
    with open(CREDS_FILE, "r") as f:
        return json.load(f)


def get_access_token():
    """获取有效的 Access Token"""
    creds = load_credentials()
    if not creds:
        print(json.dumps({
            "error": "AUTH_001",
            "message": "未授权，请先运行 outlook_auth.py authorize 完成授权。"
        }, ensure_ascii=False))
        sys.exit(1)

    import time
    if time.time() < creds.get("expires_at", 0) - 300:
        return creds["access_token"]

    # Token 过期，尝试刷新
    import subprocess
    result = subprocess.run(
        ["python3", str(Path(__file__).parent / "outlook_auth.py"), "refresh"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(json.dumps({
            "error": "AUTH_002",
            "message": "Token 已过期且刷新失败，请重新运行 authorize。"
        }, ensure_ascii=False))
        sys.exit(1)

    creds = load_credentials()
    return creds["access_token"] if creds else None


def api_call(method, path, token, data=None, params=None):
    """调用 Microsoft Graph API"""
    url = f"{GRAPH_BASE_URL}/v1.0{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        if method.upper() == "GET":
            resp = requests.get(url, headers=headers, params=params, timeout=30)
        elif method.upper() == "POST":
            resp = requests.post(url, headers=headers, json=data, timeout=30)
        elif method.upper() == "PATCH":
            resp = requests.patch(url, headers=headers, json=data, timeout=30)
        elif method.upper() == "DELETE":
            resp = requests.delete(url, headers=headers, timeout=30)
        else:
            raise ValueError(f"Unknown method: {method}")

        resp.raise_for_status()
        return resp.json() if resp.content else {}

    except requests.exceptions.HTTPError as e:
        try:
            err_body = e.response.json()
            err_msg = err_body.get("error", {}).get("message", str(e))
        except:
            err_msg = str(e)

        print(json.dumps({
            "error": "API_002",
            "message": f"Graph API 调用失败: {err_msg}",
            "http_status": e.response.status_code
        }, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "error": "API_001",
            "message": f"网络请求失败: {str(e)}"
        }, ensure_ascii=False))
        sys.exit(1)


SHANGHAI_TZ = ZoneInfo("Asia/Shanghai")

def parse_datetime(dt_str):
    """解析 ISO 8601 日期时间字符串，转换为上海时区显示"""
    if not dt_str:
        return None
    try:
        if 'T' in dt_str:
            # 替换 Z 为 +00:00 后解析
            dt_str_clean = dt_str.replace('Z', '+00:00')
            # 解析为 aware datetime
            dt = datetime.fromisoformat(dt_str_clean)
            # 如果没有时区信息，默认当作 UTC
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            # 转换为上海时区
            dt_shanghai = dt.astimezone(SHANGHAI_TZ)
            return dt_shanghai.strftime("%Y-%m-%d %H:%M:%S +08:00")
    except:
        pass
    return dt_str


def cmd_events(args):
    """查看最近 N 个日程"""
    token = get_access_token()
    count = args.get("count", 10)

    result = api_call("GET", "/me/calendar/events", token, params={
        "$top": count,
        "$orderby": "start/dateTime",
        "$filter": "start/dateTime ge " + datetime.now(ZoneInfo("UTC")).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "$select": "id,subject,start,end,location,isAllDay,showAs,bodyPreview"
    })

    events = result.get("value", [])
    output = []
    for i, ev in enumerate(events, 1):
        output.append({
            "n": i,
            "subject": ev.get("subject", "(无标题)"),
            "start": parse_datetime(ev.get("start", {}).get("dateTime")),
            "end": parse_datetime(ev.get("end", {}).get("dateTime")),
            "location": ev.get("location", {}).get("displayName", ""),
            "all_day": ev.get("isAllDay", False),
            "show_as": ev.get("showAs", "busy"),
            "id": ev.get("id", "")
        })

    print(json.dumps(output, ensure_ascii=False, indent=2))


def calendar_view(token, start_datetime, end_datetime, select_fields=None):
    """使用 calendarView API 按日期范围查询日程（支持重复周期事件展开）"""
    if select_fields is None:
        select_fields = "id,subject,start,end,location,isAllDay,showAs"
    params = {
        "startDateTime": start_datetime,
        "endDateTime": end_datetime,
        "$select": select_fields,
        "$orderby": "start/dateTime"
    }
    result = api_call("GET", "/me/calendarView", token, params=params)
    return result.get("value", [])


def cmd_today(args):
    """查看今日日程（使用 calendarView，支持重复周期事件）"""
    token = get_access_token()
    today = datetime.now(SHANGHAI_TZ).strftime("%Y-%m-%d")
    start_of_day = f"{today}T00:00:00+08:00"
    end_of_day = f"{today}T23:59:59+08:00"

    events = calendar_view(token, start_of_day, end_of_day)

    output = []
    for i, ev in enumerate(events, 1):
        output.append({
            "n": i,
            "subject": ev.get("subject", "(无标题)"),
            "start": parse_datetime(ev.get("start", {}).get("dateTime")),
            "end": parse_datetime(ev.get("end", {}).get("dateTime")),
            "location": ev.get("location", {}).get("displayName", ""),
            "all_day": ev.get("isAllDay", False),
            "id": ev.get("id", "")
        })

    if not output:
        output = {"message": "今日无日程"}

    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_week(args):
    """查看本周日程（使用 calendarView，支持重复周期事件）"""
    token = get_access_token()
    today = datetime.now(SHANGHAI_TZ)
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    start_str = start_of_week.strftime("%Y-%m-%dT00:00:00+08:00")
    end_str = end_of_week.strftime("%Y-%m-%dT23:59:59+08:00")

    events = calendar_view(token, start_str, end_str)

    output = []
    for i, ev in enumerate(events, 1):
        output.append({
            "n": i,
            "subject": ev.get("subject", "(无标题)"),
            "start": parse_datetime(ev.get("start", {}).get("dateTime")),
            "end": parse_datetime(ev.get("end", {}).get("dateTime")),
            "location": ev.get("location", {}).get("displayName", ""),
            "all_day": ev.get("isAllDay", False),
            "id": ev.get("id", "")
        })

    if not output:
        output = {"message": "本周无日程"}

    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_read(args):
    """读取单个日程详情"""
    token = get_access_token()
    event_id = args.get("event_id", "")

    if not event_id:
        print(json.dumps({"error": "API_002", "message": "event_id 不能为空"}))
        sys.exit(1)

    ev = api_call("GET", f"/me/calendar/events/{event_id}", token)

    attendees = []
    for a in ev.get("attendees", []):
        attendees.append({
            "address": a.get("emailAddress", {}).get("address", ""),
            "name": a.get("emailAddress", {}).get("name", ""),
            "response": a.get("status", {}).get("response", "none")
        })

    output = {
        "id": ev.get("id"),
        "subject": ev.get("subject", "(无标题)"),
        "start": parse_datetime(ev.get("start", {}).get("dateTime")),
        "end": parse_datetime(ev.get("end", {}).get("dateTime")),
        "location": ev.get("location", {}).get("displayName", ""),
        "all_day": ev.get("isAllDay", False),
        "show_as": ev.get("showAs", "busy"),
        "body": ev.get("body", {}).get("content", "")[:2000],
        "body_type": ev.get("body", {}).get("contentType", "text"),
        "attendees": attendees,
        "organizer": ev.get("organizer", {}).get("emailAddress", {}).get("address", ""),
        "is_recurring": bool(ev.get("recurrence")),
        "series_id": ev.get("recurrenceItemId", None)
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_create(args):
    """创建日程"""
    token = get_access_token()
    subject = args.get("subject", "")
    start = args.get("start", "")
    end = args.get("end", "")
    location = args.get("location", "")
    body = args.get("body", "")
    all_day = args.get("all_day", False)
    attendees = args.get("attendees", [])
    is_online = args.get("is_online_meeting", False)

    if not subject or not start or not end:
        print(json.dumps({
            "error": "API_002",
            "message": "subject（标题）、start（开始时间）、end（结束时间）不能为空"
        }))
        sys.exit(1)

    event_data = {
        "subject": subject,
        "start": {
            "dateTime": start,
            "timeZone": "China Standard Time"
        },
        "end": {
            "dateTime": end,
            "timeZone": "China Standard Time"
        },
        "isAllDay": all_day,
        "showAs": "busy"
    }

    if location:
        event_data["location"] = {"displayName": location}

    if body:
        event_data["body"] = {
            "contentType": "Text",
            "content": body
        }

    if attendees:
        event_data["attendees"] = [
            {"emailAddress": {"address": a, "name": ""}, "type": "required"}
            for a in attendees if a
        ]

    if is_online:
        event_data["isOnlineMeeting"] = True
        event_data["onlineMeetingProvider"] = "teamsForBusiness"

    result = api_call("POST", "/me/calendar/events", token, data=event_data)

    print(json.dumps({
        "status": "event created",
        "subject": result.get("subject"),
        "start": parse_datetime(result.get("start", {}).get("dateTime")),
        "end": parse_datetime(result.get("end", {}).get("dateTime")),
        "id": result.get("id"),
        "online_meeting_url": result.get("onlineMeeting", {}).get("joinUrl") if is_online else None
    }, ensure_ascii=False))


def cmd_quick(args):
    """快速创建1小时日程"""
    subject = args.get("subject", "快速会议")
    start = args.get("start", "")

    if not start:
        # 默认从下一个整点开始（上海时区）
        now = datetime.now(SHANGHAI_TZ)
        next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        start = next_hour.strftime("%Y-%m-%dT%H:%M:%S")

    end_dt = datetime.fromisoformat(start.replace("T", " ")).replace(tzinfo=SHANGHAI_TZ) + timedelta(hours=1)
    end = end_dt.strftime("%Y-%m-%dT%H:%M:%S")

    cmd_create({
        "subject": subject,
        "start": start,
        "end": end
    })


def cmd_update(args):
    """更新日程"""
    token = get_access_token()
    event_id = args.get("event_id", "")
    field = args.get("field", "")
    value = args.get("value", "")

    if not event_id or not field:
        print(json.dumps({"error": "API_002", "message": "event_id 和 field 不能为空"}))
        sys.exit(1)

    update_data = {}
    if field in ("subject", "location"):
        update_data[field] = value
    elif field in ("start", "end"):
        update_data[field] = {
            "dateTime": value,
            "timeZone": "China Standard Time"
        }

    if not update_data:
        print(json.dumps({"error": "API_002", "message": f"不支持的字段: {field}"}))
        sys.exit(1)

    api_call("PATCH", f"/me/calendar/events/{event_id}", token, data=update_data)
    print(json.dumps({"status": "success", "message": f"✅ 已更新 {field} 为 {value}"}))


def cmd_delete(args):
    """删除日程"""
    token = get_access_token()
    event_id = args.get("event_id", "")

    if not event_id:
        print(json.dumps({"error": "API_002", "message": "event_id 不能为空"}))
        sys.exit(1)

    api_call("DELETE", f"/me/calendar/events/{event_id}", token)
    print(json.dumps({"status": "success", "message": "✅ 日程已删除"}))


def cmd_calendars(args):
    """列出所有日历"""
    token = get_access_token()

    result = api_call("GET", "/me/calendars", token)

    output = []
    for cal in result.get("value", []):
        output.append({
            "name": cal.get("name"),
            "id": cal.get("id"),
            "color": cal.get("hexColor", "auto"),
            "total": cal.get("totalItemCount", 0),
            "unread": cal.get("unreadItemCount", 0),
            "is_default": cal.get("isDefaultCalendar", False)
        })

    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_freebusy(args):
    """查询忙闲状态"""
    token = get_access_token()
    start = args.get("start", "")
    end = args.get("end", "")
    emails = args.get("emails", [])

    if not start or not end:
        print(json.dumps({"error": "API_002", "message": "start 和 end 不能为空"}))
        sys.exit(1)

    # 如果没有指定邮箱，默认查自己
    if not emails:
        me = api_call("GET", "/me", token)
        emails = [me.get("mail", me.get("userPrincipalName", ""))]

    data = {
        "timeWindow": {
            "start": start,
            "end": end
        },
        "availabilityViewInterval": 30,
        "schedules": emails
    }

    result = api_call("POST", "/me/calendar/getSchedule", token, data=data)

    output = []
    for schedule in result.get("value", []):
        schedule_id = schedule.get("scheduleId", "")
        events = schedule.get("scheduleItems", [])

        busy_slots = [
            {
                "start": e.get("start", ""),
                "end": e.get("end", ""),
                "status": e.get("status", ""),
                "subject": e.get("subject", "")
            }
            for e in events if e.get("status") in ("busy", "tentative", "oof")
        ]

        output.append({
            "email": schedule_id,
            "busy_slots": busy_slots if busy_slots else [],
            "status": "busy" if busy_slots else "free"
        })

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: outlook_calendar.py <command> '<json_params>'")
        print("\n可用命令：events, today, week, read, create, quick, update, delete, calendars, freebusy")
        sys.exit(1)

    cmd = sys.argv[1].lower()

    # 从 stdin 或 argv 读取 JSON 参数
    args = {}
    if len(sys.argv) >= 3:
        try:
            args = json.loads(sys.argv[2])
        except json.JSONDecodeError as e:
            print(json.dumps({"error": "API_002", "message": f"JSON 参数解析失败: {e}"}))
            sys.exit(1)

    # 命令路由
    commands = {
        "events": cmd_events,
        "today": cmd_today,
        "week": cmd_week,
        "read": cmd_read,
        "create": cmd_create,
        "quick": cmd_quick,
        "update": cmd_update,
        "delete": cmd_delete,
        "calendars": cmd_calendars,
        "freebusy": cmd_freebusy,
    }

    if cmd in commands:
        commands[cmd](args)
    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)
