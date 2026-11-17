#!/usr/bin/env python3
"""Gate: every claim the tailoring added traces to a permitted source.

The claim-provenance checkpoint is the skill's highest-value rule and, until
claims.yaml existed, its most silent one: no provenance file, no citation column
in any required output, no script diffing the tailored CV against the master. A
run could skip it entirely and every downstream gate still passed — while every
automated signal in the system (an ATS REJECT on a missing keyword) rewarded the
dishonest edit.

Scope is a closed set of short atomic fields — skills leaves, certifications,
experience titles and orgs, education degrees and institutions, project roles,
publications, awards, volunteer and board lines — because that is where the named
fabrication classes land: each is one fact that is either true or fabricated, with
no middle. Free prose is deliberately out (bullets, summary, achievements, project
descriptions): rewording prose IS the skill's job, and a gate that fires on every
honest run is a gate people learn to skip. Which section is which is written down
in SCANNED_SECTIONS / OUT_OF_SCOPE_SECTIONS below, and a test derives that
partition from render_cv's rendered sections — so a section added to the CV cannot
be silently left unscanned, which is how org, institution, publications, awards,
project roles, volunteer and board sat unchecked next to the fields that were.

The master side is PARSED, and matched on whole tokens. `key in master_text` over
the raw file made a claim "sourced" by any substring hit anywhere in it: `Go` by
`django`, `Java` by `JavaScript`, `AI` by `email` — which every profile using the
canonical schema contains, so `AI` was permanently unfalsifiable — a fabricated
`MSc` certification by the real degree `MSc Computer Science`, and `PhD` by a YAML
COMMENT in the shipped example profile. Parsing to leaves is what kills the comment
class (a comment's words are still words, so word boundaries alone do not); whole
tokens are what kill the sub-word class. Neither alone does both. A tailored term
is sourced when it equals a master leaf, appears as a whole phrase inside one of
the candidate's own prose leaves, is a phrase of a master leaf **of its own kind**
(so the de-escalation "Senior ML Engineer" → "ML Engineer" stays quiet, while a
fabricated `MSc` *certification* is not sourced by a *degree*), or has a
claims.yaml row. `links` are excluded from the permitted set: an account on a
service is not a skill. (Whole-token matching already makes a bare URL inert —
one URL is one token — so what the exclusion still buys is the `{label, url}`
form, whose label is a leaf like any other.)

Employers and institutions are the exception to "a phrase of its own kind". A
name may lose a legal-form or group suffix ("Acme BV" → "Acme", "Alibaba Group"
→ "Alibaba", "株式会社リクルート" → "リクルート") or the sub-unit after its first
comma ("Leiden University, Faculty of Science" → "Leiden University"), and
nothing else: "Google" is a phrase of "Google Developer Student Club Leiden" and
names a different, far larger organisation, which is the fabricated-employer
class itself, and "TU Delft" off "TU Delft (exchange)" turns a semester into a
degree. A shortened name is ORG_TRUNCATED, and prose does not source a name
either — a client in a bullet is not an employer.

QUALIFIER_STRIPPED is deliberately narrow. It fires on two closed vocabularies
and nothing else: a dropped STATUS marker ("(in progress)", "(expired 2023)",
"(B1)", "在读", "（备考中）"), where deleting it upgrades a real credential into a
stronger one, and a dropped SUBORDINATE-RANK qualifier ("Assistant", "Associate",
"Junior", "Deputy", "Vice", "Acting", "Interim", "Trainee", "Intern", 副, 助理,
实习, 補佐, 부 …), where deleting it claims a more senior post than the one held.
Words that point the other way — Senior, Lead, Principal, Staff, Head — are not
in it: dropping them is a de-escalation, and stays quiet. It is NOT "the tailored
term is a substring of a master leaf": that version fires on `Senior ML Engineer`
→ `ML Engineer` and on `PyTorch Lightning` → `PyTorch`, the truthful reframings
this skill exists to permit, and a check that cries wolf on ordinary output is
worse than no check, because the reader learns to skip the line.

ORDER is part of the rule. The trimmed term is compared with the master entry it
came from (paired on dates and employer) and with every same-kind entry BEFORE
any looser source is consulted. Measured 2026-10-24: with the qualifier check
last, "MSc Computer Science" off "MSc Computer Science (in progress, expected
2027)" came back sourced, because the summary said "MSc Computer Science student"
and the prose pass cleared the claim before the qualifier was ever looked at.

The pairing also catches a title taken from a DIFFERENT entry. An earlier
"Analyst" role relabelled with a later role's "Data Scientist" is an exact title
of the master, so every looser source calls it sourced; only the entry it was
written on says otherwise. That is TITLE_FROM_OTHER_ENTRY, for titles, degrees
and project roles. It stays quiet when the pairing is ambiguous, and when the
dates say the tailored entry may be two master entries merged into one line.
Employers and institutions are left out of it on purpose: an entry at "Facebook"
relabelled "Meta" — the next entry's name for the same company — is honest.

Also fails if profile.yaml changed during the run. Overwriting the master is
destructive and unrecoverable, and the damage only surfaces on the NEXT
application, when the "master" has already been narrowed to the previous job.

Exit 0 = clean. Exit 1 = findings. Exit 2 = nothing recorded to check against.
"""
from __future__ import annotations

import argparse
import datetime
import json
import pathlib
import re
import sys
import unicodedata


sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import journal
import paths

GATE = "check_claims"
FINGERPRINT = "master-fingerprint.json"
SOURCE_KINDS = ("profile-line", "session-answer", "fetched-artifact")
CLAIM_KEYS = ("term", "where", "source_kind", "source_ref", "session_date",
              "retracted")
# `retracted` is a PRESENCE check, not a non-empty check: null is what a live
# claim looks like, and demanding a value would make every honest row invalid.
# It is still required to be there — in a schema where "absent" and "not
# retracted" are indistinguishable, a withdrawn claim leaves no scar, and the
# scar is the entire reason the field exists. Plan 4's check_mock.py requires
# the same six keys; a row that satisfied one and failed the other would make
# the two gates disagree about a shared artifact.
PRESENCE_ONLY_KEYS = ("retracted",)
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_PUNCT = re.compile(r"[^\w\s+#./-]", re.UNICODE)

# ── the scope registry ───────────────────────────────────────────────────────
# Keyed on render_cv's section keys, and scripts/tests/test_check_claims.py
# asserts the two sets are the same set. Adding a section to the CV without
# deciding whether it is checked now fails a test instead of passing silently.

SCANNED_SECTIONS = {
    "internships": "Display group only; entries remain in experience[] and their titles and employers are scanned there.",
    "skills":         "skills.<group>[] — the invented-tool class",
    "certifications": "certifications[] — the claimed-credential class",
    "experience":     "experience[].title (inflated title), experience[].org "
                      "(fabricated employer)",
    "education":      "education[].degree (degree not held), "
                      "education[].institution (fabricated alma mater)",
    "projects":       "projects[].role — the same seniority claim as a job title",
    "publications":   "publications[] — a fabricated paper is the most checkable "
                      "lie on an academic CV",
    "awards":         "awards[] — the same shape of credential as a certification",
    "volunteer":      "volunteer[] — names a real post at a real organisation",
    "board":          "board[] — a board seat is verifiable and often public record",
}

OUT_OF_SCOPE_SECTIONS = {
    "summary": "Free prose. Rewording it is the skill's job (gap-analysis.md §2 "
               "ALLOWED), so diffing it would fire on every honest run. Recorded "
               "deliberately in docs/superpowers/plans/"
               "2026-08-09-1-migration-and-p0-fixes.md, 'Scope, chosen deliberately'.",
    "achievements": "The executive CV's bullet band — 3-5 quantified statements "
                    "about work the candidate really did (cv-craft.md §1 'Senior "
                    "leader / Executive', candidate-situations.md §6). "
                    "gap-analysis.md §2 names "
                    "'rewording real achievements using the posting's exact "
                    "terminology' as ALLOWED, so scanning it fires on exactly the "
                    "operation the skill exists to perform. Same class as bullets, "
                    "same decision — and, like bullets, it is a permitted SOURCE.",
}

# Fields inside a scanned section that are still not scanned, and why. Not
# machine-checked (a field is not a section), but written down for the same
# reason: the next person should inherit a decision, not an omission.
OUT_OF_SCOPE_FIELDS = {
    "experience[].bullets":    "prose the candidate wrote about work they did",
    "education[].details":     "prose ('Thesis on X; GPA 8.5/10')",
    "projects[].description":  "prose",
    "projects[].name":         "the candidate's own label for their own work, "
                               "routinely renamed for readability; the checkable "
                               "facts in a project are the role and the links",
    "*.links":                 "a URL is not a claim, and is excluded from the "
                               "permitted source set for the same reason",
    "meta.headline":           "the positioning line, rewritten per posting by "
                               "design; same class as summary",
    "*.start / *.end":         "dates are not claims this gate models. Altering "
                               "them is forbidden (gap-analysis.md §2 NOT-ALLOWED) "
                               "but a date is sourced by any other date in the "
                               "file, so scanning them here would be theatre — a "
                               "field-wise diff of master vs tailored is the check "
                               "that would work, and does not exist yet",
}

# Free-prose keys, matched by key name at any depth. These are the candidate's own
# narrative about work they did, and they are the reason the bullet-only mention of
# a real tool ("Built a PyTorch pipeline") sources surfacing it into Skills — the
# cry-wolf guard this gate is pinned against. `publications` is here as well as in
# the scanned set: gap-analysis.md §1 names the candidate's own papers as valid
# evidence for a technical-depth claim.
PROSE_KEYS = ("summary", "bullets", "details", "description", "highlights",
              "notes", "achievements", "publications")
LINK_KEYS = ("links",)

# Qualifiers whose REMOVAL upgrades the claim. A CLOSED VOCABULARY, deliberately
# not "any dropped text": dropping "(2024)" off a certification, "(native)" off a
# language, "BV" off an employer or "(maternity cover)" off a title loses nothing a
# reader would have believed, and firing on those is how a gate gets ignored.
# `learning` and `studying` are deliberately absent though they name the class —
# they would fire on the master idiom `PyTorch (deep learning)` → `PyTorch`, and a
# rule that misfires on an ordinary ML CV is worse than a rule that misses
# "(learning)", which `in progress` / `in training` / `coursework` already cover.
#
# The list covers the languages this skill renders CVs in. Measured 2026-09-05:
# with English and Simplified Chinese only, an unfinished degree written
# `MSc Informatik (in Bearbeitung, voraussichtlich 2027)` -> `MSc Informatik`
# came back `sourced`, i.e. the honesty gate let a German, Dutch, Japanese or
# Korean candidate present a degree they do not hold. That is the load-bearing
# rule of the whole skill failing on language rather than on substance.
_STATUS_TOKENS = frozenset("""
    progress training ongoing expected anticipated planned pending prospective
    preparation preparing
    partial incomplete unfinished discontinued withdrawn paused deferred
    expired lapsed revoked suspended provisional candidate coursework audited
    self-taught taught beginner basic elementary intermediate conversational
    a1 a2 b1 b2 c1 c2 n1 n2 n3 n4 n5
    bearbeitung voraussichtlich laufend geplant angestrebt abgebrochen
    grundkenntnisse anfaenger anfänger fortgeschritten unvollstaendig
    unvollständig ausstehend abgelaufen
    verwacht lopend onafgerond gepland beginner basiskennis
    gevorderd verlopen bezig
    cours prevu prévu attendu inacheve inachevé debutant débutant notions
    intermediaire intermédiaire
    curso previsto esperado inacabado principiante nociones basico básico
    corso previsto incompleto principiante
""".split())
# Matched by containment, not equality: CJK writes without delimiters, so
# "预计2027" is one token and set membership would miss it. The Japanese and
# Korean entries are here for the same reason -- `修了見込み` and `졸업예정`
# never appear as separate whitespace tokens.
_STATUS_CJK = (
    "在读", "在讀", "在学", "在學", "预计", "預計", "已过期", "已失效", "待考",
    "初级", "初級", "入门", "入門", "肄业", "肄業", "未完成", "修读中", "修讀中",
    # 备考 = studying for the exam, i.e. not passed. Simplified only on purpose:
    # Japanese 備考 means "remarks", so the traditional form is listed as 備考中.
    "备考", "備考中", "准备中", "準備中",
    # Japanese
    "見込", "見込み", "在学中", "履修中", "取得予定", "予定", "中退", "失効",
    "初級", "日常会話", "勉強中",
    # Korean. 준비 is written both glued (준비중) and spaced (준비 중); the
    # spaced form leaves 중, which is in the ignorable set below.
    "재학", "재학중", "예정", "졸업예정", "수료", "중퇴", "이수중", "만료",
    "초급", "기초", "준비",
)
# A publication's status, whose removal turns a paper nobody has accepted into a
# published one: "Deep cine recon. NeurIPS 2025 (under review)" → "Deep cine
# recon. NeurIPS 2025" came back `sourced`. Only the words pointing that way —
# `in press`, `accepted` and `forthcoming` mean accepted, and dropping them
# claims nothing. Scoped to `publications` alone: "Code review" off a skill
# list, a "manuscript" award, "Physical Review Letters" are not statuses.
# `review` and `revision` are statuses only after `under` / `in`, so the pair is
# merged into one token before the test (`_publication_tokens`).
_PUBLICATION_STATUS_TOKENS = frozenset("""
    submitted preprint manuscript unpublished under_review in_review under_revision
    in_revision under_consideration
    eingereicht unveröffentlicht in_begutachtung ingediend ongepubliceerd in_beoordeling
    soumis soumise en_révision en_revision enviado enviada en_revisión sottomesso
    sottomessa in_revisione
""".split())
_PUBLICATION_STATUS_PAIRS = {
    "under": ("review", "revision", "consideration"),
    "in": ("review", "revision", "begutachtung", "beoordeling", "revisione"),
    "en": ("révision", "revision", "revisión"),
}
# Containment, like _STATUS_CJK. 심사 is "review" and stands alone in "심사 중".
_PUBLICATION_STATUS_CJK = (
    "投稿中", "已投稿", "审稿中", "審稿中", "在审", "在審", "返修", "査読中", "審査中",
    "投稿済", "심사중", "심사", "투고",
)


def _publication_tokens(tokens) -> list:
    """`tokens` with each `under review` / `in review` / `en révision` … pair
    merged into the one status token it is in `_PUBLICATION_STATUS_TOKENS`."""
    out, i = [], 0
    while i < len(tokens):
        if (i + 1 < len(tokens)
                and tokens[i + 1] in _PUBLICATION_STATUS_PAIRS.get(tokens[i], ())):
            out.append(f"{tokens[i]}_{tokens[i + 1]}")
            i += 2
            continue
        out.append(tokens[i])
        i += 1
    return out


# Tokens that carry no claim either way, so their presence in the dropped material
# neither triggers the finding nor blocks it. Anything with a digit is here (a year,
# a date) — checked AFTER the status test, so the CEFR levels above still win.
# The connectives of the other languages this skill writes CVs in are here for
# exactly the reason the English ones are: `dropped_status` requires the WHOLE
# dropped span to be status-or-nothing, so one unlisted preposition silences the
# finding. Measured: `Master Informatique (en cours, prévu 2027)` came back
# `sourced` because of the word `en`, and the Dutch case because of `nog niet`.
_IGNORABLE_TOKENS = frozenset(
    ("in of the to as at by on for and or level status since until from est "
     "approx approximately self grade "
     # "not YET finished". These carry no claim either way, which is what this
     # set is for — and without them the whole-span check rejected "not yet
     # completed" and "pas encore terminé" while accepting "no terminado" and
     # "non completato", so four of six languages fired and two did not.
     "yet still encore ancora todavia todavía aun aún ainda ännu "
     # de / nl
     "im am und oder bis seit ab noch nicht nog niet en van het op voor tot "
     "afgerond abgeschlossen "
     # fr
     "du la le les et ou a pour depuis dans "
     # es / it
     "el los las y para desde con di da del della nel su "
     # "CPA (exam in preparation)", "CFA Level III Candidate", "CPA (시험 준비 중)":
     # the exam and its part number say nothing either way, and without them the
     # whole-span rule let the status word go.
     "exam exams examination i ii iii iv "
     # zh / ja / ko connectives that survive tokenisation
     "年 月 版 중 시험").split())

# Subordinate-rank qualifiers: words whose REMOVAL claims a more senior post.
# Measured 2026-10-24, every one of these came back `sourced` because the short
# title is a phrase of the long one: Assistant Manager → Manager, Associate
# Director → Director, Junior Data Scientist → Data Scientist, 经理助理 → 经理,
# 副总监 → 总监. A closed vocabulary, for the reason the status list is one.
#
# Only the subordinate direction is here. Senior / Lead / Principal / Staff /
# Head are absent on purpose: dropping one is the honest de-escalation the gate
# must stay quiet on. Position matters, so the words are split by which side of
# the title they qualify — see `dropped_seniority`.
#
# Modifiers that qualify the head AFTER them ("Assistant Professor", "Vice
# President", "Acting Director"). `co` is "Co Founder" written with a space; the
# hyphenated "Co-Founder" is one token and already fails as unsourced.
_RANK_BEFORE = frozenset("""
    assistant asst associate assoc junior jr deputy vice acting interim adjunct co
    stellvertretender stellvertretende stellv kommissarischer kommissarische
    assistent assistentin
    waarnemend waarnemende plaatsvervangend plaatsvervangende
""".split())
# Postpositive modifiers that qualify the head BEFORE them ("Directeur adjoint",
# "Director adjunto").
_RANK_AFTER = frozenset("""
    adjoint adjointe interimaire intérimaire
    adjunto adjunta interino interina suplente aggiunto aggiunta
""".split())
# Trainee nouns, written on either side of the field ("Intern Software
# Engineer", "Software Engineer Intern", "Werkstudent Data Science").
_RANK_EITHER = frozenset("""
    intern interns internship trainee trainees apprentice apprenticeship
    praktikant praktikantin werkstudent werkstudentin auszubildender
    auszubildende azubi stagiair stagiaire becario becaria stagista tirocinante
""".split())
# Rank words that only ever appear inside a qualifier segment ("(en prácticas)").
_RANK_ONLY = frozenset("practicas prácticas praktikum tirocinio".split())
# CJK writes these glued to the title, so they are matched on the residue next to
# the kept span: a marker that qualifies what follows must END the text before
# it (副总监, 高级副总裁, 助理研究员, 見習いエンジニア, 수습기자), one that qualifies
# what precedes must START the text after it (经理助理, 課長補佐, 部長代理, 課長心得,
# 팀장 직무대리). 대리 alone is deliberately absent: in Korean it is itself a rank
# (assistant manager), not a qualifier on one.
_RANK_CJK_BEFORE = (
    "副", "助理", "实习", "实习生", "實習", "實習生", "见习", "見習", "見習い",
    "代理", "署理", "インターン", "수습", "인턴", "보조", "직무대리", "직무대행",
)
_RANK_CJK_AFTER = (
    "助理", "补佐", "補佐", "代理", "心得", "见习", "見習", "实习", "實習",
    "実習生", "研修生", "インターン", "인턴", "직무대리", "직무대행", "권한대행", "대행",
)
# Single characters too common inside other words to match by suffix: 标准
# ("standard") ends in 准, 본부 ("headquarters") ends in 부. They count only when
# they are the WHOLE residue — 准教授 → 教授, 부사장 → 사장, 부교수 → 교수.
_RANK_CJK_WHOLE = ("准", "부")
_RANK_CJK = frozenset(_RANK_CJK_BEFORE + _RANK_CJK_AFTER + _RANK_CJK_WHOLE)

# Legal-form designators, which an employer or institution name may lose (the
# group designators below and a sub-unit after the first comma are the only
# other things it may). Stripped from the end; the few written FIRST — Japanese and
# Korean forms (株式会社リクルート, (주)카카오 → tokens `株`, `주`) and the Dutch
# foundation — are stripped from the front as well. A Western form is never
# stripped from the front: "AS Roma" is not "Roma".
_LEGAL_FORMS_LEADING = frozenset("""
    株 有 주 株式会社 有限会社 合同会社 주식회사 유한회사 stichting
""".split())
_LEGAL_FORMS = frozenset("""
    inc incorporated corp corporation co ltd limited llc l.l.c llp lp plc p.l.c
    pllc gmbh ggmbh ag kg kgaa ohg ug se e.v stichting
    bv b.v nv n.v vof
    sa s.a sas s.a.s sarl s.a.r.l sl s.l slu cv c.v
    spa s.p.a srl s.r.l
    pty pte bhd sdn oy oyj ab as asa aps a/s kk k.k
    株 有 주
    股份有限公司 有限责任公司 有限責任公司 有限公司 株式会社 有限会社 合同会社
    주식회사 유한회사
""".split())
# The same CJK forms written glued to the name (腾讯科技有限公司).
_LEGAL_FORMS_GLUED = ("股份有限公司", "有限责任公司", "有限責任公司", "有限公司",
                      "株式会社", "有限会社", "合同会社", "주식회사", "유한회사")
# Corporate-group designators, dropped like a legal form but from the END only:
# "Alibaba Group" → "Alibaba", "Tencent Holdings Ltd" → "Tencent", "腾讯控股" →
# "腾讯", "楽天グループ株式会社" → "楽天". A group and its operating company are
# the same employer for a CV's purposes; "Group Lotus" is not "Lotus".
_GROUP_FORMS = frozenset("""
    group holdings holding 集团 集團 控股 グループ ホールディングス 그룹 홀딩스
""".split())
_GROUP_FORMS_GLUED = ("集团", "集團", "控股", "グループ", "ホールディングス",
                      "그룹", "홀딩스")
# Between two legal forms only: "GmbH & Co. KG", "S.A. de C.V.".
_LEGAL_JOINERS = frozenset("and und en et y e de".split())
# A leading article: "de Volksbank", "The Boston Consulting Group".
_LEADING_ARTICLES = frozenset("the de het".split())

# Scripts written without word delimiters. See `phrase_in`.
_UNSEGMENTED_RE = re.compile(r"[฀-๿　-鿿가-힯豈-﫿]")

# A delimited stretch of a leaf: "(in progress)", ", in progress", " — B1". The
# characters are ones normalize_term turns into spaces anyway, so splitting on
# them changes no token; a spaced hyphen is one too.
_SEGMENT_BREAK = re.compile(r"[()\[\]{}<>,;:|·、【】《》〈〉「」『』—–]|\s-+\s")

SOURCED, QUALIFIER, TRUNCATED, UNSOURCED, BORROWED = (
    "sourced", "qualifier", "truncated", "unsourced", "borrowed")

# Employer and institution names: matched by `_legal_core`, never by phrase, and
# against each other — a PhD candidate's university is both.
NAME_FAMILIES = ("experience.org", "education.institution")


def normalize_term(s) -> str:
    s = unicodedata.normalize("NFKC", str(s or "")).lower()
    return " ".join(_PUNCT.sub(" ", s).split())


def _token_list(text) -> list:
    """Whole tokens of `text`, trailing sentence punctuation trimmed.

    normalize_term keeps `+ # . / -` so that C++, C#, .NET and CI/CD survive as
    themselves — the cost is that a term ending a sentence normalizes to
    "kubernetes." and would then match nothing. Trailing dots are trimmed;
    leading ones are not, because ".NET" is a name.
    """
    return [t for t in (tok.rstrip(".") for tok in normalize_term(text).split()) if t]


def phrase_in(term, text) -> bool:
    """True when `term` occurs in `text` as whole tokens, never inside a word.

    Word boundaries are what stop `Java` being sourced by `JavaScript`, but they
    are a property of space-delimited scripts. Chinese, Japanese, Korean and Thai
    write without them, so a whole bullet is a single token and a token test would
    report every skill on every CJK CV as unsourced — the cry-wolf failure, not a
    fix. For a term in those scripts the test is containment within a single leaf,
    which is still far narrower than the whole-file substring it replaces.
    """
    t = normalize_term(term)
    if not t:
        return False
    if _UNSEGMENTED_RE.search(t):
        return t in normalize_term(text)
    wanted, have = _token_list(term), _token_list(text)
    n = len(wanted)
    return bool(n) and any(have[i:i + n] == wanted for i in range(len(have) - n + 1))


def _is_status(token, publication=False) -> bool:
    if publication and (token in _PUBLICATION_STATUS_TOKENS
                        or any(w in token for w in _PUBLICATION_STATUS_CJK)):
        return True
    return token in _STATUS_TOKENS or any(w in token for w in _STATUS_CJK)


def _is_ignorable(token) -> bool:
    # A token with no letter or digit at all is a bare separator ("-", "&").
    return (token in _IGNORABLE_TOKENS or any(ch.isdigit() for ch in token)
            or not any(ch.isalnum() for ch in token))


# A NEGATED completion is a status marker, and neither half of it is one on its
# own. "nog niet afgerond" is Dutch for "not yet completed": `nog`, `niet` and
# `afgerond` are all connectives or completion words, all correctly ignorable
# alone — `afgerond` by itself means the degree IS finished — so `dropped_status`
# saw no status token and stayed silent.
#
# SKILL.md cites `(nog niet afgerond)` by name as one of the five spellings this
# gate covers. Measured 2026-09-06: of six languages writing the same unfinished
# degree, five fired and Dutch did not — the one the documentation used as its
# example. A Dutch candidate could present an unfinished MSc as held and the
# honesty gate said pass.
#
# Adding `afgerond` to the status set would fire on every COMPLETED degree, which
# is why the pair is what is matched rather than either word.
_NEGATORS = frozenset("""
    not no never nog niet geen nicht kein keine noch non pas sans ne
    sin senza nao não ikke inte ingen
""".split())
_COMPLETION_WORDS = frozenset("""
    completed complete finished awarded conferred obtained graduated
    afgerond voltooid behaald afgestudeerd
    abgeschlossen beendet erworben absolviert
    termine terminé acheve achevé obtenu diplome diplômé
    terminado completado obtenido titulado finalizado
    completato terminato conseguito laureato
    avslutad slutford slutförd fullfort fullført
""".split())


def _negated_completion(tokens) -> bool:
    """Is a negator paired with a completion word inside this dropped span?

    Window of three, so "nog niet afgerond" and "noch nicht abgeschlossen" both
    match while a negator and a completion word at opposite ends of a long
    department name do not.
    """
    for i, token in enumerate(tokens):
        if token in _NEGATORS:
            if any(t in _COMPLETION_WORDS for t in tokens[i + 1:i + 4]):
                return True
    return False


def dropped_status(term, leaf, family=None):
    """The status marker `term` drops off `leaf`, or None.

    What the term dropped must be a status and NOTHING BUT a status (plus dates
    and connectives, which say nothing either way). Both halves are load-bearing:

    * "MSc Computer Science" off "MSc Computer Science (in progress, expected
      2027)" drops `progress` + `expected` and two ignorables → fires.
    * "ML Engineer" off "Senior ML Engineer" drops `senior`, "Acme" off "Acme BV"
      drops `bv`, "AWS … Practitioner" off "… (2024)" drops a year → no status,
      no finding. These are the honest reframings the gate must stay silent on.
    * "Engineer" off "Engineer, Basic Materials Group" drops `basic` — a status
      word — but also `materials` and `group`, which are not, so the dropped text
      is a department name and not a qualifier. Requiring the whole dropped span
      to be status is what tells those apart; a bare `contains a status word`
      test fires on it.

    Punctuation is whitespace by the time we compare, so "(B1)", ", in progress"
    and " — expected 2027" are one rule rather than three, and a master that
    writes the qualifier without brackets is not a way through.

    Two narrower cases fire as well, both only when the term itself carries no
    status word: everything AFTER the kept span is status ("Dutch" off "English
    (native), Dutch (B1)"; "硕士" off "计算机科学硕士在读"), or the delimited
    segments right after the kept span's own segment are ("MSc" off "MSc
    Computer Science (in progress)" — the field went with the status, and the
    status was still dropped). The segment must be the one directly after: in
    "English (native), Dutch (B1)" the B1 belongs to Dutch, and "English" drops
    nothing that qualified it.

    The `publications` family adds the publication statuses (under review,
    submitted, preprint, 投稿中 …) to the vocabulary, for that family only.
    """
    split = _split(term, leaf)
    if split is None:
        return None
    pub = family == "publications"
    before, after, later = split
    term_tokens = _token_list(term)
    if pub:
        before, after, term_tokens = (_publication_tokens(before),
                                      _publication_tokens(after),
                                      _publication_tokens(term_tokens))
        later = [_publication_tokens(seg) for seg in later]

    def status_only(tokens):
        return _status_only(tokens, pub)

    def shown(tokens):
        return " ".join(tokens).replace("_", " ")

    dropped = before + after
    if not dropped:
        return None
    if status_only(dropped):
        return shown(dropped)
    if _carries_status(term_tokens, pub):
        return None
    if status_only(after):
        return shown(after)
    # "(under review at MRM)" / "submitted to NeurIPS": a publication status
    # names its venue, so the dropped span is never status alone — and dropping
    # all of it still presents the paper as published.
    if pub and after and _is_status(after[0], True):
        lead = []
        for token in after:
            if not _accounted(token, True):
                break
            lead.append(token)
        while lead and not _is_status(lead[-1], True):
            lead.pop()
        return shown(lead)
    return shown(_leading_run(later, status_only)) or None


# The negator and the completion word are the qualifier in "nog niet afgerond",
# so they count as accounted-for rather than as leftover content. Widening
# `_IGNORABLE_TOKENS` globally instead would make `completed` invisible
# everywhere, and "MSc A" off "MSc A completed 2024" must stay silent — it drops
# no status and reads as an honest trim.
def _accounted(token, publication=False) -> bool:
    return (_is_status(token, publication) or _is_ignorable(token)
            or token in _NEGATORS or token in _COMPLETION_WORDS)


def _carries_status(tokens, publication=False) -> bool:
    return (any(_is_status(t, publication) for t in tokens)
            or _negated_completion(tokens))


def _status_only(tokens, publication=False) -> bool:
    """A status marker and nothing else: at least one status, no content."""
    return (bool(tokens) and _carries_status(tokens, publication)
            and all(_accounted(t, publication) for t in tokens))


def _leading_run(segments, test) -> list:
    """The tokens of the segments at the front of `segments` that pass `test`."""
    run = []
    for seg in segments:
        if not test(seg):
            break
        run += seg
    return run


def _segment_tokens(text) -> list:
    """[(token, segment index)]: the tokens of `text`, each tagged with the
    delimited segment it sits in. The tokens are `_token_list`'s, minus bare
    separators such as the hyphen in "First Aid - expired 2024"."""
    text = unicodedata.normalize("NFKC", str(text or ""))
    return [(tok, i) for i, seg in enumerate(_SEGMENT_BREAK.split(text))
            for tok in _token_list(seg)]


def _split(term, leaf):
    """What `leaf` says around `term`: (before, after, later_segments), or None.

    None when `term` is not a whole-token phrase of `leaf`. `before` and `after`
    are the leaf's tokens on either side of the first occurrence; `later_segments`
    are the token lists of the delimited segments after the one the occurrence
    ends in.

    Chinese, Japanese and Korean glue a qualifier to the word it qualifies, so
    "计算机科学硕士在读" is ONE token and a token match finds no "计算机科学硕士"
    in it — which is how dropping 在读 passed whenever the master wrote it without
    brackets. For a term in those scripts the occurrence is found by containment
    instead, the same fallback `phrase_in` uses, and the residue either side is
    what was dropped.

    The term is tokenised the way the leaf is, a spaced hyphen being a segment
    break on both sides. Tokenised plainly, "Engineer - Data" kept its hyphen as
    a token, never matched the leaf's tokens, and the "Assistant" dropped off
    "Assistant Engineer - Data" went unreported.
    """
    wanted = [tok for tok, _seg in _segment_tokens(term)]
    tagged = _segment_tokens(leaf)
    have = [tok for tok, _seg in tagged]
    n = len(wanted)
    if not n or not have:
        return None
    at = next((i for i in range(len(have) - n + 1) if have[i:i + n] == wanted), None)
    if at is not None:
        before, after, last = have[:at], have[at + n:], at + n - 1
    else:
        needle = " ".join(wanted)
        if not _UNSEGMENTED_RE.search(needle):
            return None
        joined = " ".join(have)
        found = joined.find(needle)
        if found < 0:
            return None
        end = found + len(needle)
        starts = [0]
        for tok in have[:-1]:
            starts.append(starts[-1] + len(tok) + 1)
        last = max(i for i, s in enumerate(starts) if s < end)
        before, after = _token_list(joined[:found]), _token_list(joined[end:])
    end_seg = tagged[last][1]
    later = {}
    for tok, seg in tagged:
        if seg > end_seg:
            later.setdefault(seg, []).append(tok)
    return before, after, [later[k] for k in sorted(later)]


def _rank_before(token) -> bool:
    """Does `token`, written BEFORE a title, make it a subordinate post?"""
    return (token in _RANK_BEFORE or token in _RANK_EITHER
            or token in _RANK_CJK_WHOLE
            or any(token.endswith(m) for m in _RANK_CJK_BEFORE))


def _rank_after(token) -> bool:
    """Does `token`, written AFTER a title, make it a subordinate post?"""
    return (token in _RANK_AFTER or token in _RANK_EITHER
            or any(token.startswith(m) for m in _RANK_CJK_AFTER))


def _is_rank(token) -> bool:
    return (token in _RANK_BEFORE or token in _RANK_AFTER or token in _RANK_EITHER
            or token in _RANK_ONLY or token in _RANK_CJK)


def _rank_only(tokens) -> bool:
    """A rank qualifier and nothing else ("(Acting)", ", Interim", "（实习）")."""
    return (any(_is_rank(t) for t in tokens)
            and all(_is_rank(t) or _accounted(t) for t in tokens))


def dropped_seniority(term, leaf):
    """The subordinate-rank qualifier `term` drops off `leaf`, or None.

    Adjacency, not presence, is the rule — a rank word somewhere in the dropped
    text is not enough:

    * a modifier written before a title qualifies the title: "Manager, Data"
      off "Assistant Manager, Data", "Director" off "Associate Director",
      "President" off "Vice President", "总监" off "副总监" → fire. Connectives
      are skipped, so "CEO" off "Personal Assistant to the CEO" fires too;
    * a postpositive one qualifies what precedes it: "Engineer" off "Engineer
      Intern", "Directeur" off "Directeur adjoint", "经理" off "经理助理";
    * a dropped segment made of nothing but a rank ("Director (Interim)",
      "Manager, Acting") fires wherever it sat.

    And the quiet half, each of which contains a rank word:

    * "Professor" off "Professor and Associate Dean" — "Associate" qualifies the
      deanship that was dropped, not the professorship that was kept;
    * "Software Engineer" off "Software Engineer, Acting Team Lead" — dropping an
      extra post is a de-escalation;
    * "Vice President" kept intact, and "Vice President" off "Senior Vice
      President" — Senior is not a subordinate qualifier.
    """
    split = _split(term, leaf)
    if split is None:
        return None
    before, after, later = split
    if not before and not after:
        return None
    nearest = next((t for t in reversed(before) if not _is_ignorable(t)), None)
    if nearest is not None and _rank_before(nearest):
        return nearest
    if after and _rank_after(after[0]):
        return after[0]
    dropped = before + after
    if _rank_only(dropped):
        return " ".join(dropped)
    return " ".join(_leading_run(later, _rank_only)) or None


def dropped_qualifier(term, leaf, family=None):
    """("status" | "seniority", the dropped words), or None."""
    status = dropped_status(term, leaf, family)
    if status:
        return "status", status
    rank = dropped_seniority(term, leaf)
    if rank:
        return "seniority", rank
    return None


def _legal_core(name) -> str:
    """`name` normalized, with legal-form and group designators and a leading
    article off.

    "Acme B.V." / "Acme BV" / "Acme" → "acme"; "Acme S.A. de C.V." → "acme";
    "Tencent Holdings Ltd" → "tencent"; "株式会社リクルート" / "(株)リクルート" →
    "リクルート"; "腾讯控股有限公司" → "腾讯"; "楽天グループ株式会社" → "楽天".
    Nothing else is removed: "Google Developer Student Club Leiden" stays
    itself, so it cannot be shortened to "Google".
    """
    if not isinstance(name, (str, int, float)) or isinstance(name, bool):
        return ""
    toks = _token_list(name)
    changed = True
    while changed and len(toks) > 1:
        changed = False
        while len(toks) > 1 and (toks[0] in _LEADING_ARTICLES
                                 or toks[0] in _LEGAL_FORMS_LEADING):
            toks.pop(0)
            changed = True
        tail = False
        while len(toks) > 1 and (toks[-1] in _LEGAL_FORMS
                                 or toks[-1] in _GROUP_FORMS):
            toks.pop()
            tail = changed = True
        if tail and len(toks) > 1 and toks[-1] in _LEGAL_JOINERS:
            toks.pop()
    core = " ".join(toks)
    changed = True
    while changed:
        changed = False
        for form in _LEGAL_FORMS_GLUED + _GROUP_FORMS_GLUED:
            if core.endswith(form) and len(core) > len(form):
                core, changed = core[:-len(form)].strip(), True
        for form in _LEGAL_FORMS_GLUED:
            if core.startswith(form) and len(core) > len(form):
                core, changed = core[len(form):].strip(), True
    return core


def _before_first_comma(name) -> str:
    """Everything before the first comma of `name`, or "" when it has none.

    "Leiden University, Faculty of Science" → "Leiden University". Only a comma
    marks a sub-unit: "TU Delft (exchange)" has no comma, so the bracket stays
    part of the name and dropping it is still a truncation.
    """
    text = unicodedata.normalize("NFKC", str(name or ""))
    return text.split(",", 1)[0] if "," in text else ""


def _relate(term, leaf, family=None):
    """(relation, detail) of `term` to one master leaf of the same kind."""
    if family in NAME_FAMILIES:
        core = _legal_core(term)
        if core and core in (_legal_core(leaf),
                             _legal_core(_before_first_comma(leaf))):
            return SOURCED, None
        return (TRUNCATED, None) if phrase_in(term, leaf) else (None, None)
    if normalize_term(term) == normalize_term(leaf):
        return SOURCED, None
    if not phrase_in(term, leaf):
        return None, None
    dropped = dropped_qualifier(term, leaf, family)
    return (QUALIFIER, dropped) if dropped else (SOURCED, None)


def relation(term, leaf, family=None):
    """How `term` relates to one master leaf of the same family.

    SOURCED; QUALIFIER (the leaf says the same thing, and the term dropped a
    status marker or a subordinate-rank qualifier off it); TRUNCATED (an
    employer or institution name shortened beyond its legal form); or None.
    """
    return _relate(term, leaf, family)[0]


# Entry-shaped sections, and the field that names the entry's organisation.
_ENTRY_PATH = re.compile(r"^(experience|education|projects)\[(\d+)\]\.(\w+)$")
_ENTRY_NAME = {"experience": "org", "education": "institution", "projects": "name"}


def _scalar(value) -> str:
    # A YAML date (`start: 2021-03-15`, unquoted) is a date object, and render_cv
    # prints it. Read as "", it gave no pairing credit, so a master written with
    # full dates paired two roles at one employer on the employer alone — a tie,
    # i.e. no pairing, and the backdated promotion went through.
    if isinstance(value, datetime.date):
        return value.isoformat()[:10]
    # A YAML boolean is no name and no date: `On`, `Yes` and `true` all load as
    # True, so two equal booleans say nothing about two equal values.
    if isinstance(value, bool) or not isinstance(value, (str, int, float)):
        return ""
    return normalize_term(value)


def _pair(where, tailored, master):
    """(field, the tailored entry, its master pair, the other master entries),
    or None when the entry does not pair.

    The tailored entry is matched to a master entry by its dates (start counts
    2, end 1) and its organisation (2) — never by position, because reordering
    and dropping entries are honest moves. A match needs a score of 2 and a
    unique best; anything less is no pairing, and the claim is then checked
    against every same-kind entry instead. The field being checked is never used
    to find its own pair.

    Why pair at all: "Data Scientist" for a role the master records as "Junior
    Data Scientist" is the commonest inflation there is, and when a later role
    really is "Data Scientist" the family-wide check finds that exact title and
    calls the claim sourced. The entry it came from is the only thing that says
    otherwise.
    """
    m = _ENTRY_PATH.match(where)
    if not m or not isinstance(tailored, dict) or not isinstance(master, dict):
        return None
    section, index, field = m.group(1), int(m.group(2)), m.group(3)
    entries = _as_list(tailored.get(section))
    mine = entries[index] if index < len(entries) else None
    if not isinstance(mine, dict):
        return None
    name_key = _ENTRY_NAME[section]
    same_name = _legal_core if section != "projects" else _scalar
    scored = []
    for theirs in _as_list(master.get(section)):
        if not isinstance(theirs, dict):
            continue
        score = 0
        for key, weight in (("start", 2), ("end", 1)):
            a = _scalar(mine.get(key))
            if a and a == _scalar(theirs.get(key)):
                score += weight
        if field != name_key:
            a = same_name(mine.get(name_key))
            if a and a == same_name(theirs.get(name_key)):
                score += 2
        scored.append((score, theirs))
    if not scored:
        return None
    best = max(score for score, _entry in scored)
    winners = [entry for score, entry in scored if score == best]
    if best < 2 or len(winners) != 1:
        return None
    return field, mine, winners[0], [e for _s, e in scored if e is not winners[0]]


def _merge_partner(mine, paired, other) -> bool:
    """Could `mine` be `paired` and `other` written as one line? Yes when
    `other` accounts for one of mine's dates that `paired` does not — the
    merged "2019-03 – present" takes its start from one role and its end from
    the next. A date both share explains nothing: two current roles both end
    "present"."""
    for key in ("start", "end"):
        date = _scalar(mine.get(key))
        if date and date != _scalar(paired.get(key)) and date == _scalar(other.get(key)):
            return True
    return False


def pairing(where, tailored, master):
    """(the master's value of this field ON THE SAME ENTRY, the other entries).

    (None, ()) when the entry does not pair, and the value is None as well when
    the paired entry has no such field. The other entries come as (their value
    of the field, whether they could be merged into this one), for
    `_borrowed`.
    """
    pair = _pair(where, tailored, master)
    if pair is None:
        return None, ()
    field, mine, paired, rest = pair
    others = [(_flat(e[field]), _merge_partner(mine, paired, e))
              for e in rest if e.get(field)]
    return (_flat(paired[field]) if paired.get(field) else None), others


def _borrowed(term, family, others):
    """The other entry's value `term` was taken from, or None.

    None as well when an entry it could have come from could also have been
    merged into this one: "Data Scientist, 2019-03 – present" over a master
    "Analyst, 2019-03 – 2021-02" and "Data Scientist, 2021-03 – present" is two
    roles on one line, and whether that line is fair is the recruiter judge's
    question, not one this gate can settle from dates.
    """
    donors = [(value, merged) for value, merged in others
              if _relate(term, value, family)[0] == SOURCED]
    if not donors or any(merged for _value, merged in donors):
        return None
    return donors[0][0]


def _as_list(v):
    if isinstance(v, str):
        return [v]
    if isinstance(v, list):
        return v
    return []


def _flat(v):
    if isinstance(v, dict):
        return " ".join(str(x) for x in v.values())
    return str(v)


def atomic_claims(profile) -> list:
    """[(term, field_path, family)] over the closed set of atomic claim fields.

    ONE walker, run over both profiles: the tailored side supplies the claims to
    check, the master side supplies the evidence they are checked against. Two
    walkers is two things to drift — and the drift that already happened here was
    `experience[].title` being scanned while `experience[].org`, the adjacent key
    in the same dict, was not.
    """
    profile = profile if isinstance(profile, dict) else {}
    out = []
    skills = profile.get("skills") or {}
    if isinstance(skills, dict):
        for group, items in skills.items():
            for item in _as_list(items):
                out.append((_flat(item), f"skills.{group}", "skills"))
    else:
        for item in _as_list(skills):
            out.append((_flat(item), "skills", "skills"))
    for i, ex in enumerate(_as_list(profile.get("experience"))):
        if not isinstance(ex, dict):
            continue
        for field in ("title", "org"):
            if ex.get(field):
                out.append((_flat(ex[field]), f"experience[{i}].{field}",
                            f"experience.{field}"))
    for i, ed in enumerate(_as_list(profile.get("education"))):
        if not isinstance(ed, dict):
            continue
        for field in ("degree", "institution"):
            if ed.get(field):
                out.append((_flat(ed[field]), f"education[{i}].{field}",
                            f"education.{field}"))
    for i, pr in enumerate(_as_list(profile.get("projects"))):
        if isinstance(pr, dict) and pr.get("role"):
            out.append((_flat(pr["role"]), f"projects[{i}].role", "projects.role"))
    for section in ("certifications", "publications", "awards", "volunteer", "board"):
        for i, item in enumerate(_as_list(profile.get(section))):
            out.append((_flat(item), f"{section}[{i}]", section))
    return out


def _leaf_strings(node):
    """Every scalar leaf under `node`, as raw strings. `links` excluded.

    The exclusion is one line here and covers both `contact.links` and
    `projects[].links`, including the `{label, url}` form: the label of a link is
    the name of a service, not evidence that the candidate has a skill.
    """
    if isinstance(node, dict):
        for key, value in node.items():
            if str(key).strip().lower() not in LINK_KEYS:
                yield from _leaf_strings(value)
    elif isinstance(node, (list, tuple)):
        for item in node:
            yield from _leaf_strings(item)
    elif node is not None and not isinstance(node, bool):
        yield str(node)


def _prose_strings(node):
    """Every leaf under a free-prose key — the candidate's own narrative.

    Only leaves *under* a PROSE_KEYS key are yielded, and they are collected by
    `_leaf_strings`, so a `links:` list nested under one is dropped there rather
    than needing a second guard here.
    """
    if isinstance(node, dict):
        for key, value in node.items():
            name = str(key).strip().lower()
            yield from (_leaf_strings(value) if name in PROSE_KEYS
                        else _prose_strings(value))
    elif isinstance(node, (list, tuple)):
        for item in node:
            yield from _prose_strings(item)


def master_sources(profile):
    """(exact, prose, families) — the permitted evidence, parsed from leaves.

    `exact` is every leaf normalized, so a term that is a whole field ANYWHERE in
    the master is sourced wherever the tailoring puts it. That is a provenance
    answer, not a semantic one: it says the candidate's own file states this exact
    string. It is what lets a skill be regrouped, and what keeps a PhD candidate's
    university quiet when it is both their `education[].institution` and their
    `experience[].org`. Its cost, accepted knowingly: moving a `projects[].role`
    verbatim into `experience[].title` is quiet too, and whether that restructure
    is *appropriate* is a question this gate cannot answer without guessing — the
    recruiter judge and the human read the CV for that.

    `prose` is the free-text leaves, matched by whole phrase. `families` keeps each
    atomic leaf under its own kind, because the looser phrase match is only safe
    within a kind — a degree does not source a certification.
    """
    exact = {normalize_term(s) for s in _leaf_strings(profile)}
    exact.discard("")
    prose = [s for s in _prose_strings(profile) if normalize_term(s)]
    families = {}
    for term, _where, family in atomic_claims(profile):
        families.setdefault(family, []).append(term)
    return exact, prose, families


def _claim_index(claims):
    """{normalized term: row} for live rows, plus findings for malformed ones."""
    live, retracted, findings = {}, {}, []
    for i, row in enumerate(claims or []):
        if not isinstance(row, dict):
            findings.append(f"BAD_CLAIM_ROW: claims.yaml[{i}] is not a mapping")
            continue
        for key in CLAIM_KEYS:
            if key not in row:
                findings.append(f"BAD_CLAIM_ROW: claims.yaml[{i}] is missing required "
                                f"key {key!r}")
            elif key not in PRESENCE_ONLY_KEYS and not str(row.get(key) or "").strip():
                findings.append(f"BAD_CLAIM_ROW: claims.yaml[{i}] has an empty "
                                f"required key {key!r}")
        if row.get("source_kind") and row["source_kind"] not in SOURCE_KINDS:
            findings.append(f"BAD_CLAIM_ROW: claims.yaml[{i}] source_kind "
                            f"{row['source_kind']!r} is not one of "
                            f"{', '.join(SOURCE_KINDS)} — there is no fourth source")
        if row.get("session_date") and not _DATE_RE.match(str(row["session_date"])):
            findings.append(f"BAD_CLAIM_ROW: claims.yaml[{i}] session_date "
                            f"{row['session_date']!r} is not YYYY-MM-DD")
        key = normalize_term(row.get("term"))
        if not key:
            continue
        (retracted if row.get("retracted") else live)[key] = row
    return live, retracted, findings


def trace(term, family, paired, exact, prose, families, others=()):
    """None when `term` is sourced, else (relation, master leaf, detail).

    The relation is QUALIFIER (detail: the dropped words), TRUNCATED, BORROWED
    (leaf: the paired entry's own value; detail: the other entry's value the
    term matches) or UNSOURCED (leaf and detail None). `others` is
    `pairing`'s second half.

    The order is the substance of the rule. A trimmed term is compared first with
    the master entry it came from (`paired`), then with every master entry of its
    own kind, and only THEN with the looser evidence: an exact leaf anywhere and
    the candidate's prose. Run the other way round, the looser evidence clears a
    claim before its dropped qualifier is ever looked at — the summary's "MSc
    Computer Science student" sourced "MSc Computer Science" for a degree the
    master marks "(in progress, expected 2027)".

    Among same-kind entries an honest match beats a dropped qualifier, as it
    always did: a holder of both "AWS … Architect – Associate" and "AWS …
    Architect – Professional" may write "AWS … Architect". The pairing is what
    stops that precedence from excusing the one entry the term actually came
    from — and from excusing a title that is another entry's outright.
    """
    names = family in NAME_FAMILIES
    if paired is not None:
        rel, dropped = _relate(term, paired, family)
        if rel == SOURCED:
            return None
        if rel is not None:
            return rel, paired, dropped
        if not names:
            donor = _borrowed(term, family, others)
            if donor is not None:
                return BORROWED, paired, donor
    kinds = NAME_FAMILIES if names else (family,)
    kin = [(leaf, *_relate(term, leaf, family))
           for kind in kinds for leaf in families.get(kind, ())]
    if any(rel == SOURCED for _leaf, rel, _dropped in kin):
        return None
    hit = next(((rel, leaf, dropped) for leaf, rel, dropped in kin
                if rel is not None), None)
    if hit is not None:
        return hit
    if normalize_term(term) in exact:
        return None
    # A name is never sourced by prose: an employer that appears only in a
    # bullet ("built dashboards for Shell") is a client, not an employer.
    if not names and any(phrase_in(term, leaf) for leaf in prose):
        return None
    return UNSOURCED, None, None


def _writeback_chain(ws, master, start_sha, now_sha):
    """(finding ids, last date) when recorded write-backs lead from start_sha to now_sha.

    online_presence.py logs each write it makes to a master with before/after
    hashes. A master changed only by those writes is not a tailoring mutation; any
    other change still is, so the chain must reach the current hash exactly.
    """
    try:
        import online_presence
        record = online_presence.load_record(
            online_presence.resolve_record_path(paths.online_presence_of(ws)))
    except (ValueError, OSError, journal.YamlUnreadable, ImportError):
        return None
    steps = [w for w in record.get("writebacks", []) if isinstance(w, dict)
             and str(w.get("master")) == str(master)]
    sha, ids, last = start_sha, [], None
    for _ in range(len(steps)):
        step = next((w for w in steps if w.get("before_sha256") == sha), None)
        if step is None:
            break
        sha = step.get("after_sha256")
        ids += [str(i) for i in step.get("finding_ids") or []]
        last = step.get("date")
        if sha == now_sha:
            return ids, last
    return None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", required=True)
    ap.add_argument("--master", default=None)
    ap.add_argument("--record", action="store_true",
                    help="fingerprint the master profile at apply-mode entry")
    args = ap.parse_args(argv)
    ws = pathlib.Path(args.workspace)
    if not ws.is_dir():
        # journal.receipt() would mkdir it, and a gate that creates the
        # workspace it is auditing has manufactured its own evidence.
        print(f"cannot run {GATE}: workspace {ws} does not exist", file=sys.stderr)
        return 2
    fp_path = ws / FINGERPRINT

    if args.record:
        if not args.master or not pathlib.Path(args.master).exists():
            journal.receipt(ws, GATE, {}, "could_not_run",
                            [f"MISSING_INPUT: master {args.master}"])
            print(f"cannot run {GATE}: --master must point at an existing profile.yaml",
                  file=sys.stderr)
            return 2
        master = pathlib.Path(args.master).resolve()
        digest = journal.sha256_file(master)
        ws.mkdir(parents=True, exist_ok=True)
        fp_path.write_text(json.dumps({
            "path": str(master), "sha256": digest,
            "mtime_ns": master.stat().st_mtime_ns}, indent=2) + "\n", encoding="utf-8")
        # "baseline_recorded", not "recorded": this path fingerprints the master
        # and checks nothing at all. While it shared "recorded" with the gates that
        # DO check, check_apply.py counted it as a pass — so a run that did only
        # this documented mode-entry step delivered a package whose claims nobody
        # had verified, and a `--record` re-run on resume erased a real failure.
        journal.receipt(ws, GATE, {"profile.yaml": digest}, "baseline_recorded", [])
        return 0

    tailored_path = ws / "tailored-profile.yaml"
    if not fp_path.exists() or not tailored_path.exists():
        missing = FINGERPRINT if not fp_path.exists() else "tailored-profile.yaml"
        code = "NO_MASTER_FINGERPRINT" if missing == FINGERPRINT else "MISSING_INPUT"
        journal.receipt(ws, GATE, {}, "could_not_run", [f"{code}: {ws / missing}"])
        print(f"cannot run {GATE}: {code} — {ws / missing} does not exist; run with "
              f"--record --master <profile.yaml> at apply-mode entry", file=sys.stderr)
        return 2

    try:
        fp = json.loads(fp_path.read_text(encoding="utf-8"))
        if not isinstance(fp, dict) or not isinstance(fp.get("path"), str):
            raise ValueError("no master path recorded")
    except (OSError, UnicodeError, ValueError) as exc:
        # A corrupt fingerprint verifies nothing; say so with the could-not-run
        # code rather than a traceback and exit 1, which reads as "findings".
        journal.receipt(ws, GATE, {}, "could_not_run",
                        [f"NO_MASTER_FINGERPRINT: {fp_path} is unreadable ({exc})"])
        print(f"cannot run {GATE}: NO_MASTER_FINGERPRINT — {fp_path} is unreadable; "
              f"re-run with --record --master <profile.yaml>", file=sys.stderr)
        return 2
    master = pathlib.Path(fp["path"])
    findings = []
    master_profile, readable = {}, False
    if not master.exists():
        findings.append(f"MASTER_MUTATED: {master} no longer exists — the master "
                        f"profile is never mutated by tailoring")
    else:
        now = journal.sha256_file(master)
        try:
            master_profile = journal.load_yaml(master)
            readable = True
        except journal.YamlUnreadable as exc:
            # The gate compares against PARSED fields, so a master it cannot parse
            # is a gate that verified nothing. Say that, and do not then emit an
            # UNSOURCED line for every term in the CV: a flood derived from a file
            # nobody could read is noise, and noise is what makes findings ignorable.
            #
            # A finding rather than exit 2, and that is the deliberate divergence:
            # the master lives OUTSIDE the workspace, MASTER_MUTATED and
            # MASTER_TOUCHED below are findings about that same file, and the other
            # half of this gate — the claims index, the tailored profile — still has
            # something to say. `readable` stays False, so nothing downstream treats
            # the empty mapping as a verified master.
            findings.append(f"MASTER_UNREADABLE: {exc.reason} — no claim was verified "
                            f"against {master}; fix the master and re-run")
        chain = _writeback_chain(ws, master, fp["sha256"], now) if now != fp["sha256"] else None
        if chain:
            ids, last_date = chain
            findings.append(f"MASTER_WRITEBACK: {master} gained {len(ids)} confirmed "
                            f"online-presence item(s) on {last_date} ({', '.join(ids)}); tell "
                            f"the user what was added, then re-run check_claims.py --record "
                            f"--master {master}")
        elif now != fp["sha256"]:
            findings.append(f"MASTER_MUTATED: profile.yaml content changed during this "
                            f"run ({fp['sha256'][:12]}… → {now[:12]}…) — the master "
                            f"profile is never mutated by tailoring; tailoring works on "
                            f"the workspace copy")
        elif master.stat().st_mtime_ns != fp.get("mtime_ns"):
            findings.append(f"MASTER_TOUCHED: profile.yaml's mtime changed during this "
                            f"run though its content is identical — something wrote to "
                            f"the master; confirm nothing is editing it")

    # Both exit 2, unlike the master above, and for the reason the master is the
    # exception: these two ARE the comparison. A claims.yaml that is present and
    # unreadable is not the same as one that is absent — absent honestly means
    # "nothing was sourced" and every UNSOURCED line that follows is true, while
    # unreadable would print that same flood about a file that may well have sourced
    # every one of them.
    try:
        tailored = journal.load_yaml(tailored_path)
        claims_path = ws / "claims.yaml"
        claims = (journal.load_yaml(claims_path, expect=list)
                  if claims_path.exists() else [])
    except journal.YamlUnreadable as exc:
        journal.receipt(ws, GATE, {}, "could_not_run", [exc.finding])
        print(f"cannot run {GATE}: {exc}", file=sys.stderr)
        return 2
    live, retracted, claim_findings = _claim_index(claims)
    findings += claim_findings

    exact, prose, families = master_sources(master_profile)
    # No readable master, nothing to check against: the MASTER_* finding above is
    # the answer, and it already fails the gate.
    for term, where, family in (atomic_claims(tailored) if readable else []):
        key = normalize_term(term)
        if not key:
            continue
        paired, others = pairing(where, tailored, master_profile)
        verdict = trace(term, family, paired, exact, prose, families, others)
        if verdict is None or key in live:
            continue
        rel, leaf, detail = verdict
        # The master's real name, not the literal 'profile.yaml', in every line
        # below: one candidate can have several masters now, and a finding that
        # names the wrong file sends the reader to a document the gate never read.
        if rel == QUALIFIER and detail[0] == "seniority":
            findings.append(f'QUALIFIER_STRIPPED: "{term}" at '
                            f'tailored-profile.yaml:{where} drops the seniority '
                            f'qualifier "{detail[1]}" off {master.name}\'s '
                            f'"{leaf}" — without it the title claims a more senior '
                            f'post than the one held. Keep the qualifier, or add a '
                            f'claims.yaml row for the fact that it no longer '
                            f'applies (a promotion, for instance)')
            continue
        if rel == QUALIFIER:
            reads_as = ("an accepted, published paper" if family == "publications"
                        else "a completed, current credential")
            findings.append(f'QUALIFIER_STRIPPED: "{term}" at '
                            f'tailored-profile.yaml:{where} drops the status '
                            f'qualifier "{detail[1]}" off {master.name}\'s '
                            f'"{leaf}" — the unqualified form reads as {reads_as}. '
                            f'Keep the qualifier, or add a '
                            f'claims.yaml row for the fact that it no longer applies')
            continue
        if rel == TRUNCATED:
            findings.append(f'ORG_TRUNCATED: "{term}" at '
                            f'tailored-profile.yaml:{where} shortens {master.name}\'s '
                            f'"{leaf}" — an employer or institution name may drop a '
                            f'legal-form or group suffix (BV, GmbH, Inc., Group, '
                            f'Holdings, 有限公司, 株式会社 …) or the sub-unit after its '
                            f'first comma, and nothing else, because a shorter name '
                            f'can name a different, larger organisation than the '
                            f'one the candidate belonged to. Use the full name, or '
                            f'add a claims.yaml row')
            continue
        if rel == BORROWED:
            findings.append(f'TITLE_FROM_OTHER_ENTRY: "{term}" at '
                            f'tailored-profile.yaml:{where} is what {master.name} '
                            f'records for a different entry ("{detail}"); the entry '
                            f'it is written on, paired by its dates and its '
                            f'employer, institution or project name, is "{leaf}" '
                            f'— a title, degree or role '
                            f'belongs to the entry it was held on, and moved onto '
                            f'another it claims a post at a time or place the '
                            f'candidate did not hold it. Restore "{leaf}", or add a '
                            f'claims.yaml row (a retitled post, for instance)')
            continue
        if key in retracted:
            findings.append(f'RETRACTED_CLAIM: "{term}" at '
                            f'tailored-profile.yaml:{where} is backed only by a '
                            f'claims.yaml row marked retracted: '
                            f'{retracted[key]["retracted"]} — remove the claim or '
                            f're-source it')
            continue
        findings.append(f'UNSOURCED: "{term}" appears in '
                        f'tailored-profile.yaml:{where}, is absent from '
                        f'{master.name}, '
                        f'and has no claims.yaml row. A keyword that appears in the job '
                        f'description is not evidence the candidate has it — source it '
                        f'or move it to HONEST-GAPS')

    for f in findings:
        print(f)
    journal.receipt(ws, GATE,
                    {"tailored-profile.yaml": journal.sha256_file(tailored_path)},
                    "fail" if findings else "pass", findings)
    return 1 if findings else 0


if __name__ == "__main__":
    from cli_io import configure_output

    configure_output()
    sys.exit(main())
