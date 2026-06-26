# Nightly Memory Consolidation — 2 AM

You are running as a scheduled nightly job to consolidate today's work into memory.

## Your Task

1. **Read today's daily note** (`memory/daily/YYYY-MM-DD.md`)
   - Review all conversations, decisions, and work from today

2. **Extract to knowledge base** (PARA method)
   - **Projects** (`knowledge/projects/`) — Active work, status updates, blockers
   - **Areas** (`knowledge/areas/`) — Ongoing responsibilities (business, dev, marketing, crypto, security)
   - **Resources** (`knowledge/resources/`) — Tutorials, patterns, lessons learned
   - **Entities** (`knowledge/entities.md`) — New people, services, accounts mentioned

3. **Update daily note**
   - Add a summary section at the end with key takeaways
   - Mark completed tasks with [x]
   - Flag blockers or open questions

4. **Update MEMORY.md**
   - Extract only high-value, long-term insights
   - Decisions that shape how we work
   - Important preferences or patterns
   - Context that will matter weeks or months from now

5. **Re-index QMD**
   - Run QMD update and embed commands to refresh the search index
   - Ensure tomorrow's memory searches are fast and current

## Output Format

Reply with a brief summary of what you consolidated:
- Number of knowledge files updated
- Key insights added to MEMORY.md
- QMD re-index status

Keep it concise — this runs automatically every night.
