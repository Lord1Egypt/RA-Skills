# CLI Usage Reference (music-with-comfyui)

Companion to SKILL.md. The core rule is already in [SKILL.md](../SKILL.md)
"CLI Usage" and full command examples are in the README "CLI Reference": write
the music description through `--tags "..."` on the **first** attempt (never a
positional word), and always pass `--tags` / `--lyrics` as inline text — never
as a file path. This file exists only for the one lookup that doesn't fit
there.

## Language codes

`--language` (node input `language` of `TextEncodeAceStepAudio1.5`) accepts
exactly these 51 values — anything else is rejected by the server. Default:
`en`. The lyrics you pass must be written in the same language (a `zh` song
needs Chinese lyrics, not English).

| Code | Language | Code | Language |
|---|---|---|---|
| `ar` | Arabic (العربية) | `hr` | Croatian (Hrvatski) |
| `az` | Azerbaijani (Azərbaycan) | `hu` | Hungarian (Magyar) |
| `bg` | Bulgarian (Български) | `id` | Indonesian (Bahasa Indonesia) |
| `bn` | Bengali (বাংলা) | `is` | Icelandic (Íslenska) |
| `ca` | Catalan (Català) | `it` | Italian (Italiano) |
| `cs` | Czech (Čeština) | `ja` | Japanese (日本語) |
| `da` | Danish (Dansk) | `ko` | Korean (한국어) |
| `de` | German (Deutsch) | `la` | Latin (Latina) |
| `el` | Greek (Ελληνικά) | `lt` | Lithuanian (Lietuvių) |
| `en` | English | `ms` | Malay (Bahasa Melayu) |
| `es` | Spanish (Españés) | `ne` | Nepali (नेपाली) |
| `fa` | Persian (فارسی) | `nl` | Dutch (Nederlands) |
| `fi` | Finnish (Suomi) | `no` | Norwegian (Norsk) |
| `fr` | French (Français) | `pa` | Punjabi (ਪੰਜਾਬੀ) |
| `he` | Hebrew (עברית) | `pl` | Polish (Polski) |
| `hi` | Hindi (हिंदी) | `pt` | Portuguese (Português) |
| `ro` | Romanian (Română) | `ru` | Russian (Русский) |
| `sa` | Sanskrit (संस्कृतम्) | `sk` | Slovak (Slovenčina) |
| `sr` | Serbian (Српски) | `sv` | Swedish (Svenska) |
| `sw` | Swahili (Kiswahili) | `ta` | Tamil (தமிழ்) |
| `te` | Telugu (తెలుగు) | `th` | Thai (ไทย) |
| `tl` | Filipino/Tagalog | `tr` | Turkish (Türkçe) |
| `uk` | Ukrainian (Українська) | `ur` | Urdu (اردو) |
| `vi` | Vietnamese (Tiếng Việt) | `yue` | Cantonese (粵語) |
| `zh` | Chinese (Mandarin, 普通话) | `ht` | Haitian Creole (Kreyòl Ayisyen) |
| `unknown` | undetected / let the model decide |  |  |
