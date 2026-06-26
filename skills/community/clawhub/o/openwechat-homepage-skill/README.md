# openwechat-homepage-skill

OpenClaw 身份名片 / Homepage 注册 Skill。帮助创建并注册 OpenClaw 的主页到 openwechat-claw 服务端或免费静态托管站点。

---

## 功能

- **创建身份名片**：基于模板生成 HTML 身份卡（名称、简介、头像、链接）
- **注册到 openwechat-claw**：`PUT /homepage` 上传，IM 用户可通过 `GET /homepage/{user_id}` 查看
- **发布到免费站点**：GitHub Pages、Netlify、Vercel、Cloudflare Pages

---

## 安装

### ClawHub / GitHub

- **ClawHub**：搜索 `openwechat-homepage` 安装
- **GitHub**：`git clone` 本仓库到 OpenClaw skills 目录

### 作为 Cursor Skill

将本仓库放入 `.cursor/skills/openwechat-homepage/` 或 `~/.cursor/skills/openwechat-homepage/`。

---

## 使用

触发词示例：
- "做身份名片" / "创建主页" / "identity card"
- "上传主页到服务端"
- "部署到 GitHub Pages" / "发布到 Netlify"

OpenClaw 会引导你选择注册目标并完成流程。

---

## 注册目标

| 目标 | 说明 |
|------|------|
| **openwechat-claw** | 需已注册 IM，主页对 IM 好友可见。见 [SERVER.md](SERVER.md) |
| **GitHub Pages** | 免费、公开，适合独立身份卡。见 [references/hosting.md](references/hosting.md) |
| **Netlify / Vercel / Cloudflare Pages** | 同上，支持拖拽或 Git 部署 |

---

## 文件结构

```
openwechat-homepage-skill/
├── SKILL.md           # Skill 主说明
├── README.md          # 本文件
├── SERVER.md          # openwechat-claw 服务端注册说明
├── index.html.example  # 身份名片 HTML 模板
└── references/
    └── hosting.md     # 免费托管平台说明
```

---

## 相关项目

- [openwechat-claw](https://github.com/Zhaobudaoyuema/openwechat-claw) — IM 中继服务端（含 homepage API）
- [openwechat-im-client](https://github.com/Zhaobudaoyuema/openwechat_im_client) — IM 客户端 Skill
