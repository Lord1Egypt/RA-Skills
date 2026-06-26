# Prompt Library Gardener
整理、去重、标签化你的 AI 提示词库，让每条 prompt 都能快速被找到和复用。

## What it does
- 🏷️ 智能分类与标签：按场景、输出类型、受众自动打标签
- 🔄 去重合并：识别语义相似 prompt，合并保留最优版本
- 📑 复用索引：为每条 prompt 生成使用说明和检索索引

## Example scenarios

**1. 每次用 AI 都要从头写 prompt**
> 👤 我每天用ChatGPT/豆包/Kimi写周报、写文案、翻译，但每次都要从头写提示词。有没有办法让我保存和复用常用的prompt？
> 🤖 个人AI提示词管理系统——工具选择：飞书文档/Notion/语雀；组织方式：按场景分（写作/编程/翻译/整理/创意），每个场景写模板prompt；模板格式：角色设定→任务说明→输出格式→约束条件→示例；推荐将最常用的5个设为快捷短语。

**2. 整理散落的 prompt**
> 👤 Import my scattered prompts from Notes, Notion, and chat history. De-duplicate and tag them by use case.
> 🤖 Consolidated library. Prompts deduplicated by semantic similarity. Auto-tagged: "writing", "coding", "analysis", "brainstorming". Conflict prompts flagged for manual review.

**3. 回归测试已有 prompt**
> 👤 It's been 6 months. Test my top 20 prompts against the current model and flag any that produce worse output than before.
> 🤖 Regression report. Each prompt tested, scored, and compared to its historical benchmark. 3 prompts flagged as degraded—suggests refined versions.
