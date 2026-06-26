"""
LIR-v2 测试用例
"""

import unittest
import sys
import os

# 添加 src 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from reflector import LogicInversionReflector, reflect, reflect_json


class TestLogicInversionReflector(unittest.TestCase):
    """测试逻辑反转反射器"""
    
    def setUp(self):
        self.reflector = LogicInversionReflector()
    
    def test_extract_anchors_basic(self):
        """测试基础锚点提取"""
        text = "我们应该选择核心业务，因为效率总是好的"
        anchors = self.reflector.extract_anchors(text)
        
        self.assertIsInstance(anchors, list)
        self.assertGreater(len(anchors), 0)
    
    def test_extract_anchors_count(self):
        """测试锚点数量"""
        text = "效率总是好的，增长是目标，自动化优于人工，AI 应该辅助人类"
        anchors = self.reflector.extract_anchors(text)
        
        # 应该提取到 3-5 个锚点
        self.assertGreaterEqual(len(anchors), 1)
        self.assertLessEqual(len(anchors), 5)
    
    def test_invert_axiom(self):
        """测试公理反转"""
        axiom = "效率总是好的"
        result = self.reflector.invert_axiom(axiom)
        
        self.assertIn("Counter_Axiom", result)
        self.assertIn("Logic_Deduction", result)
        self.assertIn("Synthetic_Conflict", result)
        self.assertIn("并非总是好的", result["Counter_Axiom"])
    
    def test_reflect_complete(self):
        """测试完整反射流程"""
        user_input = "我们应该选择机票业务作为第一个 AI 试点，因为闭环完整是成功要素"
        result = self.reflector.reflect(user_input)
        
        self.assertIn("Original_Anchors", result)
        self.assertIn("Inversion_Model", result)
        self.assertIn("Meta_Probes", result)
        self.assertIn("System_Lock", result)
        self.assertEqual(result["System_Lock"], "WAIT_FOR_HUMAN_JUDGEMENT")
        self.assertIsInstance(result["Meta_Probes"], list)
        self.assertEqual(len(result["Meta_Probes"]), 2)
    
    def test_reflect_json_format(self):
        """测试 JSON 输出格式"""
        user_input = "扁平化优于科层制"
        json_output = self.reflector.reflect_json(user_input)
        
        import json
        parsed = json.loads(json_output)
        
        self.assertIsInstance(parsed, dict)
        self.assertIn("Original_Anchors", parsed)
        self.assertIn("Inversion_Model", parsed)
    
    def test_meta_probes_quality(self):
        """测试元坐标追问质量"""
        user_input = "AI 应该辅助人类"
        result = self.reflector.reflect(user_input)
        
        probes = result["Meta_Probes"]
        self.assertEqual(len(probes), 2)
        
        # 至少有一个关于动机的追问
        motivation_keywords = ["解决", "恐惧", "证明", "认知"]
        has_motivation = any(
            any(kw in probe for kw in motivation_keywords)
            for probe in probes
        )
        self.assertTrue(has_motivation)
    
    def test_common_axioms_coverage(self):
        """测试常见公理覆盖"""
        test_cases = [
            ("效率总是好的", "效率"),
            ("增长是目标", "增长"),
            ("自动化优于人工", "自动化"),
            ("扁平化优于科层制", "扁平"),
            ("AI 应该辅助人类", "AI")
        ]
        
        for text, expected_keyword in test_cases:
            anchors = self.reflector.extract_anchors(text)
            # 至少能提取到一个锚点
            self.assertGreater(len(anchors), 0)


class TestQuickFunctions(unittest.TestCase):
    """测试快捷函数"""
    
    def test_reflect_function(self):
        """测试 reflect 快捷函数"""
        result = reflect("效率总是好的")
        self.assertIsInstance(result, dict)
        self.assertIn("Original_Anchors", result)
    
    def test_reflect_json_function(self):
        """测试 reflect_json 快捷函数"""
        import json
        json_str = reflect_json("增长是目标")
        parsed = json.loads(json_str)
        self.assertIsInstance(parsed, dict)


if __name__ == "__main__":
    unittest.main()
