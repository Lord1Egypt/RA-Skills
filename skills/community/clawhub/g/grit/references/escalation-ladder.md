# Escalation Ladder

Use this when a task is blocked and momentum matters.

## 1. Correct the current approach

Try one precise fix:
- adjust selector
- change event type
- wait for the right state
- target the real element
- use a different page/state within the same workflow

If it still fails, stop repeating it.

## 2. Change interaction method

Examples:
- DOM click → CDP mouse event
- text input setter → real keyboard input
- page navigation → direct deep link or reverse
- upload flow → add-from-library flow or reverse

## 3. Change tools

Examples:
- Playwright → Agent Browser
- Agent Browser → GUI automation
- Browser automation → native CLI/API path
- one skill → another more specific skill

## 4. Improve the environment

Examples:
- install a better tool
- attach to the real browser session
- use a different browser profile/session
- add a helper utility for screenshots, annotations, or page mapping

## 5. Split the problem

Turn one messy blocker into smaller facts:
- artifact issue
- signing issue
- version issue
- page-state issue
- account/policy issue

Solve them one by one.

## 6. Verify before escalating further

Before saying a step is solved, confirm it with evidence:
- page text/state changed
- build status changed
- uploaded artifact accepted
- file signature/fingerprint matches expectation
- button became enabled

## 7. Escalate only with a concrete hypothesis

Bad escalation:
- "try random new stuff"

Good escalation:
- "the UI click path is unreliable, so switch to a browser tool that exposes stable element refs"
- "the artifact is valid, so stop rebuilding and focus on attaching the existing bundle"

## 8. Report progress in layers

Use this format:
- solved:
- current blocker:
- next attempt:

That keeps momentum visible without wasting tokens.
