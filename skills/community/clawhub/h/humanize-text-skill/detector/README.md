# Detector engine

`detector/` is the executable expression of the humanize-text-skill skill's rules — a
zero-dependency, build-step-free detection + voice engine that scores text for
AI-writing tells in Chinese and English, and (when a voice is set) computes how
far the text sits from a target human voice. It runs identically in Node
(`>=18`) and in the browser.

The skill's `SKILL.md` is the human-readable catalog of rules; this engine is
the deterministic, testable implementation of the regex-detectable subset, plus
stylometric, AI-tool-fingerprint, and voice-distance detectors that don't make
sense as prose. See [`CATEGORIES.md`](./CATEGORIES.md) for the rule ↔ category
mapping that keeps the two in sync.

## Architecture (bilingual, symmetric)

```
detector/
├── patterns.js          # entry: analyzeText(text, options) → result
├── core/                # language-agnostic
│   ├── router.js        #   per-span zh/en/mixed detection + dispatch
│   ├── stylometry.js    #   sentence-len variance, burstiness, TTR, punct CV
│   ├── fingerprints.js  #   placeholders, citation markup, UTM, roleplay, homoglyph
│   ├── voice.js         #   ★ addition layer: text fingerprint vs. target voice
│   └── scoring.js       #   the ONE scorer (score / fidelity / voice.drift separate)
├── zh/                  vocabulary.js · structures.js · tokenizer.js · translationtone.js
├── en/                  vocabulary.js · structures.js · tokenizer.js
├── CATEGORIES.md        # type ↔ SKILL.md section ↔ language map
├── fixtures/  __tests__/
```

## Run it

```bash
npm test          # patterns.test.js + categories.test.js + bilingual.test.js
node detector/__tests__/patterns.test.js   # directly
```

```js
const Huorengan = require("./detector/patterns.js");
const r = Huorengan.analyzeText("您的文本 your text", { voiceMode: "casual" });
console.log(r.score, r.label, r.voice.drift);
```

## `analyzeText(text, options?)` → result

| Field | Type | Meaning |
|---|---|---|
| `score` | `0–100` | 0 = clean, 100 = heavy AI tone. The ONE scorer output. |
| `label` | string | `Minimal` / `Some` / `Strong` / `Heavy` (or `Empty` / `Too short` / `Text too long`) |
| `issues[]` | `{type, text, severity, suggestion, lang}` | one per detected pattern; `type` maps to CATEGORIES.md |
| `stats` | object | `wordCount`, `charCountZh`, per-tier counts, `perLang:{zh,en}`, `denseAIVocab`, normalization flags |
| `fidelity` | object | protected-spans gate: `{protectedSpans, factsOk, termsOk, registerOk, protectedViolated, fracture}` |
| `document_classification` | string | trinary `HUMAN_ONLY` / `MIXED` / `AI_ONLY` / `UNSCORED` (FN-biased) |
| `class_probabilities` | `{human,mixed,ai}` | sums to 1.0 |
| `voice` | object | `★ {detected, target, drift, suggestions}` — null when `voiceMode==='none'` |

`options`:
- `contextMode`: `general` | `technical` | `marketing` | `personal`
- `sceneMode`: `chat` | `status` | `docs` | `public-writing`
- `voiceMode`: `none` | `casual` | `professional` | `technical` | `warm` | `blunt` | `custom`
- `sample`: author sample text (for `voiceMode: 'custom'` calibration)

`policy/` is required at runtime. If `policy/voice.toml` is missing, named
voice modes should throw a clear install error rather than failing silently.

## Design notes

- **One scorer.** `score` (AI density), `fidelity` (gate, not a score), and
  `voice.drift` (target distance) are three independent dimensions. Never mixed.
- **FN-biased.** False positives damage trust more than false negatives.
- **Zero-dependency.** Chinese tokenization uses char + n-gram + punctuation,
  no segmentation library — preserves the "runs anywhere" property.
- **Length gates.** Under ~10 chars/words → `Too short` (unscorable); over 10k → `Text too long`.
