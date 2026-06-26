# 视频生成模式详解

> **核心区别**: image_to_video (首帧生成) vs reference_image_to_video (参考形象生成)

---

## 1. 四种模式对比

| 模式 | 输入图作用 | 适用场景 |
|------|-----------|---------|
| text_to_video | 无 | 无参考图，新创作 |
| **image_to_video** | **成为第1帧** | 让静态图"动"起来 |
| **reference_image_to_video** | **视觉参考** | 保持形象，改变场景 |
| first_last_frame_to_video | 成为首尾帧 | 连接两个画面 |

---

## 2. image_to_video (首帧生成)

### 定义
- 输入图 **= 视频第1帧**
- 场景/构图/角度**不能改变**
- 只能在原图基础上"动"起来

### 适用场景
1. **静态照片动画化**: 人物眨眼、动物摇尾巴、风景云飘动
2. **产品展示动画**: 旋转、缩放、聚光灯效果
3. **视频续接**: 前一镜头尾帧 → 后一镜头首帧（无缝衔接）

### 限制
❌ 不能改变场景 (草地 → 游泳池)  
❌ 不能改变角度 (正面 → 侧面)  
❌ 不能改变构图 (特写 → 全景)

---

## 3. reference_image_to_video (参考形象生成)

### 定义
- 输入图 **≠ 视频第1帧**
- 输入图作为**视觉参考**
- 保持主体外观，场景/动作**可以完全改变**

### 适用场景
1. **角色一致性 + 新场景**: 角色做不同动作（跑步/游泳/跳跃）
2. **产品一致性 + 不同环境**: 产品在客厅/办公室/户外使用
3. **IP形象延续**: 角色设定图 → 各种动作场景
4. **风格一致性**: 保持视觉风格，生成新场景

### 优势
✅ 可以改变场景  
✅ 可以改变角度  
✅ 可以改变构图  
✅ 保持主体外观一致

---

## 4. 典型错误案例

### 案例: 旺财游泳视频

**需求**:
1. 生成小狗旺财 → 得到草地站立照片 (image_A)
2. 生成旺财游泳视频

**❌ 错误方案 1**: text_to_video (无参考图)
- 结果: 生成完全不同的狗

**❌ 错误方案 2**: image_to_video (首帧生成)
- 问题: 第1帧是草地背景，无法变成游泳池
- 结果: 草地背景下做游泳动作 (不合理)

**✅ 正确方案**: reference_image_to_video
- 参考图: 草地上的旺财
- 提示词: "旺财在游泳池游泳"
- reference_strength: 0.8
- 结果: 外观像旺财，场景是游泳池 ✅

---

## 5. 决策流程

### 快速判断

```
需要生成视频
  ↓
有参考图吗？
  ├─ 无 → text_to_video
  └─ 有 → 场景需要改变吗？
      ├─ 不改 → image_to_video (让图片动起来)
      └─ 要改 → reference_image_to_video (新场景保持形象)
```

### 决策表

| 场景 | 方案 |
|------|------|
| 照片动画化 (眨眼/点头) | image_to_video |
| 产品旋转展示 | image_to_video |
| 视频镜头续接 | image_to_video |
| 角色做不同动作 | reference_image_to_video |
| 产品在不同环境 | reference_image_to_video |
| 改变拍摄角度 | reference_image_to_video |
| 改变场景 | reference_image_to_video |

---

## 6. 参数建议

### reference_strength 设置

| 需求 | 推荐值 | 说明 |
|------|--------|------|
| 高度一致 (人物面部) | 0.85-0.95 | 严格保持外观 |
| 中度一致 (产品/场景) | 0.75-0.85 | 平衡一致性和灵活性 |
| 风格参考 | 0.60-0.75 | 保持风格，允许变化 |

### 工作流建议

**角色系列视频**:
1. 生成角色标准照 (高质量参考图)
2. 用 reference_image_to_video 生成各场景
3. reference_strength 0.85-0.90 (保持外观)

**产品营销视频**:
1. 产品白底照片 (标准参考)
2. 用 reference_image_to_video 生成使用场景
3. reference_strength 0.80-0.85 (保持产品特征)

---

## 7. 常见错误

### ❌ 错误 1: 误用 image_to_video
**问题**: 想改变场景，用了 image_to_video  
**表现**: 第1帧是旧场景，提示词要求新场景 → 矛盾  
**解决**: 改变场景必须用 reference_image_to_video

### ❌ 错误 2: reference_strength 过高/过低
**问题**: 0.95+ 太严格，0.60- 一致性差  
**解决**: 人物 0.85-0.90，产品 0.80-0.85，风格 0.70-0.75

### ❌ 错误 3: 参考图质量差
**问题**: 模糊、截图、低分辨率参考图  
**解决**: 先生成高质量参考图 (SeeDream 4.5 / Nano Banana Pro)

---

## 8. Fallback 策略

### 主方案失败时

**情况 1**: reference_image_to_video 不支持该模型
- Fallback: 改用支持的模型 (Kling O1 / Veo 3.1)

**情况 2**: 一致性不足
- Fallback: 提高 reference_strength (0.80 → 0.90)
- 或: 优化参考图质量

**情况 3**: 模型无法理解复杂提示词
- Fallback: 简化提示词，分步生成

---

## 9. Quick Reference

### 模式选择速查

| 问题 | 答案 |
|------|------|
| 输入图是第1帧吗？ | 是 → image_to_video<br>否 → reference_image_to_video |
| 需要改变场景吗？ | 是 → reference_image_to_video<br>否 → image_to_video |
| 需要改变角度吗？ | 是 → reference_image_to_video<br>否 → image_to_video |
| 只是让图片动起来？ | 是 → image_to_video |
| 保持形象，新场景？ | 是 → reference_image_to_video |

### 核心原则

1. **image_to_video** = 第1帧固定，只能"动"
2. **reference_image_to_video** = 参考外观，可以改场景
3. 改变场景/角度 → 必须用 reference_image_to_video
4. 视频续接/照片动画 → 用 image_to_video
5. 一致性控制 → reference_strength 分层设置

---

**记住**: 选对模式是成功的一半！🎬
