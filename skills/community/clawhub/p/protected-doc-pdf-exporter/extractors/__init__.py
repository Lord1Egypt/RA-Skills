"""
Protected Document Extractors Suite
"""
from .base import BaseExtractor
from .wecom_weboffice import WeComWebofficeExtractor
from .dom_stepper import DOMStepperExtractor
from .tencent_docs import TencentDocsExtractor
from .feishu_extractor import FeishuExtractor

__all__ = [
    'BaseExtractor',
    'WeComWebofficeExtractor',
    'TencentDocsExtractor',
    'FeishuExtractor',
    'DOMStepperExtractor'
]
