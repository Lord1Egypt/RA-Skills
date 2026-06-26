---
name: MiVisionForge-SVOR
description: |-
  Video Object Remove with SVOR(stable video object removal). 
version: 1.0.4
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
requires:
  env:
    - SVOR_API_KEY
  bins:
    - python3
    - ffmpeg
primaryEnv: SVOR_API_KEY
---

# 视频目标分割与消除 (CLI 版)

基于 SVOR(stable video object removal) 实现视频目标分割和消除，通过命令行脚本 `video_remove.py` 执行。
支持最长3s视频的指定目标消除

## 基本信息

| 项 | 值 |
|---|---|
| 服务运营商 | 小米Tools团队 |
| 服务域名 | https://mipixgen-pre.ai.mioffice.cn |
| 开源仓库 | https://github.com/xiaomi-research/svor |
| API Key | 环境变量 `SVOR_API_KEY`（必需，可在开源仓库页面获取） |
| 脚本路径 | `scripts/video_remove.py` |


## 前置依赖

```bash
python --version      # Python 3.x
pip show requests     # requests 模块
ffmpeg -version       # ffmpeg 用于视频处理
```

## 工作流程

### 推荐两步法（复杂场景）

Step 1: 分割 → 获取 VLM 推荐 → 人工分析目标 ID
Step 2: 使用目标 ID → mask 转换 → 合并 → 消除

### 一步法（简单场景，文本提示有效时）

直接指定 classes + targets → 分割 → mask 转换 → 消除


## 命令行用法

### 1. 仅分割（获取 VLM 推荐）

```bash
python scripts/video_remove.py --video "path/to/video.mp4" --segment --classes "label:text:remove_prompt"
```

输出 VLM 推荐的目标 ID 和边界框，据此决定哪些 ID 需要消除。

### 2. 跑消除（基于 VLM 推荐）

```bash
python scripts/video_remove.py --video "path/to/video.mp4" --skip-segment --targets "label:1,2,3"
```

### 3. 一步完成

```bash
python scripts/video_remove.py --video "path/to/video.mp4" --classes "sign:sign:remove the sign" --targets "sign:2,3"
```

### 4. 多类目标消除

```bash
# 第一步：分割两类目标
python scripts/video_remove.py --video "path/to/video.mp4" --segment \
  --classes "person:person:remove pedestrians" "car:car:remove cars"

# 第二步：根据 VLM 推荐填写 targets
python scripts/video_remove.py --video "path/to/video.mp4" --skip-segment \
  --targets "person:1,3,4" "car:2"
```

### 5. 指定标注帧

```bash
python scripts/video_remove.py --video "path/to/video.mp4" --frame 16 --segment \
  --classes "girl:girl in red:remove the girl in red"
```

### 6. 框标注（文本提示无效时）

```bash
python scripts/video_remove.py --video "path/to/video.mp4" --segment \
  --classes "obj:cup:remove the cup" --boxes "obj:0.15,0.7,0.3,0.25"
```

### 7. 点标注

```bash
python scripts/video_remove.py --video "path/to/video.mp4" --segment \
  --classes "obj:cup:remove the cup" --points "obj:0.25,0.75"
```

## 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `--video` | 输入视频路径（必填） | `"D:\video.mp4"` |
| `--classes` | 分割类别 `label:text:prompt` | `"person:person:remove people"` |
| `--targets` | 目标 ID `label:1,2,3` | `"person:1,3,4"` |
| `--boxes` | 框标注 `label:x,y,w,h`（归一化 0~1） | `"obj:0.15,0.7,0.3,0.25"` |
| `--points` | 点标注 `label:x,y`（归一化 0~1） | `"obj:0.25,0.75"` |
| `--frame` | 标注帧序号（0-based），默认 0 | `--frame 16` |
| `--segment` | 仅分割，打印 VLM 推荐后退出 | |
| `--skip-segment` | 跳过分割，使用缓存 mask | |
| `--tmp-dir` | 临时目录（默认 `./temp/`） | `"C:\temp"` |

## VLM 推荐分析规则

SAM3 返回的 `suggest_obj` 包含 VLM 对目标的分析。**不要用正则表达式解析**，应人工分析：

- VLM 会说明哪些 obj_id 符合消除指令、哪些不符合
- 关注"需要保留"和"需要消除"的区分
- 结合 `object_boxes` 的坐标辅助判断位置

**示例 VLM 输出分析：**
```
VLM: 符合用户指令的有 obj_id 1、3、4（背景行人），需消除；
     obj_id 2 是前景人物，不需要消除。
→ --targets "person:1,3,4"
```

## 标注方式选择

| 场景 | 推荐方式 | 原因 |
|------|----------|------|
| 常见物体（人、车、动物） | 文本提示 | 简单直接 |
| 文本提示无法识别 | 框标注 | 比点标注更稳定 |
| 需要精确位置 | 点标注 | 定位精确 |
| 指定帧的目标 | `--frame` + 文本/框 | 定位到特定帧 |

## 多类目标消除流程

SAM3 接口一次仅能分割一类目标，多类消除需要：

1. 分别对每类目标调用 SAM3 分割
2. 分析 VLM 推荐，确定每类的 obj_id
3. 分别转换每类 mask（目标 ID → 255）
4. 用 `blend=all_mode=lighten` 合并所有 mask
5. 用合并后的 mask 调用 MiEraser 消除


## 注意事项

1. **上传限制**：网关限制约 1000KB，脚本自动压缩
2. **坐标系统**：`points`/`bounding_boxes` 用归一化坐标（0~1），`object_boxes` 用绝对像素坐标
3. **mask 格式**：消除区域像素值必须为 255，背景为 0
4. **frame_index**：选择目标清晰可见、无遮挡的帧
5. **结果链接**：预签名 URL，7 天过期
6. **中文路径**：ffmpeg 不支持中文路径，脚本自动拷贝到临时目录处理

## 错误码

| 状态码 | 含义 | 处理 |
|--------|------|------|
| 400 | 请求参数错误 | 检查参数格式 |
| 401 | 未提供 API Key | 检查 Headers |
| 403 | API Key 无效 | 检查 Key |
| 413 | 请求体过大 | 降低视频分辨率 |
| 429 | 超出速率限制 | 等待后重试 |
| 502 | 上游服务连接失败 | 重试 |
| 504 | 上游服务超时 | 重试或降低分辨率 |

## ⚠️ 隐私与安全声明

- **服务运营商**：本技能的云端处理服务由小米Tools团队运营，服务端点为 `https://mipixgen-pre.ai.mioffice.cn`，与开源仓库 [xiaomi-research/svor](https://github.com/xiaomi-research/svor) 对应
- **数据上传**：本技能会将完整视频文件上传至上述远程服务进行处理。请勿上传包含敏感个人信息或可识别身份信息的视频内容
- **数据处理**：上传的视频仅用于目标分割和消除处理，处理完成后结果通过预签名 URL 返回（7 天过期）。具体数据保留和访问控制政策请参阅小米Tools团队的服务条款
- **API 密钥安全**：所需 `SVOR_API_KEY` 仅用于向该服务认证。请勿在共享环境中设置该密钥，也请勿将其粘贴到公共日志或版本控制中
- **使用建议**：首次使用前，建议在隔离环境中使用小型、不涉及敏感内容的测试视频验证功能

