#!/bin/bash
#
# Good-Memory 安装脚本 v2.0.0
# 开箱即用版：安装后自动生效，无需任何配置
#

set -e

# 支持环境变量自定义路径
OPENCLAW_BASE="${OPENCLAW_BASE:-/root/.openclaw}"
SKILL_DIR="${SKILL_DIR:-${OPENCLAW_BASE}/workspace/skills/good-memory}"
TRACKER_FILE="${TRACKER_FILE:-${OPENCLAW_BASE}/workspace/session-tracker.json}"
AGENTS_MD="${AGENTS_MD:-${OPENCLAW_BASE}/workspace/AGENTS.md}"
SESSIONS_DIR="${SESSIONS_DIR:-${OPENCLAW_BASE}/agents/main/sessions}"

echo "=== Good-Memory 安装脚本 v2.0.0 ==="
echo "📦 开箱即用版，安装后自动生效"
echo ""

# 确保脚本有执行权限
chmod +x "${SKILL_DIR}/scripts/"*.sh
chmod +x "${SKILL_DIR}/scripts/"*.py

# ============================================
# 第一部分：初始化 tracker
# ============================================

echo "[1/3] 初始化 session-tracker..."

if [[ ! -f "$TRACKER_FILE" ]]; then
    mkdir -p "$(dirname "$TRACKER_FILE")"
    cat > "$TRACKER_FILE" << 'EOF'
{
  "description": "Session tracker - maps agent+chat to session files",
  "last_updated": "",
  "agents": {}
}
EOF
    echo "  ✅ 创建 tracker 文件: $TRACKER_FILE"
else
    echo "  ✅ tracker 文件已存在"
fi

# 扫描所有活跃session，初始化到tracker
echo ""
echo "  🔍 从sessions.json读取所有会话元数据..."
python3 << 'PYEOF'
import json
import os
from datetime import datetime, timezone

tracker_file = "/root/.openclaw/workspace/session-tracker.json"
sessions_json_path = "/root/.openclaw/agents/main/sessions/sessions.json"
sessions_dir = "/root/.openclaw/agents/main/sessions"

# 读取tracker
with open(tracker_file, 'r') as f:
    tracker = json.load(f)

added_count = 0

# 优先从sessions.json读取，100%准确
if os.path.exists(sessions_json_path):
    try:
        with open(sessions_json_path, 'r') as f:
            sessions_data = json.load(f)
        
        for session_key, info in sessions_data.items():
            # session_key格式: agent:{agent}:{channel}:{chat_type}:{chat_id}
            parts = session_key.split(':')
            if len(parts) < 5:
                continue
            
            agent = parts[1]
            chat_id = parts[-1]
            session_id = info.get('sessionId', '')
            session_file = info.get('sessionFile', '')
            
            # 构造session文件路径
            if not session_file and session_id:
                session_file = os.path.join(sessions_dir, f"{session_id}.jsonl")
            
            # 检查文件是否存在且不是reset文件
            if not os.path.exists(session_file) or '.reset.' in session_file:
                continue
            
            # 写入tracker
            if agent not in tracker["agents"]:
                tracker["agents"][agent] = {}
            if chat_id not in tracker["agents"][agent]:
                tracker["agents"][agent][chat_id] = {
                    "session_key": session_key,
                    "active": session_file,
                    "active_uuid": session_id,
                    "last_history": "",
                    "history": []
                }
                print(f"  ✅ {agent}/{chat_id}: {session_id}")
                added_count += 1
    
    except Exception as e:
        print(f"  读取sessions.json失败: {e},  fallback到文件扫描")
else:
    print("  sessions.json不存在，fallback到文件扫描")

# 如果sessions.json不可用，fallback到文件扫描
if added_count == 0:
    import re
    session_key_pattern = re.compile(r'agent:([a-zA-Z0-9_-]+):([a-zA-Z0-9_-]+):([a-zA-Z0-9_-]+):([a-zA-Z0-9_-]+)')
    
    if os.path.exists(sessions_dir):
        for f in os.listdir(sessions_dir):
            if f.endswith('.jsonl') and not any(s in f for s in ('.reset.', '.deleted.', '.lock')):
                filepath = os.path.join(sessions_dir, f)
                uuid = f.split('.')[0]
                
                # 读取前100行，寻找session_key
                session_key = ""
                chat_id = ""
                agent = "main"
                
                try:
                    with open(filepath, 'r') as file:
                        for i, line in enumerate(file):
                            if i >= 100:
                                break
                            match = session_key_pattern.search(line)
                            if match:
                                session_key = match.group(0)
                                break
                except:
                    continue
                
                if session_key:
                    parts = session_key.split(':')
                    if len(parts) >= 5:
                        agent = parts[1]
                        chat_id = parts[-1]
                        
                        if agent not in tracker["agents"]:
                            tracker["agents"][agent] = {}
                        if chat_id not in tracker["agents"][agent]:
                            tracker["agents"][agent][chat_id] = {
                                "session_key": session_key,
                                "active": filepath,
                                "active_uuid": uuid,
                                "last_history": "",
                                "history": []
                            }
                            print(f"  ✅ {agent}/{chat_id}: {uuid}")
                            added_count += 1

# 更新时间
tracker["last_updated"] = datetime.now(timezone.utc).isoformat()

# 写回tracker
with open(tracker_file, 'w') as f:
    json.dump(tracker, f, indent=2, ensure_ascii=False)

print(f"\n  扫描完成，共找到 {added_count} 个活跃会话")
PYEOF

# ============================================
# 第二部分：注入自动执行指令到 AGENTS.md
# ============================================

echo ""
echo "[2/3] 注入自动恢复指令到 AGENTS.md..."

# 检查是否已有Good-Memory指令
if grep -q "Good-Memory 会话记忆恢复" "$AGENTS_MD" 2>/dev/null; then
    echo "  ✅ Good-Memory 指令已存在，跳过注入"
else
    # 注入自动执行指令到AGENTS.md最开头
    TMP_FILE=$(mktemp)
    cat > "$TMP_FILE" << 'EOF'
# Good-Memory 会话记忆恢复
> 自动运行，无需手动操作，重置后自动恢复上下文

**Session Startup 自动执行：**
```bash
# 自动检测重置并恢复上下文，输出会自动加入到对话开头
python3 /root/.openclaw/workspace/skills/good-memory/scripts/autorecover.py
```

## 功能说明
- ✅ 自动检测所有类型的重置（系统自动重置 /new /reset）
- ✅ 重置后自动恢复上一段对话的最后30条记录
- ✅ 首条回复自动提示：「已自动恢复 上次会话的对话记录 📜 如果想要回忆更早的请对我说」
- ✅ 全平台支持，无需任何配置

## 手动命令（可选）
```bash
# 手动检测重置
bash /root/.openclaw/workspace/skills/good-memory/scripts/maintenance.sh detect <agent_name> <chat_id>

# 手动恢复历史
bash /root/.openclaw/workspace/skills/good-memory/scripts/recovery.sh read --lines 50
```

---
EOF
    # 插入到文件开头
    cat "$TMP_FILE" "$AGENTS_MD" > "${AGENTS_MD}.new" && mv "${AGENTS_MD}.new" "$AGENTS_MD"
    rm -f "$TMP_FILE"
    echo "  ✅ 自动恢复指令已注入到: $AGENTS_MD"
fi

# ============================================
# 第三部分：完成提示
# ============================================

echo ""
echo "[3/3] 安装完成！🎉"
echo ""
echo "✅ 现在已经可以正常使用了，无需任何额外配置！"
echo ""
echo "📝 效果："
echo "  • Session重置后会自动恢复上下文"
echo "  • 首条回复会提示已恢复历史记录"
echo "  • 完全自动，用户感知不到任何操作"
echo ""
echo "🔧 环境变量（可选）："
echo "export OPENCLAW_BASE=\"/path/to/your/openclaw\"  # 自定义OpenClaw安装路径"
