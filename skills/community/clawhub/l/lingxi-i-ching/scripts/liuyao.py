import argparse
import json
import os
import random
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


TIANGAN = "甲乙丙丁戊己庚辛壬癸"
DIZHI = "子丑寅卯辰巳午未申酉戌亥"
LIUSHEN_ORDER = ["青龙", "朱雀", "勾陈", "腾蛇", "白虎", "玄武"]
WUXING_SHENG = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
WUXING_KE = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}

TRIGRAMS = {
    "111": {"name": "乾", "element": "金", "branches": ["子", "寅", "辰"]},
    "110": {"name": "兑", "element": "金", "branches": ["巳", "卯", "丑"]},
    "101": {"name": "离", "element": "火", "branches": ["卯", "丑", "亥"]},
    "100": {"name": "震", "element": "木", "branches": ["子", "寅", "辰"]},
    "011": {"name": "巽", "element": "木", "branches": ["丑", "亥", "酉"]},
    "010": {"name": "坎", "element": "水", "branches": ["寅", "辰", "午"]},
    "001": {"name": "艮", "element": "土", "branches": ["辰", "午", "申"]},
    "000": {"name": "坤", "element": "土", "branches": ["未", "巳", "卯"]},
}

BRANCH_ELEMENT = {
    "子": "水",
    "丑": "土",
    "寅": "木",
    "卯": "木",
    "辰": "土",
    "巳": "火",
    "午": "火",
    "未": "土",
    "申": "金",
    "酉": "金",
    "戌": "土",
    "亥": "水",
}

MONTH_BRANCH_MAP = ["寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子", "丑"]
SHI_YING_PATTERNS = [(6, 3), (1, 4), (2, 5), (3, 6), (4, 1), (5, 2), (4, 1), (3, 6)]


@dataclass
class LineResult:
    value: int
    is_yang: bool
    is_moving: bool
    display: str


@dataclass
class GuaInfo:
    name: str
    symbol: str
    code: str


@dataclass
class PanLine:
    index: int
    ben: LineResult
    bian_is_yang: bool
    branch: str
    element: str
    liuqin: str
    liushen: str
    is_shi: bool
    is_ying: bool


def coin_toss_line(rng: random.Random) -> LineResult:
    tosses = [3 if rng.randint(0, 1) == 1 else 2 for _ in range(3)]
    total = sum(tosses)
    is_yang = total in (7, 9)
    is_moving = total in (6, 9)
    display_map = {6: "老阴 x", 7: "少阳 ━━━", 8: "少阴 ━ ━", 9: "老阳 o"}
    return LineResult(value=total, is_yang=is_yang, is_moving=is_moving, display=display_map[total])


def build_gua_codes(lines: List[LineResult]) -> Tuple[str, str]:
    ben = "".join("1" if ln.is_yang else "0" for ln in lines)
    bian_bits: List[str] = []
    for ln in lines:
        if ln.value == 6:
            bian_bits.append("1")
        elif ln.value == 9:
            bian_bits.append("0")
        else:
            bian_bits.append("1" if ln.is_yang else "0")
    return ben, "".join(bian_bits)


def load_gua_db(gua_db: Path) -> Dict[str, Dict]:
    if not gua_db.exists():
        return {}
    data = json.loads(gua_db.read_text(encoding="utf-8"))
    return {item.get("gua-xiang"): item for item in data.get("gua", []) if item.get("gua-xiang")}


def gua_symbol(code: str) -> str:
    return "/".join("━━━" if c == "1" else "━ ━" for c in reversed(code))


def get_gua_info(code: str, db: Dict[str, Dict]) -> GuaInfo:
    item = db.get(code, {})
    name = item.get("gua-name", f"卦码{code}")
    return GuaInfo(name=name, symbol=gua_symbol(code), code=code)


def calc_day_ganzhi(dt: datetime) -> Tuple[str, int]:
    base = datetime(1984, 2, 2)
    idx = (dt.date() - base.date()).days % 60
    return TIANGAN[idx % 10] + DIZHI[idx % 12], idx


def calc_month_jian(dt: datetime) -> str:
    return MONTH_BRANCH_MAP[(dt.month - 1) % 12]


def calc_kongwang(day60_index: int) -> Tuple[str, str]:
    xun_idx = day60_index // 10
    start_branch_idx = (12 - (2 * xun_idx)) % 12
    e1 = DIZHI[(start_branch_idx - 2) % 12]
    e2 = DIZHI[(start_branch_idx - 1) % 12]
    return e1, e2


def trigram_of(code3: str) -> Dict[str, object]:
    return TRIGRAMS[code3]


def palace_element(ben_code: str) -> str:
    # 专业版简化：以本卦下卦为宫
    lower = ben_code[:3]
    return str(trigram_of(lower)["element"])


def liuqin_from_element(self_element: str, target_element: str) -> str:
    if self_element == target_element:
        return "兄弟"
    if WUXING_SHENG[self_element] == target_element:
        return "子孙"
    if WUXING_SHENG[target_element] == self_element:
        return "父母"
    if WUXING_KE[self_element] == target_element:
        return "妻财"
    return "官鬼"


def assign_liushen(day_gan: str) -> List[str]:
    start_map = {
        "甲": "青龙",
        "乙": "青龙",
        "丙": "朱雀",
        "丁": "朱雀",
        "戊": "勾陈",
        "己": "腾蛇",
        "庚": "白虎",
        "辛": "白虎",
        "壬": "玄武",
        "癸": "玄武",
    }
    start = start_map.get(day_gan, "青龙")
    offset = LIUSHEN_ORDER.index(start)
    return [LIUSHEN_ORDER[(offset + i) % 6] for i in range(6)]


def assign_shi_ying(ben_code: str, bian_code: str) -> Tuple[int, int]:
    diff = sum(1 for i in range(6) if ben_code[i] != bian_code[i])
    shi, ying = SHI_YING_PATTERNS[diff if diff < len(SHI_YING_PATTERNS) else 0]
    return shi, ying


def na_jia_branches(ben_code: str) -> List[str]:
    lower = trigram_of(ben_code[:3])["branches"]
    upper = trigram_of(ben_code[3:])["branches"]
    return list(lower) + list(upper)


def compose_pan(
    ben_lines: List[LineResult],
    ben_code: str,
    bian_code: str,
    day_gz: str,
) -> List[PanLine]:
    self_ele = palace_element(ben_code)
    branches = na_jia_branches(ben_code)
    liushen = assign_liushen(day_gz[0])
    shi, ying = assign_shi_ying(ben_code, bian_code)
    out: List[PanLine] = []
    for i in range(6):
        branch = branches[i]
        element = BRANCH_ELEMENT[branch]
        out.append(
            PanLine(
                index=i + 1,
                ben=ben_lines[i],
                bian_is_yang=(bian_code[i] == "1"),
                branch=branch,
                element=element,
                liuqin=liuqin_from_element(self_ele, element),
                liushen=liushen[i],
                is_shi=(i + 1 == shi),
                is_ying=(i + 1 == ying),
            )
        )
    return out


def choose_yongshen(question: str) -> str:
    q = question or ""
    if any(k in q for k in ("钱", "财", "收入", "投资", "回款", "薪资")):
        return "妻财"
    if any(k in q for k in ("工作", "职位", "面试", "事业", "考试", "晋升", "官司")):
        return "官鬼"
    if any(k in q for k in ("学习", "文书", "证件", "合同", "房产", "手续")):
        return "父母"
    if any(k in q for k in ("健康", "治疗", "平安", "疾病", "怀孕")):
        return "子孙"
    if any(k in q for k in ("朋友", "合作", "兄弟", "同事", "竞争")):
        return "兄弟"
    return "父母"


def relation_score(src_element: str, target_element: str) -> int:
    if src_element == target_element:
        return 6
    if WUXING_SHENG[src_element] == target_element:
        return 8
    if WUXING_SHENG[target_element] == src_element:
        return -6
    if WUXING_KE[src_element] == target_element:
        return -3
    return -10


def judge_pro(
    pan_lines: List[PanLine],
    yongshen: str,
    month_branch: str,
    day_branch: str,
    kongwang: Tuple[str, str],
) -> Tuple[str, Dict[str, object]]:
    candidates = [ln for ln in pan_lines if ln.liuqin == yongshen]
    month_ele = BRANCH_ELEMENT[month_branch]
    day_ele = BRANCH_ELEMENT[day_branch]
    empty_set = {kongwang[0], kongwang[1]}

    if not candidates:
        return (f"用神{yongshen}伏藏未透，信息不足，宜再择时复占。旬空：{kongwang[0]}{kongwang[1]}", {"score": 35})

    best_score = -999
    best_line: Optional[PanLine] = None
    trace: List[str] = []

    for ln in candidates:
        score = 50
        score += relation_score(month_ele, ln.element)
        score += relation_score(day_ele, ln.element) // 2

        if ln.branch == month_branch:
            score += 10
            trace.append(f"{ln.index}爻临月建+10")
        if ln.branch == day_branch:
            score += 8
            trace.append(f"{ln.index}爻临日辰+8")
        if ln.branch in empty_set:
            score -= 15
            trace.append(f"{ln.index}爻旬空-15")
        if ln.ben.is_moving:
            score += 9
            trace.append(f"{ln.index}爻用神发动+9")
            changed_ele = "阳" if ln.bian_is_yang else "阴"
            if changed_ele == "阳":
                score += 2
            else:
                score -= 1

        if ln.is_shi:
            score += 6
            trace.append(f"{ln.index}爻持世+6")
        if ln.is_ying:
            score -= 2
            trace.append(f"{ln.index}爻临应-2")

        if score > best_score:
            best_score = score
            best_line = ln

    move_count = sum(1 for ln in pan_lines if ln.ben.is_moving)
    if move_count >= 4:
        best_score -= 5
        trace.append("动爻过多，局势反复-5")
    elif move_count == 0:
        best_score -= 3
        trace.append("全静卦，推进偏慢-3")

    if best_score >= 68:
        level = "吉势偏强"
        text = "用神得势，主线可成，宜主动推进。"
    elif best_score >= 55:
        level = "中平可为"
        text = "可做但要控节奏，先稳关键节点。"
    elif best_score >= 45:
        level = "阻力偏大"
        text = "外部牵制较强，先补条件再行动。"
    else:
        level = "谨慎观望"
        text = "时机未熟，宜暂缓重大决策。"

    assert best_line is not None
    judgment = (
        f"{level}。用神{yongshen}在{best_line.index}爻（{best_line.branch}{best_line.element}）"
        f"，评分{best_score}。{text}旬空：{kongwang[0]}{kongwang[1]}"
    )
    return judgment, {"score": best_score, "trace": trace, "best_line": best_line.index}


def plain_advice(judgment: str, score: int) -> str:
    if score >= 68:
        return "现在是可执行窗口期，建议马上做计划拆解并推进第一步。"
    if score >= 55:
        return "先做低风险试探，再逐步加码，关键节点要留缓冲。"
    if score >= 45:
        return "先补资源、人脉或信息，再决定是否正式启动。"
    return "不宜硬推，先观察一到两个周期，等待条件转强。"


def llm_advice(question: str, ben: GuaInfo, bian: GuaInfo, judgment: str, model: str) -> Optional[str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    try:
        from openai import OpenAI  # type: ignore

        client = OpenAI(api_key=api_key)
        prompt = (
            "你是专业六爻咨询师。请把断语转成具体可执行建议，"
            "不要神化，不要绝对化，80-120字。\n"
            f"问题：{question}\n本卦：{ben.name}({ben.code})\n变卦：{bian.name}({bian.code})\n断语：{judgment}\n"
        )
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "擅长将传统术语转化为现实行动建议。"},
                {"role": "user", "content": prompt},
            ],
            temperature=0.6,
        )
        return (resp.choices[0].message.content or "").strip() or None
    except Exception:
        return None


def save_history(history_path: Path, payload: Dict[str, object]) -> None:
    history_path.parent.mkdir(parents=True, exist_ok=True)
    with history_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def print_board(ben: GuaInfo, bian: GuaInfo, judgment: str, advice: str) -> None:
    print("┌─────────────────────────────────┐")
    print("│ 六爻占卜结果                    │")
    print("├─────────────────────────────────┤")
    print(f"│ 本卦：{ben.name} {ben.symbol}")
    print(f"│ 变卦：{bian.name} {bian.symbol}")
    print("├─────────────────────────────────┤")
    print(f"│ 断卦：{judgment}")
    print("├─────────────────────────────────┤")
    print(f"│ 建议：{advice}")
    print("└─────────────────────────────────┘")


def print_detail(pan_lines: List[PanLine]) -> None:
    print("\n六爻明细（上->下）")
    for i in range(5, -1, -1):
        ln = pan_lines[i]
        marks = []
        if ln.is_shi:
            marks.append("世")
        if ln.is_ying:
            marks.append("应")
        mark = "".join(marks) if marks else "  "
        bian_txt = "━━━" if ln.bian_is_yang else "━ ━"
        print(
            f"{ln.index}爻 {mark} 本:{ln.ben.display:6s} 变:{bian_txt:3s} "
            f"{ln.liuqin:2s} {ln.liushen} {ln.branch}{ln.element}"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="六爻起卦与断卦工具（专业版规则引擎）")
    parser.add_argument("--question", default="", help="占问主题")
    parser.add_argument("--seed", type=int, default=None, help="随机种子")
    parser.add_argument("--llm", action="store_true", help="启用LLM建议")
    parser.add_argument("--model", default="gpt-4o-mini", help="LLM模型名")
    parser.add_argument("--history", default=".cursor/skills/liuyao-divination/history.jsonl", help="历史记录文件")
    parser.add_argument("--gua-db", default="gua.json", help="卦库JSON路径")
    args = parser.parse_args()

    rng = random.Random(args.seed)
    lines = [coin_toss_line(rng) for _ in range(6)]
    ben_code, bian_code = build_gua_codes(lines)

    db = load_gua_db(Path(args.gua_db))
    ben = get_gua_info(ben_code, db)
    bian = get_gua_info(bian_code, db)

    now = datetime.now()
    day_gz, day60_idx = calc_day_ganzhi(now)
    month_branch = calc_month_jian(now)
    kongwang = calc_kongwang(day60_idx)
    pan_lines = compose_pan(lines, ben_code, bian_code, day_gz)
    yongshen = choose_yongshen(args.question)
    judgment, judge_meta = judge_pro(pan_lines, yongshen, month_branch, day_gz[1], kongwang)
    score = int(judge_meta["score"])
    advice = plain_advice(judgment, score)

    if args.llm:
        enhanced = llm_advice(args.question, ben, bian, judgment, args.model)
        if enhanced:
            advice = enhanced

    print_board(ben, bian, judgment, advice)
    print(
        f"\n时间：{now.strftime('%Y-%m-%d %H:%M:%S')}  月建：{month_branch}月  日辰：{day_gz}  旬空：{kongwang[0]}{kongwang[1]}"
    )
    print(f"问题：{args.question or '未提供'}  用神：{yongshen}  评分：{score}")
    print_detail(pan_lines)
    if judge_meta.get("trace"):
        print("断卦依据：" + "；".join(judge_meta["trace"]))  # type: ignore[arg-type]

    save_history(
        Path(args.history),
        {
            "ts": now.isoformat(),
            "question": args.question,
            "ben_gua": {"name": ben.name, "code": ben.code},
            "bian_gua": {"name": bian.name, "code": bian.code},
            "day_ganzhi": day_gz,
            "month_jian": month_branch,
            "kongwang": f"{kongwang[0]}{kongwang[1]}",
            "yongshen": yongshen,
            "judgment": judgment,
            "score": score,
            "advice": advice,
            "judge_trace": judge_meta.get("trace", []),
            "lines": [
                {
                    "line": ln.index,
                    "value": ln.ben.value,
                    "moving": ln.ben.is_moving,
                    "yin_yang": "阳" if ln.ben.is_yang else "阴",
                    "bian_yin_yang": "阳" if ln.bian_is_yang else "阴",
                    "branch": ln.branch,
                    "element": ln.element,
                    "liuqin": ln.liuqin,
                    "liushen": ln.liushen,
                    "shi": ln.is_shi,
                    "ying": ln.is_ying,
                }
                for ln in pan_lines
            ],
        },
    )


if __name__ == "__main__":
    main()
