# 消除 AI 感完整指南

## 一、AI 感的来源

AI 生成图片常见的"不真实"特征：

1. **过度完美的皮肤** - 像塑料/蜡像，没有毛孔和纹理
2. **不自然的眼神** - 高光位置错误，瞳孔形状异常
3. **畸形的手部** - 手指数量不对，关节扭曲
4. **光影逻辑错误** - 阴影方向不一致，光源混乱
5. **边缘光晕** - 物体边缘有奇怪的 glow/halo
6. **过度饱和** - 颜色过于鲜艳，缺乏真实世界的灰度

---

## 二、提示词加法（增加真实感）

### 人像类

**皮肤质感：**
```
skin pores, realistic skin texture, natural skin imperfections,
subtle freckles, fine lines, skin details
```

**眼睛自然化：**
```
natural eye reflection, realistic iris, catchlight in eyes,
detailed eyelashes, natural eye shape
```

**摄影设备（增加专业感）：**
```
Canon EOS R5, 85mm lens, f/1.8, shallow depth of field,
professional photography, editorial style
```

**光线描述：**
```
golden hour lighting, soft natural light, window light,
overcast lighting, cinematic lighting
```

### 产品类

**材质质感：**
```
product photography, studio lighting, soft shadows,
realistic material texture, detailed surface,
professional product shot, white background
```

**光线控制：**
```
three-point lighting, rim light, key light, fill light,
softbox lighting, clean shadows
```

### 风光/建筑类

**环境真实感：**
```
natural lighting, realistic shadows, atmospheric perspective,
weather conditions, time of day, location specific
```

### 贴身服饰 / 内衣类

**结构与贴合真实感：**
```
natural fabric tension, realistic garment fit, accurate strap placement,
natural waistband placement, subtle contact shadows, structured fitted top,
realistic decorative fabric edge, lightweight patterned fabric, realistic seam placement
```

**皮肤与面料接触：**
```
realistic skin texture, natural body contours, subtle compression from elastic edges,
soft clavicle shadows, natural waist curve, realistic stretch fabric behavior
```

---

## 三、提示词减法（去除 AI 感）

### 避免使用的词汇

**过度美化类：**
- ❌ beautiful, gorgeous, stunning, perfect
- ❌ flawless skin, perfect skin, porcelain skin
- ❌ ideal, ultimate, best quality

**模糊描述类：**
- ❌ high quality, detailed, masterpiece
- ❌ professional (单独使用)

**贴身服饰误判风险类：**
- ❌ 任何低龄化、学生化、成人化或挑逗化表达
- ❌ 不要把敏感词放进最终 prompt 或 negative prompt
- ❌ perfect doll body, impossible waist, exaggerated anatomy

**AI 特征触发类：**
- ❌ anime, cartoon, illustration (写实场景)
- ❌ dreamy, ethereal, magical (除非需要)

### 替换方案

| ❌ 避免 | ✅ 替换为 |
|--------|----------|
| beautiful woman | woman with natural features, realistic portrait |
| perfect skin | skin with natural texture, visible pores |
| stunning landscape | landscape photography, natural lighting |
| gorgeous eyes | realistic eyes with natural catchlight |
| flawless | natural, authentic, realistic |

---

## 四、负面提示词模板

### 通用负面提示词

```
low quality, worst quality, bad anatomy, bad hands, text, error,
missing fingers, extra digit, fewer digits, cropped, jpeg artifacts,
signature, watermark, username, blurry, deformed, ugly, duplicate,
morbid, extra fingers, mutated hands, poorly drawn hands,
poorly drawn face, mutation, extra limbs, extra arms, extra legs,
malformed limbs, fused fingers, too many fingers, long neck,
cross-eyed, mutated hands, polar lowres, bad face, cloned face,
amputee, missing arms, missing legs, extra foot, bad knee,
extra knees, more than 2 legs, more than 2 foot, malformed knees,
bad feet, bad tooth, fewer digits, deformed, disfigured,
floating limbs, disconnected limbs
```

### 人像专用负面提示词

```
plastic skin, wax skin, doll-like, uncanny valley, fake smile,
unnatural pose, stiff pose, exaggerated makeup, overexposed skin,
smooth skin, poreless skin, anime face, cartoon face,
unnatural eyes, dead eyes, crossed eyes, wall-eyed
```

### 产品专用负面提示词

```
cluttered background, busy background, dirty, damaged, worn,
scratched, fingerprints, dust, poor lighting, harsh shadows,
overexposed, underexposed, color cast, distorted perspective
```

---

## 五、参数设置建议

### CFG Scale（提示词遵循度）

| 场景 | 推荐值 | 说明 |
|------|--------|------|
| 写实人像 | 5-7 | 过低会偏离提示词，过高会过度锐化 |
| 产品摄影 | 7-8 | 需要精确遵循产品描述 |
| 艺术创作 | 3-5 | 给 AI 更多创意空间 |

### Sampling Steps（采样步数）

| 画质需求 | 推荐值 |
|----------|--------|
| 快速预览 | 20-25 |
| 标准质量 | 30-40 |
| 高质量 | 50-80 |

### 分辨率建议

| 用途 | 推荐尺寸 |
|------|----------|
| 社交媒体 | 1024x1024, 1024x1536 |
| 电商产品 | 1536x1536, 2048x2048 |
| 海报印刷 | 2048x3072, 2560x3840 |

---

## 六、后期优化技巧

### 1. 局部重绘（Inpainting）

**适用场景：**
- 手部修复
- 眼部调整
- 去除穿帮元素

**操作步骤：**
1. 生成基础图片
2. 标记需要修复的区域
3. 使用 inpainting 功能重新生成该区域
4. 保持其他区域不变

### 2. 图生图（Img2Img）

**适用场景：**
- 调整整体风格
- 改变光线氛围
- 细化细节

**参数建议：**
- Denoising strength: 0.3-0.6（越低越接近原图）
- 配合 ControlNet 使用效果更佳

### 3. ControlNet 应用

| 预处理器 | 用途 |
|----------|------|
| Canny | 边缘控制，保持轮廓 |
| Depth | 深度控制，保持空间关系 |
| OpenPose | 姿态控制，人物姿势 |
| Lineart | 线稿控制，动漫/插画风格 |

---

## 七、各场景避坑清单

### 人像摄影

**检查清单：**
- [ ] 手指数量正确（5根）
- [ ] 眼睛高光位置一致
- [ ] 瞳孔形状自然
- [ ] 皮肤有纹理（非塑料感）
- [ ] 牙齿数量正常
- [ ] 耳朵结构正确
- [ ] 颈部与头部连接自然

### 产品摄影

**检查清单：**
- [ ] 产品边缘清晰（无 halo）
- [ ] 阴影方向一致
- [ ] 材质质感真实
- [ ] 背景干净
- [ ] 透视关系正确
- [ ] 比例关系合理

### 室内场景

**检查清单：**
- [ ] 家具比例正确
- [ ] 光影逻辑一致
- [ ] 材质区分明显
- [ ] 空间透视合理
- [ ] 装饰品摆放自然

### 户外风光

**检查清单：**
- [ ] 地平线水平
- [ ] 天空与地面过渡自然
- [ ] 植被形态合理
- [ ] 水面反射正确
- [ ] 云层形态自然

---

## 八、真实摄影参考

### 光线类型

**自然光：**
- Golden Hour（日出后/日落前1小时）- 暖色调，长阴影
- Blue Hour（日出前/日落后）- 冷色调，柔和光线
- Overcast（阴天）- 均匀漫射光，适合人像
- Midday（正午）- 强烈直射光，硬阴影

**人工光：**
- Softbox（柔光箱）- 柔和均匀，产品摄影常用
- Beauty Dish（雷达罩）- 时尚人像，有眼神光
- Ring Light（环形灯）- 均匀照明，美妆/直播

### 摄影风格参考

**时尚杂志：**
- Vogue, Harper's Bazaar - 高级 editorial 风格
- 强调服装质感和模特姿态

**商业广告：**
- Apple, Nike 风格 - 简洁背景，突出产品
- 强调产品细节和使用场景

**纪实摄影：**
- National Geographic - 自然真实，讲故事
- 强调环境和人物关系

---

*持续更新中*
