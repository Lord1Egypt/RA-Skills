#!/usr/bin/env python3
"""
Auto-Dream Consolidation
参考 Claude Code 的 autoDream 设计

功能：
1. 扫描短期记忆（logs/）
2. 分析是否有值得保留的信息
3. 将重要信息合并到长期记忆（user/feedback/project/reference/）
4. 清理已处理的短期记忆

触发条件：
- 每天定时执行
- 或手动触发
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

MEMORY_ROOT = Path.home() / ".openclaw" / "bw-openclaw-boost" / "memory"
LOGS_DIR = MEMORY_ROOT / "logs"


@dataclass
class ConsolidationRule:
    """整理规则"""
    pattern: str  # 匹配模式
    target_type: str  # 目标记忆类型
    target_file: str  # 目标文件
    priority: int  # 优先级


# 整理规则
CONSOLIDATION_RULES = [
    ConsolidationRule(
        pattern=r"教训|纠正|避免|注意",
        target_type="feedback",
        target_file="feedback/corrections",
        priority=1
    ),
    ConsolidationRule(
        pattern=r"项目|进行中|待处理|TODO",
        target_type="project",
        target_file="project/ongoing",
        priority=2
    ),
    ConsolidationRule(
        pattern=r"配置|技术|工具|系统",
        target_type="reference",
        target_file="reference/tech-stack",
        priority=3
    ),
    ConsolidationRule(
        pattern=r"用户|角色|身份|我是",
        target_type="user",
        target_file="user/identity",
        priority=1
    ),
]


class DreamConsolidator:
    """自动整理器"""
    
    def __init__(self):
        self.processed_count = 0
        self.consolidated_count = 0
    
    def scan_logs(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        扫描近期的日志
        """
        logs = []
        
        # 扫描 logs/ 目录
        if not LOGS_DIR.exists():
            return logs
        
        for root, dirs, files in os.walk(LOGS_DIR):
            for f in files:
                if not f.endswith('.md'):
                    continue
                
                path = Path(root) / f
                
                # 检查修改时间
                mtime = datetime.fromtimestamp(path.stat().st_mtime)
                if (datetime.now() - mtime).days > days:
                    continue
                
                try:
                    content = path.read_text(encoding='utf-8')
                    
                    # 提取日期
                    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', f)
                    date = date_match.group(1) if date_match else f
                    
                    logs.append({
                        "path": path,
                        "file": f,
                        "date": date,
                        "content": content,
                        "size": len(content)
                    })
                except:
                    pass
        
        return sorted(logs, key=lambda x: x["date"], reverse=True)
    
    def extract_key_info(self, content: str) -> List[str]:
        """
        从内容中提取关键信息
        """
        key_points = []
        
        # 提取标题（## 开头的）
        titles = re.findall(r'^#{1,3}\s+(.+)$', content, re.MULTILINE)
        key_points.extend(titles)
        
        # 提取列表项
        list_items = re.findall(r'^[-*]\s+(.+)$', content, re.MULTILINE)
        key_points.extend(list_items)
        
        # 提取代码块（可能是重要配置）
        code_blocks = re.findall(r'```[\s\S]*?```', content)
        for block in code_blocks[:2]:  # 最多2个
            if len(block) < 200:
                key_points.append(block[:100])
        
        return key_points[:20]  # 最多20条
    
    def match_rule(self, content: str) -> Optional[ConsolidationRule]:
        """
        匹配整理规则
        """
        for rule in CONSOLIDATION_RULES:
            if re.search(rule.pattern, content, re.IGNORECASE):
                return rule
        return None
    
    def consolidate_log(self, log: Dict[str, Any]) -> bool:
        """
        整理单条日志
        """
        rule = self.match_rule(log["content"])
        if not rule:
            return False
        
        target_dir = MEMORY_ROOT / rule.target_type
        target_file = target_dir / f"{rule.target_file}.md"
        
        # 读取现有内容
        existing = ""
        if target_file.exists():
            existing = target_file.read_text(encoding='utf-8')
        
        # 构建更新内容
        update_time = datetime.now().strftime('%Y-%m-%d')
        key_points = self.extract_key_info(log["content"])
        
        new_entry = f"""

---

## 来自 {log['date']} 日志的更新

来源: `{log['file']}`

### 关键信息
"""
        
        for point in key_points[:10]:
            if len(point) > 200:
                point = point[:200] + "..."
            new_entry += f"- {point}\n"
        
        new_entry += f"\n_整理时间: {update_time}_"
        
        # 追加或创建
        if existing:
            # 找到最后一个 --- 分隔符，在那之前插入
            last_sep = existing.rfind('\n---\n')
            if last_sep > 0:
                updated = existing[:last_sep] + new_entry + existing[last_sep:]
            else:
                updated = existing + new_entry
        else:
            updated = f"""# {rule.target_file.replace('-', ' ').title()}

{new_entry}
"""
        
        target_file.write_text(updated, encoding='utf-8')
        self.consolidated_count += 1
        
        return True
    
    def consolidate_all(self, days: int = 7, dry_run: bool = False) -> Dict[str, Any]:
        """
        整理所有符合条件的日志
        """
        self.processed_count = 0
        self.consolidated_count = 0
        
        logs = self.scan_logs(days)
        
        results = {
            "scanned": len(logs),
            "processed": 0,
            "consolidated": 0,
            "skipped": 0,
            "details": []
        }
        
        for log in logs:
            self.processed_count += 1
            rule = self.match_rule(log["content"])
            
            if rule:
                if not dry_run:
                    self.consolidate_log(log)
                    log["path"].unlink()  # 删除已整理的日志
                
                results["details"].append({
                    "file": log["file"],
                    "matched_rule": rule.target_file,
                    "action": "consolidated" if not dry_run else "would_consolidate"
                })
                results["consolidated"] += 1
            else:
                results["skipped"] += 1
        
        results["processed"] = self.processed_count
        
        return results
    
    def format_results(self, results: Dict[str, Any]) -> str:
        """格式化结果"""
        lines = [
            "=" * 50,
            "🌙 Auto-Dream Consolidation 报告",
            "=" * 50,
            "",
            f"扫描日志数: {results['scanned']}",
            f"处理数: {results['processed']}",
            f"已整理: {results['consolidated']}",
            f"跳过: {results['skipped']}",
            "",
        ]
        
        if results["details"]:
            lines.append("📋 整理详情:")
            for detail in results["details"][:10]:
                action_emoji = "✅" if detail["action"] == "consolidated" else "📝"
                lines.append(f"  {action_emoji} {detail['file']} -> {detail['matched_rule']}")
        
        return "\n".join(lines)


def get_consolidator() -> DreamConsolidator:
    return DreamConsolidator()


if __name__ == "__main__":
    import sys
    
    consolidator = get_consolidator()
    
    if len(sys.argv) < 2:
        print("用法:")
        print("  dream_consolidation.py run [days]     # 执行整理")
        print("  dream_consolidation.py scan [days]    # 扫描（不执行）")
        print("  dream_consolidation.py status        # 查看状态")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "run":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        force = "--force" in sys.argv
        
        # 默认是安全模式（dry-run），需要 --force 才能实际删除
        dry_run = not force
        
        if force:
            print("⚠️ 警告: 即将删除已整理的日志文件！")
            print()
        
        print(f"正在整理近 {days} 天的日志{' (安全模式，仅预览)' if dry_run else ' (强制模式，将删除文件)'}...")
        results = consolidator.consolidate_all(days, dry_run=dry_run)
        print(consolidator.format_results(results))
        
        if dry_run:
            print()
            print("💡 提示: 如需实际删除，请使用: dream_consolidation.py run --force")
        else:
            print()
            print("✅ 整理完成！如需撤销，请从备份恢复日志文件。")
    
    elif cmd == "scan":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        print(f"正在扫描近 {days} 天的日志...")
        results = consolidator.consolidate_all(days, dry_run=True)
        print(consolidator.format_results(results))
    
    elif cmd == "status":
        logs = consolidator.scan_logs(days=7)
        print(f"近7天日志数: {len(logs)}")
        for log in logs[:5]:
            print(f"  - {log['file']} ({log['size']} bytes)")
