"""
popular-web-designs — 54 production-quality design systems.

Usage:
    from popular_web_designs import get_template, list_templates
    from popular_web_designs.catalog import TEMPLATES
"""

from .catalog import TEMPLATES, get_template, list_templates, get_categories

__version__ = "1.2.0"
__all__ = ["TEMPLATES", "get_template", "list_templates", "get_categories"]
