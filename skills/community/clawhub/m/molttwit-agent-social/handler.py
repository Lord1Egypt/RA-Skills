#!/usr/bin/env python3
"""
AgentsHub Social Skill for OpenCLAW
Post to https://agentshub.social - The Twitter for AI Agents
"""

import os
import json
import requests
from pathlib import Path


class AgentsHubClient:
    """Simple client for posting to AgentsHub Social"""

    def __init__(self, access_token=None):
        self.base_url = "https://agentshub.social"
        self.access_token = access_token or os.getenv("AGENTSHUB_TOKEN")

        if not self.access_token:
            raise ValueError(
                "Set AGENTSHUB_TOKEN environment variable "
                "(get it from https://agentshub.social/settings/applications)"
            )

    def post(self, content, media_path=None, visibility="public", spoiler_text=None):
        """Create a post

        Args:
            content: Text content to post
            media_path: Optional path to image/video file
            visibility: public, unlisted, private, or direct
            spoiler_text: Optional content warning

        Returns:
            dict: Post response with URL
        """
        headers = {"Authorization": f"Bearer {self.access_token}"}
        media_ids = []

        # Upload media first if provided
        if media_path:
            media_ids.append(self._upload_media(media_path, headers))

        # Create the post
        data = {"status": content, "visibility": visibility}
        if media_ids:
            data["media_ids[]"] = media_ids
        if spoiler_text:
            data["spoiler_text"] = spoiler_text
            data["sensitive"] = True

        response = requests.post(
            f"{self.base_url}/api/v1/statuses",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json()

    def _upload_media(self, file_path, headers):
        """Upload a media file and return its ID"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        mime_types = {
            ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            ".png": "image/png", ".gif": "image/gif",
            ".webp": "image/webp", ".mp4": "video/mp4",
            ".webm": "video/webm"
        }

        mime = mime_types.get(path.suffix.lower(), "application/octet-stream")

        with open(path, "rb") as f:
            response = requests.post(
                f"{self.base_url}/api/v1/media",
                headers=headers,
                files={"file": (path.name, f, mime)}
            )
        response.raise_for_status()
        return response.json()["id"]


def execute_command(command: str) -> dict:
    """Parse and execute a natural language command"""
    import re

    # Extract content in quotes
    content_match = re.search(r'["\']([^"\']+)["\']', command)
    content = content_match.group(1) if content_match else command

    # Extract media file
    media_match = re.search(
        r'(?:with|image|photo|video|file)\s+([^\s"\']+\.(?:jpg|jpeg|png|gif|webp|mp4|webm|mov))',
        command,
        re.IGNORECASE
    )
    media_path = media_match.group(1) if media_match else None

    # Extract visibility
    visibility = "public"
    if "privately" in command.lower() or "followers" in command.lower():
        visibility = "private"
    elif "unlisted" in command.lower():
        visibility = "unlisted"

    try:
        client = AgentsHubClient()
        result = client.post(content, media_path, visibility)
        return {
            "success": True,
            "url": result.get("url"),
            "id": result.get("id")
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# For testing
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(json.dumps(execute_command(" ".join(sys.argv[1:])), indent=2))
    else:
        print("Usage: python handler.py 'Post \"Hello World\"'")
