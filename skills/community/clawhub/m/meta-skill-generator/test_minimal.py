#!/usr/bin/env python3
"""
最简单的测试 - 不依赖外部库
只测试核心逻辑和语法
"""

import sys
import os
from pathlib import Path

def test_syntax():
    """测试所有 Python 文件的语法"""
    print("测试 Python 语法...")
    
    python_files = [
        "scripts/__init__.py",
        "scripts/embed_skill.py",
        "scripts/planner.py", 
        "scripts/generator.py",
        "scripts/tester.py",
        "scripts/evaluator.py",
        "scripts/optimizer.py",
        "scripts/composer.py",
        "scripts/auto_refactor.py",
    ]
    
    errors = []
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 编译检查语法
            compile(content, file_path, 'exec')
            print(f"✅ {file_path} 语法正确")
            
        except SyntaxError as e:
            print(f"❌ {file_path} 语法错误: {e}")
            errors.append(f"{file_path}: {e}")
        except Exception as e:
            print(f"❌ {file_path} 读取错误: {e}")
            errors.append(f"{file_path}: {e}")
    
    return len(errors) == 0, errors

def test_files_structure():
    """测试文件结构"""
    print("\n测试文件结构...")
    
    required_files = [
        "SKILL.md",
        "config.yaml",
        "scripts/__init__.py",
        "scripts/embed_skill.py",
        "scripts/planner.py",
        "scripts/generator.py",
        "scripts/tester.py",
        "scripts/evaluator.py",
        "scripts/optimizer.py",
        "scripts/composer.py",
        "scripts/auto_refactor.py",
        "assets/templates/base_skill.py",
        "assets/templates/metadata.yaml",
        "references/architecture.md",
        "references/api_reference.md",
        "references/examples.md"
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    return len(missing_files) == 0, missing_files

def test_config_format():
    """测试配置文件格式"""
    print("\n测试配置文件格式...")
    
    try:
        import yaml
        
        config_path = Path("config.yaml")
        if not config_path.exists():
            return False, ["config.yaml 不存在"]
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        if not isinstance(config, dict):
            return False, ["config.yaml 不是有效的字典"]
        
        if 'system' not in config:
            return False, ["配置文件缺少 'system' 部分"]
        
        print("✅ config.yaml 格式正确")
        return True, []
        
    except ImportError:
        # 如果没有 yaml 库，简单检查文件是否存在
        if Path("config.yaml").exists():
            print("⚠️ 无法测试 YAML 格式（缺少 yaml 库），但文件存在")
            return True, []
        else:
            return False, ["config.yaml 不存在"]
    except Exception as e:
        return False, [f"配置文件错误: {e}"]

def test_skill_structure():
    """测试技能结构"""
    print("\n测试技能结构...")
    
    try:
        # 测试 BaseSkill 是否可以独立运行
        base_skill_path = "assets/templates/base_skill.py"
        if not Path(base_skill_path).exists():
            return False, [f"{base_skill_path} 不存在"]
        
        with open(base_skill_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否包含必要的类和方法
        if "class BaseSkill" not in content:
            return False, ["BaseSkill 类不存在"]
        
        if "def execute" not in content:
            return False, ["execute 方法不存在"]
        
        if "def validate_input" not in content:
            return False, ["validate_input 方法不存在"]
        
        if "def handle_error" not in content:
            return False, ["handle_error 方法不存在"]
        
        print("✅ BaseSkill 结构正确")
        return True, []
        
    except Exception as e:
        return False, [f"技能结构错误: {e}"]

def test_metadata_template():
    """测试元数据模板"""
    print("\n测试元数据模板...")
    
    try:
        metadata_path = "assets/templates/metadata.yaml"
        if not Path(metadata_path).exists():
            return False, [f"{metadata_path} 不存在"]
        
        with open(metadata_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查关键字段
        required_fields = ['id:', 'name:', 'version:', 'description:']
        
        for field in required_fields:
            if field not in content:
                return False, [f"元数据模板缺少 {field}"]
        
        print("✅ metadata.yaml 模板正确")
        return True, []
        
    except Exception as e:
        return False, [f"元数据模板错误: {e}"]

def main():
    """主测试函数"""
    print("Meta-Skill-Generator 基础测试")
    print("=" * 50)
    
    tests = [
        ("文件结构", test_files_structure),
        ("Python 语法", test_syntax),
        ("配置文件", test_config_format),
        ("技能结构", test_skill_structure),
        ("元数据模板", test_metadata_template),
    ]
    
    results = []
    all_errors = []
    
    for test_name, test_func in tests:
        try:
            result, errors = test_func()
            results.append((test_name, result))
            all_errors.extend(errors)
        except Exception as e:
            print(f"{test_name} 测试异常: {e}")
            results.append((test_name, False))
            all_errors.append(f"{test_name}: {e}")
    
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
    
    if all_errors:
        print("\n错误详情:")
        for error in all_errors:
            print(f"  - {error}")
    
    print(f"\n总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("所有基础测试通过！")
        print("\n注意：完整功能需要安装依赖包：")
        print("  - chromadb")
        print("  - networkx") 
        print("  - deepseek-api-client")
        print("  - docker")
        return True
    else:
        print("部分测试失败，需要修复")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)