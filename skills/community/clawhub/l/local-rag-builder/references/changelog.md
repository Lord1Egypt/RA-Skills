## 1.0.5 (2026-06-13)

### 修复
- refactor: 标准化改造（渐进式索引表格式修复、权限文档补充）

## 1.0.4 (2026-06-13)

### 新增
- KB 专属嵌入模型：每个知识库可独立选择嵌入模型，未指定时回退全局默认
- Web UI KB 管理新增模型下拉选择器
- `/api/kb-model`、`/api/kb-models` API 端点

### 修复
- `knowledge_base_manager.py` `create_knowledge_base()` 新增 `model_id` 参数
- `rag_core.py` `get_embeddings()` 新增 `kb_name` 参数，自动查 KB 专属模型

## 1.0.3 (2026-06-13)

### 修复
- 标准化改造：SKILL.md frontmatter 修复、权限文档补充、产出物路径合规
- 三端版本同步至 1.0.3

## 1.0.2 (2026-06-13)

### 修复
- 删除根目录 `.venv_rag` 遗留虚拟环境
- 同步三端版本号至 1.0.2

## 1.0.1 (2026-06-13)

### 修复
- `rag_core.py` 配置路径失效时无法回退到 `find_model_dirs()`（`if not model_path` 改为 `if not model_path or not os.path.exists(model_path)`）
- `rag_core.py` `HuggingFaceEmbeddings` 未限制本地加载（添加 `local_files_only=True` 避免加载失败时摸 Hub）
- `embedding_model_manager.py` `_check_integrity()` 将仅有 `config.json` 的目录误判为完整（改为要求至少有权重文件）
- 删除根目录残留的空 `data/` 目录

## 1.0.0 (2026-06-07)

## 0.5.0 (2026-06-06)

### 新增
- **运行模式切换**：新增 `mode` 配置（`integrated` / `standalone`）
  - Web UI LLM 卡片改为模式选择器，集成模式下隐藏 LLM 参数
  - 新增 `/api/mode` 端点：POST 切换模式
- **pip 锁自动清理**：`--cleanup-locks` 参数、`cleanup_pip_locks()` 函数、安装前自动清理 stale 锁
- **`--no-deps` 反锁死策略**：chromadb 自动分步安装（先 22 个 core deps 再本体）
- **`--mirror` 镜像选择**：支持 `aliyun / tencent / tsinghua / ustc` 国内镜像源
- **`--dry-run` 试运行模式**：只检测不安装，报告将要安装的包列表
- **流式输出**：`_pip_run()`、`run_command()` 改为 `Popen` 逐行流式输出，用户和 Bash 工具实时看到进度
- pip 安装日志自动写入 `data/logs/pip_install_*.log`

### 修复
- **`except Exception: pass` 吞异常**：install_packages 返回空 {} 却报"安装完成"，改为明确 catch + 报告
- **安装后验证**：`pip list` + `check_missing()` 双重确认才报 OK，不再虚假通过
- **包名标准化**：`list_installed()` 统一 `_`→`-`，修复 `huggingface_hub` vs `huggingface-hub` 不匹配
- **NameError**：`--auto-install` 失败提示中的 `{python}` 未定义
- **config.py `load_config()`**：`mode` 字段非 dict 导致 `.update()` 崩溃，兼容非 dict 顶层字段

### 重构
- SKILL.md 及全文件删除 WorkBuddy 特化引用，改为 `xxxx` 代指任意智能体
- 所有 docstring 和注释统一通用化描述

## 0.4.0 (2026-06-06)

### 修复
- **【关键】`rag_env_setup.py` pip 锁死导致 auto-install 报 OK 但啥也没装的 BUG**
  - 根因：`install_packages()` 内 `except Exception: pass` 吞掉 pip 升级超时异常，返回空 `{}`，调用方误判为安装成功
  - 修复：删除裸 `except: pass`，所有异常明确 catch 并报告
  - 修复：安装后通过 `pip list` + `check_missing()` 双重验证才报 OK
  - 修复：安装前自动检测并清理 stale pip 锁文件（Windows `%LOCALAPPDATA%/pip/ephem/`）
- **新增 pip 锁自动清理** — `--cleanup-locks` 参数、`cleanup_pip_locks()` 函数、安装前自动清理
- **新增 `--no-deps` 反锁死策略** — chromadb 自动分步安装（先 core deps 再本体），耗时过长的依赖图不会一次性解析
- **新增 `--mirror` 镜像选择** — 支持 `aliyun / tencent / tsinghua / ustc` 四个国内镜像源
- **新增 `--dry-run` 试运行模式** — 只检测不安装，报告将要安装的包列表
- **SKILL.md**：更新命令速查表，补充 `--cleanup-locks` 和 `--mirror`
- **`_pip_run()` 改为流式输出而非 `capture_output`**：修复 Bash 工具因长时间无字符输出而超时杀进程的问题
- **`list_installed()` 包名标准化**：修复 pip 输出 `huggingface_hub`（下划线）但 requirements 列表写 `huggingface-hub`（连字符）导致的验证误报
- **修复 NameError**：`--auto-install` 失败提示中的 `{python}` 未定义

## 0.3.0 (2026-06-06)

### 重构
- **双模式架构**：拆分为 `rag_skill.py`（技能模式，纯检索无 LLM）和 `rag_standalone.py`（独立模式，检索+LLM 全链路）
- `rag_core.py` 删除所有 LLM 依赖，改为纯核心层。新增 `format_skill_output()` 返回结构化 JSON（含已填充 prompt）
- `embedding_model_manager.py`：路径查找改为通用内容感知方案（`_normalize` + `_name_similarity` + `_is_model_dir`），不再依赖任何特定变形模式

### 新增
- `rag_skill.py`：零 LLM 依赖的技能接口，仅返回结构化 JSON，供任何智能体使用
- `rag_standalone.py`：独立系统，含交互式 CLI + `/llm-help` 命令 + 内置三个 LLM 方案接入指南
- `references/llm-setup.md`：结构化 LLM 接入文档（LM Studio / Ollama / vLLM 三方案含配置方式）

### 修复
- `rag_web_ui.py`：修复 `verify_llm_connection` 导入路径（已迁移到 rag_standalone）
- `config.py`/`prompt_manager.py`/`rag_env_setup.py`：exception 覆盖加固
- R-10/R-11/R-23 合规修复（产出物路径迁移、文档引用更新）
- 文档引用 `rag_interface.py` 全部更新为 `rag_skill.py`/`rag_standalone.py`

## 0.2.0 (2026-06-06)

- 重构: 嵌入模型路径查找改为通用内容感知方案（`_normalize` + `_name_similarity` + `_is_model_dir`），不再依赖特定变形模式
- 重构: `verify_model` 改用 `_is_model_dir` 通用检测
- 重构: `get_model_path` 改用相似度评分匹配
- 修复: exception 覆盖率加固（config.py/prompt_manager.py/rag_env_setup.py）
- 测试: 功能测试通过（D1-D6: 0 BLOCK, 57 WARN）

## 0.1.1 (2026-06-06)

- 修复: 数据目录路径合规（R-12）
- 修复: frontmatter 补充 trigger/trigger_negative/license 字段
- 修复: 版本号格式合规

## 0.1.0 (2026-06-06)

- 初始版本
- 环境自动检测与修复（Python 版本、缺失包）
- 嵌入模型多源下载（ModelScope/HuggingFace/LLM 搜索）
- 完整性校验与路径修正
- 6 种文本切分策略 + 组合切分
- 多知识库管理与自动分类
- Prompt 模板持久化
- Web 可视化配置界面
- 结构化 JSON 接口（智能体调用）
- 交互式 CLI 界面
