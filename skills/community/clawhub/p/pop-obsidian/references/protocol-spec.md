# POP Protocol Specification — JSON-RPC over WebSocket

Version: 1.0.0
Transport: WebSocket (ws://127.0.0.1:8088)
Encoding: JSON-RPC 2.0
Auth: ATOM_TOKEN_RESONANCE

## Message Types

### Client → Server

| Method | Params | Description |
|--------|--------|-------------|
| GET_PLUGIN_MANIFEST | none | Request installed plugin capabilities |
| EXECUTE_PIPELINE | pipeline, steps[], coherence_threshold, atom_token | Execute a multi-step pipeline |
| CANCEL_PIPELINE | pipeline_id | Cancel a running pipeline |
| GET_PIPELINE_STATUS | pipeline_id | Query current pipeline state |

### Server → Client (Notifications)

| Method | Params | Description |
|--------|--------|-------------|
| STEP_COMPLETE | pipeline_id, step_id, status, output, wave_score, duration_ms | Step finished |
| STEP_STARTED | pipeline_id, step_id | Step began execution |
| COHERENCE_REPORT | pipeline_id, overall_score, step_scores, conservation_check, atom_trail_id | Pipeline complete |
| PIPELINE_FAILED | pipeline_id, failed_step, error, partial_outputs, recovery | Pipeline error |

## Step Definition Schema

```typescript
interface PipelineStep {
  id: string;                    // Unique step identifier
  action: string;                // Action to execute (maps to Obsidian plugin action)
  params: Record<string, any>;   // Action parameters (supports $ref syntax)
  depends_on?: string[];         // Explicit dependencies (auto-inferred from $refs if omitted)
  timeout_ms?: number;           // Step timeout (default: 30000)
  retry?: {
    max_attempts: number;        // Max retries on failure
    backoff_ms: number;          // Backoff between retries
  };
}
```

## Variable Reference Syntax

Steps can reference outputs from previous steps:

- `$step_id.output.field` — Access a specific field from a step's output
- `$step_id.output` — Access the entire output object
- `$step_id.wave_score` — Access the WAVE score from a step
- `$ENV_VAR` — Access environment variables (prefixed with no dot)

Examples:
```json
{"note_id": "$spark.output.id"}
{"content": "$expand.output.content"}
{"ids": ["$spark.output.id", "$expand.output.id"]}
```

## Available Actions (Obsidian Plugin)

These actions map to Obsidian vault operations:

| Action | Params | Returns |
|--------|--------|---------|
| create_note | title, content, folder?, tags? | {id, path} |
| read_note | note_id | {id, content, metadata} |
| update_note | note_id, content, append? | {id, updated_at} |
| delete_note | note_id | {deleted: true} |
| search_vault | query, limit? | {results: [{id, title, score}]} |
| ai_expand | note_id, prompt?, model? | {id, content, tokens_used} |
| generate_figure | note_id, style?, format? | {id, svg_path, score} |
| wave_check | content | {score, components, pass} |
| merge_notes | ids[], title? | {id, content} |
| export_pdf | note_id, template? | {path, size_bytes} |
| export_docx | note_id, template? | {path, size_bytes} |
| tag_note | note_id, tags[] | {id, tags} |
| link_notes | source_id, target_id, type? | {link_id} |
| run_dataview | query | {results: any[]} |
| run_templater | template, params | {output: string} |

## Coherence Threshold Behavior

The `coherence_threshold` parameter (default: 0.85) controls pipeline behavior:

- **score >= threshold:** Step passes, continue to next step
- **score >= threshold - 0.10:** Warning logged, continue with caution flag
- **score < threshold - 0.10:** Pipeline pauses, user intervention required
- **score < 0.50:** Pipeline aborts automatically

## ATOM Token Structure

```typescript
interface AtomToken {
  session_id: string;       // UUID for this session
  agent_id: string;         // Which agent initiated (claude|grok|gemini)
  timestamp: number;        // Unix epoch ms
  coherence_floor: number;  // Minimum acceptable coherence
  conservation_proof: {     // Proof that ALPHA + OMEGA = 15
    alpha: number;
    omega: number;
    hash: string;           // SHA-256 of `${alpha}:${omega}:${session_id}`
  };
  signature: string;        // HMAC-SHA256 with shared secret
}
```

## Error Codes

| Code | Meaning |
|------|---------|
| -32600 | Invalid request |
| -32601 | Method not found |
| -32602 | Invalid params |
| -32603 | Internal error |
| -32001 | Pipeline not found |
| -32002 | Step dependency unresolved |
| -32003 | Coherence below threshold |
| -32004 | ATOM token invalid |
| -32005 | Timeout exceeded |
| -32006 | Plugin not available |

## TypeScript Obsidian Plugin Stub

```typescript
import { Plugin, Notice } from 'obsidian';

const POP_PORT = 8088;

export default class POPBridgePlugin extends Plugin {
  private ws: WebSocket | null = null;
  private pipelines: Map<string, PipelineState> = new Map();

  async onload() {
    this.startWebSocketServer();
    new Notice('POP Bridge: Listening on ws://127.0.0.1:' + POP_PORT);
  }

  private startWebSocketServer() {
    // In Obsidian, we connect as client to the Rust bridge
    // The Rust bridge is the server on port 8088
    this.ws = new WebSocket(`ws://127.0.0.1:${POP_PORT}`);

    this.ws.onopen = () => {
      console.log('POP: Connected to bridge');
      this.sendManifest();
    };

    this.ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      this.handleMessage(msg);
    };

    this.ws.onclose = () => {
      console.log('POP: Disconnected, reconnecting in 5s...');
      setTimeout(() => this.startWebSocketServer(), 5000);
    };
  }

  private async handleMessage(msg: any) {
    switch (msg.method) {
      case 'EXECUTE_PIPELINE':
        await this.executePipeline(msg.params, msg.id);
        break;
      case 'CANCEL_PIPELINE':
        this.cancelPipeline(msg.params.pipeline_id);
        break;
      case 'GET_PIPELINE_STATUS':
        this.sendPipelineStatus(msg.params.pipeline_id, msg.id);
        break;
    }
  }

  private sendManifest() {
    const manifest = {
      jsonrpc: '2.0',
      method: 'PLUGIN_MANIFEST',
      params: {
        name: 'pop-obsidian-bridge',
        version: '1.0.0',
        actions: [
          'create_note', 'read_note', 'update_note', 'delete_note',
          'search_vault', 'ai_expand', 'generate_figure', 'wave_check',
          'merge_notes', 'export_pdf', 'export_docx', 'tag_note',
          'link_notes', 'run_dataview', 'run_templater'
        ],
        coherence_support: true,
        atom_auth: true
      }
    };
    this.ws?.send(JSON.stringify(manifest));
  }

  private async executePipeline(params: any, requestId: number) {
    // Resolve step DAG in topological order
    // Execute each step, sending STEP_COMPLETE after each
    // Run WAVE check at transitions
    // Send COHERENCE_REPORT when done
  }

  onunload() {
    this.ws?.close();
  }
}
```
