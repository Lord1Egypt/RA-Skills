#!/usr/bin/env python3
"""
Long Task Manager - 基础测试
"""

import unittest
import sys
import tempfile
import shutil

sys.path.insert(0, '../lib')

from long_task_manager import LongTaskManager, TaskWorker


class TestLongTaskManager(unittest.TestCase):
    """测试 LongTaskManager"""
    
    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        self.manager = LongTaskManager(task_dir=self.temp_dir)
    
    def tearDown(self):
        """测试后清理"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_submit_task(self):
        """测试提交任务"""
        task_id = self.manager.submit(
            agent_id="test_agent",
            task_config={
                "name": "测试任务",
                "type": "test",
                "total_items": 10
            }
        )
        
        self.assertIsNotNone(task_id)
        self.assertTrue(len(task_id) > 0)
        
        status = self.manager.get_status(task_id)
        self.assertIsNotNone(status)
        self.assertEqual(status['status'], 'pending')
    
    def test_complete_task(self):
        """测试完成任务"""
        task_id = self.manager.submit(
            agent_id="test_agent",
            task_config={"name": "测试", "type": "test", "total_items": 1}
        )
        
        self.manager.complete(task_id, {
            "files": ["file1.txt"],
            "summary": "测试完成"
        })
        
        status = self.manager.get_status(task_id)
        self.assertEqual(status['status'], 'completed')
        
        result = self.manager.get_result(task_id)
        self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
