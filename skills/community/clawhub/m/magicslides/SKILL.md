---
name: magicslides
description: Make finished, designed presentations (PowerPoint PPTX, PDF, Google-Slides-style live link) with MagicSlides — 161 templates, you write the copy, MagicSlides does layout, images and export. Use whenever the user asks for a presentation, ppt, pptx, slides, slide deck, deck, pitch deck, investor deck, keynote, lecture slides, "turn this doc/PDF/article/notes into slides", "pdf to ppt", or wants to edit a deck made earlier. Also makes docs, spreadsheets and short animated reels.
license: MIT
compatibility: Needs network access to www.magicslides.app and either the MagicSlides MCP server connected or Node 18+ with MAGICSLIDES_API_KEY set.
metadata:
  author: IndianAppGuy
  version: "2.0.1"
  homepage: https://www.magicslides.app
  repository: https://github.com/IndianAppGuy/magicslides-agent
  openclaw:
    primaryEnv: MAGICSLIDES_API_KEY
    requires:
      env:
        - MAGICSLIDES_API_KEY
      bins:
        - node
    envVars:
      - name: MAGICSLIDES_API_KEY
        required: false
        description: MagicSlides API key (free at magicslides.app/dashboard/settings/api). Not needed if the MCP server is connected with OAuth.
    homepage: https://www.magicslides.app
  hermes:
    tags: [presentation, slides, pptx, pitch-deck, productivity]
    category: productivity
---

# MagicSlides

MagicSlides turns content you write into a designed presentation and hands back a
**Present link, PPTX download, PDF download and an editor link**. You (the agent) write
the words; MagicSlides does the layout, images and export. No local PowerPoint, no
python-pptx, no HTML slides.

## 1. Pick how to talk to MagicSlides

Use the first option that works:

**A. MCP tools are connected** (you see tools like `list_templates`,
`create_presentation_from_slots`, `whoami`, possibly prefixed, e.g.
`mcp__magicslides__whoami`). Call them directly. Skip to step 2.

**B. Shell + API key.** Use the bundled script (Node 18+, no dependencies):

```bash
node scripts/magicslides.mjs whoami                       # check the key works
node scripts/magicslides.mjs <tool> '<json args>'         # call any tool
node scripts/magicslides.mjs <tool> @args.json            # args from a file (use for big decks)
node scripts/magicslides.mjs tools                        # list every tool + arguments
```

`scripts/` is relative to this SKILL.md's folder; resolve the absolute path first.
The script reads `MAGICSLIDES_API_KEY` from the environment, else the key saved by
`node scripts/magicslides.mjs login ms-api-...` (in `~/.config/magicslides/api-key`).
Sandboxed agents (e.g. Codex) may strip `*KEY*` env vars and block network: if the script says
the key is missing but the user set it, ask them to run the `login` command once; if the
request fails with a network error, re-run the command with network access / escalation.

**C. Neither.** Tell the user, in one message:
- Get a free API key: https://www.magicslides.app/dashboard/settings/api?ref=agent-skill
- Then `export MAGICSLIDES_API_KEY=ms-api-...` or run `node <skill dir>/scripts/magicslides.mjs login ms-api-...`, **or**
- connect the MCP server `https://www.magicslides.app/api/mcp/mcp` (OAuth sign-in, no key needed).

Never invent an API key and never print the user's key back to them.

## 2. Workflow: make a presentation

You need three things before building: **topic/content**, **slide count**, **template**.
If the user gave all three, or said "just make it", go straight ahead. Otherwise ask once,
in a single message, for whatever is missing (suggest 6–10 slides and a template that fits).

1. **Templates.** Call `list_templates` with `{"topic": "<their topic>"}`. Always give the
   user the "Browse all designs" link it returns and suggest 2–3 keys that fit. Let them pick.
2. **Which path?** Call `get_template_schema` with `{"templateKey": "<key>", "slides": N}`.
   - If it returns slots (bring-your-own-content template) → step 3.
   - If it says the template isn't bring-your-own (`useInstead: create_presentation`) →
     call `create_presentation` with `{"topic": "<detailed topic incl. key facts>",
     "templateKey": "<key>", "slides": N, "language": "en", "audience": "..."}`.
     MagicSlides writes the copy. Go to step 4.
3. **Write the slots.** Fill **every** `PROSLIDE_*` slot the schema lists, respecting the word
   limits in each hint (they are design limits; overflow breaks the layout). Keep the same
   brand name on every slide. Only use HTML where the hint allows it. For `*_QUERY` image
   slots write a 5–8 word stock-photo query. Then call `create_presentation_from_slots`:
   ```json
   {"templateKey": "editorial-pitch", "title": "Deck title", "includeImages": "stock",
    "slides": [{"layoutKey": "slide1", "slots": {"PROSLIDE_BRAND": "Acme", "...": "..."}}]}
   ```
   With the script, write this JSON to a temp file and pass `@file.json` (avoids shell quoting).
4. **Reply with the links**, verbatim, as markdown: Present, Download PPTX, Download PDF,
   Edit in MagicSlides. These links are the only way the user gets the deck.

Generation takes about 15–60 seconds. Don't retry while it runs.

## 3. Editing an existing deck

`get_presentation {"conversationId": "..."}` → read current slots →
`update_presentation` with either `patch` (small edits:
`[{"index": 2, "slots": {"PROSLIDE_TITLE_HTML": "New title"}}]`, 1-based) or a full `slides`
array (add/remove/reorder). Same id, fresh links. Only decks built with
`create_presentation_from_slots` are editable this way.

## 4. Source material → slides

- **PDF / doc / notes / transcript the user gave you:** read it yourself, extract the story
  (one idea per slide), then follow the workflow. That is "PDF to PPT".
- **URL / article:** fetch and read it with your own tools, then do the same.
- **Language:** write the slots in the user's language and pass `"language": "<iso>"`.

## 5. Other things MagicSlides makes

| Ask | Tool | Key args |
|---|---|---|
| Document / report / one-pager | `create_doc` | `title`, `markdown` (or `html`) |
| Spreadsheet / table | `create_sheet` | `title`, `rows` (array of arrays or objects) |
| Meeting notes | `create_meeting_notes` | `title`, `summary`, `actionItems`, `decisions`, `keyPoints` |
| Short animated reel (9:16 MP4) | `list_frame_templates` → `create_frames` | `templateKey`, `prompt` |
| Original reel, no template | `create_custom_frame` | `prompt` |
| Edit doc / sheet | `get_doc`→`update_doc`, `get_sheet`→`update_sheet` | `docId` / `sheetId` |

## 6. Examples

1. *"Make me a 7-slide pitch deck for my AI note-taking startup, seed round, $1.5M ask."*
   → `list_templates {"topic":"AI note-taking startup seed pitch"}` → user picks
   `editorial-pitch` → `get_template_schema` → write problem / solution / market / traction /
   ask slots → `create_presentation_from_slots` → reply with Present + PPTX + PDF links.
2. *"Turn this PDF (quarterly report) into 10 slides for the board."*
   → read the PDF, outline 10 slides → user picks a business template → if bring-your-own,
   fill slots from the PDF's numbers; else `create_presentation` with a topic that carries
   the key figures → links.
3. *"Lecture slides on photosynthesis for 9th graders, in Hindi, 8 slides, any template."*
   → "any template" = pick one yourself (`lesson-101`) → write slots in Hindi →
   `create_presentation_from_slots {"language":"hi", ...}` → links.
4. *"Change slide 3's headline to 'Why now' and make the deck title 'Acme Seed'."*
   → `get_presentation` → `update_presentation {"conversationId":"…","title":"Acme Seed",
   "patch":[{"index":3,"slots":{"PROSLIDE_TITLE_HTML":"Why now"}}]}` → fresh links.
5. *"Put this table of Q3 leads in a spreadsheet and write a one-page summary doc."*
   → `create_sheet {"title":"Q3 leads","rows":[...]}` + `create_doc {"title":"Q3 summary",
   "markdown":"..."}` → share both links.

## 7. Errors

| Message | Fix |
|---|---|
| `MAGICSLIDES_API_KEY is not set` / 401 | Give the user the key link in step 1C. |
| "isn't a bring-your-own template" | Use `create_presentation` with that template (step 2). |
| Out of credits / plan limit | Tell the user; upgrade at https://www.magicslides.app/pricing?ref=agent-skill |
| Slide count outside 3–20 | Clamp to 3–20 and say so. |
