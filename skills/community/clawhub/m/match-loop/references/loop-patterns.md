# Loop Patterns

Use this reference when running a match loop.

## Parent role

The parent is the orchestrator.
It should:
- define the target
- preserve generator/analyst role separation
- pass outputs cleanly between workers
- verify that visual QA actually happened for frontend work
- decide when the loop has converged
- stop the loop if it is thrashing

The parent should not accept vague analyst claims like “looks good” unless the analyst actually previewed the app or clearly explains why visual preview was impossible.

## Recommended prompt split

### Generator prompt should include
- what to build
- constraints
- project path
- required framework or stack
- current analyst feedback
- what to preserve from the last version
- what to change next
- commands to run tests/dev server if known

### Analyst prompt should include
- target and acceptance criteria
- project path
- current version / branch / files changed
- commands to install, run, preview, or test
- instruction to inspect both code and rendered UI
- instruction to take screenshots or record screenshot paths when useful
- instruction to run functional smoke tests/API checks when applicable
- instruction to return `accepted`, `revise`, or `blocked`

## Analyst review packet

Ask the analyst to return this structure:

```markdown
## Status
accepted | revise | blocked

## What works
- ...

## Code issues
- ...

## Visual/UI issues
- ...

## Functional/API issues
- ...

## Evidence
- Preview URL:
- Commands run:
- Screenshots:
- Console/network/test output:

## Required next changes
1. ...
2. ...
3. ...

## Acceptance rationale or blocker
- ...
```

## Visual QA checklist

For UI work, the analyst should check:
- first impression: does the page communicate the intended purpose quickly?
- hierarchy: headline, subhead, CTA, body, nav
- spacing and alignment
- typography and readable text size
- contrast and color consistency
- clipped/overflowing/overlapping text
- desktop layout
- mobile/narrow layout
- loading state
- empty state
- error state
- hover/focus/active states if relevant
- screenshots vs requested style/reference

## Functional smoke checklist

For interactive apps, the analyst should test:
- app starts without crashing
- no obvious console errors
- key buttons click
- navigation works
- forms accept input and validate sensibly
- API calls succeed or fail gracefully
- loading indicators appear when needed
- user-visible errors are understandable
- local tests pass if present and cheap to run

## Browser/computer-use escalation

Preferred inspection path:
1. Browser-native automation: Playwright MCP, Playwright CLI, direct Playwright/CDP
2. Screenshot and DOM inspection from the browser
3. Desktop tools: macbot, Hammerspoon, AppleScript/JXA, Peekaboo

Escalate when:
- the DOM looks fine but the rendered UI may be wrong
- screenshots are needed
- visual alignment/responsiveness matters
- browser automation cannot reach the visible state
- a native dialog, file picker, permission sheet, or desktop UI blocks progress

Do not default to Safari. Use Chrome unless explicitly told otherwise.

## Thrash signals

Stop or rethink the loop when:
- feedback repeats without better revisions
- the generator keeps regressing previously accepted parts
- the analyst changes standards unpredictably
- the target is too vague to judge fairly
- the app cannot be launched due to missing services or credentials
- both agents are spending more time meta-talking than improving the artifact

## Convergence heuristic

A loop is converging when:
- revisions are smaller and more targeted
- accepted parts stay stable across rounds
- evaluator complaints narrow from structural defects to polish
- visual screenshots show clear improvement
- smoke tests move from failing to passing

A loop is not converging when:
- the artifact keeps being rebuilt from scratch
- the same visual defects remain after repeated passes
- tests keep failing for different accidental reasons
- the acceptance criteria keep drifting

## Round limits

Default to practical convergence, not infinite polishing.

A good default:
- 1 generator build round
- 1 analyst review round
- 1–3 revision/review cycles
- continue beyond that only if improvement is clear and the task is worth it

## Parent summary pattern

At the end, summarize:
- number of rounds
- biggest corrections
- visual checks performed
- functional/API checks performed
- final accepted state
- what remains imperfect
