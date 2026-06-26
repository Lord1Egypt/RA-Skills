---
name: obsidian-librarian
description: Obsidian second-brain and knowledge-base skill. Save any URL, article, tweet, or X post to your Obsidian vault as clean, categorized, wikilinked markdown. Two-pass Gemini pipeline handles structure, tags, and categories. Ask your whole vault anything with RAG, backed by a local JSON index or Supabase pgvector. URL fetch via Apify. Triggers on "save this", "save it", "save this url", research capture, vault search, or querying saved notes.
version: 0.2.7
metadata: {"openclaw":{"primaryEnv":"GEMINI_API_KEY","requires":{"env":["GEMINI_API_KEY","OBSIDIAN_VAULT_PATH"],"bins":["python3","curl"]},"homepage":"https://github.com/openclaw/obsidian-librarian"}}
---

# Obsidian Librarian

A second brain for Obsidian, on autopilot. Drop any URL, article, tweet, X post, or pasted text into OpenClaw and it lands in your vault as a clean, categorized, wikilinked markdown note. Then ask your whole vault anything and get grounded answers with citations.

Use this skill when the user wants OpenClaw to store text or a URL in the Obsidian vault as a cleaned, categorized markdown note, or to search and query notes they have already saved.

Trigger shortcuts:
- Treat `save this`, `save it`, `save this url`, and `save this link` as Obsidian-librarian requests when the same message contains a URL, pasted text, or quoted content to preserve.
- Treat short follow-ups like `save it` as Obsidian-librarian requests when the immediately preceding user message provided the text or URL to store.
- Treat phrases like `search my notes`, `search my vault`, `search Obsidian`, `what do my notes say about ...`, `ask my vault`, and `query my saved notes` as Obsidian-librarian requests that should run the RAG `ask` path.
- If the message only says `save this` or `save it` with no actual content or URL available in context, do not guess; ask what should be saved.
- If the intent is ambiguous between saving to the local filesystem versus saving to the knowledge vault, prefer the Obsidian vault when the content looks like a note, article, research snippet, or social post.

The vault is mounted in the container at `/data/.openclaw/obsidian-vault`. Raw inputs are staged in `/data/.openclaw/obsidian-vault/_Inbox`, then processed into category folders.

## Environment

Required:
- `GEMINI_API_KEY`: Gemini API key used for both ingest and RAG answer generation.
- `OBSIDIAN_VAULT_PATH`: Absolute path to the mounted Obsidian vault.

Conditional:
- `APIFY_API_KEY`: Required for URL ingestion.

Optional:
- `OBSIDIAN_INBOX_FOLDER`: Override the inbox folder name. Default: `_Inbox`.
- `OBSIDIAN_GEMINI_MODEL`: Primary model override for librarian operations.
- `GEMINI_MODEL`: Fallback model name when `OBSIDIAN_GEMINI_MODEL` is unset.
- `OBSIDIAN_RAG_INDEX_PATH`: Override the local JSON RAG index path.
- `SUPABASE_URL`: Enable Supabase-backed vector storage.
- `SUPABASE_KEY`: Supabase API key for vector storage.
- `EMBEDDING_MODEL`: Embedding model override. Default: `gemini-embedding-001`.
- `EMBEDDING_DIMENSIONS`: Embedding size. Default: `384`.

URL handling policy:
- Always use Apify to read the URL first.
- For `x.com` / `twitter.com` post URLs, use the dedicated Apify tweet actor.
- If an X post contains linked URLs, follow those linked URLs through the same Apify-first path before falling back.
- If direct URL reading fails, run a web-search fallback and stage the search-result snapshot instead.
- If both stages fail, surface the full error back to OpenClaw instead of silently swallowing it.

## Supported Inputs

- Pasted text
- A local text/markdown file
- A blog/article URL
- An existing file already sitting in `_Inbox`
- A natural-language question about the saved vault

## Workflow

1. Stage the raw source in `_Inbox/`.
2. Run Gemini pass 1 to clean and structure it into markdown.
3. Run Gemini pass 2 to choose category, tags, source attribution, and candidate wikilinks.
4. Scan existing vault notes for titles and aliases to resolve `[[wikilinks]]`.
5. Write the final note with YAML frontmatter into the chosen category folder.
6. Delete the `_Inbox` file only after the final note is written successfully.

## Ingest From Text File

```bash
python3 {baseDir}/scripts/run_pipeline.py ingest --text-file /data/.openclaw/workspace/input.txt
```

## Ingest From URL

```bash
python3 {baseDir}/scripts/run_pipeline.py ingest --url "https://example.com/article"
```

## Ingest An Existing Inbox File

```bash
python3 {baseDir}/scripts/run_pipeline.py ingest --inbox-file /data/.openclaw/obsidian-vault/_Inbox/some-file.md
```

## Ask The Vault (RAG)

```bash
python3 {baseDir}/scripts/run_pipeline.py --vault-path /data/.openclaw/obsidian-vault ask "What do my notes say about AI agents?" --print-json
```

Optional flags: `--category <Category>`, `--threshold <float>` (default `0.65`), `--limit <N>` (default `5`).

## Reindex The Vault

```bash
python3 {baseDir}/scripts/run_pipeline.py --vault-path /data/.openclaw/obsidian-vault reindex
```

Add `--file <path>` to re-embed a single note instead of the full vault.

## Notes

- For long pasted text, prefer writing it to a temp file under `/data/.openclaw/workspace/` and using `ingest --text-file`.
- Use `--title "Custom Title"` on `ingest` for an explicit note title override.
- Use `--keep-inbox` only when debugging. Normal behavior is to clean up the staged source after success.
- X status URLs preserve deterministic post metadata and captured post content instead of relying on a generic article-style rewrite.
- The pipeline does forward-linking only in v1. Existing notes are not modified.
- URL ingestion requires `APIFY_API_KEY` in the container environment.
- RAG indexing runs after successful ingests. By default it uses a local JSON index; set `SUPABASE_URL` and `SUPABASE_KEY` to use Supabase pgvector instead (requires `EMBEDDING_DIMENSIONS=384` to match `sql/vault_chunks.sql`).
- `SUPABASE_URL` must point at a Supabase-compatible API surface. All requests are issued against `/rest/v1/...`, so self-hosted PostgREST needs a gateway or reverse proxy that serves that prefix.
- Before enabling Supabase, apply `sql/vault_chunks.sql` to the target database. It provisions the `vault_chunks` table, the HNSW index, and the `match_vault_chunks` RPC that the `ask` command calls.
