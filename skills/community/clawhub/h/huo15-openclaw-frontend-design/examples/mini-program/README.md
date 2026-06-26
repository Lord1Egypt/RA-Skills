# 小程序 Starter — 火一五前端设计技能 v4.3

> 微信 + 支付宝 + 抖音 + 快手 **四端** starter。**浏览器无法直接渲染** wxml / axml / ttml / ksml，必须用各家 IDE。

## 微信小程序

1. 下载并安装 [微信开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)（Stable v1.06+）
2. 打开工具 → **项目 → 导入项目** → 目录选 `wechat/`
3. AppID 选"测试号"或填自有；项目名留空走默认
4. 点**编译**：左侧模拟器看渲染；点**真机调试**扫码看真机
5. 页面走 `pages/index/index`，全局配置 `app.json`

## 支付宝小程序

1. 下载并安装 [支付宝小程序 IDE](https://opendocs.alipay.com/mini/ide/download)
2. 打开 IDE → **文件 → 打开项目** → 目录选 `alipay/`
3. 点**预览**，扫码用支付宝 App 看真机
4. 配置文件名是 `mini.project.json`（不是 `project.config.json`），别搞混

## 抖音小程序

1. 下载并安装 [抖音开发者工具](https://developer.open-douyin.com/docs/resource/zh-CN/mini-app/develop/developer-instrument/installation/developer-instrument-update-and-download)
2. 打开工具 → **项目 → 导入项目** → 目录选 `douyin/`
3. AppID 用"测试号"或填自有
4. 点**编译预览**，扫码用抖音 App 看真机
5. 模板后缀是 `.ttml` / `.ttss`（与微信 `.wxml` / `.wxss` 95% 同源，仅前缀差异）

## 快手小程序 ⭐v4.3

1. 下载并安装 [快手小程序开发者工具](https://mp.kuaishou.com/docs/develop/developerTools/downloadPath.html)
2. 打开工具 → **项目 → 导入项目** → 目录选 `kuaishou/`
3. AppID 用"测试号"或填自有
4. 点**编译预览**，扫码用快手 App 看真机
5. 模板后缀是 `.ksml` / 样式 `.css`（标准 CSS 后缀，区别于其他端）

## 四端同步迭代姿势 ⭐v4.3 升级

**推荐顺序**：微信 → 抖音 → 快手（最相近）→ 支付宝（差异最大）

### 步骤 1：先在 `wechat/` 改完

`wxml` + `wxss` + 配置全部跑通。开发体验在微信端最顺。

### 步骤 2：复制到 `douyin/` 改前缀（机械替换，3 分钟）

| 微信 | 抖音 |
|---|---|
| `wx:for` / `wx:key` / `wx:if` | `tt:for` / `tt:key` / `tt:if` |
| `wxml` 文件名 | `ttml` |
| `wxss` 文件名 | `ttss` |
| `bindtap` / `bindinput` | **保留**（兼容微信 bind 风格） |

### 步骤 3：复制到 `kuaishou/` 改前缀（机械替换，3 分钟）

| 微信 | 快手 |
|---|---|
| `wx:for` / `wx:key` / `wx:if` | `ks:for` / `ks:key` / `ks:if` |
| `wxml` 文件名 | `ksml` |
| `wxss` 文件名 | `css`（注意：快手用标准 CSS 后缀） |
| `bindtap` / `bindinput` | **保留** |

### 步骤 4：复制到 `alipay/` 改前缀（机械替换，5 分钟）

| 微信 | 支付宝 |
|---|---|
| `wx:for` / `wx:key` / `wx:if` | `a:for` / `a:key` / `a:if` |
| `bindtap` / `bindinput` / `bindsubmit` | `onTap` / `onInput` / `onSubmit` |
| `wxml` 文件名 | `axml` |
| `wxss` 文件名 | `acss` |
| `<page-meta>` | **不支持**，改 `my.setNavigationBar` API（写在 onLoad） |
| `enhanced="true"` 等微信特有属性 | 删掉 |
| `app.json` tabBar `color`/`text` | `textColor`/`name` |

### 步骤 5：四端 ICON / 图片资源建议放 CDN（本地用 base64 或纯色块占位）

## 反 AI Slop 红线（v4.3 扩展 UI 库列表）

| # | 禁用项 | 替代方案 |
|---|---|---|
| 14 | 直接套 **WeUI / Vant Weapp / TDesign-Mini / Lin-UI / TTUI / Tt-Mini-UI / KSUI / kuaishou-uikit** 默认皮 | 自定义 token，至少改 5 个变量再用 |
| 15 | 缺 `<page-meta>` + `safe-area-inset` + `rpx` 适配 | 见本目录 `wechat/pages/index/index.wxml` |

通用红线 #1 字体豁免：小程序里 `font-family` 优先 PingFang SC / Source Han Sans SC / Noto Sans SC（不能加载 Web Font）。

## 视觉风格

四端 starter 共用 ORGANIC 流派暖色调（米白 + 土橙 + 暖卡片），主题"手作商品列表"。`hero` + `chips` + 商品 `grid` 三段式，避开千篇一律的"banner + features + cta"。

## 引用关系

- 配色逻辑参考 [`references/colors.md`](../../references/colors.md) §5 ORGANIC（用 hex 表达 oklch 等价值，因小程序基础库 < 3.0 不一定支持 oklch）
- 字体策略参考 [`references/typography.md`](../../references/typography.md) §6 + 小程序豁免说明（见 SKILL.md §四 v2.2 新增段）
- 多端同步迭代速查见本文 §四端同步迭代姿势

## 四端真机扫码后必查清单

- [ ] 顶部胶囊（四端形态略有不同：微信圆角 / 支付宝椭圆 / 抖音矩形 / 快手矩形）不遮内容
- [ ] 底部 home indicator 不遮 tabBar / 内容
- [ ] 横屏 / 竖屏切换不崩
- [ ] 字号在小屏（375rpx）/ 大屏（414rpx+）都不溢出
- [ ] tabBar 用平台 native（不要自绘 view 拼接）

## 何时该用编译框架

如果同时维护 4 端，且产品复杂度 > 10 个页面，建议直接上 [Taro](https://taro-docs.jd.com/) 或 [Uni-app](https://uniapp.dcloud.net.cn/) — 写一份代码自动编译四端。本 skill 提供的 4 个 starter 是给"原生开发 + 设计样板参考"用的，不是 SaaS 级框架。
