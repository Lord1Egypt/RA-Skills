---
name: lego-moc
description: Recognise loose LEGO parts from photos into a parts inventory, then design a LEGO model (MOC) as an LDraw file - from the parts the user owns, or as a free build with unlimited parts - and have a server verify it physically - it returns fix notes, or a public page with a 3D preview and step-by-step building instructions. Works through MCP tools (scan_photos, inventory, submit_model and others) or a fallback Python script. Use when the user wants to identify, scan or count LEGO pieces from photos, build, show or correct a parts inventory, design or build a MOC from parts they own or as a free build without an inventory (a car, a house, a description, a picture), check, validate or verify a LEGO model or .ldr file, or get building instructions or a 3D preview for it. Chinese triggers - 乐高零件识别, 识别乐高零件, 拍照识别积木, 乐高零件清单, 零件库存, 用我有的零件设计 MOC, 设计乐高作品, 自由创作, 不限零件设计乐高, 检验 MOC, 检查乐高模型能不能拼, 拼装步骤, 搭建说明, 3D 预览.
version: 2.1.0
metadata:
  openclaw:
    emoji: "🧱"
    homepage: https://github.com/garmanwu/lego-moc
    requires:
      anyBins:
        - python3
        - python
    envVars:
      - name: LEGO_PARTS_SERVER
        required: false
        description: Optional. Address of the recognition server, overriding the one built into the script.
      - name: LEGO_PARTS_HOME
        required: false
        description: Optional. Local data folder, default ~/.lego-parts.
---

# LEGO parts recognition and MOC design

Two stages:

1. **Scan.** The user photographs loose parts; the server recognises them and keeps the inventory (per user ID).
2. **Design and verify.** You design a model (MOC) and write it as an LDraw file: by default from that inventory,
   or as a **free build** with any parts when the user asks for one or has no parts scanned (section 4b). The server
   checks it physically: on failure it names the offending lines; on a pass it publishes a page with a 3D view and
   step-by-step building instructions. The server designs nothing: the design is yours.

There are two ways to work. **MCP tools** (section 2) need no shell commands; use them whenever they are available.
**The script** `scripts/lego.py` (section 5) does the same through shell commands and is the fallback.

## 1. Are the MCP tools available?

Look in your tool list for these names, usually shown under a server prefix such as `lego-moc` (for example
`mcp__lego-moc__scan_photos` or `lego-moc.scan_photos`):

`scan_photos`, `scan_status`, `inventory`, `edit_inventory`, `design_guide`, `connectors`, `find_parts`,
`submit_model`, `moc_status`

- **All present:** work as in section 2.
- **All but `scan_photos`:** the host uses the remote server endpoint, which cannot read files on this computer.
  Upload photos with the script (`scan`), do everything else with the tools.
- **None present:** use the script (section 5) for this task; everything works with it. Then offer the user the
  one-time setup below, which removes the per-command approvals.

### One-time setup (the user does it)

1. Run `python3 <this skill folder>/scripts/lego.py mcp-config` (Windows: `python`). It prints a JSON block and
   makes no network call.
2. Give the user that JSON and ask them to add the `lego-moc` entry to the `mcpServers` section of the agent's MCP
   settings (settings page or MCP config file), then restart the agent or reload its MCP servers. Edit the host's
   configuration yourself only if the user asks you to.
3. After the restart the agent starts the bridge itself (`lego.py mcp`, a local stdio MCP server) and the tools
   appear. The same `~/.lego-parts/` folder and user ID are used, so nothing scanned so far is lost.

`lego.py mcp-config --remote` prints the server's own endpoint instead (`type: http`, a URL that contains the user
ID; it creates an ID if none exists). Use it only for hosts that cannot run local commands. It has no
`scan_photos`, and its URL is a credential: never post it anywhere public.

## 2. MCP flow

Every tool result has a text part for you to read and a `structuredContent` object with the fields. An error comes
back as a result with `isError: true` whose text says what happened and what to do next. Do it; don't work around
it with your own HTTP calls.

### Scan

1. **`scan_photos`** `{"paths": [...]}`: absolute paths of photo files, folders or glob patterns on this computer,
   1–30 photos per call (JPEG, PNG, WEBP, HEIC, 25 MB each). It returns at once with one task per photo; it does not
   wait for recognition. Tell the user every entry of `rejected` and `not_uploaded` with its reason. A
   `duplicate_photo` entry means that exact file was uploaded before: it is not recognised again, and `previous`
   is the first upload's result (its parts are in the inventory already). If the host times the call out, the
   upload goes on: call `scan_status` instead of uploading again. With many large photos, use several calls of
   about 8 photos.
2. **`scan_status`** `{"wait_s": 50}`: repeat until `pending` is 0 (recognition takes minutes; the first photo can
   wait for the GPU to start). Relay every entry of `notices` (`pile_photo`, `no_pieces`) to the user verbatim and
   name the failed photos with their `error`. If it stays pending for a long time, tell the user how many photos
   are still being processed instead of looping forever.

### Show and correct the inventory

3. **`inventory`**: shows the inventory with an overview picture (an image in the result) and `inventory_url`.
   Show the user the picture and give them the link; if you have a browser or preview panel, open the link there.
   Never present a table of bare part numbers: most users cannot tell what `3020` is. Point out the low-confidence
   rows (orange frame and `?` in the picture) and ask the user to check them on the page. `designable: false` rows
   have no usable 3D geometry and can never be built with. `pending_tasks > 0` means the inventory is incomplete:
   say so. Use `filter: "usable"` or `"low_confidence"` and `offset`/`limit` for long inventories.
4. **`edit_inventory`** `{"changes": [...]}`, only on the user's word (never to make a design fit):
   `{"op": "set_quantity", "key": "3001|4", "quantity": 3}`, `{"op": "remove", "key": ...}`,
   `{"op": "confirm", "key": ...}` (the user checked a low-confidence row and it is right),
   `{"op": "replace", "key": ..., "ldraw_part": "3002", "ldraw_color": 4}` (it is really another part or colour),
   `{"op": "add", "ldraw_part": "3003", "ldraw_color": 14, "quantity": 2}`, `{"op": "undo", "key": ...}`,
   `{"op": "undo_all"}`. Each change reports `ok`; tell the user which did not apply and why. The user can make the
   same edits on the inventory page.

### Design

5. **Understand the request** (section 3): subject, description, reference picture or nothing; check that the
   inventory can carry it before you design.
6. **`design_guide`**: read the whole guide before your first design in a conversation. It is the server's current
   rule book: file format, coordinates, which connectors mate, the verifier's rules, worked examples and how to use
   many parts. It also returns `usable_quantity`, `target_percent` and `default_mode` (`inventory`, or `free` when
   the user has no usable parts: then design a free build, section 4b).
7. **`connectors`** `{"parts": ["3001", "3023", ...]}` (1–40 LDraw part numbers per call): the bounds and every
   connector of each part you plan to use. Take every part's origin and connector positions from here; never guess
   them. A part reported as `unsupported` cannot be used.
8. Write the model: a `0 <title>` line, then one line `1 <colour> x y z a b c d e f g h i <part>.dat` per part, with
   `<colour>` = `ldraw_color` and `<part>` = `ldraw_part` from the inventory. Only usable rows, and per `key` at most
   its `quantity` across the whole model; count before you submit. No sub-models, no `0 STEP` lines.

### Verify and improve

9. **`submit_model`** `{"ldr": "<the whole file>", "title": "...", "brief": "<the user's request, their words>"}`;
   add `"moc_id"` to submit a new version of the same model, `"design"` only for declared moving parts (see the
   guide), and `"mode": "free"` for a free build (section 4b). It waits up to `wait_s` (default 45) and returns `status`, the `issues` (each fail names the rule, a hint,
   and the parts with their file line and position), `usage`, `resubmissions_left` and, on a pass, `url` and two
   preview pictures. If `status` is not final yet (`queued`, `checking`, `stepping`), call **`moc_status`**
   `{"moc_id": ..., "wait_s": 50}`. Status `error` is a server-side failure, not a design problem: submit the same
   model again with its `moc_id`.
10. **Failed:** fix exactly the named lines (recompute positions from `connectors`, don't nudge numbers) and submit
    again with the `moc_id`.
11. **Passed:** look at both previews and at `usage`, then decide whether another round is worth it (section 4).
    The public page always shows the latest version that passed, so a failed later round does not take it down.
12. **Report:** give the user the page `url` (say that it is public), the part and step counts, every warning, what
    you built and what you could not do. Passing means the model is physically consistent in the verifier's
    simulation, not that the real build is guaranteed to hold: say so.

## 3. Design requests

The user may give a subject ("a car"), a detailed description, a reference picture, or nothing at all.

- **Check feasibility first.** Look at the inventory (shapes, colours, quantities) before promising anything. A car
  needs wheels and axles or something that can stand in for them; a house needs enough bricks for walls and parts
  for a roof. Tell the user plainly what can and cannot be met, and propose alternatives that the parts do allow
  (a smaller version, another subject, a stylised one) instead of forcing it.
- **Description:** keep the features the user named; say which ones you had to drop or change and why.
- **Reference picture** (only if you can see images): build a model in its spirit (its shape, proportions and main
  colours) from the parts the user owns. It will not be a replica; say so.
- **Nothing given:** pick a subject that suits the inventory (its main colours and the shapes it has most of) and
  say what you chose.
- Pass the user's request text, in their words, as `brief`. Put the subject in the title.
- **Thin inventory.** If there are fewer than about 60 usable pieces, or the inventory is mostly single pieces in
  many colours, tell the user before designing: only a small or abstract model is possible. Suggest confirming
  low-confidence rows (after checking them on the inventory page) and photographing more parts spread out. A new
  photo of parts that were already counted counts them again: suggest photographing parts not scanned yet, or
  correcting the quantities afterwards with `set_quantity`.

## 4. Design first, then use many parts

The user wants a model that looks striking. Using many parts is a means to that (more size, more detail, more
presence) and never the goal. A pyramid, tower, wall or block of mixed-colour bricks that merely uses up the
inventory is a failure, however high its `usage.percent`. A smaller model with an idea and a clean colour scheme
beats it every time.

- **Concept before parts.** Decide what the model is and what makes it recognisable (its silhouette and two or
  three signature features) before you place anything. If you cannot name the subject in a few words and say what
  a viewer notices first, you have no design yet. Generic stacked shapes (pyramid, tower, cube, plain wall) are not
  a concept unless the user asked for exactly that.
- **Colour plan before parts.** Count the usable pieces per colour. Pick one dominant colour, one secondary and one
  accent from the colours the inventory has most of, and give each a region (for example walls, roof, trim). Parts
  in other colours go only where they cannot be seen (inside, underneath, the core of a thick wall) or stay unused.
  Leaving parts out because they would spoil the colours is the right call.
- **Spend extra parts on richness, not bulk.** Good uses: detail (windows, doors, trim lines, texture from plates
  between bricks, slopes and round parts on edges), depth (overhangs, recesses, layered fronts), and a scene around
  the subject (a base, a path, a garden, a fence, small side builds joined to the base). Bad uses: more layers of
  the same thing, filling the inside solid, stacking leftovers on top, widening a shape just to place more bricks.
- **`usage` is a gauge, not a quota.** `usage.percent` shows how much of the usable inventory (designable and not
  low-confidence, or confirmed) the model uses; `usage.unused` lists what is left. A rich model from a good
  inventory often reaches about 60% (`usage.target_percent`); below that, ask whether the subject could carry more
  detail or a scene. If the colour plan and the subject only allow 30%, stop at 30%.
- **Stage the work.** Version 1: the main structure in the planned colours (base, body, the big shapes). Later
  versions add a whole layer of detail at once. Only 5 resubmissions exist per model, so each round must add a lot;
  don't spend one on a single part.
- **Review every pass like a designer.** Look at both previews and ask: is the subject recognisable at a glance?
  Does the colour plan hold, or is it speckled? Does every part you added have a reason? Is the top finished rather
  than bare studs? Is it symmetric where the subject is? Remove or replace what fails these, even if usage drops.
- **Tell the user** the idea, the colours you chose, the final usage, and what you left out and why (for example
  "the 14 orange and lime pieces would have clashed"). If more parts of some colour or shape would lift the model,
  say which, so they know what to scan next.

## 4b. Free build (unlimited parts)

By default a model is designed from the user's inventory, so that they can build it from what they own. A **free
build** drops that limit: any LDraw part the verifier supports, in any colour and quantity. The physics check is the
same, and so are the page, the previews and the building steps.

- **When.** The user asks for it ("free build", "unlimited parts", "don't limit it to my parts", "自由创作",
  "不限零件", "无限零件"), or the user has no usable parts (`design_guide` returns `default_mode: "free"`). If the user
  has parts and did not ask, stay in inventory mode. When the inventory is too thin for the request, don't switch
  on your own: say what the inventory allows and offer a free build as the alternative.
- **How.** Skip the inventory. Read `design_guide` (section 10 is about free builds). Look part numbers up by name
  with **`find_parts`** `{"query": "slope 45 2 x 2"}`, get their sheets with `connectors`, and submit with
  `"mode": "free"`. Later versions of the model keep the mode. There is no `usage` in the result. Limits that
  stay: 10 to 400 parts, and only supported parts (a part `find_parts` does not find cannot be used).
- **Design for effect.** Nothing holds the design back now, so make it the best you can: pick the right part for
  every place (slopes, curved slopes, tiles, arches, windows, wheels, transparent parts), a disciplined palette
  (dominant, secondary, accent, plus neutrals), real proportions, detail, depth and a scene. A showpiece usually
  needs 150 to 400 parts. Everything in section 4 about concept, colour plan, staging and reviewing the previews
  applies; padding is as wrong here as there.
- **Tell the user** that this is a free build, not limited to their parts; that the parts list on the page is what
  they would need to get; and that the verifier does not know which part exists in which colour as a real LEGO
  element, so some may not be obtainable in that colour.

## 5. Script fallback

Use the script when the MCP tools are not available. Python 3.8+, standard library only, nothing to install.

```
python3 <this skill folder>/scripts/lego.py <command> [options] [arguments]
```

On Windows use `python` or `py -3`. Put options before the photo list.

**Keep the user's approvals few.** Many agents ask the user to approve each new shell command, network host and
write outside the workspace. So:
- Always call the script in exactly this form, as one plain command: no `cd`, no pipes, no `&&`, no environment
  prefix, no wrapper script. Then the user can approve "always allow" once for `python3 <path>/lego.py`. Tell the
  user this the first time an approval appears, and mention the MCP setup (section 1), which avoids them.
- The script needs three things, all of which the user can allow once: run `lego.py`, reach the server host shown by
  `lego.py whoami`, and read/write `~/.lego-parts/`.
- Don't run the same step twice, don't poll in a loop of short commands (use `--wait`), and don't call the server
  with curl or code of your own.
- Write `model.ldr` with your file-writing tool in as few steps as you can; avoid a series of throw-away scripts.

| Command | What it does |
|---|---|
| `scan [--no-wait] [--wait SECONDS] [--images] PHOTO...` | Uploads 1–30 photos (files, folders or glob patterns), waits up to 480 s (default) for the results and saves them. `--no-wait` returns right after uploading. |
| `status [--wait SECONDS] [--images] [TASK_ID...]` | Checks the pending tasks (or the given ones) once, or keeps polling up to SECONDS. Saves finished ones. |
| `parts [--images]` | Saves finished pending tasks, then reloads the whole inventory (with the edits made on the inventory page or with `edit_inventory`) into `parts.json`. |
| `whoami` | Shows the user ID, server and local folder. No network. |
| `moc guide [--parts-file PATH \| --parts 3001,3020,...]` | Saves the design guide `moc/DESIGN_GUIDE.md` and the connector sheets of your parts `moc/connectors.txt`. `--parts` fetches the sheets of the named parts instead (free build; no inventory needed). |
| `moc find WORD...` | Free build: lists supported part numbers whose LDraw name has every word (e.g. `moc find slope 45 2 x 2`). |
| `moc submit [--title NAME] [--brief TEXT] [--design design.json] [--moc MOC_ID] [--mode inventory\|free] [--parts-file PATH] [--no-wait] [--wait SECONDS] MODEL.ldr` | Sends the model with `parts.json` (`--mode free`: a free build, no inventory sent or checked), waits up to 300 s (default) for the check and prints the result, the parts usage and, on a pass, the preview links. `--moc` submits a new version of an existing MOC; `--brief` is the user's request. |
| `moc status [--wait SECONDS] [MOC_ID]` | Checks the pending MOC submissions (or the given one) once, or keeps polling up to SECONDS. |
| `mcp-config [--remote]` | Prints the JSON for the MCP setup (section 1). Output is only that JSON; no RESULT line. |
| `mcp` | The MCP bridge itself. The agent host runs it; don't run it yourself. |

`--images` also downloads each inventory row's LDraw picture and photo crop into `images/`.

- **Long waits.** `scan` can run for 8 minutes, `moc submit` for 5. If your shell tool times out sooner, raise its
  timeout or pass a smaller `--wait` (e.g. `--wait 100`) and continue with `status --wait 100` /
  `moc status --wait 100`. Being stopped mid-wait is safe: IDs are saved in `pending.json` / `moc/pending.json`
  first, and any later command, from any agent, collects them.
- **Server address.** Built into the downloaded script. If a command says no server is configured, the user must set
  `LEGO_PARTS_SERVER` (e.g. `https://lego.groundrl.com`, without `/skill/v1`). `LEGO_PARTS_HOME` changes the local
  folder.
- **Blocked network.** If a command reports `HTTP 403 ... not from the LEGO server` or cannot reach the server, a
  sandbox, proxy or firewall is blocking it. Ask the user to allow network access to the server's host, then run the
  same command again. New IDs are limited to 5 per network per day, and results are only saved when the script runs.

### Exit codes and RESULT

| Exit | Meaning |
|---|---|
| 0 | Scan: every task finished (done or failed), `parts.json` is current. MOC: the model **passed** the check |
| 4 | MOC: the model did not pass; the fix notes are printed |
| 3 | Still running (tasks, or a MOC check) |
| 1 | Error: read the `ERROR:` lines. For a MOC this includes status `error` (a server-side failure) |
| 2 | Usage error: bad arguments, more than 30 photos, a missing or unusable file named on the command line |

The last output line is always `RESULT {...}`, one line of JSON (except `mcp` and `mcp-config`). Parse it instead
of the text above it. Scan fields: `exit_code`, `user_id`, `done`, `failed`, `pending`, `pending_task_ids`,
`rejected` and `not_uploaded` (files not accepted, with reasons; `duplicate_photo` entries carry `task_id` and
`previous`), `notices`, `task_errors`, `errors`, `parts_file`, `tasks_dir`, `total_quantity`, `distinct_parts`,
`inventory_url`, `inventory_image`. MOC fields: `moc_id`, `version`, `status` (`queued`, `checking`, `stepping`,
`passed`, `failed`, `error`; null when nothing was checked), `url`, `fails` and `warnings` (counts), `report_file`,
`result_file`, `model_file`, `parts`, `steps`, `title`, `usage` (`used`, `usable`, `percent`, `target_percent`),
`previews`, `mode` (`inventory` or `free`), `errors`; `moc guide` adds `guide_file`, `connectors_file`, `unsupported_parts`.

### Scanning with the script

1. **Exit 3** means tasks are still running: run `lego.py status --wait 300` until it exits 0 before you read
   `parts.json`; the same whenever `RESULT` has `pending > 0`.
2. If `parts.json` has `local_pending_tasks > 0` or `pending_tasks > 0`, the inventory is incomplete: say so.
3. Relay `notices`, `task_errors`, `rejected` and `not_uploaded` as section 6 says.
4. **Show pictures:** show `inventory_image` (`~/.lego-parts/inventory.png`, refreshed with `parts.json`) the way
   you show any local image, and always give the link `inventory_url`.
5. **Corrections** belong on the server: the user makes them on the inventory page (or you, on their word, with
   `edit_inventory`), then `lego.py parts` brings them into `parts.json`. A hand edit of `parts.json` affects only
   what `moc submit` sends and is overwritten by `parts`, and by `scan` / `status` when they collect new results
   (the previous copy is kept as `parts.json.bak`); warn the user before running those.

### Designing with the script

1. `lego.py moc guide` (needs `parts.json`: scan first; run it again after the inventory changes), then read
   `moc/DESIGN_GUIDE.md` in full and take every origin and connector position from `moc/connectors.txt`.
2. Write `model.ldr` as in step 8 of section 2, using `parts.json`. A `parts.json` the user supplies by hand may
   contain only `items` (`ldraw_part`, `ldraw_color`, `quantity`, optionally `designable`, `low_confidence`): treat
   missing `designable` as true and missing `low_confidence` as false.
3. `lego.py moc submit model.ldr --title "..." --brief "..."` (add `--design design.json` only for declared moving
   parts). Pass the same `--parts-file` to `guide` and `submit` if you don't use the default `parts.json`.
   `moc submit` needs a user ID and creates one if `user.json` does not exist yet: tell the user when it does.
4. **Exit 4:** each `FAIL` block gives the rule, the reason, a hint and the parts as
   `line <n>: <part> colour <c> at (x, y, z)`; line numbers count every line of the submitted file from 1 (copy in
   `moc/<moc_id>/v<N>.ldr`, all parts in `report_file`). Fix those lines and submit a new version:
   `lego.py moc submit model.ldr --moc <moc_id>`.
   **Free build** (section 4b): `lego.py moc find <words>` to look up part numbers, `lego.py moc guide --parts
   3001,3020,...` for their sheets (it rewrites `moc/connectors.txt`: name every part you use), then
   `lego.py moc submit model.ldr --mode free ...`.
5. **Exit 0:** passed. Read the `Parts used` line and the preview links, then refine as section 4 says, with
   `--moc <moc_id>`. **Exit 3:** `lego.py moc status <moc_id> --wait 300`. **Exit 1** with `status: "error"`: a
   server-side failure; submit the same file again with `--moc`. Any other exit 1: report the `ERROR:` line (e.g.
   the daily submission limit, a full queue).

## 6. Rules

- **Relay every notice verbatim**, in the user's language: translate the full message faithfully; don't drop or
  soften it. The same for failed photos, rejected and not uploaded files (with reasons) and every verifier warning.
- **Pictures, not part numbers.** When you present the inventory, show the overview picture and give
  `inventory_url`.
- **Inventory mode is the default.** A free build only when the user asks for one or has no usable parts; say
  clearly in your report which mode the model is in.
- **Low-confidence rows** may be misidentified: build with them only after the user confirmed them (MCP:
  `edit_inventory` `confirm`; the user can also confirm on the inventory page). Never use `designable: false` rows.
- **Edits only on the user's word.**
- **Never claim a model is buildable, valid or verified unless its status is `passed`.** A status call that checked
  nothing (`status: null`) proves nothing.
- **The model page link is public:** anyone with the URL can view it. Tell the user when you give it.
- **Passing is not a real-world guarantee**: it means physically consistent in the verifier's simulation.
- **At most 5 resubmissions per model.** If it still fails, stop and tell the user honestly which rules still fail
  and on which parts.
- **The user ID is a credential.** Anyone with it, or with a link that contains it (`inventory_url`, the works page,
  the `--remote` MCP URL), can read the inventory and add to it. Give those to the user only; never post them
  anywhere public. Never delete or replace `~/.lego-parts/user.json`: the inventory and models belong to that ID. If
  the server does not recognise the ID, tell the user; don't create a new one.
- **Duplicate photos** are refused and not recognised again (`duplicate_photo`). Re-photographing parts that were
  already scanned counts them twice.
- **Photo advice:** parts spread out on a plain surface, not touching, shot from straight above in good light; piled
  parts are recognised poorly (`pile_photo`).
- **Be honest about the design.** The verifier checks physics only, never whether the model looks like its subject.
  Say what you built; if you could not see the previews, say that you have not seen the result.
- **No verification, no claim.** If neither the tools nor the script can reach the server, you may still write an
  `.ldr` from the guide, but tell the user plainly that it was not verified and has no building instructions.

## 7. Files in `~/.lego-parts/`

Shared by the MCP bridge and the script. With MCP, the inventory and results live on the server; the bridge only
writes `user.json` and `pending.json`.

| File | Content |
|---|---|
| `user.json` | `{"user_id", "server", "created_at"}`: the user's ID |
| `pending.json` | `{"task_ids": [...]}`: uploaded, result not collected by the script yet |
| `tasks/<task_id>.json` | One photo's full result (`status`, `notice`, `error`, `pieces[]` with `score`, `accepted`, `low_confidence`, `key`, `ldraw_part`, `ldraw_color`, `name`, `designable`, `crop_url`, `ldraw_image_url`, `bbox`, `candidates`) |
| `parts.json`, `parts.json.bak` | The inventory as last fetched by the script, and the copy before |
| `inventory.png` | The overview picture, refreshed with `parts.json` |
| `images/ldraw/<part>_<colour>.png`, `images/crops/<task>_<nnn>.jpg` | Downloaded with `--images` |
| `moc/DESIGN_GUIDE.md`, `moc/connectors.txt` | Written by `moc guide` |
| `moc/pending.json` | `{"moc_ids": [...]}`: submitted with the script, result not collected yet |
| `moc/<moc_id>/v<N>.ldr`, `report.v<N>.json`, `result.json` | The file submitted as version N, the server's answer for it, and the latest answer fetched |

`parts.json` rows (`items[]`): `key` (`<ldraw_part>|<ldraw_color>`; a half that could not be converted reads
`bl:<BrickLink id>` and the matching `ldraw_*` field is null), `ldraw_part`, `ldraw_color`, `color_name`,
`color_hex`, `bricklink_id`, `name`, `quantity`, `designable`, `min_score`, `low_confidence`, `ldraw_image_url`,
`crop_url`, `piece_ids`; since v2.0 also `scanned_quantity`, `edited`, `confirmed`, `category`; after `--images`
`local_ldraw_image` and `local_crop` (null when a download failed; never sent with a model). Top level:
`user_id`, `updated_at`, `pending_tasks`, `total_quantity`, `inventory_url`, `fetched_at`, `local_pending_tasks`.
Only pieces the server is fairly sure of are counted (score at least 0.60 and a clean cut-out; at least 0.80 in a
photo flagged `pile_photo`); rows come designable first, then by quantity.
