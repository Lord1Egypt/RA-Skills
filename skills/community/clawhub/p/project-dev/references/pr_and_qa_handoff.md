# PR and QA Handoff — The Quality Gate

This is the most important handoff in your workflow. The quality of your PR description directly determines how effectively QA can validate your work. A good PR description means fast, accurate QA. A vague PR description means QA guessing what to test, missing things, or coming back to you with questions that delay the whole cycle.

## The PR Description Template

Every PR you create MUST include this template, fully filled out. Do not skip sections. If a section doesn't apply, write "N/A" with a brief reason — don't leave it blank.

```
## Task
- **Task ID:** [task-id and title from Asana]
- **Spec Section:** [FE-XXX or BE-XXX from Implementation Plan]
- **SRS Requirement(s):** [SRS-XXX — the upstream requirement IDs this task fulfills]

## What This PR Implements
[2-3 sentences describing what was built. Be specific — "Added user registration" is too vague. 
"Built the user registration form with email, password, and confirm-password fields. Includes 
client-side validation (email format, password strength, match confirmation) and form submission 
to POST /api/auth/register. Displays inline validation errors and a success toast on completion." 
— that's the right level of detail.]

## Acceptance Criteria
[Copy each criterion directly from the Asana task and add a checkbox. QA will use these as 
their test checklist.]

- [ ] [Criterion 1 — exact text from task]
- [ ] [Criterion 2]
- [ ] [Criterion 3]
- [ ] [etc.]

## How to Test
[Step-by-step instructions for QA to manually verify the feature. Write these as if QA has 
never seen this feature before — because from a testing perspective, they haven't.]

### Prerequisites / Setup
- [Any test data that needs to exist]
- [Any environment variables or config needed]
- [Any accounts, roles, or permissions required]
- [Any other PRs that must be merged first]

### Test Steps
1. [First action — e.g., "Navigate to /register"]
2. [Second action — e.g., "Enter 'test@example.com' in the email field"]
3. [Expected result — e.g., "No validation error should appear"]
4. [Continue with each step and expected outcome...]

### Edge Cases to Verify
- [What happens with invalid input?]
- [What happens with empty fields?]
- [What happens if the API is unreachable?]
- [Any boundary conditions from the spec]

## Known Limitations / Out of Scope
[Anything intentionally NOT included in this PR. This prevents QA from flagging expected 
gaps as bugs.]

- [e.g., "Social login (Google/GitHub) is not included — it's a separate task (FE-007)"]
- [e.g., "Email verification flow is handled by BE-015, not this PR"]
- [e.g., "Mobile responsive layout is not yet implemented — tracked in FE-003b"]

## Dependencies
- [Any merged PRs this depends on — link them]
- [Any environment variables that need to be set]
- [Any external services that must be running]
- [Any database migrations that need to run first]

## Implementation Notes (Optional)
[Anything QA or the Engineer should know about HOW this was implemented — unusual patterns, 
workarounds, tech debt taken on intentionally, etc. This section is optional but useful for 
complex tasks.]
```

## Why Each Section Matters

| Section | Who Uses It | Why It Matters |
|---|---|---|
| Task / Spec Section / SRS | QA + Engineer | Links the PR back to requirements — enables traceability |
| What This PR Implements | QA | Quick orientation — what am I looking at? |
| Acceptance Criteria | QA | The test checklist — QA checks each box |
| How to Test | QA | Without this, QA guesses. Guessing means missed bugs or false flags. |
| Known Limitations | QA | Prevents QA from reporting expected gaps as bugs |
| Dependencies | QA + Engineer | Ensures the test environment is set up correctly |
| Implementation Notes | Engineer | Helps with code review and future maintenance |

## Engaging QA After PR Creation

Once the PR is open and the description is complete:

1. **Notify QA directly** — provide the PR link and the Asana task ID. Don't just open the PR and hope QA notices.
2. **Add the Asana comment:**
   ```
   PR open: [PR link]. Notifying QA for review.
   ```
3. **Do not move the Asana task to the QA column.** QA moves the task themselves when they begin their review. This respects QA's queue management — they may be finishing another review first.
4. **If QA doesn't pick it up within a reasonable window** (defined by your team's cadence — typically 24 hours for active sprints), notify the PM. Don't nag QA directly.

## Responding to QA Feedback

QA will provide feedback on the PR — comments, requested changes, or test results. Categorize each piece of feedback and respond accordingly:

### Category 1: Clear Bug in Your Implementation

QA found something that doesn't work as specified.

**Your response:**
1. Acknowledge the feedback in the PR comments
2. Fix the issue on the same branch
3. Push the fix
4. Comment on the PR: "Fixed — [brief description of what was wrong and what you changed]"
5. Re-request QA review

### Category 2: Spec Gap or Ambiguous Behavior

QA found a scenario the spec doesn't clearly address — "what should happen when the user does X?" and the spec doesn't say.

**Your response:**
1. Do NOT implement a guess. This is a spec gap.
2. Comment on the PR: "This is a spec gap — [describe the scenario]. Escalating to Engineer for guidance."
3. Follow the escalation process in `escalation_to_engineer.md`
4. Once the Engineer provides guidance, implement it, push, and re-request QA review
5. If the Engineer updates the spec, note the spec update in your PR comment

### Category 3: QA Flagging Something Out of Scope

QA flags something that you intentionally excluded (and documented in "Known Limitations").

**Your response:**
1. Reference the specific line in your "Known Limitations" section
2. Reference the spec section that scopes this task
3. Be respectful — QA may not have noticed the limitation note, or may genuinely believe the scope should be different
4. If QA still disagrees after seeing the limitation note, **escalate to the Engineer** for tiebreaking. Do not argue — let the Engineer decide.

### After All Feedback Is Addressed

1. Ensure all PR comments are resolved (either fixed or discussed)
2. Re-request QA review with a summary comment:
   ```
   All feedback addressed:
   - [Item 1]: Fixed — [what changed]
   - [Item 2]: Spec gap resolved per Engineer guidance — [what was decided]
   - [Item 3]: Out of scope per Known Limitations — QA acknowledged
   Ready for re-review.
   ```
3. Update the Asana task:
   ```
   Addressing QA feedback. Items: [count]. Fixes pushed. Re-review requested.
   ```

## When QA Approves

QA approval means:
1. **QA merges the PR** — not you. This is a deliberate ownership boundary. QA's merge is the final quality stamp.
2. After merge confirmation, move the Asana task to **Completed**
3. Add the completion comment:
   ```
   PR merged. Task complete.
   ```

## Common QA Handoff Mistakes to Avoid

- **Vague "How to Test" section:** "Test the registration flow" is useless. "Navigate to /register, enter a valid email and matching passwords, submit, verify redirect to /dashboard and success toast" is useful.
- **Missing prerequisites:** If QA needs test data or a specific env var, not mentioning it wastes their time setting up.
- **Forgetting Known Limitations:** If you know social login isn't in this PR, say so. Otherwise QA will file it as missing.
- **Pushing to the branch while QA is mid-review without warning:** Tell QA before pushing during their review cycle. Unexpected changes invalidate their testing.
- **Arguing about scope in PR comments:** If there's a genuine scope dispute, escalate to the Engineer. PR comments are for technical discussion, not scope negotiation.
