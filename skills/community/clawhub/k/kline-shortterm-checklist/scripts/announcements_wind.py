#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""announcements_wind.py — 公告核查（Wind 金融数据 MCP）本地辅助脚本。

背景：Wind 是 MCP 连接器，由助手(agent)调用 mcp__wind-finance__get_company_announcements 拉取公告；
本脚本不直连 Wind，而是做两件事：
  (1) --plan : 读 candidates.json（+ screen_meta.json 取数据基准日），生成待查清单
                announcement_plan.json（每只候选 1 个自然语言查询：近期公告）。
                说明：Wind 的 NL 检索对"塞满关键词"的严格查询常返回空，对"X 最近公告"这种自然宽泛查询最稳；
                四类信号（减持/业绩预警/违规/利好）全部由 --merge 的本地关键词扫描覆盖，无需多次查询。
  (2) --merge: 读助手汇总的 wind_raw.json（Wind 原始返回，按 code 归集的 items），做关键词扫描，
                输出 announcement_check.json：{code:{reduction,earnings_warn,penalty,good_news,hits,checked}}。
                扫描内置【两道防线】，缺一不可：
                  防线1 标题过滤——只保留标题含本公司名/代码的条目，丢弃跨公司/基金招募书/指数类噪音
                    （实测 Wind 曾返回"广发利鑫灵活配置混合型证券投资基金招募说明书"等无关条目）；
                  防线2 否定语境守卫——公告常用"未受到处罚/未被立案/未涉及重大资产重组…股份回购"等
                    自证清白句式，若只扫关键词会把否定句误判为 penalty/good_news，故 PENALTY/EARN/GOOD
                    三类均配 *_NEG 否定守卫（scan 内部已生效）。
报告 report_html.py 读取 announcement_check.json，把九不买 #3/#5/#6 的 👁 人工项翻转为客观判定。

用法:
  python announcements_wind.py --plan [--top N]
  python announcements_wind.py --merge
"""
import json, os, re, sys

def norm_key(code):
    return code[2:] if code[:2] in ("sh", "sz", "bj") else code

def _fold(s):
    """全角→半角 + 去空白 + 大写，用于公司简称与公告标题的宽松比对。
    交易所简称常含全角字母与空格（东财返回 "特  力Ａ"），而 Wind 公告标题用半角
    （"特  力A:…"）。直接子串比对会判定"标题不含本公司名"→ 把本公司公告整体误丢，
    形成**假阴性**（报告谎称"已客观核查、无减持无违规"，比误判更危险）。
    受影响面：所有简称含全角字母的 A/B 股（特力Ａ、万科Ａ、深物业Ａ…）。"""
    if not s:
        return ""
    out = []
    for ch in s:
        o = ord(ch)
        if o == 0x3000:            # 全角空格
            continue
        if 0xFF01 <= o <= 0xFF5E:  # 全角 ASCII → 半角
            ch = chr(o - 0xFEE0)
        if ch.isspace():
            continue
        out.append(ch)
    return "".join(out).upper()

# 简称通用后缀，用于"核心词"回退匹配（摘帽/改名导致简称错位，如 ST联创 ↔ 联创股份）
_NAME_TAIL = re.compile(r'(股份|集团|控股|实业|科技|电力|A|B)+$')

def _title_belongs(title, name, code):
    """防线1：判断公告标题是否属于本公司。三级匹配，宽严兼顾：
    ① 代码命中；② 折叠后简称命中；③ 剥离 ST/*ST 前缀与通用后缀的核心词命中（≥2字）。
    不做"首字/短词"兜底，避免把跨公司噪音（基金招募书/指数类）放进来。"""
    ft, fn, fc = _fold(title), _fold(name), _fold(code)
    if fc and fc in ft:
        return True
    if not fn:
        return False
    if fn in ft:
        return True
    core = _NAME_TAIL.sub('', re.sub(r'^\*?ST', '', fn))
    return bool(core) and len(core) >= 2 and core in ft

# 减持：命中"减持"且未被否定（未减持/提前终止减持/不减持/未收到…减持计划）
REDUCE_NEG = re.compile(r'(未减持|未实施减持|尚未实施.{0,10}减持|提前终止减持|提前终止.{0,8}减持|终止减持计划|终止.{0,6}减持计划|不减持|未收到.{0,25}减持|不存在减持|无减持计划)')
REDUCE_POS = re.compile(r'减持')
# 业绩预警（负面）：预减/预亏/亏损/下滑/同比下降/由盈转亏
EARN_NEG = re.compile(r'(业绩预减|预亏|预减|亏损|业绩下滑|同比下降|归母净利润下降|由盈转亏|业绩变动.*下降)')
# 业绩预警否定语境：如"未亏损/不存在亏损"，用于排除反向误命中
EARN_NEG_GUARD = re.compile(r'(未亏损|不存在亏损|未出现亏损|无亏损|未预亏|未业绩预减|不存在业绩预减|未预减|未同比下降|未出现下降)')
# 【防线4·业绩方向判定】业绩预告正文必然大量出现"上年同期亏损 XXX 万元"这类
# 对照基准表述，纯关键词扫描会把"扭亏为盈"的利好公告误判成业绩预减。
# 实测：银河电子 002519 半年报预告归母由 -2881 万转为 +544 万（扭亏为盈、营收+114%），
# 却因正文含"上年同期为亏损2,881.68万元"被判 earnings_warn → #6 误剔除。
# 规则：命中正向信号且无"当期预亏"表述时，判定业绩向好，不触发 #6。
EARN_POS = re.compile(r'(扭亏为盈|由负转正|由亏转盈|业绩预增|预计.{0,6}盈利|'
                      r'净利润.{0,12}同比(?:增长|大增|激增|大幅增长|飙升|上升|增加)|'
                      r'净利润.{0,12}(?:大幅增长|大幅提升|同比翻番))')
# 【防线4 强化 · 归母方向直读】(2026-08-19)
# 靠穷举"同比大增/激增/飙升/大幅增长"等修饰词永远追不全——实测联创股份 300343 半年报
# 归母 +142.36%、扣非 +440.27%、营收 +38.80%（明确向好），却因正文含"弥补【累计】亏损"
# 与"经营现金流同比下降42.70%"被判 earnings_warn，而 EARN_POS 只认"同比增长"、
# 不认"同比大增" → 防线4 未触发 → #6 误剔除。
# 对策：财报/预告正文几乎必然出现"归属于上市公司股东的净利润 X 元，同比<方向><幅度>%"，
# **直读这个方向**比模糊关键词可靠得多，且天然区分"营收增but利润降"（海兴电力 603556
# 营收+24.66% 而归母-16.67%，须真实触发 #6）。
NP_DIR = re.compile(r'归属于(?:上市公司|母公司)股东的净利润[^。；\n]{0,60}?'
                    r'同比(增长|大增|激增|大幅增长|飙升|上升|增加|下降|下滑|减少|降低|亏损)')
_NP_UP = {'增长', '大增', '激增', '大幅增长', '飙升', '上升', '增加'}

def _np_direction(t):
    """归母净利润同比方向：'up' / 'down' / None（解析不到）。
    以首现为准——正文首处通常是主口径业绩摘要，后文多为分部/表格重复。"""
    m = NP_DIR.search(t or "")
    if not m:
        return None
    return 'up' if m.group(1) in _NP_UP else 'down'
EARN_CUR_LOSS = re.compile(r'(业绩预亏|业绩预减|由盈转亏|仍处于亏损|继续亏损|持续亏损)')
# 九不买 #6 以【归母】口径判定。扣非亏损是质量提示、不是业绩预亏，
# 否则"归母扭亏为盈但扣非仍亏"的公司会被硬否决（银河电子 002519 实测中招）。
EARN_DEDUCT = re.compile(r'(扣非|扣除非经常性损益)')


def _cur_loss(t):
    """当期是否【归母】口径预亏/预减：命中点前 20 字含扣非字样的，视为扣非口径，跳过。"""
    for mt in EARN_CUR_LOSS.finditer(t):
        if EARN_DEDUCT.search(t[max(0, mt.start() - 20):mt.start()]):
            continue
        return True
    return False
# 违规/处罚/监管
PENALTY = re.compile(r'(处罚|警示函|立案|违规|监管函|问询函|通报批评|公开谴责|被立案|收到.{0,6}(函|决定))')
# 违规/处罚否定语境（关键！公告常用"未受到处罚/未被立案"等自证清白，
# 若只扫关键词会把这类否定句误判为 penalty=true，导致 #6 误翻"不买"）。
# 覆盖范围：处罚、立案、违规 三类常见否定自证表达。
PENALTY_NEG = re.compile(
    r'(未受到.{0,15}处罚|没有受过.{0,15}处罚|未受处罚|未被处罚|无.{0,6}处罚|'
    r'不涉及.{0,10}处罚|不存在.{0,20}处罚|未遭处罚|'
    r'未被立案|不存在.{0,20}立案|没有.{0,15}立案|未遭立案|不涉及.{0,10}立案|'
    r'未违规|不存在违规|无违规|不涉及违规)')
# 利好（用于 #3 利好兑现风险判定）：中标/合同/重组类 + 回购/增持类正向催化
# （回购方案、实控人/股东增持属明确利好，临近兑现需注意"买预期卖事实"风险）
GOOD = re.compile(r'(中标|签订合同|重大合同|重组|资产注入|获得批准|项目中标|签署协议|大单|订单|回购|增持)')
# 利好否定语境：公告常用"未涉及重大资产重组/股份回购/增持"等自证清单，
# 若只扫关键词会把这类否定句误判为 good_news=True（典型如股价异动公告的"不存在/未涉及…"清单）。
GOOD_NEG = re.compile(
    r'(未涉及.{0,20}(重组|回购|增持|资产注入)|不存在.{0,20}(重组|回购|增持|资产注入)|'
    r'不涉及.{0,20}(重组|回购|增持)|无.{0,8}(回购|增持)|未实施.{0,10}(回购|增持)|'
    r'不实施.{0,10}(回购|增持)|未回购|未增持)')

# ── 防线3 · 标题类型门控（2026-08-10 新增，实测必需，勿删）────────────────────
# 背景：防线2 的否定守卫覆盖不全，实测仍有大量**结构性误判**：
#   · "独立董事提名人/候选人声明与承诺" 正文含"最近三年未受到中国证监会行政处罚"变体
#     → 误判 penalty → 九不买 #6 误剔除（拓日新能 002218、光韵达 300227 实测中招）
#   · "半年度报告" 正文含合规自证段 → 误判 penalty
#   · "关于对外担保的进展公告" 正文含"下降/亏损"字样 → 误判 earnings_warn（龙蟠科技 603906）
#   · "关于董事、高级管理人员辞职暨补选董事的公告" / "控股股东股权结构变动暨完成工商变更登记"
#     → 误判 reduction → #5 误剔除（光韵达 300227）
# 根因：否定句式变体无穷无尽，靠穷举 NEG 正则堵不住。
# 对策：**关键词命中必须与公告标题的类型相符才算数**——正文关键词只做"确认"，
#       标题决定"这份公告到底是不是这一类"。这把误判从"堵漏"变成"白名单"，鲁棒得多。
RED_TITLE = re.compile(r'(减持|权益变动|股份转让|大宗交易|持股.{0,8}变动|清仓)')
EARN_TITLE = re.compile(r'(业绩预告|业绩快报|业绩预亏|业绩预减|业绩变动|业绩说明|'
                        r'年度报告|半年度报告|季度报告|年报|中报|季报)')
PEN_TITLE = re.compile(r'(处罚|问询函|监管函|警示函|关注函|立案|违规|责令|公开谴责|'
                       r'通报批评|纪律处分|风险警示|整改|监管措施|自律监管)')
GOOD_TITLE = re.compile(r'(中标|合同|订单|重组|资产注入|回购|增持|收购|投资|合作|'
                        r'协议|战略|签署|项目|获批|批准)')
# 利好标题反例：限制性股票"回购注销"是激励失效、非正向回购；股份"回购注销"同理。
# "投资者关系活动记录表"含"投资"二字但只是调研纪要，非利好事件；"异常波动"是风险提示不是利好。
GOOD_TITLE_NEG = re.compile(r'(回购注销|注销.{0,10}限制性股票|限制性股票.{0,10}(回购|注销)|'
                            r'投资者关系|异常波动|风险提示|募集说明书|募集资金)')


def scan(text, title=None):
    """关键词扫描。title 传入时启用【防线3 标题类型门控】（推荐；merge 已默认传入）。
    title=None 为兼容旧调用的无门控模式。"""
    t = text or ""
    ti = title if title is not None else ""
    gate = title is not None
    reduction = bool(REDUCE_POS.search(t)) and not bool(REDUCE_NEG.search(t))
    # 业绩预警：命中负面词且不在否定语境（如"未亏损"）中
    earnings_warn = bool(EARN_NEG.search(t)) and not bool(EARN_NEG_GUARD.search(t))
    # 违规/处罚：命中且不在"未受到处罚/未被立案"等自证否定语境中，
    # 否则会把董事候选资格里的"没有受过处罚"等清白表述误判为 penalty。
    penalty = bool(PENALTY.search(t)) and not bool(PENALTY_NEG.search(t))
    # 利好：命中且不在"未涉及重组/股份回购/增持"等自证否定清单中
    good_news = bool(GOOD.search(t)) and not bool(GOOD_NEG.search(t))
    if gate:  # 防线3：正文命中必须与标题类型相符，否则视为噪音
        reduction = reduction and bool(RED_TITLE.search(ti))
        earnings_warn = earnings_warn and bool(EARN_TITLE.search(ti))
        penalty = penalty and bool(PEN_TITLE.search(ti))
        good_news = good_news and bool(GOOD_TITLE.search(ti)) \
            and not bool(GOOD_TITLE_NEG.search(ti))
    # 防线4：业绩方向判定。优先直读【归母净利润同比方向】（最可靠）；
    # 解析不到时才回退到 EARN_POS 关键词正向信号。归母同比下降 → 保持触发（真实下滑）。
    if earnings_warn:
        d = _np_direction(t)
        if d == 'up' and not _cur_loss(t):
            earnings_warn = False
        elif d is None and EARN_POS.search(t) and not _cur_loss(t):
            earnings_warn = False
    return reduction, earnings_warn, penalty, good_news

def load_cands(cwd):
    with open(os.path.join(cwd, "candidates.json"), encoding="utf-8") as f:
        return json.load(f)

def load_date(cwd):
    try:
        with open(os.path.join(cwd, "screen_meta.json"), encoding="utf-8") as f:
            m = json.load(f)
        return m.get("data_date", "最近交易日")
    except FileNotFoundError:
        return "最近交易日"

def plan(cwd, top=None):
    cands = load_cands(cwd)
    date = load_date(cwd)
    plan_list = []
    sel = cands[:top] if top else cands
    for c in sel:
        code, name = c["code"], c["name"]
        plan_list.append({
            "code": code, "name": name, "window": f"{date} 及前 60 个交易日",
            "queries": [
                f"{name} {code} 最近公告",
            ],
        })
    out = os.path.join(cwd, "announcement_plan.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(plan_list, f, ensure_ascii=False, indent=1)
    print(f"[plan] 已写出 announcement_plan.json：{len(plan_list)} 只候选，每只 1 个查询（{name} 最近公告，本地扫描覆盖减持/业绩/违规/利好）")
    print(f"       数据基准日={date}。下一步：对每只候选调用 mcp__wind-finance__get_company_announcements(query=..., top_k=1) 拉取，")
    print(f"       把返回 items 归集进 wind_raw.json，再运行 `python announcements_wind.py --merge`。")

def merge(cwd):
    raw_path = os.path.join(cwd, "wind_raw.json")
    if not os.path.exists(raw_path):
        print("[merge] 未找到 wind_raw.json，跳过（报告将回落到 👁 人工项）。")
        return
    raw = json.load(open(raw_path, encoding="utf-8"))
    # 防线1（标题过滤）：Wind 的 NL 检索即使 query 是"X 最近公告"，仍可能返回
    # 跨公司/基金招募书/指数类噪音条目（实测曾返回"广发利鑫灵活配置混合型证券投资基金
    # 招募说明书"等）。这类条目标题不含本公司名/代码，必须丢弃，否则其正文里的
    # "未受到公开谴责、处罚"等字眼会污染关键词扫描。故只保留标题含本公司名或代码的条目。
    name_map = {norm_key(c["code"]): c["name"] for c in load_cands(cwd)}
    check = {}
    n_drop = 0
    uncovered = []      # 有返回但零条通过防线1 / 空返回 → 未真正覆盖，须标 👁
    for rec in raw:
        code = norm_key(rec.get("code", ""))
        name = name_map.get(code, "")
        items = rec.get("items", []) or []
        red = earn = pen = god = False
        hits = []
        h_red, h_earn, h_pen, h_god = [], [], [], []
        kept = 0
        for it in items:
            title = it.get("title", "") or ""
            # 标题不属于本公司 → 视为跨公司/基金/指数噪音，丢弃。
            # 比对走 _title_belongs（折叠全角/空格 + ST/后缀回退），不可用裸 `name not in title`：
            # 全角简称（"特  力Ａ" vs 标题 "特  力A:…"）会导致本公司公告被整体误丢。
            if name and not _title_belongs(title, name, code):
                n_drop += 1
                continue
            kept += 1
            content = it.get("content", "") or ""
            # 防线3：必须把 title 单独传入，scan 才会启用"标题类型门控"。
            # 只传拼接文本会退化成无门控模式（历史 bug，曾导致 #6 大面积误剔除）。
            r, e, p, g = scan(title + "\n" + content, title=title)
            red, earn, pen, god = red or r, earn or e, pen or p, god or g
            tag = f"{it.get('date', '')} {title}"
            # 按类别分桶：报告展示理由时必须取"触发该条规则的那份公告"，
            # 否则会出现"判定=减持、理由却是业绩预告"的错配。
            if r:
                h_red.append(tag)
            if e:
                h_earn.append(tag)
            if p:
                h_pen.append(tag)
            if g:
                h_god.append(tag)
            if r or e or p or g:
                hits.append(tag)
        # 假阴性防护：拿到 items 却一条都没通过防线1（或 Wind 返回 total:0），
        # 说明简称/代码对不上（Wind 代码冲突、改名等）→ 该票**未被真正核查**。
        # 此时绝不能写 checked=True，否则报告会谎称"已客观核查、无减持无违规"。
        # checked=False 时 report_html.py 自动回落 👁 人工核查路径。
        ok = kept > 0
        check[code] = {"reduction": red, "earnings_warn": earn, "penalty": pen,
                       "good_news": god, "hits": hits,
                       "hits_reduction": h_red, "hits_earn": h_earn,
                       "hits_penalty": h_pen, "hits_good": h_god, "checked": ok,
                       "n_items": len(items), "n_kept": kept}
        if not ok:
            uncovered.append(f"{code}({name or '?'})")
    out = os.path.join(cwd, "announcement_check.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(check, f, ensure_ascii=False, indent=1)
    n_red = sum(1 for v in check.values() if v["reduction"])
    n_earn = sum(1 for v in check.values() if v["earnings_warn"])
    n_pen = sum(1 for v in check.values() if v["penalty"])
    print(f"[merge] 已写出 announcement_check.json：{len(check)} 只；减持命中 {n_red}、业绩预警 {n_earn}、违规 {n_pen}")
    print(f"        本次丢弃跨公司/基金/指数类噪音标题 {n_drop} 条（防线1·标题过滤）")
    if uncovered:
        print(f"        ⚠️ 未真正覆盖 {len(uncovered)} 只（零条通过防线1 或空返回），"
              f"已标 checked=False → 报告回落 👁 人工核查：{'、'.join(uncovered)}")
    print(f"        报告将据此把九不买 #3/#5/#6 的 👁 翻转为客观判定。")

def main():
    cwd = os.getcwd()
    args = sys.argv[1:]
    if "--plan" in args:
        top = None
        if "--top" in args:
            i = args.index("--top")
            top = int(args[i + 1])
        plan(cwd, top)
    elif "--merge" in args:
        merge(cwd)
    else:
        print("用法: python announcements_wind.py --plan [--top N] | --merge")

if __name__ == "__main__":
    main()
