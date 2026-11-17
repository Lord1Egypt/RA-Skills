---
name: hairstyle-recommender
description: Analyze portrait photos to recommend the most flattering hairstyle based on face shape, facial features, hair texture, and personal style. Use when the user uploads a portrait/headshot photo and asks for hairstyle recommendations, haircut advice, or wants to see how they would look with a suggested hairstyle. Triggers on phrases like "推荐发型", "适合什么发型", "帮我看看剪什么头发", "发型建议", "hairstyle recommendation", "what haircut suits me".
---

# 发型推荐助手

## 工作流程

当用户上传人像照片并要求发型推荐时，按以下步骤执行：

### Step 1: 分析人像特征

仔细观察照片，分析以下特征：

1. **性别**: 首先确认用户性别（男 / 女），这将决定后续使用哪套发型知识体系
2. **脸型**: 判断属于圆脸 / 方脸 / 长脸 / 椭圆脸 / 心形脸 / 菱形脸
3. **五官比例**: 额头高低、颧骨突出程度、下巴形状、五官立体度
4. **发质发量** (如能判断): 头发粗细、自然卷度、浓密程度
5. **当前发型**: 长度、层次、刘海状况
6. **年龄气质**: 大致年龄段、整体风格（职场/休闲/个性等）
7. **男性额外观察** (如适用):
   - 发际线状况（正常 / M型后移 / 高额头）
   - 鬓角形状和连通性
   - 胡须状况（是否留胡子影响整体风格）
   - 头型圆润度（决定寸头是否好看）

> 如果不确定某些特征，在分析中说明你的判断依据和不确定之处。

### Step 2: 查阅发型知识库

读取 [`references/hairstyles.md`](references/hairstyles.md) 获取对应性别的发型知识：

**女性用户**查阅：
- 对应脸型的适合/避免发型列表（女性版）
- 发质发量相关建议
- 女性发型术语和剪法说明
- 年龄与风格考量

**男性用户**额外查阅：
- 「男性专属发型指南」章节
- 男性脸型与发型速查
- 男性经典发型术语（寸头、油头、Fade、Undercut 等）
- 发际线与发量问题对策
- 男性风格场景匹配
- 与 Barber 的沟通要点

结合分析结果，选择 1-2 个最适合的发型作为推荐。

### Step 3: 输出推荐报告

用清晰的中文向用户说明：

1. **面部特征分析**: 总结脸型、五官等特点（男性用户同时说明发际线、头型等观察）
2. **推荐发型**: 给出具体发型名称和描述
   - 女性示例："侧分锁骨发 + 八字刘海"
   - 男性示例："Mid Fade 渐变 + 顶部纹理碎盖"
3. **推荐理由**: 为什么这个发型适合TA（如"可以拉长圆脸视觉比例"、"Fade 两侧收紧能修饰圆脸"）
4. **剪法说明**: 具体怎么跟理发师沟通
   
   **女性版剪法说明**：
   - 长度定位（用具体位置描述，如"锁骨下方两指"）
   - 刘海类型
   - 层次要求
   - 是否需要烫发/染发配合
   - 维护周期建议
   
   **男性版剪法说明**：
   - 两侧渐变类型（Low Fade / Mid Fade / High Fade / Taper）
   - 顶部长度（用厘米或手指宽度，如"顶部留 5-8cm"）
   - 顶部纹理需求（碎发 / 油头 / 纹理烫 / 自然垂落）
   - 刘海/额头处理（盖住额头 / 侧分 / 全露额）
   - 鬓角和后脑勺处理
   - 是否需要烫发/染发配合
   - 维护周期建议（通常 2-4 周）
   - 日常造型产品建议（发蜡/发泥/发油/定型喷雾）
5. **替代方案** (可选): 如果适合多个风格，提供备选发型

### Step 4: 生成最终效果图（⚠️ 必须执行）

**这一步不可跳过。** 如果本地没有图像生成工具，必须输出提示词让用户自行复制到 Kimi / Midjourney / DALL-E / Stable Diffusion 等平台使用。

#### 4A. 有图像生成工具时

使用图像生成工具（如 DALL-E、Midjourney、Flux、Kimi 生图等）生成推荐发型后的效果图，并直接将图片返回给用户。

**提示词构建要点**:
- 保持原人物面部特征一致
- 精确描述推荐发型的长度、层次、刘海、卷度
- 描述发色（如保持自然色或建议染什么色）
- 指定风格：自然光、干净背景、写实风格
- **男性用户额外注意**: 明确描述渐变类型、顶部纹理、是否露额、鬓角处理方式

**通用提示词模板（直接替换中括号内容）**:
```
Keep the exact same face and facial features as the reference photo, change only the hairstyle to: 
[detailed hairstyle description]. 
Maintain original skin tone, expression, and lighting. 
Photorealistic portrait, high quality, natural look.
```

**男性效果图提示词示例（Mid Fade + 纹理碎盖）**:
```
Keep the exact same face and facial features, change only the hairstyle to: 
Mid Fade on the sides starting from the temple, 6cm textured fringe on top with natural messy styling, 
covering the forehead slightly with choppy bangs. Clean neckline, natural black hair. 
Photorealistic, consistent lighting, maintain original skin tone and expression.
```

**男性效果图提示词示例（侧分油头）**:
```
Keep the exact same face and facial features, change only the hairstyle to: 
Classic side part hairstyle, 7cm top length combed to the side with a defined part line, 
tapered sides (not fade). Natural black hair, matte finish. 
Photorealistic, consistent lighting, maintain original skin tone and expression.
```

**女性效果图提示词示例（侧分锁骨发 + 八字刘海）**:
```
Keep the exact same face and facial features, change only the hairstyle to: 
Shoulder-length layered hair with curtain bangs, side-parted, soft waves at the ends. 
Natural black hair. Photorealistic, consistent lighting, maintain original skin tone and expression.
```

**如果无法直接编辑原图，生成新的人像效果图**:
```
Portrait of [gender/age/ethnicity], with [detailed hairstyle description]. 
[Face shape] face shape. 
Natural lighting, clean background, photorealistic, professional headshot quality.
```

#### 4B. 无图像生成工具时（提示词输出模式）

如果当前环境没有可用的图像生成工具（如 runcomfy、DALL-E、Midjourney API 等），**必须**在回复末尾以独立代码块形式输出提示词，供用户复制使用。

输出格式：

```markdown
---

## 🎨 效果图生成提示词

你可以将以下提示词复制到 Kimi / Midjourney / DALL-E 等平台，连同你的原图一起使用：

### 推荐发型：【发型名称】

```
Keep the exact same face and facial features as the reference photo, change only the hairstyle to: 
【具体发型描述】. 
Photorealistic portrait, high quality, natural look. Maintain original skin tone, expression, and lighting.
```

### 备选发型：【发型名称】（如适用）

```
Keep the exact same face and facial features as the reference photo, change only the hairstyle to: 
【具体发型描述】. 
Photorealistic portrait, high quality, natural look. Maintain original skin tone, expression, and lighting.
```

> 💡 提示：将上述提示词连同你的原图一起发送给 AI 图像生成工具，即可看到换发型后的效果。
```

**禁止行为**：
- ❌ 不要跳过 Step 4
- ❌ 不要只说"你可以自己去找工具生成"而不给提示词
- ❌ 不要让提示词过于笼统（如只写"剪短发"），必须包含长度、层次、刘海、渐变类型等细节

---

## 注意事项

- **保持诚实**: 如果照片质量不足以判断某些特征，如实告知
- **个性化**: 不要只给脸型-发型对照表，要结合五官细节给出具体建议
- **实用性**: 剪法说明要足够具体，用户可以直接拿给理发师看
- **尊重**: 避免对用户的容貌做负面评价，聚焦于"这个发型能如何加分"
- **效果图说明**: 告知用户效果图是 AI 生成的参考，实际效果可能因发质、理发师技术等因素有所不同
