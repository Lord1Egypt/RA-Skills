#!/usr/bin/env python3
"""Ban invented numbers and prediction vocabulary from anything a reader sees.

There is no data behind "45-65% chance of an interview"; it is a made-up number that
reads with the authority of arithmetic. The ban is on the CONCEPT, not on the
punctuation: `匹配度 85 分` and `rated 8.5` are the same invented number as `85%`,
and for two years this file caught only the ones carrying a `%` or a slash. Collapsing strong / partial / gap into one
score needs a weight for a partial match, and any weight would be invented too. So the
conclusion is a word, the counts are printed with the evidence behind each row, and
this lint keeps the made-up numbers out.

Six things are masked before any scan, and every one of them was a live false
positive on output this skill's own files mandate:

* The verdict labels. 大概率被筛掉 -- the human-facing label for likely_screen_out --
  literally contains 概率. Without masking, this lint fires on the most common verdict
  the skill prints, and a gate that cries wolf on ordinary output is one people switch
  off. A bare 大概率 elsewhere still fires. The labels come from scripts/vocab.py and
  are never re-typed here: a hand-copied second spelling would silently un-mask the
  verdict it was copied from.
* URLs. https://www.gov.uk/2026/08/09/x matches the n/m score pattern and %20 matches
  the percent ban. A URL is an identifier, not a claim -- the same reason a citation's
  title is exempt from the digit ban in the market tables.
* The 30/60/90 planning horizon. modes/assess.md §10 REQUIRES a 30/60/90 table on
  exactly the two verdicts where the "what to do instead" half is the whole value, and
  _SCORE matches the 30/60 inside it. One token is masked; 8/11 still fires.
* The payload of a `quote=` field, inside a MOCK-*-V1 block only. An interview
  transcript is the one place in this skill where a number a HUMAN said out loud is the
  evidence, and "roughly 40% faster" is exactly the over-claim the provenance assessor
  is there to tag. Failing the file would force the transcript to be laundered, which
  deletes the finding and keeps the file. The assessor's own prose on the same line,
  and every line outside the block, is scanned as usual.

* Numbers this round CAPTURED, quoted with their neighbouring words. An employer's
  own job title can contain a percentage -- `AI/ML Engineer (100 % remote)` is a real
  LinkedIn card -- and discover renders titles exactly as captured. With no exemption
  the two rules contradict each other and the artifact that fails is the honest one.
  This masking differs from the four above in kind: it is not a list somebody
  maintains, it is a lookup against what the adapters and the fetcher actually
  returned, so it cannot go stale and cannot be widened by editing this file.

* Explicit refusals to provide a prediction. Naming a probability to say it is
  not being estimated is not a forecast. Only a closed refusal clause is masked;
  a later prediction and any number remain visible to the scan.

* Dates carrying a four-digit year (`2026/11/30`, `09/2021`) and `24/7`. A
  deadline is not a score, and neither is a support rota.

The candidate's own facts are part of that capture lookup in two forms only,
both bound by hash: the CV that evidence-blocks.json names, and — in apply mode,
which builds no evidence blocks — the master profile master-fingerprint.json
names (`check_claims.py --record`), parsed to its YAML leaves and never inside
the workspace.

The vocabulary bans the OUTCOME forecast, and only that. A word of chance or
certainty fires when it governs this candidate receiving an interview, a place on
the shortlist or an offer — not when it governs a question being asked
(`面试中大概率会被问到系统设计`) or names a subject (`概率论`, `maximum likelihood
estimation`), which are interview preparation and a posting's requirement.

The one allowlist: where an employer publishes its own rubric, the skill may walk the
candidate through THAT scale, in the employer's wording, with the source named. Quoting
an employer's scale is reporting. Treating it as a conclusion is inventing.

Exit 2 still writes a receipt, verdict "could_not_run", unless the workspace directory
itself is absent -- there is nothing to append to.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys

import yaml

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import journal  # noqa: E402
import vocab  # noqa: E402
import report_locales as locales  # noqa: E402
# Derived, not re-typed: the file check_claims.py --record writes at apply entry.
from check_claims import FINGERPRINT as MASTER_FINGERPRINT  # noqa: E402

GATE = "lint_no_prediction"

# Derived, never re-typed. The zh labels and the banned-word list are two views of
# the same closed set -- 大概率被筛掉 contains 概率 -- so a second hand-written copy
# here would un-mask whichever label drifted. Longest first, so masking a short
# label can never leave the tail of a longer one behind.
VERDICT_LABELS = tuple(sorted(
    tuple(vocab.VERDICT_ZH.values()) + tuple(vocab.VERDICTS) + (vocab.REFUSAL,)
    + tuple(label for card in locales.CARD_TEXT.values() for label in card["verdicts"].values()),
    key=len, reverse=True))

_URL = re.compile(r"https?://\S+")
# A planning horizon, not a score. modes/assess.md §10 mandates the table.
ROADMAP_HORIZON = re.compile(r"(?<![0-9])30\s*/\s*60\s*/\s*90(?![0-9])")
# Dates and the round-the-clock idiom, not scores. `截止 2026/11/30` and `24/7
# on-call` both fired SCORE_PATTERN (measured 2026-10-24) on a report's
# application deadline and a posting's own support rota. A date is recognised by
# its YEAR — a 19xx/20xx component at either end of the chain (`2026/11/30`,
# `2021/09`, `2025/26`, `30/11/2026`, `09/2021`) — because no score has a
# four-digit year as its numerator or its denominator. A bare `11/30` stays a
# finding: day/month and n/m are indistinguishable without the year.
_D = r"[0-9０-９]"
_YEAR = r"(?:[1１][9９]|[2２][0０])" + _D + r"{2}"
_SLASH = r"[/／]"
_DATE = re.compile(
    r"(?<![0-9０-９.．])(?:"
    + _YEAR + _SLASH + _D + r"{1,2}(?:" + _SLASH + _D + r"{1,2})?"
    + r"|" + _D + r"{1,2}" + _SLASH + r"(?:" + _D + r"{1,2}" + _SLASH + r")?" + _YEAR
    + r")(?![0-9０-９])(?![.．][0-9０-９])")
ROUND_THE_CLOCK = re.compile(r"(?<![0-9０-９])[2２][4４]\s*[/／]\s*[7７](?![0-9０-９])")
_MOCK_OPEN = re.compile(r"^\s*MOCK-[A-Z]+-V1\s*$")
_MOCK_CLOSE = re.compile(r"^\s*END-MOCK-[A-Z]+-V1\s*$")
_QUOTE_FIELD = re.compile(r"quote=")
# Fullwidth forms are the same claim in the same language. `％` (U+FF05) and `／`
# (U+FF0F) are what a Chinese IME produces by default, and `０-９` likewise — so
# the ASCII-only classes these replace left the ban unenforced in exactly the
# text it was most needed in.
#
# NOT solved by NFKC-normalising the line first, which is the obvious fix and the
# wrong one: `mask_exempt_spans` blanks URLs and verdict labels by replacing them
# with runs of spaces OF THE SAME LENGTH so the reported span still lines up with
# the original text. NFKC changes lengths (`％`→`%` is 1:1, but `㍑`→`リットル`
# is not), and a normalising pass would silently break that alignment. Widening
# the character classes keeps every offset exactly where it was.
# `‰` and the abbreviation `pct` are the same claim in different clothes;
# both exited 0.
_PERCENT = re.compile(r"[%％‰]|(?<![A-Za-z])pct(?![A-Za-z])", re.I)
# The decimal guards matter: `GPA 3.8/4.0` and `GPA 8.35/10` are real, honest,
# extremely common academic content, and the digits either side of the slash
# were being read out of the middle of them as `8/4` and `35/10`.
# The guards reject a DECIMAL, not a full stop. `GPA 3.8/4.0` and `GPA 8.35/10`
# are real, honest, extremely common academic content and the digits either side
# of the slash were read out of the middle of them as `8/4` and `35/10`. But
# `Coverage 9/10.` ends a sentence, and a first attempt that rejected any
# adjacent `.` silenced that too — caught by this file's own surface test. So
# the lookarounds reject only a dot with a DIGIT on the far side.
_SCORE = re.compile(
    r"(?<![0-9０-９])(?<![0-9０-９][.．])"
    r"[0-9０-９]+\s*[/／]\s*[0-9０-９]+"
    r"(?![0-9０-９])(?![.．][0-9０-９])")

# The Chinese half was four hand-listed words, so 「成功率」「入围率」「七成」 and
# 「百分之七十」 all shipped clean — and `--lang zh` is the DEFAULT
# (count_coverage.py:170), which made this the skill's primary output language.
#
# A bare `X率` would be wrong in the other direction: 效率, 利率, 增长率 and
# 采样率 are ordinary words on an engineer's CV. The character class is bounded
# to the words that describe getting the job, so it cannot reach them.
#
# 可能性 is deliberately ABSENT. The mandated disclaimer is
# 「本 skill 不给出面试或录用的可能性估计」 — banning the word would make the
# required text fail its own gate, which is the defect layer 1 already had once.
# Spelled out, not a character class. `[通过入围命中录取用成功面试中签]{1,3}率`
# matched any 1-3 of those characters before 率, so it fired inside ordinary
# business words the skill's own market cards use: 达成率 ("成率"), 交付率,
# 出勤率. A ban that fires on honest, mandated content is a ban that gets
# switched off. These are the words that describe GETTING THE JOB, and
# nothing else.
#
# 概率 is ALSO the name of a subject. 「熟悉概率论与数理统计」 is one of the most
# common requirements on a data or ML posting, and a report that quotes the
# requirement it is assessing blocked delivery as a forecast (measured
# 2026-10-24: DELIVER_REPORT_PREDICTION, exit 2). So the word is exempt when the
# next morpheme makes it the subject — 概率论 / 概率统计 / 概率分布 / 概率模型 —
# and NOT exempt once an outcome stands in front of it: 录用概率模型 is still
# a hiring probability, whatever noun follows it.
_PROB_SUBJECT_ZH = (r"(?:论|論|统计|統計|分布|模型|图模型|圖模型|密度|编程|編程"
                    r"|[与和及與]\s*(?:数理|數理)?\s*(?:统计|統計))")
_OUTCOME_BEFORE_PROB_ZH = (r"(?:面试|面試|录用|錄用|录取|錄取|入围|入圍|通过|通過|成功|"
                           r"中签|上岸|进面|offer)\s*")
# Predicting the interview QUESTIONS is the prep job, not a forecast of the
# outcome: `面试中大概率会被问到系统设计，请准备一个例子` blocked delivery
# (measured 2026-10-24). 被问到 / 问到 / 追问 / 考察 / 涉及 … — the object is a
# question or a topic. `让你` / `要求你` only with a verb of explaining or
# producing, because `大概率会让你进入下一轮` is the outcome again. Bare 大概率
# fires through 概率 below, so the release has to be granted there as well as on
# the hedge list — and ONLY for 大概率, the idiom; 录用概率 never reaches it.
_ZH_ASKED = (r"(?:会|将|还会|也会)?(?:被)?(?:问到|问及|问起|问你|问|追问|深挖|考察|考查|"
             r"考到|考你|聊到|聊|谈到|提到|提问|涉及|围绕|聚焦|"
             r"(?:让|要求)你(?:讲|解释|介绍|描述|展开|画|写|设计|手写|演示|举例))")
_ZH_RATE = (_OUTCOME_BEFORE_PROB_ZH + r"(?:概率|机率|機率)"
            r"|(?<!大)(?:概率|机率|機率)(?!" + _PROB_SUBJECT_ZH + r")"
            r"|(?<=大)概率(?!" + _PROB_SUBJECT_ZH + r")(?!" + _ZH_ASKED + r")"
            r"|通过率|命中率|录取率|录用率|成功率|入围率|中签率|面试率|"
            r"錄取率|錄用率|成功機會|勝算")
# The real report said 不提供匹配分或录用概率. Consume only named quantities,
# conjunctions and a clause ending; no arbitrary text or numeric estimate can
# hide inside this exception. Double negations are not refusals.
_REFUSED_QUANTITY_ZH = (r"(?:匹配分|匹配度|匹配百分比|ATS\s*分数|(?:面试|录用|录取|入围)?(?:"
                        + _ZH_RATE + r"))")
_REFUSED_PREDICTION_ZH = re.compile(
    r"(?<!不)(?<!不是)(?<!并非)(?<!不能)(?<!未必)(?<!不一定)"
    # 会/能/予 between the negator and the verb is ordinary Chinese, and so is
    # 无法. The mask was built around the single sentence one real report
    # happened to use, so `不会提供录用概率` and `无法给出录用概率` — refusals
    # this skill tells the author to write — blocked delivery as forecasts.
    r"(?:(?:不|未|没有(?:依据)?|无法|未能|不便)(?:会|能|予)?"
    r"(?:提供|给出|估算|估计|预测|计算|作出|做出)(?:任何)?"
    r"|(?:不是|并非)(?:对)?)"
    + _REFUSED_QUANTITY_ZH
    + r"(?:[、或与和及]" + _REFUSED_QUANTITY_ZH + r")*"
    r"(?:的)?(?:估计|预估|预测|数值|数字)?(?=[，。！？；,;.!?\s]|$)")
# The English half of the same exemption. `probabilit(y|ies)`, `odds` and
# `likelihood` are bare word matches in _WORDS, so every English sentence that
# REFUSES to give one fired as if it had given one — and the refusal is what
# this skill instructs the author to write. Each alternative is bounded to its
# own clause (no comma, no sentence end), so a real claim sharing the sentence
# still reaches the scanner.
_EN_FORECAST_NOUN = (r"(?:(?:interview|offer|hiring|callback|success|match|fit)\s+)?"
                     r"(?:probabilit(?:y|ies)|odds|likelihood|chances?|score)")
_NEGATED_EN = (r"(?:\b(?:does|do|did|will|would|can|could|shall|is|are|am|was|were)\s+not\b"
               r"|\bcannot\b|\b(?:can|won|don|doesn|didn|isn|aren|wouldn|couldn)['’]t\b)")
# Every alternative ends ON the quantity it refuses. An open-ended tail is what
# the first draft used, and it swallowed the rest of the clause: `does not give
# an interview probability but your odds are 80%` went silent, so a cry-wolf fix
# had opened a detection hole. Found by probing the fix with inputs it was not
# written against, not by the tests written alongside it.
_EN_OUTCOME_TAIL = (r"(?:\s+(?:of|at|for)\s+(?:getting|landing|receiving|an?|the)"
                    r"(?:\s+(?:an?|the))?(?:\s+(?:interview|offer|job|role|position))?)?")
_REFUSED_PREDICTION_EN = re.compile(
    r"(?:" + _NEGATED_EN + r"\s+(?:give|provide|offer|predict|estimate|forecast|state|"
    r"include|compute|calculate|report)(?:\s+(?:you|your|their|any|an?|the))*\s+"
    + _EN_FORECAST_NOUN + _EN_OUTCOME_TAIL +
    r"|\bno\s+" + _EN_FORECAST_NOUN + r"\s+(?:is|are|was|were)\s+"
    r"(?:provided|given|offered|stated|included|reported)"
    r"|\bnot\s+an?\s+(?:prediction|forecast|estimate|guarantee)\s+of"
    r"(?:\s+(?:your|their|the|an?))*\s+" + _EN_FORECAST_NOUN + _EN_OUTCOME_TAIL +
    r")", re.IGNORECASE)
# 七成 = 70%. The lookahead keeps 成功/成长/成员/成果/成本/成熟/成为 out; those are
# the ordinary compounds a Chinese numeral can legitimately sit in front of.
# Arabic digits too. `八成` fired and `8 成` did not — a pre-existing gap this
# audit walked into, and the two spellings are the same claim.
# 八成 is also the idiom for "most probably", the same word as 大概率, and
# `八成会问到系统设计` predicts a QUESTION — it blocked delivery through this rule
# while _HEDGE_ZH had already released it. So 八成 takes 大概率's allowance and
# nothing wider: only the idiom, only before _ZH_ASKED. 七成会问到 / 8成会问到
# are a figure, and still fire.
_ZH_TENTHS = (r"(?!八\s*成" + _ZH_ASKED + r")"
              r"[一二三四五六七八九0-9０-９]\s*成(?![功长员果本熟为立就分交交])")
_ZH_PERCENT_SPELLED = r"百分之[零一二三四五六七八九十百]+"
# Japanese tenths. `_ZH_TENTHS` gave Chinese 七成 its own rule and Japanese has
# the exact parallel in 割 — `可能性は7割です` is the same invented probability
# and sailed through a file whose commit claimed every language it writes in.
_JA_TENTHS = r"[0-9０-９一二三四五六七八九][\s]*割(?![引り])"

# Outcome forecasts in the other languages this skill writes in. The English and
# Chinese vocabularies were enforced and the rest were not, so
# `Sie werden das Vorstellungsgespräch sicher bekommen.`,
# `Je hebt een grote kans op een gesprek.`, `面接に呼ばれる可能性が高いです。` and
# `합격 확률은 높습니다.` all shipped while their English twin fired.
#
# Kept to the NOUN of chance and to a modal aimed at an interview or an offer,
# for the same reason the English set is: this must not fire on an honest
# sentence about the job itself.
# `Chance` and `kans` are the ORDINARY words for "opportunity" in German and
# Dutch — `Chancen zur Weiterbildung`, `kansen voor groei` are what postings
# actually say — so banning them bare cried wolf on honest text. English keeps
# its bare `chances?` because "chance" rarely carries that sense there; the
# collision rate is a fact about the language, not an inconsistency.
#
# So they fire only next to an OUTCOME, or in the idiom that is a forecast on
# its own. `Wahrscheinlichkeit` and `waarschijnlijkheid` stay bare: those mean
# probability and nothing else.
# Proximity to a JOB NOUN was the wrong test and an independent pass proved it:
# `die Chance, in diesem Job viel zu lernen`, `de kans om veel te leren in deze
# baan` — job nouns are exactly what makes OPPORTUNITY language job-related, so
# that rule fired on 6 of 6 honest recruiting sentences.
#
# A LIKELIHOOD predicate is the real separator. `Die Chancen stehen gut` and
# `een grote kans op een gesprek` say how probable; `wir bieten die Chance` and
# `grijp de kans` say what is on offer. `gut`/`goed` are deliberately NOT in the
# list — `eine gute Chance, das Team kennenzulernen` is an offer, and including
# them puts the false positive straight back.
def _not_after(*forms: str) -> str:
    """One fixed-width lookbehind per form: `re` takes no variable-width one."""
    return "".join("(?<!" + re.escape(form) + ")" for form in dict.fromkeys(forms))


# What is RECEIVED is the object; `im Vorstellungsgespräch` / `in het gesprek` is
# where it happens. `Sie werden im Vorstellungsgespräch Fragen bekommen` and `Je
# krijgt in het gesprek zeker vragen over je scriptie` receive QUESTIONS, and both
# fired through the werden/krijgt shapes below (measured 2026-10-24).
_DE_NOT_ADVERBIAL = _not_after(*(prep + " " + art for prep in (
    "im", "beim", "vom", "am", "in", "bei", "nach", "vor", "während", "seit", "aus", "mit")
    for art in ("", "dem ", "einem ", "des ", "eines ", "der ", "einer ")))
_NL_NOT_ADVERBIAL = _not_after(*(prep + " " + art for prep in (
    "in", "tijdens", "bij", "na", "voor", "naar", "op", "met", "over", "vóór")
    for art in ("", "het ", "een ", "de ", "je ", "jouw ", "uw ")))
_DE_LIKELIHOOD = r"hoch|gering|gro\u00df|klein|niedrig|steh(?:en|t)|liegt bei|betr\u00e4gt"
_NL_LIKELIHOOD = r"groot|grote|klein|kleine|hoog|hoge|laag|lage|gering"
_FORECAST_DE = (r"\bwahrscheinlichkeit\b"
                r"|\b(?:chance|chancen|aussichten)\b[^.!?]{0,40}\b(?:" + _DE_LIKELIHOOD + r")\b"
                r"|\b(?:" + _DE_LIKELIHOOD + r")\b[^.!?]{0,25}\b(?:chance|chancen|aussichten)\b"
                r"|\bwerden\b[^.!?]{0,40}(?=\b(?:einladung|vorstellungsgespr\u00e4ch|zusage|angebot)\b)"
                + _DE_NOT_ADVERBIAL + r"\b(?:einladung|vorstellungsgespr\u00e4ch|"
                r"zusage|angebot)\b[^.!?]{0,20}\b(?:bekommen|erhalten)\b")
_FORECAST_NL = (r"\bwaarschijnlijkheid\b"
                r"|\b(?:kans|kansen)\b[^.!?]{0,40}\b(?:" + _NL_LIKELIHOOD + r")\b"
                r"|\b(?:" + _NL_LIKELIHOOD + r")\b[^.!?]{0,25}\b(?:kans|kansen)\b"
                r"|\bkrijgt\b[^.!?]{0,40}(?=\b(?:gesprek|uitnodiging|aanbod)\b)" + _NL_NOT_ADVERBIAL
                + r"\b(?:gesprek|uitnodiging|aanbod)\b")
# The probability NOUN is also the name of a subject in every one of these
# languages — `probabilités et statistiques`, `probabilidad y estadística`,
# 確率論, 확률론 — and a posting's own requirement quoted in a report is not a
# forecast. Same exemption as _PROB_SUBJECT_ZH, same narrowness: the subject has
# to be named right next to the word.
_FORECAST_FR = (r"(?<!théorie des )(?<!calcul des )(?<!distribution de )"
                r"\b(?:probabilité|probabilités)\b"
                r"(?!\s+(?:et\s+statistiques?|conditionnelles?)\b)"
                r"|\bchances? d[eu'](?:\s|’)?(?:être|obtenir|décrocher)\b")
_FORECAST_ES_IT = (r"(?<!teoría de la )(?<!teoría de )(?<!distribución de )"
                   r"(?<!teoria della )(?<!calcolo delle )(?<!distribuzione di )"
                   r"\b(?:probabilidad|probabilidades|probabilità)\b"
                   r"(?!\s+(?:y\s+estad[ií]stica|e\s+statistica|condicional|condizionata)\b)")
# 確率的 is "stochastic" (確率的勾配降下法 = SGD), not a chance of anything.
_JA_PROB = (r"(?:合格|内定|採用|通過|面接|選考)\s*(?:の)?\s*確率"
            r"|確率(?!論|統計|分布|モデル|過程|的|密度|変数)")


# Being ASKED, or a topic COMING UP — the release _ZH_ASKED gives 大概率会被问到,
# in Japanese, Korean and Spanish. Measured 2026-10-24, each blocked delivery as
# a forecast: `面接では志望動機を聞かれる可能性が高いです`, `면접에서 프로젝트 경험에
# 대해 질문받을 가능성이 높습니다`, `En la entrevista es probable que te pregunten
# por Kafka`. A likelihood NOUN follows the verb it governs, so its release is a
# set of lookbehinds on that verb; an ADVERB comes first, so its release looks
# ahead to the verb — and never across a verb of RECEIVING the outcome:
# `おそらく面接に呼ばれて志望動機を聞かれます` and `Es muy probable que te inviten a
# una entrevista y te pregunten por Kafka` still forecast the invitation.
_JA_ASKED_STEMS = ("聞かれ", "訊かれ", "問われ", "質問され", "尋ねられ", "出題され",
                   "深掘りされ", "掘り下げられ", "突っ込まれ", "触れられ", "話題にな",
                   "話題に上", "質問が出", "質問が来")
_JA_ASKED_BEFORE = _not_after(*(stem + "る" for stem in _JA_ASKED_STEMS))
_JA_RECEIVE_VERB = (r"呼ばれ|進め|進ん|進む|進み|もらえ|貰え|獲得|通過|通り|通る|通れ|受か"
                    r"|招かれ|案内され|採用され|合格")
_JA_ASKED_AHEAD = (r"(?:(?!" + _JA_RECEIVE_VERB + r")[^。！？、\n]){0,15}?(?:"
                   + "|".join(_JA_ASKED_STEMS) + r")")
_FORECAST_JA = (_JA_ASKED_BEFORE + r"可能性が[^。！？]{0,10}高い|"
                + _JA_ASKED_BEFORE + r"見込みが[^。！？]{0,10}高い|" + _JA_PROB +
                r"|受かる見込み|通る見込み")
_KO_PROB = (r"(?:합격|채용|면접|서류)\s*확률"
            r"|확률(?!\s*(?:론|통계|분포|모델|적|과정|변수|밀도))")
_KO_ASKED_BEFORE = _not_after(*(verb + gap for verb in (
    "질문받을", "질문을 받을", "질문 받을", "질문받게 될", "질문을 받게 될", "질문이 나올",
    "물어볼", "물을", "질문할", "다뤄질", "다루어질", "출제될", "언급될") for gap in ("", " ")))
_KO_RECEIVE_VERB = r"붙|통과|합격|채용되|채용될|초대|불려|제안|오퍼"
_KO_ASKED_AHEAD = (r"(?:(?!" + _KO_RECEIVE_VERB + r")[^.!?,。\n]){0,20}?"
                   r"(?:질문\s*(?:을|이|도|은)?\s*(?:받|나오|나올|나온|들어오|들어올)"
                   r"|물어보|물어볼|물어봅|물으|물을|묻|질문하|질문할|다뤄|다루어|다룰|출제"
                   r"|언급되|언급될|꼬리\s*질문)")
_FORECAST_KO = (_KO_PROB + r"|" + _KO_ASKED_BEFORE + r"가능성이\s*[^.!?]{0,10}?(?:높|큽)"
                r"|합격할 것")
_ES_RECEIVE_VERB = (r"\b(?:te|le|les|os)\s+(?:llam|invit|contrat|seleccion|ofrec|ofrezc"
                    r"|entrevist|admit)|\b(?:consig|consegu|obten|obtien|recib|logr)\w*"
                    r"|\bpas(?:ar|es|en|ar[aá]s|ar[aá]n)\b")
_ES_ASKED_AHEAD = (r"(?:(?!" + _ES_RECEIVE_VERB + r")[^.!?;\n]){0,40}?"
                   r"(?:\b(?:te|le|les|os)\s+(?:(?:van|vayan|iban)\s+a\s+)?"
                   r"(?:pregunt|interrog|ped|pid|plante)\w*\b"
                   r"|\b(?:te|le|les|os)\s+(?:hag|har)\w*\s+preguntas\b"
                   r"|\b(?:salga|salgan|surja|surjan|aparezca|aparezcan)\b)")


# The same release in German, Dutch, French and Italian, which had none: measured
# 2026-10-24, `Nel colloquio ti chiederanno sicuramente del tuo progetto`, `In het
# gesprek vragen ze zeker naar je scriptie`, `Im Vorstellungsgespräch fragt man Sie
# sicherlich nach Ihrer Motivation` and `En entretien, on vous demandera
# probablement votre motivation` each fired as a forecast. In these four the verb
# of asking may stand on EITHER side of the hedge — `chiederanno sicuramente`
# (verb first), `wird wahrscheinlich … gefragt` (participle last) — so the release
# is a lookbehind on the verb right before the hedge, or a question ahead of it
# that nothing RECEIVED stands in front of. Asking someone to COME to an
# interview is the invitation itself (`ti chiederanno sicuramente di venire a un
# colloquio`), the same carve-out `asked to interview` has in English.
def _ask_release(words: str, asked_before: tuple, asked_ahead: str, invite: str) -> str:
    """`words`, minus the hedges that govern a question. The leading lookahead
    only spares every other position the lookbehind sets."""
    after = "|".join("(?<=" + re.escape(form) + ")" for form in dict.fromkeys(asked_before))
    return (r"(?=" + words + r")(?:" + _not_after(*asked_before) + r"(?:" + words + r")"
            r"(?!" + asked_ahead + r")|(?:" + after + r")(?:" + words + r")(?=" + invite + r"))")


def _ahead(received: str, asked: str, invite: str, reach: int = 40) -> str:
    return (r"(?:(?!" + received + r")[^.!?;\n]){0," + str(reach) + r"}?(?:" + asked + r")"
            r"(?!" + invite + r")")


def _outcome_object(prepositions: tuple, articles: str, nouns: str) -> str:
    """The outcome as a determined noun phrase — `ein Interview`, `un entretien` —
    and not inside an adverbial: `im Interview`, `lors de l'entretien`, `nel
    colloquio` are where the questions get asked, not what is received.
    `Vous obtiendrez probablement un entretien et on vous interrogera` puts the
    verb of receiving BEFORE the hedge and only its object after it."""
    phrase = r"\b(?:" + articles + r")(?:" + nouns + r")\b"
    return r"(?=" + phrase + r")" + _not_after(*(word + " " for word in prepositions)) + phrase


_DE_ASKED_BEFORE = tuple(verb + " " + who for verb in (
    "fragt", "fragen", "befragt", "befragen", "erkundigt", "erkundigen") for who in (
    "", "man ", "man Sie ", "man dich ", "man euch ", "Sie ", "dich ", "sie Sie ", "sie dich ",
    "der Interviewer ", "die Interviewer ", "die Interviewerin ")) + ("geht es ",)
_DE_PREPOSITIONS = ("im", "beim", "zum", "zur", "vom", "am", "ins", "in", "für", "auf", "durch",
                    "über", "um", "an", "ohne", "gegen", "nach", "vor", "bei", "mit", "aus",
                    "während", "seit", "zu")
_DE_RECEIVED = (r"\b(?:bekomm\w*|erhalt\w*|erh[aä]lt\w*|krieg\w*|eingeladen|einlad\w*|eingestellt"
                r"|einstell\w*|zusage\w*|weiterkomm\w*|angenommen)\b|" + _outcome_object(
                    _DE_PREPOSITIONS, r"(?:ein|eine|einen|das|die|den|der|ihr|ihre|ihren|dein|deine"
                    r"|deinen)\s+", r"vorstellungsgespr[aä]ch|einladung|zusage|angebot|jobangebot"
                    r"|stellenangebot|interview|zweitgespr[aä]ch"))
_DE_ASKED = (r"\b(?:gefragt|befragt|abgefragt|nachgefragt|fragen|fragt|angesprochen|thematisiert"
             r"|gepr[uü]ft)\b|\bzur\s+sprache\b")
_DE_INVITE = (r"[^.!?;]{0,20}?\b(?:zu(?:m)?\s+(?:einem\s+)?(?:vorstellungsgespr[aä]ch|gespr[aä]ch"
              r"|interview)|eingeladen|einladen|vorbeizukommen)\b")
_NL_ASKED_BEFORE = tuple(verb + " " + who for verb in (
    "vragen", "vraagt", "ondervragen", "ondervraagt", "informeren", "informeert") for who in (
    "", "ze ", "zij ", "men ", "ze je ", "ze u ", "men je ", "men u ", "je ", "u ",
    "de interviewer ", "de interviewers ")) + ("gaat het ",)
_NL_PREPOSITIONS = ("in", "tijdens", "bij", "voor", "na", "naar", "op", "met", "over", "om",
                    "tot", "van", "uit", "door", "zonder", "aan")
_NL_RECEIVED = (r"\b(?:krijg\w*|ontvang\w*|uitgenodigd|uitnodig\w*|nodig\w*\s+(?:je|u)\s+uit"
                r"|aangenomen|aannemen|door\s+naar|doorgaan)\b|" + _outcome_object(
                    _NL_PREPOSITIONS, r"(?:een|het|de|je|jouw|uw)\s+(?:tweede\s+)?",
                    r"gesprek|sollicitatiegesprek|uitnodiging|aanbod|baanaanbod|interview|contract"))
_NL_ASKED = (r"\b(?:vragen|vraagt|gevraagd|ondervraagd|ondervragen|bevraagd|doorgevraagd"
             r"|doorvragen)\b|\bter\s+sprake\b|\baan\s+bod\b|\b(?:gaat|gaan)\s+(?:het\s+)?over\b")
_NL_INVITE = (r"\s+(?:(?:je|u)\s+)?(?:voor\s+(?:een|het|de)\s+(?:\w+\s+)?(?:gesprek|sollicitatiegesprek"
              r"|interview)|terug\b|op\s+gesprek|(?:om\s+)?(?:langs|terug)\s+te\s+komen)")
# French and Italian put the object after the verb, so a verb of receiving only
# blocks the release with an OUTCOME object: `recevoir des questions` is prep.
_FR_ASKED_BEFORE = tuple(verb + " " for verb in (
    "demandera", "demanderont", "posera", "poseront", "interrogera", "interrogeront",
    "questionnera", "questionneront", "portera", "porteront", "abordera", "aborderont",
    "testera", "testeront"))
_FR_OUTCOME_OBJ = (r"(?:un|une|l['’]|le|la|votre|ton|ta)\s*(?:entretien|offre|proposition"
                   r"|convocation|poste)\b")
_FR_RECEIVED = (r"\b(?:(?:obten|obtiendr|recev|recevr|d[ée]croch|aur)\w*\s+" + _FR_OUTCOME_OBJ +
                r"|convoqu[ée]e?s?|invit[ée]e?s?|retenue?s?|embauch[ée]e?s?|recrut[ée]e?s?"
                r"|s[ée]lectionn[ée]e?s?)|" + _outcome_object(
                    ("à", "a", "de", "du", "des", "pendant", "durant", "lors", "pour", "dans",
                     "après", "avant", "en", "par", "sur", "avec", "sans", "chez", "au"),
                    r"(?:un|une|le|la|votre|ton|ta|cet|cette)\s+|l['’]",
                    r"entretien|offre|proposition|convocation"))
_FR_ASKED = (r"\b(?:interrog\w*|questionn\w*|demander\w*|demand[ée]e?s?|questions|abord[ée]e?s?"
             r"|aborder\w*|test[ée]e?s?|[ée]voqu\w*|port\w*\s+sur)\b"
             r"|\bquestion\s+(?:de|du|des|sur)\s+(?!temps\b|jours\b|semaines\b|mois\b)")
_FR_INVITE = (r"[^.!?;]{0,12}?\b(?:venir|revenir|passer\s+(?:un|une|l['’]|le)|participer"
              r"|vous\s+pr[ée]senter\s+(?:[àa]|au|pour))")
_IT_ASKED_BEFORE = tuple(verb + " " for verb in (
    "chiederanno", "chiederà", "chiederebbero", "domanderanno", "domanderà", "interrogheranno",
    "interrogherà", "verterà", "verteranno", "riguarderà", "riguarderanno", "approfondiranno",
    "approfondirà", "toccherà", "toccheranno", "parlerà", "parleranno"))
_IT_OUTCOME_OBJ = (r"(?:un['’]|un\s+|una\s+|il\s+|lo\s+|la\s+|l['’])?(?:colloquio|offerta|proposta"
                   r"|assunzione|convocazione)\b")
_IT_RECEIVED = (r"\b(?:(?:otterr|ottene|ottien|ricever|riceve|avr)\w*\s+" + _IT_OUTCOME_OBJ +
                r"|(?:ti|vi)\s+(?:chiamer|richiamer|convocher|inviter|assumer|selezioner|offrir)\w*"
                r"|(?:chiamat|richiamat|convocat|invitat|assunt|selezionat)[oaie]\b)|" + _outcome_object(
                    ("a", "al", "allo", "alla", "all", "nel", "nello", "nella", "nell", "del", "dello",
                     "della", "dell", "dal", "dalla", "dall", "sul", "sulla", "per", "di", "in", "con",
                     "durante", "dopo", "prima", "tra", "fra", "su", "da"),
                    r"(?:un|una|il|lo|la)\s+|un['’]|l['’]",
                    r"colloquio|offerta|proposta|assunzione|convocazione"))
_IT_ASKED = (r"\b(?:(?:ti|vi|le|gli)\s+)?(?:chied\w*|domander\w*|domandino|interrog\w*|chiest[oaie]"
             r"|verter\w*|riguarder\w*|approfondir\w*"
             r"|parler\w*\s+(?:di|del|della|dei|delle|dello)|far\w*\s+(?:\w+\s+)?domande"
             r"|domande\s+(?:su|sul|sull|sulla|sui|sugli|sulle|di|tecniche|riguard\w*|relative"
             r"|specifiche))\b")
_IT_INVITE = (r"\s+(?:di\s+)?(?:venire|tornare|partecipare|presentarti|presentarvi|sostenere"
              r"|fare\s+un\s+colloquio|un\s+colloquio|un\s+secondo)")

# ---------------------------------------------------------------------------
# The ADVERB and ADJECTIVE forms. Measured 2026-09-08: the patterns above cover
# the NOUN of probability in every language -- `Wahrscheinlichkeit`,
# `probabilidad`, `확률`, `確率` all fire -- and 13 of 15 natural predictions
# still sailed through, English and Chinese included:
#
#   You will very likely be invited to interview.        not caught
#   你很可能会拿到面试。                                  not caught
#   Es muy probable que te inviten a una entrevista.     not caught
#   면접에 초대될 가능성이 매우 높습니다.                  not caught  (adverb split 가능성이…높)
#
# So this was never a localisation gap: the check had the wrong SHAPE in all
# nine languages, and README_EN's "checks predefined expressions in all nine CV
# languages" was true only of the nouns.
#
# The adverb alone is NOT the offence and must never fire on its own. `This role
# likely involves travel`, `Die Stelle erfordert wahrscheinlich Reisebereitschaft`
# and `이 직무는 아마 출장이 잦을 것입니다` are ordinary, correct sentences, and a
# gate that fires on them is the cry-wolf this file already paid for once with
# bare `chances?`. What is banned is a probability word attached to THIS
# candidate RECEIVING an outcome, so both halves are required inside one
# sentence.
#
# The outcome list is deliberately narrow: `interview`, `offer`, `callback`,
# `shortlisted`, `hired`, `invited`. `job`, `role` and `position` are left OUT --
# `this role likely involves travel` would otherwise fire, and the posting's own
# noun is the most common word on the page.
# `most likely` has two jobs in English and only one of them is a forecast.
# Adverbial — `you will most likely get an interview` — is the ban. Attributive —
# `the most likely technical probe in the interview`, `most likely cause of a
# "please confirm" email` — names which of several options is likeliest and is
# ordinary analysis. Both of those are REAL sentences, found in the iteration-2
# baseline outputs when this pattern was measured against every markdown file in
# the repo and the results tree; they were the only two lines the widening would
# have newly fired on, and both would have been cry-wolf.
# The guard belongs on `likely` ITSELF, not on the `most likely` alternative: a
# bare `likely` matches inside `most likely` too, so excluding the longer form
# alone changed nothing (measured — both real sentences still fired).
#
# Two signals separate the two uses, and a determiner is the stronger one:
# attributive `likely` follows one (`the most likely probe`, `a likely cause`),
# adverbial `likely` follows an auxiliary (`you will likely get`). The noun
# lookahead catches the rest, where the line began mid-sentence.
_LIKELY = (r"(?<!the most )(?<!a most )(?<!the )(?<!a )(?<!an )(?<!this )(?<!that )"
           r"(?<!its )(?<!their )(?<!our )likely"
           r"(?!\s+(?:\w+\s+)?(?:cause|reason|explanation|probe|question|topic|"
           r"source|culprit|outcome|scenario|route|path|next step)\b)")
# Predicting the QUESTIONS is the interview-prep job, not a forecast of the
# outcome. `面试中大概率会被问到系统设计，请准备一个例子` blocked delivery
# (measured 2026-10-24) — the sentence the interview mode exists to write — and
# so did `The interview will probably focus on system design`. The hedge is
# released only when what it governs, immediately after it, is being ASKED or a
# topic COMING UP; `大概率会通过` and `will probably get an interview` keep it.
# The object list for `get/face … questions` is closed for the same reason:
# `get an interview` must not borrow the exemption that `get an interview
# question` earns.
# `asked to interview` / `asked back` is the invitation itself, so `asked` only
# releases the hedge when it is not followed by one.
_EN_ASKED = (r"\s+(?:to\s+)?(?:be\s+)?(?:asked|quizzed|tested|probed|pressed|grilled"
             r"|questioned|challenged)\b"
             r"(?!\s+(?:to\s+(?:interview|come\s+in|attend|meet|join)|back\b"
             r"|for\s+an?\s+(?:interview|second|follow-up|final)))"
             r"|\s+(?:to\s+)?(?:come\s+up|ask|cover|include|involve|focus|feature|probe"
             r"|test|dig|explore|revolve|center|centre|touch\s+on|start\s+with"
             r"|open\s+with|begin\s+with|consist)\b"
             r"|\s+(?:to\s+)?(?:get|face|hear|see|encounter|field)\s+"
             r"(?:(?:an?|some|the|several|a\s+few|follow-up|technical|behaviou?ral"
             r"|coding|system[- ]design|tough|hard|interview)\s+)*"
             r"(?:questions?|follow-ups?|probes?|prompts?|case\s+stud(?:y|ies)"
             r"|exercises?|take-homes?)\b")
_HEDGE_EN = (r"(?:very likely|almost certainly|quite likely|highly likely"
             r"|most " + _LIKELY + r"|" + _LIKELY +
             r"|probably|certainly|surely|doubtless)(?!" + _EN_ASKED + r")")
_OUTCOME_EN = (r"interview|offer|callback|call back|short-?list(?:ed|ing)?|hired"
               r"|invited|invitation|accepted|through to the next round")
# _ZH_ASKED (defined beside _ZH_RATE, which needs it for bare 大概率) is the
# Chinese half of the same release.
_HEDGE_ZH = (r"(?:很可能|多半|大概率|八成|十有八九|极有可能|极可能|应该能|多半会)"
             r"(?!" + _ZH_ASKED + r")")
_OUTCOME_ZH = r"面试|录取|入围|offer|通过初筛|拿到|进面"
# The DE / NL / FR / IT hedges carry the question release defined beside
# _ask_release.
_HEDGE_DE = _ask_release(r"h[o\u00f6]chstwahrscheinlich|wahrscheinlich|vermutlich|sicherlich",
                         _DE_ASKED_BEFORE, _ahead(_DE_RECEIVED, _DE_ASKED, _DE_INVITE), _DE_INVITE)
_OUTCOME_DE = (r"vorstellungsgespr[a\u00e4]ch|einladung|eingeladen|zusage|angebot"
               r"|interview")
_HEDGE_NL = _ask_release(r"hoogstwaarschijnlijk|waarschijnlijk|vermoedelijk|zeker",
                         _NL_ASKED_BEFORE, _ahead(_NL_RECEIVED, _NL_ASKED, _NL_INVITE), _NL_INVITE)
_OUTCOME_NL = r"gesprek|uitnodiging|uitgenodigd|aanbod|interview"
_HEDGE_FR = _ask_release(r"tr[e\u00e8]s probablement|probablement|vraisemblablement|s[u\u00fb]rement",
                         _FR_ASKED_BEFORE, _ahead(_FR_RECEIVED, _FR_ASKED, _FR_INVITE), _FR_INVITE)
_OUTCOME_FR = r"entretien|offre|invit[e\u00e9]|retenu|convoqu[e\u00e9]"
# The JA / KO / ES hedges carry the question release defined beside _FORECAST_JA.
_HEDGE_ES = (r"(?:muy probable|probablemente|probable|seguramente|casi seguro)"
             r"(?!" + _ES_ASKED_AHEAD + r")")
_OUTCOME_ES = r"entrevista|oferta|inviten|invitar[a\u00e1]n|contraten|seleccionen|admitan"
_HEDGE_IT = _ask_release(r"molto probabilmente|probabilmente|probabile|sicuramente",
                         _IT_ASKED_BEFORE, _ahead(_IT_RECEIVED, _IT_ASKED, _IT_INVITE), _IT_INVITE)
_OUTCOME_IT = r"colloquio|offerta|invitato|assunto|selezionato"
_HEDGE_JA = r"(?:おそらく|恐らく|十中八九|まず間違いなく|ほぼ確実)(?!" + _JA_ASKED_AHEAD + r")"
_OUTCOME_JA = r"面接|内定|採用|合格|選考通過"
_HEDGE_KO = r"(?:아마|십중팔구|거의 확실|틀림없이)(?!" + _KO_ASKED_AHEAD + r")"
_OUTCOME_KO = r"면접|합격|채용|제안|서류 통과"


# How far apart the two halves may sit. Bounded by sentence punctuation as well,
# so they cannot be borrowed from neighbouring sentences -- `The role likely
# involves travel. An offer was made to someone else.` is two facts, not a
# forecast.
#
# The CJK window is a QUARTER of the Latin one, and that is not a guess. A
# Chinese, Japanese or Korean character carries far more of a clause than a Latin
# one, and 60 of them span a whole chain of them: measured 2026-09-08, a single
# window of 60 fired on all three of
#
#   这个岗位很可能需要经常出差，团队分布在三个城市，……而面试环节安排在下午
#   この職種はおそらく出張が多く、チームは三都市に分かれており、面接は午後に行われます
#   이 직무는 아마 출장이 잦고 팀은 세 도시에 나뉘어 있으며 면접은 오후에 진행됩니다
#
# — three correct sentences, in the language the skill's own default reports are
# written in. Across every real prediction in the corpus the two halves sit at
# most 6 characters apart; the closest false positive was 21. 14 is above double
# the first and well under the second.
_GAP_LATIN, _GAP_CJK = 60, 14
# `；;` are clause terminators in CJK the way `.` is in English, and a forecast
# does not survive one.
_SENTENCE_END = r".!?\n。！？；;"


def _hedged(hedge: str, outcome: str, latin: bool = True) -> str:
    """A probability word and an outcome close together in ONE sentence."""
    b = r"\b" if latin else ""
    gap = rf"[^{_SENTENCE_END}]{{0,{_GAP_LATIN if latin else _GAP_CJK}}}"
    return (rf"{b}(?:{hedge}){b}{gap}{b}(?:{outcome}){b}"
            rf"|{b}(?:{outcome}){b}{gap}{b}(?:{hedge}){b}")


_HEDGED_FORECAST = "|".join([
    _hedged(_HEDGE_EN, _OUTCOME_EN), _hedged(_HEDGE_ZH, _OUTCOME_ZH, latin=False),
    _hedged(_HEDGE_DE, _OUTCOME_DE), _hedged(_HEDGE_NL, _OUTCOME_NL),
    _hedged(_HEDGE_FR, _OUTCOME_FR), _hedged(_HEDGE_ES, _OUTCOME_ES),
    _hedged(_HEDGE_IT, _OUTCOME_IT), _hedged(_HEDGE_JA, _OUTCOME_JA, latin=False),
    _hedged(_HEDGE_KO, _OUTCOME_KO, latin=False),
])


# ---------------------------------------------------------------------------
# CERTAINTY. The hedges above are words of PROBABILITY, and a forecast does not
# need one. Measured 2026-10-24, all three exit 0 and delivered:
#
#   你肯定能拿到面试，进面基本稳了。
#   You will definitely get an interview. An interview is almost guaranteed.
#   这个岗位你很有希望拿到 offer，十拿九稳。
#
# The certainty words cannot simply join the hedge lists, because the hedge
# lists fire on PROXIMITY to an outcome noun, and certainty words are the most
# common words in interview advice: `面试前一定要准备…`, `肯定的是…`, `you
# should definitely prepare a system-design example`, `面接では必ず志望動機を
# 聞かれます`. Each of those sits a few characters from 面试 / interview / 面接
# and none is a forecast.
#
# So a certainty word fires only when it governs the candidate RECEIVING an
# outcome — the outcome is the object of the verb it modifies (`definitely
# get an interview`, `肯定能拿到面试`, `必ず内定をもらえます`) — or when the
# outcome is the SUBJECT and certainty is its predicate (`an interview is almost
# guaranteed`, `进面基本稳了`, `内定は確実です`). `一定要` / `肯定的是`, a modal of
# NECESSITY (`通過する必要`, `통과해야`), and a negated guarantee (`不一定能`,
# `无法保证`, `not guaranteed an interview`) are left alone: the first two are
# advice, the last is the honest disclaimer.

# The outcome as an English OBJECT. A following noun that turns it into a topic
# of preparation releases it: `interview questions`, `interview format`, `offer
# negotiation` are what the skill is for.
_PREP_TAIL_EN = (r"(?!\s+(?:questions?|prep(?:aration)?|format|process|tips|practice"
                 r"|panel|loop|feedback|negotiations?|logistics|slots?|schedule)\b)")
_OUTCOME_OBJ_EN = (r"(?:an?\s+|the\s+|this\s+|that\s+|your\s+)?"
                   r"(?:(?:job\s+)?offers?|interviews?|callbacks?|call[\s-]backs?"
                   r"|shortlist\s+(?:place|spot)|(?:second|next|final)\s+round|onsite)\b"
                   + _PREP_TAIL_EN)
# `be interviewed` is deliberately absent: in interview prep the candidate
# already HAS the interview, and `you will most likely be interviewed by the
# hiring manager` is the format. `make the cut` is absent because a project
# "making the cut" for the CV is the commoner sentence.
_RECEIVE_EN = (r"(?:get|land|receive|secure|win|earn|snag|be\s+(?:offered|given|sent))\s+"
               + _OUTCOME_OBJ_EN +
               r"|be\s+(?:invited|shortlisted|hired|selected|called\s+back|asked\s+back"
               r"|offered\s+the\s+(?:job|role|position)|moved\s+forward|accepted)\b"
               r"|(?:pass|clear|get\s+(?:through|past)|make\s+it\s+(?:through|past))\s+"
               r"(?:the\s+|this\s+|your\s+)?(?:(?:cv|resume|résumé|initial|first|phone"
               r"|recruiter|hr)\s+)?(?:screen(?:ing)?|first\s+round|shortlisting|interviews?"
               r"|ats(?!\s+(?:pars\w*|checks?|tests?|scans?|format\w*|keywords?)))\b"
               r"|make\s+(?:the\s+)?shortlist\b")
_CERTAIN_EN = (r"definitely|certainly|surely|undoubtedly|absolutely|unquestionably"
               r"|almost\s+certainly|without\s+(?:a\s+)?doubt|no\s+doubt|for\s+sure"
               r"|most\s+likely|very\s+likely|highly\s+likely|probably|likely")
# `not guaranteed an interview`, `no one is guaranteed an interview` are the
# honest disclaimer, not the forecast.
_NOT_NEGATED_EN = (r"(?<!not )(?<!never )(?<!n't )(?<!n’t )(?<!no )"
                   r"(?<!one is )(?<!body is )(?<!one's )(?<!one’s )")
# A short aside between the certainty and the verb it governs does not change
# what it governs. `You will definitely, with this CV, get an interview` exited 0
# (measured 2026-10-24) because the receiving verb had to follow at once. One
# comma-delimited aside of at most 40 characters, or one filler adverb, may sit
# there; a longer gap is a second clause, not the same verb phrase.
_EN_ASIDE = r"(?:\s*,\s*[^,.;:!?]{1,40}?,\s*|\s+)"
_EN_FILLER = (r"(?:(?:also|then|still|soon|easily|quickly|eventually|surely"
              r"|be\s+able\s+to)\s+)?")
_CERTAIN_FORECAST_EN = (
    # will definitely get an interview / are going to definitely be shortlisted /
    # will, with this CV, definitely get an interview
    r"(?:\b(?:will|would)\b|'ll|’ll|\b(?:are|is|am|'re|’re)\s+going\s+to\b)"
    r"(?:\s*,\s*[^,.;:!?]{1,40}?,)?\s*"
    r"(?:" + _CERTAIN_EN + r")" + _EN_ASIDE + _EN_FILLER + r"(?:" + _RECEIVE_EN + r")"
    # definitely will be shortlisted
    r"|\b(?:" + _CERTAIN_EN + r")\s+(?:will|would)\s+(?:" + _RECEIVE_EN + r")"
    # bound / sure / certain / guaranteed to get an interview — but not the
    # imperative `make sure to` / `be sure to`, which is advice.
    r"|(?<!make )(?<!makes )(?<!making )(?<!be )" + _NOT_NEGATED_EN +
    r"\b(?:(?:almost|nearly|virtually|practically)\s+)?"
    r"(?:guaranteed|bound|sure|certain|assured|destined)\s+to\s+"
    r"(?:(?:" + _CERTAIN_EN + r")\s+)?(?:" + _RECEIVE_EN + r")"
    # guaranteed an interview / assured of an offer
    r"|" + _NOT_NEGATED_EN + r"\b(?:(?:almost|nearly|virtually|practically)\s+)?"
    r"(?:guaranteed|assured\s+of)\s+" + _OUTCOME_OBJ_EN +
    # an interview is almost guaranteed / the offer is a done deal. `to` after
    # the predicate is the scheme or the format talking — `an interview is
    # guaranteed to applicants who meet the minimum criteria`, `the interview is
    # certain to include a case study` — so it releases the sentence.
    r"|\b(?:(?:job\s+)?offers?|interviews?|callbacks?|shortlist\s+(?:place|spot))\s+"
    r"(?:is|are|looks|seems|feels|(?:will|would|should)\s+be)\s+"
    r"(?:(?:almost|nearly|virtually|practically|basically|essentially|pretty\s+much"
    r"|all\s+but|more\s+or\s+less|as\s+good\s+as)\s+)?"
    r"(?:guaranteed|assured|certain|a\s+given|a\s+(?:sure|safe)\s+(?:thing|bet)"
    r"|a\s+done\s+deal|a\s+formality|a\s+foregone\s+conclusion|locked\s+in|yours)\b"
    r"(?!\s+to\b)"
    r"|\b(?:job|role|position)\s+is\s+(?:(?:basically|practically|as\s+good\s+as)\s+)?"
    r"yours\b(?!\s+to\b)")

# Chinese. RECEIVE is the outcome as an object. 面试 followed by 官/题/经验/…
# is the interviewer or the material, not the invitation.
_ZH_CLAUSE = r"[^，,。！？；;!?\n]"
_ZH_IV = r"面试(?!官|题|问题|经验|技巧|准备|流程|形式|环节)"
_RECEIVE_ZH = (
    r"(?:拿到|拿下|获得|得到|收到|斩获|争取到|约到)\s*" + _ZH_CLAUSE + r"{0,6}?"
    r"(?:" + _ZH_IV + r"|offer|录用|录取|复试|终面|[一二三四]面|HR\s*面)"
    r"|拿\s*(?:offer|" + _ZH_IV + r")"
    r"|进(?:入|到)?\s*(?:" + _ZH_IV + r"|下一轮|复试|终面|[一二三四]面|候选名单)|进面"
    r"|(?:通过|过)(?:了)?\s*(?:简历(?:筛选|关)|初筛|筛选|笔试|" + _ZH_IV +
    r"|复试|终面|[一二三四]面|HR\s*面|背调|ATS)"
    r"|过筛|过(?=\s*[，,。！？；;!?]|\s*$)"
    r"|被" + _ZH_CLAUSE + r"{0,3}?(?:录用|录取|选中|聘用|约面|邀请(?:参加)?面试)"
    r"|入围|上岸|拿下(?:这个|该)?(?:岗位|职位|offer)")
# 稳 alone is the first half of 稳定; it is a certainty word only directly
# before the verb it guarantees (稳拿 / 稳过 / 稳进). 保证 is absent on purpose:
# its commonest use in an honest report is the disclaimer — 没有任何方法能保证
# 拿到面试 — and the negation sits too far back for a lookbehind to see.
_CERTAIN_ZH = (r"肯定|一定|必然|必定|绝对|铁定|笃定|准保|保准|稳稳(?:地)?|稳(?=[拿过进])"
               r"|毫无疑问|无疑|十拿九稳|板上钉钉|很有希望|大有希望|很有机会|大有机会|有望"
               r"|有很大(?:的)?(?:希望|机会|把握)|有(?:十足|充分)(?:的)?把握")
_ZH_NEGATOR_BEFORE = (r"(?<!不)(?<!未必)(?<!无法)(?<!不能)(?<!难以)(?<!没法)(?<!没有)"
                      r"(?<!并非)(?<!无)(?<!不敢)(?<!不是)")
_ZH_RECEIVED_NOUN = (r"(?:拿到|拿下|获得|收到)\s*" + _ZH_CLAUSE + r"{0,4}?"
                     r"(?:" + _ZH_IV + r"|offer|录用|录取)"
                     r"|offer|录用|录取|入围|进面|上岸|初筛|过筛"
                     r"|通过(?:初筛|筛选|简历筛选|" + _ZH_IV + r")|简历筛选")
# Bare 面试 as the subject takes only the unambiguous certainty predicates:
# `英文面试没问题` says the candidate can handle an English interview, which
# is an assessment of ability, not of the outcome.
_ZH_SURE_PREDICATE = (r"稳了|稳稳的|稳的|没跑了?|跑不了|十拿九稳|板上钉钉|妥了|毫无悬念|有戏"
                      r"|肯定的|必然的|铁定的|胜券在握|指日可待|是你的了|非你莫属|囊中之物"
                      r"|没(?:有|啥|什么)?悬念")
# The same predicates said with a received outcome as the subject, plus the
# understatements that mean "no obstacle" (measured 2026-11-01, both exit 0:
# 以你的背景，进面问题不大 / 这个岗位你稳了). Only after a RECEIVED outcome:
# 排版问题不大 and 英文面试没问题 judge the material and the ability.
_ZH_NO_OBSTACLE = (r"不成问题|没(?:有|啥|什么)?(?:大)?问题|问题不大|不是(?:什么)?问题"
                   r"|不在话下")
# The job itself as the subject (这个岗位你稳了 / 这份offer基本是你的了). Only the
# outcome-only predicates: 这份工作挺稳的 / 国企岗位比较稳 describe job STABILITY,
# so 稳的 / 稳稳的 are absent, and the job noun needs a determiner before it or
# 你/您 after it — 等工作稳了再跳槽 is about settling in, not a forecast.
_ZH_JOB_SURE = (r"稳了|没跑了?|跑不了|十拿九稳|板上钉钉|妥了|毫无悬念|胜券在握|是你的了"
                r"|非你莫属|囊中之物|没(?:有|啥|什么)?悬念|(?:你|您)(?:就)?拿定了")
_ZH_JOB = r"(?:岗位|职位|工作|offer|机会)"
_ZH_DEGREE = r"(?:已经|基本上|基本|应该|肯定|绝对|完全|几乎|算是|就|也)?(?:是)?"
# A denied claim is the honest disclaimer: 不能说进面问题不大 / 这不代表offer稳了.
_ZH_DENIED_BEFORE = (r"(?<!不能说)(?<!不敢说)(?<!很难说)(?<!难说)(?<!不好说)(?<!没法说)"
                     r"(?<!无法说)(?<!不代表)(?<!不等于)(?<!不意味着)(?<!并不是)(?<!不是说)")
_ZH_MEANS = (r"(?:通过|经过|经由|靠着?|凭着?|凭借|借助|依靠|依托|利用|借着?|在|于|趁着?)"
             r"[^，,。！？；;!?\n、]{1,8}?")
_CERTAIN_FORECAST_ZH = (
    # 肯定能拿到面试 / 一定可以顺利通过初筛 / 有望拿到 offer. The outcome verb must
    # follow at once (a pronoun and a modal of ABILITY at most), which is what
    # keeps 一定要… (necessity) and 肯定的是… (assertion) out.
    _ZH_NEGATOR_BEFORE + r"(?:" + _CERTAIN_ZH + r")(?:地)?"
    r"(?:你|您|他|她|也|都|还|就)?(?:能够|能|会|可以|可|将|就能|就会)?"
    r"(?:顺利|直接|轻松|成功)?(?:地)?(?:" + _RECEIVE_ZH + r")"
    # 肯定能通过内推拿到面试 / 一定可以靠这段经历拿到offer: one short phrase of
    # MEANS or time between them, opened by its coverb, still governs the same
    # verb (measured 2026-10-24, both exit 0). Only a coverb opens it, so 一定要准备
    # 好…再去面试 stays necessity; and the outcome may not be a time frame —
    # 肯定会在你拿到offer前做背调 is about the background check.
    r"|" + _ZH_NEGATOR_BEFORE + r"(?:" + _CERTAIN_ZH + r")(?:地)?"
    r"(?:你|您|他|她|也|都|还|就)?(?:能够|能|会|可以|可|将|就能|就会)?" + _ZH_MEANS +
    r"(?:顺利|直接|轻松|成功)?(?:地)?(?:" + _RECEIVE_ZH + r")"
    r"(?!\s*(?:之?前|之?后|以前|以后|的时候|时|再|才))"
    # 进面基本稳了 / 拿到offer是板上钉钉的事 / 录用基本没跑了
    r"|" + _ZH_NEGATOR_BEFORE + _ZH_DENIED_BEFORE + r"(?:" + _ZH_RECEIVED_NOUN + r")\s*(?:的事|这件事|这事)?"
    r"\s*(?:你|您)?" + _ZH_DEGREE +
    r"(?:" + _ZH_SURE_PREDICATE + r"|" + _ZH_NO_OBSTACLE + r")"
    r"|" + _ZH_IV + r"\s*(?:你|您)?" + _ZH_DEGREE +
    r"(?:" + _ZH_SURE_PREDICATE + r")"
    # 这个岗位你稳了 / 这份offer基本是你的了 / 职位你没跑了
    r"|" + _ZH_DENIED_BEFORE + r"(?:这个|这份|这一?个|该|此)\s*" + _ZH_JOB + r"\s*(?:你|您)?" + _ZH_DEGREE +
    r"(?:" + _ZH_JOB_SURE + r")"
    r"|(?<![个份该此])" + _ZH_DENIED_BEFORE + _ZH_JOB + r"\s*(?:你|您)" + _ZH_DEGREE + r"(?:" + _ZH_JOB_SURE + r")"
    # 拿到面试的机会很大 / 进面的希望很大 — a likelihood stated as high. 可能性
    # stays allowed bare: the mandated disclaimer says 不给出…可能性估计.
    r"|(?:" + _ZH_IV + r"|offer|录用|录取|入围|进面|上岸|通过(?:初筛|筛选|面试)"
    r"|拿到(?:面试|offer))\s*(?:的)?(?:机会|希望|把握|可能性?|几率)"
    r"(?:很|非常|相当|极|比较|较)?(?:大|高|不小|不低|很足|十足)")

# Japanese / Korean / Spanish: the same two shapes. A modal of necessity after
# the outcome verb (必要 / なければ / 해야 / 하세요) is advice, not a forecast.
_RECEIVE_JA = (r"(?:面接|内定|採用|合格|選考|書類選考|一次面接|二次面接|最終面接|オファー)"
               r"(?:に|を|が|へ|まで)?(?:呼ばれ|進め|進ん|進む|進み|もらえ|貰え|もら|獲得"
               r"|通過|通り|通る|通れ|受か|招かれ|案内され)"
               r"|採用され|合格(?:でき|する|します|です)")
# Necessity (必要 / なければ) and a negated certainty (とは限らない — "not
# necessarily") both follow the verb in Japanese.
_JA_NECESSITY = (r"(?![^。！？]{0,6}?(?:必要|なければ|べき|ください|ましょう|ように"
                 r"|とは限|わけでは|保証はな|保証され|かどうか))")
_CERTAIN_FORECAST_JA = (
    r"(?:間違いなく|確実に|必ず|きっと|絶対(?:に)?|ほぼ確実に)[^。！？]{0,8}?"
    r"(?:" + _RECEIVE_JA + r")" + _JA_NECESSITY +
    r"|(?:内定|採用|合格|書類通過|選考通過|面接(?:への)?(?:招待|案内))(?:は|が|も)?"
    r"(?:ほぼ|まず|もう)?(?:確実|間違いない|間違いなし)")
_RECEIVE_KO = (r"(?:면접|합격|채용|오퍼|서류(?:\s*전형)?|최종)\s*(?:을|를|에|이|가|은|는)?\s*"
               r"(?:받|붙|통과|합격하|합격할|합격합|채용되|채용될|초대되|초대받|불려)")
_KO_NECESSITY = (r"(?![^.!?。]{0,6}?(?:해야|하려면|하기\s*위해|하세요|하십시오|하도록"
                 r"|하시길|하기를|것은\s*아니|건\s*아니|지\s*않|지는\s*않|는지))")
_CERTAIN_FORECAST_KO = (
    r"(?:확실히|반드시|분명히|분명|틀림없이|무조건|당연히)[^.!?。]{0,10}?"
    r"(?:" + _RECEIVE_KO + r")" + _KO_NECESSITY +
    r"|(?:합격|채용|면접\s*기회|오퍼|서류\s*통과)\s*(?:은|는|이|가)?\s*(?:거의\s*)?"
    r"(?:확실(?!하지\s*않|치\s*않|하지\s*못)|따\s*놓은\s*당상|틀림없)")

# The question release never covers an outcome clause that comes FIRST in the
# same sentence. `面接に呼ばれて志望動機を聞かれる可能性が高いです` exited 0
# (measured 2026-10-24): 可能性が高い sat right after 聞かれる, so the release
# took it as a question's likelihood, while the te-chain puts 面接に呼ばれ — the
# invitation — under the same predicate. Korean chains the same way
# (`면접에 초대되어 경력을 질문받을 가능성이 높습니다`), and an adverb placed after
# the chain (`面接に呼ばれ、おそらく…聞かれます`) borrows the release the same way.
# A CONDITIONAL outcome is preparation, not a forecast — `面接に進んだ場合、…聞かれ
# る可能性が高い`, `면접에 초대되면 …질문받을 가능성이 높습니다` — and so is one
# framed by before/after (前 / 後 / 전 / 후).
_JA_CONDITIONAL = (r"(?![^。！？、\n]{0,5}?(?:たら|だら|[めれえけてねげせべ]ば|ば[、,]|なら|場合|際"
                   r"|時|とき|前|後|あと|ても|でも))")
_KO_CONDITIONAL = (r"(?![^.!?,。\n]{0,4}?(?:면(?!접)|경우|때|후|뒤|전|더라도))")
_RECEIVED_THEN_LIKELY = (
    r"(?:" + _RECEIVE_JA + r")" + _JA_CONDITIONAL + r"[^。！？\n]{0,20}?"
    r"(?:(?:可能性|見込み)が[^。！？]{0,10}高い|おそらく|恐らく|十中八九|まず間違いなく|ほぼ確実)"
    r"|(?:" + _RECEIVE_KO + r")" + _KO_CONDITIONAL + r"[^.!?。\n]{0,20}?"
    r"(?:가능성이\s*[^.!?]{0,10}?(?:높|큽)|아마|십중팔구|거의 확실|틀림없이)")
_RECEIVE_ES = (r"(?:conseguir|obtener|recibir|lograr)\w*\s+(?:una?\s+|la\s+|el\s+)?"
               r"(?:entrevista|oferta|plaza|puesto)\b"
               r"|\b(?:te|le|les|os)\s+(?:llam(?:ar[aá]n?|en|an)|invit(?:ar[aá]n?|en|an)"
               r"|contrat(?:ar[aá]n?|en|an)|seleccion(?:ar[aá]n?|en|an)|ofrec(?:er[aá]n?|en)"
               r"|ofrezcan|entrevist(?:ar[aá]n?|en|an))\b"
               r"|\bpasar\w*\s+(?:el|la|los|las)\s+(?:filtro|criba|entrevista|selecci[oó]n"
               r"|primera\s+ronda)")
_CERTAIN_FORECAST_ES = (
    # `no es seguro que te llamen` is the disclaimer.
    r"(?<!no es )(?<!no está )(?<!nada )"
    r"\b(?:sin\s+(?:ninguna\s+)?duda|definitivamente|seguro\s+que|seguramente"
    r"|con\s+(?:toda\s+)?seguridad|ciertamente|de\s+seguro)\b[^.!?]{0,30}?"
    r"(?:" + _RECEIVE_ES + r")"
    r"|\b(?:entrevista|oferta|plaza|puesto)\s+(?:est[aá]|queda)\s+"
    r"(?:(?:pr[aá]cticamente|casi)\s+)?(?:garantizad[oa]|asegurad[oa])\b"
    r"|\b(?:tienes|tendr[aá]s)\s+(?:la|una|el)\s+(?:entrevista|oferta|plaza|puesto)\s+"
    r"(?:(?:pr[aá]cticamente|casi)\s+)?(?:garantizad[oa]|asegurad[oa])\b")

# German, Dutch, French, Italian: the same two shapes, which these four lacked
# while their hedge tables existed. Measured 2026-10-24, exit 0: `Sie bekommen
# sicher ein Interview`, `vous aurez certainement un entretien`, `Je krijgt
# gegarandeerd een gesprek`, `Avrai di sicuro un colloquio`. `sicher`,
# `certainement`, `gegarandeerd` and `di sicuro` are in no hedge list, and must
# not be: `Das Interview ist sicher anspruchsvoll` and `vous aurez certainement
# des questions techniques` are the format and the prep. So the certainty word
# fires only next to a verb of RECEIVING whose object is the outcome — or as the
# outcome's own predicate, closing the clause (`die Zusage ist Ihnen sicher.`).
_CLAUSE_END = r"(?=\s*[.!?,;:]|\s*$)"


def _then_outcome(articled: str, received: str, means: str) -> str:
    """After the certainty word: one comma-delimited aside or one short phrase of
    means or time, then the outcome — `sicher über Ihr Netzwerk ein Interview`,
    `certainement, grâce à ce CV, un entretien` exited 0 (measured 2026-10-24)
    because the outcome had to follow at once. Here the outcome must carry its
    determiner and the phrase may not contain it, so a preposition's own object
    cannot pose as what is received: `nach dem Interview eine Rückmeldung`."""
    words = r"(?:(?!(?:l['’]|d['’])?(?:" + received + r")\b)[^\s,.;:!?]+\s+){1,3}?"
    return (r"(?:\s*,\s*[^,.;:!?]{1,40}?,\s*|\s+(?:" + means + r")\s+" + words + r")"
            + articled)


_CERTAIN_DE = (r"sicher|sicherlich|bestimmt|garantiert|zweifellos|definitiv|gewiss"
               r"|ganz\s+sicher|mit\s+sicherheit|ohne\s+zweifel|auf\s+jeden\s+fall|todsicher")
_RECEIVED_DE = (r"einladung|vorstellungsgespr[aä]ch|interview|zusage|jobangebot"
               r"|stellenangebot|angebot|zweitgespr[aä]ch")
_OUTCOME_OBJ_DE = (r"(?:(?:ein|eine|einen|die|das|den|der|ihre|ihr|deine|dein)\s+)?"
                   r"(?:" + _RECEIVED_DE + r")\b")
_RECEIVE_VERB_DE = r"bekommen|bekommst|bekommt|erhalten|erh[aä]ltst|erh[aä]lt|kriegen|kriegst|kriegt"
_NOT_NEGATED_DE = r"(?<!nicht )(?<!kein )(?<!keine )(?<!nie )(?<!niemals )"
_CERTAIN_FORECAST_DE = (
    # Sie bekommen sicher ein Interview
    r"\b(?:" + _RECEIVE_VERB_DE + r")\s+(?:(?:sie|du|ihr)\s+)?(?:" + _CERTAIN_DE + r")"
    r"(?:\s+" + _OUTCOME_OBJ_DE + r"|" + _then_outcome(
        r"(?:ein|eine|einen|die|das|den|ihre|ihr|deine|dein)\s+(?:" + _RECEIVED_DE + r")\b",
        _RECEIVED_DE, r"über|durch|dank|mit|wegen|aufgrund|nach|innerhalb|binnen|bis") + r")" +
    # Sie werden sicher eine Zusage bekommen
    r"|" + _NOT_NEGATED_DE + r"\b(?:" + _CERTAIN_DE + r")\s+" + _OUTCOME_OBJ_DE
    + r"\s+(?:" + _RECEIVE_VERB_DE + r")\b"
    # Sie werden bestimmt (zum Vorstellungsgespräch) eingeladen
    r"|" + _NOT_NEGATED_DE + r"\b(?:" + _CERTAIN_DE + r")\s+(?:(?:zum|zu\s+einem)\s+"
    r"(?:vorstellungsgespr[aä]ch|gespr[aä]ch|interview)\s+)?(?:eingeladen|eingestellt)\b"
    # Die Zusage ist Ihnen sicher. / Ein Interview ist so gut wie garantiert.
    r"|\b(?:" + _RECEIVED_DE + r")\s+(?:ist|sind)\s+(?:(?:ihnen|dir|euch)\s+)?"
    r"(?:(?:so\s+gut\s+wie|praktisch|quasi|fast)\s+)?(?:sicher|garantiert|gewiss)\b"
    + _CLAUSE_END)
_CERTAIN_NL = (r"zeker|gegarandeerd|ongetwijfeld|beslist|absoluut|stellig|sowieso"
               r"|vast\s+en\s+zeker|zeker\s+weten|met\s+zekerheid")
_RECEIVED_NL = r"sollicitatiegesprek|gesprek|uitnodiging|baanaanbod|aanbod|interview|contract"
_OUTCOME_OBJ_NL = r"(?:(?:een|het|de|je|jouw|uw|een\s+tweede)\s+)?(?:" + _RECEIVED_NL + r")\b"
_RECEIVE_VERB_NL = r"krijgt|krijg|krijgen|ontvangt|ontvang|ontvangen"
_NOT_NEGATED_NL = r"(?<!niet )(?<!geen )(?<!nooit )"
_CERTAIN_FORECAST_NL = (
    r"\b(?:" + _RECEIVE_VERB_NL + r")\s+(?:(?:je|u|jij|jullie)\s+)?(?:" + _CERTAIN_NL
    + r")(?:\s+" + _OUTCOME_OBJ_NL + r"|" + _then_outcome(
        r"(?:een|het|de|je|jouw|uw)\s+(?:tweede\s+)?(?:" + _RECEIVED_NL + r")\b",
        _RECEIVED_NL, r"via|met|door|dankzij|na|binnen|vanwege") + r")" +
    r"|" + _NOT_NEGATED_NL + r"\b(?:" + _CERTAIN_NL + r")\s+" + _OUTCOME_OBJ_NL
    + r"\s+(?:" + _RECEIVE_VERB_NL + r")\b"
    r"|" + _NOT_NEGATED_NL + r"\b(?:" + _CERTAIN_NL + r")\s+(?:(?:voor\s+(?:een|het)\s+"
    r"(?:sollicitatiegesprek|gesprek|interview))\s+)?(?:uitgenodigd|aangenomen)\b"
    r"|\b(?:" + _RECEIVED_NL + r")\s+(?:is|lijkt)\s+(?:(?:zo\s+goed\s+als|vrijwel|praktisch"
    r"|bijna)\s+)?(?:zeker|gegarandeerd|binnen)\b" + _CLAUSE_END)
_CERTAIN_FR = (r"certainement|s[uû]rement|assur[ée]ment|forc[ée]ment|ind[ée]niablement"
               r"|d[ée]finitivement|sans\s+(?:aucun\s+)?doute|[aà]\s+coup\s+s[uû]r")
_RECEIVED_FR = r"entretien|offre|proposition|convocation|embauche"
# French and Italian put the adjective after the noun, and an interview named by
# its FORMAT is the process, not the outcome: `vous aurez certainement un
# entretien technique avec l'équipe`. Same role as _PREP_TAIL_EN.
_FORMAT_TAIL_FR = (r"(?!\s+(?:technique|t[ée]l[ée]phonique|vid[ée]o|rh|avec|en\s+anglais"
                   r"|de\s+motivation|comportemental|individuel|collectif)\b)")
_OUTCOME_OBJ_FR = (r"(?:(?:un|une|le|la|votre|ton|ta|cet|cette)\s+|l['’])?"
                   r"(?:" + _RECEIVED_FR + r")\b" + _FORMAT_TAIL_FR)
_RECEIVE_VERB_FR = (r"aurez|auras|aura|obtiendrez|obtiendras|obtiendra|recevrez|recevras"
                    r"|recevra|d[ée]crocherez|d[ée]crocheras|d[ée]crochera")
_NOT_NEGATED_FR = r"(?<!pas )(?<!jamais )(?<!non )"
_CERTAIN_FORECAST_FR = (
    # vous aurez certainement un entretien
    r"\b(?:" + _RECEIVE_VERB_FR + r")\s+(?:" + _CERTAIN_FR + r")(?:\s+" + _OUTCOME_OBJ_FR
    + r"|" + _then_outcome(
        r"(?:(?:un|une|le|la|votre|ton|ta|cet|cette)\s+|l['’])(?:" + _RECEIVED_FR + r")\b"
        + _FORMAT_TAIL_FR, _RECEIVED_FR,
        r"gr[aâ]ce\s+[àa]|avec|par|via|apr[eè]s|d[eè]s|d['’]ici|sous") + r")" +
    # vous allez certainement décrocher un entretien
    r"|" + _NOT_NEGATED_FR + r"\b(?:" + _CERTAIN_FR + r")\s+(?:avoir|obtenir|recevoir"
    r"|d[ée]crocher)\s+" + _OUTCOME_OBJ_FR +
    # vous serez certainement convoqué / retenu
    r"|\b(?:serez|seras|sera)\s+(?:" + _CERTAIN_FR + r")\s+(?:convoqu[ée]|retenu|embauch[ée]"
    r"|recrut[ée]|s[ée]lectionn[ée])"
    # l'entretien est quasiment assuré.
    r"|\b(?:" + _RECEIVED_FR + r")\s+est\s+(?:(?:quasiment|presque|pratiquement)\s+)?"
    r"(?:assur[ée]e?|garantie?|acquise?|dans\s+la\s+poche)" + _CLAUSE_END)
_CERTAIN_IT = (r"sicuramente|certamente|indubbiamente|di\s+sicuro|di\s+certo|senz['’]altro"
               r"|senza\s+(?:alcun\s+)?dubbio")
_RECEIVED_IT = r"colloquio|offerta|proposta|assunzione|convocazione"
_FORMAT_TAIL_IT = (r"(?!\s+(?:tecnico|telefonico|conoscitivo|con|in\s+inglese"
                   r"|motivazionale|di\s+gruppo|individuale)\b)")
_OUTCOME_OBJ_IT = (r"(?:(?:un|una|il|lo|la)\s+|un['’]|l['’])?(?:" + _RECEIVED_IT + r")\b"
                   + _FORMAT_TAIL_IT)
_RECEIVE_VERB_IT = (r"otterrai|otterr[aà]|otterrete|avrai|avr[aà]|avrete|riceverai"
                    r"|ricever[aà]|riceverete")
_CERTAIN_FORECAST_IT = (
    # otterrai sicuramente un colloquio / avrai di sicuro un colloquio
    r"\b(?:" + _RECEIVE_VERB_IT + r")\s+(?:" + _CERTAIN_IT + r")(?:\s+" + _OUTCOME_OBJ_IT
    + r"|" + _then_outcome(
        r"(?:(?:un|una|il|lo|la)\s+|un['’]|l['’])(?:" + _RECEIVED_IT + r")\b" + _FORMAT_TAIL_IT,
        _RECEIVED_IT, r"grazie\s+a(?:l|lla|i|gli|lle)?|con|tramite|attraverso|dopo|entro|in")
    + r")" +
    # sicuramente otterrai un colloquio
    r"|(?<!non )\b(?:" + _CERTAIN_IT + r")\s+(?:" + _RECEIVE_VERB_IT
    + r"|ottenere|avere|ricevere)\s+" + _OUTCOME_OBJ_IT +
    # sarai sicuramente chiamato / convocato
    r"|\b(?:sarai|sar[aà]|sarete)\s+(?:" + _CERTAIN_IT + r")\s+(?:chiamat|convocat"
    r"|selezionat|assunt)[oaie]\b"
    # il colloquio è praticamente garantito.
    r"|\b(?:colloquio|offerta|assunzione)\s+[eè]\s+(?:(?:praticamente|quasi|ormai)\s+)?"
    r"(?:garantit[oa]|assicurat[oa]|sicur[oa]|cosa\s+fatta)" + _CLAUSE_END)
_CERTAIN_FORECAST = "|".join([_CERTAIN_FORECAST_EN, _CERTAIN_FORECAST_ZH,
                              _CERTAIN_FORECAST_JA, _CERTAIN_FORECAST_KO,
                              _CERTAIN_FORECAST_ES, _CERTAIN_FORECAST_DE,
                              _CERTAIN_FORECAST_NL, _CERTAIN_FORECAST_FR,
                              _CERTAIN_FORECAST_IT])

# A NEGATED certainty is the honest disclaimer, but its negator sits too far back
# for a lookbehind: `没人能肯定你会拿到面试`, `谁也不能保证你一定能拿到面试` and
# `No one can say for certain that you will get an interview` all fired on the
# outcome clause. Masked like a refusal (mask_exempt_spans): a negated subject or
# modal, a verb of asserting, and the outcome clause it denies — ending ON the
# outcome, so anything after it is still scanned, and no number fits inside.
# `谁也不能否认你肯定能拿到面试` / `No one can deny that you will get an interview`
# assert the outcome and are not covered: deny is not a verb of asserting.
_NEGATED_CERTAINTY_ZH = re.compile(
    r"(?:(?:没人|没有人|无人|没有谁|谁也|谁都|任何人都|没有任何(?:人|方法|工具|办法))"
    r"(?:不|没)?(?:能够|能|可以|敢)?|不能|无法|没法|没办法|不敢|难以|不可能)"
    r"\s*(?:肯定|确定|保证|担保|断定|断言|预测|打包票|说准|确保)(?:地)?(?:说)?\s*"
    r"(?:你|您|他|她|候选人)?(?:也|都|就)?"
    r"(?:" + _CERTAIN_ZH + r")?(?:地)?(?:能够|能|会|可以|可|将|就能|就会)?"
    r"(?:顺利|直接|轻松|成功)?(?:地)?(?:" + _RECEIVE_ZH + r")")
_NEGATED_FORECAST_EN = re.compile(
    r"\b(?:(?:no\s*one|no-one|nobody|nothing|no\s+(?:recruiter|tool|model|test|score))\s+"
    r"(?:(?:can|could|will|would|is\s+able\s+to)\s+)?"
    r"|(?:i|we|this\s+(?:report|skill|tool|assessment))\s+" + _NEGATED_EN + r"\s+"
    r"|(?:it\s+is|it's|it’s)\s+(?:impossible|not\s+possible)\s+to\s+"
    r"|there\s+is\s+no\s+way\s+to\s+)"
    r"(?:say|tell|know|knows|guarantee|guarantees|promise|promises|predict|predicts"
    r"|determine|confirm|be\s+(?:sure|certain))(?:\s+(?:you|them|him|her|anyone))?"
    r"(?:\s+(?:for\s+(?:certain|sure)|with\s+(?:certainty|confidence)|in\s+advance))?"
    r"(?:\s+(?:that|whether|if))?\s+(?:you|the\s+candidate|they|he|she)"
    r"(?:\s+(?:will|would|are\s+going\s+to)|'ll|’ll)?(?:\s+(?:" + _CERTAIN_EN + r"))?\s+"
    r"(?:(?:get|land|receive|secure)\s+(?:an?\s+|the\s+)?(?:interview|offer|job|role"
    r"|position)\b|" + _RECEIVE_EN + r")", re.IGNORECASE)

# The probability NOUNS, minus the subject that shares their name. `probability
# and statistics`, `maximum likelihood estimation`, `odds ratio` are posting
# requirements and statistics vocabulary; a report quoting the posting it
# assesses blocked delivery on them. Each exemption names the subject right next
# to the word, so `the probability of an interview` and `your odds` still fire.
_EN_PROBABILITY_NOUNS = (
    r"|(?<!statistics and )(?<!statistics & )(?<!theory of )(?<!conditional )"
    r"(?<!joint )(?<!marginal )(?<!posterior )(?<!prior )(?<!bayesian )"
    r"\bprobabilit(?:y|ies)\b"
    r"(?!\s+(?:theory|and\s+(?:mathematical\s+)?statistics|&\s+statistics"
    r"|and\s+stochastic|distributions?|densit(?:y|ies)|mass\s+functions?"
    r"|models?|modell?ing|spaces?|measures?|calibration)\b)"
    r"|(?<!\blog[- ])(?<!\bat )\bodds\b(?!\s+ratios?\b)"
    r"|(?<!maximum )(?<!log-)(?<!log )(?<!marginal )(?<!partial )(?<!quasi-)"
    r"(?<!profile )(?<!pseudo-)(?<!empirical )"
    r"\blikelihood\b(?!\s*(?:ratios?|functions?|estimat(?:es?|ion|ors?)|principle"
    r"|equations?|maximi[sz]ation|-based|based|surfaces?|models?)\b)")

_WORDS = re.compile(
    # `chances?` used to be bare. That was tolerable while this file only ever
    # read English — and it stopped being tolerable when the skill started
    # writing German assessments, because `Chance` is spelled identically and
    # this pattern is case-insensitive. `Wir bieten dir die Chance, in diesem
    # Job viel zu lernen` fired as an English prediction word. So did every
    # honest English `a chance to work with…`.
    #
    # It now needs a possessive or an outcome, which is what makes it a claim
    # about THIS candidate rather than a word for opportunity in either language.
    r"\b(?:your|their|his|her|our|my|the candidate'?s?)\s+chances?\b"
    r"|\bchances?\s+(?:of|at|for)\s+(?:an?\s+|the\s+)?"
    r"(?:interview|offer|job|role|position|success|being|getting|landing|"
    r"a\s+callback|progressing)"
    r"|\bchances?\s+(?:are|is|were|seem|look|looked)\b"
    + _EN_PROBABILITY_NOUNS +
    r"|\blikely to be (?:hired|interviewed|shortlisted|rejected)\b"
    r"|\b(?:strong|weak) candidate\b|\bwould pass\b|\bno-hire\b"
    r"|\b\d+(?:\.\d+)?\s*(?:percent|per cent)\b"
    r"|\bout of (?:10|100)\b"
    # Forecasts that name no number. The ban is on PREDICTING the outcome, and a
    # verification pass found the numberless English forms sailing through while
    # their Chinese analogues fired — the gate enforced in one language only.
    r"|\bshoo-?in\b|\ba lock\b|\bin the bag\b"
    r"|(?:\b(?:will|would|should)\b|'ll|’ll)\s*(?:almost certainly\s+|certainly\s+|surely\s+|"
    r"probably\s+|likely\s+)?(?:get|land|receive|secure)\s+(?:an?\s+|the\s+)?"
    r"(?:interview|offer|job|role|position)\b" + _PREP_TAIL_EN +
    # `Expect the interview to cover caching` is the format, not the outcome.
    r"|\bexpect\s+(?:an?\s+|the\s+)?(?:interview|offer)\b" + _PREP_TAIL_EN +
    r"(?!\s+to\s+(?:cover|include|focus|involve|feature|probe|test|start|open|begin"
    r"|last|take|run|consist|be\s+(?:held|run|conducted|virtual|remote|online"
    r"|technical|structured|in\s+person|a\s+panel))\b)"
    r"|\byou'?re? (?:a )?(?:strong|weak|clear|obvious) (?:fit|match|candidate)\b"
    # 確率 is the Japanese/traditional spelling of 概率.
    r"|" + _JA_PROB +
    r"|" + _ZH_RATE + r"|" + _ZH_TENTHS + r"|" + _ZH_PERCENT_SPELLED
    + r"|" + _FORECAST_DE + r"|" + _FORECAST_NL + r"|" + _FORECAST_FR
    + r"|" + _FORECAST_ES_IT + r"|" + _FORECAST_JA + r"|" + _FORECAST_KO
    + r"|" + _JA_TENTHS
    + r"|" + _HEDGED_FORECAST
    + r"|" + _CERTAIN_FORECAST
    + r"|" + _RECEIVED_THEN_LIKELY,
    re.IGNORECASE)
_ATTRIBUTION = re.compile(r"^\s*>?\s*(?:—|--|-|Source:|来源[:：])\s+.*https?://\S+")


# ---------------------------------------------------------------------------
# Score NOUNS. The two bans above catch the SYMBOLS -- `%` and `n/m` -- and an
# audit on 2026-09-05 measured what that leaves through, on the invariant this
# whole file exists for: `匹配度 85 分`, `overall score: 85`, `rated 8.5`,
# `4.5 stars`, `confidence: 0.85`, `grade: B+`, `Bewertung 8` all shipped
# silently. Collapsing evidence into a number needs a weight for a partial match
# and any weight would be invented -- that is true whichever word carries the
# number, so the ban has to be on the concept and not on the punctuation.
#
# Covering the languages this skill renders CVs in (en/de/nl/fr/es/it/zh/ja/ko),
# because banning it in English and Chinese only is the defect one level up.
#
# NOT included, deliberately: a bare `85 points`. `points` is ordinary prose --
# references/motivation-letter.md really does say "3 points" -- and this repo
# treats a gate that fires on correct output as the worse failure. A stated hole
# beats a cry-wolf.
_SCORE_NOUN_LATIN = (r"scores?|scored|scoring|ratings?|rated|graded|"
                     r"bewertung|punktzahl|beoordeling|cijfer|"
                     r"puntuaci[o\u00f3]n|punteggio|valutazione")
# `note` (fr) and `mark` (en) are left out on purpose: both are high-frequency
# ordinary words, and a French grade written `15/20` is already _SCORE's.
_SCORE_NOUN_CJK = (r"匹配度|契合度|吻合度|评分|評分|打分|得分|分数|分數|总分|總分|"
                   r"综合分|綜合分|评级|評級|等级|等級|評価|点数|點數|점수|평점|평가")

# WHERE each half applies. D2 bans the skill from scoring THIS CANDIDATE'S FIT;
# it does not ban the candidate's own past, measured results — which is exactly
# why cv.md and letter.md were excluded from this lint from the start.
#
# `mock/cheatsheet.md` and `mock/answer-guide.md` are the same kind of file: the
# candidate's own material, to be said out loud. A cheatsheet reminding someone
# they "scored 92 on the HackerRank test last year" or that a repo "received 500
# stars" is honest sourced history, and banning it there was a cry-wolf found on
# 2026-09-05. The judgement-facing artifacts — where the skill itself writes the
# number — keep the full ban.
#
# The FIT nouns stay banned everywhere, including on the candidate's own pages:
# 匹配度/契合度 and `fit score`/`match score`/`confidence` are about this
# application and can only be invented, wherever they are written.
_JUDGEMENT_SURFACES = ("report.md", "fit-assessment.md", "shortlist.md", "assessment-")
_FIT_NOUN = re.compile(
    r"(?:匹配度|契合度|吻合度)\s*[:：为是]?\s*"
    r"(?<![0-9０-９.．\-\u2013])[0-9０-９]+(?:[.．][0-9０-９]+)?"
    r"|\b(?:fit|match|compatibility)\s+(?:score|rating)\b\s*(?:of|:|=|is)?\s*"
    r"(?<![0-9.\-\u2013])[0-9]+(?:\.[0-9]+)?\b",
    re.I)


def _is_judgement_surface(label: str) -> bool:
    name = str(label or "").replace("\\", "/").split("/")[-1]
    return any(mark in name for mark in _JUDGEMENT_SURFACES)


_SCORE_NOUN = re.compile(
    r"\b(?:" + _SCORE_NOUN_LATIN + r")\b\s*(?:of|:|=|is|at|von|van|di)?\s*"
    r"(?<![0-9.\-\u2013])[0-9]+(?:\.[0-9]+)?\b(?![/／])"
    r"|(?:" + _SCORE_NOUN_CJK + r")\s*[:：为是]?\s*"
    r"(?<![0-9０-９.．\-\u2013])[0-9０-９]+(?:[.．][0-9０-９]+)?(?![/／])",
    re.I)
# The `(?![/／])` tail hands `score 8/11` back to _SCORE, which already owns the
# n/m shape. One defect, one finding: reporting the same span twice is how a
# reader learns to skim the finding list.

# A confidence expressed as a fraction of one is the same claim wearing a decimal.
_SCORE_DECIMAL = re.compile(
    r"\b(?:score|rating|fit|match|confidence|probability)\b\s*(?:of|:|=|is)?\s*"
    r"0?\.[0-9]+\b", re.I)

# Units that ARE a scale on their own.
_SCORE_UNITS = re.compile(r"\b[0-9]+(?:\.[0-9]+)?\s*(?:stars?|pts)\b", re.I)

# Letter scales. SKILL.md names `B+` in the same breath as `7/10` and "score: 82".
# The noun is required so an ordinary capital letter cannot trip it.
_SCORE_LETTER = re.compile(
    r"(?:\bgrade\b|\brating\b|评级|評級|等级|等級)\s*[:：=]?\s*"
    r"[A-F][+\-]?(?![A-Za-z0-9])", re.I)

# The bare unit form: 85 分 / 85점. The exclusion lists are what keep this off
# ordinary Chinese -- 分钟, 分析, 分类, 分级 ... and Korean 점심 (lunch). 点 is
# NOT given a bare form: 下午 3 点 is a clock time, so Japanese 点数 has to carry
# its noun above.
_SCORE_BARE = re.compile(
    r"(?<![0-9０-９.．\-\u2013])[0-9０-９]+(?:[.．][0-9０-９]+)?"
    r"\s*(?:分(?![钟鐘析部类類布支别別配享散开開成级級秒钱錢手"
    r"公司行店销銷工区區层層队隊会會段期割母子])|점(?!심))")


# Everywhere this lint runs.
# Codes whose finding is about a NUMBER, so the captured-number exemption
# is the relevant escape. PREDICTION_WORD is not here: no quotation makes
# a forecast acceptable.
_NUMBER_CODES = {"PERCENT", "SCORE_PATTERN", "SCORE_NOUN", "SCORE_DECIMAL"}

CHECKS = (("PERCENT", _PERCENT), ("SCORE_PATTERN", _SCORE),
          ("PREDICTION_WORD", _WORDS),
          ("SCORE_NOUN", _FIT_NOUN))
# Only where the skill itself is producing the number. See _JUDGEMENT_SURFACES.
JUDGEMENT_CHECKS = (("SCORE_NOUN", _SCORE_NOUN), ("SCORE_NOUN", _SCORE_DECIMAL),
                    ("SCORE_NOUN", _SCORE_UNITS), ("SCORE_NOUN", _SCORE_LETTER),
                    ("SCORE_NOUN", _SCORE_BARE))


_WS = re.compile(r"\s+")
# Only tokens that could carry an invented NUMBER are eligible for the capture
# masking. A prediction WORD that happens to sit in the posting is still the
# model's to justify -- verbatim quotation has the blockquote allowlist for that.
_NUMERIC_TOKEN = re.compile(r"[0-9\uff10-\uff19%\uff05]")


def _normalise(text: str) -> str:
    return _WS.sub(" ", str(text)).casefold()


def _json_strings(node, out: list) -> None:
    if isinstance(node, str):
        out.append(node)
    elif isinstance(node, dict):
        for value in node.values():
            _json_strings(value, out)
    elif isinstance(node, list):
        for value in node:
            _json_strings(value, out)


def journaled_captures(workspace: pathlib.Path) -> list:
    """The raw files an `adapter_call` record names, and nothing else.

    `stdout_file` is stored workspace-relative by the wrapper. A path that escapes
    the workspace is dropped rather than followed: a journal is data, and a data
    file that can name `/etc/passwd` as a capture is a traversal, not a corpus.
    """
    root = workspace.resolve()
    out, seen = [], set()
    for record in journal._records(workspace):
        if record.get("action") == "browser_call":
            from record_browser_capture import validate_record
            if validate_record(record, workspace) or record.get("classification") != "ok":
                continue
            named = record.get("snapshot_file")
        elif record.get("action") == "adapter_call":
            named = record.get("stdout_file")
        else:
            continue
        if not named:
            continue
        path = (workspace / str(named)).resolve()
        try:
            path.relative_to(root)
        except ValueError:
            continue
        if path.is_file() and path not in seen:
            seen.add(path)
            out.append(path)
    return sorted(out)


def master_profile_strings(workspace: pathlib.Path) -> list:
    """The candidate's master profile, as bound at apply-mode entry. Else [].

    Apply mode never builds evidence-blocks.json, so before this the candidate's
    own CV was never a trusted source there: a report quoting `Reduced p99 latency
    by 40% for the ranking service` word for word from the master was refused at
    delivery, and the cheapest way past it was to delete a true number.

    `check_claims.py --record` writes master-fingerprint.json at apply entry —
    the master's path and sha256 — and the claim gate already treats that file
    as the candidate's source of truth. The same binding is honoured here, on
    the same terms as the evidence CV: the bytes on disk must still hash to the
    recorded value, and only numbers quoted WITH their captured neighbours are
    masked (mask_copied_numbers is unchanged).

    Three narrowings, each closing an off switch:

    * The master must lie OUTSIDE the workspace. It always does
      (`<profile_dir>/profile.yaml` vs `<profile_dir>/applications/<slug>/`), and
      a fingerprint naming report.md or tailored-profile.yaml would let the text
      under scan authorise its own numbers.
    * Leaves are PARSED from the YAML, never read as raw text. A comment is not
      a fact about the candidate — check_claims learned that from a `PhD` that
      existed only in a YAML comment.
    * Hash and parse read the SAME bytes, so a file swapped between the two
      reads cannot be trusted on the strength of the original's hash.

    Anything unreadable returns [] — this only ever REMOVES findings, so a short
    corpus fails closed.
    """
    try:
        record = json.loads((workspace / MASTER_FINGERPRINT).read_text(encoding="utf-8"))
        expected = record["sha256"]
        master = pathlib.Path(record["path"])
        if not isinstance(expected, str):
            return []
        root = workspace.resolve()
        master = (master if master.is_absolute() else workspace / master).resolve()
        if master == root or root in master.parents:
            return []
        data = master.read_bytes()
        if hashlib.sha256(data).hexdigest() != expected:
            return []
        profile = yaml.safe_load(data.decode("utf-8"))
    except (OSError, ValueError, KeyError, TypeError, RuntimeError, yaml.YAMLError):
        return []
    out: list[str] = []
    _json_strings(profile, out)
    return out


# What a run WRITES for a reader, which therefore cannot also be the candidate's
# CV. evidence_blocks.py's default source is `<ws>/cv-source.txt`, so unlike the
# master profile the evidence CV may live inside the workspace — but never as one
# of these, or the text under scan authorises its own numbers: report.md bound as
# "the CV" exited 0 on any figure it contained.
_DELIVERABLE_SUFFIXES = frozenset((".md", ".markdown", ".pdf", ".docx", ".html", ".htm",
                                   ".tex", ".yaml", ".yml", ".json", ".jsonl"))
# User-supplied originals, the same two folders check_apply accepts as an
# original input. `raw/` is not among them: an unjournaled raw file is a note.
_ORIGINAL_INPUT_DIRS = ("inputs", "source")


def _authored_by_the_run(workspace: pathlib.Path, path: pathlib.Path,
                         scanned=()) -> bool:
    """Is `path` (resolved) a file under scan, or a deliverable/artifact the run
    itself writes inside this workspace? Either one is refused as a CV source."""
    if path in {pathlib.Path(p).resolve() for p in scanned}:
        return True
    if path in {p.resolve() for p in target_files(workspace)}:
        return True
    root = workspace.resolve()
    if path == root:
        return True
    try:
        relative = path.relative_to(root)
    except ValueError:
        return False
    if relative.parts[0] in _ORIGINAL_INPUT_DIRS:
        return False
    return (relative.parts[0] == "mock" or relative.name.startswith("judge-")
            or relative.suffix.lower() in _DELIVERABLE_SUFFIXES)


def evidence_cv_text(workspace: pathlib.Path, scanned=()) -> str:
    """The CV evidence-blocks.json binds, or "" — on the master profile's terms.

    The bytes must still hash to the recorded value, and hash and decode read the
    SAME bytes. The path must not be a file under scan or one the run authors
    (`_authored_by_the_run`); a symlink is judged by what it points at.
    """
    try:
        record = json.loads((workspace / "evidence-blocks.json").read_text(
            encoding="utf-8"))["sources"]["cv"]
        expected = record["sha256"]
        if not isinstance(expected, str) or not isinstance(record["path"], str):
            return ""
        cv = pathlib.Path(record["path"])
        cv = (cv if cv.is_absolute() else workspace / cv).resolve()
        if _authored_by_the_run(workspace, cv, scanned):
            return ""
        data = cv.read_bytes()
        if hashlib.sha256(data).hexdigest() != expected:
            return ""
        return data.decode("utf-8")
    except (OSError, ValueError, KeyError, TypeError, RuntimeError):
        return ""


def capture_corpus(workspace: pathlib.Path, scanned=()) -> str:
    """Everything this round actually CAPTURED, normalised for membership tests.

    Only true captures go in: `raw/*.json` as written by the adapter wrapper, and
    the fetched `posting-source.txt`. Artifacts the model authors -- shortlist.yaml,
    the rendered markdown -- are deliberately excluded. A corpus the model can write
    is a corpus the model can use to authorise its own invented number, which would
    turn this masking into an off switch.

    A raw file only counts if the journal says an adapter wrote it. Globbing
    `raw/*.json` was an OFF SWITCH, measured: dropping a hand-written
    `{"scratch": "fit score 8/10 overall"}` into that directory took the lint from
    exit 1 to exit 0 on unchanged prose. The corpus has to be what the adapters
    actually returned, and the only record of that is the `adapter_call` line the
    wrapper appends -- which the model cannot write without running the adapter.

    An unreadable capture is skipped rather than fatal: this function only ever
    REMOVES findings, so a corpus that comes back short fails closed.
    """
    pieces: list[str] = []
    source = workspace / "posting-source.txt"
    if source.is_file():
        try:
            pieces.append(source.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            pass
    # Candidate facts are trusted only while the evidence source hash matches,
    # and only from a file the run did not write itself.
    cv_text = evidence_cv_text(workspace, scanned)
    if cv_text:
        pieces.append(cv_text)
    pieces += master_profile_strings(workspace)
    for path in journaled_captures(workspace):
        try:
            node = json.loads(path.read_text(encoding="utf-8", errors="replace"))
        except (OSError, ValueError):
            continue
        _json_strings(node, pieces)
    # NUL joins the documents so a window cannot match across two of them.
    return _normalise(" \x00 ".join(pieces))


# Only an identifiable historical exam result can use this exemption. The
# evidence corpus is hash-verified above; arbitrary profile/raw files do not
# authorize a number. Exam identity and value both have to match.
_EXAM_RESULT = re.compile(
    r"(?P<exam>(?:大学英语)?[四六]级|CET[ -]?[46]|雅思|IELTS|托福|TOEFL|GRE|GMAT)"
    r"\s*(?:考试)?\s*(?:(?:成绩|总分|得分|score)\s*)?(?:为|是|of|[:：])?\s*"
    r"(?P<number>[0-9]+(?:\.[0-9]+)?)(?![0-9.])\s*(?:分|points?)?", re.I)


def _exam_results(text: str):
    for match in _EXAM_RESULT.finditer(text):
        exam = re.sub(r"[ -]", "", match["exam"].lower()).removeprefix("大学英语")
        exam = {"四级": "cet4", "六级": "cet6", "雅思": "ielts", "托福": "toefl"}.get(exam, exam)
        # 7 and 7.0 denote the same result; avoid float rounding of long values.
        number = match["number"]
        if "." in number:
            number = number.rstrip("0").rstrip(".")
        yield (exam, number), match.span("number")


# Rate transitions may use a different connector in the report. Bind both
# ordered values to the same named metric, never just to numbers in a corpus.
_RATE_TRANSITION = re.compile(
    r"(?P<metric>[\u3400-\u9fffA-Za-z][\u3400-\u9fffA-Za-z0-9_-]{1,48}率)"
    r"\s*(?:从|由)\s*(?P<before>[0-9]+(?:\.[0-9]+)?\s*[%％])\s*"
    r"(?:提升|提高|上升|升|增加|增|降低|下降|降|减少|减)?(?:到|至)\s*"
    r"(?P<after>[0-9]+(?:\.[0-9]+)?\s*[%％])")
_METRIC_FORECAST = re.compile(r"预计|预期|预测|目标|计划|有望|将|可能|假设|如果|若")
# Guidance may put an editorial verb directly before a Chinese metric name.
# Strip only that framing, not arbitrary prefixes of a captured metric.
_RATE_EDITORIAL_PREFIX = re.compile(
    r"^(?:请|建议|需要|应|可)?(?:保留|引用|复述|呈现|展示|说明|解释|核对|核实|提及)")
_RATE_CAUSAL_DISCUSSION = re.compile(
    r"(?:哪些|什么|其他|其它)(?:因素|变量|原因)\s*可能\s*(?:影响|导致|造成)")


def _rate_transitions(text: str):
    for match in _RATE_TRANSITION.finditer(text):
        # A future target is not historical evidence, even if its values happen
        # to equal an old result. Keep the full sentence's forecast visible.
        left = max(text.rfind(c, 0, match.start()) for c in '。；;\n\x00') + 1
        ends = [text.find(c, match.end()) for c in '。；;\n\x00']
        right = min((end for end in ends if end >= 0), default=len(text))
        # A follow-up about other possible causes does not forecast the rate.
        # Exempt only that causal qualifier after the result; keep any target,
        # condition or forecast elsewhere in the sentence visible.
        suffix = _RATE_CAUSAL_DISCUSSION.sub(
            lambda cause: cause.group(0).replace('可能', ''), text[match.end():right])
        if _METRIC_FORECAST.search(text[left:match.end()] + suffix):
            continue
        key = (match['metric'].casefold(),
               re.sub(r'\s+', '', match['before']).replace('％', '%'),
               re.sub(r'\s+', '', match['after']).replace('％', '%'))
        yield key, match


def mask_copied_numbers(line: str, corpus: str) -> str:
    """Blank numeric tokens this round captured verbatim, preserving length.

    The exemption is deliberately narrow: the token carrying the number, plus one
    neighbouring token on each side, must occur CONTIGUOUSLY in the capture. So
    quoting `(100 % remote)` off the card is exempt, while writing `100 % chance`
    around a number the card happened to contain is not -- the neighbours are what
    make it a quotation rather than a reuse of the digits.

    The window matches on TOKEN boundaries, not as a substring. A bare `8/10`
    passed as "captured" because the corpus held
    `https://example.com/2026/08/10/job` and `"8/10" in that` is true -- every
    capture carries dated URLs, so substring matching handed the exemption to any
    n/m a model cared to write. Both sides are space-padded, which is exact
    because `_normalise` has already collapsed all whitespace to single spaces.
    """
    if not corpus:  # fast path only: `x in ""` is already False for every window
        return line
    padded = " " + corpus + " "
    tokens = [(m.start(), m.end(), m.group(0)) for m in re.finditer(r"\S+", line)]
    out = list(line)
    for index, (start, end, token) in enumerate(tokens):
        if not _NUMERIC_TOKEN.search(token):
            continue
        window = [t[2] for t in tokens[max(0, index - 1):index + 2]]
        if " " + _normalise(" ".join(window)) + " " in padded:
            out[start:end] = " " * (end - start)
    known_exams = {key for key, _ in _exam_results(corpus)}
    for key, (start, end) in _exam_results(line):
        if key in known_exams:
            out[start:end] = " " * (end - start)
    known_rates = {key for key, _ in _rate_transitions(corpus)}
    for key, match in _rate_transitions(line):
        editorial_key = (_RATE_EDITORIAL_PREFIX.sub('', key[0], count=1), *key[1:])
        if key in known_rates or editorial_key in known_rates:
            for field in ('before', 'after'):
                start, end = match.span(field)
                out[start:end] = ' ' * (end - start)
    # Chinese prose has no whitespace tokens. Exempt only the numeric span
    # attached to an exact captured metric phrase; never erase prediction words.
    metric = re.compile(r"(?:效率|成本|收入|营收|耗时|延迟|转化率|准确率|产量|销量|用户数)(?:提升|提高|增长|增加|降低|减少|下降)(?:了)?\s*([0-9]+(?:\.[0-9]+)?\s*[%％])")
    for match in metric.finditer(line):
        if _normalise(match.group(0)) in corpus:
            start, end = match.span(1)
            out[start:end] = " " * (end - start)
    return "".join(out)


def mask_exempt_spans(line: str) -> str:
    """Blank URLs, labels, the roadmap horizon and explicit refusals, preserving length so
    the reported span still lines up with the original text."""
    masked = _URL.sub(lambda m: " " * len(m.group(0)), line)
    masked = ROADMAP_HORIZON.sub(lambda m: " " * len(m.group(0)), masked)
    masked = _DATE.sub(lambda m: " " * len(m.group(0)), masked)
    masked = ROUND_THE_CLOCK.sub(lambda m: " " * len(m.group(0)), masked)
    masked = _REFUSED_PREDICTION_ZH.sub(lambda m: " " * len(m.group(0)), masked)
    masked = _REFUSED_PREDICTION_EN.sub(lambda m: " " * len(m.group(0)), masked)
    masked = _NEGATED_CERTAINTY_ZH.sub(lambda m: " " * len(m.group(0)), masked)
    masked = _NEGATED_FORECAST_EN.sub(lambda m: " " * len(m.group(0)), masked)
    for label in VERDICT_LABELS:
        if label in masked:
            masked = masked.replace(label, " " * len(label))
    return masked


def mock_block_lines(lines: list[str]) -> set[int]:
    """0-based indices of lines inside a closed MOCK-*-V1 block.

    An unterminated block is NOT exempt. A block that never closes is a malformed
    artifact, and treating it as an exemption would make "type the opening line" a
    way to switch this lint off.
    """
    inside: set[int] = set()
    opened_at: int | None = None
    for index, line in enumerate(lines):
        if opened_at is None:
            if _MOCK_OPEN.match(line):
                opened_at = index
        elif _MOCK_CLOSE.match(line):
            inside.update(range(opened_at, index + 1))
            opened_at = None
    return inside


def mask_mock_quote(line: str) -> str:
    """Blank the payload of a `quote=` field, preserving length.

    `quote=` is last on the line and runs to its end, so everything after it is the
    candidate's own words. Only the payload is masked -- the tag, the ref and any
    prose before `quote=` are scanned exactly as before.
    """
    match = _QUOTE_FIELD.search(line)
    if not match:
        return line
    return line[:match.end()] + " " * len(line[match.end():])


def blockquote_allowlist(lines: list[str]) -> set[int]:
    exempt: set[int] = set()
    index = 0
    while index < len(lines):
        if not lines[index].lstrip().startswith(">"):
            index += 1
            continue
        start = index
        while index < len(lines) and lines[index].lstrip().startswith(">"):
            index += 1
        end = index - 1
        window = [lines[end]] + lines[end + 1:end + 3]
        if any(_ATTRIBUTION.match(candidate) for candidate in window):
            exempt.update(range(start, end + 1))
    return exempt


def scan_text(text: str, label: str, corpus: str = "", *,
              judgement: bool | None = None) -> list[str]:
    # A caller reading an actual debrief can know its role even when the model
    # chose a noncanonical filename. Keep the original label in every finding.
    if judgement is None:
        judgement = _is_judgement_surface(label)
    checks = CHECKS + (JUDGEMENT_CHECKS if judgement else ())
    lines = text.splitlines()
    exempt = blockquote_allowlist(lines)
    in_mock = mock_block_lines(lines)
    findings: list[str] = []
    for number, line in enumerate(lines):
        if number in exempt:
            continue
        quoted = mask_mock_quote(line) if number in in_mock else line
        masked = mask_exempt_spans(mask_copied_numbers(quoted, corpus))
        for code, pattern in checks:
            for match in pattern.finditer(masked):
                original = line[match.start():match.end()]
                findings.append(f"{code}: {label}:{number + 1}: {original!r} "
                                f"in {line.strip()!r}")
    return findings


def cannot_run(workspace: pathlib.Path, reason: str) -> int:
    """Exactly one receipt on the could-not-run path, then exit 2."""
    print(f"cannot run: {reason}", file=sys.stderr)
    if workspace.is_dir():
        journal.receipt(workspace, GATE, {}, "could_not_run", [f"NO_INPUT: {reason}"])
    return 2


def target_files(workspace: pathlib.Path) -> list[pathlib.Path]:
    found = []
    # mock/answer-guide.md is here because it is the file the candidate reads OUT
    # LOUD in the real room. It shipped unscanned by anything: a "70% chance" line
    # in it passed check_mock and every lint, on the one surface where an invented
    # number is spoken to a human rather than merely printed.
    for relative in ("report.md", "fit-assessment.md", "shortlist.md", "cheatsheet.md",
                     "mock/cheatsheet.md", "mock/answer-guide.md"):
        path = workspace / relative
        if path.exists():
            found.append(path)
    found += sorted((workspace / "mock").glob("assessment-*.md"))
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Ban predictions and invented numbers.")
    parser.add_argument("--workspace", required=True, type=pathlib.Path)
    parser.add_argument("--files", nargs="*", type=pathlib.Path, default=None)
    args = parser.parse_args(argv)

    workspace = args.workspace
    if not workspace.is_dir():
        return cannot_run(workspace, f"workspace {workspace} does not exist")
    files = list(args.files) if args.files else target_files(workspace)
    if not files:
        return cannot_run(workspace,
                          f"no rendered file to scan under {workspace}")
    # An explicit --files path that is not there is "could not run", not a
    # traceback with exit 1 — the code a caller reads as "findings".
    for path in files:
        if not path.is_file():
            return cannot_run(workspace, f"{path} not found")

    corpus = capture_corpus(workspace, files)
    findings: list[str] = []
    hashes: dict[str, str] = {}
    for path in files:
        try:
            relative = path.relative_to(workspace).as_posix()
        except ValueError:
            relative = path.name
        hashes[relative] = journal.sha256_file(path)
        findings += scan_text(path.read_text(encoding="utf-8"), relative, corpus)

    for finding in findings:
        print(finding)
    # A number finding is the one this gate gets WRONGLY actioned on: the
    # number is often the candidate's own measured result, which the
    # quantification ladder requires, and the finding says only that a `%` is
    # there. Measured 2026-10-08: an agent met exactly that on a true metric
    # and deleted the number, guessing. The exemption it needed already
    # exists — say so, once, on stderr, where it cannot dilute the per-line
    # finding contract on stdout.
    if any(f.split(":", 1)[0] in _NUMBER_CODES for f in findings):
        print("NOTICE_CAPTURED_NUMBERS: a number this round captured is exempt, but "
              "only when quoted WITH the words around it — the neighbours are what "
              "make it a quotation rather than a reuse of the digits. The candidate's "
              "own CV counts only while evidence-blocks.json binds it by hash, or — "
              "in apply mode — while master-fingerprint.json (check_claims.py "
              "--record) still matches the master profile. So: quote the captured "
              "wording, bind the evidence, or drop the number. A "
              "fit score or an outcome probability is never exempt.", file=sys.stderr)
    journal.receipt(workspace, GATE, hashes,
                    "fail" if findings else "pass", findings)
    return 1 if findings else 0


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    raise SystemExit(main())
