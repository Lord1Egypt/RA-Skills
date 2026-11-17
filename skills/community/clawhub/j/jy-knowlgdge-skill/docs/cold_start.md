# 冷启动完整指南

> 从空白服务器到 JY_Knowledge_Skill 可用的完整流程。
> **核心原则：每一步缺失都不要自作主张，先告知用户当前状态，获取确认后再执行下一步。**

## 流程总览

```
检测 Python → 安装 pip 依赖 → 配置 config.json → 安装 Docker → 部署 EasyDataset → 部署 MongoDB → 验证
    ↓               ↓                  ↓                ↓              ↓               ↓           ↓
 未安装?        缺失库?           config不存在?      docker不存在?    API不通?       容器未运行?   红灯?
    ↓               ↓                  ↓                ↓              ↓               ↓           ↓
 告知用户       列出缺失项          逐项询问          告知用户        询问用户        询问用户     定位Phase
 等待安装       询问是否安装        用户提供信息后     等待安装        确认后部署      确认后部署    修复
                确认后执行          生成config        确认后继续       curl验证        docker验证   重新验证
```

## Phase 1：Python 环境

**检测命令**：
```bash
python --version
# 或 python3 --version
```

**未安装时的用户交互话术**：
> 当前服务器未检测到 Python。JY_Knowledge_Skill 需要 Python 3.10+。
> 请从 https://www.python.org/downloads/ 下载安装，安装时勾选"Add Python to PATH"。
> 安装完成后请回复"已安装"，我会继续检测。

## Phase 2：Python 依赖

**检测命令**：
```bash
cd <skill目录>/JY_Knowlgdge_Skill
python tools/check_env.py
```

`tools/check_env.py` 会逐个检测 9 个关键依赖并报告缺失情况。

**检测逻辑（供 Model 手动检测时参考）**：
| 库 | 用途 | 检测命令 |
|----|------|----------|
| `requests` | HTTP API 调用 | `python -c "import requests"` |
| `pymongo` | MongoDB 驱动 | `python -c "import pymongo"` |
| `mammoth` | DOCX → Markdown | `python -c "import mammoth"` |
| `openpyxl` | Excel 读写 | `python -c "import openpyxl"` |
| `Pillow` | 图片处理 | `python -c "import PIL"` |
| `matplotlib` | 表格截图 | `python -c "import matplotlib"` |
| `pdfplumber` | PDF 文本提取 | `python -c "import pdfplumber"` |
| `pymupdf` | PDF 转图片 | `python -c "import fitz"` |
| `pandas` | CSV/表格处理 | `python -c "import pandas"` |

**部分缺失时的用户交互话术**：
> 检测到以下 Python 依赖缺失：[列出缺失的库]。
> 是否允许我执行 `pip install` 安装全部依赖？
> 
> 完整安装命令：
> ```bash
> pip install -r <skill目录>/JY_Knowlgdge_Skill/requirements.txt
> pip install Pillow
> ```

等用户回复"允许"/"执行"/"是"后，再执行 pip install。

## Phase 3：配置文件 config.json

**检测**：检查 `config.json` 是否存在（路径由用户指定，默认与 skill 同目录）。

**不存在时的用户交互——分批询问，不一次性列所有问题**：

**第一批——LLM 模型信息**：
> 技能需要 LLM 模型来执行分类和价值评估。请提供：
> - LLM API 地址（如 `http://192.168.x.x:1234/v1`）
> - API Key
> - 模型名称（如 `JY-Qwen3.6`）

**第二批——视觉模型信息**：
> 技能需要视觉 LLM 来分析文档中的图片。请提供：
> - 视觉模型 API 地址（通常与 LLM 相同）
> - API Key（如相同可复用）
> - 视觉模型名称

**第三批——存储路径**：
> 请确认以下数据存储路径（回车使用默认值）：
> - 数据集输出：默认 `<skill目录>/datasets`
> - 预处理缓存：默认 `<skill目录>/processed`
> - 上传文件：默认 `<skill目录>/uploads`
> - EasyDataset 服务地址：默认 `http://localhost:1717`
> - MongoDB 连接：默认 `mongodb://localhost:27017`

## Phase 4：Docker 环境

**检测命令**：
```bash
docker --version
```

**未安装时的用户交互话术**：
> 当前服务器未检测到 Docker。EasyDataset 和 MongoDB 需要 Docker 环境。
> - Windows：请从 https://www.docker.com/products/docker-desktop/ 下载安装
> - Linux：请执行 `curl -fsSL https://get.docker.com | sh`
> 安装完成后请回复"已安装"，我会继续部署服务。

## Phase 5：EasyDataset

**检测命令**：
```bash
curl -s http://localhost:1717/api/projects
```

**连接失败时的用户交互话术**：
> EasyDataset 未运行。需要执行 Docker 部署。是否允许我执行以下命令？
> ```
> docker pull ghcr.io/conardli/easy-dataset:latest
> docker rm -f easy-dataset 2>/dev/null
> docker run -d --name easy-dataset --restart unless-stopped -p 1717:3000 ghcr.io/conardli/easy-dataset:latest
> ```

用户确认后执行。部署后 curl 验证。详细部署指南见 `docs/easydataset_deploy.md`。

## Phase 6：MongoDB

**检测命令**：
```bash
docker ps --format '{{.Names}}' | grep knowledge-mongo
```

**未运行时的用户交互话术**：
> MongoDB 未运行。需要执行 Docker 部署。是否允许我执行以下命令？
> ```
> docker pull mongo:7
> docker rm -f knowledge-mongo 2>/dev/null
> docker run -d --name knowledge-mongo --restart unless-stopped -p 27017:27017 -v <用户指定的数据目录>:/data/db mongo:7
> ```

## Phase 7：最终验证

```bash
cd <skill目录>/JY_Knowlgdge_Skill
python main.py -t
```

**四盏绿灯全亮** → 环境就绪，开始使用。
**任何红灯** → 根据失败服务回到对应 Phase 修复。

## 意外情况处理通则

| 意外 | 行为 |
|------|------|
| 任何命令执行失败 | 打印完整错误输出，将错误粘贴给用户判断，不自重试超过 3 次 |
| 用户说"跳过"某 Phase | 标记为未完成，后续用到该依赖时再次提示 |
| 端口被占用 | 询问用户更换端口还是停止占用进程 |
| 磁盘空间不足 | 告知用户，暂停所有操作 |
| 权限不足（Permission denied） | 告知需要管理员权限，等确认后再执行 |
| LLM API 不可达 | 提示确认地址/端口是否正确，是否在防火墙白名单中 |
| Docker daemon 未启动 | Windows: 确认 Docker Desktop 在运行；Linux: `sudo systemctl start docker` |
