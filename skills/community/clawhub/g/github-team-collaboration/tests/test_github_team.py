"""
Unit tests for GitHub Team Collaboration
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.github_team import (
    list_open_prs,
    assign_reviewers,
    get_milestone_progress,
    get_team_metrics,
    list_issues,
    create_issue,
    get_github_token
)


class TestGitHubTeam(unittest.TestCase):
    """Test cases for GitHub team collaboration functions"""
    
    @patch.dict(os.environ, {"GITHUB_TOKEN": "test_token_123"})
    def test_get_github_token(self):
        """Test token retrieval from environment"""
        token = get_github_token()
        self.assertEqual(token, "test_token_123")
    
    def test_get_github_token_missing(self):
        """Test error when token is missing"""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                get_github_token()
    
    @patch('scripts.github_team.requests.get')
    @patch.dict(os.environ, {"GITHUB_TOKEN": "test_token"})
    def test_list_open_prs_success(self, mock_get):
        """Test listing open PRs"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"number": 1, "title": "Test PR", "state": "open"}
        ]
        mock_get.return_value = mock_response
        
        result = list_open_prs("octocat", "Hello-World")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "Test PR")
    
    @patch('scripts.github_team.requests.get')
    @patch.dict(os.environ, {"GITHUB_TOKEN": "test_token"})
    def test_list_open_prs_error(self, mock_get):
        """Test error handling in list_open_prs"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_get.return_value = mock_response
        
        result = list_open_prs("octocat", "nonexistent")
        self.assertIn("error", result[0])
    
    @patch('scripts.github_team.requests.get')
    @patch.dict(os.environ, {"GITHUB_TOKEN": "test_token"})
    def test_get_milestone_progress(self, mock_get):
        """Test milestone progress calculation"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                "title": "Sprint-1",
                "state": "open",
                "open_issues": 5,
                "closed_issues": 15,
                "due_on": None,
                "html_url": "https://github.com/test/milestone/1"
            }
        ]
        mock_get.return_value = mock_response
        
        result = get_milestone_progress("octocat", "Hello-World", "Sprint-1")
        self.assertEqual(result["title"], "Sprint-1")
        self.assertEqual(result["total_issues"], 20)
        self.assertEqual(result["progress_percent"], 75.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
