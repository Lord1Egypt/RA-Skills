#!/usr/bin/env python3
"""
Persona Forge Analyzer — 人格分析引擎

用法：
  python3 analyzer.py characters <input_file>          识别文本中所有角色
  python3 analyzer.py fragments <input_file> --character "名字"   提取角色相关片段
  python3 analyzer.py model <input_file> --character "名字"       对指定角色进行人格建模
"""

import json
import sys
import os
import re
from pathlib import Path
from collections import Counter


# ============================================================
# 文本解析模块
# ============================================================

def load_text(source_path):
    """加载文本文件，返回纯文本内容"""
    path = Path(source_path)
    if not path.exists():
        print(f"❌ 文件不存在: {source_path}")
        sys.exit(1)

    suffix = path.suffix.lower()

    if suffix == ".txt" or suffix == ".md":
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    elif suffix == ".json":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, str):
            return data
        elif isinstance(data, list):
            return "\n".join(str(item) for item in data)
        elif isinstance(data, dict):
            return json.dumps(data, ensure_ascii=False, indent=2)
    elif suffix == ".pdf":
        return load_pdf(path)
    else:
        print(f"⚠️ 不支持的格式: {suffix}，尝试作为纯文本读取")
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()


def load_pdf(path):
    """加载 PDF 文件（需要 pdfplumber）"""
    try:
        import pdfplumber
        text_parts = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        return "\n".join(text_parts)
    except ImportError:
        print("❌ PDF 解析需要 pdfplumber: pip install pdfplumber==0.11.9")
        sys.exit(1)


# ============================================================
# 角色识别模块
# ============================================================

def extract_characters(text):
    """
    从文本中识别角色。
    策略：
    1. 剧本格式：角色名：对白（如 "周朴园："）
    2. 引号格式："XXX说" / XXX道
    3. 称谓模式：XX的父亲、XX的哥哥 等
    4. 人名模式：中文姓名（2-4字）
    """
    characters = {}

    # 策略1：剧本对白格式（角色名： 或 角名：）
    drama_pattern = re.findall(r'^([A-Za-z\u4e00-\u9fff]{2,8})[：:]', text, re.MULTILINE)
    for name in drama_pattern:
        name = name.strip()
        if len(name) >= 2 and name not in {"注意", "说明", "备注", "标题", "序号"}:
            characters.setdefault(name, {"mentions": 0, "source": "剧本对白"})
            characters[name]["mentions"] += 1

    # 策略2：对话引用格式（"XXX"说/道/问/答）
    quote_pattern = re.findall(r'[\u4e00-\u9fff]{2,4}(?:说|道|问|答|喊|叫|嚷|骂|回答|告诉|告诉|问到|说道)', text)
    for phrase in quote_pattern:
        name = re.sub(r'(?:说|道|问|答|喊|叫|嚷|骂|回答|告诉|问到|说道)$', '', phrase)
        if len(name) >= 2:
            characters.setdefault(name, {"mentions": 0, "source": "对话引用"})
            characters[name]["mentions"] += 1

    # 策略3：人物描写（XXX是...的父亲/母亲/...）
    relation_pattern = re.findall(r'([\u4e00-\u9fff]{2,4})(?:是|的)(?:父亲|母亲|哥哥|姐姐|弟弟|妹妹|丈夫|妻子|儿子|女儿|爷爷|奶奶|外公|外婆)', text)
    for name in relation_pattern:
        characters.setdefault(name, {"mentions": 0, "source": "关系描述"})
        characters[name]["mentions"] += 1

    # 策略4：统计已知角色名的出现频率
    for name in list(characters.keys()):
        characters[name]["mentions"] += len(re.findall(re.escape(name), text))

    # 过滤低频误识别
    characters = {k: v for k, v in characters.items() if v["mentions"] >= 2}

    # 按出现频率排序
    sorted_chars = sorted(characters.items(), key=lambda x: x[1]["mentions"], reverse=True)

    return sorted_chars


def extract_fragments(text, character_name, context_window=200):
    """
    提取与指定角色相关的所有文本片段。
    返回：对白、旁白描述、他人评价 三类
    """
    fragments = {
        "dialogue": [],     # 该角色的对白
        "narration": [],    # 关于该角色的叙述
        "evaluation": [],   # 他人对该角色的评价
        "action": [],       # 该角色的行为描写
    }

    lines = text.split("\n")

    for i, line in enumerate(lines):
        if character_name in line:
            # 获取上下文
            ctx_start = max(0, i - 3)
            ctx_end = min(len(lines), i + 4)
            context = "\n".join(lines[ctx_start:ctx_end])

            # 判断片段类型
            stripped = line.strip()
            if stripped.startswith(character_name + "：") or stripped.startswith(character_name + ":"):
                # 对白
                dialogue_text = re.sub(r'^[^：:]*[：:]\s*', '', stripped)
                if dialogue_text:
                    fragments["dialogue"].append({
                        "text": dialogue_text,
                        "context": context,
                        "line": i + 1
                    })
            elif any(word in stripped for word in ["说", "道", "问", "答", "喊"]):
                # 行为+对白
                fragments["action"].append({
                    "text": stripped,
                    "context": context,
                    "line": i + 1
                })
            elif any(other in stripped for other in ["觉得", "认为", "看来", "其实"]) and character_name not in stripped.split("觉得")[0]:
                # 他人评价
                fragments["evaluation"].append({
                    "text": stripped,
                    "context": context,
                    "line": i + 1
                })
            else:
                # 叙述
                fragments["narration"].append({
                    "text": stripped,
                    "context": context,
                    "line": i + 1
                })

    return fragments


# ============================================================
# 人格建模模块
# ============================================================

def infer_gender(text, character_name):
    """
    从文本中推断角色性别。
    优先级：明确描述 > 代词统计 > 默认 male
    """
    # 明确性别描述（简体优先，兼顾繁体）
    explicit_male = [
        # 明确说"男"相关
        "男主角", "男主", "男性角色", "男选手", "男演员", "男声",
        "男孩", "男子", "先生", "绅士",
        # 亲属
        "哥哥", "弟弟", "父亲", "爸爸", "儿子", "丈夫", "外公", "舅舅", "伯伯",
        # 角色代词+动词（过去式/将来式排除"他是"这类主语）
        "他是", "他很", "他总", "他总是", "他性格", "他被",
    ]
    explicit_female = [
        # 明确说"女"相关
        "女主角", "女主", "女性角色", "女选手", "女演员", "女声",
        "女孩", "女子", "女士", "小姐", "千金",
        # 亲属
        "姐姐", "妹妹", "母亲", "妈妈", "女儿", "妻子", "外婆", "舅妈", "姑姑",
        # 角色代词+动词
        "她是", "她很", "她总", "她总是", "她性格", "她被",
    ]

    male_count = sum(text.count(s) for s in explicit_male)
    female_count = sum(text.count(s) for s in explicit_female)

    if female_count > male_count:
        return "female"
    elif male_count > female_count:
        return "male"
    else:
        # 统计纯代词出现频率
        he_count = len(re.findall(r'[^她\s]他[的个是所在有能于被让把]', text))
        she_count = len(re.findall(r'她[的个是所在有能于被让把]', text))
        if she_count > he_count:
            return "female"
        return "male"


def infer_personality(fragments, character_name):
    """
    从片段中推断 Big Five 人格维度 + 性格关键词。
    基于语言和行为模式的启发式推断。
    """
    # 合并所有文本
    all_text = ""
    for category in fragments.values():
        for frag in category:
            all_text += " " + frag.get("text", "") + " " + frag.get("context", "")

    # 性别推断
    gender = infer_gender(all_text, character_name)

    # Big Five 启发式推断
    scores = {}

    # 开放性（想象力、好奇心、接受新事物）
    openness_signals_pos = ["试试", "新的", "有趣", "想象", "创意", "不一般", "独特", "探索"]
    openness_signals_neg = ["传统", "规矩", "老一套", "不应该", "不可以"]
    scores["openness"] = calc_score(all_text, openness_signals_pos, openness_signals_neg)

    # 责任心（自律、计划、负责）
    conscientiousness_pos = ["必须", "一定", "负责", "认真", "规矩", "计划", "守时", "承诺"]
    conscientiousness_neg = ["随便", "算了", "无所谓", "不想", "懒得"]
    scores["conscientiousness"] = calc_score(all_text, conscientiousness_pos, conscientiousness_neg)

    # 外向性（社交、表达、活力）
    extraversion_pos = ["大家", "一起", "热闹", "喜欢", "聚会", "朋友", "兴奋", "开心"]
    extraversion_neg = ["一个人", "安静", "不想见", "独处", "沉默", "默默"]
    scores["extraversion"] = calc_score(all_text, extraversion_pos, extraversion_neg)

    # 宜人性（合作、信任、同情）
    agreeableness_pos = ["帮你", "没关系", "谢谢", "理解", "原谅", "温柔", "善良", "体谅"]
    agreeableness_neg = ["凭什么", "不答应", "滚", "讨厌", "恨", "报复", "愤怒"]
    scores["agreeableness"] = calc_score(all_text, agreeableness_pos, agreeableness_neg)

    # 神经质（情绪不稳、焦虑）
    neuroticism_pos = ["担心", "害怕", "紧张", "不安", "焦虑", "害怕", "痛苦", "崩溃"]
    neuroticism_neg = ["平静", "淡定", "无所谓", "不在乎", "冷静"]
    scores["neuroticism"] = calc_score(all_text, neuroticism_pos, neuroticism_neg)

    # 性格关键词推断
    keywords = infer_keywords(all_text, scores)

    return {
        "scores": scores,
        "keywords": keywords,
        "confidence": "推断-基于文本分析",
        "gender": gender
    }


def calc_score(text, pos_signals, neg_signals):
    """计算0-1分值"""
    pos_count = sum(1 for s in pos_signals if s in text)
    neg_count = sum(1 for s in neg_signals if s in text)
    total = pos_count + neg_count
    if total == 0:
        return 0.5  # 默认中性
    score = pos_count / total
    # 映射到 0.2-0.8 范围，避免极端值
    return round(0.2 + score * 0.6, 1)


def infer_keywords(text, scores):
    """根据文本和人格分数推断性格关键词"""
    keywords = []

    # 基于 Big Five 分数
    if scores.get("openness", 0.5) > 0.6:
        keywords.append("思想开放")
    elif scores.get("openness", 0.5) < 0.4:
        keywords.append("保守传统")

    if scores.get("conscientiousness", 0.5) > 0.6:
        keywords.append("认真负责")
    elif scores.get("conscientiousness", 0.5) < 0.4:
        keywords.append("随性自在")

    if scores.get("extraversion", 0.5) > 0.6:
        keywords.append("热情开朗")
    elif scores.get("extraversion", 0.5) < 0.4:
        keywords.append("内敛沉默")

    if scores.get("agreeableness", 0.5) > 0.6:
        keywords.append("温和善良")
    elif scores.get("agreeableness", 0.5) < 0.4:
        keywords.append("强势直接")

    if scores.get("neuroticism", 0.5) > 0.6:
        keywords.append("敏感多思")
    elif scores.get("neuroticism", 0.5) < 0.4:
        keywords.append("沉稳坚定")

    # 基于文本中的高频描述词
    desc_words = re.findall(
        r'(?:性格|为人|脾气|态度|总是|一向|常常|非常|特别|很)'
        r'([\u4e00-\u9fff]{1,3})',
        text
    )
    if desc_words:
        counter = Counter(desc_words)
        top_words = [w for w, _ in counter.most_common(3) if len(w) >= 2]
        keywords.extend(top_words)

    return list(dict.fromkeys(keywords))  # 去重保序


# ============================================================
# 语言风格提取模块
# ============================================================

def extract_linguistic_style(fragments):
    """从对白片段中提取语言风格"""
    dialogues = fragments.get("dialogue", [])
    all_dialogue_text = " ".join(d["text"] for d in dialogues)

    style = {
        "catchphrases": [],
        "fillers": [],
        "dialect": "",
        "tone": ""
    }

    if not all_dialogue_text.strip():
        return style

    # 提取高频短语（2-5字的短语）
    phrases = re.findall(r'[\u4e00-\u9fff]{2,5}', all_dialogue_text)
    if phrases:
        counter = Counter(phrases)
        # 过滤常见无意义词
        stopwords = {"一个", "什么", "怎么", "这个", "那个", "我们", "他们", "你们",
                     "不是", "可以", "因为", "所以", "但是", "如果", "已经", "就是"}
        meaningful = [(w, c) for w, c in counter.most_common(30)
                      if w not in stopwords and c >= 2]
        style["catchphrases"] = [w for w, _ in meaningful[:5]]

    # 提取语气词
    fillers = re.findall(r'[啊呢吧嘛哦嗯唉嘿噢呀啦]', all_dialogue_text)
    if fillers:
        counter = Counter(fillers)
        style["fillers"] = [f for f, _ in counter.most_common(4)]

    # 推断语调特征
    excl_count = all_dialogue_text.count("！") + all_dialogue_text.count("!")
    quest_count = all_dialogue_text.count("？") + all_dialogue_text.count("?")
    ellip_count = all_dialogue_text.count("…") + all_dialogue_text.count("...")

    tone_parts = []
    if excl_count > len(dialogues) * 0.3:
        tone_parts.append("语气强烈")
    if quest_count > len(dialogues) * 0.3:
        tone_parts.append("善于反问")
    if ellip_count > len(dialogues) * 0.2:
        tone_parts.append("说话含蓄")

    # 句子长度
    avg_len = len(all_dialogue_text) / max(len(dialogues), 1)
    if avg_len < 10:
        tone_parts.append("言简意赅")
    elif avg_len > 30:
        tone_parts.append("善于表达")

    style["tone"] = "，".join(tone_parts) if tone_parts else "平稳"

    return style


# ============================================================
# 记忆提取模块
# ============================================================

def extract_memories(fragments, character_name):
    """从片段中提取记忆条目"""
    memories = []
    memory_id = 0

    # 从行为和叙述中提取事实记忆
    for frag in fragments.get("action", []) + fragments.get("narration", []):
        text = frag["text"]
        if len(text) > 10:  # 过滤太短的
            memories.append({
                "id": memory_id,
                "category": "事实记忆",
                "content": first_person_convert(text, character_name),
                "source_line": frag.get("line", 0),
                "confidence": "medium"
            })
            memory_id += 1

    # 从对白中提取价值观记忆
    for frag in fragments.get("dialogue", []):
        text = frag["text"]
        value_signals = ["应该", "必须", "不能", "一定要", "重要", "相信", "觉得",
                         "认为", "希望", "想要", "后悔", "珍惜"]
        if any(s in text for s in value_signals) and len(text) > 5:
            memories.append({
                "id": memory_id,
                "category": "价值观记忆",
                "content": text,
                "source_line": frag.get("line", 0),
                "confidence": "medium"
            })
            memory_id += 1

    # 从评价中提取他人眼中的形象
    for frag in fragments.get("evaluation", []):
        text = frag["text"]
        if len(text) > 10:
            memories.append({
                "id": memory_id,
                "category": "情感记忆",
                "content": first_person_convert(text, character_name),
                "source_line": frag.get("line", 0),
                "confidence": "low"
            })
            memory_id += 1

    return memories


def first_person_convert(text, character_name):
    """第三人称转第一人称"""
    text = text.replace(character_name, "我")
    # 处理"他的/她的"
    text = re.sub(r'(?:他|她|它)的', '我的', text)
    text = re.sub(r'(?:他|她|它)', '我', text)
    return text.strip()


# ============================================================
# 报告生成模块
# ============================================================

def generate_report(character_name, fragments, personality, style, memories):
    """生成分析报告"""
    print(f"\n{'='*60}")
    print(f"🧬 人格分析报告：{character_name}")
    print(f"{'='*60}")

    # 片段统计
    print(f"\n📊 素材片段统计：")
    for cat, frags in fragments.items():
        label = {"dialogue": "对白", "narration": "叙述",
                 "evaluation": "他人评价", "action": "行为描写"}.get(cat, cat)
        print(f"   {label}：{len(frags)} 条")

    # 性别
    gender_label = "男" if personality.get("gender") == "male" else "女"
    print(f"\n🚻 性别：{gender_label}（自动推断）")

    # Big Five
    print(f"\n🧠 Big Five 人格维度：")
    dims = {
        "openness": "开放性",
        "conscientiousness": "责任心",
        "extraversion": "外向性",
        "agreeableness": "宜人性",
        "neuroticism": "神经质"
    }
    for key, label in dims.items():
        val = personality["scores"].get(key, 0.5)
        bar = "█" * int(val * 10) + "░" * (10 - int(val * 10))
        print(f"   {label}：{bar} {val:.1f}")

    # 关键词
    if personality["keywords"]:
        print(f"\n🏷️ 性格关键词：{'、'.join(personality['keywords'])}")

    # 语言风格
    print(f"\n💬 语言风格：")
    if style["catchphrases"]:
        print(f"   高频用语：{'、'.join(style['catchphrases'][:5])}")
    if style["fillers"]:
        print(f"   语气词：{'、'.join(style['fillers'])}")
    if style["tone"]:
        print(f"   语调特征：{style['tone']}")

    # 记忆
    print(f"\n💭 提取记忆：{len(memories)} 条")
    categories = {}
    for m in memories:
        cat = m["category"]
        categories[cat] = categories.get(cat, 0) + 1
    for cat, count in categories.items():
        print(f"   {cat}：{count} 条")

    print(f"\n{'='*60}\n")


# ============================================================
# CLI
# ============================================================

def main():
    if len(sys.argv) < 2:
        print("Persona Forge Analyzer — 人格分析引擎")
        print()
        print("用法：")
        print("  python3 analyzer.py characters <input_file>              识别角色")
        print("  python3 analyzer.py fragments <input_file> -c '名字'    提取片段")
        print("  python3 analyzer.py model <input_file> -c '名字'        人格建模")
        print("  python3 analyzer.py full <input_file> -c '名字'         完整分析")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "characters":
        if len(sys.argv) < 3:
            print("❌ 请指定输入文件")
            sys.exit(1)
        text = load_text(sys.argv[2])
        chars = extract_characters(text)
        print(f"📖 从 {sys.argv[2]} 中识别到 {len(chars)} 个角色：\n")
        for name, info in chars:
            print(f"  👤 {name}  (出现 {info['mentions']} 次, 来源: {info['source']})")
        print()

    elif cmd in ("fragments", "model", "full"):
        if len(sys.argv) < 3:
            print("❌ 请指定输入文件")
            sys.exit(1)

        # 解析参数
        source = sys.argv[2]
        character = None
        for i, arg in enumerate(sys.argv):
            if arg in ("-c", "--character") and i + 1 < len(sys.argv):
                character = sys.argv[i + 1]

        if not character:
            print("❌ 请指定角色名: -c '名字'")
            sys.exit(1)

        text = load_text(source)

        if cmd == "fragments":
            frags = extract_fragments(text, character)
            print(f"🔍 角色「{character}」的相关片段：\n")
            for cat, items in frags.items():
                label = {"dialogue": "对白", "narration": "叙述",
                         "evaluation": "评价", "action": "行为"}.get(cat, cat)
                print(f"  --- {label} ({len(items)} 条) ---")
                for item in items[:5]:
                    print(f"    L{item['line']}: {item['text'][:80]}")
                if len(items) > 5:
                    print(f"    ... 还有 {len(items)-5} 条")
                print()

        elif cmd == "model":
            frags = extract_fragments(text, character)
            personality = infer_personality(frags, character)
            style = extract_linguistic_style(frags)
            memories = extract_memories(frags, character)
            generate_report(character, frags, personality, style, memories)

        elif cmd == "full":
            frags = extract_fragments(text, character)
            personality = infer_personality(frags, character)
            style = extract_linguistic_style(frags)
            memories = extract_memories(frags, character)
            generate_report(character, frags, personality, style, memories)

            # 输出可直接用的 profile.json 结构
            profile = {
                "name": character,
                "alias": [character],
                "gender": personality.get("gender", "male"),
                "birth_year": None,
                "death_year": None,
                "relation": "小说/剧本角色",
                "occupation": "",
                "hometown": "",
                "personality": {
                    **personality["scores"],
                    "keywords": personality["keywords"]
                },
                "linguistic_style": style,
                "knowledge": {
                    "interests": [],
                    "expertise": [],
                    "devices": []
                }
            }
            print("📋 生成的 profile.json 结构：")
            print(json.dumps(profile, ensure_ascii=False, indent=2))
    else:
        print(f"❌ 未知命令: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
