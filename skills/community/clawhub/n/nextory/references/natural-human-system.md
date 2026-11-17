# 人物自然度提示词系统

## 目标

让人物更自然、真实、松弛，避免 AI 生成常见的假脸、僵硬姿势、塑料皮肤、错误手部和过度摆拍。

如果用户要求“人像更真实 / 真人感 / 皮肤真实 / 眼神真实”，先读 `references/portrait-realism-system.md`。

适用场景：
- 人像写真
- 模特图
- 穿搭图
- 内衣/家居服商业拍摄
- 生活方式广告
- 上传人物参考图的高保真生成

## 一、自然人物七层

### 1. 身份与专业感

人物提示词优先写成专业商业拍摄语境，尤其是贴身服饰、泳装、睡衣、家居服场景。

可用表达：
- `专业女性时装模特，成熟自然气质`
- `专业男性时装模特，干净克制的商业形象`
- `professional fashion model, polished catalog presence`

避免：
- `少女感`
- `幼态`
- `校园`
- 任何学生化、未成熟化、低龄化表达

### 2. 表情自然度

自然表情通常是轻微、不夸张、不对称的。

推荐写法：
- `轻微放松的嘴角，不露齿或自然微笑`
- `眼神自然聚焦，不刻意瞪大`
- `面部肌肉放松，表情有轻微不对称`
- `relaxed micro-expression, natural gaze, subtle asymmetry`

避免：
- `perfect smile`
- `big sparkling eyes`
- `doll-like face`
- `overly dramatic expression`

### 3. 眼神与眼部真实感

必须控制眼神光、瞳孔方向和视线目标。

可用表达：
- `视线看向镜头左侧一点，避免正面对瞪`
- `眼神光来自左前方主光，双眼高光方向一致`
- `natural catchlight, realistic iris detail, calm gaze`

常见错误负面词：
```text
dead eyes, crossed eyes, wall-eyed, mismatched catchlights, glassy eyes, over-sharpened iris
```

### 4. 姿态与重心

自然姿态要有重心、支撑点、肌肉放松。

推荐写法：
- `身体重心落在右腿，左膝轻微放松`
- `肩膀自然下沉，一侧肩线略低`
- `手臂与身体保持自然距离，不僵硬贴紧`
- `relaxed posture, natural weight shift, slight shoulder asymmetry`

避免：
- `stiff pose`
- `symmetrical mannequin pose`
- `unnatural spine curve`
- `floating limbs`

### 5. 手部自然度

如果手出现在画面中，必须写手部动作、接触点和手指状态。

推荐写法：
- `右手自然扶在腰侧，手指轻微弯曲，不遮挡产品关键结构`
- `手掌轻触桌面，指尖自然分开，关节弯曲合理`
- `hands relaxed, fingers slightly curved, natural knuckle structure`

如果手不是必要信息，优先减少手部复杂度：
- `双手不作为视觉重点`
- `手部自然放在画面边缘，不与首饰或肩带复杂交叠`
- `hands partially out of focus and not emphasized`

手部负面词：
```text
bad hands, extra fingers, missing fingers, fused fingers, twisted fingers, broken knuckles, unnatural hand pose
```

### 6. 皮肤与身体真实感

自然人物必须保留皮肤纹理和身体合理性。

可用表达：
- `真实皮肤纹理，可见轻微毛孔和自然肤色变化`
- `锁骨、肩颈、腰腹转折处有自然阴影`
- `不追求塑料般完美皮肤，保留轻微真实瑕疵`
- `realistic skin texture, visible pores, subtle skin tone variation, natural body contours`

避免：
- `flawless skin`
- `porcelain skin`
- `perfect doll body`
- `impossible waist`
- `exaggerated anatomy`

### 7. 服装与身体接触

人物自然度很大一部分来自服装如何贴合身体。

可用表达：
- `布料在肩膀、腰部和肘部形成自然张力`
- `腰头与皮肤接触处有轻微压痕但不过度`
- `肩带位置准确，沿肩线自然贴合`
- `natural fabric tension, realistic garment fit, subtle contact shadows`

## 二、人像提示词骨架

### 高保真人像

```text
以图1为成年人物参考，保持脸型轮廓、五官比例、发型分缝、肤色冷暖、自然妆感和体态不变。
表情为轻微放松的自然神态，眼神看向镜头附近但不僵硬直视。
身体重心自然偏向一侧，肩颈放松，手部动作简单且手指轻微弯曲。
使用 85mm 人像镜头，中浅景深，柔和侧光，保留真实皮肤纹理、轻微毛孔、自然阴影和真实发丝边缘。
```

English:
```text
Use image 1 as the professional fashion model reference. Preserve the facial outline, facial proportions, hairstyle parting, skin tone, natural makeup and body posture. Use a relaxed micro-expression with a natural gaze near the camera, not a stiff stare. The body weight shifts slightly to one side, shoulders relaxed, hands simple with gently curved fingers. Shot with an 85mm portrait lens, soft side lighting, medium-shallow depth of field, realistic skin texture, subtle pores, natural shadows and realistic hair edges.
```

### 商业模特图

```text
成年商业模特，姿态专业但不僵硬，身体重心清楚，肩线自然，表情克制放松。
产品/服装为视觉重点，人物表情和姿势服务于产品展示，不夸张摆拍。
皮肤保留真实纹理，服装在身体转折处有自然褶皱和张力，手部不遮挡关键结构。
```

English:
```text
Professional commercial fashion model with a relaxed posture, clear weight shift, natural shoulder line and restrained expression. The product or garment remains the visual priority. The pose supports product display without exaggerated modeling. Preserve realistic skin texture, natural garment folds and fabric tension around body curves. Hands do not cover key product details.
```

### 生活方式人物

```text
人物处于真实生活场景中，动作像被自然捕捉而不是刻意摆拍。
背景保留轻微生活痕迹但不杂乱，人物与环境有真实接触阴影。
光线来自窗边或环境光，皮肤、头发和服装受光方向一致。
```

English:
```text
The person is placed in a believable lifestyle scene, captured in a natural moment rather than an exaggerated pose. The background has subtle lived-in details without clutter. Use realistic contact shadows between the person and the environment. Window or ambient light affects the skin, hair and clothing consistently.
```

## 三、贴身服饰人物自然度

必须保持商业服饰目录语境：
- `professional fashion model`
- `commercial apparel catalog photography`
- `polished retail styling`
- `full-coverage garment styling`
- `clear garment structure`

自然度重点：
- 贴合关系真实
- 肩带和腰头位置准确
- 皮肤接触阴影自然
- 姿态端正自然，不过度摆拍
- 表情成熟克制

推荐写法：
```text
专业女性时装模特，商业服饰目录摄影语境，成熟克制的自然表情，肩颈放松，身体重心自然偏向一侧。
贴身服饰的肩带、结构化上装、腰头和下摆位置准确，布料沿身体曲线自然贴合，接触处有轻微真实阴影。
画面重点展示版型、面料、结构和穿着效果，整体端正干净，姿态自然。
```

English:
```text
Professional female fashion model in a commercial apparel catalog context, restrained expression, relaxed shoulders and natural weight shift. The straps, structured fitted top, waistband and hem openings are accurately placed. The fabric follows the body contours naturally with subtle contact shadows. Focus on fit, material, structure and wearing effect with clean polished catalog styling.
```

## 四、人物负面提示词

基础：
```text
plastic skin, waxy skin, poreless skin, doll-like face, uncanny valley, stiff pose, mannequin pose, unnatural smile, exaggerated expression
```

脸部：
```text
distorted face, asymmetrical eyes, crossed eyes, dead eyes, oversized eyes, over-smoothed face, cloned face, wrong facial proportions
```

身体：
```text
bad anatomy, impossible waist, exaggerated body proportions, twisted torso, broken neck, floating limbs, unnatural spine curve
```

手部：
```text
bad hands, extra fingers, missing fingers, fused fingers, twisted fingers, broken knuckles, unnatural hand pose
```

贴身服饰质量控制：
```text
warped garment, asymmetrical straps, broken fabric pattern, warped waistband, wrong product shape, changed color, stiff pose, exaggerated pose, messy background
```

## 五、自然度自检

输出前检查：
- 是否明确专业商业模特语境
- 表情是否是轻微自然表情，而不是夸张美化
- 眼神是否有目标，高光方向是否合理
- 身体是否有重心和支撑点
- 手部是否有简单、合理、低风险的动作
- 皮肤是否保留毛孔、纹理和自然色差
- 服装是否有真实张力、褶皱和接触阴影
- 是否避免低龄化表达、塑料皮肤、完美娃娃身材
