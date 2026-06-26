# 媒体 · AI · 分布式开发

> 来源：华为开发者文档
> https://developer.huawei.com/consumer/cn/doc/harmonyos-references/media-intro

---

## 媒体能力

### 图片处理（image）

```typescript
import image from '@ohos.multimedia.image';

// 创建图片对象
const color: ArrayBuffer = new ArrayBuffer(100 * 100 * 4);
let opts: image.InitializationOptions = {
  editable: true,
  pixelFormat: 3,  // RGBA_8888
  size: { width: 100, height: 100 }
};
image.createPixelMap(color, opts, (err, pixelMap) => {
  // pixelMap 即为图片对象
});

// 读取图片（从媒体库）
import photoAccessHelper from '@ohos.photoAccessHelper';

async function pickImage() {
  let PhotoSelectOptions = new photoAccessHelper.PhotoSelectOptions();
  PhotoSelectOptions.MIMEType = photoAccessHelper.PhotoViewMIMETypes.IMAGE_TYPE;
  PhotoSelectOptions.maxSelectNumber = 1;

  let photoPicker = new photoAccessHelper.PhotoViewPicker();
  let result = await photoPicker.select(PhotoSelectOptions);
  console.info(`选中图片: ${result.photoUris[0]}`);
}
```

### 视频播放（video）

```typescript
import media from '@ohos.multimedia.media';

// 创建视频播放器
let videoPlayer: media.VideoPlayer = await media.createVideoPlayer();
await videoPlayer.setUrl('https://example.com/video.mp4');
await videoPlayer.prepare();
await videoPlayer.play();

// 控制
videoPlayer.pause();
videoPlayer.seek(5000);  // 跳转到 5 秒
videoPlayer.setVolume(0.5);
videoPlayer.stop();

// 监听事件
videoPlayer.on('playbackCompleted', () => {
  console.info('播放完成');
});
videoPlayer.on('error', (err) => {
  console.error(`播放错误: ${err}`);
});
```

### 音频播放（audio）

```typescript
import audio from '@ohos.multimedia.audio';

async function playAudio() {
  let audioRenderer: audio.AudioRenderer = await audio.createAudioRenderer({
    streamInfo: {
      samplingRate: audio.AudioSamplingRate.SAMPLE_RATE_48000,
      channels: audio.AudioChannel.CHANNEL_2,
      sampleFormat: audio.AudioSampleFormat.SAMPLE_FORMAT_S16LE,
      encodingType: audio.AudioEncodingType.ENCODING_TYPE_RAW
    }
  });

  let buffer = getAudioData();  // 获取音频数据
  await audioRenderer.write(buffer);
  await audioRenderer.start();
  await audioRenderer.stop();
  await audioRenderer.release();
}
```

---

## Canvas 图形绑定

```typescript
@Entry
@Component
struct CanvasExample {
  private settings: RenderingContextSettings = new RenderingContextSettings(true);
  private context: CanvasRenderingContext2D = new CanvasRenderingContext2D(this.settings);

  build() {
    Column() {
      Canvas(this.context)
        .width('100%')
        .height('100%')
        .onReady(() => {
          // 绘制矩形
          this.context.fillStyle = '#FF5733';
          this.context.fillRect(0, 0, 200, 100);

          // 绘制圆形
          this.context.beginPath();
          this.context.arc(100, 50, 40, 0, Math.PI * 2);
          this.context.fillStyle = '#33FF57';
          this.context.fill();

          // 绘制文字
          this.context.font = '20px sans-serif';
          this.context.fillText('Hello Canvas', 20, 80);

          // 绘制图片
          let img = new ImageBitmap('https://example.com/image.png');
          this.context.drawImage(img, 0, 0);

          // 渐变
          let gradient = this.context.createLinearGradient(0, 0, 200, 0);
          gradient.addColorStop(0, '#FF0000');
          gradient.addColorStop(1, '#0000FF');
          this.context.fillStyle = gradient;
          this.context.fillRect(0, 100, 200, 50);
        })
    }
  }
}
```

---

## AI 能力（HiAI / ML）

```typescript
import ml from '@kit.MLKit';

// 文字识别（OCR）
import textRecognition from '@kit.MLKit';

async function recognizeText(imagePath: string) {
  let request = new textRecognition.TextRecognitionRequest();
  request.imgUri = imagePath;
  let result = await textRecognitionrecognize(request);
  console.info(`识别文字: ${result.text}`);
}

// 人脸检测
import faceDetection from '@kit.MLKit';

async function detectFace(imagePath: string) {
  let request = new faceDetection.FaceDetectionRequest();
  request.imgUri = imagePath;
  let result = await faceDetection.detect(request);
  console.info(`检测到 ${result.length} 张人脸`);
}

// 语音合成
import textToSpeech from '@kit.MLKit';

async function speak(text: string) {
  let synthesizer = await textToSpeech.createTTSEngine();
  let config = {
    params: {
      pitch: 1.0,
      speed: 1.0,
      volume: 1.0,
      language: 'zh-CN'
    }
  };
  await synthesizer.speak(text, config);
  await synthesizer.stop();
}
```

---

## 分布式开发（流转 / 跨设备）

### 分布式任务调度

```typescript
import wantAgent from '@ohos.want.agent';
import distributedMission from '@ohos.distributedMission';

// 跨设备启动 Ability
async function startRemoteAbility() {
  let want: Want = {
    deviceId: 'remote_device_id',
    bundleName: 'com.example.app',
    abilityName: 'EntryAbility',
    parameters: { 'message': 'hello from local device' }
  };

  await globalThis.context.startAbility(want);
  console.info('跨设备启动成功');
}

// 流转（Continuable）- 状态迁移
class MyAbility extends UIAbility {
  onContinue(wantParam) {
    // 将本地状态序列化传给目标设备
    wantParam['localState'] = JSON.stringify({
      page: this.currentPage,
      data: this.appData
    });
    return OnContinueResult.AGREE;  // 或 REJECT
  }
}
```

### 跨设备数据同步

```typescript
import distributedData from '@ohos.distributed.kvStore';

// 创建分布式数据库
let kvManager: distributedData.KVManager;
let config: distributedData.KVManagerConfig = {
  bundleName: 'com.example.app',
  userInfo: distributedData.UserInfo.SYSTEM_USER_ID
};
kvManager = distributedData.createKVManager(config);

let kvStore: distributedData.SingleKVStore;
await kvManager.getKVStore('store_id', (err, store) => {
  kvStore = store;
});

// 写入数据（自动同步到同组网设备）
await kvStore.put('key', 'value');

// 订阅数据变化
kvStore.on('dataChange', distributedData.SubscribeType.SUBSCRIBE_TYPE_REMOTE, (data) => {
  console.info(`数据变化: ${JSON.stringify(data)}`);
});

// 查询数据
let value = await kvStore.get('key');
```

### 跨设备文件访问

```typescript
import distributedFile from '@ohos.distributedfile';

// 访问远程设备文件
async function readRemoteFile(deviceId: string, path: string) {
  let dfs = distributedFile.getDistributedFile();
  let fileData = await dfs.readFile(deviceId, path);
  return fileData;
}
```

---

## 网络请求

```typescript
import http from '@ohos.net.http';

// 发送 HTTP 请求
async function fetchData() {
  let httpRequest = http.createHttp();
  let url = 'https://api.example.com/data';

  let response = await httpRequest.request(
    url,
    {
      method: http.RequestMethod.GET,
      header: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer token'
      },
      connectTimeout: 60000,
      readTimeout: 60000
    }
  );

  if (response.responseCode === 200) {
    let data = JSON.parse(response.result as string);
    console.info(`数据: ${JSON.stringify(data)}`);
  }

  httpRequest.destroy();
}

// POST 请求
async function postData() {
  let httpRequest = http.createHttp();
  let response = await httpRequest.request(
    'https://api.example.com/post',
    {
      method: http.RequestMethod.POST,
      header: { 'Content-Type': 'application/json' },
      extraData: JSON.stringify({ name: 'Alice', age: 30 })
    }
  );

  let result = JSON.parse(response.result as string);
  console.info(`响应: ${JSON.stringify(result)}`);
}
```
