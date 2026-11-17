#!/usr/bin/env python3
"""
safety_scan.py — a keyword/regex BACKSTOP for crisis and abuse signals.

This is deliberately a low-tech safety net, NOT the primary detector. The model
reading references/safety.md is the real safeguard: it understands context, irony,
and quoting in ways a keyword list never will. This script exists so that (a) a
crisis phrase in a logged entry sets `crisis_flag` in the index for cheap
longitudinal scanning, and (b) there is a mechanical floor if the model ever
misses something. It errs toward flagging; a flag means "slow down and look",
never "auto-respond with a script".

Patterns cover both English and Chinese because the output language is the user's
choice. Chinese is folded from traditional to simplified characters before matching
(scripts/_zh.py): every pattern here is written in simplified, and a traditional-script
"I want to kill myself" used to raise no flag at all. Returns categories, not a
diagnosis.

Usage:
  echo "text" | python3 safety_scan.py         # reads stdin
  python3 safety_scan.py --text "..."
  # or import: from safety_scan import scan_text
"""
import argparse
import json
import os
import re
import sys

if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _zh import to_simplified  # noqa: E402

# Each category: list of regexes. Kept specific-ish to limit false positives,
# but recall is prioritized over precision — this is a backstop.
PATTERNS = {
    "self_harm_suicide": [
        r"\bkill(ing)?\s+myself\b", r"\bend(ing)?\s+(it|my life)\b",
        r"\bsuicid", r"\bwant(ed)?\s+to\s+die\b", r"\bno\s+reason\s+to\s+live\b",
        r"\bdon'?t\s+want\s+to\s+(live|be here|wake up|go on)\b",
        r"\bself[-\s]?harm", r"\bcut(ting)?\s+myself\b", r"\boverdos",
        r"\bbetter\s+off\s+(dead|without me)\b", r"\bcan'?t\s+see\s+the\s+point\b",
        # Chinese — cover common phrasings AND variants that a naive list misses
        # 著 is a simplified character too, so the traditional 「活著」 never folds to 活着
        r"不想活", r"活不下去", r"撑不下去", r"活[着著]没(什么|甚么|啥)?(意思|意义)",
        r"活[着著].{0,3}没(什么|甚么|啥)?意思", r"不想(活了|醒来|存在)", r"活[着著](好累|没劲|真累)",
        r"自杀", r"结束(自己的|这一切|生命)", r"轻生", r"了结(自己|生命)",
        r"一了百了", r"走了算了", r"生无可恋",
        r"伤害自己", r"自残", r"想死", r"死了算了", r"没有活下去的意义",
        # Perceived burdensomeness: believing the people around you would be better off
        # without you. One of the clearest warning signs there is, and it contains none of
        # the words above.
        r"没有我[，,\s]*(大家|你们|他们|家里人?|爸妈|父母|所有人)(都)?(会|能|就)?(过得|变得)?"
        r"(更好|更轻松|更开心)",
        # The noun has to end the phrase: 「我是负担得起的」 and 「我是负担全家开销的人」 are
        # about money, and a false flag here switches the low-mood check off.
        r"我(就是|只是|是|成了|系)(个|一个)?((家里|家人|大家|你们|他们|所有人|爸妈|父母|屋企)(的|嘅))?"
        r"(累赘|负担|拖累|包袱|负累)(?=$|[。！？!?.,，、…~～\s]|了|啊|呀|吧|呢|而已|罢了)",
        r"(觉得|感觉)自己(就是|只是|是|成了)?(个|一个)?(累赘|负担|拖累|包袱|负累)"
        r"(?=$|[。！？!?.,，、…~～\s]|了|啊|呀|吧|呢|而已|罢了)",
        r"我(只会|总是|一直在|老是|就会)拖累(了)?(大家|你们|他们|家里人?|家人|爸妈|父母|所有人)",
        r"我(不在|走|死|消失)了?[，,\s]*(大家|你们|他们|家里人?|家人|爸妈|父母|所有人)?(就|会|都|也)?"
        r"(更好|更轻松|解脱|比较好|比较轻松|好过一点|好过些)",
        r"\b(i'?m|i am)\s+(just\s+)?(a|such a)\s+burden\b",
        r"\b(i\s+)?(feel|felt)\s+like\s+(i'?m\s+)?(a|such a|just a)\s+burden\b",
        r"\b(i'?ve|i have)\s+become\s+(a|such a)\s+burden\b",
        r"\beveryone('?s| is| would be| will be)\s+better\s+off\s+(without me|if i\b|with me gone)",
    ],
    "abuse_violence": [
        r"\bhit(s|ting)?\s+me\b", r"\bhurt(s|ing)?\s+me\b", r"\bafraid\s+of\s+(him|her|them|my)\b",
        r"\bthreaten", r"\bchoke", r"\bforced?\s+me\b", r"\bwon'?t\s+let\s+me\b",
        r"\bcontrols?\s+(my|me|what i)\b", r"\bisolat(e|ed|ing)\s+me\b",
        r"打我", r"动手", r"家暴", r"威胁我", r"不让我", r"控制我", r"害怕(他|她|回家)",
        r"逼我(?!加班|上班|工作|学习|干活|写|做作业|还钱)", r"掐(我|住)", r"跟踪我",
    ],
    # Coercive control — often the person doesn't call it abuse; pattern-of-control
    # signals matter. Recall-prioritized backstop (the model is the real detector).
    "coercive_control": [
        r"\bchecks?\s+my\s+phone\b", r"\bgoes?\s+through\s+my\s+phone\b",
        r"\btracks?\s+my\s+(location|phone)\b", r"\bmonitors?\s+me\b", r"\bfollows?\s+me\b",
        r"\bcontrols?\s+(my|the)\s+(money|finances|spending)\b",
        r"\bwon'?t\s+let\s+me\s+(see|go|talk|leave|work)\b",
        r"\bisolat(e|ed|ing|es)\s+me\s+from\b", r"\bwalking\s+on\s+eggshells\b",
        r"看我(的)?手机", r"查(我|你)?(的)?手机", r"翻我(的)?手机",
        r"查我(在哪|位置|岗)", r"查岗", r"打电话查(我|岗|位置)",
        r"规定我(能)?(花|见|去|联系)", r"管我(的钱|花钱|花多少)", r"不给我(钱|花钱)",
        r"不许我", r"不准我", r"不让我(出|见|联系|去|工作|上班)",
        r"孤立我", r"不敢(联系|见)(朋友|家人|以前)", r"监视我?",
        r"(挺|很|好|有点|真)怕(他|她|回家|你|老公|老婆|对象|男朋友|女朋友|男友|女友|伴侣)",
        r"如履薄冰", r"小心翼翼(地)?(过|生活|相处)",
    ],
    "acute_distress": [
        r"\bcan'?t\s+(do this|go on|take (it|this))\b", r"\bhopeless\b",
        r"\bbreak(ing)?\s+down\b", r"\bpanic attack\b", r"\bcan'?t\s+stop\s+crying\b",
        r"崩溃", r"撑不住", r"绝望", r"喘不过气", r"控制不住", r"停不下来地哭",
    ],
}


def scan_text(text):
    text = text or ""
    low = to_simplified(text).lower()
    # Folding is one character for one character, so a match's offsets point at the
    # words that were actually written — unless lower() changed the length somewhere.
    aligned = len(low) == len(text)
    hits = {}
    for cat, pats in PATTERNS.items():
        matched = []
        for p in pats:
            m = re.search(p, low)
            if m:
                matched.append(text[m.start():m.end()] if aligned else m.group(0))
        if matched:
            hits[cat] = matched
    # severity: self_harm / abuse / coercive-control => high; only acute_distress => watch
    if any(c in hits for c in ("self_harm_suicide", "abuse_violence", "coercive_control")):
        severity = "high"
    elif hits:
        severity = "watch"
    else:
        severity = "none"
    return {
        "crisis_flag": bool(hits),
        "severity": severity,
        "categories": list(hits.keys()),
        "matched": hits,
        "_action": (
            "If flagged: STOP the fortune/advice persona. See references/safety.md. "
            "This is a backstop, not a verdict — read the actual context."
        ),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", default=None)
    args = ap.parse_args()
    text = args.text if args.text is not None else sys.stdin.read()
    print(json.dumps(scan_text(text), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
