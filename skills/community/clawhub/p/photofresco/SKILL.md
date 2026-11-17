---
name: photofresco
description: Edit photos and images in PhotoFresco, a Photoshop-class editor, through its MCP server - layered editing, retouching, adjustment layers (levels, curves, exposure, hue/saturation, brightness/contrast), masks, selections, crop and resize, filters, previews, undo, and PNG/PSD export into folders the user allows. Use when the user wants an image edited, color-corrected, masked, composited or exported with PhotoFresco, or when photofresco_* tools are available. The user watches every edit in a PhotoFresco window on their computer and approves the connection and each permission.
license: MIT
compatibility: Needs the PhotoFresco MCP server (npm package photofresco, Node.js 22 or newer) and Chrome, Edge or Chromium 120+ installed on the user's computer.
metadata:
  version: "0.1.0"
  homepage: https://photofresco.com/
---

# PhotoFresco

PhotoFresco is a browser-based, Photoshop-class image editor. Its MCP server (`photofresco mcp`)
opens PhotoFresco in its own browser window on the user's computer. You edit through one tool per
editor operation; the user sees every change, and every document edit lands in the editor's History.

Use it for real image editing: layers, non-destructive adjustment layers, masks, selections,
crop/resize, filters, painting/retouching tools, text and shapes, PSD round trips. Every edit runs
on the user's computer, and the user must be present: they approve the connection and choose what
you may do.

## 1. Install the MCP server (once, by the user)

If no `photofresco_*` tools are available, ask the user to add the server. `--read` folders are
where you may open files; `--write` folders are where you may save exports. Without them you can
still create documents, edit and preview, but cannot touch their files.

If `npx` reports that the `photofresco` package is not found (it is published to npm in
mid-October 2026), the user can install the PhotoFresco plugin from
`photofresco/photofresco-agent` instead, or run it from a clone with
`node <clone>/src/bin/photofresco.js` in place of the `npx -y photofresco` part.

Claude Code:

```sh
claude mcp add photofresco -- npx -y photofresco@0.1.0 mcp --read ~/Pictures --write ~/Pictures/PhotoFresco
```

Claude Desktop (`claude_desktop_config.json`), Cursor (`~/.cursor/mcp.json` or `.cursor/mcp.json`)
and other clients that take `command`/`args`:

```json
{
  "mcpServers": {
    "photofresco": {
      "command": "npx",
      "args": ["-y", "photofresco@0.1.0", "mcp", "--read", "/Users/you/Pictures", "--write", "/Users/you/Pictures/PhotoFresco"]
    }
  }
}
```

From a source checkout of the package instead of npm (nothing to install; the MCP SDK is bundled), use
`"command": "node"` with `"args": ["/path/to/photofresco/src/bin/photofresco.js", "mcp", "--read", …]`.

Other options: `--overwrite` (exports may replace existing files in `--write` folders; you must
also pass `overwrite: true`), `--tools essentials|all|<group,…>` (which operations are listed as
tools), `--profile <folder>|ephemeral` (browser profile), `--browser <path>` (or the
`PHOTOFRESCO_BROWSER` environment variable). Starting the server and listing tools opens nothing;
the browser starts only when you call `photofresco_connect`.

## 2. Connect and ask for permissions

1. Call `photofresco_connect` with the permissions you need, a short reason and a short wait
   (`"wait_seconds": 10`). It opens PhotoFresco and returns either state `pairing` with a
   connection `code`, or state `connected` if the user already allowed (then there is no code to
   relay; go to step 3).
2. Tell the user the code and ask them to check that the PhotoFresco window shows the same code
   and click **Allow**. Until the state is `connected`, call `photofresco_connect` again with a
   longer wait (`wait_seconds` up to 170; the request expires after 3 minutes). Never claim you
   approved anything: no tool can answer the user's dialogs.
3. The session starts with **no permissions**. After Allow the user picks them in the
   **Permissions** dialog (pre-filled from your `access` request; they may grant less). If
   `session.grants` is still empty, they have not decided yet: call `photofresco_status` again
   until it lists `grants` (it also shows the pending `request` and any credit `budget`). The tool
   list changes (`tools/list_changed`) as permissions arrive.
4. Ask for more later with `photofresco_request_access`. Ask only for what the task needs:

| Permission | Lets you | Ask when |
|---|---|---|
| `read` (Read) | Document state, previews, histograms | Always |
| `edit` (Edit) | Edit, open files, create and close tabs | Any change |
| `export` (Export) | Exports and files leaving the editor | Saving results (with Read) |
| `external-write` (Send) | Send document data to PhotoFresco services (cloud documents, AI) | Only if the user asked for cloud or AI features |
| `spend` (Spend) | Paid AI up to `budget_credits` | Only if the user asked for paid AI, with a budget they agreed to |

A listed tool is documentation, not permission: the editor checks every call, and a call without
the permission fails with `capability_denied` before anything runs.

## 3. The editing loop

**Orient → change one thing → look → keep or undo.**

1. **Orient.** Call `doc_get_state` (size, layer tree with IDs, active layer, selection bounds,
   `document_id`, `revision`) and `render_preview` to see the image.
2. **Change one thing.** Prefer non-destructive edits: `adjust_add` adds an adjustment layer above
   the active layer and makes it the active layer (it does not mask itself to the selection);
   `mask_add` with `mode: "selection"` masks the active layer to the current selection (`feather`
   on a selection softens its edge across the boundary, so the selection bounds grow past the
   rectangle); `adjust_set_params` changes the active adjustment's settings later;
   `layer_set_props` changes opacity, blend mode and visibility. Coordinates are document pixels
   from the top-left. Pick the adjustment type from `adjust_add`'s `adjustment_type` enum (for
   example `exposure` or `levels` for brightness, `color-balance` or `photo-filter` for warmth);
   parameter names, ranges and their meaning are in the input schema, and arguments outside it are
   refused before anything runs. Curves points: include `{"x": 0, "y": 0}` and
   `{"x": 255, "y": 255}`, because the first and last points are extended flat to the ends, so a
   single point gives a constant output.
3. **Look.** `render_preview` (whole image), `render_region` (a rectangle at detail scale, or one
   layer with `layer_id`) and `render_mask` (a layer mask or the selection, with coverage numbers)
   return PNG images; `doc_sample_color` gives exact pixel values for before/after numbers. Check
   what changed, not just that the call succeeded.
4. **Keep or undo.** `history_undo` reverts the last History entry (selection changes count) and
   names it in its result (`undone`); `history_redo` restores it. Undo also reverts the user's own
   last edit if they made one, so check `doc_get_state` first if they have been editing. For a
   clean before/after, add the adjustment with neutral settings, mask it, then apply the settings
   with `adjust_set_params`: one undo then shows the image without the change.

Every result carries `document_id` and `revision`; the revision increases with every change by anyone.
Operations act on the session's target document only while it is the **active tab**.

Worked example: darken the sky of a 1200×800 photo and save a PNG. Each line is one tool call
with its JSON arguments (after the first `photofresco_connect`, give the user the code and repeat
the call until it returns `connected`, then wait for `grants` as described above).

```mcp
photofresco_connect {"access": {"capabilities": ["read", "edit", "export"], "reason": "Darken the sky and save a PNG"}, "wait_seconds": 10}
photofresco_import_file {"path": "/Users/you/Pictures/beach.png"}
doc_get_state {}
render_preview {"max_size": 512}
selection_rect {"x": 0, "y": 0, "w": 1200, "h": 320, "feather": 24}
adjust_add {"adjustment_type": "brightness-contrast", "params": {"brightness": -40, "contrast": 20}}
mask_add {"mode": "selection"}
render_mask {"source": "layer", "max_size": 256}
render_preview {"max_size": 512}
history_undo {}
render_preview {"max_size": 512}
history_redo {}
selection_none {}
render_region {"x": 560, "y": 280, "width": 80, "height": 80, "scale": 4}
photofresco_export_file {"path": "/Users/you/Pictures/PhotoFresco/beach-sky.png", "format": "png"}
photofresco_disconnect {}
```

`history_undo` here removes the mask, the last edit (its result says `{"undone": "…"}`), so the
next preview shows the whole image darkened; `history_redo` puts the mask back. Selection changes
are History entries too: deselecting before the undo would have made the undo restore the
selection instead.

## 4. Finding operations

The server lists the `essentials` group by default: orient, preview, layers, adjustments, masks,
selections, resize/crop, fill, undo and export (about 40 tools). For anything else (brushes and
retouching, text, shapes, layer styles, filters, paths, actions and workflows), call
`photofresco_list_tool_groups`, then `photofresco_select_tool_groups` with the groups to add
(`document`, `layers`, `selection`, `adjustments`, `painting`, `text`, `automation`, `workspace`,
`cloud`, `other`, or `all`). Read each tool's description: it states the effect, how to undo it and
the permission it needs. Effects that `history_undo` cannot reverse (closing tabs, saved actions,
cloud writes, paid AI, files written) say so.

Full operation reference: the [PhotoFresco agent README](https://github.com/photofresco/photofresco-agent#readme)
(the generated public reference replaces it once published). The live tool list is always
authoritative.

## 5. Workflows

A workflow is a portable, versioned list of operation steps with typed inputs (the same format as
a saved Action). Enable the `automation` group, check one with `workflow_validate` (nothing runs),
run it with `workflow_run`, inspect it with `workflow_runs` and undo a whole run with
`workflow_rollback`. Steps that export, send data, spend or open/close tabs need advance consent
by step ID. Format, bindings and a tested example: [references/workflows.md](references/workflows.md).

## 6. Saving results

- `photofresco_export_file` writes `png` (flattened, or one layer with `layer_id`), `psd` (layered;
  PhotoFresco-only features approximated; the result's `loss` lists what) or `pfd` (native,
  lossless; offer it when the user wants to keep editing in PhotoFresco) into a `--write` folder.
  The file is written only after every byte arrived and its SHA-256 matched; the result's `file`
  gives the written `path`, `bytes` and `sha256` (its `filename` is only the editor's default
  name for the document). An existing file is replaced only with `overwrite: true` and the
  server's `--overwrite` option. Paths outside the granted folders are refused (`path_not_granted`).
- `export_artifact` returns a resource link `photofresco://artifact/<id>`; read it with MCP
  `resources/read` (at most 6 MiB, kept 10 minutes). Use it when you need the bytes yourself.
- Files are opened with `photofresco_import_file` (PNG, JPEG, WebP, GIF, BMP, AVIF, PSD/PSB, `.pfd`;
  at most 32 MiB) from a `--read` folder only. The user can widen folders only in the server
  configuration.

## 7. What the user controls, and safety rules

- **Connection**: the user checks the code and clicks Allow. A new connection always needs a new
  Allow.
- **Permissions**: only the user grants or revokes them, at any time. A revoked permission
  interrupts work that used it; partial edits stay in History.
- **Paid AI** (`ai_generate`, `ai_remove_background`, `ai_split_layers` in the `cloud` group) needs
  Send and Spend plus a credit budget the user sets in the Permissions dialog. Ask only when the
  user wants it, say what it will do, and never ask for more budget to retry without telling them.
  Credits for a request already sent to the AI provider are not refunded.
- **Pause**: if the user edits the document, your edits pause (`lease_paused`) until they press
  **Resume**. Do not work around it; ask them.
- **Stop**: the user's Stop ends the session (`session_stopped`). Reconnect only if they ask.
- **Data**: the previews, document state and exports you request are sent to your model provider
  under its policy. Tell the user before previewing private images if that matters to them. What
  the server runs, sends and fetches is listed in `DISCLOSURE.md` in the photofresco package.
- Never try to change PhotoFresco's privacy settings, answer its dialogs, or edit other tabs.

When finished, call `photofresco_disconnect` (applied edits stay in History; `close_window: true`
also closes the window).

## 8. Errors

Failures are tool errors with a `code`, a `message` and a `hint` naming the next step. Follow the
hint. The most common:

| Code | Do this |
|---|---|
| `not_connected` | Call `photofresco_connect` and give the user the code |
| `capability_denied` | `photofresco_request_access` with the missing permission and a reason |
| `lease_paused` | The user edited; ask them to press Resume, then re-read `doc_get_state` |
| `document_not_active` | Ask the user to switch to the target tab, or `photofresco_attach` the active one |
| `no_target_document` | `photofresco_import_file`, `doc_new` or `photofresco_attach` |
| `stale_revision` | The document changed; re-read `doc_get_state` and plan again |
| `outcome_unknown` | Check `doc_get_state` before retrying; never repeat blindly |
| `path_not_granted` | Use a granted folder (see `photofresco_status` roots) |
| `pairing_denied` | The user declined; do not retry unless they ask |
| `browser_not_found` | Ask the user to install Chrome, Edge or Chromium, or set `--browser` |

Every code and its next step: [references/troubleshooting.md](references/troubleshooting.md).

## 9. Command line (when you have a shell but no MCP tools)

The same `photofresco` program is also a CLI over the same window, permissions and limits (from a
source checkout: `node /path/to/photofresco/src/bin/photofresco.js <command>`). Run
`photofresco --help` or `photofresco <command> --help` for every option; add `--json` to get one
JSON object on stdout, on success and on failure (image data is left out unless `--include-data`).
The example runs the workflow document from [references/workflows.md](references/workflows.md),
saved as `darken-sky.json`, on a granted image:

```sh
photofresco connect --read ~/Pictures --write ~/Pictures/PhotoFresco --reason "Darken the sky" --wait 0 --json
photofresco connect --json
photofresco run darken-sky.json --open ~/Pictures/beach.png --input amount=-30 --export ~/Pictures/PhotoFresco/beach-sky.png
photofresco exec doc.get_state --json
photofresco stop
```

- `connect` starts a background connector, opens the PhotoFresco window and asks for Read, Edit and
  Export unless you pass `--grant <list>` (`--grant none` asks for nothing). With `--wait 0` it
  returns as soon as the connection code is shown: exit code 75 means "still waiting", and the
  JSON carries the connection `code`. Tell the user the code, then run `connect` again until it
  exits 0 (also 75 while they are still in the Permissions dialog). Later commands reuse
  that session until `disconnect` (window stays open) or `stop` (window and connector close).
- `run <workflow.json>` runs a workflow file (format in [references/workflows.md](references/workflows.md)),
  optionally opening a granted image first (`--open`) and exporting afterwards (`--export`);
  `--input name=value` sets inputs and `--consent <step-id>` allows barrier steps.
- `open <file>` and `export <file>` move files in and out of the granted folders; `exec <op>
  [params-json]` runs one operation (`layer.add` or `layer_add`); `ops [prefix]` and
  `describe <op>` list operations and their parameters; `status`, `documents`, `attach`,
  `request-access <list>` and `outcome <request-id>` match the MCP tools. To look at a result,
  export a PNG into a `--write` folder and open it.
- Exit codes: 0 ok, 1 internal error, 2 usage, 3 no session or connector, 4 path refused,
  5 operation failed, 6 retrieval failed, 7 write failed, 8 canceled, 75 waiting for the user. With
  `--json`, a failure's `error` has `code`, `message` and `hint`; editor and connector codes are the
  same as for the MCP tools (see the error table above).
