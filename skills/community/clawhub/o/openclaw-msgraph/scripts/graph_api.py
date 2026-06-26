"""
Shared Microsoft Graph API utilities.

Provides HTTP methods for Graph API communication with auth token management.
"""

import sys
import json
import urllib.request
import urllib.error
import urllib.parse
from typing import Any, Dict, Optional

import auth

GRAPH_BASE = "https://graph.microsoft.com/v1.0"


def graph_get(path: str, params: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    GET request to Graph API.
    
    Args:
        path: API endpoint path (e.g., "/me/messages")
        params: Optional query parameters
        
    Returns:
        Parsed JSON response
    """
    token = auth.get_access_token()
    url = GRAPH_BASE + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"ERROR {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def graph_post(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    POST request to Graph API.
    
    Args:
        path: API endpoint path
        payload: Request body as dict
        
    Returns:
        Parsed JSON response, or empty dict if no content
    """
    token = auth.get_access_token()
    url = GRAPH_BASE + path
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, method="POST", headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read()
            return json.loads(content) if content else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"ERROR {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def graph_patch(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    PATCH request to Graph API.
    
    Args:
        path: API endpoint path
        payload: Request body as dict
        
    Returns:
        Parsed JSON response, or empty dict if no content
    """
    token = auth.get_access_token()
    url = GRAPH_BASE + path
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, method="PATCH", headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read()
            return json.loads(content) if content else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"ERROR {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


def graph_delete(path: str) -> None:
    """
    DELETE request to Graph API.
    
    Args:
        path: API endpoint path
    """
    token = auth.get_access_token()
    url = GRAPH_BASE + path
    req = urllib.request.Request(url, method="DELETE",
                                  headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req) as resp:
            pass  # 204 No Content on success
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"ERROR {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
