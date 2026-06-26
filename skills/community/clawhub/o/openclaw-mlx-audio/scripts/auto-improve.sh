#!/bin/bash
# openclaw-mlx-audio - 自动改进循环脚本
# 模拟 autoresearch 行为

set -e

echo "🔄 Starting auto-improve loop..."
echo "Goal: Improve openclaw-mlx-audio quality"
echo "Iterations: 20"
echo ""

ITERATIONS=20
BASELINE=100.00

# 初始化 results.tsv
if [ ! -f results.tsv ]; then
    echo "iteration	commit	metric	delta	status	description" > results.tsv
    echo "0	$(git rev-parse --short HEAD)	$BASELINE	0.00	baseline	initial state" >> results.tsv
fi

for i in $(seq 1 $ITERATIONS); do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Iteration $i/$ITERATIONS"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # 运行测试获取当前指标
    OUTPUT=$(bash test/run_tests.sh 2>&1)
    CURRENT=$(echo "$OUTPUT" | grep "SUCCESS_RATE=" | cut -d= -f2)
    
    echo "Current Success Rate: $CURRENT%"
    
    # 计算增量
    DELTA=$(echo "$CURRENT - $BASELINE" | bc)
    
    if (( $(echo "$DELTA > 0" | bc -l) )); then
        STATUS="keep"
        DESCRIPTION="Improvement detected (+$DELTA%)"
    elif (( $(echo "$DELTA < 0" | bc -l) )); then
        STATUS="discard"
        DESCRIPTION="Regression detected ($DELTA%)"
    else
        STATUS="keep"
        DESCRIPTION="Maintained baseline"
    fi
    
    # 记录到 results.tsv
    COMMIT=$(git rev-parse --short HEAD)
    echo "$i	$COMMIT	$CURRENT	$DELTA	$STATUS	$DESCRIPTION" >> results.tsv
    
    echo "Status: $STATUS"
    echo "Delta: $DELTA"
    echo ""
    
    # 等待下一次迭代
    sleep 2
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Auto-improve loop completed!"
echo "Results saved to results.tsv"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 显示摘要
echo ""
echo "📊 Summary:"
cat results.tsv | tail -10
