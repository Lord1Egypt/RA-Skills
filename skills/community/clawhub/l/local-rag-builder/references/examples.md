# 使用示例 — local-rag-builder

## 示例 1：完整搭建流程

```bash
# 1. 环境检测
cd ~/.workbuddy/skills/local-rag-builder
python scripts/rag_env_setup.py --auto-install

# 2. 下载嵌入模型
python scripts/embedding_model_manager.py --interactive
# 选择 1: BAAI/bge-small-zh-v1.5

# 3. 导入测试文档
echo "# 测试文档
RAG 即检索增强生成，是一种结合检索和生成的技术。
它先根据问题从知识库检索相关文档，再输入 LLM 生成答案。" > test_doc.md

# 4. 智能体调用（技能模式）
python scripts/rag_skill.py --query "什么是 RAG？" --json

# 5. 独立问答（需外部 LLM）
python scripts/rag_standalone.py --query "什么是 RAG？"
```

## 示例 2：Web 界面操作

```bash
# 启动 Web 面板
python scripts/rag_web_ui.py --port 8888
# 浏览器打开 http://localhost:8888
```

## 示例 3：智能体集成调用

```python
import subprocess
import json

SKILL_DIR = "~/.workbuddy/skills/local-rag-builder"
PYTHON = "python"

# 检测环境
result = subprocess.run(
    [PYTHON, f"{SKILL_DIR}/scripts/rag_env_setup.py", "--json"],
    capture_output=True, text=True
)
env_report = json.loads(result.stdout)

# 嵌入模型列表
result = subprocess.run(
    [PYTHON, f"{SKILL_DIR}/scripts/embedding_model_manager.py", "--list", "--json"],
    capture_output=True, text=True
)
models = json.loads(result.stdout)

# [技能模式] 纯检索（不依赖 LLM）
result = subprocess.run(
    [PYTHON, f"{SKILL_DIR}/scripts/rag_skill.py",
     "--query", "什么是 RAG？", "--json"],
    capture_output=True, text=True
)
data = json.loads(result.stdout)
context = data["context"]  # 智能体根据 context 自行回答

# [独立模式] 全链路问答
result = subprocess.run(
    [PYTHON, f"{SKILL_DIR}/scripts/rag_standalone.py",
     "--query", "什么是 RAG？", "--json"],
    capture_output=True, text=True
)

print(answer["answer"])
```

## 示例 4：多知识库管理

```bash
# 创建多个知识库
python scripts/knowledge_base_manager.py --create art --desc "艺术类资料"
python scripts/knowledge_base_manager.py --create tech --desc "技术文档"

# 配置自动分类规则
python scripts/knowledge_base_manager.py --set-rule art "艺术,美术,绘画"
python scripts/knowledge_base_manager.py --set-rule tech "编程,代码,算法,API"

# 测试分类
python scripts/knowledge_base_manager.py --classify "Python 编程语言"
# 输出: tech

python scripts/knowledge_base_manager.py --classify "梵高向日葵"
# 输出: art
```

## 示例 5：自定义 Prompt

```bash
# 配置带引用的 Prompt
python scripts/prompt_manager.py --set "你是严谨的研究助手。\n\n资料：\n{context}\n\n问题：{question}\n\n回答（请在末尾标注引用编号）："

# 验证模板
python scripts/prompt_manager.py --show
```
