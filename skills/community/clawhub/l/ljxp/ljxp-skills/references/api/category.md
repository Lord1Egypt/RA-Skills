# 类目接口

脚本：`scripts/category_tree.py`

积分：**首次 10**（按站点），命中缓存 **0**。过期判定：`cacheLastModified + 7天`。缓存路径：`cache/category_tree_<site>.json`。

---

## GET /category/tree

请求参数（仅这 1 个发后端）：`siteId ∈ {MLM, MLB, MLC, MLA, MCO}`

响应：

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "list": [
      {"id":"MLM458037","name":"Cell Phone Cases","zhName":"手机壳","children":[ {...} ]}
    ],
    "cacheLastModified": "2026-08-01 12:34:56"
  }
}
```

节点字段（list 内每个元素，驼峰）：

| 字段 | 说明 |
|---|---|
| `id` | 下游脚本的 `--category-id` |
| `name` | 英文 |
| `zhName` | 中文 |
| `children[]` | 子节点，递归同结构 |

---

## 脚本本地参数（不发后端，0 积分）

| 参数 | 作用 |
|---|---|
| `--search "关键词"` | 匹配 `zhName/name/id`，保留命中节点+祖先链 |
| `--depth N` | 打印截断，默认 3，`0` 不限 |
| `--output json` | 输出 `{code, msg, data}`，data=list |
| `--refresh` | 强制重拉覆盖缓存（本次 10 积分） |
| `--cache-ttl` | 本地 TTL 秒，默认 604800=7 天，`0` 永不过期 |
| `--token` | 仅首次/`--refresh` 必传 |

跳过场景：用户已给出明确类目 ID（如 `MLM458037`）→ 直接下游，不用调用。

跨站点注意：不同站点 ID **不通用**。
