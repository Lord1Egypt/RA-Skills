# Chat — LINE, Slack, and Group Messages

**Before writing to a named person on chat**, read their `## Recipients` row and the channel's row in `## Channels` in `~/Clawic/data/japanese/memory.md`, or the `styles/` file `## Boxes` points to. Chat register is per-relationship and per-app at once: the same colleague is 丁寧 in Slack and 日常 in LINE.

**Contents:** [What Chat Japanese Is](#what-chat-japanese-is) · [The 。 Problem](#the--problem) · [LINE](#line) · [Slack and 社内チャット](#slack-and-社内チャット) · [Group Chats](#group-chats) · [Laughter and Reactions](#laughter-and-reactions) · [絵文字, 顔文字, スタンプ](#絵文字-顔文字-スタンプ) · [Message Shape](#message-shape) · [What Gets Written Down](#what-gets-written-down)

## What Chat Japanese Is

Chat is not "casual writing". It is its own medium with its own grammar, and a message that follows written conventions reads as a letter delivered by hand.

| Written Japanese | Chat Japanese |
|---|---|
| 。 at the end of every sentence | No 。 at the end of a message |
| One paragraph, several sentences | One idea per message, sent as several messages |
| Subject stated | Subject dropped almost always |
| Full conjugation | Contracted: 〜てる, 〜とく, 〜ちゃう, 〜じゃう, なきゃ, けど → けど/けども → けど |
| 承知しました | 了解 / りょ / おけ / 👍 (peer only) |
| 申し訳ございません | ごめん / すまん / ごめんね |
| ありがとうございます | ありがと / あざす / 感謝 |
| Complete question | 明日いける？ |

The contractions are not optional decoration; their absence is what makes a message read as a form letter. 見ている → 見てる, 置いておく → 置いとく, 食べてしまう → 食べちゃう, 行かなければ → 行かなきゃ, というか → ってか/つーか.

## The 。 Problem

A 。 at the end of a chat message reads as cold, final, or angry to younger Japanese readers. Japanese media named the phenomenon **マルハラ** (句点ハラスメント) in 2024 coverage of generational messaging norms, and the underlying convention is older than the label: chat lines simply do not carry a full stop.

- **Do not end a chat message with 。** End on the last character, a particle, or nothing.
- Inside a multi-sentence message, a mid-message 。 is fine; it is the final one that carries the signal.
- **The exception is up the ladder.** A 敬語-level message to a customer or a 部長 keeps its punctuation, because there the omission reads as sloppy rather than warm. The line is roughly at 丁寧: 社内 Slack to a peer drops it, an email-shaped LINE to a client keeps it.
- ！ and ？ do not have the problem and are the standard way to close a friendly line without the 。 feeling.
- Age matters more than any other variable here. If the reader's age band is unknown, drop the 。 with anyone the user addresses in 常体 and keep it with anyone in 敬語.

## LINE

The default private channel in Japan for friends, family, and a large share of small-business and freelance work.

- **既読 is public.** Reading without replying is a visible act (既読スルー). When a reply will be delayed, send a two-character holder — 見た / あとで / 了解 — rather than reading silently.
- **Short and many, not long and one.** Three messages of eight characters read as a conversation; one message of forty reads as a notice. Split at the natural breath.
- **スタンプ carry propositional content** — agreement, apology, thanks, "I'm on my way" — and a well-chosen one can be a complete turn. Two limits: never as the *only* reply to a superior or a customer, and never as the reply to bad news.
- **Group leaving is visible** (◯◯がグループを退出しました), which is why Japanese group chats accumulate dormant members.
- **Voice messages are contested** — widely disliked among adults, normal among teenagers. Default to text unless the user has shown otherwise.
- **Business LINE** (LINE公式アカウント, LINE WORKS) is 丁寧, keeps its 。, and reads like a short email with the greeting cut.

## Slack and 社内チャット

- **さん is mandatory on names**, including in @mentions: @田中さん, not @田中. Companies that use given names still use さん.
- **お疲れ様です** is the universal opener and closer, and it is doing the work of お世話になっております in email. Some companies have explicitly retired it as noise; follow the house norm and record it in `## Channels`.
- **丁寧 with peers, not 敬語.** です・ます, keigo only on the other party's actions. Full 敬語 in an internal Slack message reads as either sarcasm or bad news.
- **A reaction emoji is the ack.** 👀 = seen and working on it, ✅ = done, 🙏 = thanks or please. This is why a 承知しました message can be replaced by a reaction between peers, and why it cannot be upward.
- **The one-line 。 rule applies**: a one-line Slack message drops the final 。; a three-paragraph one keeps them.
- **Thread or channel** is a house convention worth recording: some teams treat a top-level reply as noise, some treat a thread as invisible.
- **Bad news does not go in chat.** A delay, a mistake or a refusal that has consequences goes to email or a call, with the chat message only announcing that it is coming (`etiquette.md`).

## Group Chats

- **Address the person before the content**: @田中さん or 田中さん、 at the head of the line. Japanese group chats scroll fast and an unaddressed message is assumed to be for everyone and answered by nobody.
- **みなさん / 皆さん / 各位** open a message to the whole group; 各位 is the written-formal one and reads as a notice.
- **Announcements take a shape**: one line of what, one line of when, one line of what is needed from the reader. Anything longer goes to a document and the chat message links to it.
- **Reply-quoting** (Slack quote, LINE リプライ) resolves ambiguity in a fast group and costs nothing; a bare reply three messages later is unreadable.
- **Silence is an answer** in a Japanese group chat, and it usually means no or not yet. Chasing it in the group is a face cost for the person not answering; chase in DM (`etiquette.md`).

## Laughter and Reactions

| Form | Reads as | Band |
|---|---|---|
| （笑） | Neutral, safe, slightly formal; standard in blog and print | All ages |
| w / ww / www | Casual internet laughter; length scales with amount | Ubiquitous, mildly dated among the youngest |
| 草 / 大草原 | The same joke as w rendered as a word (www looks like grass) | Under ~35, internet-native |
| 笑笑 | Warm, common in LINE among young women | Under ~30 |
| 😂 / 🤣 | Safe everywhere, less specific | All ages |
| ｗｗｗ full-width | Reads as older internet | Over ~35 |
| (^^) / (´・ω・\`) / orz | 顔文字, the pre-emoji generation's register | Over ~35, or deliberately retro |

**Match length, do not escalate.** They send 笑, you send 笑; they send wwww, wwww is fine. Sending 大草原 to someone who wrote （笑） misreads the room in a way that is hard to recover from in text.

## 絵文字, 顔文字, スタンプ

Governed by `emoji_density`. Three different systems, not three intensities of one:

- **絵文字** — inline, one or two per message at most in 丁寧 register, more in 親しい. In 社外 writing: none.
- **顔文字** — a generational marker. Reads as warm and slightly dated; safe with readers over about 35, reads as parental to teenagers.
- **スタンプ** — LINE-specific, functions as a turn in the conversation rather than as decoration.
- **🙇 / 🙏** soften a request or an apology in chat where words would be too heavy. They do not replace a real apology (`etiquette.md`).
- **The smiley trap does not exist in Japanese the way it does in Chinese** — 🙂 is not read as passive-aggressive — but a lone 😅 after a request reads as "I know this is a burden", which is often exactly right.

## Message Shape

A request in chat, in the order that gets answered:

```
田中さん
来週の資料の件です

金曜までに数字だけもらえたら助かります
（フォーマットはこっちで整えます）

難しそうならそう言ってください
```

Four properties: the addressee first, the topic in its own line, the ask with its deadline and its size, and an explicit escape hatch. The escape hatch is not politeness padding — without it, a Japanese reader who cannot meet the request has no low-cost way to say so and will go silent instead (`etiquette.md`).

Bad shape, same content: 田中さん、お疲れ様です。来週の資料の件でご相談なのですが、金曜日までに数字をいただくことは可能でしょうか。ご確認のほどよろしくお願いいたします。— one block, email register, no escape hatch, and the ask is buried in the middle.

## What Gets Written Down

Destinations, all in `memory-template.md`:

- **A channel's standing rules** — 。 or no 。, スタンプ appetite, お疲れ様です or not, thread convention → a `## Channels` row, and `styles/<channel>.md` with its `## Boxes` line once it outgrows one line.
- **A person's chat-specific level** — they opened in 常体, they use 顔文字, they hate voice notes → their `## Recipients` row.
- **A message that landed badly** — a スタンプ read as dismissive, a 。 read as anger → `## Pain Points`, with the cause, so the next message starts from the correction rather than from the rule.
