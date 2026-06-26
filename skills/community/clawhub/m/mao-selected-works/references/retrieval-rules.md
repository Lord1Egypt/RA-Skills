# Retrieval Rules

默认检索顺序：

1. 结构过滤
2. 标题和别名匹配
3. 全文 FTS 检索
4. 如果用户显式要求且 `rag.enabled=true`，执行向量召回
5. 如果 `rerank.enabled=true`，对候选结果重排

配置约定：

- `rag.api.base_url` 与 `rag.api.api_key_env` 作为统一平台配置
- `rag.embedding.model`、`rag.rerank.model` 可分别覆盖模型名
- `chunk_size` 和 `chunk_overlap` 决定切分粒度
- `embedding.batch_size` 用于限制单次 embedding 请求大小，默认建议 `64`

规则：

- 用户说“第几卷”时，优先使用 `catalog` 或 `show --volume`
- 用户说“第几卷第几篇”时，优先使用 `show --volume ... --chapter ...`
- 用户说文章标题时，优先做标题精确或近似匹配
- 用户给主题词时，优先返回命中的文章和相关段落
- 用户同时给出卷次、篇次、标题、关键词时，按结构过滤后再做标题/全文/混合检索
- 混合检索只在显式开启或用户明确要求时使用
- 没命中时不编造“毛选里有这段话”

建议输出中始终带上：

- `volume`
- `article_title`
- `source_path`
- `retrieval`
- `snippet`
