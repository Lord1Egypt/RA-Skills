---
name: gzh-download-knowledge
slug: gzh-download-knowledge
displayName: 公众号文章批量导出 · 存为本地 Markdown 知识库
version: 1.0.3
summary: 把自己的公众号历史文章批量导出为本地 Markdown——后台官方「发表记录」全量列表、稳定链接、一键批量保存、纯本地运行、零 token 成本。由 webclaw3 驱动（复用你已登录的 Chrome，无需填任何 token/cookie）。
license: MIT
description: 把自己的公众号历史文章批量导出为本地 Markdown 归档——后台官方「发表记录」全量列表、稳定链接、一键批量保存、纯本地运行、零 token 成本。由 webclaw3 驱动（复用你已登录的 Chrome，无需填任何 token/cookie）。触发场景：想把公众号历史文章批量存到本地做归档/知识库（只支持自己的公众号，后台登录的那个号）。
---

# gzh-download-knowledge · 公众号文章下载归档

把自己的公众号历史文章批量保存为本地 Markdown，用于个人内容归档/知识库。路径：登录公众号后台 → 「发表记录」（官方全量历史文章列表，按发布日期倒序）→ 每篇**稳定短码链接** `mp.weixin.qq.com/s/XXX` → 打开提取正文 → 存本地。

**边界：只做自己的公众号**（后台登录的那个号，无需指定账号）。不做"抓别人的号"（版权风险 + 微信官方正在灰度"公众号文章→AI 知识库"功能）；不做任何灰色接口。

## 前置依赖（必须安装）

- **webclaw3 是本 skill 的前置依赖，必须安装**——本 skill 靠它打开你已登录的公众号后台，没有它无法运行。
- 安装 webclaw3 后，先运行检查：
  ```bash
  node <webclaw3安装路径>/scripts/webclaw3.mjs doctor
  ```
  路径通常在 `~/.claude/skills/webclaw3` 或 `~/.workbuddy/skills/webclaw3`，让 agent 自行定位；安装命令见 webclaw3 仓库 README（一条命令装好）。
- 浏览器需已登录公众号后台（`mp.weixin.qq.com`）——账号由登录态决定，运行前确认登录的是要归档的那个号。

## 使用方式

```bash
node skill.mjs <input.json>
# 或：把 input.json 放在当前目录，直接 node skill.mjs
```

### 入参（input.json）

| 字段 | 类型 | 必填 | 默认 | 说明 |
|---|---|---|---|---|
| `count` | int | 否 | `10` | 本次要新增保存的篇数（去重跳过的旧文不计入，自动继续向后抓取补满） |
| `offset` | int | 否 | `0` | 跳过前 N 篇再取——增量归档：第一次 0，第二次 10，依此类推 |
| `outputDir` | string | 否 | `/tmp/gzh-download-knowledge-output/` | 导出目录（articles/*.md + index.json 写这里） |
| `homeUrl` | string | 否 | 自动 | 带 token 的公众号后台 URL（浏览器地址栏复制）。不填时自动从已打开的后台 tab 提取 token |
| `output_dir` | string | 否 | `/tmp/gzh-download-knowledge-output/` | 管线输出目录（res.json + data.md 写这里；与导出目录同默认，也可分开指定） |
| `output_files` | object | 否 | — | `{ result, data }` 自定义 res.json / data.md 文件名 |

> 会话 token 说明：微信后台必须带 token 访问（无 token 会"请重新登录"）。运行前先在浏览器打开 mp.weixin.qq.com 公众号后台并保持登录（URL 带 token）——脚本会自动从已打开的后台 tab 提取；也可用 `homeUrl` 直接指定。

## 输出

导出目录（`outputDir`）下：

- `articles/<序号>-<标题前20字>.md`：每篇一个 Markdown，frontmatter 含 `title` / `author`（公众号名）/ `url`（稳定短码 `mp.weixin.qq.com/s/XXX`）/ `date`（发表记录日期，无则留空）
- `index.json`：`count`、`offset`、`actual`（实际保存数）、`status`（success/partial/failed）、每篇 `{title, url, status}`，partial 时附 `reason`

管线输出目录（`output_dir`）下：`res.json`（状态与计数元信息）+ `data.md`（本次保存清单）。

stdout 只输出一行 JSON：`{ status, summary, output_dir }`。

## 行为约定

- **只取「已发表」文章**：发表记录列表项即已发表文章（已删除条目是签名式 URL，不匹配短码选择器，天然跳过）。
- **顺序与增量**：发表记录按发布日期倒序（最新在前）；`offset` 映射到发表记录分页参数 begin——跳过前 offset 篇，`count` 取本次篇数，配合去重可分段归档完整个号。
- **去重**：稳定短码 `mp.weixin.qq.com/s/<短码>` 作 key；跨次运行自动扫描 `outputDir` 已有产物（articles/*.md 的 frontmatter url 与 index.json），已存在的 SKIP。**去重跳过不计入 count，自动继续向后抓取直到本次新增 count 篇**（归档时重跑会自动补全缺口，无需手动算 offset）。
- **访问节奏**：全程串行单 tab、条间 ≥2.5s、翻页/开 tab 后 sleep 6s 等加载；连续 3 篇失败立即停，不硬刚。
- 不足 `count` 时 `index.json` 标 `partial` 并给出原因（发表记录不足 / 页面加载失败 / 已删除文章）。

## 报错排查

- **报「浏览器中继服务不可用」**：webclaw3 没装/没启动。先 `curl -s http://127.0.0.1:3459/api/status` 看 `extensionConnected` 是否 true；否则按前置依赖安装 webclaw3 并运行 `node <webclaw3安装路径>/scripts/webclaw3.mjs doctor` 完成检查。
- **报「浏览器未登录公众号后台」**：扩展已连上但 mp.weixin.qq.com 会话过期。在浏览器里打开 `mp.weixin.qq.com` 完成扫码登录后重跑。
- **webclaw3 已就绪但浏览器侧没连上**（relay 响应但扩展未连）：① 确认 Chrome 扩展 wc3-chrome 已启用（chrome://extensions）；② 在 Chrome 里登录 mp.weixin.qq.com 公众号后台；③ 重跑 `node <webclaw3安装路径>/scripts/webclaw3.mjs doctor` 看 advice。
- 其余情况：看 `res.json` 的 `error`/`reason` 字段与 stderr 日志。

## 合规边界

仅官方后台自己的内容；单次 ≤ `count`；纯本地运行、不发布、不做任何抓取他人内容的路径。
