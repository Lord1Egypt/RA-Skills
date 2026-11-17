#!/usr/bin/env python3
"""
漫剧全流程生产工具 v3.0
Manju Script Generator — Novel → Character → Scene → Storyboard → Image/Video Prompt pipeline
"""

import sys, json, os, re, argparse, urllib.request
from datetime import datetime
from enum import Enum

# ─── LLM Call ───────────────────────────────────────────────────────

LLM_ENDPOINT = "http://127.0.0.1:18789/v1/chat/completions"
LLM_MODEL = "openclaw"
LLM_TOKEN = os.environ.get("GW_TOKEN", "")

def call_llm(system_prompt, user_prompt, temperature=0.7, max_tokens=8192, timeout=120):
    headers = {"Content-Type": "application/json"}
    if LLM_TOKEN:
        headers["Authorization"] = f"Bearer {LLM_TOKEN}"
    payload = json.dumps({
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }).encode()
    try:
        req = urllib.request.Request(LLM_ENDPOINT, payload, headers)
        r = urllib.request.urlopen(req, timeout=timeout)
        return json.loads(r.read())["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[ERROR] LLM call failed: {e}", file=sys.stderr)
        return None

# ─── Forbidden Word Filter ──────────────────────────────────────────

FORBIDDEN_WORDS = {
    # 血腥暴力类
    "血液飞溅": "伤口渗血", "喷血": "渗血", "鲜血淋漓": "伤痕累累",
    "血池": "深红印记", "血祭": "祭礼", "断头血": "暗红痕迹",
    "内脏出血": "内伤", "血腥场面": "激烈场面", "血债": "恩怨",
    "血洗": "清洗", "分尸": "重创", "碎尸": "击碎", "斩首": "重击",
    "砍头": "击倒", "挖眼": "伤目", "掏心": "破心", "剥皮": "伤皮",
    "凌迟": "酷刑", "虐杀": "重创", "酷刑": "严刑", "断肢": "重伤",
    "爆头": "击倒", "穿刺": "穿透", "撕咬": "攻击", "屠杀": "重创",
    "灭门": "覆灭", "焚尸": "焚烧", "鞭尸": "鞭挞", "尸横遍野": "战场惨烈",
    "血肉模糊": "伤痕累累", "骨裂": "骨伤", "脑浆": "重伤",
    "内脏外露": "重伤", "残肢断臂": "伤痕累累",
    # 裸露低俗类
    "全裸": "素衣", "半裸": "薄衫", "袒胸露背": "衣衫单薄",
    "露脐": "短衣", "露臀": "衣摆", "露私密部位": "衣襟",
    "一丝不挂": "素衣", "裸体": "素衣", "赤裸": "素衣",
    "性感暴露": "着装大胆", "挑逗性裸露": "展露风采",
    "低俗姿势": "姿态", "暴露隐私部位": "衣襟不整",
    "酥胸半露": "衣襟微敞", "衣不蔽体": "衣衫残破",
    # 色情暗示类
    "色情": "情爱", "淫秽": "不雅", "嫖娼": "勾栏", "卖淫": "风尘",
    "性交易": "交易", "一夜情": "露水情缘", "通奸": "私通",
    "乱伦": "背德", "恋童": "禁忌", "兽交": "异类",
    "约炮": "约见", "撩骚": "调笑", "打炮": "欢好", "床上戏": "私密场景",
    "胸器": "身姿", "美腿诱惑": "身姿动人", "性感撩拨": "动人",
    "暧昧低俗": "暧昧", "艳舞": "舞姿", "脱衣舞": "舞姿",
    "乳房": "胸前", "阴部": "私处", "阴茎": "下身", "臀部": "腰身",
    # 封建迷信类
    "血腥祭祀": "祭祀", "活人献祭": "献祭", "血咒": "咒术",
    "尸变": "异变", "僵尸吸血": "妖物伤人",
    "食人恶鬼": "凶恶妖物", "妖魔鬼怪": "妖魔",
    # 危害公序良俗
    "自残": "自伤", "自杀": "自尽", "暴力教唆": "教唆",
    "聚众斗殴": "冲突", "黑帮火拼": "帮派冲突", "恐怖袭击": "袭击",
    "校园暴力": "欺凌",
    # 敏感政治
    "邪教仪式": "异教仪式", "极端宗教": "狂热信仰",
    "分裂": "分离", "恐怖组织": "武装组织", "反动": "逆行", "颠覆": "推翻",
}

def apply_forbidden_filter(text):
    """替换违禁词为中性词"""
    result = text
    # 按长度降序匹配，避免短词吞噬长词
    for word in sorted(FORBIDDEN_WORDS.keys(), key=len, reverse=True):
        replacement = FORBIDDEN_WORDS[word]
        if replacement:
            result = result.replace(word, replacement)
        else:
            result = result.replace(word, "***")
    return result

# ─── Self-Check ─────────────────────────────────────────────────────

def self_check_storyboard(output_text):
    """6维自检"""
    checks = {
        "字段数": {"status": "?", "detail": ""},
        "引号": {"status": "?", "detail": ""},
        "长度": {"status": "?", "detail": ""},
        "人物": {"status": "?", "detail": ""},
        "场景": {"status": "?", "detail": ""},
        "连贯": {"status": "?", "detail": ""},
    }
    # 字段数校验
    if "panel_index" in output_text and "prompt" in output_text and "video_prompt" in output_text:
        checks["字段数"]["status"] = "✅"
        checks["字段数"]["detail"] = "包含3字段: panel_index/prompt/video_prompt"
    else:
        checks["字段数"]["status"] = "⚠️"
        checks["字段数"]["detail"] = "缺少必要字段"

    # 引号校验
    en_quotes = output_text.count('"')
    cn_quotes = output_text.count('"') + output_text.count('"')
    if en_quotes > 0 and cn_quotes == 0:
        checks["引号"]["status"] = "⚠️"
        checks["引号"]["detail"] = f"发现{en_quotes}个英文引号，需改为中文引号"
    else:
        checks["引号"]["status"] = "✅"
        checks["引号"]["detail"] = "引号格式正确"

    # 长度校验 (video_prompt ≤500字符)
    vp_matches = re.findall(r'video_prompt["\':=]+([^"\'}\]\n]+)', output_text)
    long_vps = [v for v in vp_matches if len(v.strip()) > 500]
    if long_vps:
        checks["长度"]["status"] = "⚠️"
        checks["长度"]["detail"] = f"有{len(long_vps)}个video_prompt超过500字符"
    else:
        checks["长度"]["status"] = "✅"
        checks["长度"]["detail"] = "所有video_prompt≤500字符"

    # 连贯校验
    if "衔接" in output_text or "前置" in output_text or "承接" in output_text:
        checks["连贯"]["status"] = "✅"
        checks["连贯"]["detail"] = "包含衔接指令"
    else:
        checks["连贯"]["status"] = "⚠️"
        checks["连贯"]["detail"] = "未发现衔接前置指令"

    return checks

# ─── System Prompts ─────────────────────────────────────────────────

def build_novel_system_prompt(genre):
    """小说创作系统提示词"""
    genres_prompt = """1.霸道总裁 2.追妻火葬场 3.校园甜恋 4.古风宫斗 5.武侠江湖
6.仙侠虐恋 7.悬疑惊悚 8.无限流 9.末日求生 10.豪门复仇
11.青梅竹马 12.娱乐圈恋爱 13.规则怪谈 14.民国虐恋 15.直播逆袭
16.年代爱情 17.职场商战 18.病娇囚爱 19.重生复仇 20.高甜闪婚"""

    return f"""你是一名擅长创作爆款短篇小说的顶级畅销作者，长期为番茄小说、七猫、抖音短剧等平台创作高热度短篇故事。

你尤其擅长：强冲突剧情、高情绪拉扯、极致人物反差、爽感与虐感结合、短剧式节奏、高能反转、让读者"上头"的人物关系。

你的文风特点：
1.开头三句话必须抓人
2.人物对白真实、有攻击性、有情绪
3.画面感极强
4.节奏非常快
5.几乎没有废话
6.每200字左右必须出现新冲突、新反转或新信息
7.擅长制造"误会""身份反转""追妻火葬场""极限拉扯"
8.结尾必须留巨大钩子，让人忍不住想看下一章
9.风格偏番茄小说、抖音短剧、快节奏网文、高爽感剧情流

当前选择类型: {genre}

小说要求：
1.字数控制在1000字左右
2.开头3句话必须出现爆点或冲突
3.节奏快，信息量大
4.情绪浓烈，具有强代入感
5.对话必须像真实短剧
6.每200字左右最好出现一次反转
7.要有明显的人物拉扯与关系冲突
8.结尾必须留下悬念或巨大钩子
9.禁止流水账
10.禁止平淡叙事
11.禁止AI解释感
12.要像真正的网文作者写的

输出格式：
[小说标题]

[开头爆点]
(一句话）

[中段核心冲突]
(一句话）

[结尾钩子]
(一句话）

-正文开始-

(直接输出小说正文，不要解释，不要问是否继续)

全文完"""

def build_character_prompt_instructions():
    """角色形象提示词生成指令"""
    return """根据下面提供的小说原文，整理出如下信息：

1.角色形象提示词
1.1 根据小说原文，整理出所有角色形象，需要包含人物性别、穿着、脸部特征、年龄、人物性格等。
1.2 推导出文中出现过的人物，人物可能有多种代称，要囊括文中提到的所有人物，每个人物包含名字、代称(多个代称用逗号分割)、形象描述三个字段。人物形象必须包含具体年龄，性别，发色，发型，眼睛颜色，脸部特征，上身服装，下身服装，每个输出结果必须有不一样的着装需要更好分辨。
1.3 不同场景下的同一角色分开给提示词
1.4 人物衣服要精致，全身像，完整四肢可见，从头顶到脚尖完整构图，背景留白，高个子，九头身，黄金比例身材，腿长占身高60%，专业打光，高清细节

输出格式：
角色1：XXX
场景1：XXX
	[风格描述，如：古风，3D仿真，冷光冷色调，动态光影，冷白皮]
	[年龄]岁[性别]，[发色][发型]，[眼睛颜色]眼睛，[脸部特征]，[皮肤颜色]。身穿[上身服装]，下身[下身服装]，脚穿[鞋子]。神态[神态描述]，站姿[站姿描述]，双腿修长，比例匀称。
场景2：XXX
	[风格描述]
	[详细描述]

角色2：XXX
..."""

def build_scene_prompt_instructions():
    """场景提示词生成指令"""
    return """#Role:电影级纯净场景设计专家(高辨识度版)

##核心执行逻辑(后台规则):
1.**绝对真空与匿名**:画面中严禁出现任何人影，场景描述文字中严禁出现任何角色人名。
2.**场景命名法则**:每个场景名称必须在[四个字以上]，通过具体的修饰词增加辨识度(严禁使用单一名词)
3.**四大核心要素**:场景描述必须完整涵盖:[环境类型]、[具体时间】、[空间氛围】【视觉主要特征]。
4.**Prompt开头**:所有Prompt必须以"不能出现其他人,无人纯场景,"开头。
5.**输出控制**:严禁输出任何括号内的说明文字，直接输出具体内容。

#第一步:场景提取清单
(按顺序编号列出文案中的所有地点:场景全称|核心氛围|建议色调)

#第二步:专业场景设定表(按此格式逐一输出)
**场景名称**:[四个字以上的独特命名]
**画幅构图**:横向16:9电影级场景设定图，极高画质，纯净无人的空间。写实电影风格
*视觉风格*:[填入用户指定风格]，极致细节。
**场景描述**:
[具体的地理/建筑空间属性][环境类型]
[时间时刻】【精确到时段的天气与光线状态]
[空间氛围】【如:压抑、神圣、破败、宁静等视觉情绪描述]
[主要特征]:[具体的材质、核心物件、前中后景的标志性元素，严禁提及角色姓名]
**Prompt(直接复制)**:不能出现其他人,无人，纯场景，[将上述所有环境细节融合成一段精简、极具冲击力的生图描述词，包含:no humans,empty,landscape only]"""

def build_storyboard_system_prompt(characters_json=None):
    """分镜脚本系统提示词"""
    char_info = ""
    if characters_json:
        try:
            chars = json.loads(characters_json) if isinstance(characters_json, str) else characters_json
            char_info = "## 角色信息\n"
            for c in chars:
                name = c.get("name", "?")
                role = c.get("role", "?")
                appearance = c.get("appearance", "?")
                char_info += f"  - {name}: {role}, 外貌: {appearance}\n"
        except:
            char_info = "## 角色信息\n  (角色信息解析失败)\n"

    return f"""你是一名专业漫剧分镜编剧，负责将小说文案转换为可执行的分镜脚本。

{char_info}

## 核心规则

### 内容镜头一致性原则
内容以35-50个字以内进行一次分镜头拆分，要求拆分出的单句文案内容要完整

### 3秒决策原则（执行前必检）
1. 人物是否齐全？→ 严格映射角色信息，未出现角色绝不写入
2. 场景是否连贯？→ 时间(晨/午/晚)/地点/光线必须与上一镜一致
3. 有无违禁内容？→ 自动过滤血腥/低俗/政治敏感词
→ 任一条件不满足，立即中止并重新推理

### 六维一致性准则
1. 人物一致：出现角色必须严格匹配角色信息库，未出现角色绝不写入
2. 时空一致：相邻分镜时间(晨/午/晚)、地点、光线必须无缝衔接
3. 物品一致：关键道具(如钢笔/背包)位置状态需延续上一镜
4. 动作连贯：新分镜起始动作必须承接上一镜结束状态
5. 台词合规：仅当前说话角色有张嘴动作，台词用""标注
6. 敏感过滤：自动替换违禁词(替换规则：用中性词保持剧情逻辑)

### 分镜生成四步法
STEP1 场景锚定 → 提取章节文案时间/地点/人物三角要素
STEP2 连续性检查 → 比对上一镜结尾状态(动作/台词/物品位置)
STEP3 台词植入 → 仅当章节文案含对话时添加"台词"字段
STEP4 敏感扫描 → 自动替换违禁词

### 视频提示词时间轴（10秒）
[0-3秒] 镜头：[景别]+[镜头]+[核心动作]；音效：[主音效]+[环境音]；[台词/画外音]
[3-6秒] 镜头：[景别]+[镜头]+[互动反应]；音效：[关键音效]；[台词/画外音]
[6-8秒] 镜头：[景别]+[镜头]+[情绪特写]；音效：[氛围音]；[画外音/沉默说明]
[8-10秒] 镜头：[景别]+[镜头]+[下一镜铺垫]；音效：[过渡音]

### 视频提示词要求
1. 必须包含角色标签映射语句，必须包含所有视频提示词中应该出现的角色
2. 前后分镜必须有关联性，需要思考上个画面内容后给出
3. 文案中对话放入视频提示词用""做标注
4. 不是当前角色台词不需要有张嘴、喉部动作
5. 台词时段镜头固定，不切换、不推拉
6. 不要重复生成上下分镜已经有的镜头
7. 景别多使用近景、特写、大特写等，不使用远景，少使用中景
8. 人物说台词时分析人物的当时情绪，并在分镜脚本中体现

### 图片提示词要求
1. 图片提示词内不需要映射人物
2. 不能带文字标识

### 输出格式（每个分镜3字段）
panel_index: [分镜编号]
prompt: [图片提示词]
video_prompt: [视频提示词]

### 自检要求
- 所有对话必须用中文引号""，禁用英文引号"
- video_prompt≤500字符
- 出现角色必须100%映射角色信息
- prompt必须包含原始场景信息（一字不改）
- video_prompt必须包含"衔接前置指令"段落

### 高频错误避坑
- ❌ 林辰在会议室突然出现咖啡罐(上镜在格子间)
- ✅ 林辰揉眼蹭墨痕(延续上镜断笔沾墨状态)
- ❌ 写入未出现的"王经理"角色映射
- ✅ 仅写入画面实际出现角色
- ❌ 台词时镜头切换/推拉
- ✅ 台词时段固定镜头，标注"镜头稳定，不推拉"""

# ─── Mode Functions ─────────────────────────────────────────────────

def mode_novel(args):
    """小说创作模式"""
    print("[INFO] 小说创作模式", file=sys.stderr)
    genre = args.genre
    # 支持数字编号
    genre_map = {
        "1": "霸道总裁", "2": "追妻火葬场", "3": "校园甜恋", "4": "古风宫斗",
        "5": "武侠江湖", "6": "仙侠虐恋", "7": "悬疑惊悚", "8": "无限流",
        "9": "末日求生", "10": "豪门复仇", "11": "青梅竹马", "12": "娱乐圈恋爱",
        "13": "规则怪谈", "14": "民国虐恋", "15": "直播逆袭", "16": "年代爱情",
        "17": "职场商战", "18": "病娇囚爱", "19": "重生复仇", "20": "高甜闪婚",
    }
    if genre in genre_map:
        genre = genre_map[genre]

    extra = ""
    if args.text:
        extra = f"\n\n用户额外要求：{args.text}"

    system_prompt = build_novel_system_prompt(genre)
    user_prompt = f"请使用{genre}类型创作一篇爆款短篇小说。{extra}"

    result = call_llm(system_prompt, user_prompt)
    if not result:
        result = f"[小说生成失败]\n类型: {genre}\n请检查LLM连接。"

    # 违禁词过滤
    if args.forbidden_check:
        result = apply_forbidden_filter(result)

    return result


def mode_character(args):
    """角色形象提示词模式"""
    if not args.input and not args.text:
        return "[ERROR] 需要提供小说文本 (--input 或 --text)"

    print("[INFO] 角色形象提示词模式", file=sys.stderr)
    novel = args.input_text if args.input_text else ""

    system_prompt = build_character_prompt_instructions()
    style = args.style or "写实电影，3D仿真，冷光冷色调，动态光影，冷白皮"
    user_prompt = f"小说原文:\n{novel[:20000]}\n\n通用人物风格: {style}\n\n{'需要生成三视图排版描述' if args.with_three_view else ''}"

    result = call_llm(system_prompt, user_prompt)
    if not result:
        result = "[角色形象提示词生成失败]"

    if args.forbidden_check:
        result = apply_forbidden_filter(result)

    return result


def mode_scene(args):
    """场景提示词模式"""
    if not args.input and not args.text:
        return "[ERROR] 需要提供小说文本 (--input 或 --text)"

    print("[INFO] 场景提示词模式", file=sys.stderr)
    novel = args.input_text if args.input_text else ""

    system_prompt = build_scene_prompt_instructions()
    style = args.style or "写实电影风格"
    user_prompt = f"请根据下面的小说原文，提取所有场景并生成场景设定表。\n\n风格要求: {style}，极致细节。\n\n小说原文:\n{novel[:20000]}"

    result = call_llm(system_prompt, user_prompt, temperature=0.6)
    if not result:
        result = "[场景提示词生成失败]"

    return result


def mode_storyboard(args):
    """分镜脚本模式"""
    if not args.input and not args.text:
        return "[ERROR] 需要提供小说文本 (--input 或 --text)"

    print("[INFO] 分镜脚本模式", file=sys.stderr)
    novel = args.input_text if args.input_text else ""

    characters_json = "[]"
    if args.characters:
        if os.path.isfile(args.characters):
            with open(args.characters, "r", encoding="utf-8") as f:
                characters_json = f.read()
        else:
            characters_json = args.characters

    system_prompt = build_storyboard_system_prompt(characters_json)
    user_prompt = f"请将以下小说文案转换为分镜脚本，包含图片提示词和视频提示词：\n\n{novel[:20000]}"

    result = call_llm(system_prompt, user_prompt, temperature=0.6)
    if not result:
        result = "[分镜脚本生成失败]"

    # 违禁词过滤
    if args.forbidden_check:
        result = apply_forbidden_filter(result)

    # 自检
    if args.self_check:
        checks = self_check_storyboard(result)
        result += "\n\n---\n## 输出自检报告\n"
        for check_name, check_info in checks.items():
            result += f"{check_info['status']} {check_name}: {check_info['detail']}\n"

    return result


def mode_full(args):
    """全流程模式"""
    if not args.input and not args.text:
        return "[ERROR] 需要提供小说文本 (--input 或 --text)"

    print("[INFO] 全流程模式: 角色→场景→分镜", file=sys.stderr)
    novel = args.input_text if args.input_text else ""

    result_parts = []
    result_parts.append("# 漫剧全流程生产报告\n")
    result_parts.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    result_parts.append(f"风格: {args.style}\n\n")

    # Step 1: 角色形象提示词
    print("[INFO] Step 1/3: 角色形象提示词...", file=sys.stderr)
    char_system = build_character_prompt_instructions()
    char_user = f"小说原文:\n{novel[:15000]}\n\n通用人物风格: {args.style or '写实电影，3D仿真，冷光冷色调，动态光影，冷白皮'}"
    char_result = call_llm(char_system, char_user, temperature=0.6)
    if char_result:
        if args.forbidden_check:
            char_result = apply_forbidden_filter(char_result)
        result_parts.append("## 一、角色形象\n")
        result_parts.append(char_result + "\n\n---\n\n")
    else:
        result_parts.append("## 一、角色形象\n[生成失败]\n\n---\n\n")

    # Step 2: 场景提示词
    print("[INFO] Step 2/3: 场景提示词...", file=sys.stderr)
    scene_system = build_scene_prompt_instructions()
    scene_user = f"风格要求: {args.style or '写实电影风格'}，极致细节。\n\n小说原文:\n{novel[:15000]}"
    scene_result = call_llm(scene_system, scene_user, temperature=0.6)
    if scene_result:
        result_parts.append("## 二、场景设定\n")
        result_parts.append(scene_result + "\n\n---\n\n")
    else:
        result_parts.append("## 二、场景设定\n[生成失败]\n\n---\n\n")

    # Step 3: 分镜脚本
    print("[INFO] Step 3/3: 分镜脚本...", file=sys.stderr)
    story_system = build_storyboard_system_prompt(args.characters)
    story_user = f"请将以下小说文案转换为分镜脚本，包含图片提示词和视频提示词：\n\n{novel[:15000]}"
    story_result = call_llm(story_system, story_user, temperature=0.6)
    if story_result:
        if args.forbidden_check:
            story_result = apply_forbidden_filter(story_result)
        result_parts.append("## 三、分镜脚本\n")
        result_parts.append(story_result + "\n\n")
        # 自检
        if args.self_check:
            checks = self_check_storyboard(story_result)
            result_parts.append("## 四、输出自检\n")
            for check_name, check_info in checks.items():
                result_parts.append(f"{check_info['status']} {check_name}: {check_info['detail']}\n")
    else:
        result_parts.append("## 三、分镜脚本\n[生成失败]\n\n")

    return "".join(result_parts)


# ─── Main ───────────────────────────────────────────────────────────


def mode_script(args):
    """剧本生成模式 - v4.0新增"""
    print("[INFO] 剧本生成模式", file=sys.stderr)
    genre = args.genre
    genre_map = {
        "1": "霸道总裁", "2": "追妻火葬场", "3": "校园甜恋", "4": "古风宫斗",
        "5": "武侠江湖", "6": "仙侠虐恋", "7": "悬疑惊悚", "8": "无限流",
        "9": "末日求生", "10": "豪门复仇", "11": "青梅竹马", "12": "娱乐圈恋爱",
        "13": "规则怪谈", "14": "民国虐恋", "15": "直播逆袭", "16": "年代爱情",
        "17": "职场商战", "18": "病娇囚爱", "19": "重生复仇", "20": "高甜闪婚",
    }
    if genre in genre_map:
        genre = genre_map[genre]

    extra = ""
    if args.text:
        extra = f"\n\n用户额外要求：{args.text}"

    system_prompt = f"""你是一名专业漫剧剧本编剧，擅长创作爆款漫剧剧本。

当前类型: {genre}

输出要求:
1. 先输出故事大纲：标题、开头爆点、中段核心冲突、结尾钩子
2. 再输出完整剧本，每镜格式：
【镜号】【画面描述】+【台词/旁白】+【音效/背景音乐】+【单镜时长】

要求:
- 单集总时长60秒左右
- 开篇前3秒设置强看点
- 结尾设置悬念引导下一集
- 台词口语化，精简不啰嗦
- 画面描述具体具象，适合AI生成漫剧画面
- 明确人物表情、动作、场景环境
- 禁止AI解释感，禁止平淡叙事
- 风格偏番茄小说、抖音短剧、快节奏剧情流

输出格式：
[故事标题]
[开头爆点](一句话)
[中段核心冲突](一句话)
[结尾钩子](一句话)

-正文开始-

【镜号1】【画面描述】+【台词/旁白】+【音效/背景音乐】+【单镜时长】
【镜号2】...
"""

    user_prompt = f"请使用{genre}类型创作一篇爆款漫剧剧本。{extra}"

    result = call_llm(system_prompt, user_prompt)
    if not result:
        result = f"[剧本生成失败]\n类型: {genre}\n请检查LLM连接。"

    if args.forbidden_check:
        result = apply_forbidden_filter(result)

    return result


def mode_prop(args):
    """道具提取模式 - v4.0新增"""
    if not args.input and not args.text:
        return "[ERROR] 需要提供小说文本 (--input 或 --text)"

    print("[INFO] 道具提取模式", file=sys.stderr)
    novel = args.input_text if args.input_text else ""

    system_prompt = """你是专业漫剧短视频创作专属解析提取智能体。

核心功能：接收用户输入的小说/故事全文，全自动精准拆解、梳理全文内容，完整提取所有高频重复道具。

道具提取规则：
1. 筛选标准：只提取故事中反复多次出现、高频使用、关键剧情道具、专属标志性物品
2. 剔除一次性临时杂物
3. 道具信息拆解：道具名称、外观造型、材质、颜色、尺寸、花纹细节、功能作用、独有特征
4. 道具画面出图标准：纯白背景、写实电影感、高清质感、完整全景展示，单独呈现无遮挡
5. 固定强制约束：AI仿真人电影级质感，极高画质，电影级柔光电影光效，8K超清
6. 全程纯中文输出，无英文、无乱码、无特殊符号

输出格式：
【高频关键道具清单】

道具1：[名称]
- 外观造型：[描述]
- 材质：[材质细节]
- 颜色：[主色/辅色]
- 尺寸：[尺寸数据]
- 花纹细节：[纹样描述]
- 功能作用：[剧情用途]
- 独有特征：[标志性特征]

[通用绘图提示词：纯白背景，写实电影感，高清质感，完整全景展示]

道具2：[名称]
...
"""

    user_prompt = f"请提取以下小说中的高频关键道具：\n\n{novel[:20000]}"

    result = call_llm(system_prompt, user_prompt, temperature=0.6)
    if not result:
        result = "[道具提取失败]"

    return result


def mode_threeview(args):
    """人物三视图模式 - v4.0新增"""
    print("[INFO] 人物三视图模式", file=sys.stderr)

    style = args.style or "写实电影"
    character_desc = args.input_text if args.input_text else "请描述需要生成三视图的角色"

    result = f"""# 人物三视图提示词（{style}风格）

## 提示词1（角色设定板）
一张高精度、干净极简的角色设定板/人物三视图参考页，纯白背景，整体像游戏角色建模设定图。
画面左侧展示该角色的头部高清特写，右侧展示该角色的全身三视图（包含正面、侧面、背面）。
请严格保持原图的人物形象和服装细节。严格执行左侧头部高清特写与右侧全身三视图不要有任何重叠。
背景使用极简的高级中性灰。8K超高清分辨率。
{style}风格，极致细节。

即梦模型推荐：图片模型4.7（效果最佳），4.0/4.5/4.6/5.0均可

## 提示词2（16:9三视图）
人物:16:9三视图，参考图，中心区域生成全身三视图以及一张面部特写（最左边占满三分之一的位置是面部特写，右边三分之二放正视图，侧视图，后视图）。
人物比例适中，清晰可见。严格按照比例设定，包括身高对比和头身比，线条简洁明了，流畅自然，色彩搭配协调，保持整体风格统一，背景和角色形成对比，视觉焦点集中在角色身上，确保人物比例准确，表情动作自然流畅，服装设计独特且符合角色背景，角色为自然站立状态，白底图。
{style}风格，极致细节。

即梦模型推荐：图片模型4.7（效果最佳）

## 提示词3（丰富度最高）
人物画面三视图：正面全身照、侧面全身照、背面全身照，最左侧单独放大头部细节展示，人物下方配有服装细节与配饰介绍展示图，整体构图工整专业，唯美光影，纯白背景，8K，电影级画质。
{style}风格，极致细节。

即梦模型推荐：图片模型4.7（效果最佳）

## 人物设定
{character_desc[:5000]}

## 输出要求
横版构图，白底，完整人物，不裁切，不出现多余道具，不出现文字说明，不出现LOGO，不出现水印，不出现UI界面元素，不出现点赞收藏按钮，不出现社交媒体截图感
"""

    return result


def main():
    parser = argparse.ArgumentParser(description="漫剧全流程生产工具 v3.0")
    parser.add_argument("--mode", "-m", default="novel",
                        choices=["novel", "character", "scene", "storyboard", "full"],
                        help="工作模式")
    parser.add_argument("--input", "-i", help="输入文件路径(小说文本)")
    parser.add_argument("--text", "-t", help="输入文本内容")
    parser.add_argument("--output", "-o", default="output.md", help="输出文件路径")
    parser.add_argument("--characters", "-c", help="角色配置JSON文件或JSON字符串")
    parser.add_argument("--genre", "-g", default="仙侠虐恋", help="小说类型(1-20或名称)")
    parser.add_argument("--style", "-s", default="写实电影", help="视觉风格描述")
    parser.add_argument("--with-three-view", action="store_true", help="生成三视图排版描述")
    parser.add_argument("--forbidden-check", action="store_true", default=True, help="启用违禁词过滤")
    parser.add_argument("--no-forbidden-check", action="store_false", dest="forbidden_check", help="禁用违禁词过滤")
    parser.add_argument("--duration", "-d", type=int, default=10, help="分镜时长: 10或15秒")
    parser.add_argument("--self-check", action="store_true", default=True, help="启用输出自检")
    parser.add_argument("--no-self-check", action="store_false", dest="self_check", help="禁用输出自检")

    args = parser.parse_args()

    # 读取输入文本
    args.input_text = None
    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            args.input_text = f.read()
    elif args.text:
        args.input_text = args.text

    # 路由到对应模式
    mode_map = {
        "script": mode_script,
        "prop": mode_prop,
        "threeview": mode_threeview,
        "novel": mode_novel,
        "character": mode_character,
        "scene": mode_scene,
        "storyboard": mode_storyboard,
        "script": mode_script,
    "prop": mode_prop,
    "threeview": mode_threeview,
    "full": mode_full,
    }

    mode_func = mode_map.get(args.mode)
    if not mode_func:
        print(f"[ERROR] 未知模式: {args.mode}", file=sys.stderr)
        sys.exit(1)

    print(f"[INFO] 模式: {args.mode}", file=sys.stderr)
    output = mode_func(args)

    # 写入输出
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(output)
    print(f"[OK] 输出已保存: {args.output}", file=sys.stderr)
    print(output)


if __name__ == "__main__":
    main()
