# 极义GEO 工作流指南

## 核心概念

### 什么是 GEO？
GEO（Generative Engine Optimization）= 生成式搜索引擎优化。
与传统 SEO 优化搜索引擎排名不同，GEO 优化的是品牌在 AI 搜索引擎回答中的可见度和引用率。

### 数据依赖链（重要）

```
products create → company save（完整填写） → drafts generate → articles generate
                                                ↑ 需要 keywords 文本    ↑ 需要 question_id
```

- `company save` 需要一次性完整填写公司信息，信息质量直接决定后续问题生成和文章生成的效果

#### company save 填写策略

公司信息必须基于事实，不能凭感觉编造。按以下优先级获取信息：

1. **先从用户对话中提取** — 用户可能已经提到了公司名、产品名、行业等信息，直接使用
2. **联网搜索补充** — 对于用户没有明确提供的必填字段，主动通过联网搜索获取准确信息
3. **与用户深度对话补充** — 联网搜索无法获取的信息（如目标客户描述、写作风格偏好），合并向用户提问，一次性收集
- `drafts generate` 需要先填写公司信息（`company save`），传入 `--keywords` 文本即可异步生成 L1-L4 四阶段问题草稿
- `articles generate` 必须先有问题（`drafts generate` 返回的 ID）
- `search create` 是**独立的**，只需要问题文本和品牌名，不依赖上述链路
- 依赖链中任何一步失败，后续步骤都无法执行，不要尝试绕过

### 数据层级
```
用户 → 产品(多个) → 公司信息(每产品一份)
                   → 问题草稿(多个) → 文章(多个) → 发布记录
                   → 核心词(多个)
                   → 图片素材库 → 分类(多个) → 图片(多个)
```

### 问题阶段（L1-L4）
| 阶段 | 英文 | 含义 | 示例 |
|------|------|------|------|
| L1 | inquiry | 认知层 | "什么是GEO优化？" |
| L2 | understanding | 探索层 | "GEO优化有哪些方法？" |
| L3 | consideration | 评估层 | "GEO优化工具哪个好？" |
| L4 | purchase | 决策层 | "极义GEO怎么样？值得用吗？" |

### 支持的 AI 平台
| 平台 | ID 标识 | 说明 |
|------|---------|------|
| DeepSeek | deepseek | 深度求索 |
| Kimi | kimi | 月之暗面 |
| 通义千问 | qianwen | 阿里云 |
| 豆包 | doubao | 字节跳动 |
| 文心一言 | wenxin | 百度 |
| 智谱清言 | zhipu | 智谱AI |
| 腾讯元宝 | yuanbao | 腾讯 |

---

## 典型工作流

### 流程一：品牌 AI 可见度诊断（最常用）

```
1. 查看产品列表 → products list
2. 创建搜索任务 → search create --question "品牌名怎么样" --brand "品牌名" --platforms deepseek,kimi,qianwen,doubao
3. 查看结果 → search status --task-id xxx
```

注意：`search create` 不需要先创建关键词或问题，直接传文本即可。这是最快的诊断路径。

### 流程二：内容优化与分发（完整链路）

```
1. 创建产品 → products create（如果还没有）
2. 完整填写公司信息 → company save（通过搜索和对话收集所有必填字段，一次性保存）
3. AI 生成问题草稿 → drafts generate --keywords "AI搜索优化"
4. 查看草稿 → drafts latest 或 drafts get --id xxx
5. （可选）编辑草稿 → drafts update --id xxx --inquiry "修改后的问题"
6. 生成文章 → articles generate --question-id xxx
7. （可选）上传配图 → gallery images-upload --category-id 1 --file ./img.jpg
8. 分发到自媒体 → publish record
```

**⚠️ 步骤 2 的公司信息质量直接决定步骤 3 和步骤 6 的生成效果。必填字段务必准确完整填写。**
**⚠️ 步骤 6 必须有 question_id。如果问题生成失败，文章生成无法执行。**

### 流程三：图片素材管理

```
1. 创建分类 → gallery categories-create --name "产品图"
2. 上传图片 → gallery images-upload --category-id 1 --file ./img1.jpg ./img2.png
3. 查看图片 → gallery images-list
4. 生成文章时引用图片 → articles generate --question-id xxx --image-ids 1,2,3
```

### 流程四：批量监控

```
1. 确保已有问题（questions list 查看）
2. 批量搜索 → search batch --question-ids 1,2,3 --platforms deepseek,kimi,qianwen,doubao
3. 查看批量进度 → search batch-status --batch-id xxx
```

---

## 搜索结果解读

### 单平台结果结构
```json
{
  "platform": "deepseek",
  "answer": "AI 生成的回答全文...",
  "brand_mentioned": true,
  "brand_rank": 2,
  "sentiment": "positive",
  "citations": [
    {
      "position": 1,
      "title": "引用来源标题",
      "url": "https://...",
      "domain": "example.com"
    }
  ]
}
```

### 关键指标
- **brand_mentioned**: 品牌是否被提及
- **brand_rank**: 品牌在回答中的排名位置（0=未排名）
- **sentiment**: 情感倾向（positive/neutral/negative）
- **citations**: 引用来源列表，可分析哪些内容被 AI 引用

### 结果解读与建议策略

拿到搜索结果后，不要只罗列数据，要根据结果给出有针对性的分析和建议。以下是常见场景的解读逻辑：

#### 品牌提及率分析

| 场景 | 解读 | 建议 |
|------|------|------|
| 全部平台 brand_mentioned = true | 品牌 AI 可见度良好 | 关注 brand_rank 和 sentiment，持续优化排名位置 |
| 部分平台提及、部分未提及 | 品牌在不同 AI 平台的知识库覆盖不均 | 优先针对未提及的平台生成优化内容，分析已提及平台引用了哪些来源 |
| 全部平台 brand_mentioned = false | 品牌在 AI 搜索中基本不可见 | 这是最需要 GEO 优化的情况。建议走完整链路：添加核心词 → 生成问题 → 生成文章 → 分发到自媒体，让 AI 平台能抓取到品牌相关内容 |

#### 排名位置解读

| brand_rank | 含义 | 建议 |
|------------|------|------|
| 0 | 未排名（品牌未出现在回答中） | 需要大量内容建设 |
| 1-3 | 头部位置，AI 优先推荐 | 维持现状，关注 sentiment 是否正面 |
| 4-6 | 中间位置，有提及但不突出 | 通过更多高质量内容提升排名 |
| 7+ | 靠后位置，仅作为补充提及 | 需要针对性优化，分析排名靠前的竞品引用了什么来源 |

#### 情感倾向处理

| sentiment | 解读 | 建议 |
|-----------|------|------|
| positive | AI 对品牌评价正面 | 好消息，可以截图用于品牌宣传素材 |
| neutral | AI 客观陈述，无明显倾向 | 正常状态，可通过优化内容引导更正面的表述 |
| negative | AI 对品牌有负面评价 | 需要重点关注。分析 answer 全文找到负面表述的来源，通过发布正面内容稀释负面信息 |

#### 引用来源分析

citations 是 GEO 优化的核心线索：
- **用户自有域名出现在 citations 中** — 说明品牌内容已被 AI 平台收录和引用，这是最理想的状态
- **citations 中全是第三方域名** — AI 平台引用的是别人写的关于品牌的内容，品牌对叙事缺乏控制力。建议在自有渠道发布更多权威内容
- **citations 为空** — AI 平台的回答没有标注来源，品牌提及可能来自训练数据而非实时检索。这种情况下内容分发的效果会有延迟
- **竞品域名出现在 citations 中** — 值得关注竞品的内容策略，分析他们发布了什么内容被 AI 引用

#### 跨平台对比

当多个平台的结果都返回后，重点关注：
- 哪些平台提及了品牌、哪些没有 — 不同 AI 平台的知识库更新频率和来源偏好不同
- 同一问题在不同平台的 sentiment 是否一致 — 如果某个平台特别负面，可能是该平台引用了特定的负面来源
- 各平台的 citations 重合度 — 高重合说明这些来源在 AI 生态中影响力大，值得重点维护

---

## 错误处理

### 原则
- 同一接口最多重试 1 次，连续失败 2 次后停止
- 不要反复尝试不同的绕过方式
- 明确告知用户失败原因和替代方案

### 常见错误

| 错误场景 | 处理方式 |
|---------|---------|
| 401 认证失败 | 引导用户前往 https://jike-geo.100.city 获取 API Key |
| 403 权限不足 | 检查产品归属或账号状态 |
| 500 / 服务过载 | 重试 1 次，仍失败则告知"服务暂时不可用，建议稍后再试" |
| questions generate 失败 | 告知用户原因，说明文章生成暂不可用。可直接为用户撰写 GEO 优化文章样稿作为参考 |
| articles generate 缺少 question_id | 引导用户先完成 company save → drafts generate 流程，不要尝试绕过 |
