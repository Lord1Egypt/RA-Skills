# 毛选.SKILL

为 OpenClaw 提供《毛泽东选集》本地知识库检索能力。

项目地址：https://github.com/henryczq/mao-selected-works-skill.git

## 项目说明
录入《毛选》1-7卷（静火版）语料，建立本地知识库，支持关键词和AI知识库检索两种检索模式。
默认只支持关键词检索。
如果需要开启AI知识库检索，需要配置API key。内置了嵌入模型BAAI/bge-m3、重排模型BAAI/bge-reranker-v2-m3，和硅基流动url，大家如果使用硅基流动，只需要配置环境变量MAO_SKILL_API_KEY即可。


## 快速开始

```bash
# 建立索引
python scripts/build_index.py

# 检索
python scripts/search.py search "没有调查没有发言权"
```

## 目录结构

```text
mao-selected-works/
├── SKILL.md              # Skill 定义
├── README.md             # 本文档
├── data/                 # 毛选语料 Markdown
├── scripts/
│   ├── build_index.py    # 建立索引
│   ├── search.py         # 检索
│   ├── config.py         # 配置管理
│   └── common.py         # 公共函数
├── config/
│   ├── search.json       # 当前配置
│   └── search.example.json
├── agents/
│   └── openai.yaml
└── references/            # 参考文档
    ├── corpus-format.md
    ├── retrieval-rules.md
    └── output-schema.md
```

## 配置

API key 通过环境变量配置：

```bash
export MAO_SKILL_API_KEY="sk-xxxxxx"
```

查看和修改配置：

```bash
python scripts/config.py show
python scripts/config.py set rag.api.base_url "https://api.siliconflow.cn/v1"
python scripts/config.py set rag.enabled true
```

完整配置项参考 `config/search.json`。

如需向量化建库，可继续开启：

```bash
python scripts/config.py set rag.build_embeddings_on_index true
```

## 部署步骤

1. **安装依赖**

```bash
pip install -r requirements.txt  # 如有
```

2. **配置 API key**

```bash
export MAO_SKILL_API_KEY="sk-xxxxxx"
export MAO_SKILL_API_BASE_URL="https://api.siliconflow.cn/v1"
```

3. **建立索引**

```bash
python scripts/build_index.py
```

4. **验证检索**

```bash
python scripts/search.py catalog --volume 第一卷
python scripts/search.py search "实事求是"
```

---

## 常见操作

| 操作 | 命令 |
|------|------|
| 查看配置 | `python scripts/config.py show` |
| 开启 RAG | `python scripts/config.py set rag.enabled true` |
| 开启向量建库 | `python scripts/config.py set rag.build_embeddings_on_index true` |
| 测试 embedding | `python scripts/search.py test-model --target embedding` |
| 重建索引 | `rm -f index/search.sqlite && python scripts/build_index.py` |

---

## 检索模式

| 模式 | 说明 |
|------|------|
| `catalog` | 按卷列出文章 |
| `show` | 查看指定文章全文 |
| `search` | 关键词检索段落 |
| `hybrid` | 关键词 + 向量召回的混合检索（需开启 RAG） |

详见 `SKILL.md`。
