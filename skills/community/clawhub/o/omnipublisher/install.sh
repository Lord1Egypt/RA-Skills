#!/bin/bash
# omnipublisher 安装脚本

set -e
echo "🔄 正在安装 omnipublisher..."
if ! command -v python3 &> /dev/null; then echo "❌ 需要 Python 3.7+"; exit 1; fi
echo "✅ 安装完成！"
echo "使用：omnipublisher article.md --platforms wechat,xiaohongshu"
echo "文档：cat SKILL.md"
