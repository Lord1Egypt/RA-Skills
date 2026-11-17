# Numbers, Dates, Counters, Names and Addresses

Everything in this file is checkable, which means every error in it is visible to the reader. **Before writing any personal, company or place name**, read `### Name Readings` and `## Recipients` in `~/Clawic/data/japanese/memory.md`; a reading cannot be derived from the characters, and a guessed one in a 宛名 is the error a reader never fails to notice. Governed by `numerals`, `era_dates` and `text_direction`.

**Contents:** [Grouping By Four](#grouping-by-four) · [算用数字, 漢数字, 全角](#算用数字-漢数字-全角) · [Counters](#counters) · [Counter Sound Changes](#counter-sound-changes) · [The Native Numerals](#the-native-numerals) · [Money](#money) · [Percentages, 割, Fractions](#percentages-割-fractions) · [Dates and 元号](#dates-and-元号) · [Reading Dates and Times](#reading-dates-and-times) · [年度 and Approximations](#年度-and-approximations) · [Phone Numbers and Postal Codes](#phone-numbers-and-postal-codes) · [Addresses](#addresses) · [Personal Names](#personal-names) · [Asking For a Reading](#asking-for-a-reading) · [Foreign Names](#foreign-names) · [Company and Place Names](#company-and-place-names) · [What Gets Written Down](#what-gets-written-down)

## Grouping By Four

Japanese numbers break every four digits, not every three. 万 = 10⁴, 億 = 10⁸, 兆 = 10¹², 京 = 10¹⁶.

| Figure | In Japanese prose | Not |
|---|---|---|
| 12,000 | 1万2000 | 12,000 (fine in a table, wrong in a sentence) |
| 1,200,000 | 120万 | 1.2 million rendered as 1,200,000 |
| 35,000,000 | 3500万 | 35 million |
| 3,500,000,000 | 35億 | 3.5 billion |
| 8,700,000,000,000 | 8兆7000億 | 8.7 trillion |

Convert by dividing: `value ÷ 10,000` → 万, `value ÷ 100,000,000` → 億. **A seven-digit comma-grouped figure inside Japanese prose is a translation artefact** — the reader has to re-group it mentally, and does.

- **Tables and accounting keep the three-digit comma** (1,440,000円); prose takes the 万/億 form. Both appear in the same 稟議書 legitimately: the itemised block in digits, the sentence in 万.
- **千 is a live unit inside compounds**: 一千万 (10 million), 三千億. 千 alone before a 万 is not optional — 1000万 and 一千万 are both read せんまん.
- **一万, never 万.** Japanese says いちまん where English says "ten thousand"; 万円 with no digit is only correct in 一万円札-style compounds.
- **Reading long numbers aloud**: 1,440,000 is 百四十四万 (`speaking.md`). A script that leaves the digits produces a stumble at the moment the number matters.

## 算用数字, 漢数字, 全角

| Context | Form |
|---|---|
| 横書き body text, business, web | 算用数字, 半角: 3件, 2026年 |
| 縦書き | 漢数字: 三件, 二〇二六年 (or 縦中横 for two digits) |
| Set phrases and idioms | 漢数字 always: 一石二鳥, 十人十色, 四月一日, 三が日, 一部, 一日中 |
| Ordinal and formal counts | 漢数字 or 算用数字 by house rule: 第3回 / 第三回 |
| Legal instruments | 大字: 壱, 弐, 参, 拾 — 金壱百万円也 (`documents.md`) |
| Approximate quantities in prose | 数十人, 十数件 — no digits available for these |

`numerals: mixed` is the modern default and the one that needs a rule stated: **算用数字 for anything countable or measurable, 漢数字 inside fixed expressions.** 一つ, 一部, 一度 keep the kanji even in a digit-heavy document. Full-width vs half-width digits is a `conventions` decision applied to every occurrence (`punctuation.md`).

## Counters

助数詞 are chosen by the **shape or class** of the thing, never by the number.

| Counter | For | Note |
|---|---|---|
| 本 | Long thin things: bottles, pens, trees, umbrellas, phone calls, films, home runs | The sound changes are the irregular ones |
| 枚 | Flat things: paper, plates, shirts, tickets, CDs | |
| 台 | Machines, vehicles, appliances | PCs, cars, 冷蔵庫 |
| 冊 | Bound volumes | Books, notebooks; magazines take 冊 or 部 |
| 部 | Copies of a document, print runs | 資料を3部 |
| 通 | Letters, emails, formal documents | メール1通 |
| 件 | Cases, incidents, records, enquiries | The default business counter: 問い合わせ3件 |
| 個 | Small discrete objects with no better counter | The fallback for objects |
| つ | Native counter, 1-10, anything without a specific one | The safest fallback of all |
| 人 | People | 1人 ひとり, 2人 ふたり, 4人 よにん |
| 名 | People, formal or in service register | 3名様, 参加者5名 |
| 匹 | Small animals | Cats, dogs, fish, insects |
| 頭 | Large animals | Cattle, horses, elephants |
| 羽 | Birds and rabbits | |
| 杯 | Cupfuls, glassfuls, bowls; also squid and octopus | |
| 軒 | Houses and shops | |
| 階 | Floors | 3階 さんがい or さんかい, both current |
| 回 | Times, occurrences | |
| 度 | Times, with an emotional or exceptional flavour | 二度と |
| 歳 / 才 | Age | 才 is the informal handwritten substitute |
| 円 / 分 / 秒 / 時間 | Money and duration | 時間 is duration, 時 is a clock point |
| 泊 / 日間 | Nights and days of a trip | 2泊3日 |
| 席 / 室 / 品 / 皿 | Seats, rooms, dishes, plates of food | |

Two failure modes: reaching for 個 for everything, and reaching for a counter the noun does not take. When neither the table nor the reader's own usage settles it, **つ up to nine, then 個** is the escape hatch that never reads as wrong, only as plain.

## Counter Sound Changes

The irregularities are where a fluent-sounding sentence gets caught. 1, 3, 6, 8 and 10 are the positions that change.

| Counter | 1 | 3 | 6 | 8 | 10 |
|---|---|---|---|---|---|
| 本 | いっぽん | さんぼん | ろっぽん | はっぽん | じゅっぽん |
| 杯 | いっぱい | さんばい | ろっぱい | はっぱい | じゅっぱい |
| 匹 | いっぴき | さんびき | ろっぴき | はっぴき | じゅっぴき |
| 分 | いっぷん | さんぷん | ろっぷん | はっぷん | じゅっぷん |
| 階 | いっかい | さんがい | ろっかい | はっかい | じゅっかい |
| 軒 | いっけん | さんげん | ろっけん | はっけん | じゅっけん |
| 個 / 冊 / 歳 | いっこ / いっさつ / いっさい | さんこ / さんさつ / さんさい | ろっこ / ろくさつ / ろくさい | はっこ / はっさつ / はっさい | じゅっこ / じゅっさつ / じゅっさい |
| 枚 / 台 / 件 / 人 | いちまい / いちだい / いっけん / ひとり | さんまい / さんだい / さんけん / さんにん | ろくまい / ろくだい / ろっけん / ろくにん | はちまい / はちだい / はっけん / はちにん | じゅうまい / じゅうだい / じゅっけん / じゅうにん |

The pattern behind it: **p/h-initial counters take っ + ぱ行 after 1, 6, 8 and 10, and ば行 after 3.** じっ〜 is the older reading of 十 in these positions and is still what 放送 and dictionaries give; じゅっ〜 is what almost everyone says.

Irregular readings that are not sound changes but different words: **1人 ひとり · 2人 ふたり · 4人 よにん (never よんにん) · 20歳 はたち · 1日 ついたち as a date**.

## The Native Numerals

ひとつ · ふたつ · みっつ · よっつ · いつつ · むっつ · ななつ · やっつ · ここのつ · とお. Used for objects with no specific counter, for ages of small children (三つ), and inside fixed expressions (一つずつ, 二つ返事). Above ten the native series stops and the Sino series takes over.

The 和語/漢語 split runs through the readings too: 四 is し and よん, 七 is しち and なな, 九 is く and きゅう. **In speech, なな and よん are preferred where し and しち would be ambiguous or ominous** — 4 (し = 死) and 7 (しち, easily heard as いち). Phone numbers, room numbers and prices spoken aloud take なな, よん and きゅう almost without exception.

## Money

- **円 in Japanese text, ¥ in tables and UI.** ￥ full-width in Japanese text, ¥ half-width with Latin digits; never both in one document (`punctuation.md`).
- **万円 is the working unit for salaries, budgets and prices above ~100,000**: 年収500万, 月10万, 初期費用は80万円ほど.
- **税込 or 税別 on every amount, without exception** (`documents.md`) — an amount with neither is the most common billing dispute.
- **Prices ending in 8 are the Japanese convention** (1,980円), where English retail ends in 9.
- **お金 amounts in 祝儀 avoid 4 and 9** and weddings prefer odd numbers (`documents.md`).
- The formula stays visible in any figure a reader has to approve: 月額10,000円／人 × 12名 × 12か月 = 1,440,000円（税別）.

## Percentages, 割, Fractions

| Notation | Value | Where |
|---|---|---|
| 30% | 30% | Reports, data, business |
| 3割 | 30% | Prose, discounts, sport, everyday speech |
| 3割5分 | 35% | 割 = 10%, 分 = 1%, 厘 = 0.1% |
| 半額 / 3割引 | 50% off / 30% off | 〜引き is off the price, 〜掛け is the multiplier: 7掛け = 30% off |
| 3分の2 | two-thirds | **Denominator first** — the reverse of English |
| 3.5 | 三・五 in 縦書き | 中黒 as the decimal point |
| 1.5倍 | 1.5× | 倍 is the multiplier; 2倍 = double |
| 五分五分 | 50-50 | Fixed expression, read ごぶごぶ |

The trap that changes a number's meaning: **3割 is 30%, not 3%.** And 3割減 (down 30%) versus 3割に減少 (down *to* 30%, i.e. −70%) differ by a particle.

## Dates and 元号

`era_dates` decides which appears. The arithmetic:

| Era | Started | Western year = | Example |
|---|---|---|---|
| 令和 | 2019-05-01 | era + 2018 | 令和8年 = 2026 |
| 平成 | 1989-01-08 | era + 1988 | 平成31年 = 2019 |
| 昭和 | 1926-12-25 | era + 1925 | 昭和64年 = 1989 |
| 大正 | 1912-07-30 | era + 1911 | 大正15年 = 1926 |
| 明治 | 1868 | era + 1867 | 明治45年 = 1912 |

- Going the other way: **和暦 year = western year − 2018** for 令和 (2026 → 令和8年).
- **The first year of an era is 元年, never 1年**: 令和元年 = 2019, 平成元年 = 1989.
- **Transition years belong to two eras.** 2019 is 平成31年 until April 30 and 令和元年 from May 1; 1989 is 昭和64年 to January 7 and 平成元年 after. A birth date or a contract date in a transition year needs the month before it can be converted.
- **One system per document.** A 履歴書 or a 申請書 mixing 西暦 and 和暦 across fields is treated as carelessness (`documents.md`). 公文書 and 役所 forms usually demand 和暦; anything international takes 西暦.
- **Both, when the document crosses contexts**: 2026年（令和8年）.
- **曜日 on every deadline**: 8月17日（月）まで. Japanese business readers check the day of the week, and a wrong one is caught immediately (`business.md`).

## Reading Dates and Times

The days of the month are not regular, and eight of them are native readings:

| Date | Reading | Date | Reading |
|---|---|---|---|
| 1日 | ついたち | 8日 | ようか |
| 2日 | ふつか | 9日 | ここのか |
| 3日 | みっか | 10日 | とおか |
| 4日 | よっか | 14日 | じゅうよっか |
| 5日 | いつか | 20日 | はつか |
| 6日 | むいか | 24日 | にじゅうよっか |
| 7日 | なのか | others | regular: 15日 じゅうごにち |

**1日 is ついたち as a date and いちにち as a duration.** 一日中 (all day) is いちにち. 月 readings are regular except 4月 しがつ, 7月 しちがつ, 9月 くがつ — and 9月 is never きゅうがつ.

Times: **24-hour in business and schedules** (14:00-15:00), 午前/午後 elsewhere, 〜時半 for the half hour. 4時 よじ, 7時 しちじ, 9時 くじ. 0:00 is 午前0時 or 深夜0時, and 24:00 appears in opening hours (26:00 for 2 a.m. is a real convention in nightlife and broadcast listings).

## 年度 and Approximations

- **年度 is the fiscal and school year: April 1 to March 31.** 2026年度 runs from April 2026 to March 2027, so 2026年度第4四半期 is January-March **2027**. Confusing 年 with 年度 is the most expensive date error in Japanese business writing, because both are correct words and only one is right.
- **上旬 / 中旬 / 下旬** divide a month into 1-10, 11-20, 21-end. 8月上旬 is a real commitment, not a vague one.
- **Approximation markers**: 約100件 (about) · 100件程度 (of that order) · 100件前後 (either side) · 100件ほど (softer, spoken) · 100件弱 (just under) · 100件強 (just over). 弱 and 強 are precise and are misread as "weak/strong" by non-natives.
- **Ranges take 〜**: 3〜5日, 10時〜12時. In systems known to mangle 波ダッシュ, use から (`punctuation.md`).
- **以上 and 以下 include the number; 超 and 未満 do not.** 3日以内 includes the third day. In a contract or a price table this is the difference that gets litigated.

## Personal Names

- **姓 first**, separated by a 全角 space in Japanese writing: 田中　太郎. In Latin script the government moved to surname-first in capitals for official use (YAMADA Taro) from 2020, while most private-sector English writing keeps given-name-first (`kanji-and-kana.md`).
- **A reading cannot be derived from the characters.** 東海林 is しょうじ in most families and とうかいりん in some; 小鳥遊 is たかなし; 四月一日 is わたぬき; 一 as a given name has a dozen readings. Two people with identical characters read them differently and both are right.
- **旧字体 and 異体字 are the person's actual name**: 髙橋, 﨑, 濵, 邊/邉, 齋/斎/齊/斉. Substituting the simplified form is noticed by the person it belongs to, every time. Copy the character from their signature or 名刺, and record the substitution risk in `## Environment` if a system cannot render it (`punctuation.md`).
- **ふりがな vs フリガナ**: the form says which script it wants, and filling in the wrong one is a rejection-level error on the first line (`documents.md`).
- **敬称 belongs to the name, not to the sentence**: 様 for a person, 御中 for an organisation, never both; 田中部長様 stacks two (`register.md`).
- **Do not generate ルビ for a name from its characters.** A wrong reading is an assertion; no reading is a blank.

## Asking For a Reading

Asking is cheap and expected; guessing is not.

- In person or on a call: お名前は、なんとお読みすればよろしいでしょうか. Nobody with an unusual name is surprised by this.
- In writing, when you cannot ask yet: copy the characters exactly from their signature, 名刺 or website and address the mail without ルビ. Do not invent one to look confident.
- From a 名刺: the reading is usually printed in ローマ字 under the name — the most reliable source available, and it also settles the person's own romanization (Ohno vs Ono vs Ōno).
- Confirm by using it: 田中様、と拝見しておりますが、たなか様でお間違いないでしょうか.
- Then record it in `### Name Readings`, with the source, in the same turn — a reading looked up twice has already cost more than the row.

## Foreign Names

- **カタカナ, with ・ between the parts**: ジョン・スミス, マリー・キュリー. The separator is 中黒, not a space.
- **Original order is preserved** for foreign names (given then family), which is the opposite of the Japanese order in the same document.
- **ヴ vs バ行**: 内閣告示の外来語の表記 permits both ヴィクトリア and ビクトリア; 記者ハンドブック and most newspapers use バ行. Pick one and apply it to every name in the document.
- **Long vowels use ー** and are the commonest 表記ゆれ in imported names (スミス vs スミース is not the issue; ジョーンズ/ジョンソン distinctions are).
- **An established Japanese rendering beats a phonetic one.** A person, brand or place with a form already in circulation keeps it; re-transliterating a known name from the spelling is a visible amateur move.
- **The person's own preferred rendering wins over any rule**, exactly as with a Japanese name's reading.

## Company and Place Names

- **株式会社 goes before or after the name as registered** (前株/後株) and the two are different legal names: 株式会社アクメ ≠ アクメ株式会社. Copy it from their site or signature; never abbreviate to （株） in a formal document (`business.md`).
- **Institution types have their own 敬称 pairs**: 御社/貴社, 御学/貴学, 御行/貴行, 御院/貴院 — spoken form first, written form second.
- **Place names are as unpredictable as personal names**: 放出 はなてん, 十三 じゅうそう, 御徒町 おかちまち, 日本橋 is にほんばし in Tokyo and にっぽんばし in Osaka. A place name in a spoken script carries ルビ (`speaking.md`).
- 日本 itself is にほん and にっぽん, both current; institutions fix their own (日本銀行 is にっぽんぎんこう).

## Addresses

Big to small, the reverse of the English order:

**〒100-0005　東京都千代田区丸の内1-2-3　◯◯ビル5階**

| Level | Element | Note |
|---|---|---|
| 1 | 〒 + 3-4 postal code | Always 半角 digits with a hyphen |
| 2 | 都道府県 | Omitted only for the 政令指定都市 in casual use |
| 3 | 市区町村 | 東京23区 have no 市: 千代田区 directly after 東京都 |
| 4 | 町名 | |
| 5 | 丁目・番・号 | 1-2-3 in 横書き, 一丁目二番三号 in 縦書き |
| 6 | 建物名 + 階 + 部屋番号 | On its own line in a 宛名; a missing building name is the commonest delivery failure |

- **縦書き turns every digit into 漢数字** (`punctuation.md`), which is why an envelope is not a copy-paste of a web form field.
- Phone: **市外局番-市内局番-番号**, half-width hyphens. Tokyo 03, Osaka 06 are two-digit codes with eight following digits; mobiles are 090/080/070 + 4 + 4; 0120 and 0800 are freephone; +81 drops the leading 0 (03-1234-5678 → +81-3-1234-5678).
- Reading a number aloud: 0 is ゼロ or まる, and 4/7/9 are よん/なな/きゅう. の is often inserted for the hyphen: 03の1234の5678.

## What Gets Written Down

Destinations, all in `memory-template.md`:

- **A name's confirmed reading** — a person, a company, a place, and where the reading came from (名刺, signature, asked directly, their own site) → `### Name Readings`, in the same turn it is confirmed. A reading from the person outranks anything inferred.
- **A company's exact registered form** — 前株/後株, 旧字体 in the name, the katakana rendering they use themselves → `### Terms` or `### Name Readings`, whichever the entry is.
- **A number format decision** — 全角 or 半角 digits, 西暦 or 和暦, 万円 or full figures in this user's reports → `conventions` in `config.yaml`; it is a declaration, applied to every occurrence.
- **A system that constrains a number or a name** — a form that only accepts 全角カナ in the ふりがな field, a 役所 that rejects 西暦, a font that drops 髙 → `## Environment`.
- **A recurring figure the user re-derives** — an annual budget line, a rate card, a 見積 formula → `artifacts/`, with its formula visible and its currency and tax status stated.
