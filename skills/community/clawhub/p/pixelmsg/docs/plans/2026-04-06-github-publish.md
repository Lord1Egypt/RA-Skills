# GitHub Publish Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Clean up the project structure, internationalise templates to English, generate Chinese screenshots for a Chinese README, then restore templates.

**Architecture:** Sequential tasks — cleanup first (no dependencies), then template i18n + screenshot generation in parallel where possible, then docs.

**Tech Stack:** Node.js, Playwright, bash, pixelmsg SKILL (screenshot.mjs + render.sh)

---

### Task 1: Delete development-only files

**Files:**
- Delete: `snap.mjs`
- Delete: `take-weather.mjs`
- Delete: `take-todolist.mjs`
- Delete: `index.html`
- Delete: `data.json`
- Delete: `screenshot-url.mjs`

**Step 1: Remove files**

```bash
rm snap.mjs take-weather.mjs take-todolist.mjs index.html data.json screenshot-url.mjs
```

**Step 2: Verify**

```bash
ls *.mjs *.html *.json 2>/dev/null || echo "clean"
```
Expected: only `package.json` and `package-lock.json` remain as `.json`; only `screenshot.mjs` as `.mjs`; no loose `.html`.

**Step 3: Commit**

```bash
git add -A
git commit -m "chore: remove development-only scripts and prototype files"
```

---

### Task 2: Add .gitignore

**Files:**
- Create: `.gitignore`

**Step 1: Write .gitignore**

```
node_modules/
screenshots/
.DS_Store
*.log
```

Note: `screenshots/` is intentionally ignored — screenshots are generated artefacts. The README references them via relative paths which work after `npm run screenshots` is run locally or in CI.

**Step 2: Commit**

```bash
git add .gitignore
git commit -m "chore: add .gitignore"
```

---

### Task 3: Add LICENSE (MIT)

**Files:**
- Create: `LICENSE`

**Step 1: Write LICENSE**

```
MIT License

Copyright (c) 2026 pixelmsg contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

**Step 2: Commit**

```bash
git add LICENSE
git commit -m "chore: add MIT license"
```

---

### Task 4: Flesh out package.json

**Files:**
- Modify: `package.json`

**Step 1: Rewrite package.json**

```json
{
  "name": "pixelmsg",
  "version": "1.0.0",
  "description": "Turn AI responses into beautiful image cards — render HTML templates to pixel-perfect PNGs with Playwright",
  "type": "module",
  "license": "MIT",
  "engines": { "node": ">=18" },
  "scripts": {
    "screenshots": "node screenshot.mjs templates/weather.html --viewport mobile --out ./screenshots && node screenshot.mjs templates/github-trending.html --viewport mobile --out ./screenshots && node screenshot.mjs templates/todolist.html --viewport mobile --out ./screenshots && node screenshot.mjs templates/github-stats.html --viewport desktop --out ./screenshots"
  },
  "dependencies": {
    "playwright": "^1.58.2"
  }
}
```

**Step 2: Verify**

```bash
node -e "import('./package.json', {assert:{type:'json'}}).then(m=>console.log(m.default.name))"
```
Expected: `pixelmsg`

**Step 3: Commit**

```bash
git add package.json
git commit -m "chore: flesh out package.json with name, description, scripts, license"
```

---

### Task 5: Translate templates to English

Templates needing translation (Chinese UI text → English):
- `templates/weather.html` — `lang`, city, date, labels (湿度/体感/风力), forecast days, conditions, section header
- `templates/todolist.html` — `lang`, header text, task titles, footer date
- `templates/shanghai-weather.html` — `lang`, all Chinese UI labels

`github-trending.html` and `github-stats.html` are already in English — skip.

**Files:**
- Modify: `templates/weather.html`
- Modify: `templates/todolist.html`
- Modify: `templates/shanghai-weather.html`

**Step 1: Edit weather.html**

Changes:
- `<html lang="zh-CN">` → `<html lang="en">`
- `city: '上海'` → `city: 'Shanghai'`
- `date: '2026年4月3日'` → `date: 'April 3, 2026'`
- `condition: '多云'` → `condition: 'Cloudy'`
- Forecast days: `'今天','明天','后天','周一','周二'` → `'Today','Tomorrow','Day 3','Mon','Tue'`
- Forecast conditions: `'多云','小雨','阵雨','多云','晴'` → `'Cloudy','Light Rain','Showers','Cloudy','Sunny'`
- conditionIcon keys: change Chinese keys to English (`'晴'→'Sunny'`, `'多云'→'Cloudy'`, `'小雨'→'Light Rain'`, `'阵雨'→'Showers'`, `'阴'→'Overcast'`)
- Stats labels: `'湿度'→'Humidity'`, `'体感'→'Feels Like'`, `'风力'→'Wind'`
- Wind value: `'东南风 3级'` → `'SE Wind 3'`
- Section header: `'5 天预报'` → `'5-Day Forecast'`

**Step 2: Edit todolist.html**

Changes:
- `<html lang="zh-CN">` → `<html lang="en">`
- Task titles:
  - `'阅读《深度工作》30分钟'` → `'Read Deep Work for 30 min'`
  - `'晨跑 5km'` → `'Morning run 5km'`
  - `'完成 Q2 OKR 草稿'` → `'Draft Q2 OKR'`
  - `'Review PR #142'` → keep as-is
  - `'准备周五分享'` → `'Prep Friday talk'`
- Header: `'今日待办'` → `"Today's Tasks"`
- Progress label: `完成` → `done`
- Footer date: `'April 3, Thursday'` (check template for exact location)

**Step 3: Edit shanghai-weather.html**

This template fetches live data from Open-Meteo API. Only translate static UI labels:
- `<html lang="zh-CN">` → `<html lang="en">`
- `<title>上海天气</title>` → `<title>Shanghai Weather</title>`
- All Chinese UI labels (loading text, stat labels like 湿度/体感/风力/能见度/紫外线, day names 今明后, section headers) → English equivalents

**Step 4: Verify visually — render weather and todolist**

```bash
node screenshot.mjs templates/weather.html --viewport mobile --out ./screenshots --name weather-en-check
node screenshot.mjs templates/todolist.html --viewport mobile --out ./screenshots --name todolist-en-check
```

Open the PNGs and confirm text is in English.

**Step 5: Commit**

```bash
git add templates/weather.html templates/todolist.html templates/shanghai-weather.html
git commit -m "feat: translate templates to English"
```

---

### Task 6: Generate Chinese screenshots for README.zh-CN.md

Strategy (method 3): temporarily patch demo data in the three mobile templates to Chinese, render screenshots to `screenshots/zh/`, then restore the templates.

Templates to patch:
- `weather.html` — restore Chinese city/date/labels/forecast
- `todolist.html` — restore Chinese task titles + header
- `github-trending.html` — already has English content which is fine for Chinese README too (repo names are always English on GitHub); skip patching

**Files:**
- Temporarily modify: `templates/weather.html`, `templates/todolist.html`
- Create: `screenshots/zh/` directory (gitignored)

**Step 1: Patch weather.html to Chinese data**

Revert data fields (NOT the file permanently — do it in-memory via a temp copy):

```bash
cp templates/weather.html /tmp/weather-en-backup.html
```

Edit `templates/weather.html` to set:
- `city: '上海'`, `date: '2026年4月3日'`
- conditions back to Chinese, labels back to Chinese

**Step 2: Patch todolist.html to Chinese data**

```bash
cp templates/todolist.html /tmp/todolist-en-backup.html
```

Edit `templates/todolist.html` to set Chinese task titles and header.

**Step 3: Render Chinese screenshots**

```bash
mkdir -p screenshots/zh
node screenshot.mjs templates/weather.html --viewport mobile --out ./screenshots/zh
node screenshot.mjs templates/github-trending.html --viewport mobile --out ./screenshots/zh
node screenshot.mjs templates/todolist.html --viewport mobile --out ./screenshots/zh
node screenshot.mjs templates/github-stats.html --viewport desktop --out ./screenshots/zh
```

**Step 4: Restore templates from backups**

```bash
cp /tmp/weather-en-backup.html templates/weather.html
cp /tmp/todolist-en-backup.html templates/todolist.html
```

**Step 5: Verify restoration**

```bash
node screenshot.mjs templates/weather.html --viewport mobile --out ./screenshots --name weather-restore-check
```

Confirm English text is back.

**Step 6: No commit needed** — screenshots are gitignored, templates are back to English.

---

### Task 7: Write README.zh-CN.md

**Files:**
- Create: `README.zh-CN.md`

Mirror the structure of `README.md` but:
- All prose in Chinese
- Demo screenshots reference `screenshots/zh/` paths
- Keep code blocks in English (commands don't change)
- Add a link at top pointing to English README

**Step 1: Write README.zh-CN.md**

Structure:
```
[English README](README.md) | 中文文档

# pixelmsg

> 把 AI 回复变成精美图片卡片。

## 为什么用 pixelmsg
[Chinese version of comparison table]

## 效果预览
[Demo table with screenshots/zh/ paths]

## 特性
[Chinese feature list]

## 快速开始
[Chinese prose, English commands]

## 模板列表
[Chinese description column, keep template paths in English]

## 使用方法
[Chinese prose, English commands]

## screenshot.mjs 参数
[Chinese description column]

## 设计规范
[Chinese prose]

## 贡献
[Chinese prose]

## License
MIT
```

**Step 2: Add cross-link to README.md**

Add at top of `README.md`:

```markdown
[English](README.md) | [中文](README.zh-CN.md)
```

**Step 3: Commit**

```bash
git add README.zh-CN.md README.md
git commit -m "docs: add Chinese README with localized screenshots"
```

---

### Task 8: Regenerate English screenshots and update SKILL.md

After all template changes, regenerate the canonical English screenshots:

```bash
node screenshot.mjs templates/weather.html --viewport mobile --out ./screenshots
node screenshot.mjs templates/github-trending.html --viewport mobile --out ./screenshots
node screenshot.mjs templates/todolist.html --viewport mobile --out ./screenshots
node screenshot.mjs templates/github-stats.html --viewport desktop --out ./screenshots
```

Also update `SKILL.md` to reflect `render.sh` new viewport default and remove any remaining references to old 900w naming.

**Commit:**

```bash
git add SKILL.md
git commit -m "docs: update SKILL.md render.sh viewport documentation"
```
