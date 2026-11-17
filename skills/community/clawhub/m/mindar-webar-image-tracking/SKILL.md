---
name: mindar-webar-image-tracking
description: 用 MindAR.js + A-Frame 做手机 WebAR 图像识别（扫卡牌/图片/包装出 3D 内容），包括：在纯 Node 下编译 .mind 而绕开 node-canvas、用特征点数在编译期判定目标图质量、用合成假摄像头在无头浏览器里做端到端自动验证。当用户提到 MindAR、WebAR、手机扫一扫出模型、H5 AR、图像识别跟踪、.mind 编译失败、node-canvas 装不上、无头浏览器测 AR、或 tfjs WebGL kernel 报错时使用。
agent_created: true
---

# MindAR WebAR 图像识别：编译、质检与自动化验证

MindAR.js 是手机 WebAR 里成本最低的路线（纯前端、无需 App、无需头显）。
但它的官方工具链有三个硬伤：编译依赖 `node-canvas`、没有目标图质量反馈、
只能在真机上手测。本 skill 记录绕开这三点的实测做法。

## 适用判断

- 目标是**手机浏览器打开一个 https 链接就能扫**（iOS Safari + Android Chrome）
- 识别对象是**平面图像**：卡牌、海报、包装、书页
- ✅ 优点是零安装门槛；⚠️ 局限是**只能识别、不能定位到空间坐标**——
  它给你的是「哪张图 + 图在画面里的位姿」，不是「图在世界坐标系的位姿」。
  要做「卡牌摆在桌上、模型贴在卡上」这种桌面 AR，图像识别够用；
  要做六自由度空间锚定（比如把模型钉在房间某处），得走 WebXR + 标记追踪。

---

## 一、在纯 Node 下编译 .mind（绕开 node-canvas）

`mind-ar` 的 `OfflineCompiler` 只在 `createProcessCanvas()` 里需要 `node-canvas`，
**其余整条链都是纯 JS**。所以在 CI / 无 GUI 环境里，可以继承 `CompilerBase`
并塞一个假 canvas 进去，完全跳过原生依赖。

`npm i canvas` 在 Windows 上经常编译失败，这个方法能省掉整个原生工具链。

```javascript
// compile-mind.mjs
import { CompilerBase } from './pkg/package/src/image-target/compiler-base.js'
import { buildTrackingImageList } from './pkg/package/src/image-target/image-list.js'
import { extractTrackingFeatures } from './pkg/package/src/image-target/tracker/extract-utils.js'

// ⚠️ 必须放在最后 import：tfjs kernel 是「后注册者覆盖先注册者」
import './pkg/package/src/image-target/detector/kernels/cpu/index.js'

class PredecodedCanvas {
  constructor(image) { this._image = image }        // image 已是 ImageData 形态
  getContext() {
    return {
      drawImage() {},
      getImageData() { return { data: this._image.data } },
    }
  }
}
```

关键点：

- **kernel 注册顺序不能反。** `detector.js` 会 import WebGL 版 kernel；
  CPU 版必须在它**之后** import 才会生效。顺序反了，在无 GPU 的 Node 里
  会在 `Detector` 构造时崩，报错完全指不到根因。
- `.mind` 文件是 **msgpack**，`CURRENT_VERSION = 2`。校验时用
  `CompilerBase.importData()` 走**运行时读取路径**，不要用浏览器版 `Compiler`
  （它依赖 vite 的 `?worker&inline`，在 Node 里会报
  `does not provide an export named 'default'`）。

### 命令行用法

```bash
node compile-mind.mjs \
  --image targets/guanyu.png --image targets/zhangfei.png \
  --out site/targets.mind
```

---

## 二、编译期目标图质检（把「这图能不能用」变成可测量）

MindAR 官方不给任何质量反馈——图不好就只是「扫不出来」，你得反复试。
但编译过程内部已经算出了特征点数（FREAK），**把它打出来就是质量指标**。

实测阈值：

| 可用特征点数 | 判定 | 建议 |
|---|---|---|
| `< 100` | 不可用 | 换图，别浪费时间 |
| `100 ~ 300` | 偏弱 | 能扫，但对角度/距离/光照很敏感 |
| `≥ 300` | 可用 | 正常使用 |

实测参照值（同一套编译参数下）：

- 精心设计的卡牌面（大面积古典纹样 + 汉字）→ **2497 / 2781 / 2903**
- 一张普通插画预览图 → 654
- 一张纯 ArUco 标记卡 → 498（黑白块特征太少，反而差）

**由此得出的设计结论：给识别目标图加「纹理层」是最划算的优化。**
大面积单调色块（渐变、纯色底、大留白）几乎不贡献特征点；
密集的小尺度纹样（云纹、水波、文字排印）贡献极大。
做武将卡/产品卡时，把背景铺满细密纹样，不要留大白边。

---

## 三、运行时关键参数（默认值基本都不够用）

```html
<a-scene mindar-image="imageTargetSrc: ./targets.mind;
                        maxTrack: 4;          /* 见下 */
                        missTolerance: 12;    /* 见下 */
                        warmupTolerance: 8;
                        autoStart: false;
                        uiLoading: no; uiError: no; uiScanning: no;">
```

### `maxTrack` 默认是 1 —— 多卡玩法必须调高

MindAR 默认**同时只跟踪 1 张图**。做「多张卡牌同时出现」的玩法
（卡牌对战、多人互动）如果不改这个参数，第二张卡永远不会被识别，
而且不会报任何错，只是「扫不出来」。

调成 `4` 即为最多同时 4 张。注意这是**计算成本**，每张图都要跑一次
FREAK 匹配，手机上 4 张已是可观开销，别盲目调大。

### `missTolerance` 默认 5 —— 实体卡牌手持场景太紧

单位是帧。默认 5 帧在「手机拿在手里扫桌面的卡」这种场景下会导致
位姿频繁丢失重来（手抖 + 阴影扫过）。实测调到 **12** 明显稳定。

### 其他

- `warmupTolerance` 适当调大（如 8）能让刚进入画面时更宽容。
- `autoStart: false` + 手动 `.start()` 是必要的：**必须先等用户手势**，
  否则 iOS 上 `getUserMedia` 会被拒。
- 三个 `ui*: no` 关掉内置 UI，换成自己的引导层，产品体验差很多。

---

## 四、运行时事件顺序（调试时按这个排查）

搞不清「卡在哪一步」时，按这个顺序打点：

```
start()
  → getUserMedia()                    ← 权限/摄像头问题在这里暴露
  → video loadedmetadata
  → _startAR()                        ← 异步，加载并解析 .mind
  → controller.addImageTargets(.mind)
  → dummyRun
  → emit("arReady")                   ← 模型就绪，可以开始找了
  → processVideo 循环
      → emit("targetFound") / ("targetLost")
```

**`arReady` 是「模型解析成功」的分界点。** 如果迟迟不触发，
问题在模型文件或 WebGL，不在摄像头。

建议在页面上挂 DOM 可见的状态标记（`data-ar-state` 等），
而不是只 `console.log`——这样无头测试和人工都能读。

---

## 五、无头浏览器端到端自动验证

WebAR 最难的是「改完不知道有没有坏」，只能拿手机手测。
用**合成假摄像头**可以做到全自动。

### 1. 需要 WebGL —— 所以绝不能加 `--disable-gpu`

MindAR 的 tfjs kernel 走 WebGL。加 `--disable-gpu` 会连 SwiftShader
一起关掉，然后在 `Detector` 构造时崩，报错是**极具误导性**的：

```
Cannot read properties of undefined (reading 'get')
```

这个报错和 GPU 完全看不出关系。正确姿势：

```bash
--use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader
# 千万不要加 --disable-gpu
```

同时**在页面里加 WebGL 可用性预检**，给用户可读的报错，
而不是让上面那句崩在 catch 不到的地方。

### 2. 用 Y4M 合成视频当假摄像头

```bash
--use-file-for-fake-video-capture=/path/to/card_view.y4m
```

Y4M（YUV4MPEG2）需要手写，格式要点：

```
YUV4MPEG2 W480 H640 F30:1 Ip A1:1 C420mpeg2
FRAME
<Y 平面 W*H 字节><U 平面 (W/2)*(H/2)><V 平面 (W/2)*(H/2)>
FRAME
...
```

- 色彩矩阵按 **BT.601 limited range** 填（16-235），否则浏览器侧颜色会偏。
- 每帧前面 6 字节 `FRAME\n`，第一行是文件头。
- 给个带噪声的背景 + 把目标图**按接触阴影**合成进去，识别率接近真实。

### 3. 让页面把状态回报给测试脚本

起本地 `http.server`，额外加一个 `/__state` POST 端点，
把页面打点的阶段追加写入 JSONL。测试脚本再去读，
就能断言「有没有走到 arReady」「锁到的是哪张卡」。

这样一条命令就能验证：**页面启动 AR → 拿到视频 → 模型解析成功
→ 锁定卡牌 → 认出是哪张**。

---

## 六、部署要求

WebAR 必须 **https**（`getUserMedia` 的安全上下文要求）。
本地 `http://localhost` 可以，手机访问必须走公网 https。

静态站点直接部署，注意把 `vendor/`（A-Frame、MindAR）**本地化**——
不要依赖 CDN，国内访问不稳且会被墙，页面会白屏。

---

## 七、验证清单

1. 编译产物用 `importData()` 走运行时路径校验：目标数、tracking points
2. **打印每张图的特征点数**，低于 300 就回去改图（加纹理）
3. 无头冒烟：`--use-file-for-fake-video-capture` + 状态回报端点，
   断言 `arReady` 与 `targetFound`
4. 参数复查：`maxTrack` 是否够多卡、`missTolerance` 是否够宽容
5. 真机验收：https 链接 + 至少两台不同机型（iOS Safari / Android Chrome）
