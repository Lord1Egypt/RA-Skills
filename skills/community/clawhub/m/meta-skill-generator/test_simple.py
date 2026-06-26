#!/usr/bin/env python3
"""
简单测试脚本 - 验证 meta-skill-generator 基本功能
"""

import sys
import os
import tempfile
import json
from pathlib import Path

# 添加当前目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试导入"""
    print("测试导入...")
    
    try:
        # 测试基本导入
        from scripts.generator import BaseSkill
        print("BaseSkill 导入成功")
        
        from scripts.tester import SimpleTester
        print("SimpleTester 导入成功")
        
        from scripts.evaluator import SkillEvaluator
        print("SkillEvaluator 导入成功")
        
        from scripts.planner import TaskPlanner
        print("TaskPlanner 导入成功")
        
        from scripts.embed_skill import SkillLibrary
        print("SkillLibrary 导入成功")
        
        return True
        
    except ImportError as e:
        print(f"导入失败: {e}")
        return False

def test_base_skill():
    """测试 BaseSkill"""
    print("\n测试 BaseSkill...")
    
    try:
        from scripts.generator import BaseSkill
        
        # 创建测试技能
        class TestSkill(BaseSkill):
            def execute(self, name="World"):
                return {"success": True, "result": f"Hello, {name}!"}
            
            def validate_input(self, inputs):
                return "name" in inputs
        
        skill = TestSkill()
        result = skill.execute(name="Alice")
        
        if result.get("success") and "Hello, Alice" in str(result.get("result")):
            print("BaseSkill 测试通过")
            return True
        else:
            print("BaseSkill 测试失败")
            return False
            
    except Exception as e:
        print(f"BaseSkill 测试错误: {e}")
        return False

def test_skill_generator():
    """测试 SkillGenerator（无 LLM）"""
    print("\n测试 SkillGenerator...")
    
    try:
        from scripts.generator import SkillGenerator
        
        generator = SkillGenerator(llm_client=None)  # 使用本地模式
        
        # 生成测试技能
        skill = generator.generate("发送邮件技能")
        
        if skill and skill.code:
            print("SkillGenerator 生成代码成功")
            print(f"技能名称: {skill.name}")
            print(f"代码长度: {len(skill.code)} 字符")
            return True
        else:
            print("SkillGenerator 生成失败")
            return False
            
    except Exception as e:
        print(f"SkillGenerator 测试错误: {e}")
        return False

def test_skill_evaluator():
    """测试 SkillEvaluator"""
    print("\n测试 SkillEvaluator...")
    
    try:
        from scripts.evaluator import SkillEvaluator
        from scripts.tester import TestResult
        
        evaluator = SkillEvaluator()
        
        # 模拟测试结果
        test_results = [
            TestResult("test1", True, {"result": "ok"}, None, 0.1),
            TestResult("test2", True, {"result": "ok"}, None, 0.15),
            TestResult("test3", False, None, "error", 0.2),
        ]
        
        times = [0.1, 0.15, 0.2]
        code = "def test(): pass"  # 简单代码
        
        result = evaluator.evaluate(test_results, times, code)
        
        if 0 <= result.score <= 1:
            print(f"SkillEvaluator 测试通过，得分: {result.score}")
            return True
        else:
            print(f"SkillEvaluator 测试失败，得分: {result.score}")
            return False
            
    except Exception as e:
        print(f"SkillEvaluator 测试错误: {e}")
        return False

def main():
    """主测试函数"""
    print("Meta-Skill-Generator 测试开始")
    print("=" * 50)
    
    tests = [
        ("导入测试", test_imports),
        ("BaseSkill", test_base_skill),
        ("SkillGenerator", test_skill_generator),
        ("SkillEvaluator", test_skill_evaluator),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"{test_name} 测试异常: {e}")
            results.append((test_name, False))
    
    # 汇总结果
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "通过" if result else "失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("所有测试通过！Meta-Skill-Generator 基本正常")
        return True
    else:
        print("部分测试失败，需要修复")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)