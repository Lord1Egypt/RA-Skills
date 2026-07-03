from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def check_version_tool(
    dependency: str,
    version: str,
    packaging: Optional[str] = "jar",
    classifier: Optional[null] = None
) -> Dict[str, Any]:
    """
    Check a Maven version and get all version update information in a single call
    
    Args:
        dependency: null
        version: null
        packaging: null
        classifier: null
    
    Returns:
        
    """
    arguments = {
        "dependency": dependency,
        "version": version,
        "packaging": packaging,
        "classifier": classifier
    }
    
    return call_api("1777419077234691", "check_version_tool", arguments)

def check_version_batch_tool(
    dependencies: null
) -> Dict[str, Any]:
    """
    Process multiple Maven dependency version checks in a single batch request
    
    Args:
        dependencies: null
    
    Returns:
        
    """
    arguments = {
        "dependencies": dependencies
    }
    
    return call_api("1777419077234691", "check_version_batch_tool", arguments)

def list_available_versions_tool(
    dependency: str,
    version: str,
    packaging: Optional[str] = "jar",
    classifier: Optional[null] = None,
    include_all_versions: Optional[bool] = False
) -> Dict[str, Any]:
    """
    List all available versions of a Maven artifact grouped by minor version tracks
    
    Args:
        dependency: null
        version: null
        packaging: null
        classifier: null
        include_all_versions: null
    
    Returns:
        
    """
    arguments = {
        "dependency": dependency,
        "version": version,
        "packaging": packaging,
        "classifier": classifier,
        "include_all_versions": include_all_versions
    }
    
    return call_api("1777419077234691", "list_available_versions_tool", arguments)

def scan_java_project_tool(
    workspace: str,
    include_profiles: Optional[null] = None,
    scan_all_modules: Optional[bool] = True,
    scan_mode: Optional[str] = "workspace",
    pom_file: Optional[null] = None,
    severity_filter: Optional[null] = None,
    max_results: Optional[int] = 100.0,
    offset: Optional[int] = 0.0
) -> Dict[str, Any]:
    """
    Java-specific tool for scanning Maven projects for vulnerabilities
    
    Args:
        workspace: null
        include_profiles: List of Maven profiles to activate
        scan_all_modules: null
        scan_mode: null
        pom_file: null
        severity_filter: List of severity levels to include (CRITICAL, HIGH, MEDIUM, LOW)
        max_results: null
        offset: null
    
    Returns:
        
    """
    arguments = {
        "workspace": workspace,
        "include_profiles": include_profiles,
        "scan_all_modules": scan_all_modules,
        "scan_mode": scan_mode,
        "pom_file": pom_file,
        "severity_filter": severity_filter,
        "max_results": max_results,
        "offset": offset
    }
    
    return call_api("1777419077234691", "scan_java_project_tool", arguments)

def analyze_pom_file_tool(
    pom_file_path: str,
    include_vulnerability_check: Optional[bool] = True
) -> Dict[str, Any]:
    """
    Analyze a single Maven POM file without scanning the entire workspace
    
    Args:
        pom_file_path: null
        include_vulnerability_check: null
    
    Returns:
        
    """
    arguments = {
        "pom_file_path": pom_file_path,
        "include_vulnerability_check": include_vulnerability_check
    }
    
    return call_api("1777419077234691", "analyze_pom_file_tool", arguments)

