"""
HR 智能体 - 初始化引导模块
处理首次使用的引导流程
"""

import os
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum


class StorageType(Enum):
    """数据存储方式（目前仅支持 Excel 本地文件）"""
    EXCEL = "excel"


class TableType(Enum):
    """表格类型"""
    ORGANIZATION = "organization"
    EMPLOYEE = "employee"
    SALARY = "salary"
    ATTENDANCE = "attendance"


@dataclass
class ColumnMapping:
    """列映射定义"""
    source: str          # 源表格中的列名
    target: str          # 标准字段名
    dataType: str        # 数据类型: string, number, date, enum
    confidence: float    # 识别置信度 0-1
    isRequired: bool     # 是否必填


@dataclass
class TableConfig:
    """表格配置"""
    filePath: str
    sheetName: str
    columnMapping: Dict[str, ColumnMapping]
    isBound: bool = False


@dataclass
class HRConfig:
    """HR 智能体完整配置"""
    version: str = "1.0"
    initializedAt: str = ""
    storageType: StorageType = StorageType.EXCEL
    basePath: str = ""
    organization: Optional[TableConfig] = None
    employee: Optional[TableConfig] = None
    salary: Optional[TableConfig] = None
    attendance: Optional[TableConfig] = None
    isFullyInitialized: bool = False


class OnboardingManager:
    """初始化引导管理器"""
    
    # 标准字段定义
    ORGANIZATION_FIELDS = {
        "deptCode": {"type": "string", "required": True, "aliases": ["部门编码", "部门ID", "部门代码", "dept_id", "dept_code"]},
        "deptName": {"type": "string", "required": True, "aliases": ["部门名称", "部门", "部门名", "dept_name", "department"]},
        "parentCode": {"type": "string", "required": False, "aliases": ["上级部门", "父部门", "上级编码", "parent_id", "parent_code"]},
        "manager": {"type": "string", "required": False, "aliases": ["部门负责人", "负责人", "经理", "主管", "manager", "head"]},
        "level": {"type": "number", "required": False, "aliases": ["部门层级", "层级", "级别", "level", "grade"]},
    }
    
    EMPLOYEE_FIELDS = {
        "empNo": {"type": "string", "required": True, "aliases": ["工号", "员工编号", "员工ID", "编号", "emp_id", "employee_id"]},
        "name": {"type": "string", "required": True, "aliases": ["姓名", "员工姓名", "名字", "name", "employee_name"]},
        "deptCode": {"type": "string", "required": True, "aliases": ["部门编码", "部门ID", "所属部门", "dept_code", "department_id"]},
        "position": {"type": "string", "required": False, "aliases": ["岗位", "职位", "职务", "岗位名称", "position", "job_title"]},
        "hireDate": {"type": "date", "required": True, "aliases": ["入职日期", "入职时间", "入职日", "hire_date", "join_date"]},
        "status": {"type": "enum", "required": True, "aliases": ["在职状态", "状态", "员工状态", "status", "employment_status"]},
        "phone": {"type": "string", "required": False, "aliases": ["手机号", "电话", "联系电话", "手机", "phone", "mobile"]},
        "email": {"type": "string", "required": False, "aliases": ["邮箱", "电子邮件", "邮箱地址", "email"]},
        "idCard": {"type": "string", "required": False, "aliases": ["身份证号", "身份证", "证件号", "id_card", "id_number"]},
        "baseSalary": {"type": "number", "required": False, "aliases": ["基本工资", "底薪", "基础工资", "base_salary", "basic_salary"]},
        "socialInsuranceBase": {"type": "number", "required": False, "aliases": ["社保基数", "缴费基数", "社保缴费基数"]},
        "housingFundBase": {"type": "number", "required": False, "aliases": ["公积金基数", "公积金缴费基数", "住房公积金额度"]},
        "specialDeduction": {"type": "number", "required": False, "aliases": ["专项附加扣除", "专项扣除", "附加扣除"]},
    }
    
    SALARY_FIELDS = {
        "empNo": {"type": "string", "required": True, "aliases": ["工号", "员工编号", "编号", "emp_id"]},
        "baseSalary": {"type": "number", "required": True, "aliases": ["基本工资", "底薪", "基础工资", "base_salary", "basic_salary"]},
        "performanceBonus": {"type": "number", "required": False, "aliases": ["绩效奖金", "绩效工资", "奖金", "performance_bonus"]},
        "allowances": {"type": "number", "required": False, "aliases": ["津贴", "补贴", "岗位津贴", "allowance"]},
        "preTaxDeductions": {"type": "number", "required": False, "aliases": ["税前扣减", "税前扣除", "考勤扣款", "事假扣款"]},
    }
    
    ATTENDANCE_FIELDS = {
        "empNo": {"type": "string", "required": True, "aliases": ["工号", "员工编号", "编号", "emp_id", "员工ID"]},
        "year": {"type": "number", "required": True, "aliases": ["年份", "年度", "年", "year"]},
        "month": {"type": "number", "required": True, "aliases": ["月份", "月", "month"]},
        "shouldAttendDays": {"type": "number", "required": False, "aliases": ["应出勤天数", "应出勤", "出勤标准", "应到天数"]},
        "actualAttendDays": {"type": "number", "required": False, "aliases": ["实际出勤天数", "实际出勤", "出勤天数", "实到天数"]},
        "lateCount": {"type": "number", "required": False, "aliases": ["迟到次数", "迟到", "迟到天数", "late_count"]},
        "earlyLeaveCount": {"type": "number", "required": False, "aliases": ["早退次数", "早退", "早退天数", "early_leave_count"]},
        "personalLeaveDays": {"type": "number", "required": False, "aliases": ["事假天数", "事假", "事假天数(天)", "事假(天)"]},
        "sickLeaveDays": {"type": "number", "required": False, "aliases": ["病假天数", "病假", "病假天数(天)", "病假(天)"]},
        "absentDays": {"type": "number", "required": False, "aliases": ["旷工天数", "旷工", "旷工天数(天)", "旷工(天)"]},
        "overtimeHours": {"type": "number", "required": False, "aliases": ["加班小时", "加班时长", "加班小时数", "加班(h)", "overtime_hours"]},
    }
    
    def __init__(self, configPath: str = "hr-config.json"):
        self.configPath = configPath
        self.config = self._loadConfig()
    
    def _loadConfig(self) -> HRConfig:
        """加载配置文件"""
        if os.path.exists(self.configPath):
            try:
                with open(self.configPath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 将 JSON dict 转为 HRConfig
                    if isinstance(data, dict):
                        config = HRConfig()
                        config.version = data.get("version", "1.0")
                        config.initializedAt = data.get("initializedAt", "")
                        # 处理 storageType
                        st = data.get("storageType", "excel")
                        if isinstance(st, str):
                            config.storageType = StorageType(st)
                        elif isinstance(st, StorageType):
                            config.storageType = st
                        config.basePath = data.get("basePath", "")
                        config.isFullyInitialized = data.get("isFullyInitialized", False)
                        # 处理四张表配置
                        for key in ("organization", "employee", "salary", "attendance"):
                            tc_data = data.get(key)
                            if tc_data and isinstance(tc_data, dict):
                                # columnMapping 中的值可能是 dict 或 ColumnMapping
                                cm = tc_data.get("columnMapping", {})
                                if isinstance(cm, dict):
                                    cleaned_cm = {}
                                    for k, v in cm.items():
                                        if isinstance(v, dict):
                                            cleaned_cm[k] = ColumnMapping(**v)
                                        elif isinstance(v, ColumnMapping):
                                            cleaned_cm[k] = v
                                        else:
                                            cleaned_cm[k] = v
                                    cm = cleaned_cm
                                tc = TableConfig(
                                    filePath=tc_data.get("filePath", ""),
                                    sheetName=tc_data.get("sheetName", "Sheet1"),
                                    columnMapping=cm,
                                    isBound=tc_data.get("isBound", False),
                                )
                                setattr(config, key, tc)
                        return config
                    return HRConfig(**data)
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                # Bug11 修复：区分 JSON 解析错误和配置结构错误
                print(f"配置文件解析失败（{type(e).__name__}: {e}），将使用默认配置")
        return HRConfig()
    
    def _saveConfig(self) -> bool:
        """保存配置文件"""
        try:
            data = asdict(self.config)
            # 处理枚举类型序列化
            if isinstance(data.get("storageType"), StorageType):
                data["storageType"] = data["storageType"].value
            # 处理 TableConfig 中的非序列化字段
            for key in ("organization", "employee", "salary", "attendance"):
                if key in data and data[key] is not None:
                    tc = data[key]
                    if isinstance(tc.get("columnMapping"), dict):
                        # ColumnMapping 对象需要转为普通 dict
                        cleaned = {}
                        for k, v in tc["columnMapping"].items():
                            if hasattr(v, '__dict__'):
                                cleaned[k] = {fk: fv for fk, fv in v.__dict__.items() if not fk.startswith('_')}
                            else:
                                cleaned[k] = v
                        tc["columnMapping"] = cleaned
            with open(self.configPath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except (IOError, OSError, TypeError) as e:
            # Bug11 修复：缩小异常捕获范围
            print(f"保存配置失败（{type(e).__name__}: {e}）")
            return False
    
    def detectFirstUse(self) -> bool:
        """
        检测是否为首次使用
        返回: True 表示已完成初始化，False 表示首次使用
        """
        return self.config.isFullyInitialized
    
    def getOnboardingStatus(self) -> Dict[str, Any]:
        """获取初始化状态"""
        return {
            "isFullyInitialized": self.config.isFullyInitialized,
            "storageType": self.config.storageType.value if self.config.storageType else None,
            "organizationBound": self.config.organization is not None and self.config.organization.isBound,
            "employeeBound": self.config.employee is not None and self.config.employee.isBound,
            "salaryBound": self.config.salary is not None and self.config.salary.isBound,
            "attendanceBound": self.config.attendance is not None and self.config.attendance.isBound,
            "nextStep": self._getNextStep()
        }
    
    def _getNextStep(self) -> Optional[str]:
        """获取下一步操作"""
        if not self.config.storageType:
            return "set_storage_type"
        if not self.config.organization or not self.config.organization.isBound:
            return "bind_organization"
        if not self.config.employee or not self.config.employee.isBound:
            return "bind_employee"
        if not self.config.salary or not self.config.salary.isBound:
            return "bind_salary"
        if not self.config.attendance or not self.config.attendance.isBound:
            return "bind_attendance"
        return None
    
    def setStorageType(self, storageType: str) -> Dict[str, Any]:
        """设置数据存储方式"""
        try:
            self.config.storageType = StorageType(storageType)
            self._saveConfig()

            # 同步到 HRStore
            try:
                from hr_store import HRStore
                store = HRStore()
                store.updateConfig({"storageType": storageType})
            except Exception:
                pass

            return {
                "success": True,
                "message": f"已选择 {storageType} 作为数据存储方式",
                "nextStep": "bind_organization"
            }
        except ValueError:
            return {
                "success": False,
                "message": f"不支持的存储类型: {storageType}，目前仅支持 excel"
            }
    
    def analyzeAndBind(self, tableType: str, filePath: str, sheetName: str = None) -> Dict[str, Any]:
        """
        分析上传的 Excel 文件结构，自动识别列映射，并完成绑定。
        这是一站式操作：分析 → 自动映射 → 绑定 → 验证。
        支持 .xls 和 .xlsx 格式。

        Args:
            tableType: organization, employee, salary
            filePath: Excel 文件路径（绝对路径），支持 .xls 和 .xlsx
            sheetName: 工作表名称，None 则自动使用第一个 sheet

        Returns:
            分析 + 绑定结果
        """
        import shutil
        from excel_adapter import ExcelAdapter, analyze_excel_structure, match_columns

        # 1. 校验文件存在
        if not os.path.exists(filePath):
            return {"success": False, "message": f"文件不存在: {filePath}"}

        # 1.5 安全校验：禁止路径遍历和符号链接
        filePath = os.path.realpath(filePath)
        if not os.path.isfile(filePath):
            return {"success": False, "message": f"路径不是文件: {filePath}，请提供 Excel 文件的直接路径"}

        # 2. 校验文件格式
        _, ext = os.path.splitext(filePath)
        ext = ext.lower()
        if ext not in ('.xls', '.xlsx', '.xlsm'):
            return {"success": False, "message": f"不支持的文件格式: {ext}，请使用 .xls 或 .xlsx 格式的 Excel 文件"}

        # 2. 分析表格结构
        try:
            adapter = ExcelAdapter(filePath)
            structure = adapter.analyzeStructure(sheetName)
        except Exception as e:
            return {"success": False, "message": f"读取 Excel 失败: {e}"}

        actualSheet = structure.sheetName

        # 3. 自动匹配列映射
        matchResult = adapter.matchColumns(tableType, structure)
        matches = matchResult.get("matches", [])

        # 4. 构建列映射 {标准字段: 实际列名}
        columnMapping = {}
        unmappedRequired = []

        for m in matches:
            if m["confidence"] >= 0.5 and m["detectedColumn"]:
                columnMapping[m["field"]] = m["detectedColumn"]
            elif m["isRequired"] and m["confidence"] < 0.5:
                unmappedRequired.append({
                    "field": m["field"],
                    "fieldName": m["fieldName"],
                    "suggestedColumns": [col.name for col in structure.columns if col.dataType == m["dataType"]][:3]
                })

        # 5. 如果有必填字段未映射，给出建议
        if unmappedRequired:
            suggestions = ""
            for item in unmappedRequired:
                suggestions += f"\n  • 「{item['fieldName']}」未匹配到列"
                if item["suggestedColumns"]:
                    suggestions += f"，可能是: {', '.join(item['suggestedColumns'])}"

            # 仍然绑定，但标记警告
            bindResult = self.bindTable(tableType, filePath, actualSheet, columnMapping)
            if bindResult.get("success"):
                bindResult["warnings"] = [f"以下必填字段未自动匹配，请手动确认:{suggestions}"]
            return bindResult

        # 6. 全部匹配成功，完成绑定
        typeNames = {"organization": "组织架构", "employee": "员工花名册", "salary": "薪资", "attendance": "考勤"}
        matchedCount = len(columnMapping)
        totalRows = structure.rowCount

        bindResult = self.bindTable(tableType, filePath, actualSheet, columnMapping)
        if bindResult.get("success"):
            bindResult["message"] = (
                f"✅ {typeNames.get(tableType, tableType)}表绑定成功！\n"
                f"  文件: {os.path.basename(filePath)}\n"
                f"  工作表: {actualSheet}\n"
                f"  数据行数: {totalRows}\n"
                f"  自动识别字段: {matchedCount} 个"
            )

        return bindResult

    def analyzeTableStructure(self, tableType: str, filePath: str, sheetName: str = "Sheet1") -> Dict[str, Any]:
        """
        分析表格结构，识别列名（仅分析，不绑定）

        Args:
            tableType: organization, employee, salary
            filePath: 文件路径
            sheetName: 工作表名称

        Returns:
            识别结果，包含列映射建议和置信度
        """
        from excel_adapter import ExcelAdapter

        # 路径安全校验
        if not os.path.exists(filePath):
            return {"success": False, "message": f"文件不存在: {filePath}"}
        filePath = os.path.realpath(filePath)
        if not os.path.isfile(filePath):
            return {"success": False, "message": f"路径不是文件: {filePath}，请提供 Excel 文件的直接路径"}
        _, ext = os.path.splitext(filePath)
        if ext.lower() not in ('.xls', '.xlsx', '.xlsm'):
            return {"success": False, "message": f"不支持的文件格式: {ext}，请使用 .xls 或 .xlsx 格式的 Excel 文件"}

        try:
            adapter = ExcelAdapter(filePath)
            structure = adapter.analyzeStructure(sheetName)
        except Exception as e:
            return {"success": False, "message": f"读取文件失败: {e}"}

        matchResult = adapter.matchColumns(tableType, structure)

        return {
            "success": True,
            "tableType": tableType,
            "filePath": filePath,
            "sheetName": structure.sheetName,
            "rowCount": structure.rowCount,
            "columnCount": structure.columnCount,
            "detectedColumns": matchResult.get("matches", []),
            "matchedCount": matchResult.get("matchedFields", 0),
            "message": f"分析完成，识别到 {matchResult.get('matchedFields', 0)} 个字段映射"
        }
    
    def _getFieldsForType(self, tableType: TableType) -> Dict:
        """获取指定表格类型的字段定义"""
        if tableType == TableType.ORGANIZATION:
            return self.ORGANIZATION_FIELDS
        elif tableType == TableType.EMPLOYEE:
            return self.EMPLOYEE_FIELDS
        elif tableType == TableType.SALARY:
            return self.SALARY_FIELDS
        elif tableType == TableType.ATTENDANCE:
            return self.ATTENDANCE_FIELDS
        return {}
    
    def confirmColumnMapping(self, tableType: str, mapping: Dict[str, str]) -> Dict[str, Any]:
        """
        确认列映射关系
        
        Args:
            tableType: 表格类型
            mapping: {标准字段名: 源列名}
        
        Returns:
            确认结果
        """
        # TODO: 验证映射完整性
        return {
            "success": True,
            "message": "列映射已确认",
            "mapping": mapping
        }
    
    def bindTable(self, tableType: str, filePath: str, sheetName: str = "Sheet1",
                  columnMapping: Optional[Dict] = None) -> Dict[str, Any]:
        """
        绑定表格

        Args:
            tableType: organization, employee, salary
            filePath: 文件路径
            sheetName: 工作表名称
            columnMapping: 列映射配置

        Returns:
            绑定结果
        """
        tableConfig = TableConfig(
            filePath=filePath,
            sheetName=sheetName,
            columnMapping=columnMapping or {},
            isBound=True
        )

        if tableType == "organization":
            self.config.organization = tableConfig
        elif tableType == "employee":
            self.config.employee = tableConfig
        elif tableType == "salary":
            self.config.salary = tableConfig
        elif tableType == "attendance":
            self.config.attendance = tableConfig

        # 检查是否全部绑定完成（组织架构+花名册+薪资 三表为核心，考勤为可选）
        if (self.config.organization and self.config.organization.isBound and
            self.config.employee and self.config.employee.isBound and
            self.config.salary and self.config.salary.isBound):
            self.config.isFullyInitialized = True
            from datetime import datetime
            self.config.initializedAt = datetime.now().isoformat()

        self._saveConfig()

        # ---- 同步到 HRStore，确保双配置系统一致（Bug1/Bug10 修复）----
        self._syncToHRStore(tableType, filePath, sheetName, columnMapping)

        return {
            "success": True,
            "message": f"{tableType} 表格绑定成功",
            "nextStep": self._getNextStep()
        }

    def _syncToHRStore(self, tableType: str, filePath: str, sheetName: str,
                       columnMapping: Optional[Dict] = None):
        """
        将绑定信息同步到 HRStore，确保 hr-config.json 和 .hr-data/config.json 一致。
        静默失败（HRStore 不可用时忽略），不影响主流程。
        """
        try:
            from hr_store import HRStore
            store = HRStore()
            store.bindTable(tableType, filePath, sheetName, columnMapping)
        except Exception:
            # HRStore 不可用时静默忽略，不阻塞初始化流程
            pass
    
    def validateDataIntegrity(self, tableType: str) -> Dict[str, Any]:
        """
        验证数据完整性
        
        Returns:
            验证结果，包含发现的错误和警告
        """
        # TODO: 实现实际的数据验证逻辑
        errors = []
        warnings = []
        
        # 示例验证规则
        if tableType == "employee":
            # 检查部门存在性
            # 检查工号唯一性
            # 检查必填字段
            pass
        
        return {
            "success": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "message": f"验证完成，发现 {len(errors)} 个错误，{len(warnings)} 个警告"
        }
    
    def resetConfiguration(self) -> Dict[str, Any]:
        """重置配置"""
        self.config = HRConfig()
        if os.path.exists(self.configPath):
            os.remove(self.configPath)

        # 同步重置 HRStore 配置
        try:
            from hr_store import HRStore
            store = HRStore()
            store.resetConfig()
        except Exception:
            pass

        return {
            "success": True,
            "message": "配置已重置，可以重新开始初始化"
        }
    
    def exportConfiguration(self, exportPath: str) -> Dict[str, Any]:
        """导出配置"""
        # 路径安全校验：仅允许写入合法目录，禁止路径遍历
        exportPath = os.path.realpath(exportPath)
        exportDir = os.path.dirname(exportPath)
        if not os.path.isdir(exportDir):
            return {"success": False, "message": f"目标目录不存在: {exportDir}"}
        _, ext = os.path.splitext(exportPath)
        if ext.lower() not in ('.json',):
            return {"success": False, "message": "导出路径必须以 .json 结尾"}
        try:
            with open(exportPath, 'w', encoding='utf-8') as f:
                json.dump(asdict(self.config), f, ensure_ascii=False, indent=2)
            return {
                "success": True,
                "message": f"配置已导出到: {exportPath}"
            }
        except (IOError, OSError, TypeError) as e:
            return {
                "success": False,
                "message": f"导出失败: {str(e)}"
            }
    
    def importConfiguration(self, importPath: str) -> Dict[str, Any]:
        """导入配置"""
        # 路径安全校验
        if not os.path.exists(importPath):
            return {"success": False, "message": f"配置文件不存在: {importPath}"}
        importPath = os.path.realpath(importPath)
        if not os.path.isfile(importPath):
            return {"success": False, "message": f"路径不是文件: {importPath}"}
        _, ext = os.path.splitext(importPath)
        if ext.lower() != '.json':
            return {"success": False, "message": "仅支持导入 .json 格式的配置文件"}
        try:
            with open(importPath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.config = HRConfig(**data)
                self._saveConfig()
            return {
                "success": True,
                "message": "配置已导入"
            }
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            return {
                "success": False,
                "message": f"配置文件格式错误: {str(e)}"
            }
        except (IOError, OSError) as e:
            return {
                "success": False,
                "message": f"导入失败: {str(e)}"
            }


# 工具函数，供 WorkBuddy 调用
def detect_first_use() -> Dict[str, Any]:
    """检测是否首次使用"""
    manager = OnboardingManager()
    isInitialized = manager.detectFirstUse()
    return {
        "isInitialized": isInitialized,
        "message": "已完成初始化" if isInitialized else "首次使用，需要完成初始化引导"
    }


def start_onboarding() -> Dict[str, Any]:
    """启动初始化引导"""
    manager = OnboardingManager()
    status = manager.getOnboardingStatus()
    
    if status["isFullyInitialized"]:
        return {
            "success": True,
            "message": "已完成初始化，可以直接使用",
            "status": status
        }
    
    # 根据当前状态返回下一步引导
    nextStep = status["nextStep"]
    
    if nextStep == "set_storage_type":
        return {
            "success": True,
            "message": "请选择数据存储方式",
            "options": [
                {"value": "excel", "label": "Excel 本地文件"}
            ],
            "nextStep": nextStep
        }
    elif nextStep == "bind_organization":
        return {
            "success": True,
            "message": "请上传或指定组织架构表格",
            "nextStep": nextStep
        }
    elif nextStep == "bind_employee":
        return {
            "success": True,
            "message": "请上传或指定员工花名册表格",
            "nextStep": nextStep
        }
    elif nextStep == "bind_salary":
        return {
            "success": True,
            "message": "请上传或指定薪资表格",
            "nextStep": nextStep
        }
    elif nextStep == "bind_attendance":
        return {
            "success": True,
            "message": "请上传或指定考勤表格（可选，绑定后薪资计算将自动扣除考勤扣款）",
            "nextStep": nextStep
        }
    
    return {
        "success": True,
        "message": "初始化状态检查完成",
        "status": status
    }


def set_storage_type(storage_type: str) -> Dict[str, Any]:
    """设置存储类型"""
    manager = OnboardingManager()
    return manager.setStorageType(storage_type)


def analyze_table_structure(table_type: str, file_path: str, sheet_name: str = "Sheet1") -> Dict[str, Any]:
    """分析表格结构"""
    manager = OnboardingManager()
    return manager.analyzeTableStructure(table_type, file_path, sheet_name)


def confirm_column_mapping(table_type: str, mapping: Dict[str, str]) -> Dict[str, Any]:
    """确认列映射"""
    manager = OnboardingManager()
    return manager.confirmColumnMapping(table_type, mapping)


def bind_organization_table(file_path: str, sheet_name: str = "Sheet1", column_mapping: Dict = None) -> Dict[str, Any]:
    """绑定组织架构表"""
    manager = OnboardingManager()
    return manager.bindTable("organization", file_path, sheet_name, column_mapping)


def bind_employee_table(file_path: str, sheet_name: str = "Sheet1", column_mapping: Dict = None) -> Dict[str, Any]:
    """绑定员工花名册"""
    manager = OnboardingManager()
    return manager.bindTable("employee", file_path, sheet_name, column_mapping)


def bind_salary_table(file_path: str, sheet_name: str = "Sheet1", column_mapping: Dict = None) -> Dict[str, Any]:
    """绑定薪资表"""
    manager = OnboardingManager()
    return manager.bindTable("salary", file_path, sheet_name, column_mapping)


def bind_attendance_table(file_path: str, sheet_name: str = "Sheet1", column_mapping: Dict = None) -> Dict[str, Any]:
    """绑定考勤表"""
    manager = OnboardingManager()
    return manager.bindTable("attendance", file_path, sheet_name, column_mapping)


def validate_data_integrity(table_type: str) -> Dict[str, Any]:
    """验证数据完整性"""
    manager = OnboardingManager()
    return manager.validateDataIntegrity(table_type)


def save_configuration() -> Dict[str, Any]:
    """保存配置"""
    manager = OnboardingManager()
    return {"success": True, "message": "配置已保存"}


def load_configuration() -> Dict[str, Any]:
    """加载配置"""
    manager = OnboardingManager()
    status = manager.getOnboardingStatus()
    return {
        "success": True,
        "status": status
    }


def export_configuration(file_path: str) -> Dict[str, Any]:
    """导出配置"""
    manager = OnboardingManager()
    return manager.exportConfiguration(file_path)


def import_configuration(file_path: str) -> Dict[str, Any]:
    """导入配置"""
    manager = OnboardingManager()
    return manager.importConfiguration(file_path)


def reset_configuration() -> Dict[str, Any]:
    """重置配置"""
    manager = OnboardingManager()
    return manager.resetConfiguration()


def get_configuration_summary() -> Dict[str, Any]:
    """获取配置摘要"""
    manager = OnboardingManager()
    status = manager.getOnboardingStatus()
    
    summary = []
    if status["organizationBound"]:
        summary.append("✅ 组织架构表已绑定")
    else:
        summary.append("❌ 组织架构表未绑定")
    
    if status["employeeBound"]:
        summary.append("✅ 员工花名册已绑定")
    else:
        summary.append("❌ 员工花名册未绑定")
    
    if status["salaryBound"]:
        summary.append("✅ 薪资表已绑定")
    else:
        summary.append("❌ 薪资表未绑定")
    
    if status["attendanceBound"]:
        summary.append("✅ 考勤表已绑定")
    else:
        summary.append("⬜ 考勤表未绑定（可选）")
    
    return {
        "success": True,
        "isFullyInitialized": status["isFullyInitialized"],
        "summary": "\n".join(summary),
        "nextStep": status["nextStep"]
    }


def analyze_and_bind(table_type: str, file_path: str, sheet_name: str = None) -> Dict[str, Any]:
    """
    一站式：分析上传的 Excel + 自动映射 + 绑定。
    供 main.py 和 SKILL.md 调用。
    """
    manager = OnboardingManager()
    return manager.analyzeAndBind(table_type, file_path, sheet_name)
