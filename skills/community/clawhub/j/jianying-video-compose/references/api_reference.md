# 剪映API详细参数参考

## 基础信息

- **API基础URL**: `https://np-newsmgr-uat.eastmoney.com/videomake/api/capcut-proxy`
- **认证方式**: 无需apikey，直接调用

---

## 零、素材上传（OSS）

### upload_material - 上传素材到OSS

> ⚠️ 此接口为 `multipart/form-data` 表单上传，不同于其他JSON接口

```http
POST https://np-newsmgr-uat.eastmoney.com/video-admin/api/oss/upload
Content-Type: multipart/form-data
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | file | 是 | 上传的文件（图片/视频/音频） |
| bucket | string | 是 | OSS桶名称，如 `np-vediooss-material` |
| filename | string | 是 | 文件名称（建议带扩展名） |

**返回示例**:
```json
{
  "code": 0,
  "data": {
    "ossKey": "深色质感背景图3.png"
  },
  "message": "success"
}
```

**上传后素材地址拼接**:
```
http://np-newsmgr-uat.emapd.com/videomake/api/resource/download/bucket?filename={ossKey}&bucket={bucket}
```

---

## 一、草稿管理

### create_draft - 创建草稿

```json
POST /create_draft
{"width": 1080, "height": 1920}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| width | int | 否 | 视频宽度，默认1080 |
| height | int | 否 | 视频高度，默认1920 |

**返回**: `{draft_id, draft_url}`

### save_draft - 生成草稿下载链接

```json
POST /save_draft
{"draft_id": "dfd_xxx"}
```

### get_duration - 获取素材时长

```json
POST /get_duration
{"url": "https://..."}
```

**返回**: `{duration, video_url}`

---

## 二、文本处理

### add_text - 添加文字

```json
POST /add_text
{
  "text": "文字内容",
  "start": 0,
  "end": 5,
  "draft_id": "dfd_xxx",
  "font": "抖音美好体",
  "font_color": "#FFFFFF",
  "font_size": 10,
  "font_alpha": 1.0,
  "bold": false,
  "italic": false,
  "transform_x": 0.0,
  "transform_y": -0.42,
  "track_name": "text_1",
  "vertical": false,
  "border_color": "#000000",
  "border_width": 0,
  "background_color": "#000000",
  "background_style": 0,
  "background_alpha": 0.0,
  "shadow_enabled": false,
  "intro_animation": "放大",
  "intro_duration": 0.5,
  "outro_animation": "缩小",
  "outro_duration": 0.5,
  "width": 1080,
  "height": 1920
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| text | string | 是 | 文本内容 |
| start | float | 是 | 起始时间（秒） |
| end | float | 是 | 结束时间（秒） |
| draft_id | string | 否 | 草稿ID |
| font | string | 否 | 字体名称 |
| font_color | string | 否 | 字体颜色十六进制 |
| font_size | float | 否 | 字体大小，默认8.0（字幕用10） |
| font_alpha | float | 否 | 字体透明度0-1 |
| bold | bool | 否 | 加粗 |
| italic | bool | 否 | 斜体 |
| transform_x | float | 否 | X轴偏移（0为中心） |
| transform_y | float | 否 | Y轴偏移（0为中心，正上负下） |
| track_name | string | 否 | 轨道名称 |
| vertical | bool | 否 | 是否垂直显示 |
| intro_animation | string | 否 | 入场动画 |
| intro_duration | float | 否 | 入场动画持续时间 |
| outro_animation | string | 否 | 出场动画 |
| outro_duration | float | 否 | 出场动画持续时间 |

### add_subtitle - 添加字幕

```json
POST /add_subtitle
{
  "srt": "1\\n00:00:00,000 --> 00:00:04,433\\n字幕内容",
  "draft_id": "dfd_xxx",
  "font_size": 10.0,
  "font": "抖音美好体",
  "font_color": "#FFFFFF",
  "transform_x": 0,
  "transform_y": -0.42,
  "track_name": "subtitle",
  "width": 1080,
  "height": 1920
}
```

### get_font_types - 获取可用字体列表

### get_text_intro_types - 获取文本入场动画列表

### get_text_outro_types - 获取文本出场动画列表

---

## 三、图片处理

### add_image - 添加图片

```json
POST /add_image
{
  "image_url": "http://np-newsmgr-uat.emapd.com/videomake/api/resource/download/bucket?filename=xxx.png&bucket=np-vediooss-material",
  "start": 0,
  "end": 5,
  "draft_id": "dfd_xxx",
  "width": 1080,
  "height": 1920,
  "transform_x": 0,
  "transform_y": 0,
  "scale_x": 1,
  "scale_y": 1,
  "track_name": "image_main",
  "relative_index": 0,
  "intro_animation": "放大",
  "intro_animation_duration": 0.5,
  "outro_animation": "缩小",
  "outro_animation_duration": 0.5,
  "alpha": 1.0,
  "flip_horizontal": false
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| image_url | string | 是 | 图片链接 |
| start | float | 是 | 起始时间 |
| end | float | 是 | 结束时间 |
| draft_id | string | 否 | 草稿ID |
| transform_x | float | 否 | X轴偏移 |
| transform_y | float | 否 | Y轴偏移 |
| scale_x | float | 否 | X缩放比例 |
| scale_y | float | 否 | Y缩放比例 |
| track_name | string | 否 | 轨道名称 |
| relative_index | int | 否 | 图层顺序（0最底层） |
| intro_animation | string | 否 | 入场动画 |
| intro_animation_duration | float | 否 | 入场动画时长 |
| outro_animation | string | 否 | 出场动画 |
| outro_animation_duration | float | 否 | 出场动画时长 |
| alpha | float | 否 | 透明度0-1 |

---

## 四、视频处理

### add_video - 添加视频

```json
POST /add_video
{
  "video_url": "https://...",
  "start": 0,
  "end": 0,
  "draft_id": "dfd_xxx",
  "width": 1080,
  "height": 1920,
  "transform_x": 0,
  "transform_y": 0,
  "scale_x": 1,
  "scale_y": 1,
  "speed": 1.0,
  "target_start": 0,
  "track_name": "video_main",
  "relative_index": 0,
  "volume": 1.0,
  "alpha": 1.0
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| video_url | string | 是 | 视频URL |
| start | float | 否 | 视频截取起始（秒） |
| end | float | 否 | 视频截取结束（秒），0表示不截取 |
| speed | float | 否 | 播放速度，>1加速，<1减速 |
| volume | float | 否 | 音量0-1 |
| target_start | float | 否 | 在时间线上的起始位置 |
| track_name | string | 否 | 轨道名称 |
| relative_index | int | 否 | 图层顺序 |

### get_transition_types - 获取转场动画列表

---

## 五、音频处理

### add_audio - 添加音频

```json
POST /add_audio
{
  "audio_url": "https://...",
  "start": 0,
  "end": 0,
  "draft_id": "dfd_xxx",
  "volume": 1.0,
  "target_start": 0,
  "speed": 1.0,
  "track_name": "audio_main",
  "duration": 30,
  "effect_type": "回音",
  "effect_params": [45]
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| audio_url | string | 是 | 音频URL |
| start | float | 否 | 截取起始 |
| end | float | 否 | 截取结束，0表示不截取 |
| volume | float | 否 | 音量0-1 |
| target_start | float | 否 | 在时间线上的起始位置 |
| speed | float | 否 | 播放速度 |
| track_name | string | 否 | 轨道名称 |
| duration | float | 否 | 持续时间 |
| effect_type | string | 否 | 音效类型 |
| effect_params | array | 否 | 音效参数 |

### get_audio_effect_types - 获取音频特效列表

---

## 六、特效处理

### add_effect - 添加特效

```json
POST /add_effect
{
  "effect_type": "MV封面",
  "effect_category": "scene",
  "start": 0,
  "end": 3.0,
  "draft_id": "dfd_xxx",
  "track_name": "effect_01",
  "params": [35, 45],
  "width": 1080,
  "height": 1920
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| effect_type | string | 是 | 特效名称 |
| effect_category | string | 是 | scene或character |
| start | float | 是 | 起始时间 |
| end | float | 是 | 结束时间 |
| draft_id | string | 否 | 草稿ID |
| track_name | string | 否 | 轨道名称 |
| params | array | 否 | 特效参数 |

### get_video_character_effect_types - 获取人物特效列表

### get_video_scene_effect_types - 获取场景特效列表

---

## 七、云渲染导出

### export_draft - 导出视频

```json
POST /export_draft
{
  "draft_id": "dfd_xxx",
  "resolution": "1080P",
  "framerate": "30",
  "export_cover": true
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| draft_id | string | 是 | 草稿ID |
| resolution | string | 否 | 分辨率480P/720P/1080P/2K/4K/8K |
| framerate | string | 否 | 帧率24/25/30/50/60 |
| export_cover | bool | 否 | 是否导出封面 |

**返回**: `{task_id, video_file_url, draft_file_url}`

---

## 素材OSS地址拼接

```
http://np-newsmgr-uat.emapd.com/videomake/api/resource/download/bucket?filename={ossKey}&bucket={bucket}
```

- **默认bucket**: `np-vediooss-material`
- **示例**: `http://np-newsmgr-uat.emapd.com/videomake/api/resource/download/bucket?filename=深色质感背景图3.png&bucket=np-vediooss-material`