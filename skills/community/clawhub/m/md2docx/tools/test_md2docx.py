"""
Test suite for md2docx module.

This module contains unit tests for the md2docx conversion functions.
"""

import unittest
import tempfile
import os
from pathlib import Path
from md2docx import convert_md_to_docx, batch_convert_md_to_docx, validate_pandoc_available, ValidationError, FileNotFoundError


class TestMd2Docx(unittest.TestCase):
    """Test cases for md2docx functionality."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_md_content = """# 测试标题

这是一个测试文档。

## 子标题

- 列表项1
- 列表项2

**粗体文本**

*斜体文本*

| 表格 | 测试 |
|------|------|
| 单元格1 | 单元格2 |
"""
        
    def test_convert_md_to_docx_success(self):
        """Test successful conversion of markdown to docx."""
        # Skip if pandoc not available
        if not validate_pandoc_available():
            self.skipTest("Pandoc not available")
        
        # Create test markdown file
        input_file = Path(self.temp_dir) / "test.md"
        output_file = Path(self.temp_dir) / "test.docx"
        
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(self.test_md_content)
        
        # Perform conversion
        result = convert_md_to_docx(str(input_file), str(output_file))
        
        # Assertions
        self.assertTrue(result, "Conversion should succeed")
        self.assertTrue(output_file.exists(), "Output file should exist")
    
    def test_convert_md_to_docx_nonexistent_input(self):
        """Test conversion with non-existent input file."""
        # Skip if pandoc not available
        if not validate_pandoc_available():
            self.skipTest("Pandoc not available")
        
        input_file = Path(self.temp_dir) / "nonexistent.md"
        output_file = Path(self.temp_dir) / "test.docx"
        
        # Should raise FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            convert_md_to_docx(str(input_file), str(output_file))
    
    def test_convert_md_to_docx_invalid_extension(self):
        """Test conversion with invalid file extension."""
        # Skip if pandoc not available
        if not validate_pandoc_available():
            self.skipTest("Pandoc not available")
        
        input_file = Path(self.temp_dir) / "test.txt"
        output_file = Path(self.temp_dir) / "test.docx"
        
        # Create a txt file instead of md
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write("This is not a markdown file")
        
        # Should raise ValidationError
        with self.assertRaises(ValidationError):
            convert_md_to_docx(str(input_file), str(output_file))
    
    def test_batch_convert_md_to_docx(self):
        """Test batch conversion of markdown files."""
        # Skip if pandoc not available
        if not validate_pandoc_available():
            self.skipTest("Pandoc not available")
        
        # Create multiple test markdown files
        for i in range(2):
            input_file = Path(self.temp_dir) / f"test_{i}.md"
            with open(input_file, 'w', encoding='utf-8') as f:
                f.write(f"# Test Document {i}\n\nContent for document {i}.")
        
        output_dir = Path(self.temp_dir) / "output"
        
        # Perform batch conversion
        results = batch_convert_md_to_docx(self.temp_dir, str(output_dir))
        
        # Assertions
        self.assertEqual(results["success"], 2, "Should convert 2 files successfully")
        self.assertEqual(results["failed"], 0, "Should have 0 failed conversions")
        
        # Check output files exist
        for i in range(2):
            output_file = output_dir / f"test_{i}.docx"
            self.assertTrue(output_file.exists(), f"Output file test_{i}.docx should exist")
    
    def test_batch_convert_md_to_docx_with_subdirs(self):
        """Test batch conversion with recursive option."""
        # Skip if pandoc not available
        if not validate_pandoc_available():
            self.skipTest("Pandoc not available")
        
        # Create subdirectory
        subdir = Path(self.temp_dir) / "subdir"
        subdir.mkdir()
        
        # Create markdown files in both root and subdirectory
        for i in range(2):
            # Root directory
            input_file = Path(self.temp_dir) / f"root_test_{i}.md"
            with open(input_file, 'w', encoding='utf-8') as f:
                f.write(f"# Root Test Document {i}\n\nContent for root document {i}.")
            
            # Subdirectory
            input_file = subdir / f"sub_test_{i}.md"
            with open(input_file, 'w', encoding='utf-8') as f:
                f.write(f"# Sub Test Document {i}\n\nContent for sub document {i}.")
        
        output_dir = Path(self.temp_dir) / "output_recursive"
        
        # Perform batch conversion with recursive option
        results = batch_convert_md_to_docx(self.temp_dir, str(output_dir), recursive=True)
        
        # In total, we have 4 files (2 in root + 2 in subdirectory)
        expected_total = 4
        self.assertEqual(results["success"], expected_total, f"Should convert {expected_total} files successfully")
        self.assertEqual(results["failed"], 0, "Should have 0 failed conversions")
    
    def test_batch_convert_md_to_docx_nonexistent_directory(self):
        """Test batch conversion with non-existent input directory."""
        nonexistent_dir = Path(self.temp_dir) / "nonexistent"
        output_dir = Path(self.temp_dir) / "output"
        
        # Should raise FileNotFoundError
        with self.assertRaises(FileNotFoundError):
            batch_convert_md_to_docx(str(nonexistent_dir), str(output_dir))


class TestPandocAvailability(unittest.TestCase):
    """Test pandoc availability check."""
    
    def test_validate_pandoc_available(self):
        """Test pandoc availability detection."""
        # This test will return True if pandoc is available, False otherwise
        # We just ensure the function runs without error
        result = validate_pandoc_available()
        self.assertIsInstance(result, bool)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases for conversion functions."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.temp_dir = tempfile.mkdtemp()
    
    def test_empty_markdown_file(self):
        """Test conversion of empty markdown file."""
        # Skip if pandoc not available
        if not validate_pandoc_available():
            self.skipTest("Pandoc not available")
        
        input_file = Path(self.temp_dir) / "empty.md"
        output_file = Path(self.temp_dir) / "empty.docx"
        
        # Create empty markdown file
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write("")
        
        # Should still succeed with empty content
        result = convert_md_to_docx(str(input_file), str(output_file))
        self.assertTrue(result, "Conversion of empty file should succeed")
        self.assertTrue(output_file.exists(), "Output file should exist even for empty input")


if __name__ == '__main__':
    # Check if pandoc is available before running tests
    if not validate_pandoc_available():
        print("Warning: Pandoc not found. Some tests will be skipped.")
    
    # Run the tests
    unittest.main(verbosity=2)