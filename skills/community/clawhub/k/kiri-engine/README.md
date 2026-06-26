# Kiri Engine Skill

KIRI Engine 3D 扫描重建 API 技能 - 生成 3D 模型和高斯泼溅资产

## 功能特性

- **三种扫描算法**：Photo Scan（照片级）、Featureless Scan（无特征）、3DGS Scan（高斯泼溅）
- **两种输入方式**：视频上传、图片集上传
- **完整工作流**：余额查询 → 参数确认 → 上传 → 状态轮询 → 自动下载
- **资产获取**：自动下载 ZIP 并解压到指定目录

## 支持格式

- **3D 模型**：OBJ / FBX / GLB / USDZ / STL
- **高斯泼溅**：PLY + 3DGS 格式

## 首次配置

### 1. 获取 API Key

1. 注册 KIRI Engine 开发者账号：https://www.kiriengine.com/
2. 在 API Settings 创建 API Key：https://www.kiriengine.com/api-settings
3. 格式：`kiri-<random-string>`

### 2. 存储 API Key

```powershell
# 配置文件路径（Windows）
$configPath = "$env:USERPROFILE\.kiri-engine-config.json"
@{ apiKey = "kiri-你的密钥" } | ConvertTo-Json | Set-Content $configPath -Encoding UTF8
```

### 3. 验证配置

```powershell
cd scripts
.\kiri-engine.ps1 balance
```

## 使用方法

### 检查余额

```powershell
.\kiri-engine.ps1 balance
```

### Photo Scan - 视频上传

```powershell
.\kiri-engine.ps1 photo-video -video "C:\path\to\video.mp4" `
  -modelQuality 1 -textureQuality 1 -fileFormat OBJ `
  -isMask 1 -textureSmoothing 1
```

### Photo Scan - 图片集上传

```powershell
.\kiri-engine.ps1 photo-image -images "C:\path\to\images\*.jpg" `
  -modelQuality 2 -fileFormat GLB -isMask 1 -textureSmoothing 1
```

### Featureless Scan - 视频上传

```powershell
.\kiri-engine.ps1 featureless-video -video "C:\path\to\video.mp4" -fileFormat OBJ
```

### 3DGS Scan - 图片集上传

```powershell
.\kiri-engine.ps1 3dgs-image -images "C:\path\to\images\*.jpg" `
  -isMesh 0 -isMask 0
```

### 查询任务状态

```powershell
.\kiri-engine.ps1 status -serialize "796a6f52457844b4918db3eadd64becc"
```

### 下载模型

```powershell
.\kiri-engine.ps1 download -serialize "796a6f52457844b4918db3eadd64becc" `
  -output "C:\output\dir"
```

## 参数说明

### Photo Scan 参数

| 参数 | 值域 | 默认 | 说明 |
|------|------|------|------|
| modelQuality | 1/2/3 | 1 | 模型精度（1=标准, 2=中, 3=高） |
| textureQuality | 1/2/3 | 1 | 贴图质量 |
| fileFormat | OBJ/FBX/GLB/USDZ/STL | OBJ | 输出格式 |
| isMask | 0/1 | 1 | 自动抠背景 |
| textureSmoothing | 0/1 | 1 | 贴图平滑 |

### 3DGS Scan 参数

| 参数 | 值域 | 默认 | 说明 |
|------|------|------|------|
| isMesh | 0/1 | 0 | 生成网格 |
| isMask | 0/1 | 0 | 自动抠背景 |

### 输入限制

- **视频**：分辨率 ≤ 1920×1080，时长 ≤ 3 分钟
- **图片集**：20~300 张

## 任务时长估算

| 算法 | 输入规模 | 预估时长 |
|------|---------|---------|
| Photo Scan | 视频 / <50 张图 | 10~30 分钟 |
| Photo Scan | >100 张图 / 高质量 | 30~90 分钟 |
| Featureless Scan | 视频 / 图片集 | 15~40 分钟 |
| 3DGS Scan | 视频 | 20~60 分钟 |
| 3DGS Scan | >100 张图 | 40~120 分钟 |

## 重要提示

1. **下载链接有效期 60 分钟** — 任务完成后必须立即下载
2. **服务器保留 3 天** — 超时自动删除，无法恢复
3. **余额管理** — 使用 `balance` 命令检查剩余积分

## API 文档

- Base URL: `https://api.kiriengine.app/api/`
- 官方文档: https://gentlebandit.feishu.cn/wiki/PsHawWV0gi2jePkmRoycwMwXnIc

## License

MIT

## Author

taosiuman
