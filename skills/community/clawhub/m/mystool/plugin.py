"""
mystool — 米游社工具 OpenClaw Skill 入口

支持指令:
  米游社登录               选择登录方式（短信/扫码/Cookie）
  米游社绑定 <cookie>       手动绑定账号（Cookie 登录）
  米游社账号                查看已绑定账号
  米游社解绑 <uid>          解绑账号
  米游社任务                执行每日米游币任务
  米游社签到 [游戏]         游戏签到（原神/星铁/崩3，国服）
  原神便笺                  查看原神实时便笺
  星铁便笺                  查看星穹铁道便笺
  米游币商品 [游戏]         查看商品列表
  米游社兑换 <商品ID> [数量] 兑换商品
  米游社帮助                显示帮助
"""

import asyncio
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

_HERE = Path(__file__).parent
sys.path.insert(0, str(_HERE / "src"))

from api import (
    do_bbs_tasks,
    do_exchange,
    game_sign,
    get_account_list_by_game,
    get_address_list,
    get_genshin_note,
    get_good_detail,
    get_good_list,
    get_myb_balance,
    get_starrail_note,
    SIGN_APIS,
)
from store import (
    add_account,
    clear_login_session,
    clear_sms_session,
    extract_uid_from_cookies,
    get_all_user_ids,
    get_login_session,
    get_sms_session,
    get_user_accounts,
    parse_cookie_string,
    remove_account,
    save_login_session,
    save_sms_session,
    validate_cookies,
    generate_link_code,
    verify_link_code,
    merge_user_accounts,
)
from qr_login import (
    fetch_qrcode,
    game_token_to_cookies,
    qrcode_to_image_url,
    query_qrcode,
)
from sms_login import (
    sms_send_captcha,
    sms_login_by_captcha,
    sms_get_full_cookies,
)
from formatter import (
    format_account_list,
    format_genshin_note,
    format_good_list,
    format_sign_results,
    format_starrail_note,
    format_task_result,
)

# ── 游戏别名映射 ───────────────────────────────────────────────────────────────

GAME_ALIASES = {
    # 原神
    "原神": "genshin",
    "ys": "genshin",
    "genshin": "genshin",
    # 星穹铁道
    "星穹铁道": "starrail",
    "星铁": "starrail",
    "hkrpg": "starrail",
    "starrail": "starrail",
    # 崩坏3
    "崩坏3": "honkai3",
    "bh3": "honkai3",
    "honkai3": "honkai3",
    # 崩坏学园2
    "崩坏2": "honkai2",
    "崩坏学园2": "honkai2",
    "honkai2": "honkai2",
    # 未定事件簿
    "未定": "tearsofthemis",
    "未定事件簿": "tearsofthemis",
    "tearsofthemis": "tearsofthemis",
    # 绝区零
    "绝区零": "zzz",
    "zzz": "zzz",
}

# 游戏对应服务器区域（国服）
GAME_REGIONS = {
    "genshin": "cn_gf01",
    "starrail": "prod_gf_cn",
    "honkai3": "cn01",
    "honkai2": "cn01",
    "tearsofthemis": "cn01",
    "zzz": "prod_gf_cn",
}

# 游戏对应的 game_biz
GAME_BIZ = {
    "genshin": "hk4e_cn",
    "starrail": "hkrpg_cn",
    "honkai3": "bh3_cn",
    "honkai2": "bh2_cn",
    "tearsofthemis": "nxx_cn",
    "zzz": "nap_cn",
}

# ── 登录菜单 ───────────────────────────────────────────────────────────────────
LOGIN_MENU = """🔐 请选择登录方式：

1️⃣  短信登录
    发送短信验证码到手机，自动获取完整 Cookie

2️⃣  扫码登录
    用米游社App 扫码，自动获取完整 Cookie

3️⃣  Cookie 登录
    直接粘贴 Cookie 字符串导入

回复 1/2/3 选择，或发送对应关键词"""


# ── 主处理函数 ─────────────────────────────────────────────────────────────────

async def handle(message: str, user_id: str = "default") -> Optional[str]:
    """
    处理用户消息，返回回复文本。
    返回 None 表示不响应。
    """
    msg = message.strip()

    # ── 登录入口 ──────────────────────────────────────────────────────────────
    if msg in ("米游社登录", "登录米游社", "登录"):
        return LOGIN_MENU

    # ── 选择登录方式 ──────────────────────────────────────────────────────────
    if msg in ("1", "短信登录", "1.短信登录", "1. 短信登录"):
        return await cmd_sms_login_start(user_id)

    if msg in ("2", "扫码登录", "2.扫码登录", "2. 扫码登录"):
        return await cmd_qr_login_start(user_id)

    if msg in ("3", "cookie登录", "ck登录", "3.cookie登录", "3. cookie登录",
               "cookie", "Cookie", "CK", "ck"):
        return (
            "请直接发送你的 Cookie 字符串，格式：\n\n"
            "`account_id=xxx; cookie_token=xxx; ...`\n\n"
            "💡 获取方式：登录 https://bbs.mihoyo.com 后，"
            "打开浏览器开发者工具 → Application → Cookies 复制全部内容\n\n"
            "⚠️ 如果 Cookie 中缺少 stoken，系统会提示你扫码补全"
        )

    # ── 短信登录流程（手机号 / 验证码）───────────────────────────────────────
    if get_sms_session(user_id):
        return await cmd_sms_login_verify(user_id, msg)
    
    # ── 短信验证码输入 ────────────────────────────────────────────────────────
    if msg.isdigit() and len(msg) == 6:
        # 可能是短信验证码
        return await cmd_sms_login_verify(user_id, msg)

    # ── Cookie 直接导入 ───────────────────────────────────────────────────────
    if "account_id=" in msg or "cookie_token=" in msg or "stoken=" in msg:
        return await cmd_bind(user_id, msg)

    # ── 扫码状态查询 ──────────────────────────────────────────────────────────
    if msg in ("米游社登录状态", "登录状态", "扫码确认", "确认登录"):
        return await cmd_qr_login_poll(user_id)

    # ── 查看账号 ──────────────────────────────────────────────────────────────
    if msg in ("米游社账号", "米游社账号列表", "查看账号", "我的账号"):
        accounts = get_user_accounts(user_id)
        return format_account_list(accounts)

    # ── 解绑账号 ──────────────────────────────────────────────────────────────
    if msg.startswith("米游社解绑"):
        arg = msg[len("米游社解绑"):].strip()
        accounts = get_user_accounts(user_id)
        if not accounts:
            return "❌ 未绑定任何账号"
        if not arg:
            if len(accounts) == 1:
                uid = accounts[0]["uid"]
            else:
                lines = ["请指定要解绑的账号（发送序号或 UID）："]
                for i, a in enumerate(accounts, 1):
                    lines.append(f"{i}. {a['nickname']} — {a['uid']}")
                return "\n".join(lines)
        elif arg.isdigit() and int(arg) <= 10:
            idx = int(arg) - 1
            if 0 <= idx < len(accounts):
                uid = accounts[idx]["uid"]
            else:
                return f"❌ 序号 {arg} 超出范围（共 {len(accounts)} 个账号）"
        else:
            uid = arg

        if remove_account(user_id, uid):
            nick = next((a["nickname"] for a in accounts if a["uid"] == uid), uid)
            return f"✅ 已解绑账号：{nick}（UID: {uid}）"
        return f"❌ 未找到 UID 为 {uid} 的绑定账号"

    # ── 每日任务 ──────────────────────────────────────────────────────────────
    if msg in ("米游社任务", "米游币任务", "每日任务"):
        return await cmd_daily_tasks(user_id)

    # ── 游戏签到 ──────────────────────────────────────────────────────────────
    if msg.startswith("米游社签到"):
        game_str = msg[len("米游社签到"):].strip()
        game = GAME_ALIASES.get(game_str) if game_str else None
        return await cmd_sign(user_id, game)

    # ── 原神便笺 ──────────────────────────────────────────────────────────────
    if msg in ("原神便笺", "原神实时便笺", "树脂"):
        return await cmd_note(user_id, "genshin")

    # ── 星铁便笺 ──────────────────────────────────────────────────────────────
    if msg in ("星铁便笺", "星穹铁道便笺", "开拓力"):
        return await cmd_note(user_id, "starrail")

    # ── 商品列表 ──────────────────────────────────────────────────────────────
    if msg.startswith("米游币商品"):
        game_str = msg[len("米游币商品"):].strip()
        game = GAME_ALIASES.get(game_str, "")
        return await cmd_good_list(game)

    # ── 兑换商品 ──────────────────────────────────────────────────────────────
    if msg.startswith("米游社兑换"):
        args = msg[len("米游社兑换"):].strip().split()
        if not args:
            return "用法: 米游社兑换 <商品ID> [数量]\n\n先用「米游币商品」查看商品 ID"
        goods_id = args[0]
        num = int(args[1]) if len(args) > 1 and args[1].isdigit() else 1
        return await cmd_exchange(user_id, goods_id, num)

    # ── 预约兑换（定时抢购）──────────────────────────────────────────────────
    if msg.startswith("预约兑换"):
        args = msg[len("预约兑换"):].strip().split()
        if not args:
            return "用法: 预约兑换 <商品ID>\n\n先用「米游币商品」查看商品 ID"
        goods_id = args[0]
        return await cmd_schedule_exchange(user_id, goods_id)

    # ── 查看预约列表 ──────────────────────────────────────────────────────────
    if msg in ("预约列表", "我的预约", "兑换预约"):
        return cmd_list_scheduled_exchanges(user_id)

    # ── 取消预约 ──────────────────────────────────────────────────────────────
    if msg.startswith("取消预约"):
        args = msg[len("取消预约"):].strip().split()
        if not args:
            return "用法: 取消预约 <商品ID>"
        return cmd_cancel_scheduled_exchange(user_id, args[0])

    # ── 链接账号（跨平台绑定）──────────────────────────────────────────────────
    if msg in ("生成识别码", "生成绑定码", "创建识别码"):
        return cmd_generate_link_code(user_id)
    
    if msg.startswith("链接账号 ") or msg.startswith("绑定账号 "):
        code = msg.split(maxsplit=1)[1].strip() if " " in msg else ""
        return await cmd_link_account(user_id, code)

    # ── 代理配置 ──────────────────────────────────────────────────────────────
    if msg.startswith("设置代理 ") or msg.startswith("代理地址 "):
        url = msg.split(maxsplit=1)[1].strip()
        return cmd_set_proxy(url)
    
    if msg in ("查看代理", "代理配置", "代理信息"):
        return cmd_show_proxy()

    # ── stoken 补全扫码 ───────────────────────────────────────────────────────
    if msg in ("扫码补全stoken", "补全stoken", "stoken扫码"):
        return await cmd_stoken_qr_login(user_id)

    # ── 帮助 ──────────────────────────────────────────────────────────────────
    if msg in ("米游社帮助", "mystool帮助", "mystool help"):
        return HELP_TEXT

    return None


# ── 指令实现 ───────────────────────────────────────────────────────────────────

async def cmd_sms_login_start(user_id: str) -> str:
    """
    短信登录第一步：提示用户输入手机号
    """
    save_sms_session(user_id, {"step": "await_phone"})
    return (
        "📱 短信登录\n"
        "─" * 24 + "\n\n"
        "请输入你的手机号（中国大陆）：\n"
        "格式：11位数字，如 13800138000"
    )


async def cmd_sms_login_verify(user_id: str, code: str) -> str:
    """
    处理手机号输入或验证码输入
    """
    session = get_sms_session(user_id) or {}
    step = session.get("step", "")

    # 输入手机号
    if step == "await_phone":
        phone = code
        if not re.match(r"^1\d{10}$", phone):
            return "❌ 手机号格式错误，请输入 11 位数字手机号"

        # 发送验证码
        result = await sms_send_captcha(phone)
        if not result["success"]:
            return f"❌ 发送验证码失败：{result.get('message', '未知错误')}"

        save_sms_session(user_id, {
            "step": "await_captcha",
            "phone": phone,
            "action_type": result.get("action_type", "login"),
            "device_id": result.get("device_id"),
            "device_fp": result.get("device_fp"),
        })
        return (
            f"✅ 验证码已发送到 {phone}\n"
            f"请输入收到的 6 位验证码："
        )

    # 输入验证码
    if step == "await_captcha":
        phone = session.get("phone", "")
        action_type = session.get("action_type", "login")
        device_id = session.get("device_id")
        device_fp = session.get("device_fp")

        if not phone:
            clear_sms_session(user_id)
            return "❌ 会话已过期，请重新发送「米游社登录」"

        # 登录
        result = await sms_login_by_captcha(
            phone, code, action_type,
            device_id=device_id, device_fp=device_fp
        )

        if not result["success"]:
            clear_sms_session(user_id)
            return f"❌ 登录失败：{result.get('message', '未知错误')}"

        stoken = result.get("stoken", "")
        stuid = result.get("stuid", "")
        mid = result.get("mid", "")

        if not stoken:
            clear_sms_session(user_id)
            return (
                "⚠️ 登录成功但未获取到 stoken\n"
                "请使用「扫码登录」或「Cookie 登录」方式"
            )

        # 换取完整 cookies
        cookies = await sms_get_full_cookies(stoken, stuid, mid, device_id, device_fp)
        clear_sms_session(user_id)

        return await _finish_login(user_id, stuid, cookies)

    # 没有活跃的短信会话，可能是其他验证码
    return None


async def cmd_qr_login_start(user_id: str) -> str:
    """
    发起扫码登录：生成二维码，然后后台自动轮询 60s
    """
    clear_login_session(user_id)

    ok, qr_url, ticket, device = await fetch_qrcode()
    if not ok or not qr_url or not ticket:
        return "❌ 获取二维码失败，请稍后重试"

    save_login_session(user_id, ticket, qr_url, device)

    qr_img_url = qrcode_to_image_url(qr_url)

    lines = [
        "📱 米游社扫码登录",
        "─" * 24,
        "",
        f"🔗 [点击打开二维码图片]({qr_img_url})",
        "（长按或保存图片后用米游社 App 扫码）",
        "",
        "📋 或复制以下链接在浏览器打开：",
        f"`{qr_url}`",
        "",
        "⏳ 扫码并确认后自动完成登录（最多等待 60 秒）",
    ]

    qr_msg = "\n".join(lines)

    # 后台轮询
    result = await _poll_qr_until_done(user_id, ticket, device, max_tries=60, interval=1)

    if result:
        return qr_msg + "\n\n" + result
    else:
        return qr_msg + "\n\n⏰ 等待超时，请重新发送「米游社登录」或使用其他方式"


async def _poll_qr_until_done(user_id: str, ticket: str, device: str,
                               max_tries: int = 60, interval: float = 1.0) -> Optional[str]:
    """
    后台轮询二维码状态
    """
    for _ in range(max_tries):
        await asyncio.sleep(interval)
        stat, raw = await query_qrcode(ticket, device)

        if stat == "Confirmed" and raw:
            uid = str(raw.get("uid", ""))
            game_token = raw.get("token", "")

            if not uid or not game_token:
                clear_login_session(user_id)
                return "❌ 登录数据异常，请重试"

            ok, cookies = await game_token_to_cookies(uid, game_token)
            if not ok or not cookies:
                clear_login_session(user_id)
                return "❌ Cookie 提取失败，请重试"

            return await _finish_login(user_id, uid, cookies)

        elif stat == "Expired":
            clear_login_session(user_id)
            return "❌ 二维码已过期，请重新发送「米游社登录」"

        elif stat == "error":
            return None

    clear_login_session(user_id)
    return None


async def cmd_qr_login_poll(user_id: str) -> str:
    """手动触发一次轮询"""
    session = get_login_session(user_id)
    if not session:
        return "❌ 没有进行中的登录会话，请重新发送「米游社登录」"

    stat, raw = await query_qrcode(session["ticket"], session.get("device", ""))

    if stat == "Init":
        return "⏳ 尚未扫码，请先用 App 扫描二维码"
    elif stat == "Scanned":
        return "📲 已扫码，请在 App 内点击「确认登录」"
    elif stat == "Expired":
        clear_login_session(user_id)
        return "❌ 二维码已过期，请重新发送「米游社登录」"
    elif stat == "Confirmed" and raw:
        uid = str(raw.get("uid", ""))
        game_token = raw.get("token", "")
        ok, cookies = await game_token_to_cookies(uid, game_token)
        if not ok or not cookies:
            clear_login_session(user_id)
            return "❌ Cookie 提取失败，请重试"
        return await _finish_login(user_id, uid, cookies)
    return "❌ 登录状态异常，请重新发送「米游社登录」"


async def cmd_stoken_qr_login(user_id: str) -> str:
    """
    扫码补全 stoken（用于 Cookie 登录后 stoken 缺失的情况）
    """
    accounts = get_user_accounts(user_id)
    if not accounts:
        return "❌ 未绑定任何账号，请先使用「米游社登录」绑定账号"

    # 找到缺少 stoken 的账号
    need_stoken = [a for a in accounts if not a.get("cookies", {}).get("stoken")]
    if not need_stoken:
        return "✅ 所有账号都已包含 stoken，无需补全"

    # 目前只支持补全第一个缺少 stoken 的账号
    target = need_stoken[0]
    uid = target["uid"]

    clear_login_session(user_id)

    ok, qr_url, ticket, device = await fetch_qrcode()
    if not ok:
        return "❌ 获取二维码失败"

    save_login_session(user_id, ticket, qr_url, device)
    # 标记这是 stoken 补全会话
    session = get_login_session(user_id)
    if session:
        session["mode"] = "stoken_patch"
        session["target_uid"] = uid
        save_login_session(user_id, ticket, qr_url, device)

    qr_img_url = qrcode_to_image_url(qr_url)

    return (
        f"📱 扫码补全 stoken — 账号 {target.get('nickname', uid)}\n"
        f"─" * 24 + "\n\n"
        f"🔗 [点击打开二维码]({qr_img_url})\n"
        f"用米游社App 扫码后，stoken 将自动补全到该账号\n\n"
        f"⏳ 等待扫码确认（最多 60 秒）..."
    )


async def cmd_bind(user_id: str, cookie_str: str) -> str:
    """
    Cookie 登录：解析 → 验证 → 获取游戏账号 → 保存
    如果缺少 stoken，提示用户扫码补全
    """
    cookies = parse_cookie_string(cookie_str)
    valid, msg = validate_cookies(cookies)
    if not valid:
        return f"❌ Cookie 无效\n{msg}"

    uid = extract_uid_from_cookies(cookies)
    if not uid:
        return "❌ 无法从 Cookie 中提取用户 ID，请确认 Cookie 完整"

    # 检查是否缺少 stoken
    if not cookies.get("stoken"):
        # 先保存当前 cookie，然后提示扫码补全
        result = await _finish_login(user_id, uid, cookies)
        return (
            result + "\n\n"
            "⚠️ 注意：当前 Cookie 缺少 stoken\n"
            "部分功能可能受限，建议发送「扫码补全stoken」进行补全"
        )

    return await _finish_login(user_id, uid, cookies)


async def _finish_login(user_id: str, uid: str, cookies: dict) -> str:
    """
    登录成功后：获取游戏账号、保存数据、返回成功消息
    使用 getUserGameRolesByCookie 逐游戏查询，确保 game_biz 正确
    """
    games = []
    biz_name = {
        "hk4e_cn": "原神",
        "hkrpg_cn": "星穹铁道",
        "bh3_cn": "崩坏3",
        "bh2_cn": "崩坏学园2",
        "nxx_cn": "未定事件簿",
        "nap_cn": "绝区零",
    }

    for biz, gname in biz_name.items():
        accounts = await get_account_list_by_game(cookies, biz)
        for acc in accounts:
            games.append({
                "game_biz": biz,
                "name": acc.get("nickname", gname),
                "game_uid": acc.get("game_uid", ""),
                "region": acc.get("region", ""),
                "level": 0,
            })

    nickname = games[0]["name"] if games else uid
    is_new = add_account(user_id, uid, nickname, cookies, games)
    clear_login_session(user_id)

    action = "绑定" if is_new else "更新"
    ck_fields = [k for k in cookies if k not in
                 ("account_id", "stuid", "ltuid", "login_uid",
                  "account_id_v2", "ltuid_v2")]
    total = len(get_user_accounts(user_id))

    lines = [
        f"✅ 登录成功，账号已{action}！",
        f"👤 昵称: {nickname}",
        f"🆔 米游社 UID: {uid}",
        f"🍪 Cookie: {', '.join(ck_fields) if ck_fields else '基础字段'}",
    ]
    if games:
        lines.append("🎮 游戏账号:")
        for g in games:
            biz = g.get("game_biz", "")
            gname = biz_name.get(biz, g.get("name", biz))
            lines.append(f"  • {gname}: UID {g['game_uid']}  Lv.{g['level']}")
    lines.append(f"\n📊 当前共绑定 {total} 个米游社账号")
    lines.append("发送「米游社账号」查看全部")

    if not cookies.get("stoken"):
        lines.append("\n⚠️ 缺少 stoken，建议发送「扫码补全stoken」进行补全")

    return "\n".join(lines)


async def cmd_daily_tasks(user_id: str) -> str:
    """执行每日米游币任务"""
    accounts = get_user_accounts(user_id)
    if not accounts:
        return "❌ 未绑定账号，请先发送「米游社登录」"

    all_results = []
    for acc in accounts:
        cookies = acc["cookies"]
        nickname = acc.get("nickname", acc["uid"])

        games = acc.get("games", [])
        game = "genshin"
        if games:
            biz = games[0].get("game_biz", "hk4e_cn")
            for k, v in GAME_BIZ.items():
                if v == biz:
                    game = k
                    break

        results = await do_bbs_tasks(cookies, game)
        all_results.append(format_task_result(results, nickname))

    return "\n\n".join(all_results)


# 根据 region 推断游戏类型
REGION_TO_GAME = {
    # 原神
    "cn_gf01": "genshin",
    "cn_qd01": "genshin",
    # 星穹铁道
    "prod_gf_cn": "starrail",
    "prod_qd_cn": "starrail",
    "hun02": "starrail",
    # 崩坏3
    "cn01": "honkai3",
    # 崩坏学园2
    "bh2_cn01": "honkai2",
    # 未定事件簿
    "nxx_cn01": "tearsofthemis",
    # 绝区零
    "nap_cn": "zzz",
    "nap_gf_cn": "zzz",
}


async def cmd_sign(user_id: str, target_game: Optional[str] = None) -> str:
    """
    执行游戏签到（仅国服）
    使用 getUserGameRolesByCookie API 逐游戏查询账号，解决 game_biz 为空导致漏签的问题
    """
    accounts = get_user_accounts(user_id)
    if not accounts:
        return "❌ 未绑定账号，请先发送「米游社登录」"

    # 确定要签到的游戏列表
    if target_game:
        games_to_sign = [target_game]
    else:
        games_to_sign = list(GAME_BIZ.keys())

    sign_results = []
    for acc in accounts:
        cookies = acc["cookies"]
        nickname = acc.get("nickname", acc["uid"])

        for game in games_to_sign:
            game_biz = GAME_BIZ.get(game)
            if not game_biz:
                continue

            # 用 game_biz 查询该游戏的账号列表
            game_accounts = await get_account_list_by_game(cookies, game_biz)

            if not game_accounts:
                # 没有该游戏账号，跳过
                continue

            for ga in game_accounts:
                uid = ga.get("game_uid", "")
                region = ga.get("region", "")
                acc_name = ga.get("nickname", nickname)

                if not uid:
                    continue

                ok, msg = await game_sign(cookies, game, region, uid=uid)
                sign_results.append({
                    "success": ok,
                    "msg": f"[{acc_name}] {msg}",
                })

    if not sign_results:
        return "❌ 未找到任何游戏账号，请重新登录绑定"

    return format_sign_results(sign_results)


async def cmd_note(user_id: str, game: str) -> str:
    """查询实时便笺"""
    accounts = get_user_accounts(user_id)
    if not accounts:
        return "❌ 未绑定账号，请先发送「米游社登录」"

    acc = accounts[0]
    cookies = acc["cookies"]
    nickname = acc.get("nickname", acc["uid"])

    # 用 getUserGameRolesByCookie 查找游戏 UID
    game_biz = GAME_BIZ.get(game, "")
    game_uid = None
    region = GAME_REGIONS.get(game, "cn_gf01")

    if game_biz:
        game_accounts = await get_account_list_by_game(cookies, game_biz)
        if game_accounts:
            ga = game_accounts[0]
            game_uid = ga.get("game_uid")
            region = ga.get("region") or region

    if not game_uid:
        return f"❌ 未找到 {SIGN_APIS.get(game, {}).get('name', game)} 的游戏账号"

    if game == "genshin":
        ok, data = await get_genshin_note(cookies, game_uid, region)
        if not ok or not data:
            return "❌ 获取原神便笺失败，请检查 Cookie 是否有效"
        return format_genshin_note(data, nickname)

    elif game == "starrail":
        ok, data = await get_starrail_note(cookies, game_uid, region)
        if not ok or not data:
            return "❌ 获取星穹铁道便笺失败，请检查 Cookie 是否有效"
        return format_starrail_note(data, nickname)

    return f"❌ 暂不支持 {game} 的便笺查询"


async def cmd_good_list(game: str = "") -> str:
    """查询米游币商品列表"""
    ok, goods = await get_good_list(game)
    if not ok or goods is None:
        return "❌ 获取商品列表失败，请稍后重试"
    return format_good_list(goods)


async def cmd_exchange(user_id: str, goods_id: str, num: int = 1) -> str:
    """兑换米游币商品"""
    accounts = get_user_accounts(user_id)
    if not accounts:
        return "❌ 未绑定账号，请先发送「米游社登录」"

    acc = accounts[0]
    cookies = acc["cookies"]
    games = acc.get("games", [])

    if not games:
        return "❌ 未找到游戏账号信息，请重新绑定"

    g = games[0]
    game_biz = g.get("game_biz", "hk4e_cn")
    game_uid = g.get("game_uid", "")
    region = g.get("region", "cn_gf01")

    # 获取地址列表
    ok_addr, addresses = await get_address_list(cookies)
    address_id = None
    if ok_addr and addresses:
        # 优先使用默认地址
        for addr in addresses:
            if addr.get("is_default"):
                address_id = addr.get("id")
                break
        # 没有默认地址则用第一个
        if not address_id and addresses:
            address_id = addresses[0].get("id")

    ok, msg, next_time = await do_exchange(
        cookies=cookies,
        goods_id=goods_id,
        uid=game_uid,
        region=region,
        game_biz=game_biz,
        address_id=address_id,
        num=num,
    )
    
    result = ("✅ " if ok else "❌ ") + msg
    
    # 库存不足时提示设置定时抢购
    if not ok and next_time and next_time > 0:
        from datetime import datetime
        next_dt = datetime.fromtimestamp(next_time)
        result += f"\n\n⏰ 下次补货时间: {next_dt.strftime('%Y-%m-%d %H:%M:%S')}"
        result += f"\n发送「预约兑换 {goods_id}」设置定时抢购"
    
    return result


# ── 帮助文本 ───────────────────────────────────────────────────────────────────

HELP_TEXT = """🎮 米游社工具 (mystool)
─────────────────────────
🔐 账号管理
  米游社登录            登录（短信/扫码/Cookie 三选一）✨
  扫码补全stoken        Cookie 登录后补全 stoken
  米游社账号            查看已绑定账号
  米游社解绑 [uid]      解绑账号

📅 每日任务
  米游社任务            执行米游币每日任务
  米游社签到            签到所有游戏

📊 游戏签到（国服）
  米游社签到 原神       原神签到
  米游社签到 星铁       星穹铁道签到
  米游社签到 崩3        崩坏3签到
  米游社签到 崩2        崩坏学园2签到
  米游社签到 未定       未定事件簿签到
  米游社签到 绝区零     绝区零签到

📋 实时便笺
  原神便笺              查看原神树脂等状态
  星铁便笺              查看星铁开拓力等状态

🛒 商品兑换
  米游币商品 [游戏]     查看商品列表
  米游社兑换 <ID> [数量] 兑换商品
  预约兑换 <商品ID>     预约定时抢购
  预约列表              查看全部预约
  取消预约 <商品ID>     取消预约

🔗 跨平台绑定
  生成识别码            获取跨平台绑定识别码
  链接账号 <识别码>     使用识别码链接账号

🔧 代理配置
  设置代理 <URL>        设置 IP 池代理地址
  查看代理              查看代理配置信息
─────────────────────────
定时任务每天 07:20 自动执行"""


# ── 预约兑换存储 ───────────────────────────────────────────────────────────────

EXCHANGE_SCHEDULES_FILE = Path(__file__).parent / "data" / "exchange_schedules.json"


def _load_exchange_schedules() -> Dict[str, List[dict]]:
    """加载预约兑换列表"""
    if not EXCHANGE_SCHEDULES_FILE.exists():
        return {}
    try:
        with open(EXCHANGE_SCHEDULES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_exchange_schedules(data: Dict[str, List[dict]]):
    """保存预约兑换列表"""
    EXCHANGE_SCHEDULES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(EXCHANGE_SCHEDULES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ── 代理配置指令 ───────────────────────────────────────────────────────────────

def cmd_set_proxy(url: str) -> str:
    """设置代理 API 地址"""
    import json
    from pathlib import Path
    
    config_file = Path(__file__).parent / "data" / "proxy_config.json"
    
    # 读取现有配置
    config = {}
    if config_file.exists():
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception:
            pass
    
    # 更新 API 地址
    config["api_url"] = url
    config["last_fetch_time"] = 0
    config["fetch_count_hour"] = 0
    config["hour_start"] = 0
    
    # 保存
    config_file.parent.mkdir(parents=True, exist_ok=True)
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    # 脱敏显示
    masked = url[:30] + "..." if len(url) > 30 else url
    return (
        f"✅ 代理地址已更新\n"
        f"────────────────────────\n"
        f"🔗 {masked}\n"
        f"📊 每小时限制: {config.get('max_per_hour', 20)} 次\n"
        f"⏳ 冷却时间: {config.get('cooldown_seconds', 30)} 秒"
    )


def cmd_show_proxy() -> str:
    """显示代理配置"""
    import json
    from pathlib import Path
    
    config_file = Path(__file__).parent / "data" / "proxy_config.json"
    
    if not config_file.exists():
        return "❌ 未配置代理\n发送「设置代理 <URL>」进行配置"
    
    try:
        with open(config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception:
        return "❌ 配置文件读取失败"
    
    api_url = config.get("api_url", "")
    if not api_url:
        return "❌ 未配置代理\n发送「设置代理 <URL>」进行配置"
    
    # 脱敏显示 URL
    masked = api_url[:30] + "..." if len(api_url) > 30 else api_url
    
    import time
    now = time.time()
    hour_start = config.get("hour_start", 0)
    fetch_count = config.get("fetch_count_hour", 0)
    max_per_hour = config.get("max_per_hour", 20)
    
    if now - hour_start > 3600:
        remaining = max_per_hour
    else:
        remaining = max_per_hour - fetch_count
    
    return (
        f"🔧 代理配置\n"
        f"────────────────────────\n"
        f"🔗 地址: {masked}\n"
        f"📊 本小时剩余: {remaining}/{max_per_hour} 次\n"
        f"⏳ 冷却时间: {config.get('cooldown_seconds', 30)} 秒"
    )


def cmd_generate_link_code(user_id: str) -> str:
    """生成跨平台绑定识别码"""
    accounts = get_user_accounts(user_id)
    if not accounts:
        return "❌ 你还没有绑定米游社账号\n请先发送「米游社登录」绑定账号"
    
    code = generate_link_code(user_id)
    
    return (
        "🔗 跨平台账号绑定\n"
        "────────────────────────\n"
        f"你的识别码: {code}\n"
        "────────────────────────\n"
        "📋 使用方法：\n"
        "1. 在另一个平台打开与我的对话\n"
        "2. 发送「链接账号 {识别码}」\n"
        "3. 自动共享米游社账号数据\n\n"
        "⚠️ 识别码有效期 10 分钟"
    )


async def cmd_link_account(user_id: str, code: str) -> str:
    """使用识别码链接账号"""
    if not code:
        return "❌ 请提供识别码\n格式：链接账号 XXXXXX"
    
    # 验证识别码
    source_user_id = verify_link_code(code)
    if not source_user_id:
        return "❌ 识别码无效或已过期\n请重新获取识别码"
    
    # 不能链接自己
    if source_user_id == user_id:
        return "❌ 不能链接自己账号"
    
    # 合并账号
    if merge_user_accounts(source_user_id, user_id):
        return (
            "✅ 账号链接成功！\n"
            "────────────────────────\n"
            "已共享米游社账号数据\n"
            "现在可以使用签到、便笺等功能了"
        )
    else:
        return "❌ 链接失败，原账号没有绑定米游社账号"


async def cmd_schedule_exchange(user_id: str, goods_id: str) -> str:
    """预约定时抢购"""
    accounts = get_user_accounts(user_id)
    if not accounts:
        return "❌ 未绑定账号，请先发送「米游社登录」"

    # 获取商品详情
    ok, detail = await get_good_detail(goods_id)
    if not ok or not detail:
        return f"❌ 获取商品 {goods_id} 详情失败"

    next_time = detail.get("next_time", 0)
    next_num = detail.get("next_num", 0)
    goods_name = detail.get("name") or detail.get("goods_name", "未知商品")

    if next_time <= 0:
        return f"❌ 商品「{goods_name}」暂无补货计划"

    from datetime import datetime
    next_dt = datetime.fromtimestamp(next_time)

    # 保存预约
    schedules = _load_exchange_schedules()
    user_schedules = schedules.setdefault(user_id, [])

    # 检查是否已预约
    for s in user_schedules:
        if s.get("goods_id") == goods_id:
            return f"❗ 已预约过此商品\n商品: {goods_name}\n时间: {next_dt.strftime('%Y-%m-%d %H:%M:%S')}"

    user_schedules.append({
        "goods_id": goods_id,
        "goods_name": goods_name,
        "next_time": next_time,
        "next_num": next_num,
        "created_at": time.time(),
    })
    _save_exchange_schedules(schedules)

    # 创建定时任务（使用 OpenClaw cron）
    # 这里先返回提示，实际 cron 任务需要通过 OpenClaw 的 cron 工具创建
    return (
        f"✅ 预约成功！\n"
        f"────────────────────────\n"
        f"🛒 商品: {goods_name}\n"
        f"📦 补货数量: {next_num}\n"
        f"⏰ 开抢时间: {next_dt.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"────────────────────────\n"
        f"💡 到时间会自动尝试兑换\n"
        f"发送「预约列表」查看全部预约"
    )


def cmd_list_scheduled_exchanges(user_id: str) -> str:
    """查看预约列表"""
    schedules = _load_exchange_schedules()
    user_schedules = schedules.get(user_id, [])

    if not user_schedules:
        return "📭 暂无预约兑换\n\n发送「预约兑换 <商品ID>」预约抢购"

    from datetime import datetime
    lines = ["📋 预约兑换列表", "─" * 24]

    for i, s in enumerate(user_schedules, 1):
        next_dt = datetime.fromtimestamp(s.get("next_time", 0))
        lines.append(f"\n{i}. {s.get('goods_name', '未知商品')}")
        lines.append(f"   ID: {s.get('goods_id')}")
        lines.append(f"   补货: {s.get('next_num', 0)} 件")
        lines.append(f"   时间: {next_dt.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"   取消: 取消预约 {s.get('goods_id')}")

    return "\n".join(lines)


def cmd_cancel_scheduled_exchange(user_id: str, goods_id: str) -> str:
    """取消预约"""
    schedules = _load_exchange_schedules()
    user_schedules = schedules.get(user_id, [])

    before = len(user_schedules)
    user_schedules[:] = [s for s in user_schedules if s.get("goods_id") != goods_id]

    if len(user_schedules) < before:
        schedules[user_id] = user_schedules
        _save_exchange_schedules(schedules)
        return f"✅ 已取消预约: {goods_id}"

    return f"❌ 未找到预约: {goods_id}"


# ── 定时任务入口（供 cron 调用）────────────────────────────────────────────────

async def run_daily_tasks_all() -> str:
    """对所有绑定用户执行每日任务（cron 调用），返回汇总结果。同账号去重。"""
    from store import load_accounts
    
    all_data = load_accounts()
    if not all_data:
        return "⚠️ 米游社每日任务：没有绑定账号的用户，跳过执行。"
    
    # 收集所有唯一的米游社账号（按 UID 去重）
    seen_uids = set()
    unique_accounts = []
    
    for user_id, user_data in all_data.items():
        for acc in user_data.get("accounts", []):
            uid = acc.get("uid", "")
            if uid and uid not in seen_uids:
                seen_uids.add(uid)
                unique_accounts.append(acc)
    
    if not unique_accounts:
        return "⚠️ 米游社每日任务：没有绑定账号的用户，跳过执行。"
    
    # 执行任务
    results = []
    for acc in unique_accounts:
        nickname = acc.get("nickname", acc["uid"])
        cookies = acc["cookies"]
        games = acc.get("games", [])
        
        # 选择游戏（默认用 games 列表中第一个 game_biz）
        game = "genshin"
        if games:
            biz = games[0].get("game_biz", "hk4e_cn")
            for k, v in GAME_BIZ.items():
                if v == biz:
                    game = k
                    break
        
        result = await do_bbs_tasks(cookies, game)
        results.append(format_task_result(result, nickname))
    
    return "\n\n".join(results)


async def run_sign_all() -> str:
    """对所有绑定用户执行游戏签到（cron 调用），返回汇总结果。同账号去重。"""
    from store import load_accounts
    
    all_data = load_accounts()
    if not all_data:
        return "⚠️ 米游社游戏签到：没有绑定账号的用户，跳过执行。"
    
    # 收集所有唯一的米游社账号（按 UID 去重）
    seen_uids = set()
    unique_accounts = []
    
    for user_id, user_data in all_data.items():
        for acc in user_data.get("accounts", []):
            uid = acc.get("uid", "")
            if uid and uid not in seen_uids:
                seen_uids.add(uid)
                unique_accounts.append(acc)
    
    if not unique_accounts:
        return "⚠️ 米游社游戏签到：没有绑定账号的用户，跳过执行。"
    
    # 执行签到
    results = []
    for acc in unique_accounts:
        nickname = acc.get("nickname", acc["uid"])
        cookies = acc["cookies"]
        
        # 遍历所有游戏签到
        for game, game_biz in GAME_BIZ.items():
            game_accounts = await get_account_list_by_game(cookies, game_biz)
            if not game_accounts:
                continue
            
            for ga in game_accounts:
                uid = ga.get("game_uid", "")
                region = ga.get("region", "")
                if not uid:
                    continue
                
                ok, msg = await game_sign(cookies, game, region, uid=uid)
                results.append({"success": ok, "msg": f"[{nickname}] {msg}"})
    
    return format_sign_results(results)


# ── CLI 入口（调试用）─────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    async def main():
        if len(sys.argv) < 2:
            print("用法: python plugin.py <指令>")
            print("示例: python plugin.py 米游社帮助")
            return
        msg = " ".join(sys.argv[1:])
        result = await handle(msg, user_id="cli_user")
        print(result or "(无响应)")

    asyncio.run(main())
