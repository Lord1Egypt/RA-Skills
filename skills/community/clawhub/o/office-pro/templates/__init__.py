"""
Office Pro - Templates Package

Built-in templates for contracts, reports, and other documents.
"""

from .contracts import CONTRACT_TEMPLATES
from .reports import REPORT_TEMPLATES
from .excel import EXCEL_TEMPLATES

__all__ = ['CONTRACT_TEMPLATES', 'REPORT_TEMPLATES', 'EXCEL_TEMPLATES']
