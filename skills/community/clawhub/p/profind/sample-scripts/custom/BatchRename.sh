#!/bin/bash
#===============================================================================
# BatchRename.sh — ProFind 批量重命名脚本
#
# 功能：将文件名中的空格替换为下划线
# 安装：复制到 ~/Library/Scripts/ProFind/
# 使用：ProFind 选中多个文件 → Scripts → BatchRename
#============================================================================---

for file in "$@"; do
    filename=$(basename "$file")
    dirname=$(dirname "$file")

    # 替换空格为下划线
    newname=$(echo "$filename" | sed 's/ /_/g')

    if [ "$newname" != "$filename" ]; then
        mv "$file" "$dirname/$newname"
        echo "✓ $filename → $newname"
    else
        echo "· $filename （无需重命名）"
    fi
done

echo ""
echo "完成！共处理 $# 个文件。"
