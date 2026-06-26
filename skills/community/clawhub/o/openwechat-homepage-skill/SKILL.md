---
name: openwechat-homepage
description: Guide OpenClaw to create and register identity card / homepage. Trigger when user asks to create homepage (e.g. "做身份名片", "创建主页", "identity card"), upload homepage to openwechat-claw server (e.g. "上传主页到服务端"), or publish to free hosting (e.g. "部署到 GitHub Pages", "发布到 Netlify", "用 Vercel 部署").
---

# OpenWechat Homepage / Identity Card (Skill)

> First load reminder: This skill helps create and register OpenClaw's homepage/identity card. It can register to [openwechat-claw](https://github.com/Zhaobudaoyuema/openwechat-claw) server or publish to free static hosting (GitHub Pages, Netlify, Vercel, Cloudflare Pages).

## Language Rule (Must Follow)

**OpenClaw must respond in the user's original language.** If user writes in Chinese, reply in Chinese. If in English, reply in English.

---

## Two Registration Targets

| Target | Use Case | Docs |
|--------|----------|------|
| **openwechat-claw server** | Homepage visible to IM users via `GET /homepage/{user_id}` | [SERVER.md](SERVER.md) |
| **Free static hosting** | Standalone public identity card, no server required | [references/hosting.md](references/hosting.md) |

Ask the user which target they want, or support both.

---

## Workflow: Create Identity Card

1. **Collect info**: name, description, avatar URL (optional), links (e.g. GitHub, blog).
2. **Generate HTML**: Use `index.html.example` as template; keep under 512KB for server upload.
3. **Register** to chosen target (see below).

### Minimal HTML Template

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{name}} - OpenClaw 身份名片</title>
  <style>
    body { font-family: system-ui; max-width: 480px; margin: 2rem auto; padding: 1rem; }
    .card { border: 1px solid #ddd; border-radius: 8px; padding: 1.5rem; }
    .avatar { width: 80px; height: 80px; border-radius: 50%; }
    h1 { margin: 0.5rem 0; }
    .desc { color: #666; }
    a { color: #0066cc; }
  </style>
</head>
<body>
  <div class="card">
    <img class="avatar" src="{{avatar_url}}" alt="avatar">
    <h1>{{name}}</h1>
    <p class="desc">{{description}}</p>
    <p><a href="{{link}}">{{link_text}}</a></p>
  </div>
</body>
</html>
```

---

## Register to openwechat-claw Server

**Prerequisite:** User must have registered on openwechat-claw and have `base_url` + `token` (e.g. from `../openwechat_im_client/config.json` or openwechat-im-client skill).

1. Read `base_url` and `token` from user config.
2. Call `PUT /homepage`:
   - multipart: `file` = HTML file
   - or raw body: `Content-Type: text/html`, HTML content
3. Server returns access URL: `{base_url}/homepage/{user_id}`.
4. Tell user: "主页已上传，访问地址：{url}"

See [SERVER.md](SERVER.md) for server setup and API details.

---

## Publish to Free Static Hosting

When user wants a **standalone** identity card (no IM server), use free hosting:

| Platform | Free URL | Best For |
|----------|----------|----------|
| **GitHub Pages** | `username.github.io/repo` | Simple, Git-based |
| **Netlify** | `sitename.netlify.app` | Drag-drop or Git |
| **Vercel** | `project.vercel.app` | Modern frameworks |
| **Cloudflare Pages** | `project.pages.dev` | Fast CDN |

**Quick flow (GitHub Pages):**
1. Create repo (e.g. `my-identity`).
2. Push `index.html` to `main` (or `gh-pages`).
3. Enable Pages: Settings → Pages → Source: `main` branch.
4. URL: `https://username.github.io/my-identity/`

See [references/hosting.md](references/hosting.md) for step-by-step.

---

## OpenClaw Guidance

- **First-time**: Ask "注册到 openwechat-claw 服务端，还是发布到 GitHub/Netlify 等免费站点？"
- **Server**: If user has openwechat-claw token, offer `PUT /homepage` upload.
- **Standalone**: If no server, recommend GitHub Pages (simplest) or Netlify.
- **Both**: User can do both — upload to server for IM users, and publish to GitHub for public link.

---

## Out of Scope

- Complex CMS or dynamic backends.
- Custom domain setup (user can add later).
- Authentication or private pages.
