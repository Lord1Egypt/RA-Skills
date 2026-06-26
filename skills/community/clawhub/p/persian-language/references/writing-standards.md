# Persian Writing Standards

## Unicode Character Rules

### Persian-Specific Characters (Must Use)

| Character | Persian (Correct) | Arabic (Wrong) | Unicode |
|---|---|---|---|
| Kaf | ک | ك | U+06A9 (not U+0643) |
| Yeh | ی | ي | U+06CC (not U+064A) |
| Heh (word-final) | ه | ة | U+0647 (not U+0629) |

Always verify these after generation. AI models frequently default to Arabic Unicode variants.

### Half-Space (نیم‌فاصله) — U+200C (Zero-Width Non-Joiner)

The half-space is essential in Persian typography. It separates compound elements while keeping them visually connected.

**Where to use half-space:**

| Pattern | Wrong | Correct |
|---|---|---|
| می + verb | میخواهم / می خواهم | می‌خواهم |
| نمی + verb | نمیدانم / نمی دانم | نمی‌دانم |
| Noun + ها (plural) | کتابها / کتاب ها | کتاب‌ها |
| Noun + ترین (superlative) | بزرگترین / بزرگ ترین | بزرگ‌ترین |
| Noun + تر (comparative) | بهتر (single word) | بزرگ‌تر (compound) |
| Ezafe + ای | خانهای / خانه ای | خانه‌ای |
| Possessive suffix | کتابم / کتاب م | کتابم (short) or کتاب‌ام (full) |
| Compound nouns | دانشگاه (single word) | هم‌کلاسی (compound) |

**Rule of thumb:** if removing the suffix leaves a complete word, use a half-space. If the result is not a standalone word, join directly.

---

## Punctuation

### Persian Punctuation Marks

| Purpose | Persian | Western (Wrong in Persian) |
|---|---|---|
| Comma | ، (U+060C) | , |
| Semicolon | ؛ (U+061B) | ; |
| Question mark | ؟ (U+061F) | ? |
| Quotation marks | «متن» (guillemets) | "متن" |
| Period | . (same as Latin) | . |
| Exclamation | ! (same as Latin) | ! |
| Colon | : (same as Latin) | : |
| Ellipsis | … (same as Latin) | ... |
| Parentheses | () (same as Latin) | () |
| Dash | — (em dash) or – (en dash) | - |

### Punctuation Placement in RTL

- Punctuation follows the **logical order** of the sentence, not the visual direction
- Closing punctuation (؟ ، ؛) appears at the **end** of the clause in logical order
- In mixed LTR/RTL text, use Unicode bidirectional controls if needed to prevent punctuation displacement

---

## Numerals

### When to Use Which System

| Context | Numeral Style | Example |
|---|---|---|
| Prose / running text | Persian (۰۱۲۳۴۵۶۷۸۹) | ۱۲ نفر حاضر بودند |
| Dates (شمسی) | Persian | ۱۴۰۵/۰۱/۲۱ |
| Technical / code | Western (0123456789) | `port 8080` |
| Phone numbers | Western or Persian (user preference) | ۰۹۱۲۱۲۳۴۵۶۷ or 09121234567 |
| Financial (ریال/تومان) | Persian in text, Western in tables | ۵۰۰٬۰۰۰ تومان |
| Mixed content | Match the surrounding script | — |

### Persian Numeral Mapping

| Western | Persian |
|---|---|
| 0 | ۰ |
| 1 | ۱ |
| 2 | ۲ |
| 3 | ۳ |
| 4 | ۴ |
| 5 | ۵ |
| 6 | ۶ |
| 7 | ۷ |
| 8 | ۸ |
| 9 | ۹ |

### Thousands Separator

- In Persian text: use momayyez (٬) U+066C — e.g., ۱٬۰۰۰٬۰۰۰
- Decimal separator: ممیز (/) or (٫) U+066B — e.g., ۳٫۱۴

---

## RTL Formatting Guidelines

### General Rules

1. Persian text flows **right-to-left**. All block-level elements (paragraphs, headings, list items) should start from the right.
2. Embedded Latin text (English words, code, URLs) runs **left-to-right** within the RTL flow. The Unicode Bidirectional Algorithm handles most cases automatically.
3. Do **not** add extra spaces around embedded LTR text to "fix" alignment — this usually makes it worse.

### Mixed Content Best Practices

- When a sentence mixes Persian and English, keep the sentence structure in Persian word order (SOV) and slot English terms where they naturally fall
- Example: «ما از فریم‌ورک React برای فرانت‌اند استفاده می‌کنیم.»
- For technical terms with no natural Persian equivalent, use the English term — do not force awkward translations
- Well-established Persian equivalents should be preferred: نرم‌افزار (software), سخت‌افزار (hardware), پایگاه داده (database), رایانامه (email — though ایمیل is more common in practice)

### Code Blocks and Technical Content

- Code blocks are always LTR regardless of surrounding text
- Persian comments inside code should still use correct Persian Unicode and punctuation
- Variable names and identifiers stay in Latin script

---

## Spacing Rules

- One space after punctuation marks (، ؛ . : ؟ !)
- No space before punctuation marks
- Space before opening parenthesis, no space after: (متن)
- Space after closing parenthesis, no space before: (متن)
- No space inside guillemets: «متن» not « متن »
