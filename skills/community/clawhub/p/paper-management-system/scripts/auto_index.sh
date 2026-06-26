#!/bin/bash
#=============================================================================
# Paper Management System - Auto Index Script
#
# 功能：增量索引 + 自动移动下载文件 + 全文提取 + AI提炼
# 配置：通过环境变量 PAPERMGR_* 设置，或使用默认值（相对于项目目录）
#=============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Default values relative to project directory
PAPERS_DIR="${PAPERMGR_PAPERS_DIR:-${PROJECT_DIR}/papers}"
DOWNLOADS_DIR="${PAPERMGR_DOWNLOADS_DIR:-${PROJECT_DIR}/downloads}"
DB_PATH="${PAPERMGR_DATABASE_PATH:-${PROJECT_DIR}/data/index.db}"
LOG="${PAPERMGR_LOGGING_PATH:-${PROJECT_DIR}/logs/auto_index.log}"

mkdir -p "$(dirname "$LOG")" 2>/dev/null || true
mkdir -p "$PAPERS_DIR" 2>/dev/null || true
mkdir -p "$(dirname "$DB_PATH")" 2>/dev/null || true

cd "$PAPERS_DIR"

#=============================================================================
# Step 1: 从 Downloads 目录移动新PDF文件
#=============================================================================
MOVED_COUNT=0
for f in "$DOWNLOADS_DIR"/*.pdf 2>/dev/null; do
    if [ -f "$f" ]; then
        if [[ "$(basename "$f")" == *"科研通"* ]] || [[ "$(basename "$f")" == *"ablesci"* ]]; then
            FILE_HASH=$(md5sum "$f" | awk '{print $1}')
            EXISTS=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM papers WHERE file_hash='$FILE_HASH';" 2>/dev/null || echo "0")
            
            if [ "$EXISTS" = "0" ]; then
                mv "$f" "$PAPERS_DIR/"
                echo "[$(date)] 移动文件: $(basename "$f")" >> "$LOG"
                ((MOVED_COUNT++))
            else
                echo "[$(date)] 跳过已存在: $(basename "$f")" >> "$LOG"
                rm -f "$f"
            fi
        fi
    fi
done

if [ "$MOVED_COUNT" -gt 0 ]; then
    echo "[$(date)] 从Downloads移动了 $MOVED_COUNT 个新文件" >> "$LOG"
fi

#=============================================================================
# Step 2: 检测并索引新文件
#=============================================================================
NEW_COUNT=$(python3 -c "
import sys
sys.path.insert(0, '$PROJECT_DIR/scripts')
from config import get_config
from paper_manager import get_db
import hashlib, glob

cfg = get_config()
conn = get_db()
indexed = set(r[0] for r in conn.execute('SELECT file_hash FROM papers').fetchall())
new = 0
for f in glob.glob(cfg.papers_dir + '/*.pdf'):
    try:
        h = hashlib.md5(open(f,'rb').read()).hexdigest()
        if h not in indexed:
            new += 1
    except:
        pass
conn.close()
print(new)
" 2>/dev/null || echo "0")

if [ "$NEW_COUNT" -gt 0 ]; then
    echo "[$(date)] 发现 $NEW_COUNT 个新文件，开始索引..." >> "$LOG"
    
    python3 "${PROJECT_DIR}/scripts/paper_manager.py" index >> "$LOG" 2>&1
    python3 "${PROJECT_DIR}/scripts/paper_manager.py" rename >> "$LOG" 2>&1
    python3 "${PROJECT_DIR}/scripts/extract_fulltext.py" >> "$LOG" 2>&1

    if python3 -c "
import sys
sys.path.insert(0, '$PROJECT_DIR/scripts')
from config import get_config
cfg = get_config()
print('true' if cfg.ai_enabled else 'false')
" 2>/dev/null | grep -q "true"; then
        echo "[$(date)] 开始AI提炼..." >> "$LOG"
        python3 "${PROJECT_DIR}/scripts/ai_summarize.py" >> "$LOG" 2>&1
    fi

    echo "[$(date)] 索引+全文+AI提炼完成" >> "$LOG"
else
    echo "[$(date)] 没有新文件" >> "$LOG"
fi
