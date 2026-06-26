# 阶段二：模型推荐规则 (Choice Rules)

本文档定义如何根据阶段一输出的结构化意图 JSON，按优先级规则匹配最优模型，并输出推荐结果。

---

## 输出 Schema

```json
{
  "recommended_model": "string（必须是规则中出现的模型全名）",
  "reason": "string（一句话推荐理由，面向用户展示）",
  "api_id": "string（对应 JoyCreator apiId）",
  "brand": "doubao | hailuo | kling | paiwo"
}
```

> **注意**：若 `base_params.brand_preference` 不为 null，直接跳过本规则，使用用户指定品牌，进入阶段三。

---

## 模型与 apiId 对照总表

### 视频生成模型

| 模型名称 | apiId | brand | 核心优势 |
|---------|-------|-------|---------|
| 海螺 Hailuo-2.3 | `460`(文生) / `461`(图生) | hailuo | 动作稳定、物理真实 |
| 海螺 Hailuo-2.3-Fast | `462` | hailuo | 速度优先 |
| 海螺 S2V-01 | `459` | hailuo | 主体一致性参考生视频 |
| 可灵 Kling-V3 | `565`(文生) / `566`(图生) | kling | 多镜头、音频、高质量 |
| 可灵 Kling-V2.6 | `563`(文生) / `564`(图生) | kling | 真实感、音频同步 |
| 可灵 Kling-O1 | `560`(文生) / `561`(图生) / `562`(参考) | kling | 方言、音色绑定、叙事 |
| 可灵 Kling-V1.6 | `552` | kling | 多图参考生视频 |
| 拍我 V5.5 | `401`(文生) / `402`(图生) | paiwo | 对口型、音频细致 |
| 拍我 V5 | `400`(文生) / `501`(图生) / `503`(参考) | paiwo | 稳定通用 |
| 豆包 Seedance-1.5-Pro | `750`(文生) / `751`(图生) | doubao | IP角色、分镜 |

### 图像生成模型

| 模型名称 | apiId | brand | 核心优势 |
|---------|-------|-------|---------|
| 豆包 Seedream-4.5 | `701` | doubao | 电商产品、参考图学习能力强 |
| 豆包 Seedream-4.0 | `700` | doubao | 通用图像生成 |
| 海螺 image-01 | `456` | hailuo | 人像一致性 |
| 可灵 Kling-V2.1（文生图）| `553` | kling | 高分辨率直出 |
| 可灵 Kling-V2（图生图）| `554` | kling | 图生图参考 |
| 拍我 | ❌ | — | 不支持图像生成 |

---

## 视频生成推荐规则 (VIDEO_GENERATION)

按优先级从高到低匹配，**首个命中规则即为最终推荐**：

### 规则 V1：极速/低预算/批量
**触发条件**：core_prompt 或上下文包含「快速预览」「批量」「高性价比」「便宜」

→ 推荐：`海螺 Hailuo-2.3-Fast`（apiId 视图生/文生决定）

---

### 规则 V2：复杂动作与物理场景
**触发条件**：core_prompt 包含「打斗」「格斗」「舞蹈」「跑酷」「运动员」「武侠」「激烈」等动作类词汇

→ 推荐：`海螺 Hailuo-2.3`（动作稳定性和物理真实感最佳）

---

### 规则 V3：对口型 + 精细音效
**触发条件**：`video_features.needs_audio == true` AND core_prompt 含「对口型」「台词」「说话」「演讲」「唱歌」

→ 推荐：`拍我 V5.5`（精细音效和口型同步）

---

### 规则 V4：方言 / 多语言 / 多镜头短剧
**触发条件**：`video_features.needs_audio == true` AND core_prompt 含「方言」「四川话」「粤语」「多镜头」「短剧」「多角色」「多场景」

→ 推荐：`可灵 Kling-O1`（支持方言、音色绑定、多主体连续场景）

---

### 规则 V5：IP 角色复刻 / 自动分镜
**触发条件**：core_prompt 含「IP」「角色复刻」「固定角色」「自动分镜」「系列视频」

→ 推荐：`豆包 Seedance-1.5-Pro`（IP 角色视频复刻、自动分镜能力）

---

### 规则 V6：参考图生视频（主体一致性）
**触发条件**：`base_params.has_reference == true` AND 用户要求保持「人物一致」「角色不变」「同一主体」

→ 推荐：`海螺 S2V-01`（apiId: 459，主体一致性参考生视频）

---

### 规则 V7：多镜头叙事 + 普通音频
**触发条件**：`video_features.needs_audio == true` AND core_prompt 含「多镜头」「叙事」「故事」，但不含方言

→ 推荐：`可灵 Kling-V3`（支持多镜头、sound 参数）

---

### 规则 V8：默认兜底
**触发条件**：以上规则均未命中

→ 推荐：`可灵 Kling-V3`（综合能力强，支持多场景）

---

## 图像生成推荐规则 (IMAGE_GENERATION)

### 规则 I1：电商产品图 / 强参考图学习
**触发条件**：core_prompt 含「产品」「商品」「电商」「白底」「展示图」，或 `has_reference == true`

→ 推荐：`豆包 Seedream-4.5`（apiId: 701，商业产品与垫图能力强）

---

### 规则 I2：极致真实感 / 文字渲染
**触发条件**：core_prompt 含「超真实」「皮肤纹理」「光影细节」，或包含需在图中生成的**具体文字内容**（如海报文字、标题）

→ 推荐：`可灵 Kling-V2.1`（apiId: 553，高分辨率直出，写实细节）

> 注：如有 NanoBananaPro 接入，优先推荐 NanoBananaPro。

---

### 规则 I3：人像特化
**触发条件**：core_prompt 主体是人物，且强调「人像」「面部」「写真」「肖像」「一致性」

→ 推荐：`海螺 image-01`（apiId: 456，人像一致性最佳）

---

### 规则 I4：高分辨率直出 (2K/4K)
**触发条件**：`image_features.high_quality_req == true`

→ 推荐：`可灵 Kling-V2.1`（apiId: 553，支持高分辨率）

---

### 规则 I5：图生图（有参考图，非人像）
**触发条件**：`has_reference == true` AND 非人像场景

→ 推荐：`可灵 Kling-V2`（apiId: 554，图生图参考）

---

### 规则 I6：默认兜底
**触发条件**：以上规则均未命中

→ 推荐：`豆包 Seedream-4.5`（apiId: 701，综合质量与速度均衡）

---

## Few-Shot 示例

### 示例 1：动作场景 → 海螺

**输入意图 JSON**：
```json
{
  "intent_type": "VIDEO_GENERATION",
  "core_prompt": "两名武侠在竹林中激烈对决，刀光剑影，竹叶飞舞",
  "base_params": { "aspect_ratio": "9:16", "has_reference": false, "brand_preference": null },
  "video_features": { "needs_audio": true, "camera_movement": "快速运镜", "duration": 10 }
}
```

**命中规则**：V2（含「激烈」「武侠」「对决」）

**输出**：
```json
{
  "recommended_model": "海螺 Hailuo-2.3",
  "reason": "提示词包含激烈打斗动作场景，海螺 Hailuo-2.3 在动作稳定性和物理真实感方面表现最佳。",
  "api_id": "460",
  "brand": "hailuo"
}
```

---

### 示例 2：文字渲染海报 → 可灵

**输入意图 JSON**：
```json
{
  "intent_type": "IMAGE_GENERATION",
  "core_prompt": "电影级特写海报，女孩脸部皮肤纹理清晰，阳光打在脸上，海报上写着 SUMMER",
  "base_params": { "aspect_ratio": "9:16", "has_reference": false, "brand_preference": null },
  "image_features": { "task_num": 1, "high_quality_req": true }
}
```

**命中规则**：I2（含「皮肤纹理」+ 需在图中生成文字「SUMMER」）

**输出**：
```json
{
  "recommended_model": "可灵 Kling-V2.1",
  "reason": "用户追求极致皮肤光影细节，且需要在画面中渲染特定文字，可灵 V2.1 的写实细节和文字渲染能力最佳。",
  "api_id": "553",
  "brand": "kling"
}
```

---

### 示例 3：方言短剧 → 可灵 O1

**输入意图 JSON**：
```json
{
  "intent_type": "VIDEO_GENERATION",
  "core_prompt": "四川方言搞笑对话短剧，两名角色面对面交流",
  "base_params": { "aspect_ratio": "9:16", "has_reference": false, "brand_preference": null },
  "video_features": { "needs_audio": true, "camera_movement": null, "duration": 5 }
}
```

**命中规则**：V4（needs_audio=true + 含「方言」+「多角色对话」）

**输出**：
```json
{
  "recommended_model": "可灵 Kling-O1",
  "reason": "用户需要多角色连续场景且明确需要支持方言，可灵 O1 支持方言、音色绑定与多镜头叙事。",
  "api_id": "560",
  "brand": "kling"
}
```
