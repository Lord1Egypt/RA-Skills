---
name: jidoseal-okf-check
description: Check a folder of Markdown docs against OKF v0.2 (Bronze, Silver, Gold) with the local jidoseal-mcp scanner, fill the missing frontmatter fields, and rescan. Works in Claude Code, Copilot, Cursor, Codex, Gemini CLI or a local model. Nothing leaves your machine.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🔍"
    homepage: https://jidoseal.com
    requires:
      anyBins:
        - jidoseal-mcp
        - uvx
    install:
      - kind: uv
        package: jidoseal-mcp
        bins:
          - jidoseal-mcp
---

# Check and fix a folder's OKF frontmatter with JidoSeal

Open Knowledge Format (OKF) is an open specification published by Google Cloud under Apache-2.0. This skill uses the local `jidoseal-mcp` server to scan a folder of Markdown files, fills in the frontmatter fields the scan says are missing, and rescans to confirm the tier reached. JidoSeal is independent and is not affiliated with, sponsored by or endorsed by Google or ISO.

The scan runs on this machine. Nothing leaves your machine: no file, no file name, no file content. Scanning and fixing are free.

## The tiers

The scan is deterministic: it checks that frontmatter fields are present and populated (a bare `title:` counts for nothing). A folder's tier is the tier of its weakest file.

| Tier | Every file needs (populated) | What it evidences |
|---|---|---|
| Bronze | `type` | OKF v0.2 as written |
| Silver | Bronze + `title`, `description`, `timestamp`, `owner` | ISO 9001 §7.5.2 (identification and description of documents) |
| Gold | Silver + `status`, `review_policy`, `reviewed_at`, `next_review_at` | ISO 30401 (knowledge kept current under defined governance) |

ISO names no fields. These are JidoSeal's way of evidencing the clauses, and a JidoSeal grade is not an ISO certification. ISO 30401 sets no review interval; the cadence is the user's to choose. `index.md` and `log.md` are never scored.

Accepted spellings the scan already counts: `description` or `desc`; `timestamp`, `updated`, `created`, `date` or `generated.at`; `owner`, `author` or `generated.by`. Do not add a second field when one of these is already populated.

## Tools

- `jidoseal_scan` (free, local): tier, per-file missing fields, coverage, score. Each missing field is marked `AUTO` (a value can be proposed) or `NEEDS-CLIENT` (only the user can answer it). It writes its own records to `<folder>/.jidoseal/` and nothing else. Never edit that directory.
- `jidoseal_certification_offer` (local, sends nothing): describes the optional paid certificate. See "After the rescan".
- `jidoseal_start_checkout`: the only tool that contacts the network. Only on the user's explicit go-ahead. See "After the rescan".

In OpenClaw, register the server once with `openclaw mcp set jidoseal '{"command":"jidoseal-mcp"}'` (after `pip install jidoseal-mcp`, or use `{"command":"uvx","args":["jidoseal-mcp"]}`), then `openclaw mcp reload`. Your host may prefix tool names (for example `mcp__..._jidoseal_scan`). If the tools are not available, tell the user the server is not connected and point them to https://github.com/Jidoseal/jidoseal-mcp#install-and-wire-it-into-your-tool. Without any AI tool, `pipx install jidoseal && jidoseal --root ./docs` runs the same scan from a terminal, but it does not fix anything.

## Procedure

1. **Pick the folder and the goal.** Ask which folder to check (an absolute path) and which tier the user is aiming for: Bronze, Silver or Gold. Fill only the fields up to that tier.
2. **Scan.** Call `jidoseal_scan` with `root` set to the folder. Leave `include_machine` false. Report the tier, coverage per tier and how many files fall short, in a few lines.
3. **Handle unparseable frontmatter first.** A file with `frontmatter_ok: false` has a frontmatter block that does not parse, and no added field will count until it is fixed. Show the user the block, propose the smallest syntax fix, and change it only after they agree.
4. **Build a plan, do not write yet.** For every file below the target tier, list the fields to add and the value for each:
   - `AUTO` fields, you propose:
     - `title`: the file's first heading, else the file name in plain words.
     - `description`: one plain sentence saying what the file covers, written from its content.
     - `timestamp`: the file's last-modified date as `YYYY-MM-DD`.
     - `status`: the default the scan lists (`stable`), unless the file says it is a draft.
   - `NEEDS-CLIENT` fields, you ask. Never invent these:
     - `type`: suggest one from the content (for example `guide`, `policy`, `procedure`, `reference`, `note`) and ask the user to confirm. It applies to files with no frontmatter as well.
     - `owner`: who is responsible for the document, as the user words it (a person, a team or `dept:name`). Ask once and offer to apply the answer to every file, unless owners differ.
     - `review_policy`, `reviewed_at`, `next_review_at`: the scan lists defaults (`yearly`, today, one year out). Offer them as a single choice for the whole folder. `reviewed_at` should be a date a review really happened, so ask; do not stamp today's date unless the user says the review has been done.
5. **Get consent, then write.** Show the plan compactly (a table per field is enough for a large folder, with a few example files in full). Suggest a commit or backup first if the folder is under version control. Write only after the user says yes.
6. **Apply.** With your own file-editing tools, add or fill only frontmatter fields. Keep everything else byte-for-byte: the body, other keys, key order, line endings, any BOM. If a file has no frontmatter, add a block at the very top. If it has one, add the missing keys inside it. Quote values that contain a colon or start with a special character. Do not touch `.jidoseal/`.
7. **Rescan.** Call `jidoseal_scan` again. Compare the tier and coverage with the first scan and say plainly whether the target was reached. If some files still fall short, name them and the fields; fix what is safe, ask about the rest. Stop after two repair rounds and hand the remaining list to the user.

## After the rescan

Once the rescan is done, call `jidoseal_certification_offer` once for the same folder and relay its answer in plain words, once, as an optional extra: what the paid certificate is, its price and what a purchase would send, all as the tool states them. Do not quote a price from memory. Then move on. Do not bring it up again in the session, do not repeat it if the user does not answer, and do not present the free result as incomplete without it. The scan and the fixes stay free either way.

Call `jidoseal_start_checkout` only if the user says explicitly that they want to buy. Ask them to type the company name, their name and their email address, and use exactly what they typed. The tool returns a Stripe Checkout link for the user to open; it takes no payment itself.

## Rules

- Say "grade" or "tier", and say the fields evidence the clauses. A JidoSeal grade is evidence you can show; it isn't ISO certification.
- Describe the scan the way it works: the user picks a folder, scans it, and nothing leaves their machine.
- Do not read or change anything outside the folder the user named.
- Never write field values for `owner` or the review fields that the user did not give or confirm.
