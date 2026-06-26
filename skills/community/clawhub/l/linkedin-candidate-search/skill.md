# /linkedin-search — LinkedIn 候选人搜索

根据用户的搜索要求，使用 Chrome DevTools MCP 自动搜索 LinkedIn 候选人，保存档案到 `./linkedin-save/{role}/` 目录，防止重复扫描。

---

## 参数分层

用户的自然语言查询条件必须明确分为两层，**在 PRE-CHECK 通过后、开始搜索前完成拆解**：

### 第一层：搜索参数（硬嵌入搜索 query）

这两类条件直接决定 Google/LinkedIn 的搜索字符串，**不满足则无法检索**：

| 参数 | 说明 | 示例 |
|------|------|------|
| **职位关键词** | 必须出现在 query 中 | `presales solution architect` |
| **地点** | 城市或国家，必须出现在 query 中 | `hanoi` / `vietnam` |

构建搜索 query 时直接拼入：
```
site:linkedin.com/in/ ("presales" OR "pre-sales") "cloud" "hanoi"
```

### 第二层：LLM 分析参数（获取 profile 内容后由 LLM 推断）

这类条件**无法在搜索阶段过滤**，必须等拿到 profile 文本后，由 LLM 阅读并推断：

| 参数 | 硬/软 | 推断方式 |
|------|--------|----------|
| 云经验年限（≥5年） | **硬性** | 累加各段 cloud 相关工作经历时长 |
| 总工作经验（≤15年） | **硬性** | 推算首份工作起始年份 → 至今年数 |
| 售前经历明确 | **硬性** | 职位名含 presales/pre-sales/solution consultant 或 bio 有描述 |
| 公有云经验 | 软性 | 工作经历提及 AWS/Azure/GCP/OCI/VNG/Viettel Cloud 等 |
| 私有云经验 | 软性 | 工作经历提及 OpenStack/VMware/私有化部署/on-premise cloud |

**LLM 推断规则：**
- 时长不足以判断时，标注 `unknown`，match_level 降为 B 或 C
- 所有硬性条件均满足 → A；部分满足或有一项 unknown → B；仅 URL，内容极少 → C

---

## 运行时环境要求

执行本 skill 前，必须满足以下所有条件。**在正式开始搜索前，依次完成 PRE-CHECK 检查；任一条件不满足时，立即输出修复提示并停止执行。**

### 条件一：Chrome 调试会话已启动

Chrome 必须以远程调试模式运行在 **端口 9222**，且使用带有 LinkedIn 登录态的用户配置文件。

**验证方法：** 调用 `mcp__chrome-devtools__list_pages`，若返回页面列表则通过。

**不满足时的提示：**
```
❌ Chrome 调试会话未就绪

请在终端执行以下步骤：

1. 关闭当前所有 Chrome 窗口（或强制退出）：
   pkill -9 -f "Google Chrome"

2. 复制登录态配置文件（首次使用时执行）：
   mkdir -p /tmp/chrome_debug_profile
   cp -r ~/Library/Application\ Support/Google/Chrome/Default/{Cookies,"Login Data","Web Data",Preferences,"Local State"} \
     /tmp/chrome_debug_profile/ 2>/dev/null

3. 以调试模式启动 Chrome：
   nohup "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
     --remote-debugging-port=9222 \
     --user-data-dir="/tmp/chrome_debug_profile" \
     --no-first-run --disable-sync \
     > /tmp/chrome_debug.log 2>&1 &

4. 等待 3 秒后重新执行 /linkedin-search
```

### 条件二：LinkedIn 已登录

浏览器中必须有已登录 LinkedIn 的会话（用于访问个人档案和内部搜索）。

**验证方法：** 导航至 `https://www.linkedin.com/feed/`，执行脚本检查：
```javascript
() => document.querySelector('.global-nav__me-photo') !== null ||
      document.querySelector('[data-control-name="nav.homepage"]') !== null ||
      !document.URL.includes('/login')
```
返回 `true` 则通过。

**不满足时的提示：**
```
❌ LinkedIn 未登录

请在 Chrome 浏览器中手动登录 LinkedIn：
1. 在已打开的 Chrome 窗口中访问 https://www.linkedin.com
2. 完成登录（账号/密码或验证码）
3. 确认进入 LinkedIn 主页 feed 后，重新执行 /linkedin-search
```

### 条件三：linkedin-save 目录存在

`./linkedin-save/` 目录必须存在于当前工作目录下。

**验证方法：**
```bash
ls ./linkedin-save/ 2>/dev/null || echo "MISSING"
```

**不满足时的提示：**
```
❌ linkedin-save 目录不存在

正在自动创建...（执行 mkdir -p ./linkedin-save）
```
> 此条件由 skill 自动修复，无需用户干预。

### 条件四：当前工作目录正确

Skill 在 `/Users/junye/project/test-case/linkedin-zp` 下执行，档案相对路径才正确。

**验证方法：**
```bash
pwd
```

**不满足时的提示：**
```
❌ 当前工作目录不匹配

当前目录：{实际pwd结果}
期望目录：/Users/junye/project/test-case/linkedin-zp

请在正确目录下重新打开会话，或确认 linkedin-save 目录的实际位置。
```

---

## PRE-CHECK 执行顺序

```
[1] 检查 Chrome 调试会话     → 失败则输出提示，停止
[2] 检查 LinkedIn 登录态     → 失败则输出提示，停止
[3] 检查/创建 linkedin-save  → 自动修复
[4] 检查当前工作目录         → 不匹配则警告（不强制停止）
[5] 拆解用户查询 → 分层输出第一层/第二层参数
[6] 读取已扫描 URL 集合      → 正常继续
✅ 全部通过 → 开始搜索
```

**[5] 拆解输出示例：**
```
🔍 搜索参数拆解结果：

【第一层 — 搜索 Query（硬嵌入）】
  职位关键词：presales solution architect / pre-sales / solution consultant
  地点：hanoi, vietnam

【第二层 — LLM 分析条件（profile 获取后推断）】
  硬性：云经验 ≥ 5年 / 总经验 ≤ 15年 / 售前明确
  软性：公有云经验优先 / 私有云经验加分

目标候选人数：20人
保存目录：./linkedin-save/presales-architect/
```

---

## 执行步骤

> 执行前必须完成上方 **PRE-CHECK**（含参数分层），全部通过后再执行以下步骤。

### STEP 0 — 确定保存目录，读取已扫描 URL（防重复）

根据职位关键词确定子目录：

| 职位类型 | 目录 |
|----------|------|
| 售前架构师 / Presales Architect | `./linkedin-save/presales-architect/` |
| 解决方案架构师 / Solution Architect | `./linkedin-save/solution-architect/` |
| 云销售 / Cloud Sales | `./linkedin-save/cloud-sales/` |
| 其他 | `./linkedin-save/general/` |

读取已扫描 URL（用于后续去重跳过）：
```bash
grep -h "^url:" ./linkedin-save/{role_dir}/*.md 2>/dev/null | awk '{print $2}'
```

### STEP 1 — 搜索候选人 URL（Google → LinkedIn 内部）

使用**第一层参数**（职位关键词 + 地点）直接构建搜索 query。

**优先：Google site 搜索**

搜索策略依次尝试（将 {职位} 和 {地点} 替换为实际第一层参数）：
```
# A: 精确职位
site:linkedin.com/in/ ("presales" OR "pre-sales") "cloud" "{地点}"

# B: 扩展职位变体
site:linkedin.com/in/ "solution architect" "cloud" "presales" "{地点}"

# C: 按目标公司
site:linkedin.com/in/ ("presales" OR "solution architect") "cloud" ("FPT" OR "Viettel" OR "VNPT" OR "CMC" OR "AWS" OR "Oracle") "{地点}"
```

翻页：URL 加 `&start=10`、`&start=20`。

**提取 Google 结果 JS：**
```javascript
() => {
  const out = [];
  document.querySelectorAll('h3').forEach(h3 => {
    const block = h3.closest('.g') || h3.closest('[data-hveid]') || h3.closest('[jscontroller]');
    const a = block && block.querySelector('a[href*="linkedin.com/in/"]');
    if (a) out.push({
      url: a.href.split('?')[0].replace(/^https?:\/\/[a-z]+\.linkedin\.com/, 'https://www.linkedin.com'),
      title: h3.innerText,
      snippet: block ? block.innerText.slice(0, 300) : ''
    });
  });
  return out;
}
```

**备用：LinkedIn 内部搜索**（当 Google 结果不足时）

将第一层参数拼入 URL（`{keywords}` = 职位关键词，`{geoUrn}` = 地点对应 ID）：
```
https://www.linkedin.com/search/results/people/?keywords={keywords}&geoUrn=%5B%22{geoUrn}%22%5D&origin=FACETED_SEARCH&page=N
```

常用 geoUrn：
- 越南 Vietnam：`104195383`
- 河内 Hanoi：`104195383`（越南范围，无单城市 ID）
- 胡志明市 HCM：`104195383`

**提取 LinkedIn 搜索结果 JS：**
```javascript
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  for (let y = 0; y <= 5000; y += 300) { window.scrollTo(0, y); await sleep(150); }
  await sleep(2000);
  return Array.from(document.querySelectorAll('a[href*="/in/"]'))
    .map(a => ({ href: a.href.split('?')[0], text: a.innerText.trim().slice(0, 200) }))
    .filter(l => /linkedin\.com\/in\/[^/]+\/?$/.test(l.href) && l.text.length > 3)
    .filter((v, i, a) => a.findIndex(x => x.href === v.href) === i);
}
```

### STEP 2 — 逐一访问档案（跳过已扫描），LLM 分析第二层条件

对每个新 URL：

1. `navigate_page`（允许超时，继续执行）
2. 执行滚动+提取脚本获取原始文本：

```javascript
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  for (let y = 0; y <= 8000; y += 300) { window.scrollTo(0, y); await sleep(200); }
  await sleep(2000);
  const t = document.body.innerText;
  const ei = t.indexOf('工作经历');
  return {
    header: t.slice(0, 2500),
    exp: ei > -1 ? t.slice(ei, Math.min(ei + 4000, t.length)) : '',
    url: location.href.split('?')[0]
  };
}
```

3. **LLM 分析第二层条件**（根据 header + exp 文本推断）：

```
分析目标（逐项推断，无法判断则填 unknown）：
- cloud_years：累加含 AWS/Azure/GCP/OCI/云 字样的工作段时长
- total_years：推算最早工作年份 → 至今
- presales：职位名或 bio 是否含 presales/pre-sales/solution consultant/售前
- public_cloud：是否有 AWS/Azure/GCP/OCI/公有云 经历
- private_cloud：是否有 OpenStack/VMware/私有化/on-premise 经历
- match_level：
    A = 地点✅ + cloud_years≥目标 + total_years≤上限 + presales✅
    B = 上述条件部分可验证 / 有一项 unknown
    C = 仅 URL 或内容极少，需人工核实
```

4. **立即保存档案** → STEP 3

### STEP 3 — 保存档案（URL 必存，内容尽力）

文件路径：`./linkedin-save/{role_dir}/{linkedin_id}.md`  
其中 `linkedin_id` = URL 最后一段，例如 `nguyen-the-hung-70725b1b`

**档案格式（最小化版，仅 URL 时）：**
```markdown
---
name: unknown
url: {完整LinkedIn URL}
location: unknown
current_role: unknown
cloud_years: unknown
total_years: unknown
public_cloud: unknown
private_cloud: unknown
presales: unknown
match_level: C
scanned_date: {YYYY-MM-DD}
---
```

**档案格式（有内容时，LLM 推断填充）：**
```markdown
---
name: Nguyen The Hung
url: https://www.linkedin.com/in/nguyen-the-hung-70725b1b/
location: Hanoi, Vietnam
current_role: Customer Solution Consultant – GCP @ Google
cloud_years: 8
total_years: 15
public_cloud: true
private_cloud: true
presales: true
match_level: A
scanned_date: 2026-04-28
---

## 摘要
{LLM 对第二层条件的2-3句评估说明}

## 工作经历
{从页面提取的工作经历文本}
```

### STEP 4 — 循环直到达标

统计 match_level 为 A 或 B 的档案数量：
```bash
grep -l "match_level: [AB]" ./linkedin-save/{role_dir}/*.md 2>/dev/null | wc -l
```

未达目标则切换搜索词继续（仍只改**第一层参数**变体，第二层条件不变）：
- 职位变体：`"technical presales"` / `"pre-sales engineer"` / `"solution consultant"`
- 地点不变，但可加公司名替换地点做补充：`FPT` / `Viettel` / `CMC` / `VNPT` / `Noventiq`

---

## 输出汇总

完成后输出：

```
## 候选人汇总 — {职位}，{地点}

【搜索条件】职位: presales solution architect | 地点: hanoi
【分析条件】云经验≥5年 | 总经验≤15年 | 售前明确 | 公有云优先

| # | 姓名 | 职位@公司 | 云年限 | 总年限 | 公有云 | 私有云 | 售前 | 级别 | 链接 |
|---|------|-----------|--------|--------|--------|--------|------|------|------|
| 1 | Nguyen The Hung | GCP Consultant @ Google | 8yr | 15yr | ✅ | ✅ | ✅ | A | [🔗](url) |
...

A级: N人 | B级: N人 | C级: N人（待核实）
已保存至 ./linkedin-save/presales-architect/（共 N 个档案）
```

---

## 注意事项

- **URL 必存**：哪怕页面完全空白，也要保存含 URL 的最小档案
- **3度墙**：3度好友工作经历节不可见，LLM 仅凭 header/bio 推断，标记 C 级，`exp` 字段留空
- **导航超时**：超时后继续执行滚动脚本（页面可能已部分加载）
- **重复检测**：每次保存前 grep 检查 URL 是否已存在，跳过已扫描
- **速率**：每个档案访问后自然等待（滚动脚本本身约需4秒）
- **第一层不可协商**：地点和职位关键词必须进 query，不能只靠 LLM 事后过滤
