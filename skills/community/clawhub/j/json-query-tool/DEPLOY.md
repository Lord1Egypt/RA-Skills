# JSON Query Tool Web - 部署记录

## 临时测试 URL（Cloudflare Quick Tunnel）

**当前可访问**: https://supplement-soa-bet-settle.trycloudflare.com

> ⚠️ 此 URL 为 Cloudflare 临时隧道，每次重启服务后会变化。
> 建议配置永久部署（见下方）。

## 永久部署方式

### 方式一：Vercel（推荐，30秒完成）

```bash
# 1. 安装 Vercel CLI
npm i -g vercel

# 2. 登录（浏览器自动打开）
vercel login

# 3. 部署（生产环境）
cd /root/.openclaw/workspace/projects/json-query-tool-web
vercel --prod

# 部署后获得永久 URL，如：https://json-query-tool.vercel.app
```

### 方式二：Cloudflare Pages（免费，无需信用卡）

```bash
# 1. 安装 Wrangler CLI
npm i -g wrangler

# 2. 登录 Cloudflare
wrangler login

# 3. 部署
cd /root/.openclaw/workspace/projects/json-query-tool-web
wrangler pages deploy . --project-name json-query-tool

# 部署后获得永久 URL，如：https://json-query-tool.pages.dev
```

### 方式三：GitHub Pages（免费）

```bash
# 1. 在 GitHub 创建空仓库 json-query-tool-web
gh repo create json-query-tool-web --public

# 2. 推送代码
git remote add origin https://github.com/shenghoo/json-query-tool-web.git
git push -u origin main

# 3. 启用 Pages
# GitHub → Settings → Pages → Source: main branch, / (root)

# 访问 https://shenghoo.github.io/json-query-tool-web
```

## 广告接入指南

### Google AdSense

1. 注册 [Google AdSense](https://www.google.com/adsense)
2. 获取 `ca-pub-XXXXXXXXXX` 和广告位 ID
3. 在 `index.html` 中替换以下两处占位：

```html
<!-- 顶部广告位 -->
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-XXXXXXXXXX"
     data-ad-slot="XXXXXXXXXX"
     data-ad-format="auto"></ins>

<!-- 底部广告位 -->
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-XXXXXXXXXX"
     data-ad-slot="XXXXXXXXXX"
     data-ad-format="auto"></ins>
```

### 百度广告联盟

1. 注册 [百度广告联盟](https://union.baidu.com)
2. 获取广告代码，替换占位区域

## 项目统计

- **文件大小**: index.html 约 30KB（内嵌所有代码）
- **加载时间**: < 100ms（无外部依赖）
- **支持语法**: $.key / $.arr[*] / $.obj.* / 深层嵌套
- **输出格式**: JSON / 表格 / 原始

## 部署命令速查

```bash
# Vercel
vercel --prod --token $VERCEL_TOKEN

# Cloudflare Pages
CLOUDFLARE_API_TOKEN=xxx wrangler pages deploy . --project-name json-query-tool

# Netlify
netlify deploy --dir=. --prod --auth $NETLIFY_TOKEN
```
