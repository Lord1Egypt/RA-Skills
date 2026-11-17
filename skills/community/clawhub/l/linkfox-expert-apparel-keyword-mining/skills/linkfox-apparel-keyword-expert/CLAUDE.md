# CLAUDE.md — 服装关键词挖掘与打标专家

## 快速使用

```bash
# 基础挖掘（使用服装默认模式 expand+az+numbers+reverse+gap）
python3 scripts/suggestion_miner.py --seed "summer dress" --xlsx output.xlsx

# 带产品上下文（推荐，从文件读取，避免 shell 转义问题）
python3 scripts/suggestion_miner.py \
  --seed "summer dress" \
  --product-context-file /tmp/product_context.txt \
  --xlsx output.xlsx \
  --verbose

# 也可直接传字符串（短文本可用）
python3 scripts/suggestion_miner.py \
  --seed "summer dress" \
  --product-context "Women's casual summer dresses, lightweight, floral" \
  --xlsx output.xlsx
```

## 核心文件

| 文件 | 作用 |
|------|------|
| scripts/suggestion_miner.py | 挖掘主脚本（已注入服装模板 + 新默认模式 + linkfox LLM 后端） |
| scripts/llm_tagger.py | LLM 打标 + 词库分流 |
| scripts/excel_writer.py | 7 Sheet 结构化输出 |
| templates/apparel_expand_templates.py | 服装专用扩展模板 |
| prompts/apparel_tagging.py | 最终 System Prompt + Few-shot + User 模板 |
| SKILL.md | 专家能力与流程说明 |

## 默认行为

- 挖掘模式：`expand + az + numbers + reverse + gap`
- 服装模板自动注入（裙长、领型、袖型、版型、场合、人群等）
- LLM 打标默认开启，后端默认 `linkfox`（使用 linkfox-aigc-textgen，无需外部 API Key）
- 输出多 Sheet Excel

## CLI 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| --seed | 种子词（必填） | - |
| --product-context | 产品上下文描述（短文本） | 空 |
| --product-context-file | 从文件读取产品上下文（推荐，避免转义） | 空 |
| --llm-backend | LLM 后端：linkfox / default | linkfox |
| --mode | 挖掘模式 | expand,az,numbers,reverse,gap |
| --no-tag | 关闭 LLM 打标 | false |
| --batch-size | LLM 每批关键词数量 | 50 |
| --market | Amazon 站点 | US |
| --xlsx | Excel 输出路径 | 自动落盘到会话目录 |

## 关键方法论：先看图，再写 product_context

本专家最重要的准确率提升手段，不是多挖几个模式，而是**先从商品图/详情中识别真实属性，再写成高质量 product_context**。

### 为什么要这样做？
- LLM 打标依赖产品真相。没有准确的 product_context，模型只能按字面猜相关度，肯定/否定分流会大量失真。
- 图片属性直接决定哪些词该进 positive（匹配真实特征），哪些该进 negative（与商品冲突，如 sleeveless、bodycon 等）。
- 完整属性短语（Above the Knee、V Neck、Geometric Print 等）的识别也依赖对商品本身的正确理解。

### 推荐提取维度（服装）
袖型 · 领型 · 图案 · 版型 · 合身度 · 裙长 · 材质 · 场合 · 人群 · 功能细节（口袋、收口、撞色条等）

### product_context 推荐写法
```text
Women's long sleeve casual dress with geometric scalloped floral print on black background, distinctive orange and green contrast V-neck stripe, stand collar, elastic cuffs, side pocket, shift silhouette, above-the-knee to midi length. Suitable for daily wear, casual outings, vacation and office casual. Target audience: women.
```

把这段写入文件后用 `--product-context-file` 传入，再进行挖掘和打标，整条链路的准确率会明显提高。

## 注意事项

1. **务必先完成属性提炼与 product_context 书写**，再启动挖掘。这是本专家的核心工作流，不是可选项。
2. 仅服务服装类目，其他品类请使用通用搜索建议词挖掘专家。
3. LLM 后端默认 `linkfox`（linkfox-aigc-textgen），无需额外 API Key。如需切换为 `default`（xAI/OpenAI），使用 `--llm-backend default`。
4. 完整属性短语是本专家最核心的价值产出，优先关注「完整属性短语」Sheet。
5. product_context 较长时务必使用 `--product-context-file` 从文件传入，避免 shell 转义问题。
