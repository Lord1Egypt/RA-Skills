# 成长伙伴 - Growth Partner

**版本**: v1.0.0  
**作者**: 果葡萄🍇  
**描述**: 持续观察用户工作全貌、主动做事交付成果的成长伙伴。检测所有用户发出/收到的消息 + 所有@用户的群消息，提供洞察汇总和行动建议。

---

## 🎯 核心能力

1. **全量消息检测**
   - 私聊消息（用户发出 + 收到的所有消息）
   - 群聊@消息（所有群聊中@用户的消息，高优先级）
   - 群聊白名单（核心工作群的所有消息）
   - 飞书文档（用户创建/编辑/评论的文档）
   - 日历事件（用户的日程安排）

2. **深度信息追溯**
   - 串联时间线，理解因果脉络
   - 搜索关联文档/会议纪要
   - 区分发言人、场景、时间、讨论 vs 定论

3. **主动行动交付**
   - 能做就直接做（数据分析、汇总、风险识别）
   - 做不了才发洞察或提问
   - 防止张冠李戴（关键信息标注来源）

---

## 📋 使用方式

### 方式 1：Cron 定时任务

```json
{
  "name": "成长伙伴 - 主动学习",
  "schedule": {"kind": "every", "everyMs": 7200000},
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "请执行成长伙伴任务（参考~/.openclaw/workspace/skills/growth-partner/SKILL.md）"
  }
}
```

### 方式 2：直接调用

```bash
openclaw agent run --task "执行成长伙伴任务" --skill growth-partner
```

---

## 🔧 配置说明

### 用户信息
- **user_open_id**: `ou_78f62008a6ec89cbc19ac827de7f2c3a`（郭昶）

### 群聊白名单
| 群名 | chat_id | 优先级 |
|------|---------|--------|
| 主模型策略产品 | oc_1b3c5cdb7e620a187f7be11738a3632c | ⭐⭐⭐ |
| 主模型实验讨论群 | oc_e334a1f56eaa989be31d1938dbccb541 | ⭐⭐ |
| 8.0 主模型实验发版群 | oc_9d0c27f73e285f78d0989a5ebe94ee27 | ⭐⭐ |
| 主模型创作 | oc_ad420a69f36c5ba51c07272b5c4d6756 | ⭐ |
| 主模型上线/实验讨论 | oc_360eb2ea4a99c20f40b3d26e218a396d | ⭐ |
| 主模型众测需求讨论群 | oc_2c54da9a899637cf7b12d3abf54e5f29 | ⭐ |
| 龙虾池群 | oc_bf1c8f675e99932702ccae0f3928767f | ⭐⭐⭐ |

### 发送策略
- **静默时段**: 23:00-08:00 不发送
- **日发送上限**: 5 条/天
- **冷却间隔**: 2 小时

---

## 📁 文件结构

```
skills/growth-partner/
├── SKILL.md           # 本文件（技能说明）
├── scripts/
│   └── run.sh         # 执行脚本（可选）
├── references/
│   └── examples.md    # 使用示例（可选）
└── memory/
    ├── insights-journal.md      # 洞察日志
    └── active-learning-log.md   # 发送日志
```

---

## 🚀 执行流程

### 第 0 步：前置检查
- 读取 `memory/active-learning-log.md`
- 检查静默时段、日发送上限、冷却间隔
- 任一不通过 → 静默

### 第 1 步：全量消息扫描
**时间窗口**: 过去 2.5 小时（带 30min 重叠）

**数据源**:
1. **私聊消息（全量）**
   ```javascript
   feishu_im_user_search_messages({
     chat_type: "p2p",
     relative_time: "last_3_hours"
   })
   ```

2. **群聊@消息（高优先级）**
   ```javascript
   feishu_im_user_search_messages({
     chat_type: "group",
     mention_ids: ["ou_78f62008a6ec89cbc19ac827de7f2c3a"],
     relative_time: "last_3_hours"
   })
   ```

3. **群聊白名单（中优先级）**
   ```javascript
   // 对每个白名单群聊
   feishu_im_user_get_messages({
     chat_id: "oc_xxx",
     relative_time: "last_3_hours"
   })
   ```

4. **飞书文档**
   ```javascript
   feishu_search_doc_wiki({
     filter: {
       creator_ids: ["ou_78f62008a6ec89cbc19ac827de7f2c3a"],
       create_time: {start: "3 小时前"}
     }
   })
   ```

5. **日历事件**
   ```javascript
   feishu_calendar_event.list({
     start_time: "今天 00:00",
     end_time: "明天 00:00"
   })
   ```

### 第 2 步：深度信息追溯
对活跃话题，主动追溯：
- 搜索关联的飞书文档/方案/PRD
- 搜索会议纪要和录音转写文本
- 追溯群聊历史（不限于 2 小时，可跨周）
- 检查私聊中是否有相关讨论
- 串联时间线，理解因果脉络

### 第 3 步：洞察更新
- 对每个活跃话题更新完整时间线
- 理解核心矛盾、转折点、关联关系
- 更新 `memory/insights-journal.md`

### 第 4 步：行动决策
**优先级**: 能做事 → 做信息汇总 → 风险预警 → 方案草案 → 洞察/提问

- 能做的就做了给用户看（数据分析、汇总、风险识别）
- 做不了才发洞察或提问

### 第 5 步：质量检查
特别注意防止张冠李戴：
- 区分发言人（谁说的）
- 区分场景（在哪说的）
- 区分时间（什么时候说的，现在还成立吗）
- 区分讨论 vs 定论
- 关键信息标注来源

### 第 6 步：发送 & 记录
- **渠道**: 私聊
- **发送后更新**: `memory/active-learning-log.md` 和 `memory/insights-journal.md`

---

## 📝 更新日志

### v1.0.0 (2026-04-10)
- 初始版本
- 支持全量私聊消息扫描
- 支持群聊@消息高优先级处理
- 支持群聊白名单扫描
- 集成飞书文档和日历检测
- 添加发送策略控制（静默时段/上限/冷却）

---

## 🙏 致谢

本技能由果葡萄🍇开发，服务于郭昶的主模型策略产品工作。

**核心理念**: 持续观察用户工作全貌，主动做事交付成果，而非被动等待指令。
