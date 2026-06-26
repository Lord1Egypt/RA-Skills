#!/usr/bin/env python3
"""
🔥✍️ 每日热点文案自动生成器
从热榜获取话题 → 自动生成各平台文案 → 输出结果
配合定时任务使用，每天早上自动生成
"""

import json
import sys
import os
import subprocess
from datetime import datetime

# 技能目录
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.dirname(SKILL_DIR)

# 热榜技能路径
HOT_SKILLS = {
    "bilibili": os.path.join(WORKSPACE, "bilibili-hot-daily", "fetch_hot.py"),
    "weibo": os.path.join(WORKSPACE, "weibo-hot-daily", "fetch_hot.py"),
}

# 文案生成器路径
CONTENT_WRITER = os.path.join(WORKSPACE, "hot-content-writer", "generate.py")


def fetch_hot_topics(source="all", top=5):
    """从热榜获取话题"""
    topics = []
    
    sources = HOT_SKILLS if source == "all" else {source: HOT_SKILLS.get(source)}
    
    for name, script in sources.items():
        if not script or not os.path.exists(script):
            continue
        try:
            result = subprocess.run(
                [sys.executable, script, "--top", str(top), "--format", "json", "--output", f"C:\\tmp\\hot_{name}.json"],
                capture_output=True, text=True, timeout=30, encoding="utf-8", errors="replace"
            )
            json_file = f"C:\\tmp\\hot_{name}.json"
            if os.path.exists(json_file):
                with open(json_file, "r", encoding="utf-8", errors="replace") as f:
                    data = json.load(f)
                # 不同平台的数据结构不同
                items = data.get("videos", data.get("items", data.get("data", data.get("results", []))))
                if isinstance(items, list):
                    for item in items[:top]:
                        if isinstance(item, dict):
                            title = item.get("title", item.get("name", item.get("word", "")))
                        elif isinstance(item, str):
                            title = item
                        else:
                            continue
                        # 清理乱码
                        title = title.encode("utf-8", errors="replace").decode("utf-8", errors="replace")
                        if title and len(title) > 2 and title not in [t["title"] for t in topics]:
                            topics.append({"source": name, "title": title})
        except Exception as e:
            print(f"[WARN] 获取{name}热榜失败: {e}", file=sys.stderr)
    
    return topics


def generate_content(topic, platform="xiaohongshu", style="casual"):
    """生成文案"""
    if not os.path.exists(CONTENT_WRITER):
        return {"error": "文案生成器不存在"}
    
    # 先尝试API模式
    try:
        result = subprocess.run(
            [sys.executable, CONTENT_WRITER, "--topic", topic, "--platform", platform, "--style", style, "--api"],
            capture_output=True, text=True, timeout=60, encoding="utf-8", errors="replace"
        )
        if result.returncode == 0:
            output = result.stdout.strip()
            if output and output.startswith("{"):
                parsed = json.loads(output)
                if "error" not in parsed:
                    return parsed
    except Exception:
        pass
    
    # 回退到模板模式
    try:
        result = subprocess.run(
            [sys.executable, CONTENT_WRITER, "--topic", topic, "--platform", platform, "--style", style],
            capture_output=True, text=True, timeout=30, encoding="utf-8", errors="replace"
        )
        if result.returncode == 0:
            output = result.stdout.strip()
            if output and output.startswith("{"):
                return json.loads(output)
        return {"error": "模板生成失败", "stderr": result.stderr[:200]}
    except Exception as e:
        return {"error": str(e)}


def format_for_wechat(results):
    """格式化为企微推送格式"""
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [f"🔥✍️ 每日热点文案 {today}\n"]
    
    for i, item in enumerate(results, 1):
        topic = item["topic"]
        source = item.get("source", "未知")
        content = item.get("content", {})
        
        lines.append(f"━━━ {i}. {topic} ━━━")
        lines.append(f"📌 来源：{source}")
        
        if "error" in content:
            lines.append(f"❌ 生成失败：{content['error']}")
        else:
            titles = content.get("titles", [])
            if titles:
                lines.append(f"💡 推荐标题：{titles[0]}")
            
            body = content.get("content", "")
            if body:
                # 截取前150字
                preview = body[:150] + "..." if len(body) > 150 else body
                lines.append(f"📝 文案预览：\n{preview}")
            
            hashtags = content.get("hashtags", [])
            if hashtags:
                lines.append(f"🏷️ 标签：{' '.join(hashtags[:5])}")
        
        lines.append("")
    
    lines.append("━━━━━━━━━━━━━")
    lines.append("💡 完整文案请使用 hot-content-writer 技能生成")
    lines.append("📦 安装：npx clawhub install hot-content-writer")
    
    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="每日热点文案自动生成")
    parser.add_argument("--source", default="all", choices=["all", "bilibili", "weibo"])
    parser.add_argument("--top", type=int, default=3, help="取前N个热点")
    parser.add_argument("--platform", default="xiaohongshu", help="目标平台")
    parser.add_argument("--style", default="casual", help="文案风格")
    parser.add_argument("--output", help="输出文件路径")
    parser.add_argument("--wechat-format", action="store_true", help="输出企微推送格式")
    
    args = parser.parse_args()
    
    print(f"🔍 正在获取热榜话题...", file=sys.stderr)
    topics = fetch_hot_topics(args.source, args.top)
    
    if not topics:
        print("❌ 未获取到热榜话题", file=sys.stderr)
        sys.exit(1)
    
    print(f"✅ 获取到 {len(topics)} 个话题", file=sys.stderr)
    
    results = []
    for t in topics:
        print(f"✍️ 正在生成：{t['title'][:20]}...", file=sys.stderr)
        content = generate_content(t["title"], args.platform, args.style)
        results.append({
            "topic": t["title"],
            "source": t["source"],
            "content": content
        })
    
    if args.wechat_format:
        output = format_for_wechat(results)
    else:
        output = json.dumps({
            "generated_at": datetime.now().isoformat(),
            "results": results
        }, ensure_ascii=False, indent=2)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"✅ 已保存到 {args.output}", file=sys.stderr)
    else:
        sys.stdout.buffer.write(output.encode("utf-8"))
        sys.stdout.buffer.write(b"\n")


if __name__ == "__main__":
    main()
