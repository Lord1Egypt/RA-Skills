---
name: knowledge-precipitation
version: 0.1.10
description: |
  每日知识沉淀引擎（Knowledge Auto-Precipitation Engine，KAPE）v0.1.10。自动完成：下载昨日Get笔记内容 → 结合对话记录 → 深度分析用户学习、感悟、工作状态 → 生成含主题关联图的日志简报 → 同步归档到 Get笔记（带标签）+ 飞书知识库 + 飞书文档。触发场景：「整理昨天的日志」「生成日报简报」「知识沉淀」「整理学习记录」「存档昨天的内容」。

## v0.1.10 更新说明
- **修复飞书知识库同步失败 Bug**：cron 报告成功但实际未同步到知识库「日志简报」节点
- **根因**：Step 5 飞书知识库操作没有明确指定 parent_node_token，导致节点创建到了错误位置（根目录或其他节点下）
- **修复**：在 Step 5② 飞书知识库部分明确写入正确的节点层级结构；必须先创建 wiki 节点（获得 doc_token），再写入文档内容

## v0.1.8 更新说明
- **修复星期几判断 Bug**：Agent 禁止凭推理判断日期对应的星期几，必须用 `date -jf "%Y-%m-%d" <日期> +%A` 命令验证。Bug 原因：Agent 用当前日期倒推"昨天是周几"时出错（2026-05-11 本是周一，推断成周日）
- 第一步增加强制要求：先输出 `目标日期：YYYY-MM-DD（周X）` 再开始生成内容

## v0.1.7 更新说明
- 新增强制完整输出规则：无论输入数据多少，哪怕只有1条笔记，也必须生成完整模板的所有区块（主题关联图、数据概览、核心主题、每条笔记的详细分析、张公子关注什么、可以改进什么、明日关注、关键词、今日洞察）。简报不是摘要，是完整的结构化记录。当某日数据较少时，每个主题下的「分析/联想」部分可以简短，但不得省略整个区块。

## v0.1.6 更新说明
- 新增内容过滤规则：排除科技新闻日报生成的内容（本地文件、飞书文档链接、相关新闻笔记均不纳入日志简报）

## v0.1.5 更新说明
- 新增主题关联图功能：帮助快速定位知识节点
- 日志简报结构优化：主题关联图位于数据概览之后、核心主题之前

## v0.1.4 更新说明
- 新增第零步：Get笔记授权检查与自动刷新（电脑重启后 CLI 认证状态丢失时自动修复）
- API Key 从配置文件读取后直接传给 CLI，不记录任何日志，防止隐私泄露

## v0.1.3 更新说明
- 修复 memory 文件路径格式问题（Markdown 链接语法导致 ENOENT）
- 添加容错机制：memory 文件不存在时跳过，不阻断流程
- 确保 Get笔记 API 始终被调用，不依赖 memory 文件状态
---

# KAPE — 知识自动沉淀引擎 v0.1.7

## 安全说明

本 skill 需要以下工具权限：
- `exec`：调用 getnote CLI 获取笔记数据（只读操作）
- `feishu_wiki`、`feishu_doc`：写入飞书文档
- `sessions_list`、`sessions_history`：读取对话记录

**不会执行任何本地文件写入之外的 shell 命令**，所有外部 API 调用均为只读请求。

**重要**：禁止直接调用 `https://openapi.biji.com/...` HTTPS API（会返回 `10004 未授权`），必须使用 `getnote` CLI。

## 凭证配置

Get笔记 API 凭证存储在 `openclaw.json` 中：
```json
{
  "skills": {
    "entries": {
      "getnote": {
        "apiKey": "<从配置文件读取，勿硬编码>",
        "env": {
          "GETNOTE_CLIENT_ID": "<从配置文件读取>"
        }
      }
    }
  }
}
```

飞书机器人需已加入知识库成员，否则 `feishu_wiki(spaces)` 返回空。

## 共享文件夹配置

飞书文档统一存放在共享文件夹「牛管家日志」，确保张公子有删除权限。

| 配置项 | 值 |
|--------|---|
| 文件夹名称 | 牛管家日志 |
| 文件夹 token | `FQfXfYBGGllxxydJ1SgcJZWqnpf` |
| 文件夹 URL | https://qcnu4qzh46f0.feishu.cn/drive/folder/FQfXfYBGGllxxydJ1SgcJZWqnpf |
| 张公子权限 | full_access（可删除文档） |

---

## 核心工作流

每天自动生成日志简报，三端同步归档。

### 第零步：Get笔记 授权检查与自动刷新

> ⚠️ **重要**：Get笔记 CLI 维护独立于 openclaw.json 的登录状态，电脑重启后可能被重置（显示 `Not authenticated`）。本步骤自动检测并修复，无需用户手动操作。

**操作流程：**
1. 先执行 `getnote auth status` 检查当前认证状态
2. 若返回 `Not authenticated`：
   - 从 `~/.openclaw/openclaw.json` 读取 `skills.entries.getnote.apiKey` 和 `skills.entries.getnote.env.GETNOTE_CLIENT_ID`
   - 执行 `getnote auth login --api-key "<apiKey>" --client-id "<clientId>"`（API Key 直接传给 CLI，不记录到任何日志）
   - 等待 `Logged in successfully.` 确认
3. 若已认证（`Authenticated`）：直接继续，不做任何操作

**注意**：API Key 从配置文件读取后直接作为命令行参数传给 `getnote auth login`，不写入任何日志文件或工作记忆，防止隐私泄露。

---

### 第一步：确定日期范围

- **目标日期**：昨天
- **获取方式**：
  1. 使用 `date` 命令获取当前日期：`date +%Y-%m-%d`
  2. 用 `date` 命令计算昨天的日期：`date -v-1d +%Y-%m-%d`
  3. 用 `date` 命令验证星期：`date -jf "%Y-%m-%d" "<目标日期>" +%A`
- **输出要求**：在生成简报前，先输出 `目标日期：YYYY-MM-DD（周X）`，并用 `date` 命令确认
- **日期格式**：`YYYY-MM-DD`（用于字符串前缀匹配）

### 第二步：获取数据（并行）

#### Get笔记读取

> ⚠️ **重要**：Get笔记 API 必须通过 `getnote` CLI 调用，**禁止**直接调用 `https://openapi.biji.com/...`（会返回 `10004 未授权`）。

**读取步骤：**

1. **设置 CLI 路径**（必须使用完整路径，因为 cron isolated session 的 PATH 不含 npm 全局 bin）：
   ```bash
   GETNOTE_CLI="/Users/openclawer/.npm-global/lib/node_modules/@getnote/cli/bin/getnote"
   ```

2. **检查认证状态**：
   ```bash
   ${GETNOTE_CLI} auth status
   ```
   - 若返回 `Not authenticated`：从 `~/.openclaw/openclaw.json` 读取 `skills.entries.getnote.apiKey` 和 `skills.entries.getnote.env.GETNOTE_CLIENT_ID`，然后执行 `getnote auth login --api-key "<apiKey>" --client-id "<clientId>"`
   - 若返回 `Authenticated`：直接继续

3. **读取笔记**（使用 CLI，**不要**直接调 HTTPS API）：
   ```bash
   # 读取最新笔记（自动分页），输出为 table 格式
   ${GETNOTE_CLI} notes --since-id 0 --limit 50
   
   # 读取指定知识库的笔记
   ${GETNOTE_CLI} kb eYzMmvnm --limit 20
   
   # 搜索笔记
   ${GETNOTE_CLI} search "<关键词>" --limit 10
   ```

4. **过滤目标日期**：CLI 输出为 table 格式，用 `grep` 过滤 `created` 列包含目标日期的行：
   ```bash
   ${GETNOTE_CLI} notes --since-id 0 --limit 200 2>/dev/null | \
     grep "^2026-05-13" | head -20
   ```

5. **获取单条笔记详情**：
   ```bash
   ${GETNOTE_CLI} note <note_id> --field content  # 获取正文
   ${GETNOTE_CLI} note <note_id> --field title   # 获取标题
   ```

> ⚠️ **API Key 凭证来源**：从 `~/.openclaw/openclaw.json` 的 `skills.entries.getnote.apiKey` 读取（不要硬编码）。API Key 从配置文件读取后直接作为命令行参数传给 CLI，不记录到任何日志。

### Get笔记数据读取方式（必须使用 CLI）

> ⚠️ **重要**：Get笔记 API 必须通过 `getnote` CLI 调用，不支持直接 HTTPS API 调用（直接调 `https://openapi.biji.com/...` 会返回 `10004 未授权`）。

**读取方式 A（推荐）**：用 CLI 的 `--since-id 0 --all` 拿到全部笔记，自动分页：
```bash
GETNOTE_CLI="${HOME}/.npm-global/lib/node_modules/@getnote/cli/bin/getnote"
${GETNOTE_CLI} notes --since-id 0 --all 2>/dev/null | grep -v "^ID\|^--\|^$" | awk -F'|' '{print $1,$2,$3,$4}' | while read id title type created; do
  # 过滤目标日期 created_at ~ target_date
done
```

**读取方式 B（直接 API，备用）**：如果 CLI 因 PATH 问题不可用，用 Python 读配置文件后通过 getnote CLI 保存：
```bash
# 不要直接调 openapi.biji.com（会10004未授权）
# 必须通过 getnote CLI
GETNOTE_CLI="${HOME}/.npm-global/lib/node_modules/@getnote/cli/bin/getnote"
${GETNOTE_CLI} notes --since-id 0 --limit 20  # 分页读取，每页20条，用 next_cursor 翻页
```

**修复 `getnote: command not found`**：如果执行报错 `command not found`，改用完整路径：
```bash
GETNOTE_CLI="/Users/openclawer/.npm-global/lib/node_modules/@getnote/cli/bin/getnote"
```

> ⚠️ **PATH 问题说明**：cron isolated session 的 PATH 不包含 `~/.npm-global/bin`，使用 `getnote` 命令会报 `command not found`。必须使用完整路径或确保 PATH 包含 npm 全局 bin 目录。

#### 对话记录获取

1. 用 `sessions_list` 获取所有 session（设置足够的 `activeMinutes` 覆盖目标日期）
2. 判断 session 在目标日期有活动的条件：`updatedAt` >= 目标日期开始时间 AND `updatedAt` < 今日开始时间
3. 用 `sessions_history` 读取符合条件的 session 内容（`includeTools=false`）
4. 解析用户消息（`role: user`）作为对话记录

#### 词汇存档（若有）

- **容错读取**：用 `exec` + `cat` 读取 `workspace/vocabulary/{target_date}.md`，若文件不存在或读取失败则跳过，不阻断流程
- 统计当日新增单词数量（如有）

> ⚠️ **路径处理规范**：所有从 `memory_search` 或 `sessions_list` 等工具返回的路径，返回格式可能为 Markdown 链接（如 `[2026-04-05.md](http://...`）或纯路径。传给 `read` 工具前，**必须先去除 Markdown 链接格式**，只提取纯路径部分（去掉 `[text](url)` 包装，保留 `text` 部分作为文件路径）。

### 第三步：深度分析与整理

> ⚠️ **内容过滤规则（v0.1.6 新增，必须执行）**
> 整理前需剔除【科技新闻日报】自动生成的内容，避免日志简报被机器人生成内容稀释：
> - **排除文件**：`memory/YYYY-MM-DD-tech-news.md`（科技新闻日报生成的本地新闻文件）
> - **排除文档**：飞书文档标题含「科技新闻日报」或「科技新闻热榜」的文档及其内容
> - **排除笔记**：Get笔记标签或来源为「科技新闻日报」相关条目
> - **仅保留**张公子个人学习、播客、录音、网页剪藏、手动笔记等主动获取内容

**用户行为分析**：
- 从 Get笔记的 `tags`、`title`、`source` 推断用户关注领域
- 从录音笔记数量和总时长推断学习深度
- 从内容关键词判断核心主题

**张公子画像维度**（供参考）：
| 维度 | 观察点 |
|------|--------|
| 学习风格 | 主动深度 vs 被动浏览 |
| 知识关联 | 是否跨领域建立联系 |
| 方法论倾向 | 重底层原理 vs 碎片技巧 |
| 时间感知 | 是否主动管理精力/时间 |
| 决策态度 | 务实程度、换方法频率 |

**生成日志简报结构**（见 references/briefing-template.md）

> ⚠️ **强制完整输出规则（v0.1.7 新增）**：无论输入数据多少，哪怕只有1条笔记，也必须生成完整模板的所有区块（主题关联图、数据概览、核心主题、每条笔记的详细分析、张公子关注什么、可以改进什么、明日关注、关键词、今日洞察）。简报不是摘要，是完整的结构化记录。当某日数据较少时，每个主题下的「分析/联想」部分可以简短，但不得省略整个区块。

**生成主题关联图（v0.1.5 新增）：**
根据当日笔记和对话记录，自动提取3-5个核心主题，标注主题间的关联关系，帮助快速定位知识节点。

**关联类型标签：**
- `→` 因果关系（A导致B）
- `⟶` 支撑关系（A证实/支持B）
- `⇄` 竞争关系（A与B竞争）
- `↙` 衍生关系（A衍生出B）

**生成规则：**
- 主题数量：3-5个为宜（太少则关联单薄，太多则失去焦点）
- 关系数量：每对主题间最多1条关系，优先标注最强关联
- 每条笔记/录音可归属1-2个主题
- 飞书文档中使用列表格式替代 ASCII 图形

### 第四步：写入本地文件

**必须先确保目录存在**：
```bash
mkdir -p /Users/openclawer/.openclaw/workspace/日志管理
```

**文件路径**：`/Users/openclawer/.openclaw/workspace/日志管理/{target_date}-日志简报.md`

### 第五步：三端同步归档

**① Get笔记**（**必须写入完整简报全文，不得简写**）：
```
POST https://openapi.biji.com/open/api/v1/resource/note/save
Headers:
  Authorization: {从配置文件读取}
  X-Client-ID: {从配置文件读取}
Body:
  title: "日志简报 {target_date} | {姓名}"
  content: 【必须写入完整简报全文】，包含所有章节、分析、统计数据，不得写入摘要或简短版本
  note_type: "plain_text"
  tags: ["AI整理", "日志简报"]
```

> ⚠️ **重要**：Get笔记的 `content` 字段必须包含日志简报的**完整正文**（与写入本地文件和飞书文档的内容完全一致），不得以"详见链接"为由缩减内容。

**② 飞书知识库**（必须同步，否则简报缺失）：

> ⚠️ **节点层级结构（v0.1.10 修复）**：
> - 个人知识库（space_id: `7621391289904516315`）
> - `日志简报` 节点（node_token: `SERDwHBAniUqqBkx5vNctvgKn6f`，obj_token: 对应文件夹下的日志简报）
> - **每日日志简报文档**（创建在此节点下）
>
> **执行顺序**：
> 1. 用 `lark-cli wiki +node-create --space-id 7621391289904516315 --parent-node-token SERDwHBAniUqqBkx5vNctvgKn6f --title "日志简报 {target_date} | 张公子"` 创建 wiki 节点
> 2. 获取返回的 `obj_token`（新文档的 doc token）
> 3. 用 `lark-cli docs +update --api-version v2 --doc <obj_token> --command overwrite --doc-format xml --content @<本地简报xml路径>` 写入内容
> 4. 用 `lark-cli wiki +move --node-token <新节点token> --target-parent-token SERDwHBAniUqqBkx5vNctvgKn6f --source-space-id 7621391289904516315 --target-space-id 7621391289904516315` 确保节点在正确位置（如创建到了错误位置）
> 5. 记录知识库 URL 到反馈消息

> ⚠️ **注意**：飞书知识库操作需要机器人已加入知识库成员。如果 `feishu_wiki(spaces)` 返回空，说明权限不足。

**③ 飞书文档**（主归档通道）：
0. 先获取 `tenant_access_token`：
   ```bash
   curl -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
     -H 'Content-Type: application/json' \
     -d '{"app_id":"cli_a94b4a1e43781cc7","app_secret":"{从 openclaw.json 读取 appSecret}"}'
   ```
1. 用 `exec` + `curl` 在共享文件夹中创建文档（需指定 `folder_token`）：
   ```bash
   curl -X POST 'https://open.feishu.cn/open-apis/docx/v1/documents' \
     -H 'Authorization: Bearer {tenant_access_token}' \
     -H 'Content-Type: application/json' \
     -d '{"title":"日志简报 {target_date} | 张公子","folder_token":"FQfXfYBGGllxxydJ1SgcJZWqnpf"}'
   ```
2. 用 `feishu_doc(action=write, doc_token=..., content=...)` 写入简报内容
3. 赋予张公子 `full_access` 权限（确保可删除）：
   ```bash
   curl -X POST 'https://open.feishu.cn/open-apis/drive/v1/permissions/{doc_token}/members?type=docx' \
     -H 'Authorization: Bearer {tenant_access_token}' \
     -H 'Content-Type: application/json' \
     -d '{"member_type":"openid","member_id":"ou_d8ace8a146610ca26bc07d8e68a5620f","perm":"full_access"}'
   ```
4. 将文档 URL 记录到反馈消息中

> ⚠️ **注意**：飞书知识库操作需要机器人已加入知识库成员。如果 `feishu_wiki(spaces)` 返回空，说明权限不足。

### 第六步：用户反馈

向用户发送完成通知，包含：
- 下载 Get笔记 数量（分类统计：录音/播客/纯文本等）
- 参考对话记录数量
- 简报核心发现摘要（1-3句话）
- 各端存储结果链接

---

## 错误处理原则

1. **任何一步失败不影响其他步骤**：三端归档是独立的，写入本地文件是最基本的保障
2. **明确告知用户失败原因**：如果某个平台失败，需要在反馈中说明
3. **不要静默失败**：如果关键步骤（如获取数据）失败，必须通知用户
