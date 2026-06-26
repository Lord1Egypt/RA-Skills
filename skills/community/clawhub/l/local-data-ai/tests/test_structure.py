#!/usr/bin/env python3
"""
LocalDataAI 轻量级验证测试
无需安装 heavy 依赖即可验证代码结构
"""

import os
import sys
import unittest
import tempfile
import shutil
from pathlib import Path

# 测试目录结构
def test_directory_structure():
    """验证目录结构完整"""
    base_dir = Path(__file__).parent.parent
    
    required_files = [
        "SKILL.md",
        "README.md",
        "requirements.txt",
        "config/model_config.yaml",
        "config/parser_config.yaml",
        "config/security_config.yaml",
        "scripts/local_ai_engine.py",
        "scripts/file_parser.py",
        "scripts/vector_store.py",
        "scripts/retry_adapter.py",
        "scripts/sandbox.py",
        "scripts/large_file_handler.py",
        "scripts/compliance_logger.py",
        "scripts/download_models.py",
        "examples/basic_usage.py",
        "tests/test_local_ai.py"
    ]
    
    missing = []
    for file in required_files:
        if not (base_dir / file).exists():
            missing.append(file)
    
    if missing:
        print(f"❌ 缺少文件: {missing}")
        return False
    
    print(f"✅ 目录结构完整 ({len(required_files)} 个文件)")
    return True


# 测试配置文件可解析
def test_config_files():
    """验证配置文件格式正确"""
    import yaml
    
    base_dir = Path(__file__).parent.parent
    configs = [
        "config/model_config.yaml",
        "config/parser_config.yaml",
        "config/security_config.yaml"
    ]
    
    for config_file in configs:
        try:
            with open(base_dir / config_file, 'r') as f:
                yaml.safe_load(f)
            print(f"✅ {config_file} 格式正确")
        except Exception as e:
            print(f"❌ {config_file} 解析失败: {e}")
            return False
    
    return True


# 测试 Python 语法
def test_python_syntax():
    """验证 Python 文件语法正确"""
    import py_compile
    
    base_dir = Path(__file__).parent.parent
    scripts_dir = base_dir / "scripts"
    
    py_files = list(scripts_dir.glob("*.py"))
    
    for py_file in py_files:
        try:
            py_compile.compile(str(py_file), doraise=True)
            print(f"✅ {py_file.name} 语法正确")
        except Exception as e:
            print(f"❌ {py_file.name} 语法错误: {e}")
            return False
    
    return True


# 测试类定义可导入（模拟依赖）
def test_class_definitions():
    """验证核心类定义完整"""
    base_dir = Path(__file__).parent.parent
    
    # 读取文件内容检查关键类
    checks = [
        ("scripts/local_ai_engine.py", ["LocalAIEngine", "Document", "SearchResult"]),
        ("scripts/file_parser.py", ["FileParser", "ParseResult", "Document"]),
        ("scripts/vector_store.py", ["VectorStore", "Chunk"]),
        ("scripts/sandbox.py", ["SecureSandbox", "SandboxConfig"]),
        ("scripts/large_file_handler.py", ["LargeFileHandler", "ProcessingProgress"]),
        ("scripts/compliance_logger.py", ["ComplianceLogger", "AuditLogEntry"]),
        ("scripts/retry_adapter.py", ["RetryAdapter", "FallbackHandler"])
    ]
    
    for file_path, classes in checks:
        full_path = base_dir / file_path
        with open(full_path, 'r') as f:
            content = f.read()
        
        for cls in classes:
            if f"class {cls}" not in content:
                print(f"❌ {file_path} 缺少类 {cls}")
                return False
        
        print(f"✅ {file_path} 类定义完整 ({len(classes)} 个)")
    
    return True


# 测试文档完整性
def test_documentation():
    """验证文档完整"""
    base_dir = Path(__file__).parent.parent
    
    readme = base_dir / "README.md"
    with open(readme, 'r') as f:
        content = f.read()
    
    required_sections = [
        "功能概览",
        "安装指南",
        "快速开始",
        "核心 API",
        "配置说明"
    ]
    
    missing = []
    for section in required_sections:
        if section not in content:
            missing.append(section)
    
    if missing:
        print(f"❌ README 缺少章节: {missing}")
        return False
    
    print(f"✅ README 文档完整 ({len(required_sections)} 个核心章节)")
    return True


def main():
    """运行所有验证测试"""
    print("=" * 60)
    print("LocalDataAI 轻量级验证测试")
    print("=" * 60)
    print()
    
    tests = [
        ("目录结构", test_directory_structure),
        ("配置文件", test_config_files),
        ("Python 语法", test_python_syntax),
        ("类定义", test_class_definitions),
        ("文档完整性", test_documentation)
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        print(f"\n📋 {name}:")
        print("-" * 40)
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ 测试异常: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"测试结果: ✅ {passed} 通过, ❌ {failed} 失败")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
