#!/bin/bash

# OpenMAIC PPT导出工具测试脚本

echo "🧪 测试OpenMAIC PPT导出工具"
echo "================================"

# 检查OpenMAIC目录
OPENMAIC_PATH="$HOME/.openclaw/workspace/OpenMAIC"
if [ ! -d "$OPENMAIC_PATH" ]; then
    echo "❌ OpenMAIC目录不存在: $OPENMAIC_PATH"
    exit 1
fi

echo "✅ OpenMAIC目录: $OPENMAIC_PATH"

# 检查课程目录
CLASSROOMS_PATH="$OPENMAIC_PATH/data/classrooms"
if [ ! -d "$CLASSROOMS_PATH" ]; then
    echo "❌ 课程目录不存在: $CLASSROOMS_PATH"
    exit 1
fi

echo "✅ 课程目录: $CLASSROOMS_PATH"

# 检查课程文件
COURSE_FILE="$CLASSROOMS_PATH/LLFqDUArdk.json"
if [ ! -f "$COURSE_FILE" ]; then
    echo "❌ 课程文件不存在: $COURSE_FILE"
    exit 1
fi

echo "✅ 课程文件: $COURSE_FILE"

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js未安装"
    exit 1
fi

echo "✅ Node.js版本: $(node --version)"

# 检查pptxgenjs
cd "$OPENMAIC_PATH"
if ! npm list pptxgenjs &> /dev/null; then
    echo "⚠️  pptxgenjs未安装，正在安装..."
    npm install pptxgenjs
    if [ $? -ne 0 ]; then
        echo "❌ 安装pptxgenjs失败"
        exit 1
    fi
    echo "✅ pptxgenjs已安装"
else
    echo "✅ pptxgenjs已安装"
fi

# 运行导出脚本
echo ""
echo "🚀 运行导出脚本..."
cd "$(dirname "$0")"
node export_ppt.js LLFqDUArdk

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 测试成功！"
    
    # 检查生成的PPT文件
    PPT_FILES=$(ls -la *.pptx 2>/dev/null | wc -l)
    if [ $PPT_FILES -gt 0 ]; then
        echo "📁 生成的PPT文件:"
        ls -la *.pptx
        echo ""
        echo "✅ 技能正常工作！"
    else
        echo "⚠️  未找到生成的PPT文件"
    fi
else
    echo ""
    echo "❌ 测试失败"
    exit 1
fi