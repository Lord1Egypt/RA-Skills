#!/bin/bash
# Li_python_sec_check 测试脚本

echo "========================================="
echo "Li_python_sec_check 测试"
echo "========================================="

# 测试不安全示例
echo ""
echo "📁 测试 1: 扫描不安全示例项目..."
python3 scripts/python_sec_check.py examples/unsafe-example --output ./test-reports

if [ $? -eq 0 ]; then
    echo "✅ 测试 1 完成"
else
    echo "❌ 测试 1 失败"
    exit 1
fi

# 检查报告是否生成
echo ""
echo "📊 检查报告..."
if [ -f "./test-reports/"*"_python_sec_report.md" ]; then
    echo "✅ 报告已生成"
    ls -lh ./test-reports/
else
    echo "❌ 报告未生成"
    exit 1
fi

echo ""
echo "========================================="
echo "✅ 所有测试通过！"
echo "========================================="
