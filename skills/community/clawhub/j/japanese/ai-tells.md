# AI Tells — Removing the Machine Fingerprint

The catalogue of tells is the table in SKILL.md (`## AI Tells In Japanese`). This file is the sweep that finds them in order, the English structure underneath each one, and the rewrite. **Before repairing text for a named channel or reader**, read `### Corrections` and the channel's `styles/` file named in `## Boxes` in `~/Clawic/data/japanese/memory.md`: a correction a native reader already made outranks every rule on this page.

**Contents:** [The Sweep, In Order](#the-sweep-in-order) · [Machine Translation vs Model Japanese](#machine-translation-vs-model-japanese) · [翻訳調: the English Underneath](#翻訳調-the-english-underneath) · [Rhythm](#rhythm) · [Flat Vocabulary](#flat-vocabulary) · [What Natives Do That Models Skip](#what-natives-do-that-models-skip) · [Worked Rewrite](#worked-rewrite) · [Tells By Channel](#tells-by-channel) · [Formal Text Is Supposed To Be Uniform](#formal-text-is-supposed-to-be-uniform) · [What Gets Written Down](#what-gets-written-down)

## The Sweep, In Order

Eight passes, cheapest and most structural first. The order is the point: a text whose paragraphs are an English essay is still machine-shaped after every word in it has been improved, and typography polished before the structure is fixed gets thrown away with the sentence it was in.

1. **Frame.** Delete the boilerplate wrapper: a 導入 paragraph announcing what the text will cover, まとめ as a heading, いかがでしたでしょうか, 最後までお読みいただきありがとうございました. Japanese texts start at the first real sentence and stop at the last one.
2. **Structure.** Kill scaffolding openers (まず・次に・そして・最後に as paragraph heads), equalise-length paragraphs, and the three-point essay shape imported from English. If order genuinely matters, number the items; otherwise say them.
3. **Rhythm.** Sentence length spread and ending variety (below). This is the pass that changes the reading experience most and the one models never do to themselves.
4. **Grammar-level translationese.** 私は / 私たちは / あなた, の chains, pre-nominal stacks past ~25 characters, plural markers on inanimate nouns, passive where Japanese takes an 自動詞 (`grammar.md`).
5. **Verb padding.** 〜することができます → 可能形; 漢語 verb + する where a 和語 verb exists (実施する→行う→やる, 使用する→使う); 〜を行う as a wrapper around a verb that already exists (確認を行う→確認する).
6. **Hedges.** 〜と言えるでしょう, 〜ではないでしょうか, 〜と考えられます, 〜かもしれません stacked. Keep at most one hedge per paragraph and make it carry real uncertainty.
7. **Particles.** 終助詞 at roughly one per two to three sentences in casual text (SKILL.md Rule 9), dropped subjects restored to dropped, も where English said "also", くれる/もらう where a favour was received.
8. **Typography.** Full-width marks, …… and ――, no ASCII commas, chat 。 rule (`punctuation.md`, `chat.md`).

Then read it aloud once. The sentence a native would not say out loud is the one still to rewrite, and it is almost always one with two modifiers in front of the same noun.

## Machine Translation vs Model Japanese

Two different failure profiles. Diagnosing which one produced the text tells you which pass will pay.

| Machine-translated Japanese | Model-written Japanese |
|---|---|
| Idioms rendered literally ("touch base" → 塁に触れる nonsense) | Idioms avoided entirely; the prose is generic rather than wrong |
| Untranslated words spelled in katakana | Correct but flat vocabulary: the dictionary word every time |
| ASCII punctuation and half-width marks survive from the source | Punctuation is usually correct; the rhythm is not |
| 敬体 and 常体 mixed inside one text | One level held perfectly, usually one notch too polite |
| Wrong 固有名詞: a company name translated, a surname read wrong | 固有名詞 avoided or hedged |
| Tense copied literally from the source | Tense fine; every sentence the same length |
| Subject preserved in every sentence | Subject preserved in every sentence |
| Sentence count matches the source exactly | Paragraph count and shape match an English essay |

The overlap row is the one that matters: **both keep the English subject**, and deleting 私は / 私たちは / あなたは is the single highest-yield edit on either kind of text.

## 翻訳調: the English Underneath

Each tell is an English structure that survived. Fixing the structure fixes every instance; fixing instances one at a time does not.

| English structure | What it produces in Japanese | Fix |
|---|---|---|
| Relative clause | A modifier stack in front of the noun: 昨日会議で田中さんが提案した新しい仕組み | Split at ~25 characters of modifier; let the noun arrive first (SKILL.md Rule 6) |
| "of" chains | の の の: 弊社のサービスの品質の向上 | One の per noun phrase: サービス品質の向上 — 漢語 compounds absorb the の |
| Plural -s | 問題たち, ファイルたち | Nothing, or 複数の / いくつかの; たち is for people and animals |
| "It is X that" | 〜のは〜です on every emphasis | Reorder instead: what precedes the verb is already the focus |
| Passive voice | 〜されます where Japanese has an 自動詞 | 会議が延期になりました, not 会議は延期されました (`grammar.md`) |
| "We / our company" | 私たちは / 弊社は heading every sentence | State it once; Japanese carries the topic (SKILL.md Rule 4) |
| "You can…" | あなたは〜することができます | 〜できます, subject deleted |
| "Please note that…" | なお、〜という点にご留意ください | ※ + the fact, or the fact alone |
| "In order to…" | 〜するために at the head of every second sentence | Subordinate it or drop it: purpose is often already obvious |
| Gerund subject | 〜することは〜です | Nominalise with a noun: 導入は難しい, not 導入することは難しい |
| Adjective stacking | 効果的で効率的な | One adjective, or a number |
| "very / really" | とても on everything | The specific word (SKILL.md Word Choice), or a figure |
| "And / Also / Moreover" | そして・また・さらに opening consecutive paragraphs | Japanese connects through the topic chain (`grammar.md`) |
| Bullet lists as the default answer shape | A three-bullet list where a sentence was asked for | Prose unless the content is genuinely a list of parallel items |
| Parenthetical asides | （）three times in a paragraph | 読点-separated clauses, or a second sentence |

## Rhythm

The property a Japanese reader registers before any word choice, and the one no vocabulary edit reaches.

- **Sentence length has to vary inside a paragraph.** Target 40-60 characters, split past ~80 (SKILL.md Rule 6) — but a paragraph of four sentences all between 38 and 45 characters reads as generated even though every sentence is inside the target. Put a sentence under 20 characters next to one over 40.
- **Endings have to vary.** Count consecutive sentences ending in ます. **Four identical endings in a row is the threshold** at which the text starts to hum. The escapes, in order of how invisible they are: 〜ました vs 〜ます alternation · 体言止め · a question (〜でしょうか) · 〜のです / 〜んです · a fragment · a 〜が clause carrying into the next sentence.
- **読点 density: roughly one per 15-25 characters** (Rule 6). Two failure directions, both machine-typical: a 70-character sentence with no 読点, and a 読点 after every particle.
- **Paragraph length has to vary too.** A one-sentence paragraph is legitimate and is what a model never writes.
- **体言止め at least once** in casual, social or marketing copy of any length. Zero across a 500-character X thread or note section is a signal on its own (`social-media.md`).

## Flat Vocabulary

The Word Choice table in SKILL.md is the ladder from safe to native; `register.md` has the 和語/漢語 axis. Three additions that live only here:

- **The dictionary word is right and flat.** 悪い is correct where 微妙, いまいち, 芳しくない each carry a stance. Flatness is not an error a proofreader can point at, which is exactly why it survives every review and still reads as machine.
- **Collocation, not translation.** Japanese verbs bind to specific nouns: 課題を解決する / 問題が生じる / 責任を果たす / 期待に応える / 目標を達成する. A dictionary-correct substitution inside a fixed collocation (課題を解く, 責任を実行する) parses and reads as foreign.
- **漢語 density is a register control, not a quality control.** 実施・対応・確認・検討 stacked in a chat message reads as a legal notice; the same words in a 稟議書 are correct (`business.md`). Cut 漢語 down the ladder, not everywhere.

## What Natives Do That Models Skip

| Native move | Why a model omits it | Where |
|---|---|---|
| Drops the subject once recoverable | The source sentence had one | SKILL.md Rule 4 |
| 終助詞 carrying attitude | No English equivalent to translate from | `register.md` |
| くれる / もらう on a received favour | English has no grammatical slot for it | `grammar.md` |
| Contractions: 〜てる, 〜とく, 〜ちゃう, なきゃ | Written-form training data | `chat.md` |
| An 自動詞 where blame is not being assigned | English defaults to an agent | `grammar.md` |
| 擬態語 doing the work of an adjective | English has no equivalent vocabulary | `onomatopoeia.md` |
| A sentence left unfinished (〜ので…) | Models finish every sentence | `etiquette.md` |
| 体言止め | Not a sentence by English standards | above |

Do not fabricate errors to look human. Typos and 変換ミス are a native's characteristic slip (`proofreading.md`) and introducing them deliberately trades one defect for another; the fix for flawless-and-flat is rhythm and stance, never planted mistakes.

## Worked Rewrite

Before — a note paragraph as a model produces it:

> 私たちは、今回のプロジェクトにおいて、チームの生産性を向上させることができました。まず、タスク管理ツールを導入しました。次に、週次のミーティングを実施しました。そして、進捗を可視化することにより、課題を早期に発見することが可能になったと言えるでしょう。いかがでしたでしょうか。

Four sentences, three opened with a scaffolding adverb, every one ending です・ます, one hedge with nobody behind it, and an SEO closer.

After:

> タスク管理ツールを入れ、週次のミーティングを15分に絞りました。効果が出たのはこの二つだけです。遅れがその日のうちに見えるようになり、翌週まで気づかないということがなくなりました。可視化と呼ぶほどのことはしていません。

What changed, pass by pass: the frame (いかがでしたでしょうか) deleted · the scaffolding (まず・次に・そして) deleted · 私たちは deleted · 向上させることができました → the concrete thing that happened · 実施しました → 絞りました with the number that makes it real · 〜と言えるでしょう → an assertion · lengths now run 32 / 16 / 42 / 19 characters instead of four sentences in the same band · endings run ました / です / ました / ません instead of four in a row.

## Tells By Channel

The same text is machine-shaped for different reasons depending on where it lands.

| Channel | The tell that outs it there | Fix |
|---|---|---|
| LINE | 。 on every line, no contractions, one long message instead of three short ones | `chat.md` |
| Slack | Full 敬語 to a peer, 承知いたしました where a reaction is the ack | `chat.md` |
| Business email | させていただく three times, no 名乗り, no 【】 tag on the subject, 〜のほど repeated | `business.md` |
| note / blog | Definition opener (「◯◯とは」), a 見出し over every paragraph, まとめ at the end | `social-media.md` |
| X | Hedging inside a 140-character budget, no 体言止め, a thread whose first post does not stand alone | `social-media.md` |
| 履歴書 / forms | 敬体 inside 学歴・職歴, 西暦 and 和暦 mixed across fields | `documents.md` |
| Fiction | Every character with the same 語尾, 地の文 in 敬体, no 一人称 differentiation | `fiction.md` |
| Spoken script | Written connectives (したがって), digits left unspoken, no repeated topic | `speaking.md` |
| Anything ceremonial | 忌み言葉 present because the model optimised for fluency | `documents.md` |

## Formal Text Is Supposed To Be Uniform

The over-correction to guard against. A 契約書, a 稟議書, a 公文書 or a 最敬語 letter legitimately has uniform sentence endings, no 終助詞, no rhythm variation and heavy 漢語 — de-machining those is how a document stops being a document. In formal text the tells are different ones:

- させていただく where plain 謙譲語Ⅰ is correct (`keigo.md`)
- 〜のほど, 〜させていただければ幸いです stacked into a request that no longer names the ask
- A missing 記 / 以上 pair, or 記 without 以上 (`documents.md`)
- 貴社 spoken or 御社 written (`business.md`)
- Fluent 敬語 wrapped around a sentence with no content — the formal-register equivalent of a hedge

## What Gets Written Down

Destinations, all in `memory-template.md`:

- **A tell a native reader named in the user's own text** ("これ、翻訳っぽい") → `### Corrections` with the accepted form and who said so, in the same turn. A reader-sourced tell outranks this whole file.
- **A rewrite that fixed a recurring pattern** — the de-machining edit for one channel, done once and reusable → `styles/<channel>.md` under a "Do not" line, or `artifacts/` if it runs long.
- **A pattern the user themselves keeps producing** → `## How They Work`, so the next session sweeps for it first instead of rediscovering it.
- **A platform or client that flags AI-written text** — a publisher policy, a client that asked for a declaration → `## Environment`, with the date.
