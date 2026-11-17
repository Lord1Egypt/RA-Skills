"""v2.4.0 集成测试 — 端到端跑 Kent 当前 PDF"""
import sys
import os
import time
from pathlib import Path

# 加 skill 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from invoice_extractor import extract_all_invoices, detect_duplicates, extract_train_ticket_info

PDF = "/Users/home/Nutstore Files/我的坚果云/01_Unique/000伊登优格/04-财务管理/05-报销统计/idunique-20260628-20260810/F-发票合并.pdf"


class TestIntegration:
    """集成测试：端到端跑 Kent 的真实 PDF"""
    
    def test_pdf_exists(self):
        """PDF 文件存在"""
        assert os.path.exists(PDF), f"PDF 路径不存在: {PDF}"
    
    def test_total_invoice_count(self):
        """PDF 33 页 → 27 张发票（6 组重复合并）"""
        invoices = extract_all_invoices(PDF)
        assert len(invoices) == 27, f"期望 27 张，实际 {len(invoices)} 张"
    
    def test_no_duplicate_invoices(self):
        """发票不应重复（detect_duplicates 应返回空）"""
        invoices = extract_all_invoices(PDF)
        dupes = detect_duplicates(invoices)
        assert len(dupes) == 0, f"重复发票: {dupes}"
    
    def test_performance(self):
        """27 张发票耗时 < 2 秒"""
        t0 = time.time()
        invoices = extract_all_invoices(PDF)
        elapsed = time.time() - t0
        assert elapsed < 2.0, f"耗时 {elapsed:.2f}s 超过 2 秒"
    
    def test_field_completeness(self):
        """关键字段 100% 填全"""
        invoices = extract_all_invoices(PDF)
        critical_fields = ['发票号码', '开票日期', '购买方信息-名称', '购买方信息-统一社会信用代码',
                          '项目名称', '税额', '价税合计']
        for f in critical_fields:
            filled = sum(1 for i in invoices if i[f] not in (0, None, ''))
            assert filled == 27, f"{f}: {filled}/27"
    
    def test_train_ticket_count(self):
        """火车票 9 张（含 2 张退票费）"""
        invoices = extract_all_invoices(PDF)
        train = [i for i in invoices if '火车票' in i['项目名称']]
        refund = [i for i in invoices if '退票费' in i['项目名称']]
        assert len(train) == 9, f"期望 9 张火车票，实际 {len(train)} 张"
        assert len(refund) == 2, f"期望 2 张退票费，实际 {len(refund)} 张"
    
    def test_train_ticket_amount_verification(self):
        """火车票金额校验：金额 + 税额 = 价税合计"""
        invoices = extract_all_invoices(PDF)
        train = [i for i in invoices if '火车票' in i['项目名称']]
        for inv in train:
            diff = abs(inv['金额'] + inv['税额'] - inv['价税合计'])
            assert diff < 0.05, f"发票 {inv['发票号码']}: 金额 {inv['金额']} + 税额 {inv['税额']} = {inv['金额']+inv['税额']} ≠ 价税合计 {inv['价税合计']}"
    
    def test_train_ticket_total(self):
        """火车票合计：¥907.00（与旧规则一致）"""
        invoices = extract_all_invoices(PDF)
        train = [i for i in invoices if '火车票' in i['项目名称']]
        total = sum(i['价税合计'] for i in train)
        assert abs(total - 907.00) < 0.01, f"火车票合计 ¥{total:.2f} ≠ ¥907.00"
    
    def test_vat_invoice_total(self):
        """增值税合计：¥6,866.34（价税合计）"""
        invoices = extract_all_invoices(PDF)
        vat = [i for i in invoices if '火车票' not in i['项目名称']]
        total = sum(i['价税合计'] for i in vat)
        assert abs(total - 6866.34) < 0.01, f"增值税合计 ¥{total:.2f} ≠ ¥6866.34"
    
    def test_train_ticket_buyer_info(self):
        """火车票购方信息全部填全（v2.4.0 新规则核心）"""
        invoices = extract_all_invoices(PDF)
        train = [i for i in invoices if '火车票' in i['项目名称']]
        for inv in train:
            assert inv['购买方信息-名称'], f"发票 {inv['发票号码']} 购方空"
            assert inv['购买方信息-统一社会信用代码'], f"发票 {inv['发票号码']} 税号空"
    
    def test_train_ticket_rate(self):
        """火车票税率：7 张 9% + 2 张 6%"""
        invoices = extract_all_invoices(PDF)
        train = [i for i in invoices if '火车票' in i['项目名称']]
        rates = [i['税率/征收率'] for i in train]
        assert rates.count('9%') == 7, f"期望 7 张 9%，实际 {rates.count('9%')}"
        assert rates.count('6%') == 2, f"期望 2 张 6%，实际 {rates.count('6%')}"


class TestTrainTicketInfo:
    """火车票字段抽取单元测试"""
    
    def test_price_ticket(self):
        """票价场景：税率 9%，项目名称 = 火车票"""
        text = '''
        电子发票（铁路电子客票）
        上海虹桥 G600 徐州东
        站 站
        ￥305.00
        票价:
        购买方名称:伊登优格(上海)咨询管理有限公司 统一社会信用代码:91310000MAK7RM1U9D
        '''
        info = extract_train_ticket_info(text)
        assert info['total'] == 305.00
        assert info['rate'] == '9%'
        assert info['item_name'] == '火车票'
        assert info['tax'] == 25.18
        assert info['amount'] == 279.82
        assert '上海虹桥站' in info['note']
        assert 'G600' in info['note']
    
    def test_refund_ticket(self):
        """退票费场景：税率 6%，项目名称 = 火车票-退票费"""
        text = '''
        电子发票（铁路电子客票）
        南京南 G33 上海
        ￥5.00
        退票费:
        购买方名称:伊登优格(上海)咨询管理有限公司 统一社会信用代码:91310000MAK7RM1U9D
        '''
        info = extract_train_ticket_info(text)
        assert info['total'] == 5.00
        assert info['rate'] == '6%'
        assert info['item_name'] == '火车票-退票费'
        assert info['tax'] == 0.28
        assert info['amount'] == 4.72
    
    def test_buyer_extraction(self):
        """购方信息抽取"""
        text = '''
        购买方名称:伊登优格(上海)咨询管理有限公司 统一社会信用代码:91310000MAK7RM1U9D
        '''
        info = extract_train_ticket_info(text)
        assert info['buyer'] == '伊登优格(上海)咨询管理有限公司'
        assert info['buyer_code'] == '91310000MAK7RM1U9D'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
