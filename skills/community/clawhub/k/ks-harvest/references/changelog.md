# 快手数据采集 更新日志

## 1.1.4

- 精简 frontmatter：删除 `metadata.keywords` / `metadata.category`；有价值词并入精简 `tags`（触发仍以顶层 `description` 为准）。
- 再删无效字段：`openclaw.emoji`、`metadata.enabled` / `runtime` / `env_desc`（门禁仍靠 `openclaw.primaryEnv` + `requires`）。
- 精简 `metadata.examples`：search / comment / post 各一条；去掉 search 变体与粉丝查询复读。
- HTTP 429→`RATE_LIMITED`（`noRetry=false`）；`classifyPollError` 以 `noRetry` 为准（不再依赖 `HTTP_429` 特判或一刀切 `ApiError`）。
- Create 成功读取出参 `id`（标准 36 字符 uuid）：有 `id` 时查询 `/info` **只传 `id`**（不带业务字段，避免 uuid 未命中时静默回落他单）；无 `id` 或形态不符时仍只按业务字段查。
- 新增 `references/contract.md`：「上游异步任务」约定；CLI schema / 信封不含任务 uuid。
- 执行示例改为 `node "<SKILL_ROOT>/scripts/kuaishou/…"`；faq 去掉宿主写死路径，统一用 `<SKILL_ROOT>` 占位。
- 布尔 flag（如 `--save`）：裸 flag 为 true；`--save=false`/`0` 为 false；非法赋值报错。
- 业务码映射：`410`（TOKEN 停用 Gone）/`405`（未开通）/`77`（过期）→ `AUTH_ERROR`；未知数字码兜底 `API_ERROR`；传输层补 `HTTP_404`/`HTTP_410` 说明。

## 1.1.3

- 新增 `references/faq.md`；SKILL 写入 Windows cmd/PowerShell 双壳例与「cmd 只用双引号」。
- CLI 支持 `--json-args`（与传统 flag 互斥；键名用 `keyword`/`url`/`sort` 等）；`parseCliArgs` 统一入口；SKILL/faq 补例。
- 落盘开关统一为 `GUAIKEI_ENABLE_LOG=1` 或 CLI `--save`；废弃 `KS_GUAIKEI_ENABLE_LOG`。
- `backendCodes`：在余额判断之后将裸 `errcode === 14` 稳定映射为 `PLAN_LIMIT`（不再仅依赖 errmsg 正则）。
- 修正 `requestApi` 创建重试注释：以 `noRetry` 为准；频控（多为后端 2）不重试，勿写「2–9 一律重试」。
- stdout 信封顶层可选 `cost`（透传取数接口花费估算；错误省略）。

## 1.1.2

- 链接尾部 scrub 补齐中文引号/书名号等，避免 `「」` 粘在短链/视频 id 后误判无效。
- `finishSuccess` 先落盘再 drain stdout，再 stderr 提示后 `exit(0)`。
- 错误码改为 errmsg 优先：补 `INSUFFICIENT_BALANCE`（15）、`RATE_LIMITED`（2）、`DAILY_LIMIT`（18）；频控创建不再无意义重试。
- SKILL / schema 同步禁重试说明。

## 1.1.1

- 明确套餐双上限：技能硬上限仍为 10000（按量）；包月 Token 搜索最多 30、作品最多 50、评论最多 60。
- 后端 errcode `14` 映射为稳定 `PLAN_LIMIT`；Agent 禁止同参重试，可建议降 `--limit` 或升级套餐（须用户同意）。
- 文档与示例同步：评论示例改为 40，避免包月用户按「100 条」直接踩坑。

## 1.1.0

- stdout 统一为同一份 JSON 信封；非法参数直接失败，不再改成默认值后继续请求。
- 空结果退出码为 0。查询在任务处理中继续等待；未完成不再当成空结果，次数用尽返回 `TIMEOUT`。
- 增加搜索、作品、评论的入参、出参和输出信封 schema。
- 作品只接受主页链接或纯数字 user_id；评论只接受视频链接、短链或 3x 视频 id。
- 链接会补 `www`、把 `http` 改成 `https`，并去掉 query。短参数大小写都可以。
- HTTP 429 和 5xx 会重试。查询时业务错误仍然立即失败，只有 `errcode 1` 继续等待。
- 关键词不合法退出码为 2。
- 成功结果默认不写文件。需要留底时设置 `KS_GUAIKEI_ENABLE_LOG=1`。POSIX 上日志仅当前用户可读写；Windows 靠临时目录隔离。超长文件名仍保留 `.json`。
- 写明查询最长大约等 15 分钟，以及搜索、作品、评论大约 20 分钟的任务复用窗口。
- 创建阶段最后一次失败不再打成「还要重试」。stderr 时间与信封一样用北京时间。
- 支持 `--` 结束选项。以 `-` 开头的关键词用 `--keyword=-AI` 或 `node scripts/kuaishou/search-cli.js -- -AI`。
- 日志文件名加上进程号。

## 1.0.0

- 初始版本发布
- 提供关键词搜索功能
- 提供博主作品获取功能
- 提供作品评论数据获取功能
