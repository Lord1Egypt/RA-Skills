#!/usr/bin/env python3
"""
百度百科内容提取器
用于从百度百科网页提取结构化知识
"""

import urllib.request
import urllib.parse
import re
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class BaiduBaikeExtractor:
    """百度百科内容提取器"""
    
    def __init__(self, config=None):
        self.config = config or {
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "timeout_seconds": 15,
            "max_retries": 3,
            "cache_enabled": True,
            "cache_ttl_hours": 24,
            "respect_robots": True
        }
        
        # 简单内存缓存
        self.cache = {}
        
        # 常见知识类型模式
        self.knowledge_patterns = {
            "definition": [r"([^。]+是指[^。]+)", r"([^。]+是[^。]+的一种[^。]+)", r"([^。]+定义为[^。]+)"],
            "feature": [r"特点[：:]([^。]+)", r"特征[：:]([^。]+)", r"特性[：:]([^。]+)"],
            "application": [r"应用[：:]([^。]+)", r"用途[：:]([^。]+)", r"使用场景[：:]([^。]+)"],
            "advantage": [r"优点[：:]([^。]+)", r"优势[：:]([^。]+)", r"好处[：:]([^。]+)"],
            "disadvantage": [r"缺点[：:]([^。]+)", r"不足[：:]([^。]+)", r"局限性[：:]([^。]+)"]
        }
    
    def extract_knowledge(self, topic: str) -> Dict:
        """提取主题知识"""
        print(f"🔍 从百度百科提取知识: {topic}")
        
        cache_key = f"baike_{topic}"
        
        # 检查缓存
        if self.config["cache_enabled"] and cache_key in self.cache:
            cached_time, cached_data = self.cache[cache_key]
            if time.time() - cached_time < self.config["cache_ttl_hours"] * 3600:
                print(f"   使用缓存数据")
                return cached_data
        
        try:
            # 获取百度百科页面
            html_content = self._fetch_baike_page(topic)
            
            if not html_content:
                return self._create_error_result(topic, "无法获取页面内容")
            
            # 提取结构化知识
            knowledge = self._extract_structured_knowledge(topic, html_content)
            
            # 提取基本信息
            basic_info = self._extract_basic_info(html_content)
            
            # 提取关键段落
            key_paragraphs = self._extract_key_paragraphs(html_content)
            
            # 提取分类标签
            categories = self._extract_categories(html_content)
            
            # 构建结果
            result = {
                "topic": topic,
                "source": "baidu_baike",
                "extracted_at": datetime.now().isoformat(),
                "url": self._construct_baike_url(topic),
                "basic_info": basic_info,
                "knowledge_structure": knowledge,
                "key_paragraphs": key_paragraphs,
                "categories": categories,
                "content_length": len(html_content),
                "extraction_quality": self._calculate_extraction_quality(knowledge, key_paragraphs)
            }
            
            # 缓存结果
            if self.config["cache_enabled"]:
                self.cache[cache_key] = (time.time(), result)
            
            print(f"   提取完成: {len(key_paragraphs)}个关键段落, {len(knowledge)}个知识结构")
            
            return result
            
        except Exception as e:
            print(f"   ❌ 提取失败: {e}")
            return self._create_error_result(topic, str(e))
    
    def _fetch_baike_page(self, topic: str, retry_count: int = 0) -> Optional[str]:
        """获取百度百科页面"""
        try:
            url = self._construct_baike_url(topic)
            
            headers = {
                'User-Agent': self.config["user_agent"],
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1'
            }
            
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, timeout=self.config["timeout_seconds"]) as response:
                if response.status == 200:
                    content = response.read()
                    
                    # 尝试多种编码
                    for encoding in ['utf-8', 'gbk', 'gb2312', 'iso-8859-1']:
                        try:
                            html = content.decode(encoding)
                            if '百度百科' in html and topic in html:
                                return html
                        except:
                            continue
                    
                    # 如果所有编码都失败，使用errors='ignore'
                    return content.decode('utf-8', errors='ignore')
                else:
                    print(f"   HTTP错误: {response.status}")
                    return None
                    
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"   页面不存在: {topic}")
                return None
            elif retry_count < self.config["max_retries"]:
                print(f"   HTTP错误 {e.code}, 重试 {retry_count + 1}/{self.config['max_retries']}")
                time.sleep(1)
                return self._fetch_baike_page(topic, retry_count + 1)
            else:
                print(f"   HTTP错误 {e.code}, 重试次数用尽")
                return None
                
        except Exception as e:
            if retry_count < self.config["max_retries"]:
                print(f"   网络错误: {e}, 重试 {retry_count + 1}/{self.config['max_retries']}")
                time.sleep(1)
                return self._fetch_baike_page(topic, retry_count + 1)
            else:
                print(f"   网络错误: {e}, 重试次数用尽")
                return None
    
    def _construct_baike_url(self, topic: str) -> str:
        """构造百度百科URL"""
        encoded_topic = urllib.parse.quote(topic)
        return f"https://baike.baidu.com/item/{encoded_topic}"
    
    def _extract_structured_knowledge(self, topic: str, html: str) -> Dict:
        """提取结构化知识"""
        knowledge = {}
        
        # 清理HTML标签
        text = self._clean_html(html)
        
        # 提取各种类型的知识
        for knowledge_type, patterns in self.knowledge_patterns.items():
            matches = []
            for pattern in patterns:
                found = re.findall(pattern, text)
                matches.extend(found)
            
            if matches:
                # 去重并限制数量
                unique_matches = list(set(matches))[:5]  # 每种类型最多5条
                knowledge[knowledge_type] = unique_matches
        
        # 提取定义（特殊处理）
        if "definition" not in knowledge:
            # 尝试从开头段落提取定义
            first_paragraphs = text[:500]  # 前500字符
            definition_candidates = re.findall(rf"{topic}[，,、].*?。", first_paragraphs)
            if definition_candidates:
                knowledge["definition"] = definition_candidates[:3]
        
        return knowledge
    
    def _extract_basic_info(self, html: str) -> Dict:
        """提取基本信息"""
        info = {}
        
        # 提取标题
        title_match = re.search(r'<title>(.*?)</title>', html)
        if title_match:
            info["title"] = title_match.group(1).replace(' - 百度百科', '')
        
        # 提取描述
        desc_match = re.search(r'<meta name="description" content="(.*?)"', html)
        if desc_match:
            info["description"] = desc_match.group(1)
        
        # 提取关键词
        keywords_match = re.search(r'<meta name="keywords" content="(.*?)"', html)
        if keywords_match:
            info["keywords"] = [k.strip() for k in keywords_match.group(1).split(',')]
        
        return info
    
    def _extract_key_paragraphs(self, html: str, max_paragraphs: int = 10) -> List[Dict]:
        """提取关键段落"""
        paragraphs = []
        
        # 清理HTML并分割段落
        text = self._clean_html(html)
        raw_paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        
        # 过滤和评分段落
        for para in raw_paragraphs:
            if len(para) < 20 or len(para) > 500:  # 太短或太长
                continue
            
            # 计算段落质量分数
            score = self._calculate_paragraph_score(para)
            
            if score > 0.3:  # 质量阈值
                paragraphs.append({
                    "content": para,
                    "score": score,
                    "length": len(para)
                })
        
        # 按分数排序并限制数量
        paragraphs.sort(key=lambda x: x["score"], reverse=True)
        return paragraphs[:max_paragraphs]
    
    def _extract_categories(self, html: str) -> List[str]:
        """提取分类标签"""
        categories = []
        
        # 查找分类标签
        category_patterns = [
            r'category:"(.*?)"',
            r'分类.*?[:：](.*?)<',
            r'<a[^>]*?分类[^>]*?>(.*?)</a>'
        ]
        
        for pattern in category_patterns:
            matches = re.findall(pattern, html)
            for match in matches:
                # 清理分类标签
                clean_cats = [cat.strip() for cat in match.split('·') if cat.strip()]
                categories.extend(clean_cats)
        
        # 去重
        return list(set(categories))[:10]  # 最多10个分类
    
    def _clean_html(self, html: str) -> str:
        """清理HTML标签"""
        # 移除脚本和样式
        html = re.sub(r'<script.*?>.*?</script>', '', html, flags=re.DOTALL)
        html = re.sub(r'<style.*?>.*?</style>', '', html, flags=re.DOTALL)
        
        # 移除HTML标签
        html = re.sub(r'<[^>]+>', ' ', html)
        
        # 替换多个空白字符为单个空格
        html = re.sub(r'\s+', ' ', html)
        
        # 替换HTML实体
        html = html.replace('&nbsp;', ' ')
        html = html.replace('&lt;', '<')
        html = html.replace('&gt;', '>')
        html = html.replace('&amp;', '&')
        html = html.replace('&quot;', '"')
        html = html.replace('&apos;', "'")
        
        return html.strip()
    
    def _calculate_paragraph_score(self, paragraph: str) -> float:
        """计算段落质量分数"""
        score = 0.0
        
        # 长度适中（50-300字）
        length = len(paragraph)
        if 50 <= length <= 300:
            score += 0.3
        elif 20 <= length < 50 or 300 < length <= 500:
            score += 0.1
        
        # 包含标点符号
        if any(punc in paragraph for punc in ['。', '；', '，', '：']):
            score += 0.2
        
        # 不包含无关字符
        if not any(unwanted in paragraph for unwanted in ['点击查看', '查看更多', '相关视频', '广告']):
            score += 0.2
        
        # 包含知识性词汇
        knowledge_words = ['定义', '特点', '应用', '原理', '方法', '技术', '系统', '算法']
        if any(word in paragraph for word in knowledge_words):
            score += 0.3
        
        return min(score, 1.0)
    
    def _calculate_extraction_quality(self, knowledge: Dict, paragraphs: List[Dict]) -> float:
        """计算提取质量"""
        quality = 0.0
        
        # 知识结构完整性
        if knowledge:
            quality += 0.3
            if len(knowledge) >= 3:  # 至少3种知识类型
                quality += 0.2
        
        # 关键段落数量
        if paragraphs:
            quality += 0.2
            if len(paragraphs) >= 5:  # 至少5个关键段落
                quality += 0.2
        
        # 段落平均质量
        if paragraphs:
            avg_score = sum(p["score"] for p in paragraphs) / len(paragraphs)
            quality += avg_score * 0.1
        
        return min(quality, 1.0)
    
    def _create_error_result(self, topic: str, error: str) -> Dict:
        """创建错误结果"""
        return {
            "topic": topic,
            "source": "baidu_baike",
            "extracted_at": datetime.now().isoformat(),
            "url": self._construct_baike_url(topic),
            "error": error,
            "extraction_quality": 0.0
        }


# 测试函数
def test_baidu_baike_extractor():
    """测试百度百科提取器"""
    print("=" * 60)
    print("🔬 百度百科内容提取器测试")
    print("=" * 60)
    
    extractor = BaiduBaikeExtractor()
    
    test_topics = ["职业技能", "人工智能", "机器学习"]
    
    for topic in test_topics:
        print(f"\n📚 提取主题: {topic}")
        print("-" * 40)
        
        start_time = time.time()
        result = extractor.extract_knowledge(topic)
        elapsed = time.time() - start_time
        
        if "error" in result:
            print(f"   ❌ 提取失败: {result['error']}")
        else:
            print(f"   ✅ 提取成功 ({elapsed:.1f}秒)")
            print(f"      质量分数: {result.get('extraction_quality', 0):.2f}")
            print(f"      关键段落: {len(result.get('key_paragraphs', []))}个")
            print(f"      知识类型: {len(result.get('knowledge_structure', {}))}种")
            
            # 显示一个示例段落
            paragraphs = result.get('key_paragraphs', [])
            if paragraphs:
                print(f"      示例段落: {paragraphs[0]['content'][:100]}...")
    
    print("\n" + "=" * 60)
    print("✅ 测试完成")
    print("=" * 60)


if __name__ == "__main__":
    test_baidu_baike_extractor()