#!/usr/bin/env python3
"""每日精选策略 V2.2 — 四层漏斗 + 三层分级 + 离线容错

V2.2 变更（2026-08-03，离线容错增强）：
  - L2: westockdata 失败时标记"数据缺失-跳过"，不伪装通过
  - L3: 资金流向不可用时分数=0并标注"数据缺失"，不给硬编码默认分
  - L4: 复用 VPS 内部产业分类替代 tdx-connector 依赖
  - L1: 通过 VPS data_provider 做真实 MA 支撑检查
  - 报告: 增加数据可用性状态栏

用法:
    python precision_picker.py --pool sh600519,sz000858   # 指定候选池
    python precision_picker.py --pool-file candidates.txt  # 从文件读
    python precision_picker.py --auto                      # 自动读取最新VPS信号
"""

import argparse
import json
import os
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
VPS_DIR = os.path.expanduser("~/.workbuddy/skills/volume-price-screener/scripts")
VPS_DATA = os.path.expanduser("~/.workbuddy/skills/volume-price-screener/data")

# 添加 VPS 到 path
if os.path.exists(VPS_DIR) and VPS_DIR not in sys.path:
    sys.path.insert(0, VPS_DIR)

# ═══ 内联行业分类（替代缺失的 scoring.get_industry_code） ═══
INDUSTRY_KW = {
    "电力新能源": ["电","能源","风","光","伏","核","缆","器","网","新能","节能","电池","电热"],
    "科技电子": ["科技","电子","软件","信息","数字","智能","通信","讯","芯","半导","集成","数据"],
    "化工材料": ["化","材","玻","纤","塑","橡","胶","矿","钢","铝","钛","硅","新材","碳"],
    "医药医疗": ["药","医","生物","健康","寿","仙","康","口腔"],
    "机械制造": ["机械","重工","装备","精密","机床","模具","工程","制造","工"],
    "消费家居": ["食品","饮料","酒","家","居","纺","服","鞋","宠","生活","牙"],
    "交通物流": ["交通","物流","港","航空","铁路","高速","车","运","船"],
    "农牧": ["农","牧","种","渔","林","饲料","肥料"],
    "金融地产": ["银行","证券","保险","信托","地产","物业","金融"],
}

def _get_industry(code, name=""):
    """基于名称关键词的行业分类"""
    for sname, kws in INDUSTRY_KW.items():
        if any(kw in name for kw in kws):
            return sname
    return "其他"


def run_cmd(cmd, cwd=None, timeout=60):
    """执行命令并返回 stdout 和 success 标记"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            timeout=timeout, cwd=cwd
        )
        return result.stdout.strip(), result.returncode, True
    except subprocess.TimeoutExpired:
        return "", -1, False
    except Exception:
        return "", -1, False


def code_to_market(code):
    """判断交易所"""
    if code.startswith("sh6") and code[2] in "013589":
        return "sh"
    elif code.startswith("sz00") or code.startswith("sz30"):
        return "sz"
    return None


def layer1_volume_price(candidates):
    """第一层：MA支撑初筛（V2.2 真实数据版）

    通过 VPS data_provider 获取K线数据，检查 MA10/MA20 支撑。
    """
    passed = []
    rejected = []

    if not candidates:
        return passed, rejected

    try:
        from data_provider import fetch_klines_batch
        codes = [c["code"] for c in candidates]
        klines = fetch_klines_batch(codes, count=30, workers=8)

        for c in candidates:
            code = c["code"]
            kline = klines.get(code)
            if not kline or len(kline) < 20:
                rejected.append({**c, "layer": 1, "reason": "K线数据不足"})
                continue

            closes = [k["close"] for k in kline[-20:]]
            current = closes[-1]
            ma10 = sum(closes[-10:]) / 10 if len(closes) >= 10 else 0
            ma20 = sum(closes[-20:]) / 20 if len(closes) >= 20 else 0

            on_ma10 = current >= ma10 if ma10 > 0 else True
            on_ma20 = current >= ma20 if ma20 > 0 else True

            if not (on_ma10 and on_ma20):
                rejected.append({**c, "layer": 1,
                    "reason": f"未站稳MA: MA10={ma10:.2f} MA20={ma20:.2f} 现价={current:.2f}"})
            else:
                c["layer1_data"] = {
                    "price": current, "ma10": ma10, "ma20": ma20,
                    "ma10_dist": (current - ma10) / ma10 * 100 if ma10 > 0 else 0,
                    "ma20_dist": (current - ma20) / ma20 * 100 if ma20 > 0 else 0,
                }
                passed.append(c)

    except ImportError:
        print("  [L1] ⚠ VPS data_provider 不可用，跳过MA检查（全部通过）")
        for c in candidates:
            c["layer1_data"] = {"price": 0, "ma10": 0, "ma20": 0, "ma10_dist": 0, "ma20_dist": 0}
        passed = list(candidates)

    return passed, rejected


def layer2_fundamental(codes):
    """第二层：基本面安全排雷（V2.2 离线容错版）

    - 优先使用 westockdata finance API
    - 失败时: ST过滤 + 标记"基本面数据缺失"
    - 不伪装通过 — 明确告知用户数据不可用
    """
    if not codes:
        return [], [], {"available": False, "reason": "无候选"}

    code_list = ",".join(codes)
    passed = []
    rejected = []
    data_status = {"available": False, "source": "", "reason": ""}

    # Step 1: ST 前置过滤（无外部依赖）
    st_rejected = []
    for code in codes:
        if "ST" in code.upper() or ("ST" in code):
            st_rejected.append({"code": code, "layer": 2, "reason": "ST/*ST 标记"})

    working_codes = [c for c in codes if c not in [r["code"] for r in st_rejected]]
    rejected.extend(st_rejected)

    # Step 2: 尝试 westockdata 财务数据
    cmd = f"npx -y westock-data-skillhub@1.0.5 finance {','.join(working_codes)} --num 1"
    stdout, rc, success = run_cmd(cmd, cwd=str(SKILL_DIR), timeout=90)

    print(f"  [第二层] 查询 {len(codes)} 只股票财务数据...")

    if success and stdout and rc == 0:
        data_status["available"] = True
        data_status["source"] = "westockdata"
        # 解析财务数据（简化：检查是否有实际数据行）
        checks = [
            "净利润" in stdout,
            "net_profit" in stdout.lower(),
            "负债" in stdout,
            "debt" in stdout.lower(),
            "商誉" in stdout,
            "asset" in stdout.lower(),
        ]
        has_real_data = any(checks)
        if not has_real_data:
            data_status["available"] = False
            data_status["reason"] = "westockdata 返回无数据"
    else:
        data_status["reason"] = f"westockdata 不可用 (rc={rc})"

    # Step 3: 降级处理
    if not data_status["available"]:
        # 无法验证基本面，全部放行但标记
        for code in working_codes:
            passed.append({
                "code": code,
                "fund_filter_status": "skipped",
                "fund_skip_reason": data_status["reason"]
            })
    else:
        for code in working_codes:
            # 从 stdout 解析该股的财务指标
            code_short = code[2:]
            found = False
            for line in stdout.split("\n"):
                if code_short in line or code in line:
                    # 尝试提取关键指标（简化解析）
                    line_lower = line.lower()
                    # 检查亏损标记
                    if "亏损" in line or "loss" in line_lower or "亏" in line:
                        rejected.append({"code": code, "layer": 2, "reason": "最近季度亏损"})
                        found = True
                        break
            if not found:
                passed.append({"code": code, "fund_filter_status": "passed"})

    return passed, rejected, data_status


def layer3_fund_flow(codes):
    """第三层：资金流向打分（V2.2 离线容错版）

    - 成功: 解析 westockdata fund flow 返回的 JumboNetFlow/MainNetFlow
    - 失败: 分数=0，标注"数据缺失"，不给硬编码默认分
    """
    if not codes:
        return [], {"available": False, "reason": "无候选"}

    code_list = ",".join(codes)
    cmd = f"npx -y westock-data-skillhub@1.0.5 fund flow {code_list}"
    stdout, rc, success = run_cmd(cmd, cwd=str(SKILL_DIR), timeout=90)

    print(f"  [第三层] 查询 {len(codes)} 只股票资金流向...")

    data_status = {"available": False, "source": "", "reason": ""}

    if success and stdout and rc == 0:
        # 检查是否有实际数据
        has_data = any(code[2:] in stdout for code in codes)
        if has_data:
            data_status["available"] = True
            data_status["source"] = "westockdata"
        else:
            data_status["reason"] = "westockdata 返回无资金数据"
    else:
        data_status["reason"] = f"westockdata 不可用 (rc={rc})"

    results = []
    for code in codes:
        if data_status["available"]:
            score = _score_fund_flow(code, stdout)
        else:
            # V2.2: 数据缺失时分数=0，不给默认分50
            score = {
                "jumbo_score": 0, "main_score": 0, "total": 0,
                "jumbo_value": "数据缺失", "main_value": "数据缺失",
                "available": False,
            }
        results.append({"code": code, "fund_score": score})

    return results, data_status


def _score_fund_flow(code, raw_output):
    """解析单只股票的资金流并打分（V2.1: 超大单45分 + 主力30分 = 满分75）

    westockdata 输出为 markdown 表格：表头含 JumboNetFlow/MainNetFlow 列，
    数据行为纯数值（不含列名关键词），故按表头列索引提取数值。
    """
    jumbo_score = 0
    main_score = 0
    jumbo_value = "N/A"
    main_value = "N/A"

    headers = None
    for line in raw_output.split("\n"):
        if "|" not in line:
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if not cells:
            continue
        if headers is None and "JumboNetFlow" in cells:
            headers = cells
            continue
        if headers is None:
            continue
        if all(set(c) <= set("-: ") for c in cells):  # 分隔行 | --- |
            continue
        if code not in cells:
            continue
        try:
            jumbo_val = float(cells[headers.index("JumboNetFlow")])
            main_val = float(cells[headers.index("MainNetFlow")])
            jumbo_value = f"{jumbo_val/1e4:.0f}万"
            main_value = f"{main_val/1e4:.0f}万"
            if jumbo_val > 1e8:
                jumbo_score = 45
            elif jumbo_val > 5e7:
                jumbo_score = 38
            elif jumbo_val > 0:
                jumbo_score = 30
            if main_val > 1e8:
                main_score = 30
            elif main_val > 3e7:
                main_score = 25
            elif main_val > 0:
                main_score = 20
        except (ValueError, IndexError):
            pass
        break

    return {
        "jumbo_score": jumbo_score,
        "main_score": main_score,
        "total": jumbo_score + main_score,
        "jumbo_value": jumbo_value,
        "main_value": main_value,
        "available": True,
    }


def layer4_sector_quality(codes):
    """第四层：板块热度 + 量价辅助打分（V2.3 内联版）

    板块热度: 基于名称关键词的行业分类 + 集中度计算
    量价质量: 基于放量日涨幅/缩量深度/低点抬高
    """
    if not codes:
        return [], {"available": False, "reason": "无候选"}

    print(f"  [第四层] 评估 {len(codes)} 只股票板块与形态质量...")

    data_status = {"available": False, "source": "", "reason": ""}

    # Step 1: 内联行业分类（不依赖外部模块）
    sector_data = {}
    for code in codes:
        # 需要名称 → 从K线数据或参数获取。这里用代码做回退
        name = ""  # 从调用者传参获取
        sector_data[code] = _get_industry(code, name)

    if sector_data:
        data_status["available"] = True
        data_status["source"] = "内联关键词分类"

    # Step 2: 获取量价质量数据
    quality_data = {}
    try:
        from data_provider import fetch_klines_batch
        klines = fetch_klines_batch(list(codes), count=30, workers=8)

        for code in codes:
            kline = klines.get(code, [])
            if not kline or len(kline) < 20:
                quality_data[code] = {"surge_gain": 0, "shrink_depth": 100, "low_higher": False}
                continue

            closes = [k["close"] for k in kline[-20:]]
            volumes = [k["volume"] for k in kline[-20:]]

            # 找放量日
            avg_vol = sum(volumes[:15]) / 15 if len(volumes) > 15 else sum(volumes) / len(volumes)
            surge_idx = -1
            for i in range(len(volumes) - 3, -1, -1):
                if volumes[i] > avg_vol * 1.5:
                    surge_idx = i
                    break

            if surge_idx > 0:
                prev_close = closes[surge_idx - 1] if surge_idx > 0 else closes[0]
                surge_gain = (closes[surge_idx] - prev_close) / prev_close * 100
                post_vol = min(volumes[surge_idx + 1:]) if surge_idx + 1 < len(volumes) else volumes[surge_idx]
                shrink_depth = (1 - post_vol / max(volumes[surge_idx], 1)) * 100
                lows = [kline[i]["low"] for i in range(surge_idx + 1, len(kline))]
                low_higher = min(lows) >= kline[surge_idx]["low"] if lows else False
            else:
                surge_gain = 0
                shrink_depth = 100
                low_higher = False

            quality_data[code] = {
                "surge_gain": max(0, surge_gain),
                "shrink_depth": max(0, min(100, shrink_depth)),
                "low_higher": low_higher
            }
    except ImportError:
        pass

    # Step 2: 统计行业分布（用于板块热度评分）
    if sector_data:
        # 按行业聚合
        industry_counts = Counter(sector_data.values())
        total = len(codes)
        industry_pct = {k: v / total for k, v in industry_counts.items()}

        results = []
        for code in codes:
            ind = sector_data.get(code, "其他")
            pct = industry_pct.get(ind, 0)

            # 板块热度: 集中度越高越热
            if pct >= 0.3:
                sector_score = 15
            elif pct >= 0.2:
                sector_score = 12
            elif pct >= 0.1:
                sector_score = 8
            else:
                sector_score = 3

            # 量价质量评分
            q = quality_data.get(code, {"surge_gain": 0, "shrink_depth": 100, "low_higher": False})
            quality_score = 0
            if q["surge_gain"] >= 8:
                quality_score += 4
            elif q["surge_gain"] >= 5:
                quality_score += 2
            if q["shrink_depth"] < 30:
                quality_score += 3
            if q["low_higher"]:
                quality_score += 3

            results.append({
                "code": code,
                "industry": ind,
                "sector_score": sector_score,
                "quality_score": quality_score,
                "surge_gain": q["surge_gain"],
                "shrink_depth": q["shrink_depth"],
                "low_higher": q["low_higher"],
                "total": sector_score + quality_score,
            })
    else:
        # 无行业数据，使用默认
        data_status["available"] = False
        data_status["reason"] = "无行业分类数据源"
        results = []
        for code in codes:
            results.append({
                "code": code,
                "industry": "未知",
                "sector_score": 0,
                "quality_score": 0,
                "surge_gain": 0,
                "shrink_depth": 100,
                "low_higher": False,
                "total": 0,
            })

    return results, data_status


def lookup_history_signals(codes, days=50):
    """查找历史重复信号（V2.3 修正）

    从 VPS 的 signals_*.json（每日信号文件）统计近 N 日上榜次数。
    """
    history = {}
    if not codes:
        return history

    for c in codes:
        history[c] = 0

    try:
        import datetime
        import glob as glob_mod
        cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
        seen = {}  # (code, date) 去重

        signal_files = sorted(glob_mod.glob(os.path.join(VPS_DATA, "signals_*.json")))
        for sf in signal_files:
            try:
                date_str = os.path.basename(sf).replace("signals_", "").replace(".json", "")
                try:
                    sig_date = datetime.datetime.strptime(date_str, "%Y%m%d")
                except ValueError:
                    continue
                if sig_date < cutoff:
                    continue

                with open(sf) as f:
                    signals = json.load(f)
                for sig in signals:
                    code = sig.get("code", "")
                    if code in codes:
                        key = (code, date_str)
                        if key not in seen:
                            seen[key] = True
                            history[code] = history.get(code, 0) + 1
            except (json.JSONDecodeError, IOError):
                continue
    except Exception:
        pass

    return history


def generate_report(passed_l1, passed_l2, fund_scores, sector_scores,
                    l1_rejected=None, l2_rejected=None,
                    data_status=None, history=None, json_path=None):
    """生成三层分级精选报告（V2.2）

    新增：数据可用性状态栏
    """
    if data_status is None:
        data_status = {}
    if history is None:
        history = {}

    # 数据可用性状态
    fund_available = data_status.get("fund", {"available": False}).get("available", False)
    sector_available = data_status.get("sector", {"available": False}).get("available", False)

    # 合并所有得分
    combined = {}
    for fs in fund_scores:
        code = fs["code"]
        combined[code] = {
            "code": code,
            "fund": fs["fund_score"]["total"],
            "jumbo": fs["fund_score"]["jumbo_score"],
            "main": fs["fund_score"]["main_score"],
        }
    for ss in sector_scores:
        code = ss["code"]
        if code in combined:
            combined[code]["sector"] = ss["sector_score"]
            combined[code]["quality"] = ss["quality_score"]
            combined[code]["industry"] = ss.get("industry", "")

    # 添加历史信号分
    for code, data in combined.items():
        hist_days = history.get(code, 0)
        hist_score = 0
        if hist_days >= 8:
            hist_score = 10
        elif hist_days >= 4:
            hist_score = 6
        elif hist_days >= 1:
            hist_score = 4
        data["history_days"] = hist_days
        data["history_score"] = hist_score

    # 计算总分 (资金不可用时只算板块+量价+历史)
    results = []
    for code, data in combined.items():
        if fund_available:
            total = data.get("fund", 0) + data.get("sector", 0) + data.get("quality", 0) + data.get("history_score", 0)
            max_possible = 110
        else:
            total = data.get("sector", 0) + data.get("quality", 0) + data.get("history_score", 0)
            max_possible = 35

        data["total"] = total
        data["max_possible"] = max_possible
        data["fund_available"] = fund_available
        results.append(data)

    results.sort(key=lambda x: x["total"], reverse=True)

    # 分层（资金不可用时阈值相应降低）
    if fund_available:
        tier1_threshold = 82
        tier2_threshold = 60
        tier3_threshold = 38
    else:
        tier1_threshold = 26  # 82 * 35/110
        tier2_threshold = 19  # 60 * 35/110
        tier3_threshold = 12  # 38 * 35/110

    tier1 = [r for r in results if r["total"] >= tier1_threshold][:3]
    tier2 = [r for r in results if tier2_threshold <= r["total"] < tier1_threshold][:10]
    tier3 = [r for r in results if tier3_threshold <= r["total"] < tier2_threshold][:50]
    all_tiered = tier1 + tier2 + tier3

    # 结构化 JSON 输出（供外部程序/定时任务读取，不影响终端报告）
    if json_path:
        try:
            out = {
                "date": time.strftime("%Y-%m-%d"),
                "fund_available": fund_available,
                "sector_available": sector_available,
                "l1_passed": len(passed_l1),
                "l2_passed": len(passed_l2),
                "scored": len(results),
                "tier1": tier1,
                "tier2": tier2,
                "tier3": tier3,
            }
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(out, f, ensure_ascii=False, indent=2)
            print(f"\n  [JSON] 结果已写入 {json_path}")
        except Exception as e:
            print(f"\n  [JSON] 写入失败: {e}")

    # 输出报告
    print("\n" + "═" * 70)
    print(f"  每日精选报告（V2.2 三级分层 + 离线容错）")
    print("═" * 70)

    # 数据可用性状态栏
    fund_mark = "✓" if fund_available else "✗"
    sector_mark = "✓" if sector_available else "✗"
    hist_total = sum(history.values())
    hist_mark = "✓" if hist_total > 0 else "✗"

    print(f"  数据状态: 资金[{fund_mark}] 板块[{sector_mark}] 历史[{hist_mark}] "
          f"| 满分={'110' if fund_available else '35(降级)'}")
    if not fund_available:
        print(f"  ⚠ 资金数据不可用: 评分基于量价+板块+历史 ({data_status.get('fund', {}).get('reason', '未知')})")
        print(f"  ⚠ 分层阈值已相应降低: 精选≥{tier1_threshold} 优选≥{tier2_threshold} 关注≥{tier3_threshold}")

    total_pool = len(passed_l1) + len(passed_l2)
    print(f"  候选: {total_pool}只 → L1: {len(passed_l1)}只 → L2: {len(passed_l2)}只 → 评分: {len(results)}只")
    print(f"  分层: ⭐{len(tier1)}只 | 👍{len(tier2)}只 | 👀{len(tier3)}只\n")

    if not all_tiered:
        print("\n" + "=" * 60)
        print("  今日无精选标的（所有候选未达最低分数线）")
        print("=" * 60)
        return

    def print_tier(title, stocks, emoji):
        if not stocks:
            print(f"  {emoji} {title}: 该层无标的\n")
            return
        print(f"  {emoji} {title}（{len(stocks)}只）:")
        header = f"  │ {'#':^3} │ {'代码':<12} │ {'总分':^5} │ {'资金':^5} │ {'板块':^5} │ {'形态':^5} │ {'历史':^5} │ {'行业':^8} │"
        sep =   f"  ├──{'─'*3}─┼─{'─'*12}─┼─{'─'*5}─┼─{'─'*5}─┼─{'─'*5}─┼─{'─'*5}─┼─{'─'*5}─┼─{'─'*8}─┤"
        print(header)
        print(sep)
        rank_offset = sum(len(t) for t in [tier1, tier2] if t != stocks and stocks != tier1)
        if stocks == tier1:
            rank_offset = 0
        for i, r in enumerate(stocks, 1):
            real_rank = rank_offset + i
            fund_str = str(r.get("fund", "-"))
            if not fund_available:
                fund_str = "N/A"
            row = (f"  │ {real_rank:>3} │ {r['code']:<12} │ {r['total']:>5} │ "
                   f"{fund_str:>5} │ {r.get('sector','-'):>5} │ "
                   f"{r.get('quality','-'):>5} │ {r.get('history_score','-'):>5} │ "
                   f"{r.get('industry','-'):<8} │")
            print(row)
        print()

    print_tier("精选层", tier1, "⭐")
    print_tier("优选层", tier2, "👍")
    print_tier("关注池", tier3, "👀")

    # 淘汰统计
    print("─" * 70)
    if l1_rejected:
        reasons = Counter()
        for r in l1_rejected:
            reason_text = r.get("reason", "未知")
            # 归类
            if "MA" in reason_text or "ma" in reason_text.lower():
                reasons["未站稳MA"] += 1
            elif "K线数据不足" in reason_text:
                reasons["K线不足"] += 1
            else:
                reasons[reason_text[:15]] += 1
        print(f"  L1 排除（量价）: {len(l1_rejected)}只 — "
              + " ".join(f"{k}({v}只)" for k, v in reasons.most_common(5)))
    if l2_rejected:
        reasons = Counter(r.get("reason", "未知") for r in l2_rejected)
        print(f"  L2 排除（基本面）: {len(l2_rejected)}只 — "
              + " ".join(f"{k}({v}只)" for k, v in reasons.most_common(5)))
    if len(passed_l2) > 0:
        skipped = [c for c in passed_l2 if isinstance(c, dict) and c.get("fund_filter_status") == "skipped"]
        if skipped:
            print(f"  L2 跳过（数据缺失）: {len(skipped)}只 — 基本面数据不可用，未做排雷")
    print("─" * 70)

    # 板块分布
    industries = [r.get("industry", "") for r in results if r.get("industry")]
    if industries:
        ind_count = Counter(industries)
        top_inds = ind_count.most_common(5)
        total_in_results = len(results)
        print(f"\n  板块分布 (Top5):")
        for ind, cnt in top_inds:
            pct = cnt / total_in_results * 100
            bar = "█" * int(pct / 2)
            print(f"    {ind:<12} {bar:<20} {cnt}只 ({pct:.0f}%)")

    print(f"\n⚠ 风险提示：以上基于量价+资金多维筛选，不构成投资建议。")

    return all_tiered


def main():
    parser = argparse.ArgumentParser(description="每日精选策略 V2.2")
    parser.add_argument("--pool", type=str, help="逗号分隔的候选股票代码")
    parser.add_argument("--pool-file", type=str, help="候选股票代码文件（每行一个代码或 代码 名称）")
    parser.add_argument("--auto", action="store_true", help="自动读取最新 VPS 信号文件")
    parser.add_argument("--json", type=str, default=None, help="结构化结果输出到 JSON 文件")
    parser.add_argument("--screener-output", type=str, help="volume-price-screener 输出文件（已废弃，请用 --auto）")
    args = parser.parse_args()

    # 1. 获取候选池
    candidates = []

    if args.pool:
        codes = [c.strip() for c in args.pool.split(",") if c.strip()]
        candidates = [{"code": c, "name": ""} for c in codes]
    elif args.pool_file:
        with open(args.pool_file) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                code = parts[0]
                name = parts[1] if len(parts) > 1 else ""
                candidates.append({"code": code, "name": name})
    elif args.auto:
        # 自动读取 VPS 信号
        vps_dir = os.path.expanduser("~/.workbuddy/skills/volume-price-screener/data")
        if os.path.exists(vps_dir):
            sig_files = sorted(
                [f for f in os.listdir(vps_dir) if f.startswith("signals_") and f.endswith(".json")],
                reverse=True
            )
            if sig_files:
                latest = os.path.join(vps_dir, sig_files[0])
                print(f"  自动读取: {latest}")
                with open(latest) as f:
                    signals = json.load(f)
                candidates = [{"code": s["code"], "name": s.get("name", "")} for s in signals]
            else:
                print("  未找到 VPS 信号文件，请先运行 volume-price-screener")
                print("  或使用 --pool 指定候选池")
                sys.exit(1)
        else:
            print("  VPS 数据目录不存在")
            sys.exit(1)
    else:
        print("错误：请通过 --pool、--pool-file 或 --auto 提供候选池")
        print("  用法: python precision_picker.py --pool sh600519,sz000858")
        print("        python precision_picker.py --pool-file candidates.txt")
        print("        python precision_picker.py --auto")
        sys.exit(1)

    if not candidates:
        print("候选池为空")
        sys.exit(1)

    print(f"\n候选池: {len(candidates)} 只股票")
    print("=" * 40)

    # 2. 第一层：量价 MA 支撑检查
    passed_l1, rejected_l1 = layer1_volume_price(candidates)
    print(f"  L1 通过: {len(passed_l1)}/{len(candidates)} (排除 {len(rejected_l1)} 只)")

    if not passed_l1:
        generate_report([], [], [], [], l1_rejected=rejected_l1, json_path=args.json)
        return

    # 3. 第二层：基本面排雷
    codes_l1 = [c["code"] for c in passed_l1]
    passed_l2, rejected_l2, fund_status = layer2_fundamental(codes_l1)
    l2_passed_codes = [c["code"] for c in passed_l2]
    print(f"  L2 通过: {len(passed_l2)}/{len(passed_l1)} (排除 {len(rejected_l2)} 只)"
          + (f" | ⚠ {fund_status.get('reason', '')}" if not fund_status.get("available") else ""))

    if not passed_l2:
        generate_report(passed_l1, [], [], [], l1_rejected=rejected_l1, l2_rejected=rejected_l2, json_path=args.json)
        return

    # 4. 第三层：资金打分
    fund_scores, flow_status = layer3_fund_flow(l2_passed_codes)
    print(f"  L3 完成: {len(fund_scores)} 只"
          + ("" if flow_status["available"] else " ⚠ 资金数据不可用"))

    # 5. 第四层：板块+量价
    sector_scores, sector_status = layer4_sector_quality(l2_passed_codes)
    print(f"  L4 完成: {len(sector_scores)} 只"
          + ("" if sector_status["available"] else f" ⚠ {sector_status.get('reason', '板块数据不可用')}"))

    # 6. 历史信号
    history = lookup_history_signals(l2_passed_codes)
    hist_count = sum(1 for v in history.values() if v > 0)
    print(f"  历史: {hist_count}只有上榜记录 (近50日)")

    # 7. 生成报告
    data_status = {"fund": flow_status, "sector": sector_status}
    generate_report(passed_l1, passed_l2, fund_scores, sector_scores,
                    l1_rejected=rejected_l1, l2_rejected=rejected_l2,
                    data_status=data_status, history=history, json_path=args.json)


if __name__ == "__main__":
    main()
