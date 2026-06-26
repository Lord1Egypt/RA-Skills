#!/usr/bin/env python3
"""
实时RAG验证集成模块
集成到权威知识图谱构建器中
"""

import wikipediaapi
import arxiv
import requests
from datetime import datetime
import json
import time

class RealTimeRAGValidator:
    """实时RAG验证器 - 集成到知识图谱构建器"""
    
    def __init__(self, config=None):
        """初始化验证器"""
        self.config = config or {
            "wikipedia_language": "zh",
            "arxiv_max_results": 3,
            "timeout_seconds": 10,
            "cache_enabled": True,
            "cache_ttl_seconds": 3600  # 1小时缓存
        }
        
        # 初始化API客户端
        self.wikipedia = wikipediaapi.Wikipedia(
            language=self.config["wikipedia_language"],
            user_agent="OpenClaw-KG-Builder/1.0"
        )
        
        self.arxiv_client = arxiv.Client(
            page_size=self.config["arxiv_max_results"],
            delay_seconds=1.0,
            num_retries=3
        )
        
        # 简单内存缓存
        self.cache = {}
        
    def validate_knowledge_node(self, node_name, node_description):
        """验证知识节点的权威性"""
        cache_key = f"validate_{node_name}"
        
        # 检查缓存
        if self.config["cache_enabled"] and cache_key in self.cache:
            cached_data = self.cache[cache_key]
            if time.time() - cached_data["timestamp"] < self.config["cache_ttl_seconds"]:
                print(f"  🔍 使用缓存验证: {node_name}")
                return cached_data["data"]
        
        print(f"  🔍 实时验证知识节点: {node_name}")
        
        validation_results = {
            "node_name": node_name,
            "validation_time": datetime.now().isoformat(),
            "wikipedia": self._validate_with_wikipedia(node_name),
            "arxiv": self._validate_with_arxiv(node_name),
            "standards": self._validate_with_standards(node_name),
            "confidence_score": 0.0
        }
        
        # 计算置信度分数
        validation_results["confidence_score"] = self._calculate_confidence(validation_results)
        
        # 缓存结果
        if self.config["cache_enabled"]:
            self.cache[cache_key] = {
                "data": validation_results,
                "timestamp": time.time()
            }
        
        return validation_results
    
    def _validate_with_wikipedia(self, topic):
        """使用Wikipedia验证"""
        try:
            page = self.wikipedia.page(topic)
            if page.exists():
                return {
                    "exists": True,
                    "title": page.title,
                    "summary": page.summary[:300] + "..." if len(page.summary) > 300 else page.summary,
                    "url": page.fullurl,
                    "word_count": page.text.count(' ') + 1 if page.text else 0
                }
            else:
                # 尝试搜索相关页面
                search_results = self.wikipedia.search(topic)
                if search_results:
                    return {
                        "exists": False,
                        "search_results": search_results[:3],
                        "suggestion": f"找到相关页面: {', '.join(search_results[:3])}"
                    }
        except Exception as e:
            print(f"  ⚠️  Wikipedia验证失败: {e}")
        
        return {"exists": False, "error": "验证失败"}
    
    def _validate_with_arxiv(self, topic):
        """使用arXiv验证"""
        try:
            search = arxiv.Search(
                query=topic,
                max_results=self.config["arxiv_max_results"],
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            results = []
            for paper in self.arxiv_client.results(search):
                results.append({
                    "title": paper.title,
                    "authors": [str(author) for author in paper.authors],
                    "summary": paper.summary[:200] + "..." if len(paper.summary) > 200 else paper.summary,
                    "published": paper.published.isoformat() if paper.published else None,
                    "pdf_url": paper.pdf_url,
                    "primary_category": paper.primary_category
                })
            
            return {
                "found": len(results) > 0,
                "count": len(results),
                "papers": results
            }
            
        except Exception as e:
            print(f"  ⚠️  arXiv验证失败: {e}")
            return {"found": False, "error": str(e)}
    
    def _validate_with_standards(self, topic):
        """验证国家标准（模拟）"""
        # 这里可以集成国家标准API
        # 目前模拟返回
        standard_keywords = ["GB/T", "国家标准", "技术规范", "行业标准"]
        
        has_standard = any(keyword in topic for keyword in standard_keywords)
        
        if has_standard:
            return {
                "has_standard": True,
                "suggestion": "该主题可能涉及国家标准，建议查询国家标准全文公开系统"
            }
        else:
            return {
                "has_standard": False,
                "suggestion": "未检测到明确的国家标准关联"
            }
    
    def _calculate_confidence(self, validation_results):
        """计算权威性置信度分数"""
        score = 0.0
        
        # Wikipedia存在性（40%）
        if validation_results["wikipedia"].get("exists", False):
            score += 0.4
        
        # arXiv论文数量（30%）
        arxiv_data = validation_results["arxiv"]
        if arxiv_data.get("found", False):
            paper_count = arxiv_data.get("count", 0)
            if paper_count >= 3:
                score += 0.3
            elif paper_count >= 1:
                score += 0.15
        
        # 国家标准关联（30%）
        if validation_results["standards"].get("has_standard", False):
            score += 0.3
        
        return min(score, 1.0)
    
    def enhance_knowledge_node(self, node, validation_results):
        """用验证结果增强知识节点"""
        enhanced_node = node.copy()
        
        # 添加验证信息
        enhanced_node["authoritative_validation"] = {
            "validated_at": validation_results["validation_time"],
            "confidence_score": validation_results["confidence_score"],
            "sources_checked": {
                "wikipedia": validation_results["wikipedia"].get("exists", False),
                "arxiv": validation_results["arxiv"].get("found", False),
                "standards": validation_results["standards"].get("has_standard", False)
            },
            "recommendations": self._generate_recommendations(validation_results)
        }
        
        # 根据置信度调整节点属性
        if validation_results["confidence_score"] >= 0.7:
            enhanced_node["authoritative_level"] = "high"
            enhanced_node["learning_priority"] = "essential"
        elif validation_results["confidence_score"] >= 0.4:
            enhanced_node["authoritative_level"] = "medium"
            enhanced_node["learning_priority"] = "recommended"
        else:
            enhanced_node["authoritative_level"] = "low"
            enhanced_node["learning_priority"] = "optional"
        
        return enhanced_node
    
    def _generate_recommendations(self, validation_results):
        """生成学习建议"""
        recommendations = []
        
        # Wikipedia建议
        wiki_data = validation_results["wikipedia"]
        if wiki_data.get("exists", False):
            recommendations.append({
                "type": "wikipedia",
                "priority": "high",
                "action": f"阅读Wikipedia页面: {wiki_data.get('title', '')}",
                "url": wiki_data.get("url", "")
            })
        elif wiki_data.get("search_results"):
            recommendations.append({
                "type": "wikipedia",
                "priority": "medium",
                "action": f"搜索相关页面: {', '.join(wiki_data['search_results'][:2])}"
            })
        
        # arXiv建议
        arxiv_data = validation_results["arxiv"]
        if arxiv_data.get("found", False):
            paper_count = arxiv_data.get("count", 0)
            recommendations.append({
                "type": "arxiv",
                "priority": "medium",
                "action": f"参考{paper_count}篇相关学术论文",
                "papers": arxiv_data.get("papers", [])[:2]
            })
        
        # 国家标准建议
        standards_data = validation_results["standards"]
        if standards_data.get("has_standard", False):
            recommendations.append({
                "type": "standards",
                "priority": "high",
                "action": "查询相关国家标准",
                "suggestion": standards_data.get("suggestion", "")
            })
        
        return recommendations
    
    def generate_validation_report(self, nodes_validations):
        """生成验证报告"""
        report = {
            "generated_at": datetime.now().isoformat(),
            "total_nodes": len(nodes_validations),
            "validation_summary": {
                "high_confidence": 0,
                "medium_confidence": 0,
                "low_confidence": 0
            },
            "source_coverage": {
                "wikipedia": 0,
                "arxiv": 0,
                "standards": 0
            },
            "nodes_details": []
        }
        
        for node_name, validation in nodes_validations.items():
            # 统计置信度
            score = validation.get("confidence_score", 0)
            if score >= 0.7:
                report["validation_summary"]["high_confidence"] += 1
            elif score >= 0.4:
                report["validation_summary"]["medium_confidence"] += 1
            else:
                report["validation_summary"]["low_confidence"] += 1
            
            # 统计来源覆盖
            if validation.get("wikipedia", {}).get("exists", False):
                report["source_coverage"]["wikipedia"] += 1
            if validation.get("arxiv", {}).get("found", False):
                report["source_coverage"]["arxiv"] += 1
            if validation.get("standards", {}).get("has_standard", False):
                report["source_coverage"]["standards"] += 1
            
            # 节点详情
            report["nodes_details"].append({
                "node_name": node_name,
                "confidence_score": score,
                "authoritative_level": "high" if score >= 0.7 else "medium" if score >= 0.4 else "low",
                "sources_found": [
                    source for source, data in [
                        ("wikipedia", validation.get("wikipedia", {}).get("exists", False)),
                        ("arxiv", validation.get("arxiv", {}).get("found", False)),
                        ("standards", validation.get("standards", {}).get("has_standard", False))
                    ] if data
                ]
            })
        
        return report


# 集成到知识图谱构建器的示例
def integrate_rag_into_kg_builder():
    """演示如何集成到知识图谱构建器"""
    
    print("=" * 60)
    print("🔗 实时RAG验证集成演示")
    print("=" * 60)
    
    # 创建验证器
    validator = RealTimeRAGValidator()
    
    # 示例知识节点
    sample_nodes = [
        {"id": "node_001", "name": "职业技能", "description": "系统架构账本技术"},
        {"id": "node_002", "name": "技术组件", "description": "自动执行的合约代码"},
        {"id": "node_003", "name": "协调算法", "description": "系统架构系统一致性算法"}
    ]
    
    print("📊 验证知识节点权威性:")
    nodes_validations = {}
    enhanced_nodes = []
    
    for node in sample_nodes:
        print(f"\n🔹 验证: {node['name']}")
        
        # 实时验证
        validation = validator.validate_knowledge_node(node["name"], node["description"])
        
        # 增强节点
        enhanced_node = validator.enhance_knowledge_node(node, validation)
        
        nodes_validations[node["name"]] = validation
        enhanced_nodes.append(enhanced_node)
        
        print(f"   置信度: {validation['confidence_score']:.2f}")
        print(f"   Wikipedia: {'✅' if validation['wikipedia'].get('exists') else '❌'}")
        print(f"   arXiv论文: {validation['arxiv'].get('count', 0)}篇")
    
    # 生成验证报告
    report = validator.generate_validation_report(nodes_validations)
    
    print("\n" + "=" * 60)
    print("📈 验证报告摘要")
    print("=" * 60)
    
    print(f"总节点数: {report['total_nodes']}")
    print(f"高置信度: {report['validation_summary']['high_confidence']}")
    print(f"中置信度: {report['validation_summary']['medium_confidence']}")
    print(f"低置信度: {report['validation_summary']['low_confidence']}")
    
    print(f"\n来源覆盖:")
    print(f"  Wikipedia: {report['source_coverage']['wikipedia']}/{report['total_nodes']}")
    print(f"  arXiv: {report['source_coverage']['arxiv']}/{report['total_nodes']}")
    print(f"  国家标准: {report['source_coverage']['standards']}/{report['total_nodes']}")
    
    print(f"\n🎯 集成完成！知识节点已增强权威性验证。")
    
    return enhanced_nodes, report


if __name__ == "__main__":
    # 运行演示
    enhanced_nodes, report = integrate_rag_into_kg_builder()
    
    # 保存示例结果
    output_dir = "/tmp/rag_integration_demo"
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f"{output_dir}/enhanced_nodes.json", "w", encoding="utf-8") as f:
        json.dump(enhanced_nodes, f, ensure_ascii=False, indent=2)
    
    with open(f"{output_dir}/validation_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 结果已保存到: {output_dir}/")
    print("  - enhanced_nodes.json: 增强后的知识节点")
    print("  - validation_report.json: 验证报告")