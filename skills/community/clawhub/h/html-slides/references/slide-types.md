# Slide Types

Every presentation uses four slide types. Each slide is a `<section class="slide [type-class]">` with `data-title` and `data-group` attributes used by the JS sidebar builder.

**Brand-aware elements:** Logos, accent colors, and section backgrounds all come from CSS custom properties. The same HTML works across all brand presets — only the `:root` variables change.

**Logo rule for Shopee/Sea preset:** Both Shopee logo AND SeaMoney logo MUST appear on cover slides, section dividers, and content slide headers. Use class names `.shopee` and `.seamoney` — the CSS `content` property embeds the actual logo images via base64 data URIs. For Neutral preset, omit logo elements entirely.

---

## 1. Cover Slide

First slide. Centered layout with optional logos, title, accent bar, subtitle, meta.

### With Logos — Shopee/Sea (BOTH logos MANDATORY)

```html
<section class="slide cover-slide" data-title="Title" data-group="Overview">
    <div class="slide-content">
        <div class="cover-logos reveal">
            <img src="data:," class="brand-logo shopee" alt="Shopee">
            <img src="data:," class="brand-logo seamoney" alt="SeaMoney">
        </div>
        <span class="cover-title reveal">Presentation Title</span>
        <div class="cover-accent-bar reveal"></div>
        <span class="cover-subtitle reveal">Subtitle or Description</span>
        <div class="cover-meta reveal">
            <span>Team Name</span>
            <span>2026-04-10</span>
        </div>
    </div>
    <div class="slide-footer">
        <div class="footer-left"></div>
        <div class="footer-center">Private &amp; Confidential</div>
        <div class="footer-right page-number"></div>
    </div>
</section>
```

### With Logos — Custom Brand

```html
<!-- Use brand-specific class names; CSS content: url(data:...) will embed them -->
<div class="cover-logos reveal">
    <img src="data:," class="brand-logo custom-primary" alt="Brand">
    <img src="data:," class="brand-logo custom-secondary" alt="Brand 2">  <!-- optional if only one logo -->
</div>
```

### Without Logos (Neutral preset)

```html
<section class="slide cover-slide" data-title="Title" data-group="Overview">
    <div class="slide-content">
        <span class="cover-title reveal">Presentation Title</span>
        <div class="cover-accent-bar reveal"></div>
        <span class="cover-subtitle reveal">Subtitle or Description</span>
        <div class="cover-meta reveal">
            <span>Team Name</span>
            <span>2026-04-10</span>
        </div>
    </div>
    <div class="slide-footer">
        <div class="footer-left"></div>
        <div class="footer-center">Private &amp; Confidential</div>
        <div class="footer-right page-number"></div>
    </div>
</section>
```

### Cover CSS

```css
.cover-slide { background: var(--bg-primary); }
.cover-slide .slide-content {
    align-items: center; text-align: center;
    gap: clamp(0.8rem, 2vh, 1.8rem);
}
.cover-logos { display: flex; align-items: center; gap: clamp(8px, 1.2vw, 16px); }
.cover-logos img { height: clamp(35px, 5.5vh, 62px); }
.cover-title {
    font-family: var(--font-display); font-size: var(--title-size);
    font-weight: 900; color: var(--accent); line-height: 1.1;
}
.cover-accent-bar {
    width: 100%; max-width: clamp(200px, 40vw, 500px);
    height: 3px; background: var(--accent);
}
.cover-subtitle {
    font-family: var(--font-body); font-size: var(--h3-size);
    color: var(--text-secondary); font-weight: 400;
}
.cover-meta {
    font-family: var(--font-body); font-size: var(--small-size);
    color: var(--text-muted); display: flex; gap: clamp(12px, 2vw, 24px);
}
```

---

## 2. Section Divider Slide

Colored background (uses `--section-bg`), used to transition between major topics. Large ghost section number.

```html
<section class="slide section-slide" data-title="Section Name" data-group="Section Group">
    <div class="slide-content">
        <!-- Shopee/Sea: BOTH logos MANDATORY; Neutral: omit this div -->
        <div class="section-logos reveal">
            <img src="data:," class="brand-logo shopee" alt="Shopee">
            <img src="data:," class="brand-logo seamoney" alt="SeaMoney">
        </div>
        <div class="section-accent-bar reveal"></div>
        <span class="section-title reveal">Section Title</span>
        <p class="subtitle reveal">One-line description of what this section covers.</p>
        <span class="section-number">01</span>
    </div>
    <div class="slide-footer">
        <div class="footer-left"></div>
        <div class="footer-center">Private &amp; Confidential</div>
        <div class="footer-right page-number"></div>
    </div>
</section>
```

### Section Divider CSS

```css
.section-slide { background: var(--section-bg); }
.section-slide .slide-content { align-items: flex-start; gap: clamp(0.5rem, 1.5vh, 1.2rem); }
.section-logos img { height: clamp(28px, 4vh, 45px); filter: brightness(0) invert(1); opacity: 0.9; }
.section-accent-bar { width: clamp(60px, 10vw, 120px); height: 3px; background: var(--accent); }
.section-title {
    font-family: var(--font-display); font-size: var(--h2-size);
    font-weight: 900; color: var(--text-on-accent); line-height: 1.15;
}
.section-slide .subtitle {
    font-family: var(--font-body); font-size: var(--body-size);
    color: rgba(255, 255, 255, 0.7); max-width: 60%;
}
.section-number {
    font-family: var(--font-display); font-size: clamp(3rem, 8vw, 7rem);
    font-weight: 900; color: rgba(255, 255, 255, 0.08);
    position: absolute; right: var(--slide-padding); top: 50%; transform: translateY(-50%);
}
.section-slide .slide-footer .footer-center,
.section-slide .slide-footer .page-current { color: rgba(255, 255, 255, 0.4); }
.section-slide .slide-footer .page-separator,
.section-slide .slide-footer .page-total { color: rgba(255, 255, 255, 0.25); }
```

---

## 3. Content Slide

The main information carrier. Header bar (optional logos + section title + accent line) + body area for components.

```html
<section class="slide content-slide" data-title="Slide Title" data-group="Group Name">
    <div class="slide-header">
        <!-- Shopee/Sea: BOTH logos MANDATORY; Neutral: drop .header-logos div -->
        <div class="header-logos">
            <img src="data:," class="brand-logo shopee" alt="Shopee">
            <img src="data:," class="brand-logo seamoney" alt="SeaMoney">
        </div>
        <div class="header-title-block">
            <span class="header-title">Section Title</span>
            <div class="header-line"></div>
        </div>
    </div>
    <div class="slide-content">
        <h2 class="reveal">Main insight or headline for this slide.</h2>
        <p class="reveal">Supporting context — keep to 2-3 sentences max.</p>
        <!-- INSERT COMPONENT(S) HERE with class="reveal" -->
    </div>
    <div class="slide-footer">
        <div class="footer-left"></div>
        <div class="footer-center">Private &amp; Confidential</div>
        <div class="footer-right page-number"></div>
    </div>
</section>
```

For **Neutral preset** without logos, drop the `.header-logos` div:

```html
<div class="slide-header">
    <div class="header-title-block">
        <span class="header-title">Section Title</span>
        <div class="header-line"></div>
    </div>
</div>
```

### Content Slide CSS

```css
.slide-header {
    display: flex; align-items: center;
    padding: var(--slide-padding); padding-bottom: 0;
    padding-left: calc((var(--sidebar-width) + clamp(1.5rem, 4vw, 4rem)) / var(--zoom-level, 1));
    gap: clamp(10px, 1.5vw, 20px);
}
.header-logos img { height: clamp(31px, 4.4vh, 48px); }
.header-title {
    font-family: var(--font-display); font-size: var(--h2-size);
    font-weight: 700; color: var(--accent);
}
.header-line { height: 3px; background: var(--accent); width: 100%; }
.content-slide .slide-content {
    justify-content: flex-start;
    padding-top: clamp(0.5rem, 1.5vh, 1.5rem);
    gap: var(--content-gap);
}
.content-slide p { max-width: 85%; }
```

---

## 4. Closing Slide

Last slide. Variant of cover — can use "Thank You", "Next Steps", "Q&A", etc.

```html
<section class="slide cover-slide closing-slide" data-title="Thank You" data-group="Closing">
    <div class="slide-content">
        <!-- Shopee/Sea: include both logos; Neutral: omit -->
        <div class="cover-logos reveal">
            <img src="data:," class="brand-logo shopee" alt="Shopee">
            <img src="data:," class="brand-logo seamoney" alt="SeaMoney">
        </div>
        <span class="cover-title reveal">Thank You</span>
        <div class="cover-accent-bar reveal"></div>
        <span class="cover-subtitle reveal">Presentation Title · Date</span>
        <div class="cover-meta reveal">
            <span>Questions &amp; Discussion</span>
            <span>Team Name</span>
        </div>
    </div>
    <div class="slide-footer">
        <div class="footer-left"></div>
        <div class="footer-center">Private &amp; Confidential</div>
        <div class="footer-right page-number"></div>
    </div>
</section>
```

---

## Footer (Every Slide)

Every slide MUST include this footer. Page numbers are populated by JS.

```css
.slide-footer {
    display: flex; justify-content: space-between; align-items: center;
    padding: clamp(8px, 1.5vh, 16px) var(--slide-padding);
    padding-left: calc((var(--sidebar-width) + clamp(1.5rem, 4vw, 4rem)) / var(--zoom-level, 1));
    flex-shrink: 0;
}
.page-current { font-size: 1.4vw; font-weight: 700; color: var(--text-primary); }
.page-separator { font-size: 1vw; color: var(--text-muted); margin: 0 0.35em; }
.page-total { font-size: 1vw; color: var(--text-muted); }
```
