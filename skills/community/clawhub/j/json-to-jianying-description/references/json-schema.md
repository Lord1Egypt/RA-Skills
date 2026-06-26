# JSON 格式详解

## 完整字段说明

### oralBroadcastingList[]

| 字段 | 类型 | 说明 |
|------|------|------|
| oralText | string | 原始文案文本 |
| materialDesc | string | 素材描述（用于匹配素材） |
| materialKey | string | 素材KEY，用于在 materialList 中匹配对应素材 |
| ttsResult | object | TTS 语音合成结果 |
| ttsResult.text | string | 实际朗读的文本 |
| ttsResult.duration | number | 语音总时长（秒） |
| ttsResult.audioOssBucket | string | 音频 OSS bucket |
| ttsResult.audioOssKey | string | 音频 OSS key |
| ttsResult.captionStartEnds[] | array | 字幕时间轴 |
| captionStartEnds[].caption | string | 字幕文本 |
| captionStartEnds[].startSecond | number | 起始秒数（相对当前片段） |
| captionStartEnds[].endSecond | number | 结束秒数（相对当前片段） |
| captionStartEnds[].duration | number | 持续秒数 |

### materialList[]

| 字段 | 类型 | 说明 |
|------|------|------|
| sourceType | number | 素材来源类型 |
| ossBucket | string | OSS bucket |
| ossKey | string | OSS key |
| url | string | 素材URL（可能是第三方链接） |
| width | number | 素材宽度 |
| height | number | 素材高度 |
| isUsable | number | 是否可用（1=可用） |
| imgDescScore | number | 图片描述匹配分数 |
| title | string | 素材标题 |
| titleScore | number | 标题匹配分数 |
| desc | string | 素材描述 |

### bgmInfo

| 字段 | 类型 | 说明 |
|------|------|------|
| sourceType | number | 来源类型 |
| ossBucket | string | OSS bucket |
| ossKey | string | OSS key |
| url | string | 音乐URL |
| thumb | string | 缩略图 |
| title | string | 音乐标题 |
| duration | number | 时长（毫秒） |

## 时间计算公式

```
片段N绝对起始时间 = sum(片段0.duration + 片段1.duration + ... + 片段N-1.duration)

字幕N绝对起始时间 = 片段N绝对起始时间 + captionStartEnds[N].startSecond
字幕N绝对结束时间 = 片段N绝对起始时间 + captionStartEnds[N].endSecond
```

## 素材地址拼接公式

```
图片/视频素材地址：
http://np-newsmgr-uat.emapd.com/videomake/api/resource/download/bucket?filename={ossKey}&bucket={ossBucket}

音频素材地址（相同）：
http://np-newsmgr-uat.emapd.com/videomake/api/resource/download/bucket?filename={ossKey}&bucket={ossBucket}
```

默认 bucket: `np-vediooss-material`

## 示例：完整转换

### 输入
```json
{
  "oralBroadcastingList": [
    {
      "oralText": "宝济药业 - B有重大进展！",
      "materialKey": "desc_material_D36841A87F2909BB35DC950C500064D9.jpg",
      "ttsResult": {
        "duration": 2.28,
        "captionStartEnds": [
          { "caption": "宝济药业 - B", "startSecond": 0.0, "endSecond": 1.12 },
          { "caption": "有重大进展", "startSecond": 1.12, "endSecond": 2.28 }
        ]
      }
    },
    {
      "oralText": "3月25日，宝济药业 - B公告相关进展。",
      "materialKey": "desc_material_D36841A87F2909BB35DC950C500064D9.jpg",
      "ttsResult": {
        "duration": 3.14,
        "captionStartEnds": [
          { "caption": "3月25日", "startSecond": 0.0, "endSecond": 1.03 },
          { "caption": "宝济药业 - B", "startSecond": 1.03, "endSecond": 1.92 },
          { "caption": "公告相关进展", "startSecond": 1.92, "endSecond": 3.14 }
        ]
      }
    }
  ],
  "materialList": [
    {
      "ossKey": "desc_material_D36841A87F2909BB35DC950C500064D9.jpg",
      "ossBucket": "np-vediooss-material",
      "url": "https://img0.baidu.com/it/u=1574300236,987946807&fm=253&fmt=auto&app=120&f=JPEG?w=828&h=500",
      "desc": "宝济药业大楼外观局部"
    }
  ],
  "bgmInfo": {
    "ossBucket": "np-vediooss-material",
    "ossKey": "desc_material_C6CF433C3F6ADEBA88682E05EE9D9F5F.mp3",
    "url": "https://cdnsaas.kuai.360.cn/kjjsaas/chinese_url7e382e1209120302_251114_7720795.mp3",
    "title": "氛围音乐 助眠",
    "duration": 193000
  }
}
```

### 输出
```
视频总时长：5.42秒

0-2.28秒是 desc_material_D36841A87F2909BB35DC950C500064D9.jpg 这个素材，对应的字幕：
- 0.0-1.12 秒是 "宝济药业 - B"
- 1.12-2.28 秒是 "有重大进展"

2.28-5.42秒是 desc_material_D36841A87F2909BB35DC950C500064D9.jpg 这个素材，对应的字幕：
- 2.28-3.31 秒是 "3月25日"
- 3.31-4.20 秒是 "宝济药业 - B"
- 4.20-5.42 秒是 "公告相关进展"

背景图：desc_material_D36841A87F2909BB35DC950C500064D9.jpg
素材地址：http://np-newsmgr-uat.emapd.com/videomake/api/resource/download/bucket?filename=desc_material_D36841A87F2909BB35DC950C500064D9.jpg&bucket=np-vediooss-material

BGM：氛围音乐 助眠
BGM地址：https://cdnsaas.kuai.360.cn/kjjsaas/chinese_url7e382e1209120302_251114_7720795.mp3
```