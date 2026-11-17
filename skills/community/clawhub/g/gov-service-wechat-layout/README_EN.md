# gov-service-wechat-layout (民生政务公众号排版模板)

A WorkBuddy skill that lays out WeChat official-account articles for public-service / government-affairs accounts (social security, medical insurance, housing fund, tax, civil affairs, public security, etc.).

## What it gives you
- **Nine content-type layout templates**: myth-busting / policy explainer, new-policy explainer, notice/announcement, how-to guide, cautionary case, Q&A, event/campaign recap, year-in-review, route/collection.
- **A swappable theme-color model**: one per-article theme color + two fixed semantic colors (warning-red, correct-blue).
- Templates use **inline styles only** — paste directly into the WeChat editor, formatting preserved, **no 135 editor required**. Note: reminder cards use a `<table>` wrapper instead of `<div>` because WeChat editor strips `border` from `<div>` but keeps table borders.

## Install
Unzip into `~/.workbuddy/skills/` (Windows: `C:\Users\<you>\.workbuddy\skills\`), then restart WorkBuddy.

## Use
Just say, e.g.:
- "排版这篇社保推文" (lay out this social-security article)
- "用办事指南模板排这篇" (use the how-to-guide template)
- "主题色用蓝色" (use blue as the theme color)

It picks the matching template, applies the theme color, fills placeholders, and returns paste-ready HTML.

## Recolor
```bash
python scripts/apply_theme_color.py --input assets/template-C-guide.md.html --color be5960
```
Or find-replace `#ff6d4d` in any template (keep `#ff0000` and `#5f9cef` fixed).

## Placeholders
Replace before publishing: `{{IP名}} {{城市}} {{热线}} {{公众号名}} {{机构全称}}`, plus per-article `【…】` content slots.

See `README.md` (Chinese) for the full guide, including the publish-path explainer (direct paste vs 135).
