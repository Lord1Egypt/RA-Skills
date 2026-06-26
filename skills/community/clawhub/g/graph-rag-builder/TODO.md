# TODO — Deferred Features

Features explicitly deferred from the initial build. Revisit after M5 (working MCP server) is complete.

---

## High Priority

### YouTube Transcript Fetching (M1/M2 revision)

`crawl.py` already detects and stores YouTube video IDs in the `youtube_ids` field of each raw page JSON. What's missing is actually fetching and indexing those transcripts in `extract_concepts.py`.

**What to add to M2 (`extract_concepts.py`):**
- After loading a raw page JSON, check for non-empty `youtube_ids`
- For each ID, call `YouTubeTranscriptApi.get_transcript(video_id)` (already in `requirements.txt` as `youtube-transcript-api`)
- Concatenate transcript segments into text, then chunk at ~500-word boundaries (reuse `_force_split`)
- Each transcript chunk becomes an additional entry in the page's `chunks` list, with `section = "YouTube Transcript"` and `url` set to `https://youtube.com/watch?v=<id>`
- Cache raw transcripts to `raw_content/<url_hash>_yt_<video_id>.json` so re-runs skip the API call

**Edge cases to handle:**
- `TranscriptsDisabled` — log and skip, don't crash
- `NoTranscriptFound` — try `find_generated_transcript(['en'])` as fallback
- Auto-generated vs. manually uploaded transcripts — prefer manual, note which was used in output JSON
- Rate limiting from YouTube — add `--yt-delay` flag (default 1.0s) between transcript fetches

**Why deferred:** Strudel's site has no YouTube embeds (uses live REPL). Implement when testing against a site that links to tutorial videos (e.g., a course site or library with video walkthroughs).

Relevant phase: Phase 2/3 (M2 `extract_concepts.py`)

---

### Neo4j Export
For knowledge graphs exceeding ~10,000 nodes, networkx + JSON becomes slow for complex multi-hop queries. Add an optional `--neo4j` flag to `build.py` that generates a `.cypher` file of `CREATE` statements for bulk import, or writes directly to a running Neo4j instance via the `neo4j` Python driver.

Relevant phase: Phase 4 (Graph Construction)

---

### Embedding API Support
Currently the skill uses local `sentence-transformers` (`all-MiniLM-L6-v2`). Some users may prefer API-based embeddings for better quality or to avoid the ~80MB model download. Add a `--embedding-model` flag with options:

- `local` (default) — `sentence-transformers`, no API key required
- `openai` — `text-embedding-3-small` via OpenAI API
- `voyage` — Anthropic's recommended `voyage-3` via Voyage AI API

Abstract the embedding step behind an interface so swapping providers requires no other changes.

Relevant phase: Phase 5 (Embedding Index), Phase 0 (dependency management)

---

## Medium Priority

### Incremental Graph Merging
Currently, on incremental re-run, only changed pages are re-processed — but their concepts and edges are completely replaced in the graph. This can leave orphaned nodes (concepts that no longer appear anywhere) or miss merges where the same concept name was extracted from multiple pages.

Add a graph merge pass after Phase 4 that:
1. Deduplicates concept nodes by normalized name (case-insensitive, lemmatized)
2. Removes nodes with no incoming or outgoing edges
3. Logs a diff of added/removed nodes between runs

---

### Scheduled Re-Crawls
Add a `--schedule` option (e.g., `--schedule daily`) that writes a cron entry or launchd plist to re-run `build.py` automatically for a given topic. The incremental mode means re-runs are cheap if the site hasn't changed.

---

### Graph Visualization
Generate a static HTML visualization of the knowledge graph (e.g., using `pyvis` or `d3.js` via a template) alongside the MCP server output. Useful for inspecting what the crawler found and debugging poor-quality concept extraction.

Output file: `output/<slug>/graph_viz.html`

---

## Lower Priority

### Additional Content Sources
- **GitHub repositories**: Crawl `README.md`, `/docs/`, and inline docstrings
- **Confluence / Notion**: Add authenticated crawl support via their APIs
- **Discord / Slack**: Index pinned messages and thread summaries (with user permission)
- **RSS/Atom feeds**: Watch for new content and trigger incremental updates

### Multi-Language Support
`youtube-transcript-api` supports auto-translated transcripts. Add a `--language` flag that fetches transcripts in the specified language and passes it as context to the LLM extractor.

### MCP Server Authentication
The generated `server.py` currently has no auth. For sharing a server with a team (rather than running it locally), add optional API key authentication via an environment variable.

### Chunk Quality Scoring
After LLM extraction, score each chunk by concept density (concepts extracted / word count). Surface low-density chunks to the user as candidates for manual review or exclusion. High-density chunks get priority in search ranking.

### Export to Other Formats
- **Obsidian vault**: Each concept becomes a note, with wiki-links for relationships
- **Anki flashcards**: Concept + definition → front/back flashcard export
- **JSON-LD / schema.org**: Structured data export for integration with other tools
