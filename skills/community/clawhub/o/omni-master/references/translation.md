# Translation

## Approaches

### AI Translation (Preferred)
- Use the model itself for high-quality translation
- Best for: prose, emails, articles, UI text
- Supports virtually any language pair

### Tool-Based Translation
- DeepL API (highest quality for European languages)
- Google Translate API
- LibreTranslate (self-hosted)

### CLI Tools
```bash
# Using translate-shell
trans :es "Hello, how are you?"
trans -brief :ja "Good morning"
trans -download :fr "document.pdf"
```

## Translation Workflow
1. Identify source and target languages
2. Detect domain (technical, literary, casual)
3. Translate preserving meaning and tone
4. Review for cultural appropriateness
5. Verify technical terms

## Specialized Translation

### Code/Technical
- Preserve code blocks, variables, function names
- Translate comments and documentation
- Keep error messages translatable (i18n patterns)

### UI/UX Strings
- Maintain placeholder tokens: `{name}`, `%s`
- Consider text expansion (German ~30% longer than English)
- Right-to-left support for Arabic, Hebrew

### Legal/Financial
- Use precise terminology
- Note untranslatable legal concepts
- Flag for human review

### Literary
- Preserve style and voice
- Adapt idioms rather than literal translate
- Consider cultural context

## i18n Best Practices
- Externalize all user-facing strings
- Use ICU message format for plurals
- Support date/number locale formatting
- Test with pseudo-localization

## Common Language Codes
en, es, fr, de, ja, ko, zh-CN, zh-TW, ar, ru, pt, it, hi, tr, nl, pl, sv
