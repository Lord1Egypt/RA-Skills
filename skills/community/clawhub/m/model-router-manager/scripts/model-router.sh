#!/usr/bin/env bash
# Model Router Manager - 多模型路由管理脚本

CONFIG_FILE="${HOME}/.openclaw/model-router.json"
OPENCLAW_CONFIG="${HOME}/.openclaw/openclaw.json"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 帮助信息
show_help() {
    cat << 'EOF'
Model Router Manager - 智能多模型路由管理器

用法:
  model-router [命令] [选项]

命令:
  config          配置模型链
  strategy        设置路由策略
  stats           查看使用统计
  test            测试故障转移
  list            列出已配置模型
  reset           重置配置

选项:
  --primary       设置主模型
  --fallback-1    设置第一备选
  --fallback-2    设置第二备选
  --strategy      策略: cost|speed|quality

示例:
  model-router config --primary kimi-coding/k2p5 --fallback-1 bailian/qwen3-max
  model-router strategy cost
  model-router stats
EOF
}

# 检查依赖
check_deps() {
    if ! command -v jq &> /dev/null; then
        echo -e "${RED}错误: 需要安装 jq${NC}"
        echo "安装: apt-get install jq 或 brew install jq"
        exit 1
    fi
}

# 初始化配置
init_config() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        mkdir -p "$(dirname "$CONFIG_FILE")"
        cat > "$CONFIG_FILE" << 'EOF'
{
  "version": "1.0.0",
  "strategy": "cost",
  "models": {
    "primary": "",
    "fallbacks": []
  },
  "stats": {
    "totalCalls": 0,
    "totalCost": 0,
    "failoverCount": 0,
    "savings": 0
  }
}
EOF
        echo -e "${GREEN}✓ 配置文件已创建: $CONFIG_FILE${NC}"
    fi
}

# 配置模型链
configure_models() {
    local primary=""
    local fallback1=""
    local fallback2=""
    
    # 解析参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            --primary)
                primary="$2"
                shift 2
                ;;
            --fallback-1)
                fallback1="$2"
                shift 2
                ;;
            --fallback-2)
                fallback2="$2"
                shift 2
                ;;
            *)
                shift
                ;;
        esac
    done
    
    if [[ -z "$primary" ]]; then
        echo -e "${RED}错误: 请指定主模型 --primary${NC}"
        exit 1
    fi
    
    # 更新配置
    local fallbacks="[]"
    [[ -n "$fallback1" ]] && fallbacks=$(echo "$fallbacks" | jq --arg f "$fallback1" '. + [$f]')
    [[ -n "$fallback2" ]] && fallbacks=$(echo "$fallbacks" | jq --arg f "$fallback2" '. + [$f]')
    
    jq --arg p "$primary" --argjson f "$fallbacks" '
        .models.primary = $p |
        .models.fallbacks = $f
    ' "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
    
    echo -e "${GREEN}✓ 模型链已配置:${NC}"
    echo "  主模型: $primary"
    [[ -n "$fallback1" ]] && echo "  备选1: $fallback1"
    [[ -n "$fallback2" ]] && echo "  备选2: $fallback2"
    
    # 提示更新 OpenClaw 配置
    echo -e "${YELLOW}提示: 请手动更新 ~/.openclaw/openclaw.json 中的 fallbacks${NC}"
}

# 设置策略
set_strategy() {
    local strategy="$1"
    
    if [[ ! "$strategy" =~ ^(cost|speed|quality)$ ]]; then
        echo -e "${RED}错误: 策略必须是 cost|speed|quality${NC}"
        exit 1
    fi
    
    jq --arg s "$strategy" '.strategy = $s' "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
    
    echo -e "${GREEN}✓ 路由策略已设置为: $strategy${NC}"
    
    case $strategy in
        cost)
            echo "  优先选择: 成本最低的模型"
            ;;
        speed)
            echo "  优先选择: 响应最快的模型"
            ;;
        quality)
            echo "  优先选择: 质量最高的模型"
            ;;
    esac
}

# 显示统计
show_stats() {
    if [[ ! -f "$CONFIG_FILE" ]]; then
        echo -e "${YELLOW}暂无统计数据${NC}"
        return
    fi
    
    local stats=$(jq '.stats' "$CONFIG_FILE")
    local strategy=$(jq -r '.strategy' "$CONFIG_FILE")
    local primary=$(jq -r '.models.primary' "$CONFIG_FILE")
    
    echo "═══════════════════════════════════════"
    echo "      📊 Model Router 统计面板"
    echo "═══════════════════════════════════════"
    echo ""
    echo "当前配置:"
    echo "  路由策略: $strategy"
    echo "  主模型: $primary"
    echo ""
    echo "使用统计:"
    echo "  总调用次数: $(echo "$stats" | jq -r '.totalCalls // 0')"
    echo "  总成本: \$$(echo "$stats" | jq -r '.totalCost // 0')"
    echo "  故障转移次数: $(echo "$stats" | jq -r '.failoverCount // 0')"
    echo "  节省成本: \$$(echo "$stats" | jq -r '.savings // 0')"
    echo "═══════════════════════════════════════"
}

# 列出模型
list_models() {
    echo "支持的模型平台:"
    echo ""
    echo "Kimi (kimi-coding):"
    echo "  - kimi-coding/k2p5"
    echo "  - kimi-coding/k2.5"
    echo "  - kimi-coding/k1.5"
    echo ""
    echo "百炼 (bailian):"
    echo "  - bailian/qwen3-max-2026-01-23"
    echo "  - bailian/qwen3-coder-plus"
    echo "  - bailian/qwen-vl-max"
    echo ""
    echo "OpenRouter (openrouter):"
    echo "  - openrouter/gpt-4o"
    echo "  - openrouter/claude-3.5-sonnet"
    echo "  - openrouter/gemini-pro"
    echo ""
    
    if [[ -f "$CONFIG_FILE" ]]; then
        echo "当前配置:"
        jq -r '.models | "  主: \(.primary)\n  备选: \(.fallbacks | join(", "))"' "$CONFIG_FILE"
    fi
}

# 测试故障转移
test_failover() {
    echo "🧪 测试故障转移..."
    echo ""
    
    local primary=$(jq -r '.models.primary' "$CONFIG_FILE")
    local fallbacks=$(jq -r '.models.fallbacks | join(", ")' "$CONFIG_FILE")
    
    echo "当前模型链:"
    echo "  1. $primary (主)"
    local i=2
    for model in $fallbacks; do
        echo "  $i. $model (备选$((i-1)))"
        ((i++))
    done
    
    echo ""
    echo "测试方法:"
    echo "  1. 故意使用无效模型名触发故障"
    echo "  2. 观察切换到备选模型的延迟"
    echo ""
    echo -e "${YELLOW}注意: 这会消耗少量 API 调用额度${NC}"
    echo "按 Enter 开始测试，或 Ctrl+C 取消..."
    read
    
    # 实际测试代码需要在 OpenClaw 环境中执行
    echo -e "${GREEN}✓ 请手动测试: 临时修改主模型为无效名称，观察故障转移${NC}"
}

# 重置配置
reset_config() {
    echo -e "${YELLOW}警告: 这将删除所有配置！${NC}"
    read -p "确认重置? (yes/no): " confirm
    
    if [[ "$confirm" == "yes" ]]; then
        rm -f "$CONFIG_FILE"
        init_config
        echo -e "${GREEN}✓ 配置已重置${NC}"
    else
        echo "已取消"
    fi
}

# 主入口
main() {
    check_deps
    init_config
    
    case "${1:-}" in
        config)
            shift
            configure_models "$@"
            ;;
        strategy)
            set_strategy "$2"
            ;;
        stats)
            show_stats
            ;;
        list)
            list_models
            ;;
        test)
            test_failover
            ;;
        reset)
            reset_config
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            show_help
            exit 1
            ;;
    esac
}

main "$@"