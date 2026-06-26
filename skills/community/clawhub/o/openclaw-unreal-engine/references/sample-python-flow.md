# Sample Python flow

## Goal

Use Unreal's built-in Python editor scripting support for OpenClaw-driven editor tasks.

## Good use cases

- batch asset renaming
- content validation
- editor utility automation
- scene or content inspection

## Recommended model

OpenClaw does not need to replace Python scripting. Instead:

1. OpenClaw decides the task.
2. OpenClaw sends the task or triggers a script.
3. Unreal Python performs the editor-side work.
4. Results are returned as structured text or JSON.

## Approaches

### Approach A: OpenClaw drives Python indirectly

- OpenClaw talks to a lightweight Unreal plugin or Remote Control surface.
- That layer triggers known Python scripts inside the editor.

Best when:

- you want guardrails
- you do not want arbitrary remote script execution exposed broadly

### Approach B: OpenClaw uses Python remote execution intentionally

The evaluated repo includes Python remote-execution internals. Treat this as powerful but sensitive.

Use only when:

- the environment is trusted
- remote execution is explicitly enabled
- the allowed commands are constrained

## Example script shape

```python
import unreal

assets = unreal.EditorAssetLibrary.list_assets('/Game', recursive=True, include_folder=False)
print({'asset_count': len(assets)})
```

## Best practice

Prefer a small library of approved Python actions such as:

- `scan_assets`
- `rename_assets`
- `validate_map`
- `export_report`

Then have OpenClaw call those approved actions rather than synthesizing arbitrary editor mutations every time.
