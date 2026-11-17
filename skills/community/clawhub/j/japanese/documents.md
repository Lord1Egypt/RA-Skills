# Documents — Forms, Paperwork, and Seasonal Correspondence

**Before producing any document that names a person or a company**, read `### Name Readings` and `## Recipients` in `~/Clawic/data/japanese/memory.md`: forms ask for ふりがな, and a form with a guessed reading is a form that gets returned.

**Contents:** [What Makes a Document a Document](#what-makes-a-document-a-document) · [履歴書 and 職務経歴書](#履歴書-and-職務経歴書) · [退職願, 退職届, 辞表](#退職願-退職届-辞表) · [稟議書 and 申請書](#稟議書-and-申請書) · [始末書 and お詫び状](#始末書-and-お詫び状) · [The Formal Letter](#the-formal-letter) · [年賀状 and Seasonal Cards](#年賀状-and-seasonal-cards) · [慶弔](#慶弔) · [Contracts and 見積書](#contracts-and-見積書) · [Addressing an Envelope](#addressing-an-envelope) · [What Gets Written Down](#what-gets-written-down)

## What Makes a Document a Document

Three properties separate a Japanese document from a long email, and all three are formal, not stylistic:

1. **The skeleton is fixed.** Each document type has a heading, a required set of blocks, and an order. Inventing a structure signals that the writer has never seen one.
2. **以上 closes it.** A 社内文書, a 議事録, a 通知 or an 申請書 ends with 以上 on its own line, right-aligned in print. Its absence reads as an unfinished draft.
3. **記 opens an itemised block.** When details are listed, the block is introduced by 記 centred on its own line and closed by 以上. 記 without 以上 is an error every Japanese reader catches.

Level is 最敬語 or 敬語 throughout (`register.md`), 常体 only in 報告書 and 論文 where である is the house style, and never mixed.

## 履歴書 and 職務経歴書

Two separate documents, both required in most applications, and they do different jobs: 履歴書 is the standardised identity-and-history form, 職務経歴書 is the free-form argument.

- **Form choice.** The JIS 様式例 that everyone used was withdrawn from the standard in 2020; 厚生労働省 published a recommended form in 2021 that made 性別 free-entry-or-blank and dropped 通勤時間, 扶養家族数, 配偶者 and 配偶者の扶養義務. Companies still circulate the old layout, so the safe move is to use whatever form the employer supplies and the 厚労省 form otherwise.
- **ふりがな vs フリガナ.** The form tells you which: ふりがな asks for hiragana, フリガナ for katakana. Filling in the wrong script is the most common rejection-level error on the first line of the document.
- **年月日 consistency.** Pick 西暦 or 和暦 (`era_dates`) and use it in every single field including the date of writing. Mixing them inside one 履歴書 is treated as carelessness.
- **学歴・職歴** is one column, 学歴 first, one line per entry, 入学/卒業 and 入社/退社 both listed, closed by 以上 on its own line at the bottom right of the block.
- **Company names are never abbreviated**: 株式会社 written in full, never （株）, and 前株/後株 as registered.
- **退職理由**: 一身上の都合により退職 for a voluntary exit, 会社都合により退職 for redundancy. These are terms of art with consequences for unemployment insurance; do not paraphrase them.
- **志望動機 and 自己PR** are where the document is won, and they are 敬体 throughout. The shape that works: what the company does that the writer can name specifically → what the writer did that maps to it → what they intend to do there. Generic enthusiasm reads as a mail merge.
- **職務経歴書** is 常体 or 敬体 (pick one), reverse-chronological, and numeric: 担当した規模, 期間, 人数, 成果 with figures. Two pages is the working ceiling.

## 退職願, 退職届, 辞表

Three different documents; using the wrong one is a legal and social error.

| Document | Meaning | Who | Withdrawable |
|---|---|---|---|
| 退職願 | A **request** to be allowed to resign | 正社員, normal path | Yes, until accepted |
| 退職届 | A **notification** that you are resigning | After the 願 is accepted, or when refusing negotiation | No |
| 辞表 | Resignation by a 役員 or a public servant | 取締役, 公務員 | — |

- The normal sequence is: tell the direct 上司 in person first, then submit 退職願. A 退職届 delivered before any conversation is a hostile act.
- **民法627条** lets an employee on an indefinite contract end it with two weeks' notice; company rules commonly ask for one to two months. The gap between the two is a negotiation, not a rule.
- Body text is one line: 私事、一身上の都合により、来る◯年◯月◯日をもって退職いたしたく、ここにお願い申し上げます。 The reason is never elaborated. 一身上の都合 is the reason.
- 宛名 is the 代表取締役社長's name with 殿 or 様, written **lower** on the page than the writer's own name — the one place in Japanese correspondence where that layout is correct.
- Handwritten on 白封筒, 縦書き, 三つ折り, submitted by hand. A PDF is increasingly accepted and still not the default.

## 稟議書 and 申請書

Internal approval documents. The reader is scanning for a number and a risk.

```
稟議書

                                                     2026年7月26日
                                                     営業部　田中太郎

件名：営業支援ツール導入の件

標記について、下記のとおり承認をお願いいたします。

                     記

1. 目的　　　　商談管理の属人化解消、月次レポート作成工数の削減
2. 導入対象　　営業部12名
3. 費用　　　　初年度 1,440,000円（月額10,000円／人×12名×12か月、税別）
4. 期間　　　　2026年9月1日〜2027年8月31日（自動更新）
5. 比較検討　　A社案（1,800,000円）、内製（工数6人月）と比較のうえ選定
6. リスク　　　解約は3か月前通知。データはCSVで全件エクスポート可能

                                                     以上
```

What gets a 稟議 approved: the cost as a single annual figure with its formula visible, the alternatives that were rejected and their numbers, and the exit. What gets it returned: a monthly figure with no annual total, no comparison, and no answer to "what happens if we stop".

## 始末書 and お詫び状

- **始末書** is internal and is a formal admission: 経緯 (what happened, factually, no mitigation) → 原因 → 対応 → 再発防止策 → 謝罪の一文. The 再発防止策 must be a mechanism, not a resolution: 「確認を徹底いたします」 is what a 始末書 gets returned for; 「送信前に第三者チェックを必須とする運用に変更いたしました」 is what closes it.
- **お詫び状** is external and inverts the order: apology first, then cause in one line, then the remedy with its date, then a second apology. The customer is not reading for the cause.
- Neither document argues. A 始末書 containing しかし has failed.
- Weight ladder for the apology sentence itself is in `etiquette.md`; in a written 詫び状 the floor is 誠に申し訳ございません and the ceiling is 深くお詫び申し上げます.

## The Formal Letter

Printed correspondence keeps a structure email has dropped:

| Block | Content |
|---|---|
| 頭語 | 拝啓 (standard) · 謹啓 (more formal) · 前略 (skips the seasonal greeting, and therefore the 時候の挨拶) |
| 時候の挨拶 | Month-specific: 新春の候 (Jan) · 早春の候 (Mar) · 新緑の候 (May) · 盛夏の候 (Jul) · 初秋の候 (Sep) · 師走の候 (Dec) |
| 安否の挨拶 | 貴社ますますご清栄のこととお慶び申し上げます |
| 感謝 | 平素は格別のご高配を賜り、厚く御礼申し上げます |
| 主文 | さて、 + the business |
| 末文 | まずは書中にてご挨拶申し上げます |
| 結語 | 敬具 (pairs with 拝啓) · 謹白 (with 謹啓) · 草々 (with 前略) |

The 頭語 and 結語 are a **fixed pair**; 拝啓 closed by 草々 is an error. 前略 exists precisely to skip the seasonal block, so 前略 followed by 時候の挨拶 is self-contradictory.

## 年賀状 and Seasonal Cards

| Card | Window | Notes |
|---|---|---|
| 年賀状 | Posted for 元日 delivery — 日本郵便 announces the deadline each December, typically around the 25th | 三が日 (Jan 1-3) is the delivery window; after 松の内 it becomes 寒中見舞い |
| 寒中見舞い | 松の内明け (about Jan 8) to 立春 (about Feb 4) | The reply to a 年賀状 received late, and the substitute when in 喪中 |
| 喪中はがき | Early-to-mid December, **before** the recipient writes their 年賀状 | Sent by the bereaved; announces that no 年賀状 will be sent |
| 暑中見舞い | 梅雨明け to 立秋 (about Aug 7) | After 立秋 it becomes 残暑見舞い |
| 残暑見舞い | 立秋 to end of August | |
| お中元 | Roughly July (Kanto) / August (Kansai) | Regional timing genuinely differs |
| お歳暮 | Early to mid December | |

Rules that catch people out: **賀正 and 迎春 are abbreviations** and are not used upward — to a superior or a client, 謹賀新年 or 明けましておめでとうございます in full. **No 句読点 on a 年賀状**: 、and 。 are omitted entirely, a convention held over from formal 挨拶状. **元旦 means the morning of January 1**, so 一月元旦 is redundant. And a 年賀状 to someone in 喪中 is not sent; a 寒中見舞い in late January is the correct substitute.

These are calendar-driven and belong in the `## Due` table (`memory-template.md`) — a seasonal greeting sent late is worse than one not sent.

## 慶弔

Ceremonial writing has a vocabulary blacklist, and it is checked before anything else.

| Occasion | 忌み言葉 to remove | Why |
|---|---|---|
| Wedding | 切れる, 別れる, 離れる, 終わる, 帰る, 冷める, 最後, 重ね重ね, 再び, もう一度 | Separation words, and repetition words that imply a second marriage |
| Funeral / 弔電 | 重ね重ね, たびたび, 再三, 続く, 追って, なお, 死ぬ, 生きていた頃 | Repetition implies recurrence of the loss; direct death words are replaced by ご逝去, 生前 |
| 出産・新築祝い | 落ちる, 流れる, 燃える, 倒れる | Reads as a curse on the thing being celebrated |
| 病気見舞い | 長引く, 落ちる, 根づく, 寝つく, 四 and 九 in quantities | Words that imply the illness settling in; 四 = 死, 九 = 苦 |

Envelope conventions: 御祝 / 寿 for weddings with 結び切り (a knot that does not come undone), 御霊前 / 御仏前 for funerals depending on sect and timing, and the amounts avoid 4 and 9 while weddings prefer odd numbers (a splittable even amount reads as division). The name on a 香典 envelope is written in 薄墨 — deliberately faded ink, meaning tears diluted it.

## Contracts and 見積書

- **甲/乙** are the parties, assigned in the opening and used throughout; 甲 is conventionally the client. Swapping them mid-document is the classic drafting bug.
- **本契約, 本件, 前項, 次条** are the internal pointer vocabulary; every one of them must resolve to exactly one thing after any edit.
- **Numbers appear twice** in amounts: 金壱百万円也 in 大字 (壱, 弐, 参, 拾) on formal instruments, so a figure cannot be altered by adding a stroke. Modern contracts use 算用数字 with the 漢数字 in parentheses for the total.
- **消費税** is stated as 税込 or 税別 on every amount, without exception, in both 見積書 and 請求書. An amount with neither is the single most common billing dispute.
- **有効期限** on a 見積書 (typically 発行日より30日) and **支払条件** (月末締め翌月末払い) are expected fields, not optional ones.
- **押印** is declining but not gone; 電子契約 is now normal for 業務委託 and still rare for 不動産 and 労働 contracts.
- A contract clause is 常体 with である, never です・ます.

## Addressing an Envelope

- 縦書き, 〒 and the postal code in the printed boxes, then 都道府県 → 市区町村 → 町名 → 丁目・番地・号 → building and room, each level narrower (`numbers-and-names.md`).
- **Numbers in 縦書き are 漢数字**: 三丁目五番地二号, or 3-5-2 only in 横書き.
- 会社名 in full on its own line, 部署 on the next, name last and largest, with 様 or 御中 as `register.md` decides.
- 外脇付 in the lower-left corner tells the recipient what is inside before they open it: 親展 (personal), 至急, 履歴書在中, 請求書在中. 在中 is written in red and boxed.
- The sender goes on the back, lower left, with the same address hierarchy.

## What Gets Written Down

Destinations, all in `memory-template.md`:

- **Any document skeleton that was accepted unchanged** — a 稟議書 that passed, a 議事録 format the team adopted, a 退職願 wording, a 年賀状 text → `artifacts/template-<what>.md` with the date and who accepted it. Add its `## Boxes` line in the same turn. These are the highest-reuse artifacts in this domain: the same form is filled once a year and forgotten in between.
- **The seasonal cadences the user actually keeps** — 年賀状, 喪中はがき, お歳暮, 暑中見舞い → rows in `## Due` with their window, not their date.
- **A confirmed reading or an exact company name** (前株/後株, 旧字体 in a surname) → `### Name Readings`, with the source. A 宛名 is where a wrong one becomes visible.
- **A form's quirks** — this employer's 履歴書 wants フリガナ, this 役所 rejects 西暦 → `## Environment`.
