# Escalation to Engineer — When and How to Ask for Help

The Engineer is the technical authority on the project. They wrote the Implementation Plan, they understand the architecture, and they're the right person to help when you're stuck on something the spec doesn't cover or the code won't cooperate with. But escalations cost the Engineer's time and context-switch them from their own work — so escalate with full context, and only after you've done your due diligence.

## When to Escalate

### Escalate When:

- **The spec is unclear on what to implement.** You've read the spec section referenced in your task, and you genuinely don't know what the expected behavior should be in a specific scenario.
- **There's a conflict between the spec and existing code.** The spec says to do X, but the existing codebase does Y in a way that would conflict. You need guidance on which one is correct.
- **You've tried to resolve a technical issue for 30+ minutes without progress.** You've researched, tried approaches, and you're stuck. Don't spin for hours — the Engineer can often unblock you in minutes.
- **The right solution seems to contradict the spec.** You've figured out a way to implement the feature, but it requires doing something the spec explicitly says not to do (or doesn't account for). Escalate BEFORE implementing.
- **You found a likely error in the spec.** A data type doesn't match, an API endpoint references a field that doesn't exist, a workflow step seems impossible. Flag it — the Engineer needs to know.
- **You need an architectural decision you're not empowered to make.** "Should this be a separate service or a module in the existing service?" "Should I use WebSockets or polling here?" These are Engineer decisions.

### Do NOT Escalate When:

- **You haven't read the spec section referenced in your task yet.** Read it first. The answer might be there.
- **You haven't tried anything yet.** Spend at least 30 minutes attempting a solution before escalating. The Engineer expects you to bring "here's what I tried" context.
- **It's a language/framework question your stack skills should cover.** If you're stuck on "how do I write a React useEffect hook" or "how do I set up a PostgreSQL connection pool," consult your stack-specific skills and documentation first. The Engineer isn't a coding tutor — they're the architectural authority.
- **It's a tool or environment issue you can research.** "How do I configure ESLint" or "my Docker container won't start" — research these before escalating. Escalate only if you're stuck after 30 minutes.
- **You want to deviate from the spec for personal preference.** "I think Redux is better than Context API" — unless there's a technical reason the spec's approach won't work, implement what the spec says.

## The Escalation Request Format

When you escalate, provide ALL of the following. Incomplete escalations cause back-and-forth that slows everyone down.

```
ESCALATION REQUEST
==================

TASK: [Task ID and title from Asana]
SPEC SECTION: [FE-XXX or BE-XXX — the specific section you're working from]
BRANCH: [Your current branch name]
URGENCY: [Blocking — can't continue / Non-blocking — can work around temporarily]

WHAT I'M TRYING TO DO:
[Which part of the spec you're implementing. Be specific — reference the exact 
acceptance criterion or spec paragraph.]

WHAT I TRIED:
[Approach 1: what you did, what happened]
[Approach 2: what you did, what happened]
[Include relevant code snippets, error messages, or test results]

WHAT BROKE / WHAT'S UNCLEAR:
[Exact error message, unexpected behavior, or the specific spec text that's 
ambiguous. Copy-paste the actual text — don't paraphrase.]

WHERE I AM IN THE CODE:
[File path and function/component name where you're working]

SPEC REFERENCE:
[Quote or reference the exact spec text that's relevant — section ID, paragraph, 
or acceptance criterion. If the spec is unclear, quote the part that's unclear 
and explain what's ambiguous about it.]

MY BEST GUESS (if applicable):
[If you have a theory about what the right answer might be, share it. The Engineer 
may confirm it instantly, saving everyone time.]
```

### Why Each Field Matters

| Field | Why the Engineer Needs It |
|---|---|
| Task + Spec Section | Immediately orients the Engineer to the right part of the project |
| Branch | Engineer can look at your code if needed |
| Urgency | Helps the Engineer prioritize — blocking issues get faster responses |
| What I Tried | Prevents the Engineer from suggesting things you already attempted |
| What Broke | The specific error or confusion — not a vague "it doesn't work" |
| Where in Code | Lets the Engineer look at the exact spot if they need to |
| Spec Reference | The Engineer wrote the spec — quoting it back helps them see what you're seeing |
| Best Guess | Often saves a round-trip — the Engineer confirms or corrects |

## After Receiving Engineer Guidance

1. **Implement per the guidance.** The Engineer's response is authoritative — even if you disagree with the approach, implement it unless you have a strong technical reason not to (in which case, raise it with the Engineer, don't silently deviate).

2. **If the guidance changes the spec:** Confirm with the Engineer that the spec has been updated. If the spec hasn't been updated yet, note this in your Asana task comment — the PM needs accurate specs for client reporting.

3. **Close the loop.** Add a comment to the Asana task:
   ```
   Escalation resolved: [brief summary of what was decided and what changed].
   ```

4. **If the guidance doesn't fully resolve the issue:** Say so immediately. "Thanks for the guidance on X. That resolved the API endpoint question, but I'm still unclear on how the error response should be formatted — the spec section mentions a 'standard error format' but I don't see it defined anywhere." A follow-up escalation with new information is fine. A "same question again because the first answer didn't help and I didn't say so" is frustrating.

## Escalation Etiquette

- **Be specific, not vague.** "The spec is confusing" is unhelpful. "Spec section BE-012, paragraph 3: 'The endpoint should validate against the user schema' — which schema? I see two user schemas in the codebase (UserAuth and UserProfile) and the spec doesn't specify which one" is excellent.

- **Don't apologize for escalating.** If you've followed the decision tree and done your due diligence, escalating is the right thing to do. Spinning silently for hours is worse than asking for help.

- **Don't bundle unrelated issues.** If you have two separate blockers, send two separate escalation requests. Each should be self-contained and independently resolvable.

- **Provide your branch in a ready state.** Before escalating, commit and push your current work (even if it's broken). The Engineer may want to look at your code, and "it's on my local machine" adds friction.

## Escalation vs. Other Communication Channels

| Situation | Channel | Not Escalation |
|---|---|---|
| Spec unclear / spec conflict / technical wall | **Escalate to Engineer** | — |
| Task blocked by another dev's work | **Comment in Asana + notify PM** | PM handles scheduling conflicts |
| Task scope seems wrong | **Ask PM first** (scope) or **Engineer** (technical) | Depends on whether it's a priority question or a technical one |
| QA feedback you disagree with | **Escalate to Engineer for tiebreaking** | Don't argue in PR comments |
| Status update / timeline change | **Comment in Asana** | PM reads these for reporting |
| Found a bug outside your task scope | **Report to PM** | PM decides whether to create a bug task |
