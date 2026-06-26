# MediaCrawler Automation

基于 [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler.git) 的多平台公开信息采集 skill，支持自动安装、命令行运行、WebUI、常用任务模板和结果定位。

## 这个 skill 做什么

- 自动检测 `git`
- 自动检测并安装 `uv`
- 从 GitHub 拉取或更新 MediaCrawler 项目
- 执行 `uv sync`
- 安装 Playwright Chromium
- 执行一次健康检查，确认主程序可以启动
- 提供常用搜索命令模板
- 提供 WebUI 启动命令
- 提供结果文件定位命令

## 默认项目目录

默认安装到：

```bash
$HOME/MediaCrawler
```

也可以通过环境变量覆盖：

```bash
PROJECT_PATH=/your/path/to/MediaCrawler
bash scripts/setup.sh
```

## 安装

```bash
bash scripts/setup.sh
```

## 安装脚本行为

脚本会依次执行：

1. 检查 `git`
2. 检查 `uv`，若缺失则尝试自动安装
3. 克隆项目；若目录已存在且是正确仓库，则执行 `git pull --ff-only`
4. 执行 `uv sync`（失败时自动重试一次）
5. 安装 Playwright Chromium
6. 执行 `uv run main.py --help` 做健康检查

## 使用方法

### 查看帮助

```bash
cd "$PROJECT_PATH"
uv run main.py --help
```

### 运行主程序

```bash
cd "$PROJECT_PATH"
uv run main.py
```

### 启动 WebUI

```bash
cd "$PROJECT_PATH"
uv run uvicorn api.main:app --port 8080 --reload
```

启动后访问：

```text
http://127.0.0.1:8080
```

### 抖音关键词搜索示例

```bash
cd "$PROJECT_PATH"
uv run main.py --platform dy --lt qrcode --type search --keywords "护肤" --headless false
```

### 小红书关键词搜索示例

```bash
cd "$PROJECT_PATH"
uv run main.py --platform xhs --lt qrcode --type search --keywords "护肤" --headless false
```

## 结果文件位置

当 `SAVE_DATA_OPTION = "jsonl"` 且 `SAVE_DATA_PATH = ""` 时，结果默认保存到：

```bash
data/{平台}/{存储格式}/
```

例如抖音：

```bash
data/douyin/jsonl/search_contents_YYYY-MM-DD.jsonl
data/douyin/jsonl/search_comments_YYYY-MM-DD.jsonl
data/douyin/jsonl/search_creators_YYYY-MM-DD.jsonl
```

例如小红书：

```bash
data/xiaohongshu/jsonl/search_contents_YYYY-MM-DD.jsonl
data/xiaohongshu/jsonl/search_comments_YYYY-MM-DD.jsonl
```

也可以通过：

```bash
--save_data_path "/your/custom/path"
```

指定自定义输出目录。

## 预定义命令

| 命令 | 说明 |
|------|------|
| `crawler-init` | 初始化环境（检查环境、拉取仓库、安装依赖、安装浏览器） |
| `crawler-help` | 查看主程序帮助 |
| `crawler-run` | 运行主程序 |
| `crawler-web` | 启动 WebUI（默认端口 8080） |
| `crawler-dy-search` | 抖音关键词搜索模板（二维码登录，有头模式） |
| `crawler-xhs-search` | 小红书关键词搜索模板（二维码登录，有头模式） |
| `crawler-results` | 查看当前结果文件列表 |

## 合规声明

- 仅供学习和研究使用
- 禁止用于非法用途或侵犯他人合法权益
- 执行前请确认目标行为合法合规
