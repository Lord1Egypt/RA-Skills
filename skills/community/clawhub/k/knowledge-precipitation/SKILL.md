---
name: knowledge-precipitation
version: 0.1.18
description: |
  每日知识沉淀引擎（Knowledge Auto-Precipitation Engine，KAPE）v0.1.18。自动完成：下载昨日Get笔记内容 → 结合对话记录 → 深度分析用户学习、感悟、工作状态 → 生成含主题关联图的日志简报 → 同步归档到 Get笔记（带标签）+ 飞书知识库 + 飞书文档。触发场景：「整理昨天的日志」「生成日报简报」「知识沉淀」「整理学习记录」「存档昨天的内容」。

## v0.1.18 更新说明（2026-06-27 凭证修复）
- 同步版本号至 0.1.18，修正 skill_workshop 注册信息。

## v0.1.15 更新说明（2026-06-27 Bug 修复）
- **根因**：cron isolated session 不会自动注入 `GETNOTE_CLIENT_ID` 和 `GETNOTE_API_KEY` 环境变量，导致 `getnote auth login` 失败，提示"API未授权"。
- **修复**：新增「运行时凭证读取」章节，所有调用 Get笔记 CLI 的步骤均需先从配置文件（openclaw.json + secrets.json）读取凭证后再执行，彻底摆脱对环境变量的依赖。

## v0.1.14 更新说明（2026-06-06 Bug 修复）
- **根因**：cron 执行时使用了 `grep "^2026-06-05"`（行首匹配），但日期在最后一列（行首是笔记 ID），导致 7 条笔记全部漏读。v0.1.12/v0.1.13 均已警告此 Bug，但执行端仍违反。
- **SKILL.md 强化约束**：在命令示例中直接写出正确的 `grep` 命令，**禁止**使用行首锚 `^`。

## v0.1.13 更新说明
- **Get笔记日期过滤逻辑再次确认**：CLI 输出格式为 `ID | Title | Type | Created`，日期在**最后一列**，行首是笔记 ID（不是日期）。过滤必须用 `grep "${TARGET_DATE} "`（尾部空格避免部分匹配），严禁用 `grep "^${TARGET_DATE}"`（行首不是日期，永远匹配不到）
- **分页读取逻辑补全**：当笔记数量超过 limit（200条）时，用**最后一条笔记 ID** 作为下次 `since-id` 参数继续读取，循环直至 `has_more=false`，确保不漏读

## v0.1.12 更新说明
- **修复 Get笔记 日期过滤 Bug**：`grep "^2026-05-28"` 永远匹配不到（行首是笔记 ID，不是日期），应改为 `grep "2026-05-28 "`（日期在最后一列，尾部加空格避免部分匹配）
- 同时排查其他 skill：getnote/references/list.md 已补充 CLI 输出格式说明；tech-news-daily 和 sci-china-reviewer 均无需修改

## v0.1.11 更新说明
- **修复重复创建 Bug**：SKILL.md 描述的工作流与实际 CLI 命令不匹配，导致 Agent 摸索尝试产生冗余文档/笔记
- **根因**：
  - Get笔记 SKILL 写的是直接调 HTTPS API（会返回 10004 未授权），实际应使用 `getnote save` CLI
  - 飞书文档 SKILL 写了"先创建空文档 → 再写入内容"的两步流程，但写入失败重试时 Agent 又创建了新文档
- **修复**：统一使用 CLI 的原子操作（一次命令完成创建+写入），禁止分步创建空文档再写入

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

# KAPE — 知识自动沉淀引擎 v0.1.18

## 安全说明

本 skill 需要以下工具权限：
- `exec`：调用 getnote CLI 获取笔记数据（只读操作）
- `feishu_wiki`、`feishu_doc`：写入飞书文档
- `sessions_list`、`sessions_history`：读取对话记录

**不会执行任何本地文件写入之外的 shell 命令**，所有外部 API 调用均为只读请求。

**重要**：禁止直接调用 `https://openapi.biji.com/...` HTTPS API（会返回 `10004 未授权`），必须使用 `getnote` CLI。

## 凭证配置

Get笔记 API 凭证存储位置：
- `GETNOTE_CLIENT_ID` → `openclaw.json` 的 `skills.entries.getnote.env.GETNOTE_CLIENT_ID`
- `GETNOTE_API_KEY` → `secrets.json` 的 `skills.entries.getnote.apiKey`（SecretRef 解析后的实际值）

飞书 appSecret → `secrets.json` 的 `channels.feishu.accounts.main.appSecret`

> ⚠️ **核心约束**：cron isolated session **不会**自动注入环境变量 `GETNOTE_CLIENT_ID` 和 `GETNOTE_API_KEY`，所有调用 Get笔记 CLI 的 shell 命令前**必须**先从配置文件读取凭证（详见下方「运行时凭证读取」章节）。不读取凭证直接调用 CLI 会导致"API 未授权"错误。

飞书机器人需已加入知识库成员，否则 `feishu_wiki(spaces)` 返回空。

## 运行时凭证读取

> ⚠️ **所有调用 Get笔记 CLI 的步骤**（第零步、第一步、第三步等），**必须先执行以下凭证读取代码**，再执行 CLI 命令。isolated session 无环境变量注入，绝不能省略此步骤。

```bash
GETNOTE_CLI="/Users/openclawer/.npm-global/lib/node_modules/@getnote/cli/bin/getnote"

# 从配置文件读取凭证（isolated session 不会自动注入环境变量）
GETNOTE_CFG=$(python3 -c "
import json
with open('/Users/openclawer/.openclaw/openclaw.json') as f:
    oc = json.load(f)
with open('/Users/openclawer/.openclaw/secrets.json') as f:
    sec = json.load(f)

# GETNOTE_CLIENT_ID：从 openclaw.json 直接读取
client_id = oc.get('skills',{}).get('entries',{}).get('getnote',{}).get('env',{}).get('GETNOTE_CLIENT_ID','')

# GETNOTE_API_KEY：从 secrets.json 读取（SecretRef 解析）
apikey_ref = oc.get('skills',{}).get('entries',{}).get('getnote',{}).get('apiKey',{})
if isinstance(apikey_ref, dict) and apikey_ref.get('source') == 'file':
    key_path = apikey_ref.get('id','')
    apikey = sec
    for k in key_path.split('/'):
        if k:
            apikey = apikey.get(k, {})
    api_key = apikey if isinstance(apikey, str) else apikey.get('apiKey','')
else:
    api_key = str(apikey_ref)

print(f'{client_id}\n{api_key}')
")

GETNOTE_CLIENT_ID=$(echo "$GETNOTE_CFG" | sed -n '1p')
GETNOTE_API_KEY=$(echo "$GETNOTE_CFG" | sed -n '2p')

# 验证读取结果（不打印完整 key）
echo "CLIENT_ID: ${GETNOTE_CLIENT_ID:0:10}..."
echo "API_KEY: ${GETNOTE_API_KEY:0:10}..."
```

---

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

每天自动生成日志简报，三端同步归档。**每个平台每次只执行一次原子操作，不允许先创建空文档再单独写入。**

---

### 第零步：Get笔记 凭证读取与授权检查

> ⚠️ **重要**：必须先读取凭证，再检查/执行授权。isolated session 无环境变量注入，不读取凭证会导致"API 未授权"。

**第一步：读取凭证 + 检查认证状态**
```bash
GETNOTE_CLI="/Users/openclawer/.npm-global/lib/node_modules/@getnote/cli/bin/getnote"

# 读取凭证
GETNOTE_CFG=$(python3 -c "
import json
with open('/Users/openclawer/.openclaw/openclaw.json') as f:
    oc = json.load(f)
with open('/Users/openclawer/.openclaw/secrets.json') as f:
    sec = json.load(f)
client_id = oc.get('skills',{}).get('entries',{}).get('getnote',{}).get('env',{}).get('GETNOTE_CLIENT_ID','')
apikey_ref = oc.get('skills',{}).get('entries',{}).get('getnote',{}).get('apiKey',{})
if isinstance(apikey_ref, dict) and apikey_ref.get('source') == 'file':
    key_path = apikey_ref.get('id','')
    apikey = sec
    for k in key_path.split('/'):
        if k:
            apikey = apikey.get(k, {})
    api_key = apikey if isinstance(apikey, str) else apikey.get('apiKey','')
else:
    api_key = str(apikey_ref)
print(f'{client_id}\n{api_key}')
")
GETNOTE_CLIENT_ID=$(echo "$GETNOTE_CFG" | sed -n '1p')
GETNOTE_API_KEY=$(echo "$GETNOTE_CFG" | sed -n '2p')

# 检查认证状态
${GETNOTE_CLI} auth status
```

**第二步：根据认证状态决定操作**
- 若返回 `Not authenticated`：
  ```bash
  ${GETNOTE_CLI} auth login --api-key "${GETNOTE_API_KEY}" --client-id "${GETNOTE_CLIENT_ID}"
  ```
  等待 `Logged in successfully.` 确认后再继续。
- 若返回 `Authenticated`：直接继续，不做任何操作。

---

### 第一步：确定日期范围

- **目标日期**：昨天
- **获取方式**：
  1. 使用 `date` 命令获取当前日期：`date +%Y-%m-%d`
  2. 用 `date` 命令计算昨天的日期：`date -v-1d +%Y-%m-%d`
  3. 用 `date` 命令验证星期：`date -jf "%Y-%m-%d" "<目标日期>" +%A`
- **输出要求**：在生成简报前，先输出 `目标日期：YYYY-MM-DD（周X）`，并用 `date` 命令确认
- **日期格式**：`YYYY-MM-DD`（用于字符串前缀匹配）

---

### 第二步：获取数据（并行）

#### Get笔记读取

> ⚠️ **重要**：Get笔记 API 必须通过 `getnote` CLI 调用，**禁止**直接调用 `https://openapi.biji.com/...`（会返回 `10004 未授权`）。

**读取步骤：**

1. **设置 CLI 路径 + 读取凭证**（必须先读取凭证，因为 isolated session 无环境变量）：
   ```bash
   GETNOTE_CLI="/Users/openclawer/.npm-global/lib/node_modules/@getnote/cli/bin/getnote"

   # 读取凭证（isolated session 不会自动注入环境变量）
   GETNOTE_CFG=$(python3 -c "
   import json
   with open('/Users/openclawer/.openclaw/openclaw.json') as f:
       oc = json.load(f)
   with open('/Users/openclawer/.openclaw/secrets.json') as f:
       sec = json.load(f)
   client_id = oc.get('skills',{}).get('entries',{}).get('getnote',{}).get('env',{}).get('GETNOTE_CLIENT_ID','')
   apikey_ref = oc.get('skills',{}).get('entries',{}).get('getnote',{}).get('apiKey',{})
   if isinstance(apikey_ref, dict) and apikey_ref.get('source') == 'file':
       key_path = apikey_ref.get('id','')
       apikey = sec
       for k in key_path.split('/'):
           if k:
               apikey = apikey.get(k, {})
       api_key = apikey if isinstance(apikey, str) else apikey.get('apiKey','')
   else:
       api_key = str(apikey_ref)
   print(f'{client_id}\n{api_key}')
   ")
   GETNOTE_CLIENT_ID=$(echo "$GETNOTE_CFG" | sed -n '1p')
   GETNOTE_API_KEY=$(echo "$GETNOTE_CFG" | sed -n '2p')
   ```

2. **检查认证状态**（如未认证则登录）：
   ```bash
   ${GETNOTE_CLI} auth status
   ```
   - 若返回 `Not authenticated`：
     ```bash
     ${GETNOTE_CLI} auth login --api-key "${GETNOTE_API_KEY}" --client-id "${GETNOTE_CLIENT_ID}"
     ```
   - 若返回 `Authenticated`：直接继续

3. **读取并过滤目标日期笔记（必须完成全部分页读取）**：
   ```bash
   # ⚠️ CLI 输出格式：ID | Title | Type | Created（日期在最后一列，行首是笔记ID）
   # ⚠️ 正确写法：grep "2026-05-28 "（尾部空格），匹配最后一列的日期
   # ❌ 错误写法：grep "^2026-05-28" —— 日期不在行首，永远匹配不到，**严禁使用**
   TARGET_DATE="2026-05-28"  # 昨日日期，格式 YYYY-MM-DD
   ${GETNOTE_CLI} notes --since-id 0 --limit 200 2>/dev/null | grep "${TARGET_DATE} "
   ```


4. **分页读取（防止遗漏）**：当笔记数超过 200 条时，用最后一条笔记 ID 作为下次 `since-id` 继续读取，循环直至 `has_more=false`：
   ```bash
   # 第一页
   ${GETNOTE_CLI} notes --since-id 0 --limit 200 2>/dev/null | grep "${TARGET_DATE} "
   # 下一页：用上一步最后一条笔记 ID 替换 0
   ${GETNOTE_CLI} notes --since-id <last_note_id> --limit 200 2>/dev/null | grep "${TARGET_DATE} "
   # 循环继续直至 has_more=false
   ```

5. **获取单条笔记详情**：
   ```bash
   ${GETNOTE_CLI} note <note_id> --field content  # 获取正文
   ${GETNOTE_CLI} note <note_id> --field title   # 获取标题
   ```

#### 对话记录获取

1. 用 `sessions_list` 获取所有 session（设置足够的 `activeMinutes` 覆盖目标日期）
2. 判断 session 在目标日期有活动的条件：`updatedAt` >= 目标日期开始时间 AND `updatedAt` < 今日开始时间
3. 用 `sessions_history` 读取符合条件的 session 内容（`includeTools=false`）
4. 解析用户消息（`role: user`）作为对话记录

#### 词汇存档（若有）

- **容错读取**：用 `exec` + `cat` 读取 `workspace/vocabulary/{target_date}.md`，若文件不存在或读取失败则跳过，不阻断流程
- 统计当日新增单词数量（如有）

> ⚠️ **路径处理规范**：所有从 `memory_search` 或 `sessions_list` 等工具返回的路径，返回格式可能为 Markdown 链接（如 `[2026-04-05.md](http://...`）或纯路径。传给 `read` 工具前，**必须先去除 Markdown 链接格式**，只提取纯路径部分。

---

### 第三步：深度分析与整理

> ⚠️ **内容过滤规则（v0.1.6 新增，必须执行）**
> 整理前需剔除【科技新闻日报】自动生成的内容：
> - **排除文件**：`memory/YYYY-MM-DD-tech-news.md`
> - **排除文档**：飞书文档标题含「科技新闻日报」或「科技新闻热榜」
> - **排除笔记**：Get笔记标签或来源为「科技新闻日报」相关条目
> - **仅保留**张公子个人学习、播客、录音、网页剪藏、手动笔记等主动获取内容

**生成日志简报结构**（见 `references/briefing-template.md`）

> ⚠️ **强制完整输出规则（v0.1.7 新增）**：无论输入数据多少，哪怕只有1条笔记，也必须生成完整模板的所有区块。简报不是摘要，是完整的结构化记录。

**生成主题关联图（v0.1.5 新增）：**
根据当日笔记和对话记录，自动提取3-5个核心主题，标注主题间的关联关系。

**关联类型标签：**
- `→` 因果关系（A导致B）
- `⟶` 支撑关系（A证实/支持B）
- `⇄` 竞争关系（A与B竞争）
- `↙` 衍生关系（A衍生出B）

**飞书文档中使用列表格式替代 ASCII 图形。**

---

### 第四步：写入本地文件

**必须先确保目录存在**：
```bash
mkdir -p /Users/openclawer/.openclaw/workspace/日志管理
```

**文件路径**：`/Users/openclawer/.openclaw/workspace/日志管理/{target_date}-日志简报.md`

---

### 第五步：三端同步归档（一次性操作到位）

> ⚠️ **核心原则**：每个平台每次只执行一次原子操作。不允许先创建空文档/空笔记，再单独写入内容的分步操作。如果写入失败，**先删除已创建的半成品**，再重新执行完整的原子操作。

**CLI 路径常量**（所有 `lark-cli` 命令必须使用完整路径）：
```bash
LARK_CLI="/Users/openclawer/.npm-global/bin/lark-cli"
```

---

#### ① Get笔记（使用 `getnote save` 原子操作）

```bash
GETNOTE_CLI="/Users/openclawer/.npm-global/lib/node_modules/@getnote/cli/bin/getnote"

# 读取凭证（isolated session 不会自动注入环境变量）
GETNOTE_CFG=$(python3 -c "
import json
with open('/Users/openclawer/.openclaw/openclaw.json') as f:
    oc = json.load(f)
with open('/Users/openclawer/.openclaw/secrets.json') as f:
    sec = json.load(f)
client_id = oc.get('skills',{}).get('entries',{}).get('getnote',{}).get('env',{}).get('GETNOTE_CLIENT_ID','')
apikey_ref = oc.get('skills',{}).get('entries',{}).get('getnote',{}).get('apiKey',{})
if isinstance(apikey_ref, dict) and apikey_ref.get('source') == 'file':
    key_path = apikey_ref.get('id','')
    apikey = sec
    for k in key_path.split('/'):
        if k:
            apikey = apikey.get(k, {})
    api_key = apikey if isinstance(apikey, str) else apikey.get('apiKey','')
else:
    api_key = str(apikey_ref)
print(f'{client_id}\n{api_key}')
")
GETNOTE_CLIENT_ID=$(echo "$GETNOTE_CFG" | sed -n '1p')
GETNOTE_API_KEY=$(echo "$GETNOTE_CFG" | sed -n '2p')

# content 必须是完整简报正文，不允许简写
${GETNOTE_CLI} save "<完整简报正文>" \
  --title "日志简报 {target_date} | 张公子" \
  --tag AI整理 \
  --tag 日志简报
```

> ⚠️ **禁止**直接调用 `https://openapi.biji.com/...` HTTPS API，必须使用 `getnote save` CLI。

---

#### ② 飞书知识库（先创建节点 → 再写入内容，两步都是原子的）

> ⚠️ **节点层级结构**：
> - 个人知识库（space_id: `7621391289904516315`）
> - `日志简报` 节点（node_token: `SERDwHBAniUqqBkx5vNctvgKn6f`）
> - **每日日志简报文档**（创建在此节点下）

**步骤 1：创建 wiki 节点（原子操作）**
```bash
cd /Users/openclawer/.openclaw/workspace/日志管理
${LARK_CLI} wiki +node-create \
  --space-id 7621391289904516315 \
  --parent-node-token SERDwHBAniUqqBkx5vNctvgKn6f \
  --title "日志简报 {target_date} | 张公子"
```
- 从返回的 `obj_token` 提取新文档的 doc token
- 从返回的 `node_token` 提取新 wiki 节点 token

**步骤 2：写入简报内容（原子操作）**
```bash
${LARK_CLI} docs +update \
  --api-version v2 \
  --doc "<obj_token>" \
  --command overwrite \
  --doc-format xml \
  --content @./2026-05-25-日志简报.md
```
> ⚠️ `--doc-format xml` 必须明确指定（默认 xml）。
> ⚠️ **重要**：飞书文档 **不支持 Markdown 表格**（写入时表格内容会丢失）。如简报包含表格，**必须使用 `--doc-format xml` 并提供 XML 格式内容**，XML 表格结构为 `<table><thead><tr><th>...</th></tr></thead><tbody><tr><td>...</td></tr></tbody></table>`。

**步骤 3：记录知识库 URL**

---

#### ③ 飞书文档（创建+写入一次完成，再授权）

**步骤 1：获取 tenant_access_token**
```bash
python3 -c "
import json, urllib.request
with open('/Users/openclawer/.openclaw/openclaw.json') as f:
    d = json.load(f)
# appSecret 从 secrets.json 读取
with open('/Users/openclawer/.openclaw/secrets.json') as f:
    sec = json.load(f)
app_secret = sec.get('channels',{}).get('feishu',{}).get('accounts',{}).get('main',{}).get('appSecret','')
req = urllib.request.Request(
    'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
    data=json.dumps({'app_id':'cli_a94b4a1e43781cc7','app_secret':app_secret}).encode(),
    headers={'Content-Type':'application/json'}
)
resp = urllib.request.urlopen(req, timeout=10)
print(resp.read().decode())
"
```

**步骤 2：创建文档并写入内容（原子操作）**
```bash
cd /Users/openclawer/.openclaw/workspace/日志管理
${LARK_CLI} docs +create \
  --api-version v2 \
  --parent-token FQfXfYBGGllxxydJ1SgcJZWqnpf \
  --doc-format xml \
  --content @./2026-05-25-日志简报.md
```
> ⚠️ **禁止先创建空文档再单独写入**。必须在 `--content` 中直接提供完整内容。
> ⚠️ **重要**：飞书文档 **不支持 Markdown 表格**，如简报包含表格，必须改用 `--doc-format xml` 并提供 XML 格式内容。

**步骤 3：提取 document_id（从返回的 `document.document_id`）**

**步骤 4：授予张公子 full_access 权限**
```bash
curl -X POST 'https://open.feishu.cn/open-apis/drive/v1/permissions/<document_id>/members?type=docx' \
  -H 'Authorization: Bearer {tenant_access_token}' \
  -H 'Content-Type: application/json' \
  -d '{"member_type":"openid","member_id":"ou_d8ace8a146610ca26bc07d8e68a5620f","perm":"full_access"}'
```

**步骤 5：记录文档 URL**

---

### 第六步：用户反馈

向用户发送完成通知，包含：
- Get笔记数量（分类统计：录音/播客/纯文本等）
- 参考对话记录数量
- 简报核心发现摘要（1-3句话）
- 各端存储结果链接

---

## 错误处理原则

1. **任何一步失败不影响其他步骤**：三端归档是独立的，写入本地文件是最基本的保障
2. **明确告知用户失败原因**：如果某个平台失败，需要在反馈中说明
3. **不要静默失败**：如果关键步骤（如获取数据）失败，必须通知用户
4. **写入前先查重**：写入前先检查目标日期是否已有同名笔记/文档，若有则先删除再创建