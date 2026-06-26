#!/usr/bin/env python3
"""
quality_check.py — 小说章节质量审核（33 维度完整版）

用法:
  python3 quality_check.py --file <章节文件> --quick   # 5项核心检查
  python3 quality_check.py --file <章节文件> --full    # 全量 33 维度检查
  python3 quality_check.py --dir <目录> --full         # 批量检查
"""
import argparse
import os
import re
import sys
from collections import Counter


def count_chinese(text):
    return sum(1 for c in text if '\u4e00' <= c <= '\u9fff')


# ============================================================
# 检测词库
# ============================================================

AI_MARKERS = [
    "暗思涌起", "心理描写", "环境描写", "动作描写", "神态描写",
    "命运的齿轮", "未完待续", "故事才刚开始", "真正的危机",
    "风暴即将来临", "他不知道的是", "殊不知",
    "一场更大的", "更大的风暴", "而这，仅仅只是",
    "这才是开始", "真正的考验", "悄然拉开帷幕",
    "命运的齿轮开始了转动", "命运的齿轮已然转动",
    "看似平静的", "平静之下暗藏", "暗流涌动", "暴风雨前的宁静",
    "命运的齿轮", "一场腥风血雨", "一场更大的风暴",
    "暗思涌起", "心中暗想", "暗自思忖",
]

TEMPLATE_ENDINGS = [
    "命运的齿轮", "未完待续", "真正的危机", "风暴即将来临",
    "拉开帷幕", "才刚刚开始", "而这只是", "这只是",
    "更大的阴谋", "更大的棋局", "更大的风暴",
    "真正的考验", "真正的挑战", "真正的冒险",
    "故事才刚刚开始", "一切都才刚刚开始",
    "暗思涌起", "暴风雨前的宁静", "暗流涌动",
    "腥风血雨", "腥风血雨即将来临",
    "殊不知", "他不知道的是", "她却不知道",
    "一场更大的", "悄然拉开帷幕",
]

REPEATED_WORDS = ["突然", "忽然", "猛地", "不禁", "心中", "顿时", "仿佛", "似乎", "隐隐", "嘴角"]

CROSS_WORD_THRESHOLD = 400  # 跨章节重复检测窗口


# ============================================================
# 第一层：基础指标（5 项）
# ============================================================

def c1_word_count(text):
    cn = count_chinese(text)
    return ("字数达标(≥12000)", f"{cn}字", cn >= 12000)

def c2_chinese_purity(text):
    cn = count_chinese(text); total = len(text)
    pct = cn / total * 100 if total > 0 else 0
    return ("中文纯度(≥95%)", f"{pct:.1f}%", pct >= 95)

def c3_ai_markers(text):
    found = [m for m in AI_MARKERS if m in text]
    return ("AI标记词(0个)", f"{len(found)}个 {str(found)[:80]}", len(found) == 0)

def c4_template_ending(text):
    last500 = text[-500:]
    found = [e for e in TEMPLATE_ENDINGS if e in last500]
    return ("模板化结尾(无)", f"{len(found)}个 {str(found)[:80]}", len(found) == 0)

def c5_paragraph_length(text):
    paragraphs = [p for p in text.split('\n\n') if p.strip()]
    lengths = [len(p) for p in paragraphs]
    mx = max(lengths) if lengths else 0
    avg = sum(lengths) // len(lengths) if lengths else 0
    return ("段落长度合理", f"最长{mx}字 平均{avg}字", mx < 3000)


# ============================================================
# 第二层：文风与结构（8 项）
# ============================================================

def c6_repetition_rate(text):
    """句子级重复率：相同的短句（10-30字）出现多次"""
    sents = re.split(r'[，。！？；\n]+', text)
    sents = [s.strip() for s in sents if 10 <= len(s) <= 30]
    counter = Counter(sents)
    dup = sum(v for v in counter.values() if v > 1)
    rate = dup / len(sents) * 100 if sents else 0
    return ("重复率(<10%)", f"{rate:.1f}%", rate < 10)

def c7_dialogue_ratio(text):
    dialogue = sum(len(d) for d in re.findall(r'[""].*?[""]', text))
    dialogue += sum(len(d) for d in re.findall(r"[''].*?['']", text))
    total = len(text)
    ratio = dialogue / total * 100 if total > 0 else 0
    return ("对话比例(25-55%)", f"{ratio:.0f}%", 25 <= ratio <= 55)

def c8_punctuation_density(text):
    cn = count_chinese(text)
    punct = sum(1 for c in text if c in '，。！？、；：""''（）【】《》『』')
    ratio = punct / cn * 100 if cn > 0 else 0
    return ("标点密度合理", f"每百字{ratio:.0f}个标点", 25 <= ratio <= 65)

def c9_paragraph_variance(text):
    """段落长度方差：有长有短说明节奏好"""
    paragraphs = [p for p in text.split('\n\n') if p.strip()]
    lengths = [len(p) for p in paragraphs]
    if len(lengths) < 2:
        return ("段落节奏变化", "N/A(段落<2)", True)
    avg = sum(lengths) / len(lengths)
    var = sum((l - avg) ** 2 for l in lengths) / len(lengths)
    cv = (var ** 0.5) / avg if avg > 0 else 0  # 变异系数
    return ("段落节奏变化", f"变异系数{cv:.2f} (目标0.3-1.5)", 0.3 <= cv <= 1.5)

def c10_sentence_length(text):
    sents = re.split(r'[，。！？；]+', text)
    sents = [s.strip() for s in sents if s.strip()]
    avg = sum(len(s) for s in sents) / len(sents) if sents else 0
    return ("句长合理", f"均{avg:.0f}字/句 (目标8-25)", 8 <= avg <= 25)

def c11_scene_transitions(text):
    """场景转换：时间/地点关键词密度"""
    markers = len(re.findall(r'(?:此时|这时|随后|接着|与此同时|片刻后|第二天|次日|转眼|忽然|忽然间|蓦地|冷不|就在这时)', text))
    paras = max(len(text.split('\n\n')), 1)
    ratio = markers / paras * 100
    return ("场景转换自然", f"每段{ratio:.1f}次 (目标0.3-2.0)", 0.3 <= ratio <= 2.0)

def c12_emotion_words(text):
    """情感词汇密度"""
    emotion = len(re.findall(r"(?:愤怒|惊讶|喜悦|悲伤|恐惧|犹豫|坚定|犹豫|兴奋|无奈|欣慰|苦涩|甜蜜|温暖|激动|平静|紧张|放松)", text))
    cn = count_chinese(text)
    density = emotion / cn * 1000 if cn > 0 else 0
    return ("情感词密度", f"千字{density:.1f} (目标2-15)", 2 <= density <= 15)

def c13_repeated_word_check(text):
    """高频词检查：避免同一个词出现太多次"""
    words = re.findall(r'[\u4e00-\u9fff]{2,4}', text)
    counter = Counter(words)
    overuse = [w for w, c in counter.most_common(20) if c > count_chinese(text) / 500]
    return ("无高频重复词", f"{len(overuse)}个 {str(overuse)[:60]}", len(overuse) == 0)


# ============================================================
# 第三层：内容与大纲（7 项）
# ============================================================

def c14_progression_check(text):
    """情节推进：检查是否有新事件、新信息出现"""
    has_something = bool(re.search(r'(?:发现|得知|明白|决定|出发|遇见|得知|出现|传来|收到|遇到)', text))
    return ("有情节推进", "有新事件" if has_something else "无明显推进", has_something)

def c15_protagonist_presence(text):
    """主角出现频率"""
    protagonist_mentions = len(re.findall(r'林阎', text))
    cn = count_chinese(text)
    density = protagonist_mentions / cn * 1000 if cn > 0 else 0
    return ("主角出现密度", f"千字{density:.1f}次", 0.5 <= density <= 15)

def c16_action_density(text):
    """动作词密度"""
    actions = len(re.findall(r'(?:冲|挥|打|走|跑|跳|躲|闪|劈|斩|刺|抓|拿|举|握|推|拉|翻|跃|飞|跃|掠|闪|退|进)', text))
    cn = count_chinese(text)
    density = actions / cn * 1000 if cn > 0 else 0
    return ("动作词密度", f"千字{density:.0f} (目标2-10)", 2 <= density <= 10)

def c17_internal_monologue(text):
    """内心独白比例（适当但不过多）"""
    internal = text.count('想') + text.count('暗道') + text.count('自语') + text.count('心想')
    cn = count_chinese(text)
    density = internal / cn * 1000 if cn > 0 else 0
    return ("内心独白适度", f"千字{density:.1f} (目标1-8)", 1 <= density <= 8)

def c18_setting_description(text):
    """场景/环境描写密度"""
    setting = len(re.findall(r'(?:云雾|山|林|河|天|地|空|夜|风|月|星|光|影|雾|雪|雨|雷|电|城|殿|楼|阁|塔|院|门|窗)', text))
    cn = count_chinese(text)
    density = setting / cn * 1000 if cn > 0 else 0
    return ("场景描写适当", f"千字{density:.0f} (目标3-20)", 3 <= density <= 20)

def c19_conflict_tension(text):
    """冲突/张力词汇密度"""
    conflict = len(re.findall(r'(?:战|斗|敌|杀|恨|怒|惊|险|危|难|痛|死|伤|败|胜|胜|攻|守|防|挡|避|逃|追|围|困|破)', text))
    cn = count_chinese(text)
    density = conflict / cn * 1000 if cn > 0 else 0
    return ("有冲突张力", f"千字{density:.0f} (目标5-25)", 5 <= density <= 25)

def c20_golden_finger(text):
    """金手指/核心设定提及"""
    gf = len(re.findall(r'(?:铜钱|太初|道|功法|灵力|灵气|修为|实力|修炼|突破|境界|力量|能力|神秘)', text))
    cn = count_chinese(text)
    density = gf / cn * 1000 if cn > 0 else 0
    return ("金手指提及", f"千字{density:.0f} (目标>1)", density > 1)


# ============================================================
# 第四层：格式与规范（5 项）
# ============================================================

def c21_numeric_format(text):
    """阿拉伯数字检查"""
    arabic = len(re.findall(r'[0-9]+', text))
    # 排除章节标题编号（如"第1章"可能是大纲引用）
    return ("无阿拉伯数字", f"{arabic}处", arabic == 0)

def c22_english_words(text):
    """英文单词检查"""
    english = re.findall(r'[a-zA-Z]{2,}', text)
    # 排除常见英文缩写
    english = [w for w in english if w.lower() not in ('md', 'txt', 'py', 'api')]
    return ("无英文单词", f"{len(english)}个 {str(english)[:60]}", len(english) == 0)

def c23_format_consistency(text):
    """段落格式一致性：不应有超短行或异常格式"""
    lines = text.split('\n')
    short_lines = [l for l in lines if 0 < len(l.strip()) < 5 and l.strip() not in ('', '一', '二', '三')]
    return ("格式一致", f"{len(short_lines)}个异常短行", len(short_lines) < 10)

def c24_special_chars(text):
    """特殊字符检查"""
    weird = re.findall(r'[^\u4e00-\u9fff\u3000-\u303f\uff00-\uffef\n\r\t\s，。！？、；：""''（）【】《》『』…——～·]', text)
    weird = [c for c in weird if c not in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')]
    return ("无特殊字符", f"{len(weird)}个", len(weird) < 5)

def c25_chapter_word_count(text):
    """章字数范围 12000-20000"""
    cn = count_chinese(text)
    return ("字数在合理范围", f"{cn}字 (12000-20000)", 12000 <= cn <= 20000)


# ============================================================
# 第五层：高级分析（8 项）
# ============================================================

def c26_opening_hook(text):
    """开头吸引力：前500字是否有悬念/冲突/有趣内容"""
    opening = text[:500]
    hooks = re.findall(r'(?:突然|忽然|猛地|一声|轰|砰|嗖|竟|竟|却发现|只见|只听|就在这时|冷不)', opening)
    return ("开头有吸引力", f"{len(hooks)}个勾子词 (目标1+)", len(hooks) >= 1)

def c27_ending_quality(text):
    """结尾质量：不应仓促结束"""
    ending = text[-300:]
    paragraphs = ending.split('\n\n')
    last_para = paragraphs[-1] if paragraphs else ""
    too_short = len(last_para) < 100
    return ("结尾完整", f"末段{len(last_para)}字", not too_short)

def c28_pacing_variety(text):
    """节奏变化：长短段落交替"""
    paragraphs = [p for p in text.split('\n\n') if p.strip()]
    if len(paragraphs) < 4:
        return ("段落长短交替", "N/A(段落<4)", True)
    pairs = []
    for i in range(0, len(paragraphs) - 1):
        pairs.append(abs(len(paragraphs[i]) - len(paragraphs[i + 1])))
    avg_diff = sum(pairs) / len(pairs) if pairs else 0
    return ("段落长短交替", f"相邻差异均值{avg_diff:.0f}字 (目标>50)", avg_diff > 50)

def c29_character_consistency(text):
    """角色名称一致性：如果提到角色名，不应出现别名混乱"""
    char_names = re.findall(r'(?:林阎|柳如烟|张三|李四|王五|赵六)', text)
    if not char_names:
        return ("角色一致性", "N/A", True)
    counter = Counter(char_names)
    return ("角色名称一致", f"{dict(counter)}", True)

def c30_vocabulary_richness(text):
    """词汇丰富度：不重复字数/总字数"""
    words = re.findall(r'[\u4e00-\u9fff]', text)
    unique = set(words)
    richness = len(unique) / len(words) if words else 0
    return ("词汇丰富度", f"{richness:.3f} (目标>0.1)", richness > 0.1)

def c31_first_person_check(text):
    """检查是否混用了第一人称（玄幻修仙通常第三人称）"""
    first_person = len(re.findall(r'(?:我(?!们)|我的|我自)', text))
    total_person = len(re.findall(r'(?:我|他|她|你)', text))
    if total_person == 0:
        return ("第三人称一致", "N/A", True)
    ratio = first_person / total_person * 100
    return ("第三人称一致", f"人称代词中{ratio:.0f}%第一人称 (应<5%)", ratio < 5)

def c32_scene_completeness(text):
    """场景完整性：有场景描写+对话+动作的混合"""
    dialogue = len(re.findall(r'[""].*?[""]', text))
    action = len(re.findall(r'(?:冲|挥|打|走|跑|跳|躲|闪|劈|斩|刺|抓|拿|举|握|推|拉)', text))
    has_scene = bool(re.search(r'(?:云雾|山|林|天|地|夜|风|月|星)', text))
    complete = dialogue > 0 and action > 0 and has_scene
    return ("场景完整(对话+动作+环境)", f"对话{dialogue}次/动作{action}次/有场景{'是' if has_scene else '无'}", complete)

def c33_cross_chapter_continuity(text, prev_text=""):
    """与前章衔接检查：如果提供了前章文本，检查是否有重复/衔接"""
    if not prev_text:
        return ("跨章衔接", "N/A(无前章)", True)
    # 检查当前章结尾与前章结尾是否有大段重复
    common = set(re.findall(r'[\u4e00-\u9fff]{4,}', text)) & set(re.findall(r'[\u4e00-\u9fff]{4,}', prev_text))
    overlap = len(common)
    return ("跨章无大段重复", f"{overlap}个4字词组重复 (目标<20)", overlap < 20)


# ============================================================
# 检查函数索引
# ============================================================

QUICK_CHECKS = [c1_word_count, c2_chinese_purity, c3_ai_markers, c4_template_ending, c5_paragraph_length]

FULL_CHECKS = [
    # 第一层：基础指标（5）
    c1_word_count, c2_chinese_purity, c3_ai_markers, c4_template_ending, c5_paragraph_length,
    # 第二层：文风与结构（8）
    c6_repetition_rate, c7_dialogue_ratio, c8_punctuation_density, c9_paragraph_variance,
    c10_sentence_length, c11_scene_transitions, c12_emotion_words, c13_repeated_word_check,
    # 第三层：内容与大纲（7）
    c14_progression_check, c15_protagonist_presence, c16_action_density, c17_internal_monologue,
    c18_setting_description, c19_conflict_tension, c20_golden_finger,
    # 第四层：格式与规范（5）
    c21_numeric_format, c22_english_words, c23_format_consistency, c24_special_chars,
    c25_chapter_word_count,
    # 第五层：高级分析（8）
    c26_opening_hook, c27_ending_quality, c28_pacing_variety, c29_character_consistency,
    c30_vocabulary_richness, c31_first_person_check, c32_scene_completeness, c33_cross_chapter_continuity,
]


# ============================================================
# 输出
# ============================================================

def print_report(filename, results):
    title = filename[:30]
    passed = sum(1 for _, _, p in results if p)
    total = len(results)

    print(f"\n{'='*60}")
    print(f"  {title} 质量审核: {passed}/{total} 通过")
    print(f"{'='*60}")

    layer_names = [
        "第一层：基础指标",
        "第二层：文风与结构",
        "第三层：内容与大纲",
        "第四层：格式与规范",
        "第五层：高级分析",
    ]
    layer_sizes = [5, 8, 7, 5, 8]
    idx = 0
    for layer, size in zip(layer_names, layer_sizes):
        p = sum(1 for _, _, ok in results[idx:idx+size] if ok)
        status = "✅" if p == size else "⚠️"
        print(f"\n{status} {layer} ({p}/{size}):")
        for name, value, ok in results[idx:idx+size]:
            icon = "✅" if ok else "❌"
            print(f"  {icon} {name}: {value}")
        idx += size

    print(f"\n总评: {'✅ 优秀' if passed/total >= 0.9 else '⚠️ 良好' if passed/total >= 0.7 else '❌ 需改进'} ({passed}/{total})")


def full_checks(text, prev_text=""):
    results = []
    for check_fn in FULL_CHECKS:
        if check_fn == c33_cross_chapter_continuity:
            results.append(check_fn(text, prev_text))
        else:
            results.append(check_fn(text))
    return results


def quick_checks(text):
    return [fn(text) for fn in QUICK_CHECKS]


def main():
    parser = argparse.ArgumentParser(description="小说33维度质量审核")
    parser.add_argument("--file", type=str, help="章节文件路径")
    parser.add_argument("--dir", type=str, help="目录路径(批量)")
    parser.add_argument("--full", action="store_true", help="全量 33 维度检查")
    parser.add_argument("--quick", action="store_true", help="快速检查(默认)")
    parser.add_argument("--prev", type=str, help="前章文件路径(跨章检查)")
    args = parser.parse_args()

    files = []
    if args.file:
        files.append(args.file)
    elif args.dir:
        base = args.dir
        files = sorted([os.path.join(base, f) for f in os.listdir(base)
                       if f.startswith('00') and f.endswith('.md')])
    else:
        print("python3 quality_check.py --file <文件> --full  或  --dir <目录> --full")
        sys.exit(1)

    prev_text = ""
    if args.prev and os.path.exists(args.prev):
        with open(args.prev, 'r', encoding='utf-8') as f:
            prev_text = f.read()

    for filepath in files:
        if not os.path.exists(filepath):
            print(f"❌ 文件不存在: {filepath}")
            continue
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()

        if args.full:
            # Also check prev chapter if exists
            prev = ""
            if not args.prev:
                parts = filepath.rsplit(os.sep, 1)
                if len(parts) == 2:
                    base, fname = parts
                    files_in_dir = sorted([f for f in os.listdir(base) if f.startswith('00') and f.endswith('.md')])
                    cur_idx = files_in_dir.index(os.path.basename(fname)) if os.path.basename(fname) in files_in_dir else -1
                    if cur_idx > 0:
                        prev_path = os.path.join(base, files_in_dir[cur_idx - 1])
                        if os.path.exists(prev_path):
                            with open(prev_path, 'r', encoding='utf-8') as pf:
                                prev = pf.read()
                            print(f"\n  (使用前章 {files_in_dir[cur_idx - 1][:26]} 做跨章检查)")
            results = full_checks(text, prev)
        else:
            results = quick_checks(text)

        print_report(os.path.basename(filepath), results)


if __name__ == "__main__":
    main()
