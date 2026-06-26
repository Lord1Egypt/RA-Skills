# ${repo_name}

> ${description}

**创建者**：@${created_by}　｜　**创建日期**：${created_date}　｜　**仓库地址**：${gitea_url}/${org}/${repo_name}

---

## 参与成员

${members}

> 各成员详细分工和技术背景请查阅 [`profiles/`](./profiles/) 目录下的个人档案。

---

## 目录说明

本仓库采用统一的标准目录结构，请所有成员严格按照以下规范存放文件：

| 目录 | 用途 | 文件命名建议 |
|------|------|------------|
| `meeting/` | 每次会议的纪要和讨论记录 | `YYYY-MM-DD-会议主题.md`，例如 `2026-04-01-kickoff.md` |
| `docs/` | 需求文档、设计文档、周报等 | `需求文档-v1.md`、`周报-第1周.md` |
| `src/` | 所有代码文件 | 按模块建子目录，例如 `src/perception/` |
| `data/` | 训练数据、实验数据说明 | 不上传原始大文件，上传数据说明文档或链接 |
| `reports/` | 阶段总结、实验报告 | `阶段一总结.md`、`实验报告-20260401.md` |
| `profiles/` | 成员档案，记录各成员的分工、职责和技术能力 | `用户名.md`，例如 `mayidan.md` |

> ⚠️ **请不要在根目录直接存放业务文件**，保持根目录整洁。

---

## 成员档案说明

`profiles/` 目录下每位成员都有一个个人档案文件，内容包括：
- 负责模块
- 主要职责
- 技术能力
- 备注

**请各成员在加入仓库后尽快补充自己的档案文件**，方便其他人了解分工，减少沟通成本。

---

## 会议纪要上传规范

每次会议结束后，请将纪要上传至 `meeting/` 目录：

1. 文件格式：Markdown（`.md`）
2. 文件命名：`YYYY-MM-DD-主题关键词.md`
3. 内容建议包含：时间、参会人员、讨论内容、决议事项、下次会议时间

示例文件名：`2026-04-01-项目启动会.md`

---

## 分支命名规范

| 类型 | 命名格式 | 示例 |
|------|----------|------|
| 功能开发 | `feature/简短描述` | `feature/tactile-sensor` |
| 问题修复 | `fix/简短描述` | `fix/motor-control-bug` |
| 实验 | `exp/实验名称` | `exp/training-v2` |
| 文档 | `docs/文档名称` | `docs/update-readme` |

- 主分支 `main` 为稳定版本，**不要直接向 main 推送**
- 开发完成后通过 Pull Request 合并到 main

---

## Issue 使用说明

- **任务类**：使用标签 `task`，标题格式 `【任务】描述`
- **问题类**：使用标签 `bug`，标题格式 `【问题】描述`
- **讨论类**：使用标签 `discussion`，标题格式 `【讨论】描述`

请在 Issue 中明确描述背景、期望结果和截止时间，并 Assign 给负责人。

---

## 快速开始

1. Clone 仓库：`git clone ${gitea_url}/${org}/${repo_name}.git`
2. 阅读本 README 了解目录结构和规范
3. 查看 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解协作流程
4. 补充 `profiles/你的用户名.md` 中的个人档案
5. 认领 [启动任务 Issue](${gitea_url}/${org}/${repo_name}/issues) 并开始工作

---

*本 README 由 AIFusion Bot 自动生成，请在此基础上补充项目特定内容。*
