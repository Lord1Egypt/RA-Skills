# Debug / Iteration History

This file is a human-readable release summary for the published skill page.

## Major fixes made before release

### 1. Post-generation topic stickiness
The skill originally treated the generated prompt as the default topic for later messages. This was fixed so prompt generation only applies to the current turn.

### 2. Overlong endings
The skill used to append extra next-step menus like `1 / 2 / 3`. This was removed so prompt output ends cleanly by default.

### 3. Explanation-heavy summaries
The output originally contained more teaching-style explanations. This was changed to a shorter `Prompt 关键处理` summary that says what the prompt did.

### 4. Bypass wording
Bypass replies used to sound like internal debugging language. This was changed to direct, user-facing wording.

### 5. Attached trigger support
The trigger was updated to support forms like `@prt帮我...` while still avoiding false matches such as `@promptify...`.

### 6. Clarification restraint
Clarification logic was tightened so the skill asks only the minimum missing question needed to proceed.

### 7. Execution-boundary blocker
A critical bug was found where a `@prt` request could accidentally be treated like a real execution request. This was promoted to a release blocker and fixed before release.

## Current release mindset

This skill is intended to be:
- practical
- lightweight
- user-facing
- safe in conversation
- clear about boundaries

## Update note

This skill will continue to be updated based on real usage and edge-case testing.