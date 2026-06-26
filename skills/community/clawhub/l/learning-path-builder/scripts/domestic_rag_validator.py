#!/usr/bin/env python3
"""
国内优先RAG验证器
优先使用国内开放资源验证知识权威性
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional

from simple_baike_extractor import SimpleBaikeExtractor

class DomesticRAGValidator:
    """国内优先RAG验证器"""
    
    def __init__(self, config=None):
        self.config = config or {
            "priority_order": ["baidu_baike", "national_data", "mooc_platforms"],
            "timeout_seconds": 10,
            "cache_enabled": True,
            "min_confidence_threshold": 0.3,
            "max_retries": 2
        }
        
        # 初始化提取器
        self.baike_extractor = SimpleBaikeExtractor()
        
        # 缓存
        self.cache = {}
        
        # 验证统计
        self.stats = {
            "total_validations": 0,
            "successful_validations": 0,
            "failed_validations": 0,
            "resource_usage": {}
        }
    
    def validate_knowledge_node(self, node_name: str, node_description: str = "") -> Dict:
        """验证知识节点"""
        print(f"🔍 验证知识节点: {node_name}")
        self.stats["total_validations"] += 1
        
        cache_key = f"validate_{node_name}"
        
        # 检查缓存
        if self.config["cache_enabled"] and cache_key in self.cache:
            cached_time, cached_data = self.cache[cache_key]
            if time.time() - cached_time < 3600:  # 1小时缓存
                print(f"   使用缓存验证")
                self.stats["successful_validations"] += 1
                return cached_data
        
        validation_results = {
            "node_name": node_name,
            "validation_time": datetime.now().isoformat(),
            "sources_checked": {},
            "confidence_score": 0.0,
            "authoritative_content": {},
            "recommendations": []
        }
        
        # 按照优先级顺序验证
        for source in self.config["priority_order"]:
            print(f"   检查来源: {source}")
            
            try:
                if source == "baidu_baike":
                    source_result = self._validate_with_baidu_baike(node_name)
                elif source == "national_data":
                    source_result = self._validate_with_national_data(node_name)
                elif source == "mooc_platforms":
                    source_result = self._validate_with_mooc_platforms(node_name)
                else:
                    source_result = {"available": False, "error": "未知来源"}
                
                validation_results["sources_checked"][source] = source_result
                
                # 更新统计
                if source not in self.stats["resource_usage"]:
                    self.stats["resource_usage"][source] = 0
                self.stats["resource_usage"][source] += 1
                
                # 如果找到足够信息，可以提前结束
                if source_result.get("available", False) and source_result.get("confidence", 0) >= 0.5:
                    print(f"      ✅ 找到足够信息")
                    break
                    
            except Exception as e:
                print(f"      ❌ 验证失败: {e}")
                validation_results["sources_checked"][source] = {
                    "available": False,
                    "error": str(e)
                }
        
        # 计算总体置信度
        validation_results["confidence_score"] = self._calculate_overall_confidence(
            validation_results["sources_checked"]
        )
        
        # 提取权威内容
        validation_results["authoritative_content"] = self._extract_authoritative_content(
            validation_results["sources_checked"]
        )
        
        # 生成建议
        validation_results["recommendations"] = self._generate_recommendations(
            validation_results["sources_checked"],
            validation_results["confidence_score"]
        )
        
        # 确定权威等级
        validation_results["authoritative_level"] = self._determine_authoritative_level(
            validation_results["confidence_score"]
        )
        
        # 缓存结果
        if self.config["cache_enabled"]:
            self.cache[cache_key] = (time.time(), validation_results)
        
        if validation_results["confidence_score"] >= self.config["min_confidence_threshold"]:
            print(f"   验证成功 - 置信度: {validation_results['confidence_score']:.2f}")
            self.stats["successful_validations"] += 1
        else:
            print(f"   验证失败 - 置信度: {validation_results['confidence_score']:.2f}")
            self.stats["failed_validations"] += 1
        
        return validation_results
    
    def _validate_with_baidu_baike(self, topic: str) -> Dict:
        """使用百度百科验证"""
        try:
            result = self.baike_extractor.extract_for_knowledge_graph(topic)
            
            if result.get("success", False):
                # 计算百度百科置信度
                confidence = self._calculate_baike_confidence(result)
                
                return {
                    "available": True,
                    "confidence": confidence,
                    "content": {
                        "title": result.get("title", ""),
                        "description": result.get("description", ""),
                        "paragraphs": result.get("paragraphs", []),
                        "key_info": result.get("key_info", {})
                    },
                    "url": result.get("url", ""),
                    "note": "百度百科验证成功"
                }
            else:
                return {
                    "available": False,
                    "error": result.get("error", "未知错误"),
                    "confidence": 0.0
                }
                
        except Exception as e:
            return {
                "available": False,
                "error": str(e),
                "confidence": 0.0
            }
    
    def _validate_with_national_data(self, topic: str) -> Dict:
        """使用国家数据平台验证"""
        # 目前简单实现，后续可以扩展
        try:
            # 检查是否可能涉及统计数据
            statistical_keywords = ["数据", "统计", "指标", "增长率", "占比"]
            
            has_statistical = any(keyword in topic for keyword in statistical_keywords)
            
            if has_statistical:
                return {
                    "available": True,
                    "confidence": 0.4,
                    "content": {
                        "note": "该主题可能涉及统计数据，建议查询国家数据平台",
                        "suggestion": "访问 data.stats.gov.cn 获取官方数据"
                    },
                    "url": "http://data.stats.gov.cn",
                    "note": "建议查询官方统计数据"
                }
            else:
                return {
                    "available": False,
                    "confidence": 0.1,
                    "note": "该主题不涉及明显的统计数据"
                }
                
        except Exception as e:
            return {
                "available": False,
                "error": str(e),
                "confidence": 0.0
            }
    
    def _validate_with_mooc_platforms(self, topic: str) -> Dict:
        """使用慕课平台验证"""
        # 目前简单实现，后续可以扩展
        try:
            # 检查是否可能涉及教育内容
            education_keywords = ["学习", "课程", "教学", "教育", "培训", "教程"]
            
            has_educational = any(keyword in topic for keyword in education_keywords)
            
            if has_educational:
                return {
                    "available": True,
                    "confidence": 0.3,
                    "content": {
                        "note": "该主题可能涉及教育内容，建议查询慕课平台",
                        "platforms": ["中国大学MOOC", "学堂在线"],
                        "suggestion": "搜索相关课程获取系统学习资料"
                    },
                    "urls": ["https://www.icourse163.org", "https://www.xuetangx.com"],
                    "note": "建议查询慕课平台获取系统课程"
                }
            else:
                return {
                    "available": False,
                    "confidence": 0.1,
                    "note": "该主题不涉及明显的教育内容"
                }
                
        except Exception as e:
            return {
                "available": False,
                "error": str(e),
                "confidence": 0.0
            }
    
    def _calculate_baike_confidence(self, baike_result: Dict) -> float:
        """计算百度百科置信度"""
        confidence = 0.0
        
        if not baike_result.get("success", False):
            return 0.0
        
        # 段落数量（最多0.4分）
        paragraph_count = baike_result.get("paragraph_count", 0)
        if paragraph_count >= 5:
            confidence += 0.4
        elif paragraph_count >= 3:
            confidence += 0.3
        elif paragraph_count >= 1:
            confidence += 0.2
        
        # 关键信息完整性（最多0.3分）
        key_info = baike_result.get("key_info", {})
        if key_info.get("definition"):
            confidence += 0.2
        if key_info.get("features"):
            confidence += 0.05 * min(len(key_info["features"]), 2)  # 最多0.1分
        if key_info.get("applications"):
            confidence += 0.05 * min(len(key_info["applications"]), 2)  # 最多0.1分
        
        # 描述长度（最多0.3分）
        description = baike_result.get("description", "")
        if len(description) >= 100:
            confidence += 0.3
        elif len(description) >= 50:
            confidence += 0.2
        elif len(description) >= 20:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _calculate_overall_confidence(self, sources_checked: Dict) -> float:
        """计算总体置信度"""
        if not sources_checked:
            return 0.0
        
        total_confidence = 0.0
        source_count = 0
        
        for source, result in sources_checked.items():
            if result.get("available", False):
                confidence = result.get("confidence", 0.0)
                total_confidence += confidence
                source_count += 1
        
        if source_count == 0:
            return 0.0
        
        # 加权平均：百度百科权重更高
        weighted_sum = 0.0
        weight_sum = 0.0
        
        for source, result in sources_checked.items():
            if result.get("available", False):
                confidence = result.get("confidence", 0.0)
                
                # 分配权重
                if source == "baidu_baike":
                    weight = 0.6
                elif source == "national_data":
                    weight = 0.25
                elif source == "mooc_platforms":
                    weight = 0.15
                else:
                    weight = 0.1
                
                weighted_sum += confidence * weight
                weight_sum += weight
        
        if weight_sum > 0:
            return weighted_sum / weight_sum
        else:
            return total_confidence / source_count if source_count > 0 else 0.0
    
    def _extract_authoritative_content(self, sources_checked: Dict) -> Dict:
        """提取权威内容"""
        content = {
            "definitions": [],
            "key_points": [],
            "references": [],
            "learning_suggestions": []
        }
        
        for source, result in sources_checked.items():
            if result.get("available", False):
                source_content = result.get("content", {})
                
                # 从百度百科提取
                if source == "baidu_baike":
                    key_info = source_content.get("key_info", {})
                    
                    if key_info.get("definition"):
                        content["definitions"].append({
                            "source": "baidu_baike",
                            "content": key_info["definition"],
                            "confidence": result.get("confidence", 0.0)
                        })
                    
                    if key_info.get("features"):
                        for feature in key_info["features"]:
                            content["key_points"].append({
                                "source": "baidu_baike",
                                "type": "feature",
                                "content": feature
                            })
                    
                    if key_info.get("applications"):
                        for app in key_info["applications"]:
                            content["key_points"].append({
                                "source": "baidu_baike",
                                "type": "application",
                                "content": app
                            })
                
                # 添加引用
                url = result.get("url") or result.get("urls", [""])[0]
                if url:
                    content["references"].append({
                        "source": source,
                        "url": url,
                        "note": result.get("note", "")
                    })
                
                # 添加学习建议
                suggestion = source_content.get("suggestion") or result.get("note", "")
                if suggestion:
                    content["learning_suggestions"].append({
                        "source": source,
                        "suggestion": suggestion
                    })
        
        return content
    
    def _generate_recommendations(self, sources_checked: Dict, confidence_score: float) -> List[str]:
        """生成建议"""
        recommendations = []
        
        # 基于置信度的建议
        if confidence_score >= 0.7:
            recommendations.append("✅ 主题权威性高，可放心学习")
        elif confidence_score >= 0.4:
            recommendations.append("⚠️ 主题权威性中等，建议补充其他资源")
        else:
            recommendations.append("❌ 主题权威性较低，需要谨慎参考")
        
        # 基于来源的建议
        baike_result = sources_checked.get("baidu_baike", {})
        if not baike_result.get("available", False):
            recommendations.append("🔍 未找到百度百科页面，建议手动搜索验证")
        elif baike_result.get("confidence", 0) < 0.3:
            recommendations.append("📝 百度百科信息有限，建议查找更多资料")
        
        national_result = sources_checked.get("national_data", {})
        if national_result.get("available", False) and national_result.get("confidence", 0) >= 0.3:
            recommendations.append("📊 涉及统计数据，建议查询国家数据平台获取官方数据")
        
        mooc_result = sources_checked.get("mooc_platforms", {})
        if mooc_result.get("available", False) and mooc_result.get("confidence", 0) >= 0.3:
            recommendations.append("🎓 涉及教育内容，建议查询慕课平台获取系统课程")
        
        return recommendations
    
    def _determine_authoritative_level(self, confidence_score: float) -> str:
        """确定权威等级"""
        if confidence_score >= 0.7:
            return "high"
        elif confidence_score >= 0.4:
            return "medium"
        else:
            return "low"
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return self.stats
    
    def clear_cache(self):
        """清空缓存"""
        self.cache.clear()
        print("🗑️ 缓存已清空")


def test_validator():
    """测试验证器"""
    print("=" * 60)
    print("🔬 国内优先RAG验证器测试")
    print("=" * 60)
    
    validator = DomesticRAGValidator()
    
    test_nodes = [
        {"name": "职业技能", "description": "系统架构账本技术"},
        {"name": "技术组件", "description": "自动执行的合约代码"},
        {"name": "教育大数据", "description": "教育领域的数据分析"}
    ]
    
    all_results = []
    
    for node in test_nodes:
        print(f"\n📚 验证节点: {node['name']}")
        print("-" * 40)
        
        start_time = time.time()
        result = validator.validate_knowledge_node(node["name"], node["description"])
        elapsed = time.time() - start_time
        
        print(f"   验证时间: {elapsed:.1f}秒")
        print(f"   置信度: {result['confidence_score']:.2f}")
        print(f"   权威等级: {result['authoritative_level']}")
        
        # 显示来源检查结果
        for source, source_result in result["sources_checked"].items():
            status = "✅" if source_result.get("available", False) else "❌"
            confidence = source_result.get("confidence", 0.0)
            print(f"     {status} {source}: {confidence:.2f}")
        
        all_results.append(result)
    
    print("\n" + "=" * 60)
    print("📊 验证结果汇总")
    print("=" * 60)
    
    stats = validator.get_stats()
    print(f"总验证次数: {stats['total_validations']}")
    print(f"成功验证: {stats['successful_validations']}")
    print(f"失败验证: {stats['failed_validations']}")
    
    print(f"\n资源使用情况:")
    for source, count in stats['resource_usage'].items():
        print(f"  {source}: {count}次")
    
    # 保存测试结果
    output_file = "/home/wzp/.openclaw/workspace/test_results/domestic_rag_validator_test.json"
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "test_time": datetime.now().isoformat(),
            "results": all_results,
            "stats": stats
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 测试结果已保存到: {output_file}")
    print("=" * 60)
    print("✅ 国内优先RAG验证器测试完成")


if __name__ == "__main__":
    test_validator()