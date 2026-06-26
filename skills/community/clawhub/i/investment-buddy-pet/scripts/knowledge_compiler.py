#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识编译器 - Karpathy LLM Wiki 思路实现

**功能**：
- Ingest: 投喂原始素材 → 编译结构化知识
- Query: 查询知识库 → 生成回答
- Lint: 自检知识库 → 修复问题

**使用示例**：
```bash
# 投喂并编译
python knowledge_compiler.py ingest raw/interactions/2026-04-14-*.md

# 查询知识
python knowledge_compiler.py query "定投有什么好处"

# 自检知识库
python knowledge_compiler.py lint
```
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class KnowledgeCompiler:
    """知识编译器"""
    
    def __init__(self, root_dir: str = None):
        if root_dir is None:
            root_dir = Path(__file__).parent.parent
        self.root_dir = Path(root_dir)
        
        self.data_dir = self.root_dir / "data"
        self.raw_dir = self.data_dir / "raw"
        self.wiki_dir = self.data_dir / "wiki"
        self.index_file = self.wiki_dir / "index.md"
        self.log_file = self.root_dir / "log.md"
        
        # 创建目录
        for subdir in ["raw/interactions", "raw/market-events", "raw/feedback",
                       "wiki/concepts", "wiki/entities", "wiki/topics", "wiki/patterns"]:
            (self.data_dir / subdir).mkdir(parents=True, exist_ok=True)
    
    # ========== Ingest 流程 ==========
    
    def ingest(self, raw_files: List[str]) -> Dict:
        """
        投喂原始素材并编译
        
        Args:
            raw_files: 原始文件路径列表
        
        Returns:
            {
                "processed": 5,
                "new_concepts": 2,
                "new_entities": 1,
                "new_patterns": 1,
                "updated_pages": 3
            }
        """
        stats = {
            "processed": 0,
            "new_concepts": 0,
            "new_entities": 0,
            "new_patterns": 0,
            "updated_pages": 0
        }
        
        for file_path in raw_files:
            file_path = Path(file_path)
            if not file_path.exists():
                continue
            
            # 读取原始素材
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 提取知识
            concepts = self._extract_concepts(content)
            entities = self._extract_entities(content)
            patterns = self._extract_patterns(content)
            
            # 创建或更新页面
            for concept in concepts:
                if self._create_or_update_page("concepts", concept):
                    stats["new_concepts"] += 1
                else:
                    stats["updated_pages"] += 1
            
            for entity in entities:
                if self._create_or_update_page("entities", entity):
                    stats["new_entities"] += 1
                else:
                    stats["updated_pages"] += 1
            
            for pattern in patterns:
                if self._create_or_update_page("patterns", pattern):
                    stats["new_patterns"] += 1
                else:
                    stats["updated_pages"] += 1
            
            stats["processed"] += 1
        
        # 更新索引
        self._update_index()
        
        # 记录日志
        self._log_operation("ingest", stats)
        
        return stats
    
    def _extract_concepts(self, content: str) -> List[str]:
        """提取概念"""
        # 简化实现：检测常见投资概念
        concept_keywords = [
            "定投", "估值", "风险", "收益", "复利", "分散", "仓位",
            "止盈", "止损", "择时", "基本面", "技术面"
        ]
        
        concepts = []
        for keyword in concept_keywords:
            if keyword in content:
                concepts.append(keyword)
        
        return list(set(concepts))
    
    def _extract_entities(self, content: str) -> List[str]:
        """提取实体"""
        # 简化实现：检测股票代码、基金代码、人名
        entities = []
        
        # 股票代码
        stock_codes = re.findall(r'(\d{6}\.(SH|SZ))', content)
        for code, _ in stock_codes:
            entities.append(code)
        
        # 基金代码
        fund_codes = re.findall(r'([015]\d{5})', content)
        for code in fund_codes:
            entities.append(code)
        
        # 人名（大师）
        master_names = ["巴菲特", "芒格", "达利欧", "彼得林奇", "索罗斯"]
        for name in master_names:
            if name in content:
                entities.append(name)
        
        return list(set(entities))
    
    def _extract_patterns(self, content: str) -> List[str]:
        """提取模式"""
        patterns = []
        
        # 检测用户反馈
        if "👍" in content or "有帮助" in content:
            patterns.append("有效话术")
        
        if "👎" in content or "没帮助" in content:
            patterns.append("无效话术")
        
        # 检测市场场景
        if "跌了" in content and "卖出" in content:
            patterns.append("市场大跌应对")
        
        if "涨了" in content and "买入" in content:
            patterns.append("市场大涨应对")
        
        return list(set(patterns))
    
    def _create_or_update_page(self, page_type: str, page_name: str) -> bool:
        """
        创建或更新页面
        
        Returns:
            True: 新建页面
            False: 更新页面
        """
        page_file = self.wiki_dir / page_type / f"{page_name}.md"
        
        if page_file.exists():
            # 更新页面（添加新内容）
            with open(page_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 添加更新时间
            content += f"\n\n_最后更新：{datetime.now().strftime('%Y-%m-%d')}_\n"
            
            with open(page_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return False
        else:
            # 创建新页面
            content = f"""# {page_name}

**类型**: {page_type}  
**创建时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 定义

（待补充）

## 相关页面

（待建立链接）

## 参考案例

（待补充）

---

_最后更新：{datetime.now().strftime('%Y-%m-%d')}_
"""
            with open(page_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
    
    def _update_index(self):
        """更新知识索引"""
        index_content = "# 投资宠物知识库索引\n\n"
        
        for page_type in ["concepts", "entities", "topics", "patterns"]:
            type_dir = self.wiki_dir / page_type
            if not type_dir.exists():
                continue
            
            pages = list(type_dir.glob("*.md"))
            if not pages:
                continue
            
            index_content += f"## {page_type.title()}\n\n"
            for page_file in pages:
                page_name = page_file.stem
                index_content += f"- [[{page_name}]]\n"
            index_content += "\n"
        
        with open(self.index_file, 'w', encoding='utf-8') as f:
            f.write(index_content)
    
    # ========== Query 流程 ==========
    
    def query(self, question: str) -> str:
        """
        查询知识库
        
        Args:
            question: 用户问题
        
        Returns:
            综合知识生成的回答
        """
        # 1. 提取关键词
        keywords = self._extract_keywords(question)
        
        # 2. 查找相关页面
        related_pages = self._find_related_pages(keywords)
        
        # 3. 综合生成回答
        answer = self._synthesize_answer(question, related_pages)
        
        return answer
    
    def _extract_keywords(self, question: str) -> List[str]:
        """提取问题关键词"""
        # 简化实现：分词
        return question.split()
    
    def _find_related_pages(self, keywords: List[str]) -> List[Path]:
        """查找相关页面"""
        related = []
        
        for page_type in ["concepts", "entities", "topics", "patterns"]:
            type_dir = self.wiki_dir / page_type
            if not type_dir.exists():
                continue
            
            for page_file in type_dir.glob("*.md"):
                # 检查页面内容是否包含关键词
                with open(page_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if any(kw in content for kw in keywords):
                    related.append(page_file)
        
        return related
    
    def _synthesize_answer(self, question: str, related_pages: List[Path]) -> str:
        """综合生成回答"""
        if not related_pages:
            return "抱歉，我还没有学到相关知识。"
        
        answer = f"关于\"{question}\"，我找到以下知识：\n\n"
        
        for page_file in related_pages[:3]:  # 最多引用 3 个页面
            page_name = page_file.stem
            page_type = page_file.parent.name
            
            answer += f"- **{page_name}** ({page_type}): [[{page_name}]]\n"
        
        answer += "\n要我详细解释某个概念吗？"
        
        return answer
    
    # ========== Lint 流程 ==========
    
    def lint(self) -> Dict:
        """
        自检知识库
        
        Returns:
            {
                "total_pages": 150,
                "health_score": 92,
                "issues": {
                    "isolated_pages": [...],
                    "broken_links": [...],
                    "outdated_pages": [...]
                },
                "suggestions": [...]
            }
        """
        issues = {
            "isolated_pages": [],
            "broken_links": [],
            "outdated_pages": []
        }
        
        all_pages = []
        for page_type in ["concepts", "entities", "topics", "patterns"]:
            type_dir = self.wiki_dir / page_type
            if not type_dir.exists():
                continue
            
            for page_file in type_dir.glob("*.md"):
                all_pages.append(page_file)
        
        # 检查每个页面
        for page_file in all_pages:
            with open(page_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查孤立页面（没有双向链接）
            if "[[" not in content and "]]" not in content:
                issues["isolated_pages"].append(page_file.stem)
            
            # 检查过时页面（超过 30 天未更新）
            if "_最后更新：" in content:
                match = re.search(r'_最后更新：(\d{4}-\d{2}-\d{2})_', content)
                if match:
                    last_update = datetime.strptime(match.group(1), '%Y-%m-%d')
                    days_old = (datetime.now() - last_update).days
                    if days_old > 30:
                        issues["outdated_pages"].append({
                            "page": page_file.stem,
                            "days_old": days_old
                        })
        
        # 生成报告
        report = {
            "total_pages": len(all_pages),
            "health_score": self._calculate_health_score(issues, len(all_pages)),
            "issues": issues,
            "suggestions": self._generate_suggestions(issues)
        }
        
        # 记录日志
        self._log_operation("lint", report)
        
        return report
    
    def _calculate_health_score(self, issues: Dict, total_pages: int) -> float:
        """计算健康度分数"""
        if total_pages == 0:
            return 0
        
        score = 100
        
        # 孤立页面扣分
        score -= len(issues["isolated_pages"]) * 2
        
        # 过时页面扣分
        score -= len(issues["outdated_pages"]) * 1
        
        return max(0, min(100, score))
    
    def _generate_suggestions(self, issues: Dict) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        if issues["isolated_pages"]:
            suggestions.append(f"发现{len(issues['isolated_pages'])}个孤立页面，建议建立双向链接")
        
        if issues["outdated_pages"]:
            suggestions.append(f"发现{len(issues['outdated_pages'])}个过时页面，建议更新数据")
        
        return suggestions
    
    # ========== 工具函数 ==========
    
    def _log_operation(self, operation: str, details: Dict):
        """记录操作日志"""
        log_entry = f"""
## {operation.title()} - {datetime.now().strftime('%Y-%m-%d %H:%M')}

{json.dumps(details, ensure_ascii=False, indent=2)}

"""
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)


# CLI 入口
if __name__ == '__main__':
    import sys
    
    compiler = KnowledgeCompiler()
    
    if len(sys.argv) < 2:
        print("用法：python knowledge_compiler.py <command> [args]")
        print("命令:")
        print("  ingest <file1> <file2> ...  投喂并编译")
        print("  query <question>            查询知识")
        print("  lint                        自检知识库")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "ingest":
        files = sys.argv[2:]
        if not files:
            print("请提供文件路径")
            sys.exit(1)
        
        stats = compiler.ingest(files)
        print(f"✅ 处理完成:")
        print(f"  处理文件：{stats['processed']}")
        print(f"  新增概念：{stats['new_concepts']}")
        print(f"  新增实体：{stats['new_entities']}")
        print(f"  新增模式：{stats['new_patterns']}")
        print(f"  更新页面：{stats['updated_pages']}")
    
    elif command == "query":
        if len(sys.argv) < 3:
            print("请提供问题")
            sys.exit(1)
        
        question = " ".join(sys.argv[2:])
        answer = compiler.query(question)
        print(answer)
    
    elif command == "lint":
        report = compiler.lint()
        print(f"📊 知识库健康报告:")
        print(f"  总页面数：{report['total_pages']}")
        print(f"  健康度：{report['health_score']}%")
        print(f"  孤立页面：{len(report['issues']['isolated_pages'])}")
        print(f"  过时页面：{len(report['issues']['outdated_pages'])}")
        print(f"\n建议:")
        for suggestion in report['suggestions']:
            print(f"  - {suggestion}")
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)
