#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iFlow Template Toolkit

A simple, dependency-free template and internationalization toolkit for iFlow skills.

Features:
- Template engine with variable substitution, conditionals, and loops
- Internationalization (i18n) support with multiple languages
- Zero external dependencies
"""

from .template_engine import TemplateEngine, render_template
from .i18n.translator import Translator, t, init_translator, COMMON

__version__ = '1.0.0'
__all__ = [
    'TemplateEngine',
    'render_template',
    'Translator',
    't',
    'init_translator',
    'COMMON',
]
