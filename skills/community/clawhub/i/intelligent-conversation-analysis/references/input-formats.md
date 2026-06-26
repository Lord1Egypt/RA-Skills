# 输入格式参考

## task.json 完整格式

### 文本对话输入

```json
{
  "taskType": "text",
  "resultTypes": ["summary", "keywords"],
  "taskNote": "客服咨询对话分析",
  "dialogue": {
    "sentences": [
      { "role": "agent", "text": "您好，请问有什么可以帮您？" },
      { "role": "user", "text": "我想了解一下退款流程" },
      { "role": "agent", "text": "好的，退款需要在购买后 7 天内申请，请问您是哪个订单？" },
      { "role": "user", "text": "订单号是 2024001，昨天买的" },
      { "role": "agent", "text": "好的，我帮您提交退款申请，预计 3 个工作日到账" }
    ]
  }
}
```

### 语音文件输入

```json
{
  "taskType": "audio",
  "resultTypes": ["summary", "service_inspection"],
  "taskNote": "外呼录音质检",
  "transcription": {
    "voiceFileUrl": "https://example.com/recordings/call-001.mp3",
    "fileName": "call-001.mp3",
    "roleIdentification": true
  },
  "serviceInspection": {
    "sceneIntroduction": "电话客服场景",
    "inspectionIntroduction": "检测客服服务规范性",
    "inspectionContents": [
      { "title": "礼貌用语", "content": "客服是否使用规范的问候和结束语" }
    ]
  }
}
```

---

## 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `taskType` | string | ✅ | `"text"` 或 `"audio"` |
| `resultTypes` | string[] | ✅ | 分析类型列表，至少一种 |
| `dialogue` | object | text 时必填 | 文本对话内容 |
| `transcription` | object | audio 时必填 | 语音文件配置 |
| `serviceInspection` | object | 质检时必填 | 质检配置 |
| `fields` | array | 字段提取时必填 | 字段定义 |
| `categoryTags` | array | 标签分类时必填 | 标签定义 |
| `customPrompt` | string | 自定义分析时必填 | 自定义指令 |
| `taskNote` | string | 否 | 任务备注，便于识别 |

---

## dialogue.sentences 说明

每条对话包含：

| 字段 | 值 | 说明 |
|------|-----|------|
| `role` | `"user"` | 客户/用户 |
| `role` | `"agent"` | 客服/坐席 |
| `role` | `"system"` | 系统消息 |
| `text` | string | 对话文本内容 |

**构建对话时问自己**：
- 每条消息是谁说的？客服还是客户？
- 消息顺序是否正确？
- 是否有系统消息（如 IVR 提示音）需要标注？

---

## transcription 说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `voiceFileUrl` | string | 音频文件公网 URL（必填） |
| `fileName` | string | 文件名，含扩展名（必填） |
| `roleIdentification` | boolean | 自动识别说话角色，默认 false |
| `clientChannel` | number | 双轨录音中客户的轨道编号（0 或 1） |
| `serviceChannel` | number | 双轨录音中客服的轨道编号（0 或 1） |

**音频要求**：
- 推荐 8k 采样率（其他采样率影响识别效果）
- 支持 mp3、wav 等常见格式
- URL 必须是可公网访问的地址

---

## 输入优先级

1. 命令行参数（JSON 文件路径）— 最高优先级
2. `$ARGUMENTS` 环境变量 — 次优先级
