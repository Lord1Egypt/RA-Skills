# /novel track-init - 初始化追踪系统

## 触发方式

```
/novel track-init
```

或对话式：
```
初始化追踪系统
创建追踪文件
```

---

## 功能

创建追踪系统所需的基础文件。

---

## 创建的文件

### spec/tracking/character-state.json

```json
{
  "version": "1.0",
  "characters": {
    "protagonist": {
      "name": "",
      "identity": "",
      "personality": "",
      "state": {},
      "arc": {}
    }
  },
  "last_updated": "ISO日期"
}
```

### spec/tracking/relationships.json

```json
{
  "version": "1.0",
  "relationships": [],
  "last_updated": "ISO日期"
}
```

### spec/tracking/plot-tracker.json

```json
{
  "version": "1.0",
  "plotlines": [],
  "foreshadowing": [],
  "milestones": [],
  "last_updated": "ISO日期"
}
```

---

## 输出

```
✅ 追踪系统初始化完成

📁 已创建：
- spec/tracking/character-state.json
- spec/tracking/relationships.json
- spec/tracking/plot-tracker.json
```
