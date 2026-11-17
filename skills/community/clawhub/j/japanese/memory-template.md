# Working File Templates — Japanese

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — table keys and preference areas alike | `~/Clawic/data/japanese/config.yaml` | Key by key, read-modify-write |
| Who they write to and at what level, which channels they write on, environment facts, pain points, box index, due dates | `~/Clawic/data/japanese/memory.md` | Rewritten in place; stays small |
| Terms, product names and their katakana rendering; items kept in Latin script; confirmed readings of people's and places' names; corrections from native readers; slang retired as stale | `## Glossary` in `memory.md` until it outgrows it, then `~/Clawic/data/japanese/glossary.md` | One row per term or name |
| A channel's long-form voice guide — level, opener and closer, emoji density, line-break shape, worked examples | `~/Clawic/data/japanese/styles/<channel>.md` | Born as its own file the first time a channel's rules pass one line |
| A character's voice sheet for fiction, manga, games or dubbing — 一人称, 語尾, politeness toward each other character | `~/Clawic/data/japanese/characters/<name>.md` | One file per character, from the first one |
| Pieces delivered: date, channel, reader, what it was, how it landed | `~/Clawic/data/japanese/pieces/<year>.md` | Append-only, cut by year |
| Things you produced that get re-read — templates that worked (ビジネスメール定型, 退職願, 議事録, 年賀状, 自己紹介, 乾杯の挨拶), Japanese naming decisions, reviews of someone else's text, speech and presentation scripts with ルビ, 用字用語 house sheets, 擬音語 banks for one project, 敬語 cheat-sheets for a role, headline banks | `~/Clawic/data/japanese/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| A recipient, native reviewer, client, 取引先, editor or teacher | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, every skill's contacts in one file |
| A Japanese-language effort tracked as work in progress — a note blog, a 転職 search, a manga volume, a market entry, a thesis | `~/Clawic/data/projects/<project>.md` (**shared**) | One file per project |
| **Anything durable this table does not name** | `~/Clawic/data/japanese/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

Three questions decide anything not listed, in order: would another skill want to read it (→ a shared box); is it a text read whole when its subject comes up (→ `artifacts/`); is it one more row of something accumulating (→ a `memory.md` section until the threshold).

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A term or product name got a Japanese or katakana rendering for the first time | Its row in `### Terms` |
| Something must stay in Latin script (a brand, a product code, an acronym the team uses) | `### Keep In Latin` |
| A person's, company's or place's name reading was confirmed — from a signature, a 名刺, or by asking | `### Name Readings`, with where the reading came from |
| A native reader, reviewer or the user corrected a rendering, a particle, an honorific or a level | `### Corrections`, with the accepted form and who said so |
| A slang term was judged stale, or one was adopted | `### Retired Slang`, with the year it peaked |
| The honorific and politeness level for a person were settled | `## Recipients`, keyed by their contacts key |
| A channel's voice was settled | `## Channels`; anything longer than a line goes to `styles/<channel>.md` |
| A character's voice was fixed for a story, a game or a dub | `characters/<name>.md` |
| A piece was delivered — a post, an email, a document, a speech | A row in `pieces/<year>.md`, with how it landed if that is known |
| A template, a naming decision, a review of someone's text, a script, a 用字用語 sheet or a 擬音語 bank came out of the session | `artifacts/` |
| Something about the setup cost effort to find — a form that only accepts 全角カナ, a system that mangles 〜 or ¥, a mail client that breaks 絵文字, a reader older than assumed, a character limit | `## Environment` |
| Something landed badly — a wrong level, a misread name, a joke that did not travel | `## Pain Points`, with the cause |
| A recipient, reviewer, 取引先 or teacher was named | The shared contacts box |
| The user declared a preference, including a 表記 decision | Its key in `config.yaml` |
| Recurring or seasonal work was scheduled or run | `## Due` |

## Start flat, split only when it hurts

Everything except style guides, character sheets, the pieces log, artifacts and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, promoted one level (`### Terms` inside `memory.md` becomes `## Terms` in `glossary.md`), so the split is a copy-paste and never a rewrite.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

`### Name Readings` has one extra trigger: **it splits on its own the moment the glossary splits**, into `## Name Readings` inside `glossary.md`, and never stays behind in `memory.md`. A reading looked up twice has already cost more than the row would have.

Style guides, character sheets, artifacts and the pieces log are the exception to counting: a channel voice guide, a character's 語尾, a template or a naming decision is born as its own file whatever its size, because it is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. Store the pointer in its place, in this shape: `<kind>:<locator>`.

`env:LINE_CHANNEL_SECRET` · `keychain:note-login` · `1password:Work/X/ops` · `bitwarden:Personal/LINE` · `file:~/.config/app/session`

When the user pastes something to save — a platform API config, an account handover note, a 社内 wiki page with a login in it — replace each secret value before writing and leave the pointer visible: `channel_secret: <env:LINE_CHANNEL_SECRET>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: names and their readings, 敬称 and 役職, company and 部署 names, handles and account names, group names, city and 都道府県 names, post URLs, follower and 文字数 counts, prices with their currency, invoice numbers. **Secrets, strip them**: platform app secrets and access tokens, account passwords, verification codes, マイナンバー, 基礎年金番号, full bank account and 口座 numbers, 印鑑登録 numbers, private phone numbers and home addresses the user has not asked to keep, anything inside a pasted config or `.env`.

One rule that is not about credentials: **a piece of writing often carries someone else's private business** — a 退職願 names a reason, a 忌引 message names a death, a 始末書 names a failure. Keep the template and the level decision, not the personal detail; if a full text must be kept as a reference, strip the names and the reason and say so.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [glossary.md](#glossarymd) · [styles/](#styles) · [characters/](#characters) · [pieces/](#pieces) · [artifacts/](#artifacts) · [shared contacts](#shared-contacts) · [shared projects](#shared-projects) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/japanese/` if it does not exist.

```yaml
politeness_default: auto
first_person: watashi
default_honorific: auto
kanji_density: standard
okurigana_rule: joyo
punctuation_style: 、。
text_direction: horizontal
numerals: mixed
era_dates: western
dialect: standard
slang_appetite: light
default_channel: slack
emoji_density: sparse
furigana: none
romaji_gloss: none
crude_ok: false

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
conventions:
  hyoki:                      # 表記ゆれ, settled once and applied everywhere
    ください: kana            # not 下さい
    サーバー: long-vowel      # not サーバ
    ウェブ: katakana          # not Web
  latin_spacing: true         # half-width space between Japanese and Latin
  paragraph: indent           # 全角一字下げ, not blank-line separation
voice:
  company_self: 弊社          # not 当社
  taigen_dome: welcome        # 体言止め allowed for rhythm
risk_posture:
  direct_disagreement: "soften upward, plain with peers"
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Japanese Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Glossary (41 terms, 18 readings) → `glossary.md`; read before writing any product, team or customer copy
- note voice → `styles/note.md`; read before any note article
- LINE voice → `styles/line.md`; read before any LINE message
- Pieces 2026 (33) → `pieces/2026.md`; read when asked what was sent to whom, or before reusing a piece
- ビジネスメール template → `artifacts/template-business-email.md`; read before any 社外 email
- Product name decision → `artifacts/naming-product-ja.md`; read before any Japanese marketing copy
- 用字用語 sheet → `artifacts/hyoki-house-rules.md`; read before proofreading anything long

## Due
| What | Every | Last run | Next due |
|---|---|---|---|
| Re-calibrate the slang list against what the reader actually uses | 6 months | 2026-03-02 | 2026-09-02 |
| Native review of the channel style boxes | quarter | 2026-05-10 | 2026-08-10 |
| Glossary consolidation: one rendering per term, one reading per name | quarter | 2026-04-18 | 2026-07-18 |
| 年賀状 list and text | year, drafted by 12-15 | 2025-12-14 | 2026-12-15 |
| 暑中見舞い window (梅雨明け〜立秋) | year, July | 2026-07-20 | 2027-07-20 |
| Re-check platform limits after a policy change | on change | 2026-06-01 | on change |

## Profile
Writing as: プロダクトマネージャー at a Tokyo SaaS company, not a native speaker, reads fluently.
Readers: 社内 colleagues 25-45 on Slack, 社外 customers by email, a note audience of practitioners.
Standard: 共通語, no dialect. 弊社 in writing, 私 as 一人称.

## Recipients
| Contact key | Relationship | Honorific | Level | Notes |
|---|---|---|---|---|
| tanaka@example.co.jp | 部長, two levels up | 田中部長 | 敬語 | 承知しました, never 了解; he writes 常体 downward, that does not invite reciprocity |
| sato@example.co.jp | peer, same team | 佐藤さん | 丁寧 | Slack, 絵文字 reactions as ack; opened with 常体 first |
| kobayashi@acme.co.jp | 取引先 窓口 | 小林様 | 敬語 | 御社/弊社; reading is こばやし, confirmed from 名刺 |

## Channels
| Channel | Level | Address | Emoji | Notes |
|---|---|---|---|---|
| Slack 社内 | 丁寧 | 姓 + さん | reactions only | no 。 on one-line messages, no bolding |
| Email 社外 | 敬語 | 姓 + 様 | none | full guide in `styles/email.md` |
| LINE friends | 親しい | name alone | native | no final 。 (マルハラ), スタンプ freely |

## Glossary
### Terms
| Source | Japanese | Script | Part of speech | Context / why | Set on |
|---|---|---|---|---|---|
| workspace | ワークスペース | katakana | noun | matches the UI label; never 作業領域 | 2026-03-11 |
| onboarding | 導入 | kanji | noun | 入社 only when it means a new employee | 2026-04-02 |
| dashboard | ダッシュボード | katakana | noun | long vowel kept, per `okurigana_rule` house line | 2026-04-02 |

### Keep In Latin
Acme · Acme Cloud · SaaS · API · error codes `ACM-###` · CSV

### Name Readings
| Written | Reading | Who / what | Honorific | Source | Date |
|---|---|---|---|---|---|
| 東海林 | しょうじ | 取引先 営業 | 東海林様 | 名刺 | 2026-05-02 |
| 田中 一 | たなか はじめ | 部長 | 田中部長 | asked directly | 2026-03-11 |
| 日本橋 | にほんばし | office address | — | 会社 site | 2026-03-11 |

### Corrections
| Wrong | Right | Who said so | Why | Date |
|---|---|---|---|---|
| 了解しました | 承知しました | 佐藤さん | 部長宛には避ける、社内の慣行 | 2026-03-20 |
| ご確認させていただきます | ご確認いたします | 佐藤さん | させていただく inflation; no permission involved | 2026-04-02 |

### Retired Slang
| Term | Peaked | Verdict | Date |
|---|---|---|---|
| ぴえん | 2020 | retired — reads as forced on this reader | 2026-03-02 |
| エモい | 2016 | keep — crossed into ordinary vocabulary | 2026-03-02 |

## Environment
The 社内 経費 form only accepts 全角カナ in the name field. The customer's mail system renders 〜 (波ダッシュ) as
a broken glyph, so ranges are written with 「から」. note's editor strips consecutive blank lines. The 名刺 scanner
gets 旧字体 wrong (髙 → 高) and the 取引先 notices.

## Pain Points
2026-02: a 社外 email went out with 了解しました and 〜させていただきます three times; read as both curt and
evasive at once. Every 社外 email now goes through the Politeness Ladder and the させていただく test explicitly.

## How They Work
Wants the Japanese and nothing else, then a one-line note on anything risky. Reads the explanation only if the
Japanese surprises them.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. `on change` is a valid cadence: it fires on the named event, not on a date. Japanese has real seasonal deadlines — 年賀状 has to be posted for 元日 delivery (日本郵便 announces the date each December, usually around the 25th), 喪中はがき goes out before anyone starts writing 年賀状, and 暑中見舞い has a window that closes at 立秋 — and a seasonal greeting sent late is worse than one not sent.
- **`## Recipients`**: identity is the **contacts key**, so the person is not duplicated — their name, role and channel live in the shared contacts box and only the Japanese-specific columns live here. One row per person, never per message. The `Honorific` column holds the exact string used in a greeting (田中部長, 小林様), because that is what gets pasted. A row that needs a paragraph is a `styles/` file waiting to be created.
- **`## Channels`**: one row per channel, and the row is a summary of the style box, never a replacement for it.
- **`### Name Readings`** is the section that pays for this file. A reading cannot be derived from the characters — 東海林 is しょうじ, 小鳥遊 is たかなし — and getting it wrong in a greeting or a 宛名 is a visible insult. Always record the source: a reading from a 名刺 or from the person outranks anything inferred.
- **`### Corrections`** is the second: a native correction that is not written down gets re-earned by making the same mistake in front of the same person. Always record who said so — a correction from the actual reader outranks every general rule in this skill.
- **`### Retired Slang`** keeps the verdict *and* the peak year, because "retired" without a date is unreviewable when the same term comes back as ironic usage.
- **`## Environment`** holds facts that change future decisions, in prose. Incidents go to `## Pain Points`.

| Status | Meaning |
|---|---|
| `ongoing` | Still learning their readers, level and vocabulary |
| `complete` | Level per recipient, channel voices and 表記 rules all settled |

## glossary.md

Created by the split procedure above, at `~/Clawic/data/japanese/glossary.md`. Keeps the five headings it had inside `memory.md`, promoted one level: `## Terms`, `## Keep In Latin`, `## Name Readings`, `## Corrections`, `## Retired Slang`.

- **Identity is the source term plus its part of speech** for `## Terms`, and the **written form plus the person or thing it belongs to** for `## Name Readings` — the same characters are read differently by two different people, and both rows are correct.
- Read the file before adding. If the term is there, do not add a second row: either the new context justifies a part-of-speech row, or the existing row is wrong and gets corrected in place with a new `Set on` date.
- A rendering that changes never disappears — it moves to `## Corrections` with the new form, so old text can be found and fixed.
- Katakana renderings are the ones that drift: サーバ/サーバー, ユーザ/ユーザー, インタフェース/インターフェース are all defensible and only one can be the house rule. Whichever is chosen goes in `config.yaml` under `conventions.hyoki` and the glossary row records it once.
- Past ~200 terms the file stops being readable in one pass; split by domain (`glossaries/product.md`, `-legal.md`) and leave `glossary.md` as the index with the same headings.

## styles/

One file per channel, at `~/Clawic/data/japanese/styles/<channel>.md`, created the first time a channel's rules outgrow a single line in `## Channels`. Read whole, before writing anything for that channel.

```markdown
# Style — note

*Read before any note article. Updated 2026-06-02.*

Level: 丁寧, です・ます throughout, 一人称 私.
Title: 30 characters or fewer, the concrete result in the first 15 — note truncates in the feed.
Body: 2-4 sentences per paragraph, blank line between; 見出し every ~400 字.
Kanji: standard density; ください and いただく always open (`conventions.hyoki`).
Slang: none. 専門用語 explained once, then used.
Closing: one question to the reader, then 3-5 ハッシュタグ, most specific first.
Worked opener: 半年で解約率を12%下げた、たった一つの設定変更の話です。
Do not: いかがでしたか, まとめ as a heading, ！, bolded 単語 mid-sentence.
```

If the user supplies their own style guide, 表記ルール or brand book, save it here under the same name, record the source and date at the top, and do not rewrite it in your words.

## characters/

One file per character, at `~/Clawic/data/japanese/characters/<name>.md`, from the first one. Used for fiction, manga, games, dubbing and any project where a voice has to stay identical across sessions and across files. Read before writing any line that character speaks.

```markdown
# Character — ミナ

*Read before any ミナ line. Updated 2026-07-02.*

一人称: うち (あたし only when rattled, never 私)
二人称: name + 呼び捨て to peers, あんた when annoyed
語尾: 〜じゃん, 〜っしょ, 〜んだけど; never 〜わ, never 〜のよ
Politeness: 常体 with everyone except 先生 (丁寧, and it is a joke between them)
Register drift is a plot event: she uses です・ます exactly twice in the story, both times in ch. 7
Vocabulary: short, concrete, 擬態語-heavy (`onomatopoeia.md`); no 漢語 above 常用
Do not: give her 役割語 markers of お嬢様 or ギャル — the point is that she reads as neither
```

- Identity is the character name, which is the filename. One file per character, never a table of all of them: a voice sheet is read whole, right before writing that character.
- Record the **relationships**, not just the voice: who she uses 敬語 with is a fact about the story, and it is the one that breaks first when two sessions write different chapters.
- A voice that changes on purpose gets the change and the scene recorded in the same file, so the drift is intentional and reviewable.

## pieces/

```markdown
# Pieces — 2026

| Date | Channel | Reader | What | Length | Level | How it landed |
|---|---|---|---|---|---|---|
| 2026-07-14 | note | practitioners | 解約率を下げた設定の話 | 2,400 字 | 丁寧 | 1.2k views, 3 コメント asking for the numbers |
| 2026-07-21 | email | 小林様 (acme) | 納期延期のお詫びと再提示 | 8 sentences | 敬語 | accepted, no pushback |
```

- `Length` is in 字 for written Japanese, so two rows are comparable; a spoken script records its minutes instead (`3分`) in the same cell.
- `How it landed` is the column that earns this file: without it the log is a diary, with it the next piece for the same reader starts from evidence.
- Cut by year. A year past ~150 rows splits by quarter (`pieces/2026-q3.md`), leaving `2026.md` as an index table (`Date | Channel | What | → file`).

## artifacts/

One file per thing, at `~/Clawic/data/japanese/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **a template that worked** (`template-<what>.md` — ビジネスメール, 退職願, 議事録, 稟議書, 年賀状, 自己紹介, 乾杯の挨拶, お礼状, 始末書), **a Japanese naming decision** (person, product, company, katakana rendering), **a review of someone else's text**, **a speech or presentation script** with its ルビ and pause marks, **a 用字用語 house sheet**, **a 擬音語 bank** for one project, **a 敬語 cheat-sheet** derived for one role, **a headline bank**, **a slang calibration snapshot**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Template — 社外ビジネスメール

*Read before any 社外 email. Written 2026-05-12, accepted by 小林様 unchanged.*

株式会社◯◯
◯◯部　◯◯様

いつも大変お世話になっております。
株式会社△△の（氏名）でございます。

（用件を一文で）

（詳細。一文40〜60字、箇条書きは行頭に「・」）

お手数をおかけいたしますが、何卒よろしくお願いいたします。

--
署名
```

Notes on this one: 宛名 is 会社 → 部署 → 個人名+様, never 様 on the 会社 line. 名乗り comes before the 用件, always. 何卒 in the 結び is 敬語-level; 丁寧-level uses よろしくお願いいたします without it.

```markdown
# Naming decision — product name in Japanese

*Read before any Japanese marketing or store copy. 2026-05-30.*

Decision: keep the Latin brand, add a katakana reading in parentheses on first mention only.
Rejected: full katakana as the primary form — collides with an existing 商標 in the same class.
Checked: the katakana has no unintended reading; the long vowel is written (アクミー, not アクミ).
Open: 商標 clearance in class 42 (see the project file).
```

If the user tracks the effort as a project, the decision summary also belongs in the shared `~/Clawic/data/projects/<project>.md`, with the reasoning staying here and referenced by name.

## Shared contacts

Lives at `~/Clawic/data/contacts/contacts.md` and is shared with every other skill that knows people — the user may not have any of them installed, so the format travels with this skill.

```markdown
# Contacts

| Name | Key | Role | Preferred channel | Context | Last contact | File |
|---|---|---|---|---|---|---|
| 小林健一 | kobayashi@acme.co.jp | 取引先 営業窓口 | email | approves every 見積 | 2026-07-21 | — |
```

- **Identity is `Key`**: the email in lowercase; if there is none, the handle; if neither, `<kebab-name>` plus a stable disambiguator. The key is a column of the row, never implicit.
- Read the file before adding. If the key is already there, update that row in place — never a second row for the same person. Only rows you created are yours to change; leave other skills' rows alone.
- `Preferred channel` is the type of channel (LINE, Slack, email, 電話), not the address.
- Record the person's name as they write it in `Name`; the **reading** goes in this skill's `### Name Readings`, not here, because it is Japanese-specific and other skills will not maintain it. A person addressed two different ways in two threads is the same failure as a drifting glossary term.
- **Scale cut**: one row per person while there are ≤15, or until one no longer fits its row. Past that, one file per person at `~/Clawic/data/contacts/<name>.md` and `contacts.md` becomes the index with the `File` pointer. If you arrive and the folder already looks like that, follow it.
- **Foreign columns win.** If `contacts.md` exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- Rates or fees belong here only as a note with the currency (`8,000 JPY/1000字`), never a bank detail or a portal password.
- Removing someone: delete the row, delete their `## Recipients` row, and note the date in `## Pain Points` or `## Profile`, whichever explains why. A contact list that only grows stops being one.

## Shared projects

Lives at `~/Clawic/data/projects/<project>.md`, one file per project, from the first one. Used when the Japanese-language work is something the user tracks — a note blog, a 転職 search, a manga volume, entering the Japanese market, a thesis.

```markdown
# note-blog

status: active
goal: weekly note article, 5k フォロワー by Q4
milestones: voice guide agreed 2026-05-10 · first 10 articles 08-01 · native review 08-15
decisions: 丁寧 throughout · 私 as 一人称 · no slang on this channel (see japanese artifacts)
```

- Identity is the project slug, which is the filename. Read before writing; update the existing file in place.
- Closing it is `status: done | cancelled — <date>` inside the file, never deleting it: it is the record of what was delivered. Past ~20 closed projects, move them to `projects/archive/<project>.md` without renaming.
- Keep the language detail in this skill's boxes and leave only the decision line here. Duplicating a decision in two places is how two skills start contradicting each other.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`, promoted one level.

`glossary.md` — `## Terms`, `## Keep In Latin`, `## Name Readings`, `## Corrections`, `## Retired Slang`. The readings and the corrections are why this file earns its keep: without them the same name is misread and the same dead slang is re-proposed, both in front of the same reader.

`recipients.md` — `## Recipients` and `## Channels`, once the user writes to more than a handful of people or on more than a handful of channels. Same columns, same contacts keys.
