# layman-translator

[![skills.sh](https://skills.sh/b/shxuk/layman-translator)](https://skills.sh/shxuk/layman-translator)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Python](https://img.shields.io/badge/python-%3E%3D3.8-green.svg)](./scripts/style_check.py)

简体中文 | [English](./README.en.md)

> **一句话定义**：`layman-translator` 是一个开源的**中文技术写作「去 AI 味」工作流 Agent Skill + 零依赖 Python 质检脚本集**，把 AI 味浓重的技术初稿改写成面向新手、事实锚严格对齐的干净中文文档，纯标准库本地运行、不联网。
> 适合**技术书作者、开源文档维护者、知识库写作者**；不适合**外文直译、从零无中生有创作**。

---

## 30 秒上手

```bash
# 1) 安装进 AI 助手技能目录（Claude Code / Cursor / Trae / Antigravity）
npx skills add shxuk/layman-translator

# 2) 仅跑本地零依赖 Python 质检脚本（无需 pip install）
python scripts/style_check.py path/to/draft.md
python scripts/fact_anchor_check.py path/to/01_原稿.md path/to/02_二创稿.md
```

| 场景 | 怎么用 | 需要什么 |
|---|---|---|
| **AI 助手工作流** | `npx skills add shxuk/layman-translator` 后对 AI 说「用 layman-translator 去 AI 味」 | 支持 Agent Skills 的 IDE |
| **本地脚本独立质检** | `git clone https://github.com/shxuk/layman-translator.git` 后直接跑 `scripts/*.py` | Python ≥ 3.8（零三方依赖） |

---

## 它解决什么问题

用大模型辅助写技术教程或书稿时，初稿往往自带浓重的「AI 写作腔」与排版隐患：
- **高频 AI 套话**：`综上所述`、`值得一提的是`、`不是 X 而是 Y`、`赋能 / 抓手 / 闭环 / 颗粒度`、滥用破折号 `——` 等。
- **冗余元叙述**：`值得先看清楚`、`接下来我们看` 等替读者排序、替读者下判断的废话。
- **口径与排版割裂**：中英文混排缺空格、直角引号 `「」` 与弯引号 `“”` 混用、术语大小写不统一（`mcp` / `MCP`）。
- **改写失真风险**：人工或 AI 润色后，容易把原稿中的数字、命令、路径、专有名词改丢或擅自脑补新论据。

---

## 能做什么（四道标准化流水线）

1. **第零道 · 格式统一**：只改口径与排版（术语大小写、引号、错别字），不动语义（依据 `references/风格手册.md` + `format_check.py`）。
2. **第一道 · 去 AI 味改写**：消除翻译腔与语病，面向零基础读者讲透逻辑（依据 `references/改写规则.md`、`症状目录.md`、`保护边界.md`）。
3. **第二道 · 减法（只删不添）**：专扫元叙述、假口语、重复升华与孤儿句，严禁新增原稿没有的观点或例子。
4. **第三道 · 复核与修正**：通过 `fact_anchor_check.py` 核对数字/代码/专名差集，结合 `style_check.py` 与 `毛病词典.md`（21 条）复核，仅在存在实质逻辑风险时输出 `复核报告.md`。

---

## 不能做什么

`layman-translator` **明确不负责**：
- 不做外文到中文的常规翻译；
- 不做没有原稿的从零创作或续写；
- 不替文章重新立论、不新增原稿没有的论据或数据；
- 检测到疑似真实凭证（API key / 私钥 / cookie）时立即中止处理。

---

## 工作原理

```text
01_原稿.md → [第零道 格式统一] → [第一道 去AI味改写] → [第二道 只删不添] → [第三道 事实锚与文风脚本复核] → 02_二创稿.md + 复核报告.md
```

---

## 项目事实

| 项 | 值 |
|---|---|
| 版本 | `1.0.0` |
| 许可 | MIT |
| 运行时 | Python ≥ 3.8 |
| 第三方依赖 | 0 个（纯 Python 标准库：`re`、`sys`、`pathlib`） |
| 核心脚本 | `format_check.py`、`fact_anchor_check.py`、`style_check.py`、`consistency_check.py` |
| 规则参考库 | `references/` 下 9 份独立规则文件（风格手册、症状目录、毛病词典等） |
| 不支持 | 外文翻译、无中生有创作、自动覆盖原稿 |

---

## 给 AI Agent 的速览

```text
名称：layman-translator
类型：Agent Skill + 零依赖 Python 质检脚本
作用：将 AI 味较重的中文技术初稿按四道工序去 AI 味、统一口径并对齐事实锚
何时使用：用户说"去AI味/消除翻译腔/改写技术章节/二创原稿/统一术语口径"时
何时不用：外文翻译、从零无中生有写作、常规润色
入口：SKILL.md（与本段及 llms.txt 同义）
依赖：Python >= 3.8，0 第三方依赖
安装：npx skills add shxuk/layman-translator
```

---

## 仓库结构

<details>
<summary>展开查看</summary>

```text
layman-translator/
├── SKILL.md                      # Agent 核心技能定义、工序边界与文件契约
├── llms.txt                      # 机器可读结构化摘要
├── README.md / README.en.md      # 中英双语文档
├── references/                   # 改写、减法与复核的规则库（唯一权威）
│   ├── 风格手册.md               # 术语统一表、标题层级、标点符号与错别字规范
│   ├── 改写规则.md               # 第一道重写流程与按需参考路由
│   ├── 症状目录.md               # AI 味与删除类症状清单
│   ├── 毛病词典.md               # 第三道复核 21 条核心判据
│   ├── 保护边界.md               # 代码块、引语、作者声口及功能性修辞豁免边界
│   ├── 白名单.md                 # 允许放行的特定表达白名单
│   ├── 品牌文案.md               # 品牌与产品口径规范
│   ├── 平台模式.md               # 不同发布平台的适配模式
│   └── 示例.md                   # 改写前后对照示例
└── scripts/                      # 零依赖 Python 自动化质检脚本
    ├── format_check.py           # 格式与口径扫描（第零道）
    ├── fact_anchor_check.py      # 原稿 vs 二创稿事实锚差集复核
    ├── style_check.py            # 可疑 AI 腔与高危文风正则扫描（第三道）
    └── consistency_check.py      # 跨篇一致性扫描
```

</details>

---

## 贡献与 License

欢迎提交 [Issue](https://github.com/shxuk/layman-translator/issues) 或 PR 补充高频「AI 味」词条、错别字对照表或扩展 `scripts/` 检测规则。  
[MIT](./LICENSE)
