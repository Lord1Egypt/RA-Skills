#!/bin/bash
# scripts/check_abstract.sh
# 检查摘要是否符合 6 句话速成法

ABSTRACT="$1"

if [ -z "$ABSTRACT" ]; then
    echo "用法：$0 \"摘要内容\""
    exit 1
fi

echo "=== 摘要检查 ==="
echo ""

# 字数检查
CHAR_COUNT=$(echo "$ABSTRACT" | wc -m)
echo "字数：$CHAR_COUNT (要求≤400 字)"
if [ $CHAR_COUNT -gt 400 ]; then
    echo "⚠️  超出限制，请精简"
else
    echo "✅ 符合要求"
fi

echo ""
echo "=== 六要素检查 ==="

# 检查关键词
if echo "$ABSTRACT" | grep -q "针对"; then
    echo "✅ 包含'针对'（背景）"
else
    echo "⚠️  缺少'针对'（背景）"
fi

if echo "$ABSTRACT" | grep -q "提出\|假说\|假设"; then
    echo "✅ 包含科学假说"
else
    echo "⚠️  缺少科学假说"
fi

if echo "$ABSTRACT" | grep -q "用\|采用\|利用"; then
    echo "✅ 包含研究方法"
else
    echo "⚠️  缺少研究方法"
fi

if echo "$ABSTRACT" | grep -q "探索\|研究\|分析"; then
    echo "✅ 包含研究内容"
else
    echo "⚠️  缺少研究内容"
fi

if echo "$ABSTRACT" | grep -q "意义\|价值\|为.*提供"; then
    echo "✅ 包含研究价值"
else
    echo "⚠️  缺少研究价值"
fi

echo ""
echo "=== 建议 ==="
echo "模板：针对___现状，提出___假说，用___方法进行研究，探索___问题，对阐明___机制/揭示___规律具有意义。"
