---
name: joycreator-api
description: 调用京东云灵境(Lingjing) JoyCreator 平台的 AI 生成 API。具备三阶段智能管线：① 意图理解（解析自然语言为结构化 JSON）→ ② 模型推荐（根据场景特征自动匹配最优模型）→ ③ API 调用（构造请求并提交任务）。支持文生图、文生视频、图生视频、参考图生视频，覆盖豆包/海螺/可灵/拍我等全系列模型。当用户提到灵境、JoyCreator、豆包、海螺、可灵、拍我、文生图、文生视频、图生视频、AI绘图、AI视频生成、想画图、想做视频时，必须使用此 skill。用户无需指定模型，系统可自动推荐。
---

# 灵境 JoyCreator 智能接入 Skill

## 系统架构：三阶段智能管线

```
用户自然语言输入
      │
      ▼
┌─────────────────┐
│  阶段一：意图路由  │  解析意图类型 + 提取结构化特征
│  (Router)       │  → 参考 references/router-rules.md
└────────┬────────┘
         │ 输出结构化意图 JSON
         ▼
┌─────────────────┐
│  阶段二：模型推荐  │  根据场景特征匹配最优模型
│  (Choice)       │  → 参考 references/choice-rules.md
└────────┬────────┘
         │ 输出 recommended_model + apiId
         ▼
┌─────────────────┐
│  阶段三：API调用  │  构造请求 → 提交任务 → 轮询结果
│  (Executor)     │  → 参考 references/{brand}.md
└─────────────────┘
```

---

## 前置：收集鉴权信息

**在任何阶段开始前，必须先向用户索取：**

```
请提供您的 JoyCreator App Key（在京东云 JoyCreator 控制台「应用管理」页面获取）
```

请求头格式：
```
Authorization: Bearer <app_key>
x-jdcloud-request-id: <每次请求生成的唯一 UUID>
```

---

## 阶段一：意图路由 (Router)

> 详细规则见 `references/router-rules.md`

**任务**：将用户的自然语言输入解析为标准结构化 JSON，供阶段二使用。

输出结构：
```json
{
  "intent_type": "IMAGE_GENERATION" | "VIDEO_GENERATION" | "UNKNOWN",
  "core_prompt": "提炼后的高质量提示词",
  "base_params": {
    "aspect_ratio": "16:9",
    "has_reference": false,
    "brand_preference": null
  },
  "video_features": { "needs_audio": false, "camera_movement": null, "duration": 5 },
  "image_features": { "task_num": 1, "high_quality_req": false }
}
```

**如果用户已明确指定模型品牌**（如"用可灵生成..."），跳过阶段二，直接进入阶段三。

---

## 阶段二：模型推荐 (Choice)

> 详细规则见 `references/choice-rules.md`

**任务**：根据阶段一输出的意图 JSON，按优先级规则匹配最优模型。

输出结构：
```json
{
  "recommended_model": "模型全名",
  "reason": "一句话推荐理由",
  "api_id": "对应 apiId",
  "brand": "doubao | hailuo | kling | paiwo"
}
```

推荐后**向用户展示**推荐结果和理由，询问是否确认或更换。

---

## 阶段三：API 调用 (Executor)

> 各品牌详细参数见 `references/{brand}.md`

### 统一接口
```
POST https://model.jdcloud.com/joycreator/openApi/submitTask
Authorization: Bearer <app_key>
Content-Type: application/json
```

### 请求体结构
```json
{
  "apiId": "<阶段二确定的 apiId>",
  "params": {
    "model" 或 "model_name": "<模型名称>",
    "prompt": "<阶段一提炼的 core_prompt>",
    ... 其他参数（从 base_params / video_features / image_features 中映射）
  }
}
```

### 参数品牌映射文档

| 品牌 | 参考文档 |
|------|---------|
| 豆包 (Seedream/Seedance) | `references/doubao.md` |
| 海螺 (Hailuo) | `references/hailuo.md` |
| 可灵 (Kling) | `references/kling.md` |
| 拍我 (PaiWo) | `references/paiwo.md` |

### 提交响应处理
```json
// 成功
{ "success": true, "genTaskId": "任务ID" }

// 失败
{ "success": false, "error": "错误码", "errorParamName": "出错参数名" }
```

### 轮询策略
- 每 **3 秒**查询一次任务状态
- 最多 **60 次**（约 3 分钟超时）
- 终态：`SUCCESS` 或 `FAILED`

---

## 代码生成

使用 `scripts/joycreator.py` 为用户生成可运行代码：

- **智能模式**（推荐）：`python scripts/joycreator.py`（自动走三阶段管线）
- **参数模式**：`python scripts/joycreator.py --brand kling --task text2video --prompt "..."`

---

## 安全提示

- `app_key` 建议通过环境变量 `JOYCREATOR_APP_KEY` 传入，不要硬编码
- 图片 URL 必须为**公网可访问**地址
- 生成结果 URL 有时效限制，请及时下载保存
