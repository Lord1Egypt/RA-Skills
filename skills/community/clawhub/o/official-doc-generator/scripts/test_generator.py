#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能测试脚本
测试official-document-generator技能的各项功能
"""

import os
import sys
import tempfile
import json
from pathlib import Path

# 添加技能目录到路径
skill_dir = Path(__file__).parent.parent
sys.path.insert(0, str(skill_dir))

# 导入测试模块
try:
    from scripts.generate_document import OfficialDocumentGenerator, create_example_config
    from scripts.format_validator import DocumentFormatValidator
    from scripts.sensitive_words_check import SensitiveWordsChecker
    from scripts.template_manager import TemplateManager
except ImportError as e:
    print(f"导入模块失败：{e}")
    print("请确保所有依赖已安装：pip install python-docx")
    sys.exit(1)


def test_document_generation():
    """测试文档生成功能"""
    print("🔧 测试文档生成功能...")
    
    test_cases = [
        ("meeting_minutes", "会议纪要生成测试"),
        ("speech", "发言稿生成测试"),
        ("discussion_outline", "讨论提纲生成测试"),
        ("work_report", "工作汇报生成测试")
    ]
    
    results = []
    
    for doc_type, test_name in test_cases:
        try:
            # 创建临时文件
            with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp:
                output_file = tmp.name
            
            # 生成文档
            generator = OfficialDocumentGenerator()
            config = create_example_config(doc_type)
            generator.create_document(doc_type, config)
            generator.save_document(output_file)
            
            # 检查文件是否创建成功
            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                results.append((doc_type, True, f"{test_name} ✅"))
                print(f"  {test_name}: ✅ 成功")
            else:
                results.append((doc_type, False, f"{test_name} ❌ 文件创建失败"))
                print(f"  {test_name}: ❌ 失败")
            
            # 清理临时文件
            if os.path.exists(output_file):
                os.unlink(output_file)
                
        except Exception as e:
            results.append((doc_type, False, f"{test_name} ❌ 异常: {str(e)}"))
            print(f"  {test_name}: ❌ 异常 - {e}")
    
    return results


def test_format_validation():
    """测试格式验证功能"""
    print("\n🔍 测试格式验证功能...")
    
    try:
        validator = DocumentFormatValidator()
        
        # 创建测试文档
        generator = OfficialDocumentGenerator()
        config = create_example_config("meeting_minutes")
        
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp:
            output_file = tmp.name
        
        generator.create_document("meeting_minutes", config)
        generator.save_document(output_file)
        
        # 验证格式
        result = validator.validate_document(output_file, 'gb_t_9704_2012')
        
        # 清理
        if os.path.exists(output_file):
            os.unlink(output_file)
        
        if result['valid']:
            print("  格式验证: ✅ 通过")
            return [("format_validation", True, "格式验证 ✅")]
        else:
            print(f"  格式验证: ❌ 失败 - {len(result['errors'])}个错误")
            return [("format_validation", False, f"格式验证 ❌ - {len(result['errors'])}个错误")]
            
    except Exception as e:
        print(f"  格式验证: ❌ 异常 - {e}")
        return [("format_validation", False, f"格式验证 ❌ - 异常: {str(e)}")]


def test_sensitive_words_check():
    """测试敏感词检查功能"""
    print("\n🛡️ 测试敏感词检查功能...")
    
    try:
        checker = SensitiveWordsChecker()
        
        # 测试文本
        test_text = """
        这是一份关于数字化转型的工作报告。
        我们需要积极推进数字化转型工作。
        当前经济形势总体稳定。
        """
        
        # 检查敏感词
        result = checker.check_text(test_text, 'strict')
        
        if result['valid']:
            print("  敏感词检查: ✅ 通过")
            return [("sensitive_check", True, "敏感词检查 ✅")]
        else:
            print(f"  敏感词检查: ⚠️ 发现敏感词 - {result['sensitive_count']}个")
            return [("sensitive_check", False, f"敏感词检查 ⚠️ - 发现{result['sensitive_count']}个敏感词")]
            
    except Exception as e:
        print(f"  敏感词检查: ❌ 异常 - {e}")
        return [("sensitive_check", False, f"敏感词检查 ❌ - 异常: {str(e)}")]


def test_template_management():
    """测试模板管理功能"""
    print("\n📁 测试模板管理功能...")
    
    try:
        # 创建临时模板目录
        with tempfile.TemporaryDirectory() as temp_dir:
            manager = TemplateManager(temp_dir)
            
            # 创建默认模板
            manager.create_default_templates()
            
            # 列出模板
            templates = manager.list_templates()
            
            if len(templates) >= 4:  # 应该有4个默认模板
                print(f"  模板管理: ✅ 成功创建{len(templates)}个模板")
                return [("template_management", True, f"模板管理 ✅ - {len(templates)}个模板")]
            else:
                print(f"  模板管理: ❌ 只创建了{len(templates)}个模板")
                return [("template_management", False, f"模板管理 ❌ - 只创建了{len(templates)}个模板")]
                
    except Exception as e:
        print(f"  模板管理: ❌ 异常 - {e}")
        return [("template_management", False, f"模板管理 ❌ - 异常: {str(e)}")]


def test_skill_structure():
    """测试技能目录结构"""
    print("\n📂 测试技能目录结构...")
    
    required_files = [
        "SKILL.md",
        "references/gb_t_9704_2012_standard.md",
        "references/official_language_style.md", 
        "references/document_types_specification.md",
        "references/sensitive_words_list.md",
        "scripts/generate_document.py",
        "scripts/format_validator.py",
        "scripts/sensitive_words_check.py",
        "scripts/template_manager.py"
    ]
    
    missing_files = []
    
    for file_path in required_files:
        full_path = skill_dir / file_path
        if not full_path.exists():
            missing_files.append(file_path)
    
    if not missing_files:
        print("  技能结构: ✅ 所有必需文件都存在")
        return [("skill_structure", True, "技能结构 ✅")]
    else:
        print(f"  技能结构: ❌ 缺少{len(missing_files)}个文件")
        for missing in missing_files:
            print(f"    缺失: {missing}")
        return [("skill_structure", False, f"技能结构 ❌ - 缺少{len(missing_files)}个文件")]


def main():
    """主测试函数"""
    print("="*60)
    print("official-document-generator 技能测试")
    print("="*60)
    
    all_results = []
    
    # 运行所有测试
    all_results.extend(test_skill_structure())
    all_results.extend(test_document_generation())
    all_results.extend(test_format_validation())
    all_results.extend(test_sensitive_words_check())
    all_results.extend(test_template_management())
    
    # 统计结果
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    
    total_tests = len(all_results)
    passed_tests = sum(1 for _, passed, _ in all_results if passed)
    failed_tests = total_tests - passed_tests
    
    print(f"总测试项: {total_tests}")
    print(f"通过项: {passed_tests}")
    print(f"失败项: {failed_tests}")
    
    # 详细结果
    print("\n详细结果:")
    for test_name, passed, message in all_results:
        status = "✅" if passed else "❌"
        print(f"  {status} {message}")
    
    print("\n" + "="*60)
    
    # 总体评估
    if failed_tests == 0:
        print("🎉 所有测试通过！技能功能完整。")
        return 0
    else:
        print(f"⚠️  有{failed_tests}个测试失败，需要进一步检查。")
        return 1


if __name__ == "__main__":
    sys.exit(main())