#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 增强的 txt 清理器
整合规则引擎和 AI 增强模块
"""

import os
import sys
import re
import json
import yaml
import logging
import argparse
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

# 添加模块路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ai_modules.ad_detector import AIAdDetector, AdDetectionResult, remove_ads_from_text
from ai_modules.mojibake_fixer import AIMojibakeFixer, MojibakeFixResult, apply_fixes_to_text
from ai_modules.chapter_parser import AIChapterParser, ChapterParseResult, normalize_text_chapters
from utils.llm_client import init_client, get_client

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class CleanReport:
    """清理报告"""
    original_length: int
    cleaned_length: int
    removed_chars: int
    removed_percent: float
    
    # 广告清理
    ads_removed: int
    ads_by_type: Dict[str, int]
    
    # 乱码修复
    mojibake_fixed: int
    mojibake_changes: List[Dict]
    
    # 章节识别
    chapters_found: int
    chapters_normalized: int
    
    # 处理模式
    mode: str
    ai_enabled: bool
    
    # 性能统计
    processing_time: float
    llm_calls: int
    llm_tokens: int


class AIEnhancedTxtCleaner:
    """AI 增强的 txt 清理器"""
    
    def __init__(self, config_path: Optional[str] = None):
        # 加载配置
        self.config = self._load_config(config_path)
        
        # 获取处理模式
        self.mode = self.config.get('mode', 'balanced')
        self._apply_mode_config()
        
        # 初始化 LLM 客户端
        self.llm_client = init_client(self.config)
        
        # 初始化 AI 模块
        self.ad_detector = AIAdDetector(self.config, self.llm_client)
        self.mojibake_fixer = AIMojibakeFixer(self.config, self.llm_client)
        self.chapter_parser = AIChapterParser(self.config, self.llm_client)
        
        # 统计信息
        self.total_processed = 0
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """加载配置文件"""
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(__file__),
                'config',
                'ai_config.yaml'
            )
        
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        else:
            logger.warning(f"配置文件不存在: {config_path}，使用默认配置")
            return self._default_config()
    
    def _default_config(self) -> Dict:
        """默认配置"""
        return {
            'mode': 'balanced',
            'ai_enhancement': {
                'enabled': True,
                'ad_detection': {'enabled': True, 'batch_size': 10, 'confidence_threshold': 0.8},
                'mojibake_fix': {'enabled': True, 'batch_size': 5, 'confidence_threshold': 0.7},
                'chapter_detection': {'enabled': False}
            },
            'llm': {
                'provider': 'xiaoyi',
                'model': 'glm-4-flash',
                'timeout': 30,
                'max_retries': 3
            },
            'cache': {'enabled': True, 'ttl': 3600}
        }
    
    def _apply_mode_config(self) -> None:
        """应用模式配置"""
        mode_config = self.config.get('mode_config', {}).get(self.mode, {})
        
        # 更新 AI 模块配置
        if 'ai_ad_detection' in mode_config:
            self.config.setdefault('ai_enhancement', {}).setdefault('ad_detection', {})['enabled'] = mode_config['ai_ad_detection']
        
        if 'ai_mojibake_fix' in mode_config:
            self.config.setdefault('ai_enhancement', {}).setdefault('mojibake_fix', {})['enabled'] = mode_config['ai_mojibake_fix']
        
        if 'ai_chapter_detection' in mode_config:
            self.config.setdefault('ai_enhancement', {}).setdefault('chapter_detection', {})['enabled'] = mode_config['ai_chapter_detection']
        
        logger.info(f"应用处理模式: {self.mode}")
    
    def clean(self, text: str) -> Tuple[str, CleanReport]:
        """清理文本"""
        start_time = datetime.now()
        original_length = len(text)
        
        logger.info(f"开始清理文本，原始长度: {original_length} 字符")
        
        # 1. 规则引擎预处理
        text = self._rule_pre_clean(text)
        
        # 2. AI 广告识别
        paragraphs = self._split_paragraphs(text)
        ad_results = self.ad_detector.detect(paragraphs)
        text, ad_stats = remove_ads_from_text(text, ad_results)
        
        # 3. AI 乱码修复
        mojibake_result = self.mojibake_fixer.fix(text)
        text, mojibake_stats = apply_fixes_to_text(text, mojibake_result)
        
        # 4. AI 章节识别
        chapter_result = self.chapter_parser.parse(text)
        text, chapter_stats = normalize_text_chapters(text, chapter_result)
        
        # 5. 规则引擎后处理
        text = self._rule_post_clean(text)
        
        # 生成报告
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        cleaned_length = len(text)
        
        report = CleanReport(
            original_length=original_length,
            cleaned_length=cleaned_length,
            removed_chars=original_length - cleaned_length,
            removed_percent=(original_length - cleaned_length) / original_length * 100 if original_length > 0 else 0,
            ads_removed=ad_stats.get('total_removed', 0),
            ads_by_type=ad_stats.get('by_type', {}),
            mojibake_fixed=mojibake_stats.get('total_changes', 0),
            mojibake_changes=mojibake_result.changes,
            chapters_found=chapter_result.total_chapters,
            chapters_normalized=chapter_stats.get('normalized', 0),
            mode=self.mode,
            ai_enabled=self.config.get('ai_enhancement', {}).get('enabled', True),
            processing_time=processing_time,
            llm_calls=self.llm_client.call_count,
            llm_tokens=self.llm_client.total_tokens
        )
        
        self.total_processed += 1
        logger.info(f"清理完成，处理后长度: {cleaned_length} 字符，耗时: {processing_time:.2f}s")
        
        return text, report
    
    def clean_file(self, input_path: str, output_path: Optional[str] = None) -> Tuple[str, CleanReport]:
        """清理文件"""
        # 检测编码并读取文件
        text = self._read_file_with_encoding(input_path)
        
        # 清理
        cleaned_text, report = self.clean(text)
        
        # 生成输出路径
        if output_path is None:
            base, ext = os.path.splitext(input_path)
            output_path = f"{base}_清理版{ext}"
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)
        
        logger.info(f"清理后的文件已保存: {output_path}")
        
        return output_path, report
    
    def _read_file_with_encoding(self, file_path: str) -> str:
        """自动检测编码并读取文件"""
        import chardet
        
        # 读取前 100KB 检测编码
        with open(file_path, 'rb') as f:
            raw_data = f.read(102400)
            detected = chardet.detect(raw_data)
            encoding = detected.get('encoding', 'utf-8')
            confidence = detected.get('confidence', 0)
        
        logger.info(f"检测到编码: {encoding} (置信度: {confidence:.2f})")
        
        # 尝试多种编码
        encodings_to_try = [encoding, 'utf-8', 'gbk', 'gb2312', 'gb18030', 'big5']
        
        for enc in encodings_to_try:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    return f.read()
            except (UnicodeDecodeError, LookupError):
                continue
        
        # 最后尝试使用 errors='replace'
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    
    def _split_paragraphs(self, text: str) -> List[str]:
        """分割段落"""
        # 按空行分割
        paragraphs = re.split(r'\n\s*\n', text)
        return [p.strip() for p in paragraphs if p.strip()]
    
    def _rule_pre_clean(self, text: str) -> str:
        """规则引擎预处理"""
        # 移除控制字符
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
        
        # 统一换行符
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        return text
    
    def _rule_post_clean(self, text: str) -> str:
        """规则引擎后处理"""
        # 清理多余空行
        text = re.sub(r'\n{4,}', '\n\n\n', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # 清理行尾空格
        text = re.sub(r'[ \t]+\n', '\n', text)
        
        # 标点规范化
        text = self._normalize_punctuation(text)
        
        return text
    
    def _normalize_punctuation(self, text: str) -> str:
        """标点符号规范化"""
        # 英文标点转中文（在中文上下文中）
        text = re.sub(r'([\u4e00-\u9fff]),', r'\1，', text)
        text = re.sub(r',([\u4e00-\u9fff])', r'，\1', text)
        text = re.sub(r'([\u4e00-\u9fff])\.', r'\1。', text)
        text = re.sub(r'\.([\u4e00-\u9fff])', r'。\1', text)
        text = re.sub(r'([\u4e00-\u9fff])\?', r'\1？', text)
        text = re.sub(r'\?([\u4e00-\u9fff])', r'？\1', text)
        text = re.sub(r'([\u4e00-\u9fff])!', r'\1！', text)
        text = re.sub(r'!([\u4e00-\u9fff])', r'！\1', text)
        text = re.sub(r'([\u4e00-\u9fff]):', r'\1：', text)
        text = re.sub(r':([\u4e00-\u9fff])', r'：\1', text)
        text = re.sub(r'([\u4e00-\u9fff]);', r'\1；', text)
        text = re.sub(r';([\u4e00-\u9fff])', r'；\1', text)
        
        # 省略号规范化
        text = re.sub(r'\.{6,}', '……', text)
        text = re.sub(r'。{6,}', '……', text)
        
        # 破折号规范化
        text = re.sub(r'-{2,}', '——', text)
        text = re.sub(r'~{2,}', '——', text)
        
        # 重复标点修复
        text = re.sub(r'，+', '，', text)
        text = re.sub(r'。+', '。', text)
        text = re.sub(r'！+', '！', text)
        text = re.sub(r'？+', '？', text)
        
        return text
    
    def generate_report_markdown(self, report: CleanReport) -> str:
        """生成 Markdown 格式的报告"""
        md = f"""# txt 清理报告

## 基本信息

| 项目 | 结果 |
|------|------|
| 原文长度 | {report.original_length:,} 字符 |
| 清理后长度 | {report.cleaned_length:,} 字符 |
| 移除内容 | {report.removed_chars:,} 字符 ({report.removed_percent:.2f}%) |
| 处理模式 | {report.mode} |
| AI 增强 | {'已启用' if report.ai_enabled else '未启用'} |

## 清理详情

| 项目 | 数量 |
|------|------|
| 广告清理 | {report.ads_removed} 处 |
| 乱码修复 | {report.mojibake_fixed} 处 |
| 章节识别 | {report.chapters_found} 个 |
| 章节规范化 | {report.chapters_normalized} 个 |

## 性能统计

| 项目 | 数值 |
|------|------|
| 处理时间 | {report.processing_time:.2f} 秒 |
| LLM 调用次数 | {report.llm_calls} 次 |
| Token 消耗 | {report.llm_tokens:,} |

"""
        
        if report.ads_by_type:
            md += "## 广告类型分布\n\n| 类型 | 数量 |\n|------|------|\n"
            for ad_type, count in report.ads_by_type.items():
                md += f"| {ad_type} | {count} |\n"
        
        if report.mojibake_changes:
            md += "\n## 乱码修复详情\n\n| 原字符 | 修复后 | 数量 | 方法 |\n|--------|--------|------|------|\n"
            for change in report.mojibake_changes[:20]:  # 最多显示 20 条
                md += f"| {change.get('before', '')} | {change.get('after', '')} | {change.get('count', 1)} | {change.get('method', 'ai')} |\n"
        
        return md
    
    def stats(self) -> Dict:
        """获取统计信息"""
        return {
            'total_processed': self.total_processed,
            'ad_detector': self.ad_detector.stats(),
            'mojibake_fixer': self.mojibake_fixer.stats(),
            'chapter_parser': self.chapter_parser.stats(),
            'llm_client': self.llm_client.stats()
        }


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='AI 增强的 txt 清理工具')
    parser.add_argument('input', help='输入文件路径')
    parser.add_argument('-o', '--output', help='输出文件路径')
    parser.add_argument('-m', '--mode', choices=['fast', 'balanced', 'thorough'], 
                        default='balanced', help='处理模式')
    parser.add_argument('-c', '--config', help='配置文件路径')
    parser.add_argument('-r', '--report', action='store_true', help='生成详细报告')
    
    args = parser.parse_args()
    
    # 创建清理器
    cleaner = AIEnhancedTxtCleaner(args.config)
    
    # 设置模式
    if args.mode:
        cleaner.mode = args.mode
        cleaner._apply_mode_config()
    
    # 清理文件
    output_path, report = cleaner.clean_file(args.input, args.output)
    
    # 输出报告
    if args.report:
        report_md = cleaner.generate_report_markdown(report)
        report_path = output_path.replace('.txt', '_报告.md')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_md)
        print(f"报告已保存: {report_path}")
    
    # 输出简要报告
    print(f"\n清理完成!")
    print(f"原文长度: {report.original_length:,} 字符")
    print(f"清理后长度: {report.cleaned_length:,} 字符")
    print(f"移除内容: {report.removed_chars:,} 字符 ({report.removed_percent:.2f}%)")
    print(f"处理时间: {report.processing_time:.2f} 秒")
    print(f"输出文件: {output_path}")


if __name__ == '__main__':
    main()
