# compile 完整流程

> 本流程为 compile Skill 的正式版执行流程，使用脚本门禁、断点续做和 compile 专用 checkpoint。

## Step 0 预检查

执行纪律：

- 下面所有脚本都必须通过 OpenClaw 原生工具调用执行。
- 禁止输出 `<invoke ...>`、XML、伪 tool 标签或把 shell 命令写成普通文本。
- 若工具没有真实执行成功，不得继续写“已完成/下一步”；必须重新发起原生工具调用。

```bash
bash {baseDir}/scripts/compile_precheck.sh --vault "$OPENCLAW_VAULT"
```

- `COMPILE_INBOX_DIR` 必须已由 OpenClaw config 注入；未配置时停止，不得创建或扫描 `$OPENCLAW_VAULT/Inbox`
- 校验关键路径存在
- 列出收件箱 `status != processed` 的待编译文件；`pending`、`captured`、缺失 `status` 都是待编译
- 心跳扫描必须以本脚本输出为准，禁止临时手写 `for/grep/sed` 状态扫描，避免 zsh 特殊变量或被吞掉的 stderr 造成误判
- 收件箱为空则正常退出

checkpoint：

```bash
bash {baseDir}/scripts/compile_step_checkpoint.sh \
  --step 0 --status done --audit-cmd "test -f \"$COMPILE_STATE_DIR/compile_session.json\""
```

- Step 0 checkpoint 是正式进入编译流程的门禁；若这里的脚本未真实执行成功，必须原地重发工具调用，不得改用文本声明“Step 0 已完成”。

## Step 0.0 脏数据预处理

```bash
bash {baseDir}/scripts/compile_clipper_fix.sh \
  --file "$COMPILE_INBOX_DIR/目标文件.md"
```

- 修复 `Value:` → `author:`
- 修复 frontmatter 未闭合
- 把 YAML 内图片移出到正文开头
- 修复弯引号和需要加引号的 YAML 值
- 备份优先写到 `${TMPDIR}`；未设置时回退到系统临时目录

## Step 0.1 文件名特殊字符预处理

- 清理影响 Read/Bash 的特殊字符
- 需要改名时先记录旧名和新名

## Step 0.1.5 重复检查

- 先运行确定性查重脚本：

```bash
bash {baseDir}/scripts/compile_duplicate_check.sh \
  --file "$COMPILE_INBOX_DIR/目标文件.md" \
  --vault "$OPENCLAW_VAULT"
```

- 比对目标只保留 `Knowledge/原材料仓库/`
- 标题会先做归一化，忽略 `：` / `-` 等纯标点差异
- 若原文有 `source:`，再用归一化 URL 做二次兜底
- 不再扫描 `Knowledge/中转站/` 与 `Knowledge/已入库/`，因为两者分别对应编译中的工作区和已完成入库后的下游状态，不是源文章唯一库存
- 重复则标记并跳过本篇

## Step 0.3 知识扫描

1. 先查历史：

```bash
bash {baseDir}/scripts/_shared/query_history.sh \
  --skill compile \
  --topic "主题关键词" \
  --window 30 \
  --vault "$OPENCLAW_VAULT"
```

2. 扫描 `Knowledge/_INDEX.md` 与 `Knowledge/中转站/`
3. 给 `related_wiki` 一个明确结果：非空列表或 `[]`

## Step 1 精读原文

- 精读文字内容
- 荔枝生产环境图片全读；MiniMax 支持多模态，图中关键信息必须转写进正文，避免信息只留在图片里

## Step 1.5 文件名核对

```bash
bash {baseDir}/scripts/compile_filename_check.sh \
  --file "$COMPILE_INBOX_DIR/目标文件.md" \
  --llm-summary "文章实际主题" \
  --llm-keywords "关键词1,关键词2,关键词3"
```

- 必须先给出主题概括和关键词
- 默认只输出建议改名；确认需要落盘改名后再传 `--apply`
- 改名后才允许写决策日志到 `COMPILE_FILENAME_LOG_FILE`；保留原名时不得额外创建 `filename_decisions.md` 或手写决策文件
- 未配置时停止，不得写入通用日志目录

## Step 2 生成中转站文档

1. 再查一次同主题历史：

```bash
bash {baseDir}/scripts/_shared/query_history.sh \
  --skill compile \
  --topic "主题关键词" \
  --window 30 \
  --vault "$OPENCLAW_VAULT"
```

2. 生成 frontmatter：

```bash
bash {baseDir}/scripts/compile_frontmatter_gen.sh \
  --title "标题" \
  --author "@author" \
  --source "https://example.com" \
  --compiled-by "$COMPILE_ACTOR_NAME" \
  --tags "compile,knowledge-pipeline" \
  --keywords "主题关键词1,主题关键词2" \
  --related-wiki "[[主题A]] | rough,[[主题B]] | confirmed"
```

生产环境 `COMPILE_ACTOR_NAME` 必须为 `荔枝`。

3. `keywords` 先查 `Knowledge/_INDEX.md` 的现有主题词，能复用就复用；没有再由 Agent 自行设计
4. `tags` 可为空列表，但 `keywords` 不得为空
5. `related_wiki` 必须是扁平字符串数组；多项时用 CSV 传给生成器
6. 严格按 `references/compile-template.md` 的结构写入 `Knowledge/中转站/`
7. 写入后依赖 `compile_structure_check.sh` hook 做即时结构检查

## Step 3 建立交叉引用

- 建立 Wiki 侧引用
- 建立中转站同级引用
- 精读后把 `related_wiki` 的 `rough` 更新为 `confirmed`，或删除误匹配项
- 反向补链前先读取目标文档，定位到 `## 相关文档` section 内部再插入

## Step 3.5 级联检查

- 查找同主题中转站文档是否存在可能需要更新的结论
- 把结果写入 task logger

## Step 4 归档

```bash
bash {baseDir}/scripts/compile_archive.sh \
  --source "$COMPILE_INBOX_DIR/目标文件.md" \
  --compiled "$COMPILE_TRANSIT_DIR/目标文件.md" \
  --title "目标文件" \
  --vault "$OPENCLAW_VAULT"
```

- 移动原文到 `Knowledge/原材料仓库/`
- 移动图片到 `Knowledge/原材料仓库/assets/<标题>/`
- 回写 `original` 与 `compiled_version`
- `compiled_version` 以 `--compiled` 实际路径为真源写入，不再靠标题 glob 猜测
- 归档前必须先完成中转站目标和图片目标存在性校验，避免半成状态

## Step 5 自审

```bash
bash {baseDir}/scripts/compile_check.sh \
  "$COMPILE_TRANSIT_DIR/目标文件.md" \
  --vault "$OPENCLAW_VAULT"
```

- `tags` 必须存在，但允许 `[]`
- `keywords` 不得为空
- FAIL 时写 blocked checkpoint 并停止
- PASS 后才允许进入收尾

## Step 6 收尾

- 更新执行者自己的当日日志（末尾追加，不覆盖已有内容）
- 写 `compile_task_logger.sh` 短期结构化运行日志到 `.openclaw/state/compile/runs/`，由脚本自动清理旧 runs
- 向 Gavin 汇报：标题、中转站路径、原材料路径、交叉引用数量
