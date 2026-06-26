"""
考勤管理模块单元测试
"""

import unittest
import os
import sys
import json
import tempfile
from decimal import Decimal
from unittest.mock import patch, MagicMock

# 确保可以导入项目模块
sys.path.insert(0, os.path.dirname(__file__))

from attendance_manager import (
    AttendanceRecord, AttendanceRules, AttendanceManager, _round2
)


class TestRound2(unittest.TestCase):
    """测试四舍五入辅助函数"""
    
    def test_basic(self):
        self.assertEqual(_round2(1.234), Decimal('1.23'))
        self.assertEqual(_round2(1.235), Decimal('1.24'))
        self.assertEqual(_round2(0), Decimal('0'))
        self.assertEqual(_round2(None), Decimal('0'))
    
    def test_decimal_input(self):
        self.assertEqual(_round2(Decimal('10.005')), Decimal('10.01'))
        self.assertEqual(_round2(Decimal('99.999')), Decimal('100.00'))


class TestAttendanceRecord(unittest.TestCase):
    """测试考勤记录数据模型"""
    
    def test_default_values(self):
        record = AttendanceRecord(empNo="E001", year=2026, month=4)
        self.assertEqual(record.empNo, "E001")
        self.assertEqual(record.year, 2026)
        self.assertEqual(record.month, 4)
        self.assertEqual(record.lateCount, Decimal('0'))
        self.assertEqual(record.preTaxDeductions, Decimal('0'))
        self.assertEqual(record.deductionDetails, {})
    
    def test_custom_values(self):
        record = AttendanceRecord(
            empNo="E001", year=2026, month=4,
            lateCount=Decimal('5'),
            personalLeaveDays=Decimal('2'),
            preTaxDeductions=Decimal('300.00'),
        )
        self.assertEqual(record.lateCount, Decimal('5'))
        self.assertEqual(record.personalLeaveDays, Decimal('2'))
        self.assertEqual(record.preTaxDeductions, Decimal('300.00'))


class TestAttendanceRules(unittest.TestCase):
    """测试考勤规则"""
    
    def test_default_rules(self):
        rules = AttendanceRules.default()
        self.assertEqual(rules.lateFreeQuota, 2)
        self.assertEqual(rules.lateDeductionPerTime, Decimal('50'))
        self.assertEqual(rules.earlyLeaveFreeQuota, 2)
        self.assertEqual(rules.personalLeaveDeductionRate, Decimal('1.0'))
        self.assertEqual(rules.sickLeaveDeductionRate, Decimal('0.4'))
        self.assertEqual(rules.sickLeaveFreeDays, 0)
        self.assertEqual(rules.absentDeductionMultiplier, Decimal('2.0'))
        self.assertEqual(rules.overtimePayRate, Decimal('1.5'))


class TestAttendanceManagerDeductions(unittest.TestCase):
    """测试扣减计算逻辑"""
    
    def setUp(self):
        self.manager = AttendanceManager(filePath="dummy.xlsx")
        self.manager.records = {}
        # 标准日薪：10000 / 21.75 ≈ 459.77
        self.daily_salary = Decimal('459.77')
    
    def test_no_attendance_data(self):
        """无考勤数据时返回 0"""
        result = self.manager.calculateDeductions("E999", 2026, 4, self.daily_salary)
        self.assertEqual(result.preTaxDeductions, Decimal('0'))
        self.assertEqual(result.deductionDetails, {"note": "无考勤数据"})
    
    def test_no_deduction_clean_record(self):
        """完全正常的出勤记录不产生扣减"""
        record = AttendanceRecord(
            empNo="E001", year=2026, month=4,
            shouldAttendDays=Decimal('22'),
            actualAttendDays=Decimal('22'),
            lateCount=Decimal('0'),
        )
        self.manager.records["E001-2026-04"] = record
        
        result = self.manager.calculateDeductions("E001", 2026, 4, self.daily_salary)
        self.assertEqual(result.preTaxDeductions, Decimal('0'))
    
    def test_late_within_quota(self):
        """迟到次数在免费额度内不扣款"""
        record = AttendanceRecord(empNo="E001", year=2026, month=4, lateCount=Decimal('2'))
        self.manager.records["E001-2026-04"] = record
        
        result = self.manager.calculateDeductions("E001", 2026, 4, self.daily_salary)
        # 2 次迟到在免费额度内，不扣款
        self.assertEqual(result.preTaxDeductions, Decimal('0'))
    
    def test_late_exceed_quota(self):
        """迟到超过免费额度产生扣款"""
        record = AttendanceRecord(empNo="E001", year=2026, month=4, lateCount=Decimal('5'))
        self.manager.records["E001-2026-04"] = record
        
        result = self.manager.calculateDeductions("E001", 2026, 4, self.daily_salary)
        # 5 次 - 2 次免费 = 3 次超额，每次 50 元 = 150 元
        self.assertEqual(result.preTaxDeductions, Decimal('150.00'))
        self.assertIn("迟到扣款", result.deductionDetails)
    
    def test_personal_leave(self):
        """事假按全额日薪扣除"""
        record = AttendanceRecord(empNo="E001", year=2026, month=4, personalLeaveDays=Decimal('3'))
        self.manager.records["E001-2026-04"] = record
        
        result = self.manager.calculateDeductions("E001", 2026, 4, self.daily_salary)
        # 3 天 × 459.77 × 1.0 = 1379.31
        expected = _round2(self.daily_salary * 3 * Decimal('1.0'))
        self.assertEqual(result.preTaxDeductions, expected)
        self.assertIn("事假扣款", result.deductionDetails)
    
    def test_sick_leave(self):
        """病假按 40% 日薪扣除"""
        record = AttendanceRecord(empNo="E001", year=2026, month=4, sickLeaveDays=Decimal('5'))
        self.manager.records["E001-2026-04"] = record
        
        result = self.manager.calculateDeductions("E001", 2026, 4, self.daily_salary)
        # 5 天 × 459.77 × 0.4 = 919.54
        expected = _round2(self.daily_salary * 5 * Decimal('0.4'))
        self.assertEqual(result.preTaxDeductions, expected)
        self.assertIn("病假扣款", result.deductionDetails)
    
    def test_sick_leave_with_free_days(self):
        """病假有免扣天数"""
        rules = AttendanceRules(sickLeaveFreeDays=2)
        manager = AttendanceManager("dummy.xlsx", rules=rules)
        record = AttendanceRecord(empNo="E001", year=2026, month=4, sickLeaveDays=Decimal('5'))
        manager.records["E001-2026-04"] = record
        
        result = manager.calculateDeductions("E001", 2026, 4, self.daily_salary)
        # (5 - 2) 天 × 459.77 × 0.4 = 3 × 459.77 × 0.4 = 551.72
        effective_days = Decimal('3')
        expected = _round2(self.daily_salary * effective_days * Decimal('0.4'))
        self.assertEqual(result.preTaxDeductions, expected)
    
    def test_absent(self):
        """旷工按 2 倍日薪扣除"""
        record = AttendanceRecord(empNo="E001", year=2026, month=4, absentDays=Decimal('1'))
        self.manager.records["E001-2026-04"] = record
        
        result = self.manager.calculateDeductions("E001", 2026, 4, self.daily_salary)
        # 1 天 × 459.77 × 2.0 = 919.54
        expected = _round2(self.daily_salary * 1 * Decimal('2.0'))
        self.assertEqual(result.preTaxDeductions, expected)
        self.assertIn("旷工扣款", result.deductionDetails)
    
    def test_overtime_reduces_deduction(self):
        """加班费可以抵扣考勤扣减"""
        # 同时有迟到扣款和加班费
        record = AttendanceRecord(
            empNo="E001", year=2026, month=4,
            lateCount=Decimal('4'),  # 超额 2 次 = 100 元
            overtimeHours=Decimal('8'),  # 8 小时加班
        )
        self.manager.records["E001-2026-04"] = record
        
        result = self.manager.calculateDeductions("E001", 2026, 4, self.daily_salary)
        # 迟到扣款: (4-2) × 50 = 100
        # 加班费: (459.77/8) × 8 × 1.5 = 689.66
        # 扣减 = max(100 - 689.66, 0) = 0
        self.assertEqual(result.preTaxDeductions, Decimal('0'))
        self.assertIn("迟到扣款", result.deductionDetails)
        self.assertIn("加班费", result.deductionDetails)
    
    def test_zero_daily_salary(self):
        """日薪为 0 时跳过扣减计算"""
        record = AttendanceRecord(empNo="E001", year=2026, month=4, personalLeaveDays=Decimal('5'))
        self.manager.records["E001-2026-04"] = record
        
        result = self.manager.calculateDeductions("E001", 2026, 4, Decimal('0'))
        self.assertEqual(result.preTaxDeductions, Decimal('0'))
    
    def test_combined_deductions(self):
        """综合测试：迟到+事假+病假"""
        record = AttendanceRecord(
            empNo="E001", year=2026, month=4,
            lateCount=Decimal('4'),         # 超额 2 次
            personalLeaveDays=Decimal('1'),  # 1 天事假
            sickLeaveDays=Decimal('2'),      # 2 天病假
        )
        self.manager.records["E001-2026-04"] = record
        
        result = self.manager.calculateDeductions("E001", 2026, 4, self.daily_salary)
        
        # 迟到: 2 × 50 = 100
        late_ded = _round2(Decimal('2') * Decimal('50'))
        # 事假: 1 × 459.77 × 1.0 = 459.77
        personal_ded = _round2(self.daily_salary * 1 * Decimal('1.0'))
        # 病假: 2 × 459.77 × 0.4 = 367.82
        sick_ded = _round2(self.daily_salary * 2 * Decimal('0.4'))
        
        expected = _round2(late_ded + personal_ded + sick_ded)
        self.assertEqual(result.preTaxDeductions, expected)
        self.assertIn("迟到扣款", result.deductionDetails)
        self.assertIn("事假扣款", result.deductionDetails)
        self.assertIn("病假扣款", result.deductionDetails)
    
    def test_early_leave_exceed_quota(self):
        """早退超过免费额度"""
        record = AttendanceRecord(empNo="E001", year=2026, month=4, earlyLeaveCount=Decimal('5'))
        self.manager.records["E001-2026-04"] = record
        
        result = self.manager.calculateDeductions("E001", 2026, 4, self.daily_salary)
        # (5-2) × 50 = 150
        self.assertEqual(result.preTaxDeductions, Decimal('150.00'))
        self.assertIn("早退扣款", result.deductionDetails)


class TestAttendanceManagerBatch(unittest.TestCase):
    """测试批量计算"""
    
    def setUp(self):
        self.manager = AttendanceManager(filePath="dummy.xlsx")
        self.daily_salary = Decimal('459.77')
    
    def test_batch_calculate(self):
        """批量计算指定月份的扣减"""
        # 添加 3 条不同月份的记录
        self.manager.records["E001-2026-04"] = AttendanceRecord(
            empNo="E001", year=2026, month=4, personalLeaveDays=Decimal('1'))
        self.manager.records["E002-2026-04"] = AttendanceRecord(
            empNo="E002", year=2026, month=4, lateCount=Decimal('5'))
        self.manager.records["E001-2026-03"] = AttendanceRecord(
            empNo="E001", year=2026, month=3, personalLeaveDays=Decimal('2'))
        
        daily_salaries = {"E001": self.daily_salary, "E002": self.daily_salary}
        results = self.manager.batchCalculateDeductions(2026, 4, daily_salaries)
        
        # 只计算 4 月的记录
        self.assertEqual(len(results), 2)
        self.assertIn("E001", results)
        self.assertIn("E002", results)
    
    def test_get_all_pre_tax_deductions(self):
        """获取批量扣减总额"""
        self.manager.records["E001-2026-04"] = AttendanceRecord(
            empNo="E001", year=2026, month=4, personalLeaveDays=Decimal('1'))
        self.manager.records["E002-2026-04"] = AttendanceRecord(
            empNo="E002", year=2026, month=4, personalLeaveDays=Decimal('2'))
        
        daily_salaries = {"E001": self.daily_salary, "E002": self.daily_salary}
        deductions = self.manager.getAllPreTaxDeductions(2026, 4, daily_salaries)
        
        self.assertIn("E001", deductions)
        self.assertIn("E002", deductions)
        self.assertGreater(deductions["E001"], Decimal('0'))
        self.assertGreater(deductions["E002"], Decimal('0'))


class TestAttendanceManagerQueries(unittest.TestCase):
    """测试查询功能"""
    
    def setUp(self):
        self.manager = AttendanceManager(filePath="dummy.xlsx")
        self.manager.records = {
            "E001-2026-04": AttendanceRecord(empNo="E001", year=2026, month=4),
            "E001-2026-03": AttendanceRecord(empNo="E001", year=2026, month=3),
            "E002-2026-04": AttendanceRecord(empNo="E002", year=2026, month=4),
        }
    
    def test_get_record(self):
        record = self.manager.getRecord("E001", 2026, 4)
        self.assertIsNotNone(record)
        self.assertEqual(record.empNo, "E001")
    
    def test_get_record_not_found(self):
        record = self.manager.getRecord("E999", 2026, 4)
        self.assertIsNone(record)
    
    def test_get_monthly_records(self):
        records = self.manager.getMonthlyRecords(2026, 4)
        self.assertEqual(len(records), 2)
    
    def test_get_employee_records(self):
        records = self.manager.getEmployeeRecords("E001")
        self.assertEqual(len(records), 2)
        # 按月排序
        self.assertEqual(records[0].month, 3)
        self.assertEqual(records[1].month, 4)
    
    def test_get_deduction_summary(self):
        summary = self.manager.getDeductionSummary(2026, 4)
        self.assertEqual(summary["recordCount"], 2)
        self.assertEqual(summary["year"], 2026)
        self.assertEqual(summary["month"], 4)


class TestAttendanceManagerLoading(unittest.TestCase):
    """测试从 Excel 加载（使用真实临时文件）"""
    
    def test_file_not_exists(self):
        manager = AttendanceManager(filePath="/nonexistent/path.xlsx")
        result = manager.load()
        self.assertFalse(result["success"])
    
    def test_load_success(self):
        """使用真实临时 xlsx 文件测试加载"""
        from openpyxl import Workbook
        
        config = {
            "empNo": "工号",
            "year": "年份",
            "month": "月份",
            "lateCount": "迟到次数",
            "personalLeaveDays": "事假天数",
        }
        
        # 创建真实 xlsx 文件
        wb = Workbook()
        ws = wb.active
        ws.title = "考勤"
        ws.append(["工号", "年份", "月份", "迟到次数", "事假天数"])
        ws.append(["E001", 2026, 4, 3, 1])
        ws.append(["E002", 2026, 4, 0, 2])
        
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, "test_attendance.xlsx")
        wb.save(temp_path)
        
        try:
            manager = AttendanceManager(filePath=temp_path, config=config)
            result = manager.load()
            
            self.assertTrue(result["success"])
            self.assertEqual(result["recordCount"], 2)
            self.assertIn("E001-2026-04", manager.records)
            self.assertIn("E002-2026-04", manager.records)
        finally:
            os.unlink(temp_path)
            os.rmdir(temp_dir)
    
    def test_load_with_sheet_name(self):
        """测试指定 sheetName"""
        from openpyxl import Workbook
        
        config = {"empNo": "工号", "year": "年份", "month": "月份", "sheetName": "4月考勤"}
        
        wb = Workbook()
        ws = wb.active
        ws.title = "4月考勤"
        ws.append(["工号", "年份", "月份"])
        ws.append(["E001", 2026, 4])
        
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, "test_attendance2.xlsx")
        wb.save(temp_path)
        
        try:
            manager = AttendanceManager(filePath=temp_path, config=config)
            result = manager.load()
            self.assertTrue(result["success"])
        finally:
            os.unlink(temp_path)
            os.rmdir(temp_dir)


if __name__ == '__main__':
    unittest.main()
