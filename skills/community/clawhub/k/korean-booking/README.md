# 韩国美容医美预约指南 Skill

> 基于 BeautsGO 平台的韩国美容医疗机构预约查询 Skill，支持首尔 900+ 家皮肤科、整形医院、医美机构，覆盖中/英/日/泰四种语言。用户只需说出医院名或美容项目，即可获取完整预约流程、在线咨询、价格查询及 APP 下载引导。

[![clawhub](https://img.shields.io/badge/clawhub-korean--booking-blue)](https://clawhub.ai/BeautsGO/korean-booking)
[![version](https://img.shields.io/badge/version-2.6.5-green)](https://clawhub.ai/BeautsGO/korean-booking)

**📦 安装：**
```bash
npx clawhub install korean-booking
```
或直接访问：[clawhub.ai/BeautsGO/korean-booking](https://clawhub.ai/BeautsGO/korean-booking)

---

## English Summary

**Korean Beauty & Medical Aesthetic Booking Skill** — A conversational skill for booking appointments at 900+ Seoul skin clinics, plastic surgery hospitals, and aesthetic centers via the BeautsGO platform. Supports Chinese, English, Japanese, and Thai.

**Trigger phrases:** "Book JD Skin Clinic", "I want laser treatment in Seoul", "Recommend a beauty clinic in Korea", "Download the app", etc.

---

## 功能介绍

### 触发方式（无需说出医院名）

| 用户说 | Skill 行为 |
|--------|-----------|
| `帮我预约JD皮肤科` | 返回该医院预约流程 |
| `想做激光/打玻尿酸/整形` | 按项目类型推荐收录医院列表 |
| `韩国美容医院推荐` | 返回热门机构推荐 |
| `帮我下载` / `下载APP` | 返回 iOS/Android/APK 下载链接 |
| `查价格` / `多少钱` | 打开医院价格页面 |
| `咨询客服` | 打开在线客服页面 |

### 多轮对话流程

用户安装后，可通过自然语言逐步完成整个预约，无需手动操作：

**第1轮 — 查询预约流程**
```
用户: "怎么预约 JD 皮肤科？"
Skill: 返回五大预约渠道说明 + 建议下一步操作
```

**第2轮 — 打开医院页面**
```
用户: "打开链接"
Skill: 自动打开浏览器，加载 BeautsGO 医院详情页
```

**第3轮 — 发起预约**
```
用户: "帮我预约"
Skill: 自动点击预约按钮，跳转预约表单，询问人数/时间
```

**第4轮 — 填写预约信息**
```
用户: "2人，4月10日"
Skill: 自动填写表单并提交，返回预约结果
```

**第5轮 — 咨询客服**
```
用户: "咨询客服"
Skill: 自动打开该医院在线客服页面
```

### 支持的输入方式

- 中文名：`韩国JD皮肤科怎么预约`
- 英文名：`CNP Skin Clinic appointment`
- 缩写：`jd 怎么预约`
- 自然语言：`我想约一下CNP狎鸥亭店`
- 项目意图：`想做双眼皮` / `激光去斑` / `打肉毒素`
- 后续指令：`打开链接` / `帮我预约` / `咨询客服` / `查价格` / `帮我下载`

### 预约渠道（每家医院返回）

- 🍎 **App Store**（iOS）
- 🤖 **Google Play**（Android）
- 📱 **微信小程序**
- 🟢 **微信公众号**
- 🌐 **网页端**

### 核心能力

- ✅ 首尔 900+ 家医院数据库（皮肤科、整形、医美、激光、注射）
- ✅ 四级智能匹配（精确 → 拼音 → 模糊 → 别名）
- ✅ 泛意图识别（无需说医院名，直接说做什么项目）
- ✅ 自动打开浏览器到医院详情页
- ✅ 自动点击预约按钮（Playwright）
- ✅ 自动填写预约表单并提交
- ✅ 在线客服直达
- ✅ 价格表查询
- ✅ APP 下载引导（iOS / Google Play / APK）
- ✅ 多语言支持（中/英/日/泰）

---

## 快速开始

```bash
# 从 clawhub 安装（推荐）
npx clawhub install korean-booking

# 或本地开发
npm install
```

调用示例：

```js
const skill = require('./api/skill')

// 查询预约流程
const result = await skill({
  query: 'JD皮肤科怎么预约',
  lang: 'zh'   // zh / en / ja / th
})

// 多轮对话（传入上下文）
const result2 = await skill({
  query: '帮我预约',
  lang: 'zh',
  context: { hospitalName: 'JD皮肤科' }
})

console.log(result)
```

---

## 项目结构

```
├── api/
│   ├── skill.js              # Skill 主入口
│   └── browser/
│       └── open-url.js       # 浏览器打开页面
├── core/
│   ├── preprocessor.js       # 自然语言预处理
│   ├── resolver.js           # 医院匹配（四级策略）
│   ├── service.js            # 业务编排
│   └── renderer.js           # 模板渲染
├── data/
│   └── hospitals.json        # 医院数据（900+）
├── i18n/
│   ├── zh.json               # 中文
│   ├── en.json               # 英文
│   ├── ja.json               # 日文
│   └── th.json               # 泰文
├── templates/
│   └── booking.tpl           # 预约流程模板
├── docs/
│   └── clinics/              # 静态页面（自动生成，GitHub Pages）
├── scripts/
│   └── generate-md.js        # 静态页面生成脚本
├── SKILL.md                  # Skill 元数据（clawhub）
└── skill.json                # Skill 配置
```

---

## 医院数据

医院数据存放在 `data/hospitals.json`，字段说明：

```json
{
  "id": 1,
  "name": "韩国JD皮肤科",
  "en_name": "JD Skin Clinic",
  "alias": "JD皮肤科",
  "aliases": ["jd皮肤科", "韩国jd", "jd"],
  "url": "https://i.beautsgo.com/cn/hospital/jd-skin-clinic",
  "category": "皮肤科"
}
```

新增医院只需在 `hospitals.json` 中添加记录，推送后 GitHub Actions 自动重新生成静态页面。

---

## 匹配策略

采用四级匹配，优先级从高到低：

1. **精确匹配** — 完全匹配 name / en_name / alias
2. **拼音精确匹配** — 全拼或首字母完全匹配（仅中文字符部分）
3. **中文名模糊匹配** — 查询词包含在医院名中
4. **其他字段模糊匹配** — 英文名、别名、拼音含查询词

最小匹配长度 2 个字符，防止单字误匹配。

---

## 静态页面生成

```bash
npm run generate        # 生成中文版
npm run generate:all    # 生成所有语言版本（zh/en/ja/th）
```

生成的页面位于 `docs/clinics/` 目录，部署到 GitHub Pages 供搜索引擎收录。

---

## 相关链接

- 🔗 [clawhub 技能主页](https://clawhub.ai/BeautsGO/korean-booking)
- 📱 [BeautsGO 官网](https://beautsgo.com)
- 🍎 [iOS App Store](https://apps.apple.com/cn/app/beautsgo%E5%BD%BC%E6%AD%A4%E7%BE%8E-%E9%9F%A9%E5%9B%BD%E7%9A%AE%E8%82%A4%E7%A7%91%E9%A2%84%E7%BA%A6/id6741841509)
- 🤖 [Google Play](https://play.google.com/store/apps/details?id=uni.UNIEF980DB)
