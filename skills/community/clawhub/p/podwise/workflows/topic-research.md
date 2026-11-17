# Podwise Topic Research

Use this skill to answer the question: *what do podcasts actually say about X?* It searches across Podwise's transcript corpus, synthesizes insights from multiple episodes and speakers, and produces a report that reads like research — not a playlist.

## Goals

1. Verify the Podwise MCP connection.
2. Clarify the research topic and scope with the user.
3. Use `ask_podwise` to retrieve transcript-grounded insights with cited source clips.
4. Fetch summaries and highlights from the cited episodes.
5. Synthesize a structured research report with multiple perspectives, key claims, and source links.
6. Write the report to a file and offer to export it.

## Step 1: Check the Environment

Call `get_me`. If the Podwise tools are unavailable or return an authentication error, stop and follow [../references/installation.md](../references/installation.md) before continuing.

## Step 2: Load the Listener Taste

Look for `taste.md` in the current working directory.

- If found, read the **Core Interest Areas**, **PKM tool**, and **Output Preferences** fields silently. Use these to frame the report's angle and format.
- If not found, proceed with default formatting and note at the top of the report: *"No taste.md found — run `refine-taste` to personalise research output."*

## Step 3: Clarify the Research Topic

If the user has not already stated a clear topic, ask:

1. **Topic**: What specific topic, question, or theme do you want to research? The more specific, the better — e.g. "How do AI researchers think about consciousness?" beats "AI".
2. **Angle**: Are you looking for a broad overview, a specific angle, or contrarian takes?

If the user already provided both, skip the questions and proceed.

## Step 4: Ask Podwise

Call `ask_podwise` with the research topic as the `question`.

The answer includes **cited source clips** (episode seq, speaker, timestamps) automatically — there is no separate sources flag. The call counts against the user's Ask quota and may take up to 60 seconds; do not cancel early.

Parse the result to extract all cited episode seqs and the answer text. The cited episodes are the primary sources for Step 5.

## Step 5: Fetch Deep Artifacts from Cited Episodes

For each cited episode `seq`, call `get_episode_summary` (this returns the summary, takeaways, chapters, highlights, Q&A, keywords, and mind map in one call).

**Handling cited episode count:**

- **3 or more cited episodes**: Proceed normally — fetch artifacts for all.
- **Fewer than 3 cited episodes**: Proceed with whatever episodes were cited. Add a note at the top of the report: *"Limited sources — this topic may be underrepresented in Podwise's corpus. Consider broadening your topic or angle."*
- **0 cited episodes**: `ask_podwise` succeeded but returned no source citations. Proceed using only the answer text to write the report. Add a note at the top: *"No cited episodes available — this report is based on AI synthesis only, not traceable to specific episodes."*

If `get_episode_summary` fails because an episode is not yet processed, skip that episode and note it in the report. Do not prompt for processing — do not let quota confirmation interrupt the research flow.

If the user explicitly asks to include an unprocessed episode, ask for confirmation once and then call `process_episode` with the `seq`.

## Step 6: Synthesize the Research Report

With the `ask_podwise` answer and the episode artifacts in hand, write a structured research report in four parts.

### Part 1 — Overview

2–3 paragraphs summarising the state of the topic as represented across Podwise's podcast corpus. Draw primarily from the answer. Be specific — name claims, name the kinds of speakers making them, and note any strong consensus.

### Part 2 — Key Perspectives

Identify 3–5 distinct perspectives, arguments, or schools of thought that appear across the source episodes. For each:

- Give the perspective a short label (e.g. "The optimist case", "The regulatory concern", "The practitioner view")
- Summarise it in 3–5 sentences
- Cite the episode(s) that best represent it with a link

This is the most important section. The goal is not to list what each episode said, but to map the *intellectual landscape* of the topic.

### Part 3 — Points of Tension

Where do speakers disagree? Identify 2–3 genuine tensions, contradictions, or unresolved debates found across the source material. Write 2–3 sentences on each tension and name the opposing positions. If all sources express substantially the same view, skip this section and note: *"The source material shows strong consensus on this topic — no significant tensions were found."*

### Part 4 — Source Episodes

A reference list of all episodes cited in the answer and successfully fetched in Step 5:

- **{Episode Title}** · {Podcast Name} · {date} · [Open]({episode-url})
  > {one sentence on what this episode contributes to the topic}

---

## Step 7: Write the Report File

Name the file using the pattern: `topic-research-{topic-slug}-{YYYY-MM-DD}.md`

Example: `topic-research-ai-agents-2026-03-21.md`

Write the file to the current working directory unless the user specifies another path.

Use this document template:

```markdown
# Topic Research: {Topic}

**Research question**: {the user's original framing}
**Sources**: {N} episodes across {M} podcasts
**Generated**: {date}
{If limited sources or no citations: add the applicable note from Step 5}
{If no taste profile: "Note: run `refine-taste` for personalised output."}

---

## Overview

{Part 1 content}

---

## Key Perspectives

### {Perspective label}
{3–5 sentences. Source: [{Episode Title}]({url})}

### {Perspective label}
{3–5 sentences. Source: [{Episode Title}]({url})}

---

## Points of Tension

**{Tension label}**
{2–3 sentences describing the opposing positions.}

---

## Source Episodes

- **{Episode Title}** · {Podcast Name} · {date} · [Open]({url})
  > {one-sentence contribution note}

---

_Generated by podwise-topic-research · {date}_
```

After writing the file, confirm the path and ask:
*"Would you like me to go deeper on a specific perspective, fetch the full Q&A from an episode, or export this report to your PKM?"*

## Common Failure Cases

- If `ask_podwise` times out or returns an error, report the error directly. Do not fabricate a synthesis — tell the user the research could not be completed and suggest retrying with a more specific topic.
- If the user's topic is very broad (e.g. "technology", "health"), ask them to narrow it before running — `ask_podwise` performs better on specific questions than general categories.
- If `get_episode_summary` fails for a cited episode because it is not yet processed, skip it and note it in the report. The answer remains the primary source.
- If all cited episodes fail to fetch artifacts, produce a lightweight report from the answer text only and label it clearly as a "synthesis-only report".

## Output Contract

Produce exactly one report file per run.

The report must include at minimum: Overview, Key Perspectives, and Source Episodes.

Points of Tension may be omitted only when source material shows genuine consensus.

The `ask_podwise` answer is the primary synthesis source. Episode artifacts are supplementary depth — use them to sharpen and cite the perspectives, not to replace the synthesis.

Always write the file and confirm the path. Always end with the follow-up prompt.
