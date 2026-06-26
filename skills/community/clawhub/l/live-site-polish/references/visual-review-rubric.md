# Visual Review Rubric

Use this rubric in a fresh reviewer context. A subagent is preferred.

For one task, create the reviewer context once, then reuse that same reviewer for later review rounds on the same task.

## Reviewer Input

Provide only:

- task brief
- page URL or short page identity
- before screenshot
- after screenshot
- optional focused crop for the target area

Do not provide the full implementation history.

If the page includes dynamic regions, make sure the before and after evidence is frozen to the same state before review. Do not treat slide changes, autoplay drift, or a different open tab/panel state as the intended design change.

## Reviewer Job

Judge the result as an external critic, not as a collaborator protecting prior decisions.

Evaluation order:

1. Describe what changed visually
2. Check implementation correctness
3. Check alignment and spacing quality
4. Check overall design quality
5. Check goal achievement
6. Return a verdict
7. In the same reviewer session, run one challenge follow-up asking whether the current verdict was too strict or too lenient and whether any global issue was missed

## Hard Fail Conditions

Return `bad` if any of these are true:

- the after screenshot is effectively unchanged
- important content became hidden, clipped, overlapped, or unreadable
- the patch visibly breaks nearby layout
- the edited block is visibly off-center when it should be centered
- alignment between related elements is visibly inconsistent
- padding or spacing is obviously wrong enough to read as a mistake rather than a design choice
- injected copy does not match the page language
- the solution clashes strongly with the page's visual system

## Output Schema

Use exactly these fields:

```json
{
  "objective_observations": [
    "What changed in the after state"
  ],
  "implementation_correctness": {
    "status": "pass | fail",
    "issues": [
      "Concrete implementation problems only"
    ]
  },
  "design_quality": {
    "status": "excellent | acceptable | bad",
    "notes": [
      "Comments on hierarchy, spacing, padding, centering, alignment, color, and cohesion"
    ]
  },
  "goal_achievement": {
    "status": "met | partially_met | missed",
    "notes": [
      "Whether the user's request was actually satisfied"
    ]
  },
  "verdict": "excellent | acceptable | bad"
}
```

## Verdict Meaning

- `excellent`: strong result, no meaningful reason to keep iterating
- `acceptable`: usable result, but still has polish or minor coherence issues
- `bad`: serious issue remains in implementation, alignment, spacing, or overall fit

## Reviewer Prompt Shape

Use a short instruction like:

`Review this live page redesign as an isolated visual critic. Ignore implementation history. Compare the before and after screenshots, apply the rubric, and return only the structured result.`

For later rounds on the same task, keep the same reviewer session and send only the updated after evidence plus the same rubric and task brief.
