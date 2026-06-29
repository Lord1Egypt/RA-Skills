---
name: kb_ingest
description: Compile backend-uploaded source files into Research KB Markdown wiki pages, write them to Gitea, archive sources, and return structured JSON results.
---

# Skill: kb_ingest

## 职责边界

`kb_ingest` 只负责把 Java 后端已经上传好的源文件编译成 Research KB 的 Markdown wiki 页面，并写入指定的 Gitea 知识库仓库。它不负责登录、权限判断、本地扫描、重复文件预检查、目标仓库选择、任务创建、会话记录或用户交互。

每个任务表示一次完整的源扫描上传。必须把 `payload.files[]` 当成同一个快照来理解，保留 `relativePath` 中的原始目录结构。

## 可接受任务

只接受满足以下条件的 JSON：

- `protocol = research_kb_agent_task`
- `taskType = kb_ingest`
- `kbTargets[]` 中恰好有一个目标
- `payload.files[]` 非空，且每个文件包含后端可读的 `uploadedPath`

不要要求任务 JSON 携带 Gitea token。Gitea 凭据只能从 skill 环境变量读取。

## 编译流程

处理任务时按以下顺序执行：

1. 校验任务协议和输入字段。
2. 将每个原始源文件按 `archiveSourceFile` 选项归档到 `source_files/`。
3. 先基于完整文件清单识别代码项目，而不是逐个代码文件生成页面。
4. 识别项目根目录标记：`package.json`、`pyproject.toml`、`requirements.txt`、`pom.xml`、`build.gradle`、`Cargo.toml`、`go.mod`、`.sln`、`.csproj`、`Makefile`、`CMakeLists.txt`、`Dockerfile` 等。
5. 如果一个快照包含多个明确的项目根目录，为每个根目录生成一个 `codebase` 页面；如果根目录标记显示这是 monorepo，保持整体编译，不要拆成无意义的小页。
6. 非代码文档需要识别为 `paper`、`survey`、`project`、`doc`、`experiment`、`meeting` 或 `note`。
7. 使用 `scripts/summary_templates.py` 中的中文结构生成 wiki 页面。
8. 页面内容只能来自上传文件中的证据。缺失字段写“来源未提及。”，不要用常识补全。
9. 每个 Markdown 页面必须包含 frontmatter 和非空 `sources` 数组。代码库页面的 `sources` 必须覆盖该项目摘要使用到的所有源文件。
10. 写入 Markdown 页面，更新 `catalog.json`，更新 `index.md`。
11. 多文件任务需要在 `imports/` 下写入导入报告。
12. 最终只返回一个合法的 `research_kb_agent_result` JSON。

## 生成要求

参考“先把资料编译成持久 wiki，再用于查询”的方式：入库阶段要尽量把原始资料转成可检索、可引用、可追踪的中文知识页，而不是只保存原文摘录。

不同类型页面必须关注对应信息：

- 论文：研究问题、核心贡献、方法、实验结果、局限、可复用结论。
- 综述/调研：范围、分类框架、关键发现、趋势、风险、信息缺口、团队启发。
- 项目/代码库：目标、架构、目录结构、核心模块、依赖与配置、运行测试线索、成熟度、风险、修改建议。
- 技术文档：用途、前置条件、关键概念、命令/API、配置、示例、排障。
- 实验：假设、变量、环境、数据与模型、结果、异常、结论、下一步。
- 会议：时间与参与者、议程、讨论、决议、行动项、风险、开放问题。
- 笔记：背景、核心想法、证据、不确定性、关联知识、行动项、验证问题。

## 目标目录

- `paper` -> `summaries/papers/`
- `survey` -> `summaries/surveys/`
- `project` -> `summaries/projects/`
- `doc` -> `summaries/docs_tech/`
- `experiment` -> `summaries/experiments/`
- `meeting` -> `summaries/meetings/`
- `codebase` -> `summaries/codebases/`
- `note` -> `summaries/notes/`

团队知识库可以更新 `people/` 和 `projects/general/`。个人知识库不要创建或写入这两个目录。

## 输出

必须返回如下结构，字段名和层级不能改变：

```json
{
  "protocol": "research_kb_agent_result",
  "protocolVersion": "1.0",
  "taskId": "...",
  "taskType": "kb_ingest",
  "success": true,
  "result": {
    "ingestionId": "...",
    "kbTarget": {
      "kbType": "team",
      "repoFullName": "AIFusionBot/aifhku-lab-team-kb",
      "branch": "main"
    },
    "processedFiles": 1,
    "createdMarkdownFiles": [],
    "updatedMarkdownFiles": [],
    "createdExtraPages": [],
    "archivedSourceFiles": [],
    "skippedFiles": [],
    "failedSourceFiles": [],
    "catalogUpdated": true,
    "indexUpdated": true,
    "importReportPath": ""
  },
  "errors": []
}
```

单个文件失败时放入 `failedSourceFiles`。整个任务失败时设置 `success=false`。

## 辅助入口

稳定入口是：

```bash
python3 scripts/run_task.py --stdin
python3 scripts/run_task.py --task-json <path>
```

该脚本会校验任务、抽取文本、归档源文件、生成中文 Markdown、写入 Gitea、更新目录和索引，并返回固定 JSON schema。Agent 可以在调用底层脚本前生成更丰富的页面内容，但最终响应必须仍然遵守上面的输出结构。
