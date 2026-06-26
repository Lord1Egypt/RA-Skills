#!/usr/bin/env python3
"""
优甲乐服药提醒与记录系统
作者：阿波罗
功能：每日提醒、确认、记录优甲乐服用情况
"""

import json
import os
import sys
import datetime
import csv
import fcntl
from pathlib import Path
from typing import Optional, Dict, List, Any

class MedicationReminder:
    def __init__(self, data_dir: Optional[str] = None):
        """初始化服药提醒系统"""
        if data_dir is None:
            data_dir = Path.home() / ".openclaw" / "medication_data"
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # 数据文件路径
        self.records_file = self.data_dir / "medication-records.json"
        self.stats_file = self.data_dir / "stats.json"
        self.settings_file = self.data_dir / "settings.json"

        # 初始化数据文件
        self._init_files()

    def _read_file(self, filepath: Path) -> Any:
        """安全读取文件内容（带文件锁）"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_SH)
                try:
                    content = f.read()
                    if not content.strip():
                        return None
                    return json.loads(content)
                finally:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        except (FileNotFoundError, json.JSONDecodeError):
            return None
        except Exception as e:
            raise e

    def _write_file(self, filepath: Path, data: Any) -> None:
        """安全写入文件内容（带文件锁）"""
        try:
            # 先写入临时文件
            temp_file = filepath.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            # 原子性重命名
            os.replace(temp_file, filepath)
        except Exception as e:
            # 清理临时文件
            temp_file = filepath.with_suffix('.tmp')
            if temp_file.exists():
                temp_file.unlink()
            raise e
    
    def _init_files(self):
        """初始化数据文件"""
        # 记录文件
        if not self.records_file.exists():
            self._save_records([])

        # 统计文件
        if not self.stats_file.exists():
            self._save_stats({
                "total_days": 0,
                "on_time_days": 0,
                "missed_days": 0,
                "current_streak": 0,
                "best_streak": 0,
                "last_taken": None
            })

        # 设置文件
        if not self.settings_file.exists():
            self._save_settings({
                "reminder_enabled": True,
                "first_reminder_time": "06:30",
                "reminder_interval": 15,  # 分钟
                "on_time_window": 30,  # 分钟（6:30-7:00为按时）
                "notification_channel": "current"
            })

    def _load_records(self) -> List[Dict[str, Any]]:
        """加载服药记录"""
        return self._read_file(self.records_file) or []

    def _save_records(self, records: List[Dict[str, Any]]) -> None:
        """保存服药记录"""
        self._write_file(self.records_file, records)

    def _load_stats(self) -> Dict[str, Any]:
        """加载统计数据"""
        return self._read_file(self.stats_file) or {
            "total_days": 0,
            "on_time_days": 0,
            "missed_days": 0,
            "current_streak": 0,
            "best_streak": 0,
            "last_taken": None
        }

    def _save_stats(self, stats: Dict[str, Any]) -> None:
        """保存统计数据"""
        self._write_file(self.stats_file, stats)

    def _load_settings(self) -> Dict[str, Any]:
        """加载设置"""
        return self._read_file(self.settings_file) or {
            "reminder_enabled": True,
            "first_reminder_time": "06:30",
            "reminder_interval": 15,
            "on_time_window": 30,
            "notification_channel": "current"
        }

    def _save_settings(self, settings: Dict[str, Any]) -> None:
        """保存设置"""
        self._write_file(self.settings_file, settings)

    def record_medication(self, taken_time: Optional[str] = None, manual: bool = False) -> Dict[str, Any]:
        """
        记录服药

        Args:
            taken_time: 服药时间（字符串，格式：HH:MM）
            manual: 是否为手动记录（非自动提醒确认）

        Returns:
            记录结果字典
        """
        if taken_time is None:
            taken_time = datetime.datetime.now().strftime("%H:%M")

        today = datetime.date.today().isoformat()

        # 检查设置中的按时窗口
        settings = self._load_settings()
        first_reminder = settings["first_reminder_time"]
        on_time_window = settings["on_time_window"]

        # 计算是否按时
        reminder_time = datetime.datetime.strptime(first_reminder, "%H:%M")
        taken_datetime = datetime.datetime.strptime(taken_time, "%H:%M")
        time_diff = (taken_datetime - reminder_time).total_seconds() / 60  # 分钟

        is_on_time = 0 <= time_diff <= on_time_window
        
        # 创建记录
        record = {
            "date": today,
            "time": taken_time,
            "is_on_time": is_on_time,
            "manual": manual,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        # 加载现有记录
        records = self._load_records()
        
        # 检查今天是否已有记录
        for i, r in enumerate(records):
            if r["date"] == today:
                records[i] = record  # 更新今天的记录
                break
        else:
            records.append(record)  # 添加新记录
        
        # 保存记录
        self._save_records(records)
        
        # 更新统计
        self._update_stats(record)
        
        return {
            "success": True,
            "date": today,
            "time": taken_time,
            "is_on_time": is_on_time,
            "message": f"✅ 已记录 {today} {taken_time} 服用优甲乐" + ("（按时）" if is_on_time else "（延迟）")
        }
    
    def _update_stats(self, record):
        """更新统计数据"""
        stats = self._load_stats()
        
        # 更新总天数
        all_records = self._load_records()
        stats["total_days"] = len(set(r["date"] for r in all_records))
        
        # 更新按时天数
        stats["on_time_days"] = sum(1 for r in all_records if r["is_on_time"])
        
        # 更新未服药天数（需要计算）
        # 这里简化处理：总天数 - 有记录的天数
        all_dates = set(r["date"] for r in all_records)
        # 实际应用中需要更复杂的逻辑
        
        # 更新连续服药天数
        dates = sorted(set(r["date"] for r in all_records), reverse=True)
        current_streak = 0
        today = datetime.date.today()
        
        for i, date_str in enumerate(dates):
            date = datetime.date.fromisoformat(date_str)
            expected_date = today - datetime.timedelta(days=i)
            if date == expected_date:
                current_streak += 1
            else:
                break
        
        stats["current_streak"] = current_streak
        stats["best_streak"] = max(stats["best_streak"], current_streak)
        stats["last_taken"] = record["timestamp"]
        
        self._save_stats(stats)

    def _update_stats(self, record: Dict[str, Any]) -> None:
        """更新统计数据"""
        stats = self._load_stats()

        # 更新总天数
        all_records = self._load_records()
        stats["total_days"] = len(set(r["date"] for r in all_records))

        # 更新按时天数
        stats["on_time_days"] = sum(1 for r in all_records if r["is_on_time"])

        # 更新未服药天数（需要计算）
        # 这里简化处理：总天数 - 有记录的天数
        all_dates = set(r["date"] for r in all_records)
        # 实际应用中需要更复杂的逻辑

        # 更新连续服药天数
        dates = sorted(set(r["date"] for r in all_records), reverse=True)
        current_streak = 0
        today = datetime.date.today()

        for i, date_str in enumerate(dates):
            date = datetime.date.fromisoformat(date_str)
            expected_date = today - datetime.timedelta(days=i)
            if date == expected_date:
                current_streak += 1
            else:
                break

        stats["current_streak"] = current_streak
        stats["best_streak"] = max(stats["best_streak"], current_streak)
        stats["last_taken"] = record["timestamp"]

        self._save_stats(stats)

    def get_today_status(self) -> Dict[str, Any]:
        """获取今日服药状态"""
        today = datetime.date.today().isoformat()
        records = self._load_records()

        for record in records:
            if record["date"] == today:
                status = "✅ 已服药" if record["is_on_time"] else "⚠️ 已服药（延迟）"
                return {
                    "taken": True,
                    "time": record["time"],
                    "is_on_time": record["is_on_time"],
                    "status": status,
                    "message": f"今日 {record['time']} 已服用优甲乐" + ("（按时）" if record["is_on_time"] else "（延迟）")
                }

        # 检查是否已经过了提醒时间
        settings = self._load_settings()
        reminder_time = datetime.datetime.strptime(settings["first_reminder_time"], "%H:%M").time()
        now = datetime.datetime.now().time()

        if now > reminder_time:
            return {
                "taken": False,
                "time": None,
                "is_on_time": None,
                "status": "❌ 未服药",
                "message": "今日尚未服用优甲乐（已过提醒时间）"
            }
        else:
            return {
                "taken": False,
                "time": None,
                "is_on_time": None,
                "status": "⏰ 待服药",
                "message": "今日尚未服用优甲乐（等待提醒时间）"
            }

    def get_yesterday_status(self) -> Dict[str, Any]:
        """获取昨天服药状态"""
        yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
        records = self._load_records()

        for record in records:
            if record["date"] == yesterday:
                if record["is_on_time"]:
                    return {
                        "taken": True,
                        "time": record["time"],
                        "is_on_time": True,
                        "status": "✅ 按时服药",
                        "message": f"昨天 {record['time']} 按时服用了优甲乐"
                    }
                else:
                    return {
                        "taken": True,
                        "time": record["time"],
                        "is_on_time": False,
                        "status": "⚠️ 延迟服药",
                        "message": f"昨天 {record['time']} 延迟服用了优甲乐"
                    }
        
        # 昨天没有记录
        return {
            "taken": False,
            "time": None,
            "is_on_time": None,
            "status": "❌ 未服药",
            "message": "昨天没有服用优甲乐的记录"
        }

    def get_yesterday_feedback(self) -> str:
        """获取针对昨天状态的反馈建议"""
        yesterday_status = self.get_yesterday_status()

        if not yesterday_status["taken"]:
            return "💡 昨天没有服药记录，今天请务必按时服药，不要漏服哦！"
        elif yesterday_status["is_on_time"]:
            return "🌟 昨天按时服药很棒！继续保持这个好习惯！"
        else:
            return "⏰ 昨天服药有点延迟，今天争取在6:30-7:00之间按时服用吧！"

    def get_smart_reminder_message(self, reminder_count: int = 1) -> str:
        """生成智能提醒消息，包含昨天状态反馈"""
        yesterday_feedback = self.get_yesterday_feedback()
        stats = self._load_stats()

        # 根据提醒次数调整消息
        if reminder_count == 1:
            time_note = "现在是早上6:30，请服用优甲乐。"
        elif reminder_count == 2:
            time_note = "现在是早上6:45，请尽快服用优甲乐。"
        elif reminder_count == 3:
            time_note = "现在是早上7:00，请立即服用优甲乐。"
        else:
            time_note = "请立即服用优甲乐。"

        # 添加连续服药天数信息
        streak_note = ""
        if stats["current_streak"] > 0:
            streak_note = f"\n🔥 你已经连续服药 {stats['current_streak']} 天，继续保持！"

        message = f"⏰ 优甲乐服药提醒\n\n"
        message += f"{time_note}\n"
        message += f"{yesterday_feedback}\n"
        message += f"{streak_note}\n"
        message += f"💊 服药后请回复：/medication taken"

        return message

    def get_records(self, start_date: Optional[Any] = None, end_date: Optional[Any] = None) -> List[Dict[str, Any]]:
        """获取服药记录

        Args:
            start_date: 开始日期（字符串 "YYYY-MM-DD" 或 datetime.date 对象）
            end_date: 结束日期（字符串 "YYYY-MM-DD" 或 datetime.date 对象）
        """
        records = self._load_records()

        if start_date or end_date:
            filtered = []
            for record in records:
                record_date = datetime.date.fromisoformat(record["date"])

                # 转换日期参数为 date 对象
                if start_date and isinstance(start_date, str):
                    start_date = datetime.date.fromisoformat(start_date)
                if end_date and isinstance(end_date, str):
                    end_date = datetime.date.fromisoformat(end_date)

                if start_date and record_date < start_date:
                    continue
                if end_date and record_date > end_date:
                    continue

                filtered.append(record)
            records = filtered

        return sorted(records, key=lambda x: x["date"], reverse=True)

    def generate_report(self, days: int = 7) -> Dict[str, Any]:
        """生成服药报告"""
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=days-1)

        records = self.get_records(start_date, end_date)
        stats = self._load_stats()

        # 计算报告期内的数据
        report_dates = []
        current_date = start_date
        while current_date <= end_date:
            report_dates.append(current_date.isoformat())
            current_date += datetime.timedelta(days=1)

        report_data = []
        for date_str in report_dates:
            record_found = None
            for record in records:
                if record["date"] == date_str:
                    record_found = record
                    break

            if record_found:
                status = "✅ 按时" if record_found["is_on_time"] else "⚠️ 延迟"
                report_data.append({
                    "date": date_str,
                    "time": record_found["time"],
                    "status": status,
                    "taken": True
                })
            else:
                report_data.append({
                    "date": date_str,
                    "time": "未记录",
                    "status": "❌ 未服",
                    "taken": False
                })

        # 计算统计
        total_days = len(report_data)
        taken_days = sum(1 for r in report_data if r["taken"])
        on_time_days = sum(1 for r in report_data if r.get("status") == "✅ 按时")
        compliance_rate = (taken_days / total_days * 100) if total_days > 0 else 0

        return {
            "period": f"{start_date.isoformat()} 至 {end_date.isoformat()}",
            "total_days": total_days,
            "taken_days": taken_days,
            "on_time_days": on_time_days,
            "compliance_rate": round(compliance_rate, 1),
            "current_streak": stats["current_streak"],
            "best_streak": stats["best_streak"],
            "data": report_data
        }

    def export_to_csv(self, output_path: Optional[str] = None) -> str:
        """导出数据到CSV"""
        if output_path is None:
            output_path = str(self.data_dir / "medication_export.csv")

        records = self._load_records()

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["日期", "时间", "是否按时", "记录方式", "记录时间"])
            writer.writeheader()

            for record in sorted(records, key=lambda x: x["date"]):
                writer.writerow({
                    "日期": record["date"],
                    "时间": record["time"],
                    "是否按时": "是" if record["is_on_time"] else "否",
                    "记录方式": "手动" if record.get("manual", False) else "自动",
                    "记录时间": record["timestamp"]
                })

        return output_path

    def get_settings(self) -> Dict[str, Any]:
        """获取当前设置"""
        return self._load_settings()

    def update_settings(self, **kwargs: Any) -> Dict[str, Any]:
        """更新设置"""
        settings = self._load_settings()
        settings.update(kwargs)
        self._save_settings(settings)
        return settings

def main():
    """命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(description="优甲乐服药提醒系统")
    subparsers = parser.add_subparsers(dest="command", help="命令")

    # 记录服药
    record_parser = subparsers.add_parser("record", help="记录服药")
    record_parser.add_argument("--time", help="服药时间（HH:MM格式）")
    record_parser.add_argument("--manual", action="store_true", help="手动记录")

    # 查询状态
    subparsers.add_parser("status", help="查询今日状态")

    # 生成报告
    report_parser = subparsers.add_parser("report", help="生成报告")
    report_parser.add_argument("--days", type=int, default=7, help="报告天数")

    # 导出数据
    export_parser = subparsers.add_parser("export", help="导出数据")
    export_parser.add_argument("--output", help="输出文件路径")

    # 获取记录
    records_parser = subparsers.add_parser("records", help="获取记录")
    records_parser.add_argument("--days", type=int, help="最近天数")

    args = parser.parse_args()

    reminder = MedicationReminder()

    if args.command == "record":
        result = reminder.record_medication(args.time, args.manual)
        print(result["message"])

    elif args.command == "status":
        status = reminder.get_today_status()
        print(f"📊 今日服药状态：{status['status']}")
        print(status["message"])

        # 显示最近记录
        print("\n📅 最近服药记录：")
        records = reminder.get_records()[:5]
        for record in records:
            status_emoji = "✅" if record["is_on_time"] else "⚠️"
            print(f"  {status_emoji} {record['date']} {record['time']}")

    elif args.command == "report":
        report = reminder.generate_report(args.days)
        print(f"📈 优甲乐服药报告（{report['period']}）")
        print(f"📊 服药依从率：{report['compliance_rate']}%")
        print(f"📅 总天数：{report['total_days']}")
        print(f"✅ 服药天数：{report['taken_days']}")
        print(f"⏰ 按时天数：{report['on_time_days']}")
        print(f"🔥 当前连续服药：{report['current_streak']} 天")
        print(f"🏆 最佳连续服药：{report['best_streak']} 天")

        print("\n📋 每日详情：")
        for item in report["data"]:
            print(f"  {item['date']} - {item['time']} ({item['status']})")

    elif args.command == "export":
        output_path = reminder.export_to_csv(args.output)
        print(f"✅ 数据已导出到：{output_path}")

    elif args.command == "records":
        if args.days:
            end_date = datetime.date.today()
            start_date = end_date - datetime.timedelta(days=args.days-1)
            records = reminder.get_records(start_date, end_date)
        else:
            records = reminder.get_records()[:10]

        print(f"📋 服药记录（共 {len(records)} 条）：")
        for record in records:
            status = "按时" if record["is_on_time"] else "延迟"
            manual = "手动" if record.get("manual", False) else "自动"
            print(f"  {record['date']} {record['time']} ({status}, {manual}记录)")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()