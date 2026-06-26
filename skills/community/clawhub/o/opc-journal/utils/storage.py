"""Unified storage utilities for OPC Journal."""

import os
import re
import shutil
from typing import Dict, List, Any, Optional

from utils.timezone import now_tz


def _sanitize_customer_id(customer_id: str) -> str:
    """Sanitize customer_id to prevent path traversal."""
    # Remove any path separators and parent directory references
    sanitized = re.sub(r'[\\/]', '', customer_id)
    sanitized = sanitized.replace('..', '')
    # Ensure it's not empty after sanitization
    if not sanitized:
        sanitized = "default"
    return sanitized


def build_memory_path(customer_id: str, date: str = None) -> str:
    """Build standard memory file path using dd-mm-yy format."""
    customer_id = _sanitize_customer_id(customer_id)
    if date is None:
        date = now_tz().strftime("%d-%m-%y")
    return f"~/.openclaw/customers/{customer_id}/memory/{date}.md"


def build_customer_dir(customer_id: str) -> str:
    """Build customer base directory path."""
    customer_id = _sanitize_customer_id(customer_id)
    return f"~/.openclaw/customers/{customer_id}"


def _backup_if_exists(full_path: str) -> bool:
    """Create a .bak copy of the file if it exists."""
    if os.path.exists(full_path) and os.path.getsize(full_path) > 0:
        bak_path = full_path + ".bak"
        try:
            shutil.copy2(full_path, bak_path)
            return True
        except Exception:
            return False
    return False


def write_memory_file(path: str, content: str, mode: str = "a") -> Dict[str, Any]:
    """Write content to memory file. Creates daily .bak backup if file exists."""
    try:
        full_path = os.path.expanduser(path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Backup original file before mutation
        if mode in ("a", "w"):
            _backup_if_exists(full_path)
        
        with open(full_path, mode) as f:
            if mode == "a" and f.tell() > 0:
                f.write("\n\n")
            f.write(content)
        return {
            "success": True,
            "path": full_path,
            "bytes_written": len(content.encode("utf-8"))
        }
    except Exception as e:
        return {"success": False, "error": str(e), "error_type": "storage_error"}


def read_memory_file(path: str) -> Dict[str, Any]:
    """Read content from memory file."""
    try:
        full_path = os.path.expanduser(path)
        if not os.path.exists(full_path):
            return {
                "success": False,
                "error": f"File not found: {path}",
                "error_type": "file_not_found"
            }
        with open(full_path, "r") as f:
            content = f.read()
        return {"success": True, "content": content, "path": full_path}
    except Exception as e:
        return {"success": False, "error": str(e), "error_type": "storage_error"}


def create_tool_call(tool: str, params: dict, sequence: int = 1) -> dict:
    """Create standardized tool call."""
    return {"tool": tool, "params": params, "sequence": sequence}


def format_result(status: str, result: Any, message: str) -> dict:
    """Format standardized result."""
    return {
        "status": status,
        "result": result,
        "message": message,
        "_schema_version": "1.0"
    }
