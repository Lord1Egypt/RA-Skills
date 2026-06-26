# Interview Rubric

Detailed 1-5 scoring criteria for each feedback category. Reference this when assigning scores in Phase 4.

## Communication (1-5)

| Score | Criteria |
|-------|----------|
| 1 | Silent coding. No verbal explanation. Cannot articulate what they are doing or why. |
| 2 | Minimal narration. Speaks only when prompted. Explanations are vague or incomplete ("I'll just use a hash map" with no reasoning). |
| 3 | Explains approach at a high level but skips details. States complexity when asked but doesn't volunteer it. Some gaps in reasoning ("it should work" without justification). |
| 4 | Clearly narrates thought process. States assumptions, describes approach before coding, explains complexity unprompted. Minor gaps (e.g., doesn't mention space complexity or skips one edge case verbally). |
| 5 | Exceptional clarity. Structured verbal walkthrough: restates problem, asks clarifying questions, describes brute force with complexity, explains optimization rationale, calls out edge cases proactively, and summarizes after coding. Easy to follow throughout. |

### Common deductions

- -1: Didn't ask any clarifying questions
- -1: Didn't state complexity until asked
- -1: Jumped to code without verbal plan
- -1: Used jargon without explaining reasoning

## Problem-Solving (1-5)

| Score | Criteria |
|-------|----------|
| 1 | Cannot identify a brute force approach. No progress toward a solution. |
| 2 | Identifies brute force but cannot analyze its complexity or suggest improvements. Gets stuck without hints. |
| 3 | Identifies brute force, states complexity correctly. Needs 1-2 hints to reach a better solution. Can describe the optimization at a high level. |
| 4 | Identifies brute force, correctly analyzes complexity, and independently proposes an optimized approach with correct complexity. Handles most follow-up questions well. Minor gaps in edge case identification. |
| 5 | Rapid problem decomposition. Immediately sees brute force, identifies the bottleneck, proposes the optimal approach with correct time/space complexity. Anticipates edge cases. Handles all follow-ups including constraint changes smoothly. |

### Common deductions

- -1: Wrong complexity analysis (e.g., says O(n) when it's O(n^2))
- -1: Missed obvious edge case (empty input, single element)
- -1: Could not explain WHY their optimization works
- -1: Failed to adapt when constraints changed
- -1: No brute-force baseline before jumping to optimization

## Code Quality (1-5)

| Score | Criteria |
|-------|----------|
| 1 | No working code produced. Pseudocode only (when real code was expected) or code with fundamental logic errors. |
| 2 | Code runs on happy path but has bugs on edge cases. Poor variable naming. No structure (everything in one block). |
| 3 | Code is mostly correct. Handles common cases. Reasonable naming. Some redundancy or minor inefficiency. 1-2 small bugs that candidate can fix when pointed out. |
| 4 | Clean, correct code. Good variable names, clear structure. Handles edge cases. Minor style issues only (e.g., could extract a helper function). |
| 5 | Production-quality code. Clean naming, modular structure, handles all edge cases. Defensive coding where appropriate. Candidate can explain every line and would be comfortable shipping this. |

### Common deductions

- -1: Off-by-one errors
- -1: Missing null/empty checks
- -1: Unnecessarily complex logic (could be simplified)
- -1: Poor variable names (i, j, temp, val for everything without context)
- -1: Didn't test their code mentally or with an example

## Overall Assessment Guide

| Average Score | Assessment |
|---------------|------------|
| 4.5-5.0 | Strong hire signal. Clear thinking, clean code, excellent communication. |
| 3.5-4.4 | Lean hire. Solid fundamentals with room for improvement in specific areas. |
| 2.5-3.4 | Borderline. Some strengths but significant gaps. Needs targeted practice. |
| 1.5-2.4 | Below bar. Needs substantial improvement in fundamentals. |
| 1.0-1.4 | Not ready. Recommend focused study plan before attempting interviews. |

## Feedback Writing Guidelines

When writing "What went well" and "What was missing":

**Do:**
- Reference specific moments: "When you identified that the brute force was O(n^2) due to nested loops..."
- Mention specific missing items: "Did not consider the case where the array contains duplicates"
- Quantify when possible: "Took 3 hints before reaching the sliding window approach"
- Compare to ideal: "Optimal solution uses O(1) space; your approach uses O(n) auxiliary space"
- Suggest concrete next steps: "Practice 2 more sliding-window mediums forcing yourself to state brute force first"

**Don't:**
- Use generic praise: "Good job overall"
- Be vague about gaps: "Could improve problem-solving skills"
- Skip actionable advice: always pair criticism with what the candidate should have done
- Omit the ideal approach: always show what a strong answer looks like
