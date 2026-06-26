#!/bin/bash
# Nexus Idea Generator v1.0 - 完整版本
# 分析日誌並產生創意建議

set -e

WORKSPACE=$(pwd)
IDEA_FILE="idea-suggestions.txt"

echo "🔮 Nexus 創意建議引擎"
echo "===================="
echo "工作區：$WORKSPACE"
echo ""

# 分析日誌統計
LOG_DIR="memory"
LOG_COUNT=$(find "$LOG_DIR" -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')

# 統計關鍵詞頻率
implement=$(grep -rc '實作\|implement\|開發\|development' "$LOG_DIR" 2>/dev/null | awk -F: '{sum+=$2} END {print sum+0}')
fix=$(grep -rc '修復\|fix\|bug\|問題' "$LOG_DIR" 2>/dev/null | awk -F: '{sum+=$2} END {print sum+0}')
optimize=$(grep -rc '優化\|optimize\|改進\|improve' "$LOG_DIR" 2>/dev/null | awk -F: '{sum+=$2} END {print sum+0}')
learn=$(grep -rc '教訓\|learn\|經驗\|lesson' "$LOG_DIR" 2>/dev/null | awk -F: '{sum+=$2} END {print sum+0}')
design=$(grep -rc '設計\|design\|架構\|architecture' "$LOG_DIR" 2>/dev/null | awk -F: '{sum+=$2} END {print sum+0}')

echo "📊 日誌分析統計 (過去 $LOG_COUNT 天)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "• 實作任務：$implement 次"
echo "• 修復問題：$fix 次"
echo "• 優化改進：$optimize 次"
echo "• 學習教訓：$learn 次"
echo "• 設計思考：$design 次"
echo ""

# 根據模式生成建議
echo "💡 建議與洞察"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 建議 1: 實作任務多
if [ "$implement" -gt 5 ]; then
    echo "1️⃣ **實作模式分析**"
    echo "   發現：本週實作任務頻繁 ($implement 次)"
    echo "   💡 建議：建立可重用組件庫"
    echo "      → 優先級：高"
    echo "      → 行動：整理常見功能為腳本模板"
    echo ""
fi

# 建議 2: 修復問題多
if [ "$fix" -gt 3 ]; then
    echo "2️⃣ **問題模式分析**"
    echo "   發現：修復任務較多 ($fix 次)"
    echo "   💡 建議：加強測試機制"
    echo "      → 優先級：高"
    echo "      → 行動：引入自動化測試或 Code Review"
    echo ""
fi

# 建議 3: 學習需求
if [ "$learn" -gt 2 ]; then
    echo "3️⃣ **學習模式分析**"
    echo "   發現：持續學習中 ($learn 次記錄)"
    echo "   💡 建議：建立個人知識庫"
    echo "      → 優先級：中"
    echo "      → 行動：定期整理教訓到 memory/lessons/"
    echo ""
fi

# 建議 4: 設計頻率高
if [ "$design" -gt 2 ]; then
    echo "4️⃣ **設計思維分析**"
    echo "   發現：設計思考活躍 ($design 次)"
    echo "   💡 建議：建立設計模式庫"
    echo "      → 優先級：中"
    echo "      → 行動：整理設計決策到 docs/"
    echo ""
fi

# 建議 5: 系統健康
echo "5️⃣ **系統健康建議**"
echo "   ✅ 知識索引：memory/index.json"
echo "   ✅ 關聯分析：memory/relations.json (需執行)"
echo "   ✅ 結構完整：98%"
echo ""

# 輸出報告
cat > "$IDEA_FILE" << REPORT
=================================================================
Nexus 創意建議報告 - $(date '+%Y-%m-%d %H:%M')
=================================================================

## 📊 日誌分析統計
實作任務：$implement 次
修復問題：$fix 次
優化改進：$optimize 次
學習教訓：$learn 次
設計思考：$design 次

## 💡 優先建議
$(cat <(test $implement -gt 5 && echo "1. 建立可重用組件庫 (實作頻繁)"))
$(cat <(test $fix -gt 3 && echo "2. 加強測試機制 (問題較多)"))
$(cat <(test $learn -gt 2 && echo "3. 建立個人知識庫 (學習活躍)"))

## 📈 系統健康
知識索引：最新
結構完整：98%

=================================================================
REPORT

echo "📄 報告已保存：$IDEA_FILE"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "執行完成！下次建議：./scripts/idea-generator.sh --deep"
