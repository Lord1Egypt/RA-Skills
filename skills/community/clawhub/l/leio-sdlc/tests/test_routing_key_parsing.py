import unittest
import os
import sys
import subprocess
from unittest.mock import patch, MagicMock

# Add scripts to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../scripts')))
from orchestrator import notify_channel

class TestNotificationParsing(unittest.TestCase):
    @patch('subprocess.run')
    def test_routing_key_parsing(self, mock_run):
        # Format: (input_key, expected_channel_arg, expected_target_arg)
        test_cases = [
            ("slack:channel:C12345", "slack", "channel:C12345"),
            ("channel:C67890", "channel", "C67890"),
            ("C112233", None, "C112233"),
            ("custom:provider:user:123", "custom", "provider:user:123"),
        ]
    
        with patch.dict(os.environ, {"SDLC_TEST_MODE": "false"}):
            for routing_key, expected_channel, expected_target in test_cases:
                mock_run.reset_mock()
                notify_channel(routing_key, "test message")
        
                # Extract the actual command passed to subprocess.run
                called_cmd = mock_run.call_args[0][0]

            if expected_channel:
                self.assertIn("--channel", called_cmd)
                self.assertEqual(called_cmd[called_cmd.index("--channel") + 1], expected_channel)
            else:
                self.assertNotIn("--channel", called_cmd)

            self.assertIn("-t", called_cmd)
            self.assertEqual(called_cmd[called_cmd.index("-t") + 1], expected_target)
            self.assertIn("-m", called_cmd)
            # The actual message is prefixed with "🤖 [SDLC Engine] "
            self.assertTrue(any("test message" in arg for arg in called_cmd))

if __name__ == '__main__':
    unittest.main()
