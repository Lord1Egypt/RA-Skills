#!/usr/bin/env python3
"""Basic tests for mijia-fan skill"""
import os
import sys
import unittest

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestBasic(unittest.TestCase):
    def test_import(self):
        """Test that fan_cli can be imported"""
        try:
            import scripts.fan_cli as fan_cli
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import fan_cli: {e}")

    def test_environment_variables(self):
        """Test environment variable defaults"""
        # Save original
        orig_did = os.environ.get('MIJIA_FAN_DID')
        orig_siid = os.environ.get('MIJIA_FAN_SIID')
        
        # Clear and test defaults
        if 'MIJIA_FAN_DID' in os.environ:
            del os.environ['MIJIA_FAN_DID']
        if 'MIJIA_FAN_SIID' in os.environ:
            del os.environ['MIJIA_FAN_SIID']
        
        # Import fresh to test defaults
        import importlib
        import scripts.fan_cli as fan_cli
        importlib.reload(fan_cli)
        
        self.assertIsNone(fan_cli.DID)
        self.assertEqual(fan_cli.SIID, 2)
        
        # Restore
        if orig_did:
            os.environ['MIJIA_FAN_DID'] = orig_did
        if orig_siid:
            os.environ['MIJIA_FAN_SIID'] = orig_siid


if __name__ == '__main__':
    unittest.main()
