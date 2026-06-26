---
name: aippt
description: 通过关键字或上传文件调用 Mindshow/AIPPT API 生成 PPT，包括生成大纲、生成完整 Markdown 内容、创建 PPT 任务和轮询进度。也适用于查询账号信息、获取或选择模板、上传资源文件、获取 PDF 或跳转链接，以及查看 AIPPT API 的请求和响应结构。
---

# AIPPT API

使用本 skill 时，通过内置 CLI 调用 AIPPT API：

- `aippt-cli.js`：零依赖 Node.js 命令行客户端。
- `apidoc.json`：OpenAPI 3 文档，CLI 会从中读取接口路径、请求方法、请求结构和默认服务地址。

不要安装 npm 包。CLI 只使用 Node.js 内置能力。

## 配置

调用受保护接口前需要 Bearer token：

```bash
export AIPPT_TOKEN="..."
```

获取 `AIPPT_TOKEN` 的入口：

```text
https://api-doc.mindshow.vip/
```

CLI 会自动读取 当前目录下的 `./.env`：

```dotenv
AIPPT_TOKEN=...
```

token 优先级为：`--token`、shell 环境变量 `AIPPT_TOKEN`、`.env`。不要打印 token，也不要把 token 写入 `.env` 或当前 shell 以外的位置。

默认服务地址来自 `apidoc.json`：

```text
https://api.mindshow.vip
```

只有在用户明确提供其他环境时，才覆盖服务地址：

```bash
export AIPPT_BASE_URL="https://..."
```

`AIPPT_BASE_URL` 也可以写在 `.env` 中。

## 命令

在 skill 目录下执行命令：

```bash
cd /path/to/skill
```

列出可用接口：

```bash
./aippt-cli.js list --pretty
```

调用前查看单个接口的请求和响应结构：

```bash
./aippt-cli.js schema /v1/job/get --pretty
```

调用普通 JSON 接口：

```bash
./aippt-cli.js call /v1/account/info --pretty
./aippt-cli.js call /v1/job/get --data '{"id":"job_id"}' --pretty
```

调用 SSE/GPT 流式接口。只要请求体里包含 `"stream": true`，CLI 就会把原始 SSE 响应实时输出到 stdout：

```bash
./aippt-cli.js call /v1/gpt/gen_outline_by_topic --data-file ./content_to_outline.json --pretty
```

流式调用时，stdout 是原始 `data: ...` 事件流，不是外层 JSON 包装。如果调用方需要收集生成内容，需要逐条解析 `data:` 事件。

请求体较大时，从 JSON 文件读取：

```bash
./aippt-cli.js call /v1/job/ppt_create_by_json --data-file ./request.json --pretty
```

上传文件：

```bash
./aippt-cli.js call /v1/resource/upload --file ./demo.pptx --pretty
```

## 输出约定

普通接口调用成功执行时，CLI 会向 stdout 输出机器可读 JSON：

```json
{
  "ok": true,
  "status": 200,
  "statusText": "OK",
  "path": "/v1/account/info",
  "method": "POST",
  "data": {
    "code": 0,
    "info": "succ",
    "request_id": "...",
    "data": {}
  }
}
```

需要分别判断 HTTP 成功和 API 成功：

- `ok` 和 `status` 表示 HTTP 响应状态。
- `data.code === 0` 表示 AIPPT API 操作成功。
- `data.code` 非 0 表示 API 拒绝请求；需要报告 `data.info` 和 `request_id`。
- 对于请求体包含 `"stream": true` 的流式接口，stdout 是原始 SSE，不使用上面的 JSON 包装。

CLI 参数错误或网络失败时，会向 stderr 输出 JSON，并以非 0 状态码退出。

## 常用流程

1. 使用 `schema <path>` 确认必填字段和响应结构。
2. 构造最小可用的 JSON 请求体。
3. 使用 `--data` 或 `--data-file` 调用接口。
4. 对普通接口，解析 stdout JSON，并同时检查 `status` 和 `data.code`。
5. 对创建任务类接口，保存返回的任务 id，然后轮询 `/v1/job/get`。轮询响应里的 `data.job.progress_percent` 是 PPT 任务生成进度。
6. 任务成功后，使用返回的 `ppt_url`，或按需调用 `/v1/job/get_pdf`、`/v1/job/get_jump_link` 等接口。

## 按关键字生成 PPT

当用户只给出主题、关键字或一句话需求时，按下面顺序生成 PPT：

1. 调用 `/v1/gpt/gen_outline_by_topic`，使用 SSE 生成大纲。
   - 如果用户没有指定页数，`page_count` 默认传 `25`。
   - 如果用户明确指定页数，按用户指定的页数传 `page_count`。
2. 大纲 SSE 每次返回 `data.content` 增量片段；可以在界面中实时拼接并渲染为 Markdown 大纲。
3. 从最后的 SSE 事件中读取 `data.all_content` 作为最终大纲 Markdown，同时保存 `data.content_ex_info`。
4. 默认使用系统推荐模板：不调用 `/v1/template/list`，创建 PPT 时不传 `template_id`。
5. 只有用户明确要求“选择模板”“展示模板”“指定模板”时，才调用 `/v1/template/list` 并让用户选择模板。
6. 调用 `/v1/gpt/gen_content_by_outline`，传入上一步大纲，使用 SSE 生成完整 Markdown 内容。
7. 完整内容 SSE 每次返回当前完整 `data.content` 和 `data.progress_percent`；可以在界面中实时更新 Markdown 内容和生成进度。
8. 从最后的 SSE 事件中读取 `data.content` 作为最终完整 Markdown。
9. 调用 `/v1/job/ppt_create_by_markdown`，用完整 Markdown 创建 PPT 任务；如果用户已选择模板，则同时传入 `template_id`。
10. 调用 `/v1/job/get` 循环获取 PPT 任务进度，用 `data.job.progress_percent` 更新界面，直到 `status` 为 `succeeded` 或 `failed`。

第一步请求示例：

```json
{
  "topic": "莫扎特",
  "stream": true,
  "model": "ali",
  "page_count": 25,
  "language": "zh",
  "scene": "公众演讲",
  "target_audience": "大众",
  "desc_info": ""
}
```

调用命令：

```bash
./aippt-cli.js call /v1/gpt/gen_outline_by_topic --data-file ./outline_request.json
```

该命令会实时输出原始 SSE。收集最后一个 `finish_reason` 为 `stop` 的 `data:` JSON，读取：

- `data.content`：当前增量文本片段；界面可以把这些片段按顺序追加，实时展示正在生成的大纲 Markdown。
- `data.all_content`：大纲 Markdown，传给下一步的 `outline`。
- `data.content_ex_info`：内容扩展信息，建议传给下一步的 `content_ex_info`。

第二步：模板选择策略。

默认推荐模板模式：

- 如果用户没有要求选择模板，不要调用 `/v1/template/list`。
- 创建 PPT 时不要传 `template_id`，让 `/v1/job/ppt_create_by_markdown` 自动使用系统推荐模板。
- 这种模式步骤更短，适合“帮我生成一个 PPT”“生成 25 页某主题 PPT”等普通请求。

默认推荐模板模式下，创建 PPT 请求示例：

```json
{
  "speaker": "演讲者",
  "content": "# 莫扎特\n\n## 生平与作品\n...",
  "create_ppt_flag": true,
  "create_preview_image_type": "top3"
}
```

手动选择模板模式：

- 只有用户明确提出选择模板、查看模板、指定模板风格，或当前任务确实需要用户确认模板时，才进入该模式。
- 进入该模式后，从大纲 Markdown 的一级标题中提取标题，例如第一行 `# 莫扎特` 提取为 `莫扎特`。
- 调用 `/v1/template/list`，把标题传入 `recommend_content`。

请求示例：

```json
{
  "type": "public",
  "after": "",
  "limit": 10,
  "recommend_content": "莫扎特艺术成就",
  "preview_img_width": 480,
  "preview_img_quality": 80
}
```

调用命令：

```bash
./aippt-cli.js call /v1/template/list --data-file ./template_request.json --pretty
```

向用户展示 `data.list` 时，应显示模板预览图，而不是只显示文字。至少展示：

- `template_id`：后续创建 PPT 时使用。
- `title`：模板标题。
- `from_type`：`recommend` 表示推荐模板，`default` 表示默认模板。
- `vip_flag`：是否需要会员。
- `preview_img_list[0]`：模板首张预览图，用 Markdown 图片语法直接展示。

推荐展示格式：

```markdown
1. `template_id`
   标题：模板标题
   来源：recommend/default，非 VIP/需要 VIP
   ![模板预览](preview_img_list[0])
```

用户选择模板后，保存所选模板的 `template_id`。

第三步请求示例：

```json
{
  "outline": "# 莫扎特\n## 生平与作品\n...",
  "stream": true,
  "content_ex_info": "上一步返回的 content_ex_info"
}
```

调用命令：

```bash
./aippt-cli.js call /v1/gpt/gen_content_by_outline --data-file ./content_request.json
```

生成完整内容时，每个 SSE 事件都可用于更新界面：

- `data.content`：当前完整 Markdown 内容；界面应使用它覆盖上一次内容，而不是追加。
- `data.progress_percent`：内容生成进度，范围 0-100；界面可以用它更新进度条或状态文字。

最后读取 `finish_reason` 为 `stop` 的 `data:` JSON，取 `data.content` 作为最终完整 Markdown。

第四步：创建 PPT 任务。

默认推荐模板模式请求示例：

```json
{
  "speaker": "演讲者",
  "content": "# 莫扎特\n\n## 生平与作品\n...",
  "create_ppt_flag": true,
  "create_preview_image_type": "top3"
}
```

手动选择模板模式请求示例：

```json
{
  "template_id": "用户选择的 template_id",
  "speaker": "演讲者",
  "content": "# 莫扎特\n\n## 生平与作品\n...",
  "create_ppt_flag": true,
  "create_preview_image_type": "top3"
}
```

调用命令：

```bash
./aippt-cli.js call /v1/job/ppt_create_by_markdown --data-file ./ppt_request.json --pretty
```

创建成功后，读取 `data.job.id` 作为任务 id。

第五步轮询任务：

```bash
./aippt-cli.js call /v1/job/get --data '{"id":"任务id"}' --pretty
```

建议每 5 秒轮询一次。`/v1/job/get` 返回的是 PPT 异步任务的生成进度，和 `/v1/gpt/gen_content_by_outline` 的内容生成进度不同：

- `data.job.status === "queued"`：排队中。
- `data.job.status === "running"`：PPT 生成中，读取 `data.job.progress_percent`，用于更新界面进度。
- `data.job.status === "succeeded"`：生成成功，`data.job.progress_percent` 通常为 100，读取 `data.job.ppt_url`，并展示 `data.job.preview_img_list` 中的预览图。
- `data.job.status === "failed"`：生成失败，报告 `data.job.error`。

最终回复用户时，除 PPT 下载链接外，也展示生成结果预览图：

```markdown
PPT 下载链接：
[下载 PPT](data.job.ppt_url)

预览图：
![第 1 页预览](data.job.preview_img_list[0])
![第 2 页预览](data.job.preview_img_list[1])
![第 3 页预览](data.job.preview_img_list[2])
```

## 按文件生成 PPT

当用户提供本地文件，并要求根据文件内容生成 PPT 时，先上传文件获取 `resource_id`，再把 `resource_id` 传给 `/v1/gpt/gen_outline_by_topic`。后续步骤与“按关键字生成 PPT”一致。

`/v1/resource/upload`、`/v1/gpt/gen_outline_by_topic`、`/v1/gpt/gen_content_by_outline` 会配合使用文件内容：上传后，系统会从常见文档类型中提取文本内容，例如 `docx`、`pdf`、`pptx`、`ppt`、`doc`、`txt`。这些文本会用于生成大纲，并继续用于根据大纲生成完整 Markdown 内容。

第一步：上传文件。

`/v1/resource/upload` 使用 `multipart/form-data`，不要用 JSON。文件最大 20MB，上传后的资源保留 24 小时。

调用命令：

```bash
./aippt-cli.js call /v1/resource/upload --file ./input.pdf --pretty
```

上传成功后读取：

```text
data.data.resource_id
```

第二步：根据文件生成大纲。

把上一步得到的 `resource_id` 放入 `/v1/gpt/gen_outline_by_topic` 的 `resource_id_list`。如果用户没有额外给主题，可以把 `topic` 置空或写成概括性标题；如果用户同时给了主题或要求，应同时传入 `topic` 和 `resource_id_list`。

请求示例：

```json
{
  "topic": "",
  "stream": true,
  "model": "ali",
  "page_count": 25,
  "language": "zh",
  "scene": "公众演讲",
  "target_audience": "大众",
  "desc_info": "",
  "resource_id_list": ["上传返回的 resource_id"]
}
```

调用命令：

```bash
./aippt-cli.js call /v1/gpt/gen_outline_by_topic --data-file ./file_outline_request.json
```

第三步：复用关键字生成流程。

从大纲 SSE 最后一个 `finish_reason` 为 `stop` 的 `data:` JSON 中读取：

- `data.all_content`：最终大纲 Markdown。
- `data.content_ex_info`：后续生成完整内容使用。

然后继续执行“按关键字生成 PPT”的模板策略、`/v1/gpt/gen_content_by_outline`、`/v1/job/ppt_create_by_markdown`、`/v1/job/get` 轮询步骤。

## 常用接口

- `/v1/account/info`：获取账号信息。
- `/v1/template/list`：获取 PPT 模板列表。
- `/v1/template/get`：通过 `template_id` 获取单个模板。
- `/v1/gpt/gen_outline_by_topic`：根据主题生成 PPT 大纲。
- `/v1/gpt/gen_content_by_outline`：根据大纲生成完整 PPT 内容。
- `/v1/job/ppt_create_by_json`：通过结构化 JSON 创建 PPT。
- `/v1/job/ppt_create_by_markdown`：通过 Markdown 创建 PPT。
- `/v1/job/ppt_create_by_gpt`：创建 AI 生成 PPT 任务。
- `/v1/resource/upload`：上传资源文件。
- `/v1/job/get`：通过 `id` 获取单个任务。
- `/v1/job/get_pdf`：获取任务对应 PDF。
- `/v1/job/get_jump_link`：获取编辑或查看跳转链接。

不要猜测请求字段；优先使用 `schema` 查看接口结构，`apidoc.json` 是接口定义的来源。
