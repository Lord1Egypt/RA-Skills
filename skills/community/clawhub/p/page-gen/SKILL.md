---
name: page-gen
description: 为文学作品（小说、电影、动漫、游戏等）生成精美的响应式单页 HTML 介绍和解析页面。当用户要求"介绍XX作品"、"做一个XX的介绍页面"、"生成作品解析页面"、"创建作品展示页"、"帮我做个XX的网页"时触发。支持主题配色提取、交互组件、多内容分区展示。
---

# 文学作品页面生成器

为文学作品生成自包含的单页 HTML 展示页面，包含主题配色、响应式布局和交互功能。

## 设计流程

### 1. 提取主题配色

根据作品类型选择配色方案（以下为参考建议，实际配色需根据作品具体氛围、用户偏好或品牌要求灵活调整）：

| 作品类型 | 建议配色 |
|---------|----------|
| 武侠/修仙 | 金色 (#d4a853) + 翠绿 (#2dd4a8) + 深色 (#0a0e1a) |
| 奇幻/玄幻 | 冰蓝 (#4a9eff) + 深蓝 (#0a1628) |
| 历史/权谋 | 金色 (#d4a853) + 朱红 (#c0392b) + 深色 (#0f1419) |
| 神话/志怪 | 紫色 (#8e44ad) + 粉色 (#f8cdda) + 青色 (#a8edea) |
| 家庭/情感 | 暖棕 (#8B4513) + 金色 (#DAA520) + 米白 (#FFFAF0) |
| 科幻/赛博 | 霓虹青 (#00f5ff) + 深色 (#0a0a0a) + 紫罗兰 (#a78bfa) |
| 都市/现代 | 纯白 + 蓝色 (#3b82f6) + 灰色 |

**重要提示**：上表配色仅为参考建议，实际生成时应根据以下因素灵活调整：
- 作品的具体氛围和情感基调
- 用户明确指定的配色偏好
- 作品中标志性的视觉元素（如封面、海报主色调）
- 品牌或官方配色（如有）
- 可访问性要求（对比度、色盲友好等）

### 2. 配置字体

使用 Google Fonts 国内镜像：

```html
<link rel="preconnect" href="https://fonts.loli.net">
<link href="https://fonts.loli.net/css2?family=Noto+Serif+SC:wght@400;600;700;900&family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
```

- **标题字体**: `'Noto Serif SC', serif` — 优雅文艺
- **正文字体**: `'Noto Sans SC', sans-serif` — 清晰易读

### 3. 响应式断点

- `768px` — 平板：单列布局，缩小字体
- `480px` — 手机：紧凑布局，减少内边距

## 页面结构

### 必需区块（按顺序）

1. **Hero 区** — 全视口，作品标题 + 副标题 + 关键数据 + 行动按钮
2. **粘性导航** — 区块链接 + 滚动进度指示器
3. **作品简介** — 概览卡片 + 标签
4. **作者介绍** — 作者简介 + 头像占位
5. **世界观/设定** — 世界观卡片（小说）或 创作背景（非虚构）
6. **主要人物** — 角色卡片网格
7. **情节/章节** — 时间线或卷册卡片
8. **经典语录** — 引用卡片
9. **评析/价值** — 分析卡片
10. **页脚** — 简单页脚

### 可选区块（根据内容选择）

- **种族/阵营** — 阵营卡片（奇幻作品）
- **武功/法宝** — 能力体系卡片（武侠/修仙）
- **战斗名场面** — 战斗场景卡片（动作作品）
- **人物关系图** — 关系图（复杂角色群）
- **时间线** — 历史时间线（历史作品）
- **幕后故事** — 幕后花絮（影视作品）
- **社会影响** — 文化影响（经典作品）

## 组件模板

### Hero 区

```html
<section class="hero">
    <div class="hero-badge">
        <span class="hero-badge-dot"></span>
        {分类标签}
    </div>
    <h1 class="hero-title">
        <span class="char-gold">{作品名}</span>
    </h1>
    <p class="hero-subtitle">{一句话概括}</p>
    <blockquote class="hero-quote">"{经典语录}"</blockquote>
    <div class="hero-stats">
        <div class="hero-stat">
            <div class="hero-stat-value">{数值}</div>
            <div class="hero-stat-label">{标签}</div>
        </div>
    </div>
    <a href="#section1" class="hero-cta">
        开始探索
        <span class="hero-cta-arrow">→</span>
    </a>
</section>
```

### 导航栏

```html
<nav class="nav" id="nav">
    <div class="nav-inner">
        <div class="nav-brand">{作品名}</div>
        <ul class="nav-links">
            <li><a href="#intro" class="nav-link active">作品简介</a></li>
            <li><a href="#author" class="nav-link">作者介绍</a></li>
        </ul>
        <div class="nav-right">
            <div class="nav-progress">
                <svg class="nav-progress-ring" viewBox="0 0 36 36">
                    <circle class="bg" cx="18" cy="18" r="15" />
                    <circle class="fill" id="progressRing" cx="18" cy="18" r="15"
                        stroke-dasharray="94.25" stroke-dashoffset="94.25" />
                </svg>
                <span id="progressText">0%</span>
            </div>
        </div>
    </div>
</nav>
```

### 卡片组件

```html
<div class="card">
    <div class="card-icon">📚</div>
    <h3 class="card-title">{标题}</h3>
    <p class="card-text">{描述}</p>
    <div class="card-tags">
        <span class="tag">{标签1}</span>
        <span class="tag jade">{标签2}</span>
    </div>
</div>
```

### 角色卡片

```html
<div class="character-card">
    <div class="character-avatar">👤</div>
    <div class="character-name">{角色名}</div>
    <div class="character-role">{身份}</div>
    <div class="character-desc">{描述}</div>
</div>
```

### 时间线组件

```html
<div class="timeline">
    <div class="timeline-item">
        <div class="timeline-dot"></div>
        <div class="timeline-year">{时间}</div>
        <div class="timeline-title">{事件}</div>
        <div class="timeline-desc">{描述}</div>
    </div>
</div>
```

### 引用卡片

```html
<div class="quote-card">
    <p class="quote-text">"{语录内容}"</p>
    <p class="quote-source">—— <strong>{出处}</strong></p>
</div>
```

## 交互功能

### 滚动进度条

```javascript
const progressBar = document.getElementById('progressBar');
window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = (scrollTop / docHeight) * 100;
    progressBar.style.width = progress + '%';
});
```

### 导航激活状态

```javascript
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-link');

window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop - 100;
        if (window.scrollY >= sectionTop) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === '#' + current) {
            link.classList.add('active');
        }
    });
});
```

### 返回顶部按钮

```html
<button class="back-to-top" id="backToTop" aria-label="返回顶部">↑</button>

<script>
const backToTop = document.getElementById('backToTop');
window.addEventListener('scroll', () => {
    backToTop.classList.toggle('visible', window.scrollY > 300);
});
backToTop.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});
</script>
```

### 滚动淡入动画

```css
.fade-in {
    opacity: 0;
    transform: translateY(20px);
    transition: opacity 0.6s var(--ease-out), transform 0.6s var(--ease-out);
}

.fade-in.visible {
    opacity: 1;
    transform: translateY(0);
}
```

```javascript
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));
```

## CSS 设计令牌模板

以下为示例模板，实际值需根据作品主题和配色方案调整：

```css
:root {
    /* 颜色 - 根据作品主题调整（以下为示例值） */
    --bg-primary: #0a0e1a;
    --bg-secondary: #111827;
    --bg-card: rgba(15, 23, 42, 0.85);
    --bg-card-hover: rgba(30, 41, 59, 0.95);

    --gold-primary: #d4a853;
    --gold-light: #f0d78c;
    --gold-glow: rgba(212, 168, 83, 0.4);
    --gold-subtle: rgba(212, 168, 83, 0.1);

    --accent: #2dd4a8; /* 按主题更换 */
    --accent-glow: rgba(45, 212, 168, 0.3);

    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;

    --border-subtle: rgba(212, 168, 83, 0.15);
    --border-active: rgba(212, 168, 83, 0.5);

    /* 字体 */
    --font-display: 'Noto Serif SC', serif;
    --font-body: 'Noto Sans SC', sans-serif;

    /* 间距 */
    --space-1: 4px;
    --space-2: 8px;
    --space-3: 12px;
    --space-4: 16px;
    --space-5: 20px;
    --space-6: 24px;
    --space-8: 32px;
    --space-10: 40px;
    --space-12: 48px;
    --space-16: 64px;

    /* 圆角 */
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 20px;
    --radius-xl: 28px;

    /* 阴影 */
    --shadow-card: 0 4px 24px rgba(0, 0, 0, 0.4);
    --shadow-hover: 0 12px 48px rgba(212, 168, 83, 0.25);

    /* 过渡 */
    --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
    --duration-normal: 0.3s;
}
```

## 内容指南

### Hero 区数据（选 3-5 项）

| 作品类型 | 推荐数据 |
|---------|----------|
| 小说 | 总字数、章节数、出版年份、销量 |
| 电影 | 豆瓣评分、票房、片长、上映年份 |
| 动漫 | 集数、评分、首播年份、制作公司 |
| 历史 | 跨度年数、册数、覆盖朝代 |

### 角色卡片（6-12 个角色）

- 包含主角、反派和关键配角
- 使用 emoji 作为头像占位符
- 描述保持简洁（2-3 句）

### 语录（4-8 条）

- 选择标志性、令人难忘的台词
- 标注出处角色或旁白
- 混合哲理性和情感性语录

### 标签分类

- 类型标签：历史、奇幻、武侠、都市
- 主题标签：友情、成长、权谋、爱情
- 风格标签：幽默、热血、虐心、治愈

## 输出要求

生成单个自包含 HTML 文件：

- 所有 CSS 在 `<style>` 标签内
- 所有 JavaScript 在 `<script>` 标签内
- 仅依赖 Google Fonts CDN（使用国内镜像）
- 响应式设计
- 语义化 HTML 结构
- 无障碍访问（正确使用标题层级、alt 属性、ARIA 标签）

## 质量检查清单

- [ ] 主题配色符合作品氛围（如用户未指定，参考建议配色方案）
- [ ] 所有区块有内容（无空占位符）
- [ ] 移动端响应式正常（测试 375px 宽度）
- [ ] 导航功能正常
- [ ] 动画流畅（60fps）
- [ ] 字体正确加载（有备用字体）
- [ ] 文本可读性好（对比度足够）
- [ ] 卡片有悬停效果
- [ ] 返回顶部按钮可用
- [ ] 进度指示器可用

## 使用示例

用户输入：
```
帮我做一个《三体》的介绍页面
```

提取信息：
- 标题：三体
- 作者：刘慈欣
- 类型：科幻小说
- 主题色：深空蓝 + 红色（文革时代）
- 关键数据：三部曲、88万字、雨果奖
- 角色：叶文洁、罗辑、程心、章北海等
- 核心概念：黑暗森林法则、降维打击、面壁者
- 经典语录："给岁月以文明，而不是给文明以岁月"
