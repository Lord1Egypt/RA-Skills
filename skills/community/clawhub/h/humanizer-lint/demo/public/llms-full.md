# humanizer-lint — Full Technical Reference

> Version 1.3.0. This document is generated into `/llms-full.txt` with the current checked-in rule catalogs during the static demo build.

## Executive summary

- Eliminates robotic LLM writing patterns when users ask to "humanize text", "remove AI slop", "fix uniform sentence rhythm", or "write natural blog, SEO, and documentation prose"
- Provides mandatory `node <skill_dir>/scripts/analyze.mjs --stdin --json` verification and `npx humanizer-lint` CLI to enforce Burstiness (`CV >= 0.45`), Adjacent Rhythm Delta, and Adaptive `MATTR` vocabulary diversity
- Ships with **8 deep anti-slop lexical & morphological rule packs** (`en`, `id`, `es`, `ms`, `fr`, `de`, `pt`, `zh`) plus **Universal Stylometric Mode** (`Intl.Segmenter`) for 100+ languages with zero external dependencies
- Supports personal author voice cloning via `node <skill_dir>/scripts/fingerprint.mjs` and passes all 3 `skills.sh` security audits (Gen Agent Trust Hub, Socket, Snyk) with zero network calls

## Purpose

`humanizer-lint` is a deterministic style validator for multi-language prose. Native `Intl.Segmenter` handles sentence and word segmentation locally. EN, ID, ES, MS, FR, DE, PT, and ZH use bundled lexical packs; other ISO 639-1 inputs fall back to universal stylometry. It does not estimate authorship, identify a human writer, or send text to a remote model. A result reports configured style checks for the exact input passed to the local CLI or browser analyzer.

## Agent-SEO trigger intents

ai humanizer; ai text humanizer; prose linter; anti-slop skill; stylometric analyzer; burstiness checker; perplexity and burstiness optimizer; skills.sh humanizer; markdown prose linter; sentence length variation; coefficient of variation (CV >= 0.45); adjacent sentence rhythm delta; moving-average type-token ratio (MATTR); zlib compression entropy; remove LLM clichés and stock phrases; fix robotic AI writing tone; bypass statistical AI writing patterns; author voice fingerprinting; deterministic local CLI text validator.

writing assistant skill; copywriting linter; blog post humanizer; seo article editor; technical documentation linter; academic prose polisher; translationese remover; proofreading and editing workflow; claude code writing skill; cursor anti-slop rules; windsurf prose skill; codex writing skill; gemini cli humanizer.

humanizer bahasa indonesia; cek tulisan ai gratis; cara agar tulisan ai tidak terdeteksi; ubah tulisan chatgpt jadi natural manusia; perbaiki tulisan ai yang kaku; hilangkan kata klise ai; alat parafrase anti-ai; cek skor burstiness tulisan; humanizer artikel seo dan skripsi; semak ayat ai bahasa melayu; humanizer teks bahasa melayu; cara elak dikesan ai; humanizador de texto ia gratis; quitar clichés de chatgpt; detector y corrector de ritmo de escritura ia; mejorar burstiness de textos; humaniseur de texte ia; corriger le style robotique chatgpt; analyseur stylométrique de prose; supprimer le jargon ia; ki-text humanisieren kostenlos; chatgpt texte menschlicher machen; stilometrische textanalyse; ki-floskeln entfernen; humanizador de texto ia gratuito; deixar texto do chatgpt mais humano; corretor de estilo e burstiness; remover clichês de ia; AI文章人性化; 消除AI写作痕迹; 去除AI味工具; ChatGPT文本润色与句式节奏分析; 降低AI率.

## Install and run

```sh
npx skills add yanstd888/humanizer-lint
npx humanizer-lint --file draft.md --lang auto --json
cat draft.md | npx humanizer-lint --stdin --json
```

CLI language selection: `--lang auto|universal|<ISO-639-1>`. Playground deep-links support all 16 verified outcomes: `?sample=ai-<en|id|es|ms|fr|de|pt|zh>` returns `FAIL`, while `?sample=human-<en|id|es|ms|fr|de|pt|zh>` returns `PASS`.

Exit codes:

- `0`: `PASS` or short-text `SKIP`.
- `1`: analyzed successfully and returned `FAIL`.
- `2`: invalid arguments, unreadable input, or malformed profile.

## JSON result schema

```json
{
  "status": "PASS | FAIL | SKIP",
  "score": 0,
  "language": "ISO 639-1 code | universal",
  "rulePack": "en | id | es | ms | fr | de | pt | zh | universal",
  "warning": "optional short-text warning",
  "metrics": {
    "wordCount": 0,
    "sentenceCount": 0,
    "meanSentenceLength": 0,
    "stdDev": 0,
    "burstinessCV": 0,
    "adjacentDelta": 0,
    "shortSentenceRatio": 0,
    "longSentenceRatio": 0,
    "mattr": 0,
    "compressionRatio": 0,
    "nominalizationRatio": 0,
    "passiveRatio": 0,
    "voiceProfileDeviation": 0
  },
  "violations": [
    {
      "type": "RULE_OR_METRIC_CODE",
      "ruleId": "optional lexical rule id",
      "location": "Paragraph N, Sentence M | Whole text",
      "match": "optional matched text",
      "fixInstruction": "actionable local revision guidance"
    }
  ]
}
```

## Default thresholds

- Minimum statistical sample: 20 words and 3 sentences.
- Burstiness CV: `0.45` for 8 or more sentences; `0.40` for shorter eligible text.
- Adjacent rhythm delta: `4`.
- Short-sentence ratio: `0.15` for sentences of 6 words or fewer on 8+ sentence text.
- Long-sentence ratio: `0.10` for sentences of 26 words or more on 8+ sentence text.
- MATTR: `0.72` Indonesian and Latin-script universal fallback; `0.74` English; `0.68` CJK fallback and Mandarin.
- Pass score: `80`.
- Indonesian nominalization maximum ratio: `0.045`.
- Indonesian passive maximum ratio: `0.035`.

## Scoring formula

The score starts at 100 and applies bounded deductions from the measured result:

1. **Burstiness:** when CV is under the applicable target, deduct `min(25, round((target - CV) * 100))`. For 8+ sentence text that misses either short or long sentence distribution, add 8 more points, capped at 25.
2. **Monotonous rhythm:** deduct up to 20 points at 6 points per `MONOTONOUS_RHYTHM` finding.
3. **Lexical patterns:** deduct up to 30 points: 5 each for `SLOP_PHRASE` or `DEFINITIONAL_OPENING`, and 4 each for `STRUCTURAL_CLICHE`.
4. **Morphology:** deduct 7.5 for an excessive nominalization finding and up to 15 for passive-bloating findings, capped at 15 total.
5. **Vocabulary, entropy, and profile:** deduct up to 10 total: 5 for low MATTR, 5 for structural repetition, and 5 for a supplied voice-profile deviation.

A `PASS` additionally requires score at or above the configured pass score, no forbidden slop/definitional opening, the applicable CV target, adjacent rhythm delta, and required sentence distribution. A short input returns `SKIP`; lexical slop can still be reported.

## Metrics

- **Burstiness CV:** standard deviation of sentence word counts divided by their mean.
- **Adjacent rhythm delta:** mean absolute difference between neighboring sentence word counts.
- **Adaptive MATTR:** average type-token ratio over a window chosen as the smaller of the text length and an adaptive maximum of 50 words.
- **Compression ratio:** raw-deflate byte length divided by normalized source byte length; used for repetition checks on sufficiently long text.
- **Indonesian morphology:** configured nominalization and passive patterns use whitelists/exclusions defined in the generated catalog below.

## Rule catalog

The following JSON blocks are copied directly from the checked-in rules used by the CLI and browser analyzer at build time.

### Rule catalog

The following JSON object is copied directly from all checked-in rule packs used by the CLI and browser analyzer at build time.

```json
{{ruleCatalog}}
```

### Default profile (`profiles/default-human.json`)

```json
{{defaultProfile}}
```
