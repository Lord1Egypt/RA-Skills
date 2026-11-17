# Ingest（摄取）操作

> Karpathy 三大操作之首。完整覆盖"资料入库到 Wiki 演化"的全部过程。
> 核心理念：**一次 Ingest 可能级联更新多个导览（知识复利）**。

## 1. 子任务流水线

```
Collect（收集） → Check（检查） → Link（链接特性） → Compile（编译） → Write（写入） → Cascade（级联）
   ↓                ↓                ↓                ↓                ↓              ↓
 阶段 1.1          阶段 1.2          阶段 1.3          阶段 1.4          阶段 1.5       阶段 1.6
```

## 2. Collect（收集）

### 2.1 资料来源

- 用户上传的文件（PDF/DOCX/PPTX/XLSX 等）
- 已有 IMA 知识库的内容
- 联网搜索（用 `search(source="web")`）
- 网页链接（用 `import_urls`）

### 2.2 收集方式

| 来源 | API | 说明 |
|------|-----|------|
| 用户上传文件 | `upload_file` | 上传到指定知识库 |
| 导入网页 | `import_urls` | 批量导入 URL |
| 已有知识库 | `get_knowledge_list` | 逐级浏览 |
| 用户上传笔记 | `add_knowledge` | 关联到知识库 |
| 联网搜索 | `search(source="web")` | 补充资料 |

### 2.3 资料完整性原则

> "此阶段追求完整性，不追求结构" — 所有资料都是后续编译的"原材料"

详见 [link-handling.md](link-handling.md) 第 1 节和 [api-reference.md](api-reference.md) 第 5.1 节

## 3. Check（检查）

### 3.1 是否有旧导览？

```bash
# 在目标文件夹搜索标题包含"主题导览"的笔记
curl -s -X POST "https://ima.qq.com/openapi/note/v1/search_note" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"search_type": 0, "query_info": {"title": "主题导览"}, "start": 0, "end": 20}'
```

或者用标签筛选（推荐）：
```bash
# 列出所有带"状态:已编译"标签的导览
get_knowledge_list(kb_id=X, tags=["状态:已编译"])
```

### 3.2 判断

| 情况 | 处理方式 |
|------|---------|
| 有旧导览（目标主题） | **增量更新**：Compile 模式 2 |
| 有其他主题导览 | **新建**：Compile 模式 1 |
| 没有任何知识导览 | **新建**：Compile 模式 1 |

详见 [versioning.md](versioning.md) 第 4 节

## 4. Link（链接特性）

每个文件能否在导览中链接？这是 Karpathy **"可追溯到 raw"** 的核心要求。

### 4.1 media_type 速查表（IMA 完整版）

| 值 | 类型 | 链接策略 |
|----|------|---------|
| 1 | PDF 文件 | ⚠️ 标注"请在知识库查看" |
| 2 | 网页 | ✅ 获取真实 URL |
| 3 | Word 文件 | ⚠️ 标注"请在知识库查看" |
| 4 | PPT 文件 | ⚠️ 标注"请在知识库查看" |
| 5 | Excel 文件 | ⚠️ 标注"请在知识库查看" |
| 6 | 公众号文章 | ✅ 获取真实 URL |
| 7 | Markdown | ⚠️ 不内嵌链接，写为纯文本 |
| 9 | 图片 | ⚠️ 标注"请在知识库查看" |
| 11 | 笔记 | ⚠️ 不内嵌链接，写为纯文本 |
| 12 | QA 对话 | ⚠️ 标注"请在知识库查看" |
| 13 | TXT 文本 | ⚠️ 不内嵌链接，写为纯文本 |
| 14 | Xmind | ⚠️ 标注"请在知识库查看" |
| 15 | 录音 | ⚠️ 标注"请在知识库查看" |
| 16 | 网页视频 | ⚠️ 标注"请在知识库查看" |
| 17 | 对话 | ⚠️ 标注"请在知识库查看" |
| 18 | 视频 | ⚠️ 标注"请在知识库查看" |
| 19 | 播客 | ⚠️ 标注"请在知识库查看" |
| 20 | HTML | ⚠️ 标注"请在知识库查看" |
| 21 | EPUB 文件 | ⚠️ 标注"请在知识库查看" |
| 99 | 文件夹 | ❌ 不可链接 |

详见 [link-handling.md](link-handling.md) 第 2 节

### 4.2 链接特性表模板

```markdown
| media_id | title | media_type | 链接策略 | URL/备注 |
|---------|-------|-----------|---------|---------|
| xxx | 文章A | 2 | ✅ 可内嵌 | https://... |
| xxx | 文章B | 6 | ✅ 可内嵌 | https://... |
| xxx | 文章C | 7 | ⚠️ 不内嵌 | 请在知识库中查看 |
```

## 5. Compile（编译）

### 5.1 模式 1：新建（5 步法）

1. **明确主题** — 确定核心概念（主题定位、核心概念、边界范围）
2. **梳理关键词** — 提取关键要素（每概念 3-5 个子主题）
3. **发现关系** — 找出逻辑关联（层级、并列、因果、对立）
4. **呈现结构** — 可视化知识网络（表格 + 学习路径）
5. **美化优化** — 提升可读性（标题规范、排版、信息密度）

### 5.2 模式 2：增量更新（6 步法）

1. **读旧版** — `export_note` 获取旧版本内容
2. **提取版本信息** — 从 frontmatter 读取 version/changelog
3. **对比增量** — 比对文件夹中文件与导览 sources[]
4. **识别变化** — 新增/删除/概念变化
5. **更新导览** — `append_doc`（推荐）或 `update_note`（精细）
6. **更新版本号** — patch/minor/major

详见 [guide-template.md](guide-template.md) 和 [versioning.md](versioning.md)

## 6. Write（写入）

### 6.1 选项 A：新建笔记（最简单）

```bash
curl -s -X POST "https://ima.qq.com/openapi/note/v1/import_doc" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content_format": 1,
    "content": "<完整 Markdown>",
    "title": "📖 主题导览：[主题名称]",
    "folder_id": "<目标笔记本 ID>"
  }'
# 返回: {"code": 0, "data": {"note_id": "xxx"}}
```

### 6.2 选项 B：追加内容（增量推荐）

```bash
curl -s -X POST "https://ima.qq.com/openapi/note/v1/append_doc" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{
    "note_id": "<已有导览 ID>",
    "content_format": 1,
    "content": "<追加内容>"
  }'
```

**优势**：不破坏原有结构，原子化操作。

### 6.3 选项 C：按 block 编辑（精细修改）

```bash
# 第一步：导出 block 结构
curl -s -X POST "https://ima.qq.com/openapi/note/v1/export_note_blocks" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"note_id": "<note_id>"}'

# 第二步：按 block_id 修改
curl -s -X POST "https://ima.qq.com/openapi/note/v1/update_note" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{
    "note_id": "<note_id>",
    "block_id": "<block_id>",
    "content": "<新内容>"
  }'
```

详见 [write-and-verify.md](write-and-verify.md)

### 6.4 立即验证

> **重要**：笔记创建接口返回成功不代表内容完整，必须立即验证。

```bash
# 导出并比对
curl -s -X POST "https://ima.qq.com/openapi/note/v1/export_note" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"note_id":"<note_id>","target_content_format":1}' | \
python3 -c "
import sys, json, urllib.request
d = json.load(sys.stdin)
if d['code'] == 0:
    url = d['data']['content_url']  # COS 链接，3 小时时效
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req)
    print(resp.read().decode('utf-8'))
"
```

## 7. Cascade（级联）— **append_doc 模式（v1.1.0 重构版）**

> 一次 Ingest 可能触动多个导览（不仅是新文件所在的那个）— 这是 wiki 知识复利的关键。
> **v1.1.0 关键变化**：从"创建新笔记"改为"append_doc 原地更新"，更适合普通用户工作流。

### 7.1 ⚠️ v1.1.0 设计取舍

| 维度 | v1.0.x 创建新笔记 | **v1.1.0 append_doc** |
|------|------------------|---------------------|
| API 调用 | `import_doc`（创建新笔记） | `append_doc`（追加正文） |
| frontmatter 更新 | ✅ 创建时可控 | ❌ **永远不变**（version/changelog/updated） |
| 碎片笔记 | ⚠️ 多版本笔记 | ✅ 单个笔记持续演进 |
| IMA 客户端回滚 | ❌ 难 | ✅ **容易（直接看历史）** |
| 用户期望对齐 | 偏离"git 提交"模型 | ✅ **符合"原地修改"直觉** |
| IMA 客户端历史 | ✅ 已有 | 直接在 IMA 客户端查看历史版本 |

**核心洞察**：**frontmatter 不可变 ≠ 必须创建新笔记**。
IMA 平台允许 `append_doc` 改正文，不允许改 frontmatter。v1.1.0 选择"放弃 frontmatter 演进"换取"用户期望的原地修改"。

### 7.2 Cascade 触发条件

- 新文件被 Ingest 后
- 自动计算它与所有现有导览的相关性
- 相关度 > 阈值 的导览加入"待更新列表"

### 7.3 Cascade 算法（v1.1.0 append_doc 模式）

```python
def cascade_append(new_file, all_guides, kb_id, notebook_id):
    """Cascade 算法 v1.1.0：append_doc 模式"""
    affected = []

    # === 阶段 1：标签 Jaccard 粗筛（纯 API）===
    new_tags = set(new_file.get("tags", []))
    candidate_guides = []

    for guide in all_guides:
        guide_tags = set(guide.get("tags", []))
        if not (new_tags | guide_tags):
            continue
        jaccard = len(new_tags & guide_tags) / len(new_tags | guide_tags)

        folder_bonus = 0.3 if new_file.get("parent_folder_id") == guide.get("parent_folder_id") else 0
        keyword_bonus = 0.3 if any(
            kw in guide["title"] for kw in extract_keywords(new_file["title"])
        ) else 0

        total_score = jaccard + folder_bonus + keyword_bonus
        if total_score > 0.5:  # 阈值
            candidate_guides.append({
                "guide": guide,
                "score": total_score,
                "reason": "tag_overlap" if jaccard >= 0.4 else ("folder_match" if folder_bonus else "title_match")
            })

    candidate_guides.sort(key=lambda x: -x["score"])
    candidate_guides = candidate_guides[:3]  # 最多 3 个导览

    # === 阶段 2：用户确认（必选）===
    print(f"📋 Cascade 候选导览：{len(candidate_guides)} 个")
    for c in candidate_guides:
        print(f"  - {c['guide']['title']} (相关度: {c['score']:.2f}, 原因: {c['reason']})")

    if not user_confirms():
        print("❌ 用户未确认，跳过 Cascade")
        return []

    # === 阶段 3：append_doc 模式（关键步骤）===
    affected = []
    for candidate in candidate_guides:
        guide = candidate["guide"]
        result = append_cascade_to_guide(guide, new_file, notebook_id)
        affected.append(result)

    return affected


def append_cascade_to_guide(guide, new_file, notebook_id):
    """对单个导览执行 append_doc 级联"""

    # 1. 读当前正文（从 COS URL 下载）
    current_content = download_note(guide["note_id"])

    # 3. LLM 生成新章节（包含新文章引用 + Cascade 标记）
    new_section = llm_generate_cascade_section(current_content, new_file)

    # 4. append_doc 追加到原笔记（**不改 frontmatter**）
    ima_api("openapi/note/v1/append_doc", {
        "note_id": guide["note_id"],
        "content_format": 1,
        "content": new_section
    })

    return {
        "guide_note_id": guide["note_id"],
        "score": ...,
        "new_section_added": new_section[:200]
    }




def llm_generate_cascade_section(current_content, new_file):
    """LLM 生成级联追加内容"""
    prompt = f"""当前导览末尾追加一段内容，反映新文件的纳入。

新文件：
- 标题：{new_file['title']}
- 摘要：{new_file.get('summary', 'N/A')}
- 媒体类型：{new_file['media_type']}

当前导览片段（末尾部分）：
{current_content[-500:]}  # 只看末尾

要求：
1. 输出一段 markdown，标记为"## 📌 新增 [{today()}]"
2. 包含新文件的标题 + 简要说明为什么相关
3. 不要修改原内容
4. 如果是 type 2/6 文件，附带 URL；否则标注"请在知识库查看"
5. 简洁，1-3 段

输出示例：

## 📌 新增 [{today()}]

**{new_file['title']}**

[简要说明：这篇文章与本导览的关联点]

[链接策略]
"""

    return call_llm(prompt)
```

### 7.4 Cascade 完整示例

**场景**：用户上传"遗传算法在量化交易中的应用"到"AI 量化与深度学习"文件夹。

**已有导览清单**：
- 📖 AI 量化与深度学习（v1.5 创建时的 frontmatter）
- 📖 因子与资产定价
- 📖 高频交易与微观结构

**Cascade 过程**：

| 导览 | 标签匹配 | Jaccard | 文件夹 | 总分 | 是否 Cascade |
|------|---------|---------|--------|------|-------------|
| AI 量化与深度学习 | ✅ `机器学习` | 0.7 | ✅ 同文件夹 | 1.3 | ✅ |
| 因子与资产定价 | ❌ | 0 | ❌ | 0 | ❌ |
| 高频交易 | ❌ | 0 | ❌ | 0 | ❌ |

**执行结果**：

```
[1] LLM 生成追加内容：

## 📌 新增 [2026-09-29]

**遗传算法在量化交易中的应用**

本文讨论遗传算法在量化交易中的策略优化，与本导览"机器学习理论方法"核心概念直接相关。

[《遗传算法在量化交易中的应用》](URL)

---

[3] append_doc → 笔记末尾追加上述内容

[4] 报告：✓ Cascade 完成：1 个导览更新
```

### 7.5 Cascade 后的笔记状态

**frontmatter 不变**（v1.5 创建时的）：
```yaml
---
title: 📖 主题导览：AI 量化与深度学习
type: guide
confidence: medium
created: 2026-05-13
updated: 2026-05-13  # ← 不变
version: 1.0  # ← 不变（IMA 不允许改）
changelog: [...]  # ← 不变
sources: [...]  # 不变（但 LLM 推理认为新文章不在内）
---
```

**正文末尾追加**：
```markdown
[原有完整导览内容...]

---

## 📌 新增 [2026-09-29]

**遗传算法在量化交易中的应用**

[简要说明]

[《遗传算法在量化交易中的应用》](URL)
```

### 7.6 Cascade 的成本控制

| 控制项 | 措施 |
|--------|------|
| 阈值 | Jaccard + 文件夹 + 标题匹配，阈值 0.5 |
| 数量限制 | 最多 3 个导览 |
| 用户确认 | 必选 |
| IMA 客户端历史 | 用户在 IMA 客户端查看历史版本 |
| 可关闭 | `cascade_enabled: false` 可停用 |

### 7.7 与 v1.0.x 版本的对比

| 维度 | v1.0.x 创建新笔记 | v1.1.0 append_doc |
|------|------------------|---------------------|
| 用户工作流 | 看到"v1.5 → v1.6"标签演化 | 看到一篇导览持续丰富 |
| 碎片问题 | 每个导览多个版本笔记 | 每个导览单笔记持续演进 |
| IMA 客户端搜索 | 找到多个同名笔记 | 找到一个笔记 |
| frontmatter 演进 | ✅ 真实 | ❌ 永远不变 |
| Lint 检查 updated 准确性 | ✅ | ⚠️ 不准，建议在 IMA 客户端查看 modify_time |
| **回滚方式** | 需复制旧版创建新笔记 | ✅ **直接用 IMA 客户端历史** |

### 7.8 为什么放弃"创建新笔记"？

> 我之前 v1.0.x 的设计混淆了两个目的：
> 1. **知识复利**：一次新文件影响多个导览（Cascade 的真正价值）
> 2. **版本演进**：同一导览从 v1.5 → v1.6（不是 Cascade 的本质）
>
> v1.1.0 保留目的 1（级联检测 + append_doc），放弃目的 2（创建新笔记作为版本演进）。
> **普通用户的直觉是"原地修改"，IMA 客户端的"历史版本"UI 也是为这种模型设计。**

### 7.9 IMA 限制下的取舍

| 取舍 | v1.1.0 选择 | 原因 |
|------|-------------|------|
| **保留 Cascade 多导览检测** | ✅ | 是核心价值（知识复利） |
| **append_doc 而非创建新笔记** | ✅ | 符合用户直觉 |
| **依赖 IMA 客户端历史** | ✅ | IMA 平台已支持 |
| **放弃 frontmatter 演进** | ✅ | IMA 不允许，没必要 |
| **保留版本号仅作为记录，不更新** | ✅ | 真实反映"这是同一篇笔记" |



## 8. 导览清单（Index）

> Karpathy 的 `index.md` 在 IMA 平台没有等价物，但我们用"主题导览清单"代替。

### 8.1 如何获取

```bash
# 方法 1：用标签筛选所有"已编译"导览
get_knowledge_list(kb_id=X, tags=["状态:已编译"])

# 方法 2：用 search_note 按标题定位
search_note(search_type=0, query_info={title: "主题导览"})
```

### 8.2 清单示例

| 主题导览 | 位置 | 版本 | 最后更新 | confidence |
|---------|------|:----:|:--------:|:----------:|
| 📖 主题导览：因子与资产定价 | 因子与资产定价/ | v2.3 | 2026-08-01 | high |
| 📖 主题导览：AI 量化与深度学习 | AI 量化与深度学习/ | v1.5 | 2026-07-15 | medium |
| 📖 主题导览：高频交易 | 高频交易与微观结构/ | v3.0 | 2026-06-20 | high |

### 8.3 清单的用途

- LLM 评估新文件该更新哪些导览（Cascade 算法输入）
- Lint 报告展示知识库全貌
- 用户了解"我有哪些导览"

## 9. 完整工作流示例

**场景**：用户在"AI 量化与深度学习"知识库上传一篇新文章"遗传算法在量化交易中的应用"。

```
[Ingest 触发]
   ↓
[Collect] upload_file 上传文件 → 等待完成
   ↓
[Check] 在该文件夹搜索"主题导览"：
  - 找到 "📖 主题导览：AI 量化与深度学习"（v1.5）
  - 找到 "📖 主题导览：高频交易"（v3.0）— 但不在该文件夹，跳过
   ↓
[Link] export_media_for_ima_sandbox 获取永久 URL（如适用）
   ↓
[Compile] 增量更新模式：
  - 读旧版 → 提取版本信息（v1.5）
  - 对比增量 → 1 篇新增
  - 在"机器学习理论方法"核心概念的关键要素中补充遗传算法文章
  - 评估 confidence：medium → medium（无变化）
   ↓
[Write] 用 append_doc 追加内容（不重建整个笔记）
  - note_id: xxx
  - content: <新的关键要素块>
   ↓
[Cascade] 检查其他导览：
  - "因子与资产定价" → 相关度 0.3，不更新
  - "高频交易" → 相关度 0.4，不更新
  - 没有其他受影响导览
   ↓
[报告] 告诉用户：
  - 主更新：1 个导览更新（v1.5 → v1.6）
  - 级联：0 个其他导览受影响
  - 下次建议：可考虑建"遗传算法"独立导览
```

## 10. 关键原则总结

1. **可追溯**：每个导览的 sources[] 必须能追到 raw 资料
2. **复利**：一次 Ingest 影响多个导览（不只一个）
3. **原子化**：用 append_doc 而非重建整个笔记
4. **schema 强制**：frontmatter 必填字段（confidence/sources/version）
5. **人类策展**：用户决定收录什么，LLM 维护导览
