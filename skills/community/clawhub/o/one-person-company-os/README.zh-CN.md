# One Person Company OS

[English](./README.md) | [简体中文](./README.zh-CN.md)

**面向 AI 一人创始人的可视化经营驾驶舱。**

One Person Company OS 帮一个创始人把 AI 产品想法变成可以持续检查、推进和跨会话交接的一人公司。它始终看住这条经营闭环：

`价值承诺 -> 买家 -> 产品能力 -> 交付 -> 回款 -> 学习 -> 资产`

第一个工作区围绕创始人今天真正要回答的问题建立：

- 我现在能卖的承诺是什么？
- 第一批买家是谁？
- 当前最大瓶颈是什么？
- 下一步主战场在销售、产品、交付、回款还是资产？
- 今天最短、最该推进的动作是什么？
- 哪些文件已经真实保存在我批准的工作区里？

## 你会得到什么

- 下载后可直接打开的本地经营驾驶舱
- 适合持续编辑和角色协作的 Markdown 工作面
- 用于正式交付和归档的编号 DOCX 文件
- 经营闭环图和成交管道图等确定性 SVG 视觉资产
- 与同一经营闭环一致的角色 brief、提醒规则、流程说明和起始交付件
- 可选的 AI 图片提示词，用于封面、发布帖和宣发视觉

## 工作区模型

生成后的工作区分三层：

- **HTML 阅读层**：下载后优先查看和导航
- **Markdown 工作层**：持续编辑和智能体协作
- **DOCX 交付层**：`产物/` 或 `artifacts/` 下的正式输出

中文工作区会包含：

- `阅读版/00-经营驾驶舱.html`
- `视觉素材/business-loop.svg`
- `视觉素材/revenue-pipeline.svg`
- `视觉素材/ai-image-prompts.md`

英文工作区会包含：

- `reading/00-operating-cockpit.html`
- `visual-kit/business-loop.svg`
- `visual-kit/revenue-pipeline.svg`
- `visual-kit/ai-image-prompts.md`

机器状态固定隐藏在 `.opcos/state/current-state.json`。

## 安全边界

- 脚本模式需要本机已有 `Python 3.7+`
- `scripts/ensure_python_runtime.py` 只输出兼容性与手动安装建议
- marketplace 版不会自动安装系统级依赖
- 所有生成文件只写入创始人批准的工作区
- 正常使用不需要 API key 或无关凭据
- AI 图片是可选创作资产，不是核心运行依赖

## 本地命令

```bash
python3 scripts/preflight_check.py --mode 创建公司
python3 scripts/ensure_python_runtime.py
python3 scripts/init_business.py "北辰实验室" --path ./workspace --product-name "北辰助手" --target-user "独立开发者" --core-problem "还没有一个真正能持续推进产品和成交的一人公司系统" --product-pitch "一个帮助独立开发者把产品做出来并卖出去的一人公司控制系统" --confirmed
python3 scripts/validate_release.py
```

## 一行安装

```bash
clawhub install one-person-company-os
```

## 一行启动

```text
我正在创建一个 AI 一人公司，请调用 one-person-company-os v1.0。先帮我确认可卖承诺、第一批买家和核心问题；确认后在我批准的本地目录创建工作区，用经营驾驶舱作为入口，直观展示当前瓶颈，并且只把批准后的文件保存到这个工作区内。
```

## 校验

```bash
python3 scripts/validate_release.py
```

它会校验状态模型、双语工作区、经营驾驶舱、视觉素材、DOCX-only 产物目录、角色/模板语言和公开发布物料。
