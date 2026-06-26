#!/bin/bash
# activate.sh — 为当前 Agent（或共享空间）激活知识库
# 默认 Agent 专属；加 --scope shared 或 --shared 激活跨 Agent 共享库

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"

# shellcheck disable=SC1091
source "$SCRIPT_DIR/kb-scope.sh"
kb_parse_scope "$@"
set -- "${KB_ARGS[@]}"

echo "🔧 激活 huo15-knowledge-base (scope=$KB_SCOPE)"
if [ "$KB_SCOPE" = "agent" ]; then
  echo "  Agent 目录: $AGENT_DIR"
fi
echo "  知识库目录: $KB_DATA_DIR"

kb_ensure_scope_dirs "$KB_DATA_DIR"
mkdir -p "$KB_DATA_DIR/wiki/_index"

cat > "$KB_DATA_DIR/config.json" << CONFIG_EOF
{
  "version": "0.2.0",
  "scope": "$KB_SCOPE",
  "agent_context": "$AGENT_DIR",
  "paths": {
    "raw": "$KB_DATA_DIR/raw",
    "wiki": "$KB_DATA_DIR/wiki",
    "cache": "$KB_DATA_DIR/cache"
  },
  "llm": {
    "model": "minimax/MiniMax-M2.7",
    "provider": "openclaw"
  }
}
CONFIG_EOF

# 写入 SCHEMA.md（图书馆员守则；首次激活时种入，已存在则不覆盖）
SCHEMA_TEMPLATE="$SKILL_ROOT/templates/wiki-schema.md"
SCHEMA_DEST="$KB_DATA_DIR/wiki/SCHEMA.md"
if [ ! -f "$SCHEMA_DEST" ] && [ -f "$SCHEMA_TEMPLATE" ]; then
  cp "$SCHEMA_TEMPLATE" "$SCHEMA_DEST"
  echo "  ✅ 已种入 SCHEMA.md（图书馆员守则）"
fi

if [ ! -f "$KB_DATA_DIR/wiki/index.md" ]; then
  if [ "$KB_SCOPE" = "shared" ]; then
    cat > "$KB_DATA_DIR/wiki/index.md" << 'WIKI_INDEX'
---
title: 共享知识库索引
scope: shared
last_compiled: never
---

# 共享知识库

> 跨 Agent 共享的长期知识资料（Karpathy Wiki 风格）
>
> 会通过 @huo15/openclaw-enhance 的 corpus supplement 并入龙虾原生 `memory_search`。

## 用法
```bash
kb-ingest --scope shared --url "https://..."
kb-compile --scope shared
kb-search "关键词"   # 默认同时搜 agent + shared
```

## 最近更新
暂无
WIKI_INDEX
  else
    cat > "$KB_DATA_DIR/wiki/index.md" << 'WIKI_INDEX'
---
title: 知识库索引
scope: agent
last_compiled: never
---

# 知识库

> Agent 专属知识库 — LLM 编译的结构化百科全书

## 状态

尚未编译任何文档。请先入库：
```bash
kb-ingest --url "https://..."
```

## 最近更新

暂无
WIKI_INDEX
  fi
fi

echo ""
echo "✅ 激活完成！"
echo ""
echo "目录结构："
echo "  $KB_DATA_DIR/raw/        — 原始文档"
echo "  $KB_DATA_DIR/wiki/       — 编译后的百科"
echo "  $KB_DATA_DIR/cache/      — 临时缓存"
echo "  $KB_DATA_DIR/config.json — 配置"
echo ""
echo "下一步："
if [ "$KB_SCOPE" = "shared" ]; then
  echo "  kb-ingest --scope shared --url 'https://...'  # 入库到共享库"
  echo "  kb-compile --scope shared                      # 编译共享库"
  echo ""
  echo "💡 @huo15/openclaw-enhance 会把共享 wiki 挂为 corpus=\"kb\","
  echo "   龙虾 memory_search 会自动搜到共享知识。"
else
  echo "  kb-ingest --url 'https://...'  # 入库到本 Agent"
  echo "  kb-compile                      # 编译"
  echo ""
  echo "💡 入库到跨 Agent 共享库: kb-ingest --scope shared --url '...'"
fi
echo ""
echo "快捷命令："
echo "  source $SCRIPT_DIR/env.sh                  # Agent scope"
echo "  source $SCRIPT_DIR/env.sh --scope shared   # Shared scope"
