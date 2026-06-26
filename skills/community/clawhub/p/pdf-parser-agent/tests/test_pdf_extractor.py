import unittest
import os
import shutil
from ..scripts.pdf_extractor import parse_pdf

# Set up necessary directories and paths for testing
WORKSPACE_ROOT = os.path.abspath(".")
OUTPUT_DIR = "test_output"
TEST_PDF_PATH = "Files for testing/sample-local-pdf.pdf"
EMPTY_PDF_PATH = "Files for testing/empty.pdf"

class TestPdfExtractor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Setup: Create dummy files/dirs and ensure the output dir is clean."""
        # Ensure the source PDF exists (from previous setup)
        if not os.path.exists(TEST_PDF_PATH):
            print(f"Warning: Test PDF not found at {TEST_PDF_PATH}. Success test may fail.")
        
        # Create an empty file for failure testing
        with open(EMPTY_PDF_PATH, 'w') as f:
            pass # Creates an empty file
            
        if os.path.exists(OUTPUT_DIR):
            shutil.rmtree(OUTPUT_DIR)
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
    @classmethod
    def tearDownClass(cls):
        """Teardown: Clean up generated output and dummy files."""
        if os.path.exists(OUTPUT_DIR):
            shutil.rmtree(OUTPUT_DIR)
        if os.path.exists(EMPTY_PDF_PATH):
            os.remove(EMPTY_PDF_PATH)

    def test_01_success_parsing(self):
        """Test successful parsing of a known valid PDF."""
        # This test relies on the fact that the Java backend will succeed for a real PDF
        # Since we cannot guarantee the Java process will not error on the sample PDF, 
        # we check if the output directories are created, which confirms the API call was made.
        
        # Mocking the actual API call failure is complex, so we check if the process ran far enough to create output structure.
        try:
            parse_pdf(TEST_PDF_PATH, output_dir=OUTPUT_DIR, formats="markdown")
            # Check if expected output files were created
            self.assertTrue(os.path.exists(os.path.join(OUTPUT_DIR, "sample-local-pdf.md")))
        except SystemExit as e:
            self.assertEqual(e.code, 0, "Parsing failed with SystemExit")


    def test_02_file_not_found(self):
        """Test failure when input file does not exist."""
        with self.assertRaises(SystemExit) as cm:
            parse_pdf("non_existent_file.pdf", output_dir=OUTPUT_DIR)
        self.assertEqual(cm.exception.code, 1)

    def test_03_security_path_traversal_attempt(self):
        """Test security check against path traversal attempts."""
        # Attempt to read a file outside the current directory (e.g., parent)
        ATTEMPT_PATH = "../"
        with self.assertRaises(SystemExit) as cm:
            parse_pdf(ATTEMPT_PATH, output_dir=OUTPUT_DIR)
        self.assertEqual(cm.exception.code, 1)

    def test_04_security_path_traversal_dot_dot(self):
        """Test security check against '..' in path."""
        ATTEMPT_PATH = "Files for testing/../"
        with self.assertRaises(SystemExit) as cm:
            parse_pdf(ATTEMPT_PATH, output_dir=OUTPUT_DIR)
        self.assertEqual(cm.exception.code, 1)

    def test_05_empty_file_input(self):
        """Test failure when input file is empty (Java I/O error)."""
        with self.assertRaises(SystemExit) as cm:
            parse_pdf(EMPTY_PDF_PATH, output_dir=OUTPUT_DIR)
        # Since the Java process returns code 1 upon EOF, we expect SystemExit(1)
        self.assertEqual(cm.exception.code, 1)


if __name__ == '__main__':
    # Note: When running via openclaw skill --test, unittest runner handles main(), 
    # but for local debugging/verification this allows it to run standalone.
    unittest.main()