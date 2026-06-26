"""Configuration loading module for Jira client."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for Jira connection settings."""

    def __init__(self):
        self.jira_base_url = os.getenv('JIRA_BASE_URL', '')
        self.jira_token = os.getenv('JIRA_TOKEN', '')

    def validate(self) -> bool:
        """Validate that required configuration is present."""
        if not self.jira_base_url:
            print("Error: JIRA_BASE_URL is not set")
            return False
        if not self.jira_token:
            print("Error: JIRA_TOKEN is not set")
            return False
        return True

    @property
    def api_base(self) -> str:
        """Get the base API URL."""
        return f"{self.jira_base_url}/rest/api/2"


# Global config instance
config = Config()
