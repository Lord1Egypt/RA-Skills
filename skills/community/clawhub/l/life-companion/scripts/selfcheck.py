#!/usr/bin/env python3
"""
selfcheck.py — a deterministic gate over a DRAFTED reply, before it is sent.

Why this exists: every honesty rule in this skill (no fabricated precision, no
fatalism, no invented helpline, disclaimer present, jargon glossed, no un-sourced
high-stakes number) lived only in prose checklists spread across five files. Prose
guardrails degrade with model strength — which is exactly the problem when this skill
runs on a weaker or non-Claude agent. A script does not degrade.

  python3 selfcheck.py --module destiny --file draft.md
  python3 selfcheck.py --module daily --text "..."            # or pipe on stdin
  python3 selfcheck.py --module career --file draft.md --json

Exit 0 = no blockers (warnings may still be listed and are worth reading).
Exit 1 = at least one BLOCKER — do not send the draft as-is.

WHAT THIS IS NOT: proof the reply is honest. It matches surface patterns. It cannot
see a fabricated *claim* phrased calmly, a chart read against the wrong pillars, or a
callback to something the person never said. Passing this gate is necessary, not
sufficient — the module checklists still apply.

Run it on a DRAFT REPLY, never on this skill's own reference files: those quote the
forbidden shapes in order to forbid them ("no invented 综合运 ⭐⭐⭐⭐", 'never "水逆导致
你…"'), and nothing here can tell a counter-example from an example.
"""
import argparse
import json
import re
import sys

# ---------------------------------------------------------------------------
# The canonical crisis resources. Any other phone-number-shaped string in a reply is
# assumed invented until proven otherwise — a hallucinated helpline is the single
# worst failure this skill can produce, and it is invisible to every other check.
# The SKILL.md crisis table and references/safety.md §2 carry the same list, and
# TestCrisisLinesForMoreRegions fails when a doc names a number that is not here.
# ---------------------------------------------------------------------------
KNOWN_HELPLINES = {
    "0800-0113", "08000113", "113",          # NL 113 Zelfmoordpreventie
    "988",                                    # US/Canada
    "12356",                                  # China national psych-support line
    "010-82951332", "01082951332",            # Beijing crisis centre
    "400-161-9995", "4001619995",             # 希望24
    "116123", "116 123",                      # UK/ROI Samaritans
    "0800-2000", "08002000",                  # NL Veilig Thuis
    "1-800-799-7233", "18007997233",          # US DV hotline
    "112", "911", "999", "120", "110",        # emergency services
    # Each read on its operator's or government's own page, 2026-09-13 (safety.md §2)
    "18111", "2389 2222", "2382 0000", "2896 0000",          # Hong Kong
    "18281", "18288", "2522 0434",                          # Hong Kong, abuse
    "2852 5222", "2852 5777", "28261126", "28233030",       # Macau (28233030: abuse)
    "1925", "1995",                                         # Taiwan (113 保護專線 above)
    "1771", "+65-6669-1771", "1767", "9151 1767",           # Singapore
    "1800 777 0000", "995",                                 # Singapore, abuse / ambulance
    "+603-7627 2929", "15555", "15999", "019 26 15999",     # Malaysia
    "13 11 14", "0477 13 11 14", "1300 659 467",            # Australia
    "1800 737 732", "0458 737 732", "000",                  # Australia, abuse / emergency
    "1737", "0508 828 865", "0800 456 450", "0800 733 843", "111",   # New Zealand
    "0120-061-338", "0120-279-338", "0120-279-226",         # Japan
    "0120-279-889", "8008", "119",                          # Japan, abuse (#8008) / emergency
    "109", "1577-0199", "1366",                             # South Korea
    "0800 1110111", "0800 1110222", "116 016",              # Germany (116 123 above)
    "3114", "3919", "114",                                  # France (15, 17, 18 are too short to flag)
}
# A trailing '.' used to kill the match ("call 555-0142." escaped entirely), so only
# digits and hyphens may follow.
PHONE_RE = re.compile(r"(?<![\d.\-])(?:\+?\d[\d\-. ]{2,16}\d)(?![\d\-])")
# Crisis lines are frequently SHORT codes (988, 112, 12356, 116 123). A minimum digit
# count therefore cannot be the test — "61120" is five digits and sailed through with
# zero findings. Any number near helpline language is a candidate no matter how short.
# Words that make a number a claim about where to call. Matched as words: 「打」 alone
# fired on 打卡 and 打折, and "call" and "text" inside "recall" and "context", so a
# price or a step count was blocked as an invented hotline.
HELPLINE_CONTEXT = re.compile(
    r"热线|专线|求助|拨打|打给|打电话|致电|援助|干预中心|危机|自杀|"
    r"\b(?:helpline|hotline|crisis line|lifeline|call(?:s|ed|ing)?|text(?:s|ed|ing)?|"
    r"dial(?:s|led|ing)?|phone|reach)\b", re.I)
# A short code (four digits or fewer) names a resource only beside words that say it is
# one. Otherwise "你已经坚持了 111 天" named New Zealand's 111, "114 Nachrichten" France's
# 114, and a crisis reply with no real line passed as having one.
RESOURCE_CONTEXT = re.compile(
    r"热线|专线|电话|拨打|打给|打电话|致电|报警|急救|救护|消防|求助|紧急|生命线|情绪通|"
    r"相谈|自杀|预防|자살예방|상담|전화|긴급|いのち|よりそい|ダイヤル|救急|警察|"
    r"\b(?:helpline|hotline|lifeline|mindline|samaritans|befrienders|telefonseelsorge|"
    r"hilfetelefon|call(?:s|ed|ing)?|text(?:s|ed|ing)?|dial(?:s|led|ing)?|phone|sms|"
    r"emergency|ambulance|police|appel(?:ez|er)?|numéro|urgence|notruf|polizei|talian|"
    r"hubungi|suicide)\b", re.I)
NUM_TOKEN_RE = re.compile(r"\+?\d[\d\-. ]*\d|\d")
# A few services carry digits in their name. "Call 1800RESPECT on 1800 737 732" is one
# real line, but its 1800 read as a four-digit number of its own, and 「希望24 400-161-9995」
# read as 24 400-161-9995. The names are blanked out first; the number beside them still
# has to be a known line.
SERVICE_NAMES_WITH_DIGITS = re.compile(r"1800 ?RESPECT|0508 ?TAUTOKO|0800 ?REFUGE|希望 ?24", re.I)
# Dates look exactly like phone numbers to that regex — and a fact-check block is FULL
# of them ("时效: as of 2026-08"). Excluding them matters more than it sounds: a gate
# that cries wolf on its own required artifact is a gate nobody runs twice.
DATEY_RE = re.compile(r"^\d{4}[-/]\d{1,2}(?:[-/]\d{1,2})?$|^\d{1,2}[-/]\d{1,2}(?:[-/]\d{2,4})?$")
# Only a real calendar date is stripped: the old pattern also ate 「0120-27-93」 out of an
# invented Japanese number and let the rest through.
DATE_TIME_RE = re.compile(r"(?<!\d)(?:19|20)\d{2}-(?:0?[1-9]|1[0-2])-(?:0?[1-9]|[12]\d|3[01])"
                          r"(?:[ T]\d{1,2}(?::\d{2}){0,2})?(?!\d)")
# Country codes of the places in the crisis table, and the ones dialled at home with a 0,
# so "+852 2389 2222" and the domestic 「03-7627 2929」 (+603-7627 2929) are the real lines
# they are.
_COUNTRY_CODES = ("1", "31", "33", "44", "49", "60", "61", "64", "65", "81", "82", "86",
                  "353", "852", "853", "886")
_TRUNK_ZERO = ("31", "33", "44", "49", "60", "61", "64", "81", "82", "86", "353", "886")


def _digits(s):
    return re.sub(r"\D", "", s or "")


_KNOWN_DIGITS = {_digits(h) for h in KNOWN_HELPLINES}


def _is_known_digits(d, international=False):
    if d in _KNOWN_DIGITS:
        return True
    if international:
        d = d[2:] if d.startswith("00") else d
        for cc in _COUNTRY_CODES:
            rest = d[len(cc):]
            if d.startswith(cc) and len(rest) >= 3 and (
                    rest in _KNOWN_DIGITS or (cc in _TRUNK_ZERO and "0" + rest in _KNOWN_DIGITS)):
                return True
    elif d.startswith("0") and len(d) >= 8:
        return any(cc + d[1:] in _KNOWN_DIGITS for cc in _TRUNK_ZERO)
    return False


_DASHES = dict.fromkeys(map(ord, "‐‑‒–—−﹣－"), "-")


def _number_view(text):
    """The text as a phone number reads: full-width digits and punctuation made ASCII (NFKC),
    every Unicode dash a '-', every non-breaking or thin space a ' ', and "(852) " as
    "+852 ". Written with U+2010 hyphens, an invented number fell apart into short groups
    and passed; a real one in full-width digits wasn't recognised."""
    import unicodedata
    view = unicodedata.normalize("NFKC", text).translate(_DASHES)
    return re.sub(r"\((\d{1,3})\)\s*(?=\d)",
                  lambda m: f"+{m.group(1)} " if m.group(1) in _COUNTRY_CODES else m.group(0), view)


def _looks_like_a_phone(raw, near_helpline=False, crisis=False):
    norm = raw.replace(" ", "")
    # In a crisis reply only a date with a four-digit year is let off: 「13-11-15」 is a
    # made-up Lifeline number there far more often than it is a date.
    if DATEY_RE.match(norm) and not (crisis and not re.match(r"\d{4}", norm)):
        return False
    d = _digits(norm)
    if not d:
        return False
    # In helpline language, even a 3-digit shortcode is a claim about where to call.
    return len(d) >= (3 if near_helpline else 6) or norm in KNOWN_HELPLINES


# NUM_TOKEN_RE can't see where a number stops. People write a line the way it is said,
# "12356 24 小时" or "1. 12356", and the token came out as 1235624 or 112356: the real
# national line was reported as invented, a gate teaching the reply to drop the right
# number. A token is a known line when a run of its space-separated groups is one, and
# what is left over is a list marker before it ("1.") or an hour count after it ("24").
_LIST_MARKER = re.compile(r"^\d{1,2}[.)]$")
_SMALL_COUNT = re.compile(r"^\d{1,2}$")


def _known_part(raw):
    """The digits of the known line inside a token, or None. Linear in the token: a phone
    number is at most six groups, and a long run of list markers used to take seconds."""
    groups = raw.split()
    n = len(groups)
    small_from = [True] * (n + 1)
    for k in range(n - 1, -1, -1):
        small_from[k] = small_from[k + 1] and bool(_SMALL_COUNT.match(groups[k]))
    international = raw.lstrip().startswith(("+", "00"))
    for i in range(n):
        if i and not _LIST_MARKER.match(groups[i - 1]):
            break
        for j in range(min(n, i + 6), i, -1):
            d = _digits("".join(groups[i:j]))
            if small_from[j] and _is_known_digits(d, international and i == 0):
                return d
    return None


def _is_known_line(raw):
    return _known_part(raw) is not None


def _in_a_grouped_figure(s, m):
    """`12,345` splits at the comma into 12 and 345; neither half is a phone number, and the
    000 of `1,000` isn't Australia's 000. Only a real grouped figure counts, though:
    「12356,4001619996」 is two numbers, and the second still has to be checked."""
    a, b = m.start(), m.end()
    while a > 0 and (s[a - 1].isdigit() or s[a - 1] == ","):
        a -= 1
    while b < len(s) and (s[b].isdigit() or s[b] == ","):
        b += 1
    run = s[a:b].strip(",")
    return "," in run and re.fullmatch(r"\d{1,3}(?:,\d{3})+", run) is not None


_YEAR_BEFORE = re.compile(r"(?:\b(?:since|in|from|as of|until|by)|于|从|自)\s*$", re.I)


def _is_a_year(s, m):
    """`2025 起全国统一` is a year, not a four-digit shortcode. So is the 1995 of `1995 年`,
    even though 1995 is also Taiwan's 生命線; but not the 1995 of 「1995，起码有人接」."""
    if not re.fullmatch(r"(?:19|20)\d{2}", m.group(0)):
        return False
    after = s[m.end():m.end() + 4].lstrip()
    return (after[:1] == "年" or (after[:1] == "起" and after[1:2] not in ("码", "碼"))
            or bool(_YEAR_BEFORE.search(s[max(0, m.start() - 10):m.start()])))


_SOC_CODE = re.compile(r"\d{2}-\d{4}\.\d{2}")
_DOTTED_DATE = re.compile(r"(?:19|20)\d{2}\.\d{1,2}\.\d{1,2}|\d{1,2}\.\d{1,2}\.(?:19|20)\d{2}")
_CLOCK = re.compile(r"(?:[01]?\d|2[0-4])[.:][0-5]\d")
_DECIMAL = re.compile(r"\d{1,3}\.\d+")
_RANGE = re.compile(r"([1-9]\d{2,4})-([1-9]\d{2,4})")
_MONEY_AFTER = re.compile(r"\s*(?:元|块|円|원|美元|港币|港元|日元|欧元|RMB|CNY|HKD|USD|EUR|€|\$)")
_MONEY_BEFORE = re.compile(r"(?:\$|€|¥|￥|HK\$|RM)\s*$")


def _ordinary_figure(raw, s, m, crisis, near_helpline):
    """Shapes that are not phone numbers: an O*NET code (15-2051.00), a dotted date, a clock
    time (10.30), a decimal (116.4074), an amount of money, and, outside a crisis reply and
    away from helpline words, a range (6000-8000 步)."""
    # read the token as written: with its spaces taken out, 「1. 12357」 became the decimal
    # 1.12357 and an invented number walked through; a decimal is also no excuse in a crisis
    tok = raw.strip()
    if (_SOC_CODE.fullmatch(tok) or _DOTTED_DATE.fullmatch(tok) or _CLOCK.fullmatch(tok)
            or (not crisis and _DECIMAL.fullmatch(tok))):
        return True
    if _MONEY_AFTER.match(s, m.end()) or _MONEY_BEFORE.search(s[max(0, m.start() - 4):m.start()]):
        return True
    r = _RANGE.fullmatch(tok)
    return bool(r and not crisis and not near_helpline and int(r.group(1)) < int(r.group(2)))


_FRENCH_SHORT = re.compile(r"\b(?:SAMU|Police Secours|police|pompiers|sapeurs-pompiers)"
                           r"\s*\**\s*(?:15|17|18)\b", re.I)


def _names_a_real_resource(text):
    """Does this reply actually point at a REAL crisis resource?

    Substring matching was the bug: "61120" contains "112", so an invented shortcode
    satisfied this check. Compare whole number tokens instead, and let a short code count
    only beside words that make it a line to call.
    """
    if "findahelpline" in text.lower() or _FRENCH_SHORT.search(text):
        return True
    view = _number_view(text)
    view = SERVICE_NAMES_WITH_DIGITS.sub(lambda m: " " * len(m.group(0)), view)
    for m in NUM_TOKEN_RE.finditer(view):
        part = _known_part(m.group(0))
        if part is None or _in_a_grouped_figure(view, m) or _is_a_year(view, m):
            continue
        if len(part) >= 5 or RESOURCE_CONTEXT.search(view[max(0, m.start() - 24):m.end() + 24]):
            return True
    return False

# ---------------------------------------------------------------------------
# Patterns. Each: (code, regex, severity, why, fix)
#   blocker — an outright violation of safety.md; do not send
#   warn    — legitimate sometimes; look at it before sending
# ---------------------------------------------------------------------------
# The bad outcomes a reading must never forecast. Kept as one alternation and reused,
# because the failure mode isn't a fixed phrase — it's ANY hedge attached to one of
# these. A competent model almost never writes 命中注定; it writes 「大概率保不住」.
_BAD_EVENT = (r"离婚|分手|离|破产|破财|失业|被裁|失败|没戏|生病|得病|病|出事|受伤|"
              r"车祸|意外|坐牢|去世|死|绝症|癌|流产|保不住|散伙|翻车|栽")

FATALISM = [
    (r"命中注定|注定[要会]|在劫难逃|逃不掉的?命|命该如此", "命定/宿命句式"),
    (r"血光之灾|大凶之(年|运|兆)|必有(灾|祸|难)|克(夫|妻|父|母|子)", "灾祸/克亲断语"),
    (r"(一定|必定|肯定|绝对)(会|要)[^。！\n]{0,12}(" + _BAD_EVENT + ")", "确定性坏结局"),
    (r"你(会|将)(在|于)?\s*\d{4}\s*年[^。\n]{0,12}(结婚|离婚|发财|破产|生病|升职)", "指定年份的事件预言"),
    # --- hedged prediction: the REAL failure shape. A probability attached to a life
    # event is still a prophecy; hedging it doesn't make it a reflection. ---
    # Taiwan writes 機率, which folds to 机率 rather than 概率; Cantonese says 好大機會, 實會 and
    # 梗會. The lookbehinds keep 事实会, 其实会 and 这个梗会 out.
    (r"(大概率|大机率|机率很大|好大机会|(?<![事真确落诚现老结充扎厚其])实会|(?<![这那个的])梗会|"
     r"很可能|极可能|十有八九|八九不离十|多半(会|要|是)|难免(会|要)|免不了|"
     r"恐怕(会|要)|怕是(要|会)|保不齐|说不好会|基本(上)?(会|要|没)|铁定|跑不了|"
     r"逃不过|躲不掉)[^。！？\n]{0,16}(" + _BAD_EVENT + ")",
     "带概率的坏事预言（对冲过的宿命，仍是预言）"),
    (r"(" + _BAD_EVENT + r")[^。！？\n]{0,8}(是大概率|是大机率|概率很大|机率很大|几乎是必然|在所难免)",
     "带概率的坏事预言"),
    # metaphors for the same forecast, which dodge the literal-event list
    (r"(走到(尽头|头了)|到头了|守不住|保不住|撑不到|熬不过|没(有)?好结果|"
     r"凶多吉少|难善终|收不了场)", "换成比喻的坏结局预言"),
    (r"\b(a|the)\s+(strong|good|high|real)\s+chance\s+(that\s+)?(you|he|she|they|it)\b",
     "English hedged prediction"),
    (r"\b(won'?t|will not)\s+(last|work out|survive|make it)\b", "English hedged prediction"),
    # --- veiled prediction: "容易X" is fine for a TENDENCY, not for an EVENT ---
    (r"(容易|难免|小心|当心|注意)[^。！？\n]{0,8}(出事|生病|得病|破财|破产|失业|被裁|"
     r"离婚|分手|车祸|意外|受伤|坐牢|官司)", "把事件说成「容易发生」——事件预言，不是倾向"),
    (r"(本命年|犯太岁|冲太岁|流年不利|大运不好)[^。！？\n]{0,16}(" + _BAD_EVENT + ")",
     "把年份/运势当成坏事的原因"),
    # --- astrology stated as a CAUSE rather than a traditional framing ---
    (r"(水逆|逆行|冲|刑|太岁|凶星|煞)[^。！？\n]{0,10}(导致|造成|使你|害得|让你[^。\n]{0,6}"
     r"(出事|失败|吵|分手))", "把星象说成因果，而不是传统上的提醒"),
    (r"\b(you|you'?ll)\s+(will\s+)?(definitely|certainly|surely)\s+\w+", "English certainty claim"),
    (r"\b(destined|fated)\s+to\b", "English fatalism"),
    (r"\b(you'?re )?(very )?likely to (get (sick|divorced|fired)|lose|fail)\b",
     "English hedged prediction"),
]

# A chart says nothing checkable about a THIRD party's body or fate. 宫位/六亲 describe
# how the person relates to those roles — not the relatives' actual health. Word order
# varies too much for one regex ("你母亲身体会偏弱" / "你母亲会容易生病"), so scan per
# sentence for the combination: a relative + a forecast word + a health/fate noun.
KIN = r"(父亲|母亲|爸爸|妈妈|爱人|配偶|老公|老婆|伴侣|对象|孩子|子女|儿子|女儿|兄弟|姐妹|父母)"
KIN_FORECAST = r"(会|将|容易|大概率|多半|难免|恐怕|偏|比较|不太|注定)"
KIN_SUBJECT = r"(身体|健康|寿|命|婚姻|事业|财|运|" + _BAD_EVENT + r")"
SENT_SPLIT = re.compile(r"[。！？!?\n；;]|(?<=[a-z0-9\)])\.\s")


KIN_EN = (r"\b(father|mother|mom|dad|parents?|spouse|husband|wife|partner|"
          r"child(ren)?|son|daughter|brother|sister|sibling)\b")
KIN_FORECAST_EN = (r"\b(will|going to|likely to|tends? to|may|might|is set to|"
                   r"could end up)\b")
KIN_SUBJECT_EN = (r"\b(health|illness|sick|ill|die|death|pass away|lifespan|marriage|"
                  r"divorce|money|fortune|career|accident|weak(er)?|worse)\b")


def _kin_claims(text):
    """A chart says nothing checkable about a THIRD party's body or fate — in either
    language. This used to be Chinese-only, so 'Your mother's health is likely to get
    worse' passed clean."""
    out = []
    for sent in SENT_SPLIT.split(text):
        zh = (re.search(KIN, sent) and re.search(KIN_FORECAST, sent)
              and re.search(KIN_SUBJECT, sent))
        en = (re.search(KIN_EN, sent, re.I) and re.search(KIN_FORECAST_EN, sent, re.I)
              and re.search(KIN_SUBJECT_EN, sent, re.I))
        if zh or en:
            out.append(sent.strip()[:120])
    return out


# Fatalistic 宜忌: a daily reading gives agency-framed nudges, never a prohibition.
TABOO = [
    (r"诸事不宜|百无禁忌|忌(出门|出行|远行)|不宜(出门|远行)|闭门不出|忌(动土|嫁娶|安葬|开市)",
     "黄历式禁令（本 skill 的宜忌是有能动性的建议，不是禁令）"),
    (r"(千万|绝对|务必)(别|不要|不能)[^。！？\n]{0,12}(换工作|辞职|结婚|投资|签|买房|出门)",
     "替对方下禁令"),
]

# A reading must never forecast a hiring outcome (career.md: "not a hiring predictor").
HIRING = [
    (r"(基本|多半|大概率|肯定|铁定)?(没戏|没希望|进不去|拿不到|录不上|够不着|白搭)",
     "预测录用结果"),
    (r"(肯定|一定|必然|铁定)[^。！？\n]{0,8}(能进|录取|拿到\s*offer|被录用)", "预测录用结果"),
    (r"\b(you )?(won'?t|will never|definitely won'?t) (get|land) (the )?(job|offer|role)\b",
     "predicting a hiring outcome"),
]

# Precision faked in WORDS rather than digits — dodges every \d+% pattern.
WORD_PRECISION = [
    (r"(契合度|匹配度|吻合度|准确度|把握)[^。！？\n]{0,6}"
     r"(一成|两成|三成|四成|五成|六成|七成|八成|九成|十成|大半|八九成)",
     "用汉字说的假精度"),
    (r"(八成|九成|七成|一半)[^。！？\n]{0,4}(契合|匹配|吻合|准|靠谱)", "用汉字说的假精度"),
]

# The relationship module holds ≥2 perspectives and never labels the absent partner.
# Cantonese says the same verdicts with 佢 for 他/她, 係 (folded to 系) for 是 and 嘅 for 的.
RELATIONSHIP_VERDICT = [
    (r"(他|她|佢|对方|你男朋友|你女朋友|你老公|你老婆)(就)?(是|系)(个|一个)?(典型(的|嘅)?)?"
     r"(PUA|煤气灯|自恋(型|狂)|反社会|渣男|渣女|控制狂|巨婴|妈宝)",
     "给不在场的一方贴临床/人格标签"),
    (r"(你(就)?(应该|应当|该)(要)?|建议你|趁早|果断)\s*(马上|赶紧|即刻|立刻|立即|尽快)?\s*(离开|分手|离婚|甩)",
     "替对方下决定（且在虐待情境里「直接走」可能升高危险）"),
    (r"\b(he|she|they)('s| is| are) (a )?(narcissist|sociopath|gaslighter|abuser)\b",
     "clinical label on the absent partner"),
]

DIAGNOSIS = [
    (r"你(有|患有|得了|患咗|得咗)[^。\n]{0,6}(抑郁症|忧郁症|焦虑症|双相|躁郁|人格障碍|PTSD|ADHD)", "疾病诊断"),
    (r"\byou\s+(have|are suffering from)\s+(depression|bipolar|anxiety disorder|PTSD|ADHD)\b", "diagnosis"),
    (r"(她|他|佢|对方)(是|系)(焦虑型|回避型|自恋型|边缘型)(人格)?(?!倾向)", "把倾向说成固定人格标签"),
    # dodges the copula: 「典型的回避型人格」「妥妥的自恋」「标准 PUA」
    (r"(典型(的|嘅)?|妥妥的?|标准(的|嘅)?|百分百|活脱脱)\s*(焦虑型|回避型|自恋型?|边缘型|反社会|"
     r"PUA|煤气灯|双相|躁郁|人格障碍)", "绕开系动词的人格/临床标签"),
    (r"(她|他|佢|对方)[^。！？\n]{0,8}(有|存在)[^。！？\n]{0,6}(人格障碍|心理问题|精神问题)",
     "对第三方下临床判断"),
]

FAKE_PRECISION = [
    (r"综合运[^。\n]{0,8}[★☆⭐]", "综合运星级评分"),
    (r"[★☆⭐]{2,}", "星级评分"),
    (r"(运势|今日运|财运|桃花运|事业运)[^。\n]{0,6}\d+\s*(分|/\s*10|%)", "运势打分"),
    (r"幸运数字\s*[:：]?\s*\d", "幸运数字"),
    (r"(匹配度|契合度|吻合度|准确率|成功率|命中率|match)\D{0,6}\d+(\.\d+)?\s*%", "百分比匹配度"),
    (r"(月薪|年薪|salary)\D{0,8}\d[\d,，.]*\s*(万|k|K|元|欧|美元|EUR|USD)", "薪资数字"),
    (r"(前|top)\s*\d+(\.\d+)?\s*%|百分位|percentile", "百分位"),
    (r"研究(表明|显示|证明)|studies show|科学(证明|已证实)", "伪造权威"),
]

# Ten Gods: first use must carry a plain-language gloss in brackets
# (destiny.md jargon-gloss rule — 正官(责任、规矩、把自己嵌进体系做好)).
TEN_GODS = ["比肩", "劫财", "食神", "伤官", "正财", "偏财", "正官", "七杀", "偏官",
            "正印", "偏印", "枭神"]
GLOSS_WINDOW = 25  # a gloss may trail the term by a few characters, not just hug it
GLOSS_CHARS = "（(【[「"
_OPEN, _CLOSE = "（(【[", "）)】]"


def _is_glossed(text, i, term):
    """Is this 十神 explained in plain language at its first use?

    Two legitimate forms, both used by the skill's own examples:
      正官(责任、规矩、把自己嵌进体系做好)   — term OUTSIDE, gloss follows
      乙卯(食神·表达萌芽)                  — term INSIDE the bracket with the gloss
    Only checking the first shape made every L3 timeline row warn, and a warning that
    always fires is one nobody reads.
    """
    end = i + len(term)
    if any(c in text[end:end + GLOSS_WINDOW] for c in GLOSS_CHARS):
        return True
    # look backwards for an enclosing bracket, then forwards for its close
    start = -1
    for k in range(i - 1, max(-1, i - GLOSS_WINDOW), -1):
        if text[k] in _CLOSE:
            break
        if text[k] in _OPEN:
            start = k
            break
    if start < 0:
        return False
    close = -1
    for k in range(end, min(len(text), end + GLOSS_WINDOW)):
        if text[k] in _CLOSE:
            close = k
            break
    if close < 0:
        return False
    inside = text[start + 1:close]
    return len(inside) - len(term) >= 3      # the bracket carries a real explanation

# Strength / 用神 terms are a different rule: they are the most school-dependent,
# openly heuristic part of the whole chart (safety.md §1, bazi.py `heuristic` block).
# They may be used freely — but not bare. Somewhere near them the reply has to say
# this is ONE school's rule of thumb.
STRENGTH_TERMS = ["身强", "身弱", "扶抑", "用神", "喜用神", "忌神", "调候", "偏强", "偏弱"]
HEDGE_RE = re.compile(r"一派|一种|流派|启发|估|大致|不替你(钉|定)|可能不同|别的读法|"
                      r"不同流派|各家|存疑|"
                      r"heuristic|one school|schools?\s|rule of thumb|one reading|"
                      r"one way to read|tradition|may read|read it differently|"
                      r"not settled|isn'?t settled|approximation|"
                      r"不给硬?喜忌|不替你|近中和|接近中和|near.?balanc", re.I)
# Wide enough that the hedge can live in the next sentence — which is where it usually
# is in English ("…sits close to balanced. That's one school's rule of thumb.").
HEDGE_WINDOW = 130

# High-stakes external-fact markers → safety.md §1 rule 6 + the factcheck.md block.
HIGH_STAKES = [
    r"签证|居留|永居|绿卡|入籍|国籍|移民|工签|工作许可|30\s*%\s*ruling|知识移民",
    r"报税|税率|退税|免税|社保|补贴|助学金|奖学金|贷款利率",
    # Narrowed: a bare "licence" also means a software licence, and any draft that
    # mentioned LICENSE or CC BY was being blocked for missing a fact-check block. The
    # rule is about permission to PRACTISE, so require that context.
    r"执业(?:资格|证)|职业资格认证|学历认证|行医执照|"
    r"(?:professional|occupational|medical|nursing|teaching|engineering)\s+licen[cs]"
    r"|licen[cs](?:e|ing)\s+(?:requirement|board|exam|renewal|reciprocity)"
    r"|licen[cs]ed to practi|credential(?:ing|s)?\s+(?:requirement|recognition|evaluation)",
    r"\bvisa\b|\bresidence permit\b|\bwork permit\b|\bpermanent residen",
]
FACTCHECK_MARKERS = [r"事实核查", r"来源\s*[:：]", r"时效\s*[:：]",
                     r"as of\s+\d{4}", r"你需要?自己确认"]

# Disclaimer / honesty-note markers, per module. Any ONE match satisfies it —
# the wording lives in assets/disclaimers.md and varies by locale and tone.
DISCLAIMER_MARKERS = {
    "destiny": [r"不是科学预测", r"不是预测", r"反思(的)?(镜子|视角|工具)", r"一种(读法|解读|视角)",
                r"文化(性的)?(视角|透镜)", r"not a scientific prediction", r"cultural lens",
                r"reflection", r"reflective"],
    "daily": [r"不是科学预测", r"不是预测", r"反思(的)?(镜子|视角)", r"一种(读法|解读)",
              r"图个彩头", r"not a (scientific )?prediction", r"reflective"],
    "career": [r"中等程度", r"不能预测.*(录取|拿到|hire)", r"不是(正式|验证过的)?测(评|试)",
               r"不是给你贴标签", r"起点", r"moderately", r"not a validated", r"not a label",
               r"don'?t predict"],
    "relationships": [r"只听到了?你(这)?一面", r"看不到全部", r"不是替你下判断", r"几种可能的角度",
                      r"only hearing your side", r"not a verdict"],
    "synastry": [r"不是(科学)?预测", r"不是.*依据", r"(一种|文化)(的)?视角", r"怎么相处", r"反思",
                 r"not a (scientific )?prediction", r"cultural lens"],
}
# A career fit is a measurement. In a reply that carries no band from career_match.py, a sentence
# pronouncing someone suited or unsuited is a verdict nothing measured: answering first, a codex run
# opened with 「适合，尤其适合…」 and 「很对口」 before any check had run.
CAREER_FIT_VERDICT = [
    (r"(?:^|[。！？\n])\s*(?:很|挺|比较|非常|特别|完全)?(?:适合|不适合|对口)[，,。！!]", "opens with a fit verdict"),
    (r"(?:很|挺|非常|特别|十分|高度|完全)(?:对口|匹配|契合)", "calls the fit high with nothing measured"),
    (r"(?:你|您)(?:的[^，。！？\n]{0,10})?(?:很|挺|比较|非常|特别|完全)?(?:适合|不适合)(?:做|转|去|当|走|从事|干)?"
     r"[^，。！？\n]{0,12}(?:岗位|工作|职业|行业|方向|这行|经理|工程师|设计师|研究员|分析师)",
     "pronounces them suited or unsuited to a job"),
    (r"\byou(?:'re| are)\s+(?:a\s+)?(?:great|good|strong|perfect|natural|ideal)\s+fit\b"
     r"|\byou(?:'re| are)\s+(?:well[- ])?suited\b", "pronounces them a fit"),
]
CAREER_BAND = re.compile(r"\b(?:Strong|Moderate|Low)\b|[「“\"]?[高中低][」”\"]?\s*档|档位?\s*[：:]?\s*[「“\"]?[高中低]"
                         r"|[强中低高](?:等)?(?:兴趣)?匹配")

# 合婚 has its own blockers because it is the highest-harm output this skill can
# produce: a 属相不合 verdict has ended relationships that were fine. synastry.py
# deliberately emits no verdict — this stops one being synthesized anyway.
SYNASTRY_VERDICT = [
    (r"(你们|两人|这段(感情|关系))?[^。！？\n]{0,6}(不合|合得来|合不来|不般配|不相配|"
     r"天生一对|命定的?一对|绝配|注定在一起|注定分开)", "给出「合/不合」的结论"),
    (r"(属相|生肖|八字)[^。！？\n]{0,6}(不合|相冲|犯冲|不配|克)[^。！？\n]{0,10}"
     r"(别|不要|不能|分|散|离)", "拿属相/八字当劝分或劝阻的理由"),
    (r"(合婚|配对|契合)[^。！？\n]{0,6}(得分|分数|评分|\d+\s*分|\d+\s*%)", "合婚打分"),
    (r"(克夫|克妻|旺夫|旺妻|命硬)", "克/旺 之类的断语"),
    (r"\b(you two|you)\s*(?:are|'re|'?re|aren'?t|are not)\s+(not\s+)?(a\s+)?"
     r"(perfect match|great match|meant to be|incompatible|compatible|right for each other)\b",
     "compatibility verdict"),
    (r"\b(the|your)\s+charts?\s+(say|show|tell)s?\s+[^.\n]{0,20}"
     r"(shouldn'?t|should not|won'?t work|aren'?t)\b", "chart-as-verdict"),
]
# safety.md §1 rule 7, made checkable. The rigour of the computation (real 节气
# boundaries, a real ephemeris) makes a NON-predictive reading feel like grounds for a
# real decision. This fires when a draft lets a chart term settle a high-stakes action —
# the one direction the lenses must never run (SKILL.md, "When two lenses touch the
# same question").
# NOTE the (?:...) on every one of these. A bare alternation does not compose: pasting
# "a|b" into a longer pattern makes the WHOLE pattern an alternation, so the first
# version of this rule quietly degraded into "any chart word anywhere" and appeared to
# work. Keep them grouped.
_CHART_TERM = (r"(?:八字|命盘|命理|大运|流年|流月|流日|十神|日主|星盘|本命盘|紫微|"
               r"斗数|星座|上升|宫位|命宫|盘上|盘里)")
_REAL_DECISION = (r"(?:换工作|辞职|跳槽|接(?:这个)?offer|入职|创业|分手|离婚|结婚|表白|"
                  r"复合|买房|卖房|投资|加仓|借钱|签(?:约|合同)|移民|搬去|出国|退学|休学|"
                  # Chinese splits the verb and object freely — 「把房买了」 is the same
                  # decision as 「买房」 and must not slip past.
                  r"把(?:房|车|合同|婚)(?:子)?(?:买|卖|签|结)|(?:房|车)(?:子)?(?:买|卖)了|"
                  r"把(?:工作|职)辞|婚(?:也)?结了)")
_DECIDING = (r"(?:所以(?:你)?(?:该|应该|就)|建议你|那就(?:去|把)?|可以放心|大胆|"
             r"不妨(?:就)?|说明你该|是该|适合(?:在)?(?:今年|明年|这两年|这一步)|"
             r"时机(?:到了|不对))")
RULE7 = [
    (_CHART_TERM + r"[^。！？\n]{0,24}" + _DECIDING + r"[^。！？\n]{0,12}" + _REAL_DECISION,
     "拿命理读法给现实高风险决定背书"),
    (_REAL_DECISION + r"[^。！？\n]{0,20}(?:看|按|依|据)[^。！？\n]{0,8}" + _CHART_TERM
     + r"[^。！？\n]{0,12}" + _DECIDING,
     "把现实决定挂在命理读法上"),
]

MODULES = ["destiny", "daily", "career", "relationships", "synastry",
           "journal", "crisis", "none"]


# Refusing a verdict necessarily quotes it — 「两个人合不合，是你们怎么相处决定的」 is
# the RIGHT sentence and contains 「不合」. A gate that punishes the correct refusal
# teaches the model to stop refusing, which is the opposite of the point. So for the
# verdict families, a match inside a sentence that is visibly declining or reframing
# the verdict does not count.
REFUSAL_CUE = re.compile(
    r"不是|并非|别拿|不该|不能|不作数|决定的|替你决定|取决于|要看|得看|怎么相处|"
    r"由你们|自己决定|没有?依据|说了不算|不构成|无关|谈不上|不替你|"
    r"(?:不(?:提供|给出|作出|做出|得出|给|下|做|作|打|出)|没有|没法|无法|不会|不愿|不能)[^。！？\n]{0,12}"
    r"(?:判决|结论|定论|断语|判断|评判|评分|打分|分数)|"
    r"(?:不|不会|不能|没法|无法)(?:把|将|拿)[^。！？\n]{0,12}"
    r"(?:归成|归为|归类|算成|算作|当成|当作|定为|判为|判成|说成|看成)|"
    r"(?:不|不会|不能|没法|无法)(?:谈|说|论|讨论|评价|评判|回答|判断)[^。！？\n]{0,8}"
    r"(?:合不合|合或不合|合与不合|合／不合|合/不合|般不般配|配不配)|"
    r"不(评判|打分|下定论)|"
    r"回到.{0,4}模块|走.{0,4}模块|交给|"
    r"isn'?t|is not|doesn'?t|does not|cannot|can'?t|won'?t|will not|never|rather than|not a |no such|"
    r"\b[Ww]hether\b")


# ---------------------------------------------------------------------------
# VOICE — does this read like a person, or like a form a machine filled in?
#
# Kept separate from the honesty findings above and never a blocker: sounding like a
# bot is not a safety failure, and conflating the two would dilute the checks that ARE.
# But it is measurable, and this skill's own output specs used to MANDATE the worst of
# it (emoji-headed sections, a bold label on every paragraph), so prose advice alone
# was never going to fix it.
#
# Everything here is per-1000-characters (zh) or per-300-words (en) so the numbers mean
# the same thing on a one-line check-in and on a full 命盘.
# ---------------------------------------------------------------------------
LABEL_ROW_RE = re.compile(r"^\s*(?:[-*+]\s*)?\*\*[^*\n]{2,14}\*\*\s*[：:]", re.M)

# The corrective "not X, but Y" reflex. One is a rhetorical move; five in a row is a tic.
NOT_X_BUT_Y = re.compile(
    r"不是[^。，！？\n]{1,20}[，,]\s*(?:而)?是|不是[^。\n]{1,16}也不是|"
    r"\b(?:it|this|that)'?s? (?:is )?n[o']t (?:just |only |about )?[^,;.\n]{1,34}[,;]\s*"
    r"(?:it'?s|but|rather)\b|"
    r"\bnot (?:just|only|merely) [^,.\n]{1,34},? but\b|"
    r"\bis not [^,.\n]{1,30}, but\b", re.I)

# Stock phrases that almost never survive a human rewrite.
STOCK_ZH = [r"值得注意的是", r"需要指出的是", r"总而言之", r"综上所述", r"总的来说",
            r"在某种程度上", r"不容忽视", r"至关重要", r"让我们一起", r"深入探讨",
            r"希望(?:这|以上)(?:对你)?有(?:所)?帮助", r"首先.{0,40}其次.{0,40}最后"]
STOCK_EN = [r"\bdelve\b", r"\btapestry\b", r"\ba testament to\b", r"\bnavigat\w+ the complexit",
            r"\bin the realm of\b", r"\bit'?s worth noting\b", r"\bit'?s important to note\b",
            r"\bthat being said\b", r"\bat the end of the day\b", r"\bwhen it comes to\b",
            r"\bplays? a (?:crucial|pivotal|vital) role\b", r"\bunderscores?\b", r"\bshowcases?\b",
            r"\bseamless\b", r"\bholistic\b", r"\bmyriad\b", r"\bplethora\b",
            r"\bfoster(?:ing|s)?\b", r"\bembark\b", r"\bdeep dive\b", r"\bunpack\b",
            r"^\s*(?:Importantly|Notably|Crucially|Ultimately|Moreover|Furthermore),",
            r"\bI hope this helps\b", r"\bIn summary\b", r"\bIn conclusion\b"]

TRIAD_ZH = re.compile(r"[^\s、，。]{2,8}、[^\s、，。]{2,8}、[^\s、，。]{2,8}")

# Explaining-your-own-point moves. One is fine; a habit of them is the "essay voice".
META_ZH = [r"这(?:其实|恰恰|正)是", r"某种(?:意义|程度)上", r"换句话说", r"也就是说",
           r"我们可以看到", r"可以说", r"不难看出", r"这意味着", r"归根结底",
           r"与其说.{0,20}不如说", r"既.{1,12}又.{1,12}", r"一方面.{0,40}另一方面"]
META_EN = [r"\bin other words\b", r"\bwhat this means is\b", r"\bhere'?s the thing\b",
           r"\bthe key (?:here )?is\b", r"\bin a sense\b", r"\bto put it another way\b",
           r"\bwhich is to say\b", r"\bon one hand\b.{0,80}\bon the other\b",
           r"\bthat said\b", r"\bthe point is\b"]

# Padding adverbs and nominalised verbs — the texture of writing that says little slowly.
FILLER_ZH = re.compile(r"其实|确实|的确|真的很|非常|十分|极其|相当地?|某种|一定程度")
NOMINAL_ZH = re.compile(r"(?:进行|做出|给予|加以|予以|得到|实现)(?:了)?[一二三]?[个次]?"
                        r"[\u4e00-\u9fff]{2,4}")
FILLER_EN = re.compile(r"\b(?:very|really|quite|rather|truly|actually|basically|"
                       r"essentially|fundamentally|significantly|incredibly)\b", re.I)

# A person doesn't land every paragraph on a summarising flourish.
UPSHOT_ZH = re.compile(r"^.{0,80}(?:这才是|说到底|归根到底|本质上|最终|终究)"
                       r"[^。\n]{0,40}。\s*$", re.M)
HEDGE_RE_V = re.compile(r"一种(?:读法|解读|视角)|可能|也许|或许|倾向于|传统上|不一定|"
                        r"\bmay\b|\bmight\b|\bperhaps\b|\btends? to\b|\btraditionally\b")


def _is_cjk(text):
    return len(re.findall(r"[\u4e00-\u9fff]", text)) > len(re.findall(r"[A-Za-z]", text)) / 3


def _sentences(text):
    """Split into sentences. The English path MUST split on '.' too — leaving it out
    made every English paragraph count as one sentence, so human writing scored as
    perfectly uniform and got flagged. Decimals and a few abbreviations are protected."""
    body = re.sub(r"^\s*[>|].*$", "", text, flags=re.M)          # drop quoted disclaimers
    body = re.sub(r"`[^`]*`|\*\*|__", "", body)
    body = re.sub(r"(\d)\.(\d)", r"\1<DOT>\2", body)            # 0.3°, 1.5
    body = re.sub(r"\b(Mr|Mrs|Ms|Dr|St|vs|etc|e\.g|i\.e)\.", r"\1<DOT>", body)
    parts = re.split(r"[。！？!?\n]+|(?<=[a-z0-9\)\"'])\.\s+", body)
    # Keep short ones. The >4 filter this used to have discarded exactly the fragments
    # ("就这样。" / "Three.") that the no-short-sentences check exists to find — the
    # check could never have fired for the right reason.
    return [p.replace("<DOT>", ".").strip() for p in parts
            if p and len(p.strip()) > 1]


def check_voice(text, locale=None):
    """Measure the machine-written tells. Returns findings with real numbers, so the
    fix is 'cut three of these', not 'sound more human'."""
    cjk = _is_cjk(text) if locale is None else (locale != "en")
    n_chars = max(len(re.sub(r"\s", "", text)), 1)
    n_words = max(len(re.findall(r"[A-Za-z']+", text)), 1)
    unit = n_chars / 1000 if cjk else n_words / 300
    unit = max(unit, 0.25)
    out = []

    def add(code, count, per_unit, limit, why, fix, min_count=2):
        # These families are all about HABIT, and each one's own advice says a single
        # instance is fine ("A good move once."). Short text is clamped to a quarter
        # unit, so one occurrence in a 300-character paragraph scored 4.0 and tripped a
        # limit of 2 — the check contradicting its own guidance. Never fire on one.
        if count >= min_count and per_unit > limit:
            out.append({"code": code, "severity": "voice", "count": count,
                        "per_unit": round(per_unit, 1), "limit": limit,
                        "why": why, "fix": fix})

    # A RUN of consecutive labelled rows is a list (the 分层面 grid is one by design)
    # and counts once. Labels scattered through prose are the habit worth flagging.
    lines = text.splitlines()
    labels, prev = 0, False
    for ln in lines:
        hit = bool(LABEL_ROW_RE.match(ln))
        if hit and not prev:
            labels += 1
        prev = hit or (not ln.strip() and prev)   # a blank line doesn't break a list
    add("label-template", labels, labels / unit, 3,
        f"{labels} separate places where a paragraph is captioned 「**label**：content」",
        "Captioning your own thoughts reads as a filled-in form. A deliberate grid (the "
        "分层面 block) counts once — this is about labels sprinkled through prose. Let "
        "most paragraphs just be sentences.")

    dashes = text.count("——") + len(re.findall(r"\s—\s", text))
    add("em-dash", dashes, dashes / unit, 4, f"{dashes} em-dashes",
        "The default LLM connective. Some of these are commas, some are full stops, and "
        "a couple are two separate sentences.")

    nx = len(NOT_X_BUT_Y.findall(text))
    add("not-x-but-y", nx, nx / unit, 2, f"{nx} 「不是X，是Y」/「not X, but Y」",
        "A good move once. As a reflex it becomes the tell people name first. Say the "
        "positive half on its own and trust it.")

    stock = [m.group(0) for p in (STOCK_ZH if cjk else STOCK_EN)
             for m in re.finditer(p, text, re.I | re.M)]
    if stock:
        out.append({"code": "stock-phrase", "severity": "voice", "count": len(stock),
                    "per_unit": round(len(stock) / unit, 1), "limit": 0,
                    "why": "stock phrases: " + "、".join(sorted(set(stock))[:6]),
                    "fix": "Say the thing directly instead. None of these survive a "
                           "human rewrite."})

    meta = [m.group(0) for p in (META_ZH if cjk else META_EN)
            for m in re.finditer(p, text, re.I | re.M)]
    add("explaining-yourself", len(meta), len(meta) / unit, 2,
        "narration about your own point: " + "、".join(sorted(set(meta))[:5]),
        "「这其实正是…」「换句话说」「in other words」 restate what you already said. "
        "Say it once, well, and move on. If a sentence needs a translation, rewrite the "
        "sentence.")

    filler = (FILLER_ZH if cjk else FILLER_EN).findall(text)
    add("filler-adverbs", len(filler), len(filler) / unit, 5,
        f"{len(filler)} padding adverbs ({'、'.join(sorted(set(filler))[:6])})",
        "其实/确实/非常/very/actually mostly add length, not meaning. Delete them and "
        "see whether the sentence lost anything.")

    if cjk:
        # A gloss is a definition, not prose rhythm: 正官(规矩、责任、嵌进体系) is the
        # skill's REQUIRED jargon format, and counting it as a rule-of-three punished
        # the thing the honesty rules demand. Strip bracketed spans before the scan.
        prose = re.sub(r"[（(【\[][^）)】\]]{0,80}[）)】\]]", " ", text)
        nom = NOMINAL_ZH.findall(text)
        add("nominalised-verbs", len(nom), len(nom) / unit, 2,
            f"{len(nom)} 个「进行/做出/给予+名词」({'、'.join(sorted(set(nom))[:4])})",
            "「做出决定」就是「决定」，「进行讨论」就是「聊」。动词直接用，句子立刻像人说的。")
        upshots = len(UPSHOT_ZH.findall(text))
        add("summary-flourish", upshots, upshots / unit, 2,
            f"{upshots} paragraphs end on a summarising flourish",
            "Not every paragraph needs a landing. Let some just stop.")

    if cjk:
        triads = len(TRIAD_ZH.findall(prose))
        add("rule-of-three", triads, triads / unit, 3, f"{triads} 个 A、B、C 三连并列",
            "Everything arriving in threes is a rhythm nobody actually speaks in. Make "
            "one of them two items, or one long one.")

    sents = _sentences(text)
    if len(sents) >= 8:
        lens = [len(s) if cjk else len(s.split()) for s in sents]
        mean = sum(lens) / len(lens)
        sd = (sum((x - mean) ** 2 for x in lens) / len(lens)) ** 0.5
        cv = sd / mean if mean else 0
        short = sum(1 for x in lens if x < (mean * 0.45))
        if cv < 0.45:
            out.append({"code": "uniform-rhythm", "severity": "voice",
                        "count": len(sents), "per_unit": round(cv, 2), "limit": 0.45,
                        "why": f"sentence lengths are too even (variation {cv:.2f}, "
                               f"{short} short sentences out of {len(sents)})",
                        "fix": "People vary hard: a long winding one, then four words. "
                               "Break two of the medium sentences into a long one and a "
                               "very short one."})

    if len(sents) >= 8:
        lens2 = [len(x) if cjk else len(x.split()) for x in sents]
        tiny = sum(1 for x in lens2 if x <= (6 if cjk else 4))
        if tiny == 0:
            out.append({"code": "no-short-sentences", "severity": "voice",
                        "count": 0, "per_unit": 0, "limit": 1,
                        "why": f"not one short sentence in {len(sents)}",
                        "fix": "People punctuate with fragments — 「就这样。」「没了。」"
                               "「Finish something.」 Every sentence being a complete, "
                               "well-formed clause is itself the tell."})

    hedges = len(HEDGE_RE_V.findall(text))
    add("hedge-stacking", hedges, hedges / unit, 6, f"{hedges} hedges",
        "This skill REQUIRES the reflective framing — but say it once, plainly, like a "
        "person setting a boundary. Sprinkling 「可能/倾向于/一种读法」 into every "
        "sentence is how honest framing turns into mush.")

    return {"ok_voice": not out, "cjk": bool(cjk), "findings": out,
            "_note": "Taste, measured. Never blocks — but two or three of these together "
                     "is what people mean by AI味."}


def _find(text, patterns, code, severity, fix, respect_refusal=False, skip_questions=False):
    out = []
    for pat, why in patterns:
        for m in re.finditer(pat, text, re.I):
            if skip_questions:
                # a sentence that asks is not a verdict (「你适合做产品经理吗？」)
                ends = [e for e in (text.find(c, m.end()) for c in "。！？!?\n") if e != -1]
                if ends and text[min(ends)] in "？?":
                    continue
            if respect_refusal:
                # the sentence this match sits in
                bounds = "。！？!?\n；;."
                start = max(text.rfind(c, 0, m.start()) for c in bounds) + 1
                end = min([e for e in (text.find(c, m.end()) for c in bounds)
                           if e != -1] or [len(text)])
                if REFUSAL_CUE.search(text[start:end]):
                    continue
            out.append({"code": code, "severity": severity, "why": why,
                        "evidence": m.group(0).strip()[:120], "fix": fix})
    return out


def _fold(text):
    """Traditional → simplified, one character for one character (scripts/_zh.py)."""
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    if here not in sys.path:
        sys.path.insert(0, here)
    import _zh
    return _zh.to_simplified(text)


def check(text, module="none", locale=None):
    """Run the honesty gate over a draft: {ok, module, blockers, warnings, findings}.

    The draft is folded to simplified Chinese first. Every pattern below is written in
    simplified, and a traditional-script draft used to pass the very sentence its
    simplified twin was blocked for. Folding keeps the length, so each finding's
    evidence is cut back out of the ORIGINAL text: the gate quotes the words that were
    actually written."""
    text = text or ""
    folded = _fold(text)
    r = _check(folded, module, locale)
    if folded != text:
        for x in r["findings"]:
            ev = x.get("evidence") or ""
            i = folded.find(ev) if ev else -1
            if i >= 0:
                x["evidence"] = text[i:i + len(ev)]
    return r


def _check(text, module="none", locale=None):
    f = []

    f += _find(text, FATALISM, "fatalism", "blocker",
               "safety.md §1 rule 2/3: rewrite as a tendency + agency "
               "(「传统上倾向于…」「一种读法是…」), never an event or a verdict.")
    f += _find(text, DIAGNOSIS, "diagnosis", "blocker",
               "safety.md §1 rule 5: no medical/clinical labels. Say the tendency, "
               "then point to a professional.")
    f += _find(text, FAKE_PRECISION, "fabrication", "blocker",
               "safety.md §1 rule 4: no invented score, percentage, salary, percentile "
               "or authority. Keep it qualitative, or cite a real source.")
    f += _find(text, WORD_PRECISION, "fabrication", "blocker",
               "safety.md §1 rule 4: 「八成契合」 is a fabricated number wearing a word. "
               "Give the band (低/中/高) and its confidence note, nothing sharper.")
    f += _find(text, TABOO, "fatalism", "blocker",
               "daily-fortune.md: 宜/忌 are 2–3 agency-framed nudges ("
               "「今天适合…」「大事先别拍板」), never a 黄历 prohibition or an order.")
    f += _find(text, HIRING, "hiring-prediction", "blocker",
               "career.md: this is a fit-and-direction lens, explicitly NOT a hiring "
               "predictor. Say what the role feeds and what the gap is; never whether "
               "they'd get it.")
    for sent in _kin_claims(text):
        f.append({
            "code": "kin-prediction", "severity": "blocker",
            "why": "a forecast about a relative's health or fate",
            "evidence": sent,
            "fix": "bazi-life-arc.md §2: 宫位/六亲 describe how THIS person relates to "
                   "those roles (closeness, reliance, friction) — the chart says nothing "
                   "checkable about someone else's body or life. Rewrite as their own "
                   "relational tendency, and never forecast a third party.",
        })
    if module == "career" and not CAREER_BAND.search(text):
        f += _find(text, CAREER_FIT_VERDICT, "fit-verdict-without-a-score", "blocker", respect_refusal=True,
                   skip_questions=True, fix=
                   "career.md Mode B: a fit is what career_match.py measures. With no scored check there is "
                   "no fit to report: say what --find matched, sketch the gap as questions to test, and offer "
                   "the interest check. Once it is scored, report its band (Strong / Moderate / Low) with the "
                   "confidence note.")
    if module == "synastry":
        f += _find(text, SYNASTRY_VERDICT, "synastry-verdict", "blocker", respect_refusal=True, skip_questions=True, fix=
                   "synastry.py emits no 合/不合, no score, and no recommendation, by "
                   "construction. Report the branch relations as textures to notice "
                   "(「亥巳冲，传统上读作张力与推拉」), then say plainly that whether two "
                   "people do well together is made of what they DO — and route a real "
                   "relationship question to references/modules/relationships.md.")
    f += _find(text, RELATIONSHIP_VERDICT, "one-sided-verdict", "blocker",
               "relationships.md §G + safety.md §3: hold ≥2 perspectives, voice the "
               "absent partner fairly, tendencies not labels. If it IS abuse, route to "
               "specialist DV help and respect their timing — never 'just leave', which "
               "can escalate danger.")

    # Any percentage at all is suspect in a reflective reading — the specific shapes
    # above are the common ones, but a number can be invented in a shape nobody listed.
    # Warn (not block): a percentage QUOTED from a dated official source is legitimate,
    # and the 30% ruling is a proper noun.
    for m in re.finditer(r"\d+(?:\.\d+)?\s*%", text):
        ctx = text[max(0, m.start() - 30): m.end() + 30]
        if re.search(r"ruling|来源|as of|时效", ctx, re.I):
            continue
        f.append({"code": "percentage", "severity": "warn",
                  "why": "a percentage — is it quoted from a real, dated source?",
                  "evidence": ctx.replace("\n", " ").strip()[:120],
                  "fix": "safety.md §1 rule 4/6: bands and qualitative language only. "
                         "A real external figure needs 来源 + 时效 (factcheck.md); "
                         "anything else must go."})

    # --- invented helplines -------------------------------------------------
    # Strip ISO datetimes first. A destiny reading states the birth moment
    # ("1993-04-12 07:35") on essentially every run, and to PHONE_RE that is a
    # 12-digit string with hyphens. Left in, this rule would fire on every chart
    # reading the skill produces — the fastest way to make its most important check
    # get ignored.
    # In a crisis reply every number of three digits or more is a claim about where to
    # call, whatever words stand beside it: the table's own service names (Samaritans of
    # Singapore, 情緒通, 자살예방상담전화) weren't helpline wording to this check, so a
    # made-up line one digit off the real one passed.
    crisis = module == "crisis"
    phone_scan = DATE_TIME_RE.sub(" ", _number_view(text))
    phone_scan = SERVICE_NAMES_WITH_DIGITS.sub(lambda m: " " * len(m.group(0)), phone_scan)
    for m in NUM_TOKEN_RE.finditer(phone_scan):
        raw = m.group(0).strip()
        norm = raw.replace(" ", "")
        if (_is_known_line(raw) or _in_a_grouped_figure(phone_scan, m)
                or _is_a_year(phone_scan, m)):
            continue
        window = phone_scan[max(0, m.start() - 40):m.end() + 20]
        near = bool(HELPLINE_CONTEXT.search(window))
        if _ordinary_figure(raw, phone_scan, m, crisis, near):
            continue
        if not _looks_like_a_phone(raw, near_helpline=near or crisis, crisis=crisis):
            continue
        if norm.replace("-", "") in {h.replace("-", "") for h in KNOWN_HELPLINES}:
            continue
        f.append({
            "code": "unknown-helpline", "severity": "blocker",
            "why": "a phone-number-shaped string that is not a known crisis resource",
            "evidence": raw,
            "fix": "safety.md §2: use only the listed numbers, or findahelpline.com. "
                   "NEVER improvise a helpline number — verify it or drop it.",
        })

    # --- un-glossed 十神 -----------------------------------------------------
    for term in TEN_GODS:
        i = text.find(term)
        if i < 0:
            continue
        end = i + len(term)
        if _is_glossed(text, i, term):
            continue
        f.append({
            "code": "unglossed-jargon", "severity": "warn",
            "why": f"「{term}」 appears without a plain-language gloss on first use",
            "evidence": text[max(0, i - 18): end + 18].replace("\n", " "),
            "fix": "destiny.md jargon-gloss rule: first use must be 术语(大白话), "
                   "e.g. 正官(责任、规矩、把自己嵌进体系做好). L0/L1 use zero terms.",
        })

    # --- strength / 用神 stated as fact rather than as one school's heuristic --
    for term in STRENGTH_TERMS:
        i = text.find(term)
        if i < 0:
            continue
        window = text[max(0, i - HEDGE_WINDOW): i + len(term) + HEDGE_WINDOW]
        if HEDGE_RE.search(window):
            continue
        f.append({
            "code": "unhedged-strength", "severity": "warn",
            "why": f"「{term}」 is used without saying it is one school's heuristic",
            "evidence": text[max(0, i - 20): i + len(term) + 20].replace("\n", " "),
            "fix": "safety.md §1: 身强弱/用神喜忌 are the `heuristic` half of bazi.py's "
                   "payload, not a computed fact. Label it (「按扶抑一派估…」) and note "
                   "that 调候/病药 schools may read it differently.",
        })

    f += _find(text, RULE7, "reading-as-decision", "blocker", respect_refusal=True,
               fix="safety.md §1 rule 7: a reading names what they FEEL and VALUE; it "
                   "never decides. Say that plainly, then hand the question to the lens "
                   "that owns it — career.md for a job or path, relationships.md for a "
                   "partner question, factcheck.md for anything turning on external "
                   "facts. Let the lenses rhyme; never let one certify the other.")

    # --- high-stakes external facts need the factcheck block ----------------
    hs = [m.group(0) for p in HIGH_STAKES for m in re.finditer(p, text, re.I)]
    if hs:
        has_block = any(re.search(p, text, re.I) for p in FACTCHECK_MARKERS)
        if not has_block:
            f.append({
                "code": "missing-factcheck", "severity": "blocker",
                "why": f"touches a high-stakes external fact ({', '.join(sorted(set(hs))[:3])}) "
                       f"with no 来源·时效 fact-check block",
                "evidence": sorted(set(hs))[0],
                "fix": "references/factcheck.md: research a live official source, date it, "
                       "test the conditions against THIS person, and attach the "
                       "「来源 · 时效 · 你需自己确认」 block. No web access → say you "
                       "couldn't verify and route to the source; don't assert it.",
            })

    # --- disclaimer present for the module ----------------------------------
    if module in DISCLAIMER_MARKERS:
        if not any(re.search(p, text, re.I) for p in DISCLAIMER_MARKERS[module]):
            f.append({
                "code": "missing-disclaimer", "severity": "warn",
                "why": f"no honesty/entry note found for module `{module}`",
                "evidence": "",
                "fix": "assets/disclaimers.md: one light standing note per module entry "
                       "(once, not on every line). If you already gave it earlier in this "
                       "conversation, this warning is expected — ignore it.",
            })

    # --- crisis replies must not carry the fortune persona ------------------
    if module == "crisis":
        for pat, why in [(r"运势|命盘|八字|星座|流年|大运|塔罗", "mysticism in a crisis reply"),
                         (r"\b(horoscope|zodiac|fortune|chart)\b", "mysticism in a crisis reply")]:
            for m in re.finditer(pat, text, re.I):
                f.append({"code": "crisis-persona", "severity": "blocker", "why": why,
                          "evidence": m.group(0),
                          "fix": "safety.md §2: drop the fortune/advice persona entirely. "
                                 "Plain human warmth + a real, localized resource."})
        if not _names_a_real_resource(text):
            f.append({"code": "crisis-no-resource", "severity": "blocker",
                      "why": "crisis reply surfaces no real help resource",
                      "evidence": "",
                      "fix": "safety.md §2 step 3: give a real localized line, or "
                             "findahelpline.com when you don't know their country. "
                             "Never guess a country's number."})

    blockers = [x for x in f if x["severity"] == "blocker"]
    return {
        "ok": not blockers,
        "module": module,
        "blockers": len(blockers),
        "warnings": len(f) - len(blockers),
        "findings": f,
        "_note": "A surface-pattern backstop, NOT proof the reply is honest. It cannot "
                 "see a calmly-worded fabrication, a chart read off the wrong pillars, or "
                 "a callback to something they never said. The module checklists still apply.",
    }


def main():
    ap = argparse.ArgumentParser(description="Honesty gate over a drafted reply.")
    ap.add_argument("--module", default="none", choices=MODULES,
                    help="which lens the draft is for (picks the disclaimer + crisis rules)")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--text", default=None)
    src.add_argument("--file", default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--locale", default=None, choices=["zh", "en"],
                    help="force the voice check's language (default: detect)")
    ap.add_argument("--no-voice", action="store_true", help="honesty checks only")
    args = ap.parse_args()

    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            text = fh.read()
    elif args.text is not None:
        text = args.text
    else:
        text = sys.stdin.read()

    r = check(text, args.module)
    if not args.no_voice:
        r["voice"] = check_voice(text, args.locale)
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        if r["ok"] and not r["findings"]:
            print(f"selfcheck [{r['module']}]: OK — no pattern violations.\n{r['_note']}")
        else:
            print(f"selfcheck [{r['module']}]: {r['blockers']} blocker(s), "
                  f"{r['warnings']} warning(s)\n")
            for x in r["findings"]:
                mark = "✖ BLOCKER" if x["severity"] == "blocker" else "· warn"
                print(f"{mark} [{x['code']}] {x['why']}")
                if x["evidence"]:
                    print(f"    evidence: {x['evidence']}")
                print(f"    fix: {x['fix']}\n")
            print(r["_note"])
        v = r.get("voice")
        if v and v["findings"]:
            print()
            print(f"voice [{'zh' if v['cjk'] else 'en'}]: {len(v['findings'])} thing(s) "
                  f"making this read like a form, not a person\n")
            for x in v["findings"]:
                print(f"~ {x['code']}: {x['why']}")
                print(f"    fix: {x['fix']}\n")
            print(v["_note"])
        elif v:
            print("\nvoice: clean — nothing measurably machine-written.")
    sys.exit(1 if r["blockers"] else 0)


if __name__ == "__main__":
    main()
