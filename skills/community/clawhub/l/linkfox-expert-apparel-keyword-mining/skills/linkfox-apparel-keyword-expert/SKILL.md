---
name: linkfox-apparel-keyword-expert
description: 服装品类专用关键词挖掘与语义打标专家。从种子词出发，使用 Amazon Suggestions API 进行服装向长尾挖掘（默认 expand+az+numbers+reverse+gap），结合服装专属属性模板（裙长、领型、袖型、版型、场合等），再用 LLM 进行语义打标，识别完整属性短语（Above the Knee、Off-the-Shoulder 等），并自动完成肯定词库/否定词库分流。输出可直接用于 Listing 优化与 PPC 的结构化词库。仅服务服装类目。
---

# 服装关键词挖掘与打标专家

## 定位

专门为服装类目（Dresses / Tops / Bottoms 等）设计的关键词挖掘 + 语义打标一体化专家。

与通用「搜索建议词挖掘专家」的核心区别：
- 默认模式针对服装长词、多属性短语做了优化
- 内置服装专属扩展模板（裙长、领型、袖型、版型、场合、人群等）
- 使用 LLM 进行语义打标，能正确识别完整属性短语
- 直接产出肯定词库 / 否定词库 / 待确认词库

## 核心流程

0. **（关键前置）从商品图/详情提取属性，写准 product_context**
   - 目的：给 LLM 打标提供「产品真相」，显著提升相关度判断与肯定/否定分流准确率
   - 推荐提取维度：袖型、领型、图案、版型、合身度、裙长、材质、场合、人群、功能细节
   - 输出成一段简洁的英文 product_context，再进入后续挖掘与打标
1. **服装向关键词挖掘**
   - 默认模式：`expand + az + numbers + reverse + gap`
   - 使用服装专属模板强化完整属性短语的产出
2. **去重与基础清洗**
3. **LLM 语义打标**
   - primary_type（全英文枚举）
   - 完整属性短语识别（is_complete_attribute_phrase）
   - relevance + library 分流（强依赖 product_context）
4. **结构化输出**

## 输入参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| seed | 种子词 | 必填 |
| product_context | 产品核心描述（强烈推荐） | 无 |
| market | 站点 | US |
| mode | 挖掘模式 | expand+az+numbers+reverse+gap |
| tag | 是否开启 LLM 打标 | 开启 |
| batch_size | LLM 每批处理数量 | 100 |

## 输出结构（Excel）

| Sheet | 内容 |
|-------|------|
| 摘要 | 种子词、模式、站点、总数、正/负/待确认数量、完整属性短语数量 |
| 打标明细 | 全部字段完整数据 |
| 肯定词库 | library=positive，按 relevance + confidence 排序 |
| 否定词库 | library=negative |
| 待确认词库 | library=review |
| 完整属性短语 | is_complete_attribute_phrase=true 的词，按属性分组 |
| 原始挖掘结果 | 未打标的原始 Suggestions 结果 |

## primary_type 枚举（英文）

Core Product, Dress Length, Neckline, Sleeve Type, Silhouette, Fit, Occasion, Pattern, Material, Size Type, Color, Style, Closure Type, Care, Feature, Selling Point, Scenario, Audience, Specification, Question, Brand, Competitor, Other

## 使用建议

- **强烈推荐先看图/看详情，提炼属性后再写 product_context**。这是提高整条链路准确率的最关键前置步骤。
- 默认模式已针对服装优化，一般情况下不需要手动改 mode
- 完整属性短语 Sheet 是服装场景最有价值的产出之一，建议重点使用
- 无 product_context 时，相关度判断会明显降级，更多词会进入 review

## 完整使用示例

```bash
# 推荐流程：先根据商品图提炼属性，再写 product_context，最后运行专家

python3 scripts/suggestion_miner.py \
  --seed "women long sleeve dress" \
  --product-context "Women's long sleeve casual dress with geometric scalloped floral print on black background, distinctive orange and green contrast V-neck stripe, stand collar, elastic cuffs, side pocket, shift silhouette, above-the-knee to midi length. Suitable for daily wear, casual outings, vacation and office casual. Target audience: women." \
  --mode expand,az,numbers,reverse,gap \
  --market US \
  --xlsx apparel_keywords.xlsx \
  --verbose
```

**product_context 推荐结构：**
```text
Women's [袖型] [领型] [图案] [版型] dress, [裙长], [细节], for [场合]. Target audience: women.
```

**输出重点关注：**
- `肯定词库` → 直接用于 Title / Exact
- `完整属性短语` → 服装最有价值的产出
- `否定词库` → 广告否定与清洗

## 限制

- 仅适用于服装类目
- LLM 打标需要可用的模型调用能力
- 无 product_context 时，相关度判断会降级，更多词会进入 review
