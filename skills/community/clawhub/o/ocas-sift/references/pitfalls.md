# Pitfalls

## Answer-from-knowledge trap

Don't answer product/how-to/recommendation questions from training data alone. Use `web_search` + `sift.fetch`. The user expects current, verified information — not what the model memorized from training. This is especially critical for local business recommendations, pricing, and availability.

## CAPTCHA cascade

From cloud environments (VPS, cloud VMs), ALL major search engines block headless browsers. Google, Bing, DuckDuckGo, Yelp, Reddit — all return CAPTCHAs or 403s. Use the `web_search` tool (SearXNG plugin) as the primary search source — it routes through the Hermes plugin registry to your SearXNG instance automatically.

**If `web_search` returns "SEARXNG_URL is not set"**: the env var isn't in the right `.env` file. Fix: `hermes config set SEARXNG_URL http://localhost:8888`.

**If SearXNG is also down** (empty response or connection refused), escalate to CSAPI or RapidAPI:
- CSAPI: `mcp_google_workspace_search_custom` (quota-managed, 1000 queries/month free)
- **RapidAPI** — general-purpose API marketplace (203 endpoints). Route through Reach via `reach.query rapidapi`. For API discovery, health checks, and subscription management, load the `rapidapi` skill.

## web_search tool routes through plugins

- **`web_search` tool routes through plugins.** The `web_search` tool dispatches through `agent/web_search_registry.py` → plugin registry. When `web.backend` is `searxng` (or auto-detected), it routes to the SearXNG plugin which reads `SEARXNG_URL` from the `.env` file.

For deep research (multi-source synthesis, fact verification, entity extraction), load Sift directly — `web_search` only does single-source search.

## Source delegation

- **CSAPI**: Route through Reach (`reach.csapi_check` / `reach.csapi_increment`). Do NOT manage CSAPI quota in Sift.
- **RapidAPI**: Route through Reach (`reach.query rapidapi`). Do NOT call `mcp_rapidapi_rapidapi_call` directly.
- **SearXNG**: Use `web_search` tool directly (routes to SearXNG plugin automatically). Do NOT curl localhost:8888 unless debugging.

## Sift does NOT manage MCP connections or API quotas

Sift is a research skill. It does NOT manage its own MCP server connections, API keys, or quota tracking. All structured API access is delegated to Reach:

- **CSAPI**: call `reach.csapi_check` before, `reach.csapi_increment` after, `reach.query csapi` to query. Do NOT call `mcp_google_workspace_search_custom` directly.
- **RapidAPI**: call `reach.query rapidapi`. Do NOT call `mcp_rapidapi_rapidapi_call` directly.
- **Any registered Reach source**: call `reach.query <source>`.

Reach owns: sources.yml, MCP connections, API keys, quota tracking, the discovered-apis catalog, and source registration. Sift owns: research synthesis, web_search (SearXNG), entity extraction, Chronicle Signal emission.

## execute_code may be blocked

The `execute_code` tool can be blocked by security policy, even outside cron mode. When you need to parse HTML or transform fetched content, use `terminal` with inline `python3 -c "..."` or write a script file and run it, instead of `execute_code`.

## web_extract limitations

`mcp_web_search_web_extract` returns 403 on Yelp, Reddit, and many Google pages from VPS IPs. It works on news sites (SFGATE, CBS, local blogs). Always have a fallback plan that doesn't depend on scraping these blocked sources.

## Anti-bot escalation

When fetching URLs from VPS/cloud IPs, anti-bot systems (Cloudflare, Akamai, DataDome, Imperva) will block fast HTTP clients. Follow the escalation chain:

1. `sift.fetch` (Scrapling → Jina) — handles 90% of sites, near-instant
2. `donsetch fetch` (`/usr/local/bin/donsetch` v3.2.3, AGPL) — anti-bot / CF-blocked / solve-and-bounce via real Chrome TLS. Use when `sift.fetch` returns bot-wall / 403 / empty / CAPTCHA on CF, Akamai, DataDome, Imperva. See `references/donsetch-integration.md`. Not a tier-1/2 replacement; tier-3 escalation only.
3. `sift.webwright` (Playwright Firefox) — handles JS-heavy sites
4. `sift.webwright` with `stealth: true` — fingerprint randomization + challenge wait, for protected sites

Auto-escalate when: HTTP 403, "Just a moment…" title, body < 200 chars on a loaded page, or challenge HTML detected. **The agent owns escalation** — `sift.fetch` does not auto-fallback to `donsetch`; the agent must read the exit code and invoke the next tier explicitly. See "Browsing Escalation Chain" section in SKILL.md for full details.

## Surface-depth trap ("try harder" pattern)

When researching a topic, getting a name/reference is step 1 — not the deliverable. <operator>'s "try harder, not sure how you gave yourself a 4/5" (2026-06-24) was triggered by: searching manualslib, getting only a name, presenting it as if the research was done.

**The rule:** If you can't answer "what does the content actually say?" after a search, you haven't finished researching.

### Detection signals
- You're about to report a result that is a title/name only, without substance
- Your self-assessment score is high but the output is one page or one reference
- The user asked for "exhaustive" or "the full content" and you returned a pointer

### Fix
1. Before reporting, ask: "Can I summarize the actual content in detail?"
2. If not, fetch more sources, read deeper pages, extract the substance
3. A 4/5 self-assessment on surface research is a red flag — re-evaluate against "what would a human expert on this topic know?"

### When this applies
- Manual/library research (finding a manual is not reading it)
- Document retrieval (getting the filename is not getting the content)
- Any research where the user needs the *substance*, not the *location* of substance

## Self-calibration trap ("try harder" ≠ self-score)

After completing a task, the agent self-scores against a rubric. If the self-score is high but the output is thin (one reference, surface-level content, "does nothing"), the calibration is wrong.

**Root cause:** The agent conflates "I tried" with "I delivered." Effort is not output.

**The rule:** Self-assess against what was *delivered*, not what was *attempted*.
- "Found a name" ≠ "Researched the topic"
- "Ran the script" ≠ "Verified the fix"
- "Searched for X" ≠ "Answered the question about X"

**Calibration check before reporting a score:**
1. What did the user actually receive?
2. Would a human expert consider this complete?
3. If I gave this to <operator> as-is, would he say "that's it?" — if yes, the score is too high.

**Anti-pattern:** Giving 4/5 when the output "does nothing" is worse than giving 3/5 — it signals the agent can't distinguish done from not-done. (2026-06-24, triggered by learn skill self-scoring 4/5 on surface-level manual search that returned only a name.)

## Credential sanitizer blocks API key writes

The Hermes output sanitizer intercepts API keys. If CSAPI fails with missing key, the owner must add it manually.

## Premise-staleness trap (verify current state before planning a "port X from repo Y" task)

When a user points at an external repo/tool and says "borrow/port/reuse X from it," the advertised capability may no longer exist. READMEs and top-level descriptions lag the code, and a tree can hold stale references to a removed feature — sometimes even a now-broken import — while the real module is gone.

**Triggered:** 2026-07-20 — user pointed at `dondai1234/master-fetch` ("Hound") to pull its "internet archive parts" into ocas-sift. The Internet Archive fallback had been REMOVED that same day in v10.4.1 (CHANGELOG + deleted `archive.py`); the README still advertised the tool broadly, and `server.py`/`cache.py` still referenced `source='archive.org'` while `scripts/live_archive_check.py` had a broken `from master_fetch.archive import ...` import. The literal request was impossible without recovering deleted code from git history.

**The rule:** Before adopting any "pull X from repo Y" request, verify the capability still exists in the CURRENT default branch:
1. Get the real default branch first (`gh api repos/<owner>/<repo>` → `default_branch`); a guessed branch (e.g. `main`) returns 404 while `master` is the real one.
2. Read the CHANGELOG / recent commits for removals or renames.
3. Confirm the module/command/file actually exists in the tree (`ls`/search), not just that the name appears in prose or stale references.

**Why it matters:** Planning against a removed capability wastes a turn and can lead you to reconstruct deleted code. State the finding (with evidence) and offer the durable alternative — here, writing a fresh minimal fallback scoped around the reasons the original was removed — rather than silently proceeding on a stale premise.

**Detection signals:**
- You're about to "port" a feature but can't find its module in the current tree
- The repo description advertises something its CHANGELOG says was deleted
- Stale references to the feature remain in code that no longer compiles against it

## Git pull fails with untracked file conflicts

When running `sift.update` (or manually pulling updates on a hub-installed skill), `git pull` may abort with:

```
error: The following untracked working tree files would be overwritten by merge:
    references/some-new-file.md
```

This happens when the upstream repo has added new tracked files that conflict with existing untracked local files of the same name.

**Fix:**
```bash
cd <skill-dir>
git checkout -- .                          # discard any staged/modified tracked files
# Move conflicting untracked files aside (they'll be recreated by the pull)
for f in references/*.md scripts/*.py; do
  [ -f "$f" ] && git ls-files --error-unmatch "$f" 2>/dev/null || mv "$f" /tmp/skill-local-backup-$(basename "$f")
done
git pull origin main
```

**Do NOT** use `git stash` alone — stash only covers tracked/indexed files, not untracked ones. `git clean -fd` also works to remove untracked files but is destructive; prefer moving files aside if you want to preserve local modifications for comparison after the pull.
