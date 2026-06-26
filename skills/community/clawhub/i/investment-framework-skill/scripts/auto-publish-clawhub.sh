#!/bin/bash

# ClawHub 投资框架技能包自动发布脚本
# 使用方法：./auto-publish-clawhub.sh [batch_number]
# batch_number: 2-6（第 2 批到第 6 批）

set -e

# 配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$SCRIPT_DIR/publish.log"
TOKEN="clh__9gP_tSKR3d9q2c5WzRwN1UJLeKnaOo7YbA3b7nD_W8"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 检查登录状态
check_login() {
    log "检查 ClawHub 登录状态..."
    if ! command -v clawhub > /dev/null 2>&1; then
        log "错误：ClawHub CLI 未安装"
        exit 1
    fi
    
    # 测试登录（通过检查 token 配置）
    if ! clawhub config get token > /dev/null 2>&1; then
        log "警告：ClawHub 未登录，尝试自动登录..."
        export CLAWHUB_TOKEN="$TOKEN"
        log "✅ 已设置 token"
    else
        log "✅ ClawHub 已登录"
    fi
}

# 发布函数
publish_skill() {
    local slug="$1"
    local name="$2"
    local version="$3"
    local tags="$4"
    local changelog="$5"
    local path="$6"
    
    log "发布 $name ($slug@$version)..."
    
    if clawhub publish "$path" \
        --slug "$slug" \
        --name "$name" \
        --version "$version" \
        --changelog "$changelog" \
        --tags "$tags" 2>&1 | tee -a "$LOG_FILE"; then
        log "✅ 成功发布 $slug"
        return 0
    else
        log "❌ 发布失败 $slug"
        return 1
    fi
}

# 第 2 批发布（21:15）
batch_2() {
    log "========== 开始第 2 批发布 =========="
    
    publish_skill "industry-analyst" "行业分析师" "2.0.0" \
        "industry-analysis,lifecycle,competition" \
        "按 v2.0 标准重构，添加 Front Matter、坑点章节、支持文件" \
        "$SKILL_DIR/industry-analyst"
    
    publish_skill "future-forecaster" "未来预测师" "2.0.0" \
        "future-prediction,trends,kk" \
        "按 v2.0 标准重构" \
        "$SKILL_DIR/future-forecaster"
    
    publish_skill "cycle-locator" "周期定位师" "2.0.0" \
        "economic-cycle,dalio,debt" \
        "按 v2.0 标准重构" \
        "$SKILL_DIR/cycle-locator"
    
    publish_skill "stock-picker" "选股专家" "2.0.0" \
        "stock-picking,lynch,peg" \
        "按 v2.0 标准重构" \
        "$SKILL_DIR/stock-picker"
    
    publish_skill "portfolio-designer" "组合设计师" "2.0.0" \
        "portfolio-design,yale-model,endowment" \
        "按 v2.0 标准重构" \
        "$SKILL_DIR/portfolio-designer"
    
    log "========== 第 2 批发布完成 =========="
}

# 第 3 批发布（22:15）
batch_3() {
    log "========== 开始第 3 批发布 =========="
    
    publish_skill "global-allocator" "全球配置师" "2.0.0" \
        "global-asset,diversification,rebalancing" \
        "按 v2.0 标准重构" \
        "$SKILL_DIR/global-allocator"
    
    publish_skill "simple-investor" "简单投资者" "2.0.0" \
        "simple-investing,qiu-guolu,a-share" \
        "按 v2.0 标准重构" \
        "$SKILL_DIR/simple-investor"
    
    publish_skill "bias-detector" "认知偏差检测器" "2.0.0" \
        "cognitive-bias,kahneman,decision" \
        "按 v2.0 标准重构" \
        "$SKILL_DIR/bias-detector"
    
    publish_skill "second-level-thinker" "第二层思维者" "2.0.0" \
        "second-level-thinking,marks,contrarian" \
        "按 v2.0 标准重构" \
        "$SKILL_DIR/second-level-thinker"
    
    publish_skill "qiu-guolu-investor" "邱国鹭投资智慧" "2.0.0" \
        "qiu-guolu,simple-investing,value" \
        "按 v2.0 标准重构" \
        "$SKILL_DIR/china-masters/qiu-guolu"
    
    log "========== 第 3 批发布完成 =========="
}

# 第 4 批发布（23:15）
batch_4() {
    log "========== 开始第 4 批发布 =========="
    
    publish_skill "duan-yongping-investor" "段永平投资智慧" "2.0.0" \
        "duan-yongping,benfen,long-term" \
        "按 v2.0 标准重构" \
        "$SKILL_DIR/china-masters/duan-yongping"
    
    publish_skill "li-lu-investor" "李录投资智慧" "2.0.0" \
        "li-lu,civilization,china-opportunity" \
        "按 v2.0 标准重构" \
        "$SKILL_DIR/china-masters/li-lu"
    
    publish_skill "wu-jun-investor" "吴军投资智慧" "2.0.0" \
        "wu-jun,ai,data-driven" \
        "按 v2.0 标准重构" \
        "$SKILL_DIR/china-masters/wu-jun"
    
    publish_skill "qiu-valuation" "邱国鹭估值分析" "2.0.0" \
        "valuation,pe,pb" \
        "按 v2.0 标准重构" \
        "$SKILL_DIR/china-masters/qiu-guolu/valuation-analyzer"
    
    publish_skill "qiu-quality" "邱国鹭品质分析" "2.0.0" \
        "quality,roe,moat" \
        "按 v2.0 标准重构" \
        "$SKILL_DIR/china-masters/qiu-guolu/quality-analyzer"
    
    log "========== 第 4 批发布完成 =========="
}

# 第 5 批发布（次日 00:15）
batch_5() {
    log "========== 开始第 5 批发布 =========="
    
    publish_skill "duan-culture" "段永平文化分析" "2.0.0" \
        "culture,benfen,checklist" \
        "按 v2.0 标准重构" \
        "$SKILL_DIR/china-masters/duan-yongping/culture-analyzer"
    
    publish_skill "duan-longterm" "段永平长期检查" "2.0.0" \
        "long-term,10year,holding" \
        "按 v2.0 标准重构" \
        "$SKILL_DIR/china-masters/duan-yongping/longterm-checker"
    
    publish_skill "li-civilization" "李录文明分析" "2.0.0" \
        "civilization,evolution,3.0" \
        "按 v2.0 标准重构" \
        "$SKILL_DIR/china-masters/li-lu/civilization-analyzer"
    
    publish_skill "li-china" "李录中国机会" "2.0.0" \
        "china-opportunity,modernization,core-assets" \
        "按 v2.0 标准重构" \
        "$SKILL_DIR/china-masters/li-lu/china-opportunity"
    
    publish_skill "wu-ai" "吴军 AI 趋势" "2.0.0" \
        "ai-trend,intelligence,wave" \
        "按 v2.0 标准重构" \
        "$SKILL_DIR/china-masters/wu-jun/ai-trend-analyzer"
    
    log "========== 第 5 批发布完成 =========="
}

# 第 6 批发布（次日 01:15）
batch_6() {
    log "========== 开始第 6 批发布 =========="
    
    publish_skill "wu-data" "吴军数据驱动" "2.0.0" \
        "data-driven,quantitative,analysis" \
        "按 v2.0 标准重构" \
        "$SKILL_DIR/china-masters/wu-jun/data-driven-investor"
    
    log "========== 第 6 批发布完成 =========="
    log "🎉 全部 26 个技能发布完成！"
}

# 主函数
main() {
    local batch="${1:-auto}"
    
    log "========================================"
    log "ClawHub 自动发布脚本启动"
    log "批次：$batch"
    log "========================================"
    
    check_login
    
    case "$batch" in
        2)
            batch_2
            ;;
        3)
            batch_3
            ;;
        4)
            batch_4
            ;;
        5)
            batch_5
            ;;
        6)
            batch_6
            ;;
        auto)
            # 自动模式：根据当前时间决定执行哪一批
            local hour=$(date +%H)
            
            if [ "$hour" -ge 21 ] && [ "$hour" -lt 22 ]; then
                batch_2
            elif [ "$hour" -ge 22 ] && [ "$hour" -lt 23 ]; then
                batch_3
            elif [ "$hour" -ge 23 ] && [ "$hour" -lt 24 ]; then
                batch_4
            elif [ "$hour" -ge 00 ] && [ "$hour" -lt 01 ]; then
                batch_5
            elif [ "$hour" -ge 01 ] && [ "$hour" -lt 02 ]; then
                batch_6
            else
                log "当前时间不在发布窗口内"
                log "发布窗口：21:00 - 02:00"
                exit 0
            fi
            ;;
        *)
            log "未知批次：$batch"
            log "可用批次：2, 3, 4, 5, 6, auto"
            exit 1
            ;;
    esac
    
    log "========================================"
    log "发布脚本执行完成"
    log "========================================"
}

# 执行
main "$@"
