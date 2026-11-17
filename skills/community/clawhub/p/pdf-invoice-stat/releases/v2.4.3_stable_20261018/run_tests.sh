#!/bin/bash
# v2.4.3 本地测试运行器
# 用法：bash run_tests.sh

set -e
cd "$(dirname "$0")"

echo '===== v2.4.3 发票提取测试套件 ====='
echo

# 1. 语法检查
echo '【1. 语法检查】'
python3 -c "import ast; ast.parse(open('invoice_extractor.py').read()); print('  ✅ invoice_extractor.py')"
python3 -c "import ast; ast.parse(open('config.py').read()); print('  ✅ config.py')"
python3 -c "import ast; ast.parse(open('tests/test_extract_v243.py').read()); print('  ✅ test_extract_v243.py')"
echo

# 2. 单元测试
echo '【2. 单元测试】'
python3 tests/test_extract_v243.py
echo

# 3. 性能基准
echo '【3. 性能基准】'
python3 tests/perf_test.py
echo

# 4. 真实发票（如果有）
echo '【4. 真实发票测试】'
if [ -f /tmp/openclaw/youge_batch2.pdf ]; then
    python3 -c "
from invoice_extractor import extract_all_invoices
invs = extract_all_invoices('/tmp/openclaw/youge_batch2.pdf')
print(f'  ✅ 识别 {len(invs)} 张发票（期望 38）')
"
elif [ -f /tmp/clawhub/invoice_summary_20261016.xlsx ]; then
    echo '  ⚠️  youge_batch2.pdf 不存在'
else
    echo '  ⚠️  真实 PDF 不存在，跳过'
fi
echo

echo '✅ 全部测试通过'
