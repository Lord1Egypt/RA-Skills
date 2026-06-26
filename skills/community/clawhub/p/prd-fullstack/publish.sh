#!/bin/bash

# 简单发布脚本
echo "🚀 PRD FullStack Skill 准备发布"
echo "================================="

# 检查必要文件
echo "📋 检查必要文件..."
REQUIRED_FILES=("SKILL.md" "README.md" "COLLABORATION.md" "package.json")
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ 缺少: $file"
        exit 1
    fi
done

# 检查目录
echo "📁 检查目录结构..."
REQUIRED_DIRS=("prompts" "templates" "templates-config" "examples")
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✅ $dir/"
    else
        echo "  ❌ 缺少目录: $dir"
        exit 1
    fi
done

echo ""
echo "✅ 所有检查通过！"
echo ""
echo "📦 发布信息："
echo "  Skill名称: prd-fullstack"
echo "  版本号: v1.0.0"
echo "  发布日期: $(date +'%Y-%m-%d')"
echo ""
echo "🚀 下一步："
echo "1. 登录 ClawHub: https://clawhub.ai/dashboard"
echo "2. 点击 'Upload New Skill'"
echo "3. 上传整个 prd-skill-workflow 文件夹"
echo "4. 填写表单："
echo "   - Slug: prd-fullstack"
echo "   - Display name: PRD FullStack Skill"
echo "   - Version: 1.0.0"
echo "   - Tags: prd, product, documentation, workflow, collaboration"
echo "5. 勾选许可协议"
echo "6. 填写Changelog（使用以下内容）："
echo ""
echo "PRD FullStack Skill v1.0.0 初始版本发布"
echo ""
echo "核心功能："
echo "• 完整的10步协作流程：从需求探索到项目计划"
echo "• 14章专业PRD结构：覆盖产品全维度"
echo "• 6种产品类型支持：SaaS/电商/教育/社交/内容/工具"
echo "• HTML/PDF双输出：一键生成专业文档"
echo "• 对话式协作体验：自然对话引导"
echo ""
echo "技术特性："
echo "• 模块化模板系统"
echo "• 版本管理"
echo "• 质量保证审查清单"
echo "• 示例项目包含"
echo ""
echo "7. 点击 'Publish skill'"
echo ""
echo "🎯 祝发布顺利！"