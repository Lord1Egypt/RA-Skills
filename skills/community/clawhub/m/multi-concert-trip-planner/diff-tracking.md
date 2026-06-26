# 场次变更追踪（Diff Tracking）

每次搜索完成后，将本次搜索结果保存为快照文件。下次运行时自动加载上次快照并与本次结果做 diff，在输出末尾生成「场次变更总结」。

## 快照存储

### 文件位置

快照存储在 skill 目录下的 `snapshots/` 子目录中：

```
~/.qoderwork/skills/multi-concert-trip-planner/snapshots/
├── {快照ID}.json        ← 每次搜索的结果快照
└── latest.json          ← 符号链接，指向最新快照（便于快速读取上次结果）
```

### 快照 ID 命名规则

快照 ID = `{艺人列表排序后用下划线连接}_{搜索日期YYYYMMDD}`

示例：`ado_yoasobi_20260408.json`

如果同一天对相同艺人列表搜索多次，后次覆盖前次。

### 快照 JSON 结构

```json
{
  "snapshotId": "kenshi_yonezu_ryokushaka_backnumber_20260408",
  "createdAt": "2026-04-08T15:30:00+08:00",
  "artists": ["米津玄師", "緑黄色社会", "back number"],
  "timeWindow": "2026 下半年",
  "shows": [
    {
      "id": "kenshi_yonezu_20261203_sendai",
      "artist": "米津玄師",
      "date": "2026-12-03",
      "time": "18:00",
      "venue": "セキスイハイムスーパーアリーナ",
      "city": "仙台",
      "country": "日本",
      "price": "¥9,800",
      "ticketStatus": "在售",
      "ticketUrl": "https://...",
      "source": "WebSearch snippet"
    }
  ],
  "totalShows": 15,
  "searchDuration": "约 3 分钟"
}
```

**场次 ID 生成规则：** `{艺人名拼音/英文小写}_{日期YYYYMMDD}_{城市拼音小写}`，用于跨快照匹配同一场演出。

## 工作流程

### 搜索前：加载上次快照

1. 根据当前搜索的艺人列表，在 `snapshots/` 中查找最近一次匹配的快照
2. 匹配逻辑：艺人列表排序后完全相同（忽略大小写和空格）
3. 如果找到匹配快照，加载为 `previousSnapshot`
4. 如果没有找到（首次搜索该艺人组合），跳过 diff，搜索结束后直接保存快照

**查找命令：**
```bash
ls -t ~/.qoderwork/skills/multi-concert-trip-planner/snapshots/{艺人列表快照ID前缀}*.json | head -1
```

### 搜索后：保存快照 + 执行 diff

1. 将本次搜索的所有场次整理为快照 JSON 格式
2. 写入 `snapshots/{快照ID}.json`
3. 更新 `latest.json` 指向新快照
4. 如果存在 `previousSnapshot`，执行 diff 算法

**保存命令示例：**
```bash
# 确保 snapshots 目录存在
mkdir -p ~/.qoderwork/skills/multi-concert-trip-planner/snapshots

# 写入快照文件（通过 Write 工具）
# 更新 latest.json 符号链接
ln -sf {快照ID}.json ~/.qoderwork/skills/multi-concert-trip-planner/snapshots/latest.json
```

## Diff 算法

### 匹配规则

两条场次记录被视为"同一场演出"需满足：
- **艺人相同**（忽略大小写）
- **日期相同**（精确到天）
- **城市相同**（忽略"市"/"City"后缀，如"仙台" = "仙台市"）

不依赖场次 ID 做精确匹配，因为场馆名可能在不同数据源中表述不同。

### 变更分类

对比 `previousSnapshot.shows` 和当前 `currentShows`，产出 5 类变更：

| 变更类型 | 判定逻辑 | 图标 |
|----------|----------|------|
| **新增场次** | 当前有、上次无（按艺人+日期+城市匹配不到） | 🆕 |
| **取消/下架场次** | 上次有、当前无 | ❌ |
| **场馆变更** | 同一场演出但场馆名称不同 | 🏟️ |
| **售票状态变更** | 同一场演出但售票状态变化（如"预售"→"在售"、"在售"→"售罄"） | 🎫 |
| **票价变更** | 同一场演出但票价区间发生变化 | 💰 |

**优先级排序：** 取消 > 新增 > 售票状态变更 > 场馆变更 > 票价变更

### 不变场次

如果某场演出在两次快照中完全一致（日期、城市、场馆、售票状态、票价均未变），归入"不变"，不在 diff 中展示。

## 输出格式

→ 详见 `output-template.md`「场次变更总结」部分

Diff 总结在主方案输出之后、末尾展示。包含：
- 上次搜索时间
- 各类变更的汇总数字
- 按变更类型分组的详细变更列表
- 需要用户关注的重点变更（如"在售→售罄"需要紧急关注）

## 注意事项

- 快照仅记录场次信息，不记录机票/酒店数据（这些实时数据每次搜索都不同，不适合做 diff）
- 如果两次搜索的时间窗口不同（如上次搜"下半年"，这次搜"10-12月"），diff 时只比较两次时间窗口的交集部分，避免因搜索范围缩小而产生大量虚假"取消"
- 如果用户增减了艺人列表（如上次搜 A+B，这次搜 A+B+C），新增艺人的场次全部标为"新增"，其余艺人正常做 diff
- 快照文件较小（通常 <10KB），无需定期清理。如需手动清理：`ls ~/.qoderwork/skills/multi-concert-trip-planner/snapshots/`
- 首次搜索某组艺人时，无 diff 输出，仅保存快照并提示"已保存本次搜索快照，下次搜索相同艺人时将自动显示场次变更"
