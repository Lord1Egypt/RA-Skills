# OpenClaw Memory Migrator

**迁移记忆，不迁移风险。**

一套带安全闸门的 OpenClaw Skill 与 CLI 工具，将 LanceDB Pro、官方
LanceDB 列表捕获、QMD 或 Markdown 的权威记忆迁移到 `memory-core`。

记忆迁移可能遭遇导出截断、scope 遗漏、内容重复，以及召回和回滚无法验证。
本工具通过 dry-run 清单、数量/ID/哈希对账、可审阅 Markdown 暂存和批准闸门，
让这些风险在切槽前暴露出来。

[English](README.md)

## 为什么需要它

更换记忆后端不是简单复制文件。可信迁移必须证明导出了什么、阻止不兼容向量
进入新索引、保护密钥、保留回滚路径，并在退役旧后端前量化对比召回质量。

本项目为希望从第三方记忆后端迁回 OpenClaw 官方 `memory-core` 的用户，
提供一条安全、可验证、易操作的迁移路径。

本项目提供：

- 版本化、可审阅的 JSONL 中间格式；
- 按来源核对数量、ID、哈希和重复内容；
- 生成 memory-core Markdown，但不自动改写根 `MEMORY.md`；
- 与 run ID 绑定的生产操作批准令牌；
- 可续跑阶段状态和回滚证据；
- 可复现的召回基准流程；
- 不直接写 OpenClaw SQLite 内部表。

## 支持状态

- 稳定：按版本探测的 memory-lancedb-pro JSON 捕获
- 稳定：Markdown 与 QMD 的权威 Markdown
- Beta：将官方 `memory-lancedb` 的 `ltm list` JSON 包装为带版本、按 Agent
  隔离的捕获清单
- 目标：通过 Markdown 与官方索引命令进入 memory-core

不支持解析不透明数据库、复制旧向量或自动删除重复内容。

重要：memory-lancedb-pro v1.1.0-beta.10 的 `export` 最多返回 1,000 条。
操作流程必须按 scope 与最新 stats 核对，超量时通过 `list --offset` 分页。

## 先用合成 fixture 试跑

需要 Node.js 22+，无运行时依赖。这条路径只用仓库内合成数据，不要换成真实导出。

```bash
node bin/openclaw-memory-migrator.js --help
mkdir -p canonical reports staged-memory/imports
node bin/openclaw-memory-migrator.js preflight \
  --input test/fixtures/lancedb-pro.json \
  --output canonical/memory-records.jsonl
node bin/openclaw-memory-migrator.js normalize --dry-run \
  --adapter lancedb-pro \
  --input test/fixtures/lancedb-pro.json \
  --output canonical/memory-records.jsonl
# 可选：直接对源 fixture 做冒烟审计（不写盘）
node bin/openclaw-memory-migrator.js audit --dry-run \
  --adapter lancedb-pro \
  --input test/fixtures/lancedb-pro.json
node bin/openclaw-memory-migrator.js render --dry-run \
  --adapter lancedb-pro \
  --input test/fixtures/lancedb-pro.json \
  --output staged-memory/imports/lancedb-pro
```

fixture dry-run 通过后再从 ClawHub 安装：

```bash
openclaw skills install memory-core-migrator
openclaw skills info memory-core-migrator --json
# 然后在返回的 skill 目录中运行：
node <skill-dir>/bin/openclaw-memory-migrator.js --help
```

ClawHub slug `memory-core-migrator` 与仓库/Skill id `openclaw-memory-migrator`
是同一套工具。然后用
[脱敏 dry-run 表单](https://github.com/airbing11/openclaw-memory-migrator/issues/new?template=dry-run-report.yml)
提交计数，不要提交记忆正文。

## 使用自己的导出

```bash
node bin/openclaw-memory-migrator.js --help
mkdir -p canonical reports staged-memory/imports
node bin/openclaw-memory-migrator.js preflight \
  --input export/global.json \
  --input export/main.json \
  --output canonical/memory-records.jsonl
node bin/openclaw-memory-migrator.js normalize --dry-run \
  --adapter lancedb-pro \
  --input export/global.json \
  --input export/main.json \
  --expected-total <trusted-snapshot-total> \
  --output canonical/memory-records.jsonl
# 在批准并执行 normalize --apply 写出 canonical JSONL 后：
node bin/openclaw-memory-migrator.js audit --dry-run \
  --adapter canonical-v1 \
  --input canonical/memory-records.jsonl
node bin/openclaw-memory-migrator.js render --dry-run \
  --adapter canonical-v1 \
  --input canonical/memory-records.jsonl \
  --output staged-memory/imports/lancedb-pro
```

CLI 默认只做本地、非破坏性转换。`--dry-run` 是该默认行为的显式别名，不能与
`--apply` 同时使用。生产使用前必须阅读 [`SKILL.md`](SKILL.md)。

召回对比方法见
[`docs/benchmark-methodology.md`](docs/benchmark-methodology.md)。
另见[常见问题](docs/faq.zh-CN.md)和[场景操作手册](docs/recipes.zh-CN.md)。

## 安全模型

- 仅 owner 私聊、Control UI 或本地运维终端执行
- 默认 dry-run
- 写操作前必须有 verified backup
- 批准绑定操作名与 run ID
- 环境漂移、数量或哈希不一致立即停止
- 报告保存在记忆索引范围外
- 回滚期内保留源数据

详见 [`references/operations.md`](references/operations.md) 与
[`SECURITY.md`](SECURITY.md)。

## 当前阶段

项目处于早期候选版本。先使用合成 fixture 或导出副本测试；生产切槽仍需人工
审阅。

## 真实案例边界

一次脱敏运行对齐了 1,533 条导出与规范记录，并生成 29 个暂存 Markdown 文件。
其中 8/8 Hit@5 只是迁移后健康检查，不是成对前后基准；保留恢复产物只证明
rollback readiness，不代表执行过 rollback rehearsal。近似审计也只完成
10,000 / 1,174,211 个候选对。详见有明确证据边界的
[dogfood 记录](docs/dogfood-2026-09-18.md)；这些观测不保证其他安装环境获得
相同结果。

## 反馈

当前 RC 需要的是支持来源上的脱敏 dry-run 计数，而不是原始记忆。请使用
Issue Form：

- [脱敏 dry-run 报告](https://github.com/airbing11/openclaw-memory-migrator/issues/new?template=dry-run-report.yml)
- [兼容性缺陷](https://github.com/airbing11/openclaw-memory-migrator/issues/new?template=compatibility-bug.yml)

不要上传导出文件、JSONL、截图、主机名或记忆正文。隐私红线见
[`docs/community-launch-plan.md`](docs/community-launch-plan.md)。

## 开发

```bash
npm test
npm run check
```

## 许可证

GitHub 源码仓库采用 MIT，见 [`LICENSE`](LICENSE)。通过 ClawHub 分发的 Skill
副本按照 ClawHub 发布规则采用 MIT-0。
