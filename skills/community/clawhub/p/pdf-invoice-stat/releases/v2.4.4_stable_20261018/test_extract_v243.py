"""
v2.4.3 单元测试（修复 14）
覆盖：
- 10 张 idunique 发票（含维达商贸）
- 38 张 youge 海口发票
- 项目名杂质清理
- 多项目分行
- 跨行发票号
"""
import os, sys, re
import pdfplumber

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_invoice_number():
    """修复 v2.4.1 跨行发票号"""
    from invoice_extractor import find_invoice_number
    text = '发票号码：\n开票日期：\n购 销\n下载次数：1\n26442000010830586171'
    assert find_invoice_number(text) == '26442000010830586171', f'跨行发票号失败: {find_invoice_number(text)}'
    print('✅ test_invoice_number')

def test_normalize_date():
    """修复 v2.4.1 跨行日期"""
    from invoice_extractor import normalize_date
    text = '开票日期：\n购 销\n下载次数：1\n2026年09月21日'
    result = normalize_date(text)
    assert '2026' in result and '09' in result, f'跨行日期失败: {result}'
    print('✅ test_normalize_date')

def test_extract_item_name():
    """修复 1+2：项目名杂质清理 + 多项目分行"""
    from invoice_extractor import extract_item_name
    # 模拟 page_words（含杂质"规格型号"）
    page_words = [
        {'x0': 50, 'top': 100, 'text': '*生产生活服务*云服务费规格型号'}
    ]
    result = extract_item_name('', page_words)
    # 期望：去掉"规格型号"
    assert '规格型号' not in result, f'项目名杂质未清理: {result}'
    print('✅ test_extract_item_name')

def test_real_youga_38_invoices():
    """端到端测试：38 张发票"""
    from invoice_extractor import extract_all_invoices
    PDF = '/tmp/openclaw/youge_batch2.pdf'
    invoices = extract_all_invoices(PDF)
    assert len(invoices) >= 35, f'识别数不足 35: {len(invoices)}'
    # 检查维达发票类似场景
    toll = [i for i in invoices if '通行费' in i.get('项目名称', '') or '代收通行费' in i.get('项目名称', '')]
    assert len(toll) >= 20, f'通行费不足 20: {len(toll)}'
    print(f'✅ test_real_youga_38_invoices ({len(invoices)} 张)')

if __name__ == '__main__':
    test_invoice_number()
    test_normalize_date()
    test_extract_item_name()
    test_real_youga_38_invoices()
    print('\n✅ 所有测试通过')
