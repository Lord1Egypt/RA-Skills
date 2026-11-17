# 常见问题 (FAQ) — local-rag-builder

Q: 为什么 Python 3.12 无法安装 chromadb？
A: chromadb 的 Windows 预编译轮子最高支持到 Python 3.11。建议使用 conda 创建 3.11 虚拟环境。

Q: 模型下载失败怎么办？
A: 本工具内置 4 个下载源（ModelScope、HuggingFace 镜像、官方源、LLM 搜索），每个源会自动重试 3 次。如果全部失败，可以尝试：
1. 配置环境变量 `HF_ENDPOINT` 为 `https://hf-mirror.com` 后重试
2. 使用 `--interactive` 模式选择其他源
3. 手动下载后使用 `--check` 验证

Q: 多个知识库如何切换？
A: 在 CLI 中使用 `/kb use <name>` 命令，或在配置文件的 `kb.active_kb` 字段指定。

Q: Prompt 模板如何持久化？
A: Prompt 模板保存在 `data/prompts/custom_prompt_template.txt`，程序重启后自动加载。使用 `/prompt set` 或 `--set` 命令配置后即持久化。

Q: 如何重置所有配置恢复到初始状态？
A: 运行 `python -c "from config import reset_config; reset_config()"` 或从 Web 界面点击"重置配置"按钮。这会清除 `data/config/rag_config.json` 并恢复默认值，同时重置 Prompt 模板。注意：重置不会删除知识库数据和已下载的嵌入模型。

Q: 本技能和本地 LLM（如 LM Studio）是什么关系？
A: 本技能本身可以扮演 LLM 角色，但如果你有本地运行的 LM Studio / Ollama 等服务，也可以通过配置 LLM 地址接入。技能自动适配两种模式。

Q: 向量的相似度阈值如何配置？
A: 在检索配置中配置 `score_threshold`（0-1 之间的浮点数），设为 `null` 则不启用阈值过滤。

Q: Windows 上模型路径名变形如何处理？
A: ModelScope 下载的模型名中 `.` 可能变为 `___`（如 `bge-small-zh-v1___5`）。本工具会自动检测并修正路径，无需手动处理。
