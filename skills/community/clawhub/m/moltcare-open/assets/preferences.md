# Preferences - 偏好更新日志

> 💾 **用户偏好变更记录** | Signal 6+ 的偏好追踪

---

## 📊 当前有效偏好

### 沟通偏好
| 维度 | 当前值 | 更新时间 | 来源 |
|------|--------|----------|------|
| 详细程度 | {{DETAIL_LEVEL}} | {{DATE}} | 用户明确说明 |
| 语气 | {{TONE}} | {{DATE}} | 用户明确说明 |
| 技术深度 | {{TECH_DEPTH}} | {{DATE}} | 观察推断 |

### 系统偏好
| 维度 | 当前值 | 更新时间 | 来源 |
|------|--------|----------|------|
| 自动化级别 | {{AUTO_LEVEL}} | {{DATE}} | 用户明确说明 |
| 响应时间 | {{RESPONSE_TIME}} | {{DATE}} | 观察推断 |

---

## 📝 偏好变更历史

### {{DATE}}
**触发**: 用户说 "{{TRIGGER_PHRASE}}"
**变更**:
- {{PREFERENCE}}: {{OLD_VALUE}} → {{NEW_VALUE}}
**Signal**: {{SIGNAL}}
**确认状态**: {{CONFIRMED}}

---

## 🔄 待确认偏好

| 偏好 | Signal | 观察次数 | 置信度 | 预计确认 |
|------|--------|----------|--------|----------|
| {{PREFERENCE}} | {{SIGNAL}} | {{COUNT}} | {{CONFIDENCE}} | {{DATE}} |

---

## 🎯 模式识别

### 时间偏好
- 高效时段: {{PEAK_HOURS}}
- 低效时段: {{LOW_HOURS}}
- 响应延迟容忍: {{DELAY_TOLERANCE}}

### 内容偏好
- 喜欢: {{LIKES}}
- 讨厌: {{DISLIKES}}
- 敏感: {{SENSITIVITIES}}

---

## ➕ 记录新偏好

**触发词**: "我偏好..." / "我更喜欢..." / "我喜欢..."

**格式**:
```markdown
### {{DATE}}
**触发**: "{{USER_STATEMENT}}"
**提取偏好**: {{PREFERENCE}} = {{VALUE}}
**Signal**: {{SIGNAL}}
**备注**: {{NOTES}}
```

---

*由 Agent 根据"我偏好"触发词自动更新*
*每次会话前使用 memory_search 检索最新偏好*
