#!/bin/bash
# PRD项目初始化脚本
# 创建完整的PRD项目骨架
#
# 用法：bash init-prd.sh <项目目录> <产品名称>
# 示例：bash init-prd.sh ./prd-learning "学习打卡App"

set -e

PROJECT_DIR="${1:?用法: bash init-prd.sh <项目目录> <产品名称>}"
PRODUCT_NAME="${2:?请提供产品名称}"
TODAY=$(date +%Y-%m-%d)

# 转换产品名为文件名格式（小写，空格转横线）
PRODUCT_SLUG=$(echo "$PRODUCT_NAME" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
TEMPLATES_DIR="$SKILL_DIR/templates"

if [ -d "$PROJECT_DIR" ] && [ "$(ls -A "$PROJECT_DIR" 2>/dev/null)" ]; then
  echo "❌ 目录已存在且非空: $PROJECT_DIR"
  exit 1
fi

echo "📦 初始化PRD项目: $PRODUCT_NAME"
echo "   目录: $PROJECT_DIR"
echo "   标识: $PRODUCT_SLUG"
echo ""

# 创建目录结构
mkdir -p "$PROJECT_DIR"/{fragments,output,versions,research}

# 复制模板文件
cp "$TEMPLATES_DIR/styles.css" "$PROJECT_DIR/styles.css"
cp "$TEMPLATES_DIR/build.js" "$PROJECT_DIR/build.js"
cp "$TEMPLATES_DIR/build-pdf.js" "$PROJECT_DIR/build-pdf.js"
cp "$TEMPLATES_DIR/update.sh" "$PROJECT_DIR/update.sh"
chmod +x "$PROJECT_DIR/update.sh"

# 复制HTML片段模板
if [ -d "$TEMPLATES_DIR/fragments" ]; then
  cp "$TEMPLATES_DIR/fragments/"*.html "$PROJECT_DIR/fragments/" 2>/dev/null || true
fi

# 创建 version.json
cat > "$PROJECT_DIR/version.json" << EOF
{
  "version": "1.0.0",
  "build": 0,
  "lastUpdate": "$TODAY",
  "title": "prd-${PRODUCT_SLUG}",
  "productName": "$PRODUCT_NAME"
}
EOF

# 创建 CHANGELOG.md
cat > "$PROJECT_DIR/CHANGELOG.md" << EOF
# $PRODUCT_NAME PRD 更新日志

> 格式：\`[版本号] YYYY-MM-DD — 摘要\`
EOF

# 创建 PROJECT.md
cat > "$PROJECT_DIR/PROJECT.md" << EOF
# $PRODUCT_NAME — PRD项目

> 产品标识：$PRODUCT_SLUG
> 状态：🟡 规划中
> 创建日期：$TODAY

---

## 产品信息

| 项目 | 内容 |
|------|------|
| 产品名称 | $PRODUCT_NAME |
| 产品类型 | （待识别） |
| 目标用户 |  |
| 核心痛点 |  |
| 核心价值 |  |

---

## PRD章节进度

| 章节 | 文件名 | 状态 | 备注 |
|------|--------|------|------|
| 封面 | 00-cover.html | ⏳ |  |
| 目录 | 01-toc.html | ⏳ |  |
| 概述 | 02-overview.html | ⏳ |  |
| 需求列表 | 03-requirements.html | ⏳ |  |
| 用户故事 | 04-user-stories.html | ⏳ |  |
| 功能规格 | 05-functional.html | ⏳ | 含流程图 |
| 交互说明 | 06-interaction.html | ⏳ |  |
| 数据埋点 | 07-data.html | ⏳ | 自动标准埋点 |
| 非功能需求 | 08-nonfunctional.html | ⏳ |  |
| 尾页 | 99-backpage.html | ⏳ |  |

---

## 迭代记录

| 版本 | 日期 | 变更内容 |
|------|------|----------|
| v1.0.0 | $TODAY | 初版创建 |

---

## AI生成提示

当用户描述产品想法后，执行以下步骤：

1. **需求分析**：提取5W2H，识别产品类型
2. **选择模板**：根据产品类型加载对应配置
3. **并行写作**：启动各章节Agent生成内容
4. **文档组装**：合并为完整PRD
5. **格式转换**：输出PDF + HTML + Markdown

如需迭代：用户可指定章节更新或描述新增内容
EOF

echo "✅ PRD项目创建成功！"
echo ""
echo "📁 项目结构:"
echo "   $PROJECT_DIR/"
echo "   ├── PROJECT.md          # 项目信息"
echo "   ├── version.json        # 版本信息"
echo "   ├── CHANGELOG.md        # 更新日志"
echo "   ├── build.js            # HTML构建脚本"
echo "   ├── build-pdf.js        # PDF生成脚本"
echo "   ├── update.sh           # 版本更新脚本"
echo "   ├── styles.css          # 共享样式"
echo "   ├── fragments/          # PRD内容片段"
echo "   ├── output/             # 输出目录"
echo "   └── research/           # 调研资料"
echo ""
echo "🚀 下一步：在Claude对话中描述你的产品想法，AI将自动生成完整PRD"
