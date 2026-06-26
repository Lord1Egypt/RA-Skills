# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 当前仓库状态

- 当前项目根目录已经是多来源图片下载器的主线实现。
- 根目录包含 `image_downloader/` 模块、`scripts/bing_image_downloader.py` CLI 入口，以及模型、来源、存储、摘要和集成测试。
- 处理任务时默认以根目录当前实现为准，不再把它描述成“只有 Bing 单来源”的旧版本。

## 环境与执行约定

- 当前系统的 Python 使用 `uv` 进行管理。
- 涉及 Python 运行、依赖安装、测试执行时，优先使用 `uv`。
- 根目录目前没有 `pyproject.toml`；常用方式是直接用 `uv run --with requests python ...` 运行脚本或测试。

## 提交约定

- 本仓库进行 git 提交时，提交信息使用中文。

## 常用命令

### 运行主脚本

在项目根目录运行多来源图片下载器：

```bash
uv run --with requests python "scripts/bing_image_downloader.py" "cat" --limit 10 --pages 3
```

更大下载量时，按 README 中的经验值优先增加 `--pages`：

```bash
uv run --with requests python "scripts/bing_image_downloader.py" "cat" --limit 50 --pages 5
uv run --with requests python "scripts/bing_image_downloader.py" "cat" --limit 100 --pages 10
```

### 运行测试

运行当前根目录完整测试集：

```bash
uv run --with requests python -m unittest tests.test_bing_image_downloader tests.test_models_and_sources tests.test_storage tests.test_integration_multisource -v
```

运行单个测试模块时，可用 `unittest` 的点路径：

```bash
uv run --with requests python -m unittest tests.test_storage
```

如果要运行单个测试方法，也可继续使用 `unittest` 的点路径：

```bash
uv run --with requests python -m unittest tests.test_bing_image_downloader.TestBingImageDownloader.test_collect_image_urls_across_multiple_pages
```

### 冒烟验证

```bash
uv run --with requests python "scripts/bing_image_downloader.py" "cat" --limit 10 --pages 3
```

## 根目录代码架构

### 主脚本

- `scripts/bing_image_downloader.py`
  - 这是当前根目录的 CLI 入口。
  - 它负责组织多来源候选收集、候选去重、历史索引跳过、顺序下载和运行摘要输出。

### 主要模块

- `image_downloader/models.py`
  - 定义统一候选与记录模型。
- `image_downloader/sources/`
  - 提供来源接口以及 `bing`、`demo` 等来源实现。
- `image_downloader/storage.py`
  - 负责下载记录、历史索引与重复跳过。
- `image_downloader/reporting.py`
  - 负责构建运行摘要文本。

### 测试结构

当前根目录实现包含 4 个测试模块：

- `tests/test_bing_image_downloader.py`
  - 覆盖 CLI、兼容接口与主流程行为。
- `tests/test_models_and_sources.py`
  - 覆盖统一模型与来源接口。
- `tests/test_storage.py`
  - 覆盖存储、索引与历史去重逻辑。
- `tests/test_integration_multisource.py`
  - 覆盖多来源集成流程与摘要行为。

## README / SKILL 对齐提醒

来自 `README.md` 与 `SKILL.md` 的关键约定：

- 根目录当前实现已经完成多来源 MVP。
- 输出目录固定为 `downloads/<关键词>/`。
- 当目标数量较大时，优先增加 `--pages`，而不是先改并发。
- 常见失败通常来自第三方源站不可访问，例如：`403`、SSL 错误、超时、`404`；这不一定表示脚本主流程崩溃。
- `demo` 来源主要用于统一接口与失败容错验证，不应表述为稳定真实图片来源。

## 仓库内已确认不存在的配置

以下文件在当前根目录下未发现：

- `.cursorrules`
- `.cursor/rules/**`
- `.github/copilot-instructions.md`
- `pyproject.toml`

因此当前开发信息主要以 `README.md`、脚本源码、测试文件和项目内 worktree 结构为准。
