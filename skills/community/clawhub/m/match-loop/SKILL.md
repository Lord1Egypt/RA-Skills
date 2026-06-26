---
name: match-loop
description: Two-agent iterative vibe-coding loop for OpenClaw. Use when the user wants one sub-agent to generate/build/code an app or artifact and a second analyst agent to inspect the code, visually preview the frontend in a browser like a human, run small functional/API tests, and feed concrete fixes back to the generator until the result matches the target. Triggers on requests like "match loop", "generator and analyst", "visual QA loop", "vibe-code then analyze", "have one agent code and another visually inspect it", "iterate until the UI is perfect", or "keep refining until it matches the target".
---

# Match Loop

Run a **generator ↔ visual analyst** loop.

This skill is for vibe-coding where one-shot generation is not enough. The core pattern is:
- one sub-agent **codes/builds** the thing
- one sub-agent **analyzes the code and previews the live UI like a human**
- the analyst gives concrete feedback
- the generator revises
- the loop continues until the analyst accepts the result, progress stalls, a blocker appears, or the user says `stop`

The defining feature: **the analyst must visually inspect the frontend whenever a frontend exists.** It should not only read code or logs. It should open the app in a browser, take screenshots or otherwise inspect the rendered UI, interact with it, and verify that it looks and behaves correctly.

## Roles

### 1. Generator agent

Responsible for:
- implementing the requested app, feature, page, or artifact
- fixing issues found by the analyst
- preserving working parts while revising broken/ugly/confusing parts
- running basic local checks when useful
- producing concrete revisions, not endless plans

The generator should optimize for fast, working iterations.

### 2. Analyst agent

Responsible for:
- inspecting the code for correctness, maintainability, obvious bugs, and missing pieces
- running or previewing the app locally when possible
- visually inspecting the frontend in a browser like a human user
- taking screenshots or using browser/computer-use tools to examine the UI
- testing basic flows and interactions
- checking whether API calls, forms, buttons, navigation, and visible state actually work
- giving prioritized, concrete feedback to the generator
- deciding whether the result is good enough for the task

The analyst is not a replacement generator. It should critique toward revision, not rewrite the whole project unless the implementation is structurally broken.

## Non-negotiable visual QA rule

For frontend work, the analyst must not rely on code review alone.

It should:
1. start the dev server or use the provided preview URL
2. open the app in a browser
3. inspect the rendered page visually
4. capture screenshots when useful
5. test key interactions like a human would
6. report visual and functional defects clearly

Look for things that code review often misses:
- text cut off, overlapping, too small, too large, low contrast, or misaligned
- mobile/desktop layout problems
- broken spacing, hierarchy, or visual balance
- confusing CTAs or navigation
- forms that appear fine in code but fail in the UI
- loading/error states that look ugly or broken
- API calls that silently fail
- console errors
- buttons that do nothing

If browser-native tools fail, escalate using the local browser/computer-use stack rather than pretending visual inspection happened.

Preferred order:
1. Playwright MCP / Playwright CLI / direct Playwright or CDP
2. app/browser screenshots and DOM inspection
3. macbot / Hammerspoon / AppleScript / Peekaboo for desktop-level inspection

Do not use Safari unless the user explicitly asks. Chrome is the default browser target.

## Best use cases

Use this for:
- vibe-coded web apps
- landing pages
- dashboards
- onboarding flows
- mobile-responsive pages
- React/Next/Vite/Expo web previews
- UI-heavy prototypes
- API-backed frontend apps
- code where visual behavior matters as much as implementation

## Loop workflow

### 1. Define the target

Before spawning the loop, define:
- what is being built
- what “perfect” or “good enough” means for this task
- target user / use case
- must-have features
- visual/style expectations
- functional/API expectations
- test commands or preview commands if known

If the target is fuzzy, write the best current target and let the analyst sharpen acceptance criteria during the first review.

### 2. Spawn the two roles

Create:
- one generator worker
- one analyst worker

Keep the roles explicit. The parent orchestrates handoffs and convergence.

### 3. Generator builds v1

The generator should create a real working attempt:
- implement files
- install needed dependencies when appropriate
- run basic checks if cheap
- provide how to run/preview/test it

### 4. Analyst reviews v1

The analyst should perform three layers of review:

#### Code review
- architecture / file structure
- implementation completeness
- obvious bugs
- missing edge cases
- maintainability

#### Visual browser review
- launch or open the app
- inspect the rendered UI
- take screenshots when useful
- check layout, text, hierarchy, spacing, contrast, responsiveness, and polish

#### Functional smoke test
- click key buttons/links
- fill forms if relevant
- verify navigation and visible state changes
- check console/network/API failures when available
- run tests or small API checks if appropriate

### 5. Analyst produces feedback packet

The analyst feedback should include:
- what works
- what is broken or ugly
- exact visual defects observed
- exact functional/API defects observed
- screenshots or screenshot paths when useful
- prioritized changes for the next generator pass
- acceptance status: `accepted`, `revise`, or `blocked`

### 6. Generator revises

The parent sends the analyst packet to the generator.

The generator should:
- fix the highest-impact issues first
- preserve accepted parts
- avoid unnecessary rewrites
- state what changed
- provide the next preview/test instructions

### 7. Repeat until convergence

Continue generator → analyst → generator until:
- analyst accepts the output
- remaining issues are trivial and not worth another round
- the loop is thrashing
- the task is blocked
- the user says `stop`

## Convergence rule

The analyst can call the result “perfect” only after:
- code review passes for the task’s scope
- the frontend was visually inspected, if applicable
- key interactions were tested
- major visual defects are resolved
- major functional/API defects are resolved

Do not chase fake perfection. If only tiny polish remains and the output is fit for purpose, stop and report caveats.

## Feedback quality bar

Good analyst feedback is:
- visual when visual defects exist
- specific
- prioritized
- actionable
- tied to acceptance criteria

Good:
- "The hero text wraps badly at mobile width and overlaps the CTA. Reduce headline size on <480px, add vertical spacing, and make the CTA full-width. Screenshot: /tmp/match-loop/mobile-v2.png."

Bad:
- "Looks bad."
- "Improve UI."
- "Probably fine" without previewing.

## Stop / handoff conditions

Pause or stop when:
- the user says `stop`
- the app cannot be launched because required credentials/services are missing
- the analyst cannot visually inspect despite reasonable browser/computer-use escalation
- revisions are no longer producing meaningful improvement
- the analyst accepts the result

## Parent orchestration pattern

1. define target and acceptance criteria
2. spawn generator
3. generator builds v1
4. spawn/prompt analyst with target + code/output + preview instructions
5. analyst performs code + visual + functional review
6. parent sends feedback packet to generator
7. generator revises
8. repeat until analyst accepts or stop condition is reached

## Final response expectation

At the end, summarize:
- number of rounds
- final output/version
- visual checks performed
- functional/API checks performed
- biggest fixes made
- why the analyst accepted it
- remaining caveats, if any

## Suggested companion reference

If needed, also read:
- `references/loop-patterns.md`
