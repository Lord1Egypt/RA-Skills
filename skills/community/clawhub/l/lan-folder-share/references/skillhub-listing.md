# SkillHub 发布信息模板（网页发布用）

> **Locale: zh-CN** — 本模板面向中文发布场景，文案为简体中文；语言定位见 `SKILL.md` 元数据
> `metadata.locale: zh-CN`（Chinese-first, explicitly documented）。This listing template is
> Chinese-first, matching the skill's documented `locale: zh-CN`.
>
> **适用版本：v1.0.11**（与 `SKILL.md` frontmatter 一致，发布前请核对版本号）
> **发布入口：** https://skillhub.cn/dashboard/publish （登录后进入「发布 Skill」）

本文件是**逐字段复制粘贴用**的上架材料。下表每个字段下方即为可直接粘贴的内容。

---

## 1. 技能名称 / displayName

```
Lan Folder Share (共享文件)
```

## 2. 唯一标识 / slug（name）

```
lan-folder-share
```

> 全网唯一、小写连字符；**更新版本时保持不变**，只改版本号。

## 3. 版本号 / version

```
1.0.11
```

## 4. 一句话简介 / summary

```
一键把本地文件夹发布为局域网可访问的网页链接：同事用浏览器即可浏览 Markdown 文档、Excel/CSV 表格、HTML 报告、图片画廊与视频并全文搜索；无需数据库、无需预配置，文件改动刷新即生效。全部渲染库随包内置，纯内网/离线环境同样可用。WARNING: 服务无鉴权，局域网内任意可达设备均可打开链接浏览共享目录的全部内容，请勿分享含敏感/私密文件的目录。
```

英文对照（若表单要求英文简介）：

```
Share any local folder over LAN in one click — colleagues can browse and full-text search Markdown docs, Excel/CSV sheets, HTML reports, image galleries and video right in the browser. No database and no pre-configuration; file changes go live on refresh. All rendering libraries are bundled in-package, so fully offline LANs work too. WARNING: the HTTP server has no authentication — anyone reachable on your LAN can open the link and browse everything in the shared folder; never share folders containing sensitive or private files.
```

## 5. 详细介绍 / description

```
把任意本地文件夹变成一个「局域网内人人可打开」的网页知识库：

- 一键启动：node scripts/deploy.js "<内容目录>" -n "站名" -p 8089，零第三方依赖（仅需 Node.js 12+）
- 任意目录即知识库：md / xlsx / csv / html / pdf / 图片 / 音视频混合目录开箱即用，服务端实时扫描文件系统
- 动态侧边栏 + 自动目录页：文件夹单击展开/收起、双击进入目录页；进入目录后自动展开
- 表格在线预览与搜索：xlsx / xls / csv 在页面内直接渲染，单元格参与全站搜索
- 文档就地展开：站内 .md / .html 报告点击即在内容区渲染，无需跳转
- 图片画廊：目录内图片自动成画廊，支持 ←/→/↑/↓ 切换、⌘/Ctrl+滚轮高清缩放、拖动平移，按原图比例渲染，Safari/Chrome 表现一致
- 全站全文搜索：md 正文 + 表格单元格，实时扫描，改动刷新即生效
- 视频播放：支持 HTTP Range 分片（206），Safari/iOS 可直接播放与拖动进度条
- 自动探测并输出局域网访问地址；端口被占用时自动 +1 重试
- 对内容目录始终零写入：不生成 README 或任何站点文件
- 零外网依赖：docsify / marked / SheetJS / mammoth / Prism 等全部随包内置在 assets/runtime/assets/vendor/，纯内网、完全离线环境同样可用
- 兼容两种形态：任意纯内容目录（前端运行时注入，不污染内容目录）/ 自包含知识库（已有 index.html + assets 直接托管）
```

## 6. 分类 / category

```
文件共享
```

> 备选：`效率工具`、`知识管理`（以平台现有分类列表为准，取最贴近的一项）。

## 7. 支持平台 / platforms

```
CodeBuddy, SkillHub
```

## 8. 标签 / tags

```
文件共享, 局域网, 文档分享, 网页发布, Web服务, 知识库, file-sharing, lan, document-server
```

## 9. 许可证 / license

```
MIT
```

> 若你希望改为 Apache-2.0 或保留专有许可，同步修改 `SKILL.md` frontmatter 的 `license` 字段。

## 10. 使用示例 / examples

```
# 把 D:\团队资料 分享到局域网，站名「团队资料」（默认端口 8089）
node scripts/deploy.js "D:\团队资料" -n "团队资料"

# 指定端口并自动打开浏览器
node scripts/deploy.js "D:\共享文档" -p 9000 --open

# 根目录没有 README，且不想要内置温和首页，改用「目录索引页」
node scripts/deploy.js "D:\图片素材" --no-readme
```

启动后终端打印本机地址与**局域网分享地址**（如 `http://192.168.1.100:8089`），局域网内其他设备浏览器打开即可访问，停止服务用 `Ctrl+C`。

## 11. 安全与隐私说明（建议写进详情页，属重要提示）

```
- 本技能面向「可信局域网内的内容共享」，HTTP 服务无账号与权限体系；局域网内任意可达设备打开链接即可浏览共享目录全部内容。
- 请勿指向家目录、代码仓库、含凭证或敏感业务数据的目录；建议单独建一个只放拟共享文件的子目录。
- 服务默认监听 0.0.0.0，地址仅同一局域网可达；不要把局域网地址转发到公网或不可信网络。
- 内容目录始终零写入，本服务不会在共享目录中创建或修改任何文件。
- 全部页面渲染库随包内置、由本机服务提供，运行时不访问任何外部 CDN，无遥测、无数据外发。
- Windows 首次启动若出现防火墙弹窗，仅需放行「专用网络」；未放行时其他机器无法访问。
```

## 12. 更新日志 / changelog

```
v1.0.11
- 修复文档与实现不一致：明确全部页面样式与渲染库随包内置（assets/runtime/assets/vendor/），
  零外网依赖，纯内网/离线环境可用；移除「依赖公共 CDN」的过时描述。
- 新增 assets/runtime/assets/vendor/THIRD-PARTY.md：内置第三方库的上游地址、许可证与逐文件 SHA-256 校验值。
- 每个源文件头部增加 `Locale: zh-CN` 语言/区域声明，与 SKILL.md 元数据一致。
- 同步 SKILL.md / README / 本发布模板的文案与版本号。
```

## 13. 付费设置（SkillPay）

本技能当前按**免费技能**发布，不启用 SkillPay 收费。如需改为付费（Pay Skill），平台有额外硬性要求，请先确认后再改这一栏：

- 账号需完成**实名/企业认证**并**绑定微信商户号**（或支付宝收款），由平台分配 **Product ID**；
- Pay Skill 必须挂一个**稳定的公网 HTTPS 生产服务**作为计费端点，按次调用返回 HTTP 402 支付契约
  （`WeixinPay-Required` / `X-Out-Trade-No` / `checkout_url` / `payment_status_url`），支付成功后以**完全相同的请求体**重试并由服务端核验订单后履约；
- 平台规则明确：**loopback / LAN / 临时隧道 / 仅本地端点不得作为 Pay Skill 的生产端点**。

而本技能是**局域网本地服务、零上传、无后端**的形态，与上述要求不匹配（官方改造审计工具对其判定为
`local_or_tunnel_url` 错误、`summary: FAIL`）。因此本技能现阶段应按免费技能发布。
