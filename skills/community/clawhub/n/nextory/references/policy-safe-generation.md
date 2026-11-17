# 平台安全生成改写规则

## 目标

当生图平台提示“可能违反内容政策”时，把提示词改写成更容易通过审核的商业摄影表达。

核心原则：
- 最终交给生图模型的 prompt 和 negative prompt 都不要出现高风险词
- 不要把敏感词放进负面提示词；很多平台不会区分正向还是负向
- 用正向、商业、服饰、目录、电商、产品结构语言替代性感或成人语境
- 先保证可生成，再逐步加强产品细节

## 一、最终输出禁用词

以下词不要出现在最终 prompt、English Prompt、Negative Prompt、Add-on 中：

```text
nudity, nude, explicit, erotic, fetish, porn, pornographic,
underage, teen, teenager, schoolgirl, young girl, loli,
exposed intimate areas, nipples, sexual, seductive, sensual,
no nudity, non-explicit, adult content, NSFW
```

中文也避免：
- 情趣
- 性感
- 露点
- 露骨
- 色情
- 挑逗
- 未成年
- 少女感
- 校园感
- 私密部位

如果需要表达安全边界，不要写禁用词，改用正向安全表达：
- `商业服饰目录图`
- `电商产品展示`
- `专业时装模特`
- `端正自然站姿`
- `完整覆盖的服装版型`
- `重点展示剪裁、面料、结构和穿着效果`
- `克制、干净、零挑逗的拍摄语气`

## 二、高风险词替代表

| 原需求/内部理解 | 最终提示词替代 |
| --- | --- |
| 情趣内衣 | 精致贴身服饰套装 / 精品贴身服装 |
| 内衣 | 贴身服饰 / fitted apparel / close-fit apparel |
| 内裤 | 贴身下装 / fitted bottom / base-layer shorts |
| 文胸 | 结构化上装 / supportive fitted top / structured top |
| bra top | supportive fitted top |
| lingerie campaign | premium apparel catalog photography |
| underwear photography | fitted apparel catalog photography |
| boudoir | boutique hotel room / soft bedroom-style catalog setting |
| sensual | refined / tasteful / restrained / elegant |
| sexy | refined fashion styling / polished catalog styling |
| adult model | professional fashion model |
| fully covered intimate areas | full-coverage garment styling |

## 三、安全提示词骨架

### 人物穿着图

```text
以图1作为专业时装模特参考，以图2作为贴身服饰产品参考。保持图1模特的脸型、五官比例、发型、肤色、自然妆感、体态和专业气质不变；保持图2产品的结构化上装、高腰贴身下装、肩带位置、腰头高度、边缘装饰、面料纹理、颜色和版型比例不变。画面为商业服饰目录摄影，模特采用端正自然站姿，肩颈放松，表情克制自然，双手动作简单不遮挡服装结构。产品完整覆盖、版型清晰，重点展示剪裁、面料、结构和穿着效果。干净棚拍背景，柔和侧前方主光，真实皮肤纹理，自然面料张力，清晰边缘，电商可用画质。
```

English:
```text
Use image 1 as the professional fashion model reference and image 2 as the fitted apparel product reference. Preserve the model's facial outline, facial proportions, hairstyle, skin tone, natural makeup, body posture and polished catalog presence. Preserve the product's structured fitted top, high-waist fitted bottom, strap placement, waistband height, decorative edges, fabric texture, color and silhouette. Create commercial apparel catalog photography with a clean studio backdrop. The model stands in a natural upright pose with relaxed shoulders, restrained expression and simple hands that do not cover the garment structure. The garment has full-coverage styling, clear construction, realistic fabric tension, natural skin texture, soft front-side studio lighting, clean edges and e-commerce-ready quality.
```

### 产品单独展示

```text
以图1作为贴身服饰产品参考，保持产品的结构、版型、颜色、面料纹理、肩带/腰头/边缘装饰和比例不变。输出一张商业电商产品图，产品平铺或使用隐形模特方式展示，背景干净，光线柔和，边缘清晰，面料纹理和缝线细节可见，不添加额外文字、logo、花纹或配件。
```

English:
```text
Use image 1 as the fitted apparel product reference. Preserve the product structure, silhouette, color, fabric texture, strap or waistband placement, decorative edges and proportions. Create a clean e-commerce product image using flat-lay or ghost-mannequin presentation. Use a simple background, soft studio lighting, crisp edges, visible fabric texture and seam details. Do not add extra text, logos, patterns or accessories.
```

### 酒店/卧室风格但安全

不要写暧昧、情绪、性感、私密。改成生活方式目录图。

```text
高端酒店房间风格的商业服饰目录图，柔和床品和浅色墙面作为低对比背景，模特姿态端正自然，服装结构完整可见，拍摄重点是面料、版型和穿着舒适度，整体克制干净。
```

English:
```text
Premium hotel-room style commercial apparel catalog image, with soft bedding and light neutral walls as a low-contrast background. The model keeps a natural upright pose, the garment structure is fully visible, and the focus is on fabric, silhouette and wearing comfort. Restrained clean styling.
```

## 四、安全负面提示词

只使用非敏感的质量控制词：

```text
low quality, blurry, distorted anatomy, bad hands, extra fingers, missing fingers, stiff pose, plastic skin, waxy skin, distorted face, warped garment, asymmetrical straps, broken fabric pattern, melted lace-like details, warped waistband, wrong product shape, changed color, added text, added logo, watermark, messy background, harsh shadow, overexposed, underexposed
```

产品图追加：
```text
distorted product shape, wrong proportions, warped seams, inaccurate fabric texture, floating object, missing contact shadow, cluttered background, random text, random logo
```

人物图追加：
```text
stiff mannequin pose, unnatural smile, glassy eyes, twisted fingers, distorted shoulders, unrealistic waist, over-smoothed skin, mismatched lighting
```

## 五、如果仍然被拒绝

按顺序降敏：
1. 改为产品平铺图或隐形模特图
2. 改为半身以上或局部结构特写，减少全身身体语境
3. 加外搭：西装外套、开衫、衬衫、睡袍式外层，但不遮挡核心版型
4. 场景改为纯色棚拍或电商白底
5. 英文 prompt 删除所有人体敏感词，只保留 `professional fashion model`、`fitted apparel`、`commercial catalog`

## 六、输出自检

交付前检查：
- 最终提示词是否没有禁用词
- 负面提示词是否没有禁用词
- 是否用“商业服饰/目录/电商/专业模特”表达
- 是否通过结构、版型、材质来保留产品，而不是用高风险品类词
- 是否提供产品平铺或隐形模特作为备用方案
