#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = []
# ///
"""
地理位置管理脚本

逻辑：用户配置 > 默认上海
提示：可通过 --set-location 设置城市
"""

import json
from pathlib import Path
from datetime import datetime

WALLPAPER_DIR = Path.home() / "wallpaper-daily"
LOCATION_CONFIG = WALLPAPER_DIR / "location.json"

DEFAULT_LOCATION = {
    "city": "上海",
    "region": "中国",
    "country": "China",
    "timezone": "Asia/Shanghai"
}


def get_location() -> dict:
    """获取位置：用户配置 > 默认上海"""
    if LOCATION_CONFIG.exists():
        try:
            with open(LOCATION_CONFIG) as f:
                config = json.load(f)
                if config.get("city"):
                    config["source"] = "user_config"
                    return config
        except Exception:
            pass
    
    location = DEFAULT_LOCATION.copy()
    location["source"] = "default"
    return location


def set_location(city: str, region: str = "", country: str = "") -> None:
    """保存用户配置的位置"""
    config = {
        "city": city,
        "region": region or city,
        "country": country or "China",
        "configured_at": datetime.now().isoformat()
    }
    WALLPAPER_DIR.mkdir(exist_ok=True)
    with open(LOCATION_CONFIG, 'w') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    print(f"✓ 已设置位置：{city}")


def get_weather_suggestion() -> str:
    """根据时间建议壁纸风格"""
    hour = datetime.now().hour
    return "bright" if 6 <= hour < 18 else "dark"


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="地理位置管理（用于壁纸推荐）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
提示：默认位置为上海，可通过 --set-location 设置

Examples:
  uv run scripts/loc.py
  uv run scripts/loc.py --set-location "北京"
  uv run scripts/loc.py --json
"""
    )
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--suggest", action="store_true", help="输出壁纸风格建议")
    parser.add_argument("--set-location", type=str, metavar="CITY", 
                        help="设置城市（如：北京、深圳）")
    args = parser.parse_args()
    
    if args.set_location:
        set_location(args.set_location)
        return 0
    
    location = get_location()
    
    if args.json:
        print(json.dumps(location, ensure_ascii=False, indent=2))
    elif args.suggest:
        print(get_weather_suggestion())
    else:
        source_hint = "（默认）" if location.get("source") == "default" else "（已配置）"
        print(f"📍 {location.get('city')}{source_hint}")
        if location.get("source") == "default":
            print(f"   提示：使用 --set-location 设置您的城市")
    
    return 0


if __name__ == "__main__":
    exit(main())
