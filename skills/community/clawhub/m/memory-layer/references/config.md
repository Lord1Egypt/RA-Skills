# 配置参考

## 配置文件位置

**默认配置**：`config/default.json`（Skill 自带）

**自定义配置**：`~/.openclaw/memory-config.json`（可选，覆盖默认）

---

## 凭据说明

**本 Skill 无需额外环境变量或凭据**。

| 功能 | 凭据来源 | 说明 |
|------|----------|------|
| autoDream 触发 | OpenClaw Cron | 使用现有 OpenClaw 凭据 |
| 飞书通知 | OpenClaw Feishu | 使用现有飞书配置 |
| 文件读写 | OpenClaw CLI | 使用现有文件系统权限 |

**无需以下配置**：
- ❌ API Key
- ❌ 数据库密码
- ❌ 第三方服务凭据
- ❌ 额外的环境变量

如需修改通知行为，编辑 `~/.openclaw/memory-config.json` 中的 `autoDream.notifyOnComplete`。

---

## 完整配置示例

```json
{
  "version": "2.0",
  "index": {
    "maxSizeKB": 25,
    "maxLineLength": 150,
    "archiveThreshold": 0.9,
    "archivePath": "memory/index-archive.md",
    "lruSize": 5
  },
  "topic": {
    "directory": "memory/topics/",
    "maxSizeKB": 50,
    "enableVersioning": false,
    "requireReferences": true,
    "requireContradictionMarking": true
  },
  "transcript": {
    "directory": "memory/transcripts/",
    "splitBy": "day",
    "archiveDays": 90,
    "compressFormat": "gzip"
  },
  "autoDream": {
    "enabled": true,
    "schedule": "23:00",
    "timezone": "Asia/Shanghai",
    "notifyOnComplete": false,
    "notifyChannel": "feishu",
    "similarityThreshold": 0.8,
    "minImportance": 0.2
  },
  "domains": {
    "default": {
      "name": "通用",
      "importanceBase": 0.5,
      "keywordsWeight": 0.3
    },
    "投资": {
      "name": "投资理财",
      "importanceBase": 0.8,
      "keywordsWeight": 0.5
    },
    "项目": {
      "name": "项目开发",
      "importanceBase": 0.7,
      "keywordsWeight": 0.4
    },
    "资产": {
      "name": "资产档案",
      "importanceBase": 0.7,
      "keywordsWeight": 0.3
    },
    "知识": {
      "name": "知识沉淀",
      "importanceBase": 0.5,
      "keywordsWeight": 0.4
    }
  },
  "search": {
    "defaultSearchTranscripts": false,
    "maxResults": 50,
    "minImportanceThreshold": 0.3,
    "rankingWeights": {
      "importance": 0.4,
      "relevance": 0.4,
      "recency": 0.2
    }
  }
}
```

---

## 配置参数

### index 配置

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| maxSizeKB | number | 25 | Index 文件最大大小 (KB) |
| maxLineLength | number | 150 | 每行最大字符数 |
| archiveThreshold | number | 0.9 | 归档触发阈值 |
| archivePath | string | memory/index-archive.md | 归档文件路径 |
| lruSize | number | 5 | LRU 缓存容量 |

### topic 配置

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| directory | string | memory/topics/ | Topic 目录 |
| maxSizeKB | number | 50 | 最大文件大小 (KB) |
| enableVersioning | boolean | false | 启用版本控制 |
| requireReferences | boolean | true | 要求引用 |
| requireContradictionMarking | boolean | true | 要求矛盾标记 |

### transcript 配置

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| directory | string | memory/transcripts/ | Transcript 目录 |
| splitBy | string | day | 分割方式 (day/month) |
| archiveDays | number | 90 | 归档天数阈值 |
| compressFormat | string | gzip | 压缩格式 |

### autoDream 配置

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| enabled | boolean | true | 启用自动整理 |
| schedule | string | 23:00 | 执行时间 (HH:MM) |
| timezone | string | Asia/Shanghai | 时区 |
| notifyOnComplete | boolean | false | 完成时通知 |
| notifyChannel | string | feishu | 通知渠道 |
| similarityThreshold | number | 0.8 | 相似度合并阈值 |
| minImportance | number | 0.2 | 最小重要性阈值 |

### domains 配置

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| {domain}.importanceBase | number | 0.5 | 领域基础重要性 |
| {domain}.keywordsWeight | number | 0.3 | 关键词权重 |

### search 配置

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| defaultSearchTranscripts | boolean | false | 默认搜索 Transcripts |
| maxResults | number | 50 | 最大结果数 |
| minImportanceThreshold | number | 0.3 | 最小重要性阈值 |
| rankingWeights.importance | number | 0.4 | 重要性权重 |
| rankingWeights.relevance | number | 0.4 | 相关性权重 |
| rankingWeights.recency | number | 0.2 | 时效性权重 |

---

## 用户自定义配置

如需覆盖默认配置，复制并修改：

```bash
cp config/default.json ~/.openclaw/memory-config.json
```

然后编辑 `~/.openclaw/memory-config.json`，例如：

```json
{
  "autoDream": { "schedule": "02:00" }
}
```

---

*最后更新：2026-04-03*
