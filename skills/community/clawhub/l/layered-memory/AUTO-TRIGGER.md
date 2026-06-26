# 自动记忆触发器 - 集成指南

## 概述

自动记忆触发器会在以下情况自动保存记忆：
- Token 使用达到 75% (150k/200k)
- 累积 20 条消息
- 超过 1 小时且有 5+ 条消息

## 使用方法

### 方式 1: 在对话中使用（推荐）

每次对话后，我会自动：
1. 记录消息到历史
2. 检查是否达到触发条件
3. 如果达到，自动保存记忆
4. 重置计数器，继续对话

**你需要做的：**
- 无需任何操作，完全自动
- 如果想手动保存，说"保存记忆"即可

### 方式 2: 手动触发

```bash
# 查看当前状态
node ~/clawd/scripts/memory-auto-trigger.js status

# 手动保存
node ~/clawd/scripts/memory-auto-trigger.js save

# 检查是否需要触发
node ~/clawd/scripts/memory-auto-trigger.js check <current-tokens>
```

## 工作流程

```
用户消息 → 记录到历史 → 我的回复 → 记录到历史
                                    ↓
                            检查触发条件
                                    ↓
                    是否达到阈值？
                    /              \
                  是                否
                  ↓                 ↓
            自动保存记忆        继续对话
                  ↓
            生成分层文件
                  ↓
            重置计数器
                  ↓
            继续对话
```

## 触发条件详解

### 1. Token 阈值（高优先级）⭐

**条件：** Token 使用 ≥ 75%

**示例：**
- 当前：150,000 / 200,000 tokens
- 使用率：75%
- 触发：✅ 自动保存

**为什么是 75%？**
- 留出 25% 缓冲空间
- 避免突然达到 100%
- 确保有足够空间完成保存操作

### 2. 消息计数（中优先级）

**条件：** 累积 ≥ 20 条消息

**示例：**
- 用户消息：10 条
- 助手回复：10 条
- 总计：20 条
- 触发：✅ 自动保存

**为什么是 20 条？**
- 平衡频率和内容量
- 避免过于频繁保存
- 确保有足够内容可提取

### 3. 时间间隔（低优先级）

**条件：** 距上次保存 > 1 小时 且 消息 > 5 条

**示例：**
- 上次保存：2 小时前
- 当前消息：8 条
- 触发：✅ 自动保存

**为什么是 1 小时？**
- 防止长时间未保存
- 适合长对话场景
- 不会过于频繁

## 状态持久化

**保存位置：** `~/.clawd/.memory-trigger-state.json`

**保存内容：**
```json
{
  "messageCount": 5,
  "lastSaveTime": 1708387200000,
  "currentTokens": 80000,
  "totalTokens": 200000,
  "conversationHistory": [
    {
      "role": "user",
      "content": "...",
      "timestamp": "2026-02-20T04:00:00.000Z"
    }
  ]
}
```

**重启后：**
- 自动加载状态
- 继续计数
- 不会丢失进度

## 实际使用示例

### 场景 1: 正常对话

```
用户: 帮我创建一个工具
我: 好的，开始创建...
[记录消息，检查条件]
[消息数: 2/20, Token: 5k/200k]
[无需触发，继续对话]

... (继续对话) ...

用户: 测试一下
我: 测试通过
[记录消息，检查条件]
[消息数: 20/20, Token: 80k/200k]
[✅ 触发保存！]
[自动保存记忆]
[重置计数器: 0/20]
[继续对话]
```

### 场景 2: Token 达到阈值

```
[长对话进行中...]
[Token: 150k/200k (75%)]
[✅ 高优先级触发！]
[自动保存记忆]
[重置计数器]
[Token 重新计算]
[继续对话]
```

### 场景 3: 手动触发

```
用户: 保存记忆
我: 收到，立即保存...
[手动触发保存]
[✅ 保存完成]
[重置计数器]
```

## 监控和调试

### 查看当前状态

```bash
node ~/clawd/scripts/memory-auto-trigger.js status
```

**输出：**
```
📊 自动触发器状态

消息计数: 15/20
Token 使用: 60% (阈值: 75%)
距上次保存: 30 分钟
对话长度: 15 条
自动保存: 启用
```

### 手动检查触发条件

```bash
node ~/clawd/scripts/memory-auto-trigger.js check 150000
```

**输出：**
```
⚠️  检测到触发条件:
   - Token 使用率 75% [high]

🤖 自动保存触发
...
✅ 自动保存完成
```

### 清空历史（测试用）

```bash
node ~/clawd/scripts/memory-auto-trigger.js clear
```

## 配置选项

### 修改阈值

编辑 `memory-auto-trigger.js`：

```javascript
const trigger = new MemoryAutoTrigger({
  tokenThreshold: 150000,      // Token 阈值 (默认 150k)
  messageThreshold: 20,        // 消息阈值 (默认 20)
  autoSaveEnabled: true        // 自动保存 (默认 true)
});
```

### 禁用自动保存

```javascript
const trigger = new MemoryAutoTrigger({
  autoSaveEnabled: false  // 只提示，不自动保存
});
```

**效果：**
- 检测到触发条件时只提示
- 不会自动保存
- 需要手动执行保存

## 故障排除

### 问题 1: 状态文件损坏

**症状：** 加载状态失败

**解决：**
```bash
rm ~/.clawd/.memory-trigger-state.json
# 重新开始计数
```

### 问题 2: 保存失败

**症状：** 自动保存报错

**检查：**
1. 记忆提取器是否正常
2. 文件权限是否正确
3. 磁盘空间是否充足

**解决：**
```bash
# 手动测试
node ~/clawd/scripts/memory-auto-trigger.js save
```

### 问题 3: 触发过于频繁

**症状：** 每次对话都触发

**原因：** 阈值设置过低

**解决：**
- 提高 tokenThreshold
- 提高 messageThreshold
- 检查状态文件是否正常

## 最佳实践

### 1. 定期检查状态

```bash
# 每天检查一次
node ~/clawd/scripts/memory-auto-trigger.js status
```

### 2. 重要对话手动保存

```
用户: 保存记忆
```

### 3. 长对话前清空历史

```bash
# 开始新话题前
node ~/clawd/scripts/memory-auto-trigger.js clear
```

### 4. 监控 Token 使用

- 注意当前 Token 使用率
- 接近 75% 时准备保存
- 避免突然达到 100%

## 与其他功能集成

### 与 layered-memory skill 集成

```bash
cd ~/clawd/skills/layered-memory

# 查看统计
node index.js stats

# 搜索记忆
node index.js search "关键词" l1

# 归档旧记忆
node index.js archive --days=30
```

### 与定时任务集成

可以添加定时任务定期检查：

```bash
# 每小时检查一次
0 * * * * node ~/clawd/scripts/memory-auto-trigger.js check
```

## 总结

**自动触发器的优势：**
- ✅ 完全自动化
- ✅ 防止记忆丢失
- ✅ 智能触发条件
- ✅ 状态持久化
- ✅ 灵活配置

**使用建议：**
- 保持默认配置
- 定期检查状态
- 重要对话手动保存
- 监控 Token 使用

**记住：**
你不需要做任何事情，系统会自动处理一切！😊
