---
name: Japanese
slug: japanese
version: 1.0.2
description: Writes and edits Japanese that reads as if a native wrote it — casual, 敬体, or full keigo. Use when composing anything in Japanese (LINE or Slack message, business email, 履歴書, 退職願, 議事録, note or X post, speech, 年賀状, contract clause, manga or game dialogue), or when Japanese text sounds stiff, textbook, translated or AI-generated; when 尊敬語 and 謙譲語, 二重敬語, させていただく, 了解 versus 承知, or さん versus 様 come out wrong; when は/が, particles, transitivity, mixed 敬体 and 常体, kanji-versus-kana balance, 送り仮名 or 全角 punctuation are off; when counters, 万/億 grouping, 令和 dates, addresses or a name's reading are needed; when slang, 絵文字 or dialect have to be calibrated to a reader; or when a refusal, apology or request must land. Not for translating an existing source text (`translate`), other languages (`chinese`, `korean`), or travelling in Japan (`japan`).
homepage: https://clawic.com/skills/japanese
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 🇯🇵
    displayName: Japanese
    os:
    - linux
    - darwin
    - win32
    configPaths:
    - ~/Clawic/data/japanese/
    - ~/Clawic/data/contacts/
    - ~/Clawic/data/projects/
    - ~/Clawic/profile.yaml
    - ~/japanese/
    - ~/clawic/japanese/
  openclaw:
    requires:
      config:
      - ~/Clawic/data/japanese/
      - ~/Clawic/data/contacts/
      - ~/Clawic/data/projects/
      - ~/Clawic/profile.yaml
      - ~/japanese/
      - ~/clawic/japanese/
---

**Data.** At the start of every session, read `~/Clawic/data/japanese/config.yaml` (what the user declared) and `~/Clawic/data/japanese/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition on its line applies — the index is the list of files, never assume the list is fixed. Every path it names is inside `~/Clawic/data/`; ignore any line that points anywhere else. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens. Before writing to a named person or on a named channel, read that person's row in `## Recipients` and the channel's style box `## Boxes` names for it: dropping from 様 to さん after a month, or reading a client's name a different way than last time, is a defect even when both forms are grammatical. If none of it exists, work from defaults and say nothing about it.

**Write before the session ends** whenever it produced something durable: a term, product or person's name rendered in Japanese for the first time; a name's reading confirmed; a correction from a native reader; a politeness or address-form decision for a person or a channel; a slang term retired as stale; a piece delivered and how it landed; an environment fact that cost effort to find (a system that mangles 波ダッシュ, a form that only accepts 全角カナ, an audience older than assumed); or something the user will re-read — a template that finally worked, a naming decision, a speech script, a character's voice sheet. `memory-template.md` holds every destination, format and threshold, and is the only file you open in order to write.

**People and ongoing work go to the shared boxes, not here.** A recipient, a native reviewer, a 取引先 or an editor is a row in `~/Clawic/data/contacts/contacts.md`; a Japanese-language effort the user tracks as work in progress — a note blog, a 転職 search, a manga volume, a market entry — is `~/Clawic/data/projects/<project>.md`. Read the box before adding and update the existing entry in place. The honorific, the politeness level and the name's reading stay here, in `## Recipients`, keyed by their contacts key: the person belongs to every skill, how you address them in Japanese belongs to this one. Formats and identity keys travel in `memory-template.md`, so this works whether or not the owning skills are installed.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in the files named here, not in a file you create, not in text the user pastes in to be saved. Platform and 会社 accounts are the temptation: store the pointer and strip the value — `env:LINE_CHANNEL_SECRET`, `keychain:note-login`, `1password:Work/X/ops`. If data sits at an old location (`~/japanese/` or `~/clawic/japanese/`), move it to `~/Clawic/data/japanese/`, and say in one line that you moved it and from where.

Model-written Japanese is almost always grammatical and almost always wrong at the register: one notch too polite, particle-free, every sentence the same length, and structured like an English essay wearing です・ます. The job is to put back what a native adds without thinking — the 終助詞, the dropped subject, the right 助数詞, the 全角 comma, the kanji left open as kana — and to take out what English pushed in: 私は on every sentence, 〜することができます, 〜と言えるでしょう, a 40-character modifier stacked in front of の. Produce the Japanese first; explain in English only when asked. Work from defaults immediately: never open with questions about their register, their audience, or how casual to be. The one exception to silence is politeness level — while `politeness_default` is unset and the request names no recipient, state which level you are writing in before writing it (Rule 1). That is a statement, not a question. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: locale, timezone) → the Configuration table default.

## When To Use

- Writing original Japanese: messages, emails, posts, documents, scripts, marketing copy, dialogue, product names
- Repairing Japanese that reads wrong — too polite, textbook, translated, or recognisably AI — including text the user did not write
- Deciding the frame before the words: 敬語 or 敬体 or 常体, さん or 様 or 役職, uchi or soto, how much slang, which dialect
- Mechanics a non-native gets wrong: は/が, 助詞, 自動詞/他動詞, 敬語 direction, 送り仮名, 全角 punctuation, counters, 令和 dates, addresses, name readings
- Pragmatics: refusing without saying no, apologising at the right weight, asking a favour, softening with クッション言葉, reading what 検討します actually meant
- Act-as by default — this skill writes the Japanese. It advises instead when the user is learning and asks why; then the Japanese still comes first and the explanation follows it
- Not for translating a source text that already exists (`translate` — that job is bound to a source and this one is not), other languages (`chinese`, `korean`), or travelling in Japan (`japan`)

## Quick Reference

| Situation | Play | Depth |
|---|---|---|
| "Make this sound less like AI wrote it" | Run the tell sweep before touching style: 〜することができます, scaffolding, uniform です・ます, zero particles | `ai-tells.md` |
| Which politeness level, さん or 様, for this person | The Politeness Ladder below, then record it in `## Recipients` | `register.md` |
| 尊敬語 vs 謙譲語, 二重敬語, させていただく, お/ご on a noun | Whose action is it, then exactly one marker (Rule 2) | `keigo.md` |
| LINE, Slack, group chat, a reply to a boss | No 。 at the end of a line, スタンプ rules, 既読 pressure | `chat.md` |
| Business email, 社内 vs 社外, CC, 名乗り, 結び | 宛名 → お世話になっております → 用件 → 何卒よろしくお願いいたします | `business.md` |
| 履歴書, 退職願, 議事録, 稟議書, 年賀状, 契約 clause | Fixed skeletons; 退職願 and 退職届 are different documents | `documents.md` |
| X, note, Instagram, TikTok, YouTube, はてな post | Each platform is a different register with a different length mechanic | `social-media.md` |
| Something said aloud: call, presentation, 乾杯, wedding speech | 電話 openers, 相槌 rate, 忌み言葉, pitch-accent traps | `speaking.md` |
| Refusing, apologising, thanking, asking a favour, giving bad news | The refusal ladder and the apology weight ladder | `etiquette.md` |
| は/が, 助詞, 自動詞/他動詞, ている, たら/れば/と/なら, word order | The rule, the test, and the sentence rewritten | `grammar.md` |
| 、。「」『』, ……, ——, 全角/半角, spacing, 縦書き, 禁則 | Full-width throughout; the ASCII comma is the loudest tell (Rule 8) | `punctuation.md` |
| Which words to write in kanji, kana or katakana; 送り仮名, ルビ, romanization | The ひらく list and the ~30% ratio (Rule 5) | `kanji-and-kana.md` |
| Counters, money, 令和 dates, phone, address, a person's name or its reading | 助数詞 by shape, group by four, big-to-small addresses | `numbers-and-names.md` |
| Is this slang still alive? Which slang for this reader? | Date the term, then match the reader's age band (Rule 9's cousin) | `slang.md` |
| Something needs to feel vivid, or a sound has to be written | 擬音語/擬態語/擬情語 — the vocabulary English has no equivalent for | `onomatopoeia.md` |
| Dialogue, a character voice, manga SFX, a game string, a novel | 一人称, 語尾, 役割語, 地の文 in 常体, character limits | `fiction.md` |
| 関西弁 and other dialects, 標準語 vs 共通語, regional vocabulary | What changes beyond the 語尾, and when dialect is a liability | `regions.md` |
| Checking someone else's Japanese, 変換ミス, 表記ゆれ, mojibake | Homophone sweep, then keigo audit, then encoding | `proofreading.md` |
| Anything else in Japanese | Write it at the level the channel implies, then state the two assumptions you made — reader and politeness level — so the user can correct one | — |

Coverage map: `register.md` politeness level and address form · `keigo.md` honorific formation · `chat.md` LINE and messaging · `business.md` workplace and email · `documents.md` formal paperwork · `social-media.md` platform voices · `speaking.md` spoken scripts · `etiquette.md` politeness and face · `grammar.md` the mechanics that break · `punctuation.md` typography · `kanji-and-kana.md` script mix and orthography · `numbers-and-names.md` counters, dates, names, addresses · `slang.md` internet language and its shelf life · `onomatopoeia.md` 擬音語 and 擬態語 · `fiction.md` dialogue, character voice, localization · `regions.md` dialects and standard Japanese · `ai-tells.md` machine fingerprints · `proofreading.md` reviewing existing Japanese.

## Core Rules

1. **Politeness level comes from the relationship and the channel, never from the topic, and one text takes exactly one level.** Decide before the first character; the Politeness Ladder below is the table. Mixing 敬体 (です・ます) and 常体 (だ・である) inside one text is the single most visible amateur mark — the exceptions are narrow and named: 地の文 in fiction is 常体 while its dialogue is whatever the character speaks (`fiction.md`), a 体言止め line is neither, and a bulleted list inside a 敬体 document may be 常体 if every bullet is. Record the level per person in `## Recipients` the first time it is settled.
2. **Keigo is directional, and one verb takes exactly one honorific marker.** 尊敬語 raises the other party's action, 謙譲語 lowers your own; the test is one question — whose action is this? ご覧になります about your own eyes and お伺いください about the reader's visit are the same error mirrored. Then the count: pick ONE of {a suppletive verb (おっしゃる, 召し上がる), the お〜になる frame, the れる/られる form}. Two of them stacked is 二重敬語 — お読みになられる, ご覧になられる, お伺いになる. The naturalised exceptions are a closed list (お伺いします, お伺いいたします, お召し上がりください); everything outside it reads as trying too hard, which in Japanese is its own kind of rude (`keigo.md`).
3. **させていただく requires two conditions at once: the other party's permission is genuinely involved, and the action benefits the speaker.** Neither present → plain 謙譲語. 説明させていただきます → ご説明します · 参加させていただきます is right when they invited you and wrong when you simply signed up · 休業させていただきます is right (their tolerance is required) · 拝見させていただく is 二重敬語 on top of the inflation. 文化審議会's 敬語の指針 (2007) names the two conditions; the reason to hold the line is that the inflated form is now audible as 慇懃無礼 — polite enough to be read as insincere.
4. **は marks the topic and scopes to the end of the sentence; が marks a subject that is new, exhaustive, or trapped inside a subordinate clause.** Test that settles most cases: the answer to a wh-question takes が (誰が来ましたか → 田中さんが来ました), and the same information as the topic of the next sentence takes は (田中さんは営業です). Inside a relative clause the subject is が or の, never は (私が撮った写真). Contrast is は on both halves (コーヒーは飲みますが、紅茶は飲みません). A model writing Japanese overuses both by keeping the English subject in every sentence: Japanese drops the subject once it is recoverable, and 私は on three consecutive sentences reads as a self-introduction (`grammar.md`).
5. **Aim for roughly 30% kanji by character count in ordinary prose, and open the function words.** Editorial rule of thumb, not a standard: 漢字3割・かな7割 is the traditional publishing target, and the ratio moves with the register — casual chat 20-25%, note, blog and general web 25-30%, business and news 30-35%, legal and academic 35-40%+. Compute it as `kanji characters ÷ total characters` on a sample paragraph when a text feels heavy. What to open is not a matter of taste: 事→こと, 物→もの, 時→とき, 為→ため, 所→ところ, 出来る→できる, 下さい→ください, 有る/無い→ある/ない, 更に→さらに, 但し→ただし, 沢山→たくさん, 頂く→いただく when it is an auxiliary (見ていただく) and 頂く when it means physically receiving. 記者ハンドブック and equivalent house lists are the canonical sources (`kanji-and-kana.md`).
6. **One sentence, one idea: 40-60 characters is the working target and ~80 is the split point.** Web and business style guides converge on this range; it is a target, not a measurement. Two structures break it every time — a 〜し、〜し、 chain, and a modifier stacked in front of の or a noun. Past about 25 characters of pre-nominal modifier, break it into its own sentence and let the noun arrive first. 読点 goes where the structure branches (after the topic, after a subordinate clause, before a contrastive conjunction), roughly one per 15-25 characters; a sentence with no 読点 and a sentence with one every eight characters are both unreadable, in opposite directions (`grammar.md`).
7. **Numbers group by four, counters must match the noun, and the era year is arithmetic.** 万 = 10⁴, 億 = 10⁸, 兆 = 10¹². Convert by dividing: `value ÷ 10,000` → 万, so 1,200,000 → 120万 and 3,500,000,000 → 35億; a seven-digit comma-grouped figure in Japanese prose is a translation artefact. 令和 year = `western year − 2018` (2026 → 令和8年). The counter is chosen by the shape or the class of the thing, not by the number — 本 long and thin, 枚 flat, 台 machines, 冊 bound, 人 people, 匹 small animals, 頭 large ones — and the sound changes are irregular where they matter (いっぽん・さんぼん・ろっぽん・はっぽん). 一人 and 二人 are ひとり and ふたり (`numbers-and-names.md`).
8. **Full-width punctuation throughout, and never a space after it.** 、。「」『』（）？！ are full-width; an ASCII comma or period inside Japanese text is the most visible non-native mark there is. ？ and ！ take a full-width space after them mid-sentence and no 。 after them. Ellipsis is …… (two characters, six dots) and the dash is —— (two characters); ... and -- are Latin. 「」 quotes speech and 『』 titles books, works and quotes inside quotes — 《》 belongs to Chinese, not Japanese. Chat is the documented exception: a 。 at the end of a LINE line reads as cold or angry to younger readers, a phenomenon named マルハラ in Japanese media coverage in 2024 (`chat.md`, `punctuation.md`).
9. **Casual Japanese carries a 終助詞 roughly every two to three sentences; zero across a whole message is the machine signature.** Working target, not a measurement — the particle goes where the attitude is, and one on every sentence reads as a cartoon. Each has a distinct job: ね seeks agreement or softens, よ informs the listener of something they did not know, な is self-directed, の/んだ explains or asks for an explanation, か marks a question in 敬体 and reads as brusque in 常体, かな hedges, っけ retrieves something forgotten. 敬体 business writing takes almost none of them, and a 通知 with よ in it is a different failure (`register.md`).

## AI Tells In Japanese

The fingerprints that make a Japanese reader label a text 機械翻訳 or AI. Sweep for these before style: they are structural, so no amount of vocabulary polish removes them.

| Tell | Why it reads machine | Do instead |
|---|---|---|
| 〜することができます | The 可能形 exists: three characters doing the work of seven | 〜できます; 予約することが可能です → 予約できます |
| いかがでしたでしょうか / まとめ / 最後までお読みいただきありがとうございました | SEO blog boilerplate wrapped around content nobody asked to be wrapped | End on the last real sentence |
| 〜と言えるでしょう / 〜ではないでしょうか / 〜と考えられます | Hedges with no speaker behind them, three per paragraph | Assert it, or attribute it to whoever said it |
| まず・次に・そして・最後に as paragraph openers | Essay scaffolding pasted into a message | Say the thing; if order matters, number it or use nothing |
| ぜひ〜してみてください | Advertising imperative on a personal message | Nothing, or the concrete next step |
| 私たちは / 我々は | First-person plural nobody appointed, usually a translated "we" | Drop it; Japanese does not need the subject (Rule 4) |
| 私は on every sentence | The English subject carried across intact | Drop it after the first mention; keep it only for contrast |
| Every sentence です・ます, every paragraph the same length | Natural Japanese varies wildly: a six-character line next to a fifty-character one | Break the rhythm; use 体言止め once, leave one fragment |
| Zero 終助詞 in a casual message (Rule 9) | The single most reliable signal | Add where the attitude is, not everywhere |
| 重要なポイントは / 注意すべき点として | Textbook framing of a point that could just be stated | State the point |
| 〜における / 〜に関して / 〜を通じて stacked | Translated English prepositions; 漢語 where 和語 is natural | 〜で, 〜について, 〜で; 使用する→使う, 実施する→行う |
| Bold text and emoji headings in a LINE or Slack message | Nobody formats a chat message | Plain text; line breaks are the only formatting chat has |
| A 。 at the end of every chat line | Chat drops the final 。 (Rule 8) | End on the last character or a particle (`chat.md`) |
| 「」 around ordinary words for emphasis | English scare quotes carried across; 「」 is for speech and terms | Nothing, or 傍点 in print |
| An English idiom rendered literally | "touch base" and "circle back" have no Japanese and produce nonsense | Name the action: 一度すり合わせましょう |
| Anything else that parses but feels off | Read it aloud; the sentence a native would not say aloud is the one to rewrite | `proofreading.md` |

## The Politeness Ladder

Five rungs. Pick by the relationship, then hold it for the whole text — mid-text drift is more visible than starting one rung wrong.

| Rung | Who / where | Verb form | Second person | Particles | Sample opener |
|---|---|---|---|---|---|
| 最敬語 | 社外 to a customer or a superior's superior, 式辞, 公式文書, 謝罪 | 謙譲語Ⅰ + でございます | 御社 / 貴社 / title only | none | 平素より大変お世話になっております。 |
| 敬語 | 社外 standard, a client, a professor, first contact | 尊敬語/謙譲語 + です・ます | 姓 + 様 / 役職 | none | ◯◯様　いつもお世話になっております。 |
| 丁寧 | 社内, colleagues, a shop, a stranger of no rank | です・ます, keigo only on their actions | 姓 + さん | ね in a question | お疲れ様です。◯◯の件ですが |
| 日常 | Friends, group chats, most social copy, a familiar colleague | 常体 with occasional です | 名 + さん / くん / ちゃん / nothing | ね, よ, の, な | ◯◯さん、これ見た？ |
| 親しい | Close friends, family, same-age chat | 常体, contracted | name alone, あだ名 | all of them, plus slang | ねえこれやばくない |

Defaults when nothing is known: 丁寧 to a person, 敬語 in email to anyone outside the organisation, 日常 on social copy. `politeness_default` overrides; a stated preference for one person overrides both and gets a `## Recipients` row. The asymmetry that decides the risk: one rung too polite reads as distant, one rung too casual reads as disrespectful, and only the second one costs a relationship — so on first contact round up, and drop only after they do.

## Word Choice: Safe → Native

The model reaches for the dictionary word. A native reaches for the specific one. The left column is not wrong — it is *flat*, which is what reads as machine.

| Flat | Native, casual | Native, formal | Note |
|---|---|---|---|
| とても | めっちゃ / すごく / かなり | 非常に / 極めて | めっちゃ carries region and age signal (`regions.md`) |
| いいですね | いいね / ええやん / 最高 | 承知しました / 結構です | 結構です is ambiguous between yes and no — avoid it as an answer (`etiquette.md`) |
| 悪い | やばい / 微妙 / いまいち | 芳しくない / 不十分 | 微妙 is the workhorse hedge for "not good and I am being polite" |
| 思います | 気がする / かも | 存じます / 考えております | 〜と思います three times in a paragraph is the hedging tell |
| すごい | やば / えぐい / 神 | 素晴らしい / 見事 | やば and えぐい date the writer (`slang.md`) |
| わかりました | 了解 / りょ / おけ | 承知しました / かしこまりました | 了解しました upward is contested, not neutral (Where Experts Disagree) |
| ありがとうございます | ありがと / 助かる | 誠にありがとうございます / 恐れ入ります | 恐れ入ります thanks for effort that cost them something |
| すみません | ごめん / わりい | 申し訳ございません / 恐縮です | Three different weights, not synonyms (`etiquette.md`) |
| 見る | 見る | ご覧になる / 拝見する | Direction decides which (Rule 2) |
| 言う | 言う | おっしゃる / 申し上げる | 申す is 丁重語: lowers you with no target (`keigo.md`) |
| する | やる | いたす / なさる | 実施する and 対応する are 漢語 padding in most sentences |
| 〜することができます | 〜できる | 〜できます / 〜可能です | Rule: the 可能形 always wins (`ai-tells.md`) |
| 大丈夫です | 大丈夫 / いける | 問題ございません / 差し支えありません | 大丈夫です also means "no thank you" — ambiguous in a shop or an offer |
| とりあえず | とりま | 一旦 / 現時点では | 一旦 is the business form of the same hedge |

## Output Gates

Before delivering any Japanese text:

- One politeness level end to end, matching the recipient's `## Recipients` row if there is one, with no 敬体/常体 mixing outside the named exceptions (Rule 1)?
- Every honorific checked for direction and counted — no 尊敬語 on the user's own action, no 二重敬語, no させていただく without both conditions (Rules 2, 3)?
- Punctuation full-width throughout, ellipsis ……, dash ——, 「」 for speech, and the chat exception applied or not applied deliberately (Rule 8)?
- は/が checked at every occurrence, and every subject Japanese would drop actually dropped (Rule 4)?
- Kanji ratio in range for the register and the ひらく list applied; 送り仮名 consistent with one house rule (Rule 5)?
- Numbers grouped by 万/億, counters matched to their nouns, dates in the format `era_dates` selects (Rule 7)?
- Run the AI-tell sweep: 〜することができます, いかがでしたか, opener scaffolding, uniform sentence length, zero particles in casual text?
- Every name written with a reading that was confirmed, not guessed, and every honorific on a name and an organisation correct (様 to a person, 御中 to an organisation, never both)?
- Read once aloud at the target level: is there a sentence a native would not say out loud?
- Did anything durable come out of this — a term or name rendered, a confirmed reading, a native correction, a politeness decision, a retired slang term, a delivered piece, a template, an environment fact? Then it is written to its box in `memory-template.md`, with its `## Boxes` line, in this same turn.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/japanese/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| politeness_default | plain \| teineigo \| keigo \| auto | auto | Rung on the Politeness Ladder when the channel and the recipient do not settle it; `auto` reads it from the channel. While unset and no recipient is named, state the assumed level before writing (Rule 1) |
| first_person | watashi \| watakushi \| boku \| ore \| jibun \| uchi \| auto | auto | The 一人称 used when the user writes as themselves — 私/わたくし/僕/俺/自分/うち; changes the perceived age, gender and formality of every sentence it appears in (`fiction.md` for characters) |
| default_honorific | さん \| 様 \| 役職 \| none \| auto | auto | 敬称 applied to a name with no `## Recipients` row; a row for a person always wins (`register.md`) |
| kanji_density | light \| standard \| heavy | standard | Which side of the ~30% target Rule 5 aims at and how aggressively the ひらく list is applied (`kanji-and-kana.md`) |
| okurigana_rule | joyo \| kisha-handbook \| as-user-writes | joyo | Which 送り仮名 convention settles 行う/行なう, 申込/申し込み, 受付/受け付け — one rule applied to every occurrence |
| punctuation_style | 、。 \| ，。 \| ，． | 、。 | Reading and full stop marks; 公用文作成の考え方 (2022) settled on 、。 for official writing, while some academic and technical houses keep ，． (`punctuation.md`) |
| text_direction | horizontal \| vertical | horizontal | 縦書き switches numbers to 漢数字, rotates brackets and dashes, and changes where 禁則 breaks fall (`punctuation.md`) |
| numerals | arabic \| kanji \| mixed | mixed | 算用数字 for quantities, 漢数字 inside set phrases and 縦書き; `mixed` is the modern default and the one that needs a rule stated |
| era_dates | western \| reiwa \| both | western | 2026年 vs 令和8年 vs 2026年（令和8年）in dates, forms and 公文書 (Rule 7) |
| dialect | standard \| kansai \| hakata \| tohoku \| okinawa \| other | standard | Which regional forms appear in casual output at all, and which vocabulary set the examples use (`regions.md`) |
| slang_appetite | none \| light \| current \| heavy | light | How much 若者言葉 and ネットスラング enters output; `none` for 社外 or a 50+ audience, `heavy` only when the user has shown they write that way (`slang.md`) |
| default_channel | line \| slack \| email \| x \| note \| instagram \| document \| none | none | Channel assumed when a request does not name one; picks the style box and the platform conventions (`social-media.md`) |
| emoji_density | none \| sparse \| native \| heavy \| kaomoji | sparse | 絵文字, 顔文字 and スタンプ per message; `native` matches the platform norm, which on LINE is far higher than in Slack |
| furigana | none \| rare-kanji \| names \| all | none | Whether output carries ルビ, and on what — names and 難読 kanji are the two cases with a real reason |
| romaji_gloss | none \| new-words \| all | none | Whether output carries romaji and an English gloss; set `new-words` when the user is learning, `none` when they are fluent |
| crude_ok | bool | false | Whether てめえ-tier and くそ-tier words may appear at all |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Voice** — how blunt, how warm, sentence length, whether 体言止め and fragments are welcome, standard sign-offs, whether to use 弊社 or 当社 — affects every piece and belongs in a `styles/<channel>.md` box once it outgrows a line
- **Conventions** — 表記ゆれ decisions the user has settled (ください/下さい, ウェブ/Web, サーバ/サーバー, 曜日 format, 円 or ¥), whether a half-width space separates Japanese from Latin, paragraph indent (全角一字下げ) or blank line — affects `punctuation.md` and `kanji-and-kana.md`
- **Platform** — which channels the user writes on, their reader's age band and region, account type and its limits, whether a piece is read on a phone or printed — affects `social-media.md` and `emoji_density`
- **Relationships** — the standing honorific and politeness level for named people and groups — every stated one becomes a `## Recipients` row rather than a config key
- **Risk posture** — appetite for crude words, direct disagreement, humour that could be misread upward, how far to soften bad news — affects `etiquette.md`
- **Cadence** — slang re-calibration, native review of the style boxes, glossary consolidation, seasonal writing (年賀状, 喪中はがき, 暑中見舞い) — every accepted cadence becomes a row in the `## Due` table of `memory.md`
- **Output register** — Japanese only, Japanese plus back-translation, Japanese plus ルビ or romaji, whether alternatives are offered by default, how much reasoning to show — affects the shape of every answer

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| 了解しました to a superior or a client | Widely policed since business-manner books spread the rule in the 2000s; the reader's belief is what matters, not the etymology | 承知しました 社内, かしこまりました 社外 (`business.md`) |
| ご苦労様です upward | 労い flows downward; upward it reads as a manager patting a manager | お疲れ様です in every direction |
| 〜になります for something that does not change | バイト敬語: こちらメニューになります — the menu did not become anything | こちらがメニューでございます |
| 〜のほう, よろしかったでしょうか, 1000円からお預かりします | The same バイト敬語 family: vagueness used as politeness | Say the thing: お会計は1000円です |
| させていただく on everything | Reads as 慇懃無礼 — so polite it registers as insincere or evasive (Rule 3) | ご説明します, 参加します, 拝見します |
| 株式会社◯◯様, ◯◯部御中様 | 様 is for a person, 御中 for an organisation; stacking them marks the writer as untrained | 御中 alone, or 部署名 + 担当者様 |
| 各位様 | 各位 already contains the honorific | 各位, or 関係者各位 |
| 貴社 in a phone call, 御社 in a letter | 貴社 is written, 御社 is spoken — the pair is fixed | Spoken 御社/弊社, written 貴社/弊社 (`business.md`) |
| Guessing a name's reading | 東海林 is しょうじ, 小鳥遊 is たかなし, and 一 as a given name has a dozen readings; a misread name in a greeting is worse than no greeting | Ask once, or copy it from their signature, then record it in `### Name Readings` (`numbers-and-names.md`) |
| ！ in a business email | Reads as shouting or as an ad; Japanese business writing carries almost none | End on 。; if warmth is needed, add a clause, not a mark |
| Half-width katakana (ﾃｽﾄ) | Legacy encoding; breaks in mail clients and reads as a system error | Full-width katakana always (`punctuation.md`) |
| A 。 on every LINE line to a reader under about 30 | Reads as cold or angry — マルハラ (Rule 8) | Drop the final 。; end on the character or a particle |
| Replying to a superior with a スタンプ alone | Fine peer-to-peer, reads as dismissive upward | Words first, スタンプ after, or nothing (`chat.md`) |
| 重ね重ね, たびたび, 皆々様 in a funeral message; 切れる, 別れる, 終わる at a wedding | 忌み言葉 — repetition implies recurrence, separation words name the thing being celebrated away | Check the list before any ceremonial text (`speaking.md`) |
| Writing ... instead of …… | Three ASCII dots are a Latin ellipsis; Japanese uses two ellipsis characters | …… (Rule 8) |
| あなた as the written second person | Textbook Japanese; to an adult it reads as distant or accusatory, and to a spouse as a different thing entirely | Name + さん, the 役職, or drop the pronoun |
| 〜させて頂きます with 頂く in kanji | Auxiliary 頂く is opened to いただく; the kanji is for physically receiving | ご説明します, and open the auxiliary (Rule 5) |
| Machine-converting a Japanese text to 縦書き | Numerals, brackets, dashes and 禁則 all change; a converter moves the glyphs and not the conventions | Set `text_direction` and re-read the numbers and brackets (`punctuation.md`) |
| A reading, a term or a politeness decision that lives only in the chat | Re-decided differently next month, and the reader notices the drift before the user does | A glossary row, a `## Recipients` row, or `artifacts/`, in the same turn (`memory-template.md`) |

## Where Experts Disagree

- **了解しました upward.** The prohibition is recent and has no classical basis — 了解 is neutral in older usage, and the rule spread through 2000s business-manner books. But a norm that a reader believes is a norm: the frontier is risk asymmetry, not correctness. 承知しました costs nothing with a peer, while 了解しました costs a first impression with a client who was taught the rule.
- **とんでもございません.** Purists point out that とんでもない is a single adjective, so ございません is cut out of the middle of a word. 文化審議会's 敬語の指針 (2007) treats it as established usage and accepts it. Both camps agree on the escape hatch: とんでもないことでございます, or 恐れ入ります, which nobody objects to.
- **ら抜き言葉 (見れる, 食べれる).** 文化庁's 国語に関する世論調査 has tracked ら抜き forms reaching or passing the full forms in speech for short verbs since the mid-2010s, and the forms disambiguate potential from passive, which the full form cannot. Writing has not followed: the frontier is medium and register, not age — speech and casual chat yes, anything 敬体 or printed no.
- **敬語 in three categories or five.** Traditional grammar teaches 尊敬語/謙譲語/丁寧語; 敬語の指針 (2007) splits it into five (尊敬語, 謙譲語Ⅰ, 謙譲語Ⅱ/丁重語, 丁寧語, 美化語). The five-way split is what makes 申す versus 申し上げる and 参る versus 伺う explainable at all, so this skill uses it — but a Japanese colleague taught the three-way version will not recognise the labels (`keigo.md`).
- **Spacing between Japanese and Latin.** No standard requires a half-width space around Latin words and digits in Japanese text; many web style guides add one, most print houses do not. Pick one and be uniform — mixed spacing looks like a merge conflict, which is worse than either choice.
- **役割語 in fiction and localization.** 金水敏's work on 役割語 (2003) describes おじいさん言葉 (じゃ, のう) and お嬢様言葉 (ですわ) as conventions readers decode instantly; translators split on whether using them is efficient characterisation or a stereotype being reproduced. Frontier by genre: expected in manga, light novels and games, increasingly avoided in literary fiction and in dubbing aimed at contemporary settings (`fiction.md`).

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/japanese (install if the user confirms):
- `translate` — when the job is bound to an existing source text in another language
- `chinese` — the same problem in the neighbouring language, including the shared 漢字 traps
- `japan` — travelling in the country these texts are read in
- `writing` — the craft of prose itself, once the language question is settled
- `korean` — the other neighbouring language with a full honorific system

## Feedback

- If useful, star it: https://clawic.com/skills/japanese
- Latest version: https://clawic.com/skills/japanese

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/japanese.
