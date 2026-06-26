"""
内容过滤模块

用于过滤电台内容中的结构标记，生成自然流畅的播报文本。
"""

import re


class ContentFilter:
    """
    内容过滤器
    
    过滤掉电台内容中的结构标记，使其更适合TTS播报。
    """
    
    # 需要过滤的标记模式
    MARKER_PATTERNS = [
        (r'【开场】\n?', ''),           # 【开场】标记
        (r'【结尾】\n?', ''),           # 【结尾】标记
        (r'【主体内容】\n?', ''),       # 【主体内容】标记
        (r'【新闻\d+】', ''),           # 【新闻1】【新闻2】等标记
        (r'【标题】', ''),              # 【标题】标记
        (r'【摘要】', ''),              # 【摘要】标记
        (r'^【(.+?)】\n?', r'\1\n'),   # 其他【xxx】标记，保留内容去除括号
    ]
    
    @staticmethod
    def filter_markers(text: str) -> str:
        """
        过滤内容中的结构标记
        
        Args:
            text: 原始文本
            
        Returns:
            str: 过滤后的自然文本
        """
        filtered_text = text
        
        # 应用所有过滤规则
        for pattern, replacement in ContentFilter.MARKER_PATTERNS:
            filtered_text = re.sub(pattern, replacement, filtered_text, flags=re.MULTILINE)
        
        # 清理多余空行
        filtered_text = re.sub(r'\n{3,}', '\n\n', filtered_text)
        
        # 清理行首行尾空白
        filtered_text = filtered_text.strip()
        
        return filtered_text
    
    @staticmethod
    def filter_for_tts(text: str) -> str:
        """
        为TTS合成过滤内容
        
        除了过滤标记外，还会优化文本使其更适合语音合成。
        
        Args:
            text: 原始文本
            
        Returns:
            str: 优化后的TTS文本
        """
        # 先过滤标记
        tts_text = ContentFilter.filter_markers(text)
        
        # 替换不适合TTS的字符
        tts_text = tts_text.replace('【', '').replace('】', '')
        
        # 优化标点（确保停顿自然）
        tts_text = re.sub(r'([。！？])\n', r'\1\n\n', tts_text)
        
        return tts_text
    
    @staticmethod
    def naturalize_segment_title(title: str) -> str:
        """
        将新闻标题自然化
        
        例如：【新闻1】技术突破 -> 第一条新闻：技术突破
        
        Args:
            title: 原始标题
            
        Returns:
            str: 自然化标题
        """
        # 移除【新闻x】标记
        title = re.sub(r'【新闻\d+】', '', title)
        
        # 清理空白
        title = title.strip()
        
        return title


# 便捷函数
def filter_content(text: str) -> str:
    """过滤内容标记"""
    return ContentFilter.filter_markers(text)


def filter_for_tts(text: str) -> str:
    """为TTS过滤内容"""
    return ContentFilter.filter_for_tts(text)
