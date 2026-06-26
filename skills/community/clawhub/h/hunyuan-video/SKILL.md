---
name: hunyuan-video
description: 腾讯混元生视频API - 支持文生视频、图生视频、视频风格化
homepage: https://cloud.tencent.com/document/product/1616/107795
metadata: {"clawdbot":{"emoji":"🎬","requires":{"bins":["python"],"packages":["tencentcloud-sdk-python"],"env":["TENCENT_SECRET_ID","TENCENT_SECRET_KEY"]},"primaryEnv":"TENCENT_SECRET_ID"}}
---

# Hunyuan Video - 腾讯混元生视频

基于腾讯混元大模型的视频生成服务，支持文生视频、图生视频、视频风格化三大核心功能。

## 功能

| 功能 | 命令 | 说明 |
|------|------|------|
| 🎬 文生视频 | `text2video` | 文本描述生成视频 |
| 🖼️ 图生视频 | `image2video` | 图片生成视频（支持URL或本地文件） |
| 🎨 视频风格化 | `stylization` | 视频转2D动漫/3D卡通等风格 |

## 前置要求

### 1. 安装Python依赖

```bash
pip install tencentcloud-sdk-python
```

### 2. 开通混元生视频服务

1. 登录 [腾讯混元生视频控制台](https://hunyuan.cloud.tencent.com/#/app/videoModel)
2. 阅读和同意服务协议
3. 单击开通服务

### 3. 配置腾讯云密钥

**需要的环境变量**：
- `TENCENT_SECRET_ID` - 腾讯云SecretId
- `TENCENT_SECRET_KEY` - 腾讯云SecretKey

```powershell
# Windows PowerShell - 永久设置
[Environment]::SetEnvironmentVariable("TENCENT_SECRET_ID", "your-secret-id", "User")
[Environment]::SetEnvironmentVariable("TENCENT_SECRET_KEY", "your-secret-key", "User")

# 或临时设置（当前会话）
$env:TENCENT_SECRET_ID = "your-secret-id"
$env:TENCENT_SECRET_KEY = "your-secret-key"
```

**获取密钥步骤**：
1. 访问 https://console.cloud.tencent.com/cam/capi
2. 点击「新建密钥」
3. 复制 SecretId 和 SecretKey
4. **⚠️ 注意**：SecretKey 只显示一次，请妥善保存

### 4. 验证配置

```powershell
# 检查环境变量
Write-Host "SecretId: $env:TENCENT_SECRET_ID"
Write-Host "SecretKey: $($env:TENCENT_SECRET_KEY.Substring(0,10))..."

# 测试生成
python scripts/generate.py text2video "一只小猫"
```

## 使用方法

### 1. 文生视频

```bash
python scripts/generate.py text2video "一只可爱的小猪在草地上奔跑"

# 指定分辨率
python scripts/generate.py text2video "小猪" --resolution 1080p
```

**参数**：
- `prompt`: 文本描述（必填）
- `--resolution`: 分辨率（720p, 1080p，默认720p）

### 2. 图生视频

```bash
# 使用图片URL
python scripts/generate.py image2video "https://example.com/pig.jpg"

# 使用本地图片
python scripts/generate.py image2video "./pig.png"

# 添加辅助描述
python scripts/generate.py image2video "./pig.png" --prompt "小猪在奔跑"
```

**参数**：
- `image`: 图片URL或本地路径（必填）
- `--prompt`: 辅助描述（可选）

**支持格式**：
- URL: `http://` 或 `https://` 开头
- 本地文件: 相对路径或绝对路径

### 3. 视频风格化

```bash
# 转为2D动漫风格
python scripts/generate.py stylization "https://example.com/video.mp4" --style 2d_anime

# 转为3D卡通风格
python scripts/generate.py stylization "https://example.com/video.mp4" --style 3d_cartoon
```

**风格选项**：
- `2d_anime`: 2D动漫
- `3d_cartoon`: 3D卡通
- `3d_china`: 3D国潮
- `pixel_art`: 像素风

**输入视频要求**：
- 格式：mp4、mov
- 时长：1～60秒
- 分辨率：540P~2056P
- 大小：不超过200M
- FPS：15～60fps

## 输出

生成的视频保存在 `{output}/{date}/{job_id}/` 目录下：
- `{command}_result.mp4` - 生成的视频
- `info.json` - 任务信息

## 经验总结与踩坑记录

### 1. 状态码陷阱 ⚠️

**问题**：不同接口返回的状态字段和成功值不一致！

| 接口 | 状态字段 | 成功值 |
|------|----------|--------|
| 文生视频 | `Status` | `DONE` |
| 图生视频 | `Status` | `DONE` |
| 视频风格化 | `JobStatusCode` | `4` 或 `5`+`ResultDetails:Success` |

**解决方案**：
```python
# 统一处理多种状态
success_statuses = ["JobSuccess", "SUCCESS", "DONE"]
if status in success_statuses:
    print("✅ 生成完成!")
```

### 2. 图生视频参数类型陷阱 ⚠️

**问题**：`Image` 参数不是字符串，而是对象类型！

**错误代码**：
```python
# ❌ 错误
req.Image = image_url  # 直接赋值字符串

# ✅ 正确
image = models.Image()
image.Url = image_url    # 或 image.Base64 = base64_data
req.Image = image
```

**经验**：SDK中对象类型的参数需要创建对应的对象实例。

### 3. 本地文件支持 💡

**实现方式**：读取本地文件转为base64编码

```python
if image_input.startswith('http'):
    image.Url = image_input
elif os.path.exists(image_input):
    with open(image_input, 'rb') as f:
        image.Base64 = base64.b64encode(f.read()).decode('utf-8')
```

**好处**：用户可以直接使用本地图片，无需先上传。

### 4. 视频生成时间较长 ⏱️

**观察**：
- 文生视频：约1-3分钟
- 图生视频：约1-3分钟
- 视频风格化：约2-5分钟

**建议**：设置合理的超时时间（默认600秒），并显示进度点让用户知道正在处理。

### 5. 视频风格化状态码特殊处理 ⚠️

**问题**：风格化接口返回 `JobStatusCode: 5` 但实际可能是成功！

**原因**：`StatusCode: 5` + `ResultDetails: ["Success"]` = 实际成功

**解决方案**：
```python
if status == "4" or (status == "5" and result.get("ResultDetails") == ["Success"]):
    print("✅ 实际生成成功！")
```

### 6. SSL证书验证 🔒

**问题**：下载视频时可能遇到SSL验证错误

**解决方案**：临时禁用SSL验证（仅用于下载）
```python
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
```

### 7. 并发限制 ⚠️

**限制**：
- 视频风格化：默认1个并发
- 其他功能：默认3个并发

**建议**：顺序执行，等待前一个任务完成再提交下一个。

### 8. 任务有效期 ⏰

**注意**：任务结果URL有效期为48小时，请及时下载。

## 完整示例

```bash
# 示例1：文生视频
python scripts/generate.py text2video "一只可爱的小猪在草地上奔跑，阳光明媚"

# 示例2：图生视频（本地图片）
python scripts/generate.py image2video "./my_pig.png" --prompt "小猪在奔跑"

# 示例3：视频风格化
python scripts/generate.py stylization "https://example.com/video.mp4" --style 2d_anime
```

## 注意事项

1. **异步接口**：所有功能都是异步的，需要轮询等待任务完成
2. **地域限制**：仅支持 `ap-guangzhou`
3. **网络要求**：输入URL需要可公开访问（图生视频支持本地文件）
4. **任务有效期**：48小时
5. **输出格式**：默认生成MP4格式

## 调试技巧

如果遇到问题：
1. 检查环境变量：`echo $env:TENCENT_SECRET_ID`
2. 确认服务已开通：访问控制台查看
3. 查看详细错误：使用 `RequestId` 联系客服
4. 测试API连接：先用简单prompt测试

## 相关链接

- [API概览](https://cloud.tencent.com/document/product/1616/107795)
- [混元生视频控制台](https://hunyuan.cloud.tencent.com/#/app/videoModel)
- [腾讯云密钥管理](https://console.cloud.tencent.com/cam/capi)

---

**开发经验**：在实现过程中发现SDK参数类型和文档描述可能存在差异，建议通过实际测试验证参数格式。图生视频的`Image`参数是一个典型的对象类型参数陷阱，需要特别注意。
