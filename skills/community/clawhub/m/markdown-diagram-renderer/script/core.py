#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw SKILL - Markdown 图表渲染器
核心逻辑模块
"""

import os
import re
import base64
import logging
import subprocess
import tempfile
from typing import Dict, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class DiagramDetector:
    """图表检测器 - 基于启发式规则识别图表类型"""
    
    # 图表类型识别规则 - 首行关键字模式
    PATTERNS = {
        'mermaid': [
            r'^\s*(graph|sequenceDiagram|classDiagram|stateDiagram|gantt|pie|flowchart|erDiagram)\s',
            r'^\s*%%{?\s*init',
        ],
        'graphviz': [
            r'^\s*(digraph|graph|strict)\s+\w+',
            r'^\s*(digraph|graph|strict)\s*\{',
        ],
        'plantuml': [
            r'@startuml',
            r'@enduml',
            r'@startjson',
            r'@startmindmap',
        ],
    }
    
    # 关键词权重 - 用于密度分析
    KEYWORDS = {
        'mermaid': {
            '-->': 2, '---': 1, '->>': 2, '-->>': 2,
            'graph': 3, 'sequenceDiagram': 4, 'classDiagram': 4,
            'flowchart': 3, 'erDiagram': 4, 'gantt': 4,
        },
        'graphviz': {
            '->': 2, '--': 1, 'digraph': 4, 'graph': 2,
            'node': 2, 'edge': 2, 'subgraph': 3, 'label': 1,
        },
        'plantuml': {
            '@startuml': 5, '@enduml': 5, 'actor': 3, 
            'participant': 3, 'package': 2, 'class': 2,
            'interface': 2, 'note': 1, 'arrow': 1,
        },
    }
    
    # 结构特征
    STRUCTURES = {
        'mermaid': [r'\[[^\]]+\]', r'\([^\)]+\)', r'\{[^\}]+\}'],
        'graphviz': [r'\[[^\]]+\]', r'\{[^\}]+\}', r'subgraph\s+\w+'],
        'plantuml': [r':\s*[^:]+:', r'\[\s*\]', r'\{\s*\}'],
    }
    
    def __init__(self, config: Dict):
        self.config = config
        self.threshold = config.get('confidence_threshold', 0.6)
    
    def detect(self, code_content: str, code_language: str = "") -> Dict:
        """
        检测代码块是否为图表
        
        Args:
            code_content: 代码内容
            code_language: 代码语言标识
            
        Returns:
            Dict: 检测结果
        """
        # 优先检查语言标识
        lang_map = {
            'mermaid': 'mermaid', 'mmd': 'mermaid',
            'graphviz': 'graphviz', 'dot': 'graphviz', 'gv': 'graphviz',
            'plantuml': 'plantuml', 'puml': 'plantuml',
        }
        
        if code_language:
            lang_lower = code_language.lower().strip()
            if lang_lower in lang_map:
                return {
                    'is_diagram': True,
                    'diagram_type': lang_map[lang_lower],
                    'confidence': 1.0,
                    'reason': f'语言标识：{code_language}'
                }
        
        # 内容过短直接排除
        if not code_content or len(code_content.strip()) < 10:
            return {
                'is_diagram': False,
                'diagram_type': 'unknown',
                'confidence': 0.0,
                'reason': '内容过短'
            }
        
        # 多规则评分
        scores = {t: 0.0 for t in self.PATTERNS.keys()}
        reasons = {t: [] for t in self.PATTERNS.keys()}
        
        # 阶段1: 首行关键字匹配
        lines = code_content.strip().split('\n')
        first_lines = '\n'.join(lines[:5])  # 检查前5行
        
        for diagram_type, patterns in self.PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, first_lines, re.MULTILINE | re.IGNORECASE):
                    scores[diagram_type] += 0.4
                    reasons[diagram_type].append(f'首行匹配：{pattern[:20]}')
        
        # 阶段2: 关键词密度分析
        for diagram_type, keywords in self.KEYWORDS.items():
            for keyword, weight in keywords.items():
                count = code_content.count(keyword)
                if count > 0:
                    scores[diagram_type] += min(count * weight * 0.1, 1.0)
        
        # 阶段3: 结构特征分析
        for diagram_type, structures in self.STRUCTURES.items():
            for pattern in structures:
                matches = re.findall(pattern, code_content)
                if len(matches) >= 2:
                    scores[diagram_type] += 0.2
                    reasons[diagram_type].append(f'结构特征：{len(matches)}个匹配')
        
        # 找出最高分
        best_type = max(scores, key=scores.get)
        best_score = min(scores[best_type] / 3.0, 1.0)
        
        if best_score >= self.threshold:
            return {
                'is_diagram': True,
                'diagram_type': best_type,
                'confidence': round(best_score, 2),
                'reason': '; '.join(reasons[best_type][:3]) if reasons[best_type] else '综合评分达标'
            }
        
        return {
            'is_diagram': False,
            'diagram_type': 'unknown',
            'confidence': round(best_score, 2),
            'reason': '置信度不足'
        }


class DiagramRenderer:
    """图表渲染器 - 支持多种后端"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.output_format = config.get('output_format', 'png')
    
    def render(self, code: str, diagram_type: str, output_format: str = "png") -> Dict:
        """
        渲染图表
        
        Args:
            code: 图表代码
            diagram_type: 图表类型
            output_format: 输出格式
            
        Returns:
            Dict: 渲染结果
        """
        try:
            if diagram_type == 'mermaid':
                return self._render_mermaid(code, output_format)
            elif diagram_type == 'graphviz':
                return self._render_graphviz(code, output_format)
            elif diagram_type == 'plantuml':
                return self._render_plantuml(code, output_format)
            else:
                return {
                    'success': False,
                    'error': f'不支持的图表类型：{diagram_type}'
                }
        except Exception as e:
            logger.error(f"渲染失败：{e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _render_mermaid(self, code: str, output_format: str) -> Dict:
        """渲染 Mermaid 图表"""
        # 方法1: 使用 mmdc CLI (本地)
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False, encoding='utf-8') as src:
                src.write(code.strip())
                src_path = src.name
            
            with tempfile.NamedTemporaryFile(suffix=f'.{output_format}', delete=False) as dst:
                dst_path = dst.name
            
            result = subprocess.run(
                ['mmdc', '-i', src_path, '-o', dst_path, '-b', 'white'],
                capture_output=True,
                timeout=30
            )
            
            if result.returncode == 0 and os.path.exists(dst_path):
                with open(dst_path, 'rb') as f:
                    img_data = f.read()
                os.remove(src_path)
                os.remove(dst_path)
                
                return {
                    'success': True,
                    'image_base64': base64.b64encode(img_data).decode('utf-8'),
                    'image_format': output_format
                }
            
            # 清理临时文件
            if os.path.exists(src_path):
                os.remove(src_path)
            if os.path.exists(dst_path):
                os.remove(dst_path)
                
        except FileNotFoundError:
            logger.debug("mmdc CLI 未安装，尝试在线渲染")
        except Exception as e:
            logger.warning(f"mmdc 渲染失败：{e}")
        
        # 方法2: 在线 API (备用)
        try:
            import urllib.request
            
            # 使用 mermaid.ink 服务
            encoded = base64.b64encode(code.encode('utf-8')).decode('ascii')
            url = f"https://mermaid.ink/img/{encoded}"
            
            request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(request, timeout=15) as response:
                img_data = response.read()
            
            return {
                'success': True,
                'image_base64': base64.b64encode(img_data).decode('utf-8'),
                'image_format': 'png'
            }
        except Exception as e:
            logger.warning(f"在线 Mermaid 渲染失败：{e}")
        
        return {
            'success': False,
            'error': '所有 Mermaid 渲染方法均失败，请安装 mmdc 或检查网络连接'
        }
    
    def _render_graphviz(self, code: str, output_format: str) -> Dict:
        """渲染 Graphviz 图表"""
        try:
            import graphviz
            
            source = graphviz.Source(code.strip())
            img_data = source.pipe(format=output_format)
            
            return {
                'success': True,
                'image_base64': base64.b64encode(img_data).decode('utf-8'),
                'image_format': output_format
            }
        except ImportError:
            return {
                'success': False,
                'error': 'graphviz Python 库未安装，请运行: pip install graphviz'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Graphviz 渲染失败：{str(e)}'
            }
    
    def _render_plantuml(self, code: str, output_format: str) -> Dict:
        """渲染 PlantUML 图表"""
        # 方法1: 本地 jar 包
        try:
            plantuml_jar = os.environ.get('PLANTUML_JAR', 'plantuml.jar')
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.puml', delete=False, encoding='utf-8') as src:
                src.write(code.strip())
                src_path = src.name
            
            result = subprocess.run(
                ['java', '-jar', plantuml_jar, f'-t{output_format}', src_path],
                capture_output=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # PlantUML 输出文件在同一目录
                output_file = src_path.replace('.puml', f'.{output_format}')
                if os.path.exists(output_file):
                    with open(output_file, 'rb') as f:
                        img_data = f.read()
                    os.remove(src_path)
                    os.remove(output_file)
                    
                    return {
                        'success': True,
                        'image_base64': base64.b64encode(img_data).decode('utf-8'),
                        'image_format': output_format
                    }
            
            if os.path.exists(src_path):
                os.remove(src_path)
                
        except FileNotFoundError:
            logger.debug("Java 或 PlantUML jar 未安装，尝试在线渲染")
        except Exception as e:
            logger.warning(f"本地 PlantUML 渲染失败：{e}")
        
        # 方法2: 在线 API
        try:
            import urllib.request
            import zlib
            
            def encode_plantuml(text: str) -> str:
                """PlantUML 特殊编码"""
                compressed = zlib.compress(text.encode('utf-8'))[2:-4]
                encoded = base64.b64encode(compressed).decode('ascii')
                return encoded.replace('+', '-').replace('/', '_')
            
            encoded = encode_plantuml(code.strip())
            url = f"http://www.plantuml.com/plantuml/{output_format}/{encoded}"
            
            request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(request, timeout=15) as response:
                img_data = response.read()
            
            return {
                'success': True,
                'image_base64': base64.b64encode(img_data).decode('utf-8'),
                'image_format': output_format
            }
        except Exception as e:
            logger.warning(f"在线 PlantUML 渲染失败：{e}")
        
        return {
            'success': False,
            'error': 'PlantUML 渲染失败，请安装 Java 和 PlantUML 或检查网络连接'
        }


class MarkdownProcessor:
    """Markdown 处理器 - 基于 mistletoe AST 解析"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.preserve_source = config.get('preserve_source', True)
    
    def extract_code_blocks(self, content: str) -> List[Dict]:
        """
        提取所有代码块
        
        Args:
            content: Markdown 内容
            
        Returns:
            List[Dict]: 代码块列表
        """
        try:
            # 尝试使用 mistletoe 进行 AST 解析
            from mistletoe import Document
            from mistletoe.block_token import CodeFence
            
            doc = Document.read(content)
            blocks = []
            
            def walk_tokens(tokens, content_str):
                """递归遍历 AST"""
                for token in tokens:
                    if isinstance(token, CodeFence):
                        # 计算 token 在原文中的位置
                        # mistletoe 不直接提供位置，需要通过内容匹配
                        block_content = token.children[0].content if token.children else ''
                        
                        # 构建完整的代码块字符串用于匹配
                        lang = token.language or ''
                        full_block = f"```{lang}\n{block_content}\n```"
                        
                        # 在原文中查找位置
                        idx = content_str.find(full_block)
                        if idx != -1:
                            blocks.append({
                                'language': lang.strip(),
                                'content': block_content.strip(),
                                'start': idx,
                                'end': idx + len(full_block),
                                'full_match': full_block
                            })
                    
                    # 递归处理子 token
                    if hasattr(token, 'children') and token.children:
                        walk_tokens(token.children, content_str)
            
            walk_tokens(doc.children, content)
            
            if blocks:
                return blocks
                
        except ImportError:
            logger.warning("mistletoe 未安装，使用正则表达式解析")
        except Exception as e:
            logger.warning(f"AST 解析失败，回退到正则表达式：{e}")
        
        # 回退方案：使用正则表达式
        return self._extract_with_regex(content)
    
    def _extract_with_regex(self, content: str) -> List[Dict]:
        """使用正则表达式提取代码块"""
        pattern = re.compile(r'```(\w*)\n(.*?)\n```', re.DOTALL | re.MULTILINE)
        
        blocks = []
        for match in pattern.finditer(content):
            blocks.append({
                'language': match.group(1).strip(),
                'content': match.group(2).strip(),
                'start': match.start(),
                'end': match.end(),
                'full_match': match.group(0)
            })
        
        return blocks
    
    def replace_and_save(self, file_path: str, replacements: List[Dict], 
                         preserve_source: bool = True) -> str:
        """
        替换代码块并保存
        
        Args:
            file_path: 文件路径
            replacements: 替换列表
            preserve_source: 是否保留源代码
            
        Returns:
            str: 输出文件路径
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 按位置倒序替换 (避免索引偏移)
        replacements_sorted = sorted(
            replacements, 
            key=lambda x: x['original']['start'], 
            reverse=True
        )
        
        for rep in replacements_sorted:
            original = rep['original']['full_match']
            diagram_type = rep['diagram_type']
            img_base64 = rep['image_base64']
            img_format = rep.get('image_format', 'png')
            
            # 创建图片 Markdown
            alt_text = f"{diagram_type} diagram"
            img_md = f"![{alt_text}](data:image/{img_format};base64,{img_base64})"
            
            # 可选保留源代码
            if preserve_source:
                img_md += (
                    f"\n\n<!-- 原始图表代码 -->\n"
                    f"<!--\n"
                    f"```{diagram_type}\n"
                    f"{rep['original']['content']}\n"
                    f"```\n"
                    f"-->"
                )
            
            # 替换
            content = content.replace(original, img_md, 1)
        
        # 保存
        output_path = file_path
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"文件已保存：{output_path}")
        return output_path
