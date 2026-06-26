---
name: grsai-nano-banana
description: 使用 grsai 平台的 nano-banana 模型生成图片（支持文生图、图生图）
homepage: https://grsai.ai/
metadata:
  {
    "openclaw":
      {
        "emoji": "🎨",
        "requires": { "bins": ["uv", "curl"] },
        "primaryEnv": "G RSAI_API_KEY",
      }
  }
---

# 🎨 grsai nano-banana 生图技能

使用 grsai 平台的 nano-banana 系列模型生成高质量图片，支持文生图和图生图。

---

## 📋 使用前准备

### 1. 获取 grsai API Key

1. 访问 https://grsai.ai/zh/dashboard
2. 注册/登录账户
3. 进入 **API Key 管理** 页面
4. 创建新的 API Key
5. **充值** - 确保账户有足够 credits（生图消耗积分）

### 2. 配置 API Key

**方式一：openclaw.json 配置（推荐）**
```json
{
  "skills": {
    "entries": {
      "grsai-nano-banana": {
        "apiKey": "sk-your-api-key-here"
      }
    }
  }
}
```

**方式二：环境变量**
```bash
export G RSAI_API_KEY="sk-your-api-key-here"
```

---

## 🚀 使用方法

### 方式一：自然语言对话（推荐）

直接告诉助理你的生图需求，助理会引导你确认方案：

```
用户：帮我生成一张可爱柴犬的头像
助理：好的，使用 nano-banana 生图需要确认以下信息：
      【必填】模型、提示词
      【选填】尺寸、比例、参考图
      ...
```

### 方式二：命令行调用

**文生图：**
```bash
uv run ~/.openclaw/workspace/skills/grsai-nano-banana/generate.py \
  --prompt "手绘版可爱柴犬头像" \
  --model "nano-banana-pro" \
  --resolution "1K" \
  --aspect-ratio "1:1" \
  --api-key "sk-xxx"
```

**图生图：**
```bash
uv run ~/.openclaw/workspace/skills/grsai-nano-banana/generate.py \
  --prompt "把这张图变成油画风格" \
  --input-image "https://example.com/photo.png" \
  --model "nano-banana-pro" \
  --api-key "sk-xxx"
```

---

## 📐 参数说明

### 必填参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--prompt` | 提示词，清晰描述想要的内容 | `"一只可爱的猫咪在草地上"` |
| `--api-key` | grsai API Key | `"sk-xxx"` |

### 选填参数

| 参数 | 默认值 | 选项 | 说明 |
|------|--------|------|------|
| `--model` | `nano-banana-pro` | `nano-banana-pro`<br>`nano-banana-fast`<br>`nano-banana-2`<br>`nano-banana-pro-vip` | 不同模型支持不同分辨率 |
| `--resolution` | `1K` | `1K` / `2K` / `4K` | 分辨率越高，生成时间越长 |
| `--aspect-ratio` | `auto` | `auto` / `1:1` / `16:9` / `9:16`<br>`4:3` / `3:4` / `3:2` / `2:3`<br>`5:4` / `4:5` / `21:9` | 输出图片比例 |
| `--input-image` | - | 图片 URL | 参考图（图生图时使用） |
| `--filename` | 自动生成 | 自定义文件名 | 输出文件名 |
| `--output-dir` | `./generated` | 目录路径 | 输出目录（默认相对于当前目录） |

---

## ⏱️ 生成时间

| 模型 | 1K | 2K | 4K |
|------|-----|-----|-----|
| nano-banana-fast | ~2 分钟 | ~3 分钟 | - |
| nano-banana-pro | ~5-8 分钟 | ~8-12 分钟 | ~15 分钟 |

**注意：**
- 实际时间取决于 grsai 服务器负载
- 高峰时段可能需要更长时间
- 脚本会自动轮询，无需手动等待

---

## 📁 输出文件

**保存路径：** `./generated/`（可自定义）

**命名规则：** `yyyymmdd_模型_描述.png`

**示例：**
- `20260304_pro_手绘版可爱柴犬头像.png`
- `20260304_fast_sunset_beach.png`

**自定义输出目录：**
```bash
uv run generate.py --prompt "xxx" --output-dir "/your/custom/path" --api-key "sk-xxx"
```

---

## ⚠️ 常见问题与踩坑记录

### 1. API 返回 "apikey credits not enough"

**原因：** 账户余额不足

**解决：**
1. 登录 grsai 后台
2. 检查当前 API Key 对应的账户
3. 充值 credits

---

### 2. 生成超时 "gemini timeout... Please try again later"

**原因：** grsai 后端生成时间较长

**解决：**
- 使用异步轮询模式（脚本默认）
- 等待 5 分钟后开始轮询
- 最多轮询 3 次，间隔 1 分钟
- 如仍失败，稍后重试

---

### 3. 内容违规

**原因：** 提示词包含敏感内容

**解决：**
- 调整提示词，避免敏感词汇
- 使用更委婉的描述方式

---

### 4. 模型不支持的分辨率

**原因：** 某些模型有分辨率限制

**限制说明：**
- `nano-banana-pro-vip`：仅支持 1K、2K
- `nano-banana-pro-4k-vip`：仅支持 4K

**解决：** 选择正确的模型或调整分辨率

---

### 5. 接口返回空响应

**原因：** 请求格式不正确

**正确格式：**
```json
{
  "model": "nano-banana-pro",
  "prompt": "xxx",
  "imageSize": "1K",
  "aspectRatio": "auto",
  "webHook": "-1",
  "shutProgress": false
}
```

**注意：** `webHook: "-1"` 是关键，让接口立即返回 task_id

---

### 6. 查询结果时参数错误

**错误：** 使用 `task_id` 参数

**正确：** 使用 `id` 参数
```json
{"id": "1-xxxxx"}
```

---

## 🔧 技术细节

### API 端点

| 接口 | URL | 方法 |
|------|-----|------|
| 提交任务 | `/v1/draw/nano-banana` | POST |
| 查询结果 | `/v1/draw/result` | POST |

### 请求格式

**提交任务：**
```bash
curl -X POST "https://grsai.dakka.com.cn/v1/draw/nano-banana" \
  -H "Authorization: Bearer sk-xxx" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nano-banana-pro",
    "prompt": "手绘版可爱柴犬头像",
    "imageSize": "1K",
    "aspectRatio": "1:1",
    "webHook": "-1",
    "shutProgress": false
  }'
```

**查询结果：**
```bash
curl -X POST "https://grsai.dakka.com.cn/v1/draw/result" \
  -H "Authorization: Bearer sk-xxx" \
  -H "Content-Type: application/json" \
  -d '{"id": "1-b834c0d4-dda7-4ab2-9ce6-378ea325ab3a"}'
```

### 响应格式

**提交成功：**
```json
{
  "code": 0,
  "data": {
    "id": "1-b834c0d4-dda7-4ab2-9ce6-378ea325ab3a"
  },
  "msg": "success"
}
```

**查询成功：**
```json
{
  "code": 0,
  "data": {
    "id": "1-xxxxx",
    "status": "succeeded",
    "progress": 100,
    "results": [{
      "url": "https://file3.aitohumanize.com/file/xxx.png"
    }]
  },
  "msg": "success"
}
```

---

## 📝 更新日志

- **2026-03-04** - 初始版本
  - 支持文生图、图生图
  - 异步轮询模式
  - 自动保存至 `./generated/` 目录
  - 智能文件命名

---

## 🔗 相关链接

- grsai 官网：https://grsai.ai/
- grsai 后台：https://grsai.ai/zh/dashboard
- 文档：https://grsai.ai/zh/dashboard/documents/nano-banana
