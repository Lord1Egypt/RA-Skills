---
title: Anti-AI Aesthetic Checklist
impact: HIGH
impactDescription: Self-audit after design completion to ensure no stereotypical AI design patterns remain.
tags: aesthetic,checklist,anti-ai,review
---

## Anti-AI Aesthetic Checklist

After completing the design, it must pass the checklist below. If even one item fails, revise that item.

### 🎨 Colors & Decoration

- [ ] Is the primary color NOT `#3B82F6` (Tailwind blue-500)?
- [ ] Is there no purple→blue linear gradient?
- [ ] Is there no decorative blob/glow overlay in the background?
- [ ] Do cards avoid uniform large shadows? (minimum allowed only when expressing elevation)

### 📐 Layout

- [ ] Did you avoid the stereotypical Hero → 3 Cards → CTA → Footer pattern?
- [ ] Is there asymmetric layout, varied section heights, and grid variation?
- [ ] Are all elements NOT uniformly center-aligned?

### ✍️ Typography

- [ ] Is it a Display+Body font pairing rather than Inter alone?
- [ ] Are different weights (400/600/700) used across body/subheading/heading?
- [ ] Is text hierarchy distinguished not only by size, but also by weight, font, and color?

### 📝 Content

- [ ] Is there no Lorem ipsum?
- [ ] Are generic CTAs such as "Get Started" and "Learn More" not repeated more than 3 times?
- [ ] Is there no meaningless number listing like "10K+ Users"?
- [ ] Are specific service names, copy, and differentiated CTAs included?

### 🔢 Overall

- [ ] Does the color ratio follow 60-30-10?
- [ ] Are all values referenced by tokens (`$`)?
- [ ] Does it meet WCAG AA contrast ratio (4.5:1 or higher)?
