---
name: kimi-code-quota
description: Query Kimi Code Plan quota and usage information. Use when the user wants to check their Kimi Code subscription quota, usage percentage, reset time, or API key status. Triggers on keywords like "kimi code额度", "查看kimi code", "kimi code plan", "quota", "额度查询".
---

# Kimi Code 额度查询

查询用户的 Kimi Code Plan 订阅额度、使用情况和 API Keys 状态。

## 查询流程

### 1. 打开 Kimi Code 网站

```bash
agent-browser open https://www.kimi.com/code --headed
```

### 2. 检查登录状态

获取页面快照，检查是否已登录：

```bash
agent-browser snapshot -i
```

**如果看到 "注册/登录" 按钮**：用户未登录，需要引导用户登录
- 点击 "注册/登录" 按钮
- 支持微信扫码或手机号登录
- 等待用户确认登录完成

**如果看到用户名（如 "登月者1989"）**：用户已登录，继续下一步

### 3. 进入控制台

点击 "控制台" 按钮：

```bash
agent-browser click "@e29"  # 控制台按钮的ref，可能需要根据实际情况调整
```

### 4. 获取额度信息

进入控制台后，截图并获取页面内容：

```bash
agent-browser snapshot -i
agent-browser screenshot quota.png
```

需要获取的关键信息：
- **本周用量**：百分比和重置时间（如 "7%（159小时后重置）"）
- **频限明细**：百分比和重置时间（如 "4%（3小时后重置）"）
- **会员等级**：如 Moderato、Andante、Allegretto、Allegro
- **模型权限**：如 K2.5 旗舰模型

### 5. 获取 API Keys 信息

在控制台页面查看 API Keys 表格：
- API ID
- 名称
- 创建时间
- Key（部分隐藏）
- 状态（生效中/已停用）

### 6. 汇总报告

向用户报告以下信息：

```
📊 Kimi Code Plan 额度

| 项目 | 状态 |
|------|------|
| 本周用量 | X%（X小时后重置） |
| 频限明细 | X%（X小时后重置） |
| 会员等级 | XXX |
| 模型权限 | XXX |

🔑 API Keys
- 名称: XXX
- 创建时间: XXX
- 状态: 生效中

📝 最近使用记录（可选）
- 显示最近几条使用记录
```

## 注意事项

1. **登录状态**：如果用户未登录，需要先完成登录流程
2. **ref 编号**：页面元素的 ref 编号（如 @e29）可能会变化，需要根据实际情况调整
3. **超时处理**：网络较慢时可能需要增加等待时间
4. **页面结构**：如果页面改版，可能需要更新选择器

## 示例对话

**用户**: "查一下我的kimi code额度"

**助手**: 打开浏览器访问 Kimi Code → 检查登录状态 → 进入控制台 → 获取额度信息 → 汇总报告

**用户**: "kimi code还剩多少"

**助手**: 同上流程

## 相关链接

- Kimi Code 官网: https://www.kimi.com/code
- 控制台: https://www.kimi.com/code/console
