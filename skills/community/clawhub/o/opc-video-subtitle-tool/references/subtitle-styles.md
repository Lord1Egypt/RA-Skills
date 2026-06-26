# 字幕样式配置

## 概览

本 Skill 提供8种预设字幕样式，涵盖常见的视频字幕需求。每种样式都有特定的字体颜色、描边颜色和背景颜色配置。

## 预设样式列表

### 样式1：白字黑边
- **描述**：底部居中，白色文字带黑色描边
- **适用场景**：大多数视频场景，清晰易读
- **配置参数**：
  - primaryColor: #FFFFFF
  - borderColor: #000000
  - borderWidth: 3

### 样式2：黑字白边
- **描述**：底部居中，黑色文字带白色描边
- **适用场景**：浅色背景视频
- **配置参数**：
  - primaryColor: #000000
  - borderColor: #FFFFFF
  - borderWidth: 3

### 样式3：黄字黑边
- **描述**：底部居中，黄色文字带黑色描边
- **适用场景**：需要醒目突出的字幕
- **配置参数**：
  - primaryColor: #FFde00
  - borderColor: #000000
  - borderWidth: 3

### 样式4：红字白边
- **描述**：底部居中，红色文字带白色描边
- **适用场景**：强调重要内容或情感表达
- **配置参数**：
  - primaryColor: #ab4a37
  - borderColor: #FFFFFF
  - borderWidth: 3

### 样式5：黑底白字
- **描述**：白色字体黑色背景
- **适用场景**：需要高对比度的场景
- **配置参数**：
  - primaryColor: #FFFFFF
  - background_color: #000000

### 样式6：白底黑字
- **描述**：黑色字体白色背景
- **适用场景**：简洁清晰的字幕展示
- **配置参数**：
  - primaryColor: #000000
  - background_color: #FFFFFF

### 样式7：黄底黑字
- **描述**：黑色字体黄色背景
- **适用场景**：警示或注意内容
- **配置参数**：
  - primaryColor: #000000
  - background_color: #ffde00

### 样式8：红底白字
- **描述**：红色字体白色背景
- **适用场景**：强调重要信息
- **配置参数**：
  - primaryColor: #FFFFFF
  - background_color: #a74f59

## 颜色格式说明

- 所有颜色值使用十六进制格式
- 格式示例：#FFFFFF（白色）、#000000（黑色）
- 支持标准 RGB 颜色值（6位十六进制）

## 使用方式

### 使用预设样式
在调用脚本时指定 `--style_id` 参数：
```bash
python scripts/video_subtitle.py \
  --video_url "https://example.com/video.mp4" \
  --text "字幕内容" \
  --voice_id "zh-CN-YunxiNeural" \
  --style_id 1
```

### 使用自定义样式
不指定 `--style_id`，改用自定义颜色参数：
```bash
python scripts/video_subtitle.py \
  --video_url "https://example.com/video.mp4" \
  --text "字幕内容" \
  --voice_id "zh-CN-YunxiNeural" \
  --custom_background_color "#000000" \
  --custom_border_color "#FFFFFF" \
  --custom_primary_color "#FF0000"
```

## 样式选择建议

| 视频类型 | 推荐样式 | 原因 |
|---------|---------|------|
| 通用视频 | 样式1（白字黑边） | 清晰易读，适用性广 |
| 浅色背景视频 | 样式2（黑字白边） | 高对比度，易于辨识 |
| 情感类视频 | 样式4（红字白边） | 突出情感色彩 |
| 教学视频 | 样式6（白底黑字） | 正式、专业感强 |
| 警示信息 | 样式7（黄底黑字） | 醒目提醒 |
