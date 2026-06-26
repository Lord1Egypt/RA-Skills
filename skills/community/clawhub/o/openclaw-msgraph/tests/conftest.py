"""Pytest configuration and shared fixtures."""

import sys
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))


@pytest.fixture
def mock_auth():
    """Mock auth module."""
    with patch("auth.get_access_token") as mock_token:
        mock_token.return_value = "test-token-12345"
        yield mock_token


@pytest.fixture
def sample_message():
    """Sample email message from Graph API."""
    return {
        "id": "msg-123",
        "subject": "Test Email",
        "from": {
            "emailAddress": {
                "name": "Sender",
                "address": "sender@example.com"
            }
        },
        "toRecipients": [
            {
                "emailAddress": {
                    "name": "Recipient",
                    "address": "recipient@example.com"
                }
            }
        ],
        "receivedDateTime": "2026-03-03T10:30:00.000Z",
        "isRead": False,
        "hasAttachments": True,
        "bodyPreview": "This is a test message",
        "body": {
            "contentType": "html",
            "content": "<html><body>This is a test message</body></html>"
        }
    }


@pytest.fixture
def sample_event():
    """Sample calendar event from Graph API."""
    return {
        "id": "event-456",
        "subject": "Team Sync",
        "start": {
            "dateTime": "2026-03-10T10:00:00",
            "timeZone": "America/New_York"
        },
        "end": {
            "dateTime": "2026-03-10T11:00:00",
            "timeZone": "America/New_York"
        },
        "location": {
            "displayName": "Conference Room A"
        },
        "organizer": {
            "emailAddress": {
                "name": "Organizer",
                "address": "organizer@example.com"
            }
        },
        "attendees": [
            {
                "emailAddress": {
                    "name": "Attendee 1",
                    "address": "attendee1@example.com"
                },
                "status": {
                    "response": "accepted"
                }
            }
        ],
        "isAllDay": False,
        "onlineMeetingUrl": "https://teams.microsoft.com/...",
        "isCancelled": False,
        "webLink": "https://outlook.office365.com/..."
    }


@pytest.fixture
def sample_folder():
    """Sample mail folder from Graph API."""
    return {
        "id": "folder-789",
        "displayName": "Archive",
        "totalItemCount": 42,
        "unreadItemCount": 5,
        "childFolders": []
    }
