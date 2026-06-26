#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
jisu-stock-monitor：基于极速数据股票 / 历史行情 API 的持仓预警检查（无常驻进程）。
支持：成本盈亏%、日内涨跌（个股/ETF/黄金默认阈值）、开盘跳空%、真缺口（昨高/昨低）、
动态止盈（可选跨日峰值状态文件）、告警冷却、放量/缩量、MA5/MA10、RSI 等。
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

import requests

STOCK_BASE = "https://api.jisuapi.com/stock"
HISTORY_BASE = "https://api.jisuapi.com/stockhistory"
STATE_VERSION = 2


def _json_out(obj: Any) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def _f(x: Any) -> Optional[float]:
    try:
        if x is None:
            return None
        return float(str(x).strip().replace(",", ""))
    except Exception:
        return None


def _call_jisu(base: str, path: str, appkey: str, params: Dict[str, Any]) -> Tuple[Optional[Any], Optional[dict]]:
    q = {"appkey": appkey}
    q.update({k: v for k, v in params.items() if v not in (None, "")})
    try:
        r = requests.get(f"{base}/{path}", params=q, timeout=15)
    except Exception as e:
        return None, {"error": "request_failed", "message": str(e)}
    if r.status_code != 200:
        return None, {"error": "http_error", "status_code": r.status_code, "body": r.text[:500]}
    try:
        data = r.json()
    except Exception:
        return None, {"error": "invalid_json", "body": r.text[:300]}
    if data.get("status") != 0:
        return None, {"error": "api_error", "code": data.get("status"), "message": data.get("msg")}
    return data.get("result"), None


def _resolve_state_path(req: dict) -> Optional[str]:
    """返回状态文件路径；req.state_file 为 null/false/'' 时禁用。"""
    if "state_file" in req:
        v = req["state_file"]
        if v in (False, None, ""):
            return None
        return str(v).strip()
    env = os.environ.get("JISU_STOCK_MONITOR_STATE", "").strip()
    if env:
        return env
    return None


def _load_state(path: str) -> dict:
    if not path or not os.path.isfile(path):
        return {"version": STATE_VERSION, "trailing": {}, "cooldown": {}}
    try:
        with open(path, "r", encoding="utf-8") as f:
            s = json.load(f)
        if not isinstance(s, dict):
            raise ValueError("not an object")
        s.setdefault("trailing", {})
        s.setdefault("cooldown", {})
        s["version"] = STATE_VERSION
        if not isinstance(s["trailing"], dict):
            s["trailing"] = {}
        if not isinstance(s["cooldown"], dict):
            s["cooldown"] = {}
        return s
    except Exception:
        return {"version": STATE_VERSION, "trailing": {}, "cooldown": {}}


def _save_state(path: str, state: dict) -> None:
    if not path:
        return
    state["version"] = STATE_VERSION
    d = os.path.dirname(os.path.abspath(path))
    if d and not os.path.isdir(d):
        os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(suffix=".json", prefix="jisu-sm-", dir=d or None)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def _holding_state_key(h: dict) -> str:
    sk = str(h.get("state_key") or "").strip()
    return sk or str(h.get("code") or "").strip()


def _cooldown_map_key(code_key: str, rule: str) -> str:
    return "%s|%s" % (code_key, rule)


def _cooldown_can_fire(cooldowns: dict, key: str, minutes: int) -> bool:
    if minutes <= 0:
        return True
    last = cooldowns.get(key)
    if not last:
        return True
    try:
        t0 = datetime.fromisoformat(str(last))
    except Exception:
        return True
    return (datetime.now() - t0).total_seconds() >= minutes * 60


def _cooldown_mark(cooldowns: dict, key: str) -> None:
    cooldowns[key] = datetime.now().replace(microsecond=0).isoformat()


def _maybe_trigger(
    triggers: List[dict],
    suppressed: List[dict],
    cooldowns: dict,
    code_key: str,
    cooldown_minutes: int,
    trigger: dict,
) -> None:
    rule = str(trigger.get("rule") or "")
    ck = _cooldown_map_key(code_key, rule)
    if _cooldown_can_fire(cooldowns, ck, cooldown_minutes):
        triggers.append(trigger)
        if cooldown_minutes > 0:
            _cooldown_mark(cooldowns, ck)
    else:
        suppressed.append({"rule": rule, "reason": "cooldown", "cooldown_minutes": cooldown_minutes})


def _yesterday_bar(rows: List[dict], today_iso: str) -> Optional[dict]:
    """最近一个交易日（date < 今天）的 K 线行。"""
    for row in reversed(rows):
        if not isinstance(row, dict):
            continue
        ds = str(row.get("date") or "")[:10]
        if ds and ds < today_iso:
            return row
    return None


def _read_req() -> dict:
    raw = sys.argv[2] if len(sys.argv) >= 3 else ""
    if isinstance(raw, str):
        rs = raw.strip()
        if rs == "-":
            raw = sys.stdin.read()
        elif rs.startswith("@") and len(rs) > 1:
            with open(rs[1:], "r", encoding="utf-8") as f:
                raw = f.read()
    if not raw.strip():
        return {}
    obj = json.loads(raw)
    if not isinstance(obj, dict):
        raise ValueError("JSON must be an object")
    return obj


def _sort_history_list(lst: List[dict]) -> List[dict]:
    def key_row(row: dict) -> str:
        return str(row.get("date") or "")
    return sorted(lst, key=key_row)


def _closes_volumes(rows: List[dict]) -> Tuple[List[float], List[float]]:
    """按交易日对齐：有收盘价则入列，成交量缺失记 0。"""
    closes: List[float] = []
    vols: List[float] = []
    for row in rows:
        c = _f(row.get("closingprice"))
        if c is None:
            continue
        closes.append(c)
        v = _f(row.get("tradenum"))
        vols.append(v if v is not None else 0.0)
    return closes, vols


def _sma(values: List[float], n: int) -> Optional[float]:
    if len(values) < n or n < 1:
        return None
    return sum(values[-n:]) / n


def _ma_cross_signal(closes: List[float]) -> Tuple[Optional[str], Optional[float], Optional[float]]:
    """最近一日相对前一日的 MA5/MA10 关系变化（需至少 11 根收盘）。"""
    n = len(closes)
    if n < 11:
        return None, None, None
    ma5_now = sum(closes[n - 5 : n]) / 5.0
    ma10_now = sum(closes[n - 10 : n]) / 10.0
    ma5_prev = sum(closes[n - 6 : n - 1]) / 5.0
    ma10_prev = sum(closes[n - 11 : n - 1]) / 10.0
    if ma5_prev <= ma10_prev and ma5_now > ma10_now:
        return "golden", ma5_now, ma10_now
    if ma5_prev >= ma10_prev and ma5_now < ma10_now:
        return "death", ma5_now, ma10_now
    return "none", ma5_now, ma10_now


def _rsi_simple(closes: List[float], period: int = 14) -> Optional[float]:
    if len(closes) < period + 1:
        return None
    deltas = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
    seg = deltas[-period:]
    gains = sum(d for d in seg if d > 0)
    losses = sum(-d for d in seg if d < 0)
    avg_g = gains / period
    avg_l = losses / period
    if avg_l == 0:
        return 100.0 if avg_g > 0 else 50.0
    rs = avg_g / avg_l
    return 100.0 - 100.0 / (1.0 + rs)


def _volume_surge_ratio(vols: List[float], mult: float) -> Tuple[bool, Optional[float]]:
    """最后一根成交量 vs 前 5 日均量（倍数）。"""
    if len(vols) < 6:
        return False, None
    last = vols[-1]
    prev5 = vols[-6:-1]
    if not prev5 or sum(prev5) == 0:
        return False, None
    avg5 = sum(prev5) / len(prev5)
    ratio = last / avg5 if avg5 else None
    if ratio is None:
        return False, None
    return ratio >= mult, ratio


def _volume_shrink_ratio(vols: List[float], mult: float) -> Tuple[bool, Optional[float]]:
    """最后一根成交量相对前 5 日均量，缩量：ratio <= mult（如 0.5）。"""
    if len(vols) < 6:
        return False, None
    last = vols[-1]
    prev5 = vols[-6:-1]
    avg5 = sum(prev5) / len(prev5)
    if avg5 <= 0:
        return False, None
    ratio = last / avg5
    return ratio <= mult, ratio


def _default_intraday_thresholds(typ: str) -> Tuple[float, float]:
    """默认日内涨跌幅阈值（高、低为对称负数）。"""
    t = typ.strip().lower()
    if t == "etf":
        hi = 2.0
    elif t in ("gold", "au", "commodity"):
        hi = 2.5
    else:
        hi = 4.0
    return hi, -hi


def _evaluate_holding(
    appkey: str,
    h: dict,
    history_days: int,
    state: Optional[dict],
    cooldown_minutes: int,
) -> dict:
    code = str(h.get("code") or "").strip()
    name_cfg = str(h.get("name") or "").strip()
    cost = _f(h.get("cost"))
    alerts = h.get("alerts") if isinstance(h.get("alerts"), dict) else {}
    typ = str(h.get("type") or "individual").strip().lower()
    hk = _holding_state_key(h)

    triggers: List[dict] = []
    suppressed: List[dict] = []
    err_note: Optional[dict] = None

    def _t(tr: dict) -> None:
        if state is not None and cooldown_minutes > 0:
            _maybe_trigger(triggers, suppressed, state["cooldown"], hk, cooldown_minutes, tr)
        else:
            triggers.append(tr)

    detail, err = _call_jisu(STOCK_BASE, "detail", appkey, {"code": code})
    if err:
        return {
            "code": code,
            "name": name_cfg or code,
            "ok": False,
            "error": err,
            "triggers": [],
            "suppressed_by_cooldown": [],
        }

    d = detail if isinstance(detail, dict) else {}
    name = name_cfg or str(d.get("name") or code)
    price = _f(d.get("price"))
    chg_pct = _f(d.get("changepercent"))
    tradenum = _f(d.get("tradenum"))
    open_px = _f(d.get("openningprice"))
    prev_close = _f(d.get("lastclosingprice"))
    maxprice = _f(d.get("maxprice"))
    minprice = _f(d.get("minprice"))

    def_chg_hi, def_chg_lo = _default_intraday_thresholds(typ)

    indicators: Dict[str, Any] = {}

    # —— 开盘跳空%（今开相对昨收）——
    gap_pct: Optional[float] = None
    if open_px is not None and prev_close is not None and prev_close > 0:
        gap_pct = (open_px - prev_close) / prev_close * 100.0
        indicators["gap_open_pct"] = round(gap_pct, 4)
    if alerts.get("gap_monitor") and gap_pct is not None:
        g_up = _f(alerts.get("gap_up_pct"))
        if g_up is None:
            g_up = 1.0
        g_dn = _f(alerts.get("gap_down_pct"))
        if g_dn is None:
            g_dn = -1.0
        if gap_pct >= g_up:
            _t(
                {
                    "level": "info",
                    "rule": "gap_up",
                    "message": "向上跳空开盘约 %.2f%%（阈值 ≥%.2f%%）" % (gap_pct, g_up),
                }
            )
        if gap_pct <= g_dn:
            _t(
                {
                    "level": "info",
                    "rule": "gap_down",
                    "message": "向下跳空开盘约 %.2f%%（阈值 ≤%.2f%%）" % (gap_pct, g_dn),
                }
            )

    # —— 动态止盈：可选跨日峰值（state_file + persist）或仅当日高低点 ——
    dt = alerts.get("dynamic_trailing")
    if isinstance(dt, dict) and dt.get("enable", True) is not False:
        min_peak = _f(dt.get("min_peak_profit_pct"))
        if min_peak is None:
            min_peak = 10.0
        ddw = _f(dt.get("drawdown_warn_pct"))
        if ddw is None:
            ddw = 5.0
        ddu = _f(dt.get("drawdown_urgent_pct"))
        if ddu is None:
            ddu = 10.0
        persist = dt.get("persist", True) is not False
        use_state_peak = state is not None and persist

        cand: List[float] = []
        if maxprice is not None:
            cand.append(maxprice)
        if price is not None:
            cand.append(price)
        peak_px_today = max(cand) if cand else None

        if cost is not None and cost > 0 and peak_px_today is not None and peak_px_today > 0:
            track_peak: Optional[float] = None
            if use_state_peak:
                tr_ent = state["trailing"].get(hk)
                old_cost = _f(tr_ent.get("cost")) if isinstance(tr_ent, dict) else None
                old_peak = _f(tr_ent.get("peak_price")) if isinstance(tr_ent, dict) else None
                if tr_ent is None or old_cost is None or abs(old_cost - cost) > 1e-6:
                    track_peak = peak_px_today
                else:
                    track_peak = max(old_peak or 0.0, peak_px_today)
                state["trailing"][hk] = {
                    "peak_price": track_peak,
                    "cost": cost,
                    "updated": datetime.now().replace(microsecond=0).isoformat(),
                }
            else:
                track_peak = peak_px_today

            peak_profit = (track_peak - cost) / cost * 100.0
            indicators["tracked_peak_price"] = round(track_peak, 4)
            indicators["tracked_peak_profit_pct"] = round(peak_profit, 4)
            if use_state_peak:
                indicators["trailing_persisted"] = True
            else:
                indicators["trailing_persisted"] = False

            if price is not None and track_peak > 0 and peak_profit >= min_peak:
                dd = (track_peak - price) / track_peak * 100.0
                indicators["drawdown_from_tracked_peak_pct"] = round(dd, 4)
                if ddu is not None and dd >= ddu:
                    _t(
                        {
                            "level": "warning",
                            "rule": "dynamic_trailing_urgent",
                            "message": "曾达峰值盈利 %.2f%%（≥%.2f%%），自跟踪高点回撤 %.2f%%（≥%.2f%%）"
                            % (peak_profit, min_peak, dd, ddu),
                        }
                    )
                elif ddw is not None and dd >= ddw:
                    _t(
                        {
                            "level": "warning",
                            "rule": "dynamic_trailing_warn",
                            "message": "曾达峰值盈利 %.2f%%（≥%.2f%%），自跟踪高点回撤 %.2f%%（≥%.2f%%）"
                            % (peak_profit, min_peak, dd, ddw),
                        }
                    )

    # —— 成本盈亏% ——
    profit_pct: Optional[float] = None
    if cost is not None and cost > 0 and price is not None:
        profit_pct = (price - cost) / cost * 100.0
        cap = _f(alerts.get("cost_pct_above"))
        if cap is not None and profit_pct >= cap:
            _t(
                {
                    "level": "warning",
                    "rule": "cost_pct_above",
                    "message": "相对成本盈利 %.2f%%，达到阈值 %.2f%%" % (profit_pct, cap),
                }
            )
        floor = _f(alerts.get("cost_pct_below"))
        if floor is not None and profit_pct <= floor:
            _t(
                {
                    "level": "warning",
                    "rule": "cost_pct_below",
                    "message": "相对成本亏损 %.2f%%，达到阈值 %.2f%%" % (profit_pct, floor),
                }
            )

    # —— 日内涨跌幅 ——
    if chg_pct is not None:
        thi = _f(alerts.get("change_pct_above"))
        if thi is None:
            thi = def_chg_hi if alerts.get("change_pct_above") is not False else None
        if thi is not None and chg_pct >= thi:
            _t(
                {
                    "level": "info",
                    "rule": "change_pct_above",
                    "message": "日内涨幅 %.2f%%，达到阈值 %.2f%%" % (chg_pct, thi),
                }
            )
        tlo = _f(alerts.get("change_pct_below"))
        if tlo is None:
            tlo = def_chg_lo if alerts.get("change_pct_below") is not False else None
        if tlo is not None and chg_pct <= tlo:
            _t(
                {
                    "level": "info",
                    "rule": "change_pct_below",
                    "message": "日内跌幅 %.2f%%，达到阈值 %.2f%%" % (chg_pct, tlo),
                }
            )

    need_hist = (
        bool(alerts.get("ma_monitor"))
        or _f(alerts.get("volume_surge")) is not None
        or _f(alerts.get("volume_shrink")) is not None
        or bool(alerts.get("rsi_monitor"))
        or bool(alerts.get("gap_true_monitor"))
    )
    if need_hist:
        end_d = date.today()
        start_d = end_d - timedelta(days=max(history_days, 120))
        hist, herr = _call_jisu(
            HISTORY_BASE,
            "query",
            appkey,
            {"code": code, "startdate": start_d.isoformat(), "enddate": end_d.isoformat()},
        )
        if herr:
            err_note = herr
            _t(
                {
                    "level": "info",
                    "rule": "history_unavailable",
                    "message": "历史行情拉取失败，已跳过均线/成交量对比/RSI/真缺口：%s"
                    % herr.get("message", herr),
                }
            )
        else:
            hobj = hist if isinstance(hist, dict) else {}
            raw_list = hobj.get("list") if isinstance(hobj.get("list"), list) else []
            rows = _sort_history_list([x for x in raw_list if isinstance(x, dict)])
            today_iso = date.today().isoformat()

            # —— 真缺口：当日最低 > 昨日最高 / 当日最高 < 昨日最低 ——
            if alerts.get("gap_true_monitor"):
                yb = _yesterday_bar(rows, today_iso)
                t_low = minprice
                t_high = maxprice
                y_hi = _f(yb.get("maxprice")) if yb else None
                y_lo = _f(yb.get("minprice")) if yb else None
                gmin = _f(alerts.get("gap_true_min_pct"))
                body_up_pct: Optional[float] = None
                body_dn_pct: Optional[float] = None
                if t_low is not None and y_hi is not None and y_hi > 0 and t_low > y_hi:
                    body_up_pct = (t_low - y_hi) / y_hi * 100.0
                    indicators["gap_true_body_up_pct"] = round(body_up_pct, 4)
                    ok_up = gmin is None or body_up_pct >= gmin
                    if ok_up:
                        _t(
                            {
                                "level": "info",
                                "rule": "gap_true_up",
                                "message": "真向上缺口：今日低 %.4f > 昨日高 %.4f（缺口体约 %.2f%%）"
                                % (t_low, y_hi, body_up_pct),
                            }
                        )
                if t_high is not None and y_lo is not None and y_lo > 0 and t_high < y_lo:
                    body_dn_pct = (y_lo - t_high) / y_lo * 100.0
                    indicators["gap_true_body_down_pct"] = round(body_dn_pct, 4)
                    ok_dn = gmin is None or body_dn_pct >= gmin
                    if ok_dn:
                        _t(
                            {
                                "level": "info",
                                "rule": "gap_true_down",
                                "message": "真向下缺口：今日高 %.4f < 昨日低 %.4f（缺口体约 %.2f%%）"
                                % (t_high, y_lo, body_dn_pct),
                            }
                        )

            closes, vols = _closes_volumes(rows)
            ma5 = _sma(closes, 5)
            ma10 = _sma(closes, 10)
            indicators["ma5"] = round(ma5, 4) if ma5 is not None else None
            indicators["ma10"] = round(ma10, 4) if ma10 is not None else None

            if alerts.get("ma_monitor"):
                sig, m5, m10 = _ma_cross_signal(closes)
                indicators["ma_cross"] = sig
                if sig == "golden":
                    _t(
                        {
                            "level": "warning",
                            "rule": "ma_golden_cross",
                            "message": "MA5 上穿 MA10（约 %.4f / %.4f）" % (m5 or 0, m10 or 0),
                        }
                    )
                elif sig == "death":
                    _t(
                        {
                            "level": "warning",
                            "rule": "ma_death_cross",
                            "message": "MA5 下穿 MA10（约 %.4f / %.4f）" % (m5 or 0, m10 or 0),
                        }
                    )

            mult = _f(alerts.get("volume_surge"))
            if mult is not None and mult > 0:
                hit, ratio = _volume_surge_ratio(vols, mult)
                indicators["volume_vs_ma5d"] = round(ratio, 4) if ratio is not None else None
                if hit:
                    _t(
                        {
                            "level": "info",
                            "rule": "volume_surge",
                            "message": "放量：成交量约为近5日均量的 %.2f 倍（阈值 ≥%.2f）" % (ratio or 0, mult),
                        }
                    )

            shr = _f(alerts.get("volume_shrink"))
            if shr is not None and shr > 0:
                hit2, ratio2 = _volume_shrink_ratio(vols, shr)
                indicators["volume_vs_ma5d_shrink"] = round(ratio2, 4) if ratio2 is not None else None
                if hit2:
                    _t(
                        {
                            "level": "info",
                            "rule": "volume_shrink",
                            "message": "缩量：成交量约为近5日均量的 %.2f 倍（阈值 ≤%.2f）" % (ratio2 or 0, shr),
                        }
                    )

            if bool(alerts.get("rsi_monitor")):
                rsi = _rsi_simple(closes, 14)
                indicators["rsi14"] = round(rsi, 2) if rsi is not None else None
                ob = _f(alerts.get("rsi_overbought"))
                if ob is None:
                    ob = 70.0
                os_ = _f(alerts.get("rsi_oversold"))
                if os_ is None:
                    os_ = 30.0
                if rsi is not None:
                    if rsi >= ob:
                        _t(
                            {
                                "level": "info",
                                "rule": "rsi_overbought",
                                "message": "RSI(14)=%.2f，高于超买线 %.2f" % (rsi, ob),
                            }
                        )
                    if rsi <= os_:
                        _t(
                            {
                                "level": "info",
                                "rule": "rsi_oversold",
                                "message": "RSI(14)=%.2f，低于超卖线 %.2f" % (rsi, os_),
                            }
                        )

    out: Dict[str, Any] = {
        "code": code,
        "name": name,
        "ok": True,
        "price": price,
        "changepercent": chg_pct,
        "cost": cost,
        "cost_profit_pct": round(profit_pct, 4) if profit_pct is not None else None,
        "tradenum": tradenum,
        "triggers": triggers,
        "suppressed_by_cooldown": suppressed,
        "indicators": indicators,
    }
    if err_note:
        out["history_error"] = err_note
    return out


def cmd_check() -> None:
    req = _read_req()
    holdings = req.get("holdings")
    if not isinstance(holdings, list) or not holdings:
        _json_out({"error": "missing_param", "message": "holdings (non-empty array) is required"})
        sys.exit(1)
    try:
        history_days = int(req.get("history_days", 90))
    except Exception:
        history_days = 90
    history_days = max(30, min(history_days, 365))

    try:
        cooldown_minutes = int(req.get("alert_cooldown_minutes") or 0)
    except Exception:
        cooldown_minutes = 0
    cooldown_minutes = max(0, min(cooldown_minutes, 7 * 24 * 60))

    state_path = _resolve_state_path(req)
    if cooldown_minutes > 0 and state_path is None and "state_file" not in req:
        if not os.environ.get("JISU_STOCK_MONITOR_STATE", "").strip():
            state_path = "jisu-stock-monitor.state.json"

    state: Optional[dict] = _load_state(state_path) if state_path else None

    appkey = os.environ.get("JISU_API_KEY", "").strip()
    if not appkey:
        _json_out({"error": "missing_credential", "message": "JISU_API_KEY is required"})
        sys.exit(1)

    results = []
    for h in holdings:
        if not isinstance(h, dict):
            continue
        results.append(_evaluate_holding(appkey, h, history_days, state, cooldown_minutes))

    if state_path and state is not None:
        try:
            _save_state(state_path, state)
        except Exception as e:
            _json_out({"ok": False, "error": "state_save_failed", "message": str(e)})
            sys.exit(1)

    total_trig = sum(len(r.get("triggers") or []) for r in results if r.get("ok"))
    total_sup = sum(len(r.get("suppressed_by_cooldown") or []) for r in results if r.get("ok"))
    urgent = 0
    for r in results:
        for t in r.get("triggers") or []:
            if t.get("level") == "warning":
                urgent += 1

    _json_out(
        {
            "ok": True,
            "checked_at": date.today().isoformat(),
            "disclaimer": "仅供技术学习与信息整理，不构成投资建议。",
            "summary": {
                "holdings": len(results),
                "trigger_events": total_trig,
                "warning_level_events": urgent,
                "suppressed_by_cooldown": total_sup,
                "state_file": state_path,
                "alert_cooldown_minutes": cooldown_minutes,
            },
            "results": results,
        }
    )


def main() -> None:
    if len(sys.argv) < 2:
        print(
            "Usage:\n"
            "  monitor.py check '{\"holdings\":[...]}'\n"
            "  monitor.py check @config.json\n"
            "Env: JISU_API_KEY, optional JISU_STOCK_MONITOR_STATE\n",
            file=sys.stderr,
        )
        sys.exit(1)
    cmd = sys.argv[1].strip().lower()
    if cmd != "check":
        print("unknown command: %s" % cmd, file=sys.stderr)
        sys.exit(1)
    try:
        cmd_check()
    except Exception as e:
        _json_out({"ok": False, "error": str(e)})
        sys.exit(1)


if __name__ == "__main__":
    main()
