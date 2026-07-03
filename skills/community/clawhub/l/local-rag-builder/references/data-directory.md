# 数据目录结构 — local-rag-builder

运行时数据存储在 `skills/.standardization/local-rag-builder/data/` 下：

```text
data/
├── kb/               # 向量数据库目录（每个知识库一个子目录）
│   ├── default/      # 默认知识库
│   ├── art/          # 艺术类资料
│   └── politics/     # 政治类资料
├── models/           # 下载的嵌入模型
├── prompts/          # Prompt 模板文件
├── config/           # 运行时配置
├── output/           # 导出产物
├── logs/             # 执行日志
├── cache/            # 缓存
└── config_templates/ # 用户保存的配置模板
```

重置方法：删除对应子目录即可重置相关数据。
