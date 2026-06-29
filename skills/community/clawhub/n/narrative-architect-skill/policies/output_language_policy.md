# Output Language Policy

## Purpose

Ensure the skill responds in the appropriate language.

Language is part of user intent. It is not just a style choice.

## Default Rule

Use the same language as the user's latest request.

If the user writes in English, respond in English. 
If the user writes in Chinese, respond in Chinese. 
If the user mixes languages, use the language of the requested artifact or the dominant task language.

## Artifact Language Rule

When the user asks for a specific artifact, the artifact language should follow the artifact convention unless the user requests otherwise.

Examples:

```text
GitHub README → English by default if user asks in English or project is open-source/developer-facing.
API docs → English by default unless user requests Chinese.
Chinese WeChat message → Chinese.
English investor email → English.
Bilingual output → only when requested.
```

## Explanation vs Artifact

If the user asks in Chinese for an English artifact, the skill may briefly explain in Chinese, but the artifact itself must be in English.

If the user asks in English for an English artifact, do not add Chinese commentary unless the user asks for analysis in Chinese.

## Exceptions

Use a different language only when:

1. The user explicitly requests another language.
2. The artifact convention requires another language.
3. The user asks for bilingual output.
4. Source material must be quoted or preserved in its original language.
5. The user asks for translation.

## Mixed-Language Rule

Do not mix languages casually.

Acceptable:

```text
Chinese analysis + English README
English explanation + Chinese sample message
Bilingual table when requested
```

Not acceptable:

```text
English user request → Chinese answer without reason
English README → Chinese closing notes
Chinese output → random English slogans without purpose
```

## Native Expression Rule

When writing in English, use native English structure, not translated Chinese structure.

Avoid:

```text
This skill has very strong ability to...
It can help people to start his/her own company...
```

Prefer:

```text
This skill helps solo founders start and run companies with agent staff.
It gives one founder a working team of AI agents.
```

When writing in Chinese, avoid stiff translated English.

## Failure Modes

Hard fail:

1. User asks in English and final answer is Chinese.
2. Artifact language differs from the requested language.
3. README or GitHub docs mix Chinese commentary into the deliverable.
4. The output changes language midstream without purpose.

Soft fail:

1. English is grammatical but sounds translated.
2. Chinese is correct but sounds like a literal English translation.
3. The final artifact is language-correct but not native.

## Rewrite Rule

If language mismatch occurs, regenerate in the correct language while preserving the same substantive content.

Do not apologize at length. Fix the artifact.
