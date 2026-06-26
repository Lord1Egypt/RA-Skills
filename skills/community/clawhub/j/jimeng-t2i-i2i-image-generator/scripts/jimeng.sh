#!/bin/bash
# jimeng.sh - Jimeng AI 4.0 (Volcengine) 图片生成
# 支持文生图和图生图两种模式

# 默认配置
DEFAULT_REFERENCE_IMAGE="https://cdn.jsdelivr.net/gh/SumeLabs/clawra@main/assets/clawra.png"
SCRIPT_DIR="$(dirname "$0")"

SUBMIT_URL="https://visual.volcengineapi.com"
QUERY_URL="https://visual.volcengineapi.com"

# 生成签名
generate_auth_header() {
    local ak="$1"
    local sk="$2"
    local method="$3"
    local path="$4"
    local query="$5"
    local body="$6"
    
    "$SCRIPT_DIR/sign.py" "$ak" "$sk" "$method" "$path" "$query" "$body"
}

# 提交任务
submit_task() {
    local prompt="$1"
    local image_url="$2"
    local force_single="$3"
    
    local method="POST"
    local path="/"
    local query="Action=CVSync2AsyncSubmitTask&Version=2022-08-31"
    
    # 构建请求体
    local req_body
    if [ -n "$image_url" ]; then
        # 图生图模式
        req_body="{\"req_key\":\"jimeng_t2i_v40\",\"prompt\":\"$prompt\",\"image_urls\":[\"$image_url\"],\"force_single\":$force_single}"
    else
        # 文生图模式
        req_body="{\"req_key\":\"jimeng_t2i_v40\",\"prompt\":\"$prompt\",\"force_single\":$force_single}"
    fi
    
    local auth_info=$(generate_auth_header "$VOLCENGINE_AK" "$VOLCENGINE_SK" "$method" "$path" "$query" "$req_body")
    
    local current_date=$(echo "$auth_info" | head -1)
    local payload_hash=$(echo "$auth_info" | head -2 | tail -1)
    local authorization=$(echo "$auth_info" | tail -1)
    
    local response=$(curl -s -X POST "$SUBMIT_URL?$query" \
        -H "Content-Type: application/json" \
        -H "Host: visual.volcengineapi.com" \
        -H "X-Date: $current_date" \
        -H "X-Content-SHA256: $payload_hash" \
        -H "Authorization: $authorization" \
        -d "$req_body")
    
    echo "$response"
}

# 查询结果
query_task() {
    local task_id="$1"
    
    local method="POST"
    local path="/"
    local query="Action=CVSync2AsyncGetResult&Version=2022-08-31"
    
    local req_body="{\"req_key\":\"jimeng_t2i_v40\",\"task_id\":\"$task_id\",\"req_json\":\"{\\\"return_url\\\":true}\"}"
    
    local auth_info=$(generate_auth_header "$VOLCENGINE_AK" "$VOLCENGINE_SK" "$method" "$path" "$query" "$req_body")
    
    local current_date=$(echo "$auth_info" | head -1)
    local payload_hash=$(echo "$auth_info" | head -2 | tail -1)
    local authorization=$(echo "$auth_info" | tail -1)
    
    local response=$(curl -s -X POST "$QUERY_URL?$query" \
        -H "Content-Type: application/json" \
        -H "Host: visual.volcengineapi.com" \
        -H "X-Date: $current_date" \
        -H "X-Content-SHA256: $payload_hash" \
        -H "Authorization: $authorization" \
        -d "$req_body")
    
    echo "$response"
}

# 等待结果
wait_for_result() {
    local task_id="$1"
    local max_attempts=60
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        local result=$(query_task "$task_id")
        local status=$(echo "$result" | grep -o '"status"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*"\([^"]*\)".*/\1/')
        
        echo "Attempt $((attempt + 1)): status = $status"
        
        if [ "$status" == "done" ]; then
            local code=$(echo "$result" | grep -o '"code"[[:space:]]*:[[:space:]]*[0-9]*' | head -1 | sed 's/.*: *//')
            if [ "$code" == "10000" ]; then
                local image_url=$(echo "$result" | grep -o '"image_urls"[[:space:]]*:[[:space:]]*\["[^"]*"\]' | sed 's/.*"\([^"]*\)".*/\1/')
                if [ -n "$image_url" ] && [ "$image_url" != "null" ]; then
                    echo "$result"
                    return 0
                fi
            fi
            echo "$result"
            return 1
        elif [ "$status" == "failed" ] || [ "$status" == "not_found" ] || [ "$status" == "expired" ]; then
            echo "Task failed: $result"
            return 1
        fi
        
        sleep 2
        attempt=$((attempt + 1))
    done
    
    echo "Timeout waiting for task"
    return 1
}

# 发送图片到飞书
send_to_feishu() {
    local image_url="$1"
    local caption="$2"
    local target="$3"
    
    if [ -n "$target" ]; then
        curl -s -X POST "http://localhost:18789/message" \
            -H "Content-Type: application/json" \
            -d "{
                \"action\": \"send\",
                \"channel\": \"feishu\",
                \"target\": \"$target\",
                \"message\": \"$caption\",
                \"media\": \"$image_url\"
            }" 2>/dev/null
    else
        echo "图片已生成: $image_url"
    fi
}

# 主函数
main() {
    local mode="$1"           # t2i (文生图) 或 i2i (图生图)
    local prompt="$2"         # 描述
    local reference_url="$3"  # 参考图片 (图生图模式)
    local target="$4"         # 发送目标
    local extra_opts="$5"      # 额外选项
    
    # 参数检查
    if [ -z "$mode" ] || [ -z "$prompt" ]; then
        echo "用法: $0 <mode> <prompt> [reference_url] [target] [options]"
        echo ""
        echo "参数说明:"
        echo "  mode           : t2i (文生图) 或 i2i (图生图)"
        echo "  prompt         : 图片描述"
        echo "  reference_url  : 参考图片URL (i2i模式必填, t2i模式可选)"
        echo "  target         : 飞书用户ID (可选，不填则只输出URL)"
        echo "  options        : 额外选项如 force_single=true"
        echo ""
        echo "示例:"
        echo "  # 文生图"
        echo "  $0 t2i \"一只可爱的猫咪\""
        echo "  $0 t2i \"蓝天白云\" user:ou_xxx"
        echo ""
        echo "  # 图生图 (使用默认参考图)"
        echo "  $0 i2i \"变成卡通风格\""
        echo "  $0 i2i \"戴上墨镜\""
        echo ""
        echo "  # 图生图 (自定义参考图)"
        echo "  $0 i2i \"变成油画风格\" https://example.com/ref.jpg"
        exit 1
    fi
    
    # 环境变量检查
    if [ -z "$VOLCENGINE_AK" ] || [ -z "$VOLCENGINE_SK" ]; then
        echo "Error: 请设置 VOLCENGINE_AK 和 VOLCENGINE_SK 环境变量"
        exit 1
    fi
    
    # 处理选项
    local force_single="false"
    if echo "$extra_opts" | grep -q "force_single"; then
        force_single="true"
    fi
    
    # 确定参考图
    local ref_image=""
    if [ "$mode" == "i2i" ]; then
        if [ -n "$reference_url" ]; then
            ref_image="$reference_url"
        else
            ref_image="$DEFAULT_REFERENCE_IMAGE"
        fi
    fi
    
    echo "========== Jimeng AI 4.0 =========="
    echo "模式: $mode"
    echo "描述: $prompt"
    if [ -n "$ref_image" ]; then
        echo "参考图: $ref_image"
    fi
    echo "===================================="
    echo ""
    echo "提交任务..."
    
    # 提交任务
    local submit_result
    if [ "$mode" == "t2i" ]; then
        # 文生图
        if [ -n "$reference_url" ]; then
            # 使用参考图但模式是t2i
            submit_result=$(submit_task "$prompt" "$reference_url" "$force_single")
        else
            # 纯文生图
            submit_result=$(submit_task "$prompt" "" "$force_single")
        fi
    else
        # 图生图
        submit_result=$(submit_task "$prompt" "$ref_image" "$force_single")
    fi
    
    echo "提交响应: $submit_result"
    
    local task_id=$(echo "$submit_result" | grep -o '"task_id"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"\([^"]*\)".*/\1/')
    
    if [ -z "$task_id" ] || [ "$task_id" == "null" ]; then
        echo "Error: 获取task_id失败"
        echo "$submit_result"
        exit 1
    fi
    
    echo "任务ID: $task_id"
    echo "等待生成结果..."
    
    # 等待结果
    local final_result=$(wait_for_result "$task_id")
    
    local image_url=$(echo "$final_result" | grep -o '"image_urls"[[:space:]]*:[[:space:]]*\["[^"]*"\]' | sed 's/.*"\([^"]*\)".*/\1/')
    
    if [ -z "$image_url" ] || [ "$image_url" == "null" ]; then
        echo "Error: 获取图片URL失败"
        echo "$final_result"
        exit 1
    fi
    
    echo ""
    echo "========== 完成 =========="
    echo "图片URL: $image_url"
    echo "========================="
    
    # 发送到飞书
    if [ -n "$target" ]; then
        echo "发送到飞书..."
        send_to_feishu "$image_url" "$prompt" "$target"
    fi
    
    echo "$image_url"
}

main "$@"
