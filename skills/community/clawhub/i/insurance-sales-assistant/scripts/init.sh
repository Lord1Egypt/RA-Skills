#!/bin/bash

# 销售行为管理助手 - 自动初始化脚本
# 用于首次安装时创建飞书资源

set -e

echo "🚀 销售行为管理助手 - 自动初始化"
echo "================================"
echo ""

# 检查飞书 CLI 是否安装
if ! command -v feishu &> /dev/null; then
    echo "❌ 错误：飞书 CLI 未安装"
    echo "请先安装飞书 CLI 或确保飞书 API 可用"
    exit 1
fi

# 创建配置文件目录
CONFIG_DIR="~/.openclaw/workspace"
CONFIG_FILE="$CONFIG_DIR/sales-assistant-config.json"

echo "📁 配置文件路径：$CONFIG_FILE"
echo ""

# 创建暖客池多维表格
echo "📊 创建暖客池多维表格..."
WARM_POOL_APP=$(feishu_bitable_app create --name "🔥 暖客池管理系统" --format json)
WARM_POOL_TOKEN=$(echo $WARM_POOL_APP | jq -r '.app.app_token')
echo "✅ 暖客池已创建：$WARM_POOL_TOKEN"

# 创建约访管理多维表格
echo "📅 创建约访管理多维表格..."
VISIT_APP=$(feishu_bitable_app create --name "📅 约访管理系统" --format json)
VISIT_TOKEN=$(echo $VISIT_APP | jq -r '.app.app_token')
echo "✅ 约访管理已创建：$VISIT_TOKEN"

# 创建业绩追踪多维表格
echo "🏆 创建业绩追踪多维表格..."
PERF_APP=$(feishu_bitable_app create --name "🏆 业绩追踪系统" --format json)
PERF_TOKEN=$(echo $PERF_APP | jq -r '.app.app_token')
echo "✅ 业绩追踪已创建：$PERF_TOKEN"

# 创建冷启动模板文档
echo "📝 创建冷启动模板文档..."
COLD_START_DOC=$(feishu_create_doc --title "🔥 暖客池 - 冷启动模板" --markdown-file "templates/cold-start.md")
COLD_START_ID=$(echo $COLD_START_DOC | jq -r '.doc_id')
echo "✅ 冷启动模板已创建：$COLD_START_ID"

# 创建朋友圈素材库文档
echo "📝 创建朋友圈素材库..."
MOMENT_DOC=$(feishu_create_doc --title "📝 朋友圈素材库" --markdown-file "templates/moment-library.md")
MOMENT_ID=$(echo $MOMENT_DOC | jq -r '.doc_id')
echo "✅ 朋友圈素材库已创建：$MOMENT_ID"

# 生成配置文件
echo ""
echo "💾 生成配置文件..."

cat > $CONFIG_FILE << EOF
{
  "initialized": true,
  "init_date": "$(date -Iseconds)",
  "version": "1.1.0",
  "resources": {
    "bitable": {
      "warm_pool": "$WARM_POOL_TOKEN",
      "visit_tracking": "$VISIT_TOKEN",
      "performance": "$PERF_TOKEN"
    },
    "docs": {
      "cold_start_template": "$COLD_START_ID",
      "moment_library": "$MOMENT_ID"
    },
    "forms": {
      "daily_sales": "pending",
      "weekly_review": "pending",
      "monthly_review": "pending"
    }
  },
  "settings": {
    "warmup_count": 3,
    "visit_target": 5,
    "moment_frequency": 5,
    "push_time": "09:30",
    "review_time": "20:00"
  }
}
EOF

echo "✅ 配置文件已生成：$CONFIG_FILE"
echo ""
echo "🎉 初始化完成！"
echo ""
echo "📋 下一步："
echo "1. 打开冷启动模板文档，填写 10-20 个客户信息"
echo "2. 发回给助手批量导入到暖客池"
echo "3. 配置 Cron 定时任务"
echo "4. 明天开始接收每日任务包！"
echo ""
echo "📚 资源链接已保存到：$CONFIG_FILE"
