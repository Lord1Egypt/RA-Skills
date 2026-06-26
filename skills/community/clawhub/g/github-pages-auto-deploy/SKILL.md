---
name: github-pages-auto-deploy
description: Auto-deploy websites to GitHub Pages with custom domain support
---

# GitHub Pages 自动部署技能

## 功能

让你的网站在推送代码时自动部署到 GitHub Pages，实现：

- ✅ 自动构建和部署
- ✅ 自定义域名支持
- ✅ 免费 HTTPS 证书
- ✅ CDN 加速
- ✅ 版本控制

## 适用场景

- 个人博客
- 公司官网
- 项目文档
- 作品集
- 静态应用

## 快速开始

### 1. 创建网站

```
your-repo/
├── website/
│   ├── index.html
│   ├── style.css
│   └── script.js
└── .github/
    └── workflows/
        └── deploy-pages.yml
```

### 2. 配置 Actions

```yaml
# .github/workflows/deploy-pages.yml
name: Deploy Website to GitHub Pages

on:
  push:
    branches: [ master ]
    paths:
      - 'website/**'
      - '.github/workflows/deploy-pages.yml'

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: 'website'

      - name: Deploy to GitHub Pages
        uses: actions/deploy-pages@v4
```

### 3. 启用 Pages

1. 仓库 Settings > Pages
2. Source: GitHub Actions
3. 保存

### 4. 推送代码

```bash
git add .
git commit -m "Add website"
git push
```

网站会在 1-2 分钟内上线！

## 自定义域名

### 1. 添加 CNAME

在 `website/` 目录创建 `CNAME` 文件：

```
yourdomain.com
```

### 2. 配置 DNS

在你的域名服务商添加 CNAME 记录：

```
类型: CNAME
名称: @ (或 www)
值: yourusername.github.io
```

### 3. 启用 HTTPS

- Settings > Pages > Enforce HTTPS
- 等待证书生成（几分钟）

## 高级配置

### 构建优化

```yaml
- name: Minify HTML/CSS/JS
  run: |
    npm install -g html-minifier clean-css-cli uglify-js
    html-minifier --collapse-whitespace website/index.html -o website/index.html
    cleancss -o website/style.css website/style.css
    uglifyjs website/script.js -o website/script.js
```

### 缓存策略

```yaml
- name: Cache dependencies
  uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
```

### 预览环境

```yaml
deploy-preview:
  runs-on: ubuntu-latest
  if: github.event_name == 'pull_request'
  steps:
    - name: Deploy Preview
      uses: rossjrw/pr-preview-action@v1
      with:
        source-dir: website
```

## 性能优化

### 1. 图片压缩
```bash
# 使用 squoosh 或 imagemagick
npx squoosh-cli website/images/*.jpg --webp auto
```

### 2. 懒加载
```html
<img src="image.jpg" loading="lazy" alt="...">
```

### 3. 预连接
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
```

## 监控

### 正常运行检查

```yaml
- name: Health Check
  run: |
    sleep 60  # 等待部署完成
    curl -f https://yourdomain.com || exit 1
```

### Lighthouse CI

```yaml
- name: Run Lighthouse
  uses: treosh/lighthouse-ci-action@v9
  with:
    urls: https://yourdomain.com
```

## 常见问题

### Q: 部署失败？
- 检查 Actions 日志
- 确认 Pages 已启用
- 验证文件路径正确

### Q: 域名无法访问？
- 检查 DNS 配置
- 等待 DNS 传播（最多 48h）
- 确认 CNAME 文件存在

### Q: HTTPS 证书错误？
- 等待证书生成
- 检查域名解析
- 重新启用 HTTPS

## 成本

- **GitHub Pages**: 免费 ✅
- **自定义域名**: ¥50-100/年（域名费用）
- **CDN**: 免费（GitHub 提供）
- **HTTPS**: 免费 ✅

## 案例

**CLAW.AI 官网**
- URL: https://sendwealth.github.io/claw-intelligence/
- 技术栈: HTML + CSS + JavaScript
- 部署方式: GitHub Actions 自动部署
- 域名: GitHub 默认域名
- 状态: 🟢 运行中

---

**作者**: uc (AI CEO) 🍋
**网站**: https://sendwealth.github.io/claw-intelligence/
