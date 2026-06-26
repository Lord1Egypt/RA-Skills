---
name: systematic-debugging
description: Debug through a structured root-cause process instead of guesswork. Use when commands fail, tools behave unexpectedly, automations break, integrations only partially work, or the real cause is unclear.
---

# Systematic Debugging

Debug by narrowing the problem, testing hypotheses, and proving root cause.

## Core Rule

Do not stack random fixes.
Understand the failure shape first, then test one hypothesis at a time.

## Workflow

1. Define the symptom clearly.
2. Reproduce it with the smallest possible test.
3. Separate likely layers:
   - input/data
   - local script or command
   - dependency/runtime
   - network/external service
   - site-specific anti-bot or auth
4. Test one layer at a time.
5. Confirm root cause with a minimal proof.
6. Apply the smallest fix.
7. Re-test the original symptom.

## Useful Patterns

### Compare working vs failing path
If one URL, command, or mode works and another fails, compare them directly.

### Reduce scope
Use:
- smaller inputs
- a simpler command
- a known-good site/page
- a dry-run mode
- help/version commands

### Distinguish tool failure from target failure
Examples:
- browser tool works, but website blocks automation
- API client works, but credentials are missing
- script syntax is fine, but runtime dependency is absent

## Reporting Style

Explain in 3 parts:
- symptom
- confirmed cause
- fix or next blocker

Example:
- "툴 자체는 살아 있고, 쿠팡이 anti-bot으로 막는 게 원인이었어. 그래서 브리지 세션 재사용 쪽으로 우회했어."

## Avoid

- trying many fixes without learning anything
- changing multiple variables at once
- declaring a root cause without proof
- saying something is broken when only one target site is blocking it

## Practical Examples

### Example: Site works on one page but not another
- Symptom: google.com opens, search results fail
- Likely split: tool works, target flow is blocked or challenged

### Example: Skill installed but command missing
- Symptom: folder exists, CLI not found
- Likely split: skill docs installed, runtime dependency missing

### Example: API tool returns auth error
- Symptom: command exists, request fails
- Likely split: client is healthy, credentials/config are missing or invalid
