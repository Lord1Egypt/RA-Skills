#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entropy Reduce Script - Context-Manager 熵减脚本

功能：识别并清理低价值内容，保留核心认知

用法:
    python scripts/entropy_reduce.py [--dry-run] [--force]
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

class EntropyReduce:
    """熵减引擎"""
    
    def __init__(self, data_path=None):
        self.data_path = Path(data_path) if data_path else Path(__file__).parent.parent / "data"
        self.journal_path = self.data_path / "journal"
        self.external_path = self.data_path / "external"
        self.core_path = self.data_path / "core"
        self.connections_path = self.data_path / "connections" / "connections.json"
        
        # 统计信息
        self.stats = {
            "scanned": 0,
            "low_value": 0,
            "to_delete": [],
            "to_keep": [],
            "core_updated": False
        }
    
    def load_connections(self):
        """加载认知连接"""
        if not self.connections_path.exists():
            return {}
        
        with open(self.connections_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def count_connections(self, note_name):
        """计算笔记的连接数"""
        connections = self.load_connections()
        
        count = 0
        for conn in connections.get("connections", []):
            if note_name in conn.get("nodes", []):
                count += 1
        
        return count
    
    def has_inner_judgment(self, content):
        """检查是否有内心判断"""
        judgment_keywords = [
            "我的判断", "我觉得", "我认为", "我的感受",
            "触动", "启发", "想到", "反思"
        ]
        
        for keyword in judgment_keywords:
            if keyword in content:
                return True
        
        return False
    
    def is_core_content(self, content):
        """检查是否属于最小内核"""
        core_keywords = [
            "#原则#", "#信念#", "#决策机制#", "#重要关注#",
            "最小内核", "core", "kernel"
        ]
        
        for keyword in core_keywords:
            if keyword in content:
                return True
        
        return False
    
    def scan_journal(self):
        """扫描日记"""
        print("  扫描 journal/ ...")
        
        if not self.journal_path.exists():
            print("    目录不存在")
            return
        
        for md_file in self.journal_path.glob("*.md"):
            self.stats["scanned"] += 1
            
            try:
                content = md_file.read_text(encoding='utf-8')
            except Exception as e:
                print(f"    读取失败 {md_file.name}: {e}")
                continue
            
            # 检查是否低价值
            reasons = []
            
            # 1. 无内心判断
            if not self.has_inner_judgment(content):
                reasons.append("无内心判断")
            
            # 2. 连接数少
            conn_count = self.count_connections(md_file.stem)
            if conn_count == 0:
                reasons.append("无连接")
            
            # 3. 过时（超过 90 天无更新）
            mtime = datetime.fromtimestamp(md_file.stat().st_mtime)
            if datetime.now() - mtime > timedelta(days=90):
                reasons.append("超过 90 天无更新")
            
            # 判断是否低价值
            if len(reasons) >= 2:  # 至少 2 个问题才标记为低价值
                self.stats["low_value"] += 1
                self.stats["to_delete"].append({
                    "path": str(md_file),
                    "reasons": reasons
                })
            else:
                self.stats["to_keep"].append(str(md_file))
    
    def scan_external(self):
        """扫描外部信息"""
        print("  扫描 external/ ...")
        
        if not self.external_path.exists():
            print("    目录不存在")
            return
        
        for md_file in self.external_path.rglob("*.md"):
            self.stats["scanned"] += 1
            
            try:
                content = md_file.read_text(encoding='utf-8')
            except Exception as e:
                print(f"    读取失败 {md_file.name}: {e}")
                continue
            
            # 检查是否低价值
            reasons = []
            
            # 1. 无内心判断
            if not self.has_inner_judgment(content):
                reasons.append("无内心判断")
            
            # 2. 连接数少
            conn_count = self.count_connections(md_file.stem)
            if conn_count == 0:
                reasons.append("无连接")
            
            # 判断是否低价值
            if len(reasons) >= 2:
                self.stats["low_value"] += 1
                self.stats["to_delete"].append({
                    "path": str(md_file),
                    "reasons": reasons
                })
            else:
                self.stats["to_keep"].append(str(md_file))
    
    def update_minimal_kernel(self):
        """更新最小内核"""
        print("  更新最小内核...")
        
        # 确保目录存在
        self.core_path.mkdir(parents=True, exist_ok=True)
        
        kernel_path = self.core_path / "minimal-kernel.md"
        
        if not kernel_path.exists():
            # 创建默认最小内核
            default_kernel = """# 我的最小内核

## 原则
（待完善：你坚信的做事方式）

## 信念
（待完善：你认可的世界观）

## 决策机制
（待完善：你做判断的标准）

## 重要关注
（待完善：你持续投入的领域）

---
*最后更新*: """ + datetime.now().strftime('%Y-%m-%d')
            
            kernel_path.write_text(default_kernel, encoding='utf-8')
            print("    创建默认最小内核")
        else:
            print("    最小内核已存在")
        
        self.stats["core_updated"] = True
    
    def generate_report(self):
        """生成熵减报告"""
        report = f"""## 熵减报告 - {datetime.now().strftime('%Y-%m-%d %H:%M')}

### 统计信息
- 扫描文件数：{self.stats['scanned']}
- 低价值内容：{self.stats['low_value']}
- 待删除：{len(self.stats['to_delete'])}
- 待保留：{len(self.stats['to_keep'])}
- 最小内核：{"已更新" if self.stats['core_updated'] else "未更新"}

### 待删除内容
"""
        
        for item in self.stats["to_delete"][:20]:  # 只显示前 20 个
            report += f"- `{item['path']}`\n"
            report += f"  原因：{', '.join(item['reasons'])}\n"
        
        if len(self.stats["to_delete"]) > 20:
            report += f"- ... 还有 {len(self.stats['to_delete']) - 20} 个\n"
        
        return report
    
    def run(self, dry_run=False, force=False):
        """运行熵减流程"""
        print("🧹 开始熵减...")
        print(f"  数据目录：{self.data_path}")
        print()
        
        if dry_run:
            print("🔍 模拟运行模式（不删除文件）")
            print()
        
        # 扫描
        self.scan_journal()
        self.scan_external()
        
        print()
        
        # 更新最小内核
        self.update_minimal_kernel()
        
        print()
        
        # 生成报告
        report = self.generate_report()
        print(report)
        
        # 删除文件
        if not dry_run and force:
            print("🗑️  执行删除...")
            for item in self.stats["to_delete"]:
                try:
                    Path(item["path"]).unlink()
                    print(f"  删除：{item['path']}")
                except Exception as e:
                    print(f"  删除失败 {item['path']}: {e}")
        elif not dry_run:
            print("💡 提示：使用 --force 参数执行删除")
        
        print()
        print("✅ 熵减完成")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Entropy Reduce - Context-Manager 熵减脚本')
    parser.add_argument('--dry-run', action='store_true', help='模拟运行，不删除文件')
    parser.add_argument('--force', action='store_true', help='强制执行删除')
    
    args = parser.parse_args()
    
    reducer = EntropyReduce()
    reducer.run(dry_run=args.dry_run, force=args.force)


if __name__ == '__main__':
    main()
