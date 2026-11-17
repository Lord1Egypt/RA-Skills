# 模板导航

本文件只作为模板导航页，详细模板已拆分到更小的文件，避免单文件过长导致 embedding 失败。

## 何时读哪份模板

- 高质感、品牌感、去 AI 感、提示词全面优化：
  读 `references/prompt-quality-system.md`
- 提示词更详细、更完整、细节更多、短需求扩写：
  读 `references/prompt-detail-expansion-system.md`
- 人像更真实、皮肤真实、眼神真实、真人感、别假脸：
  读 `references/portrait-realism-system.md`
- 电商产品更精致、主图更干净、材质更好、官网产品图：
  读 `references/ecommerce-product-polish-system.md`
- 生成失败、提示内容政策、审核不过、需要安全可生成版：
  读 `references/policy-safe-generation.md`
- 更完善、可直接复制、完整提示词包、复跑建议：
  读 `references/prompt-output-package.md`
- 精确模仿、1:1 还原、同一人物/同一产品保持：
  读 `references/reference-fidelity-system.md`
- 人物更自然、表情姿势真实、皮肤和手部不假：
  读 `references/natural-human-system.md`
- 人像、模特、日韩风格、欧美腿部特写：
  读 `references/patterns-portraits.md`
- 产品重打光、场景合成、角度变换、材质替换、精修：
  读 `references/patterns-products.md`
- 海报、详情页、Logo、图像编辑、多图融合、九宫格：
  读 `references/patterns-design-editing.md`

## 高优先级规则

- 先做参考图角色分配，再写 prompt
- 被平台拦截时，最终 prompt 和负面词都不要输出敏感词，改用商业服饰/电商目录表达
- 有参考图就必须输出保真等级、不可变项和允许变化项
- 有人物就必须补齐表情、眼神、重心、手部、皮肤和服装接触
- 有人像就必须补齐皮肤纹理、眼神光、微表情、头发边缘和镜头光线
- 有电商产品就必须补齐产品一致性、边缘、标签、反光、接触阴影和背景留白
- 默认输出完整提示词包，不只输出一段主 prompt
- 位置、比例、角度、镜头必须写进最终提示词
- 贴身服饰 / 家居服 / 塑身服任务先读 `lingerie-guide.md`
- 电商固定格式先读 `ecommerce-deliverables.md`
- 品牌感先读 `brand-tone-map.md`
- 最终提示词必须经过 `prompt-quality-system.md` 的质量自检
