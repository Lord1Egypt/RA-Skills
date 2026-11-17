# 版本控制（主题导览笔记）

> 适用于：阶段 2 旧版本检查 + 阶段 4 增量更新时的版本管理。

## 1. 版本信息格式

放在大标题后：

```markdown
# 主题导览：[主题名称]

**版本**：v1.0 | 创建于 YYYY-MM-DD | 更新于 YYYY-MM-DD
**更新日志**：v1.0 - 初始版本，基于知识库资料编译
```

## 2. 版本号规则

| 变更类型 | 版本号变化 | 示例 |
|---------|-----------|------|
| 仅增删文章 | patch +0.0.1 | v1.0 → v1.1 |
| 修改关键要素/设计原则 | minor +0.1 | v1.0 → v1.10 |
| 重新编译整个主题 / 核心概念结构变化 | major +1.0 | v1.0 → v2.0 |

## 3. 版本记录位置

在笔记大标题下方用加粗行标注版本号、创建日期、更新日期和更新日志。

## 4. 检查旧版本

每次编译前必须检查是否已有该主题的知识导览，避免重复创建或丢失历史版本信息。

### 检查方式

1. 在目标文件夹中搜索标题包含"主题导览"的笔记：

```bash
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/get_knowledge_list" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"knowledge_base_id": "<kb_id>", "folder_id": "<folder_id>", "count": 50}' | \
python3 -c "import sys,json; data=json.load(sys.stdin); print([f['title'] for f in data.get('data',{}).get('list',[])])"
```

2. 如果找到"主题导览：xxx"笔记，记录其 `note_id` 和版本信息
3. 如果没找到，则进入新建流程

### 判断逻辑

| 情况 | 处理方式 |
|------|---------|
| 已有该主题的旧版本导览 | **增量更新**：读取旧版本内容 → 对比知识库增量 → 更新导览 |
| 已有其他主题的导览（非本主题） | **新建**：按正常流程创建新导览 |
| 没有任何知识导览 | **新建**：按正常流程创建新导览 |

## 5. 增量更新流程

详见 [incremental-update.md](incremental-update.md)

增量更新时会修改版本号，并在更新日志中记录本次变更摘要。
