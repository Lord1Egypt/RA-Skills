# 微信小程序境外用户体验适配 Skill

一个面向微信小程序开发者的境外用户适配检测工具和指引 Skill，帮助开发者自动识别代码中会导致境外用户体验问题的位置，并基于微信官方文档给出具体适配方案。

## 核心问题

大多数小程序在设计之初只考虑了国内用户。境外用户在使用时会遇到: 手机号只支持 +86、表单不接受护照、翻译后文字溢出容器等一系列卡点。本 Skill 将这些适配经验系统化，让 AI 能够自动完成检测 + 定位 + 指引。

## 能力概览

### 1. 自动化代码扫描

内置 `validation/scan-project.js` 扫描工具，对任意小程序项目进行静态分析:

```
node validation/scan-project.js --project <小程序项目路径>
```

**检测维度包括:**

- **翻译后溢出预测 (P0/P1)** -- 扫描所有 WXML 中文文案，估算翻译为 English/Spanish/French/German 后的像素宽度，与 CSS 容器宽度对比，标记确定/可能溢出的位置。这是本 Skill 的核心特色能力。
- **CSS 溢出风险 (P1)** -- 识别固定宽度容器缺少 overflow/text-overflow/word-break 保护的选择器。
- **账号体系硬阻塞 (P0)** -- 检测手机号区号硬编码 +86、11 位长度校验硬编码、maxlength=11 等直接导致境外用户无法使用的问题。
- **表单国际化 (P0)** -- 检测姓名字段仅允许中文、证件类型缺少护照选项等问题。

输出 `reports/scan-report.md` (人类可读报告) 和 `reports/scan-result.json` (机器可读结果)。

### 2. 基于官方文档的完整适配指引

SKILL.md 包含三个核心维度的适配方案，每个维度附带可直接使用的代码示例（详见 reference.md）:

| 维度 | 解决的问题 | 关键内容 |
|------|-----------|---------|
| 账号体系 | 境外用户登不上 | 国际区号选择器方案、手机号快速验证组件接入、邮箱验证通道搭建、国际短信服务接入示例(Twilio) |
| 信息录入 | 境外用户填不了 | 证件类型扩展(护照/永居证/港澳台通行证)、姓名正则放宽、国际地址格式输入 |
| UI 与排版 | 翻译后排版乱 | 语言路由分流方案、国际版界面减法原则、溢出风险扫描模式速查表、WXSS 排版适配代码示例 |

此外，搜索触达（小程序名称/简介补充英文）和多语言适配（平台翻译已可用，自建 i18n 可选）作为 P1/P2 项列在优先级表中。

## 快速开始

### 前置要求

- Node.js >= 18.0.0
- 一个微信小程序项目 (包含 app.json)

### 安装

```bash
cd validation
npm install
```

### 运行扫描

```bash
node scan-project.js --project /path/to/your/miniprogram
```

### 输出示例

扫描完成后会在 `validation/reports/` 目录生成:
- `scan-report.md` -- 完整的 Markdown 报告，按 P0/P1 优先级排列
- `scan-result.json` -- 结构化 JSON 结果，可用于 CI/CD 集成

## 适用场景

**已有小程序改造** -- 快速定位所有需要国际化改造的点，按优先级排序。

**新建小程序规范检查** -- 开发过程中随时检查代码是否符合境外适配规范。

**发版前自检** -- 每次发布前运行一次，确认无遗漏的国际化问题，相当于自动化 code review。

## 文件结构

```
./
├── LICENSE               # MIT-0 开源协议
├── README.md             # 本文件
├── SKILL.md              # Skill 主文件 (AI 助手读取的核心 prompt)
├── reference.md          # 详细代码示例 (按需加载)
└── validation/
    ├── package.json      # npm 依赖
    ├── scan-project.js   # 核心扫描工具 (入口)
    ├── overflow-predict.js # 独立溢出预测脚本
    ├── rules/            # 检测规则模块
    │   ├── i18n-coverage.js   # 中文文案与项目配置扫描
    │   └── overflow-risk.js   # CSS 容器与溢出风险扫描
    ├── whitelists/       # API 白名单
    │   └── wx-api.json
    └── reports/          # 扫描报告输出目录 (运行后生成)
```

## 依据的官方资源

- [手机号快速验证组件](https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/getPhoneNumber.html)
- [小程序翻译能力](https://developers.weixin.qq.com/community/minihome/article/doc/000222bddd4e70130844a1db66b413)
- [wx.getAppBaseInfo 接口](https://developers.weixin.qq.com/miniprogram/dev/api/base/system/wx.getAppBaseInfo.html)
- [小程序境外交流专区](https://developers.weixin.qq.com/community/minihome/mixflow/3721056300659130376)
- 境外业务邮箱: miniprogram_global@tencent.com

## License

本项目基于 [MIT-0 License](LICENSE) 开源。
