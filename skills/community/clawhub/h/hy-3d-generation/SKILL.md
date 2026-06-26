---
name: hy-3d-generation
description: >
  输入文字或图片，通过混元生3D 3.0、3.1 模型，生成更高精度以及更高质量的3D 模型，支持文生3D，图生3D，多视图生3D，单几何生成（白模），草图生3D，智能拓扑生3D功能。
---

# 腾讯云混元生3D Skill

## 功能描述

本 Skill 提供**混元生3D**能力，基于腾讯混元大模型，将文本描述或图片智能生成 3D 模型。支持多视角图片输入、PBR 材质、自定义面数、多种输出格式。

| 场景 | 脚本 | 说明 |
|------|------|------|
| 一站式生成 | `main.py` | 提交任务 + 自动轮询，推荐使用 |
| 仅提交任务 | `submit_job.py` | 仅提交，返回 JobId |
| 仅查询任务 | `query_job.py` | 根据 JobId 查询/轮询结果 |

### 🎯 选择规则

```
用户要求生成3D模型  →  main.py（一站式，最简单推荐）
用户要求提交后自行查询  →  submit_job.py + query_job.py（分步操作）
用户已有 JobId 要查结果  →  query_job.py（单独查询）
```

> 如果用户未指定使用哪种模式，Agent 应默认使用 `main.py` 一站式脚本。

### 支持特性

- **文生3D**：支持文本描述生成 3D 模型（最多 1024 字符）
- **图生3D**：支持输入图片 URL 或 Base64 生成 3D 模型
- **多视角图片**：支持 left/right/back/top/bottom/left_front/right_front 多视角输入
- **PBR 材质**：支持开启 PBR 材质生成
- **自定义面数**：支持 10000-1500000 面数范围
- **多种生成类型**：Normal（带纹理）、LowPoly（智能拓扑）、Geometry（白模）、Sketch（草图生成）
- **多种输出格式**：默认 obj+glb，可选 STL、USDZ、FBX
- **模型版本选择**：支持 3.0 和 3.1 版本
- **自动安装依赖**：首次运行时自动安装所需 SDK
- **智能凭证检测**：优先从环境变量获取密钥，未配置时提示用户开通

## 环境配置指引

### 密钥配置

本 Skill 需要腾讯云 API 密钥才能正常工作。

#### Step 1: 开通混元3D服务

🔗 **[腾讯云3D视觉创作控制台](https://console.cloud.tencent.com/ai3d)**

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

> ⚠️ **本节是 Agent（AI 模型）的核心执行规范。当用户请求生成 3D 模型时，Agent 必须严格按照以下步骤自主执行，无需询问用户确认。**

### 🔑 通用执行规则

1. **触发条件**：用户提供了文本描述或图片，且意图为生成 3D 模型。
2. **零交互原则**：Agent 应直接执行脚本，不要向用户询问任何确认。
3. **自动选择脚本**：默认使用 `main.py`（一站式），除非用户明确要求分步操作。
4. **⛔ 禁止使用大模型自身能力替代 3D 生成（最高优先级规则）**：
   - Agent 严禁自行编造 3D 文件 URL 或描述生成结果。
   - 如果调用失败，Agent **必须**向用户返回清晰的错误说明。

---

### 📌 脚本一：一站式生成 `main.py`（推荐）

**适用场景**：用户请求生成 3D 模型，自动提交并等待结果

```bash
# 文生3D
python3 <SKILL_DIR>/scripts/main.py --prompt "文本描述"

# 图生3D
python3 <SKILL_DIR>/scripts/main.py --image-url "https://example.com/image.jpg"
```

**可选参数**：
- `--prompt <TEXT>`：文本描述，中文推荐，最多 1024 字符（与 image-url/image-base64 二选一）
- `--image-url <URL>`：输入图片 URL（与 prompt 二选一）
- `--image-base64 <BASE64>`：输入图片 Base64 数据（与 prompt 二选一）
- `--multi-view <JSON>`：多视角图片 JSON，如 `'[{"ViewType":"back","ViewImageUrl":"https://..."}]'`
- `--model <VERSION>`：模型版本，默认 `3.0`，可选 `3.0` / `3.1`
- `--enable-pbr`：开启 PBR 材质生成
- `--face-count <N>`：面数，默认 500000，范围 10000-1500000
- `--generate-type <TYPE>`：生成类型：Normal / LowPoly / Geometry / Sketch
- `--polygon-type <TYPE>`：多边形类型（仅 LowPoly）：triangle / quadrilateral
- `--result-format <FMT>`：输出格式：STL / USDZ / FBX（默认 obj+glb）
- `--no-poll`：仅提交任务不等待结果（返回 JobId）

**输出示例**：
```json
{
  "job_id": "job-xxxxxxxxxxxx",
  "status": "success",
  "result_files": [
    {
      "type": "glb",
      "url": "https://ai3d-xxx.cos.ap-guangzhou.myqcloud.com/xxx.glb",
      "preview_image_url": "https://ai3d-xxx.cos.ap-guangzhou.myqcloud.com/xxx.png"
    },
    {
      "type": "obj",
      "url": "https://ai3d-xxx.cos.ap-guangzhou.myqcloud.com/xxx.obj"
    }
  ]
}
```

> **注意**：生成的文件 URL 有效期为 **24 小时**，请及时保存。3D 生成通常需要 1~5 分钟。

---

### 📌 脚本二：仅提交任务 `submit_job.py`

**适用场景**：仅需提交任务获取 JobId，后续手动查询

```bash
python3 <SKILL_DIR>/scripts/submit_job.py --prompt "文本描述"
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
- `--poll-interval <N>`：轮询间隔秒数，默认 10
- `--max-poll-time <N>`：最大轮询时间秒数，默认 600（10min）
- `--no-poll`：仅查询一次，不轮询

**输出示例**：
```json
{
  "job_id": "job-xxxxxxxxxxxx",
  "status": "success",
  "result_files": [
    {
      "type": "glb",
      "url": "https://ai3d-xxx.cos.ap-guangzhou.myqcloud.com/xxx.glb",
      "preview_image_url": "https://ai3d-xxx.cos.ap-guangzhou.myqcloud.com/xxx.png"
    }
  ]
}
```

---

### 📋 完整调用示例

```bash
# 文生3D（基础）
python3 /path/to/scripts/main.py --prompt "一只可爱的卡通猫咪"

# 图生3D
python3 /path/to/scripts/main.py --image-url "https://example.com/cat.jpg"

# 使用 3.1 版本 + PBR 材质
python3 /path/to/scripts/main.py --prompt "一个精致的茶壶" --model 3.1 --enable-pbr

# 自定义面数
python3 /path/to/scripts/main.py --prompt "一辆跑车" --face-count 300000

# LowPoly 模式
python3 /path/to/scripts/main.py --prompt "一棵树" --generate-type LowPoly --polygon-type quadrilateral

# 白模（Geometry）
python3 /path/to/scripts/main.py --prompt "一个机器人" --generate-type Geometry

# 草图生成
python3 /path/to/scripts/main.py --image-url "https://example.com/sketch.png" --generate-type Sketch --prompt "一把椅子"

# 指定输出格式为 FBX
python3 /path/to/scripts/main.py --prompt "一只恐龙" --result-format FBX

# 多视角输入
python3 /path/to/scripts/main.py --image-url "https://example.com/front.jpg" --multi-view '[{"ViewType":"back","ViewImageUrl":"https://example.com/back.jpg"},{"ViewType":"left","ViewImageUrl":"https://example.com/left.jpg"}]'

# 仅提交任务
python3 /path/to/scripts/main.py --prompt "一座城堡" --no-poll

# 查询已有任务
python3 /path/to/scripts/query_job.py "job-xxxxxxxxxxxx"

# 通过 stdin 传入 JSON 参数
echo '{"prompt":"一只猫"}' | python3 /path/to/scripts/main.py --stdin
```

### 📐 SubmitHunyuanTo3DProJob 参数说明

| 参数 | 类型 | 必选 | 说明 |
|------|------|------|------|
| Model | String | 否 | 模型版本，默认 3.0，可选 3.0/3.1。3.1 版本不支持 LowPoly |
| Prompt | String | 三选一 | 文生3D描述，中文推荐，最多 1024 字符 |
| ImageUrl | String | 三选一 | 输入图 URL，分辨率 128~5000，大小 ≤ 8MB |
| ImageBase64 | String | 三选一 | 输入图 Base64，分辨率 128~5000，大小 ≤ 6MB |
| MultiViewImages | Array | 否 | 多视角图片，视角：left/right/back/top/bottom/left_front/right_front |
| EnablePBR | Boolean | 否 | 开启 PBR 材质，默认 false |
| FaceCount | Integer | 否 | 面数，默认 500000，范围 10000~1500000 |
| GenerateType | String | 否 | Normal/LowPoly/Geometry/Sketch，默认 Normal |
| PolygonType | String | 否 | 仅 LowPoly：triangle/quadrilateral，默认 triangle |
| ResultFormat | String | 否 | STL/USDZ/FBX，默认返回 obj+glb |

### 📐 QueryHunyuanTo3DProJob 响应说明

| 字段 | 类型 | 说明 |
|------|------|------|
| Status | String | WAIT：等待中，RUN：执行中，FAIL：失败，DONE：成功 |
| ErrorCode | String | 错误码 |
| ErrorMessage | String | 错误信息 |
| ResultFile3Ds | Array of File3D | 生成的 3D 文件数组 |

**File3D 结构**：

| 字段 | 类型 | 说明 |
|------|------|------|
| Type | String | 文件格式（如 glb、obj） |
| Url | String | 文件 URL，有效期 24 小时 |
| PreviewImageUrl | String | 预览图 URL |

### ❌ Agent 须避免的行为

- 只打印脚本路径而不执行
- 向用户询问"是否要执行 3D 生成"——应直接执行
- 手动安装依赖——脚本内部自动处理
- 忘记读取输出结果中的 `result_files` URL 并返回给用户
- 3D 生成失败时，自行编造文件 URL
- 忘记提醒用户文件 URL 有效期为 24 小时

## API 参考

- SDK 模块：`tencentcloud.ai3d.v20250513`
- 提交任务：`SubmitHunyuanTo3DProJob`
- 查询任务：`QueryHunyuanTo3DProJob`
- Endpoint：`ai3d.tencentcloudapi.com`

## 核心脚本

- `scripts/main.py` — 一站式生成，提交任务 + 自动轮询等待结果
- `scripts/submit_job.py` — 仅提交任务，返回 JobId
- `scripts/query_job.py` — 根据 JobId 查询/轮询任务状态和结果

## 依赖

- Python 3.7+
- `tencentcloud-sdk-python`（腾讯云 SDK，需包含 ai3d 模块）

安装依赖（可选 - 脚本会自动安装）：
```bash
pip install tencentcloud-sdk-python
```
