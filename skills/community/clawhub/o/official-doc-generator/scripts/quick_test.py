#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速测试脚本 - 验证增强功能基本可用性
"""

import os
import sys
import json
from pathlib import Path

# 添加技能目录到路径
skill_dir = Path(__file__).parent.parent
sys.path.insert(0, str(skill_dir))

def test_imports():
    """测试所有模块是否可以正常导入"""
    print("="*60)
    print("测试模块导入")
    print("="*60)
    
    modules_to_test = [
        ('generate_document_enhanced', 'EnhancedDocumentGenerator'),
        ('sensitive_words_check_enhanced', 'SensitiveWordsCheckerEnhanced'),
        ('revision_history', 'RevisionHistoryManager'),
        ('revision_history', 'DocumentRevisionTracker')
    ]
    
    all_imported = True
    for module_name, class_name in modules_to_test:
        try:
            module = __import__(module_name)
            if hasattr(module, class_name):
                print(f"✅ {module_name}.{class_name} - 导入成功")
            else:
                print(f"❌ {module_name}.{class_name} - 类不存在")
                all_imported = False
        except ImportError as e:
            print(f"❌ {module_name} - 导入失败: {e}")
            all_imported = False
        except Exception as e:
            print(f"❌ {module_name} - 错误: {e}")
            all_imported = False
    
    return all_imported

def test_config_files():
    """测试配置文件"""
    print("\n" + "="*60)
    print("测试配置文件")
    print("="*60)
    
    config_files = [
        os.path.join(skill_dir, "examples", "basic_config.json"),
        os.path.join(skill_dir, "examples", "enhanced_config.json")
    ]
    
    all_valid = True
    for config_file in config_files:
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                print(f"✅ {os.path.basename(config_file)} - 加载成功 ({len(str(config))} 字符)")
            else:
                print(f"❌ {config_file} - 文件不存在")
                all_valid = False
        except Exception as e:
            print(f"❌ {os.path.basename(config_file)} - 加载失败: {e}")
            all_valid = False
    
    return all_valid

def test_enhanced_document_generation():
    """测试增强版文档生成器"""
    print("\n" + "="*60)
    print("测试增强版文档生成器")
    print("="*60)
    
    try:
        from generate_document_enhanced import EnhancedDocumentGenerator
        
        # 创建测试配置
        test_config = {
            "title": "快速测试",
            "meeting_info": {
                "time": "2026年3月28日",
                "location": "测试会议室",
                "host": "测试主持人",
                "recorder": "测试记录员"
            },
            "topics": [
                "测试议题1 (Test Topic 1)",
                "测试议题2 (Test Topic 2)"
            ]
        }
        
        # 创建生成器（禁用历史跟踪以避免文件IO）
        generator = EnhancedDocumentGenerator(enable_history_tracking=False)
        
        # 创建文档
        doc = generator.create_document(
            doc_type="meeting_minutes",
            config=test_config,
            author="测试用户"
        )
        
        if doc:
            print("✅ 文档对象创建成功")
            
            # 检查样式
            if hasattr(generator, 'styles') and generator.styles:
                print(f"✅ 样式数量: {len(generator.styles)}")
                for style_name in generator.styles:
                    print(f"   - {style_name}")
            
            # 检查英文字体设置
            if hasattr(generator, 'english_font_name'):
                print(f"✅ 英文字体设置: {generator.english_font_name}")
            
            return True
        else:
            print("❌ 文档对象创建失败")
            return False
            
    except Exception as e:
        print(f"❌ 文档生成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_sensitive_words_checker():
    """测试增强版敏感词检查器"""
    print("\n" + "="*60)
    print("测试增强版敏感词检查器")
    print("="*60)
    
    try:
        from sensitive_words_check_enhanced import SensitiveWordsCheckerEnhanced
        
        # 创建检查器
        checker = SensitiveWordsCheckerEnhanced()
        
        # 测试文本
        test_text = "这是一个测试文档，包含一些测试内容。"
        
        # 检查文本
        result = checker.check_text(test_text, document_type='meeting_minutes')
        
        if isinstance(result, dict):
            print("✅ 敏感词检查器工作正常")
            print(f"   检查结果: {'通过' if result.get('valid') else '未通过'}")
            print(f"   敏感词数量: {result.get('sensitive_count', 0)}")
            
            # 检查文档类型映射
            if hasattr(checker, 'document_type_levels'):
                print(f"✅ 文档类型级别映射: {len(checker.document_type_levels)} 种类型")
            
            return True
        else:
            print("❌ 敏感词检查器返回结果格式错误")
            return False
            
    except Exception as e:
        print(f"❌ 敏感词检查测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_revision_history():
    """测试修订历史管理器"""
    print("\n" + "="*60)
    print("测试修订历史管理器")
    print("="*60)
    
    try:
        from revision_history import RevisionHistoryManager
        
        # 创建管理器
        manager = RevisionHistoryManager()
        
        # 测试创建修订记录
        record = manager.create_revision_record(
            document_path="test.docx",
            document_type="meeting_minutes",
            author="测试用户",
            action="create"
        )
        
        if isinstance(record, dict) and 'id' in record:
            print("✅ 修订记录创建成功")
            print(f"   记录ID: {record['id']}")
            print(f"   文档类型: {record.get('document_type')}")
            print(f"   操作类型: {record.get('action')}")
            
            # 检查支持的格式
            if hasattr(manager, 'supported_formats'):
                print(f"✅ 支持格式: {', '.join(manager.supported_formats)}")
            
            return True
        else:
            print("❌ 修订记录创建失败")
            return False
            
    except Exception as e:
        print(f"❌ 修订历史测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("官方文档生成器 - 增强功能快速测试")
    print("="*60)
    
    test_results = {
        'imports': test_imports(),
        'config_files': test_config_files(),
        'document_generation': test_enhanced_document_generation(),
        'sensitive_words': test_sensitive_words_checker(),
        'revision_history': test_revision_history()
    }
    
    # 显示测试结果
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    
    total_tests = len(test_results)
    passed_tests = sum(1 for result in test_results.values() if result)
    
    for test_name, result in test_results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
    
    print(f"\n📊 总计：{passed_tests}/{total_tests} 项测试通过")
    
    if passed_tests == total_tests:
        print("\n🎉 所有快速测试通过！增强功能基本可用。")
        print("\n📋 下一步：")
        print("  1. 运行完整测试: python scripts/test_enhanced_features.py")
        print("  2. 生成示例文档: python scripts/generate_document_enhanced.py --type meeting_minutes --config examples/enhanced_config.json --output test.docx")
        print("  3. 测试敏感词检查: python scripts/sensitive_words_check_enhanced.py --text \"测试文本\" --document-type meeting_minutes")
    else:
        print(f"\n⚠️  {total_tests - passed_tests} 项测试失败，请检查相关问题。")
    
    return all(test_results.values())

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)