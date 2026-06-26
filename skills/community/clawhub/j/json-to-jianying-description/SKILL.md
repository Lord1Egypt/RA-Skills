---
name: json-to-jianying-description
description: 将特定的JSON视频素材格式（包含oralBroadcastingList、materialList、bgmInfo等字段）转换为剪映API可用的自然语言视频描述。用于根据素材JSON生成视频制作指令，包括素材匹配、时间轴计算、字幕时间同步、特殊效果处理等。当用户发送包含oralBroadcastingList和materialList的JSON数据，并要求生成视频或视频描述时触发此skill。
---

# JSON 转剪映视频描述

## 输入格式

用户会发送一个包含以下关键字段的 JSON：

```json
{
  "oralBroadcastingList": [
    {
      "oralText": "文案内容",
      "materialDesc": "素材描述",
      "materialKey": "desc_material_xxx.jpg",
      "ttsResult": {
        "text": "实际朗读文本",
        "duration": 2.28,
        "audioOssBucket": "np-vediooss-material",
        "audioOssKey": "volc_tts_xxx.mp3",
        "captionStartEnds": [
          { "caption": "字幕1", "startSecond": 0.0, "endSecond": 1.12, "duration": 1.12 },
          { "caption": "字幕2", "startSecond": 1.12, "endSecond": 2.28, "duration": 1.16 }
        ]
      }
    }
  ],
  "materialList": [
    {
      "ossBucket": "np-vediooss-material",
      "ossKey": "desc_material_xxx.jpg",
      "url": "https://...",
      "desc": "素材描述"
    }
  ],
  "bgmInfo": {
    "ossBucket": "np-vediooss-material",
    "ossKey": "desc_material_xxx.mp3",
    "url": "https://...",
    "title": "背景音乐标题",
    "duration": 193000
  }
}
```

## 输出格式

转换为自然语言描述，格式如下：

```
视频总时长：X秒

0-X秒是 {materialKey} 这个素材，对应的字幕：
- 0.0-1.21 秒是 "字幕1"
- 1.21-1.91 秒是 "字幕2"
...

X-Y秒是 {materialKey} 这个素材，对应的字幕：
...

背景图：{ossKey}

特殊需求：
- 在某某时间段插入图片：{ossKey}
- 给某素材添加某某特效
```

## 转换步骤

### 1. 解析 oralBroadcastingList

- 遍历 `oralBroadcastingList` 数组
- 每个元素代表一个视频片段
- 使用 `ttsResult.captionStartEnds` 计算该片段的起止时间

### 2. 计算时间轴

- **起始时间**：累加前面所有片段的 duration
- **结束时间**：起始时间 + 当前片段的 ttsResult.duration
- 每个字幕的绝对时间 = 片段起始时间 + captionStartEnds 中的相对时间

### 3. 匹配素材

- 从 `materialList` 中查找 `ossKey` 与 `oralBroadcastingList[].materialKey` 匹配的素材
- 使用 `url` 字段作为素材地址

### 4. 处理背景图

- 默认使用 `materialList` 中的第一张图片作为背景图
- 或使用用户指定的背景图

### 5. 处理 BGM

- 提取 `bgmInfo.url` 作为背景音乐

### 6. 特殊需求识别

用户可能会指定额外需求，如：
- 在某时间段插入额外图片
- 给某素材添加特效（如"放映滚动"）
- 调整素材顺序

## 素材地址拼接

图片/视频/音频素材地址拼接：
- **基础URL**: `http://np-newsmgr-uat.emapd.com/videomake/api/resource/download/bucket`
- **拼接方式**: `${baseUrl}?filename=${ossKey}&bucket=${ossBucket}`

示例：
- ossKey: `深色质感背景图3.png`，bucket: `np-vediooss-material`
- 完整地址: `http://np-newsmgr-uat.emapd.com/videomake/api/resource/download/bucket?filename=深色质感背景图3.png&bucket=np-vediooss-material`

## 完整示例

### 输入 JSON（用户提供的例子）

```json
{
  "oralBroadcastingList": [
    {
      "oralText": "宝济药业 - B有重大进展！",
      "materialKey": "desc_material_D36841A87F2909BB35DC950C500064D9.jpg",
      "ttsResult": {
        "captionStartEnds": [
          { "caption": "宝济药业 - B", "startSecond": 0.0, "endSecond": 1.12 },
          { "caption": "有重大进展", "startSecond": 1.12, "endSecond": 2.28 }
        ],
        "duration": 2.28
      }
    },
    {
      "oralText": "3月25日，宝济药业 - B公告相关进展。",
      "materialKey": "desc_material_D36841A87F2909BB35DC950C500064D9.jpg",
      "ttsResult": {
        "captionStartEnds": [
          { "caption": "3月25日", "startSecond": 0.0, "endSecond": 1.03 },
          { "caption": "宝济药业 - B", "startSecond": 1.03, "endSecond": 1.92 },
          { "caption": "公告相关进展", "startSecond": 1.92, "endSecond": 3.14 }
        ],
        "duration": 3.14
      }
    }
    // ... more items
  ],
  "materialList": [
    {
      "ossKey": "desc_material_D36841A87F2909BB35DC950C500064D9.jpg",
      "ossBucket": "np-vediooss-material",
      "url": "https://img0.baidu.com/...",
      "desc": "宝济药业大楼外观局部"
    }
  ],
  "bgmInfo": {
    "ossBucket": "np-vediooss-material",
    "ossKey": "desc_material_C6CF433C3F6ADEBA88682E05EE9D9F5F.mp3",
    "url": "https://cdnsaas.kuai.360.cn/...",
    "title": "氛围音乐 助眠"
  }
}
```

### 输出描述

```
视频总时长：29.39秒

0-2.28秒是 desc_material_D36841A87F2909BB35DC950C500064D9.jpg 这个素材，对应的字幕：
- 0.0-1.12 秒是 "宝济药业 - B"
- 1.12-2.28 秒是 "有重大进展"

2.28-5.42秒是 desc_material_D36841A87F2909BB35DC950C500064D9.jpg 这个素材，对应的字幕：
- 2.28-3.31 秒是 "3月25日"
- 3.31-4.20 秒是 "宝济药业 - B"
- 4.20-5.42 秒是 "公告相关进展"

... (以此类推)

背景图：desc_material_D36841A87F2909BB35DC950C500064D9.jpg

BGM：氛围音乐 助眠 (url: https://cdnsaas.kuai.360.cn/...)
```

## 注意事项

1. **时间累加**：每个片段的绝对起始时间需要累加前面所有片段的 duration
2. **素材匹配**：materialKey 可能不完整（如只有文件名），需要在 materialList 中模糊匹配
3. **OSS 地址拼接**：需要将 ossKey 和 ossBucket 拼接成完整的素材地址
4. **用户额外需求**：用户可能会指定插入图片、添加特效等额外需求，需要在描述中体现

## 使用场景

当用户发送类似结构的 JSON 并要求：
- "帮我生成一个视频"
- "把这个转成视频描述"
- "用这个素材做视频"

此时应使用此 skill 进行 JSON 解析和描述转换。