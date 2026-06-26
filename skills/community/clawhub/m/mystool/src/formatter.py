"""
消息格式化工具 — 将 API 数据转为可读文本
"""

from typing import Any, Dict, List, Optional


# ── 便笺格式化 ─────────────────────────────────────────────────────────────────

def format_genshin_note(data: Dict[str, Any], nickname: str = "") -> str:
    """格式化原神实时便笺"""
    lines = [f"📊 原神实时便笺" + (f" — {nickname}" if nickname else "")]
    lines.append("─" * 24)

    # 树脂
    resin = data.get("current_resin", 0)
    max_resin = data.get("max_resin", 160)
    resin_bar = _progress_bar(resin, max_resin)
    lines.append(f"🌙 原粹树脂: {resin}/{max_resin} {resin_bar}")
    if resin < max_resin:
        recovery_time = int(data.get("resin_recovery_time", 0))
        h, m = divmod(recovery_time // 60, 60)
        lines.append(f"   回满还需: {h}h {m}m")

    # 每日委托
    task_num = data.get("finished_task_num", 0)
    total_task = data.get("total_task_num", 4)
    lines.append(f"📋 每日委托: {task_num}/{total_task} {'✅' if task_num >= total_task else '⏳'}")

    # 周本折扣
    remain_resin_discount = data.get("remain_resin_discount_num", 0)
    resin_discount_limit = data.get("resin_discount_num_limit", 3)
    lines.append(f"🏆 周本折扣: 剩余 {remain_resin_discount}/{resin_discount_limit}")

    # 洞天宝钱
    home_coin = data.get("current_home_coin", 0)
    max_home_coin = data.get("max_home_coin", 2400)
    coin_bar = _progress_bar(home_coin, max_home_coin)
    lines.append(f"🏡 洞天宝钱: {home_coin}/{max_home_coin} {coin_bar}")

    # 探索派遣
    expeditions = data.get("expeditions", [])
    if expeditions:
        lines.append(f"🗺️ 探索派遣: {len(expeditions)} 人")
        for exp in expeditions:
            status = exp.get("status", "")
            remain = int(exp.get("remained_time", 0))
            if status == "Finished" or remain == 0:
                lines.append(f"   • 已完成 ✅")
            else:
                h, m = divmod(remain // 60, 60)
                lines.append(f"   • 剩余 {h}h {m}m")

    return "\n".join(lines)


def format_starrail_note(data: Dict[str, Any], nickname: str = "") -> str:
    """格式化星穹铁道实时便笺"""
    lines = [f"📊 星穹铁道便笺" + (f" — {nickname}" if nickname else "")]
    lines.append("─" * 24)

    # 开拓力
    power = data.get("current_stamina", 0)
    max_power = data.get("max_stamina", 240)
    power_bar = _progress_bar(power, max_power)
    lines.append(f"⚡ 开拓力: {power}/{max_power} {power_bar}")
    if power < max_power:
        recovery_time = int(data.get("stamina_recover_time", 0))
        h, m = divmod(recovery_time // 60, 60)
        lines.append(f"   回满还需: {h}h {m}m")

    # 后备开拓力
    reserve = data.get("current_reserve_stamina", 0)
    if reserve > 0:
        lines.append(f"🔋 后备开拓力: {reserve}")

    # 每日实训
    daily = data.get("current_train_score", 0)
    max_daily = data.get("max_train_score", 500)
    lines.append(f"📋 每日实训: {daily}/{max_daily} {'✅' if daily >= max_daily else '⏳'}")

    # 模拟宇宙
    rogue = data.get("current_rogue_score", 0)
    max_rogue = data.get("max_rogue_score", 14000)
    lines.append(f"🌌 模拟宇宙: {rogue}/{max_rogue}")

    # 派遣
    expeditions = data.get("expeditions", [])
    if expeditions:
        lines.append(f"🗺️ 委托派遣: {len(expeditions)} 人")
        for exp in expeditions:
            remain = int(exp.get("remaining_time", 0))
            name = exp.get("name", "未知")
            if remain == 0:
                lines.append(f"   • {name} ✅")
            else:
                h, m = divmod(remain // 60, 60)
                lines.append(f"   • {name} 剩余 {h}h {m}m")

    return "\n".join(lines)


# ── 任务结果格式化 ─────────────────────────────────────────────────────────────

def format_task_result(results: Dict[str, Any], nickname: str = "") -> str:
    """格式化米游币任务执行结果"""
    lines = [f"🪙 米游币任务" + (f" — {nickname}" if nickname else "")]
    lines.append("─" * 24)

    task_map = {
        "sign": ("📍 论坛打卡", 1),
        "view": ("📖 浏览帖子", 3),
        "like": ("👍 点赞帖子", 5),
        "share": ("🔗 分享帖子", 1),
    }
    total_myb = 0
    coins_data = results.get("coins", {})
    remaining_coins = coins_data.get("remaining", 0)
    
    for key, (label, max_count) in task_map.items():
        r = results.get(key, {})
        done = r.get("done", 0)
        success = r.get("success", False)
        icon = "✅" if success else "❌"
        lines.append(f"{icon} {label}: {done}/{max_count}")
        if success:
            total_myb += done  # 每次任务约得 1 米游币
        # 显示错误信息
        if not success and "errors" in r:
            for err in r["errors"]:
                lines.append(f"   ⚠️ {err[:60]}")
        if not success and "error" in r:
            lines.append(f"   ⚠️ {r['error'][:60]}")

    # 优先使用 API 返回的米游币数量
    if remaining_coins > 0:
        lines.append(f"\n预计获得米游币: +{remaining_coins}")
    else:
        lines.append(f"\n预计获得米游币: +{total_myb}")
    return "\n".join(lines)


def format_sign_results(results: List[Dict[str, Any]]) -> str:
    """格式化多游戏签到结果"""
    lines = ["🗓️ 游戏签到结果"]
    lines.append("─" * 24)
    for r in results:
        icon = "✅" if r["success"] else "❌"
        lines.append(f"{icon} {r['msg']}")
    return "\n".join(lines)


def format_account_list(accounts: List[dict]) -> str:
    """
    格式化账号列表，依次展示每个米游社账号的详细信息。
    """
    if not accounts:
        return (
            "📭 未绑定任何米游社账号\n\n"
            "发送「米游社登录」绑定账号"
        )

    total = len(accounts)
    lines = [f"🔐 已绑定 {total} 个米游社账号\n"]

    for i, acc in enumerate(accounts, 1):
        uid = acc.get("uid", "?")
        nickname = acc.get("nickname", "未知")
        games = acc.get("games", [])
        cookies = acc.get("cookies", {})

        # Cookie 有效字段
        ck_fields = [k for k in cookies if k not in
                     ("account_id", "stuid", "ltuid", "login_uid",
                      "account_id_v2", "ltuid_v2")]
        ck_status = "✅ 完整" if ("stoken" in cookies or "cookie_token" in cookies) else "⚠️ 不完整"

        lines.append(f"{'─' * 24}")
        lines.append(f"账号 {i}/{total}")
        lines.append(f"👤 昵称: {nickname}")
        lines.append(f"🆔 米游社 UID: {uid}")
        lines.append(f"🍪 Cookie: {ck_status} ({', '.join(ck_fields) if ck_fields else '无'})")

        if games:
            lines.append(f"🎮 游戏账号 ({len(games)} 个):")
            # 游戏名映射
            biz_name = {
                "hk4e_cn": "原神",
                "hkrpg_cn": "星穹铁道",
                "bh3_cn": "崩坏3",
                "nap_cn": "绝区零",
                "hk4e_global": "原神(国际)",
                "hkrpg_global": "星铁(国际)",
            }
            for g in games:
                biz = g.get("game_biz", "")
                gname = biz_name.get(biz, g.get("name", biz or "未知"))
                gid = g.get("game_uid", "?")
                lv = g.get("level", 0)
                region = g.get("region", "")
                region_str = f" | {region}" if region else ""
                lines.append(f"  • {gname}: UID {gid}  Lv.{lv}{region_str}")
        else:
            lines.append("🎮 游戏账号: 未获取（可重新登录刷新）")

        lines.append(f"🗑 解绑: 发送「米游社解绑 {uid}」")

    lines.append("─" * 24)
    return "\n".join(lines)


def format_good_list(goods: List[dict]) -> str:
    """格式化商品列表"""
    if not goods:
        return "暂无可兑换商品"

    lines = ["🛒 米游币商品列表"]
    lines.append("─" * 24)
    for g in goods[:15]:  # 最多显示15个
        name = g.get("goods_name", "未知")
        price = g.get("price", 0)
        stock = g.get("unlimit", False)
        gid = g.get("goods_id", "")
        stock_str = "不限量" if stock else f"库存: {g.get('next_num', 0)}"
        lines.append(f"• {name}")
        lines.append(f"  💰 {price} 米游币 | {stock_str}")
        lines.append(f"  ID: `{gid}`")
    return "\n".join(lines)


# ── 工具函数 ───────────────────────────────────────────────────────────────────

def _progress_bar(current: int, maximum: int, length: int = 10) -> str:
    """生成文字进度条"""
    if maximum == 0:
        return "░" * length
    filled = int(current / maximum * length)
    return "█" * filled + "░" * (length - filled)
