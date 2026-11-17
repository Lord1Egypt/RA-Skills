# PhotoFresco workflows

A workflow is a portable, versioned list of PhotoFresco operation steps with typed inputs. It is
the same thing as a saved Action in the editor's Actions panel, so the user can also play it there.
Use one when the same edit should run on several images, or when the user wants to keep a recipe.

## Tools

Enable the `automation` group first:

```mcp
photofresco_select_tool_groups {"enable": ["automation"]}
```

| Tool | Permission | Does |
|---|---|---|
| `workflow_validate` | Read | Preflight against the target document; runs nothing. Returns `ok`, `steps`, `problems`, `warnings` and `barriers` |
| `workflow_run` | Edit | Validates, then runs every step; returns the run record (`run_id`, `state`, per-step `status`, `outputs`, `failure`) |
| `workflow_rollback` | Edit | Undoes a whole run by `run_id` if nothing else changed the document since |
| `workflow_export` | Read | A saved Action as a workflow document |
| `workflow_import` | Edit | Saves a workflow as a new Action (browser storage; `history_undo` does not remove it) |

`workflow_run` and `workflow_validate` take either `workflow` (the document below) or `action_id`
(from `action_list`), plus `inputs`, and `consent` for barrier steps.

## Format

```json
{
  "format": "photofresco.workflow",
  "version": 1,
  "name": "Darken sky",
  "source": {"width": 1200, "height": 800},
  "inputs": {
    "amount": {"type": "number", "minimum": -150, "maximum": 0, "default": -40, "description": "Brightness change"}
  },
  "requires": {
    "ops": {
      "selection.rect": {"effects": ["document"], "capabilities": ["edit"], "params": ["feather", "h", "w", "x", "y"]},
      "adjust.add": {"effects": ["document"], "capabilities": ["edit"], "params": ["adjustment_type", "params"]},
      "mask.add": {"effects": ["document"], "capabilities": ["edit"], "params": ["mode"]},
      "selection.none": {"effects": ["document"], "capabilities": ["edit"], "params": []},
      "layer.set_props": {"effects": ["document"], "capabilities": ["edit"], "params": ["id", "name"]}
    }
  },
  "steps": [
    {"id": "select", "op": "selection.rect", "params": {"x": 0, "y": 0, "w": {"$rel": 1, "of": "width"}, "h": {"$rel": 0.4, "of": "height"}, "feather": 24}},
    {"id": "darken", "op": "adjust.add", "params": {"adjustment_type": "brightness-contrast", "params": {"brightness": {"$input": "amount"}, "contrast": 20}}, "output": "sky"},
    {"id": "mask", "op": "mask.add", "params": {"mode": "selection"}},
    {"id": "deselect", "op": "selection.none", "params": {}},
    {"id": "rename", "op": "layer.set_props", "params": {"id": {"$output": "sky", "path": "id"}, "name": "Sky darken"}}
  ]
}
```

Run it on the target document (validate first):

```mcp
workflow_validate {"workflow": <the document above>, "inputs": {"amount": -30}}
workflow_run {"workflow": <the document above>, "inputs": {"amount": -30}}
```

- **`op`** is the PhotoFresco operation name, not the tool name: each tool description ends with
  "PhotoFresco operation: `<name>`" (`adjust_add` → `adjust.add`).
- **`requires.ops`** lists every op the steps use, with the effects and permissions it has today and
  the parameter names the steps pass. From a tool description: "Edits the document through an
  undoable command" = `document`; "Changes editor view or tool settings" = `view`; "Reads the
  document" = `read`; "Opens, closes, duplicates or reverts documents" = `lifecycle`; "Writes
  browser storage" = `local-storage`; "Sends document data" = `external-write`; "Spends AI credits"
  = `paid`. Permissions: Read = `read`, Edit = `edit`, Export = `export`, Send = `external-write`,
  Spend = `spend`. A wrong or outdated entry is refused as `version_mismatch` by
  `workflow_validate`; `workflow_export` writes this section for you from a saved Action.
- **Bindings** replace document-specific values: `{"$input": "name"}` (a declared input),
  `{"$output": "name", "path": "id"}` (a value an earlier step returned under `"output"`),
  `{"$layer": {"name": "Background"}}`, `{"$layer": {"active": true}}` or
  `{"$layer": {"bottom": true}}` (an existing layer), `{"$literal": value}`.
- **Coordinates**: plain numbers are pixels of `source`; `{"$rel": 0.4, "of": "height"}` (or
  `"width"`, or `{"$rel": [x0, y0, x1, y1], "of": "xy"}`) scales with the canvas the run meets.
- **Inputs** are `{ type, description?, default?, minimum?, maximum?, enum? }` with type `number`,
  `string`, `boolean`, `array`, `object` or `layer` (a layer ID chosen per run; no default).
- **Steps** may also set `"enabled": false`, `"optional": true` (skipped when unsupported) and
  `"barrier": true`.

## Barriers and consent

Steps that export, send data to PhotoFresco services, spend credits or open/close tabs cannot be
undone by rollback. They must carry `"barrier": true` and run only when the call lists their step
IDs in `consent` (nested steps as `"outer/inner"`). `workflow_validate` lists the barriers. Ask the
user before consenting on their behalf, and they still need the matching permissions.

## When something fails

Nothing runs if preflight finds a problem (`workflow_invalid`, `workflow_refused`,
`version_mismatch`). A step that fails stops the run (`workflow_step_failed`); the steps before it
stay applied as a checkpoint you can inspect with `doc_get_state` and `workflow_runs`. Undo the run
with `workflow_rollback` (refused with `rollback_conflict` if anything else changed the document
since; then use `history_undo` step by step). If the user edits the document during a run, it stops
with `document_changed`. Only one workflow runs at a time (`workflow_busy`).
