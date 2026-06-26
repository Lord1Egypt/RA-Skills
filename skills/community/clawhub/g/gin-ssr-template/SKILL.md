---
name: gin-ssr-template
description: 根据 Figma 设计稿截图生成可直接运行的 Gin SSR 页面模板（HTML + CSS）。当用户发送“gin前端模板”或提供 Figma 页面截图时触发：生成的页面必须优先保证可运行、可预览、结构完整；禁止输出任何 {{.data}}、{{.Path}}、{{.Config}} 这类动态取值；head 中 SEO/meta/application/ld+json 必须完整写死；main 区域必须严格按截图还原；写入两个文件并返回文件路径与附件。
---

# Gin SSR 前端模板生成（OpenClaw）

## 0. 最高优先级

1. 必须生成两个真实文件

- HTML：`app/templates/page/{页面名}.html`
- CSS：`app/static/css/{页面名}.css`

2. 必须保证页面可运行

- 输出的 HTML 必须是完整可渲染结构
- 不要依赖 `{{.data.Config.*}}`、`{{.data.Path}}`、`{{.Title}}` 这类动态模板变量
- 除 `{{define "页面名"}}` 和 `{{end}}` 外，默认不要输出其他 Go 模板变量
- 优先生成“直接打开就有完整结构”的静态页面骨架

3. 必须最终回复

- 回复中必须包含：页面名、HTML 路径、CSS 路径
- Telegram 会话必须追加两个 `MEDIA:` 行
- 禁止静默结束

4. main 必须按截图严格还原

- 不允许只写占位注释
- 不允许 main 为空
- 必须把截图里的核心模块、文案、按钮、输入框、卡片、列表都写出来

## 1. 页面名规则

### 1.1 标题识别

- 优先识别截图顶部标题或页面主标题
- 如果标题太泛（如“详情”“设置”“中心”），必须结合 main 首屏核心内容决定页面名
- 如果识别不到标题，在 HTML 顶部加注释：`<!-- 页面标题识别失败，需确认 -->`

### 1.2 页面名生成

页面名必须和“标题 + main 语义”一致，禁止随便命名。

优先级：

1. 优先用准确英文语义命名：

- `个人信息` + 资料编辑表单 → `user_profile`
- `收货地址` + 地址列表 → `address_list`
- `订单详情` + 订单信息卡片 → `order_detail`
- `修改密码` + 表单 → `password_edit`

2. 无法稳定翻译时，使用拼音小写下划线：

- `漫画分类` → `manhua_fenlei`

最终：

- HTML define：`{{define "{页面名}"}}`
- HTML 文件：`app/templates/page/{页面名}.html`
- CSS 文件：`app/static/css/{页面名}.css`

## 2. 输出原则

### 2.1 禁止动态取值

生成内容时，禁止出现以下写法：

- `{{.data...}}`
- `{{.Config...}}`
- `{{.Path}}`
- `{{.Title}}`
- `{{range ...}}`
- `{{if ...}}`

也就是说，页面内容、SEO、链接、标题、描述、JSON-LD 都必须使用硬编码静态值。

### 2.2 允许保留的模板语法

只允许保留：

```html
{{define "{页面名}"}} ... {{end}}
```

````

这是为了兼容 Gin 模板文件结构。

## 3. head 模板要求

head 必须完整，字段不得缺失。所有值全部硬编码，保证页面开箱可运行。

```html
{{define "{页面名}"}}
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge, chrome=1" />
    <meta name="renderer" content="webkit" />
    <meta name="HandheldFriendly" content="true" />
    <meta http-equiv="x-dns-prefetch-control" content="on" />
    <meta name="referrer" content="same-origin" />
    <meta name="yandex-verification" content="YANDEX_VERIFICATION_REPLACE_ME" />
    <meta name="msvalidate.01" content="MS_VALIDATE_REPLACE_ME" />

    <title>页面标题</title>

    <meta property="og:title" content="页面标题" />
    <meta property="og:site_name" content="站点名称" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://example.invalid/current-page" />
    <meta property="og:image" content="https://example.invalid/favicon.ico" />
    <meta property="og:description" content="页面描述" />

    <meta name="twitter:title" content="页面标题" />
    <meta name="twitter:description" content="页面描述" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:image" content="https://example.invalid/favicon.ico" />

    <link rel="shortcut icon" href="https://example.invalid/favicon.ico" />
    <meta name="description" content="页面描述" />
    <meta name="keywords" content="关键词1,关键词2,关键词3" />
    <link rel="canonical" href="https://example.invalid/current-page" />
    <meta name="robots" content="index, follow" />
    <meta name="rating" content="adult" />
    <meta name="theme-color" content="#ffffff" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-status-bar-style" content="#ffffff" />
    <meta name="template" content="Mirages" />
    <link rel="icon" type="image/x-icon" href="https://example.invalid/favicon.ico" />

    <script type="application/ld+json">
      {
        "@context": "https://schema.org",
        "@graph": [
          {
            "@type": "Organization",
            "@id": "https://example.invalid/#org",
            "name": "站点名称",
            "url": "https://example.invalid",
            "logo": {
              "@type": "ImageObject",
              "url": "https://example.invalid/static/images/logo.png"
            }
          },
          {
            "@type": "WebSite",
            "@id": "https://example.invalid/#website",
            "url": "https://example.invalid",
            "name": "站点名称",
            "inLanguage": "zh-CN",
            "publisher": {
              "@id": "https://example.invalid/#org"
            },
            "potentialAction": {
              "@type": "SearchAction",
              "target": "https://example.invalid/{search_term_string}",
              "query-input": "required name=search_term_string"
            }
          },
          {
            "@type": "CollectionPage",
            "@id": "https://example.invalid/#webpage",
            "url": "https://example.invalid/current-page",
            "name": "页面标题",
            "description": "页面描述",
            "inLanguage": "zh-CN",
            "isPartOf": {
              "@id": "https://example.invalid/#website"
            },
            "about": {
              "@id": "https://example.invalid/#org"
            }
          }
        ]
      }
    </script>

    <script src="/static/js/imgDecypt.js"></script>
    <script src="/static/js/index.js"></script>
    <script src="/static/js/bootstrap.bundle.min.js"></script>

    <link rel="stylesheet" href="/static/css/bootstrap.min.css" />
    <link rel="stylesheet" href="/static/css/style.css" />
    <link rel="stylesheet" href="/static/css/{页面名}.css" />
  </head>
  <body>
    <header class="page-header">
      <div class="page-header__inner">
        <a class="page-header__logo" href="/">LOGO</a>
        <nav class="page-header__nav">
          <a href="/">首页</a>
          <a href="/list">列表</a>
          <a href="/about">关于</a>
        </nav>
      </div>
    </header>

    <main class="{页面名}-page">
      <!-- 必须在这里用原生 HTML 严格还原截图 -->
    </main>

    <footer class="page-footer">
      <div class="page-footer__inner">
        <p>© 2026 Site Name. All Rights Reserved.</p>
      </div>
    </footer>
  </body>
</html>
{{end}}
```

## 4. main 区域还原规则

### 4.1 结构必须完整

main 中必须包含截图里能看到的真实结构，例如：

- 页面标题区
- 面包屑/说明文案
- 卡片区
- 表单区
- 列表区
- 操作按钮区
- 头像/封面/图标区
- 标签/状态区

### 4.2 文案必须补齐

- 能识别出的文案必须直接写入 HTML
- 看不清时写中文注释：

```html
<!-- 文案待确认 -->
```

- 不能因为文案看不清就把整个模块省略掉

### 4.3 CSS 必须可用

CSS 必须包含：

- 页面根容器
- 每个区块容器
- 字号、行高、颜色
- 边框、圆角、背景、阴影
- Flex / Grid 布局
- 间距（margin/padding/gap）
- 按钮、输入框、列表项样式
- 必要的移动端适配

## 5. 响应式规则

- PC 稿：默认桌面样式
- 有 H5 稿：补充

```css
@media screen and (max-width: 824px) {
  /* H5样式 */
}
```

- 只有 H5 稿：补充

```css
@media screen and (min-width: 825px) {
  /* PC样式 */
}
```

## 6. 生成步骤

1. 先识别截图 title
2. 再识别 main 里的所有模块和文案
3. 生成页面名 `{页面名}`
4. 先输出完整 HTML 骨架
5. 再把 main 按截图补全
6. 生成对应 CSS
7. 写入两个文件
8. 回复文件路径和附件

## 7. 最终回复格式

最终回复必须是：

```text
✅ 生成完成
页面名: {页面名}
HTML: app/templates/page/{页面名}.html
CSS: app/static/css/{页面名}.css
```

Telegram 会话必须追加：

```text
MEDIA:app/templates/page/{页面名}.html
MEDIA:app/static/css/{页面名}.css
```

```

```
````
