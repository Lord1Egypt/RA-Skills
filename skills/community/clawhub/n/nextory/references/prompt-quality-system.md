# 提示词质感增强系统

## 目标

把“更高级、更有质感、更全面”拆成模型可执行的视觉决策。

使用原则：
- 不堆空泛形容词
- 不覆盖用户指定的主体、角度、产品结构和品牌限制
- 先增强画面逻辑，再增强词汇质感
- 每次只选择最适合任务的一套视觉方向

## 一、视觉导演六层

最终提示词至少补齐以下 6 层。若用户要求 1:1 复刻，只补齐参考图中已经存在或可合理推断的层，不主动大改。

### 1. 视觉焦点

写清楚观众第一眼看哪里，以及为什么会先看那里。

可用表达：
- `视觉焦点集中在产品正面 logo 与材质高光处`
- `人物面部为第一视觉中心，产品位于第二视觉中心`
- `画面通过留白和暗部收束，让视线落在主体轮廓上`
- `焦点位于面料边缘、缝线和贴合转折处`

避免：
- `突出主体`
- `更吸睛`
- `视觉冲击强`

### 2. 画面层级

把前景、中景、背景分工写清楚。

可用表达：
- `前景保留少量柔焦道具，中景为主体，背景只提供低对比空间层次`
- `产品处于前景右下 1/3 区域，人物位于中景，背景虚化为浅灰色块`
- `背景道具密度低，不抢占主体边缘`
- `保留 35%-45% 负空间作为文案或品牌呼吸区`

### 3. 镜头语言

根据任务选择一种镜头，不要混写多个冲突镜头。

| 场景 | 推荐镜头语言 | 写法 |
| --- | --- | --- |
| 电商主图 | 平视或轻微俯拍，透视克制 | `eye-level product photography, slight top angle, controlled perspective` |
| 人像大片 | 50mm/85mm，中浅景深 | `85mm portrait lens, soft background separation, natural facial proportion` |
| 服装/内衣 | 50mm-70mm，减少身体变形 | `medium focal length, minimal body distortion, clean full-body proportion` |
| 产品细节 | 70mm/100mm 微距 | `macro detail shot, shallow depth of field, crisp material edge` |
| 生活方式图 | 35mm/50mm，环境叙事 | `35mm lifestyle photography, contextual environment, natural perspective` |

### 4. 光线逻辑

至少写清主光方向、光质、阴影和高光位置。

可用表达：
- `large softbox from upper left, gentle falloff, soft shadow falling to the lower right`
- `window light from camera left, subtle fill on the opposite side, natural catchlight`
- `controlled rim light outlining the product edge, no harsh hotspot`
- `low-contrast diffused lighting, visible but soft fabric folds`

光线不要互相冲突：
- 不要同时写 `hard spotlight` 和 `flat shadowless lighting`
- 不要同时写 `backlit silhouette` 和 `front-facing clear logo`，除非说明补光
- 透明/高反光材质必须写 `controlled reflections`

### 5. 色彩系统

不要只写“大地色、高级灰、莫兰迪”。要写主色、辅助色、点缀色、饱和度、对比度。

稳定结构：
```text
主色为[颜色1/颜色2]，辅助色为[颜色]，点缀色控制在小面积[颜色]，
整体低/中饱和，黑位不死黑，高光不过曝，肤色或产品色保持真实。
```

示例：
- `主色为暖灰与骨白，辅助色为浅驼色，少量香槟金作为点缀，整体低饱和、低对比`
- `主色为干净白与冷灰，点缀少量电光蓝，形成运动科技感`
- `主色为奶油色、浅木色和自然肤色，整体暖调但不过黄`

### 6. 材质与真实细节

每条高质感 prompt 至少写 2-4 个材质细节。

| 材质 | 可执行写法 |
| --- | --- |
| 皮肤 | `visible skin pores, natural fine lines, subtle uneven skin texture` |
| 棉 / 莫代尔 | `soft matte cotton texture, fine ribbed knit, natural fabric stretch` |
| 蕾丝 / 网纱 | `delicate lace edge, fine mesh transparency, realistic seam placement` |
| 缎面 / 真丝 | `soft satin sheen, controlled highlights, smooth drape` |
| 皮革 | `fine leather grain, subtle creases, controlled specular highlights` |
| 金属 | `brushed metal edge, small clean highlights, no blown-out reflection` |
| 玻璃 / 亚克力 | `transparent edge thickness, controlled refraction, clean shadow` |
| 纸张 / 包装 | `matte paper texture, crisp folded edges, clean printed surface` |

真实感细节可以包括：
- 轻微面料褶皱
- 自然皮肤纹理
- 合理接触阴影
- 不完全对称的头发或衣摆
- 产品落地阴影
- 金属边缘的小面积高光

## 二、场景化增强配方

### 人像 / 模特

涉及人物自然度时，先读 `references/natural-human-system.md`。
涉及人像真实感时，再读 `references/portrait-realism-system.md`。

优先补齐：
- 面部是否为第一焦点
- 镜头焦距与景别
- 姿态是否自然
- 皮肤是否保留纹理
- 眼神光是否合理

高质感表达：
```text
professional fashion model with natural facial proportions, relaxed professional posture,
85mm portrait lens, soft background separation, natural skin texture,
subtle catchlight in the eyes, controlled makeup finish, no plastic skin
```

### 服装 / 内衣 / 贴身服饰

涉及平台拦截或贴身服饰时，先读 `references/policy-safe-generation.md`，最终提示词使用商业服饰目录表达。

优先补齐：
- 版型结构
- 覆盖度
- 贴合关系
- 面料张力
- 安全合规语境

高质感表达：
```text
commercial apparel catalog photography, professional fashion model,
realistic garment fit, natural fabric tension, accurate strap placement,
visible seam construction, subtle skin-contact shadows, polished retail styling
```

### 产品摄影

涉及电商产品主图、详情页、四视图或材质特写时，先读 `references/ecommerce-product-polish-system.md`。

优先补齐：
- 产品结构是否保持
- logo 或正面是否清晰
- 产品角度与镜头角度是否区分
- 材质高光是否被控制
- 背景是否抢主体

高质感表达：
```text
premium product photography, controlled studio lighting,
clean edge definition, realistic material texture, soft contact shadow,
controlled reflections, uncluttered background, accurate product proportions
```

### 电商详情页 / 九宫格

优先补齐：
- 每张图承担不同销售任务
- 整组视觉统一
- 产品结构不漂移
- 信息层级清楚
- 留白与文案区明确

高质感表达：
```text
cohesive e-commerce visual set, consistent product color and structure,
clear hierarchy for hero, detail, material, fit, lifestyle and size information,
clean layout, premium brand pacing, restrained props
```

### 场景合成

优先补齐：
- 透视匹配
- 光源匹配
- 接触阴影
- 比例真实
- 边缘无光晕

高质感表达：
```text
matched perspective and scale, consistent light direction,
natural contact shadows, realistic edge blending, no halo,
product integrated into the environment without changing its structure
```

## 三、词汇替换表

| 不要写 | 改成 |
| --- | --- |
| 高级感 | `low-saturation palette, controlled highlights, refined material texture` |
| 有质感 | `visible material grain, natural folds, tactile surface detail` |
| 氛围感 | `soft directional light, muted background, gentle depth separation` |
| 大牌感 | `restrained composition, premium negative space, low-density props` |
| 成人化/挑逗化表达 | `polished commercial apparel styling, professional fashion model, restrained catalog pose` |
| 干净 | `uncluttered background, clean edge definition, controlled shadows` |
| 真实 | `natural imperfections, accurate shadows, realistic material response` |
| 精致 | `crisp seams, clean edges, subtle highlights, balanced composition` |

## 四、提示词密度控制

一条最终 prompt 的密度建议：
- 4-6 个硬约束：主体、保留项、位置、角度、结构、禁止变化
- 3-5 个质感细节：光线、色彩、材质、真实瑕疵、道具密度
- 1 个明确风格方向：例如轻奢、法式、运动、极简、买手店风
- 1 个技术摄影层：镜头、景别、景深或画幅
- 1 组场景化负面提示词

如果提示词过长，优先删除空泛形容词，不删除位置、角度、材质和锁定项。

## 五、English Prompt 写法

英文提示词不要逐字翻译中文。应转成自然、可执行的摄影语言。

规则：
- 保留数字、位置、角度、比例
- 用摄影动词和名词替代中文抽象词
- 少用逗号词串，多用完整短句
- 不把“参考图”翻译成 vague reference，必须写 `use image 1 as...`

推荐句式：
```text
Use image 1 as the [subject/product/garment] reference and keep [locked attributes] unchanged.
Place [subject/product] at [position], occupying about [ratio] of the frame, shown from [angle].
Use [lighting setup], with [shadow/highlight behavior].
The palette is [dominant colors], with [accent color] used sparingly.
Emphasize [material details] and preserve realistic [skin/fabric/product] texture.
Shot with [lens/composition], [style direction], [negative constraints].
```

## 六、负面提示词生成规则

不要每次复制超长通用负面词。按任务组合：

### 通用基础

```text
low quality, blurry, distorted perspective, inconsistent lighting, overexposed, underexposed, watermark, random text, logo distortion
```

### 人像追加

```text
plastic skin, waxy skin, poreless face, uncanny valley, bad anatomy, bad hands, extra fingers, stiff pose, unnatural eyes, crossed eyes
```

### 产品追加

```text
changed product shape, wrong logo placement, distorted label, messy background, harsh reflections, floating object, missing contact shadow
```

### 服装 / 内衣追加

```text
warped garment, wrong strap placement, broken fabric pattern, distorted seams, unrealistic body proportions, stiff pose, changed garment shape, wrong color
```

### 场景合成追加

```text
mismatched perspective, mismatched scale, inconsistent shadow direction, halo edge, pasted-on look, unrealistic contact shadow
```

## 七、最终质量自检

输出前检查：
- 主体、产品或服装是否被明确锁定
- 产品位置、产品角度、镜头角度是否分别写清
- 风格词是否被拆成色彩、光线、材质和构图
- 至少有一个视觉焦点和一个背景控制策略
- 光线方向和阴影方向是否一致
- 材质是否有具体触感，而不是只写“高质感”
- 英文提示词是否保留了中文里的关键约束
- 负面提示词是否与任务匹配，没有无意义堆叠
- 若涉及参考图，是否列出保真等级、不可变项和允许变化项
- 若涉及人物，是否补齐表情、眼神、重心、手部、皮肤和服装接触
- 若涉及平台安全，最终 prompt 和负面词是否避免高风险词
