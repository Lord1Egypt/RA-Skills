---
name: mj-gallery
description: MXAI MJ 图片生成 + 自动画廊展示技能。提交 MJ 文生图请求后，自动下载图片到本地、归档到画廊文件夹、部署网页并返回可访问链接。触发词：用MJ画、生成MJ图片、MJ文生图、MJ画廊
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - MX_AI_API_KEY
    primaryEnv: MX_AI_API_KEY
    emoji: "🎨"
---

# 🎨 mj-gallery：MJ 图片生成 + 画廊展示技能

自动完成 MJ 图片生成的完整闭环：**提交 → 轮询 → 下载 → 归档 → 部署 → 返回画廊链接**。

---

## ⛔ 强制规则

1. **不得跳过轮询**：提交后必须轮询到 status=2（完成）或 status=3（失败），禁止假设完成
2. **图片必须下载到本地**：`/workspace/mj_output/{serial}.webp`，不得直接返回 CDN URL（含 auth_key 参数，渲染会异常）
3. **必须归档到画廊**：下载后同时复制到 `/workspace/mj_gallery/`，更新画廊 index.html
4. **必须部署画廊**：使用 deploy 工具部署 `/workspace/mj_gallery/`，返回可公开访问的网页链接
5. **不得伪造结果**：serial_no、image_urls、deployed_url 均必须来自真实 API 响应
6. **prompt 限制 100 字**：MJ draw prompt 不能超过 100 个中文字符，超出时自动精简但不改变核心语义
7. **Prompt 仅用英文**：MJ prompt 统一使用英文，中文 prompt 由技能内部翻译后提交

---

## 🔧 核心工作流

```
用户: "用MJ画一只凤凰"
  ↓
Step 1: 参数判断（自动）
  - model: 默认 MJ 6.1（MJ 7.0 暂不可用，勿传 model 参数）
  - aspect_ratio: 根据用户需求判断（竖版 9:16 / 横版 16:9 / 方形 1:1）
  - speed: 默认 fast
  - iw: 有参考图时 1.2~1.5，无参考图时省略
  ↓
Step 2: 提交 mj_draw
  - prompt 英文限 100 字
  - 告知用户：任务提交中，预计 30s~3min
  ↓
Step 3: 轮询 get_task_status
  - 间隔 5 秒一次
  - 超过 60 秒仍在生成中：告知用户耐心等待，继续轮询
  - 超过 5 分钟：告知用户生成时间较长，询问是否继续等待
  ↓
Step 4: 下载图片
  - 目录准备: /workspace/mj_output/ 和 /workspace/mj_gallery/
  - 下载到: /workspace/mj_output/{serial}.webp
  - 复制到: /workspace/mj_gallery/{serial}.webp
  ↓
Step 5: 更新画廊 index.html
  - 生成新条目加入画廊（最新在前）
  - 最多保留最近 20 条记录
  ↓
Step 6: 部署画廊
  - deploy /workspace/mj_gallery → https://{id}.space.minimaxi.com
  ↓
Step 7: 返回结果
  - 展示本地图片路径: /workspace/mj_output/{serial}.webp
  - 附上画廊链接: https://{id}.space.minimaxi.com
```

---

## 📐 参数决策规则

### aspect_ratio 速查

| 用户需求 | aspect_ratio |
|----------|-------------|
| 横版、宽屏、Panorama | 16:9 |
| 竖版、头像、Porttrait | 9:16 |
| 方形、Square | 1:1 |
| 海报、Portrait Large | 3:4 |
| 电影感、Cinematic | 2:3 |
| 未指定（默认） | 16:9 |

### speed 速查

| 速度 | 积分 | 适用场景 |
|------|------|---------|
| draft（仅MJ7.0） | 2积分 | 草稿预览，MJ7.0不支持stylize |
| fast | 4积分 | 默认，日常使用 |
| turbo（仅MJ7.0） | 8积分 | 极速，MJ7.0不支持stylize |
| 未指定 | fast | — |

**注意：MJ 7.0 暂不可用，speed 参数不传，使用默认值 fast**

### iw 参考图权重速查

| 参考强度 | iw 值 | 场景 |
|----------|-------|------|
| 弱参考 | 0.5~0.8 | 风格参考、色彩参考 |
| 中等参考 | 1.0~1.25 | 构图+风格参考（默认） |
| 强参考 | 1.5~2.0 | 角色一致性、精确参考 |

---

## 🖼️ 画廊 HTML 模板

画廊路径：`/workspace/mj_gallery/index.html`

每条记录结构：
```html
<div class="card">
  <a href="{serial}.webp" target="_blank">
    <img src="{serial}.webp" alt="{prompt摘要}">
  </a>
  <div class="info">
    <p class="prompt">{prompt中文摘要}</p>
    <p class="meta">任务: {serial} · MJ 6.1 · {aspect_ratio} · {时间}</p>
  </div>
</div>
```

画廊样式要求：深色主题（#0a0a0f背景），图片全宽，圆角，阴影，简洁无冗余元素。

---

## 🚨 错误处理

| 错误类型 | 处理方式 |
|----------|---------|
| prompt 超 100 字 | 自动精简核心词，保留主语+动作+风格关键词 |
| API 返回错误 | 展示完整错误信息，告知用户 |
| 图片 URL 获取失败 | 用 thumbnail_path（缩略图）兜底 |
| 轮询超时 | 告知用户 serial_no，用户可凭编号稍后查询 |
| 部署失败 | 返回本地路径 `/workspace/mj_gallery/` 并告知 |

---

## 📁 目录结构

```
/workspace/
  mj_output/              ← 下载缓存（按 serial 归档）
    {serial}.webp
  mj_gallery/              ← 画廊网站（deploy 部署目录）
    index.html
    {serial}.webp          ← 每张图都复制到这里
```

---

## 💡 使用示例

**用户输入：**
「用MJ画一只赛博朋金风格的机械凤凰，横版」

**技能执行：**
1. 判断：aspect_ratio=16:9，英文 prompt，精简到 100 字内
2. 提交 → serial: `2041350580286263296`
3. 轮询 11 次（约 55s）→ status=2 完成
4. 下载到 `/workspace/mj_output/2041350580286263296.webp`
5. 复制到 `/workspace/mj_gallery/2041350580286263296.webp`
6. 更新 `index.html` 加入新条目
7. 部署 → `https://xxxx.space.minimaxi.com`
8. 回复：
   - MEDIA: /workspace/mj_output/2041350580286263296.webp
   - 画廊链接

---

## 版本

- v1.0.0（2026-04-07）：初版，修正 CDN URL 渲染异常问题，自动下载+部署画廊
