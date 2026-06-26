# Hopola 使用示例

## 示例 1：单入口全流程（图片）

### 输入示例
```json
{
  "mode": "pipeline",
  "task_type": "image",
  "query": "宠物品牌视觉趋势",
  "image_prompt": "一只可爱的小狗，阳光草地，高清摄影风格",
  "image_ratio": "1:1",
  "upload_enabled": true,
  "report_format": "markdown"
}
```

### 预期输出片段
```markdown
## 检索结果摘要
- 信号 1：……

## 生成结果（图片/视频/3D）
- 类型：image
- 状态：成功
- 工具：text2image_create_hydra_hoppa
- 链接：<IMAGE_URL>

## 上传结果
- 状态：成功
- 链接：<UPLOAD_URL>
```

## 示例 2：仅执行视频生成

### 输入示例
```json
{
  "mode": "stage",
  "stage": "generate-video",
  "task_type": "video",
  "video_prompt": "一只小狗在海边奔跑，电影感镜头",
  "video_ratio": "16:9",
  "video_duration": 5,
  "report_format": "markdown"
}
```

## 示例 3：仅执行 3D 生成

### 输入示例
```json
{
  "mode": "stage",
  "stage": "generate-3d",
  "task_type": "3d",
  "model3d_prompt": "卡通风格小狗手办",
  "model3d_task_type": "3d_standard",
  "model3d_format": "glb",
  "report_format": "markdown"
}
```

## 示例 4：仅执行 Logo 设计

### 输入示例
```json
{
  "mode": "stage",
  "stage": "generate-logo",
  "task_type": "logo",
  "brand_name": "PawJoy",
  "brand_industry": "宠物消费",
  "logo_prompt": "现代极简宠物品牌logo，带小狗元素，干净高级",
  "logo_ratio": "1:1",
  "report_format": "markdown"
}
```

## 示例 5：仅执行商品图生成

### 输入示例（确认前，不触发生图）
```json
{
  "mode": "stage",
  "stage": "generate-product-image",
  "task_type": "product-image",
  "product_name": "316不锈钢保温杯",
  "product_category": "家居日用",
  "product_selling_points": ["12小时保温", "防漏便携", "食品级材质"],
  "target_channel": "电商主图",
  "target_audience": "25-35岁通勤人群",
  "desired_scenes": ["纯白主图", "场景氛围图", "卖点信息图"],
  "product_image_url": "https://example.com/product.png",
  "source_image_confirmed": false,
  "product_info_confirmed": false,
  "report_format": "markdown"
}
```

### 预期输出片段（确认前）
```markdown
## 商品信息确认卡
- 商品名称：316不锈钢保温杯
- 商品类目：家居日用
- 核心卖点：12小时保温、防漏便携、食品级材质
- 渠道：电商主图
- 目标人群：25-35岁通勤人群
- 商品原图：https://example.com/product.png
- 目标场景：纯白主图、场景氛围图、卖点信息图

请确认以上信息是否正确。回复“确认生成”后开始生图。
```

### 输入示例（确认后，触发生图）
```json
{
  "mode": "stage",
  "stage": "generate-product-image",
  "task_type": "product-image",
  "product_image_url": "https://example.com/product.png",
  "desired_scenes": ["纯白主图", "场景氛围图", "卖点信息图"],
  "product_prompt": "替换为高级电商背景，突出金属质感与便携卖点",
  "source_image_confirmed": true,
  "product_info_confirmed": true,
  "report_format": "markdown"
}
```

### 预期调用参数片段（每次调用都必须携带确认源图）
```json
{
  "tool_name": "image_praline_edit_v2",
  "args": {
    "image_list": ["https://example.com/product.png"],
    "prompt": "替换为高级电商背景，突出金属质感与便携卖点",
    "output_format": "jpg",
    "size": "1024x1024"
  },
  "source_image_confirmed": true
}
```

### 预期输出片段（源图门禁失败）
```json
{
  "structured_error": {
    "code": "PRODUCT_IMAGE_UNCONFIRMED_SOURCE",
    "stage": "precheck",
    "message": "商品原图尚未确认，已拦截本次调用。",
    "details": {
      "failed_step": "source_confirmation_check",
      "missing_fields": ["source_image_confirmed"]
    },
    "retry_suggestions": [
      "确认并锁定商品原图 URL",
      "将 source_image_confirmed 设为 true 后重试",
      "确保 image_list 仅包含确认后的 product_image_url"
    ]
  }
}
```

### 输入示例（未提供任何商品源图，仅允许询问）
```json
{
  "mode": "stage",
  "stage": "generate-product-image",
  "task_type": "product-image",
  "product_name": "316不锈钢保温杯",
  "desired_scenes": ["纯白主图", "场景氛围图", "卖点信息图"],
  "product_info_confirmed": false,
  "source_image_confirmed": false
}
```

### 预期输出片段（缺图询问，不触发生图）
```markdown
## 缺少商品源图
- 当前未检测到可用商品图片
- 请上传商品图片，或提供可公网访问的 https 商品原图链接

在补齐商品源图并确认前，不会触发任何商品图生成调用。
```

### 输入示例（纯自然语言 + key + 会话上传图，第一轮仅确认）
```json
{
  "mode": "pipeline",
  "query": "帮我生成商品图，key：demo_key_product_001",
  "session_uploaded_images": [
    "/mnt/data/session_uploads/pink_tee.png"
  ],
  "auto_upload_session_images": true,
  "response_language": "zh-CN"
}
```

### 预期输出片段（第一轮）
```markdown
## 输入归一化
- 已识别商品图意图并归一化到 `task_type=product-image`、`stage=generate-product-image`
- key：demo_key_product_001（仅作任务标识）

## 商品信息确认卡
- 商品原图：https://cdn.example.com/path/pink_tee.png
- 源图确认：false

请确认商品信息与源图后再开始生成。
```

### 预期输出片段（未确认时不得本地替代）
```json
{
  "structured_error": {
    "code": "PRODUCT_IMAGE_UNCONFIRMED_SOURCE",
    "stage": "precheck",
    "message": "商品原图尚未确认，已拦截本次调用，不允许本地替代生成。",
    "details": {
      "failed_step": "source_confirmation_check"
    },
    "retry_suggestions": [
      "确认商品原图 URL",
      "将 source_image_confirmed 设为 true 后重试"
    ]
  }
}
```

### 输入示例（仅上传会话图片并自动回填商品原图）
```json
{
  "mode": "stage",
  "stage": "generate-product-image",
  "task_type": "product-image",
  "session_uploaded_images": [
    "/mnt/data/session_uploads/product_bottle.png"
  ],
  "auto_upload_session_images": true,
  "product_name": "316不锈钢保温杯",
  "product_category": "家居日用",
  "product_selling_points": ["12小时保温", "防漏便携", "食品级材质"],
  "target_channel": "电商主图",
  "target_audience": "25-35岁通勤人群",
  "desired_scenes": ["纯白主图", "场景氛围图", "卖点信息图"],
  "product_info_confirmed": false,
  "report_format": "markdown"
}
```

### 输入示例（显式提供非 URL 输入，先上传再回填）
```json
{
  "mode": "stage",
  "stage": "generate-product-image",
  "task_type": "product-image",
  "product_image_url": "/mnt/data/session_uploads/product_bottle.png",
  "auto_upload_session_images": true,
  "product_name": "316不锈钢保温杯",
  "product_category": "家居日用",
  "product_selling_points": ["12小时保温", "防漏便携", "食品级材质"],
  "target_channel": "电商主图",
  "target_audience": "25-35岁通勤人群",
  "desired_scenes": ["纯白主图", "场景氛围图", "卖点信息图"],
  "product_info_confirmed": false,
  "report_format": "markdown"
}
```

### 预期输出片段（非 URL 输入已上传并回填）
```markdown
## 输入归一化
- 原始输入类型：local_file
- 动作：先上传再回填
- 回填字段：product_image_url
- 回填结果：https://cdn.example.com/path/product_bottle.png

## 商品信息确认卡
- 商品原图：https://cdn.example.com/path/product_bottle.png
```

### 预期输出片段（会话图自动上传成功）
```markdown
## 上传结果
- 来源：session
- 状态：成功
- 最终链接：https://cdn.example.com/path/product_bottle.png

## 商品信息确认卡
- 商品原图：https://cdn.example.com/path/product_bottle.png
```

### 预期输出片段（上传失败即终止生成）
```json
{
  "structured_error": {
    "code": "PRODUCT_IMAGE_UPLOAD_FAILED",
    "stage": "precheck",
    "message": "商品源图上传失败，已终止本次生图。",
    "details": {
      "failed_step": "upload_normalization",
      "source_input_type": "session"
    },
    "retry_suggestions": [
      "重新上传清晰商品图并重试",
      "改为直接提供可公网访问的 https 商品原图链接",
      "确认网络与上传权限后再次触发生成"
    ]
  }
}
```

### 预期输出片段（image_list 与确认源图不一致时拦截）
```json
{
  "structured_error": {
    "code": "PRODUCT_IMAGE_UNCONFIRMED_SOURCE",
    "stage": "precheck",
    "message": "检测到 image_list 与已确认源图不一致，已拦截调用。",
    "details": {
      "failed_step": "image_list_source_binding_check",
      "confirmed_source": "https://cdn.example.com/path/product_bottle.png",
      "image_list": ["https://cdn.example.com/path/other.png"]
    },
    "retry_suggestions": [
      "将 image_list 修正为仅包含已确认的商品原图链接",
      "若需更换源图，先重新确认 source_image_confirmed"
    ]
  }
}
```

### 预期输出片段（生成成功可追溯字段）
```json
{
  "tool_name_used": "image_praline_edit_v2",
  "source_image_url_used": "https://cdn.example.com/path/product_bottle.png",
  "source_image_origin": "uploaded_from_session",
  "precheck_report": {
    "tool_ready": true,
    "source_accessible": true,
    "source_confirmed": true,
    "args_valid": true
  }
}
```

### 输入示例（仅执行抠图）
```json
{
  "mode": "stage",
  "stage": "cutout",
  "task_type": "product-image",
  "session_uploaded_images": [
    "/mnt/data/session_uploads/product.png"
  ],
  "auto_upload_session_images": true,
  "cutout_mode": "auto",
  "output_background": "transparent",
  "report_format": "markdown"
}
```

### 输入示例（单图生 3D）
```json
{
  "mode": "stage",
  "stage": "generate-3d",
  "task_type": "3d",
  "model3d_image_url": "https://example.com/dog.png",
  "model3d_format": "glb",
  "report_format": "markdown"
}
```

## 固定优先 + 自动发现回退
- 先使用 `preferred_tool_name`。
- 3D 阶段默认优先 `3d_hy_image_generate`，如果提供 `model3d_image_url` 则优先 `fal_tripo_image_to_3d`。
- Logo 阶段默认优先 `aiflow_nougat_create`。
- 商品图阶段固定使用 `image_praline_edit_v2`。
- 商品图阶段即使发现同类工具，也必须优先并默认命中精确工具名 `image_praline_edit_v2`。
- 商品图阶段不使用自动发现回退；固定工具不可用时按 `PRODUCT_IMAGE_TOOL_UNAVAILABLE` 处理。
- 抠图阶段固定使用 `api_v1_sod_c_async`。
- 如果固定工具不可用，再用 `/api/gateway/mcp/tools` 按 `fallback_discovery_keywords` 匹配。
- 报告中必须写出 `tool_name_used` 与 `fallback_used`。

## 错误场景示例

### 场景 A：固定工具不可用，已触发回退
```markdown
## 安全状态与错误告警
- 告警：固定工具不可用
- 动作：已回退到自动发现策略
- 结果：成功
```

### 场景 B：上传接口鉴权失败
```markdown
## 上传结果
- 状态：失败
- 原因：401
- 建议：检查环境变量 OPENCLOW_KEY 是否已注入
```

### 场景 B2：网关 key 缺失（预检拦截，禁止生成功能）
```json
{
  "structured_error": {
    "code": "GATEWAY_KEY_MISSING",
    "stage": "precheck",
    "message": "缺少网关鉴权环境变量，已停止执行生成调用。",
    "details": {
      "required_env": "OPENCLOW_KEY",
      "failed_step": "gateway_key_precheck"
    },
    "retry_suggestions": [
      "在运行环境注入 OPENCLOW_KEY",
      "确认 OpenClaw Key 生效后重新执行",
      "如为多环境部署，请同步检查容器与任务编排配置"
    ]
  }
}
```

### 场景 C：商品图参考图不可访问（结构化错误）
```json
{
  "structured_error": {
    "code": "PRODUCT_IMAGE_SOURCE_NOT_ACCESSIBLE",
    "stage": "precheck",
    "message": "商品原图链接当前不可访问，暂不进入生图。",
    "details": {
      "http_status": 403,
      "failed_step": "source_url_accessibility_check",
      "source_input_type": "explicit_url"
    },
    "retry_suggestions": [
      "重新上传原图并使用回填链接",
      "替换为可公网访问的 https 链接",
      "稍后重试并确认链接未过期"
    ]
  }
}
```

### 场景 D：商品图参数不完整（结构化错误）
```json
{
  "structured_error": {
    "code": "PRODUCT_IMAGE_MISSING_ARGS",
    "stage": "precheck",
    "message": "商品图参数不完整，已拦截调用。",
    "details": {
      "missing_fields": ["prompt", "size"],
      "failed_step": "required_args_check"
    },
    "retry_suggestions": [
      "补充商品图提示词 prompt",
      "补充输出尺寸 size（例如 1024x1024）",
      "确认后再次触发生图"
    ]
  }
}
```

### 场景 E：会员权限拦截
```markdown
## 安全状态与错误告警
- 错误码：403001
- 动作：返回 data.redirect_url 并提示用户开通会员
```

## Gateway 调用片段

### 1）发现工具
```bash
curl -s "https://hopola.ai/api/gateway/mcp/tools" \
  -H "X-OpenClaw-Key: $OPENCLOW_KEY"
```

### 2）生图
```bash
curl -s "https://hopola.ai/api/gateway/mcp/call" \
  -H "Content-Type: application/json" \
  -H "X-OpenClaw-Key: $OPENCLOW_KEY" \
  -d '{
    "tool_name": "text2image_create_hydra_hoppa",
    "args": {
      "prompt": "一只可爱的小狗，阳光草地，高清摄影风格",
      "ratio": "1:1"
    }
  }'
```

### 3）Logo 设计
```bash
curl -s "https://hopola.ai/api/gateway/mcp/call" \
  -H "Content-Type: application/json" \
  -H "X-OpenClaw-Key: $OPENCLOW_KEY" \
  -d '{
    "tool_name": "aiflow_nougat_create",
    "args": {
      "prompt": "为宠物品牌 PawJoy 设计现代极简 logo，蓝绿配色，图文组合",
      "ratio": "1:1"
    }
  }'
```
