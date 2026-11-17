#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
# ⚠️ 本文件是「京东黄金 (jdgold)」JoyCode Skill 的组成脚本。
# 执行任何脚本前，必须先阅读 Skill 根目录下的 SKILL.md，
# 严格遵循其中的执行契约、安全脱敏铁律与回复规范，
# 请勿脱离 SKILL.md 指引单独运行本脚本。
# ============================================================
"""京东黄金 · 模拟交易全权托管脚本（本地定时轮询）。

定位：由 macOS launchd（或 cron）每隔 N 分钟唤起一次，单次执行完整的
「判登录 → 拉行情 → 算买卖点 → 风控校验 → 下单 → 写日志 → 通知」闭环。
仅操作模拟金叶子，不涉及真实资金。

⚠️ 重要外部条件（脚本内置对应处理）：
  1. 登录授权会过期，且后端 /oauth/refresh 未上线 → 过期即停 + 通知，需人工重登。
  2. 关机 / 电池睡眠会让 launchd 暂停 → 醒来后补跑。
  3. 退出 AI 软件不影响本脚本（launchd 是独立系统服务）。

claw 参数：--claw 为必传启动参数，标识调用方客户端类型（codex/openclaw/joycode
等），每次调底层脚本都透传，随 x-claw 请求头上传服务端。

用法：
    python3 sim_autotrade.py --claw <client> [--daily-cap <金叶子数>]
                             [--poll-min 30] [--cooldown-min 60] [--dry-run]

风控（通用默认，所有用户一致）：
  - 总托管上限 = 账户可用余额，花完即停；
  - 单日上限：--daily-cap 可选，不设则一直托管到余额花完或用户叫停；
  - 冷却期：两次下单间隔 >= --cooldown-min（默认 60 分钟）；
  - token 过期 / 接口失败 / 余额不足：立即停 + 通知，绝不静默。
"""

import os
import sys
import json
import time
import argparse
import subprocess
from datetime import datetime, date

# ── 路径与常量 ──────────────────────────────────────────────────────
HERE = os.path.dirname(os.path.abspath(__file__))
JOS = os.path.join(HERE, "jos.py")
SIM = os.path.join(HERE, "query_sim_contest.py")
PROJECT_DIR = os.path.abspath(os.path.join(HERE, ".."))

# launchd 模板：上传限制导致包内以 .plist.txt 结尾，安装时自动兼容两种命名
PLIST_TPL_TXT = os.path.join(HERE, "autotrade.launchd.plist.txt")
PLIST_TPL_RAW = os.path.join(HERE, "autotrade.launchd.plist")
PLIST_LABEL = "com.jdgold.autotrade"
PLIST_TARGET = os.path.expanduser(
    f"~/Library/LaunchAgents/{PLIST_LABEL}.plist")

# 标的：京东 24h 金价指数（默认，见 references/price-uniquecode-enum.md）
UNIQUE_CODE = "WG-JDAU"

# 日志与状态文件（本地，不入库）
LOG_DIR = os.path.join(HERE, "..", ".joycode", "autotrade")
LOG_FILE = os.path.join(LOG_DIR, "autotrade.log")
STATE_FILE = os.path.join(LOG_DIR, "state.json")


# ── 基础工具 ────────────────────────────────────────────────────────
def _ensure_log_dir():
    try:
        os.makedirs(LOG_DIR, exist_ok=True)
    except Exception:
        pass


def log(msg, level="INFO"):
    """写本地日志 + 打印（供 launchd 捕获），带时间戳。"""
    _ensure_log_dir()
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [{level}] {msg}"
    print(line, flush=True)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def notify(title, msg):
    """通知用户：优先 macOS 系统通知，失败则退回日志。禁止静默。"""
    log(f"通知用户：{title} — {msg}", level="NOTIFY")
    try:
        safe_t = title.replace('"', "'")
        safe_m = msg.replace('"', "'")
        subprocess.run(
            ["osascript", "-e",
             f'display notification "{safe_m}" with title "{safe_t}"'],
            timeout=5, check=False,
        )
    except Exception:
        pass  # 无 GUI（如纯 CLI/远程）时静默降级，日志已记录


def load_state():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_state(state):
    _ensure_log_dir()
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    except Exception as e:
        log(f"状态写入失败：{e}", level="WARN")


# ── 底层脚本调用（统一透传 --claw --json） ──────────────────────────
def _run_sim(claw, sub_args):
    """调 query_sim_contest.py，--claw/--json 为全局参数须放子命令前。

    返回 (returncode, parsed_json_or_None, stderr_text)。
    """
    cmd = [sys.executable, SIM, "--claw", claw, "--json"] + sub_args
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    except Exception as e:
        return 1, None, f"子进程异常：{e}"
    data = _parse_json_out(r.stdout)
    return r.returncode, data, r.stderr.strip()


def _parse_json_out(out):
    """从子进程 stdout 解析 JSON。

    query_sim_contest.py --json 输出的是多行缩进 JSON，不能只取最后一行。
    优先整体解析；失败再从末尾向前逐段尝试，兼容前面掺杂日志行的情况。
    """
    text = (out or "").strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except Exception:
        pass
    lines = text.splitlines()
    # 从最后一个以 } 或 ] 结尾的位置向前扩展，找出��大可解析的 JSON 块
    for start in range(len(lines)):
        chunk = "\n".join(lines[start:]).strip()
        if not chunk or chunk[0] not in "{[":
            continue
        try:
            return json.loads(chunk)
        except Exception:
            continue
    return None


def _check_login(claw):
    """判登录态并取剩余有效期。返回 (logged_in, remaining_human)。"""
    cmd = [sys.executable, JOS, "token", "--claw", claw, "--json"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    except Exception as e:
        return False, f"检查失败：{e}"
    info = _parse_json_out(r.stdout) or {}
    return bool(info.get("logged_in")), info.get("remaining_human", "未知")


# ── 行情与策略 ──────────────────────────────────────────────────────
def _fetch_market(claw):
    """拉近 10 日 K 线 + 今日实时分时，返回策略所需的价格特征。

    返回 dict：{last, day_high, day_low, today_open, today_high, today_low}
    任一环节失败返回 None。
    """
    rc, kl, err = _run_sim(claw, ["kline", "--unique-code", UNIQUE_CODE,
                                  "--k-type", "day", "--nums", "10"])
    if rc != 0 or not kl:
        log(f"拉 K 线失败：rc={rc} {err}", level="WARN")
        return None
    items = _extract_items(kl)
    if not items:
        return None
    highs = [_f(x.get("highPrice")) for x in items if _f(x.get("highPrice"))]
    lows = [_f(x.get("lowPrice")) for x in items if _f(x.get("lowPrice"))]
    if not highs or not lows:
        return None
    day_high, day_low = max(highs), min(lows)

    # 今日实时分时（可选）：预发/非交易时段可能返回空，缺失时回退用最近 K 线收盘价
    rc, ts, err = _run_sim(claw, ["time-sharing", "--unique-code", UNIQUE_CODE,
                                  "--type", "m5"])
    prices = []
    if rc == 0 and ts:
        titems = _extract_items(ts)
        prices = [_f(x.get("lastPrice")) for x in titems if _f(x.get("lastPrice"))]
    if not prices:
        last_close = _f(items[-1].get("closePrice"))
        if not last_close:
            log("分时无数据且无法回退收盘价，本轮跳过", level="WARN")
            return None
        log("分时无数据，回退使用最近 K 线收盘价", level="INFO")
        return {
            "last": last_close,
            "day_high": day_high,
            "day_low": day_low,
            "today_open": last_close,
            "today_high": last_close,
            "today_low": last_close,
        }
    return {
        "last": prices[-1],
        "day_high": day_high,
        "day_low":day_low,
        "today_open": prices[0],
        "today_high": max(prices),
        "today_low": min(prices),
    }


def _extract_items(data):
    """从底层 JSON 里尽力取出 items 列表（兼容多层包裹）。"""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for k in ("items", "data", "result", "list"):
            v = data.get(k)
            if isinstance(v, list):
                return v
            if isinstance(v, dict):
                inner = _extract_items(v)
                if inner:
                    return inner
    return []


def _f(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def decide(mkt):
    """按「近10日 + 今日实时结合」给出信号。

    策略（低位分批建仓、高位分批止盈）：
      - 当前价接近近10日低点（<= 低点 + 区间 20%）→ 买入信号；
      - 当前价接近近10日高点（>= 高点 - 区间 20%）→ 卖出信号；
      - 其余观望。
    返回 ("buy"|"sell"|"hold", reason)。
    """
    last, hi, lo = mkt["last"], mkt["day_high"], mkt["day_low"]
    band = hi - lo
    if band <= 0:
        return "hold", "近10日无有效波动区间"
    buy_line = lo + band * 0.20
    sell_line = hi - band * 0.20
    if last <= buy_line:
        return "buy", f"当前 {last:.2f} 触及近10日低区（<= {buy_line:.2f}）"
    if last >= sell_line:
        return "sell", f"当前 {last:.2f} 触及近10日高区（>= {sell_line:.2f}）"
    return "hold", f"当前 {last:.2f} 处于中位（{buy_line:.2f}~{sell_line:.2f}），观望"


# ── 账户与下单 ──────────────────────────────────────────────────────
def _fetch_account(claw):
    """查模拟账户，返回 dict 或 None。"""
    rc, data, err = _run_sim(claw, ["account"])
    if rc != 0 or not data:
        log(f"查账户失败：rc={rc} {err}", level="WARN")
        return None
    acc = data
    if isinstance(data, dict):
        for k in ("data", "result"):
            if isinstance(data.get(k), dict):
                acc = data[k]
                break
    return acc


def _place_order(claw, side, amount_or_gram, bus_id, dry_run):
    """下单：side=buy 按金额（trade-unit 1）；side=sell 按比例（trade-unit 3）。

    返回 (ok, feedback_text)。
    """
    if side == "buy":
        args = ["buy", "--trade-unit", "1", "--bus-id", bus_id,
                "--trade-amount", str(amount_or_gram)]
    else:
        args = ["sell", "--trade-unit", "3", "--bus-id", bus_id,
                "--trade-ratio", str(amount_or_gram)]
    if dry_run:
        log(f"[DRY-RUN] 跳过实际下单：{side} {args}", level="INFO")
        return True, "（演练模式，未真实下单）"
    rc, data, err = _run_sim(claw, args)
    if rc != 0 or not data:
        return False, err or "下单接口无返回"
    desc = ""
    if isinstance(data, dict):
        body = data.get("data") if isinstance(data.get("data"), dict) else data
        desc = (body.get("tradeAmountAndGramDesc") or "") + " " + \
               (body.get("tradePriceDesc") or "")
    return True, desc.strip() or "已提交"


# ── 主流程（单次执行） ──────────────────────────────────────────────
def run_once(claw, daily_cap, cooldown_min, dry_run):
    log(f"===== 托管轮询开始（claw={claw}, dry_run={dry_run}）=====")

    # 1) 判登录态 + 剩余有效期
    logged_in, remaining = _check_login(claw)
    if not logged_in:
        notify("黄金托管已停止", "登录授权已过期，需重新登录（开浏览器授权）后才能继续托管。")
        log("登录已过期/未登录，停止本轮。", level="STOP")
        return 2
    log(f"登录有效，授权还能托管 {remaining}。")

    # 2) 拉行情算信号
    mkt = _fetch_market(claw)
    if not mkt:
        notify("黄金托管暂跳过", "行情获取失败，本轮不交易，下轮重试。")
        return 1
    side, reason = decide(mkt)
    log(f"策略信号：{side} —— {reason}")
    if side == "hold":
        log("未达交易条件，观望。")
        return 0

    # 3) 冷却期校验
    state = load_state()
    now = time.time()
    last_ts = float(state.get("last_trade_ts", 0))
    if now - last_ts < cooldown_min * 60:
        left = int((cooldown_min * 60 - (now - last_ts)) / 60)
        log(f"冷却期内（还剩约 {left} 分钟），本轮不交易。")
        return 0

    # 4) 查账户 → 总上限（=可用余额）与单日上限校验
    acc = _fetch_account(claw)
    if not acc:
        notify("黄金托管暂跳过", "账户查询失败，本轮不交易。")
        return 1
    available = _f(acc.get("availableAmount")) or 0.0
    today = date.today().isoformat()
    if state.get("day") != today:
        state["day"] = today
        state["day_spent"] = 0.0
    day_spent = float(state.get("day_spent", 0))

    if side == "buy":
        if available <= 0:
            notify("黄金托管已停止", "账户余额已花完，托管自动停止。")
            log("余额耗尽，停止托管。", level="STOP")
            save_state(state)
            return 2
        # 单笔金额：可用余额的 20%，且受单日上限约束
        amount = round(available * 0.20, 2)
        if daily_cap is not None:
            remain_cap = daily_cap - day_spent
            if remain_cap <= 0:
                log(f"已达单日上限 {daily_cap}，暂停到次日。")
                save_state(state)
                return 0
            amount = min(amount, remain_cap)
        amount = min(amount, available)
        if amount < 1:
            log("可下单金额过小（<1），跳过。")
            save_state(state)
            return 0
        bus_id = f"AT-{claw}-{int(now)}"
        ok, fb = _place_order(claw, "buy", amount, bus_id, dry_run)
        if ok:
            state["last_trade_ts"] = now
            state["day_spent"] = day_spent + amount
            save_state(state)
            notify("黄金托管已买入",
                   f"买入 {amount} 元金叶子（{reason}）。{fb}")
            log(f"买入成功：{amount} 元。{fb}", level="TRADE")
        else:
            notify("黄金托管买入失败", f"原因：{fb}")
            log(f"买入失败：{fb}", level="ERROR")
        return 0

    # side == "sell"：按 20% 比例分批止盈
    holding = _f(acc.get("currentHoldingGram")) or 0.0
    if holding <= 0:
        log("无持仓，无法卖出，跳过。")
        save_state(state)
        return 0
    ratio = 0.20
    bus_id = f"AT-{claw}-{int(now)}"
    ok, fb = _place_order(claw, "sell", ratio, bus_id, dry_run)
    if ok:
        state["last_trade_ts"] = now
        save_state(state)
        notify("黄金托管已卖出",
               f"卖出 {int(ratio*100)}% 持仓止盈（{reason}）。{fb}")
        log(f"卖出成功：{ratio} 比例。{fb}", level="TRADE")
    else:
        notify("黄金托管卖出失败", f"原因：{fb}")
        log(f"卖出失败：{fb}", level="ERROR")
    return 0


def install_launchd(claw, daily_cap=None):
    """自动生成并加载 launchd 定时任务。

    - 兼容模板命名：优先读 .plist.txt（上传限制），退回 .plist。
    - 替换占位符 __PYTHON__ / __PROJECT_DIR__ / __CLAW__。
    - 传入 daily_cap 时向 ProgramArguments 注入 --daily-cap。
    - 写入 ~/Library/LaunchAgents/ 后 launchctl load。
    用户/AI 无需手动改名或替换任何东西。
    """
    tpl_path = PLIST_TPL_TXT if os.path.exists(PLIST_TPL_TXT) else PLIST_TPL_RAW
    if not os.path.exists(tpl_path):
        notify("黄金托管安装失败", "找不到 launchd 模板文件")
        log(f"模板不存在：{PLIST_TPL_TXT} / {PLIST_TPL_RAW}", level="ERROR")
        return 1

    with open(tpl_path, "r", encoding="utf-8") as f:
        content = f.read()

    content = (content
               .replace("__PYTHON__", sys.executable)
               .replace("__PROJECT_DIR__", PROJECT_DIR)
               .replace("__CLAW__", claw))

    # 可选：注入单日上限参数（紧跟 --claw 之后）
    if daily_cap is not None:
        inject = (f"        <string>--claw</string>\n"
                  f"        <string>{claw}</string>\n"
                  f"        <string>--daily-cap</string>\n"
                  f"        <string>{daily_cap}</string>")
        content = content.replace(
            f"        <string>--claw</string>\n        <string>{claw}</string>",
            inject)

    try:
        os.makedirs(os.path.dirname(PLIST_TARGET), exist_ok=True)
        os.makedirs(LOG_DIR, exist_ok=True)
        with open(PLIST_TARGET, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        notify("黄金托管安装失败", f"写入 plist 失败：{e}")
        log(f"写入 {PLIST_TARGET} 失败：{e}", level="ERROR")
        return 1

    # 先 unload（幂等），再 load
    subprocess.run(["launchctl", "unload", PLIST_TARGET],
                   check=False, capture_output=True)
    r = subprocess.run(["launchctl", "load", PLIST_TARGET],
                       check=False, capture_output=True, text=True)
    if r.returncode != 0:
        notify("黄金托管启动失败", r.stderr.strip() or "launchctl load 失败")
        log(f"launchctl load 失败：{r.stderr.strip()}", level="ERROR")
        return 1

    cap_txt = f"，单日上限 {daily_cap}" if daily_cap is not None else "，不限单日额度"
    notify("黄金托管已启动", f"每 30 分钟自动轮询{cap_txt}")
    log(f"launchd 已加载：{PLIST_TARGET}（claw={claw}{cap_txt}）", level="INFO")
    return 0


def uninstall_launchd():
    """停止并卸载 launchd 定时任务。"""
    if not os.path.exists(PLIST_TARGET):
        log(f"未发现已安装的任务：{PLIST_TARGET}", level="INFO")
        return 0
    subprocess.run(["launchctl", "unload", PLIST_TARGET],
                   check=False, capture_output=True)
    notify("黄金托管已停止", "launchd 定时任务已卸载")
    log(f"launchd 已卸载：{PLIST_TARGET}", level="INFO")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description="京东黄金模拟交易全权托管（本地定时轮询）")
    p.add_argument("--claw", required=True,
                   help="必传：客户端类型（codex/openclaw/joycode 等），透传上报服务端")
    p.add_argument("--daily-cap", type=float, default=None,
                   help="单日买入上限（金叶子/元）；不传则不限，托管到余额花完或叫停")
    p.add_argument("--poll-min", type=int, default=30, help="轮询间隔分钟（仅记录，实际由 launchd 控制）")
    p.add_argument("--cooldown-min", type=int, default=60, help="两次下单最小间隔分钟")
    p.add_argument("--dry-run", action="store_true", help="演练模式：只算不下单")
    p.add_argument("--install-launchd", action="store_true",
                   help="自动生成并加载 launchd 定时任务（无需手动改名/替换占位符）")
    p.add_argument("--uninstall-launchd", action="store_true",
                   help="停止并卸载 launchd 定时任务")
    args = p.parse_args(argv)

    if args.uninstall_launchd:
        return uninstall_launchd()
    if args.install_launchd:
        return install_launchd(args.claw, args.daily_cap)

    try:
        return run_once(args.claw, args.daily_cap, args.cooldown_min, args.dry_run)
    except Exception as e:
        notify("黄金托管异常", f"本轮执行异常：{e}")
        log(f"未捕获异常：{e}", level="ERROR")
        return 1


if __name__ == "__main__":
    sys.exit(main())
