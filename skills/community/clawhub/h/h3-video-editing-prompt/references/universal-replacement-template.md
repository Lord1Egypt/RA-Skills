# H3 替换编辑通用表

仅在人物以外的复杂替换，或需要检查槽位归属时读取。

## 三类来源

| 内容 | 权威来源 |
|---|---|
| 目标外观 | 参考图片或用户明确描述 |
| 位置、几何、运动、接触、遮挡 | 源视频帧 |
| 光照、透视、色温、景深 | 源场景 |

不要把参考图的影棚光、背景、机位和静态姿势带进目标视频。

## 类型速查

| 替换目标 | 参考提供 | 源视频保留 | 必须排除 |
|---|---|---|---|
| 面部身份 | 脸型、眉眼、鼻、唇、皮肤纹理、识别特征 | 头姿、表情、视线、眨眼、可见嘴形、光照 | 参考发型、妆造、服装、背景、机位 |
| 整个人物 | 发型、面部、身形、服装、鞋、配饰 | 体位、重心、动作路径、速度、节奏、站位、深度顺序 | 源人物在遮罩内的旧外观；参考图姿势、背景、光照 |
| 服装 | 版型、领口、袖型、颜色、纹样、材质、配件 | 身体姿势、贴合、褶皱、摆动、下摆轨迹 | 参考图模特姿势或平铺形态 |
| 手持物 | 形状、比例、颜色、材质、附属细节 | 位置、朝向、占位、抓握点、阴影、速度、轨迹 | 参考背景、产品光、未握持姿态 |
| 背景 | 建筑、植被、地面、天空、大气与色彩层次 | 源镜头、透视、视差、人物景深位置、前景遮挡 | 参考图机位、镜头、原有光照 |
| 文字标识 | 原文、字体、字号、字重、行距、颜色 | 贴附面的透视、运动、形变、遮挡 | 参考图背景和机位 |
| 材质表面 | 粗糙度、反射、纹理尺度、磨损 | 原物体形状、体积、位置和运动 | 参考物体形状和体积 |
| 光照影调 | 光源方向、软硬、色温、反差、高光 | 场景结构、人物、动作、机位 | 参考画面内容 |
| 移除 | 无新 Subject | 背景延伸、光影回填 | 原物、原影子、残影 |

## 蒙版归属

- 遮罩内：目标外观重建，源版本逐项写为 `not carried over`。
- 遮罩外：明确保留。
- 动作与时序：只要可见，就由源视频保留。
- 不透明遮罩：不能声称复刻已经被抹掉的几何或表演。
- 半透明遮罩：可用仍然清晰的轮廓、纹理和嘴形作为源帧锚点。
- 反相／伪彩遮罩：内部结构可读时保留源几何、动作和表演，但遮罩色、源皮肤、源服装材质与全部被污染外观都不保留。
- 跨切镜目标：`<Subject 1>` 定义为同一个持续角色；每个 `[Shot N]` 都重新引用同一 `<Subject 2>`，局部出画、画面边缘和前景碎片也不例外。

## 重建句的六个槽位

1. `APPEARANCE`：目标的形状、比例、颜色、图样、材质和附属细节。
2. `SOURCE_GEOMETRY`：位置、朝向、大小、运动轨迹、速度与姿势。
3. `SOURCE_OPTICS`：光源、色温、阴影、透视、景深。
4. `CONTACT_AND_OCCLUSION`：接触点、接触阴影、前后遮挡。
5. `SEAM`：边界连续、无色差、无重影。
6. `EXCLUDE`：参考中不迁移的内容和源对象中应消失的内容。

人物口型不要在这里自由发挥；必须按 `../SKILL.md` 的口型四分支选择唯一写法。

## 类型专用句

### 手持物

```text
Its position, orientation, occupied space, grip points, contact shadow, velocity, and motion path continue from <Video 1>; the fingers remain in front of the same surfaces and the object does not independently speed up, slow down, slide, or float.
```

### 服装

```text
Its fit, folds, stretch, sway, sleeves, and hem follow the source body pose and motion, not the reference image's flat-lay or model pose.
```

### 背景

```text
The new environment follows <Video 1>'s camera, perspective, parallax, depth of field, subject placement, and foreground occlusion rather than the reference picture's own viewpoint.
```

### 矩形或阶梯状遮罩

```text
The patch boundary does not survive in the target video; the rebuilt target and the surrounding source surface meet continuously with no straight edge, step, block, seam, or colour break.
```

### 参考主体有更多画外部分

```text
The body parts outside <Video 1>'s framing remain outside the corresponding frame edges and are not pulled into view.
```

### 切镜后只剩局部目标

```text
The hard cut changes only the composition and visible amount of <Subject 1>. Every partial, cropped, edge-of-frame, or foreground portion continues to carry the same <Subject 2> identity; the source appearance and false-colour overlay do not reappear.
```

## 可见行为

人物替换只描述可见事实：

- 表情：眉、眼睑、眼周、嘴角与松紧变化；
- 视线：落点、距离、漂移、回位、眨眼；
- 动作：头、肩、躯干、四肢、重心、速度与停顿；
- 次级运动：头发、服装和配饰的滞后与回落；
- 嘴部：使用主 Skill 的唯一口型分支。

不猜“在唱歌、直播、排练、思考”等意图，不添加源视频没有的事件。

## 检查

- 参考外观、源几何和源光学三类归属清楚。
- 遮罩内的源外观没有又被列为保留。
- 接触、遮挡、其他人物与画外部位已处理。
- 旧目标和参考图非目标内容已排除。
- 提示词没有承担时间窗或真实区域蒙版的职责。
- 每个实测切点都有独立镜头段落，跨切镜身份没有只靠全局一句话维持。
- 口型规则来自主 Skill，没有自行增加手写时间轴。
