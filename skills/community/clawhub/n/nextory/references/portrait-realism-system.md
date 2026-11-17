# 人像真实感增强系统

## 目标

让人像更像真实商业摄影，而不是假脸、塑料皮肤、僵硬摆拍或过度磨皮。

适用：
- 头像
- 半身人像
- 全身模特
- 穿搭图
- 品牌目录图
- 参考图人物高保真生成

## 一、人像真实七层

### 1. 身份保真

参考图人物任务必须锁定：
- 脸型轮廓
- 眉眼比例
- 眼距与眼型
- 鼻梁与鼻尖形态
- 唇形与嘴角
- 发际线、分缝、发量、发尾形态
- 肤色冷暖
- 肩颈线条与体态

写法：
```text
保持图1人物的脸型轮廓、眉眼比例、鼻梁高度、唇形、发型分缝、肤色冷暖、肩颈线条和整体身份感不变。
```

English:
```text
Preserve the facial outline, brow-eye proportions, eye spacing, nose bridge, lip shape, hairstyle parting, skin tone, shoulder-neck line and overall identity impression from image 1.
```

### 2. 皮肤真实

避免塑料皮肤和过度磨皮。写自然纹理，但不要过度强调瑕疵。

可用表达：
- `真实皮肤纹理`
- `轻微毛孔`
- `自然肤色变化`
- `鼻翼、眼下、嘴角保留细微阴影`
- `不过度磨皮，不过度锐化`

English:
```text
realistic skin texture, subtle pores, natural skin tone variation, gentle under-eye and nose-side shadows, no over-smoothed skin
```

### 3. 眼神真实

眼神要有目标，眼神光要有来源。

可用表达：
- `视线看向镜头附近，略偏镜头左侧`
- `眼神平静自然，不夸张睁大`
- `眼神光来自左前方主光，双眼高光方向一致`
- `眼睑、卧蚕和眼下阴影自然`

English:
```text
calm natural gaze slightly off-camera, consistent catchlights from the front-left key light, realistic eyelids and subtle under-eye shadows
```

### 4. 表情真实

真实表情通常轻微、不对称、不用力。

可用表达：
- `轻微放松的嘴角`
- `面部肌肉自然放松`
- `不露齿或轻微自然微笑`
- `左右表情有轻微自然差异`

English:
```text
relaxed micro-expression, slight natural asymmetry, soft mouth corners, no forced smile
```

### 5. 姿态真实

必须给身体重心和支撑点。

可用表达：
- `身体重心落在右腿，左腿轻微放松`
- `肩膀自然下沉，一侧肩线略低`
- `脊柱自然伸展，不夸张后仰`
- `手臂与身体保持自然间隙`

English:
```text
natural weight shift, relaxed shoulders, slight shoulder asymmetry, natural spine alignment, arms resting with natural spacing from the body
```

### 6. 手部真实

手部要简单、低风险、符合动作逻辑。

推荐：
- `手部动作简单`
- `手指自然微弯`
- `手腕放松`
- `不遮挡产品关键结构`
- `手部不是视觉重点`

English:
```text
simple relaxed hands, gently curved fingers, relaxed wrists, hands not covering key product details, hands not emphasized
```

避免复杂：
- 手指交叉首饰
- 多手势
- 抓握透明物
- 贴脸遮挡
- 与肩带/头发/首饰复杂重叠

### 7. 头发真实

头发是 AI 感高发区，要写边缘和光线。

可用表达：
- `发丝边缘自然，有少量细碎发`
- `头发受光方向与脸部一致`
- `发顶不过度光滑`
- `发尾有自然层次和轻微不规则`

English:
```text
realistic hair edges, a few fine flyaway strands, hair highlights consistent with face lighting, natural layered hair ends
```

## 二、镜头与景别建议

| 人像类型 | 镜头建议 | 写法 |
| --- | --- | --- |
| 头像 | 85mm / 100mm | `85mm portrait lens, head-and-shoulders framing` |
| 半身 | 50mm / 70mm | `medium portrait framing, natural facial proportion` |
| 全身 | 50mm 左右 | `full-body fashion catalog framing, minimal body distortion` |
| 生活方式 | 35mm / 50mm | `natural lifestyle perspective, contextual background` |

避免全身图使用过强广角，否则身体比例容易变形。

## 三、光线建议

### 柔和商业人像

```text
左前上方大面积柔光作为主光，右侧微弱补光，鼻侧和下颌保留柔和阴影，背景轻微虚化。
```

English:
```text
large soft key light from the upper front-left, subtle fill from the opposite side, gentle nose-side and jawline shadows, softly separated background
```

### 自然窗边人像

```text
自然窗光从画面左侧进入，脸部高光柔和，暗部不过黑，皮肤保留自然纹理。
```

English:
```text
soft window light from camera left, gentle highlights on the face, open shadows, realistic skin texture
```

### 品牌目录人像

```text
干净棚拍光线，面部与服装都清晰，背景不抢主体，姿态端正自然。
```

English:
```text
clean studio catalog lighting, face and garment both clearly visible, low-distraction background, natural upright pose
```

## 四、可复制人像模板

### 高保真自然人像

```text
以图1作为人物参考，保持脸型轮廓、眉眼比例、眼距、鼻梁、唇形、发型分缝、肤色冷暖、自然妆感、肩颈线条和整体身份感不变。表情为轻微放松的自然神态，嘴角轻微放松，眼神看向镜头附近但不僵硬直视。身体重心自然偏向一侧，肩膀放松，手部动作简单且手指自然微弯。使用 85mm 人像镜头，中浅景深，左前上方柔和主光，右侧轻微补光，保留真实皮肤纹理、轻微毛孔、自然肤色变化、真实发丝边缘和柔和下颌阴影。
```

English:
```text
Use image 1 as the person reference. Preserve the facial outline, brow-eye proportions, eye spacing, nose bridge, lip shape, hairstyle parting, skin tone, natural makeup, shoulder-neck line and overall identity impression. Use a relaxed micro-expression with soft mouth corners and a calm gaze near the camera, not a stiff direct stare. The body weight shifts slightly to one side, shoulders relaxed, hands simple with gently curved fingers. Shot with an 85mm portrait lens, medium-shallow depth of field, soft key light from the upper front-left and subtle fill from the opposite side. Preserve realistic skin texture, subtle pores, natural skin tone variation, realistic hair edges and soft jawline shadows.
```

### 全身商业模特

```text
专业时装模特全身目录图，保持参考人物的身份感、发型、肤色、体态和肩颈线条不变。模特采用自然站姿，身体重心落在一侧腿部，另一侧膝盖轻微放松，肩线自然，双手动作简单，不遮挡服装结构。使用 50mm 左右镜头，减少身体变形，背景干净，柔和棚拍光线，服装版型、材质纹理和身体接触阴影清晰可见。
```

English:
```text
Professional full-body fashion catalog image. Preserve the identity impression, hairstyle, skin tone, posture and shoulder-neck line from the reference person. The model stands naturally with weight shifted to one leg, the other knee slightly relaxed, natural shoulder line and simple hands that do not cover the garment structure. Use around a 50mm lens to minimize body distortion, clean background, soft studio lighting, clear garment silhouette, fabric texture and natural contact shadows.
```

## 五、人像负面提示词

使用质量控制词：
```text
plastic skin, waxy skin, over-smoothed face, distorted face, wrong facial proportions, unnatural smile, stiff pose, mannequin pose, glassy eyes, mismatched catchlights, bad hands, extra fingers, missing fingers, twisted fingers, distorted shoulders, unrealistic waist, harsh shadow, overexposed skin, blurry face
```

## 六、人像自检

输出前检查：
- 是否保留了参考人物的身份感
- 是否写清表情和眼神
- 是否有身体重心和肩线
- 是否降低了手部复杂度
- 是否保留皮肤真实纹理
- 是否写清头发边缘和光线
- 是否避免夸张磨皮、假笑、过度摆拍
