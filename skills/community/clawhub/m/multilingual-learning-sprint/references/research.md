# Language Skill Research

Research snapshot: ClawHub registry data checked on 2026-07-20 with `clawhub search`, `clawhub inspect`, and direct registry API reads.

## High-Install Comparables

| Skill | Downloads | Installs | Stars | Good Parts | Gaps To Improve |
|---|---:|---:|---:|---|---|
| `language-learning` | 9,337 | 301 | 24 | Broad language coverage, many teaching modes, strong tags for discovery | Overclaims "any language", weak placement rigor, limited plan/test loop |
| `japanese-translation-and-tutor` | 4,658 | 170 | 2 | Clear translation plus tutor intent, focused use cases | Single-language scope, less sprint planning |
| `book-language-tutor` | 2,092 | 73 | 0 | Transactional clarity and real booking intent | Books tutors rather than teaching |
| `english-tutor` | 1,485 | 52 | 2 | A2-C1 positioning, workplace/daily/tech topics, scheduled quizzes in summary | Very thin implementation, schedule not clearly implemented |
| `language-learning-1-0-0` | 1,010 | 33 | 1 | Similar broad curriculum to `language-learning` | Duplicate-style packaging, limited differentiation |
| `language-tutor` | 912 | 30 | 0 | TTS audio generation, pronunciation drills, bilingual lesson audio | Requires API key, audio material only |
| `language-helper` | 801 | 25 | 0 | Quick phrase help in many languages, Chinese trigger support | Not a full learning plan |
| `language-coach` | 675 | 20 | 0 | Explicit slash-command triggers, non-intrusive correction, practical writing focus | Five-language scope, no curriculum or recurring testing |
| `afrexai-language-mastery` | 303 | 9 | 0 | Rigorous placement, CEFR map, spaced repetition, progress logs | Too long, generic triggers, heavy context load |

## What Strong Skills Do Well

- They have clear trigger language in the description and tags.
- They offer multiple modes, such as vocabulary, grammar, conversation, culture, and exam prep.
- They give concrete session templates and example commands.
- Focused skills feel safer and easier to trust than vague universal tutors.
- Skills with tools or APIs stand out when the integration is real and scoped.

## Common Weaknesses

- Placement is often self-assessed instead of tested.
- "Supports every language" claims reduce trust for low-resource languages.
- Many skills teach content but do not close the loop with spaced review and retesting.
- Interest personalization is mentioned but not operationalized.
- Scheduled quizzes are often promised without a durable scheduling mechanism.
- Payment and commercial packaging are usually absent or unclear.

## Design Choices For This Skill

- Use a compact diagnostic before planning.
- Convert learner interests into lesson material every session.
- Keep sprint plans short and measurable: 7, 14, or 30 days.
- Include an explicit review cadence: D0, D1, D3, D7, D14, D30.
- Limit active target languages to two per sprint unless the learner accepts slower progress.
- Keep Alipay AI Pay as a documented Restful service wrapper path instead of pretending native ClawHub skill billing is already available.
