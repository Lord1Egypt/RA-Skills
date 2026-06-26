#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = [
#     "polars>=1.0.0",
#     "duckdb>=1.0.0",
#     "pyobjc-framework-Cocoa>=10.0",
# ]
# ///
"""
智能壁纸推荐脚本
使用 polars + duckdb 分析用户偏好，推荐"猜你喜欢"的壁纸
"""

import polars as pl
import duckdb
import urllib.request
from pathlib import Path
from datetime import datetime
import random

PREFERENCES_FILE = Path.home() / "wallpaper-daily" / "preferences.parquet"
WALLPAPER_DIR = Path.home() / "wallpaper-daily"

# 壁纸源配置
WALLPAPER_SOURCES = {
    "nature": ["https://picsum.photos/3840/2160?random={seed}&nature"],
    "mountain": ["https://picsum.photos/3840/2160?random={seed}&mountain"],
    "forest": ["https://picsum.photos/3840/2160?random={seed}&forest"],
    "ocean": ["https://picsum.photos/3840/2160?random={seed}&ocean"],
    "city": ["https://picsum.photos/3840/2160?random={seed}&city"],
    "space": ["https://picsum.photos/3840/2160?random={seed}&space"],
}


def load_preferences() -> pl.DataFrame | None:
    """加载偏好数据"""
    if not PREFERENCES_FILE.exists():
        print("❌ 偏好数据不足，无法推荐")
        print("提示：先使用换壁纸功能并评分至少 5 次")
        return None
    
    try:
        df = pl.read_parquet(PREFERENCES_FILE)
        if len(df) < 5:
            print(f"❌ 数据量不足（当前：{len(df)}条，需要：≥5 条）")
            return None
        return df
    except Exception as e:
        print(f"❌ 读取数据失败：{e}")
        return None


def recommend_with_duckdb(df: pl.DataFrame, user_tags: list[str] = None) -> list[dict]:
    """使用 duckdb 进行智能推荐"""
    con = duckdb.connect()
    con.register('preferences', df)
    
    # 综合推荐算法
    query = """
        WITH category_stats AS (
            SELECT 
                category,
                AVG(rating) as avg_rating,
                MAX(rating) as max_rating,
                COUNT(*) as rated_count,
                SUM(CASE WHEN rating >= 7 THEN 1 ELSE 0 END) as liked_count
            FROM preferences
            GROUP BY category
        ),
        tone_stats AS (
            SELECT 
                color_tone,
                AVG(rating) as avg_rating
            FROM preferences
            WHERE color_tone != 'unknown'
            GROUP BY color_tone
        ),
        recent_trend AS (
            SELECT 
                category,
                AVG(rating) as recent_avg
            FROM preferences
            WHERE date >= EXTRACT(EPOCH FROM NOW()) - 86400 * 7
            GROUP BY category
        )
        SELECT 
            cs.category,
            cs.avg_rating as base_score,
            cs.max_rating,
            cs.liked_count * 1.0 / cs.rated_count as like_ratio,
            COALESCE(rt.recent_avg, cs.avg_rating) as recent_score,
            ts.avg_rating as tone_bonus
        FROM category_stats cs
        LEFT JOIN recent_trend rt ON cs.category = rt.category
        LEFT JOIN tone_stats ts ON ts.color_tone = (
            SELECT color_tone FROM preferences 
            WHERE category = cs.category AND rating >= 7
            ORDER BY rating DESC LIMIT 1
        )
        ORDER BY 
            (cs.avg_rating * 0.4 + 
             COALESCE(rt.recent_avg, cs.avg_rating) * 0.4 + 
             COALESCE(ts.avg_rating, 5) * 0.2) DESC
        LIMIT 3
    """
    
    result = con.execute(query).fetchall()
    con.close()
    
    if not result:
        return []
    
    recommendations = []
    for row in result:
        category, base_score, max_rating, like_ratio, recent_score, tone_bonus = row
        # 综合得分
        final_score = base_score * 0.4 + recent_score * 0.4 + (tone_bonus or 5) * 0.2
        recommendations.append({
            'category': category,
            'score': final_score,
            'base_score': base_score,
            'recent_score': recent_score,
            'like_ratio': like_ratio,
        })
    
    return recommendations


def download_recommended_wallpaper(category: str) -> Path | None:
    """下载推荐的壁纸"""
    seed = random.randint(1, 10000)
    
    if category in WALLPAPER_SOURCES:
        url_template = random.choice(WALLPAPER_SOURCES[category])
    else:
        url_template = "https://picsum.photos/3840/2160?random={seed}"
    
    url = url_template.format(seed=seed)
    
    today = datetime.now().strftime("%Y-%m-%d")
    today_dir = WALLPAPER_DIR / today
    today_dir.mkdir(exist_ok=True)
    
    filename = f"recommended-{category}-{datetime.now().strftime('%H%M%S')}.jpg"
    filepath = today_dir / filename
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            with open(filepath, 'wb') as f:
                f.write(response.read())
        
        if filepath.stat().st_size > 100 * 1024:
            print(f"✓ 下载成功：{filename}")
            return filepath
        else:
            filepath.unlink()
            return None
    except Exception as e:
        print(f"❌ 下载失败：{e}")
        return None


def set_wallpaper(image_path: Path) -> bool:
    """
    设置壁纸（macOS Tahoe 兼容）
    使用 PyObjC + killall WallpaperAgent
    """
    import subprocess
    
    abs_path = str(image_path.absolute())
    
    # 方法 1: PyObjC + NSWorkspace
    try:
        from AppKit import NSWorkspace, NSScreen
        from Foundation import NSURL
        
        url = NSURL.fileURLWithPath_(abs_path)
        workspace = NSWorkspace.sharedWorkspace()
        
        success = False
        for screen in NSScreen.screens():
            result, _ = workspace.setDesktopImageURL_forScreen_options_error_(
                url, screen, {}, None
            )
            if result:
                success = True
        
        if success:
            # macOS Tahoe: 重启 WallpaperAgent 让壁纸生效
            import time
            time.sleep(0.3)
            subprocess.run(['killall', 'WallpaperAgent'], capture_output=True, timeout=10)
            return True
            
    except ImportError:
        pass
    except Exception:
        pass
    
    # 方法 2: desktoppr 回退
    try:
        result = subprocess.run(['desktoppr', abs_path], capture_output=True, timeout=30)
        if result.returncode == 0:
            subprocess.run(['killall', 'WallpaperAgent'], capture_output=True, timeout=10)
            return True
    except FileNotFoundError:
        pass
    
    return False


def show_recommendations(recommendations: list[dict], df: pl.DataFrame) -> None:
    """显示推荐结果"""
    print("\n" + "=" * 60)
    print("🎯 猜你喜欢 - 智能推荐")
    print("=" * 60)
    
    # 用户偏好总结
    print("\n📊 你的偏好分析:")
    avg_rating = df['rating'].mean()
    top_category = df.group_by('category').agg(
        pl.col('rating').mean().alias('avg')
    ).sort('avg', descending=True).row(0)[0]
    
    print(f"  平均评分：{avg_rating:.1f}/10")
    print(f"  最爱分类：{top_category}")
    print(f"  评分次数：{len(df)}次")
    
    # 推荐列表
    print("\n🏆 推荐分类:")
    for i, rec in enumerate(recommendations, 1):
        stars = "⭐" * int(rec['score'] / 2)
        print(f"\n  {i}. {rec['category'].upper()}")
        print(f"     推荐指数：{stars} ({rec['score']:.2f}分)")
        print(f"     历史平均：{rec['base_score']:.1f}分")
        print(f"     近期趋势：{rec['recent_score']:.1f}分")
        print(f"     喜好比例：{rec['like_ratio']*100:.0f}%")
    
    # 标签建议
    print("\n🔖 热门标签:")
    all_tags = []
    for tags in df.filter(pl.col('rating') >= 7)['tags']:
        all_tags.extend([t.lower() for t in tags])
    
    if all_tags:
        from collections import Counter
        tag_counts = Counter(all_tags).most_common(5)
        for tag, count in tag_counts:
            print(f"    #{tag} ({count}次)")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="基于评分数据智能推荐壁纸",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run scripts/recommend.py
  uv run scripts/recommend.py -n   # 仅显示
  uv run scripts/recommend.py -y   # 自动应用
"""
    )
    parser.add_argument("--tags", type=str, help="偏好标签（逗号分隔）")
    parser.add_argument("-y", "--yes", action="store_true", help="自动应用，不询问")
    parser.add_argument("-n", "--no-apply", action="store_true", help="仅显示，不下载")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args()
    
    # 加载数据
    df = load_preferences()
    if df is None:
        return 1
    
    # 计算推荐
    recommendations = recommend_with_duckdb(df, args.tags.split(",") if args.tags else None)
    
    if not recommendations:
        print("❌ 无法生成推荐，数据不足")
        return 1
    
    # JSON 输出模式
    if args.json:
        import json
        output = {
            "recommendations": recommendations,
            "total_ratings": len(df),
            "avg_rating": float(df['rating'].mean())
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0
    
    print("🦞 Mac 壁纸智能推荐系统")
    print(f"数据文件：{PREFERENCES_FILE}")
    
    # 显示推荐
    show_recommendations(recommendations, df)
    
    # 应用推荐
    if not args.no_apply:
        top_rec = recommendations[0]
        print(f"\n🎨 正在下载推荐壁纸：{top_rec['category']}...")
        
        filepath = download_recommended_wallpaper(top_rec['category'])
        if filepath:
            if args.yes or input("\n是否设置为壁纸？(y/n): ").lower() == 'y':
                if set_wallpaper(filepath):
                    print("✓ 壁纸已更新")
                    return 0
                else:
                    print("❌ 设置壁纸失败")
            else:
                print("✓ 壁纸已下载，未设置")
        else:
            print("❌ 下载失败")
    
    return 0


if __name__ == "__main__":
    exit(main())
