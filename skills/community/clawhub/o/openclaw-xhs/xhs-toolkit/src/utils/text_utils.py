"""
小红书工具包文本处理工具模块

提供文本清理、格式化等工具函数
"""

import re
from typing import List, Optional


def clean_text_for_browser(text: str) -> str:
    """
    清理文本中ChromeDriver不支持的字符
    
    ChromeDriver只支持BMP(Basic Multilingual Plane)字符
    
    Args:
        text: 原始文本
        
    Returns:
        清理后的文本
    """
    if not text:
        return ""
        
    # 移除超出BMP范围的字符（U+10000及以上）
    cleaned_text = ""
    for char in text:
        # BMP字符范围是U+0000到U+FFFF
        if ord(char) <= 0xFFFF:
            cleaned_text += char
        else:
            # 用空格替换不支持的字符
            cleaned_text += " "
    
    # 清理连续的空格，但保留换行符
    # 使用 [^\S\n]+ 匹配除换行符外的所有空白字符
    cleaned_text = re.sub(r'[^\S\n]+', ' ', cleaned_text).strip()
    
    return cleaned_text


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    截断文本到指定长度
    
    Args:
        text: 原始文本
        max_length: 最大长度
        suffix: 截断后缀
        
    Returns:
        截断后的文本
    """
    if not text or len(text) <= max_length:
        return text
    
    # 确保后缀不会超过最大长度
    if len(suffix) >= max_length:
        return text[:max_length]
    
    return text[:max_length - len(suffix)] + suffix


def parse_topics_string(topics_string: str) -> List[str]:
    """
    解析话题字符串
    
    Args:
        topics_string: 话题字符串，用逗号分隔
        
    Returns:
        话题列表
    """
    if not topics_string:
        return []
    
    # 分割并清理话题
    topics = [topic.strip() for topic in topics_string.split(",") if topic.strip()]
    
    # 移除重复话题（保持顺序）
    unique_topics = []
    seen = set()
    for topic in topics:
        if topic not in seen:
            unique_topics.append(topic)
            seen.add(topic)
    
    return unique_topics


# 为了向后兼容，保留原函数名
def parse_tags_string(tags_string: str) -> List[str]:
    """
    解析标签字符串（已废弃，请使用parse_topics_string）
    
    Args:
        tags_string: 标签字符串，用逗号分隔
        
    Returns:
        标签列表
    """
    return parse_topics_string(tags_string)


def parse_file_paths_string(paths_string: str) -> List[str]:
    """
    解析文件路径字符串
    
    Args:
        paths_string: 文件路径字符串，用逗号分隔
        
    Returns:
        文件路径列表
    """
    if not paths_string:
        return []
    
    # 分割并清理路径
    paths = [path.strip() for path in paths_string.split(",") if path.strip()]
    
    return paths


def smart_parse_file_paths(paths_input) -> List[str]:
    """
    智能解析文件路径，支持多种输入格式
    
    支持的格式：
    1. 逗号分隔字符串："a,b,c,d"
    2. 数组字符串："[a,b,c]"
    3. JSON数组字符串：'["a","b","c"]'
    4. 真正的数组：["a","b","c"]
    5. 其他可迭代对象
    
    Args:
        paths_input: 各种格式的路径输入
        
    Returns:
        文件路径列表
    """
    import json
    import ast
    
    if not paths_input:
        return []
    
    # 情况1: 如果输入已经是列表或其他可迭代对象（但不是字符串）
    if isinstance(paths_input, (list, tuple)):
        # 处理数组中的每个元素，确保都是字符串
        result = []
        for item in paths_input:
            if isinstance(item, str):
                result.append(item.strip())
            else:
                # 如果不是字符串，尝试转换为字符串
                result.append(str(item).strip())
        return [path for path in result if path]  # 过滤空字符串
    
    # 情况2: 如果输入是字符串
    if isinstance(paths_input, str):
        paths_str = paths_input.strip()
        
        if not paths_str:
            return []
        
        # 2.1: 尝试解析JSON数组格式：'["a","b","c"]'
        if paths_str.startswith('[') and paths_str.endswith(']'):
            try:
                # 先尝试JSON解析
                parsed = json.loads(paths_str)
                if isinstance(parsed, list):
                    return [str(item).strip() for item in parsed if str(item).strip()]
            except json.JSONDecodeError:
                # JSON解析失败，尝试使用ast.literal_eval
                try:
                    parsed = ast.literal_eval(paths_str)
                    if isinstance(parsed, (list, tuple)):
                        return [str(item).strip() for item in parsed if str(item).strip()]
                except (ValueError, SyntaxError):
                    # 如果都解析失败，可能是格式不标准的数组字符串
                    # 尝试手动解析：[a,b,c] 这种格式
                    try:
                        # 去掉方括号
                        inner_content = paths_str[1:-1].strip()
                        if inner_content:
                            # 按逗号分割
                            items = [item.strip().strip('"\'') for item in inner_content.split(',')]
                            return [item for item in items if item]
                        else:
                            return []
                    except:
                        pass
        
        # 2.2: 尝试JSON数组格式但没有外层引号：["a","b","c"]
        try:
            # 直接尝试JSON解析
            parsed = json.loads(paths_str)
            if isinstance(parsed, list):
                return [str(item).strip() for item in parsed if str(item).strip()]
        except json.JSONDecodeError:
            pass
        
        # 2.3: 普通逗号分隔格式："a,b,c,d"
        if ',' in paths_str:
            paths = [path.strip().strip('"\'') for path in paths_str.split(',')]
            return [path for path in paths if path]
        
        # 2.4: 单个文件路径
        return [paths_str.strip().strip('"\'')]
    
    # 情况3: 其他类型，尝试转换为字符串后递归处理
    try:
        return smart_parse_file_paths(str(paths_input))
    except:
        return []


def validate_note_content(title: str, content: str) -> List[str]:
    """
    验证笔记内容
    
    Args:
        title: 笔记标题
        content: 笔记内容
        
    Returns:
        验证错误列表，空列表表示验证通过
    """
    errors = []
    
    # 检查标题
    if not title or not title.strip():
        errors.append("标题不能为空")
    elif len(title.strip()) > 50:
        errors.append("标题长度不能超过50个字符")
    
    # 检查内容
    if not content or not content.strip():
        errors.append("内容不能为空")
    elif len(content.strip()) > 1000:
        errors.append("内容长度不能超过1000个字符")
    
    return errors


def safe_print(text: str) -> None:
    """
    安全打印函数，处理Windows下的Unicode编码问题
    
    Args:
        text: 要打印的文本
    """
    try:
        print(text)
    except UnicodeEncodeError:
        # 替换常见的emoji字符为文本
        replacements = {
            '🔧': '[配置]',
            '✅': '[成功]',  
            '❌': '[失败]',
            '⚠️': '[警告]',
            '🍪': '[Cookie]',
            '🚀': '[启动]',
            '🛑': '[停止]',
            '🔍': '[检查]',
            '📝': '[笔记]',
            '📊': '[状态]',
            '💻': '[系统]',
            '🐍': '[Python]',
            '💡': '[提示]',
            '📄': '[文件]',
            '🧪': '[测试]',
            '📱': '[发布]',
            '🎉': '[完成]',
            '🌺': '[小红书]',
            '🧹': '[清理]',
            '👋': '[再见]',
            '📡': '[信号]'
        }
        
        safe_text = text
        for emoji, replacement in replacements.items():
            safe_text = safe_text.replace(emoji, replacement)
        
        print(safe_text) 