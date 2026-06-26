#!/usr/bin/env python3
"""
渔获记录脚本 - 记录路亚钓鱼成果

用法:
  python log_catch.py --species 翘嘴 --length 45 --weight 1.2 --lure "米诺 7cm" --location 千岛湖
  python log_catch.py --interactive  # 交互式录入
"""

import json
import argparse
from datetime import datetime
from pathlib import Path
import subprocess

DATA_DIR = Path.home() / "lurefish"
CATCHES_FILE = DATA_DIR / "catches.json"


def ensure_data_dir():
    """确保数据目录存在"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not CATCHES_FILE.exists():
        CATCHES_FILE.write_text("[]", encoding="utf-8")


def load_catches():
    """加载所有渔获记录"""
    ensure_data_dir()
    return json.loads(CATCHES_FILE.read_text(encoding="utf-8"))


def save_catches(catches):
    """保存渔获记录"""
    CATCHES_FILE.write_text(json.dumps(catches, ensure_ascii=False, indent=2), encoding="utf-8")


def get_weather():
    """尝试获取当前天气"""
    try:
        result = subprocess.run(
            ["curl", "-s", "wttr.in/?format=%t+%w+%p"],
            capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip() if result.stdout.strip() else "未知"
    except:
        return "未知"


def log_catch(species, length=None, weight=None, lure=None, location=None,
              technique=None, weather=None, notes=None, date=None):
    """记录一条渔获"""
    catches = load_catches()

    catch = {
        "id": len(catches) + 1,
        "date": date or datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M"),
        "species": species,
        "length": length,
        "weight": weight,
        "lure": lure,
        "location": location,
        "technique": technique,
        "weather": weather or get_weather(),
        "notes": notes
    }

    catches.append(catch)
    save_catches(catches)

    print(f"✅ 已记录 #{catch['id']}: {species}")
    if length:
        print(f"   长度: {length}cm")
    if weight:
        print(f"   重量: {weight}kg")
    if lure:
        print(f"   用饵: {lure}")
    if location:
        print(f"   钓点: {location}")

    return catch


def interactive_input():
    """交互式录入"""
    print("🎣 渔获记录 (直接回车跳过)\n")

    species = input("鱼种: ").strip() or None
    if not species:
        print("❌ 鱼种必填")
        return

    length = input("长度(cm): ").strip()
    length = float(length) if length else None

    weight = input("重量(kg): ").strip()
    weight = float(weight) if weight else None

    lure = input("用饵: ").strip() or None
    location = input("钓点: ").strip() or None
    technique = input("手法: ").strip() or None
    notes = input("备注: ").strip() or None

    log_catch(species, length, weight, lure, location, technique, notes=notes)


def main():
    parser = argparse.ArgumentParser(description="渔获记录")
    parser.add_argument("--species", help="鱼种")
    parser.add_argument("--length", type=float, help="长度(cm)")
    parser.add_argument("--weight", type=float, help="重量(kg)")
    parser.add_argument("--lure", help="用饵")
    parser.add_argument("--location", help="钓点")
    parser.add_argument("--technique", help="手法")
    parser.add_argument("--weather", help="天气")
    parser.add_argument("--notes", help="备注")
    parser.add_argument("--date", help="日期 (YYYY-MM-DD)")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互式录入")
    parser.add_argument("--list", "-l", action="store_true", help="查看最近记录")

    args = parser.parse_args()

    if args.list:
        catches = load_catches()
        print(f"📝 共 {len(catches)} 条记录\n")
        for c in catches[-10:]:
            print(f"#{c['id']} {c['date']} {c['species']} {c.get('length', '')}cm {c.get('location', '')}")
        return

    if args.interactive:
        interactive_input()
        return

    if args.species:
        log_catch(
            species=args.species,
            length=args.length,
            weight=args.weight,
            lure=args.lure,
            location=args.location,
            technique=args.technique,
            weather=args.weather,
            notes=args.notes,
            date=args.date
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
