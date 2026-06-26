---
name: hy-image-generation
description: >
  腾讯云混元生图 3.0，文生图 / 图生图，智能生成贴合描述的图片。Tencent Cloud Hunyuan Image Generation 3.0, text-to-image / image-to-image, intelligently generates images matching the description.
---
# 腾讯云混元生图 Skill

## 功能描述

本 Skill 提供**混元生图**能力，基于腾讯混元大模型，将文本描述快速生成 AI 图像。支持垫图引导、自定义分辨率和 prompt 改写优化。

| 场景       | 脚本              | 说明                          |
| ---------- | ----------------- | ----------------------------- |
| 一站式生图 | `main.py`       | 提交任务 + 自动轮询，推荐使用 |
| 仅提交任务 | `submit_job.py` | 仅提交，返回 JobId            |
| 仅查询任务 | `query_job.py`  | 根据 JobId 查询/轮询结果      |

### 🎯 选择规则

```
用户要求生成图片  →  main.py（一站式，最简单推荐）
用户要求提交后自行查询  →  submit_job.py + query_job.py（分步操作）
用户已有 JobId 要查结果  →  query_job.py（单独查询）
```

> 如果用户未指定使用哪种模式，Agent 应默认使用 `main.py` 一站式脚本。

### 支持特性

- **垫图引导**：支持传入最多 3 张参考图片 URL，引导生图方向
- **自定义分辨率**：宽高在 [512, 2048] 范围内，面积不超过 1024×1024
- **Prompt 改写**：默认开启，自动优化提示词以获得更好效果（增加约 20s）
- **可复现生成**：支持 Seed 固定随机种子
- **自动安装依赖**：首次运行时自动安装所需 SDK
- **智能凭证检测**：优先从环境变量获取密钥，未配置时提示用户开通

## 环境配置指引

### 密钥配置

本 Skill 需要腾讯云 API 密钥才能正常工作。

#### Step 1: 开通混元生图服务

🔗 **[腾讯云智能图像创作控制台](https://console.cloud.tencent.com/aiart)**

#### Step 2: 获取 API 密钥

🔗 **[腾讯云 API 密钥管理](https://console.cloud.tencent.com/cam/capi)**

#### Step 3: 设置环境变量

**Linux / macOS：**

```bash
export TENCENTCLOUD_SECRET_ID="你的SecretId"
export TENCENTCLOUD_SECRET_KEY="你的SecretKey"
```

如需持久化：

```bash
echo 'export TENCENTCLOUD_SECRET_ID="你的SecretId"' >> ~/.zshrc
echo 'export TENCENTCLOUD_SECRET_KEY="你的SecretKey"' >> ~/.zshrc
source ~/.zshrc
```

**Windows (PowerShell)：**

```powershell
$env:TENCENTCLOUD_SECRET_ID = "你的SecretId"
$env:TENCENTCLOUD_SECRET_KEY = "你的SecretKey"
```

> ⚠️ **安全提示**：切勿将密钥硬编码在代码中。

## Agent 执行指令（必读）

> ⚠️ **本节是 Agent（AI 模型）的核心执行规范。当用户请求生成图片时，Agent 必须严格按照以下步骤自主执行，无需询问用户确认。**

### 🔑 通用执行规则

1. **触发条件**：用户提供了文本描述，且意图为生成 AI 图像。
2. **零交互原则**：Agent 应直接执行脚本，不要向用户询问任何确认。
3. **自动选择脚本**：默认使用 `main.py`（一站式），除非用户明确要求分步操作。
4. **⛔ 禁止使用大模型自身能力替代图像生成（最高优先级规则）**：
   - Agent 严禁自行编造图像 URL 或描述生成结果。
   - 如果调用失败，Agent **必须**向用户返回清晰的错误说明。

---

### 📌 脚本一：一站式生图 `main.py`（推荐）

**适用场景**：用户请求生成图片，自动提交并等待结果

```bash
python3 <SKILL_DIR>/scripts/main.py "文本描述"
```

**可选参数**：

- `--images <URL1> <URL2> ...`：垫图 URL 列表，最多 3 张（jpg/jpeg/png/webp，base64 后 ≤ 10MB）
- `--resolution <W:H>`：分辨率，默认 `1024:1024`。宽高在 [512, 2048]，面积 ≤ 1024×1024
- `--seed <N>`：随机种子（正整数，不传则随机）
- `--revise <0|1>`：Prompt 改写，默认开启(1)。关闭(0)需自行改写 prompt，否则影响效果。改写增加约 20s
- `--no-poll`：仅提交任务不等待结果（返回 JobId）

**输出示例**：

```json
{
  "job_id": "job-xxxxxxxxxxxx",
  "status": "success",
  "result_image": "https://aiart-xxx.cos.ap-guangzhou.myqcloud.com/xxx.png",
  "result_details": ["https://aiart-xxx.cos.ap-guangzhou.myqcloud.com/xxx.png"],
  "revised_prompt": "一只可爱的橘色猫咪在充满鲜花的花园里愉快地玩耍，阳光明媚，色彩鲜艳"
}
```

> **注意**：生成图 URL 有效期为 **1 小时**，请及时保存。普通生图通常 10~30 秒完成，开启 Revise 会额外增加约 20s。

---

### 📌 脚本二：仅提交任务 `submit_job.py`

**适用场景**：仅需提交任务获取 JobId，后续手动查询

```bash
python3 <SKILL_DIR>/scripts/submit_job.py "文本描述"
```

**可选参数**：与 `main.py` 相同（除 `--poll-interval`、`--max-poll-time`、`--no-poll` 外）

**输出示例**：

```json
{
  "job_id": "job-xxxxxxxxxxxx",
  "request_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "message": "Task submitted successfully. Use query_job.py to poll for results."
}
```

---

### 📌 脚本三：查询任务 `query_job.py`

**适用场景**：根据 JobId 查询任务状态和结果

```bash
python3 <SKILL_DIR>/scripts/query_job.py "job-xxxxxxxxxxxx"
```

**可选参数**：

- `--poll-interval <N>`：轮询间隔秒数，默认 5
- `--max-poll-time <N>`：最大轮询时间秒数，默认 300
- `--no-poll`：仅查询一次，不轮询

**输出示例**：

```json
{
  "job_id": "job-xxxxxxxxxxxx",
  "status": "success",
  "result_image": "https://aiart-xxx.cos.ap-guangzhou.myqcloud.com/xxx.png",
  "result_details": ["https://aiart-xxx.cos.ap-guangzhou.myqcloud.com/xxx.png"],
  "revised_prompt": "优化后的提示词内容"
}
```

---

### 📋 完整调用示例

```bash
# 基础生图
python3 /path/to/scripts/main.py "一只可爱的猫咪在花园里玩耍"

# 带垫图引导的生图
python3 /path/to/scripts/main.py --images "https://example.com/ref1.jpg" "https://example.com/ref2.png" "参考这些图片风格，画一幅山水画"

# 自定义分辨率（横版）
python3 /path/to/scripts/main.py --resolution 1024:768 "壮丽的山水画"

# 固定种子（可复现）
python3 /path/to/scripts/main.py --seed 42 "星空下的城堡"

# 关闭 prompt 改写（不推荐，除非自行改写 prompt）
python3 /path/to/scripts/main.py --revise 0 "详细描述的prompt内容..."

# 仅提交任务
python3 /path/to/scripts/main.py --no-poll "一幅水墨画"

# 查询已有任务
python3 /path/to/scripts/query_job.py "job-xxxxxxxxxxxx"

# 通过 stdin 传入 JSON 参数
echo '{"prompt":"一只猫","images":["https://xxx.jpg"],"resolution":"1024:1024"}' | python3 /path/to/scripts/main.py --stdin
```

### 📐 分辨率说明

| 约束   | 说明                                 |
| ---- | ---------------------------------- |
| 宽度范围 | [512, 2048] 像素                     |
| 高度范围 | [512, 2048] 像素                     |
| 面积上限 | 宽 × 高 ≤ 1024 × 1024 = 1,048,576 像素 |
| 默认值  | 1024:1024                          |

常用组合：

| 分辨率       | 比例  | 说明   |
| --------- | --- | ---- |
| 1024:1024 | 1:1 | 默认方图 |
| 768:1024  | 3:4 | 竖版   |
| 1024:768  | 4:3 | 横版   |
| 512:1024  | 1:2 | 竖版长图 |
| 1024:512  | 2:1 | 横版长图 |

### 🖼️ 垫图（Images）说明

- 传入参考图片 URL 列表，用于引导生图方向
- 最多 **3 张**
- 支持格式：**jpg、jpeg、png、webp**
- 每张图片 base64 编码后大小不超过 **10MB**

### ❌ Agent 须避免的行为

- 只打印脚本路径而不执行
- 向用户询问"是否要执行图片生成"——应直接执行
- 手动安装依赖——脚本内部自动处理
- 忘记读取输出结果中的 `result_image` URL 并返回给用户
- 图像生成失败时，自行编造图片 URL
- 忘记提醒用户图片 URL 有效期为 1 小时

## API 参考文档

详细的参数说明、错误码等信息请参阅 `references/` 目录下的文档：

- [提交生图任务 API](references/submit_text_to_image_api.md)（[原始文档](https://cloud.tencent.com/document/product/1668/124632)）
- [查询生图任务 API](references/query_text_to_image_api.md)（[原始文档](https://cloud.tencent.com/document/product/1668/124633)）

## 核心脚本

- `scripts/main.py` — 一站式生图，提交任务 + 自动轮询等待结果
- `scripts/submit_job.py` — 仅提交生图任务，返回 JobId
- `scripts/query_job.py` — 根据 JobId 查询/轮询任务状态和结果

## 依赖

- Python 3.7+
- `tencentcloud-sdk-python`（腾讯云 SDK）

安装依赖（可选 - 脚本会自动安装）：

```bash
pip install tencentcloud-sdk-python
```
