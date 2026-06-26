# POP Plugin Catalog — Obsidian Community Plugin Manifest

This catalog maps installed Obsidian community plugins to the POP actions they expose.
When `GET_PLUGIN_MANIFEST` is received, the bridge returns entries from this catalog
filtered to what is actually installed in the vault.

Version: 1.0.0
Last updated: 2026-02-22

---

## Core Plugins (Built-in Obsidian)

These actions are always available regardless of community plugins:

| Action | Source | Description |
|--------|--------|-------------|
| `create_note` | Obsidian core | Create a new note in the vault |
| `read_note` | Obsidian core | Read note content and metadata |
| `update_note` | Obsidian core | Update or append to a note |
| `delete_note` | Obsidian core | Delete a note from the vault |
| `search_vault` | Obsidian core | Full-text search across vault |
| `tag_note` | Obsidian core | Add or update tags on a note |
| `link_notes` | Obsidian core | Create wikilinks between notes |

---

## Community Plugin Integrations

### AI Expand — `ai_expand`
**Plugin:** Obsidian Smart Composer / Local GPT / Copilot
**Minimum version:** Any LLM-chat plugin with vault API access
**Action params:**
```json
{
  "note_id": "string",
  "prompt": "string (optional, default: 'Expand this note with supporting detail')",
  "model": "string (optional, default: 'claude-sonnet-4-6')"
}
```
**Returns:** `{id, content, tokens_used, wave_score}`
**Notes:** Falls back to Claude API directly if no plugin is installed.

---

### Figure Generation — `generate_figure`
**Plugin:** AutoFigure (external tool repo) via POP bridge
**Requires:** `pip install autofigure` on the bridge host
**Action params:**
```json
{
  "note_id": "string",
  "style": "string (optional: 'scientific' | 'minimal' | 'wave-topology')",
  "format": "string (optional: 'svg' | 'png', default: 'svg')"
}
```
**Returns:** `{id, svg_path, score, wave_score}`
**Notes:** Generates publication-ready figures from note content. WAVE scored automatically.

---

### WAVE Check — `wave_check`
**Plugin:** Coherence-MCP bridge (native via ws://127.0.0.1:8088)
**Always available:** Yes — hardwired into the Rust bridge
**Action params:**
```json
{
  "content": "string"
}
```
**Returns:** `{score, components: {W, A, V, E}, pass, conservation_check}`
**Notes:** Checks WAVE coherence. Conservation law verified: α + ω = 15.

---

### Merge Notes — `merge_notes`
**Plugin:** Obsidian core (Note Composer plugin)
**Action params:**
```json
{
  "ids": ["string"],
  "title": "string (optional)"
}
```
**Returns:** `{id, content, merged_count}`

---

### Export PDF — `export_pdf`
**Plugin:** Obsidian PDF Export (built-in) / Pandoc Plugin
**Preferred:** Pandoc Plugin for LaTeX-quality output
**Action params:**
```json
{
  "note_id": "string",
  "template": "string (optional: 'default' | 'academic' | 'reson8')"
}
```
**Returns:** `{path, size_bytes}`
**Notes:** `academic` template adds proper citations, abstract section, WAVE score footer.

---

### Export DOCX — `export_docx`
**Plugin:** Pandoc Plugin
**Requires:** Pandoc binary on PATH
**Action params:**
```json
{
  "note_id": "string",
  "template": "string (optional)"
}
```
**Returns:** `{path, size_bytes}`

---

### Dataview Query — `run_dataview`
**Plugin:** Dataview (community — ID: `obsidian-dataview`)
**Minimum version:** 0.5.x
**Action params:**
```json
{
  "query": "string (Dataview query language)"
}
```
**Returns:** `{results: any[], count}`
**Example query:** `TABLE title, date FROM #research SORT date DESC`

---

### Templater — `run_templater`
**Plugin:** Templater (community — ID: `templater-obsidian`)
**Minimum version:** 1.16.x
**Action params:**
```json
{
  "template": "string (template file path in vault)",
  "params": {"key": "value"}
}
```
**Returns:** `{output: string}`
**Notes:** Template variables injected via `tp.user.param_name` convention.

---

## Manifest Response Format

When the POP bridge returns `GET_PLUGIN_MANIFEST`, it uses this structure:

```json
{
  "jsonrpc": "2.0",
  "method": "PLUGIN_MANIFEST",
  "params": {
    "name": "pop-obsidian-bridge",
    "version": "1.0.0",
    "vault": "vault-name",
    "installed_plugins": ["obsidian-dataview", "templater-obsidian", "obsidian-pandoc"],
    "actions": [
      {
        "name": "create_note",
        "source": "core",
        "always_available": true,
        "params_schema": {"title": "string", "content": "string", "folder": "string?", "tags": "string[]?"}
      },
      {
        "name": "ai_expand",
        "source": "smart-composer",
        "always_available": false,
        "installed": true,
        "params_schema": {"note_id": "string", "prompt": "string?", "model": "string?"}
      }
    ],
    "coherence_support": true,
    "atom_auth": true,
    "wave_version": "0.3.1"
  }
}
```

---

## Adding New Plugin Integrations

To add a new Obsidian plugin to the POP catalog:

1. Add an entry to this catalog with: action name, plugin ID, min version, params schema, return schema
2. Implement the action handler in the TypeScript Obsidian plugin stub (`protocol-spec.md`)
3. Register the action in `PLUGIN_MANIFEST` response
4. Test with `/pop` command end-to-end
5. Update the activation map (`../../activate/references/activation-map.md`)

---

## Conservation Law Compliance

Every action that produces content is WAVE scored before returning.
Actions that mutate vault state log an ATOM trail entry.
The conservation law **α + ω = 15** must hold across the full pipeline.
