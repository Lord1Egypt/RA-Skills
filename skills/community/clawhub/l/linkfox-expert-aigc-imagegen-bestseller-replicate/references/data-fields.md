# 字段汇总表：爆款复刻

供运行时快速查字段，不必重读 SKILL.md。

## S1 识别输入方式 + 校验

| 字段 | 中文 | 方向 | 来源/去向 |
|------|------|------|-----------|
| product_image | 商品原图（图一） | 输入 | 用户上传 → S3 imageUrls[0] |
| amazon_input | 亚马逊链接/ASIN | 输入 | 用户（方式A） |
| reference_images | 上传参考图（图二） | 输入 | 用户（方式B）→ S3 |
| provider | 生图模型 | 输入 | 用户/默认 GPT_2_IMAGE；透传不校验枚举 |
| quality | 图片质量 | 输入 | 用户/默认 high（仅 GPT_2_IMAGE） |
| aspectRatio | 宽高比 | 输入 | S1 归一化：「默认比例」/空→默认模式，由 S3 逐张探测图二；具体比例→全局透传 S3 |
| include_aplus | 是否含 A+ 图 | 输入 | 仅方式 A；默认 true；用户/前端「只要主图」→ false → S2 |
| input_mode | 输入方式 A/B | 输出 | → 决定是否走 S2 |
| asins | ASIN | 输出 | 解析自 amazon_input → S2 |
| amazonDomain | 站点域名 | 输出 | 解析/默认 amazon.com → S2 |
| provider/quality/resolution/aspectRatio/include_aplus | 透传参数 | 输出 | → S2/S3（resolution 缺省 2K；aspectRatio 具体值优先，否则逐图探测并回填；include_aplus 仅方式 A） |

## S2 抓 listing 图片（仅方式 A）→ linkfox-amazon-product-detail

| 字段 | 中文 | 方向 | 说明 |
|------|------|------|------|
| asins | ASIN | 输入 | 来自 S1 |
| amazonDomain | 站点 | 输入 | 来自 S1 |
| include_aplus | 是否含 A+ | 输入 | 来自 S1；false 时脚本加 `--main-only` |
| reference_images | 参考图集（URL） | 输出 | 主副图 +（可选）A+ → S3 |
| main_count | 主副图张数 | 输出 | → S2.5 文案 |
| aplus_count | A+ 图张数 | 输出 | → S2.5 文案 |

> 调用：`linkfox-amazon-product-detail`，参数 `asins`、`amazonDomain`，不开附加开关。落盘后用 `scripts/extract_reference_images.py` 提取 URL（禁止 inline jq）。

## S3 逐张配对生图 → linkfox-aigc-imagegen

| 字段 | 中文 | 方向 | 说明 |
|------|------|------|------|
| imageUrls | 图片列表 | 输入 | `[原图, 参考图_i]`，顺序固定 |
| prompt | 提示词 | 输入 | 固定句取自 `workflow.md` 唯一正源，不可覆盖；不追加宽高行 |
| provider | 模型 | 输入 | 透传 S1 的 provider，不校验枚举 |
| quality | 质量 | 输入 | 透传（仅 GPT_2_IMAGE） |
| outputNum | 输出张数 | 输入 | 固定 1 |
| resolution | 分辨率 | 输入 | 透传前端值；前端未传缺省 2K |
| aspectRatio | 宽高比 | 输入 | 必传；具体比例→全局透传用户选项；默认比例/空→逐张探测当前图二真实显示宽高并回填原始 `W:H` |
| replica_results | 参考图→复刻图映射 | 输出 | → S4 |

> imagegen 响应字段：`resultList[].url`（复刻图 URL）、`status`（3 成功/4 失败）、`taskId`。

## S4 落盘 + 对照展示

| 字段 | 中文 | 方向 | 说明 |
|------|------|------|------|
| replica_results | 参考图→复刻图映射 | 输入 | 来自 S3 |
| media 文件 | 落盘复刻图 | 输出 | `resolve_media_path("bestseller-replicate", ts, "png")` |
| 对照展示 | 参考图→复刻图 | 输出 | markdown 图片，交付用户 |
