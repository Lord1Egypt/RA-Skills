#!/usr/bin/env python3
"""
Build the kids AI magazine HTML from a stories JSON file + template.
Usage: python3 build_magazine.py --stories stories.json --template template.html --output output/
"""
import argparse
import json
import os
import re

def build_story_card(story, index):
    """Generate HTML for a single story card."""
    icon = story.get("icon", "🤖")
    title = story.get("title", f"故事{index}")
    paragraphs = story.get("paragraphs", [])
    dialogue = story.get("dialogue", [])
    parent_note = story.get("parent_note", "")
    source_url = story.get("source_url", "")
    source_name = story.get("source_name", "")
    audio_file = f"story{index}.mp3"

    html = f'''<div class="story-card" data-icon="{icon}">
  <h3>{icon} 故事{_cn_num(index)}：{title}</h3>
  <div class="audio-box">
    <span class="play-icon">🔊</span>
    <div style="flex:1">
      <div class="audio-label">📖 听故事（点击播放）</div>
      <audio controls preload="none" style="width:100%; margin-top:4px;">
        <source src="{audio_file}" type="audio/mpeg">
      </audio>
    </div>
  </div>
'''
    for p in paragraphs:
        html += f'  <p>{p}</p>\n'

    if dialogue:
        html += '  <div class="talk">\n'
        for d in dialogue:
            role = d.get("role", "child")
            avatar = d.get("avatar", "👶" if role == "child" else "👩")
            text = d.get("text", "")
            direction = "right" if role == "parent" else ""
            html += f'    <div class="line {direction}">\n'
            html += f'      <div class="avatar">{avatar}</div>\n'
            html += f'      <div class="bubble">{text}</div>\n'
            html += f'    </div>\n'
        html += '  </div>\n'

    if parent_note:
        source_html = ""
        if source_url and source_name:
            source_html = f'<br>📰 <a href="{source_url}" style="color:var(--pink)">新闻来源：{source_name}</a>'
        html += f'''  <div class="for-parent">
    <div class="label">👨‍👩‍👧 给爸爸妈妈的话：</div>
    {parent_note}{source_html}
  </div>\n'''

    html += '</div>\n'
    return html

def _cn_num(n):
    nums = {1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七", 8: "八", 9: "九", 10: "十"}
    return nums.get(n, str(n))

def main():
    parser = argparse.ArgumentParser(description="Build kids AI magazine HTML")
    parser.add_argument("--stories", required=True, help="Path to stories JSON")
    parser.add_argument("--template", required=True, help="Path to HTML template")
    parser.add_argument("--output", default="./output/index.html", help="Output HTML path")
    parser.add_argument("--issue", default="第1期", help="Issue number")
    parser.add_argument("--date", default="2026年3月", help="Issue date")
    args = parser.parse_args()

    with open(args.stories, "r", encoding="utf-8") as f:
        stories = json.load(f)

    with open(args.template, "r", encoding="utf-8") as f:
        template = f.read()

    # Build story cards
    story_html = ""
    for i, story in enumerate(stories, 1):
        story_html += build_story_card(story, i)

    # Replace placeholders
    output = template.replace("{{STORIES}}", story_html)
    output = output.replace("{{ISSUE}}", args.issue)
    output = output.replace("{{DATE}}", args.date)

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"✅ Magazine built: {args.output} ({len(stories)} stories)")

if __name__ == "__main__":
    main()
