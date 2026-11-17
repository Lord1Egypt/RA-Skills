[![skills.sh](https://skills.sh/b/yanstd888/humanizer-lint)](https://www.skills.sh/yanstd888/humanizer-lint/humanizer-lint)

<div align="center">

# humanizer-lint

### Humanize AI-generated text with a deterministic local AI humanizer and anti-slop prose linter

Detect repetitive LLM phrasing, uniform sentence rhythm, structural clichés, and voice-profile drift across **8 built-in language packs plus 100+ Universal Stylometry languages** without sending text to an external service.

[![GitHub Release](https://img.shields.io/github/v/release/yanstd888/humanizer-lint?style=flat-square&logo=github)](https://github.com/yanstd888/humanizer-lint/releases)
[![npm](https://img.shields.io/npm/v/humanizer-lint)](https://www.npmjs.com/package/humanizer-lint)
[![CI](https://img.shields.io/github/actions/workflow/status/yanstd888/humanizer-lint/ci.yml?branch=main&style=flat-square&label=CI)](https://github.com/yanstd888/humanizer-lint/actions/workflows/ci.yml)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-0-126a4a?style=flat-square)](package.json)
[![Snyk: Pass](https://img.shields.io/badge/Snyk-Pass-126a4a?style=flat-square)](https://www.skills.sh/yanstd888/humanizer-lint/humanizer-lint/security/snyk)
[![Socket: Pass](https://img.shields.io/badge/Socket-Pass-126a4a?style=flat-square)](https://www.skills.sh/yanstd888/humanizer-lint/humanizer-lint/security/socket)
[![Agent Trust Hub: Pass](https://img.shields.io/badge/Agent%20Trust%20Hub-Pass-126a4a?style=flat-square)](https://www.skills.sh/yanstd888/humanizer-lint/humanizer-lint/security/agent-trust-hub)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-humanizer.aiclub.ai.id-126a4a?style=flat-square)](https://humanizer.aiclub.ai.id/)
[![License](https://img.shields.io/github/license/yanstd888/humanizer-lint?style=flat-square)](LICENSE)
[![Node.js](https://img.shields.io/badge/Node.js-%3E%3D18.3-339933?style=flat-square&logo=nodedotjs&logoColor=white)](https://nodejs.org/)
[![GitHub Stars](https://img.shields.io/github/stars/yanstd888/humanizer-lint?style=flat-square)](https://github.com/yanstd888/humanizer-lint/stargazers)

[What it does](#what-it-does) | [Try in your browser](#try-in-your-browser) | [Install](#install) | [Quick start](#quick-start) | [CLI reference](#cli-reference) | [Detectors](#detectors-and-violation-types) | [Agent skill](#use-as-an-agent-skill) | [FAQ](#frequently-asked-questions)

</div>

**Summary**

- Eliminates robotic LLM writing patterns when users ask to "humanize text", "remove AI slop", "fix uniform sentence rhythm", or "write natural blog, SEO, and documentation prose"
- Provides mandatory `node <skill_dir>/scripts/analyze.mjs --stdin --json` verification and `npx humanizer-lint` CLI to enforce Burstiness (`CV >= 0.45`), Adjacent Rhythm Delta, and Adaptive `MATTR` vocabulary diversity
- Ships with **8 deep anti-slop lexical & morphological rule packs** (`en`, `id`, `es`, `ms`, `fr`, `de`, `pt`, `zh`) plus **Universal Stylometric Mode** (`Intl.Segmenter`) for 100+ languages with zero external dependencies
- Supports personal author voice cloning via `node <skill_dir>/scripts/fingerprint.mjs` and passes all 3 `skills.sh` security audits (Gen Agent Trust Hub, Socket, Snyk) with zero network calls

```sh
npx skills add yanstd888/humanizer-lint
```

Use the command above to install the agent skill. For one-off local linting, run the published `humanizer-lint` CLI below.

**8-language summary:** EN — local AI text humanizer and prose linter. ID — humanizer bahasa Indonesia dan cek tulisan AI. ES — humanizador de texto IA y corrector de ritmo. MS — humanizer teks AI dan semak ayat. FR — humaniseur de texte IA et analyseur stylométrique. DE — KI-Text humanisieren und KI-Floskeln entfernen. PT — humanizador de texto IA e corretor de burstiness. ZH — AI文章人性化与句式节奏分析.

## Try in your browser

Use the official demo: [humanizer.aiclub.ai.id](https://humanizer.aiclub.ai.id).

[humanizer-lint.pages.dev](https://humanizer-lint.pages.dev) remains available as a mirror.

Open a deterministic sample view directly:

| Language | AI Sample (FAIL) | Human Sample (PASS) |
|---|---|---|
| EN | [open](https://humanizer.aiclub.ai.id/?lang=en&sample=ai-en) | [open](https://humanizer.aiclub.ai.id/?lang=en&sample=human-en) |
| ID | [open](https://humanizer.aiclub.ai.id/?lang=id&sample=ai-id) | [open](https://humanizer.aiclub.ai.id/?lang=id&sample=human-id) |
| ES | [open](https://humanizer.aiclub.ai.id/?lang=es&sample=ai-es) | [open](https://humanizer.aiclub.ai.id/?lang=es&sample=human-es) |
| MS | [open](https://humanizer.aiclub.ai.id/?lang=ms&sample=ai-ms) | [open](https://humanizer.aiclub.ai.id/?lang=ms&sample=human-ms) |
| FR | [open](https://humanizer.aiclub.ai.id/?lang=fr&sample=ai-fr) | [open](https://humanizer.aiclub.ai.id/?lang=fr&sample=human-fr) |
| DE | [open](https://humanizer.aiclub.ai.id/?lang=de&sample=ai-de) | [open](https://humanizer.aiclub.ai.id/?lang=de&sample=human-de) |
| PT | [open](https://humanizer.aiclub.ai.id/?lang=pt&sample=ai-pt) | [open](https://humanizer.aiclub.ai.id/?lang=pt&sample=human-pt) |
| ZH | [open](https://humanizer.aiclub.ai.id/?lang=zh&sample=ai-zh) | [open](https://humanizer.aiclub.ai.id/?lang=zh&sample=human-zh) |

Use `?lang=en`, `?lang=id`, `?lang=es`, `?lang=ms`, `?lang=fr`, `?lang=de`, `?lang=pt`, or `?lang=zh` to set the playground chrome only for that visit; it does not overwrite a saved browser preference.

It works locally with zero runtime dependencies. Instead of rewriting text through another language model, it reports paragraph- and sentence-level violations with specific correction instructions. Use it to lint LLM-generated documentation, remove robotic AI phrasing from Markdown, check burstiness and lexical diversity, or add a deterministic prose gate to an agent workflow.

It can serve as a CLI text humanizer guardrail, automated writing style linter, or CI/CD documentation linter. The bundled rules flag overused AI clichés such as `delve` and `tapestry` without rewriting the source.

## Language support

| Tier | Languages | Checks |
|---|---|---|
| Tier 1 — rule packs | `en`, `id`, `es`, `ms`, `fr`, `de`, `pt`, `zh` | Universal stylometric metrics plus lexical, definitional-opening, and structural-cliché packs; Indonesian keeps its morphology rules. |
| Tier 2 — universal | `universal` or another ISO 639-1 code such as `tr`, `ja`, or `ar` | Universal stylometry through native `Intl.Segmenter`: burstiness, adjacent rhythm delta, adaptive MATTR, paragraph symmetry, repeated starters, and compression ratio. |

## Use cases & agent integration

Use this local AI text humanizer and prose linter for copywriting, blog posts, SEO articles, technical documentation, Markdown proofreading, academic prose, and natural translation polishing. Tier 1 packs flag native anti-slop phrases in English, Indonesian, Spanish, Malay, French, German, Portuguese, and Mandarin; Tier 2 applies deterministic stylometry to 100+ languages.

For a closed-loop agent workflow, install `npx skills add yanstd888/humanizer-lint`, draft without changing facts, run `humanizer-lint --lang auto`, revise only flagged prose, and re-run before returning the text. It works with Claude Code, Cursor, Windsurf, Cline, Codex, and Gemini CLI without a runtime dependency or network text upload.

## What it does

`humanizer-lint` analyzes prose after removing or neutralizing common non-prose Markdown structures. It then combines lexical rules, sentence-length statistics, structural checks, Indonesian morphology checks, and an optional voice profile into a score from 0 to 100.

The project includes:

- Eight reviewable lexical and structural rule packs for EN, ID, ES, MS, FR, DE, PT, and ZH.
- Sentence-length burstiness, adjacent rhythm delta, short/long sentence ratios, and adaptive MATTR.
- Repetition checks based on paragraph symmetry, repeated sentence starters, and compression ratio.
- Indonesian nominalization, passive-voice, loanword, and translation-style opening checks.
- Optional voice profiles generated from one to five writing samples.
- Human-readable terminal output and pure JSON output.
- Standard exit codes for agents, scripts, and CI jobs.

It does not estimate perplexity, classify who wrote the text, rewrite prose automatically, scan directories, or provide SARIF output.

## Terminal demo

Given this input:

```text
In today's fast-paced world, teams delve into a robust landscape. Moreover, this pivotal approach fosters seamless collaboration across every project. In conclusion, the solution unlocks valuable insights for everyone.
```

Run the analyzer:

```sh
humanizer-lint --file draft.md --lang en
```

The current CLI reports:

```text
Status: FAIL
Score: 39
Language: en

Metrics:
  wordCount: 29
  sentenceCount: 3
  meanSentenceLength: 9.6667
  stdDev: 0.4714
  burstinessCV: 0.0488
  adjacentDelta: 0.5
  shortSentenceRatio: 0
  longSentenceRatio: 0
  mattr: 1
  compressionRatio: 0.6972
  nominalizationRatio: 0
  passiveRatio: 0
  voiceProfileDeviation: 0.5319

Violations:
  SLOP_PHRASE | Paragraph 1, Sentence 1 | Name the exact action or subject instead.
  SLOP_PHRASE | Paragraph 1, Sentence 2 | Describe the actual consequence without inflated significance.
  SLOP_PHRASE | Paragraph 1, Sentence 2 | Name the concrete behavior or outcome.
  SLOP_PHRASE | Paragraph 1, Sentence 1 | Name the field or conditions directly.
  SLOP_PHRASE | Paragraph 1, Sentence 3 | Name what becomes possible and how.
  SLOP_PHRASE | Paragraph 1, Sentence 2 | Connect the sentences by their actual relationship.
  SLOP_PHRASE | Paragraph 1, Sentence 3 | End on the final concrete point.
  SLOP_PHRASE | Paragraph 1, Sentence 1 | Name the current condition precisely.
  SLOP_PHRASE | Paragraph 1, Sentence 2 | Describe the missing step, delay, or transition precisely.
  SLOP_PHRASE | Paragraph 1, Sentence 1 | Name the failure mode or capacity the system handles.
  SLOP_PHRASE | Paragraph 1, Sentence 3 | State the finding itself.
  MONOTONOUS_RHYTHM | Paragraph 1, Sentences 1-3 | Sentence lengths are uniform (10, 10, 9 words). Split one sentence into a short statement or merge two into a longer clause.
  LOW_BURSTINESS | Whole text | Vary sentence lengths by splitting one uniform sentence and merging another where the meaning supports it.
  LOW_ADJACENT_DELTA | Whole text | Change neighboring sentence lengths by splitting or merging only where the content allows it.
```

A failed analysis exits with code `1`. A passing fixture returns:

```text
Status: PASS
Score: 100
Language: en
```

and exits with code `0`.

## Static `SKILL.md` Humanizers vs. `humanizer-lint` (Closed-Loop CLI)

A static writing prompt can ask a model to vary prose, but it cannot verify the finished draft. `humanizer-lint` takes the smaller, deterministic approach: inspect the exact text after drafting, make only flagged revisions, then check again locally.

| Capability | Static `SKILL.md` humanizer prompt | `humanizer-lint` closed-loop CLI |
|---|---|---|
| Checks the completed draft | No | Yes, exact input is measured |
| Measures sentence rhythm | Prompt guidance only | CV, adjacent delta, short/long distribution |
| Measures vocabulary repetition | Prompt guidance only | Adaptive MATTR and repetition checks |
| Flags configured AI clichés | Model-dependent | Rule IDs and locations |
| Preserves source text | Depends on rewrite | Yes, analysis only |
| Runs offline after installation | Depends on agent/model | Yes |
| Supports EN and ID lexical rules | Prompt-dependent | Yes |
| Produces JSON and exit codes | Usually no | Yes |
| Proves human authorship | No | No |

If you are looking for an AI writing detector linter, a ChatGPT tone remover CLI, or an open-source alternative to AI humanizers, note the boundary: this tool detects configured style signals and rhythm problems. It does not claim to determine whether a human or model wrote the text.

## Install

### CLI

Run the published CLI without a global install:

```sh
npx humanizer-lint --file tulisan.md --lang id
```

Or install it globally:

```sh
npm install -g humanizer-lint
```

### Install as an agent skill

The recommended installation for coding agents is through the skills CLI:

```sh
npx skills add yanstd888/humanizer-lint
```

The public listing, installation command, and install count are available on [skills.sh](https://skills.sh/yanstd888/humanizer-lint).

### Development (from source)

Clone the repository and use `npm link` only when developing the local source:

```sh
git clone https://github.com/yanstd888/humanizer-lint.git
cd humanizer-lint
npm test
npm link
humanizer-lint --help
humanizer-fingerprint --help
```

No dependency installation or build step is required.

## Quick start

Analyze one file with auto-detection:

```sh
humanizer-lint --file draft.md --lang auto
```

Force universal stylometry for a language without a bundled pack:

```sh
humanizer-lint --file draft.md --lang universal
```

Request an ISO 639-1 language directly:

```sh
humanizer-lint --file draft.md --lang es
```

Return machine-readable JSON:

```sh
humanizer-lint --file draft.md --lang id --json
```

Analyze stdin without creating a temporary file:

```sh
cat draft.md | humanizer-lint --stdin --lang auto --json
```

Use a custom voice profile:

```sh
humanizer-lint --file draft.md --lang en --profile profiles/custom-voice.json --json
```

Without `npm link`, replace `humanizer-lint` with `node scripts/analyze.mjs` and replace `humanizer-fingerprint` with `node scripts/fingerprint.mjs`.

## Contoh / Example

Skor mengukur kecocokan dengan sinyal gaya yang diperiksa oleh linter: skor lebih tinggi berarti lebih sedikit pelanggaran yang ditemukan. Ini bukan skor probabilitas penulis AI atau manusia.

### Before

```text
Di era digital saat ini, penggunaan teknologi menjadi sangat penting bagi setiap bisnis. Tidak hanya itu, solusi ini juga memberikan manfaat yang sangat besar bagi semua pihak. Dengan demikian, organisasi dapat meningkatkan efisiensi secara signifikan dalam berbagai aspek. Pada akhirnya, pendekatan ini membuka peluang baru yang lebih optimal bagi masa depan.
```

Output dari `tests/fixtures/ai-before-id.md`:

```text
Status: FAIL
Score: 38
Language: id

Violations:
  SLOP_PHRASE | Paragraph 1, Sentence 1 | Mulai langsung dari subjek atau fakta konkret.
  SLOP_PHRASE | Paragraph 1, Sentence 3 | Sebutkan aspek yang relevan.
  SLOP_PHRASE | Paragraph 1, Sentence 4 | Tutup langsung dengan akibat atau keputusan akhir.
  MONOTONOUS_RHYTHM | Paragraph 1, Sentences 1-3 | Sentence lengths are uniform (13, 14, 11 words).
  LOW_BURSTINESS | Whole text | Vary sentence lengths by splitting one uniform sentence and merging another where the meaning supports it.
  LOW_ADJACENT_DELTA | Whole text | Change neighboring sentence lengths by splitting or merging only where the content allows it.
```

### After

```text
Pemilik toko memakai aplikasi stok untuk melihat barang yang habis pada hari yang sama. Semua melihat angka yang sama. Saat satu produk menipis, petugas memesan ulang sebelum rak kosong dan mencatat alasan setiap perubahan. Laporan harian menunjukkan barang mana yang laku, barang mana yang tertahan, dan kapan petugas harus menghubungi pemasok lagi agar toko tidak kehabisan barang yang dicari pelanggan. Pemilik toko kini membeli barang berdasarkan catatan, bukan tebakan.
```

Output dari `tests/fixtures/human-after-id.md`:

```text
Status: PASS
Score: 100
Language: id
```

Untuk contoh ini, skor naik dari **38** menjadi **100** setelah frasa template dihilangkan, subjek dibuat konkret, dan panjang kalimat divariasikan.

## CLI reference

### Analyzer

```text
humanizer-lint (--file <path> | --stdin) [--lang auto|universal|<ISO-639-1>] [--profile <path>] [--json]
```

| Option | Required | Description |
|---|---:|---|
| `--file <path>` | One input required | Read one UTF-8 text or Markdown file. |
| `--stdin` | One input required | Read the complete document from standard input. |
| `--lang auto|universal|<ISO-639-1>` | No | Select auto-detection, a bundled Tier 1 pack, or universal stylometry. Default: `auto`. |
| `--profile <path>` | No | Load a JSON voice profile. |
| `--json` | No | Print JSON only. Without it, print the terminal report. |
| `--help` | No | Print command usage. |

Exactly one of `--file` or `--stdin` is required.

### Voice fingerprint

```text
humanizer-fingerprint --input <file-or-dir> --output <profile.json> [--name <name>] [--lang id|en|auto]
```

| Option | Required | Description |
|---|---:|---|
| `--input <path>` | Yes | Read one file or up to five `.md` and `.txt` files from one directory. |
| `--output <path>` | Yes | Write the generated profile atomically. |
| `--name <name>` | No | Set the profile name. Default: `custom-voice`. |
| `--lang id|en|auto` | No | Record the intended language. Default: `auto`. |
| `--help` | No | Print command usage. |

### Exit codes

| Code | Meaning |
|---:|---|
| `0` | `PASS`, or `SKIP` for text too short for statistical scoring. |
| `1` | Analysis completed and returned `FAIL`. |
| `2` | Invalid arguments, unreadable input, or malformed profile. |

## Detectors and violation types

The JSON rule catalogs contain stable IDs. Runtime statistical checks use named violation types.

| Violation type or rule range | Language | What it detects |
|---|---|---|
| `ID001`-`ID040`, `EN001`-`EN040` / `SLOP_PHRASE` | Indonesian and English | Configured clichés, generic transitions, inflated wording, and repeated LLM vocabulary such as `delve`, `tapestry`, `testament`, and their Indonesian equivalents. |
| `ID041`-`ID042` / `DEFINITIONAL_OPENING` | Indonesian | Formulaic paragraph openings and rigid definition templates. |
| `EN041`-`EN044` / `STRUCTURAL_CLICHE` | English | Participial tails, binary formulas, repeated double-hyphens, and similar structural templates. |
| `MONOTONOUS_RHYTHM` | Both | Three adjacent sentences whose lengths differ by at most three words. |
| `LOW_BURSTINESS` | Both | Sentence-length coefficient of variation below the configured threshold. |
| `MISSING_SENTENCE_RANGE` | Both | Text with at least eight sentences that lacks enough short or long sentences. |
| `LOW_ADJACENT_DELTA` | Both | Consecutive sentence lengths that change too little. |
| `LOW_LEXICAL_DIVERSITY` | Both | Adaptive MATTR below the language threshold. |
| `LOW_ENTROPY_REPETITION` | Both | Low DEFLATE compression ratio in text of at least 150 words. |
| `SYMMETRIC_PARAGRAPHS` | Both | Three consecutive paragraphs with the same sentence count. |
| `REPETITIVE_STARTERS` | Both | A paragraph with at least three sentences beginning with the same token. |
| `EXCESSIVE_NOMINALIZATION` | Indonesian | Nominalization density above the configured threshold after whitelist filtering. |
| `PASSIVE_BLOATING` | Indonesian | Passive morphology density or consecutive translation-style subordinate openings. |
| `VOICE_PROFILE_DEVIATION` | Both | Custom-profile mean sentence length that differs from the target by more than 30 percent. |

## Metrics and scoring

| Metric | Definition |
|---|---|
| `burstinessCV` | Population standard deviation divided by mean sentence length. |
| `adjacentDelta` | Mean absolute difference between neighboring sentence lengths. |
| `mattr` | Moving-average type-token ratio over an adaptive 10- to 50-token window. |
| `compressionRatio` | Raw DEFLATE byte length divided by original UTF-8 byte length. |
| `shortSentenceRatio` | Share of sentences containing six words or fewer. |
| `longSentenceRatio` | Share of sentences containing 26 words or more. |
| `voiceProfileDeviation` | Mean relative deviation from available profile targets. It is not an authorship probability. |

The score starts at 100 and applies these caps:

| Category | Maximum deduction |
|---|---:|
| Burstiness and sentence-range checks | 25 |
| Monotonous rhythm windows | 20 |
| Lexical and structural clichés | 30 |
| Indonesian morphology | 15 |
| Vocabulary, entropy, and custom-profile deviation combined | 10 |

A normal-length document passes only when the score is at least 80, no `SLOP_PHRASE` or `DEFINITIONAL_OPENING` remains, burstiness and adjacent-delta gates pass, and the sentence-range requirement passes when applicable.

Documents below 20 words or three sentences return `SKIP`. Lexical slop phrases are still reported.

## Markdown sanitization

Before tokenization, the analyzer:

- removes YAML frontmatter, fenced code blocks, headings, and Markdown tables;
- keeps Markdown link anchor text while removing the URL;
- replaces inline code and bare URLs with `TOKEN_ENTITY`;
- removes short or unfinished list fragments while keeping complete list prose;
- removes blockquote markers while preserving the quoted prose;
- preserves paragraph boundaries for locations and structural checks.

This is deterministic sanitization, not a full Markdown or MDX abstract syntax tree parser. HTML blocks and arbitrary MDX components do not receive special parsing.

## Voice profiles

Generate a profile from one to five samples:

```sh
humanizer-fingerprint \
  --input writing-samples \
  --output profiles/custom-voice.json \
  --name editorial-voice \
  --lang en
```

The profile records mean sentence length, standard deviation, burstiness, adjacent delta, MATTR, average paragraph sentence count, and punctuation rates. Supplying it with `--profile` adds `voiceProfileDeviation`; a mean sentence-length drift above 30 percent creates a five-point profile penalty inside the 10-point vocabulary and entropy cap.

## JSON output

`--json` writes a single JSON object to stdout. The stable top-level fields are:

```json
{
  "status": "FAIL",
  "score": 39,
  "language": "en",
  "metrics": {
    "wordCount": 29,
    "sentenceCount": 3,
    "burstinessCV": 0.0488,
    "adjacentDelta": 0.5,
    "mattr": 1
  },
  "violations": [
    {
      "type": "LOW_BURSTINESS",
      "location": "Whole text",
      "actual": 0.0488,
      "target": 0.4,
      "fixInstruction": "Vary sentence lengths by splitting one uniform sentence and merging another where the meaning supports it."
    }
  ]
}
```

The real result may contain additional metric properties and violations.

## Use as an agent skill

After installation, an agent can use the skill as a closed verification loop:

1. Draft or edit prose in a supported Tier 1 language or any Universal Stylometry language without changing supported facts.
2. Run the analyzer against the exact complete draft.
3. Read every violation and edit only the affected prose or named whole-document gate.
4. Re-run the analyzer, stopping after three iterations.
5. Return only a `PASS`, or an honestly labeled short-text `SKIP` with no unresolved lexical violations.

The skill is indexed on skills.sh and its current listing passes the platform's Snyk security audit.

## Used by

The skills.sh badge at the top of this README is the public source for anonymous installation activity. GitHub's native `Used by` sidebar is generated automatically from its dependency graph; repository owners cannot set that count manually.

Because the CLI is published on npm, npm downloads and downstream package manifests are the relevant distribution signals. The skills.sh listing separately represents agent-skill installation activity.

## CI and repository automation

This repository keeps `.github` intentionally small. The included `.github/workflows/ci.yml` workflow runs the test suite and package dry-run on supported Node.js versions. A CI badge is useful because it reflects an actual workflow; issue templates, Dependabot, and release automation are omitted until the repository needs them.

To use the analyzer in another GitHub Actions workflow without an npm release, check out this repository into a subdirectory and run the script directly:

```yaml
name: prose-check

on:
  pull_request:
    paths:
      - "**/*.md"
      - "**/*.txt"

jobs:
  lint-readme:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/checkout@v4
        with:
          repository: yanstd888/humanizer-lint
          path: .humanizer-lint
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
      - run: node .humanizer-lint/scripts/analyze.mjs --file README.md --lang auto --json
```

The analyzer accepts one file per invocation. Invoke it once for each document you want to gate.

## Security properties

Production scripts use only Node.js built-ins and have no runtime dependencies. The test suite rejects production use of `child_process`, `eval`, dynamic `Function` construction, and `fetch`. The fingerprint writer writes to a temporary file and renames it into place.

Text remains local unless the surrounding agent or workflow sends it elsewhere.

## Frequently asked questions

<details>
<summary><strong>Is humanizer-lint an AI content detector?</strong></summary>

No. It detects configured lexical, structural, rhythm, and morphology signals. A pass or failure does not prove who wrote the text.

</details>

<details>
<summary><strong>Does humanizer-lint rewrite or auto-fix prose?</strong></summary>

No. It returns correction instructions but does not modify the source file. This prevents silent factual or formatting changes.

</details>

<details>
<summary><strong>Can it remove robotic AI phrasing from Markdown?</strong></summary>

It can identify the exact paragraph or sentence that matches a configured phrase or style gate. A human or coding agent then makes the smallest supported edit and runs the analyzer again.

</details>

<details>
<summary><strong>Can I install it from npm?</strong></summary>

Yes. Run `npx humanizer-lint --file draft.md --lang auto` for a one-off command, or install it globally with `npm install -g humanizer-lint`. Install the agent skill separately with `npx skills add yanstd888/humanizer-lint`.

</details>

<details>
<summary><strong>Which languages are supported?</strong></summary>

The configured lexical packs support English, Indonesian, Spanish, Malay, French, German, Portuguese, and Mandarin. Other ISO 639-1 languages use universal stylometry through native `Intl.Segmenter`; these checks measure rhythm and repetition without inventing a lexical pack.

</details>

<details>
<summary><strong>Does it send text to an API?</strong></summary>

No. Production code has no network call. The skills installer and Git operations need network access only to download the repository.

</details>

<details>
<summary><strong>Why did a short document return SKIP?</strong></summary>

Documents below 20 words or three sentences do not contain enough material for the configured statistical gates. Lexical slop phrases are still checked.

</details>

## Contributing

Contributions should remain deterministic, zero-dependency, and covered by a focused regression test.

1. Fork the repository.
2. Create a focused branch.
3. Add or update one minimal test for non-trivial behavior.
4. Run `npm test` and `npm pack --dry-run`.
5. Open a pull request that explains the user-visible effect.

Every repository change updates the package and skill version, then publishes a matching Git tag and GitHub release after verification.

## Project layout

```text
.github/
  workflows/
    ci.yml
LICENSE
README.md
SKILL.md
package.json
profiles/
  default-human.json
rules/
  en-slop.json
  id-slop.json
scripts/
  analyze.mjs
  fingerprint.mjs
  utils/
    metrics.mjs
    sanitizer.mjs
    tokenizer.mjs
tests/
  fixtures/
  test-runner.mjs
```

## License

Licensed under the [MIT License](LICENSE).
