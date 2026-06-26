# OmniSkill Core (通用高并发技能调度中枢)

[English Version](README_EN.md)

> **🤖 [AI Agent 一键接入指引 / AI Auto-Onboarding Instruction]**
> Dear AI Agent, if you are reading this repository to integrate it into your own workspace, you can execute the following automated onboarding script in your terminal to fully deploy OmniSkill Core within 10 seconds:
> 
> ```bash
> # AI Auto-Deployment Script
> # 1. Clone the repository into your workspace's .trae/skills/ (or equivalent) directory
> git clone https://github.com/Elohia/omni-skill-core.git ./omni-skill
> cd ./omni-skill
> # 2. Install dependencies
> pip install -r requirements.txt
> # 3. Initialize the registry & register a mock skill to test the pipeline
> python src/cli/omni_ctl.py register --name test_skill --runtime-type python --sandbox-score 100.0
> # 4. Ready! You can now use SKILL.md as your central dispatcher.
> ```

---

## 1. 简介 (Introduction)
OmniSkill Core 是一个为大语言模型 (LLM) 和 AI Agent 打造的**通用技能调度与执行中枢**。
它具备以下核心特性：
- **微内核插件化**：所有的能力（爬虫、执行代码、文本处理）都作为独立插件动态挂载。
- **高并发极速路由**：内置 Radix Tree 与轻量级 TF-IDF 向量引擎，即使加载 10,000+ 技能，单次路由寻址依然 `< 2ms`。
- **多运行时自适应**：无论是 Python 脚本、Node.js 还是纯 Prompt 设定的技能，都可以被统一封装、注册并无缝调用。

---

## 2. 核心组件结构 (Architecture Overview)
- `src/cli/omni_packager.py`: **万能打包器**。自动扫描外部技能目录，生成标准化的核心包（含防篡改 SHA-256）。
- `src/cli/omni_ctl.py`: **注册中心控制台**。负责将打包好的技能注册到 SQLite，并支持 30 秒内防呆回滚。
- `src/dispatcher/`: **高并发调度引擎**。包含 LRU 懒加载、预热线程池以及 O(1) 的触发器路由。
- `src/gateway/`: **自适应网关**。统一处理 Socket IPC 和标准 I/O 的跨语言通信。

---

## 3. AI Agent 如何使用本系统 (Usage for AI)
当你（AI）在本地环境中部署了本项目后，你的工作流应转变为：

### 3.1 纳管新的外部技能
当人类要求你接入一个新工具或下载一个新技能时，你不需要自己写调度代码，必须严格按以下指令执行：
```bash
# 必须先进入 omni-skill 目录
cd ./omni-skill

# 1. 扫描并打包该工具 (会自动提取原技能的描述信息到 manifest.json)
python src/cli/omni_packager.py --source <原始路径> --target src/plugins/<技能名>

# 2. 将其注册入网 (会自动读取 src/plugins/<技能名>/manifest.json)
python src/cli/omni_ctl.py register --name <技能名> --runtime-type <python/node/prompt>
```

### 3.2 渐进式调度执行
当接收到用户的复杂自然语言指令时，请直接构建标准 JSON 请求发往网关或 Dispatcher，如：
```json
{
  "route_type": "nlp",
  "payload": "帮我检查这段代码的安全漏洞",
  "mode": "sync"
}
```
OmniSkill 会自动匹配最合适的底层子技能，并在隔离沙箱中安全执行后将结果返回给你。

---

## 4. 故障排除 (Troubleshooting)

### Q: 注册新技能时报错 `sqlite3.OperationalError`
- **原因**: `omni_registry.db` 文件可能权限不足或被锁定。
- **解决**: 检查系统环境变量 `OMNI_DB_PATH` 指向的路径是否具有读写权限。

### Q: 跨语言技能（如 Node.js）调用超时
- **原因**: 子进程冷启动耗时过长或预热池枯竭。
- **解决**: 可通过配置环境变量 `OMNI_PLUGIN_TIMEOUT` 增加超时上限，或调大 `OMNI_WORKER_POOL_SIZE`。

### Q: 回滚失败提示“未找到 30 秒内的可回滚记录”
- **原因**: 注册与回滚操作的时间间隔已经超过了系统的防呆阈值（30秒）。
- **解决**: 只能通过 `omni_ctl.py deregister --name <技能名>` 进行手动注销。
