# 信息源添加规范与 Parser 编写指南

## 如何添加新信息源

用户提供新链接时，按以下步骤操作：

### Step 1：判断信息源类型

| 类型 | 特征 | 抓取难度 |
|------|------|---------|
| `forum_post` | 社区帖子，持续更新，内容在单页上 | ⭐ 简单 |
| `official_page` | 官网活动列表页，结构固定 | ⭐⭐ 中等 |
| `rss` | 有 RSS/Atom feed | ⭐ 简单 |
| `api` | 有公开 API | ⭐⭐⭐ 复杂 |
| `search_query` | 没有固定页面，靠搜索 | ⭐⭐ 中等 |

### Step 2：追加到 sources.json

在 `sources` 数组末尾追加：

```json
{
  "id": "snake_case_唯一id",
  "name": "赛事/平台显示名称",
  "url": "抓取地址",
  "type": "forum_post",
  "category": "OPC赛事 | AI赛事 | 创业大赛 | 独立开发者",
  "organizer": "主办方名称",
  "enabled": true,
  "notes": "补充说明"
}
```

**id 命名规则**：平台名_类型，全小写+下划线，如：
- `trae_forum`、`devpost_hackathons`、`kaggle_competitions`、`opencsg_opc`

### Step 3：注册 Parser（如类型已有则复用）

在 `track_events.py` 的 `PARSERS` 字典里加入：

```python
PARSERS = {
    "trae_forum": parse_trae_forum,
    "你的新id": parse_你的新函数,  # 新增这行
}
```

---

## Parser 编写规范

```python
def parse_xxx(html_text, source):
    """
    解析 XXX 平台的赛事页面
    
    Args:
        html_text: 已抓取的原始 HTML 字符串
        source: sources.json 中的 source 字典
    
    Returns:
        list[dict]: 事件列表，每个事件必须包含以下字段
    """
    text = extract_text(html_text)  # 转纯文本
    events = []
    
    # 解析逻辑...
    
    # 每个事件必填字段：
    event = {
        "id": make_id(source["id"], event_name),  # 必填，唯一标识
        "source_id": source["id"],                 # 必填
        "name": "赛事名称",                         # 必填
        "type": source.get("category", "未知"),     # 必填
        "organizer": source.get("organizer", ""),  # 建议
        "status": "报名中 | 进行中 | 已结束",       # 建议
        "url": source["url"],                       # 必填
        "discovered_at": datetime.now().strftime("%Y-%m-%d"),  # 必填
        
        # 可选字段（填尽量填）
        "prize": "奖金描述",
        "deadline": "2026-07-01",   # 报名截止
        "start_date": "",           # 开始时间
        "end_date": "",             # 结束时间
        "result_date": "",          # 结果公布时间
        "official_site": "",        # 官方网站
        "raw_snippet": text[:300],  # 原文片段（调试用）
    }
    events.append(event)
    
    return events
```

---

## 通用 Parser（无特定解析器时的回退）

当 PARSERS 中没有对应 id 时，自动使用通用解析器，提取：
- 页面标题
- 页面前 500 字文本
- 存为一条原始事件记录

适合：新信息源上线初期，先记录，再优化 parser。

---

## 已有 Parser 列表

| Parser 函数 | 对应 source id | 平台 |
|------------|--------------|------|
| `parse_trae_forum` | `trae_forum` | TRAE 官方论坛 |

---

## 注意事项

- **去重靠 event id**：同一赛事的 id 必须一致（基于 source_id + event_name 的 md5）
- **变更检测字段**：`status`、`approved_count`、`batch`、`prize`，这些字段变了会触发变更提醒
- **新增信息源后，建议立即手跑一次脚本验证**：执行命令见 SKILL.md
