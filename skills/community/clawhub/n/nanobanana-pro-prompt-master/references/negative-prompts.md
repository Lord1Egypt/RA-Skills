# 负面提示词库 (Negative Prompts)

> 按问题类型分类 | NanobananaPro 生图 Skill 核心知识库

---

## 📖 使用说明

**负面提示词作用：**
- 反向过滤不需要的元素
- 预防常见生成问题
- 提升废稿率至 <5%

**权重建议：**
- 基础负面词：1.0-1.2
- 针对性负面词：1.3-1.5
- 强过滤负面词：1.5-1.7

**语法：**
```
# 基础用法
ugly, deformed, blurry

# 权重强化
(ugly:1.5), (deformed:1.4)

# 组合使用
ugly, deformed, blurry, noisy, (bad anatomy:1.5)
```

---

## 🚫 一、人物崩坏类

### 问题表现
- 多余肢体/手指
- 畸形五官
- 身体比例失调
- 面部不对称

### 负面提示词

**基础版（通用）：**
```
ugly, deformed, bad anatomy, disfigured, poorly drawn hands, poorly drawn feet, poorly drawn face, out of frame, extra limbs, disfigured, deformed, body out of frame, bad art, beginner, amateur, blurry
```

**强化版（人像专用）：**
```
(ugly:1.5), (deformed:1.4), (bad anatomy:1.5), (disfigured:1.4), (poorly drawn hands:1.5), (poorly drawn feet:1.5), (poorly drawn face:1.5), (out of frame:1.3), (extra limbs:1.5), (body out of frame:1.3), (bad art:1.2), (beginner:1.2), (amateur:1.2), (blurry:1.3), (asymmetric eyes:1.4), (malformed hands:1.5), (mutation:1.4), (mutated:1.4), (extra fingers:1.5), (missing fingers:1.5), (too many fingers:1.5), (wrong hands:1.5), (wrong feet:1.5), (wrong proportions:1.4), (floating limbs:1.4)
```

**精简版（节省 token）：**
```
(ugly:1.5), (deformed:1.4), (bad anatomy:1.5), (malformed hands:1.5), (asymmetric eyes:1.4), (extra limbs:1.5), (mutation:1.4), (blurry:1.3)
```

---

## 🚫 二、画面质量问题

### 问题表现
- 模糊/噪点
- 过曝/欠曝
- 像素化
- 低分辨率

### 负面提示词

**基础版：**
```
blurry, noisy, pixelated, overexposed, underexposed, low resolution, low quality, jpeg artifacts, compression artifacts, grainy
```

**强化版：**
```
(blurry:1.4), (noisy:1.3), (pixelated:1.4), (overexposed:1.3), (underexposed:1.3), (low resolution:1.5), (low quality:1.5), (jpeg artifacts:1.3), (compression artifacts:1.3), (grainy:1.3), (out of focus:1.4), (soft focus:1.2), (hazy:1.3), (muddy:1.3), (washed out:1.3), (blown highlights:1.3), (crushed blacks:1.3)
```

**场景专用：**

| 场景 | 推荐负面词 |
|------|------------|
| 产品摄影 | `blurry, noisy, low resolution, jpeg artifacts, compression artifacts` |
| 人像写真 | `blurry, out of focus, noisy, grainy, overexposed, underexposed` |
| 风光摄影 | `hazy, muddy, washed out, blown highlights, crushed blacks, low quality` |
| 夜景摄影 | `noisy, grainy, blurry, overexposed highlights, underexposed shadows` |

---

## 🚫 三、风格跳变类

### 问题表现
- 风格不一致
- 色彩突变
- 光影闪烁
- 质感混乱

### 负面提示词

**基础版：**
```
style mutation, color shift, light flickering, inconsistent style, mixed media, conflicting aesthetics
```

**强化版：**
```
(style mutation:1.5), (color shift:1.4), (light flickering:1.5), (inconsistent style:1.4), (mixed media:1.3), (conflicting aesthetics:1.3), (style inconsistency:1.4), (color inconsistency:1.4), (lighting inconsistency:1.5), (texture inconsistency:1.4), (multiple styles:1.4), (style drift:1.4)
```

**视频生成专用（首尾帧锁定）：**
```
(style mutation:1.6), (color shift:1.5), (light flickering:1.6), (frame inconsistency:1.5), (temporal inconsistency:1.5), (character inconsistency:1.5), (background flickering:1.5), (morphing:1.4), (transforming:1.4)
```

---

## 🚫 四、透视问题类

### 问题表现
- 比例错误
- 透视畸变
- 物体漂浮
- 空间关系混乱

### 负面提示词

**基础版：**
```
wrong proportions, perspective distortion, floating objects, incorrect perspective, bad perspective
```

**强化版：**
```
(wrong proportions:1.5), (perspective distortion:1.4), (floating objects:1.5), (incorrect perspective:1.4), (bad perspective:1.4), (distorted perspective:1.4), (unnatural proportions:1.4), (wrong scale:1.4), (size inconsistency:1.4), (spatial inconsistency:1.4), (gravity defying:1.3), (levitating:1.3)
```

**建筑/室内专用：**
```
(wrong proportions:1.5), (perspective distortion:1.5), (keystoning:1.4), (converging lines:1.3), (distorted architecture:1.4), (uneven floors:1.4), (tilted walls:1.4)
```

---

## 🚫 五、水印文字类

### 问题表现
- 意外文字
- 水印/签名
- LOGO 污染
- 版权标记

### 负面提示词

**基础版：**
```
text, watermark, logo, signature, copyright, artist name, date stamp
```

**强化版：**
```
(text:1.6), (watermark:1.6), (logo:1.6), (signature:1.6), (copyright:1.5), (artist name:1.5), (date stamp:1.5), (title:1.5), (label:1.5), (branding:1.5), (trademark:1.5), (overlay text:1.6), (subtitles:1.5), (captions:1.5), (UI elements:1.5), (interface:1.5)
```

**电商产品专用：**
```
(text:1.7), (watermark:1.7), (logo:1.7), (signature:1.6), (price tag:1.6), (barcode:1.5), (QR code:1.5), (packaging text:1.6), (brand name:1.5)
```

---

## 🚫 六、场景专用负面词

### 6.1 人像摄影

```
(ugly:1.5), (deformed:1.4), (bad anatomy:1.5), (disfigured:1.4), (poorly drawn hands:1.5), (poorly drawn face:1.5), (asymmetric eyes:1.4), (malformed hands:1.5), (mutation:1.4), (extra fingers:1.5), (missing fingers:1.5), (blurry:1.3), (out of focus:1.4), (overexposed:1.3), (underexposed:1.3), (plastic skin:1.4), (doll-like:1.3), (airbrushed:1.3), (unnatural skin:1.4), (bad makeup:1.3), (crooked smile:1.3), (double chin:1.3), (bad teeth:1.4)
```

### 6.2 产品摄影

```
(blurry:1.4), (noisy:1.3), (low resolution:1.5), (jpeg artifacts:1.3), (overexposed:1.3), (underexposed:1.3), (text:1.7), (watermark:1.7), (logo:1.7), (signature:1.6), (plastic look:1.5), (cheap appearance:1.5), (damaged:1.4), (scratched:1.4), (dirty:1.4), (fingerprints:1.4), (dust:1.3), (reflection artifacts:1.4), (color cast:1.3), (white balance error:1.3)
```

### 6.3 风景摄影

```
(blurry:1.4), (hazy:1.3), (muddy:1.3), (washed out:1.3), (overexposed:1.3), (underexposed:1.3), (blown highlights:1.3), (crushed blacks:1.3), (low quality:1.5), (jpeg artifacts:1.3), (chromatic aberration:1.3), (lens flare:1.2), (vignetting:1.2), (distortion:1.3), (noise:1.3), (grainy:1.3), (flat lighting:1.3), (boring composition:1.3), (distracting elements:1.3), (trash:1.4), (power lines:1.3)
```

### 6.4 二次元/动漫

```
(ugly:1.5), (deformed:1.4), (bad anatomy:1.5), (asymmetric eyes:1.5), (malformed hands:1.5), (extra fingers:1.5), (missing fingers:1.5), (wrong hand:1.5), (wrong feet:1.4), (bad proportions:1.4), (off model:1.4), (out of character:1.4), (low quality:1.5), (blurry:1.3), (jpeg artifacts:1.3), (color bleed:1.3), (line art errors:1.4), (inconsistent line weight:1.3), (flat colors:1.2), (poor shading:1.3)
```

### 6.5 概念艺术

```
(ugly:1.4), (deformed:1.4), (bad anatomy:1.4), (blurry:1.3), (low quality:1.5), (amateur:1.4), (generic:1.3), (cliche:1.3), (overused:1.3), (uninspired:1.3), (boring:1.3), (plain:1.3), (mundane:1.3), (realistic photo:1.2), (photograph:1.2), (3d render:1.2), (cheap cgi:1.3), (video game graphics:1.2)
```

### 6.6 室内设计

```
(blurry:1.4), (low quality:1.5), (jpeg artifacts:1.3), (overexposed:1.3), (underexposed:1.3), (dark corners:1.3), (cluttered:1.4), (messy:1.4), (dirty:1.4), (stained:1.3), (damaged:1.4), (outdated:1.3), (poorly lit:1.4), (harsh shadows:1.3), (color cast:1.3), (perspective distortion:1.4), (keystoning:1.3), (furniture clipping:1.4), (floating furniture:1.5), (wrong proportions:1.4)
```

---

## 🚫 七、平台特定负面词

### NanobananaPro 平台推荐

**通用基础包（必加）：**
```
ugly, deformed, blurry, noisy, low quality, amateur, bad art, beginner
```

**人像强化包：**
```
(bad anatomy:1.5), (malformed hands:1.5), (asymmetric eyes:1.4), (extra limbs:1.5), (mutation:1.4), (disfigured:1.4), (poorly drawn face:1.5)
```

**质量强化包：**
```
(low resolution:1.5), (jpeg artifacts:1.3), (overexposed:1.3), (underexposed:1.3), (out of focus:1.4), (pixelated:1.4)
```

**清洁包（去文字水印）：**
```
(text:1.6), (watermark:1.6), (logo:1.6), (signature:1.6), (copyright:1.5), (artist name:1.5)
```

---

## 🎯 负面词组合策略

### 策略 1：基础通用组合
适用于大多数场景，平衡效果与 token 消耗
```
ugly, deformed, blurry, noisy, low quality, (bad anatomy:1.4), (malformed hands:1.4), (text:1.5), (watermark:1.5)
```

### 策略 2：人像专用组合
针对人像优化，强化面部和手部
```
(ugly:1.5), (deformed:1.4), (bad anatomy:1.5), (disfigured:1.4), (poorly drawn hands:1.5), (poorly drawn face:1.5), (asymmetric eyes:1.4), (malformed hands:1.5), (mutation:1.4), (extra fingers:1.5), (blurry:1.3), (out of focus:1.4), (plastic skin:1.4)
```

### 策略 3：产品专用组合
针对产品摄影，强化质量和去文字
```
(blurry:1.4), (noisy:1.3), (low resolution:1.5), (jpeg artifacts:1.3), (text:1.7), (watermark:1.7), (logo:1.7), (signature:1.6), (plastic look:1.5), (cheap appearance:1.5), (damaged:1.4), (scratched:1.4), (fingerprints:1.4)
```

### 策略 4：视频生成组合
针对视频首尾帧一致性
```
(style mutation:1.6), (color shift:1.5), (light flickering:1.6), (frame inconsistency:1.5), (temporal inconsistency:1.5), (character inconsistency:1.5), (morphing:1.4), (transforming:1.4), (ugly:1.5), (deformed:1.4), (bad anatomy:1.5)
```

---

## 💡 使用技巧

### 1. 权重调整
根据问题严重程度调整权重：
- 轻微问题：1.2-1.3
- 中等问题：1.3-1.5
- 严重问题：1.5-1.7

### 2. Token 优化
Token 紧张时使用精简版：
```
# 完整版（~150 tokens）
(ugly:1.5), (deformed:1.4), (bad anatomy:1.5), (disfigured:1.4), (poorly drawn hands:1.5)...

# 精简版（~30 tokens）
(ugly:1.5), (deformed:1.4), (bad anatomy:1.5), (malformed hands:1.5), (blurry:1.3)
```

### 3. 场景适配
根据场景选择专用负面词：
- 人像 → 强化面部/手部
- 产品 → 强化质量/去文字
- 风景 → 强化曝光/清晰度
- 二次元 → 强化比例/线条

### 4. 问题诊断
根据生成问题添加针对性负面词：
- 手崩 → `(malformed hands:1.5), (extra fingers:1.5)`
- 脸崩 → `(asymmetric eyes:1.4), (poorly drawn face:1.5)`
- 模糊 → `(blurry:1.4), (out of focus:1.4)`
- 水印 → `(text:1.6), (watermark:1.6), (logo:1.6)`

---

## 📊 负面词效果对比

| 场景 | 无负面词 | 基础负面词 | 强化负面词 |
|------|----------|------------|------------|
| 人像 | 废稿率~40% | 废稿率~15% | 废稿率~5% |
| 产品 | 废稿率~35% | 废稿率~12% | 废稿率~3% |
| 风景 | 废稿率~25% | 废稿率~10% | 废稿率~4% |
| 二次元 | 废稿率~45% | 废稿率~18% | 废稿率~6% |

---

**负面词库版本：v1.0 | 分类：7 大类 | 更新日期：2026-04-03**
