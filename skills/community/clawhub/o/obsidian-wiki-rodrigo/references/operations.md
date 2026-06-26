# Wiki Operations

## Ingest (add source)

When Rodion says "add to wiki" or shares a link/article:

1. Read source
2. Create pages in `wiki/`:
   - `summaries/` — topic summary
   - `entities/` — people, companies
   - `concepts/` — ideas, terms
3. Update `index.md` (catalog)
4. Append to `log.md`:
   ```
   ## [YYYY-MM-DD] ingest | Source name
   - Created: wiki/summaries/..., wiki/entities/...
   ```
5. Run sync

## Query (ask about wiki)

When Rodion asks "what do I know about X":

1. Read `index.md`
2. Find relevant pages
3. Answer from wiki content
4. If answer is valuable — offer to save to wiki

## Lint (health check)

Periodic or on request:

- Find contradictions between pages
- Find orphan pages (no links)
- Suggest missing cross-references
- Update `log.md` with results
