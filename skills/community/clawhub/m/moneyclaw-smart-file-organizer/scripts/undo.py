#!/usr/bin/env python3
"""
撤销操作工具 - 恢复文件整理操作
"""

import json
import shutil
from pathlib import Path
import argparse
from datetime import datetime

class UndoManager:
    def __init__(self, log_file=None):
        self.log_file = log_file
        self.operations = []
        
        if log_file and Path(log_file).exists():
            self.load_operations(log_file)
    
    def load_operations(self, log_file):
        """从日志文件加载操作"""
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line in lines:
                line = line.strip()
                if not line or line.startswith("#") or "整理统计:" in line:
                    continue
                
                # 解析操作日志
                if "移动:" in line:
                    parts = line.split("移动:")
                    if len(parts) > 1:
                        op_parts = parts[1].strip().split("→")
                        if len(op_parts) == 2:
                            source = op_parts[0].strip()
                            target = op_parts[1].strip()
                            self.operations.append({
                                "type": "move",
                                "source": source,
                                "target": target,
                                "original_line": line
                            })
                elif "删除重复文件:" in line:
                    parts = line.split("删除重复文件:")
                    if len(parts) > 1:
                        filename = parts[1].strip()
                        self.operations.append({
                            "type": "delete",
                            "filename": filename,
                            "original_line": line
                        })
                elif "移动重复文件到:" in line:
                    parts = line.split("移动重复文件到:")
                    if len(parts) > 1:
                        target = parts[1].strip()
                        self.operations.append({
                            "type": "move_duplicate",
                            "target": target,
                            "original_line": line
                        })
        
        except Exception as e:
            print(f"❌ 加载日志文件失败: {e}")
    
    def undo_last_operation(self, preview=False):
        """撤销最后一次操作"""
        if not self.operations:
            print("📭 没有可撤销的操作")
            return False
        
        last_op = self.operations[-1]
        print(f"↩️  撤销操作: {last_op['type']}")
        
        if preview:
            print(f"  预览模式 - 不会实际执行")
        
        success = False
        try:
            if last_op["type"] == "move":
                source = last_op["target"]
                target = last_op["source"]
                
                source_path = Path(source)
                target_path = Path(target)
                
                if preview:
                    print(f"  将移动: {source} → {target}")
                else:
                    if source_path.exists():
                        # 确保目标目录存在
                        target_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(source_path), str(target_path))
                        print(f"  ✅ 已恢复: {source} → {target}")
                        success = True
                    else:
                        print(f"  ❌ 源文件不存在: {source}")
            
            elif last_op["type"] == "delete":
                # 删除操作无法撤销，只能从备份恢复
                print(f"  ⚠️  删除操作无法直接撤销")
                print(f"  请检查备份目录: Backup/")
                success = False
            
            elif last_op["type"] == "move_duplicate":
                target = last_op["target"]
                target_path = Path(target)
                
                if preview:
                    print(f"  将恢复重复文件: {target}")
                else:
                    if target_path.exists():
                        # 尝试找到原位置（基于文件名）
                        filename = target_path.name
                        possible_locations = [
                            Path(".") / filename,
                            Path("Documents") / filename,
                            Path("Images") / filename,
                            Path("Videos") / filename,
                            Path("Audio") / filename,
                            Path("Archives") / filename,
                            Path("Code") / filename
                        ]
                        
                        for loc in possible_locations:
                            if not loc.exists():
                                target_path.rename(loc)
                                print(f"  ✅ 已恢复: {target} → {loc}")
                                success = True
                                break
                        
                        if not success:
                            print(f"  ❌ 无法确定原位置，文件保持在: {target}")
                    else:
                        print(f"  ❌ 文件不存在: {target}")
            
            if success and not preview:
                # 从操作列表中移除
                self.operations.pop()
            
        except Exception as e:
            print(f"  ❌ 撤销操作失败: {e}")
            success = False
        
        return success
    
    def undo_all_operations(self, preview=False):
        """撤销所有操作"""
        if not self.operations:
            print("📭 没有可撤销的操作")
            return 0
        
        total = len(self.operations)
        print(f"↩️  撤销所有操作 ({total}个)")
        
        if preview:
            print("  预览模式 - 不会实际执行")
            for i, op in enumerate(reversed(self.operations), 1):
                print(f"  {i}. {op['type']}: {op.get('source', op.get('filename', 'N/A'))}")
            return total
        
        success_count = 0
        failed_count = 0
        
        while self.operations:
            success = self.undo_last_operation(preview=False)
            if success:
                success_count += 1
            else:
                failed_count += 1
                # 跳过失败的操作
                if self.operations:
                    self.operations.pop()
        
        print(f"\n📊 撤销完成:")
        print(f"  ✅ 成功: {success_count}")
        print(f"  ❌ 失败: {failed_count}")
        print(f"  📋 总计: {total}")
        
        return success_count
    
    def list_operations(self, limit=20):
        """列出操作历史"""
        if not self.operations:
            print("📭 没有操作历史")
            return
        
        print(f"📋 操作历史 ({len(self.operations)}个):")
        print("-" * 60)
        
        for i, op in enumerate(reversed(self.operations[:limit]), 1):
            timestamp = "未知时间"
            if "original_line" in op:
                # 尝试从日志行提取时间
                line = op["original_line"]
                if line.startswith("["):
                    timestamp = line[1:9]  # 提取 [HH:MM:SS]
            
            op_type = op["type"]
            if op_type == "move":
                desc = f"{op['source']} → {op['target']}"
            elif op_type == "delete":
                desc = f"删除: {op['filename']}"
            elif op_type == "move_duplicate":
                desc = f"移动重复: {op['target']}"
            else:
                desc = str(op)
            
            print(f"{i:2d}. [{timestamp}] {op_type:15} {desc[:40]}{'...' if len(desc) > 40 else ''}")
        
        if len(self.operations) > limit:
            print(f"... 还有 {len(self.operations) - limit} 个操作未显示")

def main():
    parser = argparse.ArgumentParser(description="撤销文件整理操作")
    parser.add_argument("action", choices=["list", "undo", "undo-all"], help="操作类型")
    parser.add_argument("--log", default="organize_log.txt", help="日志文件路径")
    parser.add_argument("--preview", action="store_true", help="预览模式")
    parser.add_argument("--limit", type=int, default=20, help="列出操作数量限制")
    
    args = parser.parse_args()
    
    undo_manager = UndoManager(args.log)
    
    if args.action == "list":
        undo_manager.list_operations(args.limit)
    elif args.action == "undo":
        undo_manager.undo_last_operation(args.preview)
    elif args.action == "undo-all":
        undo_manager.undo_all_operations(args.preview)

if __name__ == "__main__":
    main()