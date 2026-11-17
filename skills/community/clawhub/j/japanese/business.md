# Business — Email, 社内文書, and Working Japanese

**Before any email to a named person**, read their `## Recipients` row in `~/Clawic/data/japanese/memory.md` for the honorific, the level and the confirmed reading of their name, and the email style box if `## Boxes` names one. A misread name in a 宛名 undoes the rest of the email.

**Contents:** [The Email Skeleton](#the-email-skeleton) · [宛名](#宛名) · [Openers and Closers](#openers-and-closers) · [社内 vs 社外](#社内-vs-社外) · [The Body](#the-body) · [Subject Lines](#subject-lines) · [CC, BCC, and Reply Discipline](#cc-bcc-and-reply-discipline) · [Standard Situations](#standard-situations) · [報連相](#報連相) · [Meetings and 議事録](#meetings-and-議事録) · [Words That Mark You](#words-that-mark-you) · [What Gets Written Down](#what-gets-written-down)

## The Email Skeleton

Japanese business email is a fixed form. Deviating from it is not creative, it is confusing.

```
件名：【ご相談】8月納品分のスケジュールについて

株式会社アクメ
営業部　小林様

いつも大変お世話になっております。
株式会社◯◯の田中でございます。

標記の件、8月納品分のスケジュールについてご相談がございます。

現在の予定では8月10日納品となっておりますが、
仕様変更の反映に想定より時間を要しており、
8月17日への変更をお願いできればと存じます。

ご都合をお伺いできますでしょうか。
お手数をおかけいたしますが、何卒よろしくお願いいたします。

--
株式会社◯◯　営業部
田中太郎（たなか　たろう）
```

Seven parts, in this order and no other: 件名 · 宛名 · 挨拶 · 名乗り · 用件 · 詳細 · 結び · 署名. The 名乗り comes **after** the greeting and **before** the business, always — a Japanese reader looks there for who is writing and finds nothing if it is in the signature only.

Line length: break at 30-35 全角 characters, on a semantic boundary, rather than letting the client wrap it. This is a real convention, not a legacy one — Japanese has no inter-word spaces, so a hard-wrapped line is easier to scan than a flowed one.

## 宛名

| Addressee | Form |
|---|---|
| A named person at a company | 株式会社アクメ / 営業部 / 小林様 — three lines, 会社 first |
| A person with a 役職 | 営業部長　小林様 or 小林営業部長 — never 小林部長様 |
| An organisation, no person named | 株式会社アクメ御中 |
| A 部署, no person named | 株式会社アクメ　営業部御中 |
| Several named people | 各位, or all names with 様 each, most senior first |
| Someone whose name you cannot read | Copy the characters exactly from their signature, never guess; once confirmed, the reading goes in `### Name Readings` with its source (`numbers-and-names.md`) |
| A person you have never contacted | Add 突然のご連絡失礼いたします after the greeting |

株式会社 goes **before or after** the name depending on the company's own registration (前株/後株) and is not interchangeable: 株式会社アクメ and アクメ株式会社 are different legal names. Copy it from their signature or their site.

## Openers and Closers

| Situation | Opener |
|---|---|
| 社外, ongoing relationship | いつもお世話になっております / 平素より大変お世話になっております |
| 社外, first contact | 突然のご連絡失礼いたします / 初めてご連絡いたします |
| 社内 | お疲れ様です |
| After a meeting | 本日はお時間をいただき、誠にありがとうございました |
| After a long gap | ご無沙汰しております |
| Early morning, any context | おはようございます (the one greeting that survives into email) |

| Situation | Closer |
|---|---|
| Default 社外 | 何卒よろしくお願いいたします |
| Default 社内 | よろしくお願いします |
| Maximum weight | 何卒よろしくお願い申し上げます |
| Asking for something burdensome | お手数をおかけいたしますが、何卒よろしくお願いいたします |
| No reply needed | ご確認いただけますと幸いです |
| Awaiting a reply | ご返信をお待ちしております |

**ご苦労様です never goes upward** — 労い flows downward. お疲れ様です is safe in every direction. Neither belongs in a 社外 email.

## 社内 vs 社外

The うち/そと line (`register.md`) decides almost everything:

| | 社内 | 社外 |
|---|---|---|
| Own company | うちの / 当社 | 弊社 / 当社 |
| Their company | — | 御社 (spoken) / 貴社 (written) |
| Own boss | 田中部長 + 尊敬語 | 部長の田中 + 謙譲語, no 敬称 |
| Level | 丁寧 | 敬語 |
| Opener | お疲れ様です | お世話になっております |
| Closer | よろしくお願いします | 何卒よろしくお願いいたします |
| Acknowledgement | 承知しました | 承知いたしました / かしこまりました |

**貴社/御社 is a written/spoken pair, not a formality pair.** 貴社 in a phone call and 御社 in a printed letter are both wrong, and both are noticed. The same pair exists for other institution types: 貴学/御学 (universities), 貴行/御行 (banks), 貴院/御院 (hospitals).

## The Body

- **結論先行.** The 用件 sentence comes first, then the detail. A Japanese business email that buries the ask in paragraph three is as badly written as an English one; the politeness lives in the framing (`etiquette.md`), not in the delay.
- **標記の件 / 表題の件** links the body to the subject line in one phrase and is the standard opener of the 用件.
- **One ask per email.** Two asks in one email means one gets answered.
- **Deadlines are absolute, not relative.** 8月17日（月）までに, never 来週まで. Add the 曜日: Japanese business readers check the day of the week and a wrong one is caught immediately.
- **Numbers in 算用数字** in horizontal business text, with 全角 or 半角 chosen once and applied consistently (`numbers-and-names.md`).
- **箇条書き** for anything with three or more items, each line opening with ・ and no trailing 。.
- **クッション言葉 before a burden**: 恐れ入りますが / お手数ですが / 差し支えなければ / あいにくですが / ご多忙のところ恐縮ですが. One is enough; two in one sentence reads as anxiety (`etiquette.md`).

## Subject Lines

The subject does two jobs: it says what the mail is, and it says what the reader has to do.

- **Tag the action in 【】**: 【ご相談】【ご確認依頼】【要返信】【日程調整】【御礼】【重要】【再送】. This is a real convention, not decoration, and it is what gets an email answered in a full inbox.
- **Name the object and the date**: 【ご確認依頼】8月分請求書の件（8/5まで）.
- **Never change the subject mid-thread** without marking it; Japanese threading conventions rely on the subject more than on headers. Re: chains are kept, not cleaned.
- **Re: Re: Re:** past about three is trimmed to one Re:.

## CC, BCC, and Reply Discipline

- **CC is a claim about responsibility.** Adding someone's 上司 to CC is a visible escalation and is read as one. Do it deliberately or not at all.
- **A person in CC does not have to reply**; a person in TO does. If a CC recipient is expected to act, name them in the body: （◯◯様、△△の件のみご確認をお願いいたします）.
- **BCC for a mass send**, always, and say so in the body (BCCにて失礼いたします) so recipients know why they cannot see each other.
- **Reply-all is the default** in a thread with CC; dropping people silently is read as going around them.
- **24 hours is the working norm** for a first response. When the answer will take longer, send a holding reply that names the date: 確認のうえ、明日中にご連絡いたします.
- **全文引用 (quote the whole thread below the reply)** is standard in Japanese business email; trimming a quoted thread is not a courtesy here, it removes the record.

## Standard Situations

| Situation | The shape that works |
|---|---|
| Declining | 誠に申し訳ございませんが、今回は見送らせていただきます — reason in one clause, no elaboration (`etiquette.md`) |
| Apologising for a delay | 対応が遅れており、申し訳ございません + the new date + what prevents a repeat. The date is the apology |
| Chasing a non-reply | 先日お送りしたメールの件、行き違いでしたら恐れ入ります + resend the content. 行き違い gives them the exit |
| Asking for a date | Offer three concrete slots with 曜日, then いずれもご都合が合わない場合は、ご希望をお知らせください |
| Introducing two people | ご紹介いたします with one line on each, both in TO, and step out of the thread after their first exchange |
| Correcting your own mistake | 先ほどのメールに誤りがございました + the correction + 訂正してお詫び申し上げます. Send it as a new mail, not a thread reply |
| Sending an attachment | Name it in the body (添付にて◯◯をお送りいたします) and match the filename to the name in the body |
| First contact, cold | 突然のご連絡失礼いたします + how you found them + the ask in two lines |
| Thanking after a meeting | Same day, before 18:00 if possible; one line on a specific thing they said |
| Year-end / new-year | 本年も大変お世話になりました / 本年もよろしくお願い申し上げます (`documents.md`) |

## 報連相

報告・連絡・相談 — the internal-communication triad every Japanese workplace names explicitly. Getting the category right decides the shape of the message:

- **報告** — upward, about something that already happened. Result first, then process. A 報告 that starts with the process reads as excuse-making.
- **連絡** — sideways, facts with no judgement attached. No opinion, no ask.
- **相談** — upward or sideways, *before* deciding. The message must contain the user's own proposed answer; a 相談 with no proposal is read as handing over the work.

The failure mode a non-native hits: sending a 相談 shaped like a 報告 (announcing a decision already taken), which reads as going around the person. When in doubt, say which one it is: ご相談です / ご報告です — a native opener, not a crutch.

## Meetings and 議事録

議事録 has a fixed skeleton and is one of the highest-value artifacts this domain produces:

```
日時：2026年7月26日（金）14:00-15:00
場所：オンライン（Zoom）
出席者：田中（◯◯）、小林様（アクメ）、佐藤（◯◯）
議題：8月納品分のスケジュール

【決定事項】
・納品日を8月17日（月）に変更
・仕様変更分の費用は次回請求に計上

【ToDo】
・修正版スケジュールの送付：田中／7月29日（火）まで
・社内承認：小林様／7月31日（木）まで

【保留】
・9月以降の納品サイクル（次回打ち合わせで再検討）
```

Rules that make it usable: **決定事項 before 議論の経緯** (nobody re-reads the discussion); every ToDo carries **担当 and 期限** or it is not a ToDo; 保留 is a real section, because an unresolved item with no home returns as a surprise. Send it within 24 hours, and use 敬称 consistently — 様 for そと attendees, no 敬称 or さん for うち, decided once and applied to the whole document.

## Words That Mark You

| Instead of | Use | Why |
|---|---|---|
| 了解しました (upward) | 承知しました / かしこまりました | The rule is recent and contested, and the reader believes it (SKILL.md, Where Experts Disagree) |
| ご苦労様です (upward) | お疲れ様です | 労い flows downward |
| なるほどですね | おっしゃる通りです / 承知しました | なるほど is an evaluation of a superior's statement; ですね does not fix it |
| とんでもございません | 恐れ入ります | Contested form; the alternative is uncontested |
| すみません (in writing) | 申し訳ございません / 恐れ入ります | すみません is spoken register in a written apology |
| わかりません | 確認いたします / 存じ上げません | わかりません closes the door; the alternatives keep it open |
| できません | 難しい状況です / いたしかねます | いたしかねます is the formal refusal (`etiquette.md`) |
| 大丈夫です | 問題ございません / 結構です | 大丈夫です is ambiguous between yes and no |
| 〜させていただきます everywhere | 〜いたします | Inflation reads as evasion (`keigo.md`) |
| 〜になります (no change) | 〜でございます / 〜です | バイト敬語 |
| 〜のほう | (delete it) | バイト敬語 vagueness |
| ！ in a 社外 mail | 。 | Reads as shouting or as advertising |

## What Gets Written Down

Destinations, all in `memory-template.md`:

- **An email template that worked** — a 依頼, an お詫び, a 見積送付, a 日程調整 — → `artifacts/template-<what>.md` with the date, who accepted it unchanged, and any per-recipient adjustment. Add its `## Boxes` line in the same turn.
- **A 議事録** the user will re-read, or one that set a precedent for the format → `artifacts/` if it is a template, `pieces/<year>.md` as a row if it was a delivered document.
- **A 取引先 contact** — their name, its confirmed reading, their 会社 and 部署 → the shared `~/Clawic/data/contacts/contacts.md`, with the reading in `### Name Readings` and the honorific in `## Recipients`.
- **A house convention discovered in the wild** — this company writes 当社 not 弊社, this team dropped お疲れ様です, this client wants 全文引用 trimmed → `## Environment`, in prose.
