#!/usr/bin/env python3
"""
Job Status Query Skill Test Script
"""

import sys
import os
import json
import unittest
from unittest.mock import patch, Mock
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.get_job_status import JobStatusFetcher


class TestJobStatusFetcher(unittest.TestCase):
    """Test job status fetcher"""
    
    def setUp(self):
        self.fetcher = JobStatusFetcher(timeout=5)
    
    @patch('scripts.get_job_status.requests.Session.get')
    def test_get_job_status_success(self, mock_get):
        """Test successful job status retrieval"""
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "code": 0,
            "message": None,
            "data": {
                "id": 20452,
                "hpcId": "hpcai28",
                "jobId": "15000",
                "jobState": "COMPLETED",
                "endTime": "2024-12-09T09:30:10"
            }
        }
        mock_get.return_value = mock_response
        
        # Call method
        result = self.fetcher.get_job_status("15000")
        
        # Verify result
        self.assertTrue(result['success'])
        self.assertEqual(result['jobId'], "15000")
        self.assertEqual(result['status'], "COMPLETED")
        self.assertEqual(result['details']['jobState'], "COMPLETED")
        self.assertIn('Job completed successfully', result['message'])
    
    @patch('scripts.get_job_status.requests.Session.get')
    def test_get_job_status_running(self, mock_get):
        """Test get running job status"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "code": 0,
            "message": None,
            "data": {
                "id": 20453,
                "hpcId": "hpcai28",
                "jobId": "15001",
                "jobState": "RUNNING",
                "startTime": "2024-12-09T09:00:00"
            }
        }
        mock_get.return_value = mock_response
        
        result = self.fetcher.get_job_status("15001")
        
        self.assertTrue(result['success'])
        self.assertEqual(result['status'], "RUNNING")
        self.assertIn('Job is currently running', result['message'])
    
    @patch('scripts.get_job_status.requests.Session.get')
    def test_get_job_status_failed(self, mock_get):
        """Test get failed job status"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "code": 0,
            "message": None,
            "data": {
                "id": 20454,
                "hpcId": "hpcai28",
                "jobId": "15002",
                "jobState": "FAILED",
                "endTime": "2024-12-09T09:15:00",
                "exitCode": 1
            }
        }
        mock_get.return_value = mock_response
        
        result = self.fetcher.get_job_status("15002")
        
        self.assertTrue(result['success'])
        self.assertEqual(result['status'], "FAILED")
        self.assertIn('Job execution failed', result['message'])
    
    @patch('scripts.get_job_status.requests.Session.get')
    def test_job_not_found(self, mock_get):
        """Test job not found"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = Exception("404 Not Found")
        mock_get.return_value = mock_response
        
        result = self.fetcher.get_job_status("99999")
        
        self.assertFalse(result['success'])
        self.assertEqual(result['jobId'], "99999")
        self.assertIn('Job not found', result['error'])
    
    @patch('scripts.get_job_status.requests.Session.get')
    def test_api_error_code(self, mock_get):
        """Test API returning error code"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "code": 1,
            "message": "Job query failed",
            "data": None
        }
        mock_get.return_value = mock_response
        
        result = self.fetcher.get_job_status("15000")
        
        self.assertFalse(result['success'])
        self.assertIn('API error', result['error'])
    
    @patch('scripts.get_job_status.requests.Session.get')
    def test_missing_job_state(self, mock_get):
        """Test missing jobState field"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "code": 0,
            "message": None,
            "data": {
                "id": 20452,
                "hpcId": "hpcai28",
                "jobId": "15000"
                # Missing jobState field
            }
        }
        mock_get.return_value = mock_response
        
        result = self.fetcher.get_job_status("15000")
        
        self.assertFalse(result['success'])
        self.assertIn('Job state field not found', result['error'])
    
    @patch('scripts.get_job_status.requests.Session.get')
    def test_network_timeout(self, mock_get):
        """Test network timeout"""
        mock_get.side_effect = Exception("Timeout")
        
        result = self.fetcher.get_job_status("15000")
        
        self.assertFalse(result['success'])
        self.assertIn('Network connection failed', result['error'])
    
    def test_invalid_job_id_format(self):
        """Test invalid jobId format"""
        # Note: Current implementation doesn't validate format, but tool definition has restrictions
        # Here test skill handling of arbitrary strings
        with patch('scripts.get_job_status.requests.Session.get') as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "code": 0,
                "message": None,
                "data": {
                    "id": 20455,
                    "hpcId": "hpcai28",
                    "jobId": "abc123",
                    "jobState": "COMPLETED"
                }
            }
            mock_get.return_value = mock_response
            
            result = self.fetcher.get_job_status("abc123")
            
            self.assertTrue(result['success'])
            self.assertEqual(result['jobId'], "abc123")
            self.assertEqual(result['status'], "COMPLETED")


class TestCommandLineInterface(unittest.TestCase):
    """Test command line interface"""
    
    def test_help_command(self):
        """Test help command"""
        import subprocess
        result = subprocess.run(
            ['python', 'scripts/get_job_status.py', '--help'],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn('usage', result.stdout.lower())
    
    def test_missing_job_id(self):
        """Test missing jobId parameter"""
        import subprocess
        result = subprocess.run(
            ['python', 'scripts/get_job_status.py'],
            capture_output=True, text=True
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('error', result.stderr.lower())


class TestStatusMessages(unittest.TestCase):
    """Test status messages"""
    
    def setUp(self):
        self.fetcher = JobStatusFetcher()
    
    def test_status_messages(self):
        """Test various status messages"""
        test_cases = [
            ("PENDING", "Job is queued and waiting"),
            ("RUNNING", "Job is currently running"),
            ("COMPLETED", "Job completed successfully"),
            ("FAILED", "Job execution failed"),
            ("CANCELLED", "Job was cancelled"),
            ("TIMEOUT", "Job execution timed out"),
            ("SUSPENDED", "Job is suspended"),
            ("CONFIGURING", "Job is being configured"),
            ("UNKNOWN", "Job status: UNKNOWN")
        ]
        
        for status, expected_message in test_cases:
            message = self.fetcher._get_status_message(status)
            self.assertEqual(message, expected_message)


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestJobStatusFetcher))
    suite.addTests(loader.loadTestsFromTestCase(TestCommandLineInterface))
    suite.addTests(loader.loadTestsFromTestCase(TestStatusMessages))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return test result
    return result.wasSuccessful()


if __name__ == '__main__':
    print("Starting job status query skill tests...")
    print("=" * 60)
    
    success = run_tests()
    
    print("=" * 60)
    if success:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Tests failed!")
        sys.exit(1)