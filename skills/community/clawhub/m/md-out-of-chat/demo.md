# md2view demo - 看看效果

这是一个 **demo**，用来看 *手机端可读性*。

## 一段 python 代码

```python
def find_anomaly(data, threshold=0.95):
    """从数据中找异常模式"""
    anomalies = []
    for item in data:
        if item.score > threshold:
            anomalies.append(item)
    return anomalies

# 调用
results = find_anomaly(items)
print(f"找到 {len(results)} 个异常")  # 输出
```

## 一段 SQL

```sql
SELECT user_id, COUNT(*) as cnt
FROM posts
WHERE created_at > '2026-01-01'
GROUP BY user_id
HAVING cnt > 100
ORDER BY cnt DESC;
```

## 一个表格（手机能不能对齐？）

| 维度 | Kimi | 元宝 | 谁赢 |
|------|------|------|------|
| 趋势数 | 10 | 5 | Kimi |
| 单个深度 | 浅 | 深 | 元宝 |
| 政策覆盖 | 广 | 窄 | Kimi |
| 技术深度 | 浅 | 深 | 元宝 |

## 列表

- 风格：蓝白灰简约
- 表格：列对齐，斑马纹
- 代码：按语言高亮
- 部署：web 链接手机可看
