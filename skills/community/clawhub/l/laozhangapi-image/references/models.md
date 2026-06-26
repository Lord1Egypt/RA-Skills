# 模型详情

## 文生图模型

| 模型 | 模型ID | 价格 | 返回格式 | 特点 |
|------|--------|------|---------|------|
| Sora Image | sora_image | $0.01/张 | URL | 文生图，支持比例（2:3/3:2/1:1） |
| GPT-4o Image | gpt-4o-image | $0.01/张 | URL | GPT-4o 文生图 |
| Nano Banana | gemini-2.5-flash-image | $0.025/张 | base64 | Gemini 2.5 Flash，基础版 |
| Nano Banana2 | gemini-3.1-flash-image-preview | $0.03/张 | base64 | Gemini 3.1 Flash，支持4K |
| Nano Banana Pro | gemini-3-pro-image-preview | $0.05/张 | base64 | Gemini 3 Pro，支持4K，复杂指令 |

## 图片编辑模型

| 模型 | 模型ID | 价格 | 返回格式 | 特点 |
|------|--------|------|---------|------|
| GPT-4o Image | gpt-4o-image | $0.01/张 | URL | 图片编辑，单图/多图 |
| Sora Image | sora_image | $0.01/张 | URL | 图片编辑 |
| Nano Banana | gemini-2.5-flash-image | $0.025/张 | base64 | 图片编辑，多图合成，快速 |
| Nano Banana2 | gemini-3.1-flash-image-preview | $0.03/张 | base64 | 图片编辑，支持4K |
| Nano Banana Pro | gemini-3-pro-image-preview | $0.05/张 | base64 | 图片编辑，复杂指令，4K |

## 选择建议

- **需要发送到飞书**：选 URL 返回的模型（sora_image / gpt-4o-image）
- **需要高质量**：选 Nano Banana Pro（支持4K）
- **性价比**：选 Nano Banana（$0.025/张）

## 预设风格

使用 `--style` 参数快速应用风格：

- 卡通 - 迪士尼卡通风格
- 油画 - 古典油画风格
- 水墨 - 中国水墨画风格
- 赛博朋克 - 霓虹灯光效果
- 素描 - 铅笔素描风格
- 水彩 - 水彩画风格

## API 端点

- URL: https://api.laozhang.ai/v1/chat/completions
- 认证: Bearer Token
- 文档: https://docs.laozhang.ai
