---
name: ht-skills
description: 管理灏天文库文集和文档，支持新建文集、新建文档、查询文集/文档、更新文档、修改文档归属、管理文档层级、查询个人花园限制与用量；支持文档片段 RAG 检索、图片上传到 COS、图片分组、查询图片列表/详情与图片额度。适用于 OpenClaw 自主写文章并上传、文集创建、文档入库、知识检索、文档移动、插图上传与外链等场景。
allowed-tools: [bash]
environment-variables:
  - HT_SKILL_SERVER_URL
  - HT_SKILL_TOKEN
config-files:
  - config.json
---

# ht-skills 灏天文库管理（客户端）

通过服务端 API 调用，需配置 `config.json` 中的`token`（个人 API Token）。

---

## 客户端注意事项（必须遵守）

- **个人花园范围**：`list_collections` / `get_collection` / 新建与修改文档等读写操作**仅针对个人花园**（`source_type=garden`）；用户在灏天文库网页上的精品文集等非花园文集不会出现在列表中，也无法通过 ht-skills 操作。
- **查询文集列表**：无 `--limit`、`--offset`；仅返回当前用户的**个人花园**文集。
- **查询文档列表**：必须带 `--collection-id`（文集 ID）；若没有文集 ID，需先 `list_collections.py --name "文集名称"` 查询，或**向用户询问目标文集名称**。
- **查询文档列表**：无 `--limit`、`--offset`。
- **更新文档**：`author` 字段不可更新，只能更新 name、content、sort、parent。
- **修改文档归属**：需有目标文集权限；文档属于多个文集时需指定 `--from-collection-id`。
- **图片上传**：需本地可读图片路径；大文件上传耗时较长。上传成功后响应中的 `file_url` 可直接用于正文插图。
- **图片分组**：使用 `--group-id` 前可用 `list_image_groups.py` 查询分组 ID；分组必须属于当前用户。
- **RAG 文档片段检索**：`--collection-ids` 须为**灏天文库公开精品文集 ID**（见下方公开目录链接）；**不要**用 `list_collections.py` 查个人花园文集 ID 来做 RAG 检索。

---

## 智能体执行规范（必须遵守）

### 规范一：修改特定文档

1. **先查询**：使用 `list_documents.py --collection-id <文集ID> --name "关键词"` 或 `get_document.py --id <ID>` 定位要修改的文档，确认文档 ID。
2. **再修改**：使用 `update_document.py --id <ID>` 修改标题、正文。

### 规范二：添加特定文档

1. **文集必填**：用户必须提供目标文集。若用户未提供或只说「随便加」「你决定」等，**必须主动询问**：「请告知要将文档添加到的文集名称」。
2. **查询文集 ID**：用户给出文集名称后，用 `list_collections.py --name "文集名称"` 查询文集 ID；若不存在则询问是否新建。
3. **添加文档**：使用 `add_document.py --collection-id <ID> --name "标题" [--content 内容] [--content-file 文件路径]`。

### 规范三：添加文集

1. **用户确认**：新建文集前**必须**让用户确认要创建的文集名称，例如：「将创建文集「xxx」，请确认名称是否正确？」。
2. **确认后再执行**：用户确认后再执行 `create_collection.py --name "文集名称"`。若使用 `--get-if-exists` 则同名已存在时直接返回已有 ID，不重复创建。

### 规范四：修改文档归属

1. **先定位文档**：用 `list_documents.py --collection-id <文集ID> --name "关键词"` 或 `get_document.py --id <ID>` 确认文档 ID。
2. **确认目标文集**：用户需提供目标文集名称或 ID；若无则 `list_collections.py --name "关键词"` 查询。
3. **执行移动**：使用 `move_document.py --id <文档ID> --collection-id <目标文集ID>`；文档属于多个文集时需加 `--from-collection-id <原文集ID>`。

### 规范五：上传图片并用于文档

1. **可选分组**：若用户要归类图片，先 `list_image_groups.py` 或 `create_image_group.py --name "分组名"` 取得 `group_id`。
2. **检查额度**（可选）：`get_image_limits_usage.py` 确认 `can_upload`。
3. **上传**：`upload_image.py --file "路径" [--remark "说明"] [--group-id N]`。
4. **使用链接**：从返回 JSON 的 `data.file_url`（或 `data.file_path` 自行拼域名）插入文档 Markdown/HTML；勿猜测 URL。

### 规范六：文档片段检索（RAG）

1. **明确检索问题**：用户给出要问的内容或关键词，作为 `--content`。
2. **确定目标文集 ID**（必填，最多 5 个）：
   - **公开精品文集 ID** 从灏天文库官方目录获取（含 ID 与名称对照表）：
     - [灏天文库文集完整目录公开](https://aiknowledge.cn/article/66521-%E7%81%8F%E5%A4%A9%E6%96%87%E5%BA%93%E6%96%87%E9%9B%86%E5%AE%8C%E6%95%B4%E7%9B%AE%E5%BD%95%E5%85%AC%E5%BC%80)
   - 在目录中按分类或搜索找到与用户问题相关的**文集名称**，取表格 **ID** 列的数字（如 `189` 对应「AI 大模型」）。
   - **勿用** `list_collections.py`：该接口只返回当前用户**个人花园**文集，与 RAG 索引的公开精品文集不是同一套数据。
   - 若用户只说了领域/主题（如「人工智能」）而未指定具体文集，应先在公开目录中挑选 1～5 个最相关的文集 ID，必要时向用户确认。
3. **执行检索**：
   ```bash
   python scripts/retrieve_documents.py --content "用户的问题" --collection-ids 189 907
   ```
4. **使用返回结果**：响应中的 `sources` 为相关片段及出处（文集名、文档名、`source` 字段等）；本接口**不调用大模型**，由智能体根据片段自行组织回答或引用。若响应含 `warning`，说明传入文集超过 5 个，已自动截断。

### 规范七：个人花园配额与会员（写操作前建议执行）

1. **写操作前先查配额**：新建文集、新建文档、移动文档、更新较长正文前，先执行 `get_garden_limits_usage.py`，确认 `usage.can_create_collection`、目标文集的 `documents_quota` 及 `limits.max_chars_per_document`。
2. **解读会员状态**：响应 `data.membership.is_member` 为 `true` 表示当前为会员（`member_status=1`）；实际配额上限仍以 `data.limits` 为准（由灏天文库计算，含等级 tier 与会员倍数）。
3. **会员失效提示**：若 `is_member` 为 `false` 且某文集 `documents_quota.used` 已超过当前 `limit`，应告知用户「存量保留，但不能再新建/扩容」；更新超长正文可能因字数上限被 403 拒绝。
4. **配额不足时**：不要强行重试写接口；向用户说明当前 `已用/上限`（如 `collections_quota.text`、`documents_quota.text`），建议删减内容、更换文集或续费会员后再操作。

### 规范八：申请花园文集晋升精品文集

1. **与个人花园维护不同**：晋升是把**已有**个人花园文集申请变为平台精品文集；记录写入 `sys_collection_upload`，由管理员在灏天文库「文集审核管理」审核。
2. **提交前先查额度**：`check_garden_promotion_quota.py`，确认 `can_submit` 为 true（每用户 24 小时最多 1 次）。
3. **确认文集 ID**：`list_collections.py` 或 `get_collection.py`；文集内应已有文档。
4. **提交**：`request_garden_promotion.py --collection-id <ID> [--reason "说明"]`。
5. **跟踪**：`list_my_garden_promotion_requests.py`（status：0 待审、1 通过、2 驳回）。

---

## 前置条件

1. **config.json**：在 client 目录配置 `config.json`，填写`token`。
2. **环境变量**（可选）：`HT_SKILL_SERVER_URL`、`HT_SKILL_TOKEN` 优先级高于 config.json。
3. **依赖**：`pip install requests`

## 脚本目录

所有脚本位于 `scripts/`，在 client 根目录执行。

## 功能一：新建文集（支持有则用、无则建）

```bash
python scripts/create_collection.py --name "文集名称" [--description "50字内简介"] [--brief "500字以上详细介绍"]
python scripts/create_collection.py --name "文集名称" --get-if-exists
```

## 功能二：新建文档到指定文集

```bash
python scripts/add_document.py --collection-id 123 --name "文档标题" [--content "正文"] [--content-file 路径] [--parent 0]
```

## 功能三：查询文集列表

```bash
python scripts/list_collections.py [--name "关键词"]
```

## 功能四：查询文集详情

```bash
python scripts/get_collection.py --id 123 [--include-docs]
```

## 功能五：查询文档列表

```bash
python scripts/list_documents.py --collection-id 123 [--name "关键词"]
# collection-id 必填。若无文集 ID，需先 list_collections 查询或向用户询问
```

## 功能六：查询文档详情

```bash
python scripts/get_document.py --id 456
```

## 功能七：更新文档（修订已发文章）

```bash
python scripts/update_document.py --id 456 --name "新标题"
python scripts/update_document.py --id 456 --content "新正文"
python scripts/update_document.py --id 456 --content-file 文件路径
python scripts/update_document.py --id 456 --sort 50
python scripts/update_document.py --id 456 --parent 0
```

## 功能八：修改文档归属（移动到目标文集）

```bash
# 将文档移动到目标文集
python scripts/move_document.py --id 456 --collection-id 789

# 文档属于多个文集时，需指定原文集 ID
python scripts/move_document.py --id 456 --collection-id 789 --from-collection-id 123
```

- `--id`：文档 ID（必填）
- `--collection-id`：目标文集 ID（必填）
- `--from-collection-id`：原文集 ID；文档只属于一个文集可不填，属于多个文集则必填

## 功能九：设置文档父级（文集内层级）

```bash
python scripts/set_document_parent.py --collection-id 123 --document-id 456 --parent 0 [--sort 1]
```

- `parent=0` 表示根文档；同级别 `sort` 越小越靠前

## 功能十：查询当前用户个人花园限制与用量

```bash
python scripts/get_garden_limits_usage.py
```

- 无参数，返回当前用户**个人花园**的限制与占用情况（仅统计 `source_type=garden` 文集）
- 占用字段使用更直观的 `已用/上限` 结构（如 `3/10`、`18/100`）
- 响应含 `data.membership`（`is_member`、`member_status`），便于向用户解释会员与配额；实际上限以 `data.limits` 为准

## 功能十一：图片分组

```bash
python scripts/create_image_group.py --name "分组名称"
python scripts/list_image_groups.py [--limit 100] [--offset 0]
python scripts/update_image_group.py --id <分组ID> --name "新名称"
```

## 功能十二：图片上传与查询

```bash
python scripts/get_image_limits_usage.py
python scripts/upload_image.py --file "图片路径" [--remark "备注"] [--group-id N]
python scripts/list_images.py [--group-id N] [--name "文件名关键词"] [--limit 50] [--offset 0]
python scripts/get_image.py --id <图片ID>
```

- 上传成功后的 `data.file_url` 为可访问地址（依赖服务端 `cos.public_base_url` 或 `cos.domain` 配置）
- `list_images.py` 的 `--name` 对应服务端查询参数 `file_name`（文件名模糊匹配）

## 功能十三：文档片段检索（RAG）

从灏天文库 RAG 向量索引中检索与问题相关的文档片段及出处，**不调用大模型**。

### 文集 ID 从哪里获取？

RAG 检索针对的是平台**公开精品文集**（已入库向量索引），ID 与名称对照见官方目录：

**[灏天文库文集完整目录公开](https://aiknowledge.cn/article/66521-%E7%81%8F%E5%A4%A9%E6%96%87%E5%BA%93%E6%96%87%E9%9B%86%E5%AE%8C%E6%95%B4%E7%9B%AE%E5%BD%95%E5%85%AC%E5%BC%80)**

目录按领域分类（如「人工智能与大模型」「编程语言与开发框架」等），每行格式为 **ID | 文集名称**。执行检索时，将表格中的 **ID 数字** 作为 `--collection-ids` 传入即可（如 ID `189` 可写 `189` 或 `collection_189`）。

> **注意**：`list_collections.py` 只能查到当前用户自己的**个人花园**文集，不能替代上述公开目录；做 RAG 检索时请以上述链接为准。

### 命令示例

```bash
# 在公开目录中查到「AI 大模型」ID 为 189、「人工智能基础」ID 为 907 后：
python scripts/retrieve_documents.py --content "什么是 Transformer？" --collection-ids 189 907

# ID 也可带 collection_ 前缀
python scripts/retrieve_documents.py --content "检索内容" --collection-ids collection_189
```

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--content` | 是 | 检索内容/用户问题 |
| `--collection-ids` | 是 | 文集 ID 列表，从[公开目录](https://aiknowledge.cn/article/66521-%E7%81%8F%E5%A4%A9%E6%96%87%E5%BA%93%E6%96%87%E9%9B%86%E5%AE%8C%E6%95%B4%E7%9B%AE%E5%BD%95%E5%85%AC%E5%BC%80)获取；支持 `21` 或 `collection_21`；**最多 5 个**，超出仅使用前 5 个并返回 `warning` |

### 返回结果怎么用

- `sources`：命中的文档片段列表，含 `content`（片段）、`document_name`、`collection_name`、`source`（出处描述）、`distance`（相似度）等
- `collection_info`：实际检索的文集、未建索引文集等汇总信息
- 智能体应基于 `sources` 组织回答，并注明引用出处；勿编造目录中不存在的文集 ID

## 功能十四：花园文集晋升申请

```bash
python scripts/check_garden_promotion_quota.py
python scripts/request_garden_promotion.py --collection-id <文集ID> [--reason "申请说明"]
python scripts/list_my_garden_promotion_requests.py [--limit 50] [--offset 0]
```

- 仅针对当前用户的**个人花园**文集（`source_type=garden`）
- 每用户 **24 小时最多 1 次**晋升申请
- 审核在灏天文库后台「文集审核管理」进行，通过后文集变为精品文集（`source_type=collection`）
