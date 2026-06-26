---
name: jianying-video-compose
description: 剪映API视频合成自动化。通过剪映代理API完成视频全流程制作，包括草稿创建、素材添加（图片/视频/音频）、文本字幕编辑、特效处理、云渲染导出。适用于需要批量生成视频、自动合成短视频、动态字幕视频等场景。
---

# 剪映API视频合成

## 快速开始

### 0. 上传素材（可选）
如果素材不在OSS上，先上传：
```json
POST https://np-newsmgr-uat.eastmoney.com/video-admin/api/oss/upload
Content-Type: multipart/form-data
```
参数：`file`（文件）、`bucket`（桶名称）、`filename`（文件名）
返回：`ossKey`（可拼接素材地址）

### 1. 创建草稿
```json
POST https://np-newsmgr-uat.eastmoney.com/videomake/api/capcut-proxy/create_draft
{"width": 1080, "height": 1920}
```
返回 `draft_id`

### 2. 添加素材
- **图片**: `add_image` - 背景图、产品图
- **视频**: `add_video` - 视频片段
- **音频**: `add_audio` - 背景音乐、音效
- **文本**: `add_text` / `add_subtitle` - 标题、字幕

### 3. 导出视频
```json
POST https://np-newsmgr-uat.eastmoney.com/videomake/api/capcut-proxy/export_draft
{"draft_id": "xxx", "resolution": "1080P", "framerate": 30}
```
> ⚠️ **注意**: 导出视频是云渲染过程，平均耗时约 **80秒**，请耐心等待返回的 `video_file_url`

## 核心概念

### relative_index 图层顺序
- 值越小越在下层，值越大越在上层
- 背景图用 `relative_index: 0`（最底层）
- 文字/图片/视频用 `relative_index: 1,2,3...`（在上层）

### track_name 轨道概念
- 相同时间段内，同一轨道（相同track_name）后者覆盖前者
- 不同轨道可叠加显示，按relative_index决定上下层

### 素材地址拼接
```
http://np-newsmgr-uat.emapd.com/videomake/api/resource/download/bucket?filename={ossKey}&bucket={bucket}
```
- 默认bucket: `np-vediooss-material`

## 常用配置

### 字幕默认配置
- 字体: 抖音美好体
- 字号: 10
- 位置: transform_y: -0.42（底部居中）
- 颜色: #FFFFFF
- 入场动画: 放大，0.5秒
- 出场动画: 缩小，0.5秒

### 可用字体
抖音美好体、思源黑体、OPPO Sans、挥墨体、文轩体、鸿蒙OS、小米MiSans、站酷快乐体

### 文本动画
放大、缩小、渐显、溶解、打字机、弹性伸缩、弹簧、闪光、旋转飞入、模糊发光、逐字弹跳

## 详细参数

完整API参数说明见 [references/api_reference.md](references/api_reference.md)