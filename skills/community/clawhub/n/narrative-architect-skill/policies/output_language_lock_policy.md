# Output Language Lock Policy

## Purpose

Output Language Lock Policy prevents the skill from drifting into the wrong language in multilingual conversations.

This applies to:

```text
final answer
draft message
pitch
private notes
section headings
explanations
README
email
chat message
social post
public artifact
personal message
```

## Core Rule

If the user's latest instruction is written clearly in one language, all user-facing output must use that language by default.

Priority order:

```text
1. Explicit user language instruction
2. Latest user message language
3. Requested artifact language
4. Current task context
5. Conversation history language
6. Operator or internal note language
```

## Hard Rule

Conversation history language must not override the latest user input language.

Example:

```text
Previous conversation: Chinese
Latest user input: "Please introduce me to a girl. I am geek and super smart, but might not talk well in front of her."
Correct output language: English
```

## Applies To Private Notes

Private notes must also follow the output language unless the user explicitly asks for another language.

Bad:

```text
Notes for you, not for her:
- 这里不能太油腻。
```

Better:

```text
Notes for you, not for her:
- Do not oversell yourself.
- Keep the first message low-pressure.
```

## Exceptions

the skill may use another language only when:

```text
the user explicitly asks for translation
the user asks for bilingual output
the user asks for Chinese analysis after English draft
the user requests notes in another language
the artifact itself requires another language
```

## Mixed-Language Input Rule

If the user mixes languages, infer the intended output language from the task-bearing sentence.

Example:

```text
"请评价 this README"
```

Output language: Chinese, because the task instruction is Chinese.

Example:

```text
"请帮我看一下: Please write this email in English"
```

Output language: English for the email artifact; Chinese may be used only outside the artifact if useful.

## Artifact Language Rule

For user-sendable artifacts, the artifact language must match the target recipient context or the explicit user request.

If uncertain, use the language of the user's latest instruction.

## Failure Modes

Hard fail:

1. User writes in English, the skill answers in Chinese.
2. Draft message is in a different language from the user's requested language.
3. Private notes use a different language without user request.
4. Section headings switch language unexpectedly.
5. Mixed-language output appears without explicit bilingual request.

Soft fail:

1. Output mostly matches language but keeps stray untranslated phrases.
2. Notes match history language rather than latest user language.
3. Artifact matches language but surrounding explanation does not.

## Rewrite Rule

If language drift is detected, rewrite the entire user-facing output in the locked language.

Do not explain the failure unless the user asks for diagnosis.

## Final Rule

Latest user language locks the response language.
