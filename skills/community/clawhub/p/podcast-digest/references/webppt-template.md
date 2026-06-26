# Web PPT 模板规范 — 播客内容幻灯片

## 适用场景
- 用户需要分享播客内容给他人
- 演讲/讨论时的视觉辅助
- 播客系列的课程化呈现

## 幻灯片结构

```
Slide 1: 封面（播客名、主题、日期、主讲人）
Slide 2: 本期提要（3-5个核心问题）
Slide 3-N: 核心观点（每页1个论点）
Slide N+1: 金句墙
Slide N+2: 争议与开放问题
Slide N+3: 延伸资源
Slide N+4: 行动清单
```

## HTML 实现方式

使用纯 HTML/CSS + 键盘/按钮翻页。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>[播客名] — [主题] · Slides</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body {
      font-family: -apple-system, 'PingFang SC', sans-serif;
      background: #000;
      overflow: hidden;
      height: 100vh;
    }
    
    .deck { width: 100vw; height: 100vh; position: relative; }
    
    .slide {
      position: absolute; inset: 0;
      display: flex; flex-direction: column;
      justify-content: center; align-items: center;
      padding: 4rem 6rem;
      opacity: 0; pointer-events: none;
      transition: opacity .4s ease;
    }
    .slide.active { opacity: 1; pointer-events: all; }
    
    /* ===== 封面幻灯片 ===== */
    .slide-cover {
      background: radial-gradient(ellipse at 30% 50%, #16213e 0%, #0f0f1a 60%);
      text-align: center;
    }
    .cover-ep {
      font-size: .9rem; letter-spacing: .15em; color: #7c3aed;
      text-transform: uppercase; margin-bottom: 1.5rem;
    }
    .cover-title {
      font-size: clamp(2rem, 5vw, 3.5rem);
      font-weight: 900; color: #f1f5f9;
      line-height: 1.2; margin-bottom: 1.5rem;
    }
    .cover-subtitle {
      font-size: 1.1rem; color: #64748b;
      max-width: 600px; line-height: 1.7;
      margin-bottom: 2rem;
    }
    .cover-meta {
      display: flex; gap: 2rem; justify-content: center;
      font-size: .85rem; color: #475569;
    }
    
    /* ===== 内容幻灯片 ===== */
    .slide-content {
      background: #0f0f1a;
      align-items: flex-start;
    }
    .slide-label {
      font-size: .75rem; color: #7c3aed; font-weight: 700;
      letter-spacing: .12em; text-transform: uppercase;
      margin-bottom: 1rem;
    }
    .slide-heading {
      font-size: clamp(1.5rem, 3vw, 2.2rem);
      font-weight: 800; color: #f1f5f9;
      line-height: 1.3; margin-bottom: 1.5rem;
      max-width: 700px;
    }
    .slide-body {
      font-size: 1rem; color: #94a3b8;
      line-height: 1.8; max-width: 720px;
    }
    .point-list { list-style: none; }
    .point-list li {
      padding: .6rem 0; border-bottom: 1px solid #1e1e3a;
      display: flex; gap: .75rem; align-items: flex-start;
      color: #cbd5e1;
    }
    .point-list li::before {
      content: '▸'; color: #7c3aed; flex-shrink: 0; margin-top: .1rem;
    }
    .highlight-box {
      background: rgba(124,58,237,.1);
      border: 1px solid rgba(124,58,237,.3);
      border-radius: 10px; padding: 1rem 1.5rem;
      margin-top: 1.25rem; font-size: .95rem; color: #a78bfa;
    }
    
    /* ===== 金句幻灯片 ===== */
    .slide-quote {
      background: linear-gradient(135deg, #0f0f1a, #1a1a2e);
      text-align: center;
    }
    .big-quote {
      font-size: clamp(1.2rem, 2.5vw, 1.8rem);
      color: #e2e8f0; font-style: italic; line-height: 1.7;
      max-width: 760px;
    }
    .big-quote::before { content: '"'; color: #7c3aed; font-size: 3rem;
                         line-height: .5; vertical-align: -.3em; margin-right: .1em; }
    .big-quote::after  { content: '"'; color: #7c3aed; font-size: 3rem;
                         line-height: .5; vertical-align: -.3em; margin-left: .1em; }
    .quote-attribution {
      margin-top: 1.5rem; font-size: .9rem; color: #64748b;
    }
    
    /* ===== 导航控件 ===== */
    .nav-controls {
      position: fixed; bottom: 2rem; right: 2rem;
      display: flex; gap: .5rem; z-index: 1000;
    }
    .nav-btn {
      width: 44px; height: 44px; border-radius: 50%;
      background: rgba(124,58,237,.2);
      border: 1px solid rgba(124,58,237,.4);
      color: #a78bfa; font-size: 1.1rem; cursor: pointer;
      display: flex; align-items: center; justify-content: center;
      transition: all .2s;
    }
    .nav-btn:hover { background: rgba(124,58,237,.4); }
    .nav-btn:disabled { opacity: .3; cursor: default; }
    
    /* ===== 进度条 ===== */
    .progress {
      position: fixed; bottom: 0; left: 0; right: 0;
      height: 3px; background: #1e1e3a;
    }
    .progress-fill {
      height: 100%; background: #7c3aed;
      transition: width .3s ease;
    }
    
    /* ===== 幻灯片编号 ===== */
    .slide-counter {
      position: fixed; bottom: 2rem; left: 50%;
      transform: translateX(-50%);
      font-size: .8rem; color: #475569;
    }
  </style>
</head>
<body>

<div class="deck" id="deck">

  <!-- Slide 1: 封面 -->
  <div class="slide slide-cover active">
    <div class="cover-ep">🎙️ [播客名] · EP[XX]</div>
    <div class="cover-title">[本期标题]</div>
    <div class="cover-subtitle">[副标题/核心问题]</div>
    <div class="cover-meta">
      <span>📅 [日期]</span>
      <span>⏱️ [时长]</span>
      <span>👤 [嘉宾]</span>
    </div>
  </div>

  <!-- Slide 2: 本期提要 -->
  <div class="slide slide-content">
    <div class="slide-label">本期提要</div>
    <div class="slide-heading">我们在讨论什么？</div>
    <ul class="point-list">
      <li>[核心问题1]</li>
      <li>[核心问题2]</li>
      <li>[核心问题3]</li>
    </ul>
  </div>

  <!-- Slides 3-N: 核心论点（每个论点独立一页） -->
  <!-- 
  <div class="slide slide-content">
    <div class="slide-label">论点 1 · [领域标签]</div>
    <div class="slide-heading">[论点标题]</div>
    <div class="slide-body">
      <p>[论点详细说明]</p>
      <ul class="point-list">
        <li>[支撑证据1]</li>
        <li>[支撑证据2]</li>
      </ul>
      <div class="highlight-box">💡 洞察：[深层含义]</div>
    </div>
  </div>
  -->

  <!-- 金句页 -->
  <!-- 
  <div class="slide slide-quote">
    <div class="big-quote">[金句文本]</div>
    <div class="quote-attribution">— [说话人] · EP[XX]</div>
  </div>
  -->

</div>

<!-- 导航 -->
<div class="nav-controls">
  <button class="nav-btn" id="prevBtn" onclick="changeSlide(-1)" disabled>←</button>
  <button class="nav-btn" id="nextBtn" onclick="changeSlide(1)">→</button>
</div>

<div class="progress"><div class="progress-fill" id="progressFill"></div></div>
<div class="slide-counter" id="counter">1 / [N]</div>

<script>
  let current = 0;
  const slides = document.querySelectorAll('.slide');
  const total = slides.length;
  
  function updateUI() {
    slides.forEach((s, i) => s.classList.toggle('active', i === current));
    document.getElementById('prevBtn').disabled = current === 0;
    document.getElementById('nextBtn').disabled = current === total - 1;
    document.getElementById('counter').textContent = `${current + 1} / ${total}`;
    document.getElementById('progressFill').style.width = 
      `${((current + 1) / total) * 100}%`;
  }
  
  function changeSlide(dir) {
    current = Math.max(0, Math.min(total - 1, current + dir));
    updateUI();
  }
  
  document.addEventListener('keydown', e => {
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') changeSlide(1);
    if (e.key === 'ArrowLeft'  || e.key === 'ArrowUp')   changeSlide(-1);
  });
  
  updateUI();
</script>

</body>
</html>
```

## 填充规则

1. 每个核心论点单独一页，不要在一页塞超过3个要点
2. 金句页只放1条金句，字要大，冲击感强
3. 最后一页放「行动清单」或「延伸资源」
4. 封面背景可用渐变色块体现播客主题色