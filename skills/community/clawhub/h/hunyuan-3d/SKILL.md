---
name: hunyuan-3d
description: 腾讯混元生3D API (OpenAI兼容接口) - 基于混元大模型的3D模型生成
homepage: https://cloud.tencent.com/document/product/1804/126189
metadata: {"clawdbot":{"emoji":"🎲","requires":{"bins":["python"],"env":["HUNYUAN_3D_API_KEY"]},"primaryEnv":"HUNYUAN_3D_API_KEY"}}
---

# Hunyuan 3D - 腾讯混元生3D (OpenAI兼容接口)

基于腾讯混元大模型的3D模型生成服务，使用OpenAI兼容接口，支持文生3D、图生3D。

## ⚠️ 重要说明

**本技能使用OpenAI兼容接口**，与传统的腾讯云API不同：
- 使用 **API Key** 认证（不是SecretId/SecretKey）
- 接口风格与OpenAI一致
- **仅支持专业版**（不支持极速版）

## 🚀 快速开始

### 第一步：开通混元生3D服务

**必须**先在腾讯云控制台开通服务：

1. 访问 [腾讯混元生3D控制台](https://console.cloud.tencent.com/ai3d)
2. 点击「立即开通」或「申请开通」
3. 阅读并同意服务协议
4. 等待服务开通（通常即时生效）

**常见问题**：
- 如果显示"资源不足"，说明服务正在初始化，请等待5-10分钟后再试
- 如果无法开通，可能需要实名认证或联系客服

### 第二步：获取API Key

1. 访问 [混元生3D API Key管理页面](https://console.cloud.tencent.com/ai3d/api-key)
2. 点击「创建API Key」
3. 输入名称（如：hunyuan-3d-key）
4. 复制生成的API Key（格式：`sk-xxxxx`）

**⚠️ 重要**：API Key只显示一次，请妥善保存！

**备用地址**：如果上述链接无法访问，也可在 [混元大模型API Key页面](https://console.cloud.tencent.com/hunyuan/start) 创建

### 第三步：配置环境变量

**⚠️ 重要区别**：
- hunyuan-image 和 hunyuan-video 使用 **腾讯云 SecretId/SecretKey**
- hunyuan-3d 使用 **混元3D专用 API Key**（格式：`sk-xxxxx`）

**需要的环境变量**：
- `HUNYUAN_3D_API_KEY` - 混元3D API Key

**Windows PowerShell**:
```powershell
# 临时设置（当前会话）
$env:HUNYUAN_3D_API_KEY = "sk-xxxxx"

# 永久设置（推荐）
[Environment]::SetEnvironmentVariable("HUNYUAN_3D_API_KEY", "sk-xxxxx", "User")
```

**Linux/Mac**:
```bash
# 临时设置
export HUNYUAN_3D_API_KEY="sk-xxxxx"

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export HUNYUAN_3D_API_KEY="sk-xxxxx"' >> ~/.bashrc
source ~/.bashrc
```

### 第四步：验证配置

```powershell
# 检查环境变量
Write-Host "API Key: $($env:HUNYUAN_3D_API_KEY.Substring(0,15))..."

# 测试生成
python scripts/generate.py --mode text --prompt "一只小狗"
```

**如果报错"资源不足"**：服务正在初始化，等待5-10分钟后重试

```bash
python scripts/generate.py --mode text --prompt "一只小狗"
```

如果看到「任务提交成功」，说明配置正确！

## 功能

- **文生3D**：通过文本描述生成3D模型
- **图生3D**：通过图片生成3D模型
- **多版本支持**：支持模型版本3.0和3.1

## 使用方法

### 基础用法

```bash
# 文生3D
python scripts/generate.py --mode text --prompt "一只可爱的小猪"

# 图生3D
python scripts/generate.py --mode image --image-url "https://example.com/pig.jpg"

# 使用3.1版本模型
python scripts/generate.py --mode text --prompt "小狗" --model 3.1
```

### 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| --mode | 生成模式 | `text`(文生3D), `image`(图生3D) |
| --prompt | 文本描述（文生3D） | "一只可爱的小猪" |
| --image-url | 图片URL（图生3D） | "https://example.com/pig.jpg" |
| --model | 模型版本 | `3.0`(默认), `3.1` |
| --output | 输出目录 | ./models |

### 模型版本说明

| 版本 | 特点 |
|------|------|
| 3.0 | 默认版本，功能完整 |
| 3.1 | 新版本，但LowPoly和Sketch参数不可用 |

### 输入要求

**文生3D**：
- 文本描述：最多1024个utf-8字符
- 支持中文提示词

**图生3D**：
- 图片格式：jpg, png, jpeg, webp
- 图片大小：≤8MB
- 分辨率：128px ~ 5000px（单边）

## 输出

生成的3D模型保存在 `{output}/{date}/{job_id}/` 目录下：
- `model.{format}` - 3D模型文件（obj/glb格式）
- `info.json` - 任务信息

**输出格式**：
- 同时返回 `.glb` 和 `.obj` 格式
- 包含纹理贴图
- 附带预览图

## 接口信息

- **Base URL**: `https://api.ai3d.cloud.tencent.com`
- **提交任务**: `POST /v1/ai3d/submit`
- **查询任务**: `POST /v1/ai3d/query`
- **认证方式**: API Key (Header: `Authorization: sk-xxxxx`)

## 踩坑记录与解决方案

### 1. 服务未开通 - ResourceUnavailable

**错误现象**：
```
ResourceUnavailable.NotExist - 计费状态未知
```

**解决方案**：
1. 访问 https://console.cloud.tencent.com/ai3d
2. 点击「立即开通」
3. 等待5-10分钟让服务初始化
4. 重试

### 2. 资源不足 - ResourceInsufficient

**错误现象**：
```
ResourceInsufficient - 资源不足
```

**解决方案**：
- 服务刚开通时可能出现，等待5-10分钟后重试
- 如果持续出现，联系腾讯云客服

### 3. API Key错误 - Unauthorized

**错误现象**：
```
HTTP 401: Unauthorized
Incorrect API key provided
```

**解决方案**：
1. 确认使用的是 **API Key**（不是SecretId/SecretKey）
2. API Key格式应为 `sk-xxxxx`
3. 在 https://console.cloud.tencent.com/hunyuan/start 创建
4. 检查环境变量是否正确设置

### 4. 响应格式问题

**发现**：OpenAI兼容接口返回格式为：
```json
{
  "Response": {
    "JobId": "xxx",
    "Status": "DONE",
    "ResultFile3Ds": [...]
  }
}
```

**注意**：状态字段是 `Status` 不是 `StatusCode`，成功状态是 `DONE` 不是 `SUCCESS`

### 5. 模型版本3.1的限制

**注意**：选择3.1版本时，LowPoly和Sketch参数不可用

### 6. 图片格式不支持

**错误**：图片上传失败

**解决**：只支持jpg, png, jpeg, webp格式

## 完整示例

```bash
# 示例1：生成小猪3D模型
python scripts/generate.py --mode text --prompt "一只可爱的小猪，粉色，卡通风格"

# 示例2：通过图片生成3D
python scripts/generate.py --mode image --image-url "https://example.com/pig-photo.jpg"

# 示例3：使用3.1版本
python scripts/generate.py --mode text --prompt "小狗" --model 3.1

# 示例4：指定输出目录
python scripts/generate.py --mode text --prompt "小猫" --output ./my_models
```

## 注意事项

1. **异步接口**：分为提交任务和查询任务两个步骤
2. **任务有效期**：24小时
3. **并发限制**：默认3个并发
4. **仅专业版**：OpenAI兼容接口不支持极速版
5. **API Key**：使用单独的API Key，不是腾讯云SecretId/SecretKey
6. **生成时间**：3D生成需要较长时间（1-5分钟），请耐心等待

## 相关链接

- [OpenAI兼容接口文档](https://cloud.tencent.com/document/product/1804/126189)
- [API Key管理](https://console.cloud.tencent.com/hunyuan/start)
- [混元生3D控制台](https://console.cloud.tencent.com/ai3d)
- [提交任务API文档](https://cloud.tencent.com/document/product/1804/123447)

## 调试技巧

如果遇到问题，可以：
1. 检查环境变量：`echo $env:HUNYUAN_3D_API_KEY`
2. 测试API Key是否有效（见上文curl示例）
3. 查看腾讯云控制台的服务状态
4. 使用RequestId联系客服查询
