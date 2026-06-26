# geo.py 命令参数速查表

所有命令格式：`python3 {baseDir}/scripts/geo.py <command> [action] [options]`

全局说明：
- 大部分命令支持 `--json` 输出原始 JSON
- 需要 `--product-id` 的命令，如果 config.json 中设置了 `product_id` 默认值则可省略

---

## check

检查连接和认证状态。

```bash
python3 geo.py check
```

无参数。输出配置信息、API Key（脱敏）、连接状态和用户信息。

---

## quota

查询当前用户的套餐额度。

```bash
python3 geo.py quota [--json]
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `--json` | 否 | 输出原始 JSON |

---

## products

产品管理。

```bash
python3 geo.py products <action> [options]
```

| action | 说明 | 必填参数 | 可选参数 |
|--------|------|---------|---------|
| `list` | 列出所有产品 | — | `--json` |
| `create` | 创建产品 | `--name` | `--description`, `--json` |
| `get` | 查看产品详情 | `--id` | `--json` |
| `update` | 更新产品 | `--id` | `--name`, `--description` |
| `delete` | 删除产品 | `--id` | — |

---

## company

产品的公司信息管理。

```bash
python3 geo.py company <action> [options]
```

| action | 说明 | 必填参数 | 可选参数 |
|--------|------|---------|---------|
| `get` | 查看公司信息 | `--product-id` | `--json` |
| `save` | 保存公司信息 | `--product-id` + 至少一个字段 | 见下方字段列表 |

公司信息字段（save 时建议一次性完整填写）：

| 参数 | 说明 | 必填 |
|------|------|------|
| `--product-name` | 产品名称 | ✅ |
| `--company-name` | 公司名称 | ✅ |
| `--industry` | 所属行业（互联网/IT、教育培训、医疗健康等） | ✅ |
| `--business-scope` | 业务范围（`national` 或 `regional`） | ✅ |
| `--cities` | 服务城市（business-scope 为 regional 时填写） | — |
| `--company-description` | 企业介绍（200-500字） | ✅ |
| `--product-description` | 产品介绍（200-500字） | ✅ |
| `--target-customer-type` | 客户类型（`To B` / `To C` / `To B,To C`） | ✅ |
| `--customer-description` | 目标客户描述（100-200字） | ✅ |
| `--competitors` | 竞争对手（逗号分隔） | ✅ |
| `--writing-style` | 写作风格（正式严谨型/轻松活泼型/专业技术型/营销推广型/新闻资讯型） | ✅ |
| `--contact-phone` | 联系电话 | 选填 |
| `--website` | 公司网站 | 选填 |
| `--editor-name` | 编辑名称/文章作者署名 | 选填 |
| `--description` | 简要描述 | 选填 |

---

## keywords

核心关键词管理。

```bash
python3 geo.py keywords <action> [options]
```

| action | 说明 | 必填参数 | 可选参数 |
|--------|------|---------|---------|
| `list` | 列出关键词 | `--product-id` | `--json` |
| `add` | 添加关键词 | `--product-id`, `--word` | `--json` |
| `delete` | 删除关键词 | `--product-id`, `--id` | — |

---

## questions

问题管理。

```bash
python3 geo.py questions <action> [options]
```

| action | 说明 | 必填参数 | 可选参数 |
|--------|------|---------|---------|
| `generate` | AI 生成问题 | `--product-id`, `--keywords`（关键词文本，逗号分隔） | `--json` |
| `list` | 按阶段分组列出问题 | `--product-id` | `--keyword-id`（筛选）, `--json` |
| `toggle` | 切换问题选中状态 | `--product-id`, `--id` | — |

`--keywords` 示例：`--keywords 代理记账,财税服务,财税数字化`

---

## drafts

问题草稿管理。异步生成 L1-L4 四阶段问题，支持历史记录。

```bash
python3 geo.py drafts <action> [options]
```

| action | 说明 | 必填参数 | 可选参数 |
|--------|------|---------|---------|
| `generate` | 异步生成问题草稿 | `--product-id`, `--keywords` | `--no-wait`, `--json` |
| `list` | 查看草稿历史 | `--product-id` | `--page`, `--page-size`, `--json` |
| `latest` | 获取最新草稿 | `--product-id` | `--json` |
| `get` | 查看指定草稿详情 | `--product-id`, `--id` | `--json` |
| `update` | 修改草稿内容 | `--product-id`, `--id` + 至少一个字段 | 见下方字段列表 |
| `delete` | 删除草稿 | `--product-id`, `--id` | — |

草稿内容字段（update 时至少填一个）：

| 参数 | 说明 |
|------|------|
| `--keywords` | 关键词 |
| `--inquiry` | L1 认知层问题（换行分隔） |
| `--understanding` | L2 探索层问题（换行分隔） |
| `--consideration` | L3 评估层问题（换行分隔） |
| `--purchase` | L4 决策层问题（换行分隔） |

生成行为：`generate` 默认会轮询等待生成完成，加 `--no-wait` 立即返回草稿 ID。草稿状态：`generating`（生成中）、`completed`（已完成）、`failed`（失败）。

---

## gallery

图片素材库管理。支持分类管理和图片上传/查看/删除。

```bash
python3 geo.py gallery <action> [options]
```

| action | 说明 | 必填参数 | 可选参数 |
|--------|------|---------|---------|
| `categories-list` | 查看分类列表 | `--product-id` | `--scope`, `--json` |
| `categories-create` | 创建分类 | `--product-id`, `--name` | `--scope`（默认 product）, `--json` |
| `categories-update` | 更新分类名称 | `--product-id`, `--id`, `--name` | `--json` |
| `categories-delete` | 删除分类 | `--product-id`, `--id` | — |
| `images-list` | 查看图片列表 | `--product-id` | `--scope`, `--category-id`, `--json` |
| `images-upload` | 上传图片 | `--product-id`, `--category-id`, `--file` | `--scope`（默认 product）, `--json` |
| `images-delete` | 删除图片 | `--product-id`, `--id` | — |

参数详情：

| 参数 | 说明 | 示例 |
|------|------|------|
| `--scope` | 分类/图片范围 | `--scope product`（产品级）或 `--scope public`（账号级） |
| `--category-id` | 分类 ID | `--category-id 1` |
| `--file` | 上传文件路径，支持多个 | `--file ./img1.jpg ./img2.png` |

---

## search

GEO 搜索（核心功能）。

```bash
python3 geo.py search <action> [options]
```

| action | 说明 | 必填参数 | 可选参数 |
|--------|------|---------|---------|
| `create` | 创建单次搜索 | `--product-id`, `--question` | `--brand`, `--platforms`, `--mode`, `--no-wait`, `--json` |
| `batch` | 批量搜索 | `--product-id`, `--question-ids` | `--platforms`, `--no-wait`, `--json` |
| `status` | 查询任务状态 | `--product-id`, `--task-id` | `--json` |
| `batch-status` | 查询批量任务状态 | `--product-id`, `--batch-id` | `--json` |
| `history` | 搜索历史 | `--product-id` | `--page`, `--size`, `--json` |

参数详情：

| 参数 | 说明 | 示例 |
|------|------|------|
| `--question` | 搜索问题文本 | `--question "什么是GEO优化"` |
| `--brand` | 要监控的品牌名 | `--brand "极义GEO"` |
| `--platforms` | AI 平台列表，逗号分隔 | `--platforms deepseek,kimi,qianwen,doubao` |
| `--mode` | 搜索模式，默认 `api` | `--mode api` 或 `--mode plugin` |
| `--no-wait` | 不等待结果，立即返回 task_id | 适合批量提交后统一查询 |
| `--task-id` | 单次搜索的任务 ID | `--task-id abc123` |
| `--batch-id` | 批量搜索的批次 ID | `--batch-id xyz789` |
| `--question-ids` | 问题 ID 列表，逗号分隔 | `--question-ids 1,2,3` |
| `--page` | 历史记录页码 | `--page 1` |
| `--size` | 每页条数 | `--size 20` |

可用平台 ID：`deepseek`, `kimi`, `qianwen`, `doubao`, `wenxin`, `zhipu`, `yuanbao`

默认行为：`create` 和 `batch` 会自动轮询等待结果返回，加 `--no-wait` 跳过轮询。轮询间隔和超时可在 config.json 中配置（`poll_interval` 默认 3 秒，`poll_timeout` 默认 300 秒）。

---

## articles

文章管理。

```bash
python3 geo.py articles <action> [options]
```

| action | 说明 | 必填参数 | 可选参数 |
|--------|------|---------|---------|
| `generate` | AI 生成文章 | `--product-id`, `--question-id` | `--instruction`, `--image-ids`, `--json` |
| `list` | 列出文章 | `--product-id` | `--question-id`（筛选）, `--json` |
| `get` | 查看文章详情 | `--product-id`, `--id` | `--json` |
| `update` | 更新文章 | `--product-id`, `--id` | `--title`, `--content`, `--status` |
| `delete` | 删除文章 | `--product-id`, `--id` | — |

| 参数 | 说明 | 示例 |
|------|------|------|
| `--question-id` | 关联的问题 ID | `--question-id 1` |
| `--instruction` | 生成指令/要求 | `--instruction "围绕品牌优势撰写"` |
| `--image-ids` | 插入的图片 ID，逗号分隔 | `--image-ids 1,2,3` |
| `--title` | 文章标题（update 用） | `--title "新标题"` |
| `--content` | 文章内容（update 用） | `--content "新内容"` |
| `--status` | 文章状态 | `--status draft` 或 `--status published` |

---

## publish

发布记录管理。

```bash
python3 geo.py publish <action> [options]
```

| action | 说明 | 必填参数 | 可选参数 |
|--------|------|---------|---------|
| `record` | 记录一次发布 | `--product-id`, `--article-id`, `--platform-id` | `--platform-name`, `--json` |
| `list` | 查看发布记录 | `--product-id` | `--article-id`（筛选）, `--json` |

---

## platforms

查看自媒体平台列表。

```bash
python3 geo.py platforms [--json]
```

无需 product-id。返回所有可用的自媒体分发平台（预设 + 自定义）。

---

## ai-platforms

查看支持的 AI 搜索平台列表。

```bash
python3 geo.py ai-platforms [--json]
```

无需 product-id。返回所有支持监控的 AI 搜索平台及其 ID 标识。

---

## sentiment

查看情感分析功能状态。

```bash
python3 geo.py sentiment [--json]
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `--json` | 否 | 输出原始 JSON |

无需 product-id。返回情感分析功能是否已开启（`enabled: true/false`）。情感分析用于评估 AI 搜索结果中品牌相关内容的情感倾向（positive/neutral/negative）。
