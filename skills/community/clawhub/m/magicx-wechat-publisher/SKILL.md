---
name: wechat-publisher
description: 将已完成的文章发布到微信公众号草稿箱。只负责排版转换、图片上传、草稿提交，不负责文章内容生成。当用户要求"发公众号""上传草稿箱""发布文章到公众号"时触发此技能。
---

# 微信公众号发送技能

## 边界

- ✅ 本技能只做：Markdown/文本 → 公众号HTML → 上传图片 → 提交草稿箱
- ❌ 本技能不做：选题、写作、内容生成（由文章生成技能负责）
- 输入：已完成的文章内容 + 配图文件
- 输出：公众号草稿箱中的可发布草稿

## 发布流程（5步）

### Step 1: 获取 access_token（Agent 执行）

从 `scripts/.wechat-config.json` 读取 appid 和 secret，然后调用微信API：

```bash
curl "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={APPID}&secret={SECRET}"
```

返回 `access_token`，后续步骤都需要用到。

### Step 2: 上传图片（Agent 执行）

> 此步骤由 Agent 通过 curl 调用微信API完成，不通过脚本。

- 正文图片 → `POST https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={TOKEN}`（multipart/form-data 上传，返回微信图床URL）
- 封面图 → `POST https://api.weixin.qq.com/cgi-bin/material/add_material?type=image&access_token={TOKEN}`（返回 media_id）

### Step 3: 转换HTML（Agent 执行）

将文章内容转为公众号专用HTML，**必须遵守排版规范**（见下方）。关键要求：
- 替换所有图片 src 为 Step 2 获得的微信图床URL
- 所有样式必须内联，禁止使用 `<style>` 标签或 CSS class

### Step 4: 上传草稿（脚本执行）

将转换好的HTML保存为文件，使用附带脚本上传到草稿箱：

```bash
node scripts/upload-draft.js --html <html文件> --title <标题> [--author <作者>]
```

脚本会自动：
1. 从 `scripts/.wechat-config.json` 读取 AppID/Secret
2. 调用微信API获取 access_token
3. 通过 `POST /cgi-bin/draft/add` 将HTML内容提交到草稿箱

### Step 5: 通知用户

上传成功后通知用户去公众号后台 → 内容与互动 → 草稿箱 中检查并设置封面图，确认后发布。

## 排版规范（公众号HTML标准）

### 全局规则

- **所有样式必须内联**，禁止 `<style>` 标签和 CSS class
- 正文不含 `<h1>` 标题（标题由公众号自动显示），开头用摘要引导块代替

### 元素规范

| 元素 | 标签 | 内联样式 |
|------|------|----------|
| 摘要块 | `<section>` | `margin:10px 0 15px;padding:15px 20px;background:#f7f8fa;border-left:4px solid #0EA5E9;font-size:15px;color:#555;line-height:1.6;` |
| 正文段落 | `<p>` | `margin:3px 0;font-size:16px;line-height:1.75;color:#333;` |
| 加粗 | `<strong>` | 不加额外样式（禁止用 `<span>` 或 class 模拟加粗） |
| 关键词高亮 | `<strong><span>` | 加粗+颜色双重强调，用于核心观点/关键数据/金句 |

### 关键词颜色高亮规则（重要！）

纯加粗在黑字中不够突出，**必须对关键词/关键句加颜色**，帮助读者快速扫到重点。

#### 颜色方案

| 用途 | 颜色 | 写法 |
|------|------|------|
| 核心观点/金句 | 品牌蓝 #0EA5E9 | `<strong style="color:#0EA5E9;">关键句</strong>` |
| 重要数据/数字 | 橙色 #f59e0b | `<strong style="color:#f59e0b;">40%</strong>` |
| 警示/冲突 | 红色 #ef4444 | `<strong style="color:#ef4444;">警示内容</strong>` |
| 正面/增长 | 绿色 #10b981 | `<strong style="color:#10b981;">增长数据</strong>` |
| 普通加粗 | 默认黑色 | `<strong>普通强调</strong>` |

#### 使用原则

- 每段最多高亮1-2处，不要全篇都是彩色（否则失去重点）
- 金句/核心观点用品牌蓝（最常用）
- 关键数字用橙色（数据冲击感）
- 不要在一句话里混用多种颜色
- 普通强调仍然用无颜色的 `<strong>`，颜色只给最关键的内容
| 二级标题 | `<h2>` | `font-size:20px;font-weight:bold;color:#111;margin-top:15px;margin-bottom:5px;padding-left:12px;border-left:4px solid #0EA5E9;` |
| 三级标题 | `<h3>` | `font-size:17px;font-weight:bold;color:#222;margin-top:12px;margin-bottom:3px;` |
| 分割线 | `<hr>` | `border:none;border-top:1px solid #eee;margin:8px 0;`（禁止用 div 模拟） |
| 引用块 | `<blockquote>` | `margin:3px 0;padding:12px 18px;background:#f7f8fa;border-left:4px solid #0EA5E9;color:#555;font-style:italic;` |
| 图片容器 | `<p>` | `text-align:center;margin:3px 0;` |
| 图片 | `<img>` | `max-width:100%;display:block;margin:0 auto;border-radius:12px;` |
| 落款 | `<p>` | `margin-top:20px;padding-top:10px;border-top:1px solid #eee;font-size:14px;color:#999;text-align:center;line-height:2;` |

### 落款标准内容

```html
<p style="margin-top:20px;padding-top:10px;border-top:1px solid #eee;font-size:14px;color:#999;text-align:center;line-height:2;">有用AI — 有用才会用，会用才有用。<br/>AI领域连续创业者、落地实战派<br/>亲手打造AI产品，服务数百家中大型名企</p>
```

### 禁止事项

- ❌ 使用 `<style>` 标签或 CSS class
- ❌ 使用 `<h1>`（标题由公众号系统渲染）
- ❌ 使用 base64 图片（使用外部图床URL或在公众号素材库上传）
- ❌ 使用 `<span class="bold">` 模拟加粗（必须用 `<strong>`）
- ❌ 使用 `<div>` 模拟分割线（必须用 `<hr>`）
- ❌ 落款中出现"个人观点，不构成投资建议"
- ❌ 落款上方出现多条分割线（只保留落款自带的 border-top）

## 文章结构模板

参考 `assets/article-template.html`，标准结构为：

```
摘要引导块（section）
正文段落...
图片（推文截图等）
引用块
正文段落...
分割线
二级标题 + 图片 + 正文段落...
分割线
二级标题 + 图片 + 正文段落...
...（重复章节）
分割线
二级标题"写在最后" + 结尾段落...
落款
```

## 脚本工具

- `scripts/upload-draft.js` — 草稿上传脚本（Node.js），负责调用微信API提交草稿
- 仅使用 Node.js 内置模块（https, fs, path），无需安装额外依赖
- 用法：`node scripts/upload-draft.js --html <html文件> --title <标题> [--author <作者>]`

## 配置说明

- AppID/Secret 存放于 `scripts/.wechat-config.json`（本地文件，请勿提交到版本控制）
- 首次使用：`node scripts/upload-draft.js --appid xxx --secret xxx --save-config`
- 保存后后续使用无需再传入 appid/secret 参数
- 服务器公网 IP 需加入公众号后台的 IP 白名单

---

## 关于

本技能由 **magicx** 开发维护。

- 公众号：**有用AI** — 有用才会用，会用才有用
- 视频号：**有用AI**
- 邮箱：youyouyoumagic@gmail.com
- 许可证：ISC © magicx

![扫码关注视频号「有用AI」](assets/youai_sph_qrcode.JPG)
