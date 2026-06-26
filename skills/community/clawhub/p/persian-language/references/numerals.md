# Persian Numerals — Complete Reference

The #1 numeric error in AI output is picking the wrong digit family. The #2 error is using Western separators (`,` and `.`) inside Persian numbers. This file fixes both and covers every adjacent case.

---

## 1. The Three Digit Families (Pick the Right One)

Three families look similar but are **different Unicode ranges**. Only one is correct for Persian.

| Family | Digits | Unicode range | Use for |
|---|---|---|---|
| **Persian (Extended Arabic-Indic)** | ۰ ۱ ۲ ۳ ۴ ۵ ۶ ۷ ۸ ۹ | U+06F0–U+06F9 | **Persian prose — always** |
| Arabic-Indic | ٠ ١ ٢ ٣ ٤ ٥ ٦ ٧ ٨ ٩ | U+0660–U+0669 | Arabic only — **never in Persian** |
| Western (ASCII) | 0 1 2 3 4 5 6 7 8 9 | U+0030–U+0039 | Code, technical IDs, LTR contexts |

**Critical distinctions AI models miss:**

- ۴ (Persian four, U+06F4) vs ٤ (Arabic four, U+0664) — visually different, both common in model output
- ۵ (Persian five, U+06F5) vs ٥ (Arabic five, U+0665)
- ۶ (Persian six, U+06F6) vs ٦ (Arabic six, U+0666)

These three (۴، ۵، ۶) are where Arabic-Indic digits most often leak into Persian output. Always verify.

**Mechanical fix:** after generating a Persian number, replace any U+0660–U+0669 codepoint with its U+06F0–U+06F9 counterpart (offset +0x90).

---

## 2. When to Use Digits vs. Words

Persian prose does not always use digits. Register matters.

| Situation | Style | Example |
|---|---|---|
| Small numbers in flowing prose (≤10, especially for counting) | Words | «سه کتاب خریدم» (not «۳ کتاب خریدم») |
| Large or precise numbers | Persian digits | «۱٬۲۳۴ نفر شرکت کردند» |
| Dates, times, measurements, prices, phone | Persian digits | «ساعت ۸ صبح»، «۵۰۰٬۰۰۰ تومان» |
| Technical, code, IDs, versions, ports | Western digits | «`port 8080`»، «نسخه 3.14» inside a code context |
| Percentages, statistics, data tables | Persian digits | «۲۳٫۵٪ رشد» |
| Formal/literary writing | Favor words for small numbers | «بیست سال پیش» > «۲۰ سال پیش» |
| Age (casual) | Persian digits | «۳۲ سالمه» |
| Chapter/section numbers | Words or digits; be consistent | «فصل سوم» or «فصل ۳» |

**Rule of thumb:** if a number *feels* like data (count, price, date, ID), use digits. If it *feels* like part of a sentence's rhythm (one, two, a few, twenty years), use words.

### Number Words — Quick Table

| Digit | Word | | Digit | Word |
|---|---|---|---|---|
| ۱ | یک | | ۱۰ | ده |
| ۲ | دو | | ۱۱ | یازده |
| ۳ | سه | | ۱۲ | دوازده |
| ۴ | چهار | | ۲۰ | بیست |
| ۵ | پنج | | ۳۰ | سی |
| ۶ | شش | | ۱۰۰ | صد |
| ۷ | هفت | | ۱٬۰۰۰ | هزار |
| ۸ | هشت | | ۱٬۰۰۰٬۰۰۰ | میلیون |
| ۹ | نه | | ۱٬۰۰۰٬۰۰۰٬۰۰۰ | میلیارد |

Compound: «بیست و سه»، «صد و پنجاه و هفت»، «دو هزار و چهارصد». Use «و» to join.

---

## 3. Separators — Thousands and Decimal

Persian uses **dedicated Unicode separators**, not Western `,` and `.`.

| Purpose | Character | Unicode | Example |
|---|---|---|---|
| Thousands (momayyez) | ٬ | U+066C | ۱٬۰۰۰٬۰۰۰ |
| Decimal (momayyez aashaari) | ٫ | U+066B | ۳٫۱۴ |
| Percent | ٪ | U+066A | ۲۵٪ |

**Common errors:**

| Wrong | Correct |
|---|---|
| ۱,۰۰۰,۰۰۰ (ASCII comma) | ۱٬۰۰۰٬۰۰۰ (U+066C) |
| ۳.۱۴ (ASCII period) | ۳٫۱۴ (U+066B) |
| 25% with Persian digits ۲۵% | ۲۵٪ (U+066A) |
| ۱٫۰۰۰٫۰۰۰ (decimal used as thousands) | ۱٬۰۰۰٬۰۰۰ |

**Notes:**
- Plain ASCII `.` and `,` *do* appear in Persian writing in practice, especially online, and are readable — but the Unicode separators are the correct typographic form. Default to correct form unless the user's existing text uses ASCII.
- In technical/code contexts, keep Western digits and Western separators together (`1,000,000` or `3.14`). Do not mix Persian digits with Western separators.

---

## 4. Ordinals

| Form | Example | Register / Use |
|---|---|---|
| Spelled out | اول، دوم، سوم، چهارم، پنجم | Default for prose |
| Digit + «م» | ۱م، ۲م، ۳م | Informal, compact (lists, UI) |
| Digit + «ام» | ۱ام، ۲ام، ۳ام | Informal alternative |
| Digit + «-م» | ۱-م، ۲-م | Rare, avoid |
| «نخست» for «اول» | نخستین بار | Literary/formal alternative |

**Irregular forms to memorize:** اول (not یکم in most contexts, though یکم exists for dates: «یکم فروردین»), سوم (not سهم), چهلم (۴۰), صدم (۱۰۰), هزارم (۱٬۰۰۰).

**Dates use «یکم» not «اول» for the first day:** «یکم فروردین ۱۴۰۵».

---

## 5. Dates (Solar Hijri — شمسی)

Iran's civil calendar is **Solar Hijri** (هجری خورشیدی / شمسی). Current year: ۱۴۰۵.

### Formats

| Style | Example | When |
|---|---|---|
| Numeric slashed | ۱۴۰۵/۰۱/۲۴ | Forms, receipts, tables |
| Year-first ISO-like | ۱۴۰۵-۰۱-۲۴ | Tech/log contexts |
| Written out | ۲۴ فروردین ۱۴۰۵ | Prose, letters, news |
| Full written | بیست و چهارم فروردین ۱۴۰۵ | Formal/literary |
| With weekday | پنج‌شنبه، ۲۴ فروردین ۱۴۰۵ | Letters, invitations |

**Order:** day/month/year in numeric form (**not** year/day/month). For the slashed form, YYYY/MM/DD is also acceptable and common in official documents — pick one and be consistent.

### Month Names (in order)

| # | شمسی | Gregorian span |
|---|---|---|
| ۱ | فروردین | Mar 21 – Apr 20 |
| ۲ | اردیبهشت | Apr 21 – May 21 |
| ۳ | خرداد | May 22 – Jun 21 |
| ۴ | تیر | Jun 22 – Jul 22 |
| ۵ | مرداد | Jul 23 – Aug 22 |
| ۶ | شهریور | Aug 23 – Sep 22 |
| ۷ | مهر | Sep 23 – Oct 22 |
| ۸ | آبان | Oct 23 – Nov 21 |
| ۹ | آذر | Nov 22 – Dec 21 |
| ۱۰ | دی | Dec 22 – Jan 20 |
| ۱۱ | بهمن | Jan 21 – Feb 19 |
| ۱۲ | اسفند | Feb 20 – Mar 20 |

### Weekdays

| Day | Persian |
|---|---|
| Saturday | شنبه |
| Sunday | یک‌شنبه |
| Monday | دوشنبه |
| Tuesday | سه‌شنبه |
| Wednesday | چهارشنبه |
| Thursday | پنج‌شنبه |
| Friday | جمعه |

Persian week starts on شنبه (Saturday). Weekend is پنج‌شنبه/جمعه (Thursday afternoon + Friday in practice; Friday only officially).

### Dual Dating (When Mixing Calendars)

When a date must be legible to both Iranian and international audiences, put شمسی first:

«۲۴ فروردین ۱۴۰۵ (۱۳ آوریل ۲۰۲۶)»

Do **not** silently convert Gregorian to شمسی in user content without signaling it.

---

## 6. Time

| Style | Example |
|---|---|
| Digital | ساعت ۸:۳۰ |
| With AM/PM | ساعت ۸:۳۰ صبح / ۸:۳۰ شب |
| 24-hour | ساعت ۲۰:۳۰ |
| Spoken | ساعت هشت و نیم |
| Quarter past | ساعت هشت و ربع |
| Quarter to | یک ربع به نه |
| Minutes | ساعت ۸ و ۱۰ دقیقه |

- Use **ASCII colon `:`** between hours and minutes — there is no Persian-specific time separator.
- «صبح» (morning), «ظهر» (noon), «بعدازظهر» (afternoon), «عصر» (late afternoon), «شب» (night), «نیمه‌شب» (midnight).

---

## 7. Phone Numbers

Iranian mobile format: 11 digits starting with `09`.

| Style | Example |
|---|---|
| Unformatted | ۰۹۱۲۱۲۳۴۵۶۷ |
| Grouped (common) | ۰۹۱۲ ۱۲۳ ۴۵۶۷ |
| With country code | +۹۸ ۹۱۲ ۱۲۳ ۴۵۶۷ or ۰۰۹۸۹۱۲۱۲۳۴۵۶۷ |
| Landline (Tehran) | ۰۲۱ ۸۸۱۲۳۴۵۶ |

- Use Persian digits in prose, Western in technical fields/forms where the backend expects ASCII.
- Do **not** insert momayyez (٬) in phone numbers — it's for thousands, not grouping.

---

## 8. Currency

Iran has two units in everyday use:

- **ریال (Rial)** — official currency, used in legal, banking, tax, and official documents
- **تومان (Toman)** — everyday unit, 1 تومان = 10 ریال. Used in shops, ads, casual speech, receipts

### Formatting

| Context | Example |
|---|---|
| Casual price | ۵۰٬۰۰۰ تومان |
| Formal/legal | مبلغ ۵۰۰٬۰۰۰ ریال |
| Large numbers (shorthand) | ۵ میلیون تومان، ۲ میلیارد تومان |
| Written out | پانصد هزار تومان |

- Always use momayyez (٬) for thousands: ۱٬۲۰۰٬۰۰۰ تومان.
- The unit follows the number with a space: «۵۰۰٬۰۰۰ تومان», not «۵۰۰٬۰۰۰تومان».
- In running prose, prefer the shorthand for readability: «حدود ۲ میلیون تومان» over «۲٬۰۰۰٬۰۰۰ تومان».

---

## 9. Percentages

| Style | Example | Notes |
|---|---|---|
| Number + ٪ | ۲۵٪ | Persian percent sign U+066A, no space |
| Number + درصد | ۲۵ درصد | Spelled out, space before درصد |
| Decimal percent | ۲۳٫۵٪ or ۲۳٫۵ درصد | Use momayyez (٫) for decimal |

- Prefer «درصد» in formal prose; «٪» in tables and UI.
- Do **not** use `%` (ASCII) with Persian digits.

---

## 10. Math and Operators

| Operator | Persian word | Symbol |
|---|---|---|
| + | جمع / به‌علاوهٔ | + |
| − | منها / منهای | − (U+2212) or - |
| × | ضربدر / در | × or * |
| ÷ | تقسیم بر | ÷ or / |
| = | مساوی با / برابر با | = |
| < | کوچک‌تر از | < |
| > | بزرگ‌تر از | > |

- In math expressions in Persian text: «۲ + ۳ = ۵» reads correctly thanks to the Unicode bidi algorithm.
- Use Persian digits in mathematical prose; Western digits in code blocks or LaTeX.

### Negative Numbers

- Written: «منفی ۵» or «-۵» (with leading minus).
- In tables, prefer the minus sign U+2212 («−۵») for typography.

### Ranges

| Style | Example | Use |
|---|---|---|
| Prose | «از ۱۰ تا ۲۰ نفر» | Preferred in flowing text |
| Dashed | «۱۰–۲۰» (en dash U+2013) | Tables, compact lists |
| Slashed | «۱۰/۲۰» | Ambiguous, avoid |

---

## 11. Numbers in RTL Flow

Numbers always render **left-to-right**, even inside RTL text. The Unicode bidirectional algorithm handles this automatically — **do not** manually reverse digits.

Correct: «قیمت ۱٬۲۳۴٬۵۶۷ تومان است.» (the number reads 1,234,567 LTR within the RTL sentence)

**Bidi pitfalls:**
- Leading/trailing punctuation on numbers can jump to the wrong side. If a number is followed by Persian text, put no space-control characters between them and let the algorithm work.
- If a number is genuinely misrendering (e.g., the last digit jumping to the start), wrap it with a Left-to-Right Embedding (LRE U+202A) + PDF (U+202C), but this is rarely needed.
- Never write digits backwards to "fix" display — the underlying bytes are always logical order.

---

## 12. Mixed Persian / Technical Content

| Context | Digit family | Separators |
|---|---|---|
| Persian prose with an embedded code token | Persian in prose, Western inside code | Persian separators in prose, Western inside code |
| Version numbers in tech writing | Western: «نسخه 3.14.0» | Western `.` |
| File sizes in a tutorial | Persian prose OK: «فایل ۲۰۰ مگابایت است» | Persian |
| SQL, JSON, YAML, URLs | Always Western | Always Western |
| UUIDs, hashes, API keys | Always Western | N/A |
| Timestamps in logs | Western | ISO format |

**Rule:** the digit family follows the **surrounding linguistic context**, not the document's overall language. A code block stays Western even in a Persian article.

---

## 13. Quality Checklist for Numerics

Before returning Persian text that contains numbers, verify:

- [ ] All digits are Persian (U+06F0–U+06F9), not Arabic-Indic (U+0660–U+0669)
- [ ] Thousands separator is ٬ (U+066C), not `,`
- [ ] Decimal separator is ٫ (U+066B), not `.`
- [ ] Percent sign is ٪ (U+066A), not `%`
- [ ] Dates use شمسی calendar, formatted day/month/year or YYYY/MM/DD consistently
- [ ] Currency: تومان in casual, ریال in formal, momayyez used, space before unit
- [ ] Time uses ASCII `:` between hours and minutes
- [ ] Ordinals match register (spelled out in prose, digit+م in lists)
- [ ] Small numbers in prose are spelled out where register calls for it
- [ ] Code/technical identifiers remain in Western digits
- [ ] Numbers inside RTL text are not manually reversed
- [ ] No mixed digit families in a single number (e.g., never «۱2۳»)

---

## 14. Mechanical Conversion Utilities (for Reference)

### Western → Persian digit mapping

```
0→۰  1→۱  2→۲  3→۳  4→۴  5→۵  6→۶  7→۷  8→۸  9→۹
```

### Arabic-Indic → Persian digit mapping (add 0x90 to codepoint)

```
٠→۰  ١→۱  ٢→۲  ٣→۳  ٤→۴  ٥→۵  ٦→۶  ٧→۷  ٨→۸  ٩→۹
```

### Separator replacements inside Persian numbers

```
,  →  ٬    (thousands)
.  →  ٫    (decimal — but only inside a number, not as sentence period!)
%  →  ٪    (percent)
```

**Caution:** never blindly replace `.` with `٫` across a whole document — only inside numeric literals. Sentence-ending periods stay `.`.
