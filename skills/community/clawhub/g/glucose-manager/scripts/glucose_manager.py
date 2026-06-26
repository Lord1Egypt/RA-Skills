#!/usr/bin/env python3
"""
血糖数据管理脚本
Blood Glucose Data Manager

功能：
- 添加血糖记录
- 导入数据（CSV、Excel、JSON）
- 导出数据
- 查询记录
- 删除记录
"""

import json
import csv
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import uuid

# 尝试导入 pandas（用于 Excel 支持）
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

# 默认数据文件路径
DEFAULT_DATA_PATH = Path.home() / ".workbuddy" / "glucose_data.json"


class GlucoseManager:
    """血糖数据管理器"""
    
    def __init__(self, data_path: Optional[Path] = None):
        """
        初始化管理器
        
        Args:
            data_path: 数据文件路径，默认为 ~/.workbuddy/glucose_data.json
        """
        self.data_path = data_path or DEFAULT_DATA_PATH
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """加载数据文件"""
        if not self.data_path.exists():
            # 创建默认数据结构
            default_data = {
                "records": [],
                "user_profile": {
                    "diabetes_type": None,
                    "target_range": {
                        "fasting_min": 4.4,
                        "fasting_max": 7.0,
                        "post_meal_max": 10.0,
                        "bedtime_min": 6.0,
                        "bedtime_max": 8.0
                    }
                },
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "version": "1.0"
                }
            }
            # 确保目录存在
            self.data_path.parent.mkdir(parents=True, exist_ok=True)
            self._save_data(default_data)
            return default_data
        
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载数据失败: {e}")
            return {"records": [], "user_profile": {}, "metadata": {}}
    
    def _save_data(self, data: Optional[Dict] = None):
        """保存数据到文件"""
        if data is None:
            data = self.data
        
        data["metadata"]["last_updated"] = datetime.now().isoformat()
        
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def add_record(
        self,
        glucose_value: float,
        measurement_type: str = "random",
        timestamp: Optional[str] = None,
        meal_info: Optional[Dict] = None,
        exercise_info: Optional[Dict] = None,
        medication_info: Optional[Dict] = None,
        notes: str = "",
        tags: List[str] = None
    ) -> Dict:
        """
        添加血糖记录
        
        Args:
            glucose_value: 血糖值 (mmol/L)
            measurement_type: 测量类型 (fasting/pre_meal/post_meal/random/bedtime)
            timestamp: 测量时间，ISO格式字符串，默认当前时间
            meal_info: 饮食信息 {"carbs_g": float, "description": str}
            exercise_info: 运动信息 {"type": str, "duration_min": int}
            medication_info: 用药信息 {"name": str, "dose": str}
            notes: 备注
            tags: 标签列表
        
        Returns:
            新创建的记录
        """
        record = {
            "id": str(uuid.uuid4()),
            "timestamp": timestamp or datetime.now().isoformat(),
            "glucose_value": round(glucose_value, 1),
            "unit": "mmol/L",
            "measurement_type": measurement_type,
            "meal_info": meal_info or {},
            "exercise_info": exercise_info or {},
            "medication_info": medication_info or {},
            "notes": notes,
            "tags": tags or []
        }
        
        self.data["records"].append(record)
        self._save_data()
        
        return record
    
    def get_records(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        measurement_type: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[Dict]:
        """
        查询记录
        
        Args:
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            measurement_type: 测量类型过滤
            limit: 限制返回数量
        
        Returns:
            记录列表
        """
        records = self.data["records"]
        
        # 日期过滤
        if start_date:
            start_dt = datetime.fromisoformat(start_date)
            records = [r for r in records if datetime.fromisoformat(r["timestamp"]) >= start_dt]
        
        if end_date:
            end_dt = datetime.fromisoformat(end_date) + timedelta(days=1)
            records = [r for r in records if datetime.fromisoformat(r["timestamp"]) < end_dt]
        
        # 类型过滤
        if measurement_type:
            records = [r for r in records if r["measurement_type"] == measurement_type]
        
        # 按时间排序（最新在前）
        records = sorted(records, key=lambda x: x["timestamp"], reverse=True)
        
        # 限制数量
        if limit:
            records = records[:limit]
        
        return records
    
    def get_recent(self, hours: int = 24) -> List[Dict]:
        """
        获取最近的记录
        
        Args:
            hours: 最近多少小时
        
        Returns:
            记录列表
        """
        start_time = datetime.now() - timedelta(hours=hours)
        return self.get_records(start_date=start_time.isoformat())
    
    def delete_record(self, record_id: str) -> bool:
        """
        删除记录
        
        Args:
            record_id: 记录ID
        
        Returns:
            是否成功删除
        """
        original_count = len(self.data["records"])
        self.data["records"] = [r for r in self.data["records"] if r["id"] != record_id]
        
        if len(self.data["records"]) < original_count:
            self._save_data()
            return True
        return False
    
    def import_data(
        self,
        file_path: str,
        format_type: Optional[str] = None,
        column_mapping: Optional[Dict] = None
    ) -> Dict:
        """
        从文件导入数据
        
        Args:
            file_path: 文件路径
            format_type: 文件格式 (csv/excel/json)，自动检测如果为None
            column_mapping: 列映射，用于指定哪些列对应哪些字段
        
        Returns:
            导入结果统计
        """
        path = Path(file_path)
        
        # 自动检测格式
        if format_type is None:
            suffix = path.suffix.lower()
            if suffix == '.csv':
                format_type = 'csv'
            elif suffix in ['.xlsx', '.xls']:
                format_type = 'excel'
            elif suffix == '.json':
                format_type = 'json'
            else:
                return {"success": False, "error": f"不支持的文件格式: {suffix}"}
        
        try:
            if format_type == 'json':
                return self._import_json(file_path)
            elif format_type == 'csv':
                return self._import_csv(file_path, column_mapping)
            elif format_type == 'excel':
                return self._import_excel(file_path, column_mapping)
            else:
                return {"success": False, "error": f"不支持的格式: {format_type}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _import_json(self, file_path: str) -> Dict:
        """导入 JSON 文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            imported_data = json.load(f)
        
        if isinstance(imported_data, list):
            # 列表格式
            records = imported_data
        elif isinstance(imported_data, dict) and "records" in imported_data:
            # 完整数据结构
            records = imported_data["records"]
        else:
            return {"success": False, "error": "JSON格式不正确"}
        
        # 为每条记录添加ID（如果没有）
        for record in records:
            if "id" not in record:
                record["id"] = str(uuid.uuid4())
        
        self.data["records"].extend(records)
        self._save_data()
        
        return {
            "success": True,
            "imported_count": len(records),
            "total_records": len(self.data["records"])
        }
    
    def _import_csv(self, file_path: str, column_mapping: Optional[Dict] = None) -> Dict:
        """导入 CSV 文件"""
        # 默认列映射
        default_mapping = {
            "timestamp": ["时间", "timestamp", "time", "date", "日期"],
            "glucose_value": ["血糖", "血糖值", "glucose", "value", "glucose_value"],
            "measurement_type": ["类型", "type", "measurement_type", "测量类型"]
        }
        
        mapping = column_mapping or default_mapping
        imported_count = 0
        errors = []
        
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            
            for row_idx, row in enumerate(reader, start=2):
                try:
                    record = self._parse_row(row, mapping)
                    if record:
                        record["id"] = str(uuid.uuid4())
                        self.data["records"].append(record)
                        imported_count += 1
                except Exception as e:
                    errors.append(f"第{row_idx}行: {str(e)}")
        
        self._save_data()
        
        return {
            "success": True,
            "imported_count": imported_count,
            "total_records": len(self.data["records"]),
            "errors": errors[:10]  # 只返回前10个错误
        }
    
    def _import_excel(self, file_path: str, column_mapping: Optional[Dict] = None) -> Dict:
        """导入 Excel 文件"""
        if not PANDAS_AVAILABLE:
            return {"success": False, "error": "需要安装 pandas 库才能导入 Excel 文件"}
        
        df = pd.read_excel(file_path)
        
        # 默认列映射
        default_mapping = {
            "timestamp": ["时间", "timestamp", "time", "date", "日期"],
            "glucose_value": ["血糖", "血糖值", "glucose", "value", "glucose_value"],
            "measurement_type": ["类型", "type", "measurement_type", "测量类型"]
        }
        
        mapping = column_mapping or default_mapping
        imported_count = 0
        errors = []
        
        for idx, row in df.iterrows():
            try:
                record = self._parse_row(row.to_dict(), mapping)
                if record:
                    record["id"] = str(uuid.uuid4())
                    self.data["records"].append(record)
                    imported_count += 1
            except Exception as e:
                errors.append(f"第{idx+2}行: {str(e)}")
        
        self._save_data()
        
        return {
            "success": True,
            "imported_count": imported_count,
            "total_records": len(self.data["records"]),
            "errors": errors[:10]
        }
    
    def _parse_row(self, row: Dict, mapping: Dict) -> Optional[Dict]:
        """解析数据行为记录"""
        record = {
            "timestamp": None,
            "glucose_value": None,
            "unit": "mmol/L",
            "measurement_type": "random",
            "meal_info": {},
            "exercise_info": {},
            "medication_info": {},
            "notes": "",
            "tags": []
        }
        
        # 查找并映射字段
        for field, possible_names in mapping.items():
            for name in possible_names:
                if name in row and row[name] is not None and str(row[name]).strip():
                    value = row[name]
                    
                    if field == "timestamp":
                        # 尝试解析时间
                        if isinstance(value, datetime):
                            record["timestamp"] = value.isoformat()
                        else:
                            # 尝试多种日期格式
                            for fmt in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d", "%Y/%m/%d %H:%M", "%Y/%m/%d"]:
                                try:
                                    dt = datetime.strptime(str(value), fmt)
                                    record["timestamp"] = dt.isoformat()
                                    break
                                except ValueError:
                                    continue
                            if not record["timestamp"]:
                                record["timestamp"] = datetime.now().isoformat()
                    
                    elif field == "glucose_value":
                        try:
                            # 清理数值字符串
                            val_str = str(value).replace(',', '.').strip()
                            record["glucose_value"] = round(float(val_str), 1)
                        except (ValueError, TypeError):
                            return None
                    
                    elif field == "measurement_type":
                        type_str = str(value).lower()
                        type_mapping = {
                            "空腹": "fasting", "fasting": "fasting",
                            "餐前": "pre_meal", "pre_meal": "pre_meal", "餐前血糖": "pre_meal",
                            "餐后": "post_meal", "post_meal": "post_meal", "餐后血糖": "post_meal",
                            "睡前": "bedtime", "bedtime": "bedtime",
                            "随机": "random", "random": "random"
                        }
                        record["measurement_type"] = type_mapping.get(type_str, "random")
        
        # 验证必需字段
        if record["glucose_value"] is None:
            return None
        
        if not record["timestamp"]:
            record["timestamp"] = datetime.now().isoformat()
        
        return record
    
    def export_data(
        self,
        output_path: str,
        format_type: str = "json",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict:
        """
        导出数据到文件
        
        Args:
            output_path: 输出文件路径
            format_type: 导出格式 (json/csv/excel)
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            导出结果
        """
        records = self.get_records(start_date, end_date)
        
        try:
            if format_type == 'json':
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump({
                        "records": records,
                        "exported_at": datetime.now().isoformat()
                    }, f, ensure_ascii=False, indent=2)
            
            elif format_type == 'csv':
                with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
                    if records:
                        fieldnames = ["timestamp", "glucose_value", "unit", "measurement_type", "notes"]
                        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
                        writer.writeheader()
                        writer.writerows(records)
            
            elif format_type == 'excel':
                if not PANDAS_AVAILABLE:
                    return {"success": False, "error": "需要安装 pandas 库才能导出 Excel 文件"}
                
                df = pd.DataFrame(records)
                df.to_excel(output_path, index=False)
            
            else:
                return {"success": False, "error": f"不支持的导出格式: {format_type}"}
            
            return {
                "success": True,
                "exported_count": len(records),
                "output_path": output_path
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_statistics(self, days: int = 30) -> Dict:
        """
        获取统计信息
        
        Args:
            days: 统计最近多少天
        
        Returns:
            统计信息
        """
        start_date = (datetime.now() - timedelta(days=days)).isoformat()
        records = self.get_records(start_date=start_date)
        
        if not records:
            return {
                "total_records": 0,
                "avg_glucose": None,
                "min_glucose": None,
                "max_glucose": None,
                "time_in_range": None
            }
        
        values = [r["glucose_value"] for r in records]
        
        # 目标范围（默认）
        target_min = 4.4
        target_max = 10.0
        
        in_range_count = sum(1 for v in values if target_min <= v <= target_max)
        
        return {
            "total_records": len(records),
            "avg_glucose": round(sum(values) / len(values), 1),
            "min_glucose": min(values),
            "max_glucose": max(values),
            "std_dev": round(self._calculate_std(values), 2),
            "time_in_range": round(in_range_count / len(values) * 100, 1),
            "period_days": days
        }
    
    def _calculate_std(self, values: List[float]) -> float:
        """计算标准差"""
        if len(values) < 2:
            return 0.0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
        return variance ** 0.5


# 命令行接口
def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法:")
        print("  python glucose_manager.py add <glucose_value> [measurement_type]")
        print("  python glucose_manager.py list [days]")
        print("  python glucose_manager.py stats [days]")
        print("  python glucose_manager.py import <file_path>")
        print("  python glucose_manager.py export <output_path> [format]")
        return
    
    manager = GlucoseManager()
    command = sys.argv[1]
    
    if command == "add":
        if len(sys.argv) < 3:
            print("错误: 请提供血糖值")
            return
        
        glucose_value = float(sys.argv[2])
        measurement_type = sys.argv[3] if len(sys.argv) > 3 else "random"
        
        record = manager.add_record(glucose_value, measurement_type)
        print(f"已添加记录: {record['glucose_value']} mmol/L ({record['measurement_type']})")
    
    elif command == "list":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        records = manager.get_records(
            start_date=(datetime.now() - timedelta(days=days)).isoformat()
        )
        
        print(f"\n最近 {days} 天的血糖记录 ({len(records)} 条):")
        print("-" * 80)
        for r in records:
            time_str = datetime.fromisoformat(r["timestamp"]).strftime("%Y-%m-%d %H:%M")
            print(f"{time_str} | {r['glucose_value']:5.1f} mmol/L | {r['measurement_type']:10s} | {r['notes']}")
    
    elif command == "stats":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        stats = manager.get_statistics(days)
        
        print(f"\n最近 {days} 天的血糖统计:")
        print("-" * 40)
        print(f"记录数量: {stats['total_records']}")
        if stats['avg_glucose']:
            print(f"平均血糖: {stats['avg_glucose']} mmol/L")
            print(f"最低血糖: {stats['min_glucose']} mmol/L")
            print(f"最高血糖: {stats['max_glucose']} mmol/L")
            print(f"标准差: {stats['std_dev']}")
            print(f"目标范围内时间: {stats['time_in_range']}%")
    
    elif command == "import":
        if len(sys.argv) < 3:
            print("错误: 请提供文件路径")
            return
        
        result = manager.import_data(sys.argv[2])
        if result["success"]:
            print(f"导入成功: {result['imported_count']} 条记录")
            if result.get("errors"):
                print(f"警告: {len(result['errors'])} 行有错误")
        else:
            print(f"导入失败: {result['error']}")
    
    elif command == "export":
        if len(sys.argv) < 3:
            print("错误: 请提供输出路径")
            return
        
        format_type = sys.argv[3] if len(sys.argv) > 3 else "json"
        result = manager.export_data(sys.argv[2], format_type)
        
        if result["success"]:
            print(f"导出成功: {result['exported_count']} 条记录 -> {result['output_path']}")
        else:
            print(f"导出失败: {result['error']}")
    
    else:
        print(f"未知命令: {command}")


if __name__ == "__main__":
    main()
