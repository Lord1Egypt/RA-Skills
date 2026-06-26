# Post-processing: Detection & Correction SOP

## Applicable Scenarios

Detecting and surgically fixing narrative weight misalignment in completed technical tutorials, deep-dive articles, and interview prep content.

## Detection Workflow

### Step 1: Extract Core Concepts from the Article

Scan the article for all technical details presented as core concepts. Indicators:
- Appears in section/subsection titles
- Has independently elaborated code examples and explanations
- Prioritized in interview talking points / summaries

### Step 2: Identify the Proposition Conveyed by Each Core Concept

Before applying the substitution test, you must determine **what proposition each core concept is actually conveying in this article's context**. The same technical detail can carry different propositions depending on context.

For each core concept from Step 1, answer:

> **What is this concept actually asserting in this article? What would the reader take away as the key insight?**

Common pitfall: substituting the literal term/implementation instead of the proposition. For example:
- "JSX is `React.createElement()` syntax sugar" — the proposition is "JSX has no independent semantics, it's just JS function calls" (Architectural), NOT "JSX compiles to the specific function `createElement`" (Transport).
- The distinction hinges on what the article is asserting, not what technical term appears on the surface.

**Proposition granularity**: When a concept is elaborated at different depths, read the proposition at the level the article actually elaborates. If the article devotes a full section to the math, the proposition is at the math level. If it only mentions the concept in passing, read at the conceptual level. See `references/proposition-granularity-guide.md` for the decision flowchart and worked examples.

### Step 3: Apply Substitution Test to Each Proposition

For each proposition identified in Step 2, answer:

> **If this proposition were replaced with an alternative, would the user's observable behavior change?**

Determine role: Architectural / Transport / Configurable (definitions in SKILL.md)

### Step 4: Compare Narrative Weight vs. Role

For each core concept, compare its **actual role** against its **narrative weight in the article**:

| Actual Role | Narrative Weight | Verdict |
|-------------|-----------------|---------|
| Architectural | High (independent section / key elaboration) | ✅ Correct |
| Architectural | Low (compressed into a few flow steps / one table row) | ❌ Misalignment: obscured |
| Transport | High (independent section / key elaboration) | ❌ Misalignment: over-highlighted |
| Transport | Low (one paragraph, mentioned in passing) | ✅ Correct |
| Configurable | Medium (mentioned as needed / supplementary note) | ✅ Correct |
| Configurable | High (independent section / key elaboration) | ❌ Misalignment: disproportionate length |

### Step 5: Output Detection Report

Format:

```
- [✅ Correct] xxx: presented as core, actually Architectural
- [❌ Over-highlighted] xxx: presented as core, actually Transport; yyy is the actual Architectural core
- [❌ Obscured] xxx: compressed into a detail, actually Architectural core
- [❌ Disproportionate] xxx: independent chapter, actually Configurable
```

If all items are ✅, detection passes and the process terminates.

## Correction Workflow

Execute only when detection finds ❌ items.

### Principles

- **Local weight migration**, not full rewrite
- **Change narrative weight only, not facts** — keep existing code examples and comparison tables if they are correct
- After correction, run detection again to confirm issues are resolved

### Steps

1. **Downgrade Transport concepts**:
   - Remove from section/chapter titles
   - Compress length to "First, the signal is obtained via [transport method], then..."
   - Remove independent elaboration (e.g., from "one of three core mechanisms" to supplementary note)

2. **Upgrade Architectural concepts**:
   - Make into section title or core subsection
   - Elaborate on how it determines user-observable behavior
   - Use it as the anchor for the reader's mental model
   - Add independent code examples demonstrating behavioral differences

3. **Handle Configurable over-length**:
   - Downgrade from independent chapter to supplementary note/aside
   - Keep facts but compress elaboration

4. **Align all cross-references**:
   - Interview talking points, pitfall tables, summary paragraphs should align with the article's narrative structure
   - Change only focus/framing, not correct factual content

5. **Second-pass detection**:
   - Run the detection workflow again on the corrected article
   - If all ✅, proceed to Step 6 (Authoritative Verification)
   - If ❌ items remain, continue correcting (but typically one round suffices)

6. **Authoritative Verification**:
   - **Purpose**: Ensure corrections did not introduce technical semantic errors. The preceding steps only verify internal consistency (narrative weight alignment), but do not check against external ground truth. This step closes that gap.
   - **Scope**: Only verify **modified sections** — sections that were rewritten, retitled, or had their key propositions rephrased during correction. Unmodified content was already correct and needs no re-verification.
   - **What to verify vs. what NOT to verify**:
     - **Verify: technical facts** — behavioral claims, mechanism descriptions, API behavior. These must match authoritative sources.
     - **Do NOT verify: narrative framing** — which concept gets emphasized, how sections are organized, what appears first. Official documentation serves a different purpose (comprehensive reference / API lookup) than our articles (mental model construction). Official docs may highlight a concept for reference convenience while our framework classifies it as Transport/Configurable. This divergence is expected and intentional.
     - **Boundary test**: if the article says "X does Y" and official docs say "X does Z", that's a fact error → ❌. If the article says "X is the core mechanism" and official docs give X its own section but our framework classifies X as Transport, that's a framing difference → ✅ (not an error).
   - **Method**:
     a. For each modified section, extract its **core technical propositions** (the behavioral claims it makes)
     b. Search authoritative sources (official documentation, team blog posts, MDN, RFCs) for each proposition
     c. Compare: does the modified text's **factual claim** match what authoritative sources describe?
   - **Output format**:

   ```
   - [✅ Verified] "Proposition X": factually matches [source URL/description]
   - [⚠️ Ambiguous] "Proposition X": modified text says A, authoritative source says B — may need human review
   - [❌ Incorrect] "Proposition X": modified text contradicts [source URL/description] — correction needed
   ```

   - **If errors found**:
     - Do NOT auto-correct (the error may be subtle and require human judgment about what went wrong in the weight migration)
     - Report the errors to the user with specific source citations
     - User decides whether to fix manually or re-run correction
   - **If no errors found**: Post-processing terminates successfully

## Common Unexpected Results and Countermeasures

| Unexpected Result | Cause | Countermeasure |
|-------------------|-------|----------------|
| Detection finds no issues, but misalignment exists | Substitution test not applied strictly, or obscured Architectural concepts were missed | Focus on details "compressed into flow steps" — they're the easiest to overlook |
| Detection finds issues, but not narrative weight misalignment | Confusing "narrative weight misalignment" with other writing issues (unclear logic, incorrect code) | Return to substitution test — only focus on "role vs. narrative weight" mismatches |
| Architectural concepts incorrectly flagged as Transport | Substitution test applied to the literal term instead of the proposition conveyed in context | Re-execute Step 2 (proposition identification): identify what the article is actually asserting, then re-apply substitution test to the proposition, not the surface term |
| Article quality degrades after correction | Changed parts that shouldn't have been changed (deleted correct code examples, altered correct facts) | Strictly follow "change narrative weight only, not facts"; in second-pass detection, verify factual completeness of modified sections |
| Post-processing loop never terminates | Correction introduces new misalignment (e.g., upgrading A caused B to be over-downgraded) | If second pass has only 1-2 borderline items, use human judgment on whether further adjustment is worthwhile — avoid over-iteration |
| Authoritative verification finds errors | Weight migration accidentally altered a technical claim (e.g., "just a signal method" oversimplified a behavior) | Report to user with source citations — do not auto-correct; the fix may require re-examining the proposition identification in Step 2 |
| Authoritative verification finds no sources | The topic is niche or too new for authoritative documentation | Flag as unverified rather than verified; the user should review manually |
| Authoritative verification disagrees with the article's framing but not its facts | The article's emphasis differs from official docs (e.g., official docs highlight SyntheticEvent, article highlights Fiber traversal) | This is expected — narrative weight realignment intentionally diverges from common framing; only flag if the technical claim itself is wrong, not just the emphasis |
| Proposition granularity causes different substitution results | Same detail read at conceptual level → Architectural, read at implementation level → Configurable | Use the article's own elaboration depth as the tiebreaker: if the article elaborates the math, read at math level; if it only mentions the concept, read at conceptual level. See `references/proposition-granularity-guide.md` |
