"""
HR 智能体 - 薪资计算引擎
支持个税累计预扣法、社保公积金、年终奖优化
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
import json


# 设置 Decimal 精度
def _round_decimal(d, n=0):
    """四舍五入到指定小数位"""
    return d.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


@dataclass
class TaxBracket:
    """个税税率级距"""
    level: int                      # 级数
    minIncome: Decimal              # 下限（含）
    maxIncome: Optional[Decimal]    # 上限（不含），None 表示无上界
    rate: Decimal                   # 税率
    quickDeduction: Decimal         # 速算扣除数


@dataclass
class InsuranceConfig:
    """社保公积金配置"""
    city: str                       # 城市
    year: int                       # 年度
    
    # 养老保险
    pensionEmployeeRate: Decimal    # 个人比例
    pensionEmployerRate: Decimal    # 单位比例
    pensionBaseMin: Decimal         # 基数下限
    pensionBaseMax: Decimal         # 基数上限
    
    # 医疗保险
    medicalEmployeeRate: Decimal
    medicalEmployerRate: Decimal
    medicalBaseMin: Decimal
    medicalBaseMax: Decimal
    
    # 失业保险
    unemploymentEmployeeRate: Decimal
    unemploymentEmployerRate: Decimal
    unemploymentBaseMin: Decimal
    unemploymentBaseMax: Decimal
    
    # 工伤保险（仅单位缴纳）
    injuryEmployerRate: Decimal
    injuryBaseMin: Decimal
    injuryBaseMax: Decimal
    
    # 生育保险（仅单位缴纳）
    maternityEmployerRate: Decimal
    maternityBaseMin: Decimal
    maternityBaseMax: Decimal
    
    # 公积金
    housingFundEmployeeRate: Decimal
    housingFundEmployerRate: Decimal
    housingFundBaseMin: Decimal
    housingFundBaseMax: Decimal


@dataclass
class MonthPayroll:
    """单月薪资计算结果"""
    # 基本信息
    year: int
    month: int
    employeeId: str
    employeeName: str
    
    # 收入项（固定）
    baseSalary: Decimal = Decimal('0')           # 基本工资
    positionAllowance: Decimal = Decimal('0')    # 岗位津贴
    # 浮动项（需导入具体数据）
    performanceBonus: Decimal = Decimal('0')     # 绩效奖金
    overtimePay: Decimal = Decimal('0')          # 加班费
    otherIncome: Decimal = Decimal('0')          # 其他收入
    
    # 税前扣减项（考勤扣款、事假、迟到等）
    preTaxDeductions: Decimal = Decimal('0')      # 税前扣减合计
    
    # 收入合计（= 固定项 + 浮动项 - 税前扣减）
    grossPay: Decimal = Decimal('0')             # 应发合计
    
    # 扣除项 - 社保
    pensionInsurance: Decimal = Decimal('0')     # 养老保险
    medicalInsurance: Decimal = Decimal('0')     # 医疗保险
    unemploymentInsurance: Decimal = Decimal('0') # 失业保险
    socialInsurance: Decimal = Decimal('0')      # 社保小计（养老+医疗+失业）
    # 扣除项 - 公积金
    housingFund: Decimal = Decimal('0')          # 公积金
    totalInsurance: Decimal = Decimal('0')       # 社保公积金合计
    
    # 扣除项 - 其他
    otherDeductions: Decimal = Decimal('0')      # 其他扣除（税后）
    
    # 个税计算
    taxableIncome: Decimal = Decimal('0')        # 应纳税所得额
    taxAmount: Decimal = Decimal('0')            # 个税金额
    taxBracketLevel: int = 0                     # 当前税率级数
    taxBracketRate: Decimal = Decimal('0')       # 当前税率
    taxBracketChanged: bool = False              # 本月是否跳档
    
    # 实发工资
    netPay: Decimal = Decimal('0')               # 实发工资
    
    # 基数信息（供参考）
    socialInsuranceBaseUsed: Decimal = Decimal('0')  # 实际使用的社保基数
    housingFundBaseUsed: Decimal = Decimal('0')      # 实际使用的公积金基数
    
    # 累计数据（用于累计预扣法）
    cumulativeIncome: Decimal = Decimal('0')     # 累计收入
    cumulativeDeduction: Decimal = Decimal('0')  # 累计减除费用（5000*月数）
    cumulativeInsurance: Decimal = Decimal('0')  # 累计社保公积金
    cumulativeTaxableIncome: Decimal = Decimal('0')  # 累计应纳税所得额
    cumulativeTax: Decimal = Decimal('0')        # 累计已缴个税
    taxPayable: Decimal = Decimal('0')           # 本月应缴个税


@dataclass
class YearEndBonus:
    """年终奖计算结果"""
    bonusAmount: Decimal                         # 年终奖金额
    taxableBonus: Decimal = Decimal('0')         # 应纳税所得额
    taxAmount: Decimal = Decimal('0')            # 个税金额
    netBonus: Decimal = Decimal('0')             # 税后年终奖
    effectiveRate: Decimal = Decimal('0')        # 实际税率
    optimalMethod: str = ""                      # 最优计税方式


class TaxCalculator:
    """个税计算器"""
    
    # 2026年个税税率表（年度累计）
    TAX_BRACKETS_2026 = [
        TaxBracket(1, Decimal('0'), Decimal('36000'), Decimal('0.03'), Decimal('0')),
        TaxBracket(2, Decimal('36000'), Decimal('144000'), Decimal('0.10'), Decimal('2520')),
        TaxBracket(3, Decimal('144000'), Decimal('300000'), Decimal('0.20'), Decimal('16920')),
        TaxBracket(4, Decimal('300000'), Decimal('420000'), Decimal('0.25'), Decimal('31920')),
        TaxBracket(5, Decimal('420000'), Decimal('660000'), Decimal('0.30'), Decimal('52920')),
        TaxBracket(6, Decimal('660000'), Decimal('960000'), Decimal('0.35'), Decimal('85920')),
        TaxBracket(7, Decimal('960000'), None, Decimal('0.45'), Decimal('181920')),
    ]
    
    # 年终奖单独计税税率表（月度）
    BONUS_TAX_BRACKETS = [
        TaxBracket(1, Decimal('0'), Decimal('3000'), Decimal('0.03'), Decimal('0')),
        TaxBracket(2, Decimal('3000'), Decimal('12000'), Decimal('0.10'), Decimal('210')),
        TaxBracket(3, Decimal('12000'), Decimal('25000'), Decimal('0.20'), Decimal('1410')),
        TaxBracket(4, Decimal('25000'), Decimal('35000'), Decimal('0.25'), Decimal('2660')),
        TaxBracket(5, Decimal('35000'), Decimal('55000'), Decimal('0.30'), Decimal('4410')),
        TaxBracket(6, Decimal('55000'), Decimal('80000'), Decimal('0.35'), Decimal('7160')),
        TaxBracket(7, Decimal('80000'), None, Decimal('0.45'), Decimal('15160')),
    ]
    
    # 个税起征点（每月）
    DEDUCTION_BASE = Decimal('5000')
    
    @classmethod
    def calculateMonthlyTax(
        cls,
        monthlyIncome: Decimal,
        monthlyInsurance: Decimal,
        month: int,
        cumulativeIncome: Decimal = None,
        cumulativeInsurance: Decimal = None,
        cumulativeTax: Decimal = None,
        specialDeduction: Decimal = None
    ) -> Tuple[Decimal, Decimal, Decimal, int, Decimal, bool]:
        """
        计算单月个税（累计预扣法）
        
        Args:
            monthlyIncome: 当月收入
            monthlyInsurance: 当月社保公积金
            month: 月份（1-12）
            cumulativeIncome: 本年累计收入（不含本月）
            cumulativeInsurance: 本年累计社保公积金（不含本月）
            cumulativeTax: 本年累计已缴个税
            specialDeduction: 专项附加扣除（每月）
        
        Returns:
            (本月应缴个税, 累计应纳税所得额, 累计已缴个税, 税率级数, 税率, 是否跳档)
        """
        # 处理 None 默认值（用 is not None 避免 Decimal('0') 被 falsy 误判）
        zero = Decimal('0')
        cumulativeIncome = cumulativeIncome if cumulativeIncome is not None else zero
        cumulativeInsurance = cumulativeInsurance if cumulativeInsurance is not None else zero
        cumulativeTax = cumulativeTax if cumulativeTax is not None else zero
        specialDeduction = specialDeduction if specialDeduction is not None else zero
        
        # 累计收入
        newCumulativeIncome = cumulativeIncome + monthlyIncome
        
        # 累计减除费用（5000 * 月数）
        cumulativeDeduction = cls.DEDUCTION_BASE * month
        
        # 累计社保公积金
        newCumulativeInsurance = cumulativeInsurance + monthlyInsurance
        
        # 累计专项附加扣除
        cumulativeSpecialDeduction = specialDeduction * month
        
        # 累计应纳税所得额
        cumulativeTaxableIncome = (
            newCumulativeIncome 
            - cumulativeDeduction 
            - newCumulativeInsurance 
            - cumulativeSpecialDeduction
        )
        
        # 确保不为负
        cumulativeTaxableIncome = max(cumulativeTaxableIncome, Decimal('0'))
        
        # 计算累计应缴个税
        newCumulativeTax = cls._calculateTaxByBracket(cumulativeTaxableIncome)
        
        # 获取当前税率级距
        currentBracket = cls.getTaxBracket(cumulativeTaxableIncome)
        bracketLevel = currentBracket.level if currentBracket else 0
        bracketRate = currentBracket.rate if currentBracket else Decimal('0')
        
        # 检测跳档：上月所在级数 ≠ 本月
        bracketChanged = False
        if month > 1 and cumulativeTax is not None and cumulativeIncome is not None:
            # 上月累计应纳税所得额 = 上月累计收入 - 上月累计减除费用 - 上月累计社保 - 上月累计专项附加
            prevCumDeduction = cls.DEDUCTION_BASE * (month - 1)
            prevCumSpecial = specialDeduction * (month - 1)
            prevTaxable = (
                cumulativeIncome 
                - prevCumDeduction 
                - cumulativeInsurance 
                - prevCumSpecial
            )
            prevTaxable = max(prevTaxable, Decimal('0'))
            prevBracket = cls.getTaxBracket(prevTaxable)
            if prevBracket and currentBracket and prevBracket.level != currentBracket.level:
                bracketChanged = True
        
        # 本月应缴个税 = 累计应缴 - 累计已缴
        taxPayable = newCumulativeTax - cumulativeTax
        
        return taxPayable, cumulativeTaxableIncome, newCumulativeTax, bracketLevel, bracketRate, bracketChanged
    
    @classmethod
    def _calculateTaxByBracket(cls, taxableIncome: Decimal) -> Decimal:
        """根据税率表计算个税"""
        if taxableIncome <= 0:
            return Decimal('0')
        
        for bracket in cls.TAX_BRACKETS_2026:
            if bracket.maxIncome is None or taxableIncome <= bracket.maxIncome:
                return taxableIncome * bracket.rate - bracket.quickDeduction
        
        # 超过最高级距
        lastBracket = cls.TAX_BRACKETS_2026[-1]
        return taxableIncome * lastBracket.rate - lastBracket.quickDeduction
    
    @classmethod
    def calculateYearEndBonus(cls, bonusAmount: Decimal, monthlySalary: Decimal = Decimal('0')) -> YearEndBonus:
        """
        计算年终奖个税，自动选择最优计税方式
        
        Args:
            bonusAmount: 年终奖金额
            monthlySalary: 当月工资（用于并入综合所得的估算）
        
        Returns:
            年终奖计算结果
        """
        # ---- 方式1：单独计税 ----
        monthlyBonus = bonusAmount / 12
        taxRate = Decimal('0')
        quickDeduction = Decimal('0')
        
        for bracket in cls.BONUS_TAX_BRACKETS:
            if bracket.maxIncome is None or monthlyBonus <= bracket.maxIncome:
                taxRate = bracket.rate
                quickDeduction = bracket.quickDeduction
                break
        
        taxSeparate = bonusAmount * taxRate - quickDeduction
        if taxSeparate < Decimal('0'):
            taxSeparate = Decimal('0')
        netBonusSeparate = bonusAmount - taxSeparate
        
        # ---- 方式2：并入综合所得（估算） ----
        # 假设全年 12 个月工资相同，年终奖并入后重新计算全年个税
        annualIncome = monthlySalary * 12 + bonusAmount
        annualDeduction = cls.DEDUCTION_BASE * 12
        annualTaxable = max(annualIncome - annualDeduction, Decimal('0'))
        taxCombined = cls._calculateTaxByBracket(annualTaxable)
        
        # 不含年终奖的全年个税
        annualIncomeWithout = monthlySalary * 12
        annualTaxableWithout = max(annualIncomeWithout - annualDeduction, Decimal('0'))
        taxWithout = cls._calculateTaxByBracket(annualTaxableWithout)
        
        # 年终奖并入方式增加的税额
        taxBonusCombined = taxCombined - taxWithout
        if taxBonusCombined < Decimal('0'):
            taxBonusCombined = Decimal('0')
        netBonusCombined = bonusAmount - taxBonusCombined
        
        # ---- 选择最优方式 ----
        if taxBonusCombined <= taxSeparate:
            optimalMethod = "并入综合所得"
            taxAmount = taxBonusCombined
        else:
            optimalMethod = "单独计税"
            taxAmount = taxSeparate
        
        return YearEndBonus(
            bonusAmount=bonusAmount,
            taxableBonus=bonusAmount,
            taxAmount=taxAmount,
            netBonus=bonusAmount - taxAmount,
            effectiveRate=(taxAmount / bonusAmount * 100).quantize(Decimal('0.01')) if bonusAmount > 0 else Decimal('0'),
            optimalMethod=optimalMethod
        )
    
    @classmethod
    def getTaxBracket(cls, taxableIncome: Decimal) -> Optional[TaxBracket]:
        """获取适用的税率级距"""
        for bracket in cls.TAX_BRACKETS_2026:
            if bracket.maxIncome is None or taxableIncome <= bracket.maxIncome:
                return bracket
        return cls.TAX_BRACKETS_2026[-1]


class InsuranceCalculator:
    """社保公积金计算器"""
    
    # 2026年主要城市社保公积金配置（示例数据，实际需更新）
    CITY_CONFIGS = {
        "北京": InsuranceConfig(
            city="北京", year=2026,
            pensionEmployeeRate=Decimal('0.08'), pensionEmployerRate=Decimal('0.16'),
            pensionBaseMin=Decimal('6821'), pensionBaseMax=Decimal('35283'),
            medicalEmployeeRate=Decimal('0.02'), medicalEmployerRate=Decimal('0.095'),
            medicalBaseMin=Decimal('6821'), medicalBaseMax=Decimal('35283'),
            unemploymentEmployeeRate=Decimal('0.005'), unemploymentEmployerRate=Decimal('0.005'),
            unemploymentBaseMin=Decimal('6821'), unemploymentBaseMax=Decimal('35283'),
            injuryEmployerRate=Decimal('0.004'), injuryBaseMin=Decimal('6821'), injuryBaseMax=Decimal('35283'),
            maternityEmployerRate=Decimal('0.008'), maternityBaseMin=Decimal('6821'), maternityBaseMax=Decimal('35283'),
            housingFundEmployeeRate=Decimal('0.12'), housingFundEmployerRate=Decimal('0.12'),
            housingFundBaseMin=Decimal('2420'), housingFundBaseMax=Decimal('35283'),
        ),
        "上海": InsuranceConfig(
            city="上海", year=2026,
            pensionEmployeeRate=Decimal('0.08'), pensionEmployerRate=Decimal('0.16'),
            pensionBaseMin=Decimal('7384'), pensionBaseMax=Decimal('36921'),
            medicalEmployeeRate=Decimal('0.02'), medicalEmployerRate=Decimal('0.10'),
            medicalBaseMin=Decimal('7384'), medicalBaseMax=Decimal('36921'),
            unemploymentEmployeeRate=Decimal('0.005'), unemploymentEmployerRate=Decimal('0.005'),
            unemploymentBaseMin=Decimal('7384'), unemploymentBaseMax=Decimal('36921'),
            injuryEmployerRate=Decimal('0.002'), injuryBaseMin=Decimal('7384'), injuryBaseMax=Decimal('36921'),
            maternityEmployerRate=Decimal('0.01'), maternityBaseMin=Decimal('7384'), maternityBaseMax=Decimal('36921'),
            housingFundEmployeeRate=Decimal('0.07'), housingFundEmployerRate=Decimal('0.07'),
            housingFundBaseMin=Decimal('2590'), housingFundBaseMax=Decimal('36921'),
        ),
        "广州": InsuranceConfig(
            city="广州", year=2026,
            pensionEmployeeRate=Decimal('0.08'), pensionEmployerRate=Decimal('0.14'),
            pensionBaseMin=Decimal('5284'), pensionBaseMax=Decimal('26421'),
            medicalEmployeeRate=Decimal('0.02'), medicalEmployerRate=Decimal('0.085'),
            medicalBaseMin=Decimal('5284'), medicalBaseMax=Decimal('26421'),
            unemploymentEmployeeRate=Decimal('0.005'), unemploymentEmployerRate=Decimal('0.005'),
            unemploymentBaseMin=Decimal('5284'), unemploymentBaseMax=Decimal('26421'),
            injuryEmployerRate=Decimal('0.002'), injuryBaseMin=Decimal('5284'), injuryBaseMax=Decimal('26421'),
            maternityEmployerRate=Decimal('0.0085'), maternityBaseMin=Decimal('5284'), maternityBaseMax=Decimal('26421'),
            housingFundEmployeeRate=Decimal('0.05'), housingFundEmployerRate=Decimal('0.05'),
            housingFundBaseMin=Decimal('2300'), housingFundBaseMax=Decimal('39579'),
        ),
        "深圳": InsuranceConfig(
            city="深圳", year=2026,
            pensionEmployeeRate=Decimal('0.08'), pensionEmployerRate=Decimal('0.14'),
            pensionBaseMin=Decimal('5284'), pensionBaseMax=Decimal('26421'),
            medicalEmployeeRate=Decimal('0.02'), medicalEmployerRate=Decimal('0.06'),
            medicalBaseMin=Decimal('5284'), medicalBaseMax=Decimal('26421'),
            unemploymentEmployeeRate=Decimal('0.005'), unemploymentEmployerRate=Decimal('0.007'),
            unemploymentBaseMin=Decimal('5284'), unemploymentBaseMax=Decimal('26421'),
            injuryEmployerRate=Decimal('0.0014'), injuryBaseMin=Decimal('5284'), injuryBaseMax=Decimal('26421'),
            maternityEmployerRate=Decimal('0.005'), maternityBaseMin=Decimal('5284'), maternityBaseMax=Decimal('26421'),
            housingFundEmployeeRate=Decimal('0.05'), housingFundEmployerRate=Decimal('0.05'),
            housingFundBaseMin=Decimal('2360'), housingFundBaseMax=Decimal('43659'),
        ),
        "杭州": InsuranceConfig(
            city="杭州", year=2026,
            pensionEmployeeRate=Decimal('0.08'), pensionEmployerRate=Decimal('0.14'),
            pensionBaseMin=Decimal('4812'), pensionBaseMax=Decimal('24060'),
            medicalEmployeeRate=Decimal('0.02'), medicalEmployerRate=Decimal('0.095'),
            medicalBaseMin=Decimal('4812'), medicalBaseMax=Decimal('24060'),
            unemploymentEmployeeRate=Decimal('0.005'), unemploymentEmployerRate=Decimal('0.005'),
            unemploymentBaseMin=Decimal('4812'), unemploymentBaseMax=Decimal('24060'),
            injuryEmployerRate=Decimal('0.002'), injuryBaseMin=Decimal('4812'), injuryBaseMax=Decimal('24060'),
            maternityEmployerRate=Decimal('0.006'), maternityBaseMin=Decimal('4812'), maternityBaseMax=Decimal('24060'),
            housingFundEmployeeRate=Decimal('0.12'), housingFundEmployerRate=Decimal('0.12'),
            housingFundBaseMin=Decimal('2490'), housingFundBaseMax=Decimal('38390'),
        ),
    }
    
    @classmethod
    def getCityConfig(cls, city: str, year: int = 2026) -> Optional[InsuranceConfig]:
        """获取城市社保配置"""
        return cls.CITY_CONFIGS.get(city)
    
    @classmethod
    def calculateInsurance(
        cls,
        salary: Decimal,
        city: str,
        year: int = 2026,
        housingFundRate: Optional[Decimal] = None,
        housingFundBase: Optional[Decimal] = None
    ) -> Dict[str, Decimal]:
        """
        计算社保公积金
        
        Args:
            salary: 社保缴费基数（通常为上年度月平均工资，或花名册中的社保基数）
            city: 城市
            year: 年度
            housingFundRate: 自定义公积金比例（None 则使用默认）
            housingFundBase: 公积金缴费基数（None 则使用 salary）
        
        Returns:
            各项社保公积金金额，包含 socialInsurance 和 housingFund 分项。
            如果城市不支持，返回空结果（不会抛异常），并设置 _unsupportedCity 标记。
        """
        config = cls.getCityConfig(city, year)
        if not config:
            # Bug6 修复：不支持的城镇，返回零值结果而非崩溃
            return {
                "pensionInsurance": Decimal('0'),
                "medicalInsurance": Decimal('0'),
                "unemploymentInsurance": Decimal('0'),
                "socialInsurance": Decimal('0'),
                "housingFund": Decimal('0'),
                "totalInsurance": Decimal('0'),
                "employerPension": Decimal('0'),
                "employerMedical": Decimal('0'),
                "employerUnemployment": Decimal('0'),
                "employerHousingFund": Decimal('0'),
                "socialInsuranceBaseUsed": Decimal('0'),
                "housingFundBaseUsed": Decimal('0'),
                "_unsupportedCity": True,
            }
        
        # 确定缴费基数（在上下限之间）
        def getBase(base: Decimal, minBase: Decimal, maxBase: Decimal) -> Decimal:
            return max(min(base, maxBase), minBase)
        
        # 社保基数
        pensionBase = getBase(salary, config.pensionBaseMin, config.pensionBaseMax)
        medicalBase = getBase(salary, config.medicalBaseMin, config.medicalBaseMax)
        unemploymentBase = getBase(salary, config.unemploymentBaseMin, config.unemploymentBaseMax)
        
        # 公积金基数（可单独指定）
        hfActualBase = housingFundBase if housingFundBase is not None else salary
        housingFundBaseFinal = getBase(hfActualBase, config.housingFundBaseMin, config.housingFundBaseMax)
        
        # 计算个人缴纳部分
        pension = (pensionBase * config.pensionEmployeeRate).quantize(Decimal('0.01'))
        medical = (medicalBase * config.medicalEmployeeRate).quantize(Decimal('0.01'))
        unemployment = (unemploymentBase * config.unemploymentEmployeeRate).quantize(Decimal('0.01'))
        socialInsurance = pension + medical + unemployment
        
        # 公积金（可使用自定义比例）
        hfRate = housingFundRate if housingFundRate else config.housingFundEmployeeRate
        housingFund = (housingFundBaseFinal * hfRate).quantize(Decimal('0.01'))
        
        total = socialInsurance + housingFund
        
        return {
            # 个人社保（养老+医疗+失业）
            "pensionInsurance": pension,
            "medicalInsurance": medical,
            "unemploymentInsurance": unemployment,
            "socialInsurance": socialInsurance,
            # 个人公积金
            "housingFund": housingFund,
            # 合计
            "totalInsurance": total,
            # 单位缴纳部分（供参考）
            "employerPension": (pensionBase * config.pensionEmployerRate).quantize(Decimal('0.01')),
            "employerMedical": (medicalBase * config.medicalEmployerRate).quantize(Decimal('0.01')),
            "employerUnemployment": (unemploymentBase * config.unemploymentEmployerRate).quantize(Decimal('0.01')),
            "employerHousingFund": (housingFundBaseFinal * config.housingFundEmployerRate).quantize(Decimal('0.01')),
            # 基数信息（供参考）
            "socialInsuranceBaseUsed": pensionBase,  # 社保实际使用基数（取养老为代表）
            "housingFundBaseUsed": housingFundBaseFinal,
        }


class PayrollEngine:
    """薪资计算引擎"""
    
    def __init__(self):
        self.taxCalculator = TaxCalculator()
        self.insuranceCalculator = InsuranceCalculator()
    
    def calculatePayroll(
        self,
        employeeId: str,
        employeeName: str,
        year: int,
        month: int,
        baseSalary: Decimal,
        city: str,
        positionAllowance: Decimal = Decimal('0'),
        performanceBonus: Decimal = Decimal('0'),
        overtimePay: Decimal = Decimal('0'),
        otherIncome: Decimal = Decimal('0'),
        otherDeductions: Decimal = Decimal('0'),
        preTaxDeductions: Decimal = Decimal('0'),
        specialDeduction: Decimal = Decimal('0'),
        cumulativeData: Optional[Dict] = None,
        insuranceBase: Optional[Decimal] = None,
        housingFundBase: Optional[Decimal] = None,
        housingFundRate: Optional[Decimal] = None,
    ) -> MonthPayroll:
        """
        计算单月薪资
        
        Args:
            employeeId: 员工ID
            employeeName: 员工姓名
            year: 年份
            month: 月份
            baseSalary: 基本工资（从花名册读取）
            city: 社保缴纳城市
            positionAllowance: 岗位津贴
            performanceBonus: 绩效奖金（浮动项，需导入）
            overtimePay: 加班费（浮动项，需导入）
            otherIncome: 其他收入（浮动项，需导入）
            otherDeductions: 其他扣除（税后）
            preTaxDeductions: 税前扣减合计（考勤扣款、事假、迟到等）
            specialDeduction: 专项附加扣除（每月）
            cumulativeData: 累计数据 {cumulativeIncome, cumulativeInsurance, cumulativeTax}
            insuranceBase: 社保缴费基数（None 则使用花名册中的 socialInsuranceBase 或 baseSalary）
            housingFundBase: 公积金缴费基数（None 则使用 insuranceBase 或社保基数）
            housingFundRate: 公积金比例（None 则使用城市默认）
        
        Returns:
            薪资计算结果
        """
        # 应发合计 = 固定收入 + 浮动收入 - 税前扣减
        grossPay = (
            baseSalary + positionAllowance + performanceBonus + overtimePay + otherIncome
            - preTaxDeductions
        )
        
        # 确保应发不为负
        if grossPay < 0:
            grossPay = Decimal('0')
        
        # 社保基数：从花名册直接读取，由调用方传入（insuranceBase 参数）
        # 注意：基数应来自花名册的「社保基数」列，而非应发工资
        socialInsuranceBase = insuranceBase if insuranceBase is not None else grossPay
        
        # 计算社保公积金（应发为0时不计算）
        if grossPay <= 0:
            insuranceResult = {k: Decimal('0') for k in
                ["pensionInsurance", "medicalInsurance", "unemploymentInsurance",
                 "socialInsurance", "housingFund", "totalInsurance",
                 "socialInsuranceBaseUsed", "housingFundBaseUsed"]}
        else:
            insuranceResult = self.insuranceCalculator.calculateInsurance(
                socialInsuranceBase, city, year,
                housingFundRate=housingFundRate,
                housingFundBase=housingFundBase,
            )
        totalInsurance = insuranceResult["totalInsurance"]
        
        # 获取累计数据
        if cumulativeData is None:
            cumulativeData = {}
        
        cumulativeIncome = cumulativeData.get("cumulativeIncome", Decimal('0'))
        cumulativeInsurance = cumulativeData.get("cumulativeInsurance", Decimal('0'))
        cumulativeTax = cumulativeData.get("cumulativeTax", Decimal('0'))
        
        # 计算个税
        taxPayable, cumulativeTaxableIncome, newCumulativeTax, bracketLevel, bracketRate, bracketChanged = self.taxCalculator.calculateMonthlyTax(
            monthlyIncome=grossPay,
            monthlyInsurance=totalInsurance,
            month=month,
            cumulativeIncome=cumulativeIncome,
            cumulativeInsurance=cumulativeInsurance,
            cumulativeTax=cumulativeTax,
            specialDeduction=specialDeduction
        )
        
        # 实发工资 = 应发 - 社保公积金 - 个税 - 其他扣除（税后）
        netPay = grossPay - totalInsurance - taxPayable - otherDeductions
        
        return MonthPayroll(
            year=year,
            month=month,
            employeeId=employeeId,
            employeeName=employeeName,
            baseSalary=baseSalary,
            positionAllowance=positionAllowance,
            performanceBonus=performanceBonus,
            overtimePay=overtimePay,
            otherIncome=otherIncome,
            preTaxDeductions=preTaxDeductions,
            grossPay=grossPay,
            pensionInsurance=insuranceResult["pensionInsurance"],
            medicalInsurance=insuranceResult["medicalInsurance"],
            unemploymentInsurance=insuranceResult["unemploymentInsurance"],
            socialInsurance=insuranceResult["socialInsurance"],
            housingFund=insuranceResult["housingFund"],
            totalInsurance=totalInsurance,
            otherDeductions=otherDeductions,
            taxableIncome=cumulativeTaxableIncome,
            taxAmount=taxPayable,
            taxBracketLevel=bracketLevel,
            taxBracketRate=bracketRate,
            taxBracketChanged=bracketChanged,
            netPay=netPay,
            socialInsuranceBaseUsed=insuranceResult["socialInsuranceBaseUsed"],
            housingFundBaseUsed=insuranceResult["housingFundBaseUsed"],
            cumulativeIncome=cumulativeIncome + grossPay,
            cumulativeDeduction=Decimal('5000') * month,
            cumulativeInsurance=cumulativeInsurance + totalInsurance,
            cumulativeTaxableIncome=cumulativeTaxableIncome,
            cumulativeTax=newCumulativeTax,
            taxPayable=taxPayable
        )
    
    def calculateYearEndBonus(
        self,
        bonusAmount: Decimal,
        monthlySalary: Decimal = Decimal('0')
    ) -> YearEndBonus:
        """计算年终奖"""
        return self.taxCalculator.calculateYearEndBonus(bonusAmount, monthlySalary)
    
    def batchCalculatePayroll(
        self,
        employees: List[Dict],
        year: int,
        month: int,
        historicalData: Optional[Dict[str, Dict]] = None
    ) -> List[MonthPayroll]:
        """
        批量计算薪资
        
        Args:
            employees: 员工列表，每个员工包含薪资信息
                支持 "employeeId" 或 "empNo" 作为员工标识（兼容两种命名）
            year: 年份
            month: 月份
            historicalData: 历史累计数据
                key 支持 "employeeId" 或 "empNo"（自动兼容）
                value: {cumulativeIncome, cumulativeInsurance, cumulativeTax}
        
        Returns:
            薪资计算结果列表
        """
        results = []
        historicalData = historicalData or {}
        
        for emp in employees:
            # 兼容 employeeId 和 empNo 两种命名（Bug5 修复）
            employeeId = emp.get("employeeId") or emp.get("empNo", "")
            # historicalData 也兼容两种 key
            cumData = historicalData.get(employeeId)
            if cumData is None and "empNo" in emp:
                cumData = historicalData.get(emp["empNo"])
            if cumData is None and "employeeId" in emp:
                cumData = historicalData.get(emp["employeeId"])
            cumulativeData = cumData or {}
            
            result = self.calculatePayroll(
                employeeId=employeeId,
                employeeName=emp.get("employeeName", ""),
                year=year,
                month=month,
                baseSalary=Decimal(str(emp.get("baseSalary", 0))),
                city=emp.get("city", "北京"),
                positionAllowance=Decimal(str(emp.get("positionAllowance", 0))),
                performanceBonus=Decimal(str(emp.get("performanceBonus", 0))),
                overtimePay=Decimal(str(emp.get("overtimePay", 0))),
                otherIncome=Decimal(str(emp.get("otherIncome", 0))),
                otherDeductions=Decimal(str(emp.get("otherDeductions", 0))),
                preTaxDeductions=Decimal(str(emp.get("preTaxDeductions", 0))),
                specialDeduction=Decimal(str(emp.get("specialDeduction", 0))),
                cumulativeData=cumulativeData,
                insuranceBase=Decimal(str(emp["insuranceBase"])) if emp.get("insuranceBase") else None,
                housingFundBase=Decimal(str(emp["housingFundBase"])) if emp.get("housingFundBase") else None,
                housingFundRate=Decimal(str(emp["housingFundRate"])) if emp.get("housingFundRate") else None,
            )
            results.append(result)
        
        return results


# 工具函数（供 WorkBuddy 调用）
def calculate_payroll(
    employee_id: str,
    employee_name: str,
    year: int,
    month: int,
    base_salary: float,
    city: str,
    **kwargs
) -> Dict:
    """计算单月薪资"""
    engine = PayrollEngine()
    
    result = engine.calculatePayroll(
        employeeId=employee_id,
        employeeName=employee_name,
        year=year,
        month=month,
        baseSalary=Decimal(str(base_salary)),
        city=city,
        positionAllowance=Decimal(str(kwargs.get("position_allowance", 0))),
        performanceBonus=Decimal(str(kwargs.get("performance_bonus", 0))),
        overtimePay=Decimal(str(kwargs.get("overtime_pay", 0))),
        otherIncome=Decimal(str(kwargs.get("other_income", 0))),
        otherDeductions=Decimal(str(kwargs.get("other_deductions", 0))),
        preTaxDeductions=Decimal(str(kwargs.get("pre_tax_deductions", 0))),
        specialDeduction=Decimal(str(kwargs.get("special_deduction", 0))),
        cumulativeData=kwargs.get("cumulative_data"),
        insuranceBase=Decimal(str(kwargs["insurance_base"])) if kwargs.get("insurance_base") else None,
        housingFundBase=Decimal(str(kwargs["housing_fund_base"])) if kwargs.get("housing_fund_base") else None,
        housingFundRate=Decimal(str(kwargs["housing_fund_rate"])) if kwargs.get("housing_fund_rate") else None,
    )
    
    return {
        "success": True,
        "data": {
            "year": result.year,
            "month": result.month,
            "employeeId": result.employeeId,
            "employeeName": result.employeeName,
            "grossPay": float(result.grossPay),
            "totalInsurance": float(result.totalInsurance),
            "taxAmount": float(result.taxAmount),
            "netPay": float(result.netPay),
            "details": {
                "baseSalary": float(result.baseSalary),
                "positionAllowance": float(result.positionAllowance),
                "performanceBonus": float(result.performanceBonus),
                "preTaxDeductions": float(result.preTaxDeductions),
                "pensionInsurance": float(result.pensionInsurance),
                "medicalInsurance": float(result.medicalInsurance),
                "unemploymentInsurance": float(result.unemploymentInsurance),
                "socialInsurance": float(result.socialInsurance),
                "housingFund": float(result.housingFund),
            },
            "baseInfo": {
                "socialInsuranceBaseUsed": float(result.socialInsuranceBaseUsed),
                "housingFundBaseUsed": float(result.housingFundBaseUsed),
            },
            "taxInfo": {
                "bracketLevel": result.taxBracketLevel,
                "bracketRate": float(result.taxBracketRate),
                "bracketChanged": result.taxBracketChanged,
            },
            "cumulative": {
                "cumulativeIncome": float(result.cumulativeIncome),
                "cumulativeTaxableIncome": float(result.cumulativeTaxableIncome),
                "cumulativeTax": float(result.cumulativeTax)
            }
        }
    }


def calculate_year_end_bonus(bonus_amount: float, monthly_salary: float = 0) -> Dict:
    """计算年终奖"""
    engine = PayrollEngine()
    result = engine.calculateYearEndBonus(
        bonusAmount=Decimal(str(bonus_amount)),
        monthlySalary=Decimal(str(monthly_salary))
    )
    
    return {
        "success": True,
        "data": {
            "bonusAmount": float(result.bonusAmount),
            "taxAmount": float(result.taxAmount),
            "netBonus": float(result.netBonus),
            "effectiveRate": float(result.effectiveRate),
            "optimalMethod": result.optimalMethod
        }
    }


def calculate_insurance(salary: float, city: str, year: int = 2026) -> Dict:
    """计算社保公积金"""
    calculator = InsuranceCalculator()
    result = calculator.calculateInsurance(Decimal(str(salary)), city, year)
    
    return {
        "success": True,
        "data": {k: float(v) for k, v in result.items()}
    }


def get_tax_bracket(taxable_income: float) -> Dict:
    """获取适用税率级距"""
    bracket = TaxCalculator.getTaxBracket(Decimal(str(taxable_income)))
    
    if bracket:
        return {
            "success": True,
            "data": {
                "level": bracket.level,
                "minIncome": float(bracket.minIncome),
                "maxIncome": float(bracket.maxIncome) if bracket.maxIncome else None,
                "rate": float(bracket.rate),
                "quickDeduction": float(bracket.quickDeduction)
            }
        }
    
    return {"success": False, "error": "无法确定税率级距"}
