#!/usr/bin/env python3
"""
Kimi 额度自动抓取 - 带 cookie + localStorage 持久化
套路：加载 cookies + 设置 localStorage access_token → 访问 subscription 页 → 抓额度

使用前请按 SKILL.md 配置说明填入你自己的认证信息。
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from playwright.async_api import async_playwright

# ==========================
# ⚠️ 用户配置区 — 使用前必须修改
# ==========================

# 1. Cookies 文件路径：将 Kimi 登录 cookies 导出为 JSON 放在此路径
#    格式：Playwright cookies 数组 [{name, value, domain, path}, ...]
COOKIES_FILE = Path("kimi_cookies.json")

# 2. 微信推送目标 ID（openclaw-weixin 通道）
#    获取方式：openclaw message list-accounts --channel openclaw-weixin
TARGET_ID = "YOUR_WECHAT_ID@im.wechat"

# 3. Kimi localStorage 认证数据
#    从浏览器开发者工具 → Application → Local Storage 复制
LS_DATA = {
    "access_token": "YOUR_ACCESS_TOKEN",
    "refresh_token": "YOUR_REFRESH_TOKEN",
    "msh_user_id": "YOUR_MSH_USER_ID",
    "msh_user_subscription_data": '{"currentMembershipLevel":25}',
}

# ==========================
# 以下为通用逻辑，通常无需修改
# ==========================

MONITOR_URL = "https://www.kimi.com/membership/subscription"


def wechat_push(message: str):
    """推送消息到微信（通过 openclaw CLI）"""
    import subprocess
    cmd = [
        "openclaw", "message", "send",
        "--channel", "openclaw-weixin",
        "--target", TARGET_ID,
        "--message", message,
    ]
    try:
        subprocess.run(cmd, capture_output=True, timeout=30)
    except Exception as e:
        print(f"[ERROR] Push failed: {e}")


def get_cycle_info(today: datetime):
    """获取当前额度周期信息（默认每月22日重置）"""
    year, month, day = today.year, today.month, today.day

    # 确定周期起止
    if day >= 22:
        cycle_start = datetime(year, month, 22)
        if month == 12:
            cycle_end = datetime(year + 1, 1, 21)
        else:
            cycle_end = datetime(year, month + 1, 21)
    else:
        if month == 1:
            cycle_start = datetime(year - 1, 12, 22)
        else:
            cycle_start = datetime(year, month - 1, 22)
        cycle_end = datetime(year, month, 21)

    cycle_days = (cycle_end - cycle_start).days + 1
    days_passed = (today - cycle_start).days + 1

    return cycle_start, cycle_end, cycle_days, days_passed


def save_cookies(cookies: list):
    with open(COOKIES_FILE, "w") as f:
        json.dump(cookies, f, indent=2)
    print(f"[INFO] Cookies saved to {COOKIES_FILE}")


def load_cookies() -> list:
    if not COOKIES_FILE.exists():
        return []
    try:
        with open(COOKIES_FILE) as f:
            cookies = json.load(f)
        print(f"[INFO] Loaded {len(cookies)} cookies")
        return cookies
    except Exception as e:
        print(f"[ERROR] Failed to load cookies: {e}")
        return []


async def fetch_quota(playwright) -> dict:
    browser = await playwright.chromium.launch(headless=True, channel="chrome")
    context = await browser.new_context(
        viewport={"width": 1280, "height": 800},
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    )

    # 加载 cookies
    cookies = load_cookies()
    if cookies:
        await context.add_cookies(cookies)
        print("[INFO] Cookies injected into browser context")

    page = await context.new_page()

    try:
        # Step 1: 访问主站，让 sameSite=Strict cookie 生效
        print("[INFO] Visiting www.kimi.com to warm up cookies...")
        await page.goto("https://www.kimi.com/", wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(2)

        # Step 2: 注入 localStorage 认证数据
        print("[INFO] Injecting localStorage auth data...")
        for key, value in LS_DATA.items():
            await page.evaluate(f"localStorage.setItem('{key}', '{value}')")
        print("[INFO] localStorage injected")

        # Step 3: 刷新页面，让前端读取 localStorage 识别登录态
        print("[INFO] Refreshing page to activate auth state...")
        await page.reload(wait_until="domcontentloaded")
        await asyncio.sleep(3)

        # Step 4: 访问 subscription 页面
        print(f"[INFO] Navigating to {MONITOR_URL}")
        await page.goto(MONITOR_URL, wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(2)

        body_text = await page.evaluate("() => document.body.innerText")
        print(f"[DEBUG] Page body preview: {body_text[:300]}")

        # 检查是否已登录（页面显示套餐名或订阅相关字样）
        if "订阅" not in body_text and "subscription" not in body_text.lower():
            print("[WARN] Not logged in or cookies expired")
            await browser.close()
            return {"need_login": True}
        print("[INFO] Auth state confirmed")

        # 提取额度 - 用 DOM selector 精确抓取
        usage_pct = await page.evaluate(r"""() => {
            const el = document.querySelector('.usage-title');
            if (el) {
                const m = el.textContent.match(/(\d+\.?\d*)%/);
                return m ? parseFloat(m[1]) : null;
            }
            // 备选：搜索包含 % 的元素
            const els = [...document.querySelectorAll('*')];
            const usageEl = els.find(e => {
                const t = e.textContent;
                return t && /\d+\.\d+%/.test(t) && e.className && e.className.includes('usage');
            });
            if (usageEl) {
                const m = usageEl.textContent.match(/(\d+\.?\d*)%/);
                return m ? parseFloat(m[1]) : null;
            }
            return null;
        }""")

        # 提取重置日期
        reset_date = await page.evaluate(r"""() => {
            const els = [...document.querySelectorAll('*')];
            const el = els.find(e => {
                const t = e.textContent;
                return t && t.includes('Reset time') && /\d{4}-\d{2}-\d{2}/.test(t);
            });
            if (el) {
                const m = el.textContent.match(/(\d{4}-\d{2}-\d{2})/);
                return m ? m[1] : null;
            }
            return null;
        }""")

        # 保存刷新后的 cookie（延长有效期）
        new_cookies = await context.cookies()
        save_cookies(new_cookies)

        await browser.close()
        print("[INFO] Browser closed")

        if usage_pct is not None:
            return {
                "usage_pct": usage_pct,
                "remaining_pct": round(100 - usage_pct, 2),
                "reset_date": reset_date or "",
            }
        else:
            return {"error": "Could not parse quota from page"}

    except Exception as e:
        print(f"[ERROR] During fetch: {e}")
        await browser.close()
        return {"error": str(e)}


async def main():
    print(f"\n{'='*50}")
    print(f"Kimi Quota Fetcher - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")

    async with async_playwright() as playwright:
        result = await fetch_quota(playwright)

    if result is None:
        print("[ERROR] No result returned")
        return 1

    if result.get("need_login"):
        msg = (
            "⚠️ Kimi 额度监控\n"
            "登录态已过期，需要重新配置认证信息。\n"
            "请检查 cookies 和 localStorage token 是否有效。"
        )
        wechat_push(msg)
        print("[INFO] Login needed notification pushed to WeChat")
        return 2

    if "error" in result:
        print(f"[ERROR] {result['error']}")
        wechat_push(f"❌ Kimi 额度抓取失败：{result['error']}")
        return 1

    # 获取额度数据
    usage_pct = result["usage_pct"]
    remaining_pct = result["remaining_pct"]
    reset_date_str = result.get("reset_date", "")

    # 周期计算
    now = datetime.now()
    today = datetime(now.year, now.month, now.day)
    cycle_start, cycle_end, cycle_days, days_passed = get_cycle_info(today)
    days_remaining = cycle_days - days_passed

    start_str = cycle_start.strftime("%m.%d")
    end_str = cycle_end.strftime("%m.%d")

    # 计划用量 = 按周期均摊
    daily_plan = 100.0 / cycle_days
    planned_used = daily_plan * days_passed
    raw_balance = planned_used - usage_pct  # 原始差额（计划 - 实际）

    # KimiClaw预估 = 剩余天数 × 0.6%/天
    projected_extra = days_remaining * 0.6

    # 抵扣逻辑：KimiClaw预估先抵扣差额
    display_balance = max(raw_balance - projected_extra, 0)
    net_kimiclaw_extra = max(projected_extra - raw_balance, 0)
    if net_kimiclaw_extra <= 0:
        net_kimiclaw_extra = None

    # 进度条
    projected_total = usage_pct + (net_kimiclaw_extra or 0)
    projected_total = min(projected_total, 100.0)

    bar_filled = int((projected_total / 100.0) * 10)
    bar = "█" * bar_filled + "░" * (10 - bar_filled)

    today_str = today.strftime("%m.%d")

    # 组装消息
    msg_lines = [
        f"📊 Kimi 额度日报 · {today_str}",
        "",
        f"周期：{start_str} – {end_str}（共{cycle_days}天）",
        f"进度：{bar} {projected_total:.1f}%",
        "",
        "📌 截止今日：",
        f"   累计计划：{planned_used:.2f}%",
        f"   累计实际：{usage_pct:.2f}%",
        f"   差   额：+{display_balance:.2f}%",
    ]

    if net_kimiclaw_extra is not None:
        msg_lines.append(f"   KimiClaw预估：+{net_kimiclaw_extra:.1f}%")

    msg_lines.append("")
    msg_lines.append(f"💰 剩余总额度：{remaining_pct:.2f}%")

    msg = "\n".join(msg_lines)

    wechat_push(msg)
    print(f"[INFO] Quota pushed: used={usage_pct}%, remaining={remaining_pct}%")
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
