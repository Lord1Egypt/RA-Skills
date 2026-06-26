# Language Coach

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

Multi-language writing coach for grammar, word choice, collocations, and idiom errors. Supports English, Chinese, Spanish, French, and Japanese.

## Supported Languages

| Command | Language | Native Speakers |
|---------|----------|-----------------|
| `//en`  | English | ~1.5B |
| `//cn`  | Chinese (Mandarin) | ~1.1B |
| `//es`  | Spanish | ~550M |
| `//fr`  | French | ~280M |
| `//ja`  | Japanese | ~125M |

## Installation

```bash
# Via Git
git clone https://github.com/KaigeGao1110/language-coach ~/.openclaw/workspace/skills/language-coach
```

## Quick Start

Type `//[lang] ` followed by your text:

```
//en I already send the report to Oleg yesterday

//cn 我来到了美国已经三年了

//es Yo tengo muchos años de experiencia

//fr Je suis très bonne en français

//ja 私は日本語が少し話せます
```

## What It Does

- Corrects grammar errors
- Fixes word choice mistakes
- Improves collocations and idiomatic expressions
- Fixes register issues
- Language-specific error detection

## Correction Format

Each correction includes:
1. Original sentence
2. Corrected version
3. Brief explanation (1 sentence)

## Examples

### English
```
//en Can you please confirm if you received my email?
✅ (correct — no change needed)

//en I want to discuss about the project tomorrow.
Correction: I want to discuss the project tomorrow.
Why: "Discuss" is a transitive verb — it takes a direct object without "about."
```

### Chinese
```
//cn 这个是一个很好例子。
Correction: 这是一个很好的例子。
Why: 指示代词作主语时，定语标记"的"更自然地连接形容词。
```

### Spanish
```
//es Yo soy muy bueno en francés.
Correction: Se me da muy bien el francés.
Why: "Darse bien" is more idiomatic for describing skills/abilities.
```

### French
```
//fr J'ai allé à Paris.
Correction: Je suis allé à Paris.
Why: "Aller" uses être as the auxiliary in compound tenses, not avoir.
```

### Japanese
```
//ja 明日私は友達に会いました。
Correction: 昨日私は友達に会いました。
       or: 明日私は友達に会うつもりです。
Why: "会いました" is past tense but 明日 indicates future — match tense to time marker.
```

## Design Principles

- **Brief** — one meaningful correction per message
- **Practical** — focus on errors that affect clarity
- **Non-intrusive** — only correct real issues, not style preferences
- **Educational** — show the pattern, not just the fix
- **Language-aware** — each language has its own rule set

## For AI Agents

Install into your OpenClaw workspace skills directory.

## Language

Corrections are provided in the target language or English, depending on what best explains the error.
