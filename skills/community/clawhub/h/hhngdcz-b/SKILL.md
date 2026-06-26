---
name: project-doc-gen
description: 分析当前项目代码库，自动生成全面的技术文档（项目概览、架构设计、模块说明、API 文档、数据模型、依赖关系、部署说明），输出到 docs/ 目录。通过 subagent 并行分析，适用于任意规模的项目。
license: MIT
metadata:
  author: zhouhe
  version: "3.1"
---

分析当前项目代码，生成全面的技术文档到 `docs/` 目录。通过 general-purpose subagent 并行分析代码库并用 Write 工具写入文件，返回值只含摘要。

**输入**：空（整个项目）| 子目录路径 | 逗号分隔的模块名称列表

**输出**：`docs/` 目录下的 README.md、architecture.md、modules/*.md、api.md、data-model.md、dependencies.md、deployment.md

---

## 核心架构

```
主 agent（协调者，不读源码、不读文档内容）
  ├── 步骤 1: 预检 + 顶层扫描 + 智能分组 + 用户确认
  ├── 步骤 2: general-purpose subagent 并行（模块文档 + 依赖/部署文档，每批最多 5 个）
  ├── 步骤 3: general-purpose subagent 并行（架构 + API/数据模型文档）
  └── 步骤 4: 主 agent 写 README.md + Glob 验证 + 总结
```

**关键原则**：
1. subagent 统一用 `general-purpose` 类型，通过 Write 工具写入文件
2. subagent 返回值只含一行摘要，绝不回传文档全文
3. 主 agent 绝不读源码，也绝不读 subagent 生成的文档内容
4. 小模块合并、大模块裁剪，subagent 总数控制在 5-8 个

---

## 步骤 1：预检、扫描、分组与用户确认

**1a. 预检**：检查 `docs/` 是否存在。已有文档时用 AskUserQuestion 让用户选择：覆盖重写（推荐）/ 仅补充 / 取消。

**1b. 读取项目元数据**：查找 `pyproject.toml`、`package.json`、`Cargo.toml`、`go.mod`、`pom.xml`、`build.gradle`、`*.csproj`、`CMakeLists.txt`。读取 `README.md` 和 `CLAUDE.md`（如有）。

**1c. 顶层结构扫描**（仅 Glob，不读文件内容）：
- 列出所有源码文件路径
- 排除：`.git`、`.venv`、`.env`、`.claude`、`.idea`、`.vscode`、`node_modules`、`vendor`、`target`、`build`、`dist`、`__pycache__`、`docs/`
- 按目录结构划分模块分组，记录文件路径和数量

**1d. 智能分组合并**（目标 5-8 个 subagent）：

| 规模 | 文件数 | 策略 |
|------|-------|------|
| 小 | ≤ 5 | 合并 2-3 个到同一 subagent |
| 中 | 6-20 | 单独一个 subagent |
| 大 | > 20 | 单独一个 subagent，裁剪：优先入口/API/类型文件，跳过测试/mock/迁移 |

**1e. 用户确认**：AskUserQuestion 展示分组结果，用户可增删改。

**1f. 创建目录**：`mkdir -p docs/modules`

如果输入是路径则仅扫描该路径；如果输入是模块名列表则跳过 1c/1d/1e。

---

## 步骤 2：并行生成模块文档 + 依赖/部署文档

用 TaskCreate 跟踪进度。每批最多 5 个 general-purpose subagent 并行启动：

- **模块文档 subagent** × N — prompt 模板见 `prompts/module-doc.md`
- **依赖+部署文档 subagent** × 1 — prompt 模板见 `prompts/deps-deploy.md`

每批完成后用 Glob 确认文件写入。

---

## 步骤 3：并行生成全局文档

模块文档全部完成后，最多 2 个 general-purpose subagent 并行：

- **架构文档 subagent** — prompt 模板见 `prompts/architecture.md`
- **API+数据模型文档 subagent** — prompt 模板见 `prompts/api-datamodel.md`

---

## 步骤 4：验证与生成入口文档

a. Glob 确认 `docs/**/*.md` 全部写入
b. 主 agent 直接写 `docs/README.md`（项目名称、技术栈、文档导航目录、生成时间）
c. 展示结果：文档列表、状态、失败项提示

---

## 护栏

- subagent 通过 Write 工具写文件，返回值只含摘要，绝不回传文档全文
- 主 agent 绝不读源码，也绝不读文档内容到上下文
- 绝不编造未实现的功能
- 绝不修改源码
- subagent 失败则记录并继续，最终汇报失败项
- "仅补充"模式下已有文档的模块跳过
- 中文编写，术语保留英文，大量使用 ASCII 图表
- 合并的小模块仍各自生成独立文档
