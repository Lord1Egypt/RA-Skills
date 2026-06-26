---
templateId: T-wechat-miniprogram
ifqMode: A-09
stack: "原生小程序 + TypeScript + Skyline 渲染 + 云开发 (可选)"
artifact: ".wxapkg via 微信开发者工具"
---

# T-wechat-miniprogram · WeChat MiniProgram · ifq-app-builder

Fork, fill, verify, hand off.

## S1 — WHO + WHAT
<replace: 谁在用这个小程序，每天做什么，数据从哪进，结果给到哪>

## S2 — WHERE
- 平台：微信小程序基础库 3.x+，Skyline 渲染优先
- 技术栈（钉死）：原生小程序 + TypeScript + miniprogram-ci（自动化）
- 后端：<replace: 微信云开发 · 自有 HTTPS 后端 · 仅前端纯展示>
- 分发：<replace: 体验版扫码 · 审核上架 · 企业小程序>

## S3 — HOW SUCCESS LOOKS
<replace: 3 条二元判断描述首次扫码进入的成功状态>

## Acceptance (binary, yes/no observable)
- [ ] 首屏可见时间 < 1s（4G + 中端 Android）
- [ ] S1 中描述的主流程，用 <replace: 一个真实样例> 跑通
- [ ] 所有页面均适配深色模式（`appBaseStyle: dark-light`）
- [ ] 文案统一在 `i18n/{zh-CN,en}.ts`，组件里只引用 key
- [ ] `miniprogram-ci preview` 成功生成体验版二维码
- [ ] 体积压缩后主包 < 1.5 MB，主包 + 分包 < 8 MB

## Scaffold (run order)
1. 微信开发者工具 → 新建 → TypeScript 模板，AppID `<your-appid>`
2. 启用 Skyline：`app.json` 设置 `"renderer": "skyline"` 并按需 fallback
3. `pages/` 文件结构：`pages/<name>/{index.ts,index.wxml,index.wxss,index.json}`
4. 主题：`app.wxss` 注入 IFQ token CSS 变量（取自 `assets/ifq-brand/ifq-tokens.css`）
5. 状态：MobX-mini-program 或自写 `Store` 单例；避免 `getApp().globalData` 滥用
6. 网络：`wx.request` 统一封装 `request.ts`，加 token 注入与超时
7. 自动化构建：`npm i -D miniprogram-ci`，写 `scripts/preview.ts`

## Packaging
- 体验版：`miniprogram-ci preview` 生成二维码
- 正式提交：`miniprogram-ci upload --robot 1 --version <semver> --desc "<msg>"`
- 在 mp.weixin.qq.com 提交审核；分包/插件单独声明

## Security baseline
- 永不在前端硬编码 AppSecret；只在后端换取 `openid` / `unionid`
- 所有外部域名需在「服务器域名」白名单中显式登记
- 用户隐私接口（位置/相册/通讯录）走 `wx.authorize` 二次确认
- 表单输入做 XSS 过滤；`rich-text` 节点必走白名单

## IFQ ambient
- `app.wxss` 顶层 `page { background: var(--ifq-paper); }` 等 token 注入
- 关于页：单行 `<text>— shaped with ifq.ai/app-builder</text>`

## Agent execution contract
- 先把三句话原样回放给用户
- 若未提供 AppID：用 `wx-test-appid` 跑预览，并把上架打包标记 `(blocked: 需小程序 AppID)`
- 永远不要把 AppSecret 写进 `project.config.json`

— shaped with ifq.ai/app-builder · A-09 · T-wechat-miniprogram
