#!/bin/bash
# 亚马逊市场调研报告 - 一键生成
# 用法: bash market-research.sh "Deck Boxes" 671804011
# 就这么简单。

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RUN_TASK="$SCRIPT_DIR/run_task.sh"
MERGE_HTML="$SCRIPT_DIR/merge_html.py"
TIMEOUT=600

NAME="${1:?用法: bash market-research.sh \"类目名称\" 节点ID}"
NODE_ID="${2:?用法: bash market-research.sh \"类目名称\" 节点ID}"
SITE="美国"

# 输出目录
REPORT_DIR="/tmp/market-research-${NODE_ID}"
HTML_DIR="$REPORT_DIR/html"
OUTPUT_DIR="$WORKSPACE/output"
rm -rf "$REPORT_DIR"
mkdir -p "$HTML_DIR" "$OUTPUT_DIR"

# 文件名安全处理
SAFE_NAME=$(echo "$NAME" | tr ' /' '-' | tr -cd '[:alnum:]-_')

echo "╔══════════════════════════════════════════╗"
echo "  📊 $NAME ($NODE_ID)"
echo "  亚马逊${SITE}站 市场调研报告"
echo "╚══════════════════════════════════════════╝"
echo ""

# ========== 4 个任务并行 ==========

echo "⏳ 启动 4 个分析任务..."
echo ""

bash "$RUN_TASK" "1、@卖家精灵-选产品 在亚马逊${SITE}站，类目节点id: ${NODE_ID}，数据快照: nearly，按销量倒序排列，返回前100条商品数据
2、@智能数据查询 对上一步数据生成2张报告：
【报告1：市场容量概览】类目总商品数、总月销量、总月销售额、TOP1月销量及占比、TOP3/TOP5/TOP10月销售额占比（垄断率）、FBA配送销售额占比、平均价格、中位数价格、平均评分值
【报告2：上架时间分布】按3个月内、3个月-1年、1年-3年、3年以上统计产品数、月销量、市场份额占比，结论：新品是否有机会
生成HTML报告含表格和图表" "$TIMEOUT" > "$REPORT_DIR/A.txt" 2>&1 &

bash "$RUN_TASK" "1、@卖家精灵-选产品 在亚马逊${SITE}站，类目节点id: ${NODE_ID}，数据快照: nearly，按销量倒序排列，返回前100条商品数据
2、@智能数据查询 对上一步数据生成2张报告：
【报告1：价格区间分析】最高/最低/平均价格，按每50美金阶梯分组统计产品数和销售额占比，定价建议
【报告2：REVIEW分析】平均评价数量、平均评级，评论数区间（0-100/100-500/500-1000/1000-5000/5000+）的产品数和销量占比，评分区间分布，新品评价门槛建议
生成HTML报告含表格和图表" "$TIMEOUT" > "$REPORT_DIR/B.txt" 2>&1 &

bash "$RUN_TASK" "1、@卖家精灵-选产品 在亚马逊${SITE}站，类目节点id: ${NODE_ID}，数据快照: nearly，按销量倒序排列，返回前100条商品数据
2、@智能数据查询 对上一步数据生成2张报告：
【报告1：品牌集中度】TOP10品牌销售额、市场份额、产品数，CR1/CR3/CR5/CR10，垄断结论
【报告2：卖家分布】按卖家所在地统计产品数和销售额占比，按配送方式（FBA/FBM/AMZ）统计销售额占比，中国卖家占比
生成HTML报告含表格和图表" "$TIMEOUT" > "$REPORT_DIR/C.txt" 2>&1 &

bash "$RUN_TASK" "1、@卖家精灵-选产品 在亚马逊${SITE}站，类目节点id: ${NODE_ID}，数据快照: nearly，按销量倒序排列，返回前100条商品数据
2、@智能数据查询 对上一步数据生成2张报告：
【报告1：竞品Top10】Top10的ASIN、标题、品牌、价格、月销量、月销售额、评分、评论数、上架时间、配送方式
【报告2：总体评价】100条产品的平均评分评论数、Top10平均评论数（进入门槛）、新品（<12个月）数量和销量占比
生成HTML报告含表格和图表" "$TIMEOUT" > "$REPORT_DIR/D.txt" 2>&1 &

echo "  [A] 市场概览 + 上架时间"
echo "  [B] 价格分析 + REVIEW"
echo "  [C] 品牌集中度 + 卖家分布"
echo "  [D] 竞品Top10 + 总体评价"
echo ""
echo "⏳ 等待完成（约 3-5 分钟）..."
echo ""

wait

# ========== 下载报告 ==========

echo "📥 下载报告..."
IDX=1
for F in A B C D; do
    RESULT="$REPORT_DIR/${F}.txt"
    STATUS=$(grep '^STATUS:' "$RESULT" 2>/dev/null | awk '{print $2}')
    if [ "$STATUS" != "finished" ]; then
        echo "  ⚠️  任务 $F: $STATUS"
        continue
    fi
    grep '^REPORT_' "$RESULT" | while IFS= read -r LINE; do
        URL="${LINE#REPORT_*: }"
        FNAME=$(printf "%02d-%s.html" "$IDX" "$F")
        curl -sL "$URL" -o "$HTML_DIR/$FNAME"
        echo "  ✅ $FNAME"
        IDX=$((IDX + 1))
    done
done

HTML_COUNT=$(find "$HTML_DIR" -name "*.html" 2>/dev/null | wc -l | tr -d ' ')
if [ "$HTML_COUNT" -eq 0 ]; then
    echo "❌ 没有报告生成"
    for F in A B C D; do cat "$REPORT_DIR/${F}.txt" 2>/dev/null; done
    exit 1
fi

# ========== 合并 ==========

OUTPUT="$OUTPUT_DIR/${SAFE_NAME}-market-report.html"
echo ""
echo "📑 合并 $HTML_COUNT 份报告..."
python3 "$MERGE_HTML" "$HTML_DIR/" -o "$OUTPUT" -k "$NAME ($NODE_ID)"

echo ""
echo "╔══════════════════════════════════════════╗"
echo "  ✅ 完成!"
echo "  📄 $OUTPUT"
echo "  📊 $(du -h "$OUTPUT" | awk '{print $1}')"
echo "╚══════════════════════════════════════════╝"
echo ""
echo "OUTPUT: $OUTPUT"
