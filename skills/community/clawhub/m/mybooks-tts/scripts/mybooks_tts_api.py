#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mybooks_tts_api.py — MyBooks MiMo TTS REST API Client

Usage:
    python3 mybooks_tts_api.py <tool-name> '<json-args>'

Environment Variables:
    MYBOOKS_HOST         Server URL with port (e.g., http://192.168.1.2:8082)
    MYBOOKS_USER         Login username (must be admin)
    MYBOOKS_PASSWORD     Login password
    MYBOOKS_SSL_VERIFY   Set to "false" to skip SSL certificate verification (self-signed certs)

Authentication:
    Automatically signs in via /api/user/sign_in before each tool invocation.
    Session cookies (user_id, lt) are maintained throughout the script lifecycle.
    If err=user.need_login is received, the script re-authenticates once and retries.
    All TTS endpoints require admin permission.

API Prefix:
    /api/toolbox/mimo_tts/
"""

import json
import os
import sys
import base64
import urllib.parse
import urllib3
from typing import Any, Dict

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# ============================================================================
# Constants
# ============================================================================

REQUIRED_ENV_VARS = ["MYBOOKS_HOST", "MYBOOKS_USER", "MYBOOKS_PASSWORD"]

API_PREFIX = "/api/toolbox/mimo_tts"

ERROR_MESSAGES = {
    "env_missing": {
        "status": "error",
        "message": (
            "MYBOOKS_HOST is not set. Please configure MYBOOKS_HOST "
            "(e.g. http://192.168.31.102:8082), MYBOOKS_USER and MYBOOKS_PASSWORD."
        ),
    },
    "auth_missing": {
        "status": "error",
        "message": "MYBOOKS_USER or MYBOOKS_PASSWORD is not set. Authentication is required.",
    },
}

AVAILABLE_TOOLS = [
    "tts_save_config",
    "tts_test_connection",
    "tts_convert",
    "tts_progress",
    "tts_clone_upload",
    "tts_clone_list",
    "tts_clone_delete",
    "tts_clone_audio",
    "tts_prompt_list",
    "tts_prompt_save",
    "tts_prompt_delete",
]


# ============================================================================
# MyBooksTTSAPI Class
# ============================================================================

class MyBooksTTSAPI:
    """Main API client for MyBooks MiMo TTS REST API."""

    def __init__(self, host: str, username: str, password: str):
        """
        Initialize MyBooks TTS API client.

        Args:
            host: Server URL with port (e.g., http://127.0.0.1:8082)
            username: Login username (must be admin)
            password: Login password
        """
        self.host = host.rstrip('/')
        self.username = username
        self.password = password
        self.session_cookies = {}

        # Try importing requests
        try:
            import requests
            self.requests = requests
            self.verify_ssl = os.environ.get("MYBOOKS_SSL_VERIFY", "true").lower() in ("true", "1", "yes")
        except ImportError:
            self._print_error(
                "Python 'requests' library is required. Install with: pip3 install requests"
            )
            sys.exit(1)

    def _print_error(self, message: str) -> None:
        """Print error to stderr."""
        print(json.dumps({"status": "error", "message": message}), file=sys.stderr)

    def sign_in(self) -> None:
        """Authenticate with the server and store session cookies."""
        url = f"{self.host}/api/user/sign_in"
        data = f"username={self.username}&password={self.password}"

        try:
            resp = self.requests.post(
                url,
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=30,
                verify=self.verify_ssl
            )
            resp.raise_for_status()
            result = resp.json()

            if result.get("err") != "ok":
                self._print_error(f"Login failed: {json.dumps(result)}")
                sys.exit(1)

            self.session_cookies.update(resp.cookies.get_dict())

        except Exception as e:
            self._print_error(f"Login failed: {str(e)}")
            sys.exit(1)

    def _call_api(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        """
        Internal method to call API endpoints.

        Args:
            method: HTTP method (GET, POST, etc.)
            path: API path (e.g., /api/toolbox/mimo_tts/progress)
            **kwargs: Additional arguments for requests (data, json, files, etc.)

        Returns:
            Parsed JSON response
        """
        url = f"{self.host}{path}"
        kwargs.setdefault('cookies', self.session_cookies)
        kwargs.setdefault('timeout', 30)
        kwargs.setdefault('verify', self.verify_ssl)

        try:
            resp = self.requests.request(method, url, **kwargs)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _call_with_auto_relogin(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        """
        Call API and automatically re-authenticate if session expired.

        Args:
            method: HTTP method
            path: API path
            **kwargs: Additional arguments for requests

        Returns:
            Parsed JSON response
        """
        result = self._call_api(method, path, **kwargs)

        if result.get("err") == "user.need_login":
            self.sign_in()
            result = self._call_api(method, path, **kwargs)

        return result

    # ========================================================================
    # Tool Methods
    # ========================================================================

    def tts_save_config(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save TTS API configuration (encrypted server-side).

        Args:
            api_url (str, required): API endpoint URL
            model_name (str, required): Model ID (e.g., mimo-v2.5-tts)
            api_type (str, required): chat_completions / audio_speech / custom
            api_key (str, required): API key
            auth_type (str, optional): bearer / basic / custom (default: bearer)
            voice_name (str, optional): Preset voice ID or audio_speech voice
            voice_desc (str, optional): Custom voice description
            clone_voice (str, optional): Clone voice name
        """
        required = ["api_url", "model_name", "api_type", "api_key"]
        for field in required:
            if not args.get(field):
                return {"status": "error", "message": f"{field} is required"}

        body = {k: v for k, v in args.items() if v is not None}
        return self._call_with_auto_relogin(
            "POST",
            f"{API_PREFIX}/config",
            json=body,
        )

    def tts_test_connection(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Test API connection using saved configuration.

        Args: none
        """
        return self._call_with_auto_relogin("POST", f"{API_PREFIX}/test")

    def tts_convert(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Start EPUB-to-audiobook conversion (async background task).

        Args:
            book_id (int, required): Book ID
            api_url (str, required): API endpoint URL
            model_name (str, required): Model ID
            api_type (str, required): chat_completions / audio_speech / custom
            api_key (str, required): API key
            auth_type (str, optional): bearer / basic / custom
            voice_name (str, optional): Preset voice ID or audio_speech voice
            voice_desc (str, optional): Custom voice description
            clone_voice (str, optional): Clone voice name
        """
        required = ["book_id", "api_url", "model_name", "api_type", "api_key"]
        for field in required:
            if not args.get(field):
                return {"status": "error", "message": f"{field} is required"}

        body = {k: v for k, v in args.items() if v is not None}
        return self._call_with_auto_relogin(
            "POST",
            f"{API_PREFIX}/convert",
            json=body,
        )

    def tts_progress(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Query current TTS conversion progress.

        Args: none
        """
        return self._call_with_auto_relogin("GET", f"{API_PREFIX}/progress")

    def tts_clone_upload(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Upload a clone voice sample (MP3/WAV, <=7MB).

        Args:
            voice_name (str, required): Clone voice name
            file_path (str, required): Absolute path to local audio file
        """
        voice_name = args.get("voice_name", "")
        file_path = args.get("file_path", "")

        if not voice_name:
            return {"status": "error", "message": "voice_name is required"}
        if not file_path:
            return {"status": "error", "message": "file_path is required"}

        if not os.path.isfile(file_path):
            return {"status": "error", "message": f"File not found: {file_path}"}

        # Validate format
        ext = os.path.splitext(file_path)[1].lower().lstrip('.')
        if ext not in ('mp3', 'wav'):
            return {"status": "error", "message": "Only MP3 and WAV formats are supported"}

        # Validate size (7MB limit)
        file_size = os.path.getsize(file_path)
        if file_size > 7 * 1024 * 1024:
            return {"status": "error", "message": f"File too large: {file_size} bytes (max 7MB)"}

        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                data = {'voice_name': voice_name}
                return self._call_with_auto_relogin(
                    "POST",
                    f"{API_PREFIX}/clone/upload",
                    data=data,
                    files=files,
                )
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def tts_clone_list(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        List all uploaded clone voices.

        Args: none
        """
        return self._call_with_auto_relogin("GET", f"{API_PREFIX}/clone/list")

    def tts_clone_delete(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Delete a clone voice by name.

        Args:
            voice_name (str, required): Clone voice name to delete
        """
        voice_name = args.get("voice_name", "")
        if not voice_name:
            return {"status": "error", "message": "voice_name is required"}

        return self._call_with_auto_relogin(
            "POST",
            f"{API_PREFIX}/clone/delete",
            json={"voice_name": voice_name},
        )

    def tts_clone_audio(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Download/preview a clone voice audio file (binary WAV).

        Args:
            voice_name (str, required): Clone voice name
            save_to (str, optional): Local path to save the audio;
                                     if omitted, returns base64-encoded audio
        """
        voice_name = args.get("voice_name", "")
        if not voice_name:
            return {"status": "error", "message": "voice_name is required"}

        save_to = args.get("save_to", "")
        query = urllib.parse.urlencode({"voice_name": voice_name})

        url = f"{self.host}{API_PREFIX}/clone/audio?{query}"
        kwargs = {
            'cookies': self.session_cookies,
            'timeout': 60,
            'verify': self.verify_ssl,
        }

        try:
            resp = self.requests.get(url, **kwargs)

            # Check for auth redirect
            try:
                ct = resp.headers.get('Content-Type', '')
                if 'json' in ct:
                    result = resp.json()
                    if result.get("err") == "user.need_login":
                        self.sign_in()
                        kwargs['cookies'] = self.session_cookies
                        resp = self.requests.get(url, **kwargs)
                        ct = resp.headers.get('Content-Type', '')
                        if 'json' in ct:
                            return resp.json()
            except Exception:
                pass

            content = resp.content

            if save_to:
                with open(save_to, 'wb') as f:
                    f.write(content)
                return {
                    "err": "ok",
                    "msg": "Audio saved",
                    "path": save_to,
                    "size": len(content),
                }
            else:
                # Return base64 for small files
                b64 = base64.b64encode(content).decode('ascii')
                return {
                    "err": "ok",
                    "msg": "Audio retrieved",
                    "voice_name": voice_name,
                    "size": len(content),
                    "base64": b64,
                }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def tts_prompt_list(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        List all saved voice prompt descriptions.

        Args: none
        """
        return self._call_with_auto_relogin("GET", f"{API_PREFIX}/prompt/list")

    def tts_prompt_save(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save a voice prompt description (same name overwrites).

        Args:
            name (str, required): Prompt name
            desc (str, required): Voice description text
        """
        name = args.get("name", "")
        desc = args.get("desc", "")

        if not name:
            return {"status": "error", "message": "name is required"}
        if not desc:
            return {"status": "error", "message": "desc is required"}

        return self._call_with_auto_relogin(
            "POST",
            f"{API_PREFIX}/prompt/save",
            json={"name": name, "desc": desc},
        )

    def tts_prompt_delete(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Delete a voice prompt by name.

        Args:
            name (str, required): Prompt name to delete
        """
        name = args.get("name", "")
        if not name:
            return {"status": "error", "message": "name is required"}

        return self._call_with_auto_relogin(
            "POST",
            f"{API_PREFIX}/prompt/delete",
            json={"name": name},
        )

    # ========================================================================
    # Tool Dispatcher
    # ========================================================================

    def execute_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool by name.

        Args:
            tool_name: Name of the tool to execute
            args: Tool arguments as dict

        Returns:
            Tool execution result
        """
        tool_method = getattr(self, tool_name, None)

        if tool_method is None or not callable(tool_method):
            return {
                "status": "error",
                "message": (
                    f"Unknown tool: {tool_name}. "
                    f"Available tools: {', '.join(AVAILABLE_TOOLS)}"
                ),
            }

        return tool_method(args)


# ============================================================================
# CLI Entry Point
# ============================================================================

def main():
    """Command-line entry point."""
    if len(sys.argv) < 2:
        print(json.dumps({
            "status": "error",
            "message": "Usage: mybooks_tts_api.py <tool-name> '<json-args>'",
        }), file=sys.stderr)
        sys.exit(1)

    tool_name = sys.argv[1]
    args_json = sys.argv[2] if len(sys.argv) > 2 else "{}"

    # Parse arguments
    try:
        args = json.loads(args_json)
    except json.JSONDecodeError as e:
        print(json.dumps({
            "status": "error",
            "message": f"Invalid JSON arguments: {str(e)}",
        }), file=sys.stderr)
        sys.exit(1)

    # Check environment variables
    host = os.environ.get("MYBOOKS_HOST", "")
    username = os.environ.get("MYBOOKS_USER", "")
    password = os.environ.get("MYBOOKS_PASSWORD", "")

    if not host:
        print(json.dumps(ERROR_MESSAGES["env_missing"]), file=sys.stderr)
        sys.exit(1)

    if not username or not password:
        print(json.dumps(ERROR_MESSAGES["auth_missing"]), file=sys.stderr)
        sys.exit(1)

    # Create API client and execute
    api = MyBooksTTSAPI(host, username, password)
    api.sign_in()
    result = api.execute_tool(tool_name, args)

    # Output result
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
