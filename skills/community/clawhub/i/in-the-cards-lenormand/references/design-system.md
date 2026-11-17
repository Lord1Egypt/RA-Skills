# Design System — In the Cards v3.3

Shared design tokens, typography, fonts, and card reference used across all product templates.

## Global Design Constants

```css
/* -- Kami Lenormand Theme -- */
--parchment:   #f5f4ed;   /* page background */
--near-black:  #141413;   /* body text */
--dark-warm:   #3d3d3a;   /* secondary text */
--stone:       #6b6a64;   /* meta, page numbers */
--brand:       #1B365D;   /* ink-blue accent */
--border:      #e8e6dc;   /* page borders */
--border-soft: #e5e3d8;   /* soft borders */

/* Card polarity colors */
--positive:    #E1F5EE;   /* soft teal fill */
--positive-stroke: #5DCAA5;
--negative:    #FAECE7;   /* soft terracotta fill */
--negative-stroke: #D85A30;
--neutral:     #EEEDFE;   /* soft purple fill */
--neutral-stroke: #AFA9EC;

/* Typography */
--serif: "Chiron Sung HK WS", "Source Han Serif SC", "Noto Serif CJK SC", "Songti SC", Georgia, serif;
```

## Font Loading

**All product templates MUST include font loading.** Chiron Sung HK (昭源宋體) and Chiron Hei HK (昭源黑體) variable fonts are served via jsDelivr CDN.

```html
<style>
/* Chiron Sung HK (昭源宋體) + Chiron Hei HK (昭源黑體) via jsDelivr CDN */
@import url('https://cdn.jsdelivr.net/npm/chiron-sung-hk-webfont@latest/css/vf.css');
@import url('https://cdn.jsdelivr.net/npm/chiron-hei-hk-webfont@latest/css/vf.css');
</style>
```

Font families:
- Serif: `"Chiron Sung HK WS"` — weight 200–900 (variable), PADG axis 0–10
- Sans: `"Chiron Hei HK WS"` — weight 200–900 (variable)

## Card Slug Reference

Card slugs (for internal lookup only — no image URLs used):

| # | Slug | # | Slug | # | Slug |
|---|------|---|------|---|------|
| 1 | rider | 13 | child | 25 | ring |
| 2 | clover | 14 | fox | 26 | book |
| 3 | ship | 15 | bear | 27 | letter |
| 4 | house | 16 | stars | 28 | man |
| 5 | tree | 17 | stork | 29 | woman |
| 6 | clouds | 18 | dog | 30 | lily |
| 7 | snake | 19 | tower | 31 | sun |
| 8 | coffin | 20 | garden | 32 | moon |
| 9 | bouquet | 21 | mountain | 33 | key |
| 10 | scythe | 22 | crossroads | 34 | fish |
| 11 | whip | 23 | mice | 35 | anchor |
| 12 | birds | 24 | heart | 36 | cross |
