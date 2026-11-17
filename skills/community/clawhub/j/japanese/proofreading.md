# Proofreading — Reviewing Japanese Someone Else Wrote

Reviewing is a different job from writing: the text has an author, a purpose and a house style that all outrank preference. **Before reviewing anything**, read `conventions.hyoki` in `~/Clawic/data/japanese/config.yaml`, `### Corrections` in `memory.md`, and any house sheet `## Boxes` names (`artifacts/hyoki-house-rules.md`) — correcting a text toward a rule the house has already rejected is worse than not reviewing it.

**Contents:** [校正 and 校閲](#校正-and-校閲) · [The Pass Order](#the-pass-order) · [変換ミス](#変換ミス) · [表記ゆれ](#表記ゆれ) · [The Keigo Audit](#the-keigo-audit) · [Verifying Numbers, Names and Dates](#verifying-numbers-names-and-dates) · [Encoding](#encoding) · [What a Non-Native Can Flag](#what-a-non-native-can-flag) · [Delivering the Review](#delivering-the-review) · [校正記号](#校正記号) · [Reviewing Your Own Text](#reviewing-your-own-text) · [What Gets Written Down](#what-gets-written-down)

## 校正 and 校閲

Japanese publishing separates two jobs and hires two people:

- **校正** — the text against itself and against the proofs: typos, 変換ミス, 表記ゆれ, typography, layout, 禁則, whether the corrections from the previous round were applied.
- **校閲** — the text against the world: facts, names, dates, figures, quotations, legal exposure, whether the 主張 survives its own evidence.

Say which one is being delivered. A 校正 pass that silently rewrites an argument oversteps, and a 校閲 pass that ignores a 変換ミス has not finished. Most requests to review Japanese want both, and the two produce different lists.

## The Pass Order

Ten passes, in this order. The order is load-bearing: each pass can invalidate the work of any pass after it, and none of them can invalidate a pass before it.

1. **Encoding and rendering.** Mojibake, 半角カナ, missing 旧字体, broken 〜 or ¥. Fixing style in a text that is about to be re-exported wastes the pass (`punctuation.md`).
2. **Completeness.** Missing sections, an unresolved placeholder, a 記 without its 以上, a subject line that no longer matches the body.
3. **表記ゆれ inventory.** Build the list before changing anything; a single decision resolves dozens of instances (below).
4. **変換ミス.** Homophones, which no spell-checker catches because every candidate is a real word.
5. **Politeness level.** One rung end to end, no 敬体/常体 mixing outside the named exceptions (SKILL.md Rule 1). A level change forces rewrites, so it precedes any sentence-level work.
6. **Keigo audit.** Direction, marker count, させていただく, うち/そと (below).
7. **Grammar.** は/が, particles, transitivity, modifier stacks, 読点 placement (`grammar.md`).
8. **Numbers, names, dates.** Verified against a source, not corrected from memory (below).
9. **Typography.** Full-width marks, ……, ――, 「」, spacing, 禁則.
10. **Rhythm and machine tells.** Sentence-length spread, ending variety, hedges, scaffolding (`ai-tells.md`).

Then read the whole thing aloud once. Anything a native would not say out loud is the last item on the list.

## 変換ミス

The IME picks a real word from the same reading, so the error survives every automated check and reads as carelessness rather than as foreignness. This table is the sweep; the ones that change an obligation are marked.

| Reading | Candidates | Distinction |
|---|---|---|
| いがい | 以外 / 意外 | Other than / unexpected |
| ほしょう | 保証 / 保障 / 補償 | **Guarantee / safeguard / compensate — changes the obligation in a contract** |
| せいさく | 制作 / 製作 | Creative work / manufacturing |
| たいしょう | 対象 / 対照 / 対称 | Target / contrast / symmetry |
| ついきゅう | 追求 / 追及 / 追究 | Pursue a goal / pursue responsibility / investigate |
| はやい | 早い / 速い | Early / fast |
| はかる | 図る / 計る / 測る / 諮る / 謀る | Plan / count / measure / consult a body / plot |
| おさめる | 収める / 納める / 治める / 修める | Store / deliver-pay / govern / master |
| かえる | 変える / 換える / 替える / 代える | Change / exchange / replace / substitute |
| つとめる | 務める / 努める / 勤める | Serve in a role / make an effort / be employed |
| すすめる | 進める / 勧める / 薦める | Advance / advise / recommend a candidate |
| あらわす | 表す / 現す / 著す | Express / reveal / author |
| きく | 聞く / 聴く / 訊く | Hear / listen / ask (訊く is outside 常用漢字) |
| みる | 見る / 観る / 診る / 看る | See / watch / examine medically / care for |
| かたい | 硬い / 固い / 堅い | Hard / firm / solid-reliable |
| いどう | 移動 / 異動 | **Physical move / personnel transfer — an HR notice inverts** |
| せいさん | 精算 / 清算 / 生産 | **Settle an amount / wind up an account / produce** |
| ようけん | 用件 / 要件 | The business at hand / a requirement |
| きてい | 規定 / 規程 | **A provision / a set of rules as a document** |
| とくちょう | 特徴 / 特長 | Distinguishing feature / advantage |
| たいせい | 体制 / 態勢 / 体勢 | Structure / readiness / physical posture |
| かいとう | 回答 / 解答 | A reply / an answer to a problem |
| しょうかい | 紹介 / 照会 | Introduce / make an enquiry |
| しょよう | 所用 / 所要 | Personal business / required (所要時間) |
| てきせい | 適正 / 適性 | Appropriate / aptitude |
| おくる | 送る / 贈る | Send / give as a gift |
| かいほう | 開放 / 解放 | Open up / set free |
| いし | 意志 / 意思 | Will, determination / intention in the legal sense |
| かてい | 過程 / 課程 | Process / curriculum |
| はじめて | 初めて / 始めて | For the first time / having started |
| さいご | 最後 / 最期 | Last / the end of a life — **the 慶弔 trap** |
| こうえん | 公演 / 講演 / 後援 | Performance / lecture / sponsorship |
| かんしん | 関心 / 感心 / 歓心 | Interest / admiration / someone's favour |
| せいちょう | 成長 / 清聴 / 静聴 | Growth / attentive listening / silent listening (`speaking.md`) |

The first check in any business or legal text is 保証/保障/補償, then 移動/異動, then 精算/清算. Those three appear in contracts, HR notices and invoices, and the wrong one is actionable rather than embarrassing.

## 表記ゆれ

Orthographic drift inside one document. Nobody notices a single instance; everyone notices the second form on page three.

The classes, and what to inventory:

| Class | Example drift |
|---|---|
| 送り仮名 | 行う / 行なう · 申し込み / 申込み / 申込 · 受付 / 受け付け |
| ひらく or とじる | ください / 下さい · いただく / 頂く · こと / 事 · できる / 出来る |
| Katakana long vowel | サーバ / サーバー · ユーザ / ユーザー · インタフェース / インターフェース |
| Script for a term | ウェブ / Web / WEB · メール / mail · Eメール / eメール |
| 全角 / 半角 | Digits, Latin letters, brackets, the space around Latin runs |
| Number notation | 1つ / 一つ · 30% / 3割 · 1,200,000 / 120万 |
| Terminology | ユーザー / 利用者 / お客様 for the same person |
| 敬称 | 様 in the 宛名 and さん in the body |
| Dates | 2026年7月26日 / 2026/7/26 / R8.7.26 |
| Units | 円 / ¥ / ￥ · % / パーセント · か月 / ヶ月 / カ月 |

The procedure, and it is the same every time:

1. **Inventory first.** List every term that appears in two forms, with a count of each. Do not fix anything during this pass.
2. **Decide once per term**, in this precedence: the client's or house sheet → `conventions.hyoki` → 常用漢字表 and 記者ハンドブック-style convention → the form already dominant in the document.
3. **Apply to every occurrence**, including headings, captions, alt text, filenames in the body, and the subject line.
4. **Record the decision** in `conventions.hyoki` so the next document starts settled.

Japanese editorial workflows lean on 校正 tooling for exactly this class (the checker built into 一太郎 and Word's Japanese proofing, and dedicated products used by publishers and corporate 広報); they catch 表記ゆれ and some 二重敬語 mechanically and they do not catch the homophone table above. Treat a tool report as pass 3, never as the review.

## The Keigo Audit

Run `keigo.md`'s Denial Diagnostic over every honorific in the text, in that order. Three counts are worth taking mechanically before reading for sense:

- **Markers per verb.** More than one is 二重敬語 — お読みになられる, ご覧になられる. The naturalised exceptions are the closed list in `keigo.md`.
- **させていただく instances.** Each has to pass both conditions (SKILL.md Rule 3). Three in one email is the pattern that reads as evasive regardless of whether each instance is defensible.
- **敬称 stacking.** 田中部長様, 各位様, 御中様, 株式会社◯◯様 (`register.md`).

Then the two that need judgement: **direction** (尊敬語 on the writer's own action is the error that survives every polish) and **うち/そと** (a 部長 given his title in a message to a customer).

## Verifying Numbers, Names and Dates

This is 校閲, and it is verification against a source — never correction from memory.

- **Every figure recomputed** from its own formula: unit price × quantity × months, tax status stated, total matching.
- **万/億 grouping** consistent with the document's own convention, and no seven-digit comma figure inside prose (`numbers-and-names.md`).
- **Era arithmetic**: 令和 year = western − 2018, and a transition year (2019, 1989) checked against its month.
- **年度 vs 年**: 2026年度第4四半期 is January-March 2027.
- **曜日 against the calendar.** A deadline with the wrong day of the week is the error Japanese business readers catch fastest.
- **Names character by character** — 髙 vs 高, 﨑 vs 崎, 邊 vs 邉 — against the person's own signature, plus the reading if the document carries ふりがな.
- **Company names** for 前株/後株 and full 株式会社 (`business.md`).
- **Quotations and titles** against the original, including whether 『』 or 「」 is correct for the work type.
- **忌み言葉** in anything ceremonial, checked before anything else in that document (`documents.md`).

## Encoding

The receipts, in the order they usually appear (`punctuation.md` has the symptom table): charset declared and consistent · no 半角カナ · 〜 rendering correctly or replaced with から · ¥ not appearing as a backslash · 機種依存文字 (①, ㈱, ℡, ㎡) flagged if the text crosses a mail gateway or a border · CSV exports saved as UTF-8 with BOM if Excel will open them · 旧字体 surviving the target font.

A file that will be printed, mailed and posted to the web needs the check three times — the failures are per-pipeline, not per-text.

## What a Non-Native Can Flag

Being explicit about this is what makes a review trustworthy rather than presumptuous.

| Flag with confidence | Needs a native reader |
|---|---|
| Typography and 全角/半角 | Whether a sentence sounds natural |
| 表記ゆれ and 送り仮名 consistency | Collocation: whether this verb takes this noun |
| Digit, date and 曜日 arithmetic | Whether a refusal is too blunt or too soft |
| 二重敬語 count and 敬称 stacking | Whether a joke lands |
| Honorific direction (whose action) | Whether a dialect line is right for its region |
| Counter/noun mismatch | Whether a slang term is current |
| 忌み言葉 presence | Nuance between two near-synonyms |
| Missing 記/以上, 名乗り, 曜日 | Whether the text sounds like this author |

For the right column, say so: 「ここは私では判断がつかないので、ネイティブの方にご確認ください」 is a professional sentence, and guessing there is how a review loses its authority for the left column too.

## Delivering the Review

- **Never rewrite silently.** Original → suggestion → one-line reason. The author has to be able to reject an item without unpicking the rest.
- **Three tiers, labelled**: 要修正 (wrong — a fact, an honorific direction, a name, a figure) · 推奨 (convention and consistency — 表記ゆれ, typography, level) · 好み (style preference, and it is offered once and not argued).
- **Batch by class, not by line number.** A writer fixes all 表記ゆれ in one pass and all keigo in another; a list ordered by position makes them switch modes forty times.
- **Give the counts** ("送り仮名: 行う/行なう mixed, 11 vs 3 — recommend 行う"). A count is what turns a preference into a decision.
- **Do not touch quoted material, a supplied house sheet, or the author's name for their own things.** Flag, never edit.
- **When the author is senior or a native speaker**, judgement calls go out as questions (〜という理解でよろしいでしょうか) and mechanical items go out as findings. The tier labels do this work for you.
- **State what was not checked** — facts, legal exposure, the numbers against their source — so the absence is a decision and not an omission.

## 校正記号

The standard proof marks (JIS Z 8208) still used on paper and PDFs, and the vocabulary that comes with them:

| Mark / word | Means |
|---|---|
| 赤字 / 赤入れ | The corrections themselves |
| トル | Delete |
| トルツメ | Delete and close the gap |
| トルアキ | Delete and leave the space |
| イキ | Stet — restore what was marked for deletion |
| ママ | Leave as the author wrote it; deliberate |
| ○字アキ / ツメ | Insert / remove that much space |
| 版面 / ノンブル / 柱 | Type area / page number / running head |
| 初校 · 再校 · 責了 · 校了 | First proof · second proof · approved subject to final fixes · approved |

責了 (approved on condition the remaining fixes are made without another round) is the one that matters commercially: it ends the review loop, and saying it means accepting whatever is left.

## Reviewing Your Own Text

The same list, minus the things you cannot see in your own writing. Three that work:

- **Read it aloud.** Catches rhythm, keigo chains and modifier stacks that the eye reads past.
- **Change the medium.** Paper, a different font, or 縦書き surfaces 表記ゆれ that is invisible in the editor it was written in.
- **Sweep for one class at a time**, in the pass order above. Reading for everything at once finds nothing.

And the one that is not optional in this domain: **check the name and the number before you check anything else**, because those are the two errors a reader cannot un-see.

## What Gets Written Down

Destinations, all in `memory-template.md`:

- **A review delivered on someone else's text** → `artifacts/review-<what>.md` with the date, the three tiers as they were sent, and what the author accepted. Its `## Boxes` line goes in the same turn. The accepted/rejected split is what calibrates the next review for the same author.
- **Every 表記 decision made during the pass** → `conventions.hyoki` in `config.yaml`. A review that settles ten terms and records none has to be repeated in full next month.
- **A correction the author or a native reviewer made to your review** → `### Corrections`, with who said so. Being wrong about a rule is the cheapest lesson available and only if it is written down.
- **A house or client style sheet received during the job** → `artifacts/hyoki-house-rules.md`, saved as given, with source and date.
- **A pipeline quirk found while checking encoding** — a CMS that strips 全角 spaces, an export that reintroduces 半角カナ → `## Environment`.
