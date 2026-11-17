# Nonbana Pro (Flux) 提示词规范

## 一、平台特性

Nonbana Pro 基于 Flux 模型，具有以下特点：

- **自然语言理解强**：可以用完整句子描述，不限于标签式提示词
- **提示词跟随度高**：能较好地理解复杂描述
- **写实能力强**：原生支持高质量写实图像生成
- **多图参考**：支持多张参考图融合

---

## 二、提示词结构模板

### 标准结构

```
[主体描述] + [场景/环境] + [光线条件] + [摄影设备/风格] + [画质参数]
```

### 详细分解

**1. 主体描述（必填）**
```
- 主体类型：人物/产品/建筑/风景
- 外观特征：颜色、材质、形状、尺寸
- 状态/动作：静态展示/动态姿势/使用场景
- 细节要求：特写/全身/局部
```

**2. 场景/环境**
```
- 室内/室外
- 背景类型：纯色/渐变/实景/虚化
- 环境元素：家具、植物、装饰品等
- 氛围描述：温馨/专业/奢华/自然
```

**3. 光线条件**
```
- 光源类型：自然光/人工光/混合光
- 光线方向：正面光/侧光/逆光/顶光
- 光线质感：柔和/硬光/漫射
- 时间氛围：清晨/正午/黄昏/夜晚
```

**4. 摄影设备/风格**
```
- 相机型号：Canon EOS R5, Sony A7R IV
- 镜头参数：85mm f/1.8, 24-70mm f/2.8
- 摄影类型：product photography, portrait, editorial
- 风格参考：cinematic, documentary, commercial
```

**5. 画质参数**
```
- 分辨率：2K, 4K, 8K
- 画质描述：highly detailed, sharp focus, crisp
- 色彩：vibrant colors, muted tones, monochromatic
```

---

## 三、光线描述词汇表

### 自然光

| 类型 | 英文描述 | 效果 |
|------|----------|------|
| 黄金时刻 | golden hour lighting, warm sunlight | 暖色调，柔和阴影 |
| 蓝色时刻 | blue hour, twilight | 冷色调，神秘氛围 |
| 阴天 | overcast lighting, soft diffused light | 均匀柔和，无硬阴影 |
| 正午 | harsh midday sun, strong sunlight | 强烈对比，硬阴影 |
| 窗边光 | window light, natural window lighting | 柔和侧光，适合人像 |
| 逆光 | backlit, rim lighting | 轮廓光，氛围感强 |

### 人工光

| 类型 | 英文描述 | 适用场景 |
|------|----------|----------|
| 柔光箱 | softbox lighting, soft studio light | 产品摄影，人像 |
| 无影灯 | shadowless lighting, even illumination | 白底产品图 |
| 聚光灯 | spotlight, focused beam | 强调重点，戏剧效果 |
| 环形灯 | ring light, circular catchlight | 美妆，直播 |
| 三灯布光 | three-point lighting, key fill rim | 专业人像 |

---

## 四、设备描述词汇表

### 相机型号

```
Canon EOS R5, Canon EOS 5D Mark IV
Sony A7R IV, Sony A1
Nikon Z9, Nikon D850
Fujifilm GFX 100
Hasselblad X2D
```

### 镜头参数

**人像镜头：**
```
85mm f/1.2, 85mm f/1.4, 85mm f/1.8
135mm f/1.8, 105mm f/1.4
```

**标准变焦：**
```
24-70mm f/2.8, 24-105mm f/4
```

**广角镜头：**
```
16-35mm f/2.8, 14-24mm f/2.8
```

**微距镜头：**
```
100mm macro f/2.8, 90mm macro
```

### 摄影风格

```
product photography - 产品摄影
portrait photography - 人像摄影
editorial photography - 杂志编辑风格
commercial photography - 商业广告
lifestyle photography - 生活方式
documentary photography - 纪实摄影
fashion photography - 时尚摄影
architectural photography - 建筑摄影
food photography - 美食摄影
automotive photography - 汽车摄影
```

---

## 五、负面提示词模板

### 通用负面提示词

```
lowres, bad anatomy, bad hands, text, error, missing fingers,
extra digit, fewer digits, cropped, worst quality, low quality,
normal quality, jpeg artifacts, signature, watermark, username,
blurry, artist name, bad proportions, duplicate, morbid,
mutilated, out of frame, extra fingers, mutated hands,
poorly drawn hands, poorly drawn face, mutation, deformed,
ugly, bad anatomy, bad hands, text, error, missing fingers,
extra digit, fewer digits, cropped, worst quality, low quality,
normal quality, jpeg artifacts, signature, watermark, username,
blurry, artist name, bad proportions, duplicate, morbid,
mutilated, out of frame, extra fingers, mutated hands,
poorly drawn hands, poorly drawn face, mutation, deformed,
ugly
```

### 人像专用

```
plastic skin, wax skin, doll face, anime face, cartoon,
uncanny valley, fake smile, dead eyes, crossed eyes,
wall-eyed, malformed face, extra limbs, fused fingers,
too many fingers, long neck, double head, double face
```

### 产品专用

```
cluttered background, busy background, dirty, damaged,
worn, scratched, fingerprints, dust, poor lighting,
harsh shadows, overexposed, underexposed, color cast,
distorted perspective, warped, bent, broken
```

---

## 六、参数设置参考

### CFG Scale

| 值 | 效果 |
|----|------|
| 1-3 | 高度创意，提示词跟随度低 |
| 4-6 | 平衡创意与遵循 |
| 7-9 | 严格遵循提示词（推荐） |
| 10-15 | 过度锐化，可能出现伪影 |

### Sampling Steps

| 值 | 用途 |
|----|------|
| 20-25 | 快速预览 |
| 30-40 | 标准质量 |
| 50-60 | 高质量 |
| 80+ | 极致细节（耗时较长） |

### 推荐组合

**快速预览：**
- Steps: 25
- CFG: 7

**标准质量：**
- Steps: 35
- CFG: 7.5

**高质量：**
- Steps: 50
- CFG: 8

---

## 七、多图参考技巧

### 图1 + 图2 = 图3 模式

**材质迁移：**
```
图2的[物品]使用图1的[材质]
```

**图案迁移：**
```
图2的图案印在图1的[物品]上
```

**角度匹配：**
```
将图1产品的拍摄角度、摆放姿态、朝向完全调整为与图2参考图一致
```

### 人物 + 服装

```
[人物描述]穿着图1的衣服，[场景描述]，[光线描述]
```

### 产品 + 场景

```
图1产品放到[场景描述]，[光线描述]，保持产品角度和材质
```

---

## 八、常见场景提示词模板

### 电商白底图

```
product photography, white background, softbox lighting,
clean shadows, professional product shot, highly detailed,
sharp focus, 8k resolution, commercial photography
```

### 时尚人像

```
editorial fashion photography, natural lighting,
85mm lens, f/1.8, shallow depth of field,
professional model, realistic skin texture,
cinematic color grading, 4k resolution
```

### 室内场景

```
interior design photography, natural window light,
wide angle lens, 24mm, architectural photography,
warm and cozy atmosphere, realistic materials,
professional interior shot, 4k
```

### 美食摄影

```
food photography, natural lighting, overhead shot,
50mm lens, f/2.8, rustic background,
appetizing presentation, professional food styling,
warm tones, 4k resolution
```

### 汽车摄影

```
automotive photography, golden hour lighting,
24-70mm lens, dramatic angle, reflections,
professional car photography, cinematic,
highly detailed, 4k resolution
```

---

## 九、标签控制（K Pro）

### 使用红框保护

在不想被改变的区域添加红框，生成后去掉红框。

### 标注识别

**步骤1：** 让模型标注识别的物品
```
在图片上用中文标注，你识别的物品名称
```

**步骤2：** 基于标注精确描述
```
根据标注的[物品名称]进行[操作描述]
```

---

## 十、安全合规提示词策略

### 更稳的合规表达

**换脸场景：**
- ❌ 使用图2的脸
- ✅ 参考图2的角色特征，商业摄影风格

**时尚展示：**
- ❌ 成人化、挑逗化或暴露化表达
- ✅ 商业服饰目录风格、专业时装模特展示、端正自然姿态

**姿势描述：**
- ❌ 暧昧、迷人姿势
- ✅ 专业模特姿势、自然姿态

---

*持续更新中*
