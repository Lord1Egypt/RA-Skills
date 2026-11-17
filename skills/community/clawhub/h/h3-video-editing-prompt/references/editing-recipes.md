# H3 视频编辑精简配方

仅在需要可复制骨架或处理异常时读取本文件。通用判断以 `../SKILL.md` 为准。

## 0. 三输入 Ref 条件模式

输入关系：带蒙版 Ref 视频负责目标定位与表演，参考图负责新外观，独立音频负责最终声音或声音参考。

```text
<Subject 1> is the masked performance carrier in <Video 1>, providing visible pose, motion, expression, gaze, mouth movement, and timing rather than retained appearance inside the overlay.
<Subject 2> is the target person or object in <Picture 1>, providing the complete appearance inside the overlay.
<Video 1> is the reference-condition video for the target edit, providing the shot, camera, scene, geometry, contact, occlusion, and temporal performance.
<Audio 1> is the separately supplied synchronized audio signal used unchanged in the final video.
```

最后一行只在独立音频确实作为最终音轨、且时长和起点已与视频对齐时使用，对应 `audio reuse` / `fully_copy`。若只借音色或风格，改为 `audio reference` / `reference`，且不把波形当口型时间轴。

人物目标：`<Subject 2>` 继承 Ref 视频逐时刻可见的眉眼、视线、嘴角、头身姿态、手势、节奏和情绪表现。普通物体目标只继承蒙版载体的中心、占位、朝向、缩放、运动路径、速度、接触与遮挡，不写情绪或口型。

独立音频与 Ref 视频原口型同步时，使用第 1 节骨架里的联合约束。若是新台词或不同时间轴，删除“保留精确源唇形”的句子，改为：

```text
Her brows, eyelids, gaze, head motion, posture, gestures, and overall performance timing continue from <Video 1>, while her lips and jaw articulate the final signal in <Audio 1>. No hand-written word, syllable, or phoneme timing is imposed; precise synchronization is completed by a dedicated audio-driven lip-sync or face-reenactment stage when needed.
```

### 反相伪彩 + 跨切镜持续替换

适用于“整个人被蓝绿负片／伪彩覆盖，内部五官与动作仍可读；切镜后目标只剩局部入镜”的素材。

```text
<Subject 1> is the same marked target character wherever any part of that character appears in <Video 1>, including full, partial, cropped, edge-of-frame, foreground, and post-cut appearances. The false-colour overlay identifies the character but is not target content.
```

`detailed_description` 必须按实测切点拆镜头，不能只写 `[Shot 1]`：

```text
[Shot 1] Every visible part of <Subject 1> carries the complete appearance of <Subject 2>. The false-colour appearance is not carried over; source frames provide pose, motion, expression, mouth trajectory, contact, and occlusion only.

[Shot 2] At {MEASURED_CUT_TIME}, a hard cut changes the composition. <Subject 1> remains {PARTIAL_POSITION_AND_CROP}. Every visible portion continues to carry the same <Subject 2> identity established in [Shot 1]. The cut changes framing and visible area only; it does not reset the replacement, restore the source character, or turn the partial target into unmarked scenery.
```

后接一次集中排除：`no green, cyan, blue, negative colour, transparency, fringe, hard patch, double outline, source-feature leakage, ghosting, or flicker remains`。目标贴画面边缘时保留原裁切，参考图中多出的身体部位继续留在画外。

本次已检查的素材属于这一模式：`00:03.875` 硬切后，目标只剩画面左侧局部前景。此时间仅用于该素材；其他视频必须重新测量。若仍跨切镜回源，逐镜头生成后按原切点拼接。

## 1. 蒙版换人：六字段骨架

先替换所有花括号。不存在或未接入音频时，删除全部 `<Audio 1>` 和 `audio reuse` 内容，按第 2 节改写。

```text
subject_definitions:
<Subject 1> is the masked performer in <Video 1>. Only the appearance inside the marked region is rebuilt; the visible pose, motion, timing, and unmasked body parts remain source-owned.
<Subject 2> is the complete target appearance in <Picture 1>: {reference appearance anchors}.
<Video 1> is the source video for the target edit, providing the shot structure, body position, motion, visible facial performance, lighting, perspective, occlusion, and timing.
<Audio 1> is the separately supplied final audio signal, synchronized to <Video 1> and reused unchanged.

summary:
[video editing + reference generation + audio reuse] The target video is an edited version of <Video 1>. The masked performer carries the complete appearance of <Subject 2>, while the source performance and scene timing remain unchanged and the synchronized final signal from <Audio 1> is used. No other figure is altered.

retention_analysis:
<Subject 1> (appears in {shots}): partially_preserved - {unmasked body parts}, pose, motion, position, and timing are retained; appearance inside the marked region is rebuilt as <Subject 2>.
<Subject 2> (appears in {shots}): attribute_transfer - the complete reference appearance is transferred without the reference picture's background, lighting, camera angle, or pose.
<Video 1> (edit source): partially_preserved - shot structure, scene, motion, visible performance, timing, lighting, perspective, contact, and occlusion are retained.
<Audio 1>: fully_copy - the separately supplied synchronized final signal is reused unchanged and serves as the timing check for the visible articulation.

detailed_description:
[Shot 1] {composition and visible source scene}. The masked performer carries the complete appearance of <Subject 2>: {shape, face, hair, body, clothing, accessories}. {source appearance inside the mask} is not carried over. Her position, scale, pose, weight shifts, limb paths, head motion, speed, pauses, and secondary motion follow <Video 1>. Her expression and gaze retain the visible brow, eyelid, eye-line, blink, and facial-tension sequence from the source. Her visible articulation follows <Video 1>: the upper- and lower-lip contours, mouth corners, jaw opening, visible teeth and tongue, full closures, pauses, and coupled head motion keep the source frames' timing. <Audio 1> is reused unchanged and validates the same openings, closures, sustained sounds, pauses, breaths, and emphasis. {occluders and held props} keep their exact position, motion, contact, and depth order. Her lighting and colour temperature come from the source scene; joins at {boundaries} remain continuous with no seam or colour break. Every other figure keeps their exact appearance, position, motion, timing, and depth order. Nothing not visible in <Video 1> is added. No new dialogue or event appears.

overall_soundscape:
The separately supplied synchronized final track from <Audio 1> is reused unchanged.

non_diegetic_music:
N/A
```

不要写 `frame for frame`、`perfectly exact` 等保证性措辞；提示词只表达期望归属，不能证明输出精度。

## 2. 只输入视频帧的节点

若节点不接收音频，骨架做四处修改：

1. `summary` 删除 `+ audio reuse` 和原音轨保留句。
2. 删除 `<Audio 1>` 定义及保留分析。
3. 口型段改为：

```text
Her upper- and lower-lip contours, mouth corners, jaw opening, visible teeth and tongue, full closures, pauses, and coupled head motion keep the exact visible sequence and timing from <Video 1>. No audio-based synchronization is claimed in this generation pass.
```

4. 两个声音字段均写 `N/A`，除非用户明确要求由后续节点生成新声音。

生成后将未修改的原音轨重新封装回成片。需要精确口型时，继续做专用 audio-driven lip-sync 或 face reenactment；不要继续堆提示词。

## 3. 不透明嘴部遮罩

不透明遮罩已经抹掉唇形，不能说“保留源嘴形”。

- 有同步音频并真实接入：只可要求按音频生成近似开闭口、持续音和停顿；明确最终可能需要专用口型重演。
- 无音频：默认中性闭口，或使用用户提供的可靠台词与对齐数据。
- 不得人工按汉字、单词、音节或音素编时间表。

## 4. 蒙版半途出现

提示词不能保护未标记时段。处理方式：

1. 全帧测得第一帧有效蒙版和镜头切点。
2. 未标记段不进入 H3；只生成标记段。
3. 音频在同一时间点切片，拼接后保持连续。
4. 输出统一 fps、尺寸、像素格式和时间基。
5. 起点位于镜头内时留短重叠并检查接缝；位于硬切点时直接拼接。

不要在提示词中写 `before the mask appears, nothing changes`；这不是有效边界。

## 5. 成片口型诊断

先比较源视频、生成视频和最终封装文件：

| 现象 | 优先检查 | 处理 |
|---|---|---|
| 全程固定提前或滞后 | 解码起点、音频 priming、重采样、封装时间戳 | 实测 lag 后校正音轨或时间戳 |
| 个别闭口或元音错误 | 生成嘴形本身 | 专用音频驱动 lip-sync / face reenactment |
| 越到后面越偏 | fps、帧数、总时长、sample rate、time base、变速 | 先修时间轴，再做口型 |
| 画面人物并非发声者 | 声源归属 | 不要让听者去匹配别人的声音 |
| 前半段构图消失 | 未标记帧也进入了 H3 | 按第 4 节切段重做 |

判断口型时同时看：上下唇轮廓、嘴角、下颌开合、牙齿与舌头可见度、完整闭口帧、停顿、呼吸、重音以及头部联动。只看“有没有张嘴”不够。

## 6. 多人物与遮挡

人物替换至少写两类归属：

```text
The masked performer is the only figure whose appearance comes from <Subject 2>.
Every other figure keeps their exact appearance, position, motion, timing, and depth order from <Video 1>.
```

发丝、眼镜、麦克风、手、衣袖、杯子等压在重建区域前方时，各自保留位置、运动、接触点和深度顺序。嘴或手持有的道具单独写，避免被人物重建一起抹掉。

## 7. 其他替换类型

### 物体

- 外观来自参考；位置、朝向、占位、速度、轨迹、抓握点、接触阴影与遮挡来自源视频。
- 大小冲突默认保持源占位，优先保证抓握与遮挡自洽。
- 新物体不因“看起来更重或更轻”而改变源运动速度。

### 服装

- 参考图提供版型、颜色、纹样、材质和配件。
- 源身体驱动贴合、褶皱、摆动和下摆轨迹；不保留参考图的平铺或模特姿势。

### 背景

- 参考图提供可见环境元素。
- 透视、视差、镜头、景深位置和前景遮挡来自源视频；不复制参考图自身机位。

### 画内文字

- 原文逐字保留，不翻译。
- 字体、字号、行距、颜色和留白来自参考；透视、表面形变、运动和遮挡来自源视频。

### 移除

- 不为被移除物创建新的 `<Subject N>`。
- 描述移除后可见的背景延伸、光影回填和无残影结果。

## 8. 最小自检

- 六字段名称和顺序正确。
- 只使用官方标签。
- 遮罩内外的外观归属没有冲突。
- 音频文件存在且节点收到音频，才写 `<Audio 1>` 与 `audio reuse`。
- 源嘴形与音频共同约束时，没有让音频覆盖源嘴形轨迹。
- 反相／伪彩遮罩没有把遮罩色当成目标外观；内部可见几何与表演仍归源视频。
- 多镜头素材不是只写 `[Shot 1]`；每个切点都重新声明同一 `<Subject 2>`，包括局部出画和前景碎片。
- 无音轨或嘴形被抹除时，没有承诺逐帧同步。
- 已漂移成片走测量与专用流程，不再只改提示词。
- 字符数目标约 7000，硬性不超过 10000。
