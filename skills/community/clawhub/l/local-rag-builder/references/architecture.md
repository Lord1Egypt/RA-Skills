# 架构设计 — local-rag-builder v1.0.0

## 整体架构

```
┌─────────────────────────────────────────────────────┐
│             CLI (rag_skill.py / rag_standalone.py)    │
│                    Web UI (rag_web_ui.py)           │
├─────────────────────────────────────────────────────┤
│   rag_core.py         (RAG 问答核心)                │
│   text_splitter.py    (5 切分策略 + GuardStack + 后处理 + 插件注册)  │
│   knowledge_base_manager.py (多知识库管理)           │
│   prompt_manager.py   (Prompt 模板管理)              │
│   embedding_model_manager.py (嵌入模型生命周期)       │
│   rag_env_setup.py    (环境检测与安装)               │
├─────────────────────────────────────────────────────┤
│   config.py           (统一配置管理)                 │
│   utils.py            (通用工具函数)                 │
├─────────────────────────────────────────────────────┤
│   data/ (技能数据目录)                               │
│   ├── kb/             (向量知识库)                   │
│   ├── models/         (嵌入模型)                     │
│   ├── prompts/        (Prompt 模板)                 │
│   ├── config/         (运行时配置)                   │
│   └── output/         (导出产物)                     │
└─────────────────────────────────────────────────────┘
```

## 模块依赖关系

```
rag_skill.py / rag_standalone.py (双入口)
  ├── rag_core.py
  │   ├── config.py ← utils.py
  │   ├── prompt_manager.py ← utils.py
  │   ├── text_splitter.py
  │   └── knowledge_base_manager.py ← utils.py
  ├── embedding_model_manager.py ← utils.py
  └── rag_env_setup.py

rag_web_ui.py (入口)
  ├── config.py ← utils.py
  ├── prompt_manager.py ← utils.py
  ├── text_splitter.py        ← 策略注册表 + 守卫注册表
  ├── embedding_model_manager.py
  ├── knowledge_base_manager.py
  └── rag_core.py
```

## 数据流

### 索引流程（文档入库）
```
文档 → text_splitter.py (切分) → embeddings (向量化) → Chroma (存储)
```

### 切分流水线架构

```
原始文本 → [守卫栈(多选)] → [主策略(单选)] → [后处理(单选/不选)] → 最终 chunks

守卫栈：mermaid / code / math / table / html（可扩展）
主策略：fixed / recursive / headers / sentence / semantic（可扩展）
后处理：recursive / fixed / semantic 子切（metadata 白名单继承）
```

## 查询流程（问答）
```
用户问题 → embeddings (向量化) → Chroma (检索) → 上下文 + Prompt → LLM → 回答
```

## 数据目录结构

```
skills/.standardization/local-rag-builder/data/
├── kb/                    # 向量知识库
│   ├── default/           # 默认知识库
│   ├── art/               # 艺术类 (按分类规则)
│   ├── politics/          # 政治类
│   └── kb_index.json      # 知识库索引
├── models/                # 嵌入模型
│   └── model_index.json   # 模型索引
├── prompts/               # Prompt 模板
│   └── custom_prompt_template.txt
├── config/                # 运行时配置
│   └── rag_config.json
├── output/                # 导出产物
├── cache/                 # 下载缓存
├── config_templates/      # 配置模板
└── kb/
    ├── default/
    ├── kb_index.json
    └── auto_classify_rules.json  # 分类规则
```

## 配置体系

配置由 `config.py` 统一管理，JSON 格式存储。

配置层级：
1. 默认配置（`DEFAULT_CONFIG` 硬编码）
2. 持久化配置（`data/config/rag_config.json`）
3. 运行时更新（通过 Web UI 或 CLI）

重置操作将删除持久化配置并恢复默认值。
