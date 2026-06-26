#!/usr/bin/env bash
# ========== harness-compress.sh ==========
# MEMORY 压缩库（当前实现基础压缩，子章节拆分待扩展）

# 压缩 MEMORY.md：清理重复条目 & 归档旧内容
# 用法：compress_memory <memory_file>
compress_memory() {
    local mem_file="${1:-MEMORY.md}"
    [[ ! -f "$mem_file" ]] && return 0

    local size_before=$(stat -c%s "$mem_file" 2>/dev/null || echo 0)
    local tmp=$(mktemp)

    # 基础清理：删除空行、尾部空白（不改变语义）
    sed '/^[[:space:]]*$/d' "$mem_file" | sed 's/[[:space:]]*$//' > "$tmp"

    # 如果清理后变小则替换，否则保留原文件
    local size_after=$(stat -c%s "$tmp" 2>/dev/null || echo 0)
    if [[ "$size_after" -lt "$size_before" ]]; then
        mv "$tmp" "$mem_file"
        return 0
    else
        rm -f "$tmp"
        return 1
    fi
}
