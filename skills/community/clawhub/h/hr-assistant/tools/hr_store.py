"""
HR 智能体 - 统一数据持久化层

基于 JSON 的本地存储，包含：
  1. 配置管理（初始化状态、表格绑定、列映射）
  2. 操作审计日志（JSONL 格式，append-only）
  3. 薪资历史（按月归档）
  4. 对话历史

存储目录结构：
  <dataDir>/
    config.json        # 全局配置
    audit.log.jsonl    # 操作审计日志
    payroll/
      2026-04.json     # 月度薪资计算结果
      2026-05.json
    conversations/
      <sessionId>.json # 对话历史
"""

import os
import json
import uuid
import shutil
from typing import Dict, List, Optional, Any
from datetime import datetime, date
from pathlib import Path


class HRStore:
    """
    HR 智能体统一数据持久化层
    
    所有数据存储在用户本地，不上云。
    使用纯 JSON 格式，无需数据库依赖。
    """
    
    def __init__(self, dataDir: Optional[str] = None):
        """
        初始化存储
        
        Args:
            dataDir: 数据目录路径，默认为当前目录下的 .hr-data/
        """
        self.dataDir = dataDir or os.path.join(os.getcwd(), ".hr-data")
        self._configCache: Optional[Dict] = None
        self._ensureDirectories()
    
    def _ensureDirectories(self):
        """确保存储目录存在"""
        os.makedirs(self.dataDir, exist_ok=True)
        os.makedirs(os.path.join(self.dataDir, "payroll"), exist_ok=True)
        os.makedirs(os.path.join(self.dataDir, "conversations"), exist_ok=True)
    
    # ================================================================
    # 配置管理
    # ================================================================
    
    @property
    def configPath(self) -> str:
        return os.path.join(self.dataDir, "config.json")
    
    def loadConfig(self) -> Dict:
        """
        加载全局配置
        
        Returns:
            配置字典，包含：
            - version: 版本号
            - storageType: 存储类型 (excel)
            - isFullyInitialized: 是否完成初始化
            - initializedAt: 初始化完成时间
            - tables: {organization: {...}, employee: {...}, salary: {...}}
            - columnMappings: {employee: {...}, organization: {...}}
        """
        if self._configCache is not None:
            return self._configCache
        
        if os.path.exists(self.configPath):
            try:
                with open(self.configPath, 'r', encoding='utf-8') as f:
                    self._configCache = json.load(f)
                    return self._configCache
            except json.JSONDecodeError:
                # Bug8 修复：JSON 损坏时先备份再重建，避免静默丢失配置
                backupPath = self.configPath + ".corrupted.bak"
                try:
                    shutil.copy2(self.configPath, backupPath)
                    print(f"[HRStore] 配置文件损坏，已备份到: {backupPath}")
                except IOError:
                    print(f"[HRStore] 配置文件损坏且备份失败: {self.configPath}")
                pass
            except IOError:
                pass
        
        # 默认配置
        default = {
            "version": "1.0",
            "storageType": "",
            "isFullyInitialized": False,
            "initializedAt": "",
            "tables": {
                "organization": {"filePath": "", "sheetName": "", "isBound": False},
                "employee": {"filePath": "", "sheetName": "", "isBound": False},
                "salary": {"filePath": "", "sheetName": "", "isBound": False},
                "attendance": {"filePath": "", "sheetName": "", "isBound": False},
            },
            "columnMappings": {
                "employee": {},
                "organization": {},
                "salary": {},
                "attendance": {},
            },
        }
        self._configCache = default
        return default
    
    def saveConfig(self, config: Optional[Dict] = None) -> bool:
        """
        保存全局配置
        
        Args:
            config: 配置字典，None 则保存当前缓存
        
        Returns:
            是否成功
        """
        data = config if config is not None else self._configCache
        if data is None:
            data = self.loadConfig()
        
        try:
            with open(self.configPath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self._configCache = data
            return True
        except IOError as e:
            print(f"保存配置失败: {e}")
            return False
    
    def getConfigValue(self, key: str, default: Any = None) -> Any:
        """获取配置项"""
        config = self.loadConfig()
        # 支持点号路径，如 "tables.employee.filePath"
        keys = key.split(".")
        value = config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            if value is None:
                return default
        return value
    
    def updateConfig(self, updates: Dict) -> bool:
        """
        更新配置项（合并方式）
        
        Args:
            updates: 要更新的配置项（支持嵌套字典合并）
        
        Returns:
            是否成功
        """
        config = self.loadConfig()
        self._deepMerge(config, updates)
        return self.saveConfig(config)
    
    @staticmethod
    def _deepMerge(base: Dict, override: Dict):
        """深度合并字典"""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                HRStore._deepMerge(base[key], value)
            else:
                base[key] = value
    
    def isInitialized(self) -> bool:
        """是否已完成初始化"""
        config = self.loadConfig()
        return config.get("isFullyInitialized", False)
    
    def getTableConfig(self, tableType: str) -> Dict:
        """
        获取表格绑定配置
        
        Args:
            tableType: organization / employee / salary
        """
        config = self.loadConfig()
        tables = config.get("tables", {})
        return tables.get(tableType, {"filePath": "", "sheetName": "", "isBound": False})
    
    def bindTable(self, tableType: str, filePath: str, sheetName: str = "",
                  columnMapping: Optional[Dict] = None) -> bool:
        """
        绑定表格
        
        Args:
            tableType: organization / employee / salary
            filePath: 文件路径
            sheetName: 工作表名称
            columnMapping: 列映射配置
        """
        config = self.loadConfig()
        
        tables = config.setdefault("tables", {})
        tables[tableType] = {
            "filePath": filePath,
            "sheetName": sheetName,
            "isBound": True,
            "boundAt": datetime.now().isoformat(),
        }
        
        # 保存列映射
        if columnMapping:
            mappings = config.setdefault("columnMappings", {})
            mappings[tableType] = columnMapping
        
        # 检查是否全部绑定完成（组织架构+花名册+薪资 三表为核心，考勤为可选）
        all_bound = all(
            tables.get(t, {}).get("isBound", False)
            for t in ("organization", "employee", "salary")
        )
        
        if all_bound and not config.get("isFullyInitialized"):
            config["isFullyInitialized"] = True
            config["initializedAt"] = datetime.now().isoformat()
        
        return self.saveConfig(config)
    
    def getNextBindingStep(self) -> Optional[str]:
        """
        获取下一个需要绑定的表格类型
        
        Returns:
            organization / employee / salary / None(全部完成)
        """
        config = self.loadConfig()
        
        if not config.get("storageType"):
            return "storage_type"
        
        tables = config.get("tables", {})
        for tableType in ("organization", "employee", "salary", "attendance"):
            if not tables.get(tableType, {}).get("isBound", False):
                return tableType
        
        return None
    
    def getOnboardingStatus(self) -> Dict:
        """获取初始化状态摘要"""
        config = self.loadConfig()
        tables = config.get("tables", {})
        
        return {
            "isFullyInitialized": config.get("isFullyInitialized", False),
            "storageType": config.get("storageType", ""),
            "initializedAt": config.get("initializedAt", ""),
            "organization": {
                "isBound": tables.get("organization", {}).get("isBound", False),
                "filePath": tables.get("organization", {}).get("filePath", ""),
                "boundAt": tables.get("organization", {}).get("boundAt", ""),
            },
            "employee": {
                "isBound": tables.get("employee", {}).get("isBound", False),
                "filePath": tables.get("employee", {}).get("filePath", ""),
                "boundAt": tables.get("employee", {}).get("boundAt", ""),
            },
            "salary": {
                "isBound": tables.get("salary", {}).get("isBound", False),
                "filePath": tables.get("salary", {}).get("filePath", ""),
                "boundAt": tables.get("salary", {}).get("boundAt", ""),
            },
            "attendance": {
                "isBound": tables.get("attendance", {}).get("isBound", False),
                "filePath": tables.get("attendance", {}).get("filePath", ""),
                "boundAt": tables.get("attendance", {}).get("boundAt", ""),
            },
            "nextStep": self.getNextBindingStep(),
            "columnMappings": config.get("columnMappings", {}),
        }
    
    def resetConfig(self) -> bool:
        """重置配置（保留审计日志和薪资历史）"""
        self._configCache = {
            "version": "1.0",
            "storageType": "",
            "isFullyInitialized": False,
            "initializedAt": "",
            "tables": {
                "organization": {"filePath": "", "sheetName": "", "isBound": False},
                "employee": {"filePath": "", "sheetName": "", "isBound": False},
                "salary": {"filePath": "", "sheetName": "", "isBound": False},
                "attendance": {"filePath": "", "sheetName": "", "isBound": False},
            },
            "columnMappings": {},
        }
        return self.saveConfig(self._configCache)
    
    def exportConfig(self) -> str:
        """导出配置为 JSON 字符串"""
        return json.dumps(self.loadConfig(), ensure_ascii=False, indent=2)
    
    def importConfig(self, jsonStr: str) -> bool:
        """导入配置"""
        try:
            data = json.loads(jsonStr)
            return self.saveConfig(data)
        except (json.JSONDecodeError, TypeError):
            return False
    
    # ================================================================
    # 操作审计日志
    # ================================================================
    
    @property
    def auditLogPath(self) -> str:
        return os.path.join(self.dataDir, "audit.log.jsonl")
    
    def appendAuditLog(self, action: str, targetType: str = "",
                       targetId: str = "", details: Optional[Dict] = None,
                       operator: str = "system") -> str:
        """
        追加审计日志
        
        Args:
            action: 操作类型（add_employee / update_employee / delete_employee / 
                    batch_update / calculate_payroll / bind_table / reset_config 等）
            targetType: 目标类型（employee / department / config）
            targetId: 目标 ID（工号、部门编码等）
            details: 操作详情
            operator: 操作者（默认 system）
        
        Returns:
            日志条目 ID
        """
        entry = {
            "id": uuid.uuid4().hex[:12],
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "targetType": targetType,
            "targetId": targetId,
            "details": details or {},
            "operator": operator,
        }
        
        try:
            with open(self.auditLogPath, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except IOError as e:
            print(f"写入审计日志失败: {e}")
        
        return entry["id"]
    
    def queryAuditLogs(self, action: Optional[str] = None,
                       targetId: Optional[str] = None,
                       startDate: Optional[str] = None,
                       endDate: Optional[str] = None,
                       limit: int = 100) -> List[Dict]:
        """
        查询审计日志
        
        Args:
            action: 按操作类型筛选
            targetId: 按目标 ID 筛选
            startDate: 起始日期 (YYYY-MM-DD)
            endDate: 结束日期 (YYYY-MM-DD)
            limit: 最大返回条数
        
        Returns:
            日志条目列表（倒序，最新在前）
        """
        results = []
        
        if not os.path.exists(self.auditLogPath):
            return results
        
        try:
            with open(self.auditLogPath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    
                    # 筛选
                    if action and entry.get("action") != action:
                        continue
                    if targetId and entry.get("targetId") != targetId:
                        continue
                    if startDate:
                        ts = entry.get("timestamp", "")[:10]
                        if ts < startDate:
                            continue
                    if endDate:
                        ts = entry.get("timestamp", "")[:10]
                        if ts > endDate:
                            continue
                    
                    results.append(entry)
        except IOError:
            pass
        
        # 倒序返回
        results.reverse()
        return results[:limit]
    
    def getAuditStats(self) -> Dict:
        """获取审计统计"""
        logs = self.queryAuditLogs(limit=10000)
        
        action_counts = {}
        daily_counts = {}
        
        for log in logs:
            action = log.get("action", "unknown")
            action_counts[action] = action_counts.get(action, 0) + 1
            
            day = log.get("timestamp", "")[:10]
            if day:
                daily_counts[day] = daily_counts.get(day, 0) + 1
        
        return {
            "totalActions": len(logs),
            "actionCounts": action_counts,
            "recentDaily": dict(sorted(daily_counts.items(), reverse=True)[:30]),
            "lastAction": logs[0] if logs else None,
        }
    
    # ================================================================
    # 薪资历史
    # ================================================================
    
    def _payrollPath(self, year: int, month: int) -> str:
        """薪资文件路径"""
        return os.path.join(self.dataDir, "payroll", f"{year}-{month:02d}.json")
    
    def savePayrollResult(self, year: int, month: int, results: List[Dict]) -> bool:
        """
        保存薪资计算结果
        
        Args:
            year: 年份
            month: 月份
            results: 薪资计算结果列表
        
        Returns:
            是否成功
        """
        data = {
            "year": year,
            "month": month,
            "calculatedAt": datetime.now().isoformat(),
            "employeeCount": len(results),
            "totalGrossPay": sum(r.get("grossPay", 0) for r in results),
            "totalNetPay": sum(r.get("netPay", 0) for r in results),
            "totalDeductions": sum(r.get("totalDeductions", 0) for r in results),
            "results": results,
        }
        
        try:
            os.makedirs(os.path.join(self.dataDir, "payroll"), exist_ok=True)
            with open(self._payrollPath(year, month), 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except IOError as e:
            print(f"保存薪资结果失败: {e}")
            return False
    
    def loadPayrollResult(self, year: int, month: int) -> Optional[Dict]:
        """
        加载薪资计算结果
        
        Returns:
            薪资数据或 None
        """
        path = self._payrollPath(year, month)
        if not os.path.exists(path):
            return None
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    def listPayrollHistory(self) -> List[Dict]:
        """
        列出薪资计算历史
        
        Returns:
            [{year, month, calculatedAt, employeeCount, totalNetPay}, ...]
        """
        payroll_dir = os.path.join(self.dataDir, "payroll")
        if not os.path.exists(payroll_dir):
            return []
        
        history = []
        for filename in sorted(os.listdir(payroll_dir)):
            if not filename.endswith(".json"):
                continue
            
            path = os.path.join(payroll_dir, filename)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                history.append({
                    "year": data.get("year"),
                    "month": data.get("month"),
                    "calculatedAt": data.get("calculatedAt"),
                    "employeeCount": data.get("employeeCount", 0),
                    "totalNetPay": data.get("totalNetPay", 0),
                    "totalGrossPay": data.get("totalGrossPay", 0),
                })
            except (json.JSONDecodeError, IOError):
                continue
        
        # 倒序
        history.reverse()
        return history
    
    def getPayrollComparison(self, year: int, month: int) -> Optional[Dict]:
        """
        获取薪资环比变化（与上月对比）
        
        Returns:
            {current: {...}, previous: {...}, changes: [...]}
        """
        current = self.loadPayrollResult(year, month)
        if not current:
            return None
        
        # 计算上月
        prev_month = month - 1
        prev_year = year
        if prev_month < 1:
            prev_month = 12
            prev_year -= 1
        
        previous = self.loadPayrollResult(prev_year, prev_month)
        
        changes = []
        if previous:
            prev_results = {r["empNo"]: r for r in previous.get("results", [])}
            curr_results = {r["empNo"]: r for r in current.get("results", [])}
            
            for empNo, curr in curr_results.items():
                if empNo in prev_results:
                    prev = prev_results[empNo]
                    net_diff = curr.get("netPay", 0) - prev.get("netPay", 0)
                    changes.append({
                        "empNo": empNo,
                        "name": curr.get("name", ""),
                        "previousNet": prev.get("netPay", 0),
                        "currentNet": curr.get("netPay", 0),
                        "diff": net_diff,
                    })
        
        return {
            "current": {
                "year": year,
                "month": month,
                "totalNetPay": current.get("totalNetPay", 0),
                "employeeCount": current.get("employeeCount", 0),
            },
            "previous": {
                "year": prev_year,
                "month": prev_month,
                "totalNetPay": previous.get("totalNetPay", 0) if previous else 0,
                "employeeCount": previous.get("employeeCount", 0) if previous else 0,
            } if previous else None,
            "changes": changes,
        }
    
    # ================================================================
    # 对话历史
    # ================================================================
    
    def _conversationPath(self, sessionId: str) -> str:
        return os.path.join(self.dataDir, "conversations", f"{sessionId}.json")
    
    def saveConversation(self, sessionId: str, turns: List[Dict]) -> bool:
        """
        保存对话历史
        
        Args:
            sessionId: 会话 ID
            turns: 对话轮次列表
        """
        data = {
            "sessionId": sessionId,
            "updatedAt": datetime.now().isoformat(),
            "turnCount": len(turns),
            "turns": turns,
        }
        
        try:
            with open(self._conversationPath(sessionId), 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except IOError:
            return False
    
    def loadConversation(self, sessionId: str) -> Optional[Dict]:
        """加载对话历史"""
        path = self._conversationPath(sessionId)
        if not os.path.exists(path):
            return None
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    def listConversations(self, limit: int = 20) -> List[Dict]:
        """列出最近的对话会话"""
        conv_dir = os.path.join(self.dataDir, "conversations")
        if not os.path.exists(conv_dir):
            return []
        
        conversations = []
        for filename in os.listdir(conv_dir):
            if not filename.endswith(".json"):
                continue
            
            path = os.path.join(conv_dir, filename)
            try:
                stat = os.path.getmtime(path)
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                conversations.append({
                    "sessionId": data.get("sessionId", filename[:-5]),
                    "updatedAt": datetime.fromtimestamp(stat).isoformat(),
                    "turnCount": data.get("turnCount", 0),
                })
            except (json.JSONDecodeError, IOError):
                continue
        
        # 按更新时间倒序
        conversations.sort(key=lambda x: x["updatedAt"], reverse=True)
        return conversations[:limit]
    
    # ================================================================
    # 数据导出/备份
    # ================================================================
    
    def exportAllData(self) -> Dict:
        """
        导出所有数据（用于备份）
        
        Returns:
            包含所有数据的字典
        """
        return {
            "exportedAt": datetime.now().isoformat(),
            "version": "1.0",
            "config": self.loadConfig(),
            "payrollHistory": self.listPayrollHistory(),
            "auditStats": self.getAuditStats(),
            "recentConversations": self.listConversations(limit=5),
        }
    
    def getStorageInfo(self) -> Dict:
        """获取存储信息"""
        total_size = 0
        file_count = 0
        
        for root, dirs, files in os.walk(self.dataDir):
            for filename in files:
                path = os.path.join(root, filename)
                total_size += os.path.getsize(path)
                file_count += 1
        
        payroll_count = len(self.listPayrollHistory())
        audit_count = len(self.queryAuditLogs(limit=1))  # 快速检查是否有日志
        
        return {
            "dataDir": self.dataDir,
            "totalSizeBytes": total_size,
            "totalSizeMB": round(total_size / 1024 / 1024, 2),
            "fileCount": file_count,
            "payrollRecords": payroll_count,
            "hasAuditLog": audit_count > 0,
            "isInitialized": self.isInitialized(),
        }
