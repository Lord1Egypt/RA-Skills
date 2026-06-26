# 推送模板

## Telegram

目标: 8290054457
限制: 4096 字符/条

### 完整版 (推荐)

```
🆕 OpenClaw 版本更新 | {版本号}

📅 发布于: {日期}

━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 更新内容:

【新增功能】

{新增功能列表}

━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 问题修复 (部分):

{问题修复列表}

━━━━━━━━━━━━━━━━━━━━━━━━━━

🔗 完整更新日志:
https://github.com/openclaw/openclaw/releases/tag/{版本号}
```

### 精简版 (超过限制时使用)

```
🆕 OpenClaw {版本号} 发布！

{主要更新亮点}

🔗 https://github.com/openclaw/openclaw/releases
```

## 解析发布说明

原始内容格式:

```
### Changes
- Android/chat settings: ...
- iOS/onboarding: ...

### Fixes
- Dashboard/chat UI: ...
- ...
```

翻译规则:
1. `Changes` → 【新增功能】
2. `Fixes` → 【问题修复】
3. 每条以 `- ` 开头，提取核心内容
4. 超过 4096 字符时，使用精简版

## 提取规则

### 新增功能 (Changes)
- 保留功能名称和简要描述
- 去除 PR 编号和贡献者信息

### 问题修复 (Fixes)
- 按类别分组（UI/网关/安全/平台等）
- 保留核心修复内容
