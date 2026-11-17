# 场景操作手册

以下示例只操作导出副本。运行目录必须位于所有 OpenClaw 索引目录之外。

## 对账多个 LanceDB Pro scope

1. 用已安装插件的 stats 命令记录每个 scope 的数量。
2. 分别导出或分页捕获每个非空 scope。
3. 传入全部文件并设置精确总数：

```bash
node bin/openclaw-memory-migrator.js normalize --dry-run \
  --adapter lancedb-pro \
  --input export/global.json \
  --input export/main.json \
  --input export/other-scope.json \
  --expected-total 1533 \
  --output canonical/memory-records.jsonl
```

不要自动容忍 ±1。保留来源侧前后快照，并用证据明确解释并发写入。

## 强制近似重复审计完整

对 `n` 条记录，在排除精确文本对之前，候选对上限是 `n * (n - 1) / 2`。先
dry-run：

```bash
node bin/openclaw-memory-migrator.js audit --dry-run \
  --adapter canonical-v1 \
  --input canonical/memory-records.jsonl \
  --max-comparisons 2000000 \
  --require-complete-approximate
```

检查 `total_candidates`、`performed`、`coverage` 与 `warnings`。只在本机时间和
内存预算允许时提高上限。

## 安全消费机器可读输出

正常 JSON 只写 stdout，警告和错误只写 stderr。调用方需要
`{code,message,next_action,details}` 时添加 `--json-errors`：

```bash
node bin/openclaw-memory-migrator.js audit \
  --adapter canonical-v1 \
  --input canonical/memory-records.jsonl \
  --json-errors >reports/audit.stdout.json 2>reports/audit.stderr.jsonl
```

解析 JSON 前不要合并两个流。

## 分页捕获受限来源

v0.1 由操作者负责来源分页。读取已安装插件的 `list --help`，固定
scope/limit/offset，保留每页，并在合并后检查 ID 无遗漏、无重复。本工具不会把
分页捕获伪称为官方插件导出。

## 错误到修复动作

- `COUNT_MISMATCH`：重新捕获计数或修正 `--expected-total`。
- `SCOPE_MISSING`：补齐 scope 或清单身份。
- `MANIFEST_INVALID`：重新生成并验证来源清单。
- `AUDIT_INCOMPLETE`：提高 `--max-comparisons`。
- `APPROVAL_INVALID`：重跑 dry-run，并签发新的操作/run 绑定批准。
- `OUTPUT_CONFLICT` / `SYMBOLIC_LINK`：改用新的普通输出路径。

## 隐私红线

不要在 Issue 或聊天中粘贴真实记忆、片段、查询、导出、JSONL、审计文件、截图、
主机名、Agent/频道 ID、私有路径、令牌或备份哈希。使用合成 fixture 复现问题。
