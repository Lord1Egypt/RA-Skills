# 贴身服饰 / 家居服 / 塑身服提示词指南

## 目标

把贴身服饰类需求稳定改写成更容易通过平台审核的商业服饰摄影提示词。

本指南服务于：
- 电商产品图
- 专业模特上身图
- 品牌目录图
- 四视图 / 详情页 / 九宫格

优先读取：`references/policy-safe-generation.md`

## 一、先做安全分流

看到用户提到贴身服饰、内衣、内裤、连体衣、睡裙、家居服、塑身服时：
1. 内部理解真实品类
2. 最终输出使用平台安全表达
3. 不在最终 prompt 或 negative prompt 里放高风险词

安全表达优先级：
- `商业服饰目录摄影`
- `贴身服饰产品展示`
- `结构化上装`
- `高腰贴身下装`
- `一体式贴身服装`
- `家居服套装`
- `塑身版型服装`
- `专业时装模特`
- `完整覆盖的服装版型`
- `重点展示剪裁、面料、结构和穿着效果`

## 二、品类映射

| 用户说法 | 最终提示词建议 |
| --- | --- |
| 女款内衣套装 | 精致贴身服饰套装 / fitted apparel set |
| 文胸 / bra | 结构化上装 / supportive fitted top |
| 内裤 / briefs | 高腰贴身下装 / fitted bottom |
| 男士内裤 | 男士贴身下装 / men's fitted base-layer shorts |
| 连体衣 / bodysuit | 一体式贴身服装 / one-piece fitted garment |
| 睡裙 / chemise | 吊带家居裙 / lightweight lounge dress |
| 塑身衣 | 塑身版型服装 / contouring fitted garment |
| 吊袜带 | 腰部装饰带 / waist accessory strap |

如果用户的参考图本身版型更大胆，也用结构、版型、覆盖度、面料、边缘装饰来描述，不使用挑逗或成人化语言。

## 三、必须锁定的产品信息

### 结构

必须关注：
- 上装轮廓
- 肩带粗细和位置
- 下装腰头高度
- 腿口或下摆弧度
- 背部连接结构
- 侧边拼接
- 边缘装饰
- 缝线走向

男士款额外关注：
- 腰头宽度和 logo 带
- 裤腿长度
- 前片支撑结构
- 腿口包边
- 贴身度
- 运动感或家居感

### 材质

高频材质安全写法：
- 细密花纹织物
- 轻薄网状织物
- 柔和缎面光泽
- 弹力棉
- 莫代尔
- 罗纹针织
- 弹力包边
- 细密边缘装饰

英文安全写法：
- `fine patterned fabric`
- `lightweight mesh-like fabric`
- `soft satin-like sheen`
- `stretch cotton texture`
- `modal-like smooth texture`
- `ribbed knit texture`
- `elastic trim`
- `decorative fabric edge`

### 穿着关系

必须写清：
- 高腰 / 中腰 / 低腰
- 贴身程度
- 包裹度
- 面料张力
- 肩带和腰头位置
- 布料在身体转折处的自然褶皱
- 皮肤与服装接触处的自然阴影

## 四、推荐安全场景

### 1. 电商白底 / 纯色背景

最容易通过平台审核。

关键词：
- `clean studio backdrop`
- `commercial apparel catalog photography`
- `soft studio lighting`
- `clear garment structure`
- `subtle natural shadow`
- `e-commerce-ready quality`

### 2. 品牌目录棚拍

适合模特上身展示。

关键词：
- `premium apparel catalog`
- `professional fashion model`
- `polished retail styling`
- `restrained clean composition`
- `soft sculpted studio light`

### 3. 家居生活方式图

适合睡衣、家居服、轻薄套装。

关键词：
- `premium homewear catalog setting`
- `soft bedding and neutral wall`
- `natural upright pose`
- `clean lifestyle catalog image`

避免使用暧昧、挑逗、成人化场景词。

## 五、可复制安全模板

### 模板 A: 白底电商模特图

```text
图1为专业时装模特参考，图2为贴身服饰产品参考。保持图1模特的脸型、五官比例、发型、肤色、自然妆感、体态和专业气质不变；保持图2产品的结构化上装、高腰贴身下装、肩带位置、腰头高度、边缘装饰、面料纹理、颜色和版型比例不变。画面为商业服饰目录摄影，模特采用端正自然站姿，肩颈放松，表情克制自然，双手动作简单不遮挡服装结构。产品版型完整清晰，重点展示剪裁、面料、结构和穿着效果。干净棚拍背景，柔和侧前方主光，真实皮肤纹理，自然面料张力，清晰边缘，电商可用画质。
```

English:
```text
Use image 1 as the professional fashion model reference and image 2 as the fitted apparel product reference. Preserve the model's facial outline, facial proportions, hairstyle, skin tone, natural makeup, body posture and polished catalog presence. Preserve the product's structured fitted top, high-waist fitted bottom, strap placement, waistband height, decorative edges, fabric texture, color and silhouette. Create commercial apparel catalog photography with a clean studio backdrop. The model stands in a natural upright pose with relaxed shoulders, restrained expression and simple hands that do not cover the garment structure. The garment construction is clear, with realistic fabric tension, natural skin texture, soft front-side studio lighting, clean edges and e-commerce-ready quality.
```

### 模板 B: 产品平铺 / 隐形模特

```text
以图1作为贴身服饰产品参考，保持产品结构、版型、颜色、面料纹理、肩带/腰头/边缘装饰和比例不变。输出一张商业电商产品图，产品平铺或使用隐形模特方式展示，背景干净，光线柔和，边缘清晰，面料纹理和缝线细节可见，不添加额外文字、logo、花纹或配件。
```

English:
```text
Use image 1 as the fitted apparel product reference. Preserve the product structure, silhouette, color, fabric texture, strap or waistband placement, decorative edges and proportions. Create a clean e-commerce product image using flat-lay or ghost-mannequin presentation. Use a simple background, soft studio lighting, crisp edges, visible fabric texture and seam details. Do not add extra text, logos, patterns or accessories.
```

### 模板 C: 家居目录风

```text
以图1作为专业时装模特参考，以图2作为家居贴身服饰参考。保持模特身份感、体态、肤色和发型不变，保持服装的肩带位置、腰线、下摆、面料纹理和颜色不变。画面为高端家居服目录摄影，浅色床品和中性墙面作为低对比背景，模特采用端正自然姿态，画面重点是服装版型、面料舒适度和穿着效果，整体克制干净。
```

English:
```text
Use image 1 as the professional fashion model reference and image 2 as the lounge fitted apparel reference. Preserve the model identity impression, posture, skin tone and hairstyle. Preserve the garment strap placement, waistline, hem shape, fabric texture and color. Create a premium homewear catalog image with soft bedding and neutral walls as a low-contrast background. The model keeps a natural upright pose. Focus on garment silhouette, fabric comfort and wearing effect with restrained clean styling.
```

### 模板 D: 四视图 / 详情页

```text
输出一组商业电商展示图，包括正面、侧面、背面和面料细节特写。整组保持同一产品的版型、颜色、面料纹理、肩带位置、腰头高度、边缘装饰和比例一致。每张图只改变视角、裁切和信息重点，不改变产品结构。
```

## 六、安全负面提示词

只使用质量控制词，不放敏感词：

```text
low quality, blurry, distorted anatomy, bad hands, extra fingers, missing fingers, stiff pose, plastic skin, waxy skin, distorted face, warped garment, asymmetrical straps, broken fabric pattern, melted decorative edges, warped waistband, wrong product shape, changed color, added text, added logo, watermark, messy background, harsh shadow, overexposed, underexposed
```

男士款追加：

```text
warped waistband logo, unnatural front panel shape, deformed thighs, exaggerated muscles, broken hem, asymmetrical leg openings, wrong fabric texture
```

## 七、如果平台仍拒绝

优先切换为：
1. 产品平铺图
2. 隐形模特图
3. 半身目录图
4. 外搭衬衫/开衫/外套的品牌目录图
5. 纯白背景产品详情页

不要继续加入成人化词或敏感负面词。

## 八、和其他参考文档的配合

- 安全改写：读 `references/policy-safe-generation.md`
- 面料词扩展：读 `references/fabric-guide.md`
- 去 AI 感：读 `references/anti-ai-guide.md`
- 位置角度：读 `references/spatial-control.md`
- 逆向复刻：读 `references/reverse-engineering.md`
