# 🦞 OpenClaw 镜像网站 Skill

将线上网站完整镜像到本地，支持离线浏览。自动处理网络检测、递归下载、文件名清理（去除 `?v=`/`?t=` 等查询参数）、资源引用修复，并启动本地预览服务器。

## 安装

将 `mirror-website` 文件夹放入你的 skills 目录即可：

```
skills/
└── user/
    └── mirror-website/
        ├── SKILL.md
        └── README.md
```

## 用法

在对话中直接告诉 Claude 你想镜像哪个网站，以及保存到哪里。

### 基本格式

```
镜像网站: <网址>，保存地址: <本地路径>
```

### 输入示例

**指定保存路径：**

```
镜像网站: www.example.com，保存地址: /home/user/sites/example
```

```
镜像网站: blog.example.org，保存地址: /tmp/blog-backup
```

**不指定路径（自动使用默认路径）：**

```
镜像网站: www.example.com
```

**其他触发方式（自然语言）：**

```
帮我把 example.com 下载到本地
```

```
克隆一下 docs.example.com 保存到 /home/user/docs
```

```
我想离线浏览 blog.example.org，保存到桌面
```

```
抓取 www.example.com 到 /data/mirror
```

## 功能特性

| 功能 | 说明 |
|------|------|
| 网络自动检测 | 先尝试直连，失败后自动尝试本地代理 |
| 递归下载 | 最大深度 5 层，自动下载页面所需的 CSS/JS/图片等资源 |
| 文件名清理 | 去除 `?v=`、`?t=`、`?ver=` 等查询参数，还原干净文件名 |
| 引用路径修复 | 同步修复 HTML/CSS/JS 中的资源引用路径 |
| 重复扩展名修复 | 自动修复 `style.css.css` → `style.css` |
| 本地预览 | 自动启动 Python HTTP Server（默认端口 9527） |
| 结果验证 | 自动检查残留问题并输出文件类型分布 |

## 执行流程

```
解析输入 → 创建目录 → 检测网络/代理 → wget 递归下载
    → 补充下载带参数资源 → 清理文件名 → 修复引用路径
    → 验证结果 → 启动预览服务器 → 输出摘要
```

## 文件名清理示例

| 下载后的文件名 | 清理后 |
|---------------|--------|
| `common.js?v=202312021610` | `common.js` |
| `foot_menu.css?t=20231032` | `foot_menu.css` |
| `DPlayer.min.js?v=5` | `DPlayer.min.js` |
| `style.css%3Fver=1.2` | `style.css` |
| `audio.css.css` | `audio.css` |

## 限制

- **仅支持静态/SSR 网站**：wget 无法执行 JavaScript，SPA（单页应用）或纯前端渲染的站点无法完整镜像
- **外部资源不下载**：仅下载目标域名下的资源，CDN 或第三方域名的资源不会被抓取
- **登录后内容**：需要登录才能访问的页面无法镜像
