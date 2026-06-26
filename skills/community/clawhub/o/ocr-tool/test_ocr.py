#!/usr/bin/env python3
"""
Test script for OCR Tool skill
"""

import subprocess
import os
import sys

def test_tesseract_installation():
    """Test if Tesseract is installed and working"""
    print("Testing Tesseract installation...")
    
    try:
        result = subprocess.run(
            ['tesseract', '--version'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            print("✓ Tesseract is installed")
            print(f"  Version: {result.stdout.split()[1]}")
            return True
        else:
            print("✗ Tesseract returned error")
            return False
            
    except FileNotFoundError:
        print("✗ Tesseract not found in PATH")
        return False
    except Exception as e:
        print(f"✗ Error testing Tesseract: {str(e)}")
        return False

def test_language_packs():
    """Test if Chinese language packs are available"""
    print("\nTesting language packs...")
    
    # List available languages
    try:
        result = subprocess.run(
            ['tesseract', '--list-langs'],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            langs = result.stdout.strip().split('\n')[1:]  # Skip first line
            print(f"✓ Found {len(langs)} language packs")
            
            # Check for Chinese
            chinese_packs = [lang for lang in langs if 'chi' in lang]
            if chinese_packs:
                print(f"✓ Chinese language packs: {', '.join(chinese_packs)}")
                return True
            else:
                print("✗ No Chinese language packs found")
                print("  Install with: tesseract-ocr-chi-sim package")
                return False
        else:
            print("✗ Failed to list languages")
            return False
            
    except Exception as e:
        print(f"✗ Error listing languages: {str(e)}")
        return False

def test_ocr_on_sample():
    """Test OCR on a sample image if available"""
    print("\nTesting OCR functionality...")
    
    # Check if there's a sample image
    sample_images = [
        'test_image.png',
        'sample.png',
        'announcement.png'
    ]
    
    found_image = None
    for img in sample_images:
        if os.path.exists(img):
            found_image = img
            break
    
    if not found_image:
        print("⚠ No sample image found for testing")
        print("  Create a test_image.png with some text to test OCR")
        return None
    
    print(f"✓ Found sample image: {found_image}")
    
    try:
        # Test English OCR
        result = subprocess.run(
            ['tesseract', found_image, 'stdout'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=10
        )
        
        if result.returncode == 0:
            text = result.stdout.strip()
            if text:
                print(f"✓ OCR successful (English)")
                print(f"  Extracted {len(text)} characters")
                if len(text) > 100:
                    print(f"  Preview: {text[:100]}...")
                else:
                    print(f"  Content: {text}")
                return True
            else:
                print("⚠ OCR returned empty text")
                return False
        else:
            print(f"✗ OCR failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ OCR timed out")
        return False
    except Exception as e:
        print(f"✗ Error during OCR: {str(e)}")
        return False

def test_python_script():
    """Test the Python OCR script"""
    print("\nTesting Python OCR script...")
    
    script_path = os.path.join('scripts', 'ocr_extract.py')
    if not os.path.exists(script_path):
        print("✗ Python script not found")
        return False
    
    try:
        # Test script import
        import importlib.util
        spec = importlib.util.spec_from_file_location("ocr_extract", script_path)
        module = importlib.util.module_from_spec(spec)
        
        # Mock sys.argv for testing
        import sys
        original_argv = sys.argv
        sys.argv = ['ocr_extract.py', '--help']
        
        try:
            spec.loader.exec_module(module)
            print("✓ Python script loads successfully")
            
            # Check if main functions exist
            if hasattr(module, 'run_tesseract'):
                print("✓ Function 'run_tesseract' exists")
            if hasattr(module, 'extract_financial_info'):
                print("✓ Function 'extract_financial_info' exists")
            if hasattr(module, 'analyze_image'):
                print("✓ Function 'analyze_image' exists")
                
            return True
        finally:
            sys.argv = original_argv
            
    except Exception as e:
        print(f"✗ Error testing Python script: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("OCR Tool Skill - Test Suite")
    print("=" * 60)
    
    tests = [
        ("Tesseract Installation", test_tesseract_installation),
        ("Language Packs", test_language_packs),
        ("OCR Functionality", test_ocr_on_sample),
        ("Python Script", test_python_script),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n[{test_name}]")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ Test failed with exception: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed! OCR Tool skill is ready.")
        return 0
    elif passed >= total / 2:
        print("⚠ Some tests failed, but core functionality may work.")
        print("   Check the failed tests above for details.")
        return 1
    else:
        print("❌ Multiple tests failed. OCR Tool may not work correctly.")
        print("   Please fix the issues above.")
        return 2

if __name__ == '__main__':
    sys.exit(main())