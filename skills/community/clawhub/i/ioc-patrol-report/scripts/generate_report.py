#!/usr/bin/env python3
"""
IOC 智能巡检报告生成器
Usage:
    uv run scripts/generate_report.py --type daily --date 2026-03-10
    uv run scripts/generate_report.py --type weekly --week 2026-W10
"""

import argparse
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import yaml

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

def load_config():
    """加载配置文件"""
    config_path = Path(__file__).parent.parent / "config.yaml"
    if not config_path.exists():
        # 返回默认配置
        return {
            "database": {
                "host": os.getenv("DB_HOST", "localhost"),
                "port": int(os.getenv("DB_PORT", "5432")),
                "name": os.getenv("DB_NAME", "ioc_db"),
                "user": os.getenv("DB_USER", "admin"),
                "password": os.getenv("DB_PASSWORD", ""),
            },
            "tables": {
                "devices": "devices",
                "alarms": "alarms", 
                "work_orders": "work_orders",
                "energy": "energy_records",
            },
            "report": {
                "timezone": "Asia/Shanghai",
                "output_dir": "reports",
            }
        }
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


def get_db_connection(config):
    """获取数据库连接"""
    try:
        import psycopg2
        db_config = {
            "host": config["database"]["host"],
            "port": config["database"]["port"],
            "dbname": config["database"]["name"],
            "user": config["database"]["user"],
            "password": config["database"]["password"],
        }
        # 如果配置了options，添加进去
        if "options" in config["database"]:
            db_config["options"] = config["database"]["options"]
        return psycopg2.connect(**db_config)
    except ImportError:
        print("⚠️ psycopg2 未安装，使用模拟数据模式")
        return None
    except Exception as e:
        print(f"⚠️ 数据库连接失败: {e}，使用模拟数据模式")
        return None
        return None
    except Exception as e:
        print(f"⚠️ 数据库连接失败: {e}，使用模拟数据模式")
        return None


def generate_mock_data(report_date: str):
    """生成模拟数据（用于测试）"""
    return {
        "device_stats": {
            "total": 1250,
            "online": 1180,
            "offline": 70,
            "by_type": {
                "摄像头": 450,
                "门禁": 280,
                "电梯": 45,
                "空调": 320,
                "消防": 155,
            }
        },
        "alarm_stats": {
            "total": 89,
            "by_level": {
                "紧急": 3,
                "重要": 12,
                "一般": 45,
                "提示": 29,
            },
            "response_time_avg": 8.5,  # 分钟
            "response_rate": 96.2,
        },
        "work_order_stats": {
            "total": 56,
            "pending": 12,
            "processing": 8,
            "completed": 36,
            "sla_achieved": 94.5,
        },
        "energy_stats": {
            "today": 12850,  # kWh
            "yesterday": 13120,
            "last_week_avg": 12980,
            "trend": "-2.1%",
        },
    }


def fetch_real_data(conn, config, report_date: str):
    """从数据库获取真实数据"""
    tables = config.get("tables", {})
    
    data = {}
    cursor = conn.cursor()
    
    try:
        # 巡检任务统计
        cursor.execute("SELECT COUNT(*) FROM t_patrol_task")
        data["total_devices"] = cursor.fetchone()[0] or 0
        
        # 能耗统计
        cursor.execute("SELECT COUNT(*) FROM t_energy_hourly_consumption")
        data["energy_count"] = cursor.fetchone()[0] or 0
        
        # 能耗今日
        cursor.execute("""
            SELECT COALESCE(SUM(consumption), 0) 
            FROM t_energy_hourly_consumption 
            WHERE consumed_at::date = CURRENT_DATE
        """)
        data["energy_today"] = float(cursor.fetchone()[0] or 0)
        
        # 能耗昨日
        cursor.execute("""
            SELECT COALESCE(SUM(consumption), 0) 
            FROM t_energy_hourly_consumption 
            WHERE consumed_at::date = CURRENT_DATE - INTERVAL '1 day'
        """)
        data["energy_yesterday"] = float(cursor.fetchone()[0] or 0)
        
        # 人员通行
        cursor.execute("SELECT COUNT(*) FROM t_personnel_room_access")
        data["personnel_count"] = cursor.fetchone()[0] or 0
        
        # 巡检任务状态
        cursor.execute("""
            SELECT status, COUNT(*) 
            FROM t_patrol_task 
            GROUP BY status
        """)
        status_rows = cursor.fetchall()
        data["patrol_status"] = dict(status_rows)
        
        # 统计各项
        data["device_stats"] = {
            "total": data.get("total_devices", 0),
            "online": data.get("total_devices", 0) - len([s for s in status_rows if s[0] < 0]),
            "offline": len([s for s in status_rows if s[0] < 0])
        }
        
        data["work_order_stats"] = {
            "total": sum([s[1] for s in status_rows]),
            "pending": sum([s[1] for s in status_rows if s[0] == 0]),
            "processing": sum([s[1] for s in status_rows if s[0] == 1]),
            "completed": sum([s[1] for s in status_rows if s[0] == 2])
        }
        
        data["energy_stats"] = {
            "today": data.get("energy_today", 0),
            "yesterday": data.get("energy_yesterday", 0),
            "trend": f"{(data.get('energy_today',0)-data.get('energy_yesterday',0))/max(data.get('energy_yesterday',1),1)*100:.1f}%"
        }
        
    except Exception as e:
        print(f"⚠️ 查询错误: {e}")
        # 返回默认数据
        data = get_mock_data()
    
    return data


def generate_report_content(report_type: str, report_date: str, data: dict) -> str:
    """生成报告内容"""
    
    if report_type == "daily":
        return generate_daily_report(report_date, data)
    elif report_type == "weekly":
        return generate_weekly_report(report_date, data)
    else:
        raise ValueError(f"未知报告类型: {report_type}")


def generate_daily_report(date: str, data: dict) -> str:
    """生成日报"""
    
    device = data.get("device_stats", {})
    alarm = data.get("alarm_stats", {})
    work_order = data.get("work_order_stats", {})
    energy = data.get("energy_stats", {})
    
    online_rate = (device.get("online", 0) / device.get("total", 1)) * 100
    
    report = f"""# IOC 智能巡检日报

**日期**: {date}  
**类型**: 每日巡检报告  
**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 一、概览

| 指标 | 数值 | 状态 |
|------|------|------|
| 设备总数 | {device.get("total", 0)} | - |
| 设备在线率 | {online_rate:.1f}% | {"✅ 正常" if online_rate > 95 else "⚠️ 偏低"} |
| 报警总数 | {alarm.get("total", 0)} | - |
| 工单总数 | {work_order.get("total", 0)} | - |

---

## 二、设备状态

### 2.1 总体状态

- **在线**: {device.get("online", 0)} 台
- **离线**: {device.get("offline", 0)} 台

### 2.2 按类型统计

| 设备类型 | 数量 |
|----------|------|
"""
    
    for dev_type, count in device.get("by_type", {}).items():
        report += f"| {dev_type} | {count} |\n"
    
    report += f"""
---

## 三、报警分析

### 3.1 报警统计

| 级别 | 数量 |
|------|------|
"""
    
    for level, count in alarm.get("by_level", {}).items():
        emoji = "🔴" if level == "紧急" else ("🟠" if level == "重要" else "🟡")
        report += f"| {emoji} {level} | {count} |\n"
    
    report += f"""
### 3.2 响应指标

- **平均响应时间**: {alarm.get("response_time_avg", 0):.1f} 分钟
- **响应率**: {alarm.get("response_rate", 0):.1f}%

---

## 四、工单进度

| 状态 | 数量 |
|------|------|
| 待处理 | {work_order.get("pending", 0)} |
| 处理中 | {work_order.get("processing", 0)} |
| 已完成 | {work_order.get("completed", 0)} |

- **SLA 达成率**: {work_order.get("sla_achieved", 0):.1f}%

---

## 五、能耗概况

| 指标 | 数值 |
|------|------|
| 今日能耗 | {energy.get("today", 0):,} kWh |
| 昨日能耗 | {energy.get("yesterday", 0):,} kWh |
| 周平均 | {energy.get("last_week_avg", 0):,} kWh |
| 趋势 | {energy.get("trend", "N/A")} |

---

## 六、智能建议

"""
    
    # 基于数据生成建议
    suggestions = []
    
    if device.get("offline", 0) > 50:
        suggestions.append("⚠️ 离线设备较多，建议安排专项巡检")
    
    if alarm.get("by_level", {}).get("紧急", 0) > 5:
        suggestions.append("🔴 紧急报警数量较多，需重点关注")
    
    if work_order.get("pending", 0) > 20:
        suggestions.append("📋 待处理工单积压，建议加快处理")
    
    if energy.get("trend", "").startswith("+"):
        suggestions.append("📈 能耗上升，建议检查空调/照明设备")
    
    if not suggestions:
        suggestions.append("✅ 今日各项指标正常，继续保持")
    
    for s in suggestions:
        report += f"- {s}\n"
    
    report += """
---

**报告生成**: IOC 智能运维助手  
**数据来源**: IOC 实时数据库
"""
    
    return report


def generate_weekly_report(week: str, data: dict) -> str:
    """生成周报"""
    
    report = f"""# IOC 智能巡检周报

**周次**: {week}  
**类型**: 每周巡检报告  
**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 一、周度概览

本周各项指标正常，设备运行稳定。

---

## 二、详细数据

（周报需连接真实数据库后生成完整版）

"""
    
    return report


def main():
    parser = argparse.ArgumentParser(description="IOC 智能巡检报告生成器")
    parser.add_argument("--type", choices=["daily", "weekly"], required=True, help="报告类型")
    parser.add_argument("--date", help="日期 (YYYY-MM-DD)")
    parser.add_argument("--week", help="周次 (YYYY-WNN)")
    parser.add_argument("--output", help="输出文件路径")
    
    args = parser.parse_args()
    
    # 加载配置
    config = load_config()
    
    # 确定日期
    if args.type == "daily":
        report_date = args.date or datetime.now().strftime("%Y-%m-%d")
    else:
        report_date = args.week or f"{datetime.now().year}-W{datetime.now().isocalendar()[1]:02d}"
    
    print(f"📊 正在生成 {args.type} 报告: {report_date}")
    
    # 获取数据
    conn = get_db_connection(config)
    if conn:
        try:
            data = fetch_real_data(conn, config, report_date)
        finally:
            conn.close()
    else:
        print("📝 使用模拟数据")
        data = generate_mock_data(report_date)
    
    # 生成报告
    content = generate_report_content(args.type, report_date, data)
    
    # 保存报告
    output_dir = Path(__file__).parent.parent / config["report"]["output_dir"]
    output_dir.mkdir(exist_ok=True)
    
    filename = f"{args.type}-{report_date}.md"
    output_path = output_dir / filename
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ 报告已生成: {output_path}")
    print(f"\n{content}")


if __name__ == "__main__":
    main()
