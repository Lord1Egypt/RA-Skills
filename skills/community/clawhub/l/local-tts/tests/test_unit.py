#!/usr/bin/env python3
"""
Unit tests for local-tts scripts.

These tests verify that the TTS scripts can be imported and have correct structure.
For actual TTS generation tests, see test_integration.py
"""

import unittest
import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


class TestScriptImports(unittest.TestCase):
    """Test that scripts can be imported."""
    
    def test_tts_macos_imports(self):
        """Test that tts_macos.py is valid Python syntax."""
        script_path = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'tts_macos.py')
        with open(script_path, 'r', encoding='utf-8') as f:
            code = f.read()
        # Should compile without errors
        compile(code, script_path, 'exec')
    
    def test_tts_linux_imports(self):
        """Test that tts_linux.py is valid Python syntax."""
        script_path = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'tts_linux.py')
        with open(script_path, 'r', encoding='utf-8') as f:
            code = f.read()
        # Should compile without errors
        compile(code, script_path, 'exec')


class TestScriptStructure(unittest.TestCase):
    """Test script structure and constants."""
    
    def test_macos_models_defined(self):
        """Test that macOS script has models defined."""
        script_path = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'tts_macos.py')
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertIn('MODELS', content)
        self.assertIn('base', content)
        self.assertIn('customvoice', content)
        self.assertIn('voicedesign', content)
    
    def test_linux_models_defined(self):
        """Test that Linux script has models defined."""
        script_path = os.path.join(os.path.dirname(__file__), '..', 'scripts', 'tts_linux.py')
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertIn('MODELS', content)
        self.assertIn('base', content)
        self.assertIn('customvoice', content)
        self.assertIn('voicedesign', content)
    
    def test_default_voices_defined(self):
        """Test that default voices are defined."""
        for script in ['tts_macos.py', 'tts_linux.py']:
            script_path = os.path.join(os.path.dirname(__file__), '..', 'scripts', script)
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.assertIn('DEFAULT_FEMALE_VOICE', content)
            self.assertIn('DEFAULT_MALE_VOICE', content)
            self.assertIn('Chelsie', content)
            self.assertIn('Aiden', content)
    
    def test_argument_parsing(self):
        """Test that scripts have argument parsing."""
        for script in ['tts_macos.py', 'tts_linux.py']:
            script_path = os.path.join(os.path.dirname(__file__), '..', 'scripts', script)
            with open(script_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.assertIn('argparse', content)
            self.assertIn('text', content)  # 'text' argument (positional)
            self.assertIn('--voice', content)
            self.assertIn('--model', content)


class TestDocumentation(unittest.TestCase):
    """Test that documentation exists and is valid."""
    
    def test_skill_md_exists(self):
        """Test that SKILL.md exists."""
        skill_path = os.path.join(os.path.dirname(__file__), '..', 'SKILL.md')
        self.assertTrue(os.path.exists(skill_path))
    
    def test_skill_md_has_frontmatter(self):
        """Test that SKILL.md has YAML frontmatter."""
        skill_path = os.path.join(os.path.dirname(__file__), '..', 'SKILL.md')
        with open(skill_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertTrue(content.startswith('---'))
        self.assertIn('name:', content)
        self.assertIn('description:', content)
    
    def test_references_exist(self):
        """Test that reference files exist."""
        ref_dir = os.path.join(os.path.dirname(__file__), '..', 'references')
        self.assertTrue(os.path.exists(ref_dir))
        
        expected_files = [
            'macos_mlx_audio.md',
            'linux_windows_transformers.md',
            'privacy_security.md'
        ]
        
        for filename in expected_files:
            filepath = os.path.join(ref_dir, filename)
            self.assertTrue(os.path.exists(filepath), f"Missing reference file: {filename}")
    
    def test_privacy_security_content(self):
        """Test that privacy/security doc has required content."""
        doc_path = os.path.join(os.path.dirname(__file__), '..', 'references', 'privacy_security.md')
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertIn('privacy', content.lower())
        self.assertIn('security', content.lower())
        # Check for GDPR or compliance mention
        has_gdpr_or_compliance = 'GDPR' in content or 'compliance' in content.lower()
        self.assertTrue(has_gdpr_or_compliance, "Should mention GDPR or compliance")


class TestPackageJson(unittest.TestCase):
    """Test package.json metadata."""
    
    def test_package_json_exists(self):
        """Test that package.json exists."""
        json_path = os.path.join(os.path.dirname(__file__), '..', 'package.json')
        self.assertTrue(os.path.exists(json_path))
    
    def test_package_json_valid(self):
        """Test that package.json is valid JSON."""
        import json
        json_path = os.path.join(os.path.dirname(__file__), '..', 'package.json')
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.assertIn('name', data)
        self.assertIn('version', data)
        self.assertIn('description', data)
        self.assertEqual(data['name'], 'local-tts')
    
    def test_version_matches(self):
        """Test that VERSION file matches package.json."""
        import json
        
        json_path = os.path.join(os.path.dirname(__file__), '..', 'package.json')
        version_path = os.path.join(os.path.dirname(__file__), '..', 'VERSION')
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        with open(version_path, 'r', encoding='utf-8') as f:
            version = f.read().strip()
        
        self.assertEqual(data['version'], version)


class TestScriptsExecutable(unittest.TestCase):
    """Test that scripts are executable."""
    
    def test_scripts_executable(self):
        """Test that scripts have executable permissions (Unix only)."""
        if os.name == 'nt':  # Windows
            self.skipTest("Executable permissions not applicable on Windows")
        
        scripts_dir = os.path.join(os.path.dirname(__file__), '..', 'scripts')
        for script in ['tts_macos.py', 'tts_linux.py']:
            script_path = os.path.join(scripts_dir, script)
            if os.path.exists(script_path):
                self.assertTrue(os.access(script_path, os.X_OK),
                               f"{script} should be executable")


if __name__ == '__main__':
    unittest.main()
