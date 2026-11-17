<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/default-banner.png">
    <source media="(prefers-color-scheme: light)" srcset="assets/default-banner.png">
    <img alt="mu-mbti-job" src="assets/default-banner.png" width="100%">
  </picture>
</p>

# 🧬 mu-mbti-job · MBTI人格与职业测评

> 三档深度（70/93/144 题）的中英双语 MBTI 人格与职业测评，输出专业 PDF 报告 —— 纯本地运行，核心零依赖。

[English](README.md) | **中文** | [🌐 在线主页](https://muippt.github.io/mu-mbti-job/)

[![微信公众号](https://img.shields.io/badge/muippt-07C160?logo=wechat&logoColor=white)](https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA)
[![小红书](https://img.shields.io/badge/muippt-FF2442?logo=xiaohongshu&logoColor=white)](https://xhslink.com/m/ESxtgUNMdl)
[![书籍](https://img.shields.io/badge/书籍-图解团队管理-BBDDE5?logo=bookstack&logoColor=white)](https://item.m.jd.com/product/14547345.html)
[![mu-skill集合](https://img.shields.io/badge/mu--skill集合-9E95B7?logo=refinedgithub&logoColor=white)](https://muippt.github.io/mu-skill-hub/)
[![License](https://img.shields.io/github/license/muippt/mu-mbti-job)](LICENSE)
[![Version](https://img.shields.io/github/v/release/muippt/mu-mbti-job)](https://github.com/muippt/mu-mbti-job/releases)
[![Stars](https://img.shields.io/github/stars/muippt/mu-mbti-job)](https://github.com/muippt/mu-mbti-job/stargazers)

### 💡 使用场景示例

- 🧬 **个人深度自评** —— 快速版 70 题 / 标准版 93 题 / 专业版 144 题，10–25 分钟完成
- 📄 **中英双语 PDF 报告** —— 四维度分析、人格画像、职业岗位推荐、人际匹配，双语对照排版
- 👥 **团队组建分析** —— 聚合多位成员结果，生成团队分布热力图与互补配对建议
- 💼 **职业方向参考** —— 每种类型 4 个适配岗位，附推荐理由与发展建议
- 🤝 **人际匹配洞察** —— 最佳搭档型与挑战型，附具体协作策略
- 🔄 **随时断点续答** —— 答题页自动保存进度，答题中途可切换中英文
- 🏠 **无服务器团队聚合** —— 对话粘贴回传或文件夹批量，一条命令出团队报告

---

### ✨ 核心亮点

#### 📊 三档题库深度

| 档位 | 题数 | 时长 | E/I · S/N · T/F · J/P |
|------|------|------|------------------------|
| 快速版 | 70 | ~10 分钟 | 16 · 19 · 18 · 17 |
| 标准版 | 93 | ~15 分钟 | 21 · 26 · 24 · 22（Form M 结构） |
| 专业版 | 144 | ~25 分钟 | 32 · 40 · 38 · 34 |

一份 144 题双语超集题库（`data/questions.json`），通过 `version_added` 标记严格划分子集。计分引擎启动时校验维度题数，不匹配立即报错（fail loud），绝不静默出错。

#### 📑 双报告模式

| 报告 | 页数 | 内容 |
|------|------|------|
| 个人报告 | 5 | 封面、四维度分析、人格特征（核心特征/优势盲区/工作风格/决策方式/压力反应/沟通偏好）、职业岗位推荐、人际匹配 |
| 团队报告 | 6 | 封面、成员概览、16 型分布+特征速览、四维度团队热力、团队优势与盲区、协作建议与互补配对 |

#### 📄 报告截图范例

| 封面 | 四维度分析 | 职业岗位推荐 |
|------|------------|--------------|
| ![封面](assets/report-page1.png) | ![四维度](assets/report-page2.png) | ![职业推荐](assets/report-page4.png) |

---

### 📌 与同类工具对比

| 维度 | 🧭 mu-mbti-job | 16personalities | 在线 MBTI 仿站 |
|------|----------------|-----------------|--------------------|
| 本地运行，答案不出设备 | ✅ | ❌ | ❌ |
| 中英双语报告 | ✅ | 部分 | ❌ |
| 三档深度（70/93/144 题） | ✅ | ❌ | ❌ |
| 团队聚合报告 | ✅ | ❌ | ❌ |
| 清晰度指数 + Top3 相似类型 | ✅ | ❌ | 少见 |
| 专业 PDF 输出 | ✅ | 付费墙 | ❌ |
| 核心零依赖 | ✅ | — | — |

---

### 🚀 五大工作流

| 工作流 | 场景 | 触发方式 |
|--------|------|---------|
| 个人测评 | 想了解自己的人格类型与职业适配 | 对 Agent 说 "MBTI" / "测一下MBTI"，或直接跑 CLI |
| 团队分析 | 团队负责人想基于成员结果做团队画像 | 说 "团队分析"，或运行 `team_pipeline.py` |
| 断点续答 | 答到一半暂停，稍后回来继续 | 重新打开 quiz.html，进度自动恢复 |

**交互模式**（叠加在个人测评之上）：

| 模式 | 适合 | 工作方式 |
|------|------|---------|
| 卡片式 | 与 AI Agent 对话中 | 题目渲染为可点选的选项卡片 |
| 对话式 | 纯文本宿主 | 每条消息一题，回复 A/B |
| 网页式 | 长测试、团队、桌面端 | 生成 quiz.html，支持自动保存、中英切换、一键复制答案回传 |

---

### ⚙️ 技术规格

| 项目 | 说明 |
|------|------|
| 类型 | AI Agent Skill + 独立 Python CLI |
| 依赖 | 核心零依赖（Python 3.9+ 标准库）；可选 `weasyprint` / `reportlab` |
| 兼容环境 | macOS / Linux / Windows（Python 3.9+；无头 PDF 需 Chrome 或 Edge） |
| 文件结构 | `data/`（题库、16 型画像、职业映射）+ `scripts/`（4 个 CLI 工具）+ `references/` |
| 输入 | 答案 JSON（网页导出、卡片模式或手动） |
| 输出 | 中英双语 PDF 报告（个人/团队）、计分结果 JSON |
| 语言 | 中文 / English（题目、报告、界面） |
| 版本 | 1.1.1 |
| 许可证 | MIT |

---

### 🛠️ 快速开始

**① 安装**

```bash
git clone https://github.com/muippt/mu-mbti-job.git ~/.claude/skills/mu-mbti-job
```

> 其他 Agent 可改用其约定的 skill 目录，或项目级 `.claude/skills/mu-mbti-job`。

**② 验证**

重启 / 重新加载 Agent 后，输入：

```
列出我当前可用的 Skills
```

**③ 使用**

```
我想做一个 MBTI 测评，看看我的性格类型和职业方向 —— 请用 mu-mbti-job。
```

也可以直接进入指定工作流：

```
帮我给团队的 5 位成员做一次 MBTI 团队分析。
```

```
生成专业版 144 题的英文答题页面。
```

不依赖 Agent 的独立 CLI 用法：

```bash
python3 scripts/build_quiz_page.py --version quick -o quiz.html   # 生成答题页
python3 scripts/score.py answers.json -o result.json              # 计分
python3 scripts/generate_report.py result.json -o report.pdf      # 生成 PDF
python3 scripts/team_pipeline.py ./team_answers/ -o team.pdf      # 团队模式
```

---

### 🔒 安全与隐私

- **全程本地** —— 答题页是单个静态 HTML 文件；计分和 PDF 生成都是离线脚本
- **无遥测、无账号、无数据采集** —— 什么都不上传
- **答案属于你** —— 纯 JSON 文件，可查看、可保留、可删除

> ⚠️ 测评结果仅供自我认知参考。MBTI 属于类型学工具而非临床诊断量表，不可用于招聘、晋升、绩效等人事决策。

---

### ⭐ Star 趋势

如果这个工具帮到了你或你的团队，欢迎点个 ⭐ —— 让更多人发现这个尊重隐私的 MBTI 测评。

[在 Star History 查看](https://www.star-history.com/?repos=muippt%2Fmu-mbti-job&type=date) — 有 star 数据后将更新趋势图。

> 三档深度、双语 PDF、团队模式 —— 全部离线完成。

---

### 👤 作者简介

🎓 清华大学出版社签约作家 / 2026当当影响力作家 / 某互联网大厂 AI 大模型业务 HR 砖家 / 一级人力资源管理师 / 二级心理咨询师 / 野生设计师

📚 著有[《图解团队管理》](https://item.m.jd.com/product/14547345.html)，服务客户有字节跳动、腾讯、百度、中国移动、SMG、BOE…

💡 [微信公众号](https://mp.weixin.qq.com/s/YLtXENt_7WzO2DgJCFUtPA) / [小红书](https://xhslink.com/m/ESxtgUNMdl)：muippt

### 📄 许可证与致谢

[MIT](LICENSE) © 2026 muippt

- 题库维度结构参考 MBTI Form M 题量分布（标准版 E/I 21、S/N 26、T/F 24、J/P 22）
- 灵感来自开源 MBTI 项目，以及对隐私优先替代方案的追求

> 声明：本项目大部分内容由 AI 辅助完成。如您认为您的作品被使用但未获得适当署名，请提交 issue。
