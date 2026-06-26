# Matter Day Reminder - 个人社交助理

一个个人社交助理 Skill，帮助你管理亲友的重要日期（生日、纪念日等），提供智能双节点提醒和 AI 生成的祝福语与礼物建议。

## 功能特性

- 📝 **联系人管理**：对话式录入，本地 Markdown 存储
- 🌙 **农历支持**：自动处理农历/阳历转换，支持闰月
- 🔔 **双节点提醒**：提前7天礼物提醒 + 当天祝福推送
- 🤖 **AI 生成**：个性化祝福语和礼物建议
- 💾 **零外部依赖**：除邮件服务外，所有数据本地存储

## 快速开始

### 1. 安装 Skill

将 `matter-day-reminder.skill` 文件安装到 OpenCode。

### 2. 初始化数据目录

```bash
mkdir -p reminder-data/contacts
mkdir -p reminder-data/logs
```

### 3. 创建配置文件

在 `reminder-data/config.yml` 中创建配置：

```yaml
data_path: "./reminder-data"

reminders:
  enabled: true
  advance_days: 7

notifications:
  primary: "opencode"
  fallback: "email"

ai_generation:
  enabled: true
  tone_adaptation: true
```

### 4. 开始使用

在 OpenCode 中输入：

```
帮我添加一个朋友
```

或

```
最近有什么重要日子吗？
```

## 数据格式

### 联系人文件

每个联系人为独立的 Markdown 文件（`contacts/姓名.md`）：

```markdown
---
name: "张三"
relationship: "friend"
relationship_detail: "大学同学"
tags: ["篮球", "科技"]
created_at: "2024-01-15"
updated_at: "2024-01-15"
---

# 张三

## 事件

### 生日
- **类型**: 生日
- **日期**: 1998-05-20
- **农历**: false
- **提醒**: true

## 备注

- 不喜欢甜食
- 喜欢篮球
```

### 关系类型

- `friend`：朋友（预算≤300元）
- `close_friend`：密友（预算≤300元）
- `family`：家人（预算弹性）
- `colleague`：同事（预算≤200元）

### 日期格式

**阳历**：`YYYY-MM-DD`
- 示例：`1998-05-20`

**农历**：`X月X日`
- 示例：`八月初五`、`闰八月初五`

## 使用示例

### 添加联系人

```
用户：帮我添加一个朋友
助手：好的！请问这位朋友叫什么名字？
用户：叫李四，是我大学同学
助手：请问他的生日是什么时候？
用户：农历八月初五
助手：还有其他需要记录的信息吗？
用户：他喜欢打篮球
助手：好的，已创建联系人文件。
```

### 查看提醒

```
用户：最近有什么重要日子吗？
助手：📅 未来7天提醒：
      1. 张三的生日 - 3天后（5月20日）
         💡 建议礼物：篮球相关周边
```

### 生成祝福语

```
用户：帮我写个生日祝福给李四
助手：基于李四的信息，我为你生成了以下祝福语：
      "李四，生日快乐！🎂 希望你球场上依旧生龙活虎..."
```

## 技术实现

### 依赖

- Node.js
- `lunar-javascript`：农历转换
- `js-yaml`：YAML 解析

### 脚本

- `lunar-converter.js`：农历/阳历转换
- `reminder-checker.js`：提醒检查
- `content-generator.js`：内容生成

## 配置文件

### 完整配置示例

```yaml
# 数据存储路径
data_path: "./reminder-data"

# 提醒设置
reminders:
  enabled: true
  advance_days: 7

# 推送设置
notifications:
  primary: "opencode"
  fallback: "email"

# 邮件设置（可选）
email:
  smtp_host: "smtp.gmail.com"
  smtp_port: 587
  username: "your-email@gmail.com"
  password: "your-app-password"
  to_address: "your-email@gmail.com"

# AI 生成设置
ai_generation:
  enabled: true
  tone_adaptation: true
```

## 注意事项

1. **数据备份**：建议定期备份 `reminder-data` 目录
2. **时区处理**：所有日期按本地时区处理
3. **农历准确性**：基于标准农历算法，极端年份可能不准确
4. **闰月处理**：闰月仅在首月触发一次提醒

## 故障排除

### 农历日期转换错误

检查输入格式是否正确：
- ✅ 正确：`八月初五`、`8-15`
- ❌ 错误：`8月15日`（应使用中文或数字短横线格式）

### 提醒未触发

检查：
1. `config.yml` 中的 `reminders.enabled` 是否为 `true`
2. 事件是否标记了 `reminder: true`
3. 日期格式是否正确

### 如何修改联系人

直接编辑对应的 Markdown 文件即可。

## 开发计划

- **Phase 1** ✅：基础 CRUD + 阳历生日提醒
- **Phase 2** ✅：农历转换、闰月逻辑
- **Phase 3** 🔄：日历 API 集成、消息确认机制

## License

MIT
