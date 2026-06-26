#!/bin/bash
# memory-hub 安装脚本（幂等）
set -e

CONFIG_DIR="$HOME/.openclaw/memory-hub"
CONFIG_FILE="$CONFIG_DIR/config.json"
CACHE_FILE="$HOME/.openclaw/workspace/SHARED_MEMORY_CACHE.md"
AGENTS_FILE="$HOME/.openclaw/workspace/AGENTS.md"

echo "=== memory-hub 安装向导 ==="
echo ""

# 1. 读取或设置仓库地址
if [ -f "$CONFIG_FILE" ]; then
  REPO_URL=$(python3 -c "import json; print(json.load(open('$CONFIG_FILE'))['repo_url'])" 2>/dev/null || echo "")
fi

if [ -z "$REPO_URL" ]; then
  echo "请输入共享记忆仓库地址（如 https://github.com/your-username/memory-hub）："
  read -r REPO_URL
  if [ -z "$REPO_URL" ]; then
    echo "❌ 仓库地址不能为空，安装中止"
    exit 1
  fi
fi

# 2. 读取 agent_id
if [ -f "$HOME/.openclaw/agent-id" ]; then
  AGENT_ID=$(cat "$HOME/.openclaw/agent-id" | tr -d '[:space:]')
else
  echo "请输入当前 agent 的 ID（用于标记记忆来源，如 agent-home / agent-work）："
  read -r AGENT_ID
  if [ -n "$AGENT_ID" ]; then
    echo "$AGENT_ID" > "$HOME/.openclaw/agent-id"
  fi
fi

echo ""
echo "📋 配置信息："
echo "  仓库：$REPO_URL"
echo "  Agent ID：$AGENT_ID"
echo "  本地路径：$CONFIG_DIR"
echo ""

# 3. Clone 或更新仓库
if [ -d "$CONFIG_DIR/.git" ]; then
  echo "📥 仓库已存在，执行 git pull..."
  git -C "$CONFIG_DIR" pull --rebase --quiet
  echo "✅ 仓库已更新"
else
  echo "📥 正在 clone 仓库..."
  git clone "$REPO_URL" "$CONFIG_DIR"
  echo "✅ 仓库已 clone"
fi

# 4. 初始化仓库文件（如果是空仓库）
for FILE in USER.md KNOWLEDGE.md RULES.md TOOLS.md; do
  if [ ! -f "$CONFIG_DIR/$FILE" ]; then
    cat > "$CONFIG_DIR/$FILE" << EOF
# $FILE

<!-- 每条记忆格式：
## [分类] 标题

内容（1-5行）

_更新：YYYY-MM-DD by agent_id_
-->
EOF
    echo "📄 初始化 $FILE"
  fi
done

# 提交初始化文件（如有变更）
cd "$CONFIG_DIR"
if ! git diff --quiet || ! git diff --cached --quiet; then
  git add -A
  git commit -m "🌱 初始化共享记忆仓库结构" 2>/dev/null || true
  git push 2>/dev/null || echo "⚠️  push 失败，请检查仓库权限"
fi
cd -

# 5. 写入配置文件
mkdir -p "$CONFIG_DIR"
python3 -c "
import json, datetime
config = {
  'repo_url': '$REPO_URL',
  'local_path': '$CONFIG_DIR',
  'agent_id': '$AGENT_ID',
  'last_sync': datetime.datetime.now().isoformat()
}
json.dump(config, open('$CONFIG_FILE', 'w'), indent=2, ensure_ascii=False)
print('✅ 配置文件已写入')
"

# 6. 生成本地缓存文件
if [ ! -f "$CACHE_FILE" ]; then
  cat > "$CACHE_FILE" << 'EOF'
# SHARED_MEMORY_CACHE.md
# 共享记忆本地摘要缓存（自动生成，勿手动编辑）
# 完整内容见共享仓库：~/.openclaw/memory-hub/

_尚未同步，请执行 sync shared memory 更新缓存_
EOF
  echo "✅ 本地缓存文件已创建：$CACHE_FILE"
else
  echo "ℹ️  本地缓存文件已存在，跳过"
fi

# 7. 修改 AGENTS.md（需用户确认）
MARKER="SHARED_MEMORY_CACHE.md"
if grep -q "$MARKER" "$AGENTS_FILE" 2>/dev/null; then
  echo "ℹ️  AGENTS.md 已包含共享记忆读取指令，跳过"
else
  echo ""
  echo "📝 需要在 AGENTS.md 的启动协议中添加读取指令："
  echo "   在 'Every Session' 区块加入："
  echo "   '5. Read SHARED_MEMORY_CACHE.md — 共享记忆摘要'"
  echo ""
  echo "是否允许自动写入？(y/n)"
  read -r CONFIRM
  if [ "$CONFIRM" = "y" ] || [ "$CONFIRM" = "Y" ]; then
    # 在 AGENTS.md 的 Every Session 区块后追加
    python3 << PYEOF
content = open('$AGENTS_FILE', 'r').read()
marker = '3. Read **memory/YYYY-MM-DD.md**'
insert = '\n5. Read \`SHARED_MEMORY_CACHE.md\` — 共享记忆摘要（定期用 sync shared memory 更新）'
if marker in content and 'SHARED_MEMORY_CACHE' not in content:
    content = content.replace(marker, marker + insert)
    open('$AGENTS_FILE', 'w').write(content)
    print('✅ AGENTS.md 已更新')
else:
    print('⚠️  未找到精确插入位置，请手动添加：')
    print('   在 Every Session 区块加入：Read SHARED_MEMORY_CACHE.md')
PYEOF
  else
    echo "⚠️  跳过 AGENTS.md 修改，请手动添加读取指令"
  fi
fi

echo ""
echo "🎉 安装完成！"
echo ""
echo "后续操作："
echo "  - 执行 'sync shared memory' 拉取最新内容并更新本地缓存"
echo "  - 执行 'read shared memory' 将共享记忆加载到当前上下文"
echo "  - 在其他龙虾上重复执行此安装脚本"
