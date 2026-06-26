#!/usr/bin/env python3
"""
简化版百度百科提取器
使用更简单的提取逻辑
"""

import urllib.request
import urllib.parse
import re
import json
import time
from datetime import datetime

class SimpleBaikeExtractor:
    """简化版百度百科提取器"""
    
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    def get_baike_summary(self, topic):
        """获取百度百科摘要"""
        print(f"🔍 获取百度百科摘要: {topic}")
        
        try:
            # 构造URL
            encoded_topic = urllib.parse.quote(topic)
            url = f"https://baike.baidu.com/item/{encoded_topic}"
            
            # 发送请求
            headers = {'User-Agent': self.user_agent}
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8', errors='ignore')
                
                # 提取标题
                title_match = re.search(r'<title>(.*?)</title>', html)
                title = title_match.group(1).replace(' - 百度百科', '') if title_match else topic
                
                # 提取描述
                desc_match = re.search(r'<meta name="description" content="(.*?)"', html)
                description = desc_match.group(1) if desc_match else ""
                
                # 简单提取正文内容（更简单的方法）
                # 查找包含主题的段落
                paragraphs = []
                
                # 方法1：查找div class="lemma-summary"
                summary_match = re.search(r'<div class="lemma-summary"[^>]*>(.*?)</div>', html, re.DOTALL)
                if summary_match:
                    summary_text = re.sub(r'<[^>]+>', '', summary_match.group(1))
                    summary_text = re.sub(r'\s+', ' ', summary_text).strip()
                    if summary_text:
                        paragraphs.append(summary_text)
                
                # 方法2：查找包含主题的文本段落
                if not paragraphs:
                    # 提取所有文本内容
                    text_content = re.sub(r'<[^>]+>', ' ', html)
                    text_content = re.sub(r'\s+', ' ', text_content)
                    
                    # 查找包含主题的句子
                    sentences = re.split(r'[。！？；]', text_content)
                    relevant_sentences = [s.strip() for s in sentences if topic in s and len(s) > 10]
                    paragraphs.extend(relevant_sentences[:5])  # 最多5句
                
                # 方法3：如果还找不到，使用描述
                if not paragraphs and description:
                    paragraphs.append(description)
                
                result = {
                    "topic": topic,
                    "title": title,
                    "url": url,
                    "description": description,
                    "paragraphs": paragraphs,
                    "paragraph_count": len(paragraphs),
                    "retrieved_at": datetime.now().isoformat(),
                    "success": True
                }
                
                print(f"   ✅ 获取成功: {len(paragraphs)}个段落")
                return result
                
        except Exception as e:
            print(f"   ❌ 获取失败: {e}")
            return {
                "topic": topic,
                "success": False,
                "error": str(e),
                "retrieved_at": datetime.now().isoformat()
            }
    
    def extract_for_knowledge_graph(self, topic):
        """为知识图谱提取信息"""
        result = self.get_baike_summary(topic)
        
        if not result.get("success", False):
            return result
        
        # 分析提取的内容
        paragraphs = result.get("paragraphs", [])
        
        # 提取关键信息
        key_info = {
            "definition": "",
            "features": [],
            "applications": []
        }
        
        for para in paragraphs:
            para_lower = para.lower()
            
            # 提取定义（通常在第一段）
            if not key_info["definition"] and ("是指" in para or "定义为" in para or "是" in topic):
                key_info["definition"] = para
            
            # 提取特点
            if "特点" in para or "特征" in para or "特性" in para:
                # 简单提取特点列表
                features = re.findall(r'[1-9][、.]\s*([^，。]+)', para)
                if features:
                    key_info["features"].extend(features)
                else:
                    # 提取冒号后的内容
                    feature_match = re.search(r'[：:]\s*([^。]+)', para)
                    if feature_match:
                        key_info["features"].append(feature_match.group(1))
            
            # 提取应用
            if "应用" in para or "用途" in para or "使用" in para:
                app_match = re.search(r'[：:]\s*([^。]+)', para)
                if app_match:
                    key_info["applications"].append(app_match.group(1))
        
        # 如果没有找到定义，使用第一个段落
        if not key_info["definition"] and paragraphs:
            key_info["definition"] = paragraphs[0]
        
        # 添加到结果
        result["key_info"] = key_info
        
        return result


def test_extractor():
    """测试提取器"""
    print("=" * 60)
    print("🔬 简化版百度百科提取器测试")
    print("=" * 60)
    
    extractor = SimpleBaikeExtractor()
    
    test_topics = ["职业技能", "人工智能", "协调算法"]
    
    all_results = []
    
    for topic in test_topics:
        print(f"\n📚 测试主题: {topic}")
        print("-" * 40)
        
        start_time = time.time()
        result = extractor.extract_for_knowledge_graph(topic)
        elapsed = time.time() - start_time
        
        if result.get("success", False):
            print(f"   ✅ 成功 ({elapsed:.1f}秒)")
            print(f"      标题: {result.get('title', 'N/A')}")
            print(f"      段落数: {result.get('paragraph_count', 0)}")
            
            key_info = result.get("key_info", {})
            if key_info.get("definition"):
                print(f"      定义: {key_info['definition'][:80]}...")
            if key_info.get("features"):
                print(f"      特点: {len(key_info['features'])}个")
            if key_info.get("applications"):
                print(f"      应用: {len(key_info['applications'])}个")
        else:
            print(f"   ❌ 失败: {result.get('error', '未知错误')}")
        
        all_results.append(result)
    
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    
    success_count = sum(1 for r in all_results if r.get("success", False))
    total_count = len(all_results)
    
    print(f"成功: {success_count}/{total_count}")
    
    if success_count >= 2:
        print("✅ 提取器基本可用")
        print("   可以用于RAG集成")
    else:
        print("❌ 提取器需要改进")
        print("   需要调整提取逻辑")
    
    # 保存测试结果
    output_file = "/home/wzp/.openclaw/workspace/test_results/baike_extractor_test.json"
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "test_time": datetime.now().isoformat(),
            "results": all_results,
            "summary": {
                "success_count": success_count,
                "total_count": total_count
            }
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 测试结果已保存到: {output_file}")
    print("=" * 60)


if __name__ == "__main__":
    test_extractor()