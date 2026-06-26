# Chapter Workflow — Step-by-Step Process

This reference defines the exact workflow for creating, reviewing, and approving chapters within the book pipeline.

---

## Chapter Brief Template

When creating a brief for any chapter, produce a file (`ch[XX]-brief.md`) containing ALL of the following:

```
# CHAPTER [X] BRIEF — [Chapter Title]

## Book
**[Book Title]**
**Subtitle:** [Subtitle]

## Chapter Status
Ready for draft.

## What Previous Chapters Established (Do Not Repeat)
[Bullet list of key points already covered — writer must NOT re-explain these]

## Chapter Goal
[2-3 sentences: what this chapter must accomplish for the reader]

## Target Reader State at Chapter Start
[What the reader knows, feels, and expects arriving at this chapter]

## Reader State at Chapter End
[3-4 bullet points: "The reader should finish thinking..."]

## Non-Negotiable Chapter Purpose
[Numbered list: 4-6 things this chapter MUST do]

## What the Chapter Must Cover
[Bullet list of specific content areas]

## What This Chapter Must NOT Do
[Explicit list of pitfalls, repetitions, and tone failures to avoid]

## Opening Guidance
[How the chapter should open — what NOT to open with, and examples of good openings]

## Tone Guidance
[Specific tone notes for this chapter]

## Structure Suggestion
[Numbered sequence: rough flow of the chapter — guidance, not rigid]

## Content Notes
[Specific instructions about examples, analogies, scenarios]

## Research Requirements
[What evidence/sources this chapter needs]

## Source Handling
[Rules for citations, verification markers]

## Continuity Requirements
[What must be read before drafting, what must be maintained]

## Humanization Rules for This Chapter
### Must do
[Chapter-specific positive instructions]
### Must avoid
[Chapter-specific forbidden patterns]

## Forbidden Feel
[If this chapter sounds like X, Y, or Z — it has failed]

## Word Count
Target **[X,XXX to X,XXX words]**.

## Deliverable Format
1. Full chapter draft
2. Short source note section
3. All [NEEDS VERIFICATION] markers left in place

## Chapter Ending Requirement
[How the chapter must end — forward momentum into next chapter]
```

---

## Drafting Process (For Writers)

### Before Writing
1. Read the chapter brief completely
2. Read the continuity document — understand what has been established
3. Read the research notes for this chapter
4. Read the humanization rules (load `references/humanization-rules.md`)
5. Identify the target word count range

### While Writing
1. Follow the brief's structure suggestion as a guide, not a rigid template
2. Open with a hook — human, specific, recognizable. Never a definition or statistic.
3. Hit every item in "Non-Negotiable Chapter Purpose"
4. Cover every item in "What the Chapter Must Cover"
5. Avoid every item in "What This Chapter Must NOT Do"
6. Apply humanization rules continuously — don't save it for a later pass
7. Mark any uncertain factual claims with [NEEDS VERIFICATION]

### After Writing — Self-Review
1. Run the full humanization pass (Section 5 of humanization rules)
2. Scan for every forbidden word and phrase — rewrite any found
3. Count em-dashes — reduce if >1 per 1,000 words
4. Check paragraph openers for repetition
5. Read the last paragraph aloud — does it sound like a TED talk? Rewrite.
6. Verify word count is within target range
7. Confirm source note section is included
8. Confirm all [NEEDS VERIFICATION] markers are in place

### Delivery
Post the complete draft with:
- Full chapter text
- Word count
- Source note section listing claims needing citation verification
- All [NEEDS VERIFICATION] markers preserved

---

## Review Process (For Reviewers)

### Step 1: Read the Draft
Read the full chapter without scoring first. Note first impressions.

### Step 2: Run Quality Checklist
Load `references/quality-checklist.md` and check every item.

### Step 3: Score
Score all 6 dimensions (1-10):
- Humanization (25%)
- Continuity (20%)
- Genre Fit (15%)
- Craft (15%)
- Content Accuracy (15%)
- Engagement (10%)

### Step 4: Verdict
- **Average >= 7, no dimension < 5** → APPROVED
- **Average 6-7** → REVISE (one rewrite attempt with specific notes)
- **Average < 6** → REWRITE (start fresh with new guidance)

### Step 5: Report
Write the review report using the format in quality-checklist.md.

### Step 6: Post-Approval Actions
When a chapter is approved by the final authority:
1. Save approved chapter as `.docx` to `{{BOOKS_DIR}}/[book-slug]/manuscript/ch[XX]-approved.docx`
2. Update CHAPTER-TRACKER.md with new status
3. Update continuity.md with chapter summary
4. Write the next chapter's brief
5. Write/gather the next chapter's research notes
6. Update NEXT-ACTION.md

---

## Continuity Document Format

The continuity document (`continuity.md`) must be updated after every approved chapter:

```
# CONTINUITY — [Book Title]

## Current Story/Argument State
[1-2 paragraphs: where the book stands after the latest chapter]

## What Must Stay Consistent
[Bullet list: voice, tone, approach, recurring elements]

## Running Themes
[Bullet list: themes introduced and maintained across chapters]

## Chapter Summaries

### Chapter 1 — [Title]
**Status:** [Approved/Draft/etc.]
**Summary:** [3-4 paragraph summary covering: what happens, key elements introduced, tone set, how it ends]
**Key elements introduced:** [Bullet list]

### Chapter 2 — [Title]
...

## Unresolved Threads
[What needs to be picked up or resolved in future chapters]
```

---

## Research Notes Template

For each chapter requiring research support, produce a file (`ch[XX]-research-notes.md`):

```
# CHAPTER [X] RESEARCH NOTES — [Chapter Title]

## Research Status
[Who prepared this, how heavy the research load is]

## Key Areas to Support
### 1. [Topic Area]
[What evidence is needed, what claims must be supported, any specific data points]
[NEEDS VERIFICATION] markers for specific statistics

### 2. [Topic Area]
...

## What This Chapter Does NOT Need
[Research that would be excessive or off-topic]

## Tone Reminder
[How the research should be integrated — seamlessly, not as info-dumps]

## Bridge to Next Chapter
[How this chapter's content leads into the next]
```
