"""
HR 智能体 - 持久化层测试
覆盖配置管理、审计日志、薪资历史、对话历史
"""

import os
import sys
import json
import tempfile
import shutil
import unittest

sys.path.insert(0, os.path.dirname(__file__))

from hr_store import HRStore


class TestHRStoreConfig(unittest.TestCase):
    """配置管理测试"""
    
    def setUp(self):
        self.tempDir = tempfile.mkdtemp()
        self.store = HRStore(self.tempDir)
    
    def tearDown(self):
        shutil.rmtree(self.tempDir)
    
    def test_default_config(self):
        """测试默认配置"""
        config = self.store.loadConfig()
        self.assertEqual(config["version"], "1.0")
        self.assertFalse(config["isFullyInitialized"])
        self.assertEqual(config["storageType"], "")
        self.assertIn("tables", config)
        self.assertIn("organization", config["tables"])
    
    def test_config_file_created(self):
        """测试配置文件自动创建"""
        config_path = os.path.join(self.tempDir, "config.json")
        self.store.loadConfig()  # 触发创建
        # 不会立即创建文件，只在 save 时创建
        self.assertFalse(os.path.exists(config_path))
        
        self.store.saveConfig()
        self.assertTrue(os.path.exists(config_path))
    
    def test_save_and_load_config(self):
        """测试配置保存和加载"""
        self.store.updateConfig({"storageType": "excel"})
        
        # 新 store 实例应该能读到
        store2 = HRStore(self.tempDir)
        config = store2.loadConfig()
        self.assertEqual(config["storageType"], "excel")
    
    def test_get_config_value(self):
        """测试点号路径读取配置"""
        self.store.updateConfig({
            "tables": {
                "employee": {"filePath": "/test/emp.xlsx"}
            }
        })
        
        path = self.store.getConfigValue("tables.employee.filePath")
        self.assertEqual(path, "/test/emp.xlsx")
        
        # 不存在的路径
        self.assertIsNone(self.store.getConfigValue("tables.xxx.filePath"))
    
    def test_deep_merge(self):
        """测试深度合并"""
        self.store.updateConfig({
            "tables": {
                "employee": {"filePath": "/test/emp.xlsx"}
            }
        })
        self.store.updateConfig({
            "tables": {
                "organization": {"filePath": "/test/org.xlsx"}
            }
        })
        
        config = self.store.loadConfig()
        self.assertEqual(config["tables"]["employee"]["filePath"], "/test/emp.xlsx")
        self.assertEqual(config["tables"]["organization"]["filePath"], "/test/org.xlsx")
    
    def test_is_initialized(self):
        """测试初始化状态检查"""
        self.assertFalse(self.store.isInitialized())
        
        self.store.updateConfig({"isFullyInitialized": True})
        self.assertTrue(self.store.isInitialized())
    
    def test_bind_table(self):
        """测试表格绑定"""
        self.assertFalse(self.store.isInitialized())
        
        self.store.bindTable("organization", "/org.xlsx", "组织架构")
        self.assertFalse(self.store.isInitialized())
        
        self.store.bindTable("employee", "/emp.xlsx", "员工花名册")
        self.assertFalse(self.store.isInitialized())
        
        self.store.bindTable("salary", "/salary.xlsx", "薪资表")
        self.assertTrue(self.store.isInitialized())
        
        # 验证绑定详情
        org = self.store.getTableConfig("organization")
        self.assertTrue(org["isBound"])
        self.assertEqual(org["filePath"], "/org.xlsx")
    
    def test_bind_table_with_column_mapping(self):
        """测试表格绑定带列映射"""
        mapping = {"empNo": "工号", "name": "姓名"}
        self.store.bindTable("employee", "/emp.xlsx", columnMapping=mapping)
        
        config = self.store.loadConfig()
        self.assertEqual(config["columnMappings"]["employee"]["empNo"], "工号")
    
    def test_next_binding_step(self):
        """测试下一步绑定"""
        self.assertEqual(self.store.getNextBindingStep(), "storage_type")
        
        self.store.updateConfig({"storageType": "excel"})
        self.assertEqual(self.store.getNextBindingStep(), "organization")
        
        self.store.bindTable("organization", "/org.xlsx")
        self.assertEqual(self.store.getNextBindingStep(), "employee")
        
        self.store.bindTable("employee", "/emp.xlsx")
        self.assertEqual(self.store.getNextBindingStep(), "salary")
        
        self.store.bindTable("salary", "/salary.xlsx")
        # 三张核心表绑定完成后，考勤表为可选的下一步
        self.assertEqual(self.store.getNextBindingStep(), "attendance")
    
    def test_onboarding_status(self):
        """测试初始化状态摘要"""
        status = self.store.getOnboardingStatus()
        self.assertFalse(status["isFullyInitialized"])
        self.assertEqual(status["storageType"], "")
        self.assertFalse(status["organization"]["isBound"])
    
    def test_reset_config(self):
        """测试配置重置"""
        self.store.bindTable("organization", "/org.xlsx")
        self.store.updateConfig({"storageType": "excel"})
        
        self.store.resetConfig()
        config = self.store.loadConfig()
        self.assertFalse(config["isFullyInitialized"])
        self.assertEqual(config["storageType"], "")
        self.assertFalse(config["tables"]["organization"]["isBound"])
    
    def test_export_import_config(self):
        """测试配置导出导入"""
        self.store.updateConfig({"storageType": "excel"})
        self.store.bindTable("organization", "/org.xlsx")
        
        exported = self.store.exportConfig()
        
        # 用新目录导入
        newDir = tempfile.mkdtemp()
        try:
            newStore = HRStore(newDir)
            self.assertTrue(newStore.importConfig(exported))
            self.assertEqual(newStore.loadConfig()["storageType"], "excel")
        finally:
            shutil.rmtree(newDir)
    
    def test_directory_structure(self):
        """测试存储目录结构"""
        expected_dirs = ["payroll", "conversations"]
        for d in expected_dirs:
            self.assertTrue(os.path.isdir(os.path.join(self.tempDir, d)))


class TestHRStoreAuditLog(unittest.TestCase):
    """审计日志测试"""
    
    def setUp(self):
        self.tempDir = tempfile.mkdtemp()
        self.store = HRStore(self.tempDir)
    
    def tearDown(self):
        shutil.rmtree(self.tempDir)
    
    def test_append_log(self):
        """测试追加日志"""
        log_id = self.store.appendAuditLog(
            action="add_employee",
            targetType="employee",
            targetId="E001",
            details={"name": "张伟"}
        )
        
        self.assertIsNotNone(log_id)
        self.assertEqual(len(log_id), 12)
    
    def test_query_logs(self):
        """测试查询日志"""
        self.store.appendAuditLog("add_employee", "employee", "E001")
        self.store.appendAuditLog("add_employee", "employee", "E002")
        self.store.appendAuditLog("delete_employee", "employee", "E001")
        
        # 查询所有
        logs = self.store.queryAuditLogs()
        self.assertEqual(len(logs), 3)
        
        # 按操作类型筛选
        add_logs = self.store.queryAuditLogs(action="add_employee")
        self.assertEqual(len(add_logs), 2)
        
        # 按 targetId 筛选
        e001_logs = self.store.queryAuditLogs(targetId="E001")
        self.assertEqual(len(e001_logs), 2)
    
    def test_query_logs_order(self):
        """测试日志查询顺序（最新在前）"""
        for i in range(5):
            self.store.appendAuditLog("test_action", "test", f"ID{i:03d}")
        
        logs = self.store.queryAuditLogs()
        self.assertEqual(logs[0]["targetId"], "ID004")  # 最新
        self.assertEqual(logs[-1]["targetId"], "ID000")
    
    def test_query_logs_with_limit(self):
        """测试日志查询限制"""
        for i in range(10):
            self.store.appendAuditLog("test", "test", f"ID{i}")
        
        logs = self.store.queryAuditLogs(limit=3)
        self.assertEqual(len(logs), 3)
    
    def test_audit_stats(self):
        """测试审计统计"""
        self.store.appendAuditLog("add_employee", "employee", "E001")
        self.store.appendAuditLog("add_employee", "employee", "E002")
        self.store.appendAuditLog("calculate_payroll", "payroll", "2026-04")
        
        stats = self.store.getAuditStats()
        self.assertEqual(stats["totalActions"], 3)
        self.assertEqual(stats["actionCounts"]["add_employee"], 2)
    
    def test_jsonl_format(self):
        """测试 JSONL 格式正确"""
        self.store.appendAuditLog("test", "test", "T001")
        
        log_path = self.store.auditLogPath
        with open(log_path, 'r') as f:
            lines = f.readlines()
        
        self.assertEqual(len(lines), 1)
        entry = json.loads(lines[0])
        self.assertIn("id", entry)
        self.assertIn("timestamp", entry)
        self.assertIn("action", entry)


class TestHRStorePayroll(unittest.TestCase):
    """薪资历史测试"""
    
    def setUp(self):
        self.tempDir = tempfile.mkdtemp()
        self.store = HRStore(self.tempDir)
    
    def tearDown(self):
        shutil.rmtree(self.tempDir)
    
    def test_save_and_load_payroll(self):
        """测试薪资保存和加载"""
        results = [
            {"empNo": "E001", "name": "张伟", "grossPay": 50000, "netPay": 38000, "totalDeductions": 12000},
            {"empNo": "E002", "name": "李明", "grossPay": 45000, "netPay": 34000, "totalDeductions": 11000},
        ]
        
        self.assertTrue(self.store.savePayrollResult(2026, 4, results))
        
        data = self.store.loadPayrollResult(2026, 4)
        self.assertIsNotNone(data)
        self.assertEqual(data["year"], 2026)
        self.assertEqual(data["month"], 4)
        self.assertEqual(data["employeeCount"], 2)
        self.assertEqual(data["totalNetPay"], 72000)
    
    def test_load_nonexistent_payroll(self):
        """测试加载不存在的薪资记录"""
        data = self.store.loadPayrollResult(2099, 12)
        self.assertIsNone(data)
    
    def test_list_payroll_history(self):
        """测试薪资历史列表"""
        self.store.savePayrollResult(2026, 3, [{"empNo": "E001", "netPay": 38000}])
        self.store.savePayrollResult(2026, 4, [{"empNo": "E001", "netPay": 38500}])
        
        history = self.store.listPayrollHistory()
        self.assertEqual(len(history), 2)
        # 最新在前
        self.assertEqual(history[0]["year"], 2026)
        self.assertEqual(history[0]["month"], 4)
    
    def test_payroll_comparison(self):
        """测试薪资环比对比"""
        self.store.savePayrollResult(2026, 3, [
            {"empNo": "E001", "name": "张伟", "grossPay": 50000, "netPay": 38000, "totalDeductions": 12000},
        ])
        self.store.savePayrollResult(2026, 4, [
            {"empNo": "E001", "name": "张伟", "grossPay": 50000, "netPay": 39000, "totalDeductions": 11000},
        ])
        
        comparison = self.store.getPayrollComparison(2026, 4)
        self.assertIsNotNone(comparison)
        self.assertEqual(comparison["current"]["totalNetPay"], 39000)
        self.assertEqual(len(comparison["changes"]), 1)
        self.assertEqual(comparison["changes"][0]["diff"], 1000)
    
    def test_payroll_comparison_no_previous(self):
        """测试无上月数据时的环比"""
        self.store.savePayrollResult(2026, 4, [
            {"empNo": "E001", "name": "张伟", "grossPay": 50000, "netPay": 38000, "totalDeductions": 12000},
        ])
        
        comparison = self.store.getPayrollComparison(2026, 4)
        self.assertIsNotNone(comparison)
        self.assertIsNone(comparison["previous"])
        self.assertEqual(len(comparison["changes"]), 0)


class TestHRStoreConversation(unittest.TestCase):
    """对话历史测试"""
    
    def setUp(self):
        self.tempDir = tempfile.mkdtemp()
        self.store = HRStore(self.tempDir)
    
    def tearDown(self):
        shutil.rmtree(self.tempDir)
    
    def test_save_and_load_conversation(self):
        """测试对话保存和加载"""
        turns = [
            {"role": "user", "content": "查看E001"},
            {"role": "assistant", "content": "已找到员工"},
        ]
        
        self.assertTrue(self.store.saveConversation("session-001", turns))
        
        data = self.store.loadConversation("session-001")
        self.assertIsNotNone(data)
        self.assertEqual(data["turnCount"], 2)
        self.assertEqual(data["sessionId"], "session-001")
    
    def test_load_nonexistent_conversation(self):
        """测试加载不存在的对话"""
        data = self.store.loadConversation("nonexistent")
        self.assertIsNone(data)
    
    def test_list_conversations(self):
        """测试列出对话"""
        self.store.saveConversation("session-001", [{"role": "user", "content": "hi"}])
        self.store.saveConversation("session-002", [{"role": "user", "content": "hello"}])
        
        convs = self.store.listConversations()
        self.assertEqual(len(convs), 2)
    
    def test_list_conversations_limit(self):
        """测试对话列表限制"""
        for i in range(10):
            self.store.saveConversation(f"session-{i:03d}", [])
        
        convs = self.store.listConversations(limit=5)
        self.assertEqual(len(convs), 5)


class TestHRStoreStorageInfo(unittest.TestCase):
    """存储信息测试"""
    
    def setUp(self):
        self.tempDir = tempfile.mkdtemp()
        self.store = HRStore(self.tempDir)
    
    def tearDown(self):
        shutil.rmtree(self.tempDir)
    
    def test_storage_info(self):
        """测试存储信息"""
        self.store.saveConfig()
        info = self.store.getStorageInfo()
        
        self.assertEqual(info["dataDir"], self.tempDir)
        self.assertTrue(info["fileCount"] >= 1)  # config.json
        self.assertTrue(info["totalSizeBytes"] > 0)
        self.assertFalse(info["hasAuditLog"])
    
    def test_export_all_data(self):
        """测试导出所有数据"""
        self.store.updateConfig({"storageType": "excel"})
        self.store.savePayrollResult(2026, 4, [])
        
        exported = self.store.exportAllData()
        self.assertIn("exportedAt", exported)
        self.assertIn("config", exported)
        self.assertEqual(exported["config"]["storageType"], "excel")


class TestHRStoreEdgeCases(unittest.TestCase):
    """边界情况测试"""
    
    def setUp(self):
        self.tempDir = tempfile.mkdtemp()
        self.store = HRStore(self.tempDir)
    
    def tearDown(self):
        shutil.rmtree(self.tempDir)
    
    def test_corrupted_config_file(self):
        """测试配置文件损坏"""
        config_path = os.path.join(self.tempDir, "config.json")
        with open(config_path, 'w') as f:
            f.write("{corrupted json")
        
        # 应该返回默认配置而不是崩溃
        config = self.store.loadConfig()
        self.assertEqual(config["version"], "1.0")
    
    def test_import_invalid_json(self):
        """测试导入无效 JSON"""
        self.assertFalse(self.store.importConfig("not json at all"))
    
    def test_empty_audit_query(self):
        """测试空审计日志查询"""
        logs = self.store.queryAuditLogs()
        self.assertEqual(len(logs), 0)
    
    def test_payroll_file_creation(self):
        """测试薪资文件自动创建目录"""
        # 删除 payroll 目录
        payroll_dir = os.path.join(self.tempDir, "payroll")
        if os.path.exists(payroll_dir):
            shutil.rmtree(payroll_dir)
        
        # 保存应该自动创建目录
        self.store.savePayrollResult(2026, 4, [])
        self.assertTrue(os.path.exists(payroll_dir))


if __name__ == "__main__":
    unittest.main()
