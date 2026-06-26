---
name: group_summarizer
description: "Synthesizes member-parent markdown reports into a continuous narrative."
metadata:
  openclaw:
    emoji: 🦞
    version: "1.0.0"
---

# group_summarizer

Read all markdown files in "~/openclaw_agent/src/temp_sync/" recursively. 

## Logic
1. **Reading**: Read all markdown files in "~/openclaw_agent/src/temp_sync/" recursively.
2. **Grouping**: Categorize all content by the parent folder name (which represents the Team Member).
3. **Synthesis**: For each member, treat multiple days of reports as a single, continuous progress narrative. Do not repeat daily headers; blend them into a coherent update.
4. **Exclusion**: Do not include any meta-talk (e.g., "Here is the summary...") or technical details about how the file was generated. Provide only the synthesized content.
5. **Formatting**: 
   - Use `## [Member Name]` as the primary headers.
   - Use standard markdown for the body.

## Output
- **Target Path**: "~/openclaw_agent/src/latest_summaries/daily/{{date}}.md"
- **Date Variable**: Use the current UTC+8 date in `YYYY-MM-DD` format.

## Usage Examples
- "Run group_summarizer"
- "Generate the daily report using group_summarizer"
