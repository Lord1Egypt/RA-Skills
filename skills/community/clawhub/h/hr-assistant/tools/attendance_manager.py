"""
HR 智能体 - 考勤管理模块
处理考勤数据的导入、管理和扣减自动计算。

功能：
  1. 从绑定好的考勤 Excel 导入考勤数据
  2. 按规则自动计算迟到/早退/事假/病假/旷工扣款
  3. 为薪资计算提供 preTaxDeductions 数据
  4. 考勤规则可配置（额度、扣款标准等）

数据模型：
  AttendanceRecord - 单条考勤记录
  AttendanceRules - 扣减规则配置
"""

import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from decimal import Decimal, ROUND_HALF_UP


def _round2(d) -> Decimal:
    """四舍五入到 2 位小数"""
    if d is None:
        return Decimal('0')
    return Decimal(str(d)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


@dataclass
class AttendanceRecord:
    """单条考勤记录"""
    empNo: str                              # 工号
    year: int                               # 年份
    month: int                              # 月份
    shouldAttendDays: Decimal = Decimal('0')  # 应出勤天数
    actualAttendDays: Decimal = Decimal('0')  # 实际出勤天数
    lateCount: Decimal = Decimal('0')       # 迟到次数
    earlyLeaveCount: Decimal = Decimal('0')  # 早退次数
    personalLeaveDays: Decimal = Decimal('0')  # 事假天数
    sickLeaveDays: Decimal = Decimal('0')   # 病假天数
    absentDays: Decimal = Decimal('0')      # 旷工天数
    overtimeHours: Decimal = Decimal('0')   # 加班小时数
    # 计算结果
    preTaxDeductions: Decimal = Decimal('0')  # 考勤扣减合计
    deductionDetails: Dict = field(default_factory=dict)  # 扣减明细


@dataclass
class AttendanceRules:
    """
    考勤扣减规则（可配置）
    
    所有金额单位：元
    所有比例：Decimal（如 0.5 表示 50%）
    """
    # 迟到/早退
    lateFreeQuota: int = 2                  # 每月免费迟到次数
    lateDeductionPerTime: Decimal = Decimal('50')  # 超额迟到每次扣款
    earlyLeaveFreeQuota: int = 2             # 每月免费早退次数
    earlyLeaveDeductionPerTime: Decimal = Decimal('50')  # 超额早退每次扣款
    
    # 事假
    personalLeaveDeductionRate: Decimal = Decimal('1.0')  # 事假扣薪比例（1.0 = 全额扣日薪）
    
    # 病假
    sickLeaveDeductionRate: Decimal = Decimal('0.4')  # 病假扣薪比例（0.4 = 扣 40% 日薪）
    sickLeaveFreeDays: int = 0               # 每月免扣病假天数
    
    # 旷工
    absentDeductionMultiplier: Decimal = Decimal('2.0')  # 旷工扣薪倍数（2.0 = 扣 2 倍日薪）
    
    # 加班
    overtimePayRate: Decimal = Decimal('1.5')  # 加班费倍率（按日薪/8h 计算）
    
    @classmethod
    def default(cls) -> 'AttendanceRules':
        """返回默认规则"""
        return cls()


class AttendanceManager:
    """
    考勤管理器
    负责考勤数据的加载、查询和扣减计算。
    """
    
    def __init__(self, filePath: str, config: Optional[Dict] = None, rules: Optional[AttendanceRules] = None):
        """
        初始化考勤管理器
        
        Args:
            filePath: 考勤 Excel 文件路径
            config: 列映射配置 {标准字段名: 实际列名}，由 onboarding 自动生成
            rules: 扣减规则，None 则使用默认规则
        """
        self.filePath = filePath
        self.config = config or {}
        self.rules = rules or AttendanceRules.default()
        self.records: Dict[str, AttendanceRecord] = {}  # key: "empNo-year-month"
        self._loaded = False
    
    def load(self) -> Dict[str, Any]:
        """
        加载考勤数据
        
        Returns:
            {success, message, recordCount}
        """
        from excel_adapter import ExcelAdapter
        
        if not os.path.exists(self.filePath):
            return {"success": False, "message": f"考勤文件不存在: {self.filePath}"}
        
        try:
            adapter = ExcelAdapter(self.filePath)
            sheetName = self.config.get("sheetName")
            data = adapter.readData(sheetName)
        except Exception as e:
            return {"success": False, "message": f"读取考勤文件失败: {e}"}
        
        if not data or not isinstance(data, list) or len(data) == 0:
            return {"success": False, "message": "考勤文件无数据"}
        
        # 列名映射：config 中保存的是 {标准字段: 实际列名}
        # readData 返回 List[Dict]，每个 dict 的 key 是实际列名
        # 正向映射：标准字段名 → 实际列名（直接使用 config）
        col_mapping = {k: v for k, v in self.config.items()}
        
        # 逐条读取
        loaded = 0
        for row_data in data:
            if not isinstance(row_data, dict):
                continue
            record = self._parseRowDict(row_data, col_mapping)
            if record:
                key = f"{record.empNo}-{record.year}-{record.month:02d}"
                self.records[key] = record
                loaded += 1
        
        self._loaded = True
        return {
            "success": True,
            "message": f"已加载 {loaded} 条考勤记录",
            "recordCount": loaded
        }
    
    def _parseRowDict(self, row: Dict, col_mapping: Dict[str, str]) -> Optional[AttendanceRecord]:
        """解析单行数据（dict 格式，来自 readData）为 AttendanceRecord"""
        def get_val(field: str) -> Any:
            # 通过正向映射找到实际列名，再从 row 中取值
            actual_col = col_mapping.get(field)
            if actual_col and actual_col in row:
                return row[actual_col]
            # 也直接尝试标准字段名
            return row.get(field)
        
        emp_no = get_val("empNo")
        if not emp_no:
            return None
        
        year = get_val("year")
        month = get_val("month")
        if year is None or month is None:
            return None
        
        try:
            year = int(year)
            month = int(month)
        except (ValueError, TypeError):
            return None
        
        return AttendanceRecord(
            empNo=str(emp_no).strip(),
            year=year,
            month=month,
            shouldAttendDays=_round2(get_val("shouldAttendDays")),
            actualAttendDays=_round2(get_val("actualAttendDays")),
            lateCount=_round2(get_val("lateCount")),
            earlyLeaveCount=_round2(get_val("earlyLeaveCount")),
            personalLeaveDays=_round2(get_val("personalLeaveDays")),
            sickLeaveDays=_round2(get_val("sickLeaveDays")),
            absentDays=_round2(get_val("absentDays")),
            overtimeHours=_round2(get_val("overtimeHours")),
        )
    
    def calculateDeductions(self, empNo: str, year: int, month: int,
                            dailySalary: Decimal) -> AttendanceRecord:
        """
        计算单个员工的考勤扣减
        
        Args:
            empNo: 工号
            year: 年份
            month: 月份
            dailySalary: 日薪（= 月薪 / 应出勤天数，或 月薪 / 21.75）
        
        Returns:
            包含扣减明细的考勤记录
        """
        key = f"{empNo}-{year}-{month:02d}"
        record = self.records.get(key)
        
        if not record:
            return AttendanceRecord(
                empNo=empNo, year=year, month=month,
                preTaxDeductions=Decimal('0'),
                deductionDetails={"note": "无考勤数据"}
            )
        
        return self._applyRules(record, dailySalary)
    
    def batchCalculateDeductions(self, year: int, month: int,
                                  dailySalaries: Dict[str, Decimal]) -> Dict[str, AttendanceRecord]:
        """
        批量计算考勤扣减
        
        Args:
            year: 年份
            month: 月份
            dailySalaries: {empNo: dailySalary} 日薪映射
        
        Returns:
            {empNo: AttendanceRecord} 包含扣减的记录
        """
        results = {}
        for key, record in self.records.items():
            emp_no, rec_year, rec_month = key.rsplit('-', 2)
            try:
                rec_year = int(rec_year)
                rec_month = int(rec_month)
            except ValueError:
                continue
            
            # 只计算指定年月的记录
            if rec_year != year or rec_month != month:
                continue
            
            daily_salary = dailySalaries.get(emp_no, Decimal('0'))
            results[emp_no] = self._applyRules(record, daily_salary)
        
        return results
    
    def _applyRules(self, record: AttendanceRecord, dailySalary: Decimal) -> AttendanceRecord:
        """应用扣减规则"""
        if dailySalary <= 0:
            record.preTaxDeductions = Decimal('0')
            record.deductionDetails = {"note": "日薪为0，跳过扣减计算"}
            return record
        
        details = {}
        total = Decimal('0')
        
        # 1. 迟到扣款
        late_ded = self._calcLateDeduction(record.lateCount)
        if late_ded > 0:
            details["迟到扣款"] = float(late_ded)
            total += late_ded
        
        # 2. 早退扣款
        early_ded = self._calcEarlyLeaveDeduction(record.earlyLeaveCount)
        if early_ded > 0:
            details["早退扣款"] = float(early_ded)
            total += early_ded
        
        # 3. 事假扣款 = 日薪 × 事假天数 × 比例
        personal_ded = dailySalary * record.personalLeaveDays * self.rules.personalLeaveDeductionRate
        personal_ded = _round2(personal_ded)
        if personal_ded > 0:
            details["事假扣款"] = float(personal_ded)
            details["事假明细"] = f"{record.personalLeaveDays}天 × ¥{dailySalary} × {self.rules.personalLeaveDeductionRate}"
            total += personal_ded
        
        # 4. 病假扣款 = 日薪 × 病假天数 × 比例（扣除免扣天数）
        effective_sick_days = max(Decimal('0'), record.sickLeaveDays - Decimal(str(self.rules.sickLeaveFreeDays)))
        sick_ded = dailySalary * effective_sick_days * self.rules.sickLeaveDeductionRate
        sick_ded = _round2(sick_ded)
        if sick_ded > 0:
            details["病假扣款"] = float(sick_ded)
            details["病假明细"] = f"{effective_sick_days}天 × ¥{dailySalary} × {self.rules.sickLeaveDeductionRate}"
            total += sick_ded
        
        # 5. 旷工扣款 = 日薪 × 旷工天数 × 倍数
        absent_ded = dailySalary * record.absentDays * self.rules.absentDeductionMultiplier
        absent_ded = _round2(absent_ded)
        if absent_ded > 0:
            details["旷工扣款"] = float(absent_ded)
            details["旷工明细"] = f"{record.absentDays}天 × ¥{dailySalary} × {self.rules.absentDeductionMultiplier}"
            total += absent_ded
        
        # 6. 加班费（正项，可抵扣）
        overtime_pay = dailySalary / Decimal('8') * record.overtimeHours * self.rules.overtimePayRate
        overtime_pay = _round2(overtime_pay)
        if overtime_pay > 0:
            details["加班费"] = float(overtime_pay)
            details["加班明细"] = f"{record.overtimeHours}h × (¥{dailySalary}/8) × {self.rules.overtimePayRate}"
            total -= overtime_pay
        
        # 确保扣减不为负（加班费不应导致负扣减）
        total = max(total, Decimal('0'))
        
        record.preTaxDeductions = _round2(total)
        record.deductionDetails = details
        return record
    
    def _calcLateDeduction(self, lateCount: Decimal) -> Decimal:
        """计算迟到扣款"""
        exceed = lateCount - Decimal(str(self.rules.lateFreeQuota))
        if exceed > 0:
            return _round2(exceed * self.rules.lateDeductionPerTime)
        return Decimal('0')
    
    def _calcEarlyLeaveDeduction(self, earlyCount: Decimal) -> Decimal:
        """计算早退扣款"""
        exceed = earlyCount - Decimal(str(self.rules.earlyLeaveFreeQuota))
        if exceed > 0:
            return _round2(exceed * self.rules.earlyLeaveDeductionPerTime)
        return Decimal('0')
    
    def getRecord(self, empNo: str, year: int, month: int) -> Optional[AttendanceRecord]:
        """获取指定员工的考勤记录"""
        key = f"{empNo}-{year}-{month:02d}"
        return self.records.get(key)
    
    def getMonthlyRecords(self, year: int, month: int) -> List[AttendanceRecord]:
        """获取指定月份所有考勤记录"""
        results = []
        for key, record in self.records.items():
            parts = key.rsplit('-', 2)
            try:
                rec_year, rec_month = int(parts[1]), int(parts[2])
            except (ValueError, IndexError):
                continue
            if rec_year == year and rec_month == month:
                results.append(record)
        return results
    
    def getEmployeeRecords(self, empNo: str) -> List[AttendanceRecord]:
        """获取指定员工所有考勤记录"""
        results = []
        for key, record in self.records.items():
            if key.startswith(f"{empNo}-"):
                results.append(record)
        return sorted(results, key=lambda r: (r.year, r.month))
    
    def getDeductionSummary(self, year: int, month: int) -> Dict[str, Any]:
        """
        获取指定月份的考勤扣减汇总
        
        Returns:
            {totalCount, totalDeductions, details...}
        """
        records = self.getMonthlyRecords(year, month)
        
        total_ded = Decimal('0')
        late_count = Decimal('0')
        early_count = Decimal('0')
        personal_days = Decimal('0')
        sick_days = Decimal('0')
        absent_days = Decimal('0')
        overtime_hours = Decimal('0')
        
        for r in records:
            total_ded += r.preTaxDeductions
            late_count += r.lateCount
            early_count += r.earlyLeaveCount
            personal_days += r.personalLeaveDays
            sick_days += r.sickLeaveDays
            absent_days += r.absentDays
            overtime_hours += r.overtimeHours
        
        return {
            "year": year,
            "month": month,
            "recordCount": len(records),
            "totalDeductions": float(total_ded),
            "summary": {
                "总迟到次数": int(late_count),
                "总早退次数": int(early_count),
                "总事假天数": float(personal_days),
                "总病假天数": float(sick_days),
                "总旷工天数": float(absent_days),
                "总加班小时": float(overtime_hours),
            }
        }
    
    def getPreTaxDeductions(self, empNo: str, year: int, month: int) -> Decimal:
        """
        获取指定员工的考勤扣减总额（供薪资计算调用）
        
        Args:
            empNo: 工号
            year: 年份
            month: 月份
        
        Returns:
            考勤扣减总额（Decimal），未找到返回 0
        """
        record = self.getRecord(empNo, year, month)
        if record:
            return record.preTaxDeductions
        return Decimal('0')
    
    def getAllPreTaxDeductions(self, year: int, month: int,
                                dailySalaries: Dict[str, Decimal]) -> Dict[str, Decimal]:
        """
        批量获取指定月份所有员工的考勤扣减总额
        
        Args:
            year: 年份
            month: 月份
            dailySalaries: {empNo: dailySalary}
        
        Returns:
            {empNo: preTaxDeductions}
        """
        batch = self.batchCalculateDeductions(year, month, dailySalaries)
        return {emp_no: rec.preTaxDeductions for emp_no, rec in batch.items()}
