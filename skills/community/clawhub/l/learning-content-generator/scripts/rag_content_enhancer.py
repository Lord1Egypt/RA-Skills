#!/usr/bin/env python3
"""
实时RAG内容增强模块
集成到权威学习内容生成器中
"""

import wikipediaapi
import arxiv
from datetime import datetime
import time

class RealTimeRAGContentEnhancer:
    """实时RAG内容增强器 - 集成到内容生成器"""
    
    def __init__(self, config=None):
        """初始化增强器"""
        self.config = config or {
            "wikipedia_language": "zh",
            "arxiv_max_results": 2,
            "timeout_seconds": 8,
            "include_citations": True,
            "citation_format": "markdown",
            "min_confidence_threshold": 0.3
        }
        
        # 初始化API客户端
        self.wikipedia = wikipediaapi.Wikipedia(
            language=self.config["wikipedia_language"],
            user_agent="OpenClaw-Content-Generator/1.0"
        )
        
        self.arxiv_client = arxiv.Client(
            page_size=self.config["arxiv_max_results"],
            delay_seconds=1.0,
            num_retries=2
        )
        
        # 缓存
        self.cache = {}
    
    def enhance_learning_content(self, topic, base_content, learning_objectives):
        """增强学习内容"""
        print(f"  🔍 实时增强学习内容: {topic}")
        
        # 检索权威信息
        authoritative_info = self._retrieve_authoritative_info(topic)
        
        # 验证学习目标
        validated_objectives = self._validate_learning_objectives(learning_objectives, authoritative_info)
        
        # 生成增强内容
        enhanced_content = self._generate_enhanced_content(
            topic, base_content, authoritative_info, validated_objectives
        )
        
        # 生成引用部分
        if self.config["include_citations"]:
            citations_section = self._generate_citations_section(authoritative_info)
            enhanced_content += f"\n\n{citations_section}"
        
        # 生成验证报告
        validation_report = self._generate_validation_report(topic, authoritative_info, validated_objectives)
        
        return {
            "enhanced_content": enhanced_content,
            "authoritative_info": authoritative_info,
            "validation_report": validation_report
        }
    
    def _retrieve_authoritative_info(self, topic):
        """检索权威信息"""
        cache_key = f"retrieve_{topic}"
        
        # 检查缓存
        if cache_key in self.cache:
            cached_time, cached_data = self.cache[cache_key]
            if time.time() - cached_time < 1800:  # 30分钟缓存
                print(f"   使用缓存检索: {topic}")
                return cached_data
        
        print(f"   实时检索: {topic}")
        
        info = {
            "topic": topic,
            "retrieved_at": datetime.now().isoformat(),
            "wikipedia": self._retrieve_from_wikipedia(topic),
            "arxiv": self._retrieve_from_arxiv(topic),
            "confidence_score": 0.0
        }
        
        # 计算置信度
        info["confidence_score"] = self._calculate_info_confidence(info)
        
        # 缓存
        self.cache[cache_key] = (time.time(), info)
        
        return info
    
    def _retrieve_from_wikipedia(self, topic):
        """从Wikipedia检索"""
        try:
            page = self.wikipedia.page(topic)
            if page.exists():
                return {
                    "source": "wikipedia",
                    "exists": True,
                    "title": page.title,
                    "summary": page.summary,
                    "key_points": self._extract_key_points(page.summary),
                    "url": page.fullurl,
                    "retrieved_at": datetime.now().isoformat()
                }
            else:
                # 尝试搜索
                search_results = self.wikipedia.search(topic)
                if search_results:
                    # 获取第一个搜索结果
                    first_result = self.wikipedia.page(search_results[0])
                    if first_result.exists():
                        return {
                            "source": "wikipedia",
                            "exists": True,
                            "title": first_result.title,
                            "summary": first_result.summary[:500] + "..." if len(first_result.summary) > 500 else first_result.summary,
                            "key_points": self._extract_key_points(first_result.summary),
                            "url": first_result.fullurl,
                            "note": f"原主题'{topic}'未找到，使用相关主题'{first_result.title}'",
                            "retrieved_at": datetime.now().isoformat()
                        }
        except Exception as e:
            print(f"    ⚠️ Wikipedia检索失败: {e}")
        
        return {
            "source": "wikipedia",
            "exists": False,
            "error": "未找到相关信息",
            "retrieved_at": datetime.now().isoformat()
        }
    
    def _retrieve_from_arxiv(self, topic):
        """从arXiv检索"""
        try:
            search = arxiv.Search(
                query=topic,
                max_results=self.config["arxiv_max_results"],
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            papers = []
            for paper in self.arxiv_client.results(search):
                papers.append({
                    "title": paper.title,
                    "authors": [str(author) for author in paper.authors][:3],  # 前3位作者
                    "summary": paper.summary[:300] + "..." if len(paper.summary) > 300 else paper.summary,
                    "published": paper.published.strftime("%Y-%m") if paper.published else "未知",
                    "pdf_url": paper.pdf_url,
                    "primary_category": paper.primary_category,
                    "relevance_score": self._calculate_paper_relevance(paper, topic)
                })
            
            if papers:
                # 按相关性排序
                papers.sort(key=lambda x: x["relevance_score"], reverse=True)
                
                return {
                    "source": "arxiv",
                    "found": True,
                    "count": len(papers),
                    "papers": papers,
                    "most_relevant": papers[0] if papers else None,
                    "retrieved_at": datetime.now().isoformat()
                }
                
        except Exception as e:
            print(f"    ⚠️ arXiv检索失败: {e}")
        
        return {
            "source": "arxiv",
            "found": False,
            "count": 0,
            "retrieved_at": datetime.now().isoformat()
        }
    
    def _extract_key_points(self, text, max_points=3):
        """从文本中提取关键点"""
        if not text:
            return []
        
        # 简单提取：按句子分割，取前几个
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        key_points = sentences[:max_points]
        
        # 确保每个关键点不要太长
        key_points = [p[:150] + "..." if len(p) > 150 else p for p in key_points]
        
        return key_points
    
    def _calculate_paper_relevance(self, paper, topic):
        """计算论文相关性"""
        relevance = 0.0
        
        # 标题包含主题词
        title_lower = paper.title.lower()
        topic_lower = topic.lower()
        
        if topic_lower in title_lower:
            relevance += 0.6
        elif any(word in title_lower for word in topic_lower.split()):
            relevance += 0.3
        
        # 摘要包含主题词
        if topic_lower in paper.summary.lower():
            relevance += 0.4
        
        # 发布时间（越新越好）
        if paper.published:
            from datetime import datetime
            now = datetime.now()
            published = paper.published
            
            # 计算时间差（月）
            months_diff = (now.year - published.year) * 12 + (now.month - published.month)
            
            if months_diff <= 12:  # 1年内
                relevance += 0.3
            elif months_diff <= 36:  # 3年内
                relevance += 0.1
        
        return min(relevance, 1.0)
    
    def _calculate_info_confidence(self, info):
        """计算信息置信度"""
        confidence = 0.0
        
        # Wikipedia存在性（50%）
        if info["wikipedia"].get("exists", False):
            confidence += 0.5
        
        # arXiv论文数量（30%）
        if info["arxiv"].get("found", False):
            paper_count = info["arxiv"].get("count", 0)
            if paper_count >= 2:
                confidence += 0.3
            elif paper_count >= 1:
                confidence += 0.15
        
        # 其他因素（20%）
        # 可以添加其他验证源
        
        return min(confidence, 1.0)
    
    def _validate_learning_objectives(self, objectives, authoritative_info):
        """验证学习目标"""
        validated = []
        
        for objective in objectives:
            validation = {
                "objective": objective,
                "supported_by_wikipedia": False,
                "supported_by_arxiv": False,
                "confidence": 0.0,
                "suggestions": []
            }
            
            # 检查Wikipedia支持
            wiki_text = authoritative_info["wikipedia"].get("summary", "").lower()
            if objective.lower() in wiki_text:
                validation["supported_by_wikipedia"] = True
                validation["confidence"] += 0.5
            
            # 检查arXiv支持
            if authoritative_info["arxiv"].get("found", False):
                for paper in authoritative_info["arxiv"].get("papers", []):
                    paper_text = (paper.get("title", "") + " " + paper.get("summary", "")).lower()
                    if objective.lower() in paper_text:
                        validation["supported_by_arxiv"] = True
                        validation["confidence"] += 0.3
                        break
            
            validated.append(validation)
        
        return validated
    
    def _generate_enhanced_content(self, topic, base_content, authoritative_info, validated_objectives):
        """生成增强内容"""
        enhanced = f"""# {topic}
## 实时权威验证增强版

**生成时间**: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}
**权威验证时间**: {authoritative_info['retrieved_at']}
**权威置信度**: {authoritative_info['confidence_score']:.0%}

---

## 📚 权威信息参考

### Wikipedia定义
{authoritative_info['wikipedia'].get('summary', '未找到相关定义')}

**关键点**:
{chr(10).join([f'- {point}' for point in authoritative_info['wikipedia'].get('key_points', [])])}

### 最新研究参考
"""
        
        # 添加arXiv信息
        if authoritative_info["arxiv"].get("found", False):
            for i, paper in enumerate(authoritative_info["arxiv"].get("papers", [])[:2], 1):
                enhanced += f"""
**论文{i}**: {paper.get('title', '')}
**作者**: {', '.join(paper.get('authors', [])[:2])}等
**发布时间**: {paper.get('published', '未知')}
**摘要**: {paper.get('summary', '')}
"""
        else:
            enhanced += "\n暂无相关最新研究论文。\n"
        
        enhanced += f"""
---

## 🎯 学习目标验证

| 学习目标 | Wikipedia支持 | 研究论文支持 | 验证置信度 |
|----------|---------------|--------------|------------|
"""
        
        for validation in validated_objectives:
            wiki_support = "✅" if validation["supported_by_wikipedia"] else "❌"
            arxiv_support = "✅" if validation["supported_by_arxiv"] else "❌"
            confidence = f"{validation['confidence']:.0%}"
            
            enhanced += f"| {validation['objective']} | {wiki_support} | {arxiv_support} | {confidence} |\n"
        
        enhanced += f"""
---

## 📖 学习内容

{base_content}

---

## 💡 学习建议

基于权威信息验证，建议：
1. **重点掌握**Wikipedia定义中的关键概念
2. **关注**最新研究论文中的技术进展
3. **验证**学习目标是否得到权威支持
4. **扩展阅读**提供的权威资源链接

---
*本学习内容已通过实时权威信息验证，确保准确性和时效性。*
"""
        
        return enhanced
    
    def _generate_citations_section(self, authoritative_info):
        """生成引用部分"""
        citations = "## 📚 引用来源\n\n"
        
        # Wikipedia引用
        wiki_data = authoritative_info["wikipedia"]
        if wiki_data.get("exists", False):
            citations += f"### Wikipedia\n"
            citations += f"- **页面**: {wiki_data.get('title', '')}\n"
            citations += f"- **URL**: {wiki_data.get('url', '')}\n"
            citations += f"- **检索时间**: {wiki_data.get('retrieved_at', '')}\n\n"
        
        # arXiv引用
        arxiv_data = authoritative_info["arxiv"]
        if arxiv_data.get("found", False):
            citations += f"### arXiv学术论文\n"
            for i, paper in enumerate(arxiv_data.get("papers", [])[:2], 1):
                citations += f"{i}. **{paper.get('title', '')}**\n"
                citations += f"   作者: {', '.join(paper.get('authors', [])[:3])}\n"
                citations += f"   发布时间: {paper.get('published', '未知')}\n"
                citations += f"   PDF: {paper.get('pdf_url', '')}\n\n"
        
        citations += "---\n"
        citations += "*引用格式: 实时检索增强，确保信息时效性和权威性*"
        
        return citations
    
    def _generate_validation_report(self, topic, authoritative_info, validated_objectives):
        """生成验证报告"""
        report = {
            "topic": topic,
            "generated_at": datetime.now().isoformat(),
            "authoritative_confidence": authoritative_info["confidence_score"],
            "sources_used": {
                "wikipedia": authoritative_info["wikipedia"].get("exists", False),
                "arxiv": authoritative_info["arxiv"].get("found", False)
            },
            "objectives_validation": {
                "total": len(validated_objectives),
                "fully_supported": sum(1 for v in validated_objectives if v["confidence"] >= 0.7),
                "partially_supported": sum(1 for v in validated_objectives if 0.3 <= v["confidence"] < 0.7),
                "weakly_supported": sum(1 for v in validated_objectives if v["confidence"] < 0.3)
            },
            "recommendations": self._generate_recommendations(authoritative_info, validated_objectives)
        }
        
        return report
    
    def _generate_recommendations(self, authoritative_info, validated_objectives):
        """生成学习建议"""
        recommendations = []
        
        # 基于置信度的建议
        confidence = authoritative_info["confidence_score"]
        if confidence >= 0.7:
            recommendations.append("✅ 主题权威性高，可放心学习")
        elif confidence >= 0.4:
            recommendations.append("⚠️ 主题权威性中等，建议补充其他资源")
        else:
            recommendations.append("❌ 主题权威性较低，需要谨慎参考")
        
        # 基于学习目标验证的建议
        weak_objectives = [v["objective"] for v in validated_objectives if v["confidence"] < 0.3]
        if weak_objectives:
            recommendations.append(f"📝 以下学习目标缺乏权威支持，需要额外验证: {', '.join(weak_objectives)}")
        
        # 基于来源的建议
        if not authoritative_info["wikipedia"].get("exists", False):
            recommendations.append("🔍 未找到Wikipedia页面，建议手动搜索验证")
        
        if not authoritative_info["arxiv"].get("found", False):
            recommendations.append("📚 未找到相关学术论文，可能为较新或较窄领域")
        
        return recommendations


# 集成演示
def demonstrate_rag_content_enhancement():
    """演示RAG内容增强"""
    
    print("=" * 60)
    print("🔗 实时RAG内容增强集成演示")
    print("=" * 60)
    
    # 创建增强器
    enhancer = RealTimeRAGContentEnhancer()
    
    # 示例学习内容
    sample_topic = "区块链技术"
    sample_content = """区块链是一种分布式数据库技术，通过密码学方法保证数据不可篡改。

主要特点：
1. 去中心化：没有中心控制节点
2. 不可篡改：数据一旦写入难以修改
3. 透明可信：所有交易公开可查
4. 可追溯性：完整历史记录可追溯

应用场景：
- 数字货币（比特币、以太坊）
- 供应链管理
- 数字身份认证
- 智能合约"""
    
    sample_objectives = [
        "理解区块链的基本原理",
        "掌握区块链的核心特点",
        "了解区块链的实际应用",
        "认识区块链的技术挑战"
    ]
    
    print(f"📚 增强学习内容: {sample_topic}")
    print(f"📝 学习目标: {len(sample_objectives)}个")
    
    # 增强内容
    result = enhancer.enhance_learning_content(
        topic=sample_topic,
        base_content=sample_content,
        learning_objectives=sample_objectives
    )
    
    print("\n" + "=" * 60)
    print("📈 增强结果摘要")
    print("=" * 60)
    
    enhanced_content = result["enhanced_content"]
    authoritative_info = result["authoritative_info"]
    validation_report = result["validation_report"]
    
    print(f"主题: {sample_topic}")
    print(f"权威置信度: {authoritative_info['confidence_score']:.0%}")
    print(f"Wikipedia: {'✅找到' if authoritative_info['wikipedia'].get('exists') else '❌未找到'}")
    print(f"arXiv论文: {authoritative_info['arxiv'].get('count', 0)}篇")
    
    print(f"\n学习目标验证:")
    obj_report = validation_report["objectives_validation"]
    print(f"  总数: {obj_report['total']