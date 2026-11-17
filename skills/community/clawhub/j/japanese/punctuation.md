# Punctuation and Typography

Japanese typography is where non-native text is caught fastest, because the marks are visible at a glance and no amount of vocabulary polish hides them. Governed by `punctuation_style`, `text_direction` and the `conventions` block in `config.yaml`.

**Contents:** [The Marks](#the-marks) · [、and 。](#and-) · [Brackets and Quotes](#brackets-and-quotes) · [Ellipsis and Dashes](#ellipsis-and-dashes) · [？ and ！](#-and-) · [全角 and 半角](#全角-and-半角) · [Spacing](#spacing) · [Line Breaking and 禁則](#line-breaking-and-禁則) · [縦書き](#縦書き) · [Encoding and Mojibake](#encoding-and-mojibake) · [What Gets Written Down](#what-gets-written-down)

## The Marks

| Mark | Name | Job |
|---|---|---|
| 、 | 読点 | Clause separator and list separator inside a clause |
| 。 | 句点 | Full stop |
| ・ | 中黒 | Joins items in a compound list, separates katakana words, marks a decimal in 縦書き |
| ： | コロン | Rare in Japanese prose; normal in headings and forms |
| 「」 | かぎ括弧 | Speech, quotations, terms being introduced |
| 『』 | 二重かぎ括弧 | Titles of books and works; a quote inside a quote |
| （） | 丸括弧 | Parenthetical, readings, sources |
| 【】 | 隅付き括弧 | Tags and labels: 【重要】【ご確認依頼】 |
| ［］ | 角括弧 | Editorial insertions, technical notation |
| 〜 | 波ダッシュ | Ranges: 3〜5日 |
| ー | 長音符 | Long vowel in katakana — not a dash |
| ―― | ダッシュ | Interruption, aside; two characters |
| …… | 三点リーダー | Trailing off; two characters, six dots |
| ／ | スラッシュ | Alternatives; increasingly common |
| ※ | 米印 | Footnote or caveat marker |
| 々 | 踊り字 | Repeats the preceding kanji: 人々, 時々 |

Everything above is full-width. An ASCII comma, period, question mark, parenthesis or quotation mark inside Japanese text is the loudest non-native mark there is, and it survives every style edit because spell-checkers do not flag it.

## 、and 。

- **No space after either.** The character's own width includes its trailing space; adding one produces a visible gap.
- **句点 goes inside the closing 括弧 in modern usage when the quote is a full sentence** — 「行きます。」と言った is the traditional form, and 「行きます」と言った (no 。 before 」) is the dominant modern convention in publishing and on the web. Pick one and hold it; the mixed form is what looks wrong.
- **No 。 after ？ or ！.** They terminate the sentence themselves.
- **No 。 at the end of a heading**, a slide bullet, a 箇条書き item, or a 年賀状 (`documents.md`).
- **`punctuation_style` decides the pair**: 、。 is the default and what 公用文作成の考え方 (2022) settled on for official writing. Some academic, technical and scientific houses use ，． or ，。 — legacy of the older 公用文 convention — and a paper submitted to such a journal follows the journal, not this default.
- **Chat drops the final 。** (SKILL.md Rule 8, `chat.md`).

## Brackets and Quotes

- **「」 is the quotation mark.** ASCII "quotes" and full-width “quotes” in Japanese text are both imports; the second is common in machine output and reads as translated.
- **『』 for titles of books, films, albums, series, and for a quote nested inside a 「」.** 《》 is Chinese, not Japanese — using it is a specific and visible error in a text that also uses 漢字 (`chinese`).
- **Nesting is 「…『…』…」**, never 「…「…」…」.
- **【】 tags a subject line or a label** and is standard in email and on video titles (`business.md`, `social-media.md`).
- **Do not use 「」 for emphasis.** English scare quotes carried across read as either a quotation the reader cannot find or as sarcasm. For emphasis, print uses 傍点 (side dots), the web uses bold sparingly, and most Japanese prose simply rewrites the sentence.
- **（）for readings and asides**: 田中太郎（たなか・たろう）, 2026年（令和8年）.

## Ellipsis and Dashes

- **…… is two characters.** One … alone is acceptable in casual and web text; three ASCII dots (...) is a Latin ellipsis and marks the text as foreign. Publishing convention is the doubled form.
- **―― (ダッシュ) is also two characters** and marks an interruption or an aside. It is not the same character as the 長音符 ー, the hyphen -, or the 波ダッシュ 〜, and substituting one for another is a common encoding artefact.
- **〜 for ranges**: 10時〜12時, 3〜5日. In text that will pass through systems with encoding trouble, から is the safe substitute (below).
- **ー is only ever a long vowel in katakana**: コーヒー, サーバー. It never joins words.

## ？ and ！

Neither is native to classical Japanese; both are now standard, with rules:

- **Full-width, always.** A half-width ? in Japanese text is a visible break.
- **A full-width space follows them mid-sentence**: 本当ですか？　それは知りませんでした。 This is the one place Japanese uses a space inside a sentence.
- **No 。 after them.**
- **？ is often omitted in 敬体 written questions** where か already marks the question: いかがでしょうか。 is complete. It is required after a 常体 question with no か: 行く？
- **！ is near-absent from business writing** and reads as shouting or as advertising (`business.md`). It is normal in chat, social copy and fiction.
- **!? and ?! are fiction and manga conventions**; in prose they read as a comic panel.

## 全角 and 半角

| Element | Convention |
|---|---|
| Japanese characters | Always 全角 |
| Katakana | Always 全角 — 半角カナ (ﾃｽﾄ) is a legacy encoding that breaks in mail and reads as a system error |
| Punctuation in Japanese text | 全角 |
| Latin letters | 半角 in modern practice; 全角 alphabet (ＡＢＣ) reads as dated or as a form field |
| Digits | 半角 in 横書き body text; 全角 in some print house styles; 漢数字 in 縦書き |
| Spaces | 全角 for indentation, 半角 for separating Latin words |
| Parentheses around Japanese | 全角（） |
| Parentheses around Latin | Either, chosen once |

**The rule that matters is uniformity.** A document with 全角 digits in one table and 半角 in the next reads as assembled from two sources — which it usually was. When a form or a system demands one form (many Japanese web forms accept only 全角カナ in a name field), that is an `## Environment` fact, not a style choice.

## Spacing

- **No spaces between Japanese words.** Word boundaries are carried by the script alternation itself, which is one of the jobs kanji does (`kanji-and-kana.md`).
- **Latin-Japanese spacing is a house choice** with no standard behind it: many web style guides put a half-width space around Latin words and digits (Web制作 vs Web 制作), most print houses do not. `conventions.latin_spacing` decides, and whichever it is, it applies to every occurrence — mixed spacing looks like a merge conflict.
- **全角一字下げ** (one full-width space) indents the first line of a paragraph in print and in formal documents; the web convention is a blank line between paragraphs with no indent. Both are correct; mixing them is not.
- **No space after 、or 。**
- **A full-width space after ？ and ！** mid-sentence (above).

## Line Breaking and 禁則

禁則処理 is the set of rules about what may not start or end a line. Word processors and browsers apply it automatically; anything hand-broken has to respect it.

- **May not begin a line** (行頭禁則): 、。 ）」』】 ？！ ー 々 ゛ ゜ small kana (ぁぃぅぇぉっゃゅょ).
- **May not end a line** (行末禁則): （「『【 and other opening brackets.
- **Break at 文節 boundaries** in anything hand-broken — a subtitle, a slide, a 縦書き layout, an email wrapped at 30-35 characters (`business.md`). A break in the middle of a word or a compound is legible but reads as careless.
- **Subtitles**: break before a particle group, never after を or に leaving them stranded at the head of the next line (`fiction.md`).

## 縦書き

Set by `text_direction`. It is not a rotation; it is a different set of conventions.

| Element | 横書き | 縦書き |
|---|---|---|
| Numbers | 算用数字 | 漢数字: 三丁目五番地 |
| Long numbers | 1,440,000 | 百四十四万 or 一四四〇〇〇〇 |
| Brackets | （） | Rotated forms, handled by the renderer |
| Dash and ellipsis | ―― …… | Same characters, rotated |
| Latin text | Inline | Rotated 90°, or set 縦中横 for two-digit numbers |
| Reading order | Left to right, top to bottom | Top to bottom, **right to left** |
| Page turn | Left | Right — a 縦書き book opens from what a Latin reader calls the back |

Uses: novels, manga, newspapers, formal letters, 履歴書 in some formats, 退職願, 弔辞, business cards' Japanese side. **A machine conversion of 横書き to 縦書き moves the glyphs and not the conventions** — the numerals, the Latin runs and the 禁則 all need re-reading by hand.

Manga adds panel order: right to left, top to bottom, which is why a translated manga read left-to-right requires either mirroring the art or leaving the reading order intact and telling the reader (`fiction.md`).

## Encoding and Mojibake

The Japanese-specific encoding failures, and what each looks like:

| Symptom | Cause | Fix |
|---|---|---|
| 譁�蟄怜喧縺� | UTF-8 read as Shift_JIS | Declare the charset; convert once, do not double-convert |
| 繧ｨ繝ｩ繝ｼ | UTF-8 read as EUC-JP or CP932 | Same |
| Excel opens a UTF-8 CSV as garbage | Excel assumes the system codepage | Save UTF-8 **with BOM**, or use UTF-16LE with tabs |
| 〜 renders as a broken glyph | 波ダッシュ U+301C vs 全角チルダ U+FF5E — Windows and Unicode mapped them differently | Pick one; substitute から in ranges when a system is known to break |
| ¥ appears as \ (or the reverse) | Shift_JIS maps 0x5C to both | Use the full-width ￥ or write 円 |
| 髙, 﨑, 濵 vanish or become 高, 崎, 浜 | 旧字体 and 異体字 outside the target font or the target charset | Keep the character; note the substitution risk in `## Environment` (people notice their own name) |
| Emoji become tofu (□) | Font or platform lacks the codepoint | Substitute a 顔文字 or drop it |
| Half-width katakana appears | Legacy system export | Convert to 全角 |

**Circled numbers ①②③, ㈱, ℡, ㎡ and Roman numerals Ⅰ Ⅱ Ⅲ are 機種依存文字** — they render on Japanese systems and can break elsewhere. They are ubiquitous in domestic business documents and risky in anything crossing a border or a mail gateway.

## What Gets Written Down

Destinations, all in `memory-template.md`:

- **A 表記 decision the user settles** — ください or 下さい, サーバ or サーバー, 全角 or 半角 digits, latin spacing on or off, 「」 with or without the inner 。 → `conventions.hyoki` in `config.yaml`, because it is a declaration, not an observation. Applied to every occurrence from then on.
- **A house or client style sheet** the user supplies → `artifacts/hyoki-house-rules.md`, saved as given, with its source and date, and its `## Boxes` line.
- **A system's typographic quirk** — a form that only takes 全角カナ, a mail client that mangles 〜, a font missing 髙, a CSV pipeline that needs a BOM → `## Environment`. These cost real time to rediscover and are invisible until they break.
