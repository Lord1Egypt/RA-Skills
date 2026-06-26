# Persian Language Skill 📝

An [OpenClaw](https://openclaw.ai) capability layer that gives your AI native-level Persian (Farsi) fluency across any task.

## What It Does

Stop AI Persian mistakes forever. This skill automatically fixes:

- ✅ **Correct Unicode** — Uses ک/ی (Persian), not ك/ي (Arabic)
- ✅ **Proper half-spaces** — می‌خواهم، نمی‌توانم (not میخواهم)
- ✅ **Register matching** — Formal vs colloquial, automatic detection
- ✅ **Cultural context** — Ta'arof, Solar Hijri dates, Iranian conventions
- ✅ **RTL formatting** — Persian punctuation (« » ، ؛ ؟)
- ✅ **Natural translation** — Idioms, not word-for-word calques
- ✅ **Persian numerals** — Correct digit family (۰-۹, not ٠-٩), proper separators (٬ ٫ ٪)

Works for: Writing, translation, content generation, data extraction, code comments, and any Persian workflow.

---

## Recent Updates

### v2.0 (April 2026) — Persian Numerals Overhaul

**Major addition:** Comprehensive `numerals.md` reference file (13KB)

**What changed:**
- ✅ **Digit family correction** — Persian digits (۰-۹, U+06F0–U+06F9) vs Arabic-Indic (٠-٩, U+0660–U+0669)
- ✅ **Persian separators** — Thousands ٬ (U+066C), decimal ٫ (U+066B), percent ٪ (U+066A)
- ✅ **Solar Hijri dates** — Complete formatting guide (۱۴۰۵/۰۱/۲۴, ۲۴ فروردین ۱۴۰۵)
- ✅ **Currency** — Toman vs Rial, proper formatting (۵۰٬۰۰۰ تومان)
- ✅ **Phone numbers** — Iranian mobile/landline formats
- ✅ **Ordinals** — اول، دوم، سوم vs ۱م، ۲م، ۳م
- ✅ **Time, percentages, math** — Complete coverage
- ✅ **Mixed content rules** — When to use Persian vs Western digits
- ✅ **Quality checklist** — 12-point numeric verification

**Why this matters:**
- The #1 error in AI Persian output is wrong digit family (mixing ٤ with ۴)
- The #2 error is using Western separators (`,` and `.`) in Persian numbers
- This update fixes both permanently

**Updated files:**
- `SKILL.md` — Added numerals section to Core Instructions
- `references/numerals.md` — NEW 13KB comprehensive guide
- Quality checklist expanded with numeric checks

---

## Installation

### Option 1: Symlink (Recommended)

```bash
git clone https://github.com/nimaansari/persian-language.git
ln -s "$(pwd)/persian-language" ~/.openclaw/skills/persian-language
```

### Option 2: Direct Clone

```bash
cd ~/.openclaw/skills/
git clone https://github.com/nimaansari/persian-language.git
```

---

## Quick Examples

### Unicode: Right vs Wrong

**❌ Bad (Arabic Unicode):**
```
كتاب - ي - نمي خواهم
```

**✅ Good (Persian Unicode):**
```
کتاب - ی - نمی‌خواهم
```

### Register Matching

**❌ Formal email with informal ending:**
```
با احترام،
موضوع جلسه رو بررسی کردیم.
مرسی!
```

**✅ Consistent formal register:**
```
با احترام،
موضوع جلسه را بررسی کردیم.
با تشکر و احترام
```

### Half-Space Usage

**❌ Missing half-spaces:**
```
نمیتوانم کتابها را بخوانم
```

**✅ Correct half-spaces:**
```
نمی‌توانم کتاب‌ها را بخوانم
```

### Persian Numerals (NEW v2.0)

**❌ Wrong digit family (Arabic-Indic):**
```
قیمت ٤٥٬٠٠٠ تومان
```

**✅ Correct Persian digits:**
```
قیمت ۴۵٬۰۰۰ تومان
```

**❌ Western separators:**
```
۳.۱۴ درصد رشد ۱,۲۳۴,۵۶۷ نفر
```

**✅ Persian separators:**
```
۳٫۱۴ درصد رشد ۱٬۲۳۴٬۵۶۷ نفر
```

---

## Testing

Test with these prompts after installation:

- "Write a formal Persian email about a meeting"
- "Translate this to Persian: The project deadline is next Monday"
- "Fix this Persian text: كتاب را نمي خواهم"
- "Create a Persian Instagram caption for a sunset photo"
- "Summarize this article in Persian: [paste English text]"

---

## What's Included

| File | Purpose |
|------|---------|
| `SKILL.md` | Core skill instructions with triggers and quality checklist |
| `references/writing-standards.md` | Unicode, punctuation, RTL formatting rules |
| `references/numerals.md` | **NEW** Digit families, separators, dates, currency, phone, time, math |
| `references/tone-register.md` | Formal/informal registers, ta'arof, politeness guidelines |
| `references/common-mistakes.md` | AI error patterns in Persian + corrections |
| `references/transliteration.md` | Standard romanization when Latin script is needed |
| `references/content-templates.md` | Ready-made templates: email, social, report, announcement |

**Total:** 60KB of comprehensive Persian language guidance

---

## Use Cases

### ✍️ Content Writing
- Blog posts in Persian
- Social media captions (Instagram, Twitter, Telegram)
- Ad copy and marketing materials
- Product descriptions

### 📧 Professional Communication
- Formal business emails
- Reports and proposals
- Official announcements
- Academic writing

### 🌐 Translation
- English → Persian (natural, not literal)
- Persian → English (preserving tone and nuance)
- Technical documentation localization
- Subtitle and transcript translation

### 💻 Development
- Code comments in Persian
- Documentation in Farsi
- Localized UI strings
- Error messages and help text

---

## Quality Standards

Every Persian output is automatically checked for:

- [ ] No Arabic Unicode characters (ك → ک, ي → ی)
- [ ] Half-spaces in compound words (می‌، نمی‌، ها، ترین)
- [ ] Persian punctuation (« » ، ؛ ؟)
- [ ] Consistent register (formal/colloquial)
- [ ] Correct numerals (Persian for prose, Western for tech)
- [ ] Intact RTL formatting
- [ ] Natural translation (not word-for-word)
- [ ] Accurate cultural references

---

## Why This Skill?

Most AI models trained on general multilingual data make consistent mistakes with Persian:

1. **Wrong Unicode** — Uses Arabic ك/ي instead of Persian ک/ی
2. **Missing half-spaces** — Writes میخواهم instead of می‌خواهم
3. **Register confusion** — Mixes formal and informal inappropriately
4. **Cultural gaps** — Mishandles ta'arof, dates, and social context
5. **Literal translation** — Word-for-word calques instead of natural Persian

This skill fixes all of these by providing explicit guidance and reference materials.

---

## Requirements

- [OpenClaw](https://openclaw.ai) installed
- AI model with Persian support (Claude, GPT-4, Gemini, etc.)

---

## Contributing

Found an error pattern or want to add templates? PRs welcome!

1. Fork the repository
2. Add your improvements to the appropriate `references/` file
3. Update examples in `SKILL.md` if needed
4. Submit a pull request

---

## License

MIT License - see [LICENSE](LICENSE) for details

---

## Credits

Created by [Nima Ansari](https://github.com/nimaansari)

Part of the [OpenClaw](https://openclaw.ai) skills ecosystem

---

## Support

- 🐛 Issues: [GitHub Issues](https://github.com/nimaansari/persian-language/issues)
- 💬 Discussions: [OpenClaw Discord](https://discord.com/invite/clawd)
- 📚 Docs: [OpenClaw Documentation](https://docs.openclaw.ai)

---

**تبریک! حالا هوش مصنوعی شما فارسی را درست می‌نویسد.** 🎉
