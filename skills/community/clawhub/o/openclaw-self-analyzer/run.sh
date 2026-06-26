#!/bin/bash
# OpenClaw 自分析一键运行脚本

echo "=== OpenClaw 自分析工具 ==="
echo ""

cd /root/.openclaw/workspace/skills/openclaw-self-analyzer

# 1. 运行架构分析
echo "1️⃣ 运行架构分析..."
python3 core/architecture_analyzer.py

echo ""
echo "2️⃣ 生成钩子..."
python3 generators/hook_generator.py

echo ""
echo "3️⃣ 生成报告..."
python3 reporters/report_generator.py

echo ""
echo "✅ 分析完成！"
echo ""
echo "📄 查看结果:"
echo "  - 架构映射: /root/.openclaw/workspace/openclaw_architecture.json"
echo "  - 详细报告: /root/.openclaw/workspace/skills/openclaw-self-analyzer/reports/"
echo "  - 生成的钩子: /root/.openclaw/workspace/skills/openclaw-self-analyzer/generated_hooks/"
