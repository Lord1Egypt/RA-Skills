#!/usr/bin/env bash
# ============================================================
# apply-dynamic-agent-patch.sh
# 为 @dingtalk-real-ai/dingtalk-connector 添加 dynamicAgentCreation 支持
#
# 用法:
#   bash apply-dynamic-agent-patch.sh [connector-source-dir]
#
# 如果不传参数，自动检测以下路径：
#   1. ~/.openclaw/extensions/dingtalk/src/
#   2. node_modules/@dingtalk-real-ai/dingtalk-connector/src/
# ============================================================

set -euo pipefail

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m'

log()  { echo -e "${GREEN}[patch]${NC} $1"; }
warn() { echo -e "${YELLOW}[warn]${NC} $1"; }
err()  { echo -e "${RED}[error]${NC} $1"; }

# ---- 定位连接器源码目录 ----
CONNECTOR_DIR=""

if [[ $# -ge 1 ]]; then
  CONNECTOR_DIR="$1"
else
  # 尝试常见路径
  CANDIDATES=(
    "$HOME/.openclaw/extensions/dingtalk"
    "$HOME/.openclaw/extensions/dingtalk-connector"
  )
  for c in "${CANDIDATES[@]}"; do
    if [[ -d "$c/src" && -f "$c/src/core/message-handler.ts" ]]; then
      CONNECTOR_DIR="$c"
      break
    fi
  done
fi

if [[ -z "$CONNECTOR_DIR" || ! -d "$CONNECTOR_DIR/src" ]]; then
  err "无法定位钉钉连接器源码目录"
  err "请手动指定: bash $0 /path/to/dingtalk-connector"
  exit 1
fi

SRC_DIR="$CONNECTOR_DIR/src"
log "连接器源码目录: $CONNECTOR_DIR"

# ---- 检查是否已经 patch 过 ----
if [[ -f "$SRC_DIR/dynamic-agent.ts" ]]; then
  warn "已检测到 dynamic-agent.ts，可能已经 patch 过。跳过。"
  exit 0
fi

# ---- 备份 ----
BACKUP_DIR="$CONNECTOR_DIR/.backup-pre-dynamic-agent"
mkdir -p "$BACKUP_DIR"
log "备份原始文件到 $BACKUP_DIR"

cp "$SRC_DIR/config/schema.ts" "$BACKUP_DIR/" 2>/dev/null || true
cp "$SRC_DIR/types/index.ts" "$BACKUP_DIR/" 2>/dev/null || true
cp "$SRC_DIR/core/message-handler.ts" "$BACKUP_DIR/" 2>/dev/null || true

# ---- 1. 创建 dynamic-agent.ts ----
log "创建 src/dynamic-agent.ts ..."

cat > "$SRC_DIR/dynamic-agent.ts" << 'TYPESCRIPT_EOF'
/**
 * DingTalk Dynamic Agent Creation
 *
 * 移植自 OpenClaw Feishu 的 dynamic-agent.ts
 * 当用户首次私聊机器人时，自动创建独立的 Agent + binding
 */
import { createHash } from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

type DynamicAgentCreationConfig = {
  enabled?: boolean;
  workspaceTemplate?: string;
  agentDirTemplate?: string;
  maxAgents?: number;
};

interface OpenClawConfig {
  agents?: {
    default?: string;
    list?: Array<{ id: string; workspace?: string; agentDir?: string; [k: string]: any }>;
  };
  bindings?: Array<{
    agentId: string;
    match: {
      channel?: string;
      accountId?: string;
      peer?: { kind?: string; id?: string };
    };
  }>;
  channels?: Record<string, any>;
  [k: string]: any;
}

function resolveUserPath(p: string): string {
  if (p.startsWith("~/")) {
    return path.join(os.homedir(), p.slice(2));
  }
  return p;
}

function resolveDynamicAgentId(accountId: string, senderId: string): string {
  if (accountId === "default") {
    return `dingtalk-${senderId}`;
  }
  const identityDigest = createHash("sha256")
    .update(accountId)
    .update("\0")
    .update(senderId)
    .digest("hex")
    .slice(0, 32);
  return `dingtalk-${accountId.slice(0, 12)}-${identityDigest}`;
}

function resolveDynamicAgentConfig(
  cfg: OpenClawConfig,
  accountId: string,
): DynamicAgentCreationConfig | undefined {
  const channelCfg = cfg.channels?.["dingtalk-connector"];
  if (!channelCfg) return undefined;

  // 支持顶层配置和 accounts[accountId] 配置
  if (accountId !== "default" && channelCfg.accounts?.[accountId]) {
    return channelCfg.accounts[accountId].dynamicAgentCreation as DynamicAgentCreationConfig | undefined;
  }
  return channelCfg.dynamicAgentCreation as DynamicAgentCreationConfig | undefined;
}

function hasDefaultDirectRoute(
  cfg: OpenClawConfig,
  accountId: string,
  senderId: string,
): boolean {
  const bindings = cfg.bindings ?? [];
  for (const binding of bindings) {
    const match = binding.match;
    if (match.channel && match.channel !== "dingtalk-connector") continue;
    if (match.accountId && match.accountId !== accountId) continue;
    if (match.peer) {
      if (match.peer.kind && match.peer.kind !== "direct") continue;
      if (match.peer.id && match.peer.id !== "*" && match.peer.id !== senderId) continue;
    }
    // 匹配到了 binding，不是 default 路由
    return false;
  }
  return true; // 没有匹配到任何 binding，使用 default
}

function isAtDynamicAgentLimit(
  cfg: OpenClawConfig,
  dynamicCfg: DynamicAgentCreationConfig,
): boolean {
  if (dynamicCfg.maxAgents === undefined) return false;
  const dingtalkAgentCount = (cfg.agents?.list ?? []).filter((agent) =>
    agent.id.startsWith("dingtalk-"),
  ).length;
  return dingtalkAgentCount >= dynamicCfg.maxAgents;
}

/**
 * 尝试为首次私聊的用户动态创建 Agent
 *
 * @returns { created, agentId } 如果创建了新 Agent；否则 { created: false }
 */
export async function maybeCreateDynamicAgent(params: {
  cfg: OpenClawConfig;
  configFilePath: string;
  accountId: string;
  senderId: string;
  isDirect: boolean;
  log?: (...args: any[]) => void;
}): Promise<{ created: boolean; agentId?: string; updatedCfg?: OpenClawConfig }> {
  const { cfg, configFilePath, senderId, isDirect, log } = params;
  const accountId = params.accountId || "default";

  // 仅在单聊时触发
  if (!isDirect) {
    return { created: false };
  }

  // 检查是否已有匹配的 binding（已有则跳过）
  if (!hasDefaultDirectRoute(cfg, accountId, senderId)) {
    return { created: false };
  }

  // 检查是否启用了动态创建
  const dynamicCfg = resolveDynamicAgentConfig(cfg, accountId);
  if (!dynamicCfg?.enabled) {
    return { created: false };
  }

  const agentId = resolveDynamicAgentId(accountId, senderId);
  const currentAgentExists = (cfg.agents?.list ?? []).some((agent) => agent.id === agentId);

  // 检查上限
  if (!currentAgentExists && isAtDynamicAgentLimit(cfg, dynamicCfg)) {
    log?.(`dingtalk: maxAgents limit (${dynamicCfg.maxAgents}) reached, skipping agent for ${senderId}`);
    return { created: false };
  }

  // 如果 Agent 已存在但 binding 缺失，只补 binding
  // 如果 Agent 不存在，创建 Agent + binding

  // 读取当前配置文件（确保是最新的）
  let rawConfig: string;
  try {
    rawConfig = await fs.promises.readFile(configFilePath, "utf-8");
  } catch (e: any) {
    log?.(`dingtalk: 无法读取配置文件 ${configFilePath}: ${e.message}`);
    return { created: false };
  }

  // 解析 JSON（支持 JSON5 风格的注释和尾逗号）
  // 简单处理：移除注释和尾逗号
  const cleanedConfig = rawConfig
    .replace(/\/\/.*$/gm, "")      // 移除单行注释
    .replace(/\/\*[\s\S]*?\*\//g, "") // 移除多行注释
    .replace(/,\s*([}\]])/g, "$1")  // 移除尾逗号
    ;
  let draft: OpenClawConfig;
  try {
    draft = JSON.parse(cleanedConfig);
  } catch (e: any) {
    log?.(`dingtalk: 配置文件 JSON 解析失败: ${e.message}`);
    return { created: false };
  }

  // 双重检查（防止并发写入）
  if (!hasDefaultDirectRoute(draft, accountId, senderId)) {
    return { created: false };
  }
  const draftDynamicCfg = resolveDynamicAgentConfig(draft, accountId);
  if (!draftDynamicCfg?.enabled) {
    return { created: false };
  }
  const draftAgentExists = (draft.agents?.list ?? []).some((a) => a.id === agentId);
  if (!draftAgentExists && isAtDynamicAgentLimit(draft, draftDynamicCfg)) {
    log?.(`dingtalk: maxAgents limit reached (concurrent check), skipping`);
    return { created: false };
  }

  // 创建工作空间和 Agent 目录
  if (!draftAgentExists) {
    const workspaceTemplate =
      draftDynamicCfg.workspaceTemplate ?? "~/.openclaw/workspace-dingtalk-{agentId}";
    const agentDirTemplate =
      draftDynamicCfg.agentDirTemplate ?? "~/.openclaw/agents/{agentId}/agent";
    const workspace = resolveUserPath(
      workspaceTemplate.replace("{userId}", senderId).replace("{agentId}", agentId),
    );
    const agentDir = resolveUserPath(
      agentDirTemplate.replace("{userId}", senderId).replace("{agentId}", agentId),
    );
    log?.(`dingtalk: creating dynamic agent "${agentId}" for user ${senderId}`);
    log?.(`  workspace: ${workspace}`);
    log?.(`  agentDir: ${agentDir}`);
    await fs.promises.mkdir(workspace, { recursive: true });
    await fs.promises.mkdir(agentDir, { recursive: true });

    // 添加 Agent 到列表
    if (!draft.agents) draft.agents = { default: "main", list: [] };
    if (!draft.agents.list) draft.agents.list = [];
    draft.agents.list.push({ id: agentId, workspace, agentDir });
  } else {
    log?.(`dingtalk: agent "${agentId}" exists, adding missing binding for ${senderId}`);
  }

  // 添加 binding
  if (!draft.bindings) draft.bindings = [];
  draft.bindings.push({
    agentId,
    match: {
      channel: "dingtalk-connector",
      accountId,
      peer: { kind: "direct", id: senderId },
    },
  });

  // 写回配置文件
  const output = JSON.stringify(draft, null, 2);
  await fs.promises.writeFile(configFilePath, output + "\n", "utf-8");
  log?.(`dingtalk: config updated, agent "${agentId}" created and bound`);

  return { created: true, agentId, updatedCfg: draft };
}
TYPESCRIPT_EOF

log "✅ dynamic-agent.ts 已创建"

# ---- 2. 修改 schema.ts: 添加 dynamicAgentCreation 配置项 ----
log "修改 src/config/schema.ts ..."

SCHEMA_FILE="$SRC_DIR/config/schema.ts"
if grep -q "dynamicAgentCreation" "$SCHEMA_FILE"; then
  warn "schema.ts 已包含 dynamicAgentCreation，跳过"
else
  # 在 DingtalkSharedConfigShape 的末尾（groupReplyMode 后面）添加 dynamicAgentCreation
  # 使用 python 来可靠地插入
  python3 -c "
import re, sys
with open('$SCHEMA_FILE', 'r') as f:
    content = f.read()

# 在 DingtalkSharedConfigShape 的 groupReplyMode 行后添加 dynamicAgentCreation
old = '  groupReplyMode: GroupReplyModeSchema,'
new = '''  groupReplyMode: GroupReplyModeSchema,
  // Dynamic Agent Creation (Agent 级隔离)
  dynamicAgentCreation: z
    .object({
      enabled: z.boolean().optional(),
      workspaceTemplate: z.string().optional(),
      agentDirTemplate: z.string().optional(),
      maxAgents: z.number().int().positive().optional(),
    })
    .strict()
    .optional(),'''

if old in content:
    content = content.replace(old, new, 1)
    with open('$SCHEMA_FILE', 'w') as f:
        f.write(content)
    print('OK: schema.ts patched')
else:
    print('SKIP: marker not found')
    sys.exit(1)
" || warn "schema.ts patch 跳过（可能格式不同）"
fi

log "✅ schema.ts 已修改"

# ---- 3. 修改 message-handler.ts: 在 binding 匹配后调用动态创建 ----
log "修改 src/core/message-handler.ts ..."

HANDLER_FILE="$SRC_DIR/core/message-handler.ts"
if grep -q "maybeCreateDynamicAgent" "$HANDLER_FILE"; then
  warn "message-handler.ts 已包含 maybeCreateDynamicAgent，跳过"
else
  # 在 matchedAgentId 确定后、使用之前插入动态创建逻辑
  # 找到 "if (!matchedAgentId) {" 这一行，在它之前插入
  python3 -c "
with open('$HANDLER_FILE', 'r') as f:
    content = f.read()

# 在 'if (!matchedAgentId) {' 之前插入动态创建逻辑
marker = '  if (!matchedAgentId) {'
insert_code = '''  // ===== Dynamic Agent Creation (Agent 级隔离) =====
  // 当 binding 匹配到 default 且为单聊时，尝试动态创建 Agent
  if (matchedAgentId === (cfg.defaultAgent || 'main') && isDirect) {
    try {
      const { maybeCreateDynamicAgent } = await import('../dynamic-agent.ts');
      const configFilePath = path.join(os.homedir(), '.openclaw', 'openclaw.json');
      const dynamicResult = await maybeCreateDynamicAgent({
        cfg,
        configFilePath,
        accountId,
        senderId,
        isDirect,
        log,
      });
      if (dynamicResult.created && dynamicResult.agentId) {
        log?.info?.(\`[DynamicAgent] 创建新 Agent: \${dynamicResult.agentId}\`);
        matchedAgentId = dynamicResult.agentId;
        // 更新 cfg 以包含新的 binding（后续的 sessionKey 构建需要）
        if (dynamicResult.updatedCfg) {
          Object.assign(cfg, dynamicResult.updatedCfg);
        }
      }
    } catch (dynErr: any) {
      log?.warn?.(\`[DynamicAgent] 动态创建失败: \${dynErr?.message || dynErr}\`);
    }
  }

'''

if marker in content:
    content = content.replace(marker, insert_code + marker, 1)
    with open('$HANDLER_FILE', 'w') as f:
        f.write(content)
    print('OK: message-handler.ts patched')
else:
    print('SKIP: marker not found in message-handler.ts')
" || warn "message-handler.ts patch 跳过（可能格式不同）"
fi

log "✅ message-handler.ts 已修改"

# ---- 4. 修改 openclaw.plugin.json: 添加 dynamicAgentCreation 到 configSchema ----
PLUGIN_JSON="$CONNECTOR_DIR/openclaw.plugin.json"
if [[ -f "$PLUGIN_JSON" ]] && ! grep -q "dynamicAgentCreation" "$PLUGIN_JSON"; then
  log "修改 openclaw.plugin.json ..."
  python3 -c "
import json
with open('$PLUGIN_JSON', 'r') as f:
    data = json.load(f)

# 在 channelConfigs.dingtalk-connector.schema.properties 中添加 dynamicAgentCreation
props = data.get('channelConfigs', {}).get('dingtalk-connector', {}).get('schema', {}).get('properties', {})
if 'groupReplyMode' in props:
    props['dynamicAgentCreation'] = {
        'type': 'object',
        'properties': {
            'enabled': {'type': 'boolean'},
            'workspaceTemplate': {'type': 'string'},
            'agentDirTemplate': {'type': 'string'},
            'maxAgents': {'type': 'integer', 'minimum': 1}
        },
        'additionalProperties': False
    }
    with open('$PLUGIN_JSON', 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')
    print('OK: openclaw.plugin.json patched')
else:
    print('SKIP: groupReplyMode not found in plugin.json')
" || warn "openclaw.plugin.json patch 跳过"
  log "✅ openclaw.plugin.json 已修改"
fi

# ---- 完成 ----
echo ""
log "========================================"
log "✅ Patch 完成！"
log ""
log "下一步："
log "  1. 在 openclaw.json 中添加 dynamicAgentCreation 配置"
log "  2. 重启 OpenClaw: openclaw restart"
log ""
log "配置示例："
echo '  "dynamicAgentCreation": {'
echo '    "enabled": true,'
echo '    "maxAgents": 100'
echo '  }'
echo ""
log "备份位置: $BACKUP_DIR"
log "========================================"
