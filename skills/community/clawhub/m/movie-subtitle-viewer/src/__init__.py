"""
Movie Subtitle Viewer for OpenClaw
让 AI 通过字幕「看」电影
"""

from .subtitle_client import SubtitleClient
from .subtitle_parser import parse_subtitle, parse_subtitle_with_time

__all__ = ['SubtitleClient', 'parse_subtitle', 'parse_subtitle_with_time']
