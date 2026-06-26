#!/usr/bin/env python3
"""
Package Version Tracker
查询 npm/pypi 包版本信息
"""

import json
import sys
import urllib.request
import urllib.error
from datetime import datetime
from typing import Optional, Dict, Any, List


def fetch_npm_package(package_name: str) -> Dict[str, Any]:
    """查询 npm 包信息"""
    url = f"https://registry.npmjs.org/{package_name}/latest"
    
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            return {
                "success": True,
                "name": data.get("name"),
                "version": data.get("version"),
                "description": data.get("description", ""),
                "license": data.get("license", ""),
                "homepage": data.get("homepage", ""),
                "repository": data.get("repository", {}).get("url", ""),
            }
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"success": False, "error": f"Package '{package_name}' not found on npm"}
        return {"success": False, "error": f"HTTP Error: {e.code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def fetch_npm_versions(package_name: str) -> List[Dict[str, str]]:
    """查询 npm 包所有版本"""
    url = f"https://registry.npmjs.org/{package_name}"
    
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            versions = data.get("versions", {})
            version_list = []
            for v in list(versions.keys())[-5:]:  # 最近5个版本
                time_data = data.get("time", {})
                version_list.append({
                    "version": v,
                    "time": time_data.get(v, "N/A")
                })
            return version_list
    except Exception:
        return []


def fetch_pypi_package(package_name: str) -> Dict[str, Any]:
    """查询 PyPI 包信息"""
    url = f"https://pypi.org/pypi/{package_name}/json"
    
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            info = data.get("info", {})
            return {
                "success": True,
                "name": info.get("name"),
                "version": info.get("version"),
                "summary": info.get("summary", ""),
                "author": info.get("author", ""),
                "license": info.get("license", ""),
                "home_page": info.get("home_page", ""),
                "pypi_url": info.get("package_url", ""),
            }
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"success": False, "error": f"Package '{package_name}' not found on PyPI"}
        return {"success": False, "error": f"HTTP Error: {e.code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def fetch_pypi_versions(package_name: str) -> List[Dict[str, str]]:
    """查询 PyPI 包所有版本"""
    url = f"https://pypi.org/pypi/{package_name}/json"
    
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            releases = data.get("releases", {})
            version_list = []
            for v, infos in list(releases.items())[-5:]:  # 最近5个版本
                if infos:
                    version_list.append({
                        "version": v,
                        "time": infos[0].get("upload_time", "N/A")[:10] if infos else "N/A"
                    })
            return version_list
    except Exception:
        return []


def compare_versions(v1: str, v2: str) -> Dict[str, Any]:
    """比较两个版本号"""
    def parse_version(v: str) -> List[int]:
        parts = v.replace("-", ".").replace("_", ".").split(".")
        return [int(p) if p.isdigit() else 0 for p in parts[:3]]
    
    parts1 = parse_version(v1)
    parts2 = parse_version(v2)
    
    # 补齐长度
    max_len = max(len(parts1), len(parts2))
    parts1.extend([0] * (max_len - len(parts1)))
    parts2.extend([0] * (max_len - len(parts2)))
    
    if parts1 > parts2:
        result = f"v1 > v2 ({v1} > {v2})"
    elif parts1 < parts2:
        result = f"v1 < v2 ({v1} < {v2})"
    else:
        result = f"v1 = v2 ({v1} = {v2})"
    
    return {
        "version1": v1,
        "version2": v2,
        "result": result,
        "comparison": parts1[0] - parts2[0]
    }


def format_output(data: Dict[str, Any], package_type: str) -> str:
    """格式化输出"""
    if not data.get("success", False):
        return f"❌ {data.get('error', 'Unknown error')}"
    
    lines = []
    lines.append(f"📦 **{package_type.upper()} Package: {data.get('name', 'N/A')}**")
    lines.append(f"")
    lines.append(f"**Version:** `{data.get('version', 'N/A')}`")
    
    if package_type == "npm":
        if data.get("description"):
            lines.append(f"**Description:** {data.get('description')}")
        if data.get("license"):
            lines.append(f"**License:** {data.get('license')}")
    else:  # pypi
        if data.get("summary"):
            lines.append(f"**Summary:** {data.get('summary')}")
        if data.get("author"):
            lines.append(f"**Author:** {data.get('author')}")
    
    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    
    if not args:
        print("Usage:")
        print("  python package_version_tracker.py npm <package_name>")
        print("  python package_version_tracker.py pypi <package_name>")
        print("  python package_version_tracker.py compare <v1> <v2>")
        sys.exit(1)
    
    command = args[0].lower()
    
    if command == "npm":
        if len(args) < 2:
            print("Usage: python package_version_tracker.py npm <package_name>")
            sys.exit(1)
        package_name = args[1]
        result = fetch_npm_package(package_name)
        versions = fetch_npm_versions(package_name)
        
        output = format_output(result, "npm")
        
        if versions:
            output += "\n\n**Recent Versions:**\n"
            for v in reversed(versions):
                output += f"- `{v['version']}` ({v['time'][:10] if len(v['time']) >= 10 else v['time']})\n"
        
        print(output)
        
    elif command == "pypi":
        if len(args) < 2:
            print("Usage: python package_version_tracker.py pypi <package_name>")
            sys.exit(1)
        package_name = args[1]
        result = fetch_pypi_package(package_name)
        versions = fetch_pypi_versions(package_name)
        
        output = format_output(result, "pypi")
        
        if versions:
            output += "\n\n**Recent Versions:**\n"
            for v in reversed(versions):
                output += f"- `{v['version']}` ({v['time']})\n"
        
        print(output)
        
    elif command == "compare":
        if len(args) < 3:
            print("Usage: python package_version_tracker.py compare <v1> <v2>")
            sys.exit(1)
        result = compare_versions(args[1], args[2])
        print(f"🔢 Version Compare: {result['result']}")
        
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
