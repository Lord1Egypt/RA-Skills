"""
文章解析模块
"""

import re
from pathlib import Path
from typing import Optional

from .types import Article, Section


class ArticleParser:
    """文章解析器"""
    
    @staticmethod
    def parse(file_path: str) -> Article:
        """
        解析 Markdown 文章
        
        Args:
            file_path: 文章文件路径
            
        Returns:
            Article 对象
            
        Raises:
            FileNotFoundError: 文件不存在
            ValueError: 文件格式错误
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        content = path.read_text(encoding='utf-8')
        return ArticleParser.parse_markdown(content)
    
    @staticmethod
    def parse_markdown(content: str) -> Article:
        """
        解析 Markdown 内容
        
        Args:
            content: Markdown 内容
            
        Returns:
            Article 对象
        """
        lines = content.strip().split('\n')
        
        # 提取标题（第一个 # 开头的行）
        title = ""
        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                title = line.lstrip('#').strip()
                break
        
        if not title:
            # 如果没有标题，使用第一行
            title = lines[0].strip() if lines else "无标题"
        
        # 解析章节
        sections = ArticleParser._parse_sections(lines)
        
        # 生成摘要
        summary = title
        
        return Article(
            title=title,
            sections=sections,
            summary=summary
        )
    
    @staticmethod
    def _parse_sections(lines: list[str]) -> list[Section]:
        """
        解析章节
        
        Args:
            lines: 行列表
            
        Returns:
            章节列表
        """
        sections = []
        current_section = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            
            # 跳过空行
            if not line:
                continue
            
            # 检查是否是章节标题（## 开头）- 优先检查
            if line.startswith('##'):
                # 保存之前的章节
                if current_section and current_content:
                    sections.append(Section(
                        title=current_section,
                        content='\n'.join(current_content).strip()
                    ))
                    current_content = []
                
                current_section = line.lstrip('#').strip()
                continue
            
            # 跳过文章标题行（# 开头，但不是 ##）
            if line.startswith('#'):
                # 保存之前的章节
                if current_section and current_content:
                    sections.append(Section(
                        title=current_section,
                        content='\n'.join(current_content).strip()
                    ))
                    current_content = []
                continue
            
            # 添加到当前章节内容
            if current_section is None:
                # 如果没有章节标题，创建一个默认章节
                current_section = "内容"
            current_content.append(line)
        
        # 保存最后一个章节
        if current_section and current_content:
            sections.append(Section(
                title=current_section,
                content='\n'.join(current_content).strip()
            ))
        
        # 如果没有解析出章节，创建默认章节
        if not sections:
            sections.append(Section(
                title="内容",
                content=lines[0] if lines else ""
            ))
        
        return sections
    
    @staticmethod
    def extract_all_content(article: Article) -> str:
        """
        提取文章的全部内容
        
        用于插图（完整表达文章内容）
        
        Args:
            article: 文章对象
            
        Returns:
            全部内容文本
        """
        parts = [article["title"]]
        
        for section in article["sections"]:
            parts.append(f"{section['title']}: {section['content']}")
        
        return " ".join(parts)
    
    @staticmethod
    def get_plain_text(md_content: str) -> str:
        """
        获取纯文本（去除 Markdown 语法）
        
        Args:
            md_content: Markdown 内容
            
        Returns:
            纯文本
        """
        # 去除标题标记
        text = re.sub(r'#+ ', '', md_content)
        # 去除加粗
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        # 去除链接
        text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
        # 去除图片
        text = re.sub(r'!\[.*?\]\(.+?\)', '', text)
        # 去除代码块
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        text = re.sub(r'`(.+?)`', r'\1', text)
        
        return text.strip()
