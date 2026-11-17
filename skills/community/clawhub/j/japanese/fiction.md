# Fiction, Manga, Games, and Localization

Japanese grammaticalises who is speaking. A character is identified by their 一人称, their 語尾 and how they address each person — before any content — which means a voice decided in chapter 1 has to be reproduced exactly in chapter 12. **Before writing any line a named character speaks**, read `~/Clawic/data/japanese/characters/<name>.md`; a voice that drifts is the defect readers report first. Governed by `first_person`, `crude_ok` and `text_direction`.

**Contents:** [地の文 and 台詞](#地の文-and-台詞) · [Dialogue Typography](#dialogue-typography) · [一人称](#一人称) · [二人称](#二人称) · [語尾 and 役割語](#語尾-and-役割語) · [Building a Distinct Voice](#building-a-distinct-voice) · [Register Drift as a Plot Event](#register-drift-as-a-plot-event) · [ルビ as a Device](#ルビ-as-a-device) · [Manga](#manga) · [Games and UI Strings](#games-and-ui-strings) · [Localizing Into Japanese](#localizing-into-japanese) · [Subtitles and Dubbing](#subtitles-and-dubbing) · [What Gets Written Down](#what-gets-written-down)

## 地の文 and 台詞

- **地の文 (narration) is 常体, dialogue is whatever the character speaks.** This is the named exception to the one-text-one-level rule (SKILL.md Rule 1, `register.md`). A novel with 敬体 narration is either a children's book, an epistolary novel, or a mistake.
- **だ or である, chosen once.** だ is spoken-flavoured and dominant in contemporary fiction and light novels; である is essayistic and reads as distance or as a period piece. Literary narration often uses neither, ending on 体言止め and on 〜た.
- **Person**: 一人称 narration takes the narrator's own 一人称, which then also characterises the narration itself — a 俺 narrator's prose is shorter and blunter than a 私 narrator's, and that consistency is the craft. 三人称 narration picks a viewpoint character per scene and stays inside them; head-hopping mid-scene is as visible in Japanese as in English.
- **Tense alternates on purpose.** Japanese narration slips from 〜た into the present (歴史的現在) to bring a moment close, then back. A chapter entirely in 〜た reads as a report; one entirely in the present reads as a screenplay. The alternation is the rhythm, and a model that normalises the tense flattens it.
- **Sentence length is where voice lives in narration**: an action beat is six characters, a reflective one is fifty (`ai-tells.md`).

## Dialogue Typography

- **Each speech goes on its own line, opened with 「 and no 一字下げ.** The bracket occupies the indent. Ordinary paragraphs take 全角一字下げ.
- **No 。 before 」** in the dominant modern convention: 「行きます」と言った. The traditional form keeps it. Pick one and hold it across the whole work (`punctuation.md`).
- **？ and ！ inside 「」 take no 。 either**, and a full-width space follows them only mid-line.
- **『』 is speech inside speech**, a work's title, or a voice through a device (phone, radio, television) in many manga and light novels.
- **（）marks internal monologue** in manga and games; prose usually renders thought as narration with no marker, since 常体 narration and thought are already the same register.
- **…… trails off, —— interrupts.** Both are two characters. A line ending 「でも、それは……」 and a line cut by 「待って——」 are different events and readers read them as different.
- **Attribution is often absent.** Japanese dialogue frequently identifies the speaker through 一人称, 語尾 and politeness alone, and a と言った on every line reads as a script rather than a novel. This only works if the voices are actually distinct, which is why the voice sheet is upstream of everything here.
- **縦書き** changes numerals, brackets and 禁則 (`punctuation.md`), and it is the default for novels and manga.

## 一人称

The single most information-dense choice in Japanese characterisation. `first_person` sets the user's own; characters get their own per sheet.

| Form | Signals | Notes |
|---|---|---|
| 私 (わたし) | Neutral, adult, any gender in formal contexts | The default; on a male character it reads as formal or reserved |
| わたくし | Maximum formality, or an old-money register | 最敬語 and お嬢様 both |
| あたし | Casual, feminine, warm | Often written in hiragana to soften further |
| 僕 | Boyish, soft, educated; adult men in gentle or public registers | On a girl (ボクっ娘) it is a deliberate marked choice |
| 俺 | Blunt, masculine, intimate or rough | The default for young male characters; 社外 never |
| 自分 | Self-effacing; military, sports, 体育会系, Kansai casual | Also a second person in Kansai |
| うち | Feminine casual, strongly Kansai-coded | See `regions.md` |
| わし | Elderly, or a Western-Japan older man | 役割語 |
| 我輩 / 拙者 / 某 | Period, samurai, or comic anachronism | Instantly reads as a joke in a modern setting |
| ワイ / おいら / オレっち | Regional, rough, or net-persona | |
| Own name | Childish, cute, or deliberately performed | An adult woman doing it is a characterisation, never neutral |

Two rules: **a character has one 一人称 and changes it only as an event** (below), and **the 一人称 conditions everything downstream** — a 俺 character who uses 〜ですね is either being polite on purpose or is written wrong.

## 二人称

| Form | Signals |
|---|---|
| Name + 呼び捨て | Intimacy or seniority; the unmarked choice between close characters |
| Name + さん/くん/ちゃん | Ordinary politeness; the suffix is a relationship fact worth recording |
| あなた | Distant, formal, or a wife to a husband — never neutral in dialogue |
| 君 | Downward or affectionate; dated from a superior, ordinary in songs |
| お前 | Intimate between friends, aggressive from a stranger |
| あんた | Casual and slightly rough; in Kansai it is close to neutral |
| てめえ / 貴様 | Hostility, and 貴様 was historically respectful — period fiction inverts it |
| おぬし / そなた | Period register |
| Nothing | The most common option in natural dialogue; Japanese drops it |

Who calls whom what, in both directions, is a table on the voice sheet — not a per-scene decision.

## 語尾 and 役割語

金水敏's 役割語 (2003) describes patterns readers decode instantly without ever having met a speaker who talks that way. Genre decides whether using them is efficient or lazy (SKILL.md, Where Experts Disagree).

| Type | Markers | Reads as |
|---|---|---|
| 博士語 | 〜じゃ, 〜のう, わし | Old scholar, sage |
| お嬢様言葉 | 〜ですわ, 〜ますの, ごきげんよう, わたくし | Wealthy, sheltered |
| 武士語 | 〜でござる, 拙者, かたじけない | Samurai, or a joke |
| 男性語 | 〜だぜ, 〜だぞ, 〜さ, 俺 | Assertive, young male |
| 女性語 | 〜わ, 〜かしら, 〜のよ, 〜だもの | Feminine — largely fictional; real speech dropped most of it |
| ギャル | 〜じゃん, 〜っしょ, まじ, やば, うち | Young, urban, casual |
| ツンデレ | べ、別に〜, 〜なんだからね | Genre convention, self-aware |
| 幼児語 | Reduplication, name as 一人称, 〜でちゅ | Small child |
| 外国人風 | Katakana, particle drop, 〜アルヨ | A stereotype with a history; avoid outside period parody |
| 方言 | See `regions.md` | Region, warmth, or comic relief — and a liability if written badly |

**女性語 is the one to watch.** Contemporary Japanese women largely do not use 〜わ or 〜かしら, so a modern-setting novel that gives every female character those endings reads as written in the 1970s. Fiction keeps them as a convention; realism does not.

## Building a Distinct Voice

Nine dimensions. Two characters who differ on three or more are distinguishable with no attribution line at all.

1. **一人称** and whether it ever changes.
2. **二人称 per interlocutor**, both directions.
3. **語尾**: the two or three endings they actually use, and the two they never use.
4. **Politeness per relationship** — who gets 敬語, who gets 常体, and where the exception is (memory-template's example character uses 丁寧 only with 先生, and it is a joke between them).
5. **Vocabulary register**: 和語 or 漢語 (`register.md`), 常用漢字 ceiling, loanword appetite.
6. **Sentence length and completeness**: who finishes sentences, who trails off, who uses 体言止め.
7. **Contractions**: 〜てる/〜ている, 〜なきゃ/〜なければ (`chat.md`).
8. **擬態語 appetite** — a character who never uses one reads as controlled or cold (`onomatopoeia.md`).
9. **What they call other characters and things** — nicknames, 役職, the word they use for their own home or job.

The test: take three lines of dialogue, strip the attributions, and ask whether the assignment is recoverable. If not, the characters share a voice.

## Register Drift as a Plot Event

The device Japanese has and English mostly lacks: **a change in politeness level is an event in the story**.

- 敬語 → 常体 between two characters marks the moment a relationship changed, and readers date it exactly.
- 常体 → 敬語 marks anger, distance, or a formal role being assumed — colder than any insult.
- A 一人称 change (僕 → 俺, 私 → うち) marks growing up, a mask coming off, or a persona being adopted.
- 呼び方 changes — 田中さん → 田中 → 名前 — are a relationship's whole arc rendered in address forms.

Every one of these has to be deliberate and recorded on the sheet with the scene it happens in, or a later session writes the pre-change voice and undoes it.

## ルビ as a Device

Beyond reading aid (`kanji-and-kana.md`), ルビ is a semantic layer Japanese prose uses and English cannot: the kanji says one thing and the reading says another.

本気(マジ) · 運命(さだめ) · 敵(とも) · 世界(せかい) written over a foreign word · a technical name with its in-world reading. The kanji carries the meaning, the ルビ carries how it is spoken and felt.

- Standard in light novels, manga and games; sparing in literary fiction; absent in business text.
- **Set it once and keep it**: a term that takes ルビ on every appearance in chapter 1 and none in chapter 5 reads as an editing failure. The common convention is first appearance per chapter.
- In plain text it goes in （）after the word; in HTML it is `<ruby>`; game and manga pipelines each have their own tag syntax, and that syntax is an `## Environment` fact.

## Manga

- **Reading order is right to left, top to bottom** — panels, balloons within a panel, and pages (`punctuation.md`). A translation read left-to-right must either mirror the art or state the reading order.
- **Balloons are 縦書き**, so numbers become 漢数字 and brackets rotate. Two-digit numbers use 縦中横.
- **Line breaks inside a balloon are manual and must respect 禁則**: no 、。）」 at the head of a line, no opening bracket at the end. A balloon holds a few short lines, so dialogue is written to the balloon, not fitted afterwards.
- **SFX are drawn, not typeset** — katakana, distorted, part of the art (`onomatopoeia.md`). Localizing them is an art decision before it is a translation decision.
- **Small text outside the balloon** (つぶやき, ツッコミ) is a register of its own and is where most of the humour sits.
- **A line that will be lettered is planned at two lengths**: the ideal and the one that fits. Deliver both.

## Games and UI Strings

The failure modes here are structural and cost money to discover late.

- **Placeholders and particles.** 「%sを手に入れた！」 works; 「%sは強い」 does not, because は/が depends on the noun's discourse status and sometimes on whether it ends in a vowel. Design strings so the variable sits before を or に, and never split a Japanese sentence across two concatenated strings — SOV order means the English concatenation order produces nonsense.
- **Counters break with variable numbers.** 「%d個のアイテム」 is safe because 個 accepts almost anything; 「%d本」 is not (`numbers-and-names.md`). Where the noun varies, use 個 or つ, or key the counter to the item.
- **No plural or gender agreement** — the one thing Japanese localization gets for free.
- **Length limits are in 全角 units** and Japanese usually runs shorter than English for the same content, then blows the limit on 敬語. Menus are 体言止め; system messages are 丁寧; NPC dialogue is per-character.
- **敬語 is a character property**, so an NPC class (shopkeeper, guard, noble) needs its politeness fixed once in a table rather than per string.
- **Legacy pipelines** carry 半角カナ, Shift_JIS and fixed-width fonts; those are `## Environment` facts and they decide what characters may be used at all (`punctuation.md`).

## Localizing Into Japanese

English gives the translator less information than Japanese requires, so localization means **inventing characterisation data the source does not contain**:

- English "I" carries no age, gender or register; Japanese demands 私/僕/俺/うち on the first line a character speaks. Decide it for every character before translating any of them, and write it on the sheet.
- English "you" likewise: the 二人称 grid is a decision, not a translation.
- **Honorifics**: keep -san/-kun/-chan as ローマ字 in an English-facing product, or map them onto the Japanese originals when localizing into Japanese. The pairing has to be consistent across the whole product.
- **Name order** flips or does not, once, for the entire product (`numbers-and-names.md`).
- **Humour rarely survives**; the working move is to replace the joke at the same beat with a joke that works, and flag it for the client rather than translating a pun literally.
- **役割語 is the shortcut and the risk**: it characterises instantly and reproduces a stereotype. Expected in manga, light novels and games; increasingly avoided in literary fiction and in contemporary-setting dubbing.

## Subtitles and Dubbing

- **字幕 conventions**: the long-standing industry rule of thumb is about **4 characters per second** of speech, with lines of roughly 13-14 全角 characters and no more than two lines on screen. That budget is far below what the actor says, so subtitling is compression, not translation.
- **Break on a 文節 boundary**, never leaving を or に stranded at the head of the next line (`punctuation.md`).
- **Subtitles drop punctuation**: 。 is replaced by a space, 、 by a half-width gap; ？ and ！ survive.
- **吹き替え is written to the 尺** — the mouth flaps and the shot length — so the constraint is syllable count and breath, not character count. A dub script and a subtitle script for the same scene share almost no wording.
- **Both are read by people who also hear the original.** A subtitle that contradicts an audible name or number is caught instantly, which is why 固有名詞 and figures are checked against the source list rather than translated afresh (`proofreading.md`).

## What Gets Written Down

Destinations, all in `memory-template.md`:

- **A character's voice** — 一人称, 二人称 per character, 語尾, politeness grid, vocabulary ceiling, what they never say → `characters/<name>.md`, from the first character, with its `## Boxes` line in the same turn. This is the box that makes a multi-session project possible.
- **A voice change that is a plot event** → the same file, with the scene it happens in, so it stays intentional.
- **The project's standing conventions** — 。 inside 」 or not, ルビ policy, honorific handling, name order, SFX policy → `artifacts/style-<project>.md`, and the shared `~/Clawic/data/projects/<project>.md` gets the one-line decision.
- **A coined term, a place name, an in-world word with its ルビ** → `### Terms`, with the reading. A term rendered two ways across chapters is the most common continuity error in this domain.
- **A pipeline constraint** — string length in 全角, a tag syntax for ルビ, an encoding, a balloon size → `## Environment`.
