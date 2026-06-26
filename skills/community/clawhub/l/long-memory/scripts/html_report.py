#!/usr/bin/env python3
"""HTML 可视化报告：生成漂亮的记忆分析报告"""

import argparse
import json
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from lib.filelock import safe_read

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"


def generate_html_report(memory_dir: Path, output: Path) -> str:
    """生成完整的 HTML 可视化报告"""
    conv_dir = memory_dir / "conversations"
    
    # 收集数据
    files_data = []
    total_size = 0
    total_sessions = 0
    all_tags = {}
    all_topics = {}
    tag_timeline = []
    topic_timeline = []

    if conv_dir.exists():
        for fp in sorted(conv_dir.glob("*.md")):
            content = fp.read_text(encoding="utf-8")
            size = fp.stat().st_size
            sessions = content.count("## [")
            total_size += size
            total_sessions += sessions

            import re
            tags = list(set(t.strip() for tl in re.findall(r'\*\*标签[：:]\*\*\s*(.+)', content)
                          for t in tl.split("，") if t.strip()))
            topics = [t.strip() for t in re.findall(r'###\s*话题[：:]\s*(.+)', content)]

            for tag in tags:
                all_tags[tag] = all_tags.get(tag, 0) + 1
                tag_timeline.append({"date": fp.stem, "tag": tag, "count": 1})

            for topic in topics:
                all_topics[topic] = all_topics.get(topic, 0) + 1
                topic_timeline.append({"date": fp.stem, "topic": topic})

            files_data.append({
                "date": fp.stem,
                "size": size,
                "sessions": sessions,
                "tags": tags,
                "topics": topics,
            })

    # 生成 HTML
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Long Memory 记忆分析报告</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
         background: #0f0f23; color: #e0e0e0; padding: 2rem; }}
  .container {{ max-width: 1200px; margin: 0 auto; }}
  h1 {{ color: #ff6b6b; margin-bottom: 0.5rem; font-size: 2rem; }}
  .subtitle {{ color: #888; margin-bottom: 2rem; }}
  .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem; }}
  .stat-card {{ background: #1a1a2e; border-radius: 12px; padding: 1.5rem; 
               border: 1px solid #2a2a4a; }}
  .stat-value {{ font-size: 2rem; font-weight: bold; color: #4ecdc4; }}
  .stat-label {{ color: #888; margin-top: 0.5rem; }}
  .section {{ background: #1a1a2e; border-radius: 12px; padding: 1.5rem; 
             margin-bottom: 1rem; border: 1px solid #2a2a4a; }}
  .section h2 {{ color: #ff6b6b; margin-bottom: 1rem; font-size: 1.2rem; }}
  .bar-chart {{ display: flex; flex-direction: column; gap: 0.5rem; }}
  .bar-row {{ display: flex; align-items: center; gap: 0.5rem; }}
  .bar-label {{ width: 120px; text-align: right; font-size: 0.85rem; color: #aaa; overflow: hidden;
               text-overflow: ellipsis; white-space: nowrap; }}
  .bar-track {{ flex: 1; height: 24px; background: #2a2a4a; border-radius: 12px; overflow: hidden; }}
  .bar-fill {{ height: 100%; border-radius: 12px; transition: width 0.5s; }}
  .bar-fill.teal {{ background: linear-gradient(90deg, #4ecdc4, #44a08d); }}
  .bar-fill.purple {{ background: linear-gradient(90deg, #a855f7, #6366f1); }}
  .bar-fill.orange {{ background: linear-gradient(90deg, #f59e0b, #ef4444); }}
  .bar-value {{ width: 40px; font-size: 0.8rem; color: #888; }}
  .timeline {{ display: flex; flex-direction: column; gap: 0.3rem; }}
  .timeline-item {{ display: flex; align-items: center; gap: 0.5rem; padding: 0.3rem 0; }}
  .timeline-date {{ width: 80px; font-size: 0.8rem; color: #888; }}
  .timeline-bar {{ flex: 1; height: 8px; background: #2a2a4a; border-radius: 4px; }}
  .timeline-fill {{ height: 100%; border-radius: 4px; background: #4ecdc4; }}
  .tag-cloud {{ display: flex; flex-wrap: wrap; gap: 0.5rem; }}
  .tag {{ padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.8rem; background: #2a2a4a; }}
  .tag-count {{ color: #4ecdc4; font-weight: bold; margin-left: 0.3rem; }}
  table {{ width: 100%; border-collapse: collapse; }}
  th, td {{ padding: 0.5rem; text-align: left; border-bottom: 1px solid #2a2a4a; }}
  th {{ color: #888; font-size: 0.85rem; }}
  td {{ font-size: 0.9rem; }}
</style>
</head>
<body>
<div class="container">
  <h1>🧠 Long Memory</h1>
  <p class="subtitle">记忆分析报告 · 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}</p>

  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-value">{len(files_data)}</div>
      <div class="stat-label">对话天数</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">{total_sessions}</div>
      <div class="stat-label">对话段数</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">{total_size / 1024:.1f} KB</div>
      <div class="stat-label">总数据量</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">{len(all_tags)}</div>
      <div class="stat-label">标签数</div>
    </div>
    <div class="stat-card">
      <div class="stat-value">{len(all_topics)}</div>
      <div class="stat-label">话题数</div>
    </div>
  </div>

  <div class="section">
    <h2>🏷️ 标签热度</h2>
    <div class="bar-chart">"""

    max_tag = max(all_tags.values()) if all_tags else 1
    for tag, count in sorted(all_tags.items(), key=lambda x: -x[1])[:10]:
        pct = count / max_tag * 100
        html += f"""
      <div class="bar-row">
        <div class="bar-label">{tag}</div>
        <div class="bar-track"><div class="bar-fill teal" style="width:{pct}%"></div></div>
        <div class="bar-value">{count}</div>
      </div>"""

    html += """
    </div>
  </div>

  <div class="section">
    <h2>💬 话题分布</h2>
    <div class="bar-chart">"""

    max_topic = max(all_topics.values()) if all_topics else 1
    for topic, count in sorted(all_topics.items(), key=lambda x: -x[1])[:10]:
        pct = count / max_topic * 100
        html += f"""
      <div class="bar-row">
        <div class="bar-label">{topic[:20]}</div>
        <div class="bar-track"><div class="bar-fill purple" style="width:{pct}%"></div></div>
        <div class="bar-value">{count}</div>
      </div>"""

    html += """
    </div>
  </div>

  <div class="section">
    <h2>📈 对话活跃度</h2>
    <div class="timeline">"""

    max_sessions = max((f["sessions"] for f in files_data), default=1)
    for f in files_data[-14:]:  # 最近14天
        pct = f["sessions"] / max_sessions * 100 if max_sessions > 0 else 0
        html += f"""
      <div class="timeline-item">
        <div class="timeline-date">{f['date']}</div>
        <div class="timeline-bar"><div class="timeline-fill" style="width:{pct}%"></div></div>
        <div style="font-size:0.8rem;color:#888;width:40px">{f['sessions']}</div>
      </div>"""

    html += f"""
    </div>
  </div>

  <div class="section">
    <h2>📋 对话详情</h2>
    <table>
      <tr><th>日期</th><th>对话数</th><th>大小</th><th>标签</th><th>话题</th></tr>"""

    for f in reversed(files_data[-20:]):
        tags_str = " ".join(f'<span class="tag">{t}</span>' for t in f["tags"][:5])
        topics_str = ", ".join(t[:20] for t in f["topics"][:3])
        size_str = f"{f['size'] / 1024:.1f}KB" if f["size"] > 1024 else f"{f['size']}B"
        html += f"""
      <tr><td>{f['date']}</td><td>{f['sessions']}</td><td>{size_str}</td>
          <td>{tags_str}</td><td>{topics_str}</td></tr>"""

    html += """
    </table>
  </div>
</div>
</body>
</html>"""

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")
    return str(output)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="HTML 可视化报告")
    p.add_argument("--memory-dir", default=None)
    p.add_argument("--output", "-o", default=None, help="输出 HTML 文件路径")
    args = p.parse_args()

    md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
    md = Path(md)

    if args.output:
        out = Path(args.output)
    else:
        out = md / "report.html"

    result = generate_html_report(md, out)
    print(f"✅ 报告已生成: {result}")
