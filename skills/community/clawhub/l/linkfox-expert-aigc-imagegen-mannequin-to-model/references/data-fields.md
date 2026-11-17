# 字段汇总表：人台换模特

供运行时快速查字段，不必重读 SKILL.md。

## S1 校验图片 URL 可访问性

| 字段 | 中文 | 方向 | 来源/去向 |
|------|------|------|-----------|
| imageUrls | 图片 URL 列表 | 输入/输出 | 用户上传（第1张=人台图，第2张=模特参考，第3张=背景参考）；校验后直接用于 S2、S3 |

## S2 调 linkfox-aigc-textgen 生成出图 prompt

| 字段 | 中文 | 方向 | 说明 |
|------|------|------|------|
| imageUrls | 图片 URL 列表 | 输入 | 来自 S1 校验后的 URL，供 textgen 做图片解读 |
| customerKeywords | 用户补充提示词 | 输入 | 替换 system prompt 中 `{customer_keywords}` 占位符 |
| prompt | textgen system prompt | 输入 | 内联固化的提示词正文，含 Completion Rule / Black Box Rule / Output Format |
| model | textgen 模型 | 输入 | 固定 GEM_3_1_PRO |
| thinkingLevel | 思考深度 | 输入 | 固定 medium |
| generatedPrompt | 英文出图提示词 | 输出 | ≤512 tokens 纯英文 img2img prompt → S3 |

## S3 调 linkfox-aigc-imagegen 出图

| 字段 | 中文 | 方向 | 说明 |
|------|------|------|------|
| prompt | 出图提示词 | 输入 | 来自 S2 generatedPrompt |
| imageUrls | 参考图 URL | 输入 | 来自 S1 校验后的 URL（人台图+可选模特参考+可选背景参考） |
| provider | 生图模型 | 输入 | 用户指定，默认 BANANA_PRO |
| aspectRatio | 宽高比 | 输入 | 来自用户 ratio 参数，默认 1:1 |
| resolution | 分辨率 | 输入 | 来自用户，默认 2K |
| outputNum | 输出张数 | 输入 | 固定 1 |
| quality | 图片质量 | 输入 | 固定 high |
| 模特上身图路径 | 结果图 | 输出 | `Saved full response:` 后的本地路径，交付用户 |
