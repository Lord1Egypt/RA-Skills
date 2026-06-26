# Poster Style Reference Guide

## Modern Gradient Poster

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Modern Poster</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    body {
      min-height: 100vh;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
      font-family: 'Inter', system-ui, sans-serif;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 2rem;
    }
    
    .poster {
      background: rgba(255,255,255,0.1);
      backdrop-filter: blur(20px);
      border-radius: 24px;
      padding: 3rem;
      max-width: 600px;
      width: 100%;
      text-align: center;
      color: white;
      box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
    }
    
    .badge {
      background: rgba(255,255,255,0.2);
      padding: 0.5rem 1rem;
      border-radius: 50px;
      font-size: 0.875rem;
      margin-bottom: 1.5rem;
      display: inline-block;
    }
    
    .title {
      font-size: 3rem;
      font-weight: 800;
      line-height: 1.1;
      margin-bottom: 1rem;
    }
    
    .subtitle {
      font-size: 1.25rem;
      opacity: 0.9;
      margin-bottom: 2rem;
    }
    
    .cta {
      background: white;
      color: #6366f1;
      padding: 1rem 2rem;
      border-radius: 50px;
      font-weight: 600;
      display: inline-block;
      text-decoration: none;
    }
  </style>
</head>
<body>
  <div class="poster">
    <div class="badge">限时活动</div>
    <h1 class="title">创造无限可能</h1>
    <p class="subtitle">探索设计的边界，释放创意的力量</p>
    <a href="#" class="cta">立即参与</a>
  </div>
</body>
</html>
```

## Chinese Traditional Style

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>中国风海报</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700;900&display=swap" rel="stylesheet">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    body {
      min-height: 100vh;
      background: linear-gradient(180deg, #faf8f5 0%, #f5f0e8 100%);
      font-family: 'Noto Serif SC', serif;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 2rem;
    }
    
    .poster {
      max-width: 500px;
      width: 100%;
      background: #fffef9;
      border: 3px solid #8b0000;
      padding: 3rem;
      position: relative;
    }
    
    .poster::before,
    .poster::after {
      content: '';
      position: absolute;
      width: 20px;
      height: 20px;
      border: 2px solid #8b0000;
    }
    
    .poster::before { top: 10px; left: 10px; border-right: none; border-bottom: none; }
    .poster::after { bottom: 10px; right: 10px; border-left: none; border-top: none; }
    
    .decoration {
      text-align: center;
      font-size: 2rem;
      color: #8b0000;
      margin-bottom: 1rem;
    }
    
    .title {
      font-size: 2.5rem;
      font-weight: 900;
      color: #2c1810;
      text-align: center;
      writing-mode: vertical-rl;
      margin: 0 auto 2rem;
      letter-spacing: 0.5em;
      line-height: 2;
    }
    
    .subtitle {
      font-size: 1.125rem;
      color: #5c4033;
      text-align: center;
      line-height: 2;
    }
    
    .seal {
      width: 60px;
      height: 60px;
      background: #8b0000;
      color: #ffd700;
      border-radius: 4px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.5rem;
      margin: 2rem auto 0;
    }
  </style>
</head>
<body>
  <div class="poster">
    <div class="decoration">◆ ◇ ◆</div>
    <h1 class="title">春风雅集</h1>
    <p class="subtitle">
      传统文化艺术展<br>
      二〇二六年 · 春
    </p>
    <div class="seal">印</div>
  </div>
</body>
</html>
```

## Minimalist Style

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Minimalist Poster</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    body {
      min-height: 100vh;
      background: #fafafa;
      font-family: system-ui, -apple-system, sans-serif;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 2rem;
    }
    
    .poster {
      max-width: 500px;
      width: 100%;
      text-align: center;
    }
    
    .line {
      width: 60px;
      height: 1px;
      background: #000;
      margin: 0 auto 2rem;
    }
    
    .title {
      font-size: 4rem;
      font-weight: 300;
      letter-spacing: -0.02em;
      margin-bottom: 1rem;
      color: #111;
    }
    
    .subtitle {
      font-size: 1rem;
      color: #666;
      margin-bottom: 3rem;
      font-weight: 300;
    }
    
    .details {
      font-size: 0.875rem;
      color: #999;
      line-height: 2;
    }
  </style>
</head>
<body>
  <div class="poster">
    <div class="line"></div>
    <h1 class="title">Less,<br>but better.</h1>
    <p class="subtitle">Design Exhibition 2026</p>
    <div class="details">
      March 15 - April 30<br>
      Gallery One, Shanghai
    </div>
  </div>
</body>
</html>
```

## Tech/Digital Style

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Tech Poster</title>
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    body {
      min-height: 100vh;
      background: #0a0a0f;
      font-family: 'Orbitron', monospace;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 2rem;
      overflow: hidden;
    }
    
    .grid-bg {
      position: fixed;
      inset: 0;
      background-image: 
        linear-gradient(rgba(0,255,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,255,0.03) 1px, transparent 1px);
      background-size: 50px 50px;
    }
    
    .poster {
      max-width: 600px;
      width: 100%;
      text-align: center;
      position: relative;
      z-index: 1;
    }
    
    .glow-text {
      font-size: 3.5rem;
      font-weight: 900;
      background: linear-gradient(90deg, #00ffff, #ff00ff, #00ffff);
      background-size: 200% auto;
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      animation: glow 3s linear infinite;
      text-shadow: 0 0 40px rgba(0,255,255,0.5);
    }
    
    @keyframes glow {
      to { background-position: 200% center; }
    }
    
    .subtitle {
      color: #00ffff;
      font-size: 1rem;
      margin: 1.5rem 0;
      letter-spacing: 0.3em;
      text-transform: uppercase;
    }
    
    .date {
      color: rgba(255,255,255,0.5);
      font-size: 0.875rem;
      border: 1px solid rgba(0,255,255,0.3);
      display: inline-block;
      padding: 0.75rem 2rem;
    }
  </style>
</head>
<body>
  <div class="grid-bg"></div>
  <div class="poster">
    <h1 class="glow-text">未来已来</h1>
    <p class="subtitle">AI Summit 2026</p>
    <div class="date">2026.06.15 | 北京</div>
  </div>
</body>
</html>
```

## Luxury Style

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Luxury Poster</title>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    body {
      min-height: 100vh;
      background: #000;
      font-family: 'Playfair Display', serif;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 2rem;
    }
    
    .poster {
      max-width: 500px;
      width: 100%;
      background: linear-gradient(180deg, #1a1a1a 0%, #0a0a0a 100%);
      border: 1px solid rgba(212,175,55,0.3);
      padding: 4rem 3rem;
      text-align: center;
    }
    
    .gold-line {
      width: 80px;
      height: 2px;
      background: linear-gradient(90deg, transparent, #d4af37, transparent);
      margin: 0 auto 2rem;
    }
    
    .brand {
      color: #d4af37;
      font-size: 0.75rem;
      letter-spacing: 0.5em;
      text-transform: uppercase;
      margin-bottom: 2rem;
    }
    
    .title {
      color: #fff;
      font-size: 2.5rem;
      font-weight: 400;
      line-height: 1.3;
      margin-bottom: 1rem;
    }
    
    .title em {
      color: #d4af37;
      font-style: italic;
    }
    
    .subtitle {
      color: rgba(255,255,255,0.6);
      font-size: 1rem;
      margin-bottom: 2rem;
    }
    
    .cta {
      color: #d4af37;
      border: 1px solid #d4af37;
      padding: 1rem 2.5rem;
      font-size: 0.75rem;
      letter-spacing: 0.2em;
      text-transform: uppercase;
      display: inline-block;
      text-decoration: none;
      transition: all 0.3s;
    }
    
    .cta:hover {
      background: #d4af37;
      color: #000;
    }
  </style>
</head>
<body>
  <div class="poster">
    <div class="gold-line"></div>
    <div class="brand">Exclusive Collection</div>
    <h1 class="title">The Art of<br><em>Elegance</em></h1>
    <p class="subtitle">A celebration of timeless beauty</p>
    <a href="#" class="cta">Discover More</a>
  </div>
</body>
</html>
```

## Nature/Organic Style

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>自然风格海报</title>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;500;700&display=swap" rel="stylesheet">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    body {
      min-height: 100vh;
      background: linear-gradient(180deg, #e8f5e9 0%, #c8e6c9 100%);
      font-family: 'Noto Sans SC', sans-serif;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 2rem;
    }
    
    .poster {
      max-width: 500px;
      width: 100%;
      background: rgba(255,255,255,0.9);
      border-radius: 20px;
      padding: 3rem;
      text-align: center;
      box-shadow: 0 20px 60px rgba(34,139,34,0.15);
    }
    
    .leaf {
      font-size: 3rem;
      margin-bottom: 1rem;
    }
    
    .title {
      font-size: 2.5rem;
      font-weight: 700;
      color: #2e7d32;
      margin-bottom: 1rem;
    }
    
    .subtitle {
      font-size: 1.125rem;
      color: #558b2f;
      font-weight: 300;
      margin-bottom: 2rem;
      line-height: 1.8;
    }
    
    .info {
      background: #f1f8e9;
      padding: 1.5rem;
      border-radius: 12px;
      color: #33691e;
    }
    
    .info-item {
      margin: 0.5rem 0;
      font-size: 0.9rem;
    }
  </style>
</head>
<body>
  <div class="poster">
    <div class="leaf">🌿</div>
    <h1 class="title">绿色生活节</h1>
    <p class="subtitle">
      回归自然，拥抱健康<br>
      共同创造可持续的未来
    </p>
    <div class="info">
      <div class="info-item">📅 2026年4月22日</div>
      <div class="info-item">📍 城市森林公园</div>
      <div class="info-item">🎫 免费入场</div>
    </div>
  </div>
</body>
</html>
```

## Responsive Breakpoints

```css
/* Mobile First Approach */
.poster {
  padding: 1.5rem;
  font-size: 16px;
}

.title {
  font-size: 2rem;
}

/* Tablet */
@media (min-width: 768px) {
  .poster {
    padding: 2.5rem;
  }
  .title {
    font-size: 3rem;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .poster {
    padding: 3rem;
  }
  .title {
    font-size: 4rem;
  }
}

/* Print */
@media print {
  body {
    background: white;
  }
  .poster {
    box-shadow: none;
    page-break-inside: avoid;
  }
}
```

## Chinese Typography Combinations

```css
/* Classical Chinese */
.font-classical {
  font-family: "Noto Serif SC", "STSong", "SimSun", serif;
}

/* Modern Chinese */
.font-modern {
  font-family: "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
}

/* Creative Chinese */
.font-creative {
  font-family: "ZCOOL XiaoWei", "ZCOOL QingKe HuangYou", cursive;
}

/* Handwriting Chinese */
.font-handwriting {
  font-family: "Ma Shan Zheng", "Liu Jian Mao Cao", cursive;
}
```

## English Typography Combinations

```css
/* Classic Serif */
.font-classic {
  font-family: "Playfair Display", "Georgia", serif;
}

/* Modern Sans */
.font-sans {
  font-family: "Inter", "Helvetica Neue", sans-serif;
}

/* Display Bold */
.font-display {
  font-family: "Bebas Neue", "Oswald", sans-serif;
}

/* Elegant Script */
.font-script {
  font-family: "Cormorant Garamond", "GFS Didot", serif;
}
```
