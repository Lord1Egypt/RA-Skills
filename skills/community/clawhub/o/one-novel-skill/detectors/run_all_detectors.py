#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
one-novel-skill 六套检测引擎 + 可选安全过滤 - 统一入口

用法:
  python run_all_detectors.py --input 正文/第001章.txt [--book .]
  python run_all_detectors.py --input 正文/第001章.txt --json  (输出 JSON)
"""

import os, sys, re, json, math
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
DE_AI_DIR = SKILL_DIR / "references" / "de-ai"



_BASELINES_CACHE = {}


def _load_detection_yaml():
    """从 YAML 加载检测配置，失败时返回 None（使用内联默认值）。
    
    YAML 文件为可选增强（单一真相源）；
    内联列表始终保持可用，不依赖外部文件。
    """
    yaml_path = DE_AI_DIR / "detection_config.yaml"
    if not yaml_path.exists():
        return None
    try:
        # 纯 Python YAML 解析（无依赖）
        raw = yaml_path.read_text(encoding="utf-8", errors="replace")
        lines = raw.split("\n")
        result = {}
        current_key = None
        current_list = []
        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if stripped.endswith(":") and not stripped.startswith("-"):
                if current_key and current_list:
                    result[current_key] = current_list
                current_key = stripped[:-1].strip()
                current_list = []
            elif stripped.startswith("- "):
                val = stripped[2:].strip()
                if val.startswith('"') and val.endswith('"'):
                    val = val[1:-1]
                elif val.startswith("'") and val.endswith("'"):
                    val = val[1:-1]
                current_list.append(val)
            elif current_key and ":" in stripped and not stripped.startswith("-"):
                parts = stripped.split(":", 1)
                sub_key = parts[0].strip()
                sub_val = parts[1].strip()
                if sub_val.startswith('"') and sub_val.endswith('"'):
                    sub_val = sub_val[1:-1]
                if current_key not in result or not isinstance(result[current_key], dict):
                    result[current_key] = {}
                try:
                    result[current_key][sub_key] = int(sub_val)
                except ValueError:
                    result[current_key][sub_key] = sub_val
        if current_key and current_list:
            result[current_key] = current_list
        return result
    except Exception:
        return None

def load_baselines(genre="general"):
    """按类型加载基线,general 基线作为 fallback 合并
    已缓存: 同一 genre 第二次调用直接返回缓存副本。
    """
    cache_key = genre
    if cache_key in _BASELINES_CACHE and isinstance(_BASELINES_CACHE.get(cache_key), dict):
        import copy
        return copy.deepcopy(_BASELINES_CACHE[cache_key])
    paths = []
    if genre != "general":
        gp = DE_AI_DIR / f"baselines_{genre}.json"
        if gp.exists():
            paths.append(gp)
    paths.append(DE_AI_DIR / "baselines.json")
    bl = {"_meta": {"merged_from": []}}
    for p in paths:
        if p.exists():
            try:
                with open(p, "r", encoding="utf-8", errors="replace") as f:
                    data = json.load(f)
                    bl["_meta"]["merged_from"].append(p.name)
                    if "meta" in data:
                        bl.setdefault("meta", {}).update(data["meta"])
                    for key, val in data.items():
                        if key != "meta":
                            bl[key] = val
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                print(f"  [!] 基线文件损坏: {p.name} ({e}), 跳过")
                continue
    _BASELINES_CACHE[cache_key] = bl
    return bl


def get_bl(key, field, default):
    obj = _BASELINES_CACHE.get(key, {})
    if isinstance(obj, dict):
        return obj.get(field, default)
    return default

BANNED_P0 = ["毋庸置疑","不可否认","值得一提的是","总而言之","众所周知",
    "命运的齿轮","从某种意义上说","在某种程度上","由此可见",
    "综上所述","不可忽视的是",]
# IRON_RULES.md 同步确认:与 IRON_RULES.md P0 列表一致(含全部 11 项)
BANNED_TEMPLATES = ["不是","而是","仿佛","犹如","宛若","眼中闪过一丝",
    "嘴角勾起一抹","他知道","她知道","他感到","她感到","他觉得"]
BANNED_ENDINGS = ["他终于明白了","她终于懂得","他不知道的是",
    "更大的挑战还在后面","总的来说"]
AI_CONNECTIVES = ["随着","首先","其次","最后","因此","此外","总之","然而"]
TEMPLATE_OPENINGS = ["随着","在当今","众所周知"]
LLM_PLANNING = ["用户希望","用户需要","我需要确保","我需要考虑","接下来要考虑",
    "需要确定","需要检查","需要确保","可以考虑","可能的结构","可能的设计",
    "因此,","然后我们要","我们需要","我们要确保",
    "好的,","嗯,","让我","首先我需要",
    "首先,","接下来,","最后,","现在开始","接下来我",
    "我需要思考","我要考虑","我打算","我需要重新",
    "让我再想","让我重新","现在确定了","好的现在",]
LLM_THINKING_PREFIX = ["Thinking","思考过程","推理过程","让我思考","让我分析"]

def is_cn(c): return '\u4e00' <= c <= '\u9fff'
def extract_cn(t): return [c for c in t if is_cn(c)]
def split_sents(t): return [s.strip() for s in re.split(r'[\u3002\uff01\uff1f!?\n]|\.{6,}',t) if len(extract_cn(s))>=2]
def split_paras(t): return [p.strip() for p in t.split('\n') if len(extract_cn(p))>=10]

def detect_md(t):
    r = []
    if re.search(r'\*\*[^*]+\*\*', t): r.append("粗体 ** 残留")
    if re.search(r'^#{1,6}\s', t, re.M): r.append("标题 # 残留")
    if '```' in t: r.append("代码块 ``` 残留")
    if re.search(r'>\s', t, re.M): r.append("引用块 > 残留")
    if re.search(r'^\s*[-*]\s', t, re.M): r.append("列表 - 残留")
    return r

def detect_chatgpt(t):
    r = []
    if re.search(r'turn0(search|image|news|file)\d+', t): r.append("turn0xxx标记")
    if 'utm_source=chatgpt.com' in t or 'utm_source=openai' in t: r.append("utm_source标记")
    return r

def count_punct(t):
    tc = len(extract_cn(t))
    if tc==0: return {}
    return {"comma":t.count(",")/tc*1000,"period":t.count("。")/tc*1000,
        "exc":t.count("!")/tc*1000,"que":t.count("?")/tc*1000,
        "dash":(t.count("--")+t.count("-"))/tc*1000,
        "colon":t.count(":")/tc*1000}

def sent_stats(t, _sents=None):
    ss = _sents if _sents is not None else split_sents(t)
    if not ss: return {}
    l = [len(extract_cn(s)) for s in ss]
    m = sum(l)/len(l); v = sum((x-m)**2 for x in l)/len(l)
    subj = sum(1 for s in ss[:50] if re.match(r'^[他她它]',s[:4]))
    return {"avg":round(m,1),"std":round(math.sqrt(v),1),"n":len(l),
        "subj_ratio":round(subj/max(len(ss[:50]),1),2)}

_DETECT_CFG = _load_detection_yaml()
if _DETECT_CFG and isinstance(_DETECT_CFG, dict):
    # 仅合并有效 key
    _CONFIG_MERGED_KEYS = []
    if "banned_p0" in _DETECT_CFG:
        BANNED_P0 = list(dict.fromkeys(BANNED_P0 + _DETECT_CFG["banned_p0"]))
        _CONFIG_MERGED_KEYS.append("banned_p0")
    if "banned_endings" in _DETECT_CFG:
        BANNED_ENDINGS = list(dict.fromkeys(BANNED_ENDINGS + _DETECT_CFG["banned_endings"]))
        _CONFIG_MERGED_KEYS.append("banned_endings")
    if "ai_connectives" in _DETECT_CFG:
        AI_CONNECTIVES = list(dict.fromkeys(AI_CONNECTIVES + _DETECT_CFG["ai_connectives"]))
        _CONFIG_MERGED_KEYS.append("ai_connectives")
    if "template_openings" in _DETECT_CFG:
        TEMPLATE_OPENINGS = list(dict.fromkeys(TEMPLATE_OPENINGS + _DETECT_CFG["template_openings"]))
        _CONFIG_MERGED_KEYS.append("template_openings")


class Result:
    def __init__(s): s.passed=True; s.issues=[]; s.sev=1
    def add(s,n,p,d,sev=1):
        if not p: s.passed=False
        if d: s.issues.extend(d)
        if not p: s.sev=sev
        return {"name":n,"passed":p,"details":d}

def d1_banned(t):
    r=Result(); f=[]
    for w in BANNED_P0:
        c=t.count(w)
        if c>0: f.append(f"P0禁用词'{w}'x{c}")
    for e in BANNED_ENDINGS:
        if e in t: f.append(f"P0禁用结尾'{e}'")
    for w in AI_CONNECTIVES:
        c=t.count(w)
        if c>3: f.append(f"P1'{w}'x{c}")
    p1_templates = {"仿佛":2,"犹如":2,"宛若":2,"眼中闪过一丝":1,"嘴角勾起一抹":1}
    for tmpl, threshold in p1_templates.items():
        c = t.count(tmpl)
        if c >= threshold:
            f.append(f"P1模板'{tmpl}'x{c}")
    # 定义所有引号字符(用于上下文豁免判断)
    QUOTE_CHARS = ['\u201c','\u201d','\u300c','\u300d','\u300e','\u300f','"']
    # 一次性构建引号位图,供整个循环复用(O(n),而非每个词重建一次)
    in_quote = [False] * len(t)
    for q_open, q_close in [('\u201c', '\u201d'), ('\u300c', '\u300d'), ('\u300e', '\u300f'), ('"', '"')]:
        depth = 0
        for i, c in enumerate(t):
            if c == q_open:
                depth += 1
            elif c == q_close:
                depth = max(0, depth - 1)
            elif depth > 0:
                in_quote[i] = True
    for w in ["他知道","她知道","他感到","她感到","他觉得"]:
        cnt = t.count(w)
        # 引号豁免：位图已在外层一次性构建（含智能引号+ASCII双引号）
        non_quote_cnt = 0
        wlen = len(w)
        search_from = 0
        while True:
            pos2 = t.find(w, search_from)
            if pos2 == -1:
                break
            if not any(in_quote[pos2:pos2+wlen]):
                non_quote_cnt += 1
            search_from = pos2 + 1
        if non_quote_cnt > 0:
            f.append(f"P0直接告情'{w}'x{non_quote_cnt}")
    r.add("禁用词扫描",len(f)==0,f,3)
    return r

def d2_humanizer(t):
    r=Result(); f=[]
    hype=["重要意义","奠定了","不可替代","极其重要","划时代"]
    for w in hype:
        if w in t: f.append(f"夸大意义'{w}'")
    promo=["值得关注","值得推荐","不容错过","必读"]
    for w in promo:
        if w in t: f.append(f"宣传语言'{w}'")
    filler=["我们可以看到","我们会发现","换句话说","也就是说"]
    for w in filler:
        if w in t: f.append(f"填充短语'{w}'")
    r.add("Humanizer-zh",len(f)<=2,f,2)
    return r

def d3_qmai(t):
    r=Result(); f=[]; sc=0
    if t.count("不是")>2 and t.count("而是")>2: f.append("1-二分对照过度"); sc+=1
    col=sum(1 for l in t.split('\n') if ':' in l and len(l)>20 and not l.strip().startswith('"'))
    if col>3: f.append("2-冒号滥用"); sc+=1
    if t.count("你")>3: f.append("3-二人称泛滥"); sc+=1
    rw=sum(t.count(w) for w in ["首先","其次","最后","总之"])
    if rw>3: f.append("4-路标词密集"); sc+=1
    if "让我们一起" in t: f.append("5-协作腔"); sc+=1
    if re.search(r'在.{0,10}的今天',t) or re.search(r'随着.{0,20}的发展',t):
        f.append("7-模板式开头"); sc+=1
    pa_matches = re.findall(r'([^,。!?\n"]{2,15},)([^,。!?\n"]{2,15},)([^,。!?\n"]{2,15},)', t)
    parallel_count = 0
    for m in pa_matches:
        segs = [s.strip().rstrip(',') for s in m]
        if len(segs) == 3:
            pref = [s[:min(4, len(s))] for s in segs]
            if len(set(pref)) == 1:
                seg_lens = [len(s) for s in segs]
                len_diff = max(seg_lens) - min(seg_lens)
                median_len = sorted(seg_lens)[1]
                if median_len > 0 and len_diff / median_len < 0.6:
                    parallel_count += 1
    if parallel_count > 2: f.append(f"6-排比结构x{parallel_count}"); sc+=1
    aw=sum(1 for w in ["复杂","微妙","深刻","关键","证明","独特"] if w in t)
    if aw>=3: f.append("8-AI特征词堆叠"); sc+=1
    for w in ["显然","事实上","实际上","本质上"]:
        if w in t: f.append(f"9-总结腔'{w}'"); sc+=1; break
    mt=sum(t.count(w) for w in ["然而","但是","不过"])
    if mt>4: f.append("10-机械转折"); sc+=1
    md_score = 0
    if re.search(r'\*\*[^*]+\*\*', t): md_score += 1
    if re.search(r'^#{1,6}\s', t, re.M): md_score += 1
    if '```' in t: md_score += 1
    if re.search(r'^\s*[-*]\s', t, re.M): md_score += 1
    if md_score >= 2: f.append(f"11-Markdown过度x{md_score}"); sc+=1
    r.add("QMAI 11项",sc<=3,f,2)
    return r

def d4_baselines(t, genre="general", baselines=None, _cn_chars=None, _sents=None):
    r=Result(); f=[]
    pc=count_punct(t)
    cn_chars = _cn_chars if _cn_chars is not None else extract_cn(t)
    ss = sent_stats(t, _sents=_sents) if _sents else sent_stats(t)
    tc = len(cn_chars)
    if not ss or tc<100: r.add("统计基线",True,["文本过短"]); return r
    bl = baselines if isinstance(baselines, dict) else _BASELINES_CACHE
    bl_sent_mean = bl.get("avg_sent_len_chars",{}).get("mean",29.7)
    bl_sent_std = bl.get("avg_sent_len_chars",{}).get("std",10.0)
    bl_cp = bl.get("comma_period_ratio",{}).get("mean",3.9)
    bl_eq = bl.get("excl_ques_per_1000",{}).get("mean",9.75)
    bl_dash = bl.get("dash_per_1000",{}).get("p95",4.47)
    bl_colon = bl.get("colon_per_1000",{}).get("p95",9.78)
    bl_sent_p5 = bl.get("avg_sent_len_chars",{}).get("p5",19.7)
    bl_sent_p95 = bl.get("avg_sent_len_chars",{}).get("p95",39.7)
    if ss["avg"]<bl_sent_p5 or ss["avg"]>bl_sent_p95:
        f.append("句长"+str(ss["avg"])+" (基线"+str(bl_sent_p5)+"-"+str(bl_sent_p95)+")")
    bl_std = get_bl("avg_sent_len_chars","std",10.0)
    std_low = round(bl_std * 0.6, 1)
    if ss["std"]<std_low: f.append(f"句长方差{ss['std']}<{std_low}")
    if pc.get("period",0)>0:
        cp=pc["comma"]/pc["period"]
        cp_low = round(bl_cp * 0.3, 1)
        cp_high = round(bl_cp * 2.2, 1)
        if cp<cp_low or cp>cp_high: f.append(f"逗号句号比{cp:.1f} (基线{cp_low}-{cp_high})")
    eq=pc.get("exc",0)+pc.get("que",0)
    eq_low = round(bl_eq * 0.3, 1)
    if eq < eq_low: f.append(f"感叹+问号密度{eq:.1f}/千字<{eq_low}")
    if pc.get("dash",0)>bl_dash: f.append(f"破折号{pc['dash']:.2f}>P95{bl_dash}")
    # subj_ratio 已在添加为基线指标维度,但当前 calibrate_baselines.py 未输出此字段
    # 若基线无此数据则静默跳过
    subj_bl = bl.get("subj_ratio",{}).get("p95",0)
    if subj_bl > 0 and ss.get("subj_ratio",0) > subj_bl:
        f.append(f"句首人物主语{ss['subj_ratio']*100:.0f}%>P95{subj_bl*100:.0f}%")
    min_chars = 2000 if genre in ("xianxia","xuanhuan","urban") else 1500
    if tc<min_chars:
        if tc < 300:
            r.add("统计基线",True,["文本过短,跳过"])
            return r
        print(f"  [i] 字数{tc}<{min_chars}(参考,不影响AI判定)")
    r.add("统计基线",len(f)<=3,f,2)
    return r

def d6_subject_distribution(t, _sents=None):
    sents = _sents if _sents is not None else split_sents(t)
    if len(sents) < 10:
        return Result()
    r = Result()
    human_subj = 0
    time_env = 0
    total = 0
    for s in sents[:80]:
        s = s.strip()
        if not s:
            continue
        total += 1
        first_word = s[:3]
        time_markers = ["第", "这", "那", "明", "昨", "今", "当", "随", "在", "从", "向", "朝", "往"]
        if any(s.startswith(m) for m in time_markers):
            time_env += 1
            continue
        if first_word[0] in "他她它你我":
            human_subj += 1
    if total == 0:
        return r
    human_ratio = human_subj / total
    if human_ratio > 0.50 and total >= 10:
        r.issues.append(f"句首人物主语{human_ratio:.0%}(真书~35%,AI~65%)")
        r.passed = False
    return r

# ── d7: IRON_RULES P0 补全 — 连续主谓宾 / !!!??? / 省略号过度 ──

def d7_sentence_patterns(t, _sents=None):
    """检测: 连续3句主谓宾相同 / !!!???堆砌 / 省略号过度"""
    r = Result()
    issues = []

    if _sents is None:
        _sents = split_sents(t)

    # 1. 连续3句以上主谓宾结构相同（检测句首人称重复）
    if len(_sents) >= 3:
        consecutive_svo = 0
        max_consecutive = 0
        for s in _sents:
            s_clean = s.strip()
            if s_clean and len(s_clean) >= 2:
                first_two = s_clean[:2]
                if first_two in ("他打", "他走", "他看", "他说", "他拿", "他去", "他来",
                                 "她打", "她走", "她看", "她说", "她拿", "她去", "她来"):
                    consecutive_svo += 1
                    max_consecutive = max(max_consecutive, consecutive_svo)
                else:
                    consecutive_svo = 0
        if max_consecutive >= 3:
            issues.append(f"连续{max_consecutive}句主谓宾结构相同（P0禁止）")

    # 2. 连续 !!! 或 ??? 堆砌
    exclamation_pile = len(re.findall(r"!{3,}", t))
    question_pile = len(re.findall(r"\?{3,}", t))
    if exclamation_pile > 0:
        issues.append(f"感叹号堆砌x{exclamation_pile}（P0禁止）")
    if question_pile > 0:
        issues.append(f"问号堆砌x{question_pile}（P0禁止）")

    # 3. 省略号过度使用（>5次/千字 或连续出现）
    ellipsis_count = t.count("……") + t.count("...")
    cn_chars = extract_cn(t)
    tc = len(cn_chars)
    if tc > 0:
        ellipsis_per_k = ellipsis_count / tc * 1000
        if ellipsis_per_k > 5:
            issues.append(f"省略号密度{ellipsis_per_k:.1f}/千字（P0建议<5）")
    # 连续省略号
    if "…………" in t or "......" in t:
        issues.append("连续省略号堆砌（P0禁止）")

    r.add("句式模式", len(issues) == 0, issues, 3)
    return r

# ── d8: IRON_RULES P1 补全 — 副词过载 / 对话标签 / 路标词 ──

def d8_style_details(t):
    """检测: 副词过载 / 对话标签单一 / 路标词重复 / 模板句首"""
    r = Result()
    issues = []

    # 1. 副词过载: 缓缓/慢慢/轻轻/悄悄 每千字 > 4次
    cn_chars = extract_cn(t)
    tc = max(len(cn_chars), 1)
    adverbs = ["缓缓", "慢慢", "轻轻", "悄悄", "渐渐", "微微", "淡淡"]
    for adv in adverbs:
        count = t.count(adv)
        per_k = count / tc * 1000
        if per_k > 4:
            issues.append(f"副词'{adv}'过载: {per_k:.1f}/千字（P1建议≤4）")

    # 2. 对话标签单一: "说道/问道/回答" >50%
    dialogue_tags = re.findall(r'(说道|问道|回答|答道|说道|喊道|叫道|骂道|笑道)', t)
    if dialogue_tags:
        total_tags = len(dialogue_tags)
        simple_tags = sum(1 for tag in dialogue_tags if tag in ("说道", "问道", "回答"))
        if total_tags > 5 and simple_tags / total_tags > 0.5:
            issues.append(f"对话标签'{'说道/问道/回答'}'占比{simple_tags/total_tags:.0%}（P1建议<50%）")

    # 3. 模板句首: 与此同时/紧接着/就在这时/恰在此时
    template_starts = ["与此同时", "紧接着", "就在这时", "恰在此时", "正在这时"]
    paras = split_paras(t)
    template_count = 0
    for p in paras:
        for ts in template_starts:
            if p.strip().startswith(ts):
                template_count += 1
                break
    if template_count >= 3:
        issues.append(f"模板句首x{template_count}（P1建议避免）")

    # 4. 段落边界路标词重复: 然而/但是/不过 连续段落开头
    road_signs = ["然而", "但是", "不过", "可是", "因此", "所以", "于是"]
    consecutive_road = 0
    for p in paras:
        started_with_road = any(p.strip().startswith(rs) for rs in road_signs)
        if started_with_road:
            consecutive_road += 1
        else:
            consecutive_road = 0
    if consecutive_road >= 3:
        issues.append(f"连续{consecutive_road}段以路标词开头（P2建议优化）")

    r.add("风格细节", len(issues) == 0, issues, 2)
    return r


def d5_structure(t, _cn_chars=None):
    r=Result(); f=[]
    f.extend(detect_md(t)); f.extend(detect_chatgpt(t))
    esc = t.count(chr(27))
    if esc > 0:
        f.append(f"ANSI控制字符x{esc}")
    for p in split_paras(t):
        for o in TEMPLATE_OPENINGS:
            if p.startswith(o): f.append('模板开头: ' + p[:30]); break
    feel=sum(t.count(w) for w in ["感到","觉得","内心","心中","心里"])
    if feel>3: f.append(f"情绪告知词x{feel}")
    plan_hits = sum(t.count(w) for w in LLM_PLANNING)
    if plan_hits >= 3:
        f.append(f"LLM规划式语言x{plan_hits}")
    think_hits = sum(1 for pfx in LLM_THINKING_PREFIX if t.startswith(pfx) or pfx in t[:200])
    if think_hits > 0:
        f.append(f"LLM推理前缀x{think_hits}")
    r.add("结构异常",len(f)<=0,f,2)
    return r

def run_all(text,bname="未知",genre="general",safety=False,fast_mode=False):
    # baselines 按需加载，通过参数传递（避免全局态并发安全风险）
    baselines = load_baselines(genre)
    bl_meta = baselines.get("meta", {})
    cn_chars = extract_cn(text)
    sents = split_sents(text)
    tc=len(cn_chars)
    det_count = "六套" if not safety else "六套+安全过滤"
    print(f"\n{'='*50}")
    print(f"  {det_count}检测引擎 - 完整扫描")
    print(f"  文件: {bname}")
    print(f"  类型: {genre}")
    print(f"  字数: {tc} 汉字")
    if bl_meta.get("total_chapters", 0) > 0:
        print(f"  基线样本: {bl_meta['total_chapters']} 章")
    print(f"{'='*50}\n")
    label = "4.统计基线(7698本)" if genre=="general" else f"4.统计基线({genre.upper()})"
    if fast_mode:
        detectors=[("1.禁用词扫描(P0)",d1_banned),("5.AI文结构异常",d5_structure),("6.主语分布",d6_subject_distribution)]
        w_dict={"1.":3,"5.":2,"6.":2}
    else:
        detectors=[("1.禁用词扫描(P0)",d1_banned),("2.Humanizer-zh",d2_humanizer),
            ("3.QMAI 11项",d3_qmai),(label,d4_baselines),
            ("5.AI文结构异常",d5_structure),("6.主语分布",d6_subject_distribution),
            ("7.句式模式(P0补全)",d7_sentence_patterns),("8.风格细节(P1补全)",d8_style_details)]
        w_dict={"1.":3,"2.":2,"3.":2,"4.":2,"5.":3,"6.":2,"7.":3,"8.":2}
    all_issues=[]; vote=0; w_total=sum(w_dict.values())
    if fast_mode:
        print(f"  [模式] 快速检测(跳过Humanizer/QMAI/基线统计)")
    safety_blocked = False
    safety_loaded = False
    if safety:
        try:
            sys.path.insert(0, str(Path(__file__).parent))
            from content_safety_filter import run_safety
            safety_loaded = True
        except Exception as e:
            print(f"  [FAIL] 6.内容安全过滤  模块加载失败: {e}")
            print(f"          安全过滤已禁用,请检查 content_safety_filter.py 是否存在\n")
        if safety_loaded:
            try:
                safe_result = run_safety(text, bname)
                if safe_result["severity"] != "PASS":
                    safety_blocked = safe_result["severity"] == "BLOCK"
            except Exception as e:
                print(f"  [FAIL] 6.内容安全过滤  检测执行出错: {e}\n")
    for name,fn in detectors:
        if fn is d4_baselines:
            det=fn(text, genre, baselines, _cn_chars=cn_chars, _sents=sents)
        elif fn is d5_structure:
            det=fn(text, _cn_chars=cn_chars)
        elif fn is d6_subject_distribution:
            det=fn(text, _sents=sents)
        elif fn is d7_sentence_patterns:
            det=fn(text, _sents=sents)
        else:
            det=fn(text)
        issue_count=len(det.issues)
        for iss in det.issues: all_issues.append(iss)
        if not det.passed: vote+=next((v for k,v in w_dict.items() if name.startswith(k)), 1)
        status="[OK]" if det.passed else "[!]"
        print(f"  {status} {name.ljust(35)} {issue_count} 个问题")
    ratio=vote/max(w_total,1)
    # 阈值校准自 baselines.json (默认 GREEN<0.15, YELLOW<0.4)
    GREEN_TH = baselines.get("meta", {}).get("thresholds", {}).get("green", 0.15)
    YELLOW_TH = baselines.get("meta", {}).get("thresholds", {}).get("yellow", 0.4)
    if ratio<GREEN_TH: cls="[GREEN] 人类创作"
    elif ratio<YELLOW_TH: cls="[YELLOW] 疑似AI"
    else: cls="[RED] AI创作特征"
    print(f"\n  加权投票: {vote}/{w_total} = {ratio:.1%}")
    print(f"\n{'-'*50}")
    print(f"  判定: {cls}")
    print(f"  总问题: {len(all_issues)} 处")
    if all_issues:
        print(f"\n  问题清单:")
        for iss in all_issues[:15]: print(f"    ! {iss}")
        if len(all_issues)>15: print(f"    ...及{len(all_issues)-15}处其他")
    print(f"{'-'*50}\n")
    return {"classification":cls,"total_issues":len(all_issues),"issues":all_issues[:15]}

def main():
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--input","-i",required=True)
    p.add_argument("--genre","-g",default="general",
        choices=["general","xianxia","xuanhuan","dushi","yanqing",
                 "xuanyi","kehuan","lishi","junshi","youxi"],
        help="小说类型(默认通用基线)")
    p.add_argument("--json",action="store_true")
    p.add_argument("--no-safety",action="store_true",help="禁用内容安全过滤(第6套,默认开启)")
    p.add_argument("--mode",default="polish",choices=["fast","polish"],
        help="检测模式:fast(快速/日更,仅d1+d5) | polish(精修/发布,全六套+d6主语分布)")
    p.add_argument("--chapter","-c")
    args=p.parse_args()
    ip=Path(args.input)
    if not ip.exists(): print(f"[ERR] 文件不存在: {ip}"); sys.exit(1)
    if not args.safety:
        print("[WARN] --no-safety: 内容安全过滤已关闭。建议保留默认开启以过滤违规内容。")
    sf_path = Path(__file__).parent / "content_safety_filter.py"
    if args.safety and not sf_path.exists():
        print(f"[WARN] content_safety_filter.py 不存在于: {sf_path.parent}")
        print(f"      安全过滤不可用，跳过。如需开启请确保文件存在。")
        args.safety = False
    with open(ip,"r",encoding="utf-8",errors="ignore") as f: text=f.read()
    fast_mode = (args.mode == "fast")
    result=run_all(text,args.chapter or ip.stem,args.genre,args.safety,fast_mode)
    if args.json: print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=="__main__": main()
