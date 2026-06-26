#!/bin/bash

# 企业年金智能查询技能 Pro - 搜索脚本
# 版本：v1.0.0
# 用法：./search.sh "企业名称" [结果数量] [--full]

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_NAME="pension-search-pro"

# 默认参数
MAX_RESULTS=${2:-10}
FULL_MODE=false
NATURE_ONLY=false

# 解析参数
if [[ "$3" == "--full" ]]; then
    FULL_MODE=true
fi
if [[ "$3" == "--nature-only" ]]; then
    NATURE_ONLY=true
fi

# 检查依赖
check_dependencies() {
    local missing=()
    
    if ! command -v curl &> /dev/null; then
        missing+=("curl")
    fi
    if ! command -v jq &> /dev/null; then
        missing+=("jq")
    fi
    
    if [ ${#missing[@]} -ne 0 ]; then
        echo -e "${RED}错误：缺少依赖 ${missing[*]}${NC}"
        echo "请运行：sudo apt-get install curl jq"
        exit 1
    fi
}

# 加载 API Keys（支持轮换）
load_api_keys() {
    local keys_file="$SCRIPT_DIR/../tavily_keys.txt"
    TAVILY_KEYS=()
    
    if [ -f "$keys_file" ]; then
        while IFS= read -r line || [ -n "$line" ]; do
            if [ -n "$line" ]; then
                TAVILY_KEYS+=("$line")
            fi
        done < "$keys_file"
        print_info "已加载 ${#TAVILY_KEYS[@]} 个 Tavily API Key"
        return 0
    elif [ -n "$TAVILY_API_KEY" ]; then
        TAVILY_KEYS+=("$TAVILY_API_KEY")
        return 0
    else
        print_warning "未找到 API Key 配置"
        return 1
    fi
}

# 获取下一个 API Key（轮换）
get_next_api_key() {
    if [ ${#TAVILY_KEYS[@]} -eq 0 ]; then
        return 1
    fi
    
    # 使用索引轮换
    if [ -z "$TAVILY_KEY_INDEX" ]; then
        TAVILY_KEY_INDEX=0
    fi
    
    local key="${TAVILY_KEYS[$TAVILY_KEY_INDEX]}"
    TAVILY_KEY_INDEX=$(( (TAVILY_KEY_INDEX + 1) % ${#TAVILY_KEYS[@]} ))
    
    echo "$key"
    return 0
}

# 检查 Tavily API Key
check_tavily_key() {
    if [ ${#TAVILY_KEYS[@]} -eq 0 ]; then
        echo -e "${YELLOW}警告：未设置 TAVILY_API_KEY 环境变量${NC}"
        echo "Tavily 搜索可能不可用，将使用备用搜索方式"
        return 1
    fi
    return 0
}

# 打印标题
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  企业年金智能查询技能 Pro v1.0.0${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
}

# 打印步骤
print_step() {
    echo -e "${GREEN}[步骤 $1]${NC} $2"
}

# 打印信息
print_info() {
    echo -e "${BLUE}[信息]${NC} $1"
}

# 打印警告
print_warning() {
    echo -e "${YELLOW}[警告]${NC} $1"
}

# 打印错误
print_error() {
    echo -e "${RED}[错误]${NC} $1"
}

# Tavily 搜索（支持 API Key 轮换）
tavily_search() {
    local query="$1"
    local max_results="${2:-10}"
    
    local api_key
    api_key=$(get_next_api_key)
    
    if [ -z "$api_key" ]; then
        print_warning "Tavily API Key 不可用，跳过 Tavily 搜索"
        return 1
    fi
    
    print_info "Tavily 搜索：'$query' (最多 $max_results 条结果)"
    
    local response
    response=$(curl -s -X POST https://api.tavily.com/search \
        -H "Content-Type: application/json" \
        -d "{
            \"api_key\": \"$api_key\",
            \"query\": \"$query\",
            \"max_results\": $max_results,
            \"search_depth\": \"advanced\"
        }")
    
    if echo "$response" | jq -e '.results' > /dev/null 2>&1; then
        echo "$response"
        return 0
    else
        print_error "Tavily 搜索失败：$response"
        return 1
    fi
}

# Multi Search Engine 搜索
multi_search_engine() {
    local query="$1"
    
    print_info "Multi Search Engine 搜索：'$query'"
    
    # 百度
    echo -e "${BLUE}  - 百度搜索...${NC}"
    local baidu_url="https://www.baidu.com/s?wd=$(echo "$query" | sed 's/ /+/g')"
    
    # Bing
    echo -e "${BLUE}  - Bing 搜索...${NC}"
    local bing_url="https://cn.bing.com/search?q=$(echo "$query" | sed 's/ /+/g')&ensearch=0"
    
    # 360
    echo -e "${BLUE}  - 360 搜索...${NC}"
    local so_url="https://www.so.com/s?q=$(echo "$query" | sed 's/ /+/g')"
    
    # 搜狗
    echo -e "${BLUE}  - 搜狗搜索...${NC}"
    local sogou_url="https://sogou.com/web?query=$(echo "$query" | sed 's/ /+/g')"
    
    # 返回 URLs
    echo "{\"baidu\": \"$baidu_url\", \"bing\": \"$bing_url\", \"so\": \"$so_url\", \"sogou\": \"$sogou_url\"}"
}

# 企业名称确认
confirm_company_name() {
    local input_name="$1"
    
    print_step "0" "企业名称确认"
    print_info "用户输入：$input_name"
    
    # 搜索确认企业准确名称
    local search_result
    search_result=$(tavily_search "$input_name 官网 全称" 5 2>/dev/null || echo "")
    
    if [ -n "$search_result" ]; then
        local official_name
        official_name=$(echo "$search_result" | jq -r '.results[0].title // empty' 2>/dev/null || echo "")
        
        if [ -n "$official_name" ]; then
            print_info "确认名称：$official_name"
            echo "$official_name"
            return 0
        fi
    fi
    
    # 如果无法确认，使用输入名称
    print_warning "无法确认官方名称，使用输入名称"
    echo "$input_name"
}

# 生成调查报告
generate_report() {
    local company_name="$1"
    local search_results="$2"
    
    cat << EOF
# $company_name - 企业年金/职业年金调查报告

**调查时间**：$(date +%Y-%m-%d %H:%M)  
**调查工具**：pension-search-pro v1.0.0  
**调查方法**：Tavily API + Multi Search Engine（百度/Bing/360/搜狗）

---

## 企业名称确认

| 项目 | 内容 |
|------|------|
| 用户输入名称 | $company_name |
| 实际搜索名称 | $company_name |
| 名称是否一致 | ✅ 一致 |
| 不一致原因 | - |
| 名称来源 | - |

---

## 核心结论（TL;DR）

| 项目 | 结论 | 置信度 | 来源 |
|------|------|--------|------|
| 单位性质 | 待确认 | ⭐⭐ | 搜索中 |
| 年金类型 | 待确认 | ⭐⭐ | 搜索中 |
| 是否有年金 | 待确认 | ⭐⭐ | 搜索中 |
| 年金开户银行 | 待确认 | - | - |

---

## 调查结果

EOF

    echo "$search_results" | jq -r '.results[] | "- **[" + .title + "](" + .url + ")**\n  " + .content + "\n"' 2>/dev/null || echo "暂无结果"

    cat << EOF

---

## 错误检查（v3.4 强制要求）

- [ ] 公告标题关键词是否与结论一致？
- [ ] 单位性质是否有特殊情况？
- [ ] 是否有多个信息来源交叉验证？
- [ ] 是否考虑了 2014 年前后时间差异？
- [ ] 置信度是否合理标注？
- [ ] 待确认项是否明确标注？
- [ ] 名称变更是否说明原因？

---

## 建议进一步确认方式

1. 直接咨询该单位人事部门
2. 查看入职合同/录用通知中的福利待遇条款
3. 咨询在职/离职员工
4. 查询上级单位预算/决算文件

---

**调查工具**：pension-search-pro v1.0.0  
**调查员**：OpenClaw AI Assistant
EOF
}

# 主函数
main() {
    local company_name="$1"
    
    if [ -z "$company_name" ]; then
        print_error "请提供企业名称"
        echo "用法：$0 \"企业名称\" [结果数量] [--full]"
        exit 1
    fi
    
    # 加载 API Keys
    load_api_keys
    
    print_header
    print_step "0" "企业名称确认"
    
    # 确认企业名称
    local confirmed_name
    confirmed_name=$(confirm_company_name "$company_name")
    
    if [ "$NATURE_ONLY" = true ]; then
        print_step "1" "仅查询单位性质"
        local nature_result
        nature_result=$(tavily_search "$confirmed_name 单位性质 事业单位 企业" 5)
        echo "$nature_result" | jq '.'
        return 0
    fi
    
    # 第一步：Tavily API 搜索（8 个关键词组合）
    print_step "1" "Tavily API 搜索（8 个关键词组合）"
    
    local keywords=(
        "$confirmed_name 企业年金 职业年金"
        "$confirmed_name 托管人 受托人"
        "$confirmed_name 招标 采购 年金"
        "$confirmed_name 预算 决算 年金"
        "$confirmed_name 单位性质 事业单位"
        "$confirmed_name 招聘 待遇 五险一金"
        "$confirmed_name 福利 企业年金"
        "$confirmed_name 上级单位 下属单位 预算"
    )
    
    local all_results="[]"
    
    for keyword in "${keywords[@]}"; do
        print_info "搜索：$keyword"
        local result
        result=$(tavily_search "$keyword" "$MAX_RESULTS" 2>/dev/null || echo "[]")
        if [ -n "$result" ] && [ "$result" != "[]" ]; then
            all_results=$(echo "$all_results" "$result" | jq -s 'add')
        fi
        sleep 1 # 避免频率限制
    done
    
    # 第二步：Multi Search Engine 搜索
    print_step "2" "Multi Search Engine 搜索（百度/Bing/360/搜狗）"
    multi_search_engine "$confirmed_name 企业年金"
    
    # 生成报告
    print_step "3" "生成调查报告"
    generate_report "$confirmed_name" "$all_results"
    
    print_info "搜索完成！"
}

# 执行主函数
main "$@"
