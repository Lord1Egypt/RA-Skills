#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw SKILL - Markdown 图表渲染器
主入口文件

功能：
1. 自动识别 Markdown 文档中的图表代码块（Mermaid/Graphviz/PlantUML）
2. 渲染图表为图片
3. 替换原代码块为 Base64 内联图片
4. 可选保留原始代码为注释
"""

import os
import re
import json
import base64
import logging
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any

from core import DiagramDetector, DiagramRenderer, MarkdownProcessor

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [MD_DIAGRAM_RENDERER] - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MDDiagramRendererSkill:
    """OpenClaw SKILL 主类 - Markdown 图表渲染器"""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化 SKILL
        
        Args:
            config: SKILL 配置，来自 skill.yaml 或运行时传入
        """
        self.config = config or {}
        self.detector = DiagramDetector(self.config)
        self.renderer = DiagramRenderer(self.config)
        self.processor = MarkdownProcessor(self.config)
        
        self._stats = {
            'files_processed': 0,
            'blocks_detected': 0,
            'blocks_rendered': 0,
            'blocks_failed': 0,
        }
    
    def parse_markdown(self, file_path: str = None, content: str = None) -> Dict:
        """
        Tool: 解析 Markdown 文档
        
        Args:
            file_path: Markdown 文件路径
            content: 或直接传入 Markdown 内容
            
        Returns:
            Dict: 解析结果，包含代码块列表
        """
        try:
            if content is None:
                if not file_path or not os.path.exists(file_path):
                    return {
                        'success': False,
                        'code_blocks': [],
                        'error': '文件路径无效或文件不存在'
                    }
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            
            code_blocks = self.processor.extract_code_blocks(content)
            
            return {
                'success': True,
                'code_blocks': code_blocks,
                'total_blocks': len(code_blocks),
                'error': None
            }
            
        except Exception as e:
            logger.error(f"解析 Markdown 失败：{e}")
            return {
                'success': False,
                'code_blocks': [],
                'error': str(e)
            }
    
    def detect_diagram(self, code_content: str, code_language: str = "") -> Dict:
        """
        Tool: 检测代码块是否为图表
        
        Args:
            code_content: 代码内容
            code_language: 代码语言标识
            
        Returns:
            Dict: 检测结果
        """
        try:
            result = self.detector.detect(code_content, code_language)
            
            return {
                'success': True,
                'is_diagram': result['is_diagram'],
                'diagram_type': result['diagram_type'],
                'confidence': result['confidence'],
                'reason': result['reason'],
                'error': None
            }
            
        except Exception as e:
            logger.error(f"检测图表失败：{e}")
            return {
                'success': False,
                'is_diagram': False,
                'diagram_type': 'unknown',
                'confidence': 0.0,
                'reason': str(e),
                'error': str(e)
            }
    
    def render_diagram(self, code_content: str, diagram_type: str, 
                       output_format: str = "png") -> Dict:
        """
        Tool: 渲染图表为图片
        
        Args:
            code_content: 图表代码
            diagram_type: 图表类型 (mermaid/graphviz/plantuml)
            output_format: 输出格式 (png/svg)
            
        Returns:
            Dict: 渲染结果，包含 Base64 图片
        """
        try:
            result = self.renderer.render(code_content, diagram_type, output_format)
            
            return {
                'success': result['success'],
                'image_base64': result.get('image_base64', ''),
                'image_format': result.get('image_format', output_format),
                'error': result.get('error')
            }
            
        except Exception as e:
            logger.error(f"渲染图表失败：{e}")
            return {
                'success': False,
                'image_base64': '',
                'image_format': output_format,
                'error': str(e)
            }
    
    def replace_and_save(self, file_path: str, replacements: List[Dict], 
                         preserve_source: bool = True) -> Dict:
        """
        Tool: 替换代码块为图片并保存
        
        Args:
            file_path: 文件路径
            replacements: 替换列表，每项包含 {original, image_base64, diagram_type}
            preserve_source: 是否保留源代码
            
        Returns:
            Dict: 保存结果
        """
        try:
            output_path = self.processor.replace_and_save(
                file_path=file_path,
                replacements=replacements,
                preserve_source=preserve_source
            )
            
            self._stats['files_processed'] += 1
            
            return {
                'success': True,
                'output_path': output_path,
                'stats': self._stats.copy(),
                'error': None
            }
            
        except Exception as e:
            logger.error(f"保存文件失败：{e}")
            return {
                'success': False,
                'output_path': None,
                'stats': self._stats.copy(),
                'error': str(e)
            }
    
    def execute(self, input_file: str, output_file: str = None, 
                config: Optional[Dict] = None) -> Dict:
        """
        SKILL 主执行入口
        
        Args:
            input_file: 输入 Markdown 文件路径
            output_file: 输出文件路径 (可选，默认覆盖原文件)
            config: 运行时配置覆盖
            
        Returns:
            Dict: 执行结果
        """
        # 合并配置
        if config:
            self.config.update(config)
        
        logger.info(f"开始处理文件：{input_file}")
        
        try:
            # 步骤 1: 解析 Markdown
            parse_result = self.parse_markdown(file_path=input_file)
            if not parse_result['success']:
                return {
                    'success': False,
                    'message': '解析失败',
                    'error': parse_result['error'],
                    'stats': self._stats
                }
            
            code_blocks = parse_result['code_blocks']
            logger.info(f"检测到 {len(code_blocks)} 个代码块")
            
            # 步骤 2: 检测并渲染图表
            replacements = []
            for idx, block in enumerate(code_blocks):
                # 检测是否为图表
                detect_result = self.detect_diagram(
                    code_content=block['content'],
                    code_language=block['language']
                )
                
                if not detect_result['is_diagram']:
                    logger.debug(f"[{idx+1}/{len(code_blocks)}] 非图表代码块，跳过")
                    continue
                
                self._stats['blocks_detected'] += 1
                logger.info(
                    f"[{idx+1}/{len(code_blocks)}] 检测到图表："
                    f"{detect_result['diagram_type']} "
                    f"(置信度：{detect_result['confidence']:.2f})"
                )
                
                # 渲染图表
                render_result = self.render_diagram(
                    code_content=block['content'],
                    diagram_type=detect_result['diagram_type'],
                    output_format=self.config.get('output_format', 'png')
                )
                
                if render_result['success']:
                    self._stats['blocks_rendered'] += 1
                    replacements.append({
                        'original': block,
                        'image_base64': render_result['image_base64'],
                        'image_format': render_result.get('image_format', 'png'),
                        'diagram_type': detect_result['diagram_type'],
                        'confidence': detect_result['confidence']
                    })
                    logger.info(f"  ✓ 渲染成功")
                else:
                    self._stats['blocks_failed'] += 1
                    logger.warning(f"  ✗ 渲染失败：{render_result['error']}")
            
            # 步骤 3: 替换并保存
            if replacements:
                # 如果指定了输出文件，先复制
                save_path = output_file if output_file else input_file
                
                save_result = self.replace_and_save(
                    file_path=save_path,
                    replacements=replacements,
                    preserve_source=self.config.get('preserve_source', True)
                )
                
                if not save_result['success']:
                    return {
                        'success': False,
                        'message': '保存失败',
                        'error': save_result['error'],
                        'stats': self._stats
                    }
                
                output_path = save_result['output_path']
            else:
                output_path = input_file
                logger.info("未检测到可渲染的图表")
            
            return {
                'success': True,
                'message': '处理完成',
                'output_path': output_path,
                'replacements_count': len(replacements),
                'stats': self._stats
            }
            
        except Exception as e:
            logger.error(f"执行失败：{e}", exc_info=True)
            return {
                'success': False,
                'message': '执行异常',
                'error': str(e),
                'stats': self._stats
            }
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return self._stats.copy()
    
    def reset_stats(self):
        """重置统计信息"""
        self._stats = {
            'files_processed': 0,
            'blocks_detected': 0,
            'blocks_rendered': 0,
            'blocks_failed': 0,
        }


# ============== OpenClaw 标准入口 ==============

def create_skill(config: Optional[Dict] = None) -> MDDiagramRendererSkill:
    """
    OpenClaw 标准：创建 SKILL 实例
    
    Args:
        config: SKILL 配置
        
    Returns:
        MDDiagramRendererSkill: SKILL 实例
    """
    return MDDiagramRendererSkill(config)


def main(event: Dict, context: Optional[Any] = None) -> Dict:
    """
    OpenClaw 标准：主入口函数
    
    Args:
        event: 事件数据，包含 input_file, output_file, config 等
        context: 运行上下文
        
    Returns:
        Dict: 执行结果
    """
    # 从 event 中提取参数
    input_file = event.get('input_file')
    output_file = event.get('output_file')
    config = event.get('config', {})
    
    # 创建并执行 SKILL
    skill = create_skill(config)
    result = skill.execute(input_file, output_file, config)
    
    return result


# CLI 支持
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='OpenClaw SKILL - Markdown 图表渲染器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 处理单个文件
  python main.py document.md
  
  # 指定输出文件
  python main.py document.md -o output.md
  
  # 设置置信度阈值
  python main.py document.md --threshold 0.7
  
  # 输出 SVG 格式
  python main.py document.md --format svg
  
  # 不保留源代码
  python main.py document.md --no-preserve
        """
    )
    
    parser.add_argument('input_file', help='输入 Markdown 文件路径')
    parser.add_argument('-o', '--output', dest='output_file', help='输出文件路径')
    parser.add_argument('--threshold', type=float, default=0.6, 
                        help='图表识别置信度阈值 (默认: 0.6)')
    parser.add_argument('--format', choices=['png', 'svg'], default='png', 
                        help='输出图片格式 (默认: png)')
    parser.add_argument('--no-preserve', action='store_true', 
                        help='不保留原始图表代码')
    parser.add_argument('-v', '--verbose', action='store_true', 
                        help='显示详细日志')
    parser.add_argument('-q', '--quiet', action='store_true', 
                        help='静默模式，只输出错误')
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.quiet:
        logging.getLogger().setLevel(logging.ERROR)
    
    config = {
        'confidence_threshold': args.threshold,
        'output_format': args.format,
        'preserve_source': not args.no_preserve,
    }
    
    # 模拟 OpenClaw event
    event = {
        'input_file': args.input_file,
        'output_file': args.output_file,
        'config': config
    }
    
    result = main(event)
    
    # 输出结果
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 退出码
    exit(0 if result['success'] else 1)
