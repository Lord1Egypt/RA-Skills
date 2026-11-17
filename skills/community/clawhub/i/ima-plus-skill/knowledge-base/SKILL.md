---
name: IMA 知识库模块
description: IMA 知识库操作模块。负责上传文件、添加网页/微信文章到知识库、搜索与浏览知识库内容、获取知识库信息。
allowed-tools: Bash,Read
metadata: {"openclaw":{"emoji":"📚","requires":{"bins":["node"]}}}
---

# Knowledge Base (知识库)

API base path: `openapi/wiki/v1` — 完整数据结构和接口参数详见 `references/api.md`。

## 接口决策表

| 用户意图 | 调用接口 | 关键参数 |
| --- | --- | --- |
| 上传文件到知识库 | `check_repeated_names` → `create_media` → COS Upload → `add_knowledge` | `media_type`（按扩展名），`knowledge_base_id`，`file_name`，`file_size` |
| 上传到某个文件夹 | 先定位文件夹 → 同上（`folder_id` 传入） | 见「脚本速查」upload_to_kb |
| 添加网页/微信文章 | `import_urls` | `urls`（1-10），`knowledge_base_id`，可选 `folder_id` |
| 添加笔记到知识库 | `add_knowledge` | `media_type=11`，`note_info.content_id=<note_id>`，`knowledge_base_id` |
| 检查文件名重复 | `check_repeated_names` | `params[].name`，`params[].media_type`，`knowledge_base_id`，`folder_id` |
| 获取知识库信息 | `get_knowledge_base` | `ids`（1-20 个，包装为数组） |
| 浏览内容列表 / 文件夹 | `get_knowledge_list` | `knowledge_base_id`，`cursor`，`limit`(1~50)，可选 `folder_id` |
| 库内搜索 | `search_knowledge` | `query`，`knowledge_base_id`，`cursor` |
| 按名称找知识库 | `search_knowledge_base` | `query`，`cursor`，`limit`(1~20) |
| 查看自己有哪些知识库 | `search_knowledge_base` | `query: ""` |
| 添加内容但未指定库 | `get_addable_knowledge_base_list` | `cursor`，`limit`(1~50) |
| 查看/导出原文 | `get_media_info` | `media_id`；下载时 URL 后追加 `response-content-type=application/octet-stream&response-content-disposition=attachment;filename="<名>"` |
| 创建文件夹 | `create_folder` | `knowledge_base_id`，`name`，可选 `folder_id`（父夹） |
| 重命名文件/文件夹 | `rename_knowledge` | `knowledge_base_id`，`media_id`，`name` |
| 移动文件（**不支持文件夹**） | `move_knowledge` | `src_knowledge_base_id`，`dst_knowledge_base_id`，`infos:[{media_id}]`，可选 `dst_folder_id` |
| 获取下载链接 | `export_media_for_ima_sandbox` | `media_id`；返回 `url`+`headers`，下载需带 `headers` |
| 创建知识库 | `create_knowledge_base` | `name`(必填)，`type`(1001/1002/1004)，可选 `description`/`cover-url`/`recommended-questions` |
| 修改库基本信息 | `update_knowledge_base_basic_info` | `id`，自动推导 `update_fields`（1名 2封面 3简介 4推荐问题） |
| 置顶/取消置顶 | `set_knowledge_top` | `knowledge_base_id`，`media_id`，`is_top`(布尔) |
| 打/移除标签 | `tag_add` / `tag_remove` | `knowledge_base_id`，`item_id`(=media_id)，`tag_name` |
| 列/搜标签 | `tag_list` | `knowledge_base_id`，可选 `keyword`/`cursor`，`limit` |
| 重命名/删除标签 | `tag_rename` / `tag_delete` | 重命名新名存在自动合并；删除不可逆 |
| 修改库权限 | `update_knowledge_base_permission` | `id`，自动推导 `update_fields`（1导出状态 2加入类型） |
| 加入知识库 | `join_knowledge` | `knowledge_base_id`，`name`（**真实加入，有副作用**） |
| 批量更新访问状态 | `update_knowledge_access_status` | `knowledge_base_id`，`infos:[{media_id}]`(≤10)，`access_status`(1/2/3) |
| 广场发现 | `search_knowledge_base_in_square` | `question`(必填，**不是** query)，`cursor`(首次空)，`limit` |

**`search_knowledge_base` vs `get_addable_knowledge_base_list`**：用户说了库名 → 前者按名搜；用户没说加到哪个库 → 后者列出可选库让用户选。**绝不要**在用户已明确库名时调 `get_addable_knowledge_base_list`。

---

## ⛔ 文件上传安全门（仅文件上传 → `add_knowledge` 流程）

```
GATE 1 [TYPE]   preflight-check.cjs 先行，pass=false 直接拒绝。视频/B站/YouTube/file:// → 引导用户用 IMA 客户端。绝不问"还要试吗"
GATE 2 [NAME]   add_knowledge 的 title 必须等于 file_name（含扩展名），绝不改名/缩写/翻译
GATE 3 [DUP]    所有文件上传前先 check_repeated_names；is_repeated=true → 问用户保留两者(追加 _YYYYMMDDHHmmss)或取消；不支持替换
GATE 4 [EXIT]   cos-upload.cjs 非零退出 → 立即停止，不调 add_knowledge
```

## 上传文件到知识库

**首选一键脚本** `upload_to_kb.cjs`（封装 GATE 1-4 全部五步，自动重名处理与 JSON 解析，失败即停）：

```bash
node knowledge-base/scripts/upload_to_kb.cjs --file a.pdf --path "我的知识库/项目/文档"
node knowledge-base/scripts/upload_to_kb.cjs --file a.pdf --path "我的知识库"          # 根目录
node knowledge-base/scripts/upload_to_kb.cjs --file a.pdf --cancel-if-dup             # 重名时取消
```

目标库**必须显式指定**（`--path` 首选 / `--kb-name` 兼容 / `--folder` 指定文件夹），脚本不自动选库。批量重名检查见 `api.md`（最多 2000 个文件名）。

### 添加网页 / 微信文章 / 笔记

```bash
# 网页/微信（无 GATE，非文件）
ima_api "openapi/wiki/v1/import_urls" '{"knowledge_base_id": "<库ID>", "urls": ["https://..."], "folder_id": "<可选>"}'
# 返回 results 映射 {url: {url, ret_code, media_id}}

# 笔记 → 知识库
ima_api "openapi/wiki/v1/add_knowledge" '{"media_type": 11, "note_info": {"content_id": "<note_id>"}, "title": "笔记标题", "knowledge_base_id": "<库ID>"}'

# URL 指向可下载文件时：先探测 content-type → 下载 → preflight-check → 走上传流程（详见 api.md §URL Type Detection）
```

---

## 🌐 自然语言目录解析（统一入口，优先使用）

**所有需要知识库/文件夹的操作，用自然语言路径，禁止让用户提供 kb_id。**

```bash
node resolve_path.cjs --path "我的知识库/项目/文档"   # → { kb_id, kb_name, folder_id, folder_name }
node resolve_path.cjs --path "我的知识库"             # folder_id 空 = 根目录
node resolve_path.cjs --path "项目/文档"              # 唯一库可省略库名
```

**使用规则**：
1. 用户给了路径/名称 → **直接 `resolve_path.cjs --path`**，不要手动 search + list 逐步找 ID
2. 解析结果分层缓存（防重名串库、无 TTL、失效自愈），重复解析同一路径 0 次 API
3. 所有封装脚本支持 `--path "库名/文件夹..."` 直接传
4. 用户没给位置 → 用 `--kb-name` 或让用户选择
5. **面向用户永远只展示名称**，禁止暴露 kb_id / folder_id / media_id
6. ⛔ **禁止擅自使用 `--kb <id>`**：即使解析拿到 ID 也不得主动用，一律 `--path`；仅用户明确要求指定 ID 时可用

## 脚本速查

> 所有脚本支持 `--path "库名/文件夹..."`（自动解析），兼容 `--kb-name`。详见各脚本头部 Usage 注释。

```bash
# 文件夹：创建（可多级）/ 浏览 / 重命名 / 置顶（仅文件夹，media_type=99）
node knowledge-base/scripts/create_folder.cjs --path "库/父夹" --name "新夹"
node knowledge-base/scripts/list_all_files.cjs --path "库/夹" [--json] [--with-url]
node knowledge-base/scripts/rename_knowledge.cjs --path "库" --media-id <id> --name "新名"
node knowledge-base/scripts/set_knowledge_top.cjs --path "库" --media-id <folder_id> --is-top true   # ⚠️ 仅文件夹，文件报 220001

# 移动（仅文件，≤10 个） / 导出媒体
node knowledge-base/scripts/move_knowledge.cjs --src-path "库A" --dst-path "库B/目标夹" --media-id id1,id2
node knowledge-base/scripts/export_media.cjs --media-id <id> [--download --out /path/save]

# 标签（文件夹不支持打标签；rename 重名自动合并、delete 不可逆，调用前确认）
node knowledge-base/scripts/tag_add.cjs --path "库" --media-id <id> --tag-name "重要"
node knowledge-base/scripts/tag_remove.cjs --path "库" --media-id <id> --tag-name "重要"
node knowledge-base/scripts/tag_list.cjs --path "库" [--keyword 关键词]
node knowledge-base/scripts/tag_rename.cjs --path "库" --old-tag-name 旧 --new-tag-name 新
node knowledge-base/scripts/tag_delete.cjs --path "库" --tag-name 待删

# 知识库管理（普通成员写操作会 220030，需创建者/协作成员/管理员）
node knowledge-base/scripts/create_knowledge_base.cjs --name "库名" --type 1001        # 1001个人 1002共享 1004订阅
node knowledge-base/scripts/update_knowledge_base_basic_info.cjs --path "库" --name 新名 [--description 简介]
node knowledge-base/scripts/update_knowledge_base_permission.cjs --path "库" --visible-export-status 3 [--join-type 1]  # ⚠️ 影响全库成员，调用前确认
node knowledge-base/scripts/update_knowledge_access_status.cjs --path "库" --media-id id1,id2 --access-status 3

# 广场发现 / 加入（join 真实加入公开库，调用前确认用户确实要加）
node knowledge-base/scripts/search_knowledge_base_in_square.cjs --question "关键词"
node knowledge-base/scripts/join_knowledge.cjs --path "知识库名称" --name "知识库名称"
```

## 打包导出为 zip（整库 / 文件夹 / 多文件）

```bash
# ① 整个库 / ② 某个文件夹（递归）/ ③ 指定多文件（--media-ids）
node knowledge-base/scripts/export_kb_zip.cjs --path "我的知识库" --out /path/out.zip
node knowledge-base/scripts/export_kb_zip.cjs --path "我的知识库/项目" --out /path/out.zip
node knowledge-base/scripts/export_kb_zip.cjs --path "我的知识库" --media-ids id1,id2 --out /path/out.zip

# 打包前先看调用量：--count（JSON）/ --estimate / --dry-run（列出将导出的文件）
node knowledge-base/scripts/export_kb_zip.cjs --path "我的知识库" --count
```

- 导出需 API key **开通导出权限**（凭证见主 SKILL.md「Credential Check」；agent-interface 普通 key 会 220030）
- 超 50 次/分钟自动限速；单文件失败跳过不中断，全部失败不生成 zip
- ⚠️ 订阅库（普通成员）不可下载，引导用户到 IMA 客户端
- 完整 SOP 见 `references/troubleshooting.md`「批量导出打包 SOP」

---

## 查询类工作流

```bash
# 库信息 / 浏览 / 搜索 / 可添加库列表
ima_api "openapi/wiki/v1/get_knowledge_base" '{"ids": ["<库ID>"]}'
ima_api "openapi/wiki/v1/get_knowledge_list" '{"knowledge_base_id": "<库ID>", "cursor": "", "limit": 20}'
ima_api "openapi/wiki/v1/search_knowledge" '{"query": "关键词", "knowledge_base_id": "<库ID>", "cursor": ""}'
ima_api "openapi/wiki/v1/get_addable_knowledge_base_list" '{"cursor": "", "limit": 20}'

# 原文内容（get_media_info）处理分支：
#   media_type=11 且有 notebook_ext_info.notebook_id → 作为 note_id 走 notes 模块 get_doc_content
#   url_info.url 非空 → 用 url+headers 请求原文
#   否则 → 提示用户用 IMA 客户端查看原文
```

`list_all_files.cjs` 递归遍历全库输出目录树（限深 20、单目录 2500 条保护），`--json` 输出结构化数组，`--with-url` 逐个拿下载链接（订阅库多为空/220030）。

## 分页 / 响应 / 用户体验

- **分页**：所有列表/搜索接口游标分页，首次 `cursor: ""`，用 `next_cursor` 翻页，`is_end=true` 停止
- **响应**：统一 `{ code, msg, data }`；`code=0` 成功，`code≠0` 直接展示 `msg`
- **隐藏 ID**：面向用户永不暴露 `knowledge_base_id` / `media_id` / `folder_id`，只展示名称
- **精简进度**：不暴露内部步骤，只报告结果（如「正在上传 report.pdf…」→「已添加到知识库「XX」✓」）；批量操作汇总成功/失败
- **格式化展示**：库列表带描述（ID 列表调 `get_knowledge_base` 补描述）；内容列表带 📁/📄 前缀与文件数；搜索结果显示所在文件夹

## 注意事项

- 文件夹是知识条目（`media_type=99`），其 `media_id` 即 `folder_id`
- 扩展名用于 `media_type` 检测与 `file_ext`（无点号，如 `pdf`）；COS `--content-type` 传实际 MIME
- URL 入库先检测是否文件型 → `api.md §URL Type Detection`；MediaType 枚举/大小限制 → `api.md §MediaType`
- **IMA OpenAPI 不支持删除任何实体**（文件/文件夹/库），需客户端手动清理
- 错误码（220030 / 51 / 220001 等）先读 `references/troubleshooting.md`
