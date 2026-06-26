#!/usr/bin/env python3
"""
Dream Daemon - 梦境整合守护进程
自动将Working Memory晋升到Long-term Memory
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime, timedelta
from typing import List, Dict, Any
import re

# 路径配置
WORKSPACE_ROOT = os.getcwd()
MEMORY_DIR = os.path.join(WORKSPACE_ROOT, "memory")
MEMORY_INDEX_PATH = os.path.join(WORKSPACE_ROOT, "MEMORY.md")
SESSION_STATE_PATH = os.path.join(WORKSPACE_ROOT, "SESSION-STATE.md")

# 整合参数
WORKING_MEMORY_TTL_DAYS = 7  # Working memory保留天数
MIN_IMPORTANCE_FOR_PROMOTION = 0.7  # 晋升最低重要性
MAX_INDEX_SIZE_KB = 5  # MEMORY.md最大大小


class DreamDaemon:
    """梦境整合守护进程"""
    
    def __init__(self):
        self.promoted_count = 0
        self.pruned_count = 0
        self.stats = {
            "oriented": False,
            "gathered": 0,
            "consolidated": 0,
            "pruned": 0
        }
    
    def orient(self) -> Dict[str, Any]:
        """
        Phase 1: Orient - 扫描现有记忆结构
        """
        result = {
            "memory_index_exists": os.path.exists(MEMORY_INDEX_PATH),
            "session_state_exists": os.path.exists(SESSION_STATE_PATH),
            "memory_dirs": {},
            "daily_logs": []
        }
        
        # 检查各类型目录
        for mem_type in ['user', 'feedback', 'project', 'reference']:
            type_dir = os.path.join(MEMORY_DIR, mem_type)
            if os.path.exists(type_dir):
                files = [f for f in os.listdir(type_dir) if f.endswith('.md')]
                result["memory_dirs"][mem_type] = len(files)
            else:
                result["memory_dirs"][mem_type] = 0
        
        # 扫描daily logs
        if os.path.exists(MEMORY_DIR):
            for f in os.listdir(MEMORY_DIR):
                if re.match(r'\d{4}-\d{2}-\d{2}\.md$', f):
                    result["daily_logs"].append(f)
        
        self.stats["oriented"] = True
        return result
    
    def gather(self) -> List[Dict[str, Any]]:
        """
        Phase 2: Gather - 收集Working Memory信号
        从daily logs中提取需要晋升的内容
        """
        signals = []
        cutoff_date = datetime.now() - timedelta(days=WORKING_MEMORY_TTL_DAYS)
        
        if not os.path.exists(MEMORY_DIR):
            return signals
        
        for filename in os.listdir(MEMORY_DIR):
            if not re.match(r'\d{4}-\d{2}-\d{2}\.md$', filename):
                continue
            
            filepath = os.path.join(MEMORY_DIR, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 提取日期
                file_date = datetime.strptime(filename.replace('.md', ''), '%Y-%m-%d')
                
                # 跳过太新的文件（还没稳定）
                if file_date > datetime.now() - timedelta(days=1):
                    continue
                
                # 提取关键信号
                # 模式1: 用户偏好
                if '用户' in content or '偏好' in content or 'preference' in content.lower():
                    signals.append({
                        "source": filename,
                        "type": "user",
                        "content": self._extract_signal(content, 'user'),
                        "importance": 0.8
                    })
                
                # 模式2: 决策
                if '决策' in content or '决定' in content or 'decision' in content.lower():
                    signals.append({
                        "source": filename,
                        "type": "project",
                        "content": self._extract_signal(content, 'decision'),
                        "importance": 0.9
                    })
                
                # 模式3: 纠正
                if '纠正' in content or '改正' in content or '不是' in content:
                    signals.append({
                        "source": filename,
                        "type": "feedback",
                        "content": self._extract_signal(content, 'correction'),
                        "importance": 0.85
                    })
                
            except Exception as e:
                print(f"[WARN] Failed to read {filename}: {e}")
        
        self.stats["gathered"] = len(signals)
        return signals
    
    def consolidate(self, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Phase 3: Consolidate - 晋升到Long-term
        """
        result = {
            "promoted": [],
            "skipped": []
        }
        
        for signal in signals:
            if signal.get("importance", 0) < MIN_IMPORTANCE_FOR_PROMOTION:
                result["skipped"].append(signal)
                continue
            
            # 写入对应类型目录
            mem_type = signal.get("type", "other")
            type_dir = os.path.join(MEMORY_DIR, mem_type)
            os.makedirs(type_dir, exist_ok=True)
            
            # 生成文件名
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"{timestamp}_{mem_type}.md"
            filepath = os.path.join(type_dir, filename)
            
            # 写入记忆文件
            content = self._format_memory_file(signal)
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                result["promoted"].append({
                    "type": mem_type,
                    "file": filename,
                    "content": signal.get("content", "")[:100]
                })
                self.promoted_count += 1
            except Exception as e:
                print(f"[ERROR] Failed to write {filepath}: {e}")
        
        # 更新MEMORY.md索引
        self._update_memory_index(result["promoted"])
        
        self.stats["consolidated"] = len(result["promoted"])
        return result
    
    def prune(self) -> Dict[str, Any]:
        """
        Phase 4: Prune - 清理过期内容
        """
        result = {
            "archived_logs": [],
            "removed_entries": []
        }
        
        cutoff_date = datetime.now() - timedelta(days=WORKING_MEMORY_TTL_DAYS)
        
        # 归档过期的daily logs
        archive_dir = os.path.join(MEMORY_DIR, "archive")
        os.makedirs(archive_dir, exist_ok=True)
        
        if os.path.exists(MEMORY_DIR):
            for filename in os.listdir(MEMORY_DIR):
                if not re.match(r'\d{4}-\d{2}-\d{2}\.md$', filename):
                    continue
                
                file_date = datetime.strptime(filename.replace('.md', ''), '%Y-%m-%d')
                if file_date < cutoff_date:
                    src = os.path.join(MEMORY_DIR, filename)
                    dst = os.path.join(archive_dir, filename)
                    try:
                        os.rename(src, dst)
                        result["archived_logs"].append(filename)
                        self.pruned_count += 1
                    except Exception as e:
                        print(f"[WARN] Failed to archive {filename}: {e}")
        
        # 清理MEMORY.md中的过期引用
        if os.path.exists(MEMORY_INDEX_PATH):
            self._clean_memory_index()
        
        self.stats["pruned"] = len(result["archived_logs"])
        return result
    
    def _extract_signal(self, content: str, signal_type: str) -> str:
        """从内容中提取信号"""
        lines = content.split('\n')
        relevant_lines = []
        
        keywords = {
            'user': ['用户', '偏好', '喜欢', 'preference'],
            'decision': ['决策', '决定', '选择', 'decision', '采用'],
            'correction': ['纠正', '不是', '应该', '不对', 'correction']
        }
        
        target_keywords = keywords.get(signal_type, [])
        
        for line in lines:
            if any(kw in line.lower() for kw in target_keywords):
                # 清理行内容
                cleaned = line.strip()
                if cleaned and len(cleaned) > 10:
                    relevant_lines.append(cleaned)
        
        return '\n'.join(relevant_lines[:3])  # 最多返回3行
    
    def _format_memory_file(self, signal: Dict[str, Any]) -> str:
        """格式化记忆文件"""
        return f"""---
name: memory_{datetime.now().strftime("%Y%m%d%H%M%S")}
description: {signal.get('content', '')[:100]}
type: {signal.get('type', 'other')}
created: {datetime.now().strftime("%Y-%m-%d")}
---

## 内容
{signal.get('content', '')}

## 来源
{signal.get('source', 'unknown')}

## 重要性
{signal.get('importance', 0.7)}
"""
    
    def _update_memory_index(self, promoted: List[Dict[str, Any]]):
        """更新MEMORY.md索引"""
        if not promoted:
            return
        
        # 读取现有索引
        existing_content = ""
        if os.path.exists(MEMORY_INDEX_PATH):
            try:
                with open(MEMORY_INDEX_PATH, 'r', encoding='utf-8') as f:
                    existing_content = f.read()
            except Exception:
                pass
        
        # 添加新条目
        new_entries = []
        for item in promoted:
            entry = f"- [{item['file']}]({item['type']}/{item['file']}) — {item['content']}"
            new_entries.append(entry)
        
        # 按类型组织
        sections = {
            "user": "## User Memory\n",
            "feedback": "## Feedback Memory\n",
            "project": "## Project Memory\n",
            "reference": "## Reference\n"
        }
        
        if not existing_content:
            new_content = "# MEMORY.md — 长期记忆索引\n\n"
            for section in sections.values():
                new_content += section + "\n"
        else:
            new_content = existing_content
        
        # 追加新条目
        for item in promoted:
            section_header = sections.get(item['type'], "## Other\n")
            if section_header in new_content:
                # 在对应section后追加
                idx = new_content.find(section_header) + len(section_header)
                entry = f"- [{item['file']}]({item['type']}/{item['file']}) — {item['content']}\n"
                new_content = new_content[:idx] + entry + new_content[idx:]
        
        try:
            with open(MEMORY_INDEX_PATH, 'w', encoding='utf-8') as f:
                f.write(new_content)
        except Exception as e:
            print(f"[ERROR] Failed to update MEMORY.md: {e}")
    
    def _clean_memory_index(self):
        """清理MEMORY.md中的过期引用"""
        if not os.path.exists(MEMORY_INDEX_PATH):
            return
        
        try:
            with open(MEMORY_INDEX_PATH, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 检查每行引用的文件是否存在
            new_lines = []
            for line in lines:
                # 检查是否是引用行
                match = re.search(r'\[(.*?)\]\((.*?)\)', line)
                if match:
                    link_path = match.group(2)
                    full_path = os.path.join(MEMORY_DIR, link_path)
                    if os.path.exists(full_path):
                        new_lines.append(line)
                    else:
                        self.pruned_count += 1
                else:
                    new_lines.append(line)
            
            with open(MEMORY_INDEX_PATH, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
                
        except Exception as e:
            print(f"[ERROR] Failed to clean MEMORY.md: {e}")
    
    def run_full_cycle(self) -> Dict[str, Any]:
        """执行完整的梦境周期"""
        print("[DREAM] Starting consolidation cycle...")
        
        # Phase 1: Orient
        print("[DREAM] Phase 1: Orienting...")
        orient_result = self.orient()
        print(f"  - Memory dirs: {orient_result['memory_dirs']}")
        print(f"  - Daily logs: {len(orient_result['daily_logs'])}")
        
        # Phase 2: Gather
        print("[DREAM] Phase 2: Gathering signals...")
        signals = self.gather()
        print(f"  - Signals gathered: {len(signals)}")
        
        # Phase 3: Consolidate
        print("[DREAM] Phase 3: Consolidating...")
        consolidate_result = self.consolidate(signals)
        print(f"  - Promoted: {len(consolidate_result['promoted'])}")
        print(f"  - Skipped: {len(consolidate_result['skipped'])}")
        
        # Phase 4: Prune
        print("[DREAM] Phase 4: Pruning...")
        prune_result = self.prune()
        print(f"  - Archived logs: {len(prune_result['archived_logs'])}")
        
        return {
            "stats": self.stats,
            "promoted_count": self.promoted_count,
            "pruned_count": self.pruned_count
        }


def main():
    parser = argparse.ArgumentParser(description="Dream Daemon - Memory Consolidation")
    parser.add_argument("command", choices=["consolidate", "status", "auto"],
                        help="consolidate: 执行整合 | status: 查看状态 | auto: 自动定时运行")
    parser.add_argument("--interval", type=int, default=86400,
                        help="auto模式的运行间隔（秒），默认86400（每天）")
    
    args = parser.parse_args()
    
    daemon = DreamDaemon()
    
    if args.command == "consolidate":
        result = daemon.run_full_cycle()
        print("\n[RESULT]")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    elif args.command == "status":
        orient_result = daemon.orient()
        print(json.dumps(orient_result, ensure_ascii=False, indent=2))
        
    elif args.command == "auto":
        print(f"[AUTO] Starting auto consolidation, interval: {args.interval}s")
        while True:
            try:
                daemon.run_full_cycle()
                time.sleep(args.interval)
            except KeyboardInterrupt:
                print("\n[AUTO] Stopped by user")
                break
            except Exception as e:
                print(f"[ERROR] {e}")
                time.sleep(60)  # 出错后等待1分钟重试


if __name__ == "__main__":
    main()
