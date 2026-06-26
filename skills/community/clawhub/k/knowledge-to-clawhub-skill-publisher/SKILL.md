---
name: knowledge-to-clawhub-skill-publisher
description: Turn a solved workflow into canonical knowledge docs and a self-contained ClawHub-publishable skill. 把一个已验证流程沉淀成规范知识文档，并打包成可发布到 ClawHub 的自包含 skill。
homepage: https://docs.openclaw.ai/tools/clawhub
---

# Knowledge to ClawHub Skill Publisher

Use this skill when a workflow has already been proven in practice and should now be captured as durable docs plus a reusable skill.
当一个流程已经在实战中验证过，并且现在需要沉淀成长期文档与可复用 skill 时，使用这个 skill。

## Read First | 先读这些

Review these files before doing any packaging work:
在做打包工作之前，先看这些文件：

- `{baseDir}/README.md`
- `{baseDir}/WORKFLOW.md`
- `{baseDir}/FAQ.md`
- `{baseDir}/CHANGELOG.md`

## Primary Rule | 核心原则

Do not publish a skill from a raw chat transcript. First extract a stable workflow and write canonical docs.
不要直接把原始聊天记录发布成 skill。先提炼稳定流程，再写成规范知识文档。

## Workflow | 执行流程

1. Identify the stable workflow and remove one-off chat noise.
   识别稳定流程，去掉一次性聊天噪音。
2. Write canonical docs under `knowledge/runbooks/` if working inside a shared knowledge repository.
   如果在共享知识仓库中工作，先把规范文档写到 `knowledge/runbooks/`。
3. Create a self-contained skill folder under `skills/shared/<skill-name>/`.
   在 `skills/shared/<skill-name>/` 下创建自包含 skill 目录。
4. Add:
   补齐以下文件：
   - `SKILL.md`
   - `README.md`
   - `WORKFLOW.md`
   - `FAQ.md`
   - `CHANGELOG.md`
5. Keep package references self-contained via `{baseDir}`.
   使用 `{baseDir}` 保持包内引用自包含。
6. Publish only after the docs and package are aligned.
   只在文档和包内容一致后再发布。
7. Verify the remote package after publish.
   发布后验证远端包内容。

## Strong Heuristics | 强判断规则

- if the process is not proven yet, document it as a draft instead of publishing a skill
- if the workflow depends on hidden workspace files, make the package self-contained first
- if `CHANGELOG.md` is missing, add it before the first stable release
- if the audience is mixed, prefer bilingual docs

中文解释：

- 流程还没验证过，就先记成草稿，不要急着发布 skill。
- 如果流程依赖工作区外部文件，先把包改成自包含。
- 如果缺 `CHANGELOG.md`，最好在第一个稳定版本前补上。
- 面向中英文混合用户时，优先双语。

## Safe Commands | 安全命令

```bash
make sync
clawhub publish /absolute/path/to/skill-folder --slug your-skill --name "Your Skill" --version 1.0.0
clawhub inspect your-skill --version 1.0.0 --files
```

## Response Format | 输出格式

Always return:
始终返回：

1. current workflow status
2. missing artifacts
3. next single best action
4. verification after that

## Constraints | 约束

- do not treat ClawHub as the source of truth
- do not publish secrets, machine-specific tokens, or raw transcripts
- keep skill bundles self-contained when possible
- prefer `knowledge/` as the canonical Markdown source

中文约束：

- 不要把 ClawHub 当成事实源。
- 不要发布密钥、机器专属 token，或原始聊天记录。
- 尽量保持 skill 包自包含。
- 优先把 `knowledge/` 作为规范 Markdown 来源。
