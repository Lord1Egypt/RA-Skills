# -*- coding: utf-8 -*-
"""
幼儿园英语全套课程 - 共享数据与 I18N

集中存放：字母表、主题词汇库、CVC 拼读词、高频词、
等级→题型映射、默认题量、中英文界面文案、渲染样式。

所有题型生成器 (generators/g_*.py) 都从这里取数据，避免各自硬编码。
"""

import random

# ----------------------------------------------------------------- 基础字母
UPPER = [chr(ord("A") + i) for i in range(26)]
LOWER = [chr(ord("a") + i) for i in range(26)]
LETTER_PAIRS = list(zip(UPPER, LOWER))  # [('A','a'), ...]

# 字母 → 代表性发音示例（用于 letter_sound / 自然拼读铺垫）
LETTER_SOUND = {
    "A": ("/æ/", "apple", "🍎"), "B": ("/b/", "ball", "⚽"),
    "C": ("/k/", "cat", "🐱"), "D": ("/d/", "dog", "🐶"),
    "E": ("/e/", "egg", "🥚"), "F": ("/f/", "fish", "🐟"),
    "G": ("/g/", "goat", "🐐"), "H": ("/h/", "hat", "🎩"),
    "I": ("/ɪ/", "ink", "🖋"), "J": ("/dʒ/", "jam", "🍯"),
    "K": ("/k/", "kite", "🪁"), "L": ("/l/", "lion", "🦁"),
    "M": ("/m/", "milk", "🥛"), "N": ("/n/", "nose", "👃"),
    "O": ("/ɒ/", "orange", "🍊"), "P": ("/p/", "pig", "🐷"),
    "Q": ("/kw/", "queen", "👑"), "R": ("/r/", "red", "🔴"),
    "S": ("/s/", "sun", "☀️"), "T": ("/t/", "toy", "🧸"),
    "U": ("/ʌ/", "umbrella", "☂️"), "V": ("/v/", "van", "🚐"),
    "W": ("/w/", "water", "💧"), "X": ("/ks/", "box", "📦"),
    "Y": ("/j/", "yellow", "🟡"), "Z": ("/z/", "zoo", "🦁"),
}

# ----------------------------------------------------------------- 主题词汇库
# 每个词：[单词, emoji 图示, 中文]
VOCAB = {
    "colors": [
        ["red", "🔴", "红色"], ["blue", "🔵", "蓝色"], ["yellow", "🟡", "黄色"],
        ["green", "🟢", "绿色"], ["orange", "🟠", "橙色"], ["purple", "🟣", "紫色"],
        ["pink", "🌸", "粉色"], ["black", "⚫", "黑色"], ["white", "⚪", "白色"],
        ["brown", "🤎", "棕色"],
    ],
    "animals": [
        ["cat", "🐱", "猫"], ["dog", "🐶", "狗"], ["pig", "🐷", "猪"],
        ["cow", "🐮", "牛"], ["duck", "🦆", "鸭子"], ["fish", "🐟", "鱼"],
        ["bird", "🐦", "鸟"], ["rabbit", "🐰", "兔子"], ["bear", "🐻", "熊"],
        ["lion", "🦁", "狮子"], ["elephant", "🐘", "大象"], ["monkey", "🐵", "猴子"],
        ["tiger", "🐯", "老虎"], ["panda", "🐼", "熊猫"], ["frog", "🐸", "青蛙"],
        ["horse", "🐴", "马"],
    ],
    "food": [
        ["apple", "🍎", "苹果"], ["banana", "🍌", "香蕉"], ["orange", "🍊", "橙子"],
        ["grape", "🍇", "葡萄"], ["cake", "🍰", "蛋糕"], ["egg", "🥚", "鸡蛋"],
        ["bread", "🍞", "面包"], ["milk", "🥛", "牛奶"], ["rice", "🍚", "米饭"],
        ["pizza", "🍕", "披萨"], ["icecream", "🍦", "冰淇淋"], ["cookie", "🍪", "饼干"],
    ],
    "numbers": [
        ["one", "1️⃣", "一"], ["two", "2️⃣", "二"], ["three", "3️⃣", "三"],
        ["four", "4️⃣", "四"], ["five", "5️⃣", "五"], ["six", "6️⃣", "六"],
        ["seven", "7️⃣", "七"], ["eight", "8️⃣", "八"], ["nine", "9️⃣", "九"],
        ["ten", "🔟", "十"],
    ],
    "body": [
        ["head", "🤕", "头"], ["eye", "👁", "眼睛"], ["ear", "👂", "耳朵"],
        ["nose", "👃", "鼻子"], ["mouth", "👄", "嘴"], ["hand", "✋", "手"],
        ["foot", "🦶", "脚"], ["face", "😐", "脸"],
    ],
    "family": [
        ["mom", "👩", "妈妈"], ["dad", "👨", "爸爸"], ["baby", "👶", "宝宝"],
        ["grandma", "👵", "奶奶"], ["grandpa", "👴", "爷爷"], ["boy", "🧒", "男孩"],
        ["girl", "👧", "女孩"],
    ],
    "toys": [
        ["ball", "⚽", "球"], ["car", "🚗", "车"], ["doll", "🪆", "玩偶"],
        ["block", "🧱", "积木"], ["kite", "🪁", "风筝"], ["balloon", "🎈", "气球"],
        ["teddy", "🧸", "泰迪熊"],
    ],
    "clothes": [
        ["hat", "🎩", "帽子"], ["shirt", "👕", "衬衫"], ["dress", "👗", "连衣裙"],
        ["shoe", "👟", "鞋"], ["sock", "🧦", "袜子"],
    ],
    "nature": [
        ["sun", "☀️", "太阳"], ["moon", "🌙", "月亮"], ["star", "⭐", "星星"],
        ["flower", "🌸", "花"], ["tree", "🌳", "树"], ["cloud", "☁️", "云"],
        ["rain", "🌧", "雨"], ["snow", "❄️", "雪"],
    ],
    "school": [
        ["book", "📖", "书"], ["pen", "✏️", "笔"], ["bag", "🎒", "书包"],
        ["ruler", "📏", "尺子"], ["paper", "📄", "纸"],
    ],
    "actions": [
        ["run", "🏃", "跑"], ["jump", "🤾", "跳"], ["sing", "🎤", "唱"],
        ["eat", "🍽", "吃"], ["sleep", "😴", "睡"], ["read", "📚", "读"],
        ["play", "🤹", "玩"], ["swim", "🏊", "游泳"],
    ],
}

# ----------------------------------------------------------------- CVC 拼读词（短元音）
# 按元音分组，供 phonics_cvc 使用
CVC = {
    "a": ["cat", "hat", "bat", "mat", "map", "bag", "cap", "fan", "jam", "rat", "can", "pan", "van", "bad", "tag"],
    "e": ["bed", "red", "pen", "hen", "ten", "leg", "net", "pet", "wet", "web"],
    "i": ["pig", "big", "dig", "pin", "bin", "fin", "sit", "hit", "bit", "kid", "lid", "six"],
    "o": ["dog", "log", "hot", "pot", "dot", "top", "mop", "box", "fox", "hop", "pop", "cop"],
    "u": ["bus", "sun", "run", "cup", "pup", "bug", "rug", "hug", "mug", "nut", "cut", "tub"],
}

# ----------------------------------------------------------------- 高频词（Dolch Pre-Primer）
SIGHT_WORDS = [
    "a", "and", "away", "big", "blue", "can", "come", "down", "find", "for",
    "funny", "go", "help", "here", "I", "in", "is", "it", "jump", "little",
    "look", "make", "me", "my", "not", "one", "play", "red", "run", "said",
    "see", "the", "three", "to", "two", "up", "we", "where", "yellow", "you",
]

# ----------------------------------------------------------------- 简单句型模板
# (句型框架, 可选填空词[单词], emoji 图示)
SENTENCE_PATTERNS = [
    ("I see a {}.", ["cat", "dog", "pig", "cow", "duck", "fish", "bird", "bear", "lion", "frog"],
     {"cat": "🐱", "dog": "🐶", "pig": "🐷", "cow": "🐮", "duck": "🦆", "fish": "🐟", "bird": "🐦", "bear": "🐻", "lion": "🦁", "frog": "🐸"}),
    ("This is a {}.", ["red", "blue", "yellow", "green", "orange", "purple", "pink", "brown"],
     {"red": "🔴", "blue": "🔵", "yellow": "🟡", "green": "🟢", "orange": "🟠", "purple": "🟣", "pink": "🌸", "brown": "🤎"}),
    ("I like {}.", ["apple", "banana", "orange", "cake", "milk", "bread", "egg", "cookie"],
     {"apple": "🍎", "banana": "🍌", "orange": "🍊", "cake": "🍰", "milk": "🥛", "bread": "🍞", "egg": "🥚", "cookie": "🍪"}),
    ("It is {}.", ["sun", "moon", "star", "flower", "tree", "cloud", "snow"],
     {"sun": "☀️", "moon": "🌙", "star": "⭐", "flower": "🌸", "tree": "🌳", "cloud": "☁️", "snow": "❄️"}),
    ("I can {}.", ["run", "jump", "sing", "eat", "sleep", "read", "play", "swim"],
     {"run": "🏃", "jump": "🤾", "sing": "🎤", "eat": "🍽", "sleep": "😴", "read": "📚", "play": "🤹", "swim": "🏊"}),
]

# ----------------------------------------------------------------- 情景对话模板
DIALOGUES = [
    ("What's this?", "It's a {}.",
     ["cat", "dog", "pig", "cow", "duck", "fish", "bird", "bear", "lion", "frog"],
     {"cat": "🐱", "dog": "🐶", "pig": "🐷", "cow": "🐮", "duck": "🦆", "fish": "🐟", "bird": "🐦", "bear": "🐻", "lion": "🦁", "frog": "🐸"}),
    ("What color is it?", "It's {}.",
     ["red", "blue", "yellow", "green", "orange", "purple", "pink", "brown"],
     {"red": "🔴", "blue": "🔵", "yellow": "🟡", "green": "🟢", "orange": "🟠", "purple": "🟣", "pink": "🌸", "brown": "🤎"}),
    ("How are you?", "I am {}.",
     ["happy", "sad", "tired", "good"],
     {"happy": "😄", "sad": "😢", "tired": "😴", "good": "🙂"}),
    ("What do you like?", "I like {}.",
     ["apple", "banana", "orange", "cake", "milk", "bread"],
     {"apple": "🍎", "banana": "🍌", "orange": "🍊", "cake": "🍰", "milk": "🥛", "bread": "🍞"}),
]

# ----------------------------------------------------------------- 等级配置
LEVEL_NAME = {
    1: "字母启蒙 Letters",
    2: "自然拼读 Phonics",
    3: "词汇句型 Words & Sentences",
    4: "阅读对话 Reading & Speaking",
}

# 各等级默认练习量
DEFAULT_COUNTS = {1: 8, 2: 8, 3: 8, 4: 8}

# 等级 → 题型（diagnosis 时覆盖全部）
LEVEL_TOPICS = {
    1: ["letter_trace", "letter_match", "letter_sound", "vocab_theme"],
    2: ["letter_sound", "phonics_cvc", "word_pic", "fill_letter", "vocab_theme"],
    3: ["word_pic", "fill_letter", "sight_words", "sentence", "vocab_theme"],
    4: ["sentence", "dialogue", "sight_words", "phonics_cvc"],
}

# 题型中文名（答案页/日志用）
TOPIC_LABEL = {
    "letter_trace": "字母描红",
    "letter_match": "大小写配对",
    "letter_sound": "字母发音",
    "phonics_cvc": "自然拼读",
    "word_pic": "看图识词",
    "vocab_theme": "主题词汇",
    "fill_letter": "补全单词",
    "sight_words": "高频词",
    "sentence": "简单句型",
    "dialogue": "情景对话",
}


# ----------------------------------------------------------------- I18N 界面文案
I18N = {
    "zh": {
        "page_title": "幼儿园英语练习 · L{level}",
        "head_title": "幼儿园英语 · {level}",
        "name_label_prefix": "姓名：",
        "name_label_suffix": "　共 {n} 题",
        "answer_title": "参考答案（家长用）",
        "hint_print": "打印设置：A4 纵向、边距默认、勾选「背景图形」",
        "score_title": "评价栏（家长填写）",
        "score_points": "得分：",
        "score_correct": "做对：",
        "score_total_suffix": " / {n} 题",
        "score_comment": "一句话点评：",
    },
    "en": {
        "page_title": "Kindergarten English · L{level}",
        "head_title": "English Fun · L{level}",
        "name_label_prefix": "Name: ",
        "name_label_suffix": "　Total: {n}",
        "answer_title": "Answer Key (for parents)",
        "hint_print": "Print: A4 portrait, default margins, enable 'Background graphics'",
        "score_title": "Score (for parents)",
        "score_points": "Score: ",
        "score_correct": "Correct: ",
        "score_total_suffix": " / {n}",
        "score_comment": "Comment: ",
    },
}

# 指令文案：zh / en 两版，按 lang 选取
INSTR = {
    "letter_trace": {
        "zh": "照着描，再自己写几遍。",
        "en": "Trace the letter, then write it on your own.",
    },
    "letter_match": {
        "zh": "把大写字母和对应的小写字母连起来 / 圈一圈。",
        "en": "Match each big letter to its small letter.",
    },
    "letter_sound": {
        "zh": "圈出读音相同的图片 / 字母。",
        "en": "Circle the picture / letter with the same sound.",
    },
    "phonics_cvc": {
        "zh": "拼一拼，写出这个词的发音。",
        "en": "Blend the sounds and say the word.",
    },
    "word_pic": {
        "zh": "看图，圈出正确的单词。",
        "en": "Look at the picture. Circle the correct word.",
    },
    "vocab_theme": {
        "zh": "读出单词，连一连。",
        "en": "Say the words and match them.",
    },
    "fill_letter": {
        "zh": "看图，把缺的字母补上。",
        "en": "Look at the picture. Fill in the missing letter.",
    },
    "sight_words": {
        "zh": "认读高频词，圈出目标词。",
        "en": "Read the sight word. Circle the target word.",
    },
    "sentence": {
        "zh": "看图，选词把句子补充完整。",
        "en": "Look and complete the sentence with a word.",
    },
    "dialogue": {
        "zh": "读一读对话，补全答句。",
        "en": "Read the dialogue and complete the answer.",
    },
}


# ----------------------------------------------------------------- 工具函数
def rid():
    """随机种子"""
    return random.randint(1, 10 ** 6)


def pick(rng, seq):
    return rng.choice(seq)


def sample(rng, seq, k):
    return rng.sample(seq, k) if hasattr(seq, "__iter__") else seq


def shuffle(rng, seq):
    s = list(seq)
    rng.shuffle(s)
    return s


# ----------------------------------------------------------------- 渲染样式
CSS = """
:root{--ink:#1a2b3c;--line:#345;--muted:#7a8a99;--accent:#e17055;--soft:#f3f6f9;}
*{box-sizing:border-box;}
body{margin:0;background:#e9edf1;color:var(--ink);
  font-family:"Comic Sans MS","Segoe UI",Verdana,"Microsoft YaHei",sans-serif;}
.no-print{text-align:center;padding:10px;background:#fff;position:sticky;top:0;z-index:9;
  border-bottom:1px solid #ddd;}
.no-print button{padding:8px 22px;font-size:14px;cursor:pointer;background:var(--accent);
  color:#fff;border:none;border-radius:6px;}
.sheet{width:190mm;min-height:273mm;margin:8mm auto;padding:8mm 9mm;background:#fff;
  box-shadow:0 1px 6px rgba(0,0,0,.15);page-break-after:always;position:relative;
  display:flex;flex-direction:column;}
.sheet:last-child{page-break-after:auto;}
.head{border-bottom:3px solid var(--accent);padding-bottom:3mm;margin-bottom:5mm;}
.head h1{margin:0;font-size:20pt;letter-spacing:1px;color:var(--accent);}
.meta{font-size:11pt;color:#555;margin-top:2mm;}
.meta .fill{display:inline-block;border-bottom:1px solid var(--line);min-width:42mm;}
.card{break-inside:avoid;margin-bottom:5mm;padding:4mm;border:2px dashed #cdd8e0;border-radius:10px;
  background:var(--soft);}
.card .t{font-size:14pt;font-weight:700;color:var(--ink);margin-bottom:1mm;}
.card .i{font-size:10.5pt;color:var(--muted);margin-bottom:2mm;font-family:"Microsoft YaHei",sans-serif;}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:6mm 9mm;flex:1;align-content:start;}
.grid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:5mm 6mm;flex:1;align-content:start;}
.bigletter{font-size:46pt;font-weight:800;color:var(--accent);text-align:center;line-height:1.1;
  text-shadow:1px 1px 0 #fff;}
.tracebox{border:2px solid #bcd;width:24mm;height:24mm;display:inline-flex;align-items:center;
  justify-content:center;font-size:30pt;color:#bcd;border-radius:6px;margin:1mm;}
.writebox{display:inline-block;width:16mm;height:16mm;border-bottom:2px solid var(--line);
  margin:1mm;text-align:center;font-size:18pt;line-height:16mm;}
.pic{font-size:30pt;text-align:center;}
.wlbl{font-size:10pt;color:#666;margin-top:1mm;}
.wordopt{display:flex;gap:6mm;justify-content:center;flex-wrap:wrap;font-size:16pt;margin-top:1mm;}
.wordopt span{border:2px solid #bcd;border-radius:8px;padding:1mm 3mm;min-width:18mm;text-align:center;}
.blank{border-bottom:2px solid var(--line);display:inline-block;min-width:16mm;height:1.5em;
  vertical-align:middle;text-align:center;}
.sound{font-size:14pt;color:var(--accent);font-weight:700;}
.matchrow{display:flex;justify-content:space-between;align-items:center;font-size:22pt;margin:1mm 0;}
.matchcol{display:flex;flex-direction:column;gap:3mm;}
.dotline{border-bottom:2px dotted #9ab;flex:1;margin:0 4mm;}
.sentence{font-size:18pt;line-height:2;}
.dialoguebox{font-size:16pt;line-height:1.9;background:#fff;padding:3mm;border-radius:8px;}
.qA{font-weight:700;color:#2d6cdf;}
.qB{color:#16a085;}
.ans{margin-top:6mm;padding:5mm;background:#fff8f4;border:2px solid var(--accent);border-radius:10px;}
.ans h2{margin:0 0 2mm;font-size:14pt;color:var(--accent);}
.ans ol{margin:0;padding-left:20px;font-size:12pt;line-height:1.7;}
.ans li{margin-bottom:1mm;}
.score{margin-top:6mm;padding:4mm;background:#fafcff;border:1px solid #cdd8e0;border-radius:10px;font-size:11pt;}
.score .t2{font-weight:700;margin-bottom:2mm;}
.score .row2{display:flex;gap:10mm;margin-bottom:2mm;}
.score .fill{border-bottom:1px solid var(--line);display:inline-block;min-width:18mm;}
.score .fill.sm{min-width:10mm;}
@media print{
  body{background:#fff;}
  .no-print{display:none;}
  .sheet{box-shadow:none;margin:0;width:auto;min-height:0;height:265mm;}
  @page{size:A4 portrait;margin:10mm;}
}
"""
