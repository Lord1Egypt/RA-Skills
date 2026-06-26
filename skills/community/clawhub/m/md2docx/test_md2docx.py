#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for md2docx skill
Tests template file existence and conversion functionality
"""

import os
import sys
from pathlib import Path
import tempfile
import subprocess

# Add the tools directory to the path so we can import md2docx
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tools'))

try:
    from tools.md2docx import MD2DocxConverter
except ImportError:
    print("❌ Could not import MD2DocxConverter from tools/md2docx.py")
    sys.exit(1)


def test_template_exists():
    """Test that the standard-official-template.docx exists"""
    print("Testing template file existence...")
    
    template_path = Path("tools/standard-official-template.docx")
    
    if template_path.exists():
        print("OK Template file exists:", template_path)
        return True
    else:
        print("ERROR Template file does not exist:", template_path)
        return False


def test_converter_initialization():
    """Test that the converter can be initialized properly"""
    print("\nTesting converter initialization...")
    
    try:
        converter = MD2DocxConverter()
        
        # Check that template paths are set correctly
        print(f"   Template directory: {converter.template_dir}")
        print(f"   Default template: {converter.default_template}")
        
        if converter.default_template.exists():
            print("OK Converter initialized successfully with valid template")
            return True
        else:
            print("ERROR Converter template not found")
            return False
    except Exception as e:
        print(f"ERROR Error initializing converter: {str(e)}")
        return False


def test_conversion_functionality():
    """Test basic conversion functionality with a sample markdown"""
    print("\nTesting conversion functionality...")
    
    # Create a temporary markdown file for testing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as temp_md:
        temp_md.write("# 测试标题\n\n这是一个测试文档。\n\n## 测试二级标题\n\n包含一些测试内容。\n\n- 列表项1\n- 列表项2\n\n```python\nprint('Hello World')\n```\n")
        temp_md_path = temp_md.name
    
    try:
        converter = MD2DocxConverter()
        
        # Test if template exists before attempting conversion
        if not converter.default_template.exists():
            print("ERROR Cannot test conversion: template file missing")
            return False
        
        # Create temporary output directory
        with tempfile.TemporaryDirectory() as temp_out_dir:
            # Attempt conversion
            output_file = converter.convert(temp_md_path, output_dir=temp_out_dir)
            
            # Check if output file was created
            if os.path.exists(output_file):
                print(f"OK Conversion successful: {os.path.basename(output_file)} created")
                
                # Check file size (should be non-zero if valid docx)
                if os.path.getsize(output_file) > 0:
                    print("OK Output file has content")
                    return True
                else:
                    print("ERROR Output file is empty")
                    return False
            else:
                print("ERROR Conversion failed: output file not created")
                return False
                
    except Exception as e:
        print(f"ERROR Conversion test failed: {str(e)}")
        return False
    finally:
        # Clean up temporary markdown file
        if os.path.exists(temp_md_path):
            os.remove(temp_md_path)


def run_all_tests():
    """Run all tests and report results"""
    print("Running md2docx skill tests...\n")
    
    tests = [
        ("Template File Existence", test_template_exists),
        ("Converter Initialization", test_converter_initialization),
        ("Conversion Functionality", test_conversion_functionality),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"[{test_name}]")
        if test_func():
            passed += 1
        print()  # Empty line for readability
    
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed!")
        return True
    else:
        print(f"Warning: {total - passed} test(s) failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)