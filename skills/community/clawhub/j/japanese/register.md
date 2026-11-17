# Register — Politeness Level and Address Form

**Before writing to a named person**, read their row in `## Recipients` in `~/Clawic/data/japanese/memory.md`, and the channel's row in `## Channels` or the `styles/` file its `## Boxes` line points to. The level is a standing decision about a relationship, not a fresh choice per message; re-deciding it every time is how the drift starts.

**Contents:** [What Decides the Rung](#what-decides-the-rung) · [うち and そと](#うち-and-そと) · [敬体 and 常体](#敬体-and-常体) · [Honorifics on a Name](#honorifics-on-a-name) · [Second Person: Mostly Don't](#second-person-mostly-dont) · [終助詞 by Rung](#終助詞-by-rung) · [和語 and 漢語](#和語-and-漢語) · [Level Drift](#level-drift) · [What Gets Written Down](#what-gets-written-down)

## What Decides the Rung

The ladder table lives in SKILL.md. What decides the rung, in order of authority:

1. A `## Recipients` row for this person. Beats everything, including a channel default — the same person is addressed the same way in Slack and in email.
2. The document type. 契約書, 公文書, 式辞 and a formal 通知 are 最敬語 whoever writes them; a LINE message is never 最敬語 even to a 社長.
3. **うち/そと position** — the axis Japanese has and English does not. Everything else is secondary to it (below).
4. Power distance: 役職 gap, age gap, and whether the user is asking for something.
5. The channel default in `## Channels`, then `politeness_default` in `config.yaml`.

Two properties non-natives get backwards:

- **Level is not politeness.** A 最敬語 text can be brutal (契約の解除を通知いたします). A 日常 text can be exquisitely considerate (ごめん、無理させちゃった？). Choosing a high rung to be kind produces cold text; kindness lives in the pragmatics (`etiquette.md`), not in the rung.
- **The rung is a property of the text, not of the sentence.** One 書き言葉 sentence inside a casual message reads as sarcasm — ご査収ください dropped into a friend's chat is a joke, and if it was not meant as one the reader hears one anyway.

## うち and そと

The single structural difference from European politeness systems: Japanese honorifics encode **which group you are speaking from**, not just how much you respect someone.

| You are talking to | Your own boss is | Your own company is | Their boss is |
|---|---|---|---|
| A colleague (うち) | 田中部長 — 尊敬語 on his actions | — | — |
| A customer or 取引先 (そと) | 田中 — no 敬称, no 尊敬語, he is うち now | 弊社 / 当社 | 御社の田中様, 尊敬語 |
| Your own family, to an outsider | 父, 母, 兄 — plain | — | お父様, お母様 |

So: 部長の田中はただいま席を外しております, said to a customer about your own 部長 — dropping the title and using 謙譲語 about a person you would never address that way internally. To a colleague, the same sentence is 田中部長は席を外していらっしゃいます. Getting this backwards (田中部長がおっしゃっていました, to a customer) is the error that most reliably marks a speaker as untrained, because it is invisible in a textbook and audible in a meeting.

The boundary moves with the situation. In a conversation with another 部署 of the same company, your 部署 is うち; in a conversation with a customer, the whole company is うち; in a conversation with a foreign partner, the whole industry can be. Ask each time: relative to this listener, which side of the line am I on?

## 敬体 and 常体

One text, one style. The forms:

| | 敬体 | 常体 |
|---|---|---|
| Copula | です / でございます | だ / である |
| Verb | 行きます / 行きません | 行く / 行かない |
| Past | 行きました | 行った |
| Adjective | 高いです / 高くありません | 高い / 高くない |
| Noun-adjective | 静かです | 静かだ / 静かである |

- **だ and である are not interchangeable.** だ is spoken-flavoured 常体 (blogs, fiction dialogue, casual writing); である is written-flavoured (papers, reports, editorials, 論説). A paper written in だ reads as a blog post; a blog written in である reads as a parody of a paper.
- **The named exceptions to no-mixing**: 地の文 in fiction is 常体 while its dialogue is whatever the character speaks (`fiction.md`); a 体言止め line is neither and is a legitimate rhythm device in both; a bulleted list inside a 敬体 document may be 常体 if *every* bullet is; and a heading is not a sentence.
- **In 常体, the question particle か is brusque.** 行くか？ is a challenge. 常体 questions rise on the last syllable in speech and take の, って or nothing in writing: 行くの？ 行く？

## Honorifics on a Name

| Form | Use | Note |
|---|---|---|
| 姓 + さん | The default for almost everyone: colleagues, peers, strangers, most customers in speech | Never on yourself, never on your own family to an outsider |
| 姓 + 様 | Written form to a customer, a 取引先, anyone 社外 | 様 on an envelope, 御中 on an organisation, never both |
| 姓 + 役職 (田中部長) | Anyone with a rank, 社内 | The 役職 *is* the honorific: 田中部長様 is wrong |
| 役職 alone (部長, 社長) | Direct address to that person, 社内 | Common and correct; 部長、ご相談があります |
| 姓 + 先生 | Teachers, doctors, lawyers, 議員, and anyone whose expertise is being deferred to | Safe when a title is unknown and the person clearly has standing |
| 名 + さん | Where the surname is shared or the workplace uses given names | Increasingly common at startups; follow the house norm |
| 姓/名 + くん | Downward or peer-to-peer, historically to men, now mixed | Upward it is patronising; in some companies it is being retired entirely |
| 姓/名 + ちゃん | Children, close friends, family | Never at work to an adult you do not know well |
| 呼び捨て (no honorific) | Very close friends, family, sports teams, and *your own side* when speaking to そと | To anyone else it is either intimacy or an insult, with nothing in between |
| 御中 | An organisation or a 部署 as the addressee | 株式会社◯◯御中; add 様 only when a person is named instead |
| 各位 | A group of addressees in writing | 関係者各位, 保護者各位; 各位様 is wrong |

Two failure modes worth naming: **dropping an honorific by accident** (a typo that deletes さん reads as contempt), and **stacking two** (田中部長様, 各位様, 御中様), which reads as untrained rather than over-polite.

## Second Person: Mostly Don't

Japanese avoids the second-person pronoun where English requires it. Ranked by safety:

1. **Name + honorific.** 田中さんのご意見は — the default in every register.
2. **役職.** 部長はいかがお考えですか.
3. **Nothing.** いかがでしょうか carries "what do you think" with no pronoun at all. This is the native default in 敬語.
4. **そちら / 御社 / 貴社** for organisations.
5. **あなた** — textbook-only in practice. To an adult stranger it is distant or accusatory; between spouses it is a term of address with its own meaning; in a form or a survey it is normal (あなたのお名前).
6. **君 / お前 / あんた / てめえ** — a descending ladder of intimacy and then aggression. 君 downward from a superior is dated but survives; お前 is intimate among friends and a threat from a stranger.

A model writing Japanese produces あなた because the source said "you". Deleting it is usually the whole fix.

## 終助詞 by Rung

| Particle | Job | Rungs |
|---|---|---|
| ね | Seeks agreement, softens, shares a feeling the listener also has | All rungs; そうですね is standard even in 敬語 |
| よ | Informs the listener of something they did not know | 丁寧 and below; ですよ can sound corrective upward |
| よね | Checks a shared assumption | 丁寧 and below |
| な | Self-directed, thinking aloud | 日常, 親しい; male-leaning in stereotype, universal in practice |
| の / んだ | Explains, or asks for an explanation | 日常, 親しい; ~のです is its 敬体 form and is formal, not casual |
| かな | Hedges a guess or a request | 日常, 親しい |
| っけ | Retrieves something half-forgotten | 日常, 親しい |
| わ | Soft assertion; feminine in 標準語 stereotype, ordinary and gender-neutral in 関西 | Depends entirely on region (`regions.md`) |
| ぞ / ぜ | Strong assertion, masculine, mostly fiction and sports | 親しい, and `fiction.md` |
| じゃん / でしょ | Invites agreement forcefully | 日常, 親しい |

Rate, not rule: roughly one particle per two to three sentences in casual text (SKILL.md Rule 9). 敬語 takes ね in questions and almost nothing else; 最敬語 takes none and also drops the subject wherever the sentence survives without it.

## 和語 and 漢語

The same content, rungs apart, by choosing the native word or the Sino-Japanese one:

| 和語 (softer, spoken) | 漢語 (harder, written) |
|---|---|
| やる / する | 実施する / 行う |
| 使う | 使用する / 利用する |
| 話し合う | 協議する / 打ち合わせる |
| わかる | 理解する / 把握する |
| 決める | 決定する / 確定する |
| 送る | 送付する / 発送する |
| 見る | 確認する / 拝見する |
| だいたい | 概ね / 約 |
| すぐ | 早急に / 至急 |
| あとで | 後ほど / 追って |

Two directions of failure. 和語 in a 契約書 is amateurish. 漢語 in a message is the far more common failure for a model, and it is what produces "sounds like a robot": 確認いたしました、追って連絡いたします in a LINE message to a friend reads as a legal notice. When in doubt in casual text, take the 和語.

## Level Drift

The three places the level slips inside one text:

- **The opener is 敬語 and the body is not.** いつもお世話になっております。followed by あの件、どうなってる？ Fix the body, not the opener.
- **The closing formula outranks the message.** 何卒よろしくお願い申し上げます under a two-line note about lunch.
- **A pasted quotation drags its rung along.** Quoting a 通達 inside a chat message imports 書き言葉; frame it (部長からの原文はこれです：) so the reader knows which voice is which.

## What Gets Written Down

Level decisions decay the moment they leave the session, and their failure mode — addressing someone the wrong way twice — is visible to the reader and invisible to the writer. Destinations, all in `memory-template.md`:

- **The honorific and the rung for a named person** → a `## Recipients` row keyed by their contacts key, in the same turn it is settled. Write the reason too: "he writes 常体 downward, that does not invite reciprocity" is what stops the decision being re-argued.
- **A channel's standing level** → a `## Channels` row; anything longer than one line becomes `styles/<channel>.md` with its `## Boxes` line.
- **A correction from the reader themselves** ("さん付けでいいですよ") → `### Corrections`, with who said so. It outranks every rule on this page.
