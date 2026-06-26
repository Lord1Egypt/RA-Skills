#!/bin/bash
# Polymarket 预测市场工具

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; BLUE='\033[0;34m'; NC='\033[0m'

# 平台信息
show_info() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}🎰 Polymarket 预测市场${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    echo -e "${GREEN}📌 平台简介${NC}"
    echo "Polymarket 是一个基于 Polygon 链的预测市场平台"
    echo "允许用户用 USDC 对未来事件进行交易"
    echo ""
    
    echo -e "${GREEN}📊 基本信息${NC}"
    echo "• 链: Polygon"
    echo "• 代币: USDC"
    echo "• 官网: polymarket.com"
    echo "• 特点: 低费用、无需 KYC"
    echo ""
    
    echo -e "${GREEN}💰 如何开始${NC}"
    echo "1. 安装 Metamask 钱包"
    echo "2. 获取 Polygon USDC"
    echo "3. 打开 polymarket.com"
    echo "4. 连接钱包，开始交易"
    echo ""
}

# 热门市场
show_markets() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}🔥 热门市场类型${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    echo "【政治类】"
    echo "• 2028年总统大选"
    echo "• 各国大选结果"
    echo "• 国际关系事件"
    echo ""
    
    echo "【体育类】"
    echo "• 世界杯冠军"
    echo "• 奥运会奖牌榜"
    echo "• 各大联赛冠军"
    echo ""
    
    echo "【科技类】"
    echo "• AI 发展预测"
    echo "• 公司产品发布"
    echo "• 技术突破"
    echo ""
    
    echo "【金融类】"
    echo "• BTC 价格预测"
    echo "• 股市指数"
    echo "• 经济指标"
    echo ""
    
    echo -e "${YELLOW}📌 访问 polymarket.com 查看实时市场${NC}"
}

# 下注策略
show_strategy() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}📈 下注策略${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    echo -e "${GREEN}策略1: 概率优势${NC}"
    echo "当你自己判断的概率 > 市场定价时买入"
    echo ""
    echo "例子:"
    echo "• 你认为 BTC 有 80% 概率涨"
    echo "• 市场定价 '是' = \$0.60 (60%)"
    echo "• 80% > 60% → 值得买入"
    echo ""
    
    echo -e "${GREEN}策略2: 分散投资${NC}"
    echo "不要把全部资金投入一个市场"
    echo "• 单个市场 ≤ 10% 资金"
    echo "• 多个市场分散风险"
    echo ""
    
    echo -e "${GREEN}策略3: 流动性考虑${NC}"
    echo "选择流动性好的市场"
    echo "• 交易量大的市场"
    echo "• 买卖价差小"
    echo ""
    
    echo -e "${GREEN}策略4: 独立判断${NC}"
    echo "• 不要盲目跟从他人"
    echo "• 做好自己的研究"
    echo "• 设置止盈止损"
    echo ""
}

# 收益计算
show_calc() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}🧮 收益计算器${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    echo "输入示例计算:"
    echo ""
    echo "投入: 100 USDC"
    echo "买入价格: \$0.60 (60% 概率)"
    echo "结果: 是 (事件发生)"
    echo ""
    
    # 计算
    invest=100
    price=0.60
    
    profit=$(echo "scale=2; $invest * (1 - $price) / $price" | bc)
    rate=$(echo "scale=2; ($profit / $invest) * 100" | bc)
    
    echo "--- 计算结果 ---"
    echo "收益: $profit USDC"
    echo "利润率: $rate%"
    echo ""
    
    echo "--- 公式 ---"
    echo "收益 = 投入 × (1 - 买入价格) / 买入价格"
    echo "利润率 = (收益 / 投入) × 100%"
    echo ""
    
    echo "--- 结果是 '否' 的情况 ---"
    echo "损失: 100 USDC (全部)"
    echo ""
    
    echo -e "${YELLOW}⚠️ 风险: 如果结果与你的判断相反，将损失全部投入!${NC}"
}

# 风险管理
show_risk() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}⚠️ 风险管理${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    echo -e "${RED}⚠️ 重要警告${NC}"
    echo "预测市场有风险，可能损失全部本金!"
    echo "请仅使用可承受损失的资金"
    echo ""
    
    echo -e "${GREEN}✅ 风险控制原则${NC}"
    echo ""
    echo "1. 仓位控制"
    echo "   • 单个市场 ≤ 10% 资金"
    echo "   • 建议 5% 更安全"
    echo ""
    
    echo "2. 止损策略"
    echo "   • 亏损 50% 考虑退出"
    echo "   • 亏损 70% 强制止损"
    echo ""
    
    echo "3. 止盈策略"
    echo "   • 盈利 100% 可部分获利"
    echo "   • 保留本金，只用利润继续"
    echo ""
    
    echo "4. 心理控制"
    echo "   • 不要上头"
    echo "   • 不要 FOMO"
    echo "   • 独立判断"
    echo ""
    
    echo -e "${RED}❌ 不要做${NC}"
    echo "• 不要借usdt/eth"
    echo "• 不要 All in 单个市场"
    echo "• 不要听信陌生人推荐"
    echo "• 不要情绪化交易"
    echo ""
}

# 快速链接
show_links() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}🔗 常用链接${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "• 官网: https://polymarket.com"
    echo "• 市场: https://polymarket.com/markets"
    echo "• 文档: https://docs.polymarket.com"
    echo ""
}

# 帮助
show_help() {
    cat << HELP
🎰 Polymarket 预测市场工具

用法: ./main.sh [选项]

选项:
  --info, -i       平台介绍
  --markets, -m    热门市场
  --strategy, -s   下注策略
  --calc, -c       收益计算
  --risk, -r       风险管理
  --links, -l      常用链接
  --help, -h       显示帮助

示例:
  ./main.sh --info
  ./main.sh --markets
  ./main.sh --calc

HELP
}

main() {
    local action=""
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --info|-i) action="info"; shift ;;
            --markets|-m) action="markets"; shift ;;
            --strategy|-s) action="strategy"; shift ;;
            --calc|-c) action="calc"; shift ;;
            --risk|-r) action="risk"; shift ;;
            --links|-l) action="links"; shift ;;
            --help|-h) action="help"; shift ;;
            *) shift ;;
        esac
    done
    
    case "$action" in
        info) show_info ;;
        markets) show_markets ;;
        strategy) show_strategy ;;
        calc) show_calc ;;
        risk) show_risk ;;
        links) show_links ;;
        help|*) show_help ;;
    esac
}

main "$@"
