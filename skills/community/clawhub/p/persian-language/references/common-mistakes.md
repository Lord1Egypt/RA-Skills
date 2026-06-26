# Common AI Mistakes in Persian Generation

This file catalogs recurring errors that AI models make when generating Persian text, with corrections and explanations.

---

## 1. Unicode Errors

### Arabic Characters Instead of Persian

**The most frequent and most visible error.**

| Error | Correction | How to Detect |
|---|---|---|
| ك (U+0643) | ک (U+06A9) | Search for U+0643 in output |
| ي (U+064A) | ی (U+06CC) | Search for U+064A in output |
| ة (U+0629 taa marbuta) | ه (U+0647) or ت | Context-dependent |
| ؤ (U+0624) | و (rare in Persian) | Almost never used in Persian |
| ئ (U+0626) | ی or ئ (context) | Only valid in specific words |

**Fix:** After generating Persian text, programmatically replace Arabic variants with Persian equivalents. This is a mechanical fix that should always be applied.

### Missing Half-Spaces

| Error | Correction | Rule |
|---|---|---|
| میروم | می‌روم | می + verb always gets half-space |
| نمیدانم | نمی‌دانم | نمی + verb always gets half-space |
| کتابها | کتاب‌ها | noun + ها plural |
| بزرگترین | بزرگ‌ترین | adjective + ترین superlative |
| خانهای | خانه‌ای | noun + ای indefinite |

**Fix:** Apply half-space rules systematically. When in doubt, use a half-space — it's almost never wrong to separate a prefix/suffix from its root.

---

## 2. Grammar Errors

### Wrong Verb Conjugation

Persian verbs conjugate by person/number. Common AI errors:

| Error | Correction | Issue |
|---|---|---|
| من می‌رود | من می‌روم | First person needs -م ending |
| ما می‌کنم | ما می‌کنیم | Plural subject needs plural verb |
| آن‌ها رفتم | آن‌ها رفتند | Third person plural needs -ند |

### Ezafe Construction Errors

The ezafe (-e) links nouns to modifiers. It's unwritten but must be grammatically correct:

| Error | Correction | Rule |
|---|---|---|
| کتابِ بزرگِ | کتابِ بزرگ | No ezafe on final adjective |
| خانه‌ی من (in formal) | خانهٔ من or خانه من | Use hamze or omit in formal |
| دوست خوب من | دوستِ خوبِ من | Ezafe needed between each link |

### Subject-Object-Verb Order Violations

Persian is SOV (Subject-Object-Verb). AI models trained primarily on English (SVO) sometimes produce unnatural word order:

- Wrong: «من دارم می‌خوانم کتاب را» (SVO-like)
- Right: «من دارم کتاب را می‌خوانم» or «من کتاب را دارم می‌خوانم»

**Fix:** Always place the verb at the end of the clause in standard Persian.

### را (rā) Marker Errors

را marks definite direct objects. Common mistakes:

| Error | Correction | Rule |
|---|---|---|
| من کتاب خواندم | من کتاب را خواندم | Definite object needs را |
| من یک کتاب را خواندم | من یک کتاب خواندم | Indefinite objects don't take را |
| به او را گفتم | به او گفتم | Indirect objects (with preposition) don't take را |

---

## 3. Translation Errors

### Literal Calques (Word-for-Word Translation)

| English | Wrong Persian (Calque) | Natural Persian |
|---|---|---|
| "It makes sense" | آن حس می‌سازد | منطقی است / درست است |
| "I'm looking forward to" | من به جلو نگاه می‌کنم | مشتاقانه منتظرم / بی‌صبرانه چشم به راهم |
| "At the end of the day" | در پایان روز (literal) | در نهایت / نهایتاً |
| "Keep in mind" | در ذهنت نگه‌دار | در نظر داشته باش / یادت باشه |
| "Break the ice" | یخ را بشکن | سر صحبت را باز کردن |
| "It's up to you" | آن بالای توست | دست خودته / به خودت بستگی داره |
| "Take it easy" | آن را آسان بگیر | بی‌خیال / سخت نگیر |

### Over-Formal Translation

AI tends to generate overly stiff Persian when translating casual English:

| English | Over-Formal | Natural |
|---|---|---|
| "Hey, what's up?" | سلام، اوضاع و احوال شما چگونه است؟ | سلام، چطوری؟ / سلام، چه خبر؟ |
| "Got it, thanks!" | فهمیدم، از شما متشکرم! | فهمیدم، ممنون! / باشه، مرسی! |
| "No worries" | هیچ نگرانی‌ای وجود ندارد | نگران نباش / مشکلی نیست |

### Under-Formal Translation

Less common, but sometimes AI is too casual for a formal context:

| English | Under-Formal | Appropriate Formal |
|---|---|---|
| "Please be advised" | بدون اینکه | به استحضار می‌رساند |
| "We regret to inform" | متأسفیم بگیم | با کمال تأسف به اطلاع می‌رساند |

---

## 4. Register Mixing

### Mixing Formal and Colloquial in One Text

This is a very common AI error — starting formal and drifting colloquial, or vice versa.

**Indicators of formal register:** شما، می‌باشد، است، بنده، خواهشمند است، به عرض می‌رساند
**Indicators of colloquial register:** تو، -ه (هست → هس / است → ـه)، میشه، نمیشه، چطوری

**Rule:** Pick one register and maintain it throughout the text. If the user hasn't specified, match the register of their input. If generating from scratch for a specific context, use:
- Formal: official documents, business emails, academic text, news
- Colloquial: social media, casual messaging, dialogue, captions

### Colloquial Verb Forms (For Reference)

| Formal | Colloquial | Meaning |
|---|---|---|
| می‌خواهم | می‌خوام | I want |
| نمی‌دانم | نمی‌دونم | I don't know |
| می‌گویم | می‌گم | I say |
| می‌آید | میاد | It comes |
| می‌رود | می‌ره | It goes |
| است | ـه / هست | is |
| نیست | نیس | is not |
| می‌شود | می‌شه | it becomes / is possible |
| نمی‌شود | نمی‌شه | it's not possible |
| بگویید | بگید | say (imperative, plural/formal) |

---

## 5. Cultural Errors

### Mishandling Ta'arof

Ta'arof expressions are **formulaic** and should not be taken literally:

| Expression | Literal Meaning | Actual Meaning |
|---|---|---|
| قابلی نداره | It has no worth | You're welcome / Don't mention it |
| قدم‌تان روی چشم | Your step on my eye | You're very welcome (to visit) |
| خواهش می‌کنم | I beg of you | You're welcome |
| ببخشید زحمت‌تان دادم | Sorry I troubled you | Thank you for your help |
| تعارف نکنید | Don't do ta'arof | Please, go ahead / Don't be polite |

### Wrong Calendar

Iran uses the **Solar Hijri** (شمسی / هجری خورشیدی) calendar. AI models often output Gregorian dates without conversion.

- Current Solar Hijri year: ۱۴۰۵
- New Year (نوروز): ۱ فروردین = approximately March 20-21 Gregorian
- When writing dates for an Iranian audience, **always provide شمسی first**, optionally Gregorian in parentheses

### Currency

- Iran's official currency: ریال (Rial)
- Common spoken unit: تومان (Toman) = ۱۰ ریال
- In casual/commercial contexts, prices are almost always in تومان
- In official/legal/banking contexts, use ریال

---

## 6. Formatting Errors

### Wrong Quote Marks

- Wrong: "متن فارسی" (English double quotes)
- Wrong: 'متن فارسی' (English single quotes)
- Right: «متن فارسی» (guillemets)
- For nested quotes: «او گفت: ‹برو›»

### Wrong Comma/Question Mark

- Wrong: متن فارسی, ادامه
- Right: متن فارسی، ادامه
- Wrong: آیا درسته?
- Right: آیا درسته؟

### Number Direction in RTL

When numbers appear in RTL text, they still read left-to-right. Don't reverse them:
- Right: قیمت ۵۰۰٬۰۰۰ تومان است
- The number ۵۰۰٬۰۰۰ reads as 500,000 (left to right within RTL flow)
