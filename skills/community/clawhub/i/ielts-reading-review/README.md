# IELTS Reading Review 雅思阅读复盘助手

> Finish a reading passage, hand it to AI, get a complete review — error analysis, synonym tracking, vocabulary tagging, and mistake pattern detection, all in one go.

做完阅读题，丢给 AI，自动出复盘笔记——错题拆解、同义替换积累、考点词标注、易错模式追踪，一步到位。

---

## 🆕 What's New in v5.4 — OAuth 风格浏览器授权流

**告别 F12 复制 token 的笨流程**——客户端模式绑定账号体验彻底重做：

### 🎯 30 秒上手（替代原来 5 分钟）

```bash
bash ~/.workbuddy/skills/ielts-reading-review/scripts/setup-client-mode.sh
```

脚本自动完成 4 件事：

1. **本机起临时 HTTP 服务**（随机空闲端口监听 OAuth 回调）
2. **唤起浏览器**到 `https://www.liuxue.online/ielts/authorize.html`
3. **页面显示 OAuth 风格卡片**：客户端名 / 本机回调地址 / 当前账号 / 权限列表 / 【拒绝】【授权】
4. **点【授权】** → token 通过 `<img>` 请求回传本机 → 自动写入 `~/.zshrc` → 显示绑定账号名

### 🔒 安全设计

| 风险点 | 防护机制 |
|---|---|
| token 被中间人截获 | 全程仅浏览器 ↔ 本机 127.0.0.1，不走第三方 |
| token 进 URL bar 被记录 | 用 `<img src=...?token>` GET 而非 `location.href`，不留浏览历史 |
| CORS / Private Network 拦截 | 用图片请求绕过预检 |
| 跨站伪造请求 | `secrets.token_urlsafe(16)` 生成 state，服务端校验 |
| 恶意回调地址 | 授权页强制白名单：仅 `127.0.0.1 / localhost / ::1` + http |

### 🪟 三系统全覆盖

- macOS：`open` 命令唤起浏览器
- Linux：`xdg-open`
- 兜底：打印链接，用户手动复制到浏览器

### 🛟 兜底模式

浏览器/网络异常时：

```bash
bash setup-client-mode.sh --manual
```

回退到 F12 → Console → `localStorage.ielts_user_token` 复制粘贴的老流程。

---

## 🆕 What's New in v3.1 — Web Hand-off

### 🌐 生成物一键上传到 Web 端

v3.1 在保持纯离线生成的同时，**明确了 JSON 产出物与 Web 端的对接路径**：

- 访问 https://www.liuxue.online/ielts/submit.html 切到「**上传 JSON**」Tab
- 把 skill 生成的 `.json` 文件拖进去 → 成绩、答案、用时自动入库
- 首页成绩矩阵、词汇本、同义替换本实时更新

### 📊 Web 端新增 JSON 导入能力

Web 端 `submit.html` 新增第 4 种提交模式（粘贴文本 / PDF / 拍照 / **上传 JSON**），与 skill 的产出物严格对齐 v3.0 schema。

## 🆕 What's New in v3.0 — Offline-First

### 🔌 去服务器依赖，纯本地生成

v3.0 重构为**纯离线模式**：

- ✅ 复盘 HTML — 专业排版，浏览器直接查看
- ✅ 复盘 PDF — 一键导出，存档分享
- ✅ 结构化 JSON — 包含成绩、错题、词汇、同义替换等全量数据
- 🔜 数据上传 — 后续通过 Web 端功能将 JSON 导入云系统，实现多设备同步

**不再依赖任何远程 API**，AI Agent 在本地完成所有分析和生成工作。

### 📋 填空回填 4 步检查

每道填空题强制 4 步验证：语法 → 词性 → 语义 → 字数，杜绝低级失误。

### ✅ 正确题确认 + 进步表扬

- 做对的题也会简要确认，展示同义替换映射帮你强化记忆
- 每篇开头先肯定你的进步点，保持刷题动力

### 🔢 错误分类扩展到 12 类

涵盖：同义替换识别失败、NG/FALSE 混淆、过度推理、填空重复题干、语法误解、选项不完全匹配、词汇缺口、粗心、词形错误、跨代/范围混淆、类别推理误判、邻近干扰词。

---

## 🚀 快速开始（3 步上手）

### 第一步：安装 Skill

```bash
# ClawHub 安装（推荐）
clawhub install ielts-reading-review

# 或手动复制到 skills 目录
cp -r ielts-reading-review ~/.workbuddy/skills/
```

### 第二步：做完一篇阅读题

用剑桥雅思真题（Cambridge IELTS）做完一篇阅读，准备好：
- ✅ 原文（拍照/截图/粘贴文字都行）
- ✅ 正确答案
- ✅ 你的答案（标出哪些做错了）
- ⭕ 可选：翻译、用时

### 第三步：发给 AI，说"帮我复盘"

就这么简单。AI 会自动生成：
1. **复盘 HTML** — 专业排版的复盘笔记
2. **复盘 JSON** — 结构化数据文件，供后续导入 Web 系统
3. **复盘 PDF**（可选）— 从 HTML 生成，便于存档

---

## 📖 完整使用案例

> 以下是一个真实的使用过程，以剑4 Test 3 Passage 1 为例。

### 你发给 AI 的内容

```
我做完了剑4 Test3 Passage1，帮我复盘。

文章：Micro-Enterprise Credit for Street Youth
用时：34:40
得分：7/13

我的答案 vs 正确答案：
Q1: 我选D → 正确A
Q2: 我选C → 正确D
Q3: ✅
Q4: ✅
Q5: 我填 Sudan and India → 正确 Sudan
Q6: ✅
Q7: 我填 shoe shine → 正确 Shoe Shine Collective
Q8-Q10: ✅
Q11: 我选 NOT GIVEN → 正确 NO
Q12: ✅
Q13: 我选D → 正确A

（然后把原文和翻译也贴上来）
```

### AI 自动产出

AI 会在本地生成三个文件：

#### 📄 复盘 HTML — `剑4-Test3-Passage1-街头青年信贷复盘.html`

包含以下模块：
- 得分总览 + Band 分换算 + 核心问题一句话
- 进步点肯定
- 逐题错因分析（定位原文、映射同义替换、分类错因、给出教训）
- 正确题确认
- 同义替换积累表
- 考点词表
- 核心问题总结
- 行动清单

#### 📊 结构化 JSON — `剑4-Test3-Passage1-街头青年信贷复盘.json`

```json
{
  "version": "3.0.0",
  "source": { "book": 4, "test": 3, "passage": 1 },
  "score": { "correct": 7, "total": 13, "band": "5.0" },
  "wrongQuestions": [...],
  "synonyms": [...],
  "vocabulary": [...],
  "problems": [...]
}
```

后续可通过 Web 端将此 JSON 上传到云系统，实现多设备同步和进度追踪。

#### 📑 复盘 PDF（可选）

```bash
node scripts/generate-pdf.js 剑4-Test3-Passage1-街头青年信贷复盘.html
```

---

## 🎯 Features

| 功能 | 说明 |
|------|------|
| **逐题错因分析** | 定位原文、映射同义替换、分类错因（12 类）、给出 1 句话教训 |
| **正确题确认** | 正确答案也简要展示同义替换映射，强化记忆 |
| **同义替换积累** | 自动提取题目-原文同义替换对，跨篇持续积累 |
| **考点词标注** | 基于刘洪波 538 考点词（⭐⭐⭐/⭐⭐/⭐）+ COCA 5000 词频 |
| **易错模式追踪** | 跨篇检测反复犯的错 |
| **📋 填空回填检查** | 每道填空题 4 步强制验证（语法/词性/语义/字数） |
| **📊 打分 & Band 换算** | 原始分→雅思 Band 分数换算（学术类） |
| **📄 结构化 JSON 输出** | 成绩、错题、词汇、同义替换全量数据，供 Web 系统导入 |
| **HTML + PDF 输出** | 排版专业的复盘笔记，支持打印和存档 |

## 📂 File Structure

```
ielts-reading-review/
├── SKILL.md                          # Skill 定义（AI 读这个文件理解工作流）
├── README.md                         # 使用说明（你正在看的这个）
├── assets/
│   ├── review-template.html          # HTML 模板 + CSS 样式
│   └── bilingual-template.html       # 双语对照页面模板
├── references/
│   ├── error-taxonomy.md             # 12 类错误分类体系
│   ├── 538-keywords-guide.md         # 考点词评级指南
│   ├── score-band-table.md           # 分数→Band 换算表
│   └── review-style-guide.md         # 写作风格规范
└── scripts/
    └── generate-pdf.js               # PDF 生成脚本
```

## 🧠 内置做题方法论

### T/F/NG 三步判断法
1. **找话题** — 原文有没有讨论题目说的这个话题？→ 没有 → **NOT GIVEN**
2. **找立场** — 如果话题存在，作者同意还是反对？→ **TRUE** / **FALSE**
3. **验证** — "如果我选 TRUE/FALSE，能指出原文哪一句吗？"指不出来 → 大概率 **NOT GIVEN**

### 填空题防重复规则
答案不要重复题目中已有的词。填完后把答案放回原句完整读一遍。

### 选择题逐词验证法
选项中的**每个关键词**都要在原文找到对应。"大致相关" ≠ "能选"。前半句对但后半句多了信息 → 干扰项。

## 📤 数据导入 Web 系统

v3.1 起，生成的 JSON 文件可**直接通过 Web 端导入**（已上线）：

### 方式 1：Web 端拖拽上传（推荐）

1. 访问 **https://www.liuxue.online/ielts/submit.html**
2. 登录账号（第一次使用会引导注册）
3. 切换到顶部 Tab「**📊 上传 JSON**」
4. 把 skill 生成的 `.json` 文件拖入上传区（或点击选择）
5. 点「导入到我的记录」

导入成功后，以下页面会自动刷新：
- **首页成绩矩阵** — 新篇目变绿，显示得分
- **词汇本** — JSON 中的考点词自动合并
- **同义替换本** — JSON 中的同义替换对自动入库
- **个人中心** — 统计总数、均分、Band 分更新

### 方式 2：命令行批量上传（进阶）

需要额外安装 `ielts-server-sync` skill（作者个人维护，不公开发布）：

```bash
# 单文件
node ~/.workbuddy/skills/ielts-server-sync/scripts/upload.js 剑5-T1-P2.json
# 批量
node ~/.workbuddy/skills/ielts-server-sync/scripts/upload.js --batch ./reviews/
# 查服务器记录
node ~/.workbuddy/skills/ielts-server-sync/scripts/upload.js --status
```

### 方式 3：HTML 本地存档

直接双击生成的 `.html` 文件，浏览器打开即可阅读 / 打印，不依赖任何服务器，隐私可控。

## 👤 Who It's For

雅思备考者，尤其是：
- 阅读 5-7 分想突破的
- 复盘效率低，做完题不知道怎么分析的
- 同样的错反复犯，需要系统追踪的
- 想把词汇积累和真题练习结合起来的

## ⚙️ Requirements

- 支持 SKILL.md 的 AI Agent（如 OpenClaw、Claude Code、WorkBuddy/CodeBuddy）
- PDF 导出需要：Node.js + puppeteer-core + 本地 Chrome（可选，不装也能用 HTML）

## 🤝 Contact & Feedback

If this Skill helps your IELTS prep, a ⭐ Star would mean a lot!

如果这个 Skill 对你备考有帮助，欢迎点个 ⭐ 支持！

- 💡 **Feature requests / Bug reports**: [Open an Issue](https://github.com/dengjiawei1226/ielts-reading-review/issues)

## License

MIT-0
