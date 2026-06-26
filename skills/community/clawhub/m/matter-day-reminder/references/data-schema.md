# 提醒数据结构

## 配置文件 (config.yml)

```yaml
# 数据存储路径
data_path: "./reminder-data"

# 提醒设置
reminders:
  enabled: true
  advance_days: 7  # 提前提醒天数
  
# 推送设置
notifications:
  primary: "opencode"  # 主渠道
  fallback: "email"    # 兜底渠道
  
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
  tone_adaptation: true  # 根据关系调整语气
```

## 联系人 Markdown Schema

每个联系人为独立的 Markdown 文件，使用 YAML Frontmatter + Markdown 内容。

### Frontmatter 字段

| 字段名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| name | string | 是 | 联系人姓名 |
| relationship | string | 是 | 关系类型：friend, close_friend, family, colleague |
| relationship_detail | string | 否 | 关系详情描述 |
| tags | array | 否 | 标签数组，如 ["篮球", "科技"] |
| created_at | string | 是 | 创建日期，格式 YYYY-MM-DD |
| updated_at | string | 是 | 更新日期，格式 YYYY-MM-DD |

### 事件格式

在 Markdown 正文中使用三级标题定义事件：

```markdown
### 事件名称
- **类型**: 事件类型（生日、纪念日等）
- **日期**: 日期格式
  - 阳历：YYYY-MM-DD
  - 农历：X月X日 或 农历八月初五
- **农历**: true/false
- **提醒**: true/false
```

### 完整示例

```markdown
---
name: "李四"
relationship: "family"
relationship_detail: "父亲"
tags: ["书法", "茶", "旅游"]
created_at: "2024-01-15"
updated_at: "2024-01-15"
---

# 李四

## 事件

### 生日
- **类型**: 生日
- **日期**: 农历八月初五
- **农历**: true
- **提醒**: true

### 结婚纪念日
- **类型**: 纪念日
- **日期**: 1990-10-01
- **农历**: false
- **提醒**: true

## 备注

- 喜欢喝茶，尤其是龙井
- 不喜欢太吵闹的地方
- 最近想学书法
```

## 关系类型定义

| 类型 | 标识 | 预算规则 | 语气风格 |
|------|------|----------|----------|
| 朋友 | friend | ≤300元 | 轻松随意 |
| 密友 | close_friend | ≤300元 | 亲密自然 |
| 家人 | family | 弹性 | 温暖关怀 |
| 同事 | colleague | ≤200元 | 礼貌专业 |

## 日期格式规范

### 阳历日期

格式：`YYYY-MM-DD`

示例：
- 1990-05-20
- 2024-12-25

### 农历日期

格式支持多种形式：

1. **标准格式**：X月X日
   - 八月初五
   - 腊月二十三

2. **数字格式**：X-X
   - 8-15
   - 12-23

3. **闰月**：在月份前加"闰"
   - 闰八月初五
   - 闰8-15

## 目录结构

```
reminder-data/
├── config.yml              # 全局配置文件
├── contacts/               # 联系人目录
│   ├── zhang-san.md
│   ├── li-si.md
│   └── wang-wu.md
└── logs/                   # 日志目录（可选）
    └── reminders.log
```

## 提醒数据结构

当检查提醒时，生成以下数据结构：

```json
{
  "contact": "联系人姓名",
  "relationship": "关系类型",
  "relationship_detail": "关系详情",
  "event": "事件名称",
  "event_type": "事件类型",
  "target_date": "目标日期（阳历）",
  "original_date": "原始日期（农历或阳历）",
  "is_lunar": true/false,
  "days_until": 距离天数,
  "reminder_type": "today/advance",
  "reminder_title": "提醒标题"
}
```

## 闰月处理规则

1. **闰月标记**：在农历日期中使用"闰"字标记，如"闰八月"
2. **触发规则**：闰月仅在首次出现时触发提醒
3. **转换逻辑**：使用 lunar-javascript 库自动处理闰月转换
4. **边界情况**：如果闰月不存在于当年（如今年没有闰八月），则自动跳过
