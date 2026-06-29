# Output Language Lock Harness

## Purpose

Output Language Lock Harness checks whether the skill respects the language of the user's latest instruction.

It runs before final output for every task.

## Required Input

```yaml
language_lock:
  locked_language:
  source:
  exception:
```

## Checkpoints

### 1. Final Answer Language

Does the final answer use the locked language?

### 2. Draft Artifact Language

Does the sendable artifact use the locked language?

### 3. Notes Language

Do private notes use the locked language?

### 4. Section Heading Language

Do headings use the locked language?

### 5. No Mixed-Language Drift

Does the output avoid unexpected switching?

## Hard Fail Examples

User:

```text
Please introduce me to a girl. I am geek and super smart, but might not talk well in front of her.
```

Bad output:

```text
这个不用 pitch。你不需要把自己卖出去。
```

Why bad:

```text
Latest user instruction is English.
Output is Chinese.
```

Good output:

```text
You do not need to sell yourself.
```

## Exceptions

Allowed only when the user asks for:

```text
translation
bilingual output
Chinese explanation
English draft with Chinese notes
language comparison
```

## Failure Modes

Hard fail:

1. Output language differs from locked language.
2. Notes language differs from locked language.
3. Heading language differs from locked language.
4. A previous conversation language overrides latest user language.
5. Artifact language differs from requested language.

Soft fail:

1. One or two stray terms remain.
2. Proper nouns are translated unnecessarily.
3. Mixed-language examples appear without need.

## Rewrite Rule

If failed, rewrite all user-facing output in the locked language.

Do not preserve wrong-language notes.

## Final Rule

Language match is a delivery contract, not a style preference.
