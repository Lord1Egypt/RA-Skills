# goto-codedev-manager

面向 OpenClaw 的**多 IDE / 多 AI 编程 Agent 统一调度 Skill**。它不替代任何 IDE，而是把
Codex、Claude Code、QoerCN（原 Lingma）、Trae、VS Code、Cursor、Qoder 等编程工具统一接入，围绕**项目目录 +
Git Diff + 命令行**来管理开发：下达开发任务、分析代码变更、识别数据库结构需求、生成 EF Core
Migration、产出数据库变更交接单、运行测试构建、生成中文开发报告。

是 GotoPlan「AI 开发运维协同闭环」的开发端，与 `goto-devops-orchestrator`（调度）、
`goto-cloudserver-manager`（服务器/数据库执行）协同。

## 架构

```
OpenClaw
  └── goto-codedev-manager
        ├── adapters/   编程 Agent / IDE 适配轴（谁来改代码）
        │     codex · claude_code · qoer · lingma · trae · vscode · cursor · qoder · generic
        ├── stacks/     后端技术栈适配轴（怎么识别实体/生成 Migration）
        │     dotnet(efcore)   ← MVP
        ├── core/       config_loader · policy_engine · adapter_selector ·
        │               dispatcher · diff_analyzer · entity_extractor ·
        │               schema_contract · report_generator
        ├── executor/   local_executor（subprocess 跑 git/dotnet/各 IDE CLI）
        └── reports/    中文报告模板
```

**两条轴正交**：新增技术栈只动 `stacks/`，新增编程工具只动 `adapters/`，变更分析逻辑两者都不动。

## 安装

```
openclaw skills install @feixuelingcloud/goto-codedev-manager
```

或本地开发：

```
pip install -e .
```

## 配置

1. **工作区** `config/workspaces.yaml`（参考 `workspaces.yaml.example`）：登记本地项目路径、
   技术栈、首选/回退编程 Agent、EF 项目路径、**测试库连接串**（`${TEST_DB_CONNECTION}` 引用 `.env`，
   禁止填生产库）。
2. **适配器** `config/adapters.yaml`：启用哪些编程 Agent 及其优先级。
3. **权限** `config/policies.yaml`：三级权限（只读/确认/禁止），一般无需改。
4. **环境变量** `.env`（参考 `.env.example`）：测试库连接串、各 CLI 可执行文件名。

IDE CLI 适配采用配置驱动：`project_args` 用于读取项目数据，`task_args` 用于下达任务指令，
`open_args` 用于访问/打开工作区。若本机 Qoer、Trae、Cursor、Qoder 等 CLI 参数与默认值不同，
只需要调整 `config/adapters.yaml`，无需修改 Python 代码。

## 适配器选择顺序

`assign_coding_task` 等动作由 `adapter_selector` 自动选 Agent：

1. 显式 `agent` 参数 → 2. workspace.preferred_agent（可用）→ 3. fallback_agent →
4. adapters.yaml 中按 priority 升序第一个可用 → 5. 兜底 `generic`（仅读 Git Diff，
   代码生成交给用户/外部 IDE）。

> CLI 不可用（未安装对应命令）会自动降级。Lingma 已作为 QoerCN 的兼容入口，
> 通过 Qoer CLI 访问项目并下达任务；Trae、VS Code、Cursor、Qoder 等 IDE 也统一走 CLI。

## 典型工作流

```
用户：用 Codex 在 gotoplan-backend 开发"客户管理模块"，并识别数据库变更。

codedev-manager：
1. read_project_context        读分支/改动/技术栈
2. assign_coding_task          经 Codex CLI 开发（需确认）
3. analyze_git_diff            结构化变更
4. detect_database_changes     发现新增 Customer 实体
5. generate_schema_contract    写 .db-contract/pending-changes.json
6. run_tests                   dotnet test
7. generate_report             开发同步报告
```

交接单 `pending-changes.json` 由 `goto-devops-orchestrator` 消费，调
`goto-cloudserver-manager` 的 `apply_schema` 在测试库落库（需确认）——
`SchemaContract.to_unified_schema()` 已转成 cloudserver 的 `UnifiedSchema` 格式。

## 安全边界

| 级别 | 动作 |
|---|---|
| 自动允许 | 读代码、分析 Git Diff、识别实体、生成 Migration 草案/交接单、跑测试构建、生成报告 |
| 需确认 | 下达开发任务、生成 Migration、测试库落库、git 提交 |
| 禁止 | 直连生产库执行 Migration、`git push --force`、重置 Migration 历史、`git reset --hard`、删分支 |

数据库变更**只生成 Migration / 交接单，绝不在本端直连任何数据库执行**（落库由 cloudserver 在
orchestrator 确认门控下完成）。

## 测试

```
python -m pytest -q
```

## 已支持 / 规划

- 编程工具：Codex、Claude Code、QoerCN（兼容 Lingma）、Trae、VS Code、Cursor、Qoder 均走 CLI；
  `generic` 仅作为最终 Git Diff 兜底。二期：MCP 深度连接、JetBrains/Visual Studio 插件。
- 技术栈：.NET / EF Core（MVP）。二期：Node(Prisma/TypeORM)、Python(Alembic/Django)、Java(Flyway)。
