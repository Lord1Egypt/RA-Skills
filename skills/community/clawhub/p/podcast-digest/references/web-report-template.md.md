# Web 报告模板规范 — 播客深度纪要

## 设计原则

- 深色主题（护眼，适合长时间阅读）
- 响应式布局
- 卡片式信息架构
- 渐进式展示（折叠/展开）
- 标签系统（点击可过滤）

## 色彩系统

```css
--bg-primary: #0f0f1a;        /* 主背景 */
--bg-card: #1a1a2e;           /* 卡片背景 */
--bg-elevated: #252540;       /* 悬浮元素 */
--accent-purple: #7c3aed;     /* 主强调色 */
--accent-blue: #2563eb;       /* 次强调色 */
--accent-green: #059669;      /* 成功/关联色 */
--accent-amber: #d97706;      /* 警告/张力色 */
--text-primary: #f1f5f9;      /* 主文字 */
--text-secondary: #94a3b8;    /* 次要文字 */
--text-muted: #475569;        /* 弱化文字 */
--border: #2d2d4e;            /* 边框色 */
```

## 完整 HTML 结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[播客名] EP[XX] — 深度纪要</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body {
      font-family: -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif;
      background: #0f0f1a;
      color: #f1f5f9;
      line-height: 1.7;
    }
    
    /* ===== 导航 ===== */
    nav {
      position: sticky; top: 0; z-index: 100;
      background: rgba(15,15,26,0.95);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid #2d2d4e;
      padding: 0 2rem;
      display: flex; align-items: center; gap: 2rem;
      height: 56px;
    }
    nav .logo { font-weight: 700; color: #7c3aed; font-size: 0.9rem; }
    nav a { color: #94a3b8; text-decoration: none; font-size: 0.85rem; 
            transition: color .2s; }
    nav a:hover { color: #f1f5f9; }
    
    /* ===== 英雄区 ===== */
    .hero {
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
      padding: 4rem 2rem 3rem;
      border-bottom: 1px solid #2d2d4e;
    }
    .hero-inner { max-width: 900px; margin: 0 auto; }
    .episode-badge {
      display: inline-block;
      background: rgba(124,58,237,0.2);
      color: #a78bfa;
      border: 1px solid rgba(124,58,237,0.4);
      border-radius: 20px;
      padding: .25rem 1rem;
      font-size: .8rem; font-weight: 600;
      margin-bottom: 1rem;
    }
    .hero h1 { font-size: 2rem; font-weight: 800; line-height: 1.3;
               margin-bottom: .75rem; }
    .hero .tagline { color: #94a3b8; font-size: 1.05rem; margin-bottom: 1.5rem; }
    .meta-row { display: flex; flex-wrap: wrap; gap: 1.5rem; }
    .meta-item { display: flex; align-items: center; gap: .4rem;
                 color: #64748b; font-size: .85rem; }
    
    /* ===== 主布局 ===== */
    .container { max-width: 900px; margin: 0 auto; padding: 2rem; }
    .section { margin-bottom: 3rem; }
    .section-title {
      font-size: 1.1rem; font-weight: 700; color: #a78bfa;
      letter-spacing: .05em; text-transform: uppercase;
      margin-bottom: 1.25rem;
      display: flex; align-items: center; gap: .5rem;
    }
    .section-title::after {
      content: ''; flex: 1; height: 1px; background: #2d2d4e;
    }
    
    /* ===== 卡片 ===== */
    .card {
      background: #1a1a2e;
      border: 1px solid #2d2d4e;
      border-radius: 12px;
      padding: 1.5rem;
      margin-bottom: 1rem;
      transition: border-color .2s, transform .2s;
    }
    .card:hover { border-color: #7c3aed; transform: translateY(-1px); }
    .card-header { display: flex; align-items: flex-start; 
                   justify-content: space-between; cursor: pointer; }
    .card-title { font-weight: 600; font-size: 1rem; }
    .card-body { margin-top: 1rem; color: #94a3b8; font-size: .9rem; 
                 display: none; }
    .card-body.open { display: block; }
    .card-badge {
      font-size: .7rem; padding: .2rem .6rem;
      border-radius: 10px; font-weight: 600; white-space: nowrap;
    }
    .badge-purple { background: rgba(124,58,237,.2); color: #a78bfa; }
    .badge-blue   { background: rgba(37,99,235,.2);  color: #93c5fd; }
    .badge-green  { background: rgba(5,150,105,.2);  color: #6ee7b7; }
    .badge-amber  { background: rgba(217,119,6,.2);  color: #fcd34d; }
    .badge-red    { background: rgba(220,38,38,.2);  color: #fca5a5; }
    
    /* ===== 论点卡片 ===== */
    .argument-card {
      border-left: 3px solid #7c3aed;
    }
    .argument-level {
      font-size: .75rem; color: #7c3aed; font-weight: 700;
      margin-bottom: .5rem;
    }
    .evidence { background: #0f1929; border-radius: 8px; padding: .75rem 1rem;
                margin-top: .75rem; font-size: .85rem; color: #93c5fd; }
    .tension  { background: #1f0f0f; border-radius: 8px; padding: .75rem 1rem;
                margin-top: .75rem; font-size: .85rem; color: #fca5a5; }
    
    /* ===== 金句 ===== */
    .quote-card {
      border-left: 3px solid #2563eb;
      background: #0f1929;
    }
    .quote-text {
      font-size: 1.05rem; color: #e2e8f0; font-style: italic;
      margin-bottom: .75rem; line-height: 1.8;
    }
    .quote-text::before { content: '"'; color: #2563eb; font-size: 1.5rem; }
    .quote-text::after  { content: '"'; color: #2563eb; font-size: 1.5rem; }
    .quote-speaker { font-size: .8rem; color: #64748b; }
    .quote-insight { margin-top: .75rem; padding-top: .75rem;
                     border-top: 1px solid #1e2d4e; }
    .insight-row { display: flex; gap: .5rem; align-items: baseline;
                   margin-bottom: .4rem; font-size: .85rem; }
    .insight-label { color: #7c3aed; font-weight: 600; min-width: 4em; }
    
    /* ===== 标签云 ===== */
    .tag-cloud { display: flex; flex-wrap: wrap; gap: .5rem; }
    .tag {
      padding: .3rem .75rem; border-radius: 20px;
      font-size: .8rem; cursor: pointer; transition: all .2s;
      border: 1px solid #2d2d4e; color: #94a3b8;
    }
    .tag:hover, .tag.active {
      background: rgba(124,58,237,.2);
      border-color: #7c3aed; color: #a78bfa;
    }
    
    /* ===== 嘉宾卡片 ===== */
    .guest-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px,1fr));
                  gap: 1rem; }
    .guest-card {
      background: #1a1a2e; border: 1px solid #2d2d4e; border-radius: 12px;
      padding: 1.25rem; text-align: center;
    }
    .guest-avatar {
      width: 56px; height: 56px; border-radius: 50%;
      background: linear-gradient(135deg, #7c3aed, #2563eb);
      display: flex; align-items: center; justify-content: center;
      font-size: 1.4rem; margin: 0 auto .75rem;
    }
    .guest-name { font-weight: 700; margin-bottom: .25rem; }
    .guest-role { font-size: .8rem; color: #64748b; margin-bottom: .75rem; }
    .guest-stance {
      font-size: .8rem; color: #a78bfa;
      background: rgba(124,58,237,.1); border-radius: 6px;
      padding: .4rem .6rem;
    }
    
    /* ===== 关联播客 ===== */
    .related-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px,1fr));
                    gap: 1rem; }
    .related-card {
      background: #1a1a2e; border: 1px solid #2d2d4e; border-radius: 12px;
      padding: 1.25rem; cursor: pointer; transition: all .2s;
    }
    .related-card:hover { border-color: #059669; }
    .related-ep { font-size: .75rem; color: #059669; margin-bottom: .4rem; }
    .related-title { font-weight: 600; margin-bottom: .4rem; }
    .related-link { font-size: .8rem; color: #94a3b8; }
    .relation-badge { font-size: .75rem; background: rgba(5,150,105,.15);
                      color: #6ee7b7; padding: .15rem .5rem; border-radius: 10px; }
    
    /* ===== 学习路径 ===== */
    .learning-path { display: flex; flex-direction: column; gap: 0; }
    .path-item {
      display: flex; gap: 1rem; align-items: flex-start; padding: 1rem 0;
      border-bottom: 1px solid #1e1e3a;
    }
    .path-num {
      width: 28px; height: 28px; border-radius: 50%;
      background: linear-gradient(135deg, #7c3aed, #2563eb);
      display: flex; align-items: center; justify-content: center;
      font-size: .75rem; font-weight: 700; flex-shrink: 0;
    }
    
    /* ===== Mermaid 容器 ===== */
    .mermaid-wrapper {
      background: #1a1a2e; border: 1px solid #2d2d4e; border-radius: 12px;
      padding: 1.5rem; overflow-x: auto; margin-bottom: 1.5rem;
    }
    
    /* ===== 页脚 ===== */
    footer {
      border-top: 1px solid #2d2d4e;
      padding: 2rem;
      text-align: center;
      color: #475569; font-size: .8rem;
    }
    
    /* ===== 展开/折叠 JS ===== */
  </style>
</head>
<body>

  <!-- 导航 -->
  <nav>
    <span class="logo">🎙️ PODCAST DIGEST</span>
    <a href="#guests">嘉宾</a>
    <a href="#arguments">核心论点</a>
    <a href="#quotes">金句</a>
    <a href="#diagram">关系图</a>
    <a href="#related">关联期</a>
  </nav>

  <!-- 英雄区 -->
  <div class="hero">
    <div class="hero-inner">
      <div class="episode-badge">EP[XX] · [播客名]</div>
      <h1>[本期标题]</h1>
      <p class="tagline">[核心主题一句话描述]</p>
      <div class="meta-row">
        <span class="meta-item">📅 [日期]</span>
        <span class="meta-item">⏱️ [时长]</span>
        <span class="meta-item">👤 [主持人]</span>
        <span class="meta-item">🎯 [嘉宾数]位嘉宾</span>
      </div>
    </div>
  </div>

  <div class="container">
    
    <!-- 嘉宾介绍 -->
    <section class="section" id="guests">
      <div class="section-title">🎭 本期嘉宾</div>
      <div class="guest-grid">
        <!-- 用 .guest-card 填充 -->
      </div>
    </section>

    <!-- 核心论点 -->
    <section class="section" id="arguments">
      <div class="section-title">💡 核心论点</div>
      <!-- 用 .argument-card 填充，每个论点一张卡片 -->
      <!-- 卡片内包含 .evidence 和 .tension -->
    </section>

    <!-- 金句与洞察 -->
    <section class="section" id="quotes">
      <div class="section-title">✨ 金句与洞察</div>
      <!-- 用 .quote-card 填充 -->
    </section>

    <!-- 关系图 -->
    <section class="section" id="diagram">
      <div class="section-title">🗺️ 内容结构图</div>
      <div class="mermaid-wrapper">
        <!-- 嵌入 SVG 或 Mermaid 渲染结果 -->
      </div>
    </section>

    <!-- 知识标签 -->
    <section class="section" id="tags">
      <div class="section-title">🏷️ 知识标签</div>
      <div class="tag-cloud">
        <!-- 用 .tag 填充 -->
      </div>
    </section>

    <!-- 关联播客 -->
    <section class="section" id="related">
      <div class="section-title">🔗 关联期数</div>
      <div class="related-grid">
        <!-- 用 .related-card 填充 -->
      </div>
    </section>

    <!-- 学习路径 -->
    <section class="section" id="learning">
      <div class="section-title">📚 延伸学习路径</div>
      <div class="learning-path">
        <!-- 用 .path-item 填充 -->
      </div>
    </section>

  </div>

  <footer>
    由 Claude Podcast Digest 生成 · [生成日期]
  </footer>

  <script>
    // 卡片折叠/展开
    document.querySelectorAll('.card-header').forEach(header => {
      header.addEventListener('click', () => {
        const body = header.nextElementSibling;
        if (body && body.classList.contains('card-body')) {
          body.classList.toggle('open');
        }
      });
    });
    
    // 标签过滤（可选功能）
    document.querySelectorAll('.tag').forEach(tag => {
      tag.addEventListener('click', () => {
        tag.classList.toggle('active');
      });
    });
  </script>

</body>
</html>
```

## 填充指引

1. 将每个 `[占位符]` 替换为实际内容
2. 嘉宾卡片按主持人 → 嘉宾顺序排列
3. 论点卡片按重要性降序排列
4. 金句不超过 8 条，每条必须有洞察解析
5. 关联播客至少 2 条，标注关联类型（深化/对比/前提/扩展）