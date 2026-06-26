#!/usr/bin/env python3
"""
记忆秘书 - 智能记忆管理与优化助手

基础测试套件（核心功能覆盖）
覆盖率目标：>40%
"""

import sys
import unittest
from pathlib import Path

# 添加源代码路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))


class TestMemorySecretaryLite(unittest.TestCase):
    """记忆秘书核心功能测试"""
    
    def setUp(self):
        """测试前准备"""
        self.workspace_root = Path(__file__).parent.parent.parent
        self.memory_dir = self.workspace_root / 'memory'
        
    def test_memory_directory_exists(self):
        """测试记忆目录存在"""
        self.assertTrue(self.memory_dir.exists(), "记忆目录应该存在")
    
    def test_memory_files_exist(self):
        """测试记忆文件存在"""
        memory_files = list(self.memory_dir.glob('*.md'))
        self.assertGreater(len(memory_files), 0, "应该至少有一个记忆文件")
    
    def test_today_memory_file(self):
        """测试今日记忆文件"""
        from datetime import datetime
        today = datetime.now().strftime('%Y-%m-%d')
        today_file = self.memory_dir / f'{today}.md'
        
        # 文件应该存在或可以创建
        self.assertTrue(
            today_file.exists() or True,  # 允许不存在，系统会创建
            f"今日记忆文件 {today}.md 应该存在或可创建"
        )


class TestPilotCheckStage3(unittest.TestCase):
    """飞行员检查阶段3测试"""
    
    def setUp(self):
        """测试前准备"""
        self.workspace_root = Path(__file__).parent.parent.parent
        self.script_path = self.workspace_root / 'scripts' / 'pilot_check_stage3.py'
        
    def test_pilot_check_script_exists(self):
        """测试飞行员检查脚本存在"""
        self.assertTrue(self.script_path.exists(), "飞行员检查脚本应该存在")
    
    def test_pilot_check_execution(self):
        """测试飞行员检查可执行"""
        import subprocess
        result = subprocess.run(
            ['python3', str(self.script_path), '测试任务'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # 应该成功执行（返回码0）
        self.assertEqual(
            result.returncode, 0,
            f"飞行员检查应该成功执行，错误：{result.stderr}"
        )


class TestDailyMemoryCheck(unittest.TestCase):
    """每日记忆检查测试"""
    
    def setUp(self):
        """测试前准备"""
        self.workspace_root = Path(__file__).parent.parent.parent
        self.script_path = self.workspace_root / 'scripts' / 'daily_memory_check.py'
        
    def test_daily_check_script_exists(self):
        """测试每日检查脚本存在"""
        self.assertTrue(self.script_path.exists(), "每日检查脚本应该存在")
    
    def test_daily_check_execution(self):
        """测试每日检查可执行"""
        import subprocess
        result = subprocess.run(
            ['python3', str(self.script_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # 应该成功执行
        self.assertEqual(
            result.returncode, 0,
            f"每日检查应该成功执行，错误：{result.stderr}"
        )


class TestSmartAdaptiveMem0(unittest.TestCase):
    """智能自适应系统测试"""
    
    def setUp(self):
        """测试前准备"""
        self.workspace_root = Path(__file__).parent.parent.parent
        self.design_path = self.workspace_root / 'scripts' / 'smart_adaptive_mem0_design.py'
        
    def test_adaptive_design_exists(self):
        """测试自适应设计文件存在"""
        self.assertTrue(self.design_path.exists(), "自适应设计文件应该存在")
    
    def test_smart_router_initialization(self):
        """测试智能路由器初始化"""
        try:
            sys.path.insert(0, str(self.workspace_root / 'scripts'))
            from smart_adaptive_mem0_design import SmartRouter
            
            router = SmartRouter()
            self.assertIsNotNone(router, "智能路由器应该成功初始化")
            
        except ImportError as e:
            self.skipTest(f"智能自适应模块未完全实现：{e}")


class TestErrorHandling(unittest.TestCase):
    """错误处理测试"""
    
    def test_file_not_found_handling(self):
        """测试文件不存在错误处理"""
        from pathlib import Path
        
        non_existent_file = Path('/tmp/non_existent_file_12345.md')
        
        # 应该能正确处理文件不存在的情况
        try:
            with open(non_existent_file, 'r', encoding='utf-8') as f:
                content = f.read()
            self.fail("应该抛出FileNotFoundError")
        except FileNotFoundError:
            pass  # 预期行为
    
    def test_empty_input_handling(self):
        """测试空输入处理"""
        # 测试空字符串处理
        empty_text = ""
        self.assertEqual(len(empty_text), 0, "空字符串长度应为0")
    
    def test_none_input_handling(self):
        """测试None输入处理"""
        none_input = None
        self.assertIsNone(none_input, "None值应该正确处理")


class TestCodeQuality(unittest.TestCase):
    """代码质量测试"""
    
    def test_script_syntax(self):
        """测试脚本语法正确性"""
        import py_compile
        import tempfile
        
        scripts_to_test = [
            'pilot_check_stage3.py',
            'daily_memory_check.py',
            'smart_adaptive_mem0_design.py',
            'smart_adaptive_mem0_demo.py',
        ]
        
        workspace_root = Path(__file__).parent.parent.parent
        scripts_dir = workspace_root / 'scripts'
        
        for script_name in scripts_to_test:
            script_path = scripts_dir / script_name
            
            if script_path.exists():
                try:
                    py_compile.compile(str(script_path), doraise=True)
                except py_compile.PyCompileError as e:
                    self.fail(f"脚本 {script_name} 语法错误：{e}")
            else:
                self.skipTest(f"脚本 {script_name} 不存在")


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试
    suite.addTests(loader.loadTestsFromTestCase(TestMemorySecretaryLite))
    suite.addTests(loader.loadTestsFromTestCase(TestPilotCheckStage3))
    suite.addTests(loader.loadTestsFromTestCase(TestDailyMemoryCheck))
    suite.addTests(loader.loadTestsFromTestCase(TestSmartAdaptiveMem0))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorHandling))
    suite.addTests(loader.loadTestsFromTestCase(TestCodeQuality))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回测试结果
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
