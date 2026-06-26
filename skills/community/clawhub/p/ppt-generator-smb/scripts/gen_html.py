#!/usr/bin/env python3
"""HTML 幻灯片生成器 - 乔布斯风极简科技感"""

import argparse
import json
import os

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{height:100%;overflow:hidden;background:#0a0a0a;font-family:'Helvetica Neue',Arial,'PingFang SC','Microsoft YaHei',sans-serif}}
.slide{{width:100vw;height:100vh;display:none;flex-direction:column;justify-content:center;align-items:center;padding:60px 80px;position:relative}}
.slide.active{{display:flex}}
.slide::before{{content:'';position:absolute;top:50%;left:50%;width:700px;height:700px;background:radial-gradient(circle,rgba(255,107,53,.12) 0%,transparent 70%);transform:translate(-50%,-50%);pointer-events:none}}
h1{{color:#fff;font-size:3.2rem;font-weight:900;text-align:center;line-height:1.3;margin-bottom:20px}}
h2{{color:#fff;font-size:2.6rem;font-weight:800;text-align:center;margin-bottom:35px}}
h3{{color:#FF6B35;font-size:1.6rem;font-weight:700;margin-bottom:15px}}
p{{color:rgba(255,255,255,.85);font-size:1.4rem;line-height:1.8;text-align:center;max-width:900px}}
.subtitle{{color:rgba(255,255,255,.5);font-size:1.2rem;margin-top:15px}}
.highlight{{color:#FF6B35}}
.card{{background:rgba(255,255,255,.04);border-radius:18px;padding:35px;margin:12px;border:1px solid rgba(255,255,255,.08);flex:1;min-width:280px}}
.card h4{{color:#FF6B35;font-size:1.2rem;margin-bottom:12px}}
.card p{{font-size:1rem;color:rgba(255,255,255,.7);text-align:left}}
.cards{{display:flex;gap:25px;flex-wrap:wrap;justify-content:center;margin-top:25px}}
.grid-2{{display:grid;grid-template-columns:1fr 1fr;gap:35px;margin-top:25px}}
.stat-item{{text-align:center;margin:0 30px}}
.stat-number{{color:#fff;font-size:3.5rem;font-weight:900;background:linear-gradient(135deg,#FF6B35,#FF9F5A);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.stat-label{{color:rgba(255,255,255,.5);font-size:.95rem;margin-top:10px;text-transform:uppercase;letter-spacing:2px}}
.bar-chart{{display:flex;align-items:flex-end;justify-content:center;gap:35px;height:220px;margin-top:35px}}
.bar{{display:flex;flex-direction:column;align-items:center;gap:8px}}
.bar-fill{{width:55px;background:linear-gradient(180deg,#FF6B35,#FF9F5A);border-radius:8px 8px 0 0}}
.bar-label{{color:rgba(255,255,255,.6);font-size:.85rem}}
.bar-value{{color:#fff;font-size:.95rem;font-weight:700}}
ul{{list-style:none;margin:20px 0}}
ul li{{color:rgba(255,255,255,.85);font-size:1.2rem;padding:10px 0;border-bottom:1px solid rgba(255,255,255,.08);display:flex;align-items:center}}
ul li::before{{content:'→';color:#FF6B35;margin-right:15px}}
.swot{{background:rgba(255,107,53,.08);border-radius:18px;padding:30px;border:1px solid rgba(255,107,53,.25);flex:1}}
.swot h4{{color:#fff;font-size:1.3rem;margin-bottom:12px}}
.swot ul li{{font-size:1rem;padding:8px 0}}
.conclusion{{background:linear-gradient(135deg,rgba(255,107,53,.15),rgba(255,159,90,.08));border-radius:25px;padding:45px;border:2px solid rgba(255,107,53,.35)}}
.page-num{{position:absolute;bottom:30px;right:40px;color:rgba(255,255,255,.25);font-size:.85rem}}
</style>
</head>
<body>
{slides}
<div id="nav" style="position:fixed;bottom:30px;left:50%;transform:translateX(-50%);display:flex;align-items:center;gap:30px;z-index:999">
  <button id="prev" onclick="go(cur-1)" style="width:50px;height:50px;border-radius:50%;border:2px solid rgba(255,255,255,.3);background:rgba(0,0,0,.5);color:#fff;font-size:1.5rem;cursor:pointer;backdrop-filter:blur(10px)">&#8592;</button>
  <span id="pageInfo" style="color:rgba(255,255,255,.6);font-size:1rem;min-width:60px;text-align:center">1 / {total}</span>
  <button id="next" onclick="go(cur+1)" style="width:50px;height:50px;border-radius:50%;border:2px solid rgba(255,255,255,.3);background:rgba(0,0,0,.5);color:#fff;font-size:1.5rem;cursor:pointer;backdrop-filter:blur(10px)">&#8594;</button>
</div>
<script>
let cur=0;const total={total};const slides=document.querySelectorAll('.slide');
function go(n){{slides[cur].classList.remove('active');cur=Math.max(0,Math.min(n,total-1));slides[cur].classList.add('active');updateNav()}}
function updateNav(){{document.getElementById('prev').style.opacity=cur===0?'0.3':'1';document.getElementById('next').style.opacity=cur===total-1?'0.3':'1';document.getElementById('pageInfo').textContent=(cur+1)+' / '+total}}
document.onkeydown=e=>{{if(e.key==='ArrowRight'||e.key==='ArrowDown')go(cur+1);if(e.key==='ArrowLeft'||e.key==='ArrowUp')go(cur-1)}};
document.ontouchstart=e=>{{const x=e.touches[0].clientX;if(x>window.innerWidth/2)go(cur+1);else go(cur-1)}};
setTimeout(updateNav,100);
</script>
</body>
</html>'''

def make_slide(content, index, total):
    return f'<div class="slide{" active" if index == 0 else ""}" id="s{index+1}">{content}<span class="page-num">{index+1} / {total}</span></div>\n'

def make_title_slide(title, subtitle):
    content = f'''
  <div style="font-size:5rem;margin-bottom:20px">🦞</div>
  <h1>{title}</h1>
  <p class="subtitle">{subtitle}</p>'''
    return content

def make_content_slide(title, items):
    if isinstance(items, list):
        items_html = ''.join(f'<li>{item}</li>' for item in items)
        return f'\n  <h2>{title}</h2>\n  <ul>{items_html}</ul>\n'
    return f'\n  <h2>{title}</h2>\n  <p>{items}</p>\n'

def make_cards_slide(title, cards):
    cards_html = ''
    for card in cards:
        cards_html += f'<div class="card"><h4>{card["icon"]} {card["title"]}</h4><p>{card["content"]}</p></div>\n'
    return f'\n  <h2>{title}</h2>\n  <div class="cards">{cards_html}</div>\n'

def make_chart_slide(title, data):
    bars = ''
    for item in data:
        h = item.get("height", 100)
        bars += f'''<div class="bar">
      <div class="bar-value">{item["value"]}</div>
      <div class="bar-fill" style="height:{h}px"></div>
      <div class="bar-label">{item["label"]}</div>
    </div>\n'''
    return f'\n  <h2>{title}</h2>\n  <div class="bar-chart">{bars}</div>\n'

def make_swot_slide(title, strengths, weaknesses):
    s_items = ''.join(f'<li>{s}</li>' for s in strengths)
    w_items = ''.join(f'<li>{w}</li>' for w in weaknesses)
    return f'''
  <h2>{title}</h2>
  <div class="grid-2">
    <div class="swot"><h4>💪 Strengths 优势</h4><ul>{s_items}</ul></div>
    <div class="swot" style="border-color:rgba(255,149,0,.35);background:rgba(255,149,0,.06)"><h4>⚠️ Weaknesses 劣势</h4><ul>{w_items}</ul></div>
  </div>\n'''

def main():
    parser = argparse.ArgumentParser(description='HTML 幻灯片生成器')
    parser.add_argument('--title', required=True, help='演示文稿标题')
    parser.add_argument('--subtitle', default='', help='副标题')
    parser.add_argument('--output', default='slides.html', help='输出文件路径')
    parser.add_argument('--data', help='JSON 数据文件')
    args = parser.parse_args()
    
    # 如果提供了 JSON 数据文件
    if args.data and os.path.exists(args.data):
        with open(args.data, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {"slides": []}
    
    # 生成幻灯片
    slides_html = ''
    slides_html += make_slide(make_title_slide(args.title, args.subtitle), 0, len(data.get("slides", [])) + 1)
    
    for i, slide in enumerate(data.get("slides", [])):
        slide_type = slide.get("type", "content")
        if slide_type == "content":
            content = make_content_slide(slide["title"], slide.get("items", slide.get("content", "")))
        elif slide_type == "cards":
            content = make_cards_slide(slide["title"], slide.get("cards", []))
        elif slide_type == "chart":
            content = make_chart_slide(slide["title"], slide.get("data", []))
        elif slide_type == "swot":
            content = make_swot_slide(slide["title"], slide.get("strengths", []), slide.get("weaknesses", []))
        else:
            content = make_content_slide(slide["title"], slide.get("content", ""))
        slides_html += make_slide(content, i + 1, len(data.get("slides", [])) + 1)
    
    total = len(data.get("slides", [])) + 1
    html = HTML_TEMPLATE.format(title=args.title, slides=slides_html, total=total)
    
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Done: {args.output}")

if __name__ == '__main__':
    main()
