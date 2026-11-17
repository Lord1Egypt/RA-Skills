# NotebookLM MCP — HTTP REST API reference

The `@roomi-fields/notebooklm-mcp` HTTP server (default `http://localhost:3000`,
override with `NOTEBOOKLM_SERVER_URL`). All bodies are JSON. Every notebook op
accepts either `notebook_id` (a UUID) or `notebook_url`. Only the endpoints most
relevant to research are listed; see the project README for the full 33.

## Health & auth

| Method | Path          | Body               | Purpose                                                       |
| ------ | ------------- | ------------------ | ------------------------------------------------------------- |
| GET    | `/health`     | —                  | Reachability + `{ authenticated, headless, current_account }` |
| POST   | `/setup-auth` | `{ show_browser }` | Interactive Google login (visible browser)                    |
| POST   | `/re-auth`    | `{ show_browser }` | Switch account / fresh login (e.g. after daily quota)         |
| POST   | `/de-auth`    | —                  | Log out, clear session                                        |

Interactive login is usually better run as the CLI command
`notebooklm-mcp-setup-auth` in a terminal (a stdio client's tool timeout can cut
off the up-to-10-minute login).

## Query (the core)

| Method | Path   | Body                                                    | Purpose                |
| ------ | ------ | ------------------------------------------------------- | ---------------------- |
| POST   | `/ask` | `{ question, notebook_id, source_format, session_id? }` | Citation-backed answer |

- `source_format`: `none` \| `inline` \| `footnotes` \| `json` \| `expanded`.
  Use `json` for machine-readable citations (source names + cited excerpts),
  `expanded` for human-readable footnotes with excerpts.
- Omit `session_id` for a fresh question (fastest, uses the internal RPC path);
  pass a stable `session_id` to continue a multi-turn conversation.

## Notebooks & sources

| Method  | Path                   | Body                                                          | Purpose                                      |
| ------- | ---------------------- | ------------------------------------------------------------- | -------------------------------------------- |
| GET     | `/notebooks`           | —                                                             | List notebooks (id + name)                   |
| POST    | `/notebooks`           | `{ title }`                                                   | Create a notebook                            |
| GET     | `/notebooks/scrape`    | —                                                             | Force a live scrape of the account           |
| POST    | `/content/sources`     | `{ source_type, url\|text\|file_path, title?, notebook_url }` | Add a source (`url`/`text`/`file`/`youtube`) |
| GET/PUT | `/notebooks/:id/share` | `{ public }`                                                  | Read / set public-link status                |

## Content generation

| Method | Path                 | Body                              | Purpose                                                                                   |
| ------ | -------------------- | --------------------------------- | ----------------------------------------------------------------------------------------- |
| POST   | `/content/generate`  | `{ notebook_id, content_type }`   | Studio: `audio` \| `report` \| `video` \| `infographic` \| `presentation` \| `data_table` |
| POST   | `/content/study-aid` | `{ notebook_id, kind, focus? }`   | `kind`: `flashcards` \| `quiz`                                                            |
| POST   | `/content/mind-map`  | `{ notebook_id, title? }`         | Interactive mind map, saved to the notebook                                               |
| POST   | `/content/research`  | `{ notebook_id, query, import? }` | Web/Drive source discovery (fast/deep)                                                    |
| GET    | `/content`           | `?notebook_id=`                   | List generated artifacts                                                                  |
| GET    | `/content/download`  | `?notebook_id=&type=`             | Download audio/video/infographic bytes                                                    |

## Batch → vault (for large research runs)

| Method | Path              | Body                                                                   | Purpose                                                                                                   |
| ------ | ----------------- | ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| POST   | `/batch-to-vault` | `{ questions[], vault_dir, notebook_id, source_format, slug_prefix? }` | Run many questions, write each answer as markdown + JSON sidecar (`nblm-answer-v1`) for offline retrieval |
