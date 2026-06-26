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
偏好管理脚本
评分 CRUD + 统计报告，统一管理 preferences.parquet
"""

import polars as pl
import duckdb
from pathlib import Path
from datetime import datetime, timedelta

PREFERENCES_FILE = Path.home() / "wallpaper-daily" / "preferences.parquet"

# 与 change.py 保持一致
CATEGORIES = ["nature", "mountain", "forest", "ocean", "city", "space"]
COLOR_TONES = ["dark", "bright", "warm", "cool"]
MOODS = [
    "平静", "愉悦", "振奋", "专注", "放松",
    "孤独", "忧郁", "温暖", "自由", "神秘",
]


def load_preferences() -> pl.DataFrame | None:
    """加载偏好数据"""
    if not PREFERENCES_FILE.exists():
        return None
    try:
        return pl.read_parquet(PREFERENCES_FILE)
    except Exception:
        return None


def save_preferences(df: pl.DataFrame) -> bool:
    """保存偏好数据"""
    try:
        PREFERENCES_FILE.parent.mkdir(parents=True, exist_ok=True)
        df.write_parquet(PREFERENCES_FILE)
        return True
    except Exception as e:
        print(f"❌ 保存失败：{e}")
        return False


def get_current_wallpaper_path() -> Path | None:
    """获取当前桌面壁纸路径（macOS）"""
    try:
        from AppKit import NSWorkspace, NSScreen
        workspace = NSWorkspace.sharedWorkspace()
        for screen in NSScreen.screens():
            url = workspace.desktopImageURLForScreen_(screen)
            if url and url.isFileURL():
                path = Path(url.path())
                if path.exists():
                    return path
        return None
    except Exception:
        return None


def ask_rating_interactive() -> tuple[int, list[str], str, str, str] | None:
    """交互式询问评分"""
    try:
        print("\n=== 壁纸评分 ===")
        print("请为这张壁纸评分 (1-10, 10 为最喜欢):")
        rating_input = input("评分：").strip()
        if not rating_input.isdigit():
            return None
        rating = int(rating_input)
        if rating < 1 or rating > 10:
            print("评分必须在 1-10 之间")
            return None

        print("\n可选标签（逗号分隔，回车跳过）:")
        print("建议：森林、山脉、海洋、暗色调、明亮、宁静...")
        tags_input = input("标签：").strip()
        tags = [t.strip() for t in tags_input.split(",") if t.strip()] if tags_input else []

        print("\n色调 (1-4):", ", ".join(f"{i}.{t}" for i, t in enumerate(COLOR_TONES, 1)))
        tone_input = input("选择：").strip()
        color_tone = COLOR_TONES[int(tone_input) - 1] if tone_input.isdigit() and 1 <= int(tone_input) <= 4 else "unknown"

        print("\n分类 (1-6):", ", ".join(f"{i}.{c}" for i, c in enumerate(CATEGORIES, 1)))
        cat_input = input("选择：").strip()
        category = CATEGORIES[int(cat_input) - 1] if cat_input.isdigit() and 1 <= int(cat_input) <= len(CATEGORIES) else "nature"

        print("\n心情 (1-10):", ", ".join(f"{i}.{m}" for i, m in enumerate(MOODS, 1)))
        mood_input = input("选择：").strip()
        mood = MOODS[int(mood_input) - 1] if mood_input.isdigit() and 1 <= int(mood_input) <= 10 else "平静"

        return rating, tags, color_tone, category, mood
    except (KeyboardInterrupt, EOFError):
        print("\n已取消")
        return None


def cmd_add(filepath: Path, source_url: str = "") -> int:
    """新增评分"""
    if not filepath.exists():
        print(f"❌ 文件不存在：{filepath}")
        return 1

    result = ask_rating_interactive()
    if not result:
        return 1

    rating, tags, color_tone, category, mood = result
    abs_path = str(filepath.absolute())

    new_record = pl.DataFrame({
        "date": [datetime.now()],
        "wallpaper_path": [abs_path],
        "rating": [rating],
        "tags": [tags],
        "color_tone": [color_tone],
        "category": [category],
        "mood": [mood],
        "source_url": [source_url or ""],
    })

    df = load_preferences()
    if df is not None:
        df = pl.concat([df, new_record])
    else:
        df = new_record

    if save_preferences(df):
        print(f"✓ 已保存评分：{rating}/10，分类：{category}")
        return 0
    return 1


def cmd_list(limit: int = 20, json_out: bool = False) -> int:
    """列出评分记录"""
    df = load_preferences()
    if df is None or len(df) == 0:
        print("❌ 暂无评分数据")
        return 1

    total_count = len(df)
    df = df.sort("date", descending=True).head(limit)

    if json_out:
        import json
        rows = df.to_dicts()
        for r in rows:
            if isinstance(r.get("date"), datetime):
                r["date"] = r["date"].isoformat()
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return 0

    print("\n" + "=" * 70)
    print("📋 评分记录")
    print("=" * 70)
    print(f"共 {total_count} 条，显示最近 {limit} 条\n")

    for i, row in enumerate(df.iter_rows(named=True), 1):
        fname = Path(row["wallpaper_path"]).name
        d = row["date"]
        date_str = d.strftime("%Y-%m-%d %H:%M") if hasattr(d, "strftime") else datetime.fromtimestamp(d).strftime("%Y-%m-%d %H:%M") if isinstance(d, (int, float)) else str(d)
        tags_str = ", ".join(row["tags"][:3]) if row["tags"] else "-"
        print(f"  {i:3d}. [{date_str}] {row['rating']}/10 | {row['category']:8s} | {row['color_tone']:6s} | {fname[:30]}")
        if tags_str != "-":
            print(f"       标签: {tags_str}")

    return 0


def cmd_set(index: int, rating: int | None = None, category: str | None = None) -> int:
    """修改指定索引的评分"""
    df = load_preferences()
    if df is None or len(df) == 0:
        print("❌ 暂无评分数据")
        return 1

    df_sorted = df.sort("date", descending=True)
    if index < 1 or index > len(df_sorted):
        print(f"❌ 索引超出范围 (1-{len(df_sorted)})")
        return 1

    row_info = df_sorted.row(index=index - 1, named=True)
    mask = (pl.col("date") == row_info["date"]) & (pl.col("wallpaper_path") == row_info["wallpaper_path"])

    if rating is not None:
        if rating < 1 or rating > 10:
            print("❌ 评分必须在 1-10 之间")
            return 1
        df = df.with_columns(pl.when(mask).then(pl.lit(rating)).otherwise(pl.col("rating")).alias("rating"))
    if category is not None and category in CATEGORIES:
        df = df.with_columns(pl.when(mask).then(pl.lit(category)).otherwise(pl.col("category")).alias("category"))

    if save_preferences(df):
        print(f"✓ 已更新第 {index} 条记录")
        return 0
    return 1


def cmd_del(index: int) -> int:
    """删除评分"""
    df = load_preferences()
    if df is None or len(df) == 0:
        print("❌ 暂无评分数据")
        return 1

    df_sorted = df.sort("date", descending=True)
    if index < 1 or index > len(df_sorted):
        print(f"❌ 索引超出范围 (1-{len(df_sorted)})")
        return 1
    to_drop = df_sorted.row(index=index - 1, named=True)
    mask = (pl.col("date") == to_drop["date"]) & (pl.col("wallpaper_path") == to_drop["wallpaper_path"])
    df = df.filter(~mask)

    if save_preferences(df):
        print("✓ 已删除")
        return 0
    return 1


def _analyze_with_polars(df: pl.DataFrame) -> None:
    """Polars 统计分析"""
    print("\n" + "=" * 60)
    print("📊 Polars 统计分析")
    print("=" * 60)

    print(f"\n📈 数据概览:")
    print(f"  总评分数：{len(df)}")
    print(f"  数据时间范围：{df['date'].min()} ~ {df['date'].max()}")
    print(f"  平均评分：{df['rating'].mean():.2f}/10")

    print(f"\n⭐ 评分分布:")
    rating_dist = df.group_by('rating').agg(pl.col('rating').count().alias('count')).sort('rating')
    for row in rating_dist.iter_rows():
        bar = "█" * row[1]
        print(f"  {row[0]}分：{bar} ({row[1]}次)")

    print(f"\n🏷️ 分类偏好:")
    category_stats = df.group_by('category').agg(
        pl.col('rating').mean().alias('avg_rating'),
        pl.col('rating').count().alias('count')
    ).sort('avg_rating', descending=True)
    for row in category_stats.iter_rows():
        stars = "⭐" * int(row[1] / 2)
        print(f"  {row[0]:10s}: {stars} ({row[1]:.1f}分，{row[2]}次)")

    print(f"\n🎨 色调偏好:")
    tone_stats = df.group_by('color_tone').agg(
        pl.col('rating').mean().alias('avg_rating'),
        pl.col('rating').count().alias('count')
    ).sort('avg_rating', descending=True)
    for row in tone_stats.iter_rows():
        if row[0] != "unknown":
            print(f"  {row[0]:10s}: {row[1]:.1f}分 ({row[2]}次)")

    if 'mood' in df.columns:
        print(f"\n😊 情绪分布:")
        mood_stats = df.group_by('mood').agg(
            pl.col('rating').mean().alias('avg_rating'),
            pl.col('rating').count().alias('count')
        ).sort('count', descending=True)
        for row in mood_stats.iter_rows():
            bar = "█" * min(row[2], 20)
            print(f"  {row[0]:6s}: {bar} ({row[1]:.1f}分，{row[2]}次)")

    print(f"\n🔖 热门标签:")
    all_tags = []
    for tags in df['tags'].to_list():
        if tags is not None:
            all_tags.extend(tags)
    if all_tags:
        tag_counts = pl.DataFrame({'tag': all_tags}).group_by('tag').agg(
            pl.col('tag').count().alias('count')
        ).sort('count', descending=True).head(10)
        for i, row in enumerate(tag_counts.iter_rows(), 1):
            print(f"  {i:2d}. #{row[0]} ({row[1]}次)")

    print(f"\n📅 近期趋势 (最近 7 天):")
    cutoff = datetime.now() - timedelta(days=7)
    recent = df.filter(pl.col('date') >= cutoff)
    if len(recent) > 0:
        recent_avg = recent['rating'].mean()
        overall_avg = df['rating'].mean()
        trend = "↑" if recent_avg > overall_avg else "↓" if recent_avg < overall_avg else "→"
        print(f"  近期平均：{recent_avg:.2f}分 {trend} (总体：{overall_avg:.2f}分)")
    else:
        print("  最近 7 天无评分")


def _analyze_with_duckdb(df: pl.DataFrame) -> None:
    """DuckDB 深度分析"""
    print("\n" + "=" * 60)
    print("🦆 DuckDB 深度分析")
    print("=" * 60)

    con = duckdb.connect()
    con.register('preferences', df)

    print("\n🏆 评分最高的壁纸:")
    result = con.execute("""
        SELECT wallpaper_path, rating, category, color_tone, array_to_string(tags, ', ') as tags
        FROM preferences WHERE rating >= 8 ORDER BY rating DESC, date DESC LIMIT 5
    """).fetchdf()
    for i, row in result.iterrows():
        print(f"  {i+1}. {row['wallpaper_path'].split('/')[-1]}")
        print(f"     评分：{row['rating']} | 分类：{row['category']} | 色调：{row['color_tone']}")

    print("\n🔍 分类 + 色调组合分析:")
    result = con.execute("""
        SELECT category, color_tone, ROUND(AVG(rating), 2) as avg_rating, COUNT(*) as count
        FROM preferences WHERE color_tone != 'unknown'
        GROUP BY category, color_tone HAVING COUNT(*) >= 2
        ORDER BY avg_rating DESC LIMIT 8
    """).fetchdf()
    for i, row in result.iterrows():
        print(f"  {row['category']:10s} + {row['color_tone']:6s}: {row['avg_rating']}分 ({row['count']}次)")

    print("\n⚖️ 推荐权重计算:")
    result = con.execute("""
        SELECT category, AVG(rating) as base_score, COUNT(*) as confidence,
               AVG(rating) * (1 + 0.1 * LN(COUNT(*) + 1)) as weighted_score
        FROM preferences GROUP BY category ORDER BY weighted_score DESC
    """).fetchdf()
    for i, row in result.iterrows():
        print(f"  {row['category']:10s}: 基础分 {row['base_score']:.2f} × 置信度 = {row['weighted_score']:.2f}")

    con.close()


def cmd_stats(json_out: bool = False) -> int:
    """完整统计报告"""
    df = load_preferences()
    if df is None or len(df) == 0:
        print("❌ 暂无评分数据")
        print("提示：先使用换壁纸功能并评分，积累数据后再分析")
        return 1

    if json_out:
        import json
        stats = {
            "total_ratings": len(df),
            "avg_rating": float(df['rating'].mean()),
            "top_category": df.group_by('category').agg(
                pl.col('rating').mean().alias('avg')
            ).sort('avg', descending=True).row(0)[0]
        }
        print(json.dumps(stats, ensure_ascii=False, indent=2))
        return 0

    print("🦞 Mac 壁纸偏好分析报告")
    print(f"数据文件：{PREFERENCES_FILE}")
    print(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    _analyze_with_polars(df)
    _analyze_with_duckdb(df)

    print("\n" + "=" * 60)
    print("💡 智能建议")
    print("=" * 60)
    avg_rating = df['rating'].mean()
    top_category = df.group_by('category').agg(
        pl.col('rating').mean().alias('avg')
    ).sort('avg', descending=True).row(0)[0]
    print(f"\n  ✓ 你的平均评分：{avg_rating:.1f}/10")
    print(f"  ✓ 最喜爱的分类：{top_category}")
    print(f"  ✓ 建议：多尝试 {top_category} 类壁纸")
    if avg_rating < 6:
        print(f"  ⚠ 提示：近期壁纸满意度较低，建议调整推荐策略")

    return 0


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="偏好管理：评分 CRUD + 统计报告",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run scripts/preference.py           # 列出评分（默认）
  uv run scripts/preference.py add       # 对当前壁纸评分
  uv run scripts/preference.py add path   # 对指定文件评分
  uv run scripts/preference.py ls -n 10   # 最近 10 条
  uv run scripts/preference.py set 3 9    # 第 3 条改为 9 分
  uv run scripts/preference.py del 5     # 删除第 5 条
  uv run scripts/preference.py stats     # 完整统计报告
"""
    )
    sub = parser.add_subparsers(dest="cmd")

    p_add = sub.add_parser("add", help="新增评分")
    p_add.add_argument("path", nargs="?", type=str, help="壁纸路径（省略=当前桌面）")
    p_add.add_argument("--source-url", type=str, default="", help="来源 URL")

    p_list = sub.add_parser("list", help="列出评分")
    p_list.add_argument("--limit", "-n", type=int, default=20, help="条数")
    p_list.add_argument("--json", action="store_true", help="JSON 输出")
    p_ls = sub.add_parser("ls", help="同 list")
    p_ls.add_argument("--limit", "-n", type=int, default=20, help="条数")
    p_ls.add_argument("--json", action="store_true", help="JSON 输出")

    p_set = sub.add_parser("set", help="修改评分")
    p_set.add_argument("index", type=int, help="记录序号")
    p_set.add_argument("rating", type=int, nargs="?", help="新评分 1-10")
    p_set.add_argument("--category", "-c", type=str, choices=CATEGORIES, help="新分类")

    p_del = sub.add_parser("del", help="删除评分")
    p_del.add_argument("index", type=int, help="记录序号")

    p_stats = sub.add_parser("stats", help="完整统计报告")
    p_stats.add_argument("--json", action="store_true", help="JSON 输出")

    args = parser.parse_args()

    if args.cmd is None:
        return cmd_list(20, False)

    if args.cmd == "add":
        if getattr(args, "path", None):
            return cmd_add(Path(args.path).expanduser(), getattr(args, "source_url", "") or "")
        path = get_current_wallpaper_path()
        if path is None:
            print("❌ 无法获取当前桌面壁纸，请指定路径：preference add <path>")
            return 1
        return cmd_add(path, getattr(args, "source_url", "") or "")

    if args.cmd in ("list", "ls"):
        return cmd_list(args.limit, args.json)

    if args.cmd == "set":
        if args.rating is None and getattr(args, "category", None) is None:
            print("❌ 请指定 rating 或 --category")
            return 1
        return cmd_set(args.index, args.rating, getattr(args, "category", None))

    if args.cmd == "del":
        return cmd_del(args.index)

    if args.cmd == "stats":
        return cmd_stats(getattr(args, "json", False))

    return 0


if __name__ == "__main__":
    exit(main())
