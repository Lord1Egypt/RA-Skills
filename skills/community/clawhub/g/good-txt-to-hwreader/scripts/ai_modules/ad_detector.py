#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 广告识别模块
使用 LLM 识别非标准广告和变体广告
"""

import json
import re
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# 导入 LLM 客户端
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.llm_client import LLMClient, get_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AdDetectionResult:
    """广告检测结果"""
    is_ad: bool
    confidence: float
    ad_type: str
    reason: str
    paragraph: str


# 广告检测 Prompt 模板
AD_DETECTION_PROMPT = """# 角色
你是一个专业的文本广告识别专家，擅长识别各种形式的广告和推广内容。

# 任务
判断以下段落是否为广告/推广/水印内容。

# 判断标准
1. 包含推广链接、二维码提示
2. 引导下载APP、关注公众号、加入群聊
3. 平台水印、来源声明
4. 作者推广、打赏引导
5. 变体广告（故意添加干扰字符避开检测）
6. 软广（伪装成正文但实际是推广）

# 输出格式（仅输出 JSON，不要其他内容）
{{"is_ad": true/false, "confidence": 0.0-1.0, "ad_type": "watermark|promotion|soft_ad|author_promo|other|none", "reason": "判断理由"}}

# 待检测段落
{paragraph}"""

# 批量广告检测 Prompt 模板
BATCH_AD_DETECTION_PROMPT = """# 角色
你是一个专业的文本广告识别专家，擅长识别各种形式的广告和推广内容。

# 任务
判断以下多个段落是否为广告/推广/水印内容。

# 判断标准
1. 包含推广链接、二维码提示
2. 引导下载APP、关注公众号、加入群聊
3. 平台水印、来源声明
4. 作者推广、打赏引导
5. 变体广告（故意添加干扰字符避开检测）
6. 软广（伪装成正文但实际是推广）

# 输出格式（仅输出 JSON 数组，不要其他内容）
[
  {{"index": 0, "is_ad": true/false, "confidence": 0.0-1.0, "ad_type": "watermark|promotion|soft_ad|author_promo|other|none", "reason": "判断理由"}},
  {{"index": 1, "is_ad": true/false, "confidence": 0.0-1.0, "ad_type": "...", "reason": "..."}},
  ...
]

# 待检测段落列表
{paragraphs}"""


class AIAdDetector:
    """AI 广告识别器"""
    
    def __init__(self, config: Dict, llm_client: Optional[LLMClient] = None):
        self.config = config.get('ai_enhancement', {}).get('ad_detection', {})
        self.enabled = self.config.get('enabled', True)
        self.batch_size = self.config.get('batch_size', 10)
        self.confidence_threshold = self.config.get('confidence_threshold', 0.8)
        self.max_paragraphs = self.config.get('max_paragraphs', 100)
        
        # LLM 客户端
        self.llm = llm_client or get_client(config)
        
        # 统计信息
        self.detected_count = 0
        self.total_processed = 0
    
    def detect(self, paragraphs: List[str]) -> List[AdDetectionResult]:
        """检测广告段落"""
        if not self.enabled:
            logger.info("AI 广告识别已禁用")
            return []
        
        # 限制处理数量
        if len(paragraphs) > self.max_paragraphs:
            logger.warning(f"段落数量超过限制 ({len(paragraphs)} > {self.max_paragraphs})，仅处理前 {self.max_paragraphs} 个")
            paragraphs = paragraphs[:self.max_paragraphs]
        
        # 先用规则引擎过滤已知广告
        rule_results = self._rule_filter(paragraphs)
        
        # 收集需要 AI 检测的段落（仅收集可疑段落）
        ai_needed = []
        ai_indices = []
        
        # 可疑广告特征
        suspicious_patterns = [
            r'【.*?】',  # 方括号内容
            r'www\.',   # 网址
            r'http',    # 链接
            r'下载',    # 下载关键词
            r'关注',    # 关注关键词
            r'APP',     # APP 关键词
            r'公众号',  # 公众号
            r'群',      # 群
            r'VIP',     # VIP
            r'正版',    # 正版
            r'防盗',    # 防盗
        ]
        
        for i, (para, is_ad) in enumerate(zip(paragraphs, rule_results)):
            if not is_ad and len(para.strip()) > 0:
                # 检查是否包含可疑特征
                is_suspicious = any(re.search(p, para, re.IGNORECASE) for p in suspicious_patterns)
                if is_suspicious:
                    ai_needed.append(para)
                    ai_indices.append(i)
        
        logger.info(f"规则引擎识别: {sum(rule_results)} 个广告，可疑段落: {len(ai_needed)} 个")
        
        # 如果没有可疑段落，直接返回规则结果
        if not ai_needed:
            results = []
            for i, para in enumerate(paragraphs):
                if rule_results[i]:
                    results.append(AdDetectionResult(
                        is_ad=True,
                        confidence=1.0,
                        ad_type="rule_matched",
                        reason="规则引擎匹配",
                        paragraph=para
                    ))
                    self.detected_count += 1
                else:
                    results.append(AdDetectionResult(
                        is_ad=False,
                        confidence=0.0,
                        ad_type="none",
                        reason="无广告特征",
                        paragraph=para
                    ))
            self.total_processed += len(paragraphs)
            return results
        
        # AI 批量检测（仅检测可疑段落）
        ai_results = self._batch_detect(ai_needed)
        
        # 合并结果
        results = []
        for i, para in enumerate(paragraphs):
            if rule_results[i]:
                # 规则已识别
                results.append(AdDetectionResult(
                    is_ad=True,
                    confidence=1.0,
                    ad_type="rule_matched",
                    reason="规则引擎匹配",
                    paragraph=para
                ))
                self.detected_count += 1
            elif i in ai_indices:
                # AI 检测结果
                idx = ai_indices.index(i)
                if idx < len(ai_results):
                    results.append(ai_results[idx])
                    if ai_results[idx].is_ad:
                        self.detected_count += 1
                else:
                    results.append(AdDetectionResult(
                        is_ad=False,
                        confidence=0.0,
                        ad_type="none",
                        reason="未检测",
                        paragraph=para
                    ))
            else:
                # 无广告特征
                results.append(AdDetectionResult(
                    is_ad=False,
                    confidence=0.0,
                    ad_type="none",
                    reason="无广告特征",
                    paragraph=para
                ))
        
        self.total_processed += len(paragraphs)
        return results
    
    def _rule_filter(self, paragraphs: List[str]) -> List[bool]:
        """规则引擎快速过滤"""
        # 已知广告模式
        ad_patterns = [
            r'【[^】]*下载[^】]*】',
            r'【[^】]*APP[^】]*】',
            r'【[^】]*收藏[^】]*】',
            r'【[^】]*订阅[^】]*】',
            r'【[^】]*关注[^】]*】',
            r'【[^】]*QQ[^】]*】',
            r'【[^】]*微信[^】]*】',
            r'【[^】]*群[^】]*】',
            r'更多精彩.*?请访问',
            r'本文来自',
            r'首发.*?网站',
            r'独家首发',
            r'转载请注明',
            r'本书由.*?整理',
            r'下载.*?请到',
            r'温馨提示.*?APP',
            r'www\.[a-z0-9]+\.com',
            r'http[s]?://[^\s<>"]+',
            r'==+.*?==+',
        ]
        
        results = []
        for para in paragraphs:
            is_ad = False
            for pattern in ad_patterns:
                if re.search(pattern, para, re.IGNORECASE):
                    is_ad = True
                    break
            results.append(is_ad)
        
        return results
    
    def _batch_detect(self, paragraphs: List[str]) -> List[AdDetectionResult]:
        """批量 AI 检测"""
        results = []
        
        for i in range(0, len(paragraphs), self.batch_size):
            batch = paragraphs[i:i + self.batch_size]
            batch_results = self._detect_batch(batch)
            results.extend(batch_results)
        
        return results
    
    def _detect_batch(self, paragraphs: List[str]) -> List[AdDetectionResult]:
        """检测一批段落"""
        # 构建批量 Prompt
        para_list = "\n".join([f"[{i}] {p}" for i, p in enumerate(paragraphs)])
        prompt = BATCH_AD_DETECTION_PROMPT.format(paragraphs=para_list)
        
        # 调用 LLM
        response = self.llm.call(prompt)
        
        if not response.success:
            logger.error(f"LLM 调用失败: {response.error}")
            return [AdDetectionResult(
                is_ad=False,
                confidence=0.0,
                ad_type="none",
                reason=f"LLM 错误: {response.error}",
                paragraph=p
            ) for p in paragraphs]
        
        # 解析结果
        try:
            # 尝试提取 JSON
            content = response.content.strip()
            if content.startswith('```'):
                content = content.split('\n', 1)[1] if '\n' in content else content
                content = content.rsplit('```', 1)[0] if '```' in content else content
            
            data = json.loads(content)
            
            # 检查数据格式
            if isinstance(data, list):
                # 已经是数组格式，直接使用
                logger.debug(f"收到数组格式响应，包含 {len(data)} 个结果")
            elif isinstance(data, dict):
                # 检查是否是 OpenClaw agent 响应格式
                if 'payloads' in data:
                    # 提取 payloads 中的 text
                    payloads = data.get('payloads', [])
                    if payloads and isinstance(payloads, list):
                        text_content = payloads[0].get('text', '') if payloads else ''
                        # 从 text 中提取 JSON
                        if '```json' in text_content:
                            json_match = text_content.split('```json')[1].split('```')[0].strip()
                            try:
                                data = json.loads(json_match)
                            except json.JSONDecodeError:
                                pass
                        elif text_content.startswith('[') or text_content.startswith('{'):
                            try:
                                data = json.loads(text_content)
                            except json.JSONDecodeError:
                                pass
                
                # 单个结果，转换为数组
                if isinstance(data, dict) and 'index' in data:
                    data = [data]
                elif isinstance(data, dict) and 'results' in data:
                    data = data['results']
                elif isinstance(data, dict):
                    # 其他字典格式，尝试作为单个结果处理
                    logger.debug(f"字典格式响应，键: {list(data.keys())}")
                    if 'is_ad' in data:
                        # 单个广告检测结果
                        data = [data]
                    else:
                        data = []
            
            # 确保 data 是列表
            if not isinstance(data, list):
                logger.debug(f"数据不是列表格式: {type(data).__name__}，已转换为空列表")
                data = []
            
            results = []
            for i, para in enumerate(paragraphs):
                # 查找对应的结果
                item = None
                if isinstance(data, list):
                    item = next((d for d in data if isinstance(d, dict) and d.get('index') == i), None)
                
                if item and isinstance(item, dict):
                    is_ad = item.get('is_ad', False)
                    confidence = item.get('confidence', 0.0)
                    
                    # 应用置信度阈值
                    if is_ad and confidence < self.confidence_threshold:
                        is_ad = False
                        logger.debug(f"段落 {i} 置信度不足: {confidence} < {self.confidence_threshold}")
                    
                    results.append(AdDetectionResult(
                        is_ad=is_ad,
                        confidence=confidence,
                        ad_type=item.get('ad_type', 'none'),
                        reason=item.get('reason', ''),
                        paragraph=para
                    ))
                else:
                    results.append(AdDetectionResult(
                        is_ad=False,
                        confidence=0.0,
                        ad_type="none",
                        reason="未找到检测结果",
                        paragraph=para
                    ))
            
            return results
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON 解析失败: {e}\n内容: {response.content[:200]}")
            return [AdDetectionResult(
                is_ad=False,
                confidence=0.0,
                ad_type="none",
                reason="JSON 解析失败",
                paragraph=p
            ) for p in paragraphs]
    
    def detect_single(self, paragraph: str) -> AdDetectionResult:
        """检测单个段落"""
        prompt = AD_DETECTION_PROMPT.format(paragraph=paragraph)
        response = self.llm.call(prompt)
        
        if not response.success:
            return AdDetectionResult(
                is_ad=False,
                confidence=0.0,
                ad_type="none",
                reason=f"LLM 错误: {response.error}",
                paragraph=paragraph
            )
        
        try:
            content = response.content.strip()
            if content.startswith('```'):
                content = content.split('\n', 1)[1] if '\n' in content else content
                content = content.rsplit('```', 1)[0] if '```' in content else content
            
            data = json.loads(content)
            is_ad = data.get('is_ad', False)
            confidence = data.get('confidence', 0.0)
            
            if is_ad and confidence < self.confidence_threshold:
                is_ad = False
            
            return AdDetectionResult(
                is_ad=is_ad,
                confidence=confidence,
                ad_type=data.get('ad_type', 'none'),
                reason=data.get('reason', ''),
                paragraph=paragraph
            )
        except json.JSONDecodeError:
            return AdDetectionResult(
                is_ad=False,
                confidence=0.0,
                ad_type="none",
                reason="JSON 解析失败",
                paragraph=paragraph
            )
    
    def stats(self) -> Dict:
        """获取统计信息"""
        detection_rate = self.detected_count / self.total_processed if self.total_processed > 0 else 0
        return {
            'enabled': self.enabled,
            'total_processed': self.total_processed,
            'detected_count': self.detected_count,
            'detection_rate': f"{detection_rate:.2%}"
        }


def remove_ads_from_text(text: str, results: List[AdDetectionResult]) -> Tuple[str, Dict]:
    """从文本中移除广告"""
    stats = {
        'total_removed': 0,
        'by_type': {}
    }
    
    # 按段落分割文本
    paragraphs = re.split(r'\n\s*\n', text)
    
    # 创建需要移除的段落集合
    ads_to_remove = set()
    for result in results:
        if result.is_ad:
            # 标准化广告文本用于匹配
            ad_normalized = re.sub(r'\s+', '', result.paragraph.strip())
            ads_to_remove.add(ad_normalized)
    
    # 过滤掉广告段落
    kept_paragraphs = []
    for para in paragraphs:
        para_normalized = re.sub(r'\s+', '', para.strip())
        if para_normalized not in ads_to_remove:
            kept_paragraphs.append(para)
        else:
            stats['total_removed'] += 1
            # 记录广告类型
            for result in results:
                if result.is_ad:
                    result_normalized = re.sub(r'\s+', '', result.paragraph.strip())
                    if result_normalized == para_normalized:
                        stats['by_type'][result.ad_type] = stats['by_type'].get(result.ad_type, 0) + 1
                        break
    
    # 重新组合文本
    text = '\n\n'.join(kept_paragraphs)
    
    return text, stats
