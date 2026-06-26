# getCurrentInfo API

## 描述

获取 Meteor Master AI 的当前信息。

## 命令

```bash
mma post --method getCurrentInfo --data-file <filePath>
```

**注意：** 必须传递一个文件，即使是空对象 `{}` 也需要先写入文件。

## 示例

```bash
# 创建数据文件
echo '{}' > data.json

# 使用默认端口
mma post --method getCurrentInfo --data-file data.json

# 指定端口
mma post --method getCurrentInfo --port 9000 --data-file data.json
```

## 响应格式

```json
{
  "success": true,
  "message": "Request completed",
  "data": {
    "uuid": "17ff364f",
    "mode": 1,
    "workingStatus": 0,
    "path": "/path/to/video.mp4",
    "pathInfo": {
      "title": "我的摄像头",
      "path": "rtsp://admin:101038aA@192.168.0.152:554/Streaming/Channels/101",
      "useProxy": false,
      "httpProxy": "http://127.0.0.1:7897",
      "mark": "#FFAA47",
      "longitude": 120.7134,
      "latitude": 31.2483,
      "defaultMaskPath": "U:\DNG\其他\meteormaster\流星测试\Channels.png",
      "autoConnectThis": false,
      "actionAfterAutoConnect": 1,
      "otherArg": "",
      "starMapData": {
        "aspectRatio": 1.7777777777777777,
        "azimuth": 29.098903781765063,
        "cameraRotationZ": 0,
        "cameraType": "normal",
        "elevation": 17.289377736521303,
        "fisheyeStrength": 0.5,
        "focalLength": 20,
        "latitude": "28",
        "longitude": "100",
        "shootTime": "2026-01-13T04:47:19.553Z"
      }
    },
    "liveMetaData": {
      "chromaFormat": "4:2:0",
      "duration": 0,
      "fps": "25",
      "hasAudio": false,
      "hasKeyframesIndex": false,
      "hasVideo": true,
      "height": 1440,
      "level": "5.0",
      "metadata": {
        "duration": 0,
        "encoder": "Lavf62.6.103",
        "filesize": 0,
        "framerate": 25,
        "height": 1440,
        "title": "Media Presentation",
        "videocodecid": 7,
        "videodatarate": 0,
        "width": 2560
      },
      "mimeType": "video/x-flv; codecs=\"avc1.4d4032\"",
      "profile": "Main",
      "refFrames": 1,
      "sarDen": 1,
      "sarNum": 1,
      "segmentCount": 1,
      "videoCodec": "avc1.4d4032",
      "videoDataRate": 0,
      "width": 2560
    },
    "videoMetaData": {
      "avg_frame_rate": "12/1",
      "bit_rate": "19183000",
      "chroma_location": "left",
      "codec_long_name": "H.265 / HEVC (High Efficiency Video Coding)",
      "codec_name": "hevc",
      "codec_tag": "0x31637668",
      "codec_tag_string": "hvc1",
      "codec_type": "video",
      "coded_height": 1088,
      "coded_width": 1920,
      "color_primaries": "bt709",
      "color_range": "tv",
      "color_space": "bt709",
      "color_transfer": "bt709",
      "display_aspect_ratio": "16:9",
      "duration": "5.333333",
      "duration_ts": 128000,
      "extradata_size": 118,
      "has_b_frames": 0,
      "height": 1080,
      "id": "0x1",
      "index": 0,
      "level": 153,
      "nb_frames": "64",
      "pix_fmt": "yuv420p",
      "profile": "Main",
      "r_frame_rate": "12/1",
      "refs": 1,
      "sample_aspect_ratio": "1:1",
      "start_pts": 0,
      "start_time": "0.000000",
      "time_base": "1/24000",
      "width": 1920
    },
    "imageList": [
      {
        "source": "/path/to/image1.raw",
        "preview": "/path/to/image1.jpg",
        "thumb": "data:image/jpeg;base64,..."
      }
    ],
    "recordFolderPath": "/path/to/record/folder",
    "haveMask": true,
    "starMapData": {
      "aspectRatio": 1.7777777777777777,
      "azimuth": 29.098903781765063,
      "cameraRotationZ": 0,
      "cameraType": "normal",
      "elevation": 17.289377736521303,
      "fisheyeStrength": 0.5,
      "focalLength": 20,
      "latitude": "28",
      "longitude": "100",
      "shootTime": "2026-01-13T04:47:19.553Z"
    },
    "totalNum": 42,
    "useTime": 4,
    "currentVideoTime": 60,
    "playing": true,
    "isMuted": false,
    "mediaServerRTMPPort": 5000,
    "mediaServerHTTPPort": 7000，
    "supportMMABridgeMethods": ["getCurrentInfo", "getFilterList", "getDataList"],

  }
}
```

## 响应字段说明

- `success` (布尔值): 表示请求是否成功
- `message` (字符串): 状态消息
- `data` (对象): 包含实际信息
  - `uuid` (字符串): 唯一标识符，用于标识当前MMA实例
  - `mode` (整数): 当前所在的模式，即选择输入源的模式
    - 0: 开始界面
    - 1: 分析视频模式
    - 2: 分析直播模式
    - 3: 分析摄像头模式
    - 4: 分析图片序列模式
    - 5: 向MMA推流模式
  - `workingStatus` (整数): 当前工作状态，表示分析的状态。这个对用户很重要而且不要搞错数字与状态的对应关系！
    - 0: 初始状态
    - 1: 读取视频中
    - 2: 视频读取完毕
    - 3: 分析中
    - 4: 分析已结束
    - 5: 直播分析中
  - `path` (字符串): 文件路径
    - mode=1时为视频文件的路径
    - mode=4时为图片序列文件夹的路径
  - `pathInfo` (对象): 直播、摄像头或推流相关信息
    - `title` (字符串): 标题
    - `path` (字符串): RTSP或其他视频流地址
    - `useProxy` (布尔值): 是否使用代理
    - `httpProxy` (字符串): HTTP代理地址
    - `mark` (字符串): 标记颜色（如"#FFAA47"）
    - `longitude` (浮点数): 经度
    - `latitude` (浮点数): 纬度
    - `defaultMaskPath` (字符串): 默认蒙版路径
    - `autoConnectThis` (布尔值): 是否自动连接
    - `actionAfterAutoConnect` (整数): 自动连接后的动作
      - 1: 立即启动分析
      - 2: 启动定时任务
    - `otherArg` (字符串): 其他FFmpeg参数
    - `starMapData` (对象): 星图数据（同下文starMapData字段，但是此处的信息是记录在文件中的默认值，如果下文有starMapData那么以他为准）
  - `liveMetaData` (对象): 直播视频流元数据（由ffprobe读取）
    - `chromaFormat` (字符串): 色度采样格式（如"4:2:0"）
    - `duration` (浮点数): 视频时长（秒），直播流通常为0
    - `fps` (字符串): 帧率（如"25"）
    - `hasAudio` (布尔值): 是否包含音频流
    - `hasKeyframesIndex` (布尔值): 是否有关键帧索引
    - `hasVideo` (布尔值): 是否包含视频流
    - `height` (整数): 视频高度（像素）
    - `level` (字符串): 编码级别（如"5.0"）
    - `metadata` (对象): 额外的元数据信息
      - `duration` (浮点数): 视频时长（秒）
      - `encoder` (字符串): 编码器信息（如"Lavf62.6.103"）
      - `filesize` (整数): 文件大小（字节）
      - `framerate` (浮点数): 帧率
      - `height` (整数): 视频高度（像素）
      - `title` (字符串): 标题
      - `videocodecid` (整数): 视频编码ID
      - `videodatarate` (整数): 视频数据率
      - `width` (整数): 视频宽度（像素）
    - `mimeType` (字符串): MIME类型（如"video/x-flv; codecs=\"avc1.4d4032\""）
    - `profile` (字符串): 编码配置文件（如"Main"）
    - `refFrames` (整数): 参考帧数
    - `sarDen` (整数): 样本宽高比分母
    - `sarNum` (整数): 样本宽高比分子
    - `segmentCount` (整数): 分段数
    - `videoCodec` (字符串): 视频编解码器（如"avc1.4d4032"）
    - `videoDataRate` (整数): 视频数据率
    - `width` (整数): 视频宽度（像素）
  - `videoMetaData` (对象): 本地视频元数据（由ffprobe读取）
    - `avg_frame_rate` (字符串): 平均帧率（如"12/1"）
    - `bit_rate` (字符串): 比特率（如"19183000"）
    - `chroma_location` (字符串): 色度位置（如"left"）
    - `codec_long_name` (字符串): 编解码器全名（如"H.265 / HEVC (High Efficiency Video Coding)"）
    - `codec_name` (字符串): 编解码器名称（如"hevc"）
    - `codec_tag` (字符串): 编解码器标签（十六进制，如"0x31637668"）
    - `codec_tag_string` (字符串): 编解码器标签字符串（如"hvc1"）
    - `codec_type` (字符串): 编解码器类型（如"video"）
    - `coded_height` (整数): 编码高度（像素）
    - `coded_width` (整数): 编码宽度（像素）
    - `color_primaries` (字符串): 色彩原色（如"bt709"）
    - `color_range` (字符串): 色彩范围（如"tv"）
    - `color_space` (字符串): 色彩空间（如"bt709"）
    - `color_transfer` (字符串): 色彩传输特性（如"bt709"）
    - `display_aspect_ratio` (字符串): 显示宽高比（如"16:9"）
    - `duration` (字符串): 视频时长（秒，如"5.333333"）
    - `duration_ts` (整数): 时长时间戳
    - `extradata_size` (整数): 额外数据大小
    - `has_b_frames` (整数): B帧数量
    - `height` (整数): 视频高度（像素）
    - `id` (字符串): 流ID（如"0x1"）
    - `index` (整数): 流索引
    - `level` (整数): 编码级别
    - `nb_frames` (字符串): 总帧数
    - `pix_fmt` (字符串): 像素格式（如"yuv420p"）
    - `profile` (字符串): 编码配置文件（如"Main"）
    - `r_frame_rate` (字符串): 实际帧率（如"12/1"）
    - `refs` (整数): 参考帧数
    - `sample_aspect_ratio` (字符串): 样本宽高比（如"1:1"）
    - `start_pts` (整数): 起始时间戳
    - `start_time` (字符串): 起始时间（如"0.000000"）
    - `time_base` (字符串): 时间基（如"1/24000"）
    - `width` (整数): 视频宽度（像素）
  - `imageList` (数组): 图片序列列表（mode=4时有效）
    - 每个元素包含以下字段:
      - `source` (字符串): 原始图片文件路径
      - `preview` (字符串): JPG格式预览图路径
      - `thumb` (字符串): 缩略图（Base64编码）
  - `recordFolderPath` (字符串): 点击开始监控直播后指定的缓存文件夹路径
  - `haveMask` (布尔值): 是否设置了蒙版
  - `starMapData` (对象): 星图数据，记录了夜空标定后摄像机的相关信息
    - `aspectRatio` (浮点数): 宽高比（如1.7777777777777777）
    - `azimuth` (浮点数): 方位角（度）
    - `cameraRotationZ` (浮点数): 摄像机Z轴旋转角度
    - `cameraType` (字符串): 摄像机类型（如"normal"）
    - `elevation` (浮点数): 高度角（度）
    - `fisheyeStrength` (浮点数): 鱼眼强度（0-1之间）
    - `focalLength` (浮点数): 焦距
    - `latitude` (字符串): 纬度
    - `longitude` (字符串): 经度
    - `shootTime` (字符串): 拍摄时间（ISO 8601格式，如"2026-01-13T04:47:19.553Z"）
  - `totalNum` (整数): 当前分析出来的流星结果总数。这个对用户来说比较重要！
  - `useTime` (数字): 分析耗时，单位是秒。这个对用户来说比较重要！
  - `currentVideoTime` (浮点数): 当前播放时间（秒）
  - `playing` (布尔值): 当前是否在播放
  - `isMuted` (布尔值): 当前是否静音
  - `mediaServerRTMPPort` (整数): 媒体服务器RTMP接收端口，任何MMA外部的视频流，会经过ffmpeg转码后推送到rtmp://localhost:${mediaServerRTMPPort}/live/MeteorMaster上面，然后由node-media-server转发到渲染进程上。MMA的分析也依赖rtmp://localhost:${mediaServerRTMPPort}/live/MeteorMaster这个地址。
  - `mediaServerHTTPPort` (整数): 媒体服务器HTTP输出端口，用于显示直播画面。这个就是node-media-server转发出来推送到渲染进程上使用的端口（http://localhost:${mediaServerHTTPPort}/live/MeteorMaster.flv ），在渲染进程中，mpegts.js会使用这个地址的画面信息渲染到MMA的界面上。
  - `supportMMABridgeMethods`: 当前MMA版本支持的MMABridge方法名列表。如果支持的方法不在当前SIKLL中，可以提示用户前往更新SKILL（https://clawhub.ai/mordom0404/mma-bridge）
