#!/bin/bash

# ========================================
# Lovart AI Design Skill - 示例脚本
# ========================================

# 确保已设置 API Key
if [ -z "$LOVART_API_KEY" ]; then
  echo "❌ 错误: 未找到 LOVART_API_KEY 环境变量"
  echo "请先设置: export LOVART_API_KEY='your_api_key_here'"
  exit 1
fi

# API 基础 URL
API_BASE="https://api.lovart.ai/v1"

# ========================================
# 示例 1: 生成产品图片
# ========================================
generate_product_image() {
  echo "📸 生成产品图片..."

  response=$(curl -s -X POST "$API_BASE/design/generate" \
    -H "Authorization: Bearer $LOVART_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "prompt": "Premium wireless headphones product photography, white background, professional studio lighting, commercial grade, 4K resolution",
      "width": 1920,
      "height": 1080,
      "model": "flux"
    }')

  echo "Response: $response"
  task_id=$(echo $response | jq -r '.id')
  echo "✅ 任务 ID: $task_id"
  echo ""
}

# ========================================
# 示例 2: 生成社交媒体广告
# ========================================
generate_social_media_ad() {
  echo "📱 生成社交媒体广告..."

  response=$(curl -s -X POST "$API_BASE/design/generate" \
    -H "Authorization: Bearer $LOVART_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "prompt": "Vibrant summer sale Instagram advertisement, bright sunny colors, beach theme, bold SALE text, energetic composition, 1080x1080",
      "width": 1080,
      "height": 1080,
      "style": "social_media"
    }')

  echo "Response: $response"
  task_id=$(echo $response | jq -r '.id')
  echo "✅ 任务 ID: $task_id"
  echo ""
}

# ========================================
# 示例 3: 检查任务状态
# ========================================
check_status() {
  if [ -z "$1" ]; then
    echo "❌ 请提供任务 ID"
    echo "用法: ./examples.sh check <task_id>"
    exit 1
  fi

  echo "🔍 检查任务状态: $1"

  response=$(curl -s -X GET "$API_BASE/design/$1" \
    -H "Authorization: Bearer $LOVART_API_KEY")

  echo "Response: $response"

  status=$(echo $response | jq -r '.status')
  progress=$(echo $response | jq -r '.progress // 0')

  echo "📊 状态: $status"
  echo "📈 进度: $progress%"

  if [ "$status" = "completed" ]; then
    result_url=$(echo $response | jq -r '.result_url')
    echo "✅ 完成! 下载链接: $result_url"
  fi
  echo ""
}

# ========================================
# 示例 4: 等待任务完成
# ========================================
wait_for_completion() {
  if [ -z "$1" ]; then
    echo "❌ 请提供任务 ID"
    echo "用法: ./examples.sh wait <task_id>"
    exit 1
  fi

  task_id=$1
  echo "⏳ 等待任务完成: $task_id"

  while true; do
    response=$(curl -s -X GET "$API_BASE/design/$task_id" \
      -H "Authorization: Bearer $LOVART_API_KEY")

    status=$(echo $response | jq -r '.status')
    progress=$(echo $response | jq -r '.progress // 0')

    echo -ne "\r进度: $progress% | 状态: $status    "

    if [ "$status" = "completed" ]; then
      echo ""
      result_url=$(echo $response | jq -r '.result_url')
      echo "✅ 完成! 下载链接: $result_url"

      # 可选: 自动下载
      # curl -O $result_url
      break
    elif [ "$status" = "failed" ]; then
      echo ""
      echo "❌ 任务失败"
      break
    fi

    sleep 3
  done
  echo ""
}

# ========================================
# 示例 5: Logo 设计概念
# ========================================
generate_logo_concept() {
  echo "🎨 生成 Logo 设计概念..."

  response=$(curl -s -X POST "$API_BASE/design/generate" \
    -H "Authorization: Bearer $LOVART_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "prompt": "Modern tech company logo concept, minimalist geometric shapes, gradient blue to purple, clean lines, innovative, vector style",
      "width": 1024,
      "height": 1024,
      "style": "minimal"
    }')

  echo "Response: $response"
  task_id=$(echo $response | jq -r '.id')
  echo "✅ 任务 ID: $task_id"
  echo ""
}

# ========================================
# 命令行接口
# ========================================
case "$1" in
  product)
    generate_product_image
    ;;
  social)
    generate_social_media_ad
    ;;
  logo)
    generate_logo_concept
    ;;
  check)
    check_status $2
    ;;
  wait)
    wait_for_completion $2
    ;;
  *)
    echo "========================================"
    echo "Lovart AI Design Skill - 示例脚本"
    echo "========================================"
    echo ""
    echo "用法: ./examples.sh <命令> [参数]"
    echo ""
    echo "命令:"
    echo "  product    - 生成产品图片"
    echo "  social     - 生成社交媒体广告"
    echo "  logo       - 生成 Logo 设计概念"
    echo "  check <id> - 检查任务状态"
    echo "  wait <id>  - 等待任务完成并显示结果"
    echo ""
    echo "示例:"
    echo "  ./examples.sh product"
    echo "  ./examples.sh check abc123def456"
    echo "  ./examples.sh wait abc123def456"
    echo ""
    ;;
esac
