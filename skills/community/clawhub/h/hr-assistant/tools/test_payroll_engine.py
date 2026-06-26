"""
HR 智能体 - 薪资计算引擎单元测试
"""

import unittest
from decimal import Decimal
from payroll_engine import (
    TaxCalculator,
    InsuranceCalculator,
    PayrollEngine,
    TaxBracket,
    MonthPayroll,
    YearEndBonus
)


class TestTaxCalculator(unittest.TestCase):
    """测试个税计算器"""
    
    def test_calculate_monthly_tax_basic(self):
        """测试基础个税计算"""
        # 月薪 10000，无社保，1月份
        tax, taxableIncome, cumulativeTax, bracketLevel, bracketRate, bracketChanged = TaxCalculator.calculateMonthlyTax(
            monthlyIncome=Decimal('10000'),
            monthlyInsurance=Decimal('0'),
            month=1
        )
        
        # 应纳税所得额 = 10000 - 5000 = 5000，税率 3%
        # 个税 = 5000 * 0.03 = 150
        self.assertEqual(tax, Decimal('150'))
        self.assertEqual(taxableIncome, Decimal('5000'))
        self.assertEqual(bracketLevel, 1)
        self.assertEqual(bracketRate, Decimal('0.03'))
        self.assertFalse(bracketChanged)
    
    def test_calculate_monthly_tax_with_insurance(self):
        """测试含社保的个税计算"""
        # 月薪 15000，社保 2000，1月份
        tax, taxableIncome, cumulativeTax, bracketLevel, bracketRate, bracketChanged = TaxCalculator.calculateMonthlyTax(
            monthlyIncome=Decimal('15000'),
            monthlyInsurance=Decimal('2000'),
            month=1
        )
        
        # 应纳税所得额 = 15000 - 5000 - 2000 = 8000，税率 3%
        # 个税 = 8000 * 0.03 = 240
        self.assertEqual(tax, Decimal('240'))
        self.assertEqual(bracketLevel, 1)
        self.assertEqual(bracketRate, Decimal('0.03'))
    
    def test_calculate_monthly_tax_cumulative(self):
        """测试累计预扣法"""
        # 1月份：月薪 20000，社保 3000
        tax1, taxableIncome1, cumulativeTax1, _, _, _ = TaxCalculator.calculateMonthlyTax(
            monthlyIncome=Decimal('20000'),
            monthlyInsurance=Decimal('3000'),
            month=1
        )
        # 应纳税所得额 = 20000 - 5000 - 3000 = 12000，税率 3%
        # 个税 = 12000 * 0.03 = 360
        self.assertEqual(tax1, Decimal('360'))
        
        # 2月份：同样的薪资
        tax2, taxableIncome2, cumulativeTax2, _, _, _ = TaxCalculator.calculateMonthlyTax(
            monthlyIncome=Decimal('20000'),
            monthlyInsurance=Decimal('3000'),
            month=2,
            cumulativeIncome=Decimal('20000'),
            cumulativeInsurance=Decimal('3000'),
            cumulativeTax=cumulativeTax1
        )
        # 累计应纳税所得额 = 40000 - 10000 - 6000 = 24000，税率 3%
        # 累计个税 = 24000 * 0.03 = 720
        # 本月个税 = 720 - 360 = 360
        self.assertEqual(tax2, Decimal('360'))
    
    def test_calculate_monthly_tax_bracket_change(self):
        """测试税率级距跳档"""
        # 高收入，测试跳档到 10%
        # 月薪 50000，社保 5000
        tax, taxableIncome, cumulativeTax, bracketLevel, bracketRate, bracketChanged = TaxCalculator.calculateMonthlyTax(
            monthlyIncome=Decimal('50000'),
            monthlyInsurance=Decimal('5000'),
            month=1
        )
        # 应纳税所得额 = 50000 - 5000 - 5000 = 40000
        # 其中 36000 按 3%，4000 按 10%
        # 个税 = 36000 * 0.03 + 4000 * 0.10 = 1080 + 400 = 1480
        self.assertEqual(tax, Decimal('1480'))
        self.assertEqual(bracketLevel, 2)
        self.assertEqual(bracketRate, Decimal('0.10'))
    
    def test_calculate_year_end_bonus(self):
        """测试年终奖计算（月薪=0 时并入综合所得更优）"""
        result = TaxCalculator.calculateYearEndBonus(Decimal('36000'))
        
        # 月薪为 0 时，并入综合所得：全年收入 36000 - 减除 60000 → 负数 → 税 0
        # 单独计税：36000 * 0.03 = 1080
        # 选择并入综合所得（更优）
        self.assertEqual(result.taxAmount, Decimal('0'))
        self.assertEqual(result.netBonus, Decimal('36000'))
        self.assertEqual(result.optimalMethod, "并入综合所得")

    def test_calculate_year_end_bonus_with_salary(self):
        """测试年终奖计算（有月薪时单独计税更优）"""
        result = TaxCalculator.calculateYearEndBonus(Decimal('36000'), Decimal('20000'))
        
        # 单独计税：36000 / 12 = 3000，税率 3%，税 = 1080
        # 并入综合所得：全年 = 240000 + 36000 - 60000 = 216000，税 = 216000*20% - 16920 = 26280
        #   不含年终奖：全年 = 240000 - 60000 = 180000，税 = 180000*20% - 16920 = 19080
        #   年终奖并入增加税 = 26280 - 19080 = 7200
        # 7200 > 1080 → 单独计税更优
        self.assertEqual(result.taxAmount, Decimal('1080'))
        self.assertEqual(result.netBonus, Decimal('34920'))
        self.assertEqual(result.optimalMethod, "单独计税")

    def test_calculate_year_end_bonus_high_amount(self):
        """测试高额度年终奖（月薪=0 时并入综合所得更优）"""
        result = TaxCalculator.calculateYearEndBonus(Decimal('100000'))
        
        # 单独计税：100000 / 12 = 8333.33，税率 10%，税 = 100000*0.10 - 210 = 9790
        # 并入综合所得：全年 = 100000 - 60000 = 40000，税 = 40000*10% - 2520 = 1480
        # 1480 < 9790 → 并入更优
        self.assertEqual(result.taxAmount, Decimal('1480'))
        self.assertEqual(result.netBonus, Decimal('98520'))
        self.assertEqual(result.optimalMethod, "并入综合所得")


class TestInsuranceCalculator(unittest.TestCase):
    """测试社保公积金计算器"""
    
    def test_calculate_insurance_beijing(self):
        """测试北京社保计算"""
        result = InsuranceCalculator.calculateInsurance(
            salary=Decimal('15000'),
            city="北京",
            year=2026
        )
        
        # 北京基数上限 35283，下限 6821，15000 在范围内
        # 养老：15000 * 8% = 1200
        self.assertEqual(result["pensionInsurance"], Decimal('1200'))
        # 医疗：15000 * 2% = 300
        self.assertEqual(result["medicalInsurance"], Decimal('300'))
        # 失业：15000 * 0.5% = 75
        self.assertEqual(result["unemploymentInsurance"], Decimal('75'))
        # 公积金：15000 * 12% = 1800
        self.assertEqual(result["housingFund"], Decimal('1800'))
        # 合计：3375
        self.assertEqual(result["totalInsurance"], Decimal('3375'))
    
    def test_calculate_insurance_with_base_limit(self):
        """测试缴费基数上下限"""
        # 低工资，按下限缴纳
        result = InsuranceCalculator.calculateInsurance(
            salary=Decimal('5000'),
            city="北京",
            year=2026
        )
        
        # 北京养老下限 6821
        # 养老：6821 * 8% = 545.68
        self.assertEqual(result["pensionInsurance"], Decimal('545.68'))
    
    def test_calculate_insurance_high_salary(self):
        """测试高工资（超过上限）"""
        result = InsuranceCalculator.calculateInsurance(
            salary=Decimal('50000'),
            city="北京",
            year=2026
        )
        
        # 北京基数上限 35283
        # 养老：35283 * 8% = 2822.64
        self.assertEqual(result["pensionInsurance"], Decimal('2822.64'))
    
    def test_unsupported_city(self):
        """测试不支持的城市应返回降级结果而非抛异常"""
        result = InsuranceCalculator.calculateInsurance(
            salary=Decimal('10000'),
            city="未知城市",
            year=2026
        )
        
        # 不支持城市时返回全 0 结果并标记
        self.assertTrue(result.get("_unsupportedCity"))
        self.assertEqual(result["pensionInsurance"], Decimal('0'))
        self.assertEqual(result["totalInsurance"], Decimal('0'))


class TestPayrollEngine(unittest.TestCase):
    """测试薪资计算引擎"""
    
    def setUp(self):
        self.engine = PayrollEngine()
    
    def test_calculate_payroll_basic(self):
        """测试基础薪资计算"""
        result = self.engine.calculatePayroll(
            employeeId="E001",
            employeeName="张三",
            year=2026,
            month=1,
            baseSalary=Decimal('15000'),
            city="北京"
        )
        
        # 验证结果类型
        self.assertIsInstance(result, MonthPayroll)
        self.assertEqual(result.employeeId, "E001")
        self.assertEqual(result.employeeName, "张三")
        
        # 验证应发
        self.assertEqual(result.grossPay, Decimal('15000'))
        
        # 验证社保（北京 15000 工资）
        self.assertEqual(result.pensionInsurance, Decimal('1200'))
        self.assertEqual(result.medicalInsurance, Decimal('300'))
        self.assertEqual(result.unemploymentInsurance, Decimal('75'))
        self.assertEqual(result.housingFund, Decimal('1800'))
        self.assertEqual(result.totalInsurance, Decimal('3375'))
        
        # 验证个税
        # 应纳税所得额 = 15000 - 5000 - 3375 = 6625
        # 税率 3%，个税 = 198.75
        expectedTax = Decimal('198.75')
        self.assertEqual(result.taxAmount, expectedTax)
        
        # 验证实发
        # 实发 = 15000 - 3375 - 198.75 = 11426.25
        expectedNetPay = Decimal('11426.25')
        self.assertEqual(result.netPay, expectedNetPay)
    
    def test_calculate_payroll_with_bonus(self):
        """测试含奖金的薪资计算"""
        result = self.engine.calculatePayroll(
            employeeId="E002",
            employeeName="李四",
            year=2026,
            month=3,
            baseSalary=Decimal('20000'),
            city="上海",
            positionAllowance=Decimal('3000'),
            performanceBonus=Decimal('5000')
        )
        
        # 应发 = 20000 + 3000 + 5000 = 28000
        self.assertEqual(result.grossPay, Decimal('28000'))
    
    def test_calculate_payroll_with_cumulative_data(self):
        """测试含累计数据的薪资计算"""
        result = self.engine.calculatePayroll(
            employeeId="E003",
            employeeName="王五",
            year=2026,
            month=6,
            baseSalary=Decimal('25000'),
            city="深圳",
            cumulativeData={
                "cumulativeIncome": Decimal('125000'),  # 前5个月累计收入
                "cumulativeInsurance": Decimal('25000'),  # 前5个月累计社保
                "cumulativeTax": Decimal('3750')  # 前5个月累计个税
            }
        )
        
        # 验证累计数据正确更新
        self.assertEqual(result.cumulativeIncome, Decimal('150000'))  # 125000 + 25000
    
    def test_batch_calculate_payroll(self):
        """测试批量薪资计算"""
        employees = [
            {
                "employeeId": "E001",
                "employeeName": "张三",
                "baseSalary": 15000,
                "city": "北京"
            },
            {
                "employeeId": "E002",
                "employeeName": "李四",
                "baseSalary": 20000,
                "city": "上海",
                "performanceBonus": 5000
            }
        ]
        
        results = self.engine.batchCalculatePayroll(
            employees=employees,
            year=2026,
            month=1
        )
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].employeeName, "张三")
        self.assertEqual(results[1].employeeName, "李四")
        self.assertEqual(results[1].grossPay, Decimal('25000'))  # 20000 + 5000


class TestEdgeCases(unittest.TestCase):
    """测试边界情况"""
    
    def test_zero_salary(self):
        """测试零工资"""
        engine = PayrollEngine()
        result = engine.calculatePayroll(
            employeeId="E001",
            employeeName="张三",
            year=2026,
            month=1,
            baseSalary=Decimal('0'),
            city="北京"
        )
        
        self.assertEqual(result.grossPay, Decimal('0'))
        self.assertEqual(result.taxAmount, Decimal('0'))
        self.assertEqual(result.netPay, Decimal('0'))
    
    def test_negative_taxable_income(self):
        """测试应纳税所得额为负"""
        # 工资低于起征点+社保
        tax, taxableIncome, cumulativeTax, _, _, _ = TaxCalculator.calculateMonthlyTax(
            monthlyIncome=Decimal('5000'),
            monthlyInsurance=Decimal('1000'),
            month=1
        )
        
        # 应纳税所得额 = 5000 - 5000 - 1000 = -1000，应为 0
        self.assertEqual(tax, Decimal('0'))
        self.assertEqual(taxableIncome, Decimal('0'))
    
    def test_high_income_tax_bracket(self):
        """测试高收入税率级距"""
        # 测试最高税率 45%
        tax, taxableIncome, cumulativeTax, bracketLevel, bracketRate, bracketChanged = TaxCalculator.calculateMonthlyTax(
            monthlyIncome=Decimal('100000'),
            monthlyInsurance=Decimal('5000'),
            month=12,
            cumulativeIncome=Decimal('1140000'),  # 前11个月累计 114万
            cumulativeInsurance=Decimal('55000'),
            cumulativeTax=Decimal('300000')
        )
        
        # 累计应纳税所得额 = 120万 - 6万 - 6万 = 108万
        # 超过 96万部分按 45%
        self.assertTrue(tax > 0)
        self.assertEqual(bracketLevel, 7)
        self.assertEqual(bracketRate, Decimal('0.45'))


def run_tests():
    """运行所有测试"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestTaxCalculator))
    suite.addTests(loader.loadTestsFromTestCase(TestInsuranceCalculator))
    suite.addTests(loader.loadTestsFromTestCase(TestPayrollEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
