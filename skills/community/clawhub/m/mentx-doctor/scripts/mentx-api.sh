#!/bin/bash
# mentx-doctor API 调用脚本
# 用于调用 Mentx.com 医疗辅助决策接口
# 增强版：异步任务 + 轮询检查，等待期间可提供情绪陪伴

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 临时目录
TEMP_DIR="/tmp/mentx-doctor"
mkdir -p "$TEMP_DIR"

# 检查 API 密钥
check_api_key() {
  if [ -z "$MENTX_API_KEY" ]; then
    echo -e "${RED}错误：未配置 MENTX_API_KEY 环境变量${NC}"
    echo "请先到 https://developer.mentx.com/ 注册并获取 API 密钥"
    echo "然后设置：export MENTX_API_KEY=\"your_key_here\""
    exit 1
  fi
}

# 生成任务 ID
generate_task_id() {
  echo "mentx_$(date +%s)_$$"
}

# 上传文件
upload_file() {
  local file_path="$1"
  local file_name=$(basename "$file_path")
  
  echo -e "${YELLOW}正在上传文件：$file_name${NC}"
  
  response=$(curl -s -X POST "https://developer.mentx.com/v1/files/upload" \
    -H "Authorization: Bearer $MENTX_API_KEY" \
    -F "file=@$file_path" \
    -F "agent=AI-GP-ReportAgent")
  
  echo "$response"
}

# 异步启动报告生成任务（后台运行，立即返回）
start_report_task() {
  local user_message="$1"
  local user_id="$2"
  local files_json="$3"
  local task_id=$(generate_task_id)
  local result_file="$TEMP_DIR/${task_id}.result"
  local status_file="$TEMP_DIR/${task_id}.status"
  
  # 初始状态：running
  echo "running" > "$status_file"
  
  # 构建请求体
  local request_body
  if [ -z "$files_json" ] || [ "$files_json" = "[]" ]; then
    request_body=$(cat <<EOF
{
  "agent": "AI-GP-ReportAgent",
  "userId": "$user_id",
  "messages": [
    {
      "role": "user",
      "content": "$user_message"
    }
  ],
  "stream": false
}
EOF
)
  else
    request_body=$(cat <<EOF
{
  "agent": "AI-GP-ReportAgent",
  "userId": "$user_id",
  "messages": [
    {
      "role": "user",
      "content": "$user_message"
    }
  ],
  "files": $files_json,
  "stream": false
}
EOF
)
  fi
  
  # 后台执行 API 调用
  (
    echo -e "${BLUE}[任务 $task_id] 开始生成医疗报告...${NC}"
    
    response=$(curl -s -X POST "https://developer.mentx.com/v1/chat/completions" \
      -H "Authorization: Bearer $MENTX_API_KEY" \
      -H "Content-Type: application/json" \
      -d "$request_body")
    
    # 保存结果到文件
    echo "$response" > "$result_file"
    echo "completed" > "$status_file"
    
    echo -e "${BLUE}[任务 $task_id] 报告已生成，保存到：$result_file${NC}"
  ) &
  
  # 立即返回任务 ID 和状态文件路径
  echo "{\"task_id\": \"$task_id\", \"status_file\": \"$status_file\", \"result_file\": \"$result_file\"}"
}

# 检查任务状态
check_task_status() {
  local task_id="$1"
  local status_file="$TEMP_DIR/${task_id}.status"
  local result_file="$TEMP_DIR/${task_id}.result"
  
  if [ ! -f "$status_file" ]; then
    echo "{\"status\": \"not_found\", \"message\": \"任务不存在\"}"
    return
  fi
  
  local status=$(cat "$status_file")
  
  if [ "$status" = "completed" ]; then
    # 读取结果并返回
    local result=$(cat "$result_file")
    echo "{\"status\": \"completed\", \"result\": $result}"
    # 清理临时文件
    rm -f "$status_file" "$result_file"
  else
    echo "{\"status\": \"running\", \"message\": \"报告正在生成中，请稍候...\"}"
  fi
}

# 轮询等待结果（带超时）
poll_result() {
  local task_id="$1"
  local timeout="${2:-60}"  # 默认 60 秒超时
  local interval="${3:-3}"  # 默认 3 秒轮询一次
  local elapsed=0
  
  while [ $elapsed -lt $timeout ]; do
    local result=$(check_task_status "$task_id")
    local status=$(echo "$result" | grep -o '"status": *"[^"]*"' | cut -d'"' -f4)
    
    if [ "$status" = "completed" ]; then
      echo "$result"
      return 0
    elif [ "$status" = "not_found" ]; then
      echo "{\"status\": \"error\", \"message\": \"任务不存在\"}"
      return 1
    fi
    
    # 等待后再次检查
    sleep $interval
    elapsed=$((elapsed + interval))
    echo -e "${BLUE}[轮询] 已等待 ${elapsed}秒，继续检查...${NC}" >&2
  done
  
  echo "{\"status\": \"timeout\", \"message\": \"等待超时，请稍后重试\"}"
  return 1
}

# 检测紧急症状
check_emergency() {
  local message="$1"
  local emergency_keywords="胸痛|剧烈头痛|呼吸困难|大出血|意识不清|昏迷|窒息|心脏骤停|严重外伤|中毒|自杀"
  
  if echo "$message" | grep -qiE "$emergency_keywords"; then
    return 0  # 是紧急情况
  fi
  return 1  # 不是紧急情况
}

# 同步获取报告（旧版，保留兼容）
get_report() {
  local user_message="$1"
  local user_id="$2"
  local files_json="$3"
  
  echo -e "${YELLOW}正在生成医疗辅助分析报告...${NC}"
  echo "（这大约需要 15-30 秒）"
  
  # 启动异步任务
  local task_info=$(start_report_task "$user_message" "$user_id" "$files_json")
  local task_id=$(echo "$task_info" | grep -o '"task_id": *"[^"]*"' | cut -d'"' -f4)
  
  # 轮询等待结果
  poll_result "$task_id" 60 3
}

# 主函数
main() {
  local action="$1"
  shift
  
  case "$action" in
    "check_key")
      check_api_key
      echo -e "${GREEN}API 密钥配置正常${NC}"
      ;;
    "upload")
      check_api_key
      upload_file "$@"
      ;;
    "start")
      # 异步启动任务，立即返回任务 ID
      check_api_key
      start_report_task "$@"
      ;;
    "check")
      # 检查任务状态
      check_task_status "$@"
      ;;
    "poll")
      # 轮询等待结果
      check_api_key
      poll_result "$@"
      ;;
    "report")
      # 同步获取报告（旧版兼容）
      check_api_key
      get_report "$@"
      ;;
    "emergency")
      if check_emergency "$1"; then
        echo "EMERGENCY_DETECTED"
      else
        echo "NORMAL"
      fi
      ;;
    *)
      echo "用法：$0 {check_key|upload|start|check|poll|report|emergency} [参数...]"
      echo ""
      echo "命令说明:"
      echo "  check_key          检查 API 密钥配置"
      echo "  upload <文件路径>   上传文件获取 file_id"
      echo "  start <消息> <用户 ID> [files_json]  异步启动报告任务，立即返回任务 ID"
      echo "  check <任务 ID>     检查任务状态（非阻塞）"
      echo "  poll <任务 ID> [超时] [间隔]  轮询等待结果（阻塞）"
      echo "  report <消息> <用户 ID> [files_json]  同步获取报告（旧版兼容）"
      echo "  emergency <消息>   检测是否为紧急症状"
      echo ""
      echo "🆕 异步流程示例:"
      echo "  1. task=\$(./mentx-api.sh start \"我头疼\" user123)"
      echo "  2. ./mentx-api.sh check \$task  # 可重复调用直到 completed"
      echo "  3. 获取结果后通过消息工具发送给用户"
      exit 1
      ;;
  esac
}

main "$@"
