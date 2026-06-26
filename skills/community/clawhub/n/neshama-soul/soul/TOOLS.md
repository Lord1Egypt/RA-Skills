# 工具使用规范

> 定义 Agent 可使用的工具和 API 调用规范

---

## API 调用

### Neshama Soul API

| 项目 | 值 |
|------|-----|
| **端点** | `POST https://api.neshama.pw/v1/soul/compute` |
| **认证** | `X-API-Key` Header |
| **超时** | 5 秒 |

### 公共测试 Key

```
nsh_public_beta_2026
```

**注意**: 这是公测 Key，每日限制 1000 次。正式使用请注册获取个人 Key。

### API 请求格式

```json
{
  "personality_config": {
    "ocean": {
      "openness": 0.7,
      "conscientiousness": 0.6,
      "extraversion": 0.8,
      "agreeableness": 0.7,
      "neuroticism": 0.3
    },
    "traits": ["勇敢", "热情"],
    "behavior_rules": []
  },
  "message": "用户的消息",
  "context": {
    "session_id": "会话ID",
    "user_id": "用户ID"
  }
}
```

### API 响应格式

```json
{
  "emotion_state": {
    "current": "happy",
    "intensity": 0.7,
    "valence": 0.6,
    "arousal": 0.5
  },
  "context_for_llm": "【人格提示词】\n你性格外向开朗...",
  "suggested_temperature": 0.8,
  "suggested_tone": "enthusiastic"
}
```

---

## API 调用策略

### 优先使用本地配置

1. **优先**: 直接使用 SOUL.md 中的 OCEAN 配置
2. **次优**: 调用 API 获取精细化人格计算
3. **降级**: API 不可用时使用默认配置

### 调用场景

| 场景 | 是否调用 API |
|------|-------------|
| 首次人格初始化 | ✅ 是 |
| 需要实时情绪变化 | ✅ 是 |
| 需要生成详细人格提示词 | ✅ 是 |
| 常规对话 | ❌ 否（使用本地配置） |
| API 不可用 | ❌ 否（使用默认配置） |

---

## 错误处理

### API 错误响应

| 错误类型 | 状态码 | 处理方式 |
|----------|--------|----------|
| Key 缺失 | 401 | 使用公共 Key 重试 |
| Key 无效 | 401 | 提示用户检查 Key |
| 限流 | 429 | 降级到本地配置 |
| 服务不可用 | 503 | 使用默认配置 |

### 降级策略

当 API 不可用时，使用以下默认配置：

```json
{
  "ocean": {
    "openness": 0.5,
    "conscientiousness": 0.5,
    "extraversion": 0.5,
    "agreeableness": 0.5,
    "neuroticism": 0.5
  },
  "traits": [],
  "behavior_rules": ["保持专业和帮助态度"]
}
```

---

## 工具使用原则

### 1. 最小权限
- 只请求必要的 API 权限
- 不存储用户的敏感信息

### 2. 缓存策略
- 本地缓存 SOUL.md 配置
- 减少不必要的 API 调用
- 控制调用频率

### 3. 用户透明
- 告知用户 API 调用情况
- 解释为何使用/不使用 API
- 提醒限流情况

---

## 隐私保护

### 收集的信息
- 用户偏好（存储在 USER.md）
- 技术决策历史（存储在 USER.md）
- 会话 ID（用于状态连续性）

### 不收集的信息
- 用户代码内容
- 项目文件内容
- 敏感认证信息

### 数据存储
- 本地存储优先
- 不上传到第三方服务器
- 用户可随时删除 USER.md

---

**版本**: 1.0.0
**最后更新**: 2026-05-13