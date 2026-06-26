#!/bin/bash
# OpenClaw 多实例记忆同步脚本
# 用法: ./sync-memory.sh <远程用户@远程IP> <远程workspace路径>
# 例: ./sync-memory.sh root@your-server-ip /home/user/.openclaw/workspace

set -euo pipefail

REMOTE="$1"
REMOTE_WS="$2"
LOCAL_WS="${3:-$HOME/.openclaw/workspace}"
TMP_DIR=$(mktemp -d)

echo "🧠 OpenClaw 记忆同步"
echo "===================="
echo "本地: $LOCAL_WS"
echo "远程: $REMOTE:$REMOTE_WS"
echo ""

# 1. 拉取远程文件
echo "📥 拉取远程记忆..."
scp "$REMOTE:$REMOTE_WS/MEMORY.md" "$TMP_DIR/remote-MEMORY.md" 2>/dev/null || echo "# 远程 MEMORY 为空" > "$TMP_DIR/remote-MEMORY.md"
mkdir -p "$TMP_DIR/remote-memory"
scp -r "$REMOTE:$REMOTE_WS/memory/"* "$TMP_DIR/remote-memory/" 2>/dev/null || true

# 2. 合并 MEMORY.md（叠加，不覆盖）
echo "🔄 合并 MEMORY.md..."
if [ -f "$LOCAL_WS/MEMORY.md" ]; then
    # 找出远程有但本地没有的段落
    # 简单策略：把远程内容追加到本地末尾（去重）
    python3 -c "
import sys

def read_file(path):
    try:
        with open(path, 'r') as f:
            return f.read()
    except:
        return ''

local = read_file('$LOCAL_WS/MEMORY.md')
remote = read_file('$TMP_DIR/remote-MEMORY.md')

# 按段落分割（以 ## 或 ### 开头的行作为分隔符）
local_lines = set(line.strip() for line in local.split('\n') if line.strip())
remote_lines = set(line.strip() for line in remote.split('\n') if line.strip())

# 远程有但本地没有的行
new_lines = [line for line in remote.split('\n') if line.strip() not in local_lines]

if new_lines:
    # 找出哪些段落是新的（以 # 开头）
    new_sections = []
    current_section = []
    for line in remote.split('\n'):
        stripped = line.strip()
        if stripped.startswith('## ') and stripped not in local:
            if current_section:
                new_sections.append('\n'.join(current_section))
            current_section = [line]
        elif current_section:
            if stripped and stripped not in local_lines:
                current_section.append(line)
        # skip lines that already exist locally
    
    # 追加到本地
    with open('$LOCAL_WS/MEMORY.md', 'a') as f:
        f.write('\n\n<!-- 来自远程实例的同步内容 -->\n')
        for section in new_sections:
            f.write(section + '\n')
    print(f'  本地新增 {len(new_sections)} 个段落')
else:
    print('  本地无需更新')

# 同样，本地有但远程没有的
local_only = [line for line in local.split('\n') if line.strip() not in remote_lines]
if local_only:
    with open('$TMP_DIR/merged-remote-MEMORY.md', 'w') as f:
        f.write(remote)
        f.write('\n\n<!-- 来自远程实例的同步内容 -->\n')
        for line in local_only:
            f.write(line + '\n')
    print(f'  远程新增 {len([l for l in local_only if l.startswith(\"##\")])} 个段落')
else:
    # 远程不需要更新
    import shutil
    shutil.copy('$TMP_DIR/remote-MEMORY.md', '$TMP_DIR/merged-remote-MEMORY.md')
    print('  远程无需更新')
" 2>&1
fi

# 3. 同步 memory/ 日记文件（按日期补齐）
echo "🔄 同步 memory/ 日记..."
mkdir -p "$LOCAL_WS/memory"

# 本地缺失的 → 从远程拉
for f in "$TMP_DIR/remote-memory/"*.md; do
    [ -f "$f" ] || continue
    fname=$(basename "$f")
    if [ ! -f "$LOCAL_WS/memory/$fname" ]; then
        cp "$f" "$LOCAL_WS/memory/$fname"
        echo "  📥 拉取: $fname"
    else
        # 同一天的文件，合并去重
        python3 -c "
local_lines = set()
remote_new = []
with open('$LOCAL_WS/memory/$fname', 'r') as f:
    for line in f:
        local_lines.add(line.strip())
with open('$f', 'r') as f:
    for line in f:
        if line.strip() and line.strip() not in local_lines:
            remote_new.append(line)
if remote_new:
    with open('$LOCAL_WS/memory/$fname', 'a') as f:
        f.write('\n<!-- 来自远程实例 -->\n')
        f.writelines(remote_new)
    print(f'  🔀 合并: $fname (+{len(remote_new)} 行)')
" 2>&1
    fi
done

# 远程缺失的 → 推过去
for f in "$LOCAL_WS/memory/"*.md; do
    [ -f "$f" ] || continue
    fname=$(basename "$f")
    if [ ! -f "$TMP_DIR/remote-memory/$fname" ]; then
        scp "$f" "$REMOTE:$REMOTE_WS/memory/$fname"
        echo "  📤 推送: $fname"
    fi
done

# 4. 推送合并后的 MEMORY.md 回远程
echo "📤 推送合并后的 MEMORY.md..."
scp "$TMP_DIR/merged-remote-MEMORY.md" "$REMOTE:$REMOTE_WS/MEMORY.md" 2>/dev/null || true

# 5. 清理
rm -rf "$TMP_DIR"

echo ""
echo "✅ 记忆同步完成！"
