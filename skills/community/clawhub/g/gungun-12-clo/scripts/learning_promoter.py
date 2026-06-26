#!/usr/bin/env python3
"""
12 号滚滚 - 学习推广器
将学习推广到 AGENTS.md, SOUL.md, TOOLS.md
"""

import re
import sys
from datetime import datetime
from pathlib import Path

class LearningPromoter:
    def __init__(self, workspace="/home/admin/.openclaw/workspace"):
        self.workspace = Path(workspace)
        self.learnings_file = self.workspace / ".learnings" / "LEARNINGS.md"
        
    def promote_to_soul(self, learning_id, rule, section="behavioral"):
        """推广到 SOUL.md"""
        return self._promote_to_file("SOUL.md", learning_id, rule, section)
    
    def promote_to_agents(self, learning_id, workflow, section="workflow"):
        """推广到 AGENTS.md"""
        return self._promote_to_file("AGENTS.md", learning_id, workflow, section)
    
    def promote_to_tools(self, learning_id, tip, section="tool_tip"):
        """推广到 TOOLS.md"""
        return self._promote_to_file("TOOLS.md", learning_id, tip, section)
    
    def promote_to_memory(self, learning_id, knowledge):
        """推广到 MEMORY.md"""
        return self._promote_to_file("MEMORY.md", learning_id, knowledge, "knowledge")
    
    def _promote_to_file(self, filename, learning_id, content, section_type):
        """推广到指定文件"""
        filepath = self.workspace / filename
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # 读取现有内容
        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                existing = f.read()
        else:
            existing = f"# {filename}\n\n"
        
        # 根据文件类型生成不同的内容格式
        if filename == "SOUL.md":
            new_section = self._format_soul_entry(learning_id, content, timestamp)
        elif filename == "AGENTS.md":
            new_section = self._format_agents_entry(learning_id, content, timestamp)
        elif filename == "TOOLS.md":
            new_section = self._format_tools_entry(learning_id, content, timestamp)
        elif filename == "MEMORY.md":
            new_section = self._format_memory_entry(learning_id, content, timestamp)
        else:
            new_section = f"\n## 🌪️ {timestamp} - 来自 {learning_id}\n\n{content}\n\n"
        
        # 写入文件
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(existing + new_section)
        
        # 更新学习状态
        self._update_learning_status(learning_id, "promoted", filename)
        
        print(f"✅ 已推广到 {filename}: {learning_id}")
        return True
    
    def _format_soul_entry(self, learning_id, content, timestamp):
        """格式化 SOUL.md 条目"""
        return f"""
## 🌪️ {timestamp} - 来自 {learning_id}

{content}

"""
    
    def _format_agents_entry(self, learning_id, content, timestamp):
        """格式化 AGENTS.md 条目"""
        return f"""
## 🌪️ {timestamp} - 来自 {learning_id}

{content}

"""
    
    def _format_tools_entry(self, learning_id, content, timestamp):
        """格式化 TOOLS.md 条目"""
        return f"""
## 🌪️ {timestamp} - 来自 {learning_id}

{content}

"""
    
    def _format_memory_entry(self, learning_id, content, timestamp):
        """格式化 MEMORY.md 条目"""
        return f"""
## 🌪️ {timestamp} - 来自 {learning_id}

{content}

"""
    
    def _update_learning_status(self, learning_id, new_status, promoted_to):
        """更新学习记录的状态"""
        if not self.learnings_file.exists():
            print(f"⚠️ 学习文件不存在：{self.learnings_file}")
            return
        
        with open(self.learnings_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 查找并更新对应学习的状态
        # 简单实现：找到 learning_id 所在的条目，更新状态
        pattern = rf"(\[{re.escape(learning_id)}\].*?)(\*\*Status\*\*: pending)"
        replacement = f"\\1**Status**: {new_status}\n**Promoted**: {promoted_to}"
        
        updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        if updated_content != content:
            with open(self.learnings_file, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print(f"📝 已更新学习状态：{learning_id}")
        else:
            print(f"⚠️ 未找到学习记录：{learning_id}")
    
    def check_recurring_patterns(self, min_recurrence=3):
        """检查重复出现的模式"""
        if not self.learnings_file.exists():
            return []
        
        with open(self.learnings_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # 查找所有 Pattern-Key
        pattern_keys = re.findall(r"Pattern-Key: (.+)", content)
        
        # 统计出现次数
        from collections import Counter
        key_counts = Counter(pattern_keys)
        
        # 返回重复的模式
        recurring = [(key, count) for key, count in key_counts.items() if count >= min_recurrence]
        
        if recurring:
            print(f"🔄 发现 {len(recurring)} 个重复模式:")
            for key, count in recurring:
                print(f"  - {key}: {count}次")
        else:
            print("✅ 未发现重复模式")
        
        return recurring


def main():
    """命令行接口"""
    promoter = LearningPromoter()
    
    if len(sys.argv) < 2:
        print("用法：python learning_promoter.py <command> [args]")
        print("命令:")
        print("  promote <file> <learning_id> <content>  - 推广学习到文件")
        print("  soul <learning_id> <rule>               - 推广到 SOUL.md")
        print("  agents <learning_id> <workflow>         - 推广到 AGENTS.md")
        print("  tools <learning_id> <tip>               - 推广到 TOOLS.md")
        print("  check                                   - 检查重复模式")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "promote":
        if len(sys.argv) < 5:
            print("用法：promote <file> <learning_id> <content>")
            sys.exit(1)
        filename = sys.argv[2]
        learning_id = sys.argv[3]
        content = " ".join(sys.argv[4:])
        promoter._promote_to_file(filename, learning_id, content, "manual")
    
    elif command == "soul":
        if len(sys.argv) < 4:
            print("用法：soul <learning_id> <rule>")
            sys.exit(1)
        learning_id = sys.argv[2]
        rule = " ".join(sys.argv[3:])
        promoter.promote_to_soul(learning_id, rule)
    
    elif command == "agents":
        if len(sys.argv) < 4:
            print("用法：agents <learning_id> <workflow>")
            sys.exit(1)
        learning_id = sys.argv[2]
        workflow = " ".join(sys.argv[3:])
        promoter.promote_to_agents(learning_id, workflow)
    
    elif command == "tools":
        if len(sys.argv) < 4:
            print("用法：tools <learning_id> <tip>")
            sys.exit(1)
        learning_id = sys.argv[2]
        tip = " ".join(sys.argv[3:])
        promoter.promote_to_tools(learning_id, tip)
    
    elif command == "check":
        promoter.check_recurring_patterns()
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
