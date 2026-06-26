"""
Office Pro - Enterprise Document Automation Suite

Enterprise-grade Word and Excel document automation tool.
Now with simplified API for AI Agents.

Quick Start:
    >>> from office_pro import generate_contract
    >>> generate_contract('parking_lease', 
    ...                   party_a='张三',
    ...                   party_b='李四',
    ...                   location='XX小区地下停车场',
    ...                   monthly_rent=500)

Features:
    - One-click document generation with built-in templates
    - Complete contract templates (10 types)
    - Excel templates (6 types)
    - Report templates
    - No external template files required
    - Graceful degradation without optional dependencies
"""

from simple_api import (
    QuickGenerator,
    generate_contract,
    generate_report,
    generate_excel,
    list_templates,
    num_to_chinese,
    ExcelChartBuilder,
    WordStyleBuilder,
    create_chart,
    create_styled_document,
)

__version__ = '1.2.0'

__all__ = [
    'QuickGenerator',
    'generate_contract',
    'generate_report',
    'generate_excel',
    'list_templates',
    'num_to_chinese',
    'ExcelChartBuilder',
    'WordStyleBuilder',
    'create_chart',
    'create_styled_document',
]


class OfficeProError(Exception):
    """Base exception for Office Pro"""
    pass


class DependencyError(OfficeProError):
    """Dependency missing error"""
    pass


def check_dependencies():
    """
    Check available dependencies and return status.
    
    Returns:
        dict: Dependency status
    """
    deps = {
        'python-docx': False,
        'openpyxl': False,
        'pandas': False,
    }
    
    try:
        import docx
        deps['python-docx'] = True
    except ImportError:
        pass
    
    try:
        import openpyxl
        deps['openpyxl'] = True
    except ImportError:
        pass
    
    try:
        import pandas
        deps['pandas'] = True
    except ImportError:
        pass
    
    return deps


def get_version_info():
    """
    Get version and dependency information.
    
    Returns:
        dict: Version and dependency info
    """
    return {
        'version': __version__,
        'dependencies': check_dependencies(),
    }
