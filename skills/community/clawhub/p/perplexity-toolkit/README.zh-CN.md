# Perplexity Toolkit

[English](README.md) | **简体中文**

## 简介

Perplexity Toolkit 通过浏览器控制自动化 Perplexity AI 搜索 — 支持搜索、提取、批量处理和结果分析。

## 核心功能

- **4 种搜索模式**：标准搜索（Standard）、深度研究（Deep Research）、模型委员会（Model Council）、逐步学习（Step-by-step Learning）
- **批量流水线**：批量搜索数百条查询，支持断点续跑与速率限制
- **结果聚合**：去重来源、按频次排序、自动生成报告
- **来源提取**：获取所有引用链接，含标题与摘要
- **追问捕获**：提取 Perplexity 推荐的后续追问问题
- **常驻控制台**：固定 tab/group 工作台——任务线程、分步命令、模型切换、附件、可选 Jev 判真
- **历史管理**：查看与管理搜索历史
- **Agent Skills**：[`skills/`](skills/) 下三份可直接加载的 `SKILL.md`——路由策略、会话纪律、验证规则——供驱动本工具包的 agent 使用

## 快速开始

```bash
# 安装（推荐）：让 `perplexity` 进入 PATH
pipx install git+https://github.com/mfang0126/perplexity-toolkit.git

# 或开发模式，只装进「当前」环境：
#   pip install -e .
# 用 pip 时务必装进 agent 实际运行的那个环境，
# 否则 `command -v perplexity` 找不到它。

# 单次搜索
perplexity search "2026 年最好的 AI 编程助手"

# 多条 CLI 命令共用同一个任务 session；全局选项必须放在子命令前
perplexity --session-prefix coding-agents-2026 search "2026 年最好的 AI 编程助手"

# 仅在明确需要时跳过默认质量/readback 标注
perplexity --no-verify search "2026 年最好的 AI 编程助手"

# 深度研究（多步推理，约 60–120 秒）
perplexity search "2026 年 AI 安全风险" -m deep_research

# 从文件批量搜索
perplexity batch -i queries.json -o results.json

# 聚合结果并生成报告
perplexity aggregate results.json -f markdown

# 查看搜索历史
perplexity history
```

搜索默认会附加质量检查。JSON 输出始终是 stdout 上的单个 JSON 文档，
不会再混入人类可读的质量文本。质量结果区分 HTTP 可达性和有界页面
readback，并在逐条 claim 经过人工或语义证据核验前标记为
`verification_state: candidate`、`claim_support: not_evaluated`。

## CLI 命令一览

| 命令 | 说明 |
| --- | --- |
| `perplexity search` | 单次搜索（4 种模式可选） |
| `perplexity batch` | 批量搜索，支持恢复与限速 |
| `perplexity aggregate` | 聚合结果、去重来源、生成报告 |
| `perplexity history` | 管理搜索历史 |
| `perplexity console` | 常驻控制台：固定 tab/group、任务线程、分步命令、模型切换、附件、可选 Jev 判真 |

## 常驻控制台（固定 tab / 固定 group）

锁定一个 tab 一个 group 专门给 Perplexity，每个任务 = 一个线程：

```bash
perplexity console ask "问题" --task my-project -f json    # 创建或续接任务线程
perplexity console ask "追问" --task my-project            # 同一线程内追问
perplexity console ask "新话题" --new-thread --task other  # 同一 tab 内开新线程
perplexity console status | threads | selfcheck
```

- 每步都有读回闸门（输入框等值+编辑器状态、提问轮次归属、完成信号、轮次作用域提取）；失败必带截图证据（`~/.perplexity-console/evidence/`），不会把未验证结果当作成功。
- 状态落盘 `~/.perplexity-console/state.json`；daemon 重启后自动重建 tab 并回到保存的线程 URL（session→tab 映射仅存于 daemon 内存）。
- 编辑器与内部状态脱钩时先做一次有界重载自愈，仍失败则大声报错。
- 分步命令 `fill / submit / wait / extract / send / attach / files / detach / open` 由 staged-turn 账本衔接——可单独重试、可自由组合（意图驱动）。
- `perplexity console models` / `model "<名称>"` 切换模型（回读验证）；`ask --file` 附加文件（≤8MB，chip 验证）。
- 可选 Jev 判真（`--judge` 或 `PERPLEXITY_CONSOLE_JUDGE=1`）：提取判真 + 失败路由；fill/wait/extract 失败时按 Jev 处置执行**一次**有界恢复（重跑全部原闸门），发送路径保持只建议；fail-open，管道永不依赖它。

## Python API

```python
from perplexity_toolkit.search import search, deep_research, model_council

# 标准搜索
result = search("Python vs Rust 2026")
print(result["answer"])      # 完整回答文本
print(result["sources"])     # [{text, href}, ...]
print(result["follow_ups"])  # ["追问问题", ...]

# 深度研究（更详细、耗时更长）
result = deep_research("AI agent 框架对比")

# 模型委员会（多模型多角度回答）
result = model_council("新手最适合学什么编程语言")
```

## 批次流水线

```python
from perplexity_toolkit.batch import run_batch

queries = [
    {"query": "主题 1", "mode": "search"},
    {"query": "主题 2", "mode": "deep_research"},
]
results = run_batch(queries, output_file="results.json", delay=5.0)
```

## 架构

```
perplexity_toolkit/
├── __init__.py          # 包初始化
├── config.py            # 配置管理
├── search.py            # 核心搜索函数（4 种模式）
├── batch.py             # 批量流水线（支持恢复）
├── aggregator.py        # 结果聚合与报告
├── history.py           # 会话历史管理
├── verify.py            # 来源/答案质量校验
├── routing.py           # 用户意图路由门（CLI vs 直连浏览器）
├── console.py           # 常驻控制台（固定 tab/group，逐步闸门）
├── console_judge.py     # 可选 Jev 判真层（advisory，fail-open）
├── drivers/             # 浏览器驱动抽象层
│   ├── base.py          # 抽象 BrowserDriver 接口
│   └── webbridge.py     # Kimi WebBridge 实现
├── utils/               # DOM 解析与事件/时序辅助
│   ├── __init__.py
│   ├── antidetect.py    # 拟人节奏 / 反检测
│   └── i18n.py          # 界面文案多语言表
└── commands/            # CLI
    └── cli.py
```

## 浏览器驱动

工具包基于抽象 `BrowserDriver` 接口。当前实现：

- **WebBridgeDriver** — Kimi WebBridge（Chrome 扩展 + 本地守护进程）

这是**唯一**已实现的后端。所有搜索模式都通过它驱动真实的已登录浏览器，
没有 API key 或无头模式路径。`aggregate` 是唯一不需要浏览器的子命令，
因为它只对你已经抓取到的结果 JSON 做后处理。

接入新后端（Playwright、Selenium 等）时，在 `drivers/` 下实现 `BrowserDriver`：

```python
from perplexity_toolkit.drivers.base import BrowserDriver

class PlaywrightDriver(BrowserDriver):
    def navigate(self, url, new_tab=True, group_title=""): ...
    # Optional session hygiene hook; unsupported drivers may omit it.
    def list_tabs(self): ...
    def snapshot(self): ...
    def click(self, selector): ...
    def fill(self, selector, value): ...
    def evaluate(self, code): ...
    def screenshot(self, path=None): ...
    def close(self): ...
```

## 环境要求

- Python 3.9+
- Kimi WebBridge 守护进程（`~/.kimi-webbridge/bin/kimi-webbridge start`）
- 已安装 Kimi WebBridge 扩展的 Chrome 浏览器
- Perplexity 账号（免费版或 Pro 均可）

## 安装后自检

按顺序跑这三步，每一步隔离一类故障。

```bash
# 1. 命令是否可达？
command -v perplexity && perplexity --help >/dev/null && echo "CLI OK"

# 2. WebBridge 守护进程是否启动？
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"list_tabs"}'

# 3. Chrome 是否已连接？
#    守护进程正常时第 2 步返回 {"ok":true,...}。
#    若返回 "no extension connected"，说明进程在跑但 Chrome 没接上——
#    打开 Chrome 并检查 WebBridge 扩展。
```

| 现象 | 原因 | 处理 |
|---|---|---|
| `command -v perplexity` 找不到 | 装进了不在 `PATH` 上的环境 | `pipx install git+https://github.com/mfang0126/perplexity-toolkit.git`，或 `export PERPLEXITY_BIN=/完整/路径/perplexity` |
| curl 连 10086 失败 | 守护进程没启动 | `~/.kimi-webbridge/bin/kimi-webbridge start` |
| 守护进程返回 `no extension connected` | Chrome 未接入 | 打开 Chrome，确认 WebBridge 扩展已启用。这**不是**限流或会话数上限 |
| 搜索返回空答案 | 该浏览器未登录 Perplexity | 在同一个 Chrome profile 登录 perplexity.ai |

给 agent 作者的提醒：不要用裸的 `python3 -c "import perplexity_toolkit"` 做探测。
工具包只存在于安装它的那个环境里，通常不是 `python3` 解析到的解释器。
应改为探测可执行文件（`command -v perplexity`、`$PERPLEXITY_BIN`、
`$VIRTUAL_ENV/bin/perplexity`），并把结果报告为「当前环境未解析到」而不是「未安装」。

## 已知限制

- 深度研究模式会在查询中多出一个 "/" 前缀（Perplexity 可正常处理）
- Jev 子菜单模型项（如 "GPT-5.6 Sol | Max"）会出现在 `console models` 列表中，但暂不支持程序化选择
- 控制台附件通过页内注入上传，上限 8MB；更大文件需为 Kimi 扩展开启 Chrome 的「允许访问文件网址」，走官方 WebBridge 上传通道

## 许可

MIT

