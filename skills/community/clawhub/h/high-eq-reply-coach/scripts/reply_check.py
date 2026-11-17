#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高情商回复教练（chat-reply-coach）确定性核心 —— 纯标准库零依赖

四个用途：
  1. 输入快筛  --check-input  chat.txt   危机信号（家暴/抑郁/自伤/轻生）→ 转介卡 rc=3；
                                          操控请求（PUA/打压/拿捏）→ 拒绝+替代路径 rc=4；
                                          否则 CLEAN rc=0。
  2. 场景速查  --list / --scene <key>     场景卡：识别信号/框架/骨架/雷区（rc=0）。
  3. 输出自扫  --check-output draft.md    生成稿过定性词/操控词/承诺词黑名单，
                                          命中即列明并 rc=1，禁止带险交付。
  4. 三档质量门 --check-draft draft.md   三档齐全/每条带注解/简短档真短/档间非同句。
  5. 演示      --demo                     跑一条完整链路示例。

硬约束（与 SKILL.md 安全红线一一对应）：
1. 危机信号命中 → 只给专业求助路径，绝不生成话术；
2. 操控请求命中 → 拒绝 + 给真诚表达替代，绝不教 PUA；
3. 生成稿绝不含关系定性词（他不爱你/老板想裁你）、操控术语、效果承诺词；
4. 缺数据不猜：check-input 只报告命中事实，不解读、不延伸。

判定设计（2026-11-02 独立审查后重构，详见 docs/chat-reply-coach_独立审查报告_20261102.md）：
- 危机信号分「强信号（词组级）」+「弱信号（词根 + 必要语境锚点）」两层，
  早期只用精确子串匹配单字词根，导致「我最近很抑郁 / 活着好累 / 我要解脱」等
  高频表达全部漏报；弱信号层专治此类漏报，同时用语境锚点控制误报。
- 「重开」游戏语境与自杀黑话同形，改用上下文判定（游戏锚点优先豁免）。
- 操控请求改「动作请求式」判定：术语 + 请求动词共现才拦，
  受害者自述（「他对我冷暴力」）不再被误判为施控者求教。
- 三档质量门的分块锚点改为「行级档位标签」，不再用全文首个匹配位置，
  避免导语枚举三档名导致好稿被误杀。
- 黑名单扫描区分「话术本体」与「注解/教学举例区」，注解里的反例引用不再误拦。

用法示例：
    python reply_check.py --check-input chat.txt
    python reply_check.py --text "对方发了这句话，先帮我筛"
    python reply_check.py --scene rel_coldwar
    python reply_check.py --check-output draft.md
    python reply_check.py --check-draft draft.md
    python reply_check.py --demo
"""

import argparse
import difflib
import re
import sys
from pathlib import Path

# Windows 控制台中文输出兜底
if sys.stdout and hasattr(sys.stdout, "buffer"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ---------------------------------------------------------------------------
# ① 危机信号 · 强信号层：词组级命中，几乎无歧义
#     命中即转介，不生成话术。宁可误报（用户随口一说会自己忽略），不可漏报。
#     个别强词有科普/研究等良性语境，走 CRISIS_STRONG_GUARD 白名单豁免。
# ---------------------------------------------------------------------------
CRISIS_STRONG = [
    "家暴", "被打了", "动手打我", "打我", "扇我", "扇耳光", "扇我耳光", "揪头发",
    "拿刀", "掐我", "掐脖子", "威胁要杀", "杀了我", "同归于尽",
    "自杀", "自残", "自伤", "割腕", "吞药", "过量服药",
    "不想活了", "活不下去", "想死", "轻生", "活着没意思", "没意思活着",
    "想结束这一切", "结束自己的生命", "伤害自己",
    "抑郁症", "抑郁了",
    "紫砂",          # 年轻人自杀隐喻（谐音）
]

# 强信号的良性语境豁免：{词: 豁免正则}。命中豁免语境（如科普/研究/求助专业帮助）
# 且窗口内没有第一人称痛苦的自我指涉时放行。
# 注意「抑郁症」天然双义（患病自述 vs 科普讨论），靠「研究/门诊/量表/公开课」等
# 第三人称/知识语境豁免；第一人称痛苦表达（我抑郁了/我有抑郁症很痛苦）照拦。
CRISIS_STRONG_GUARD = {
    "抑郁症": r"(研究|成因|科普|门诊|量表|评分|诊断标准|公开课|讲座|识别|数据|发病率|患者.{0,4}(?:家属|亲友)|得了抑郁症的(?:人|患者)|治疗抑郁症|抑郁症的(?:治疗|预防|成因|症状))",
    "自杀":   r"(研究|成因|科普|干预|热线|预防|数据|统计|公开课|讲座|自杀的(?:原因|预防|干预|心理)|防自杀|自杀干预)",
    "抑郁":   r"(研究|成因|科普|门诊|量表|诊断标准|公开课|讲座|识别|数据|治疗)",
}

# ② 危机信号 · 弱信号层：(词根正则, 展示标签, 必要语境锚点, 豁免语境)
#    语境锚点存在才命中 —— 避免「抑郁研究」「工作解脱了」「这题想不开」这类误报。
#    语境锚点为 None 的条目必须有 guard 豁免兜底，防止纯词根误报。
CRISIS_WEAK = [
    (r"抑郁", "抑郁",
     r"抑郁了|抑郁症|抑郁得|很抑郁|有点抑郁|特别抑郁|总是抑郁|感觉抑郁|情绪.{0,3}抑郁|"
     r"一直抑郁|心里.{0,3}抑郁|中度抑郁|重度抑郁|抑郁情绪|抑郁状态|抑郁得厉害",
     r"抑郁(研究|模型|识别|检测|量表|评分|指数|数据|测试|门诊|科普|诊断标准|公开课|讲座)"
     r"|抑郁症的(成因|治疗|预防|症状|干预)|研究抑郁症"),
    (r"好累|很累|太累|撑不住|撑不下去|熬不下去|熬不住|受不了", "活着好累",
     r"活着|人生|生命|日子|每天|这样下去|没意思|煎熬|撑|熬",
     r"(工作|加班|上班|复习|背单词|代码|论文|考试|项目|搬砖|客户|健身|跑步|加班).{0,8}(好累|很累|太累)|"
     r"(好累|很累|太累).{0,8}(但|不过|，然后|先睡|先去|就充实)"),
    (r"没意思", "没意思",
     r"活着|人生|生命|日子|活下去|每天|不想过",
     r"没意思(吃|玩|逛|看|去哪儿|去哪|换|关)"),
    (r"解脱", "解脱",
     r"想|要|不如|活着|人生|生命|结束|一切",
     r"解脱(了|出来)?(这份|工作|束缚|压力|困境|房贷|束缚)"),
    (r"想不开", "想不开",
     r"想|总是|一直|活着|人生|生命|日子|心里|这日子|总觉得|有时候|最近",
     r"(工作|代码|方案|方法|问题|题目|这道|怎么做|思路|技术|设计|算法|逻辑|公式|语法|半天|好几天|纠结|卡).{0,8}想不开|想不开.{0,8}(工作|代码|方案|方法|问题|题目|这道|算法|逻辑|公式|语法|卡|纠结)"),
    (r"想消失|消失算了|干脆消失|没有我|想不见", "想消失",
     r"想|要|干脆|不如|离开|世界|没人|大家.{0,4}更好",
     r"消失(了|不见|在视野|的动态|在群里|在列表)"),
]

# ③「重开」特殊处理：游戏语境（这局重开 / 重开一把 / 队友说重开）极常见，
#    自杀黑话（我想重开 / 重开人生）也真实存在。同一个词无法靠词表区分，
#    改为上下文判定：命中游戏锚点 → 豁免；命中黑暗语境锚点 → 拦截；
#    两者都没有（孤立一句「重开吧」）→ 按游戏语境处理，放行。
CRISIS_GAME_CONTEXT = (
    r"局(?![面])|这把|那把|开黑|匹配|排位|上分|连跪|翻盘|游戏|队友|"
    r"再来|再开|下一把|又开|重新开|开一局|再来一局|重开一把|重开一局|重开一下"
)
CRISIS_DARK_CONTEXT = r"人生|生命|活着|想死|要死|结束|一切|从零|重来一次|想|要|不如"

# 歧义豁免：这些词在特定常见短语里**不是**危机信号。
# 例：「我想死你了」是情话不是轻生；「晚上打我电话」是约电话不是家暴。
# 处理方式：先把豁免短语从文本里抹掉，再看危机词是否仍然存在。
# 只豁免该词自身——文案里若另有真危机词（如同时出现「不想活了」）仍会命中。
CRISIS_EXEMPT = {
    "想死": ["想死你", "想死我"],          # 想死你了 / 想死我了 = 想念
    "打我": ["打我电话", "打我手机", "打我个电话", "打我过来"],
}

# ---------------------------------------------------------------------------
# 操控请求识别（输入扫描）
#
# 关键区分：施控者求教 vs 受害者自述。
#   「教我几招怎么拿捏女朋友」 → 操控（拦截）
#   「他对我冷暴力半个月，我怎么办」 → 受害者求助（放行，走 rel_coldwar）
# 早期版本把「冷暴力」「忽冷忽热」当操控词硬拦，导致本 skill 自己的两个核心场景
# （冷战破冰 / 争吵降温）被自己的快筛拦死 —— 现改为动作请求式判定。
# ---------------------------------------------------------------------------

# ① 明确操控请求：独立成句即可判定（不需要上下文共现）
MANIP_STRONG = [
    "让她离不开", "让他离不开", "让她离不开我", "让他离不开我",
    "废物测试", "服从性测试", "精神控制", "欲擒故纵", "洗脑",
    "怎么拿捏", "怎么调教", "怎么驯服", "怎么pua", "怎么PUA",
    "怎么吊着", "怎么打压", "怎么冷落",
    "教我拿捏", "教我调教", "教我pua", "教我PUA", "教我打压", "教我冷暴力",
    "教教我拿捏", "教教我打压", "教我忽冷忽热",
]

# ①b 强操控词的良性语境豁免：受害者/旁观者在讨论如何应对这些手法时，
#     「欲擒故纵」「打压」等词以**客体身份**出现（破解/应对/摆脱/识破…），
#     不是求教。命中豁免语境则该强词不算操控请求。
MANIP_STRONG_GUARD = {
    "欲擒故纵": r"(破解|应对|识破|看穿|反制|摆脱|对付|怎么破|怎么办|他的|她的|对方)",
    "精神控制": r"(破解|应对|识破|摆脱|逃离|自救|报警|求助|他对我|她对我|对象对我|从.{0,6}走出来)",
    "洗脑":     r"(破解|应对|识破|摆脱|自救|报警|他对我|她对我|被.{0,4}洗脑|怎么走出来)",
    "废物测试": r"(应对|怎么回|怎么破|识别|他的|她的|对方发)",
    "服从性测试": r"(应对|识别|拒绝|他的|她的|对方|怎么破)",
}

# ② 操控术语：需与「请求动词」共现才算求教
MANIP_TERMS = ["pua", "PUA", "拿捏", "调教", "打压", "吊着", "忽冷忽热", "冷暴力", "驯服"]

# 请求动词/句式（施控者求教的标志）
MANIP_REQUEST_RE = re.compile(
    r"(教我|教教|想学|求教|请教|怎么用|怎么玩|怎么搞|怎么操作|怎么整|怎么收拾|"
    r"怎样才能|怎么才能|如何才能|帮我用|帮我搞|给我一套|帮我出一套|几招|拿一套|出一套)"
)

# 求助语境（受害者在求助，不是在求教）——命中则该术语不算操控请求
MANIP_GUARD_RE = re.compile(
    r"(应对|处理|面对|破解|摆脱|结束|停止|反制|拒绝|如何避免|怎么办|怎么处理|"
    r"怎么回复|怎么回|不知道怎么回|该怎么办)"
)

# 生成稿黑名单（输出自扫）：定性词 / 操控术语 / 效果承诺
OUTPUT_BLOCKLIST = [
    # 关系定性（替用户给人下结论）
    "他不爱你", "她不爱你", "不爱你了", "不在乎你", "没把你当",
    "就是想逼你走", "想裁掉你", "想裁你", "看不起你",
    "渣男", "渣女", "绿茶", "白眼狼",
    # 操控术语（生成稿里绝不出现）
    "废物测试", "服从性测试", "精神控制", "欲擒故纵", "冷暴力惩罚",
    "打压一下", "忽冷忽热", "拿捏住", "吊着他", "吊着她",
    # 效果承诺（话术没有保证）
    "保证让他", "保证让她", "一定能让他", "一定能让她", "这样回他肯定",
    "百分百有效", "稳赢", "必回",
    "一定会回你", "肯定回你", "秒回必", "百试百灵", "绝对有效", "屡试不爽",
    "必定成功", "保证成功",
]
# 兼容旧引用名（历史脚本/快照引用过 _OUTPUT_BLOCKLIST）
_OUTPUT_BLOCKLIST = _OUTPUT_BLOCKLIST = OUTPUT_BLOCKLIST
# 教学/举例语境标记：命中该标记的行跳过黑名单扫描
# （注解里的反例引用、SKILL.md 自己举的「不要写成…」例子都不该被拦）
_TEACHING_MARKER_RE = re.compile(
    r"(注解|风险\s*[:：]|写法\s*[:：]|备注\s*[:：]|说明\s*[:：]|不要写成|别写成|"
    r"不说|不暗示|禁止|避免写成|黑名单|改写|改成|重写|翻车|错误示范|反面教材|"
    r"一律拒绝|不得|不能出现|应改写|误杀|反例)"
)

# ---------------------------------------------------------------------------
# 危机转介卡 / 操控拒绝卡（全文固定，与 references/refusal_playbook.md 一致）
# ---------------------------------------------------------------------------
CRISIS_CARD = """【先停一下】

你提到的内容（命中：{hits}）已经超出「怎么回消息」能帮到的范围。
你的安全和状态，比回什么都重要。建议现在就联系：

- 全国心理援助热线：12356（24 小时，免费）
- 遭遇家暴或人身威胁：全国妇联维权热线 12338；紧急情况直接拨 110
- 也可以先告诉你信任的家人或朋友——别一个人扛

话术生成已停止。这不是拒绝你，是这件事值得更专业的人帮你。
（如果你只是转述别人的话或随口一说，请忽略本提示，重新描述你的场景即可。）"""

MANIPULATION_REFUSAL = """【这个忙我帮不了】

你要的这类技巧（命中：{hits}）属于操控话术——靠打压、制造焦虑、情绪操纵
维持的关系，伤人也不长久，我不提供。

但如果你真正的目标是「让这段关系变好 / 让对方重视我」，这些我能帮：
- 坦诚表达需求：用非暴力沟通（观察-感受-需要-请求）说清楚你要什么；
- 建立边界：DESC 法（描述-表达-明确-结果）守住你的底线；
- 提升吸引力：靠真实状态与稳定情绪，不靠套路。

告诉我具体场景（谁、发生了什么、你想达到什么），我按正规框架给你写。"""

# ---------------------------------------------------------------------------
# 场景库（结构化直查）
# 字段：name / 关系 / 识别信号 / 主框架 / 备选框架 / 骨架 / 雷区
# 与 references/scenes.md 互为详略两个版本，改动时两边同步。
# ---------------------------------------------------------------------------
SCENES = {
    "work_refuse_overtime": {
        "name": "拒绝加班/下班派活", "关系": "职场-对上级",
        "signals": "下班时间派活、周末加急、「辛苦一下」、临时需求",
        "framework": "三明治拒绝法（接受-转折-建设）",
        "alt": "简短确认+边界声明",
        "skeleton": "接住态度（「好的，这个需求我记下了」）→ 摆事实（「手头 A 项目今晚要交」）→ 给替代（「明早九点我先处理这个，十点前给您初稿」）",
        "pitfalls": "别只回「做不了」；别情绪化吐槽；连续拒绝必须给替代方案，否则印象分流失；反复派活按渐进阶梯逐级加码（软→明→坚）",
    },
    "work_report_up": {
        "name": "向上汇报/邀功", "关系": "职场-对上级",
        "signals": "周报/述职/项目进展/「做得怎么样了」",
        "framework": "PREP（结论-理由-例证-重申）",
        "alt": "STAR（情境-任务-行动-结果）",
        "skeleton": "结论先行（「本周按期完成，超预期 10%」）→ 数据支撑 → 归因到动作（不是运气）→ 下一步计划",
        "pitfalls": "别流水账；别只讲苦劳不讲结果；数据要可核实",
    },
    "work_performance": {
        "name": "绩效面谈/谈薪", "关系": "职场-对上级",
        "signals": "绩效沟通/调薪/年终面谈/「你觉得自己这季度怎么样」",
        "framework": "STAR 举证 + PREP 诉求",
        "alt": "锚定+让步",
        "skeleton": "STAR 列 2-3 个可量化成果 → PREP 提诉求（结论=期望数字/评级）→ 沉默等对方出价，别自己往下砍",
        "pitfalls": "别用「我需要钱」当理由；别当场接受第一个报价；诉求要有市场对照",
    },
    "work_blame": {
        "name": "被甩锅/被质疑", "关系": "职场-平级/上级",
        "signals": "群里点名、「这个锅谁背」、被质疑能力、跨部门推责、被骂/被批评",
        "framework": "SBI（情境-行为-影响）还原事实",
        "alt": "DESC（描述-表达-明确-结果）",
        "skeleton": "先稳情绪不回怼 → 时间线还原事实（带证据：邮件/记录）→ 聚焦解决（「现在最重要的是补窟窿，分工建议…」）",
        "pitfalls": "别在群里互撕；别情绪化反问「你什么意思」；事实陈述不带人身评价",
    },
    "work_urge": {
        "name": "催人/被催进度", "关系": "职场-通用",
        "signals": "「好了吗」「几点能给」、催别人或被催、催进度/催稿",
        "framework": "SBI + 明确承诺",
        "alt": "PREP",
        "skeleton": "催别人：说影响不说人品（「这个 delay 会卡住下游测试」）+ 要具体时间；被催：给准确时间点 + 风险提示前置",
        "pitfalls": "别回「尽快」（等于没说）；别催第三次还不升级",
    },
    "work_apologize": {
        "name": "工作失误道歉", "关系": "职场-通用",
        "signals": "出错了/背锅已定/需要认错止损",
        "framework": "承认-补救-预防 三段式",
        "alt": "SBI",
        "skeleton": "承认具体错误（不甩锅不找借口）→ 已做/将做的补救 → 预防机制（「我已加了双人复核」）",
        "pitfalls": "别「对不起但是…」（但是一出口道歉清零）；别过度自责表演",
    },
    "work_credit": {
        "name": "被抢功劳/成果被冒领", "关系": "职场-平级/上级",
        "signals": "同事把我的方案说成他做的、汇报里没提我、功劳被抢、被冒领",
        "framework": "SBI 还原事实 + 不撕破脸的自我主张",
        "alt": "PREP（先摆事实结论，再提协作机制）",
        "skeleton": "先私下沟通不在群里开撕 → 事实链（什么场合、说了什么、我的哪部分产出留痕在哪）→ 谈影响（「后续这类项目建议明确署名与分工」）→ 提制度性诉求（针对流程不针对人）",
        "pitfalls": "别在群里公开对撕（赢口舌输关系）；别只抱怨不给机制；事实必须留痕（文档版本/群记录/邮件），没留痕先补证据再谈",
    },
    "work_resign": {
        "name": "提离职/辞职开口", "关系": "职场-对上级",
        "signals": "想离职、辞职、提离职怎么开口、拿到offer要走",
        "framework": "PREP + 感恩-明确-交接",
        "alt": "三明治",
        "skeleton": "一对一私下面谈（不在群里/邮件突袭）→ 明确表态（「我决定离职」不试探不拉扯）→ 一段具体的感谢（学到的一件实事）→ 交接方案（时间线/文档/带人）→ 离职原因只说中性（发展方向），不吐槽不控诉",
        "pitfalls": "别拿离职当谈判筹码（除非真想留，且想好被挽留的答案）；原因不评价具体人；提前量按合同；领导当场挽留时别当场松口，回去想清楚再答复",
    },
    "work_ostracism": {
        "name": "被孤立/被排挤", "关系": "职场-同事/团队",
        "signals": "群里没人理、开会不叫我、同事抱团、被排挤",
        "framework": "SBI 观察事实 + 自我节奏（先事实后归因）",
        "alt": "找关键人一对一 DESC",
        "skeleton": "先区分「真孤立」还是「自己多心」（列三个可观察事实再下结论）→ 不急于讨好融入 → 找一个相对中立的关键人一对一了解 → 工作上保持稳定交付 → 若涉霸凌/歧视，留证据走 HR 路径",
        "pitfalls": "别群发小作文质问；别过度讨好换认同（越讨好越被轻看）；长期霸凌且 HR 无效→认真评估去留，不硬扛",
    },
    "rel_icebreak": {
        "name": "破冰/开场", "关系": "情感-暧昧/初识",
        "signals": "刚加好友/想开场/尬聊中/「在吗」之后没话",
        "framework": "共同话题 + 开放式提问",
        "alt": "场景钩子（从对方动态找切入点）",
        "skeleton": "从对方可见信息找具体点（头像/动态/共同群话题）→ 一句具体评论（不是「你好漂亮」）→ 开放式问题收尾（不用「是不是」能答完的）",
        "pitfalls": "别查户口式连问；别「在吗」开场；别上来就夸外表",
    },
    "rel_flirt": {
        "name": "撩人/暧昧升温/主动表白", "关系": "情感-暧昧/恋人",
        "signals": "想撩、暧昧期、想逗TA开心、「在干嘛」「想你了」、土味情话、调情升温、想表白/怎么开口",
        "framework": "撩人三式（具体夸/好奇缺口/推拉lite）",
        "alt": "场景钩子 + 夸张幽默",
        "skeleton": "具体化夸奖（夸细节不夸整体）或好奇缺口（说半句留半句，如「刚看到个东西想到你了」）或推拉lite（先小调侃再夸，调侃只落无伤大雅的小事）",
        "pitfalls": "调侃落点必须抬高对方或落中性小事——落贬低=打压=PUA（黑名单硬拦）；土味情话连发显油腻；不开黄腔；对方明确反感即停",
    },
    "rel_coldwar": {
        "name": "冷战/已读不回/被冷暴力", "关系": "情感-恋人",
        "signals": "冷战、已读不回超一天、吵架后互不联系、他对我冷暴力、对象不回我消息、催我回消息",
        "framework": "非暴力沟通 NVC（观察-感受-需要-请求）",
        "alt": "先递台阶+约时间谈",
        "skeleton": "不翻旧账、不问「你什么意思」→ 描述事实（「这三天我们没说话」）→ 说自己的感受（「我挺难受的」）→ 提一个小请求（「今晚打个电话好吗」）",
        "pitfalls": "破冰第一条别讲道理分对错；别用「你再不回我就…」威胁；别找朋友轮番劝",
    },
    "rel_apologize": {
        "name": "情感道歉", "关系": "情感-恋人/家人",
        "signals": "自己理亏/说错话/对方生气冷战",
        "framework": "承认-共情-改正 三段式",
        "alt": "NVC",
        "skeleton": "承认具体哪件事错了（不是「我错了行了吧」）→ 说出对方的感受（「你当时肯定很委屈」）→ 具体改进行动（不是空头保证）",
        "pitfalls": "别「对不起，但是…」；别道歉完立刻要对方表态原谅；空头支票式保证扣分",
    },
    "rel_marriage_pressure": {
        "name": "催婚/被逼相亲", "关系": "情感-家人（父母/亲戚）",
        "signals": "催婚、催生、被安排相亲、亲戚追问「什么时候结婚」",
        "framework": "三明治 + 明确边界（不给虚假希望）",
        "alt": "DESC（描述-表达-明确-结果）",
        "skeleton": "先接住关心（「我知道你们是为我好」）→ 明确表态（不含糊，不用「再说吧」）→ 给替代（「我自己在接触，有进展会告诉你们」或「这两年我想先稳工作」）→ 若被逼过紧，约定下次再谈的时间",
        "pitfalls": "别硬顶伤感情（出发点是关心）；别用「再说吧」拖（拖延会被反复追问）；最忌承诺一个糊弄的假期限（后面更难收）；相亲被逼到人身攻击时先暂停再谈",
    },
    "rel_parents": {
        "name": "跟父母沟通大事", "关系": "情感-家人（父母）",
        "signals": "跟爸妈说大事：换工作/不考研/去外地/对象他们不满意/要钱创业",
        "framework": "PREP + 接关心-摆计划-要信任",
        "alt": "NVC",
        "skeleton": "先接住他们的担心（「我知道你们怕什么」）→ 摆事实摆计划（不是甩情绪）→ 要一个具体的信任（「给我一年，年底看结果」）→ 分歧大不当场争输赢，约下次再谈",
        "pitfalls": "别「你们不懂」开场（一出口就对立）；要钱/要自由都要给可验证的里程碑；当场吵起来用暂停技术，改天再谈",
    },
    "rel_reject": {
        "name": "拒绝表白/邀约", "关系": "情感-被追求",
        "signals": "被表白想拒绝/不想去的约会/备胎想脱身、表白被拒后怎么回应",
        "framework": "明确-感谢-不吊着",
        "alt": "三明治",
        "skeleton": "感谢对方的真诚 → 明确表态（不含糊、不「再说吧」）→ 不给虚假希望（不说「以后说不定」）",
        "pitfalls": "模糊拒绝=吊着，伤害更大；别发好人卡还继续享受对方付出",
    },
    "rel_boundary": {
        "name": "立边界（查手机/越界要求）", "关系": "情感-恋人/家人",
        "signals": "被要求查手机/报备行踪/断绝异性朋友/借钱给对象、被嫌弃/被说胖",
        "framework": "DESC（描述-表达-明确-结果）",
        "alt": "NVC",
        "skeleton": "描述具体行为（「昨天你翻了我手机」）→ 表达感受（「我不舒服，感觉不被信任」）→ 明确边界（「手机是个人隐私」）→ 说清后果与替代（「有问题可以直接问我」）",
        "pitfalls": "边界说出口就要执行；别一边拒绝一边内疚补偿；涉及转账投资的越界要求转 scam-radar",
    },
    "rel_conflict": {
        "name": "争吵降温", "关系": "情感/家人",
        "signals": "对话在升级、开始翻旧账、音量变高、互相指责、对方说我胖了/嫌我",
        "framework": "暂停技术 + NVC",
        "alt": "先接情绪再谈事",
        "skeleton": "叫暂停（「我们都冷静半小时再聊」→ 这不是逃避，是说清时间的暂停）→ 回来后先认自己的情绪部分 → NVC 说事不评价人",
        "pitfalls": "别在气头上做决定（分手/辞职/拉黑）；别翻三个月前的旧账；人身攻击的话收不回",
    },
    "gen_refuse_money": {
        "name": "拒绝借钱", "关系": "通用-朋友/亲戚",
        "signals": "借钱/周转/担保/「过几天还你」",
        "framework": "明确+简短+不解释过多",
        "alt": "三明治",
        "skeleton": "直接表态（「这次帮不上」）→ 一句理由即可（不编长篇故事，理由越多破绽越多）→ 可选给非钱的帮助（「帮你看看有没有正规渠道」）",
        "pitfalls": "别问「借多少」（一问就难拒绝）；别被「这么点钱都不借」绑架；对方若提投资/理财抵债，转 scam-radar；反复来借按渐进阶梯逐级加码",
    },
    "gen_school": {
        "name": "家校沟通（家长对老师）", "关系": "通用-家长对老师/学校",
        "signals": "家长群被@、跟老师沟通孩子问题、老师反馈情况怎么回",
        "framework": "PREP + 配合姿态",
        "alt": "SBI",
        "skeleton": "先回应事实与感谢关注 → 家庭侧动作（「我们在家会…」）→ 请老师同步观察点 → 有异议时先私下找老师，不在群里争",
        "pitfalls": "别在家长群抬杠/晒娃/拉踩；涉及孩子被区别对待，先做事实记录（时间/事情/在场人）再沟通；情绪上头的话隔夜再发",
    },
    "gen_complaint": {
        "name": "客诉/维权沟通", "关系": "通用-对商家/机构",
        "signals": "买到问题商品/服务缩水/要退款投诉、对方不给钱、房东涨租",
        "framework": "STAR 摆事实 + 明确诉求",
        "alt": "PREP",
        "skeleton": "事实链（时间/订单/问题/凭证）→ 依据（三包/消法/合同条款）→ 明确诉求（退货/退款/赔偿金额）→ 升级路径预告（「未解决将向 12315 投诉」）",
        "pitfalls": "别情绪化辱骂（截图对你不利）；诉求要具体可执行；口头承诺要落到文字",
    },
}

# 口语别名 → scene key，宽容输入。
# 方向性规则：
#   · 「被表白/拒绝表白」→ rel_reject（拒人）；「我要表白/怎么表白」→ rel_flirt（开口），不搞反。
#   · 「催进度/催稿」→ 职场催；「对象催/催我回」→ 情感冷战，别被单字「催」抢路由。
#   · 单字别名一律不收（「催」「表白」单字歧义太大），只收方向明确的组合词。
_ALIASES = {  # 口语别名 → scene key，宽容输入
    "加班": "work_refuse_overtime", "派活": "work_refuse_overtime",
    "周末加班": "work_refuse_overtime", "周末派活": "work_refuse_overtime",
    "周末值班": "work_refuse_overtime", "周末去公司": "work_refuse_overtime",
    "周末也来": "work_refuse_overtime", "临时需求": "work_refuse_overtime",
    "汇报": "work_report_up", "邀功": "work_report_up",
    "绩效": "work_performance", "谈薪": "work_performance",
    "甩锅": "work_blame", "背锅": "work_blame", "骂我": "work_blame",
    "批评我": "work_blame", "质疑我": "work_blame", "不背这个锅": "work_blame",
    "催进度": "work_urge", "催稿": "work_urge", "催一下": "work_urge",
    "催我进度": "work_urge", "催我交": "work_urge", "催我发": "work_urge",
    "领导催": "work_urge", "老板催": "work_urge",
    "工作道歉": "work_apologize", "失误": "work_apologize",
    "抢功劳": "work_credit", "抢功": "work_credit", "冒领": "work_credit",
    "离职": "work_resign", "辞职": "work_resign",
    "孤立": "work_ostracism", "排挤": "work_ostracism",
    "破冰": "rel_icebreak", "开场": "rel_icebreak",
    "撩": "rel_flirt", "撩妹": "rel_flirt", "撩汉": "rel_flirt",
    "暧昧": "rel_flirt", "调情": "rel_flirt", "升温": "rel_flirt", "土味情话": "rel_flirt",
    "表白": "rel_flirt", "我要表白": "rel_flirt", "怎么表白": "rel_flirt",
    "主动表白": "rel_flirt", "开口表白": "rel_flirt",
    "冷战": "rel_coldwar", "已读不回": "rel_coldwar",
    "不理我": "rel_coldwar", "没回我": "rel_coldwar", "不回我": "rel_coldwar",
    "不回消息": "rel_coldwar", "被冷暴力": "rel_coldwar", "冷暴力": "rel_coldwar",
    "对象催": "rel_coldwar", "他催": "rel_coldwar", "她催": "rel_coldwar",
    "催我回": "rel_coldwar",
    "催婚": "rel_marriage_pressure", "催生": "rel_marriage_pressure",
    "逼婚": "rel_marriage_pressure", "相亲": "rel_marriage_pressure",
    "父母": "rel_parents", "爸妈": "rel_parents",
    "道歉": "rel_apologize",
    "拒绝表白": "rel_reject", "被表白": "rel_reject", "表白被拒": "rel_reject",
    "备胎": "rel_reject", "不想去约会": "rel_reject",
    "边界": "rel_boundary", "查手机": "rel_boundary", "说我胖": "rel_boundary",
    "吵架": "rel_conflict", "争吵": "rel_conflict", "嫌弃我": "rel_conflict",
    "借钱": "gen_refuse_money", "借我": "gen_refuse_money", "借点": "gen_refuse_money",
    "借款": "gen_refuse_money", "借两万": "gen_refuse_money", "借一万": "gen_refuse_money",
    "借五万": "gen_refuse_money", "借三千": "gen_refuse_money", "借点钱": "gen_refuse_money",
    "周转": "gen_refuse_money", "找我妈借": "gen_refuse_money", "资金周转": "gen_refuse_money",
    "担保": "gen_refuse_money",
    "家长群": "gen_school", "家校": "gen_school", "老师": "gen_school",
    "投诉": "gen_complaint", "维权": "gen_complaint", "退款": "gen_complaint",
    "不给钱": "gen_complaint", "不付款": "gen_complaint", "涨租": "gen_complaint",
}


def _read_text(path_str):
    p = Path(path_str)
    if not p.exists():
        print(f"[ERROR] 文件不存在: {p}", file=sys.stderr)
        sys.exit(2)
    try:
        return p.read_text(encoding="utf-8-sig")  # 兼容 Windows 记事本 BOM
    except UnicodeDecodeError:
        print(f"[ERROR] 文件不是合法 UTF-8 文本: {p}", file=sys.stderr)
        sys.exit(2)


def _get_text(path, inline=None):
    """inline（--text 直接传文本）优先于文件路径，免落临时文件。"""
    if inline is not None:
        return inline
    if path:
        return _read_text(path)
    print("[ERROR] 需要文件路径，或用 --text 直接传文本。", file=sys.stderr)
    return None


# ---------------------------------------------------------------------------
# 危机信号判定
# ---------------------------------------------------------------------------
def _find_strong(text, terms, exemptions=None):
    """强信号：子串命中；豁免短语先抹掉再看是否仍存在。"""
    hits = []
    for w in terms:
        if w not in text:
            continue
        if exemptions and w in exemptions:
            residual = text
            for phrase in exemptions[w]:
                residual = residual.replace(phrase, "")
            if w not in residual:
                continue
        hits.append(w)
    return hits


def _find_crisis(text):
    """返回危机命中标签列表（去重、保序）。

    强信号层：词组级直接命中（个别词有良性语境豁免，见 CRISIS_STRONG_GUARD）。
    弱信号层：词根必须与语境锚点共现才命中（治「我最近很抑郁」这类漏报）。
    「重开」：游戏锚点优先豁免，黑暗语境锚点才拦截。
    """
    hits = []
    strong_hits = _find_strong(text, CRISIS_STRONG, CRISIS_EXEMPT)
    # 强信号的良性语境豁免（科普/研究/门诊等知识语境）
    if strong_hits and CRISIS_STRONG_GUARD:
        for w in list(strong_hits):
            guard = CRISIS_STRONG_GUARD.get(w)
            if guard and re.search(guard, text):
                # 豁免语境命中，再看第一人称痛苦自述是否同时存在：
                # 「他研究抑郁症的成因」→ 放行；「我有抑郁症想自杀」→ 自杀词已另命中
                # 2026-11-06 加固（ClawHub 安全扫描 SDI-4）：豁免语境命中但句中同时出现
                # 第一人称+痛苦/结束意图表述时，不豁免——宁可误报不可漏放
                first_person_distress = re.search(
                    r"(我|自己).{0,12}(想死|不想活|结束.{0,4}生命|离开这个世界|活着.{0,4}没(意思|意义))"
                    r"|(想死|不想活|轻生).{0,8}(念头|想法|冲动)",
                    text,
                )
                if first_person_distress:
                    continue  # 有第一人称痛苦意图，保留命中不豁免
                strong_hits.remove(w)
    hits.extend(strong_hits)

    for pat, label, ctx, guard in CRISIS_WEAK:
        for m in re.finditer(pat, text):
            window = text[max(0, m.start() - 12): m.end() + 12]
            if guard and re.search(guard, window):
                continue
            if ctx and not re.search(ctx, window):
                continue
            hits.append(label)
            break

    # 「重开」上下文判定
    if "重开" in text:
        for m in re.finditer("重开", text):
            window = text[max(0, m.start() - 12): m.end() + 12]
            if re.search(CRISIS_GAME_CONTEXT, window):
                continue
            if re.search(CRISIS_DARK_CONTEXT, window):
                hits.append("重开")
                break

    # 去重保序
    seen = set()
    out = []
    for h in hits:
        if h not in seen:
            seen.add(h)
            out.append(h)
    return out


# ---------------------------------------------------------------------------
# 操控请求判定
# ---------------------------------------------------------------------------
def _find_manipulation(text):
    """返回操控请求命中标签列表。

    ① 强操控短语独立成句即判（教我拿捏 / 让她离不开 / 服从性测试 …），
       但命中 MANIP_STRONG_GUARD 良性语境（破解/应对/识破…）的强词豁免。
    ② 操控术语需与请求动词共现（教我/怎么用/想学/求 …）才判。
    ③ 求助语境（应对/怎么办/怎么回/破解 …）命中时该术语不算操控请求 ——
       受害者自述（「他对我冷暴力，我怎么办」）不再被误拦。
    """
    hits = []
    low = text.lower()

    for w in MANIP_STRONG:
        present = (w.lower() in low) if w.isascii() else (w in text)
        if not present:
            continue
        guard = MANIP_STRONG_GUARD.get(w)
        if guard and re.search(guard, text):
            continue  # 受害者/旁观者语境，豁免
        hits.append(w)

    for term in MANIP_TERMS:
        needle = term.lower()
        for m in re.finditer(re.escape(needle), low):
            window = low[max(0, m.start() - 14): m.end() + 14]
            if MANIP_GUARD_RE.search(window):
                continue
            if MANIP_REQUEST_RE.search(window):
                hits.append(term)
                break

    seen = set()
    out = []
    for h in hits:
        if h not in seen:
            seen.add(h)
            out.append(h)
    return out


def cmd_check_input(path, inline=None):
    """输入快筛：危机 > 操控 > CLEAN。只报告命中事实，不解读。"""
    text = _get_text(path, inline)
    if text is None:
        return 2
    crisis = _find_crisis(text)
    if crisis:
        print(CRISIS_CARD.format(hits="、".join(crisis)))
        return 3
    manip = _find_manipulation(text)
    if manip:
        print(MANIPULATION_REFUSAL.format(hits="、".join(manip)))
        return 4
    print("CLEAN：未命中危机信号与操控请求，可进入场景识别流程。")
    return 0


# ---------------------------------------------------------------------------
# 输出自扫：黑名单（区分话术本体与注解/教学举例区）
# ---------------------------------------------------------------------------
_ANNOT_TAIL_RE = re.compile(
    r"[（(]?\s*(?:注解|风险|为什么这么写|适用|写法|备注|说明)\s*[:：].*$"
)


def _strip_annotation_tail(line):
    """去掉行尾的注解段（…（注解：…） / —— 注解：…），只留话术主体。"""
    return _ANNOT_TAIL_RE.sub("", line)


def _scan_blocklist(text):
    """扫描黑名单。

    跳过「教学/举例语境」行（注解里写「不要写成‘他不爱你’那种」不拦）；
    引号内的黑名单词照拦（话术本体里出现就是硬伤）。
    返回命中列表 [(词, 行号)]。
    """
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        teaching = _TEACHING_MARKER_RE.search(line)
        for w in OUTPUT_BLOCKLIST:
            if w not in line:
                continue
            if teaching:
                # 教学语境（2026-11-06 收紧，ClawHub 扫描 SDI-4）：
                # 同行黑名单词出现 ≥2 次 → 不像单纯引用，照拦；
                # 行不在注解结构里（无「注解：/风险：」前缀）→ 照拦
                if line.count(w) >= 2 or not re.match(r"\s*(注解|风险\s*[:：]|写法\s*[:：]|备注)", line):
                    hits.append((w, i))
                # 其余情况视为教学性引用，跳过
                continue
            hits.append((w, i))
    return hits


def cmd_check_output(path, inline=None):
    """生成稿自扫：定性词/操控词/承诺词黑名单，命中禁交付。"""
    text = _get_text(path, inline)
    if text is None:
        return 2
    hits = _scan_blocklist(text)
    if hits:
        print("[BLOCKED] 生成稿命中黑名单，禁止交付，请改写后重扫：", file=sys.stderr)
        for w, ln in hits:
            print(f"  - 行{ln} 命中: {w}", file=sys.stderr)
        return 1
    print("OK：生成稿未命中黑名单（定性词/操控词/承诺词）。")
    return 0


# ---------------------------------------------------------------------------
# 三档质量门
# ---------------------------------------------------------------------------

# 档位标签识别：必须是「行首的档位名」，而不是全文任意位置的第一个匹配。
# 行首可带 markdown 前缀（# / > / - / * / 数字序号 / **加粗**）。
# 后缀接受 型 / 版 / 档 / 风格 —— SKILL.md 文档里写的「坦诚直接」「撩人幽默」也算。
_TIER_LINE_RE = re.compile(
    r"^[ \t]*(?:[#>]+[ \t]*)?(?:[-*+][ \t]*)?(?:\d+[.、)）][ \t]*)?"
    r"(?:\*\*)?"
    r"(稳妥|张力|坦诚(?:直接)?|撩人(?:幽默)?|简短)"
    r"(?:型|版|档|风格)?"
    r"(?:\*\*)?"
    r"[ \t]*(?:[（(][^）)]*[）)])?[ \t]*(?:[：:—-][ \t]*)?",
    re.M,
)

_TIER_FAMILY = {
    "稳妥": "稳妥型",
    "张力": "张力型",
    "坦诚": "张力型",
    "坦诚直接": "张力型",
    "撩人": "张力型",
    "撩人幽默": "张力型",
    "简短": "简短型",
}

_TIER_ORDER = ["稳妥型", "张力型", "简短型"]


def _find_tier_positions(text):
    """返回 [(档位族, 起始位置, 匹配长度)]，行级识别。"""
    out = []
    for m in _TIER_LINE_RE.finditer(text):
        # 取标签里的词根（正则第 1 组）
        word = m.group(1)
        fam = _TIER_FAMILY.get(word)
        if not fam:
            continue
        out.append((fam, m.start(), m.end() - m.start()))
    return out


def _split_tiers(text):
    """按行级档位标签切分三档。

    返回 {档位族: 块文本}；缺档则该族不在字典里。
    同一族多次出现时取第一次（导语里枚举档名不会污染分块）。
    """
    pos = _find_tier_positions(text)
    blocks = {}
    for i, (fam, start, length) in enumerate(pos):
        if fam in blocks:
            continue
        end = pos[i + 1][1] if i + 1 < len(pos) else len(text)
        blocks[fam] = text[start:end]
    return blocks


def _body(blk):
    """去掉标题行与结尾固定话术（以 > 开头的引用），只留话术主体，用于长度/相似度比较。"""
    lines = []
    for ln in blk.splitlines():
        if ln.lstrip().startswith((">", "#")):
            continue
        lines.append(_strip_annotation_tail(ln))
    return "\n".join(lines)


def _spoken(blk):
    """只取引号内的话术本体（「…」/“…”），排除注解文字对相似度的稀释。"""
    quotes = re.findall(r"「([^」]{2,})」|“([^”]{2,})”", blk)
    return "".join(a or b for a, b in quotes)


def _has_annotation(blk):
    """该档是否带注解。

    注解必须是「注解/风险/为什么这么写/适用/写法/备注/说明 + 冒号」的显式结构，
    而不是块内任意位置出现关键词 —— 否则话术正文里的「为什么」会被误判成注解。
    """
    pat = re.compile(
        r"(?:^|[\s（(])(?:注解|风险|为什么这么写|适用|写法|备注|说明)\s*[:：]"
    )
    return bool(pat.search(blk))


def cmd_check_draft(path, inline=None):
    """三档质量门：黑名单 + 三档齐全 + 每条带注解 + 简短档真短 + 档间非同句。
    这是把「三档齐全、每条附注解、三档有差异」从口头声称变成可机器验证。"""
    text = _get_text(path, inline)
    if text is None:
        return 2
    if not text.strip():
        print("[ERROR] 待检稿为空。", file=sys.stderr)
        return 2

    hard = []   # 命中即禁交付
    soft = []   # 提示项，不阻断

    for w, ln in _scan_blocklist(text):
        hard.append(f"行{ln} 命中黑名单词「{w}」")

    blocks = _split_tiers(text)
    for fam in _TIER_ORDER:
        if fam not in blocks:
            hard.append(f"缺{fam}（三档必须齐全，缺一档=没给选项）")

    if len(blocks) == len(_TIER_ORDER):
        ordered = [(fam, blocks[fam]) for fam in _TIER_ORDER]

        # 每条必须带注解（结构化判定）
        for fam, blk in ordered:
            if not _has_annotation(blk):
                hard.append(f"{fam} 没有任何注解（需要「注解：/风险：/写法：…」这样的显式标注）")

        # 简短型必须显著短于稳妥型
        lens = {fam: len(_body(blk)) for fam, blk in ordered}
        if lens.get("简短型") and lens.get("稳妥型"):
            ratio = lens["简短型"] / lens["稳妥型"]
            if ratio > 0.6:
                soft.append(f"简短型偏长（是稳妥型的 {ratio:.0%}，建议 ≤60%）——简短档的意义在「话少」")

        # 两档不能是同一句的改写：≥95% 且长度接近才硬拦，≥85% 提示
        # 稳妥型 vs 简短型 本来就是压缩关系，最多提示不硬拦
        for i in range(len(ordered)):
            for j in range(i + 1, len(ordered)):
                a, b = ordered[i], ordered[j]
                sa = _spoken(a[1]) or _body(a[1])
                sb = _spoken(b[1]) or _body(b[1])
                r = difflib.SequenceMatcher(None, sa, sb).ratio()
                pair = f"{a[0]} 与 {b[0]} 相似度 {r:.0%}"
                if r >= 0.95 and min(len(sa), len(sb)) / max(len(sa), len(sb), 1) >= 0.85:
                    if {a[0], b[0]} == {"稳妥型", "简短型"}:
                        soft.append(pair + "，稳妥与简短本是压缩关系，确认是否只是删字")
                    else:
                        hard.append(pair + "，几乎同句（三档必须换思路不是换词）")
                elif r >= 0.85:
                    soft.append(pair + "，疑似同义改写，建议换思路")

    if hard:
        print("[BLOCKED] 三档质量门未过，禁止交付：", file=sys.stderr)
        for h in hard:
            print(f"  - {h}", file=sys.stderr)
        for s in soft:
            print(f"  ~ {s}", file=sys.stderr)
        return 1

    print("OK：三档齐全、每条有注解、档间不重复、未命中黑名单。")
    for s in soft:
        print(f"  提示：{s}")
    return 0


# ---------------------------------------------------------------------------
# 场景查询
# ---------------------------------------------------------------------------
# 结构化兜底正则（别名表覆盖不了的口语变体）：(正则, 场景)
_STRUCTURAL_PATTERNS = [
    (r"借.{0,4}(?:块|万|千|百|元|块钱)", "gen_refuse_money"),   # 借五百/借两万块/借3千
    (r"(?:借|贷)款", "gen_refuse_money"),
    (r"周转", "gen_refuse_money"),
    (r"(?:催|逼)(?:我)?(?:婚|生|相亲)", "rel_marriage_pressure"),
    (r"(?:不回|没回|不接).{0,6}(?:消息|电话|微信)", "rel_coldwar"),
    (r"(?:冷暴力|忽冷忽热)", "rel_coldwar"),
    (r"(?:表白|告白)", None),  # 方向不定（主动/被动），不给兜底，交给别名与 AI 判断
    (r"(?:加|值)(?:个)?(?:班|夜班)", "work_refuse_overtime"),
    (r"(?:涨|升)(?:租|房租)", "gen_complaint"),
    (r"(?:退|退款|退货)", "gen_complaint"),
]


def _resolve_scene(key):
    """精确 key 优先；别名按**长度降序**匹配（「催婚」不会被更短的「催」抢走）；
    再退到结构化正则兜底（借+金额 / 不回消息 这类别名表枚举不尽的变体）。"""
    if key in SCENES:
        return key
    for alias in sorted(_ALIASES, key=len, reverse=True):
        if alias in key:
            return _ALIASES[alias]
    for pat, scene in _STRUCTURAL_PATTERNS:
        if scene and re.search(pat, key):
            return scene
    return None


def _nearest_scenes(key, top=3):
    """匹配不上时给最接近的候选（按场景名 + 识别信号的字面重合度排序）。"""
    def score(k):
        s = SCENES[k]
        hay = s["name"] + s["signals"] + s["关系"]
        return sum(1 for ch in set(key) if ch in hay)
    ranked = sorted(SCENES, key=lambda k: (-score(k), len(SCENES[k]["name"])))
    return ranked[:top]


def cmd_scene(key):
    k = _resolve_scene(key)
    if not k:
        print(f"[ERROR] 未找到场景「{key}」。用 --list 看全部场景，或试口语词（如：冷战/借钱/甩锅）。", file=sys.stderr)
        near = _nearest_scenes(key)
        if near:
            print("最接近的场景：", file=sys.stderr)
            for nk in near:
                print(f"  - {nk}（{SCENES[nk]['name']}）", file=sys.stderr)
        return 2
    s = SCENES[k]
    lines = [
        f"【场景卡】{s['name']}（{k}）",
        "",
        f"- 关系：{s['关系']}",
        f"- 识别信号：{s['signals']}",
        f"- 主用框架：{s['framework']}",
        f"- 备选框架：{s['alt']}",
        f"- 句式骨架：{s['skeleton']}",
        f"- 雷区：{s['pitfalls']}",
        "",
        "框架公式与例句见 references/frameworks.md；生成后记得 --check-output 自扫再交付。",
    ]
    print("\n".join(lines))
    return 0


def cmd_list():
    print(f"场景库共 {len(SCENES)} 个场景：")
    print("")
    cur = None
    for k, s in SCENES.items():
        group = k.split("_")[0]
        if group != cur:
            cur = group
            print({"work": "【职场】", "rel": "【情感】", "gen": "【通用】"}[group])
        print(f"  {k:26s} {s['name']}")
    print("")
    print("用法：python reply_check.py --scene <key 或口语词，如：冷战>")
    return 0


def cmd_demo():
    """演示完整链路：输入快筛 → 场景卡 → 骨架（生成由 AI 按骨架完成）。"""
    print("=== Demo：「对象冷战三天，怎么破冰」===")
    print("")
    print("[1] 输入快筛")
    print("    CLEAN：无危机信号、无操控请求。")
    print("")
    print("[2] 场景匹配 --scene rel_coldwar")
    cmd_scene("rel_coldwar")
    print("")
    print("[3] 三档生成（AI 按骨架落笔，此处仅示例稳妥型一条）")
    print("    稳妥型：「这几天我们都没说话（观察），我心里挺不好受的（感受），")
    print("    我不想我们这样僵着（需要），今晚我给你打个电话，咱好好说说好吗？（请求）」")
    print("    —— 注解：NVC 四步全落，没翻旧账没问「你什么意思」；风险：语气偏软，")
    print("    若对方习惯直来直去可换坦诚型。")
    print("")
    print("[4] 交付前 --check-draft 质量门 → 出具三档完整稿后执行。")
    return 0


def main():
    ap = argparse.ArgumentParser(
        description="高情商回复教练确定性核心：输入快筛/场景速查/输出自扫/三档质量门（只给路径与选项，不替用户定性）")
    ap.add_argument("--check-input", metavar="TXT", nargs="?", const="", default=None,
                    help="扫描用户输入/聊天文本：危机→转介卡(rc=3)；操控请求→拒绝(rc=4)；否则 CLEAN(rc=0)。可配 --text 免文件")
    ap.add_argument("--check-output", metavar="MD", nargs="?", const="", default=None,
                    help="扫描生成稿黑名单：命中定性词/操控词/承诺词即 rc=1，禁止交付")
    ap.add_argument("--check-draft", metavar="MD", nargs="?", const="", default=None,
                    help="三档质量门：黑名单+三档齐全+每条带注解+档间不重复，未过 rc=1")
    ap.add_argument("--text", metavar="STR", default=None,
                    help="直接传入待检文本（免落临时文件）。单独使用＝输入快筛；可与三个 --check-* 组合覆盖其文件")
    ap.add_argument("--scene", metavar="KEY", default=None,
                    help="查场景卡（支持 key 或口语词，如 rel_coldwar / 冷战 / 借钱）")
    ap.add_argument("--list", action="store_true", help="列出全部场景")
    ap.add_argument("--demo", action="store_true", help="跑一条完整链路示例")
    args = ap.parse_args()

    if args.check_input is not None:
        sys.exit(cmd_check_input(args.check_input, args.text))
    if args.check_output is not None:
        sys.exit(cmd_check_output(args.check_output, args.text))
    if args.check_draft is not None:
        sys.exit(cmd_check_draft(args.check_draft, args.text))
    if args.text:
        sys.exit(cmd_check_input(None, args.text))
    if args.scene:
        sys.exit(cmd_scene(args.scene))
    if args.list:
        sys.exit(cmd_list())
    if args.demo:
        sys.exit(cmd_demo())
    ap.print_help()
    sys.exit(2)


if __name__ == "__main__":
    main()
