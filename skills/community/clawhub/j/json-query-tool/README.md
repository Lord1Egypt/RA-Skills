# JSON Query Tool Web

在线 JSON 查询工具，纯前端实现，数据不上传服务器。

**部署状态**: 待部署（需配置 API Token）

## 功能特性

- ✅ 纯前端 HTML/CSS/JS，无后端依赖
- ✅ 支持路径查询 `$.store.book[*].author`
- ✅ 支持数组索引 `users[0].email`
- ✅ 支持通配符 `[*]` 和 `.*`
- ✅ 支持深层嵌套查询
- ✅ JSON / 表格 / 原始三种输出格式
- ✅ 响应式设计，移动端可用
- ✅ 预置示例数据，即开即用
- ✅ 广告位（Google AdSense / 百度广告联盟）

## 文件结构

```
json-query-tool-web/
├── index.html          # 完整单页应用（所有代码内嵌）
├── DEPLOY.md           # 部署指南
└── README.md
```

## 快速部署

### 方式一：Vercel（推荐，免费）

```bash
npm i -g vercel
vercel login
cd json-query-tool-web
vercel --prod
```

### 方式二：Cloudflare Pages（免费）

```bash
npm i -g wrangler
wrangler login
cd json-query-tool-web
wrangler pages deploy . --project-name json-query-tool
```

### 方式三：GitHub Pages

1. 创建空仓库 `json-query-tool-web`
2. 推送代码
3. Settings → Pages → 选择 main branch / (root)
4. 访问 `https://[username].github.io/json-query-tool-web`

## 广告接入

### Google AdSense
在 `index.html` 中找到占位标记 `<!-- 百度广告联盟 / Google AdSense 占位 -->`，替换为：
```html
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXX" crossorigin="anonymous"></script>
<ins class="adsbygoogle" style="display:block" data-ad-client="ca-pub-XXXXXXXXXX" data-ad-slot="XXXXXXXXXX"></ins>
```

### 百度广告联盟
替换为百度广告代码即可。

## 部署 URL（待填写）

项目部署后，在此记录 URL：

- **Vercel URL**: https://json-query-tool.vercel.app
- **Cloudflare URL**: https://json-query-tool.pages.dev

## 技术栈

- HTML5 + CSS3 + Vanilla JavaScript
- 无框架依赖，文件大小 < 35KB
- 加载速度 < 100ms
