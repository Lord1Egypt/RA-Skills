# 贵数 Images API 与终端使用

适用脚本版本：1.1.0。文生图沿用原版协议；参考图请求的重复 `image` 字段、蒙版和 2.5 质量处理对照贵数网页版客户端实现（2026-11-03）。本说明不承诺账户权限、上游可用性或真实计费结果。

## 入口与运行环境

- [ClawHub Skill](https://clawhub.ai/quqi1599/guishu-gpt-image-2)
- [贵数图片教程](https://llm-token.cn/tutorials/gpt-image-2)
- [Skills 支持说明](https://llm-token.cn/tutorials/skills-support)
- [网页版](https://image2.gpt-agent.cc/)
- Python 3.10+，无需 pip 依赖；Node.js/ClawHub CLI 只用于安装包，不用于执行 Python 脚本。

安装包后，终端命令中的脚本路径应指向实际安装目录。不要把 `{baseDir}` 原样粘贴到终端。自定义 OpenClaw 工作区须相应修改路径。

### macOS / Linux

在自己的终端中配置贵数 Key，不要发给 Agent：

```bash
export LLM_TOKEN_API_KEY="你的贵数Key"
python3 --version
python3 "$HOME/.openclaw/workspace/skills/guishu-gpt-image-2/scripts/generate.py" \
  --prompt "蓝色音箱产品海报，干净背景" --dry-run
```

确认参数后去掉 `--dry-run` 才会实际生图并产生费用。批量任务先用 dry-run 查看 `prompt_count` 和 `image_count`。

### Windows PowerShell

```powershell
$env:LLM_TOKEN_API_KEY = "你的贵数Key"
py -3 --version
$imageSkill = Join-Path $env:USERPROFILE '.openclaw\workspace\skills\guishu-gpt-image-2\scripts\generate.py'
py -3 $imageSkill --prompt '蓝色音箱产品海报，干净背景' --dry-run
```

如果安装时未启用 `py` 启动器，用 `python --version` 确认版本后，将 `py -3` 换成 `python`。上述环境变量仅在当前终端会话生效；从独立 GUI/服务启动的 Agent 不会自动继承，需在那个运行环境配置。不要为测试而修改全局凭据或代理。

## 请求协议

文生图：`POST https://api.llm-token.cn/v1/images/generations`，JSON。

```json
{"model":"gpt-image-2","prompt":"蓝色音箱产品海报，干净背景","size":"1024x1024","n":1,"quality":"high","response_format":"b64_json"}
```

参考图/编辑：`POST https://api.llm-token.cn/v1/images/edits`，`multipart/form-data`。文本字段与文生图相同，每张图一个 `image` 文件字段，可附一个 `mask` 字段。脚本负责 boundary，不能手填成普通 `application/json`。其他兼容服务明确要求 `image[]` 时使用 `--image-field 'image[]'`。

认证：`Authorization: Bearer <贵数Key>`。生成请求不跟随重定向；图片下载是无认证 GET，绝不携带生成 Key。下载仅允许 HTTPS 公网地址，重定向目标也会检查；签名 URL 过期可能无法恢复。

## 模型和参数

| 参数 | 本地行为与边界 |
|---|---|
| `--model` | 默认保留 `gpt-image-2`；可显式填写其他 Images API 模型，不能用图片模型代替 Agent 主对话模型 |
| `--quality` | 默认 `high`；支持 `auto/low/medium/high`；`xhigh/max` 只接受完整的 Flare/Sunburst ID |
| Flare/Sunburst 的 `auto` | 贵数地址上省略 `quality` 字段，让服务选默认值；自定义服务保留字面量 |
| `--size` | 默认 `1024x1024`，也可 `auto` 或 `宽x高`，本地检查每边 64–4096；不承诺全部尺寸或比例都被上游接受 |
| `--n` | 1–10，每条提示词的图片数；默认 1；本地上限不等于每个模型都支持 10 张 |
| `--image` | 可重复指定本地 PNG/JPEG/WebP，单张不超过 50 MiB，总量不超过 200 MiB，最多 16 张；这是脚本限制 |
| `--mask` | Alpha PNG，与第一张 PNG 图尺寸一致；二者各不超过 50 MiB；透明像素代表编辑区域 |
| `--response-format` | 默认 `b64_json`；也可 `url`；两种返回都可本地保存 |
| `--output-format` | `png/jpeg/webp`；未指定时沿用上游默认，落盘扩展名以图片实际文件头为准 |
| `--background` | `auto/opaque/transparent`，不指定就不发送；JPEG 不支持透明；具体模型是否支持透明须看结果 |
| `--output-compression` | 0–100，只与显式 JPEG/WebP 一起使用 |
| `--timeout` / `--download-timeout` | 默认 1200 / 120 秒的 socket 等待，不是整个作业的总耗时承诺 |
| `--json` | stdout 仅输出结果 JSON，stderr 输出进度，适合 Agent/脚本读取 |

不自动从普通模型切换 4K、Flare 或 Sunburst，不自动改变大小、质量或数量来绕过错误；这些选择会改变内容、可用性和费用。

## 保存和恢复

新任务必须使用空输出目录。默认在当前目录的 `outputs/guishu-image-日期-随机标识/` 创建任务目录。

| 文件 | 内容 |
|---|---|
| `NNN-II.png/jpeg/webp` | 原图字节；文件名不含提示词 |
| `state.json` | 每条任务状态、请求参数、提示词摘要哈希、request ID、文件哈希；恢复依据 |
| `response-NNN.json` | 恢复所需的图片 Base64 或 URL；默认移除修订提示词与不相关响应字段 |
| `request.json` | 每条任务的参数、状态和已保存数量；默认不包含 prompt |
| `index.html` | 已保存图片的本地预览；内容转义、无脚本；`--no-gallery` 不创建或更新 |
| `prompts.json` | 仅 `--save-prompts` 开启后写入，便于复用提示词；该选项也在 state/request 中保存提示词 |
| `.lock` | 防止两个进程同时写同一任务；进程退出后锁释放，不要在运行中删除 |

恢复示例：

```bash
python3 "$HOME/.openclaw/workspace/skills/guishu-gpt-image-2/scripts/generate.py" \
  --resume ./outputs/speaker --download-timeout 180 --json
```

`--resume` 不要求 Key，禁止混入新提示词、参考图、endpoint 或模型参数，不提交尚未开始的任务。原版 1.0.0 没有 `state.json`，不能直接恢复旧目录；已有原图保留，不能重生成冒充恢复。

HTTP 失败、连接中断或用户取消后，上游可能已受理。脚本保留状态而不猜测是否扣费；它没有通用账单查询能力，也不会虚构任务查询 URL。只有当用户明确确认重新生成时，才创建新目录进行新请求。批量失败后不要重跑整份提示词文件。

## 从 1.0.0 升级

- 已有文生图命令和 `--api-key` 参数保留；空提示词改为报错。
- 仅使用 `OPENAI_API_KEY` 的旧环境需改为贵数专用变量，或显式添加 `--key-env OPENAI_API_KEY`。
- 提示词记录从默认开启改为 `--save-prompts`；产物名称不再包含提示词英文摘要。
- 非空输出目录不允许新生成，避免覆盖旧结果；新任务使用新目录。
- 默认模型、方图尺寸和 high 质量不变；模型升级由用户明确选择。
- 本地/模拟测试不等于线上真实生图验收；发布新版本前应按授权测试一张新图和一张参考图编辑，并核对保存结果与用量。
