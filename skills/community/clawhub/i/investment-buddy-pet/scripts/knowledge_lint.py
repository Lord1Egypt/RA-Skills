#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Knowledge Lint Script - 投资宠物知识库健康检查脚本

基于 Karpathy LLM Wiki 思路
功能：检查知识库健康状态，发现并修复问题

用法:
    python scripts/knowledge_lint.py [--fix] [--report]
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

class KnowledgeLint:
    """知识库健康检查引擎"""
    
    def __init__(self, base_path=None):
        self.base_path = Path(base_path) if base_path else Path(__file__).parent.parent
        self.wiki_path = self.base_path / "wiki"
        self.index_path = self.base_path / "index.md"
        self.log_path = self.base_path / "log.md"
        
        # 问题报告
        self.issues = {
            "orphan_pages": [],      # 孤立页面
            "broken_links": [],       # 断链
            "contradictions": [],     # 矛盾信息
            "outdated_pages": []      # 过时信息
        }
        
        # 统计信息
        self.stats = {
            "checked": 0,
            "issues_found": 0,
            "issues_fixed": 0
        }
    
    def get_all_pages(self):
        """获取所有知识页面"""
        pages = []
        for subdir in ["concepts", "entities", "patterns", "topics"]:
            subdir_path = self.wiki_path / subdir
            if not subdir_path.exists():
                continue
            
            for md_file in subdir_path.glob("*.md"):
                pages.append({
                    "path": md_file,
                    "category": subdir,
                    "name": md_file.stem
                })
        
        return pages
    
    def extract_links(self, content):
        """从内容中提取双链引用"""
        # 匹配 [[页面名]] 格式
        links = re.findall(r'\[\[([^\]]+)\]\]', content)
        return links
    
    def check_orphan_pages(self, pages):
        """检查孤立页面（没有被任何页面引用）"""
        print("  检查孤立页面...")
        
        # 收集所有引用
        all_links = set()
        for page in pages:
            try:
                content = page["path"].read_text(encoding='utf-8')
                links = self.extract_links(content)
                all_links.update(links)
            except Exception as e:
                print(f"    读取失败 {page['name']}: {e}")
        
        # 查找孤立页面
        for page in pages:
            if page["name"] not in all_links and page["name"] != "index":
                self.issues["orphan_pages"].append(page)
                self.stats["issues_found"] += 1
    
    def check_broken_links(self, pages):
        """检查断链（引用了不存在的页面）"""
        print("  检查断链...")
        
        # 收集所有存在的页面名
        existing_pages = set(page["name"] for page in pages)
        existing_pages.add("CLAUDE.md")
        existing_pages.add("index.md")
        
        # 检查每个页面的引用
        for page in pages:
            try:
                content = page["path"].read_text(encoding='utf-8')
                links = self.extract_links(content)
                
                for link in links:
                    # 处理带路径的链接
                    link_name = link.split("/")[-1] if "/" in link else link
                    
                    if link_name not in existing_pages:
                        self.issues["broken_links"].append({
                            "source": page["name"],
                            "target": link
                        })
                        self.stats["issues_found"] += 1
            except Exception as e:
                print(f"    检查失败 {page['name']}: {e}")
    
    def check_outdated_pages(self, pages):
        """检查过时页面（超过 6 个月未更新）"""
        print("  检查过时页面...")
        
        six_months_ago = datetime.now().timestamp() - (180 * 24 * 60 * 60)
        
        for page in pages:
            try:
                mtime = page["path"].stat().st_mtime
                if mtime < six_months_ago:
                    self.issues["outdated_pages"].append(page)
                    self.stats["issues_found"] += 1
            except Exception as e:
                print(f"    检查失败 {page['name']}: {e}")
    
    def fix_orphan_pages(self):
        """修复孤立页面"""
        print("  修复孤立页面...")
        
        if not self.issues["orphan_pages"]:
            print("    无需修复")
            return
        
        # 简单修复：在 index.md 中添加链接
        # 实际应该根据内容智能链接
        print(f"    发现 {len(self.issues['orphan_pages'])} 个孤立页面")
        print("    建议：手动审查并添加到相关主题或删除")
    
    def fix_broken_links(self):
        """修复断链"""
        print("  修复断链...")
        
        if not self.issues["broken_links"]:
            print("    无需修复")
            return
        
        # 简单修复：移除断链
        # 实际应该创建缺失页面或更新引用
        print(f"    发现 {len(self.issues['broken_links'])} 个断链")
        print("    建议：创建缺失页面或移除引用")
    
    def generate_report(self):
        """生成检查报告"""
        report = f"""## Lint Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}

```json
{{
  "checked": {self.stats['checked']},
  "issues_found": {self.stats['issues_found']},
  "issues_fixed": {self.stats['issues_fixed']}
}}
```

### 孤立页面 ({len(self.issues['orphan_pages'])})
"""
        
        for page in self.issues["orphan_pages"][:10]:  # 只显示前 10 个
            report += f"- [[{page['name']}]] ({page['category']}) - 建议审查\n"
        
        if len(self.issues["orphan_pages"]) > 10:
            report += f"- ... 还有 {len(self.issues['orphan_pages']) - 10} 个\n"
        
        report += f"\n### 断链 ({len(self.issues['broken_links'])})\n"
        
        for issue in self.issues["broken_links"][:10]:
            report += f"- [[{issue['source']}]] 引用了不存在的 [[{issue['target']}]]\n"
        
        if len(self.issues["broken_links"]) > 10:
            report += f"- ... 还有 {len(self.issues['broken_links']) - 10} 个\n"
        
        report += f"\n### 过时信息 ({len(self.issues['outdated_pages'])})\n"
        
        for page in self.issues["outdated_pages"][:10]:
            report += f"- [[{page['name']}]] - 最后更新超过 6 个月\n"
        
        if len(self.issues["outdated_pages"]) > 10:
            report += f"- ... 还有 {len(self.issues['outdated_pages']) - 10} 个\n"
        
        report += "\n---\n*报告生成时间*: " + datetime.now().strftime('%Y-%m-%d %H:%M')
        
        return report
    
    def run(self, fix=False, report=False):
        """运行 Lint 流程"""
        print("🧹 开始 Knowledge Lint...")
        print(f"  知识库目录：{self.wiki_path}")
        print()
        
        # 获取所有页面
        pages = self.get_all_pages()
        self.stats["checked"] = len(pages)
        
        print(f"📊 检查 {len(pages)} 个页面...")
        print()
        
        # 执行检查
        self.check_orphan_pages(pages)
        self.check_broken_links(pages)
        self.check_outdated_pages(pages)
        
        print()
        
        # 执行修复
        if fix:
            print("🔧 执行修复...")
            self.fix_orphan_pages()
            self.fix_broken_links()
            print()
        else:
            print("💡 提示：使用 --fix 参数自动修复问题")
            print()
        
        # 生成报告
        if report:
            report_content = self.generate_report()
            print(report_content)
            
            # 保存到日志
            with open(self.log_path, 'a', encoding='utf-8') as f:
                f.write("\n" + report_content + "\n")
        
        # 输出统计
        print("✅ Lint 完成")
        print()
        print("📊 统计信息:")
        print(f"  检查页面数：{self.stats['checked']}")
        print(f"  发现问题数：{self.stats['issues_found']}")
        print(f"  已修复问题：{self.stats['issues_fixed']}")
        print()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Knowledge Lint - 投资宠物知识库健康检查脚本')
    parser.add_argument('--fix', action='store_true', help='自动修复问题')
    parser.add_argument('--report', action='store_true', help='生成详细报告')
    
    args = parser.parse_args()
    
    lint = KnowledgeLint()
    lint.run(fix=args.fix, report=args.report)


if __name__ == '__main__':
    main()
