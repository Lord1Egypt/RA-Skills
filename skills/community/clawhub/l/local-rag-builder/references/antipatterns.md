# 反模式 — local-rag-builder

## 不要在 SKILL.md 正文写完整教程

**错误做法**：在 SKILL.md 中展开所有脚本的详细用法。

**正确做法**：SKILL.md 只写概要，详细教程拆分到 `references/guide.md`。本技能已遵循此规范。

## 不要硬编码模型路径

**错误做法**：
```python
model_path = "D:/models/bge-small-zh-v1.5"
```

**正确做法**：通过配置系统管理模型路径，支持 Web UI 和 CLI 动态切换。

## 不要在所有场景都用同一种切分策略

**错误做法**：对所有文档都用固定窗口切分。

**正确做法**：根据文档类型选择策略（Markdown → 标题切，长文 → 语义切，通用 → 递归切）。

## 不要忽略 Python 版本兼容性

**错误做法**：在 Python 3.12+ 上直接安装 chromadb。

**正确做法**：使用 `rag_env_setup.py` 检测版本，必要时创建 3.11 虚拟环境。
