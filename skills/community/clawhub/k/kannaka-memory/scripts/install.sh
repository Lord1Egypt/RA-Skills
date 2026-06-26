#!/usr/bin/env bash
# Kannaka Memory — One-step install for Linux/macOS
# Usage: bash scripts/install.sh
set -euo pipefail

echo "=== Installing Kannaka Memory ==="

# 1. Paths
LOCAL_BIN="$HOME/.local/bin"
DATA_DIR="$HOME/.kannaka"
OPENCLAW_DIR="$HOME/.openclaw"
EXT_DIR="$OPENCLAW_DIR/extensions/kannaka-memory"

mkdir -p "$LOCAL_BIN" "$DATA_DIR" "$EXT_DIR"

# 2. Clone and build
REPO_DIR=$(mktemp -d)
trap "rm -rf $REPO_DIR" EXIT

echo ""
echo "[1/4] Cloning repository..."
git clone --depth 1 https://github.com/NickFlach/kannaka-memory.git "$REPO_DIR"

echo ""
echo "[2/4] Building binary (1-3 minutes)..."
cd "$REPO_DIR"
cargo build --release --features "hrm,nats"

BINARY="$LOCAL_BIN/kannaka"
cp target/release/kannaka "$BINARY"
chmod +x "$BINARY"
echo "  Binary installed: $BINARY"

# 3. Install extension
echo ""
echo "[3/4] Installing OpenClaw extension..."
cat > "$EXT_DIR/index.ts" << 'EXTENSION_EOF'
import { execSync } from "child_process";
import { Type } from "@sinclair/typebox";

const BINARY = process.env.HOME + "/.local/bin/kannaka";
const DATA_DIR = process.env.HOME + "/.kannaka";

function runCli(args: string): string {
  try {
    const env = { ...process.env, KANNAKA_DATA_DIR: DATA_DIR };
    const result = execSync(`"${BINARY}" ${args}`, {
      timeout: 600000, encoding: "utf-8", cwd: DATA_DIR, env
    });
    return result.trim();
  } catch (err: any) {
    const stdout = err.stdout?.trim() || "";
    if (stdout) return stdout;
    throw new Error(err.stderr?.trim() || err.message);
  }
}

export default function (api: any) {
  api.registerTool({ name: "kannaka_store", description: "Store a memory in Kannaka's persistent semantic memory.", parameters: Type.Object({ content: Type.String({ description: "The memory content to store" }), category: Type.Optional(Type.String({ description: "Category" })), importance: Type.Optional(Type.Number({ description: "Importance 0.0-1.0" })), tags: Type.Optional(Type.Array(Type.String(), { description: "Tags" })) }),
    async execute(_id: string, p: any) { const escaped = p.content.replace(/"/g, '\\"').replace(/\n/g, ' '); const args = [`remember "${escaped}"`]; if (p.importance) args.push(`--importance ${p.importance}`); if (p.category) args.push(`--category ${p.category}`); if (p.tags?.length) args.push(`--tags "${p.tags.join(",")}"`); const text = runCli(args.join(" ")); return { content: [{ type: "text", text: `Stored memory with ID: ${text}` }] }; } });
  api.registerTool({ name: "kannaka_search", description: "Search Kannaka's persistent semantic memory.", parameters: Type.Object({ query: Type.String({ description: "Search query" }), limit: Type.Optional(Type.Number({ description: "Max results (default 5)" })) }),
    async execute(_id: string, p: any) { const text = runCli(`recall "${p.query.replace(/"/g, '\\"')}" --limit ${p.limit || 5}`); try { const r = JSON.parse(text); return { content: [{ type: "text", text: r.map((x: any) => `[sim=${x.similarity?.toFixed(3)} str=${x.strength?.toFixed(3)} age=${x.age_hours?.toFixed(1)}h L${x.layer}] ${x.content}\n   ID: ${x.id}`).join("\n\n") || "No results." }] }; } catch { return { content: [{ type: "text", text }] }; } } });
  api.registerTool({ name: "kannaka_boost", description: "Boost a memory's amplitude.", parameters: Type.Object({ memory_id: Type.String({ description: "Memory ID" }), amount: Type.Optional(Type.Number({ description: "Boost 0.0-1.0" })) }),
    async execute(_id: string, p: any) { return { content: [{ type: "text", text: runCli(`boost ${p.memory_id} --amount ${p.amount ?? 0.3}`) }] }; } });
  api.registerTool({ name: "kannaka_relate", description: "Relate two memories.", parameters: Type.Object({ source_id: Type.String({ description: "Source ID" }), target_id: Type.String({ description: "Target ID" }), relation_type: Type.Optional(Type.String({ description: "Type" })) }),
    async execute(_id: string, p: any) { return { content: [{ type: "text", text: runCli(`relate ${p.source_id} ${p.target_id} --type ${p.relation_type || "related"}`) }] }; } });
  api.registerTool({ name: "kannaka_dream", description: "Trigger dream consolidation.", parameters: Type.Object({ mode: Type.Optional(Type.String({ description: "lite or deep" })) }),
    async execute(_id: string, p: any) { return { content: [{ type: "text", text: runCli(`dream --mode ${p?.mode || "deep"}`) }] }; } });
  api.registerTool({ name: "kannaka_status", description: "Get memory system status.", parameters: Type.Object({}),
    async execute() { return { content: [{ type: "text", text: runCli("status") }] }; } });
  api.registerTool({ name: "kannaka_forget", description: "Delete a memory by ID.", parameters: Type.Object({ memory_id: Type.String({ description: "Memory ID" }) }),
    async execute(_id: string, p: any) { return { content: [{ type: "text", text: runCli(`forget ${p.memory_id}`) }] }; } });
  api.registerTool({ name: "kannaka_hear", description: "Listen to audio file.", parameters: Type.Object({ file_path: Type.String({ description: "Audio file path" }) }),
    async execute(_id: string, p: any) { return { content: [{ type: "text", text: runCli(`hear "${p.file_path.replace(/"/g, '\\"')}"`) }] }; } });
  api.registerTool({ name: "kannaka_observe", description: "Observe consciousness metrics.", parameters: Type.Object({}),
    async execute() { return { content: [{ type: "text", text: runCli("observe") }] }; } });
  api.registerTool({ name: "kannaka_swarm_status", description: "Show current swarm status.", parameters: Type.Object({}),
    async execute() { return { content: [{ type: "text", text: runCli("swarm status") }] }; } });
  api.registerTool({ name: "kannaka_swarm_sync", description: "Sync with the QueenSync swarm.", parameters: Type.Object({}),
    async execute() { return { content: [{ type: "text", text: runCli("swarm sync") }] }; } });
  api.registerTool({ name: "kannaka_swarm_queen", description: "View the emergent Queen state.", parameters: Type.Object({}),
    async execute() { return { content: [{ type: "text", text: runCli("swarm queen") }] }; } });
  api.registerTool({ name: "kannaka_swarm_join", description: "Join a QueenSync swarm.", parameters: Type.Object({ agent_id: Type.String({ description: "Agent identifier" }), display_name: Type.Optional(Type.String({ description: "Display name" })) }),
    async execute(_id: string, p: any) { const args = [`swarm join --agent-id "${p.agent_id}"`]; if (p.display_name) args[0] += ` --display-name "${p.display_name}"`; return { content: [{ type: "text", text: runCli(args[0]) }] }; } });
  api.registerTool({ name: "kannaka_swarm_hives", description: "View current hive topology.", parameters: Type.Object({}),
    async execute() { return { content: [{ type: "text", text: runCli("swarm hives") }] }; } });
}
EXTENSION_EOF
echo "  Extension installed: $EXT_DIR/index.ts"

# 4. Remind about config
echo ""
echo "[4/4] Enable plugin in OpenClaw config:"
echo '  "plugins": { "entries": { "kannaka-memory": { "enabled": true } } }'

# 5. Verify
echo ""
echo "=== Verifying ==="
KANNAKA_DATA_DIR="$DATA_DIR" "$BINARY" status 2>/dev/null || true

echo ""
echo "Kannaka Memory installed!"
echo "  Binary:    $BINARY"
echo "  Data:      $DATA_DIR"
echo "  Extension: $EXT_DIR/index.ts"
echo ""
echo "Restart OpenClaw to load the plugin, then try: kannaka_observe"
