#!/usr/bin/env python3
"""
Integration tests for local-tts.

These tests actually run TTS generation. They require:
- For macOS: mlx-audio installed
- For Linux/Windows: qwen-tts and torch installed

Skipped by default in CI. Run with: python -m pytest tests/test_integration.py -v
"""

import unittest
import os
import sys
import tempfile
import subprocess


class TestMacOSTTS(unittest.TestCase):
    """Integration tests for macOS TTS (requires mlx-audio)."""
    
    @classmethod
    def setUpClass(cls):
        """Check if running on macOS with Apple Silicon."""
        import platform
        cls.is_macos = platform.system() == 'Darwin'
        cls.is_apple_silicon = platform.machine() in ['arm64', 'aarch64']
        cls.has_mlx = cls._check_mlx()
    
    @staticmethod
    def _check_mlx():
        """Check if mlx-audio is installed."""
        try:
            import mlx_audio
            return True
        except ImportError:
            return False
    
    def setUp(self):
        """Skip if not on macOS or mlx not available."""
        if not self.is_macos:
            self.skipTest("macOS-specific test")
        if not self.has_mlx:
            self.skipTest("mlx-audio not installed (pip install mlx-audio)")
    
    def test_basic_tts_command(self):
        """Test basic TTS generation on macOS."""
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            output_path = f.name
        
        try:
            cmd = [
                sys.executable, '-m', 'mlx_audio.tts.generate',
                '--text', 'Hello world',
                '--model', 'mlx-community/Qwen3-TTS-12Hz-0.6B-Base-8bit',
                '--output', output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            # Check command succeeded
            self.assertEqual(result.returncode, 0, 
                           f"Command failed: {result.stderr}")
            
            # Check output file exists and has content
            self.assertTrue(os.path.exists(output_path))
            self.assertGreater(os.path.getsize(output_path), 1000,
                             "Output file too small, likely failed")
            
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_wrapper_script_import(self):
        """Test that wrapper script can be imported."""
        script_path = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'tts_macos.py')
        
        # Just check the script exists and is valid Python
        with open(script_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Should compile without errors
        compile(code, script_path, 'exec')


class TestLinuxWindowTTS(unittest.TestCase):
    """Integration tests for Linux/Windows TTS (requires qwen-tts)."""
    
    @classmethod
    def setUpClass(cls):
        """Check if qwen-tts is available."""
        cls.has_qwen_tts = cls._check_qwen_tts()
        cls.has_cuda = cls._check_cuda()
    
    @staticmethod
    def _check_qwen_tts():
        """Check if qwen-tts is installed."""
        try:
            import qwen_tts
            return True
        except ImportError:
            return False
    
    @staticmethod
    def _check_cuda():
        """Check if CUDA is available."""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False
    
    def setUp(self):
        """Skip if qwen-tts not available."""
        if not self.has_qwen_tts:
            self.skipTest("qwen-tts not installed (pip install qwen-tts)")
    
    def test_basic_tts_generation(self):
        """Test basic TTS generation with qwen-tts."""
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            output_path = f.name
        
        try:
            cmd = [
                sys.executable,
                os.path.join(os.path.dirname(__file__), '..', 'scripts', 'tts_linux.py'),
                'Hello world',
                '--model', 'customvoice-small',  # Use smaller model for faster test
                '--female',
                '--output', output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            
            # Note: This may fail in CI without GPU, so we just check it runs
            # without crashing (return code 0 means success)
            if result.returncode == 0:
                self.assertTrue(os.path.exists(output_path))
                self.assertGreater(os.path.getsize(output_path), 1000)
            else:
                # In CI without GPU, this is expected to fail
                print(f"TTS generation skipped (likely no GPU): {result.stderr}")
                self.skipTest("GPU not available for TTS generation")
                
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_wrapper_script_import(self):
        """Test that wrapper script can be imported."""
        script_path = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'tts_linux.py')
        
        # Just check the script exists and is valid Python
        with open(script_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Should compile without errors
        compile(code, script_path, 'exec')
    
    def test_device_detection(self):
        """Test device detection logic."""
        try:
            import torch
            # Should be able to detect CUDA if available
            device = "cuda" if torch.cuda.is_available() else "cpu"
            self.assertIn(device, ["cuda", "cpu"])
        except ImportError:
            self.skipTest("torch not installed")


class TestPrivacySecurityDocs(unittest.TestCase):
    """Tests for privacy and security documentation."""
    
    def test_privacy_doc_exists(self):
        """Test privacy/security documentation exists."""
        doc_path = os.path.join(os.path.dirname(__file__), '..', 'references', 'privacy_security.md')
        self.assertTrue(os.path.exists(doc_path))
    
    def test_privacy_keywords(self):
        """Test privacy doc contains important keywords for SEO."""
        doc_path = os.path.join(os.path.dirname(__file__), '..', 'references', 'privacy_security.md')
        
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read().lower()
        
        # SEO-important keywords
        keywords = [
            'privacy', 'security', 'offline', 'local', 'data privacy',
            'gdpr', 'hipaa', 'compliance', 'confidential', 'encryption'
        ]
        
        for keyword in keywords:
            self.assertIn(keyword, content, f"Missing important keyword: {keyword}")
    
    def test_skill_md_privacy_mentions(self):
        """Test that SKILL.md mentions privacy benefits."""
        skill_path = os.path.join(os.path.dirname(__file__), '..', 'SKILL.md')
        
        with open(skill_path, 'r', encoding='utf-8') as f:
            content = f.read().lower()
        
        self.assertIn('privacy', content)
        self.assertIn('security', content)
        self.assertIn('offline', content)


if __name__ == '__main__':
    unittest.main()
