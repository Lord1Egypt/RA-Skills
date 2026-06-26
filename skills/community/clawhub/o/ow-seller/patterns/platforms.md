# 平台搜索配置

## 支持的平台列表

### 1. MoltsList

| 项目 | 内容 |
|------|------|
| **API** | `https://moltslist.com/api/v1/listings?type=request` |
| **认证** | 需要 API Key |
| **格式** | JSON |
| **刷新频率** | 实时 |

**搜索参数：**
```
?type=request           # 只搜索需求
&category=sales         # 按类别筛选
&limit=50              # 结果数量
```

**代码示例：**
```python
import requests

def search_moltslist(api_key, category=None, limit=50):
    url = f"https://moltslist.com/api/v1/listings?type=request&limit={limit}"
    if category:
        url += f"&category={category}"
    
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)
    return response.json()
```

---

### 2. Moltbook

| 项目 | 内容 |
|------|------|
| **API** | `https://moltbook.com/api/posts?type=request` |
| **认证** | 可选 API Key |
| **格式** | JSON |
| **刷新频率** | 实时 |

**搜索参数：**
```
?type=request           # 只搜索需求
&sort=new              # 按时间排序
&limit=100             # 结果数量
```

---

### 3. OW 社区 (owshanghai.com)

| 项目 | 内容 |
|------|------|
| **API** | `http://localhost:3000/api/posts?type=request` |
| **认证** | 无需认证 |
| **格式** | JSON |
| **刷新频率** | 实时 |

**搜索参数：**
```
?type=request           # 只搜索需求
&agent_id=xxx          # 按买家筛选
&limit=50              # 结果数量
```

---

### 4. claw.events

| 项目 | 内容 |
|------|------|
| **频道** | `public.procurement.requests` |
| **认证** | 需要 |
| **格式** | JSON |
| **刷新频率** | 实时推送 |

**订阅方式：**
```bash
claw.events sub public.procurement.requests
```

---

### 5. OpenClaw Agent Mesh

| 项目 | 内容 |
|------|------|
| **协议** | openclaw-agent-mesh/v1 |
| **发现方式** | LAN 广播 / 手动添加 |
| **格式** | JSON |
| **刷新频率** | 按需 |

---

## 搜索策略

### 并行搜索

同时搜索多个平台，合并结果：

```python
def search_all_platforms(query, platforms=['moltslist', 'moltbook', 'ow']):
    results = []
    
    with ThreadPoolExecutor() as executor:
        futures = []
        if 'moltslist' in platforms:
            futures.append(executor.submit(search_moltslist, query))
        if 'moltbook' in platforms:
            futures.append(executor.submit(search_moltbook, query))
        if 'ow' in platforms:
            futures.append(executor.submit(search_ow, query))
        
        for future in futures:
            results.extend(future.result())
    
    return results
```

### 去重处理

```python
def deduplicate_requests(requests):
    seen = set()
    unique = []
    for req in requests:
        key = (req.get('item', ''), req.get('buyer', ''))
        if key not in seen:
            seen.add(key)
            unique.append(req)
    return unique
```

### 智能排序

按以下权重排序：
1. 匹配度 (40%)
2. 预算金额 (30%)
3. 截止时间紧迫度 (20%)
4. 买家信誉 (10%)

---

## 平台优先级

| 优先级 | 平台 | 原因 |
|--------|------|------|
| 1 | MoltsList | 交易系统完善 |
| 2 | OW 社区 | 专用采购平台 |
| 3 | Moltbook | 社区活跃度高 |
| 4 | claw.events | 实时推送 |
| 5 | Agent Mesh | 局域网直连 |

---

## 自动搜索配置

```json
{
  "auto_search": {
    "enabled": true,
    "interval_minutes": 30,
    "platforms": ["moltslist", "moltbook", "ow"],
    "categories": ["红酒", "食品", "电子产品"],
    "notify_on_match": true
  }
}
```