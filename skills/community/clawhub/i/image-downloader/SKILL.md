---
name: image-downloader
description: 当用户需要按关键词批量下载图片、从 Bing 或多个图片来源收集候选、保存图片到本地目录、避免重复下载，或希望复用当前仓库里的现成图片下载流程时使用。遇到类似“帮我按关键词下载 10 张图片”“批量抓取 Bing 图片并保存到本地”“从多个来源收集图片候选再下载”“需要下载摘要和保存目录”这类请求时，应主动使用这个 skill。
---

# 多来源关键词图片批量下载

这个 skill 用于复用当前目录中的 `scripts/bing_image_downloader.py` 脚本，让其他 agent 能稳定完成“按关键词从多个来源收集候选并下载图片到本地”的任务。

## 项目链接

- GitHub 仓库：https://github.com/16Miku/image-downloader-skill
- ClawHub 页面：https://clawhub.ai/16miku/image-downloader

## 何时使用
当用户明确提出以下类型需求时，优先使用本 skill：
- 按关键词批量下载公开图片到本地
- 想从 Bing 或当前脚本支持的多个来源收集图片候选
- 想保存 10、50、100 张关键词图片到本地目录
- 想通过增加页数或扩大候选池来提高最终成功数量
- 想复用现成脚本执行下载，并拿到保存目录、成功数量和运行摘要
- 想避免重复下载之前已经保存过的内容

如果用户要的是：
- 其他搜索引擎或站点的专用下载器开发
- 图像识别、分类、审核、打标
- 非关键词方式（例如固定页面 URL 批量抓取）

则这个 skill 不是最佳选择。

## 依赖文件
- 主脚本：`scripts/bing_image_downloader.py`
- 测试文件：`tests/test_bing_image_downloader.py`
- 集成测试：`tests/test_integration_multisource.py`

## 工作流程
按下面顺序执行：

1. 读取用户需求中的关键词、目标数量、页数。
2. 如果用户没给页数，按下面经验值选择：
   - 10 张：`--pages 3`
   - 50 张：`--pages 5`
   - 100 张：`--pages 10`
3. 运行脚本：
   - 如果当前环境有 `uv`，使用 `uv run --with requests python` 运行。
   - 如果没有 `uv`（例如服务器、容器、OpenClaw Agent），直接使用 `python3` 运行，需确保 `requests` 已安装。
4. 检查输出中：
   - 成功下载数量
   - 候选总数与去重后数量
   - 来源统计
   - 失败原因（常见为 403、SSL、超时）
5. 向用户汇报：
   - 实际保存目录
   - 成功数量
   - 是否达到目标数量
   - 当前来源统计
   - 如未达标，说明通常是第三方源站拒绝访问、超时或链接失效，而非脚本崩溃

## 推荐命令模板

### 有 uv 环境

#### 下载 10 张
```bash
uv run --with requests python "scripts/bing_image_downloader.py" "cat" --limit 10 --pages 3
```

#### 下载 50 张
```bash
uv run --with requests python "scripts/bing_image_downloader.py" "cat" --limit 50 --pages 5
```

#### 下载 100 张
```bash
uv run --with requests python "scripts/bing_image_downloader.py" "cat" --limit 100 --pages 10
```

### 无 uv 环境（服务器 / OpenClaw Agent）

```bash
python3 "scripts/bing_image_downloader.py" "cat" --limit 10 --pages 3
```

## 参数映射规则
- 用户说“下载 10 张” → `--limit 10`
- 用户说“下载 50 张” → `--limit 50`
- 用户说“下载 100 张” → `--limit 100`
- 用户没说页数时，按上面的推荐默认值设置 `--pages`
- 用户明确给出页数时，尊重用户输入

## 输出说明
脚本会把结果保存到：
```text
downloads/<关键词>/
```

例如关键词 `cat` 会保存到：
```text
downloads/cat/
```

文件名按顺序编号，例如：
- `001.jpg`
- `002.jpg`
- `003.png`

此外，脚本会记录下载元数据与历史索引，用于后续运行时跳过已下载过的候选内容。

## 常见问题解释
### 为什么会出现下载失败？
因为搜索结果中的原图通常来自第三方网站，不是都由当前来源自己托管。第三方站点可能拒绝脚本访问，常见错误：
- `403 Forbidden`
- SSL 证书错误
- 连接超时
- 404 Not Found

### 为什么加大 `--pages` 后下载数量会提高？
因为脚本会抓更多结果页，收集更大的候选链接池。即使其中一部分链接失效，仍然可以用后面的候选补位。

## 给用户的汇报模板
完成后可按下面结构回复用户：

```text
已执行关键词图片批量下载。
- 关键词：<关键词>
- 目标数量：<limit>
- 抓取页数：<pages>
- 候选总数：<候选数量>
- 去重后数量：<去重后数量>
- 实际成功下载：<成功数量>
- 来源统计：<来源统计>
- 保存目录：downloads/<关键词>/

如果存在失败链接，通常是第三方图片源拒绝访问、超时或链接失效，不影响脚本继续补充后续候选。
```

## 注意事项
- 这是一个“按关键词下载公开图片”的现成流程复用 skill，当前来源至少包含 Bing，不要把它表述成通用全网图片下载器。
- 优先复用现有脚本，不要重复手写新下载器，除非用户明确要求修改或升级脚本。
- 当用户要求“提高下载数量”时，优先建议增加 `--pages` 或扩大候选池，而不是先改成并发下载。
- 当用户提到”不想重复下载”时，应明确说明当前流程支持基于历史索引跳过重复候选。

## OpenClaw Agent 定时任务

本 skill 已在 OpenClaw Agent 上完成实际验证，支持通过 cron 定时任务自动下载图片并发送到飞书。

### 定时任务执行流程

1. 设置 `PATH` 和 `bash` 严格模式
2. 检查 Python 和 `requests` 环境
3. 执行图片下载脚本
4. 检查下载目录中的图片文件
5. 逐张调用 `openclaw message send` 发送到飞书
6. 记录结果到日志

### 发送到飞书的正确命令

```bash
openclaw message send \
  --channel feishu \
  --target “<飞书接收人 open_id>” \
  --media “/path/to/downloads/关键词/001.jpg” \
  --json
```

### 已验证的注意事项

- `demo` 来源的 `NameResolutionError` 报错是正常现象，可忽略
- “实际成功下载 0”可能是历史去重生效，不代表任务失败
- cron 环境中需要显式设置 `PATH`，避免找不到 `python3` 或 `openclaw`
- 发送失败时优先检查 CLI 命令格式，不要先入为主认为是权限问题

详细部署步骤和脚本模板见 `README.md` 的”OpenClaw Agent 部署与定时任务”章节。
