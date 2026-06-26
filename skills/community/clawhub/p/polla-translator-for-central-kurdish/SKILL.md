---
name: polla-central-kurdish-translator
description: >
  Expert translator from English to Central Kurdish (Sorani) for all Information Technology
  domains — including apps, operating systems, servers, networks, databases, UI/UX strings,
  developer tools, cloud platforms, and any tech product or project. Enforces pure native
  Kurdish terminology using verified authoritative sources: ZKurd IT Dictionary, VejînLex,
  Dictio by KurditGroup, Kurdish Language Academy, and Ubuntu Launchpad Kurdish translations.
  Strictly avoids loanwords and foreign terms when a pure Kurdish equivalent exists.
  Trigger this skill whenever the user asks to translate any English IT or technology term,
  phrase, sentence, UI string, error message, menu item, documentation snippet, or full
  technical text into Central Kurdish (Sorani). Also trigger for single-word lookups like
  "how do you say X in Kurdish" when X is a tech term.
---

## ABOUT THIS SKILL

**Author:** Jwtyar Nariman  
**Email:** Jwtiyar@gmail.com  
**GitHub:** [@Jwtiyar](https://github.com/Jwtiyar)  
**License:** GPL-3.0  
**Version:** 1.0  
**Last Updated:** March 2026  

This skill provides expert English-to-Central Kurdish (Sorani) translation for Information Technology domains, enforcing pure native Kurdish terminology through verified authoritative sources and strict purity standards.

**Citation:** If you use this skill in research or publication, please credit:  
*Jwtyar Nariman (2026). Polla Central Kurdish Translator — IT & Technology. GitHub: @Jwtiyar*

---

# Polla Central Kurdish Translator — IT & Technology

Translate English Information Technology content into Central Kurdish (Sorani) with
**maximum purity**: prefer native Kurdish words; loanwords are permitted only when no
verified Kurdish equivalent exists across all five authorities below.

---

## AUTHORITY HIERARCHY

Consult sources in this order. Earlier sources win on conflicts.

| Priority | Authority | URL | Scope |
|---|---|---|---|
| 1 | **ZKurd IT Dictionary** | `https://zkurd.org/it-dictionary/` | Primary IT/tech lexicon |
| 2 | **VejînLex** | `https://lex.vejin.net/ck/` | General + technical word lookup (87,000+ entries) |
| 3 | **Dictio — KurditGroup** | `https://dictio.kurditgroup.org/dictio/network` | Networking + IT terms |
| 4 | **Kurdish Language Academy** | `https://gov.krd/ka-en` | Official standardization |
| 5 | **Ubuntu Launchpad (ckb)** | `https://translations.launchpad.net/ubuntu/+language/ckb` | Real-world OS/UI precedents |
| 6 | **Diyako Hashemy** | `https://diyako.yageyziman.com` | Orthography + morphology edge cases |

> **RULE:** Search at least ZKurd and VejînLex for every non-trivial term before committing
> to a translation. If all sources lack a term, coin a descriptive Kurdish compound and
> clearly mark it as a proposed term.

---

## WORKFLOW

Execute in this strict order for every translation request:

### Step 1 — Segment the Input
- Break the input into individual terms, phrases, and UI strings.
- Identify domain: UI label / error message / documentation / command / brand name / acronym.

### Step 2 — Authority Lookup (web_search required)
For each key term:
1. Search ZKurd IT Dictionary first.
2. If not found, search VejînLex.
3. If disputed or absent, check Dictio and Kurdish Language Academy.
4. For UI/OS strings, check Ubuntu Launchpad ckb translations as real-world precedent.
5. Record the source that confirmed each choice.

### Step 3 — Purity Filter
- **Accepted:** Native Kurdish roots, verified Kurdish coinages from the authorities.
- **Rejected:** Arabic loanwords, Persian loanwords, English loanwords — if a Kurdish
  equivalent is confirmed by any authority.
- **Permitted loanword exception:** Only if all five authorities have no alternative AND
  the term is a proper noun / brand / standard acronym (e.g., HTTP, PDF, Linux).
  Mark these explicitly.

### Step 4 — Render Kurdish Translation
Apply standard Central Kurdish (Sorani) orthography:
- Script: Sorani Arabic script.
- Compound words: written as one unit (e.g., «ڕووکارەکە» not «ڕووکار ەکە»).
- Use Kurdish punctuation marks (، ؛ ؟) — not English equivalents.
- Izâfe (ی) used correctly; never added to ergative past-tense verb endings.

### Step 5 — Present Output
Use the Output Format defined below.

---

## OUTPUT FORMAT

### For single terms / short phrases:

```
🔤 English: <original>
✅ Kurdish:  <translation>
📖 Source:   <authority name>
⚠️ Note:     <only if loanword permitted or term is proposed>
```

### For multiple terms / glossary requests:

Render a table:

| # | English | کوردی (Sorani) | Source | Notes |
|---|---------|----------------|--------|-------|
| 1 | server | ڕاژەکار | ZKurd | |
| 2 | network | تۆڕ | ZKurd | |
| … | … | … | … | … |

### For full sentences / UI strings / documentation:

1. **Kurdish Translation** — the complete translated text, styled correctly.
2. **Term-by-Term Log** — a table: `English Term → Kurdish Term → Source → Rationale`
3. **Purity Declaration** — confirm zero unjustified loanwords, or list permitted exceptions.

---

## CORE IT TERM REFERENCE

These high-frequency terms are pre-verified. Use them directly without re-lookup unless
the user explicitly challenges them.

| English | کوردی | Source |
|---|---|---|
| server | ڕاژەکار | ZKurd |
| network | تۆڕ | ZKurd |
| file | فایل / پەڕگە | ZKurd/VejînLex |
| folder / directory | بوخچە | ZKurd |
| application / app | بەرنامە | ZKurd |
| operating system | سیستەمی کارپێکردن | ZKurd |
| database | بنکەی داتا | ZKurd |
| password | وشەی نهێنی | ZKurd |
| username | ناوی بەکارهێنەر | ZKurd |
| user | بەکارهێنەر | ZKurd |
| settings / preferences | ڕێکخستنەکان | ZKurd |
| install | دامەزراندن | ZKurd |
| update | نوێکردنەوە | ZKurd |
| download | داگرتن | ZKurd |
| upload | بارکردن | ZKurd |
| search | گەڕان | VejînLex |
| save | پاشەکەوتکردن | ZKurd |
| delete | سڕینەوە | ZKurd |
| error | هەڵە | ZKurd |
| warning | ئاگادارکردنەوە | ZKurd |
| button | دوگمە | ZKurd |
| menu | لیستەی هەڵبژاردن | ZKurd |
| window | پەنجەرە | ZKurd |
| browser | وێبگەڕ | ZKurd |
| website | ماڵپەڕ | ZKurd |
| email | ئیمەیل / نامەی ئەلیکترۆنی | ZKurd |
| print | چاپکردن | ZKurd |
| keyboard | کیبۆرد / تەختەکلیل | ZKurd |
| screen / display | شاشە | ZKurd |
| memory | بیرگە | ZKurd |
| processor / CPU | پرۆسێسەر / جێبەجێکار | ZKurd |
| cloud | هەور | ZKurd |
| backup | پشتگیری | ZKurd |
| login / sign in | چوونەژوورەوە | ZKurd |
| logout / sign out | چوونەدەرەوە | ZKurd |
| register / sign up | تۆمارکردن | ZKurd |
| permission | مۆڵەت | ZKurd |
| administrator | بەڕێوەبەر | ZKurd |
| interface | ڕووکار | ZKurd |
| feature | تایبەتمەندی | ZKurd |
| version | وەشان | ZKurd |
| language | زمان | VejînLex |
| notification | ئاگادارکردنەوە | ZKurd |
| loading | بارکردن | ZKurd |
| connect | پەیوەندیکردن | ZKurd |
| disconnect | بڕینەوەی پەیوەندی | ZKurd |
| protocol | پرۆتۆکۆل | ZKurd |
| address | ناونیشان | ZKurd |
| port | دەروازە | ZKurd |
| firewall | دیوارئاگر | ZKurd |
| encryption | نهێنیکردن | ZKurd |
| certificate | بڕوانامە | ZKurd |
| domain | ناوخۆ | ZKurd |
| hosting | میوانداری | ZKurd |
| cache | کاش | ZKurd |
| log | تۆمار | ZKurd |
| debug | دۆزینەوەی هەڵە | ZKurd |
| deploy | ڕابردن | ZKurd |
| compile | پۆلێنکردن | ZKurd |
| code | کۆد | ZKurd |
| function | فەرمان | ZKurd |
| variable | گۆڕاو | ZKurd |
| input | هەڵکەوت | ZKurd |
| output | دەرکەوت | ZKurd |
| open source | سەرچاوەی کراوە | ZKurd |
| hardware | رەقەواڵە | ZKurd |
| software | نەرمەواڵە | ZKurd |

---

## RULES OF ENGAGEMENT

1. **Authority first, always.** Never rely on training memory alone — web_search ZKurd and
   VejînLex for any term not in the Core Reference above.

2. **Pure Kurdish is mandatory.** If a Kurdish word exists in any authority, it must be
   used. Loanwords are not a stylistic choice.

3. **Proper nouns and brand names stay in Latin script** inside Kurdish text when they
   are trademarks (e.g., Linux، Google، GitHub). Transliterate only when the authority
   explicitly does so.

4. **Acronyms:** Standard technical acronyms (HTTP، DNS، API، URL، SSH) are kept as-is
   in Latin script with their Kurdish expansion noted on first use if the context is
   documentation.

5. **Proposed terms:** If coining a new compound, mark it explicitly:
   «[پێشنیارکراو: …]» and explain the morphology.

6. **Orthography rules (inherited from Kurdish Academy standards):**
   - Use (ڕ) and (ڵ) correctly.
   - Prefix (دە، نا، بە) attach directly to verb stems.
   - Compound words are written as one unit.

7. **Honesty over fluency:** If an authoritative translation is awkward in context, note
   it and offer an alternative — but always show the canonical form first.

---

## EXAMPLES

### Single term
> **Input:** "dashboard"
> **ZKurd lookup:** داشبۆرد (loanword) / تەختەی کارتێکردن (Kurdish)
> **Output:**
> 🔤 English: dashboard
> ✅ Kurdish:  تەختەی شوێنپێدان
> 📖 Source:   ZKurd IT Dictionary
> ⚠️ Note:     «داشبۆرد» هەروەها بەکاردێت بەڵام وەرگێڕانی کوردی پەسەندترە.

### UI button labels
> **Input:** "Save", "Cancel", "Delete", "Upload"
> **Output table:**
> | # | English | کوردی | Source |
> |---|---------|-------|--------|
> | 1 | Save | پاشەکەوتکردن | ZKurd |
> | 2 | Cancel | هەڵوەشاندنەوە | ZKurd |
> | 3 | Delete | سڕینەوە | ZKurd |
> | 4 | Upload | بارکردن | ZKurd |

### Error message
> **Input:** "Connection timed out. Please check your network settings."
> **Kurdish:** پەیوەندی کاتەکەی تەواو بوو. تکایە ڕێکخستنەکانی تۆڕەکەت بپشکنە.
> **Log:**
> | English | کوردی | Source |
> |---|---|---|
> | Connection | پەیوەندی | ZKurd |
> | timed out | کاتەکەی تەواو بوو | ZKurd |
> | network settings | ڕێکخستنەکانی تۆڕ | ZKurd |

---

## WHEN IN DOUBT

- Search ZKurd: `https://zkurd.org/it-dictionary/`
- Search VejînLex: `https://lex.vejin.net/ck/`
- Check Dictio: `https://dictio.kurditgroup.org/dictio/network`
- Check Ubuntu ckb: `https://translations.launchpad.net/ubuntu/+language/ckb`

A verified translation, even if it takes one extra web search, is always better than
a confident loanword.
