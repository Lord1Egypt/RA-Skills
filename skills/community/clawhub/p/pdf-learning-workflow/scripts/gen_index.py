#!/usr/bin/env python3
"""为书籍生成 HTML 总导航页"""
import sys, os, re

def generate_index(book_dir):
    files = os.listdir(book_dir)
    book_name = os.path.basename(book_dir)
    
    # 查找关键文件
    full_md = next((f for f in files if f.endswith('.md') and not f.endswith('-guide.md') and f != 'chapter_structure.md'), None)
    guide_md = next((f for f in files if f.endswith('-guide.md')), None)
    chapter_file = "chapter_structure.md"
    
    # 学习笔记
    learning_dir = os.path.join(book_dir, "learning")
    chapters = []
    if os.path.isdir(learning_dir):
        for f in sorted(os.listdir(learning_dir)):
            if f.endswith('.md') and not f.endswith('.html'):
                base = os.path.splitext(f)[0]
                title = re.sub(r'^chapter_\d+_', '', base).replace('-', ' ')
                m = re.match(r'chapter_(\d+)', f)
                num = m.group(1) if m else ''
                html_exists = os.path.exists(os.path.join(learning_dir, base + '.html'))
                chapters.append((num, title, f, base + '.html' if html_exists else ''))
    
    # 图片统计
    assets_dir = os.path.join(book_dir, "assets")
    img_count = len([f for f in os.listdir(assets_dir) if f.endswith('.png')]) if os.path.isdir(assets_dir) else 0
    
    # 构建章节列表 HTML
    chapter_items = []
    for num, title, md_file, html_file in chapters:
        links = ''
        if html_file:
            links += f'<a class="html-link" href="learning/{html_file}">HTML</a>'
        links += f'<a class="md-link" href="learning/{md_file}">MD</a>'
        chapter_items.append(f'''
    <div class="chapter-item">
      <span class="chapter-num">{num}</span>
      <span class="chapter-title">{title}</span>
      <div class="chapter-links">{links}</div>
    </div>''')
    
    chapters_html = ''.join(chapter_items)
    
    # 统计 HTML 笔记数
    html_count = sum(1 for _, _, _, h in chapters if h)
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{book_name} — 学习导航</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    background: #0d1117; color: #c9d1d9;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    line-height: 1.6; padding: 40px 20px;
    max-width: 900px; margin: 0 auto;
  }}
  h1 {{ color: #58a6ff; font-size: 28px; margin-bottom: 4px; }}
  .subtitle {{ color: #8b949e; font-size: 14px; margin-bottom: 24px; }}
  .stats {{ display: flex; gap: 16px; margin-bottom: 28px; flex-wrap: wrap; }}
  .stat-card {{
    background: #161b22; border: 1px solid #30363d; border-radius: 8px;
    padding: 12px 18px; text-align: center; min-width: 100px;
  }}
  .stat-card .num {{ color: #58a6ff; font-size: 24px; font-weight: 600; display: block; }}
  .stat-card .label {{ color: #8b949e; font-size: 12px; }}
  .nav-links {{ display: flex; gap: 10px; margin-bottom: 28px; flex-wrap: wrap; }}
  .nav-links a {{
    display: inline-flex; align-items: center; gap: 6px;
    padding: 8px 16px; border-radius: 6px; font-size: 14px;
    text-decoration: none; transition: .15s;
  }}
  .nav-links a.primary {{ background: #1f6feb; color: #fff; border: 1px solid #1f6feb; }}
  .nav-links a.primary:hover {{ background: #388bfd; }}
  .nav-links a.secondary {{ background: #21262d; color: #c9d1d9; border: 1px solid #30363d; }}
  .nav-links a.secondary:hover {{ background: #30363d; border-color: #58a6ff; }}
  h2 {{ color: #f0883e; font-size: 18px; margin: 24px 0 12px; border-bottom: 1px solid #30363d; padding-bottom: 6px; }}
  .chapter-list {{ display: flex; flex-direction: column; gap: 6px; }}
  .chapter-item {{
    display: flex; align-items: center; gap: 10px;
    background: #161b22; border: 1px solid #30363d; border-radius: 6px;
    padding: 10px 14px; transition: .15s;
  }}
  .chapter-item:hover {{ border-color: #58a6ff; background: #1c2333; }}
  .chapter-num {{
    background: #1f6feb; color: #fff; border-radius: 50%;
    width: 28px; height: 28px; display: flex; align-items: center; justify-content: center;
    font-size: 12px; font-weight: 600; flex-shrink: 0;
  }}
  .chapter-title {{ flex: 1; font-size: 14px; }}
  .chapter-links {{ display: flex; gap: 4px; }}
  .chapter-links a {{
    padding: 3px 10px; border-radius: 4px; font-size: 11px;
    text-decoration: none; transition: .15s;
  }}
  .chapter-links a.html-link {{ background: #23863633; color: #3fb950; border: 1px solid #23863655; }}
  .chapter-links a.html-link:hover {{ background: #23863655; }}
  .chapter-links a.md-link {{ background: #1f6feb33; color: #58a6ff; border: 1px solid #1f6feb55; }}
  .chapter-links a.md-link:hover {{ background: #1f6feb55; }}
  .footer {{ margin-top: 40px; padding-top: 16px; border-top: 1px solid #30363d; font-size: 12px; color: #8b949e; }}
</style>
</head>
<body>
  <h1>📖 {book_name}</h1>
  <p class="subtitle">扫描版 PDF → OCR → 学习优化笔记</p>

  <div class="stats">
    <div class="stat-card"><span class="num">{len(chapters)}</span><span class="label">章节</span></div>
    <div class="stat-card"><span class="num">{img_count}</span><span class="label">插图</span></div>
    <div class="stat-card"><span class="num">{html_count}</span><span class="label">HTML 笔记</span></div>
  </div>

  <div class="nav-links">
    <a class="primary" href="{guide_md.replace('.md', '.html') if guide_md else '#'}">📋 导读</a>
    <a class="secondary" href="{chapter_file}">📑 章节结构</a>
    <a class="secondary" href="{full_md.replace('.md', '.html') if full_md else '#'}">📄 全文</a>
  </div>

  <h2>📚 章节</h2>
  <div class="chapter-list">{chapters_html}</div>

  <div class="footer">
    由 pdf-learning-workflow 生成 | {book_name}
  </div>
</body>
</html>'''

    out_path = os.path.join(book_dir, 'index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"✅ 导航页已生成: {out_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: gen_index.py <book_output_dir>")
        sys.exit(1)
    generate_index(sys.argv[1])
