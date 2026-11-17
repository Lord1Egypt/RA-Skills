# 安全准则

> 任何破坏性操作前必读。任何不可逆操作必须先备份 + 用户确认 + 操作日志。
>
> ⚠️ **2026-09 重要更新**：IMA 平台当前 API **不支持**笔记、文件夹、文件的删除操作（仅支持标签删除）。详见第 3 节。

## 1. 破坏性操作清单

| 操作 | API | 风险 | 保护级别 |
|------|-----|------|:--------:|
| ~~删除笔记~~ | ~~`delete_note`~~ | ❌ **API 不支持** | — |
| 删除标签 | `tag_delete` | 所有关联自动解除 | 🔴 高 |
| 重命名标签 | `tag_rename` | 新名重复会**自动合并** | 🔴 高 |
| 移动文件 | `move_knowledge` | 标签数组可能清空 | 🟡 中 |
| ~~删除文件夹~~ | — | ❌ **API 不支持** | — |
| ~~删除文件~~ | — | ❌ **API 不支持** | — |

**IMA 平台删除能力边界（2026-09 现状）**：
- ✅ 可删除：标签（`tag_delete`）
- ❌ 不可删除：笔记、知识库、文件夹、文件、媒体
- 不可删除对象的处理方式：用户需在 **IMA 客户端手动删除**

## 2. 通用保护原则

1. **备份优先**：所有破坏性操作前必须先备份到本地
2. **三重确认门**：备份完成 + 内容已验证 + 用户显式确认
3. **操作日志**：每次破坏性操作后必须记录到 `/sandbox/workspace/logs/note_operations.log`
4. **优先用可逆方案**：`tag_remove` 优于 `tag_delete`，创建新笔记优于删除旧笔记
5. **影响范围可见**：执行前必须告诉用户"将影响 X 个文件/标签"
6. **IMA 限制认知**：删除笔记/文件夹/文件只能让用户在客户端操作，不要尝试构造或寻找删除 API

## 3. 删除笔记 — v1.1.x 策略：不删除

> ⚠️ **IMA 平台当前 API 不支持删除任何内容**。
> 这是 IMA 设计哲学的一部分（防止误删），不是 ima-wiki 的限制。

### 3.1 v1.1.x 策略

| 操作 | IMA 支持 | ima-wiki 应对 |
|------|:--------:|-------------|
| 删除笔记 | ❌ | **不删除**，让用户在 IMA 客户端手动操作 |
| 删除文件夹 | ❌ | **不删除** |
| 删除文件 | ❌ | **不删除** |
| 删除标签 | ✅ | 可用 `tag_delete`（参考 [tagging.md](tagging.md)）|

### 3.2 替代"删除"的工作流

**核心理念**：
- v1.0.x 时代：试图"创建新笔记替代旧笔记"（已废弃）
- **v1.1.0+**：用 Cascade + append_doc 原地更新，**永远不删除任何东西**
- 用户想"恢复旧版"：在 IMA 客户端查看笔记历史版本

### 3.3 严禁操作

❌ 不要尝试：
- 调用已失效的 `delete_note` API
- 构造或寻找"伪删除"接口
- 通过 `push_note` + `content_cos_key` 覆盖试图"擦除"内容
- 重试 `delete_note`（浪费时间）

✅ 应当做：
- 明确告知用户 IMA 平台的 API 边界
- 推荐用户在 IMA 客户端查看历史版本
- 指引客户端手动删除路径

> **删除能力的边界**：详见 [references/security.md 第 7 节](security.md) - IMA 平台已知限制

### 3.2 客户端手动删除流程

如需删除旧笔记，按以下流程告知用户：

**步骤 1：告知用户**
- 笔记标题：XXX
- 笔记 ID：XXX
- 删除位置：XXX（哪个笔记本）

**步骤 2：用户确认**
- 用户明确回复"确认删除"

**步骤 3：指引用户在 IMA 客户端操作**
- 打开 IMA 客户端 → 进入对应笔记本
- 找到目标笔记 → 右键 → 删除
- 或者：笔记右上角 ⋯ → 删除

**步骤 4：验证删除结果**
- 用 `list_note`（单数）API 确认笔记不在列表中

### 3.3 严禁操作

❌ **不要尝试**：
- 调用已失效的 `delete_note` API（即使文档还有说明）
- 构造或寻找其他"伪删除"接口
- 通过 `push_note` + `content_cos_key` 覆盖试图"擦除"内容
- 重试 `delete_note`（浪费时间）

✅ **应当做**：
- 明确告知用户 IMA 平台的 API 边界
- 推荐"创建新笔记替代"方案
- 指引客户端手动删除路径

## 4. 删除标签（`tag_delete`）保护

> ⚠️ 删除后所有关联自动解除，不可恢复。

调用前必须：
1. 用 `tag_list(keyword=新名)` 检查新名是否存在
2. 用 `get_knowledge_list(tags=[标签])` 列出受影响文件数
3. 告知用户所有关联自动解除且不可恢复
4. **用户显式确认**

```bash
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/tag_delete" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"knowledge_base_id": "<kb_id>", "tag_name": "<标签名>"}'
```

## 5. 重命名标签（`tag_rename`）保护

> ⚠️ 新名重复会**自动合并**到旧名——所有文件可能被打上意外标签。

调用前必须：
1. 用 `tag_list(keyword=新名)` 检查新名是否存在
2. 若存在，告知用户会"自动合并"并显式确认
3. 用 `get_knowledge_list` 列出受影响文件数
4. **用户显式确认**

```bash
curl -s -X POST "https://ima.qq.com/openapi/wiki/v1/tag_rename" \
  -H "ima-openapi-clientid: $IMA_OPENAPI_CLIENTID" \
  -H "ima-openapi-apikey: $IMA_OPENAPI_APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"knowledge_base_id": "<kb_id>", "old_tag_name": "<旧名>", "new_tag_name": "<新名>"}'
```

## 6. 移动文件（`move_knowledge`）保护

详见 [folder-organization.md](folder-organization.md) 第 0.4 节。

关键保护：
- 移动前**必须备份标签**（`move` 会清空标签数组）
- 移动后**逐个重新打标**

## 7. 操作日志

所有破坏性操作后必须记录：

```bash
# 追加到操作日志
echo "$(date -Iseconds) | <操作类型>: <note_id 或 tag_name> | 标题: <标题> | 备份路径: <路径>" \
  >> /sandbox/workspace/logs/note_operations.log
```

**日志格式**：

```
时间戳 | 操作 | ID | 标题 | 备份路径
```

**目的**：建立可审计的操作记录，万一误删可追溯。

## 8. 删除能力演进追踪

IMA 平台删除能力可能随版本变化，使用前建议：

1. 用 `npx clawhub inspect ima-knowledge` 或类似官方 skill 看最新规则
2. 检查 ima-knowledge SKILL.md 的"规则"部分是否有变更
3. 测试 API 是否已恢复支持

已知能力矩阵（2026-09-28 现状）：

| 操作 | 2026-05 试跑 | 2026-09 现状 |
|------|:------------:|:------------:|
| 删除标签 | ✅ 可用 | ✅ 可用 |
| 删除笔记 | ✅ 可用 | ❌ 不可用 |
| 删除文件夹 | ❌ 不可用 | ❌ 不可用 |
| 删除文件 | ❌ 不可用 | ❌ 不可用 |
| 删除知识库 | ❌ 不可用 | ❌ 不可用 |

> 💡 即使历史试跑中 `delete_note` 可用，**当前已不可用**。务必按 2026-09 现状执行。

## 8. 网络调用白名单（v1.1.2 新增）

### 8.1 允许的 URL 模式

| 域名 | 用途 | 数据类型 |
|------|------|---------|
| `https://ima.qq.com/openapi/wiki/v1/*` | IMA 知识库 API | 结构化 JSON |
| `https://ima.qq.com/openapi/note/v1/*` | IMA 笔记 API | 结构化 JSON |
| `https://ima.qq.com/openapi/*` 返回的 `content_url` | COS 链接 | COS URL（指向腾讯云） |
| `https://ima.qq.com/agent-interface` | IMA 配置文档 | URL（不下载） |
| `https://github.com/cookfish/ima-wiki` | 仓库地址 | URL（不下载） |

### 8.2 显式禁止项

ima-wiki **绝不做**：

- ❌ 下载并执行远程脚本
- ❌ 调用 `eval()` / `exec()` / `subprocess` / `os.system()` / `popen()`
- ❌ 运行 `npm install` / `pip install` 等包管理命令
- ❌ 访问非 `ima.qq.com` 域名的第三方 URL
- ❌ 下载 npm 包 / Python wheel / 二进制可执行文件
- ❌ 执行从 IMA 下载的任何内容

### 8.3 数据流

```
腾讯 IMA 平台
  ↓
  API 返回结构化 JSON（仅元数据，无代码）
  ↓
ima-wiki skill
  ↓ 解析为 Markdown 文本
  ↓ 作为 LLM 输入或生成导览内容
  ↓
[无中间文件，直接通过 IMA API 写入]
```

### 8.4 凭证管理

- `IMA_OPENAPI_CLIENTID` 和 `IMA_OPENAPI_APIKEY` 由用户配置
- 不在 ima-wiki 中硬编码
- 不传输到任何第三方
- 仅用于腾讯 IMA API 调用

### 8.5 风险审计表

| skill specter 警告 | ima-wiki 实际行为 | 风险等级 |
|-------------------|-----------------|:--------:|
| 下载并执行远程代码 | ❌ 不下载任何代码 | ✅ 无风险 |
| 绕过代码审查 | ❌ 不执行任何下载内容 | ✅ 无风险 |
| 引入恶意代码 | ❌ 仅解析结构化 JSON 和 Markdown | ✅ 无风险 |

### 8.6 安全审查方法

用户安装 ima-wiki 后，可以这样验证：

```bash
# 1. 检查 ima-wiki 实际下载的 URL
grep -roE "https?://[a-zA-Z0-9./_-]+" /sandbox/workspace/skills/ima-wiki/

# 2. 检查是否有动态代码执行
grep -rE "eval|exec|subprocess|os\.system|shell|popen" /sandbox/workspace/skills/ima-wiki/

# 3. 检查是否有包安装
grep -rE "npm install|pip install|brew install|apt install" /sandbox/workspace/skills/ima-wiki/

# 预期结果：
# (1) 全部 URL 都是 ima.qq.com 或 github.com/cookfish/ima-wiki
# (2) 无任何输出
# (3) 无任何输出
```
