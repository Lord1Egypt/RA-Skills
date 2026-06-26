# Memory Tree 快速参考卡

## 核心公式

```
记忆 = 分块 + 打分 + 树状压缩 + 热度追踪
```

## 14 条快速打分规则

| 触发词 | 分值 |
|---|---|
| 记住/记忆/保存 | +0.25 |
| 偏好/喜欢/讨厌 | +0.25 |
| 金额（5 万、100 元） | +0.20 |
| 重要/必须/一定 | +0.20 |
| 需要/想要/希望 | +0.15 |
| bug/错误/异常 | +0.15 |
| 版本号 | +0.10 |
| 项目/仓库 | +0.10 |
| 配置 | +0.10 |
| 成功/完成 | +0.10 |
| API key/token | +0.05 |
| 日期时间 | +0.05 |
| <20 字 | ×0.5 |

## 数据库 4 张表

| 表 | 作用 |
|---|---|
| memory_chunks | 记忆块（content + score + is_admitted） |
| memory_topics | 主题/实体（name + hotness + summary） |
| memory_chunk_topics | Chunk-Topic 多对多关联 |
| memory_summaries | L1/L2 摘要压缩 |

## FTS5 搜索

```python
# 中文 → LIKE（准确）
WHERE content LIKE '%关键词%'

# 英文 → FTS5 MATCH（快）
WHERE content MATCH 'keyword'
```

## 热度公式

```
提及: hotness += 0.05
衰减: hotness *= 0.95 (每日)
活跃: >0.5
归档: <0.1
```

## 坑点速查

1. `is_admitted` 存 0/1，不是 score
2. INSERT 参数数 = 列数
3. NOT IN 要加 `IS NOT NULL`
4. FTS5 外部表删除先 `INSERT INTO fts(fts) VALUES('delete')`
5. 中文不能用 FTS5 MATCH
6. WAL 锁冲突用独立进程清理

## MVP 最小实现

见 `references/mvp-implementation.py` — 约 200 行，含：
- Schema 初始化
- 确定性 Chunk ID
- 14 条 Fast Score
- 中文/英文双模式搜索
- 统计接口

可直接复制到任何 Python 项目。
