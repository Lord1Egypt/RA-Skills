"""选号 + 兑奖 + 报表 + 手动录入。规则查表全在 config/rules.json。"""
from __future__ import annotations

import json
import re
import secrets
from collections import Counter
from datetime import timedelta
from pathlib import Path
from typing import Any

import store

_RNG = secrets.SystemRandom()
_RULES_PATH = Path(__file__).resolve().parent.parent / "config" / "rules.json"
RULES: dict[str, Any] = json.loads(_RULES_PATH.read_text(encoding="utf-8-sig"))
LOTTERIES: dict[str, Any] = RULES["lotteries"]
PRIZE: dict[str, Any] = RULES["prize_rules"]


# ---------- 工具 ----------
def normalize_lottery(value: str) -> str:
    if not value:
        raise ValueError("缺少彩种")
    text = str(value).lower().strip()
    if text in LOTTERIES:
        return text
    for key, cfg in LOTTERIES.items():
        for alias in cfg.get("aliases", []):
            if str(alias).lower() == text:
                return key
    raise ValueError(f"未知彩种: {value}")


def pad(n: int) -> str:
    return f"{int(n):02d}"


def pick_unique(lo: int, hi: int, count: int, sort: bool = True) -> list[int]:
    nums = _RNG.sample(range(lo, hi + 1), count)
    return sorted(nums) if sort else nums


def pick_digits(count: int, lo: int = 0, hi: int = 9) -> list[int]:
    return [_RNG.randint(lo, hi) for _ in range(count)]


# ---------- 单注生成 ----------
def generate_one(key: str, play_type: str) -> dict[str, Any]:
    cfg = LOTTERIES[key]
    if key in {"fc3d", "pl3"}:
        return {"digits": gen_digit3(play_type), "play_type": play_type}
    if key == "kl8":
        count = max(1, min(10, int(play_type)))
        sec = cfg["sections"][0]
        return {"nums": pick_unique(sec["min"], sec["max"], count, True),
                "play_count": count, "play_type": str(count)}
    out: dict[str, Any] = {}
    for sec in cfg["sections"]:
        if sec.get("unique"):
            out[sec["key"]] = pick_unique(sec["min"], sec["max"], sec["count"],
                                          sec.get("sort", True))
        else:
            out[sec["key"]] = pick_digits(sec["count"], sec["min"], sec["max"])
    return out


def gen_digit3(play_type: str) -> list[int]:
    if play_type == "group6":
        return pick_unique(0, 9, 3, True)
    if play_type == "group3":
        pair = pick_unique(0, 9, 2, False)
        repeated = _RNG.choice(pair)
        return sorted(pair + [repeated])
    return pick_digits(3)


# ---------- 成本 / 默认 ----------
def ticket_cost(key: str, multiple: int, is_additional: bool) -> float:
    cfg = LOTTERIES[key]
    price = float(cfg.get("price", 2))
    if is_additional:
        price += float(cfg.get("additional_price", 0))
    return price * max(1, int(multiple))


def default_play_type(key: str, override: str | None) -> str:
    if override:
        return override
    return str(LOTTERIES[key].get("default_play_type", "standard"))


# ---------- 文本格式 ----------
def format_numbers(key: str, numbers: dict[str, Any]) -> str:
    sep = "  "
    plus = " + "
    if key == "ssq":
        return sep.join(pad(n) for n in numbers["red"]) + plus + pad(numbers["blue"][0])
    if key == "dlt":
        return sep.join(pad(n) for n in numbers["front"]) + plus + sep.join(pad(n) for n in numbers["back"])
    if key == "qlc":
        return sep.join(pad(n) for n in numbers["basic"])
    if key == "kl8":
        return sep.join(pad(n) for n in numbers["nums"])
    if key in {"fc3d", "pl3", "pl5", "qxc"}:
        return sep.join(str(n) for n in numbers["digits"])
    return ""


def render_message(key: str, tickets: list[dict[str, Any]], total_cost: float) -> str:
    name = LOTTERIES[key]["name"]
    head = [name, f"{len(tickets)}注"]
    first = tickets[0]
    if int(first.get("multiple", 1)) > 1:
        head.append(f"{first['multiple']}倍")
    if key == "dlt" and first.get("is_additional"):
        head.append("追加")
    if key == "kl8":
        head.insert(1, f"选{first.get('play_count') or first.get('play_type')}")
    if key in {"fc3d", "pl3"}:
        head.insert(1, _digit3_label(first.get("play_type")))
    if first.get("draw_date"):
        head.append(f"开奖 {first['draw_date']}")
    lines = ["｜".join(part for part in head if part)]
    lines.append(f"投入：{total_cost:g}元")
    lines.append("")
    for t in tickets:
        lines.append(format_numbers(key, t["numbers"]))
    return "\n".join(lines)


def _digit3_label(play_type: str | None) -> str:
    return {"single": "单选", "group3": "组三", "group6": "组六"}.get(str(play_type or ""), "")


# ---------- 选号入口 ----------
def generate(lottery: str, count: int = 1, play_type: str | None = None,
             multiple: int = 1, is_additional: bool = False,
             budget: float | None = None) -> dict[str, Any]:
    key = normalize_lottery(lottery)
    play = default_play_type(key, play_type)
    multiple = max(1, int(multiple or 1))
    if budget is not None:
        unit = ticket_cost(key, multiple, is_additional)
        count = max(1, int(float(budget) // unit))
    count = max(1, int(count))

    import fetch
    track = fetch.resolve_tracking(key)
    issue = track.get("issue")
    draw_date = track.get("draw_date")

    batch_uuid = store.new_batch_uuid()
    tickets: list[dict[str, Any]] = []
    cost_each = ticket_cost(key, multiple, is_additional)
    for _ in range(count):
        nums = generate_one(key, play)
        ticket = {
            "lottery": key,
            "play_type": nums.get("play_type", play),
            "numbers": nums,
            "cost": cost_each,
            "multiple": multiple,
            "is_additional": is_additional,
            "batch_uuid": batch_uuid,
            "issue": issue,
            "draw_date": draw_date,
            "status": "active",
        }
        ticket["id"] = store.insert_ticket(ticket)
        ticket["formatted"] = format_numbers(key, nums)
        tickets.append(ticket)
    total_cost = cost_each * len(tickets)
    text = render_message(key, tickets, total_cost)
    result: dict[str, Any] = {
        "ok": True, "lottery": key, "batch_uuid": batch_uuid,
        "tickets": tickets, "total_cost": total_cost,
        "issue": issue, "draw_date": draw_date,
        "message_text": text, "numbers_message": text, "split_messages": True,
    }
    notice = track.get("notice")
    followups = ["号码已入账，开奖后会自动核对。"]
    if notice:
        followups.insert(0, notice)
    result["followup_messages"] = followups
    return result


# ---------- 兑奖 ----------
def evaluate(key: str, ticket_nums: dict[str, Any], draw_nums: dict[str, Any],
             play_type: str, is_additional: bool, multiple: int,
             draw_ctx: dict[str, Any]) -> dict[str, Any]:
    if key == "ssq":
        facts = {"red": _count_match(ticket_nums["red"], draw_nums["red"]),
                 "blue": int(ticket_nums["blue"][0] == draw_nums["blue"][0])}
        return _match_rule(key, facts, multiple, False, draw_ctx)
    if key == "dlt":
        facts = {"front": _count_match(ticket_nums["front"], draw_nums["front"]),
                 "back": _count_match(ticket_nums["back"], draw_nums["back"])}
        return _match_rule(key, facts, multiple, is_additional, draw_ctx)
    if key == "qlc":
        special = draw_nums.get("special")
        facts = {"basic": _count_match(ticket_nums["basic"], draw_nums["basic"]),
                 "special": int(special is not None and special in ticket_nums["basic"])}
        return _match_rule(key, facts, multiple, False, draw_ctx)
    if key == "qxc":
        td = ticket_nums["digits"]; dd = draw_nums["digits"]
        main = sum(1 for a, b in zip(td[:6], dd[:6]) if a == b)
        tail = int(td[6] == dd[6])
        return _match_rule(key, {"main": main, "tail": tail}, multiple, False, draw_ctx)
    if key in {"fc3d", "pl3"}:
        return _eval_digit3(ticket_nums["digits"], draw_nums["digits"], play_type, multiple)
    if key == "pl5":
        if ticket_nums["digits"] == draw_nums["digits"]:
            cfg = PRIZE["pl5"]
            return _win(cfg["level"], float(cfg["amount"]) * multiple, False)
        return _lose()
    if key == "kl8":
        play_count = str(ticket_nums.get("play_count") or play_type)
        hits = _count_match(ticket_nums["nums"], draw_nums["nums"])
        table = PRIZE["kl8"].get(play_count, {})
        entry = table.get(str(hits))
        if isinstance(entry, dict) and entry.get("float"):
            level = str(entry.get("level") or f"选{play_count}一等奖")
            api_amt = _api_prize_amount(level, draw_ctx, False)
            if api_amt is None:
                api_amt = _api_prize_amount(f"中{hits}", draw_ctx, False)
            return _win(level, (api_amt or 0) * multiple, api_amt is None)
        if entry is not None:
            return _win(f"中{hits}", float(entry) * multiple, False)
        return _lose()
    return _lose()


def _count_match(ticket: list[int], draw: list[int]) -> int:
    counts = Counter(draw or [])
    hits = 0
    for n in ticket or []:
        if counts[n] > 0:
            counts[n] -= 1
            hits += 1
    return hits


def _match_rule(key: str, facts: dict[str, int], multiple: int,
                is_additional: bool, draw_ctx: dict[str, Any]) -> dict[str, Any]:
    for rule in PRIZE[key]:
        candidates = rule.get("any") or [rule.get("when", {})]
        if any(all(facts.get(k) == v for k, v in cand.items()) for cand in candidates):
            level = rule["level"]
            api_amt = _api_prize_amount(level, draw_ctx, is_additional)
            if rule.get("float"):
                return _win(level, (api_amt or 0) * multiple, api_amt is None)
            amount = _dlt_pool_amount(key, level, draw_ctx)
            if amount is None:
                amount = api_amt if api_amt is not None else float(rule.get("amount", 0))
            if is_additional:
                amount += _api_additional(level, draw_ctx) or float(rule.get("additional_amount", 0))
            return _win(level, amount * multiple, False)
    return _lose()


def _eval_digit3(ticket: list[int], draw: list[int], play_type: str, multiple: int) -> dict[str, Any]:
    rules = PRIZE["digit3"]
    if play_type == "single":
        if ticket == draw:
            return _win(rules["single"]["level"], rules["single"]["amount"] * multiple, False)
        return _lose()
    if play_type == "group3":
        if len(set(draw)) == 2 and Counter(ticket) == Counter(draw):
            return _win(rules["group3"]["level"], rules["group3"]["amount"] * multiple, False)
        return _lose()
    if len(set(draw)) == 3 and Counter(ticket) == Counter(draw):
        return _win(rules["group6"]["level"], rules["group6"]["amount"] * multiple, False)
    return _lose()


def _dlt_pool_amount(key: str, level: str, draw_ctx: dict[str, Any]) -> float | None:
    if key != "dlt":
        return None
    amounts = PRIZE.get("dlt_pool_amounts", {})
    under = amounts.get("under", {})
    over = amounts.get("at_or_over", {})
    if level not in under and level not in over:
        return None
    threshold = float(PRIZE.get("dlt_pool_threshold", 800000000))
    pool = float(draw_ctx.get("prize_pool") or 0)
    table = over if pool >= threshold else under
    return float(table.get(level, under.get(level, 0)))


def _api_prize_amount(level: str, draw_ctx: dict[str, Any], include_add: bool) -> float | None:
    for d in draw_ctx.get("prize_details", []) or []:
        if level == d.get("prize_level") or level == d.get("prize_name"):
            amt = _money(d.get("prize_amount") or d.get("singlebonus") or d.get("bonus"))
            if include_add:
                amt += _money(d.get("additional_amount") or d.get("addbonus"))
            return amt if amt > 0 else None
    return None


def _api_additional(level: str, draw_ctx: dict[str, Any]) -> float | None:
    for d in draw_ctx.get("prize_details", []) or []:
        if level == d.get("prize_level") or level == d.get("prize_name"):
            amt = _money(d.get("additional_amount") or d.get("addbonus"))
            return amt if amt > 0 else None
    return None


def _money(value: Any) -> float:
    return store._to_float(value) or 0.0  # type: ignore[attr-defined]


def _win(level: str, amount: float, pending: bool) -> dict[str, Any]:
    return {"is_winning": True, "prize_level": level,
            "prize_amount": amount, "prize_pending": pending}


def _lose() -> dict[str, Any]:
    return {"is_winning": False, "prize_level": "",
            "prize_amount": 0.0, "prize_pending": False}


def check_prize(lottery: str | None = None, issue: str | None = None) -> dict[str, Any]:
    where = ["t.status='active'"]
    params: list[Any] = []
    if lottery:
        where.append("t.lottery=?")
        params.append(normalize_lottery(lottery))
    if issue:
        where.append("(t.issue=? OR (t.issue IS NULL AND d.issue=?))")
        params.extend([issue, issue])
    sql = f"""
      SELECT t.*, d.issue AS d_issue, d.numbers_json AS d_numbers,
             d.prize_pool AS d_pool, d.prize_details_json AS d_details
      FROM tickets t
      JOIN draws d ON d.lottery = t.lottery
        AND ((t.issue IS NOT NULL AND t.issue=d.issue)
             OR (t.issue IS NULL AND t.draw_date IS NOT NULL AND t.draw_date=d.draw_date))
      WHERE {' AND '.join(where)}
      ORDER BY t.id DESC
    """
    checked = []
    win_count = 0
    total = 0.0
    rows = store.fetch_all(sql, params)
    for row in rows:
        ticket_nums = json.loads(row["numbers_json"])
        draw_nums = json.loads(row["d_numbers"] or "{}")
        details = json.loads(row["d_details"] or "[]")
        result = evaluate(
            row["lottery"], ticket_nums, draw_nums,
            row["play_type"] or "standard",
            bool(row["is_additional"]),
            int(row["multiple"] or 1),
            {"prize_pool": row["d_pool"], "prize_details": details},
        )
        store.update_ticket_prize(int(row["id"]), float(result["prize_amount"]),
                                   result["prize_level"], bool(result["prize_pending"]))
        checked.append({**result, "ticket_id": int(row["id"]), "issue": row["d_issue"]})
        if result["is_winning"]:
            win_count += 1
            total += float(result["prize_amount"])
    msg = f"兑奖完成：{len(checked)} 注，中奖 {win_count} 注，金额 {total:g} 元"
    return {"ok": True, "checked_count": len(checked),
            "winning_count": win_count, "total_amount": total,
            "results": checked, "message_text": msg}


# ---------- 报表 ----------
def report(since_days: int = 30) -> dict[str, Any]:
    cutoff = (store.cn_now() - timedelta(days=int(since_days))).date().isoformat()
    rows = store.fetch_all(
        """SELECT lottery, COUNT(*) AS n, SUM(cost) AS cost,
                  SUM(prize_amount) AS prize, SUM(prize_pending) AS pending
           FROM tickets WHERE status IN ('active','matched')
             AND substr(created_at,1,10) >= ?
           GROUP BY lottery ORDER BY lottery""",
        (cutoff,),
    )
    if not rows:
        return {"ok": True, "since_days": since_days,
                "message_text": f"近 {since_days} 天没有有效记录。"}
    total_cost = sum(float(r["cost"] or 0) for r in rows)
    total_prize = sum(float(r["prize"] or 0) for r in rows)
    pending = sum(int(r["pending"] or 0) for r in rows)
    lines = [f"近 {since_days} 天报表"]
    for r in rows:
        name = LOTTERIES.get(r["lottery"], {}).get("name", r["lottery"])
        lines.append(f"{name}：{r['n']} 注｜投入 {float(r['cost'] or 0):g}｜回报 {float(r['prize'] or 0):g}")
    lines.append(f"合计：投入 {total_cost:g}｜回报 {total_prize:g}｜盈亏 {total_prize - total_cost:g}")
    if pending:
        lines.append(f"另有 {pending} 注浮动奖待 API 补金额")
    return {"ok": True, "since_days": since_days, "rows": rows,
            "total_cost": total_cost, "total_prize": total_prize,
            "message_text": "\n".join(lines)}


# ---------- 手动录入 ----------
def record_manual(lottery: str, text: str, multiple: int = 1,
                  is_additional: bool = False, issue: str | None = None) -> dict[str, Any]:
    key = normalize_lottery(lottery)
    nums = re.findall(r"\d+", text or "")
    if not nums:
        return {"ok": False, "error": "未识别到号码",
                "message_text": "没找到号码。格式举例：双色球 01 05 12 18 25 31 + 09"}
    parsed = _parse_manual_numbers(key, [int(n) for n in nums])
    if not parsed:
        return {"ok": False, "error": "号码格式不符",
                "message_text": "号码格式不符，请用 `01 05 12 18 25 31 + 09` 这种格式。"}
    import fetch
    track = fetch.resolve_tracking(key) if not issue else {"issue": issue, "draw_date": None}
    batch_uuid = store.new_batch_uuid()
    cost_each = ticket_cost(key, multiple, is_additional)
    saved = []
    for item in parsed:
        ticket = {
            "lottery": key, "play_type": item.get("play_type", "standard"),
            "numbers": item, "cost": cost_each, "multiple": multiple,
            "is_additional": is_additional, "batch_uuid": batch_uuid,
            "issue": track.get("issue"), "draw_date": track.get("draw_date"),
            "status": "active",
        }
        ticket["id"] = store.insert_ticket(ticket)
        ticket["formatted"] = format_numbers(key, item)
        saved.append(ticket)
    total = cost_each * len(saved)
    text_msg = render_message(key, saved, total)
    return {"ok": True, "tickets": saved, "total_cost": total,
            "message_text": text_msg, "numbers_message": text_msg, "split_messages": True,
            "followup_messages": ["已记录到账本，开奖后会自动核对。"]}


def _parse_manual_numbers(key: str, nums: list[int]) -> list[dict[str, Any]]:
    if key == "ssq":
        if len(nums) >= 7:
            return [{"red": sorted(nums[:6]), "blue": [nums[6]]}]
    elif key == "dlt":
        if len(nums) >= 7:
            return [{"front": sorted(nums[:5]), "back": sorted(nums[5:7])}]
    elif key == "qlc":
        if len(nums) >= 7:
            return [{"basic": sorted(nums[:7])}]
    elif key == "kl8":
        if 1 <= len(nums) <= 10:
            return [{"nums": sorted(nums), "play_count": len(nums), "play_type": str(len(nums))}]
    elif key == "qxc":
        digits = _expand_digits(nums)
        if len(digits) >= 7:
            return [{"digits": digits[:7]}]
    elif key == "pl5":
        digits = _expand_digits(nums)
        if len(digits) >= 5:
            return [{"digits": digits[:5]}]
    elif key in {"fc3d", "pl3"}:
        digits = _expand_digits(nums)
        if len(digits) >= 3:
            play = "group6" if len(set(digits[:3])) == 3 else ("group3" if len(set(digits[:3])) == 2 else "single")
            return [{"digits": digits[:3], "play_type": play}]
    return []


def _expand_digits(nums: list[int]) -> list[int]:
    if all(0 <= n <= 9 for n in nums):
        return nums
    out: list[int] = []
    for n in nums:
        out.extend(int(c) for c in str(n))
    return out
