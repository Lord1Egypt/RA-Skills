#!/usr/bin/env python3
"""
单话题深度创作工具 - v6.0
搜索当天真实热门话题，选择一个深度创作，生成简约图片，自动发布
"""

import json
import urllib.request
import ssl
import argparse
import random
import time
from datetime import datetime
from pathlib import Path

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

def fetch_jina_search(query, retry=3):
    """使用 Jina Search API 搜索，支持重试"""
    for i in range(retry):
        try:
            url = f"https://s.jina.ai/{urllib.request.quote(query)}"
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=30, context=ssl_context) as response:
                data = json.loads(response.read().decode())
                results = data.get('data', [])
                if results:
                    return results
        except Exception as e:
            print(f"  尝试 {i+1}/{retry}: {e}")
            if i < retry - 1:
                time.sleep(2)
    return []

def fetch_jina_read(url, retry=2):
    """使用 Jina Reader 读取网页内容"""
    for i in range(retry):
        try:
            read_url = f"https://r.jina.ai/{url}"
            req = urllib.request.Request(read_url, headers={"Accept": "text/markdown"})
            with urllib.request.urlopen(req, timeout=30, context=ssl_context) as response:
                return response.read().decode()[:10000]
        except Exception as e:
            if i < retry - 1:
                time.sleep(2)
    return ""

def create_deep_content(keyword, selected_topic):
    """针对单个话题创作深度小红书文案"""
    
    emojis = {
        '减肥': '🔥', '职场': '💼', '学习': '📚', '科技': '💻',
        '美食': '🍔', '旅游': '✈️', '生活': '✨', '时尚': '👗',
        '健身': '💪', '护肤': '💆', 'AI': '🤖'
    }
    
    emoji = emojis.get(keyword, '📌')
    
    # 标题模板
    title_templates = [
        f"{emoji} 关于{selected_topic[:15]}，这篇说清楚了！",
        f"{emoji} {selected_topic[:18]}，亲测有效！",
        f"{emoji} 终于有人把{selected_topic[:12]}说明白了！",
        f"{emoji} {selected_topic[:16]}，看这篇就够了！"
    ]
    title = random.choice(title_templates)[:20]
    
    # 创作深度内容
    content = f"""【深度解读】{selected_topic}

📌 最近这个话题很火，今天给大家深度解读一下！

━━━━━━━━━━━━━━━━

🔍 什么是{selected_topic[:10]}？

简单来说，这是当下{keyword}领域的热门趋势。

━━━━━━━━━━━━━━━━

💡 核心要点：

✓ 为什么这个话题会火？
  - 满足了实际需求
  - 符合当下趋势
  - 有实际可操作性

✓ 适合哪些人？
  - 对{keyword}感兴趣
  - 想要改变现状
  - 愿意尝试新方法

✓ 需要注意什么？
  - 选择适合的方法
  - 不要盲目跟风
  - 坚持才能看到效果

━━━━━━━━━━━━━━━━

📝 实操指南：

【第一阶段】了解与准备
1. 深入了解基本原理
2. 评估自身情况
3. 做好准备工作

【第二阶段】开始实践
1. 从简单方法开始
2. 记录过程和感受
3. 根据反馈调整

【第三阶段】持续优化
1. 总结经验教训
2. 形成自己的方法
3. 持续改进坚持

━━━━━━━━━━━━━━━━

🎯 行动建议：

□ 收藏本文，方便回顾
□ 选择 1-2 个要点开始
□ 记录实践过程和变化
□ 在评论区分享经验

━━━━━━━━━━━━━━━━

❓ 常见问题：

Q：这个方法真的有效吗？
A：因人而异，关键是找到适合自己的并坚持。

Q：多久能看到效果？
A：一般 2-4 周开始有感觉，3 个月会有明显变化。

Q：有什么需要避免的坑？
A：不要急于求成，不要盲目跟风，要科学实践。

━━━━━━━━━━━━━━━━

👇 互动话题：
你对这个话题有什么看法？
欢迎在评论区分享你的经验和疑问！

#{keyword} #深度解读 #干货分享 #实用指南 #2026 趋势 #经验分享"""

    return {
        "title": title,
        "content": content,
        "tags": [f"#{keyword}", "#深度解读", "#干货分享"],
        "selected_topic": selected_topic,
        "word_count": len(content)
    }

def generate_simple_image(keyword, title):
    """生成简约图片 - 纯色背景 + 标题"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        width, height = 1080, 1440
        img = Image.new('RGB', (width, height), color=(240, 240, 240))
        draw = ImageDraw.Draw(img)
        
        # 配色方案（纯色）
        colors = {
            '减肥': (255, 182, 193),
            '职场': (100, 149, 237),
            '学习': (255, 218, 185),
            '科技': (138, 43, 226),
            '美食': (255, 165, 0),
            '旅游': (135, 206, 235),
            '生活': (255, 192, 203),
            '时尚': (255, 20, 147),
            '健身': (50, 205, 50),
        }
        
        bg_color = colors.get(keyword, (100, 149, 237))
        
        # 填充纯色背景
        draw.rectangle([(0, 0), (width, height)], fill=bg_color)
        
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
        except:
            title_font = ImageFont.load_default()
        
        # 绘制标题（居中）
        main_title = f"📌 {keyword}"
        title_bbox = draw.textbbox((0, 0), main_title, font=title_font)
        title_x = (width - (title_bbox[2] - title_bbox[0])) // 2
        title_y = height // 2
        draw.text((title_x, title_y), main_title, fill=(255, 255, 255), font=title_font)
        
        output_path = "/tmp/xiaohongshu-simple.jpg"
        img.save(output_path, quality=90)
        print(f"✅ 简约图片已生成：{output_path}")
        return [output_path]
        
    except Exception as e:
        print(f"⚠️ 图片生成失败：{e}")
        return []

def publish_to_xiaohongshu(title, content, images):
    """发布到小红书"""
    import subprocess
    
    # 处理内容中的特殊字符
    safe_content = content.replace('\n', '\\n').replace('"', '\\"')
    cmd = f"mcporter call 'xiaohongshu.publish_content(title: \"{title}\", content: \"{safe_content}\", images: {json.dumps(images)})'"
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=90)
        if result.stdout and ('成功' in result.stdout or 'Success' in result.stdout):
            print(f"✅ 发布成功：{result.stdout}")
            return {"status": "success", "message": result.stdout}
        else:
            return {"status": "error", "message": result.stdout or result.stderr}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def main():
    parser = argparse.ArgumentParser(description='单话题深度创作工具 v6.0')
    parser.add_argument('--keyword', '-k', type=str, default='职场干货',
                       help='搜索关键词')
    parser.add_argument('--auto-publish', '-a', action='store_true',
                       help='自动发布到小红书')
    parser.add_argument('--topic', '-t', type=str, default='',
                       help='指定话题（可选）')
    
    args = parser.parse_args()
    
    keyword = args.keyword
    auto_publish = args.auto_publish
    custom_topic = args.topic
    
    print(f"🔍 开始搜索 \"{keyword}\" 相关的当天热门话题...\n")
    
    hot_topics = []
    
    # 搜索热门话题（多个查询，确保获取真实数据）
    queries = [
        f"{keyword} 热门话题 2026 今天",
        f"{keyword} 最新趋势 火爆",
        f"{keyword} 深度解读 指南"
    ]
    
    for query in queries:
        print(f"  - 搜索：{query}")
        results = fetch_jina_search(query, retry=3)
        
        for item in results[:5]:
            title = item.get('title', '')
            if title and len(title) > 15 and len(title) < 100:
                hot_topics.append(title[:80])
        
        if hot_topics:
            print(f"    ✅ 找到 {len(hot_topics)} 个话题")
            break
        else:
            time.sleep(3)
    
    # 如果搜索失败，明确提示
    if not hot_topics:
        print("\n❌ 无法获取当天热门话题，请检查网络连接后重试")
        print("\n建议：")
        print("1. 检查网络连接")
        print("2. 稍后重试")
        print("3. 使用 --topic 参数指定话题")
        return
    
    # 去重
    hot_topics = list(dict.fromkeys(hot_topics))[:10]
    
    # 输出热门话题清单
    print("\n" + "=" * 70)
    print(f"📋 {keyword} - 当天热门话题")
    print("=" * 70)
    
    for i, topic in enumerate(hot_topics, 1):
        print(f"\n【话题{i}】{topic}")
    
    # 选择话题
    if custom_topic:
        selected_topic = custom_topic
        print(f"\n✅ 使用指定话题：{selected_topic}")
    else:
        selected_topic = hot_topics[0] if hot_topics else f"{keyword}新趋势"
        print(f"\n🎯 自动选择话题：{selected_topic}")
    
    # 创作深度内容
    print("\n" + "=" * 70)
    print(f"📝 针对话题创作文案：{selected_topic}")
    print("=" * 70)
    
    article = create_deep_content(keyword, selected_topic)
    
    print(f"\n标题：{article['title']}")
    print(f"\n内容：\n{article['content']}")
    print(f"\n字数：{article['word_count']} 字")
    
    # 生成简约图片
    print("\n" + "=" * 70)
    print("🎨 生成简约图片...")
    images = generate_simple_image(keyword, article['title'])
    
    # 保存到文件
    output_path = Path(f"/home/admin/openclaw/workspace/temp/xiaohongshu-{keyword}-deep.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    draft = f"""# 小红书深度图文草稿 - {keyword}

## 选定话题
{selected_topic}

## 标题
{article['title']}

## 内容
{article['content']}

## 图片
{chr(10).join(images) if images else '无'}

---
生成时间：{datetime.now().isoformat()}
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(draft)
    
    print(f"\n💾 文案已保存到：{output_path}")
    
    # 发布到小红书
    if auto_publish:
        print("\n📤 自动发布到小红书...")
        if not images:
            print("⚠️ 图片生成失败，无法发布")
        else:
            result = publish_to_xiaohongshu(article['title'], article['content'], images)
            if result['status'] == 'success':
                print(f"✅ 发布成功！")
            else:
                print(f"❌ 发布失败：{result['message']}")
    else:
        print("\n⏳ 如需发布，请添加 --auto-publish 参数")
    
    print("\n✅ 流程完成！")

if __name__ == "__main__":
    main()
