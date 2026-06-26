---
name: pop-obsidian
description: >
  Plugin Orchestration Protocol (POP) for Obsidian integration. Use this skill when the user
  mentions "POP", "Obsidian plugin", "pipeline orchestration", "idea to publish", "websocket bridge",
  "plugin manifest", "Obsidian automation", "note-to-paper pipeline", "knowledge pipeline",
  or wants to orchestrate multi-step workflows through Obsidian. This skill implements the
  5-phase JSON-RPC protocol over WebSocket for real-time plugin orchestration.
version: 1.0.0
---

# POP Super-Obsidian — Plugin Orchestration Protocol

The POP protocol enables real-time orchestration of multi-step pipelines through Obsidian.
It connects Claude (orchestrator), Obsidian (vault + UI), and the Rust TUI (monitoring dashboard)
via JSON-RPC over WebSocket at ws://127.0.0.1:8088.

## Protocol Overview

POP operates in 5 phases, each with specific JSON-RPC message types:

### Phase 1: Discovery
**Message:** `GET_PLUGIN_MANIFEST`
**Purpose:** Ask the Obsidian plugin what capabilities are installed.

```json
{
  "jsonrpc": "2.0",
  "method": "GET_PLUGIN_MANIFEST",
  "id": 1
}
```

**Response:** Returns a manifest of all installed Obsidian plugins with their exposed actions.
Use this to understand what the vault can do before constructing a pipeline.

### Phase 2: Orchestration
**Message:** `EXECUTE_PIPELINE`
**Purpose:** Send a named pipeline with steps to execute.

```json
{
  "jsonrpc": "2.0",
  "method": "EXECUTE_PIPELINE",
  "params": {
    "pipeline": "idea-to-publish",
    "steps": [
      {"id": "spark", "action": "create_note", "params": {"title": "...", "content": "..."}},
      {"id": "expand", "action": "ai_expand", "params": {"note_id": "$spark.output.id"}},
      {"id": "visual", "action": "generate_figure", "params": {"note_id": "$expand.output.id"}},
      {"id": "verify", "action": "wave_check", "params": {"content": "$expand.output.content"}},
      {"id": "assemble", "action": "merge_notes", "params": {"ids": ["$spark", "$expand", "$visual"]}},
      {"id": "export", "action": "export_pdf", "params": {"note_id": "$assemble.output.id"}}
    ],
    "coherence_threshold": 0.85,
    "atom_token": "$ATOM_TOKEN_RESONANCE"
  },
  "id": 2
}
```

**Step references:** Use `$step_id.output.field` to reference outputs from previous steps.
This creates a DAG of dependencies that the orchestrator resolves in topological order.

### Phase 3: Progress
**Message:** `STEP_COMPLETE`
**Direction:** Obsidian → Claude (notification)

```json
{
  "jsonrpc": "2.0",
  "method": "STEP_COMPLETE",
  "params": {
    "pipeline_id": "...",
    "step_id": "expand",
    "status": "complete",
    "output": {"id": "note-abc", "content": "..."},
    "wave_score": 0.91,
    "duration_ms": 1250
  }
}
```

Each step completion is forwarded to the Rust TUI for real-time gauge updates.

### Phase 4: Coherence
**Message:** `COHERENCE_REPORT`
**Purpose:** Full pipeline coherence assessment after all steps complete.

```json
{
  "jsonrpc": "2.0",
  "method": "COHERENCE_REPORT",
  "params": {
    "pipeline_id": "...",
    "overall_score": 0.89,
    "step_scores": {"spark": 0.92, "expand": 0.91, "visual": 0.87, "verify": 0.93},
    "conservation_check": {"alpha": 7, "omega": 8, "sum": 15, "valid": true},
    "atom_trail_id": "ATOM-2026-02-16-..."
  }
}
```

If `overall_score < coherence_threshold`, the pipeline is flagged for review.

### Phase 5: Error
**Message:** `PIPELINE_FAILED`
**Direction:** Either direction (any party can signal failure)

```json
{
  "jsonrpc": "2.0",
  "method": "PIPELINE_FAILED",
  "params": {
    "pipeline_id": "...",
    "failed_step": "visual",
    "error": "Figure generation timed out",
    "partial_outputs": {"spark": "...", "expand": "..."},
    "recovery": "retry_step"
  }
}
```

**Recovery options:** `retry_step`, `skip_step`, `abort`, `rollback`

## Built-in Pipelines

Read `references/pipeline-templates.md` for full pipeline definitions.

### Quick Reference

| Pipeline | Trigger | Steps |
|----------|---------|-------|
| idea-to-publish | "idea to publish", "note to paper" | Spark → Expand → Visual → Verify → Assemble → Export |
| research-digest | "research digest", "literature summary" | Fetch → Summarize → Score → Tag → Canvas |
| quantum-circuit | "quantum circuit", "place redstone" | Generate → Verify → Export mcfunction → Place |
| paper-draft | "draft paper", "write paper" | RAG → AI-Researcher → AutoFigure → WAVE → PDF |

## Connection Architecture

```
Claude (Orchestrator)
    ↓ JSON-RPC
ws://127.0.0.1:8088
    ↓
Rust WebSocket Bridge (crates/websocket-bridge)
    ├── → Obsidian Plugin (vault operations)
    ├── → Rust TUI (crates/tui — monitoring dashboard)
    └── → WAVE Scorer (coherence at each transition)
```

The Rust bridge is the central hub. It:
1. Receives EXECUTE_PIPELINE from Claude
2. Dispatches steps to Obsidian
3. Receives STEP_COMPLETE from Obsidian
4. Forwards telemetry to the TUI
5. Runs WAVE checks at transitions
6. Sends COHERENCE_REPORT back to Claude

## Authentication

All POP messages include an ATOM token for authentication:
- `$ATOM_TOKEN_RESONANCE` — generated via atom_tag_generate
- Token encodes: session ID, agent identity, coherence threshold, conservation proof
- Five-strand anyon braid topology (see docs/ATOM_AUTH.md)

## Implementing the Obsidian Side

The Obsidian plugin needs to:

1. **Listen** on ws://127.0.0.1:8088 for incoming connections
2. **Expose** GET_PLUGIN_MANIFEST with all installed plugin actions
3. **Handle** EXECUTE_PIPELINE by running steps against the vault
4. **Report** STEP_COMPLETE after each step with outputs and timing
5. **Generate** COHERENCE_REPORT using vault content analysis

For the TypeScript implementation details, read `references/protocol-spec.md`.
