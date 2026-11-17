# OppHub 阶段 2 修订版 v4：录入确认 + 解析字段 + 知识库分组展示

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** skill 录入走"用户确认"流程(覆盖 4 种 entryType), 同时输出结构化字段; web `/knowledge` 按 opcId 分组, 每组只显示现行版.

**Architecture:** skill 端新增 confirmation state machine (输出 confirm 卡片 → 收 yes/no/modify → submit), cards 跟 parsedFields 一起入库. web 端 `/knowledge` 用 opcId 分组, 现行版 (supersededAt IS NULL) 渲染, 历史版只能从"📜 历史"按钮看. web 端顶部加录入引导.

**Tech Stack:** openclaw skill (录入主路), opphub-web (展示 + 引导)

---

## 0. 关键边界 (钉死)

- **录入主路**: openclaw skill, IM 端
- **web 不写**: 不建表单
- **匹配 / 推送**: 不动, 那是 server worker + opphub-ws 的事
- **enum 强制**: 不做
- **rawText 强结构校验**: 不做, 但加版本头

---

## 1. 任务地图 (6 个)

```
Task 1: skill rawText 顶部加 <!-- opphub-raw-text-v1 --> 头 (3 个 bin)
Task 2: skill 端 card 同时输出 parsedFields 结构化字段
Task 3: skill 端 confirm 状态机 - 4 种 entryType 全部列清单, 用户确认后入库
Task 4: web /knowledge 按 opcId 分组, 每组只显示现行版
Task 5: web /knowledge 顶部"如何录入"文字引导
Task 6: 部署 ECS + 终验
```

---

## Task 1: skill 端 rawText 加 `<!-- opphub-raw-text-v1 -->` 头

**Files:**
- Modify: `opphub-skill/bin/opphub-knowledge-card.js`
- Modify: `opphub-skill/bin/opphub-knowledge-discover.js`
- Modify: `opphub-skill/bin/opphub-knowledge-submit.js`

- [ ] **Step 1: knowledge-discover.js passthrough 时加版本头**

文件 `opphub-skill/bin/opphub-knowledge-discover.js`, 找到:

```js
      rawText: args.rawText,
```

修改为:

```js
      rawText: ensureVersionHeader(args.rawText),
```

并在文件顶部 (import 之后) 添加工具函数:

```js
// v4.0.9: rawText 顶部加版本头, 让 server 端能识别协议版本
//   v1 (当前): 自由文本, 不锁结构, 内容是 LLM 自由拼出来的 rawText
//   v2 (未来): 加结构化字段 (parseKeyFields 强校验)
function ensureVersionHeader(rawText) {
  if (!rawText) return rawText;
  if (rawText.startsWith("<!-- opphub-raw-text-v1 -->")) return rawText;
  return `<!-- opphub-raw-text-v1 -->\n${rawText}`;
}
```

- [ ] **Step 2: knowledge-discover.js skeleton 也加版本头**

找到 `buildRawTextSkeleton` 函数, 修改 return:

```js
function buildRawTextSkeleton(name) {
  const skeleton = `# ${name} · 自动画像 (skill turn 阶段 1 拼骨架)\n\n` +
    SOURCE_SKELETON.map((s, i) => `## ${i + 1}. ${s.name}\n(${s.purpose})\n\n`).join("");
  return `<!-- opphub-raw-text-v1 -->\n${skeleton}`;
}
```

- [ ] **Step 3: knowledge-card.js card.text 加版本头**

文件 `opphub-skill/bin/opphub-knowledge-card.js`, 找到所有 `text: \`${name} · ...` 字段 (ability / upstream / downstream 三段), 在前面加 `<!-- opphub-raw-text-v1 -->\n`:

(改 3 处, 示意 ability 一处)

```js
// 改前:
text: `${name} · 能力卡片 · ${dimension}\n\n(证据: rawText 包含 "${dimension}")\n\n(来自 rawText 实查, 非模板填空)`,

// 改后:
text: `<!-- opphub-raw-text-v1 -->\n${name} · 能力卡片 · ${dimension}\n\n(证据: rawText 包含 "${dimension}")\n\n(来自 rawText 实查, 非模板填空)`,
```

- [ ] **Step 4: knowledge-submit.js 兜底**

文件 `opphub-skill/bin/opphub-knowledge-submit.js`, 在 `for (const card of cards)` 块内, 找到:

```js
    const { type, dimension, text } = card;
    if (!type || !dimension || !text) {
      continue;
    }
    const idempotencyKey = sha256(`${opcId}|${type}|${dimension}`);
    const fullRawText = rawTextCtx ? `${rawTextCtx}\n\n---\n${text}` : text;
    const contentHash = sha256(fullRawText);
```

修改为:

```js
    const { type, dimension, text } = card;
    if (!type || !dimension || !text) {
      continue;
    }
    // v4.0.9: 兜底 - 老的 card.text 没版本头时, 补上 (旧 skill 数据兼容)
    const textWithHeader = text.startsWith("<!-- opphub-raw-text-v1 -->")
      ? text
      : `<!-- opphub-raw-text-v1 -->\n${text}`;
    const idempotencyKey = sha256(`${opcId}|${type}|${dimension}`);
    const fullRawText = rawTextCtx ? `${rawTextCtx}\n\n---\n${textWithHeader}` : textWithHeader;
    const contentHash = sha256(fullRawText);
```

- [ ] **Step 5: 验证 skill 输出带版本头**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/skills/opphub

echo "=== discover passthrough 期望 rawText 首行是 v1 ==="
node bin/opphub-knowledge-discover --name "测试公司" --raw-text "上海睿驰嘉禾是一家 MCN" --json 2>&1 | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('rawText 首行:', d.get('rawText','').split(chr(10))[0])
"

echo "=== discover query-plan skeleton 也带 v1 ==="
node bin/opphub-knowledge-discover --name "测试公司" --json 2>&1 | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('skeleton 首行:', d.get('rawTextSkeleton','').split(chr(10))[0])
"
```

预期: 两个输出首行都是 `<!-- opphub-raw-text-v1 -->`

- [ ] **Step 6: Commit**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/skills/opphub
git checkout main
git add bin/opphub-knowledge-card.js bin/opphub-knowledge-discover.js bin/opphub-knowledge-submit.js
git commit -m "feat(skill): rawText 顶部加 opphub-raw-text-v1 版本头 (未来 v2 兼容)"
```

---

## Task 2: skill 端 card 同时输出 parsedFields 结构化字段

**Files:**
- Modify: `opphub-skill/bin/opphub-knowledge-card.js`
- Modify: `opphub-skill/bin/opphub-knowledge-submit.js`

**背景**: server schema 已经有 `parsedFields: Json` 字段 (prisma/schema.prisma:172 注释里写 "拆出的结构化字段"), 但 skill 端目前不输出. 这一 task 让 skill 把抽出的结构化字段带过去.

- [ ] **Step 1: knowledge-card.js 顶层输出加 parsedFields 字段**

文件 `opphub-skill/bin/opphub-knowledge-card.js`, 找到 main 函数最后 return 的 JSON (大约 `result` 对象), 在 `cards` 字段后加 `parsedFields`:

```js
// 改前 (示意):
const result = {
  ok: true,
  name,
  industry: { ... },
  cards,
  unmatchedTemplates,
  ...
};

// 改后:
const result = {
  ok: true,
  name,
  industry: { ... },
  cards,
  parsedFields: extractParsedFields(name, rawText, industry),  // 新增
  unmatchedTemplates,
  ...
};
```

- [ ] **Step 2: extractParsedFields 函数实现**

在 knowledge-card.js 顶部 (INDUSTRY_TEMPLATES 后面) 加:

```js
// 从 rawText 抽结构化字段 (公司基础信息)
function extractParsedFields(name, rawText, industry) {
  const fields = {};
  fields.companyName = name;
  fields.industry = industry ? { code: industry.code, name: industry.name } : null;

  // 法律实体
  const legalPersonMatch = rawText.match(/法人[:：]\s*([^\n]+)/);
  if (legalPersonMatch) fields.legalPerson = legalPersonMatch[1].trim().slice(0, 50);

  // 注册资本
  const capitalMatch = rawText.match(/注册资本[:：]\s*([^\n]+)/);
  if (capitalMatch) fields.registeredCapital = capitalMatch[1].trim().slice(0, 50);

  // 信用代码
  const creditMatch = rawText.match(/(?:信用代码|统一社会信用代码)[:：]\s*([A-Z0-9]{18,20})/);
  if (creditMatch) fields.creditCode = creditMatch[1].trim();

  // 团队规模
  const sizeMatch = rawText.match(/(?:团队规模|规模|人数)[:：]\s*([^\n]+)/);
  if (sizeMatch) fields.teamSize = sizeMatch[1].trim().slice(0, 50);

  // 地址
  const addressMatch = rawText.match(/地址[:：]\s*([^\n]+)/);
  if (addressMatch) fields.address = addressMatch[1].trim().slice(0, 100);

  // 城市 (从地址或 rawText 提取)
  const cities = ["上海", "北京", "深圳", "广州", "杭州", "成都", "南京", "武汉", "苏州", "天津", "重庆"];
  for (const c of cities) {
    if (rawText.includes(c)) { fields.city = c; break; }
  }

  // 业务描述 (取 2. 业务描述 段)
  const bizMatch = rawText.match(/##\s*2\.\s*业务描述\s*\n+([\s\S]*?)(?=\n##\s|\s*$)/);
  if (bizMatch) fields.businessDescription = bizMatch[1].trim().slice(0, 500);

  return fields;
}
```

- [ ] **Step 3: knowledge-submit.js 把 parsedFields 传给 ingest**

文件 `opphub-skill/bin/opphub-knowledge-submit.js`, 找到 cards 加载的地方 (大约 `const cards = ...`), 在读 cards.json 后, 提取 parsedFields:

```js
// 改前:
let cardsDoc;
try {
  cardsDoc = JSON.parse(readFileSync(args.cards, "utf8"));
} catch (e) { ... }

const name = cardsDoc.name || args.company || "(未指定)";
const cards = Array.isArray(cardsDoc.cards) ? cardsDoc.cards : ...;
```

修改为:

```js
let cardsDoc;
try {
  cardsDoc = JSON.parse(readFileSync(args.cards, "utf8"));
} catch (e) { ... }

const name = cardsDoc.name || args.company || "(未指定)";
const cards = Array.isArray(cardsDoc.cards) ? cardsDoc.cards : ...;
const parsedFields = cardsDoc.parsedFields || null;  // 新增
```

然后在 for 循环的 body 提交时, 加 `parsedFields` 字段. 找到 `body: JSON.stringify({` 那块:

```js
        body: JSON.stringify({
          opcId,
          rawText: fullRawText,
          sourceType: "auto",
          entryType: type,
          entryDimension: dimension,
          idempotencyKey,
          contentHash,
          forceOverride: args.forceOverrideConflict,
        }),
```

修改为 (用 const card 关联 parsedFields 一次, 因为 cards 数组里其实没 parsedFields, 是顶层):

```js
        body: JSON.stringify({
          opcId,
          rawText: fullRawText,
          sourceType: "auto",
          entryType: type,
          entryDimension: dimension,
          idempotencyKey,
          contentHash,
          parsedFields: parsedFields ?? undefined,  // 第一张卡带, 后续重复 server 用 no_change
          forceOverride: args.forceOverrideConflict,
        }),
```

(只在第一张卡带 parsedFields 也可以, server 端用 idempotencyKey 关联, 后续 no_change 时不需要再传. 但为简化, 每张都传, server 会去重.)

- [ ] **Step 4: 验证 card 输出含 parsedFields**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/skills/opphub

echo "=== knowledge-card 输出含 parsedFields ==="
node bin/opphub-knowledge-card \
  --name "测试公司" \
  --raw-text '# 测试公司 · 自动画像

## 1. 工商信息
- 名称: 测试公司
- 法人: 张三
- 注册资本: 100万
- 信用代码: 91310110MA12345678
- 团队规模: 50人
- 地址: 上海市杨浦区某路 1 号

## 2. 业务描述
短视频内容制作, 达人投放

' \
  --json 2>&1 | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('parsedFields:', json.dumps(d.get('parsedFields', {}), ensure_ascii=False, indent=2))
"
```

预期: 输出 parsedFields 含 companyName / legalPerson / city / businessDescription 等

- [ ] **Step 5: Commit**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/skills/opphub
git checkout main
git add bin/opphub-knowledge-card.js bin/opphub-knowledge-submit.js
git commit -m "feat(skill): knowledge-card 输出 parsedFields, knowledge-submit 透传"
```

---

## Task 3: skill 端 confirmation state machine (4 种 entryType 全部列清单)

**Files:**
- Modify: `opphub-skill/bin/opphub-knowledge-card.js` (加 confirmation payload)
- Modify: `opphub-knowledge-submit.js` 加 `--confirm` 开关 (默认拒绝, 收到才入)
- Modify: `SKILL.md` (更新「偶合录入 [公司]」的描述, 加确认步骤)

**背景**: 当前 skill 6 步里第 4 步说 "给你 1 张清单确认" 但没具体实现. 这一 task 让 card 步骤输出 confirm 卡片 (含 4 种 entryType 全部), submit 默认拒绝, 收到 `--confirm` 才入库.

注意: 这是 skill 端"工作流"调整, 不是新增 bin.

- [ ] **Step 1: knowledge-card.js 输出确认 payload**

文件 `opphub-skill/bin/opphub-knowledge-card.js`, 找到 main 函数最后 return 的 JSON, 在 `unmatchedTemplates` 后加 `confirmation` 字段:

```js
const result = {
  ok: true,
  name,
  industry: { ... },
  cards,
  parsedFields,
  unmatchedTemplates,
  confirmation: buildConfirmationList(name, industry, cards, parsedFields),  // 新增
  ...
};
```

- [ ] **Step 2: buildConfirmationList 函数**

在 knowledge-card.js 顶部 `extractParsedFields` 后面加:

```js
// 生成 4 种 entryType 全部的确认清单
// 用途: 供 IM bot 给用户发「将要录入什么」的清单
function buildConfirmationList(name, industry, cards, parsedFields) {
  const groups = {
    ability: { label: "我能提供", emoji: "✅", items: [] },
    downstream: { label: "我想找", emoji: "🔍", items: [] },
    upstream: { label: "我的依赖", emoji: "⬆️", items: [] },
    peer: { label: "同行关系", emoji: "🔗", items: [] },
  };
  for (const c of cards) {
    if (groups[c.type]) {
      groups[c.type].items.push({
        dimension: c.dimension,
        evidenceSource: c.evidenceSource ?? "rawText 关键词命中",
      });
    }
  }

  // 把空组去掉, 只列有内容的
  const nonEmpty = Object.entries(groups).filter(([_, g]) => g.items.length > 0);

  return {
    name,
    industry: industry ? { code: industry.code, name: industry.name } : null,
    companyName: parsedFields?.companyName ?? name,
    businessDescription: parsedFields?.businessDescription ?? null,
    totalCards: cards.length,
    groups: nonEmpty.map(([type, g]) => ({ type, label: g.label, emoji: g.emoji, items: g.items })),
    instructions: "回复「确认」入库；回复「删 <type.dimension>」去掉某条；回复「重抽」回到阶段 1",
  };
}
```

- [ ] **Step 3: knowledge-submit.js 加 `--confirm` 开关**

文件 `opphub-skill/bin/opphub-knowledge-submit.js`, 找到 `parseArgs` 函数, 加 `--confirm` 解析:

```js
else if (a === "--confirm") args.confirm = true;
```

并在 main 函数顶部, 在读完 cards 之后, 加校验:

```js
if (!args.confirm) {
  if (wantJson) out({
    ok: false,
    error: "needs_confirmation",
    message: "未确认 — 需先跑 knowledge-card 看 confirmation 清单, 用户回复'确认'后再加 --confirm 入库",
  });
  process.exit(1);
}
```

(没 --confirm 直接拒绝, 防止 skill 端自动入库跳过用户确认)

- [ ] **Step 4: SKILL.md 更新「偶合录入」流程**

文件 `opphub-skill/SKILL.md`, 找到 "### 5. @bot 说\"偶合录入 [公司名]\"" 这一节, 在最后追加确认步骤:

在原 `6 步` 描述后加:

> 第 4 步拆出能力后, bot **不直接入库**, 先给一张确认清单 (含 4 种 entryType: 我能提供/我想找/我的依赖/同行关系).
> 用户回复:
> - 「确认」 → bot 调 `knowledge-submit --confirm` 入库
> - 「删 <type.dimension>」 → bot 去掉某条重发清单
> - 「重抽」 → 回到阶段 1 重新联网查
> - 「改 <字段>」 → 改解析字段后重发清单

- [ ] **Step 5: 验证 confirmation 输出**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/skills/opphub

echo "=== knowledge-card 输出含 confirmation ==="
node bin/opphub-knowledge-card \
  --name "测试公司" \
  --raw-text '# 测试公司

## 2. 业务描述
达人投放, 短视频脚本

' \
  --json 2>&1 | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('confirmation:', json.dumps(d.get('confirmation', {}), ensure_ascii=False, indent=2))
"

echo "=== submit 不带 --confirm 期望拒绝 ==="
echo '[]' > /tmp/empty.json
node bin/opphub-knowledge-submit --cards /tmp/empty.json --json 2>&1 | head -10
```

预期: confirmation 含 4 个 groups (空组会跳过), submit 返 `needs_confirmation` 错误

- [ ] **Step 6: Commit**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/skills/opphub
git checkout main
git add bin/opphub-knowledge-card.js bin/opphub-knowledge-submit.js SKILL.md
git commit -m "feat(skill): card 输出 confirmation 清单 (4 entryType), submit 加 --confirm 开关"
```

---

## Task 4: web /knowledge 按 opcId 分组, 每组只显示现行版

**Files:**
- Modify: `opphub-web/app/knowledge/page.tsx`

- [ ] **Step 1: 改 fetch + 状态**

文件 `opphub-web/app/knowledge/page.tsx`, 找到 fetch 数据逻辑 (大约 `fetch(\`${apiBase}/api/knowledge?opcId=me&entryType=${tab}\`)`). 修改成不带 entryType 过滤 (拉所有现行版, server 默认就只返 `supersededAt: null`):

```tsx
fetch(`${apiBase}/api/knowledge?opcId=me`, {
  headers: { authorization: "Bearer " + token },
})
```

(原 code 带 `&entryType=${tab}` 过滤, 改为拉所有, 然后在客户端按 tab 过滤显示. 因为 grouping 要按 opcId 看全部)

- [ ] **Step 2: 客户端按 entryType 过滤 + 按 opcId 分组**

在 component 里, fetch 数据后:

```tsx
const filtered = entries.filter((e) => e.entryType === tab);
const grouped: Array<{ opcId: string; entries: typeof entries }> = [];
const byOpc = new Map<string, typeof entries>();
for (const e of filtered) {
  const k = parsedCompanyName(e) || "未命名公司";  // 同一 opcId 下用 companyName 分组
  if (!byOpc.has(k)) byOpc.set(k, []);
  byOpc.get(k)!.push(e);
}
for (const [k, v] of byOpc) grouped.push({ opcId: k, entries: v });
```

(注意: 所有 entry 共享 opcId="me", 但 rawText 里 companyName 不同. 我们的分组维度是 companyName, 不是 opcId. 这里修正: 把"按 opcId 分组"理解为"按公司分组", 用 parsedFields.companyName 或 rawText 头一行提取)

- [ ] **Step 3: 新增 parsedCompanyName helper**

在 component 里加:

```tsx
function parsedCompanyName(entry: { entryType: string | null; entryDimension: string | null; rawText: string }): string {
  // 优先级 1: 解析 rawText 头部 "## 1. 工商信息" 段中的 "- 名称:"
  const match = entry.rawText.match(/^-\s*名称[:：]\s*([^\n]+)/m);
  if (match) return match[1].trim().slice(0, 30);
  // 优先级 2: 用 entryDimension 当 fallback
  return entry.entryDimension || "未命名";
}
```

(临时方案, 阶段 3 重做时用 server 端 parsedFields 字段)

- [ ] **Step 4: 改渲染 (masonry → group by company)**

在 JSX 里, 把原来 `entries.map((e) => <EntryCard ...)` 改成:

```tsx
{grouped.map((g) => (
  <div key={g.opcId} style={{ breakInside: "avoid", marginBottom: 16 }}>
    <div style={{
      fontSize: 12, fontWeight: 600, color: "rgba(255,255,255,0.9)",
      marginBottom: 8, paddingLeft: 4,
    }}>
      📇 {g.opcId} · {g.entries.length} 条
    </div>
    {g.entries.map((e) => <EntryCard key={e.id} entry={e} ... />)}
  </div>
))}
```

- [ ] **Step 5: 验证 build**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-web && npm run build 2>&1 | grep -E "(Compiled|error|knowledge)" | head -10
```

预期: `Compiled successfully`, 路由 `/knowledge` 仍存在

- [ ] **Step 6: Commit**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-web
git checkout main
git add app/knowledge/page.tsx
git commit -m "feat(knowledge): /knowledge 按 companyName 分组, 只显示现行版"
```

---

## Task 5: web /knowledge 顶部"如何录入"文字引导

**Files:**
- Modify: `opphub-web/app/knowledge/page.tsx`

- [ ] **Step 1: 在 `<h1>` 之后, 插入引导卡片**

文件 `opphub-web/app/knowledge/page.tsx`, 找到 `<h1 style={{ color: "white", fontSize: 24, margin: "0 0 6px" }}>📇 知识库</h1>`, **在它后面** 插入:

```tsx
{/* 录入引导 - skill 是录入主路 */}
<div style={{
  background: "rgba(255,255,255,0.95)",
  border: "1px solid #e0e7ff",
  borderRadius: 12,
  padding: "16px 20px",
  marginBottom: 16,
  color: "#1f2937",
  boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
}}>
  <div style={{ fontSize: 15, fontWeight: 600, marginBottom: 8 }}>💡 如何录入一条知识？</div>
  <div style={{ fontSize: 13, color: "#4b5563", lineHeight: 1.8, marginBottom: 8 }}>
    录入是 openclaw skill 在你的 IM 客户端里完成的, 不在网页. 装好 <code>opphub</code> skill + plugin 后, 在飞书/钉钉/微信/Telegram 里给偶合 bot 发:
  </div>
  <ul style={{ fontSize: 13, color: "#374151", lineHeight: 1.9, margin: 0, paddingLeft: 20 }}>
    <li><code style={codeInline}>偶合录入 [公司名]</code> — 录入公司能力画像 (skill 自动联网查 + 推断行业 + 拆 4 种能力 + 等你确认)</li>
    <li><code style={codeInline}>偶合录入我的能力: [一段话]</code> — 录入你个人能力</li>
    <li><code style={codeInline}>偶合录入我要找: [需求描述]</code> — 录入你想找的需求</li>
    <li><code style={codeInline}>偶合录入关联公司 + 合同 xls</code> — 上传合同 xls 拆上下游</li>
  </ul>
  <div style={{ fontSize: 12, color: "#6b7280", marginTop: 10, paddingTop: 10, borderTop: "1px dashed #e5e7eb" }}>
    bot 拆完会先给你一张「将要录入」的清单 (含 4 种 entryType: 我能提供/我想找/我的依赖/同行关系), 你回复"确认"才入库.
    5 秒后, 你录入的内容会出现在这里, 系统会自动跑匹配, 通知你潜在合作方.
    还没装 skill?<a href="https://github.com/mtty-ai/opphub-skill" target="_blank" rel="noreferrer" style={{ color: "#4f46e5" }}>安装文档</a>
  </div>
</div>
```

并在文件底部 styles 段添加:

```tsx
const codeInline: React.CSSProperties = {
  background: "#eef2ff",
  color: "#4f46e5",
  padding: "1px 6px",
  borderRadius: 4,
  fontSize: 12,
  fontFamily: 'ui-monospace, "SF Mono", Menlo, monospace',
};
```

- [ ] **Step 2: 验证 build**

```bash
cd opphub-web && npm run build 2>&1 | grep -E "(Compiled|error|knowledge)" | head -10
```

预期: `Compiled successfully`

- [ ] **Step 3: Commit**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-web
git checkout main
git add app/knowledge/page.tsx
git commit -m "feat(knowledge): /knowledge 顶部加'如何录入'文字引导 (含确认流程说明)"
```

---

## Task 6: 部署 ECS + 终验

- [ ] **Step 1: scp web 改动**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev
scp opphub-web/app/knowledge/page.tsx opphub-ecs:/opt/1panel/www/opphub-web/app/knowledge/page.tsx
```

(skill 端是用户机器, 不需要 scp)

- [ ] **Step 2: 容器 build + 重启**

```bash
ssh opphub-ecs "docker exec opphub-web sh -c 'cd /app && npm run build 2>&1 | tail -5'"
ssh opphub-ecs "docker restart opphub-web"
sleep 5
ssh opphub-ecs 'docker ps | grep opphub-web'
```

- [ ] **Step 3: 验证生产 /knowledge 有引导文字**

```bash
ssh opphub-ecs 'curl -s http://localhost:3000/knowledge | grep -c "如何录入" || echo "0"'
```

预期: >= 1

- [ ] **Step 4: git tag**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-web
git tag phase-2-confirm-group
```

---

## 完成判定 (v4 修订版)

- [ ] Task 1: skill 3 个 bin 输出 rawText 首行带 `<!-- opphub-raw-text-v1 -->` 头
- [ ] Task 2: skill knowledge-card 输出 parsedFields, knowledge-submit 透传到 ingest
- [ ] Task 3: skill knowledge-card 输出 confirmation 清单 (4 entryType 全部), submit 不带 --confirm 拒绝
- [ ] Task 4: web `/knowledge` 按 companyName 分组, 每组只显示现行版
- [ ] Task 5: web `/knowledge` 顶部有"如何录入"文字引导
- [ ] Task 6: ECS 部署 + 引导文字在生产可见
- git tag `phase-2-confirm-group`

## YAGNI 范围 (本阶段明确不做)

- ❌ /knowledge/new 表单
- ❌ /api/knowledge/dimensions 端点
- ❌ entryDimension enum 强制
- ❌ rawText 强结构校验
- ❌ skill 端做匹配 (server worker 的事)
- ❌ skill 端做推送 (opphub-ws 的事)
- ❌ lib/knowledge-dimensions.ts 共享 enum
- ❌ 📌 自定义 标记
- ❌ 录入成功 banner (skill 跑完用户已在 IM 端, web 这里不重复)
- ❌ 矛盾 / 重复检测 (阶段 3+)

## 为什么 v4 比 v3 更好

- v3 只加 rawText 版本头 + web 引导 (4 文件), 是 "格式" 升级, 没碰核心流程
- v4 在 v3 基础上**加 3 件事**:
  - **确认流程** (skill 端的核心安全网, 防止乱入库)
  - **确认清单覆盖 4 种 entryType** (不只是 ability, 包含 downstream/upstream/peer)
  - **结构化字段** (parsedFields, 让 web 端有数据画公司卡片)
  - **按公司分组** (web 端展示的核心组织维度, 现行版 vs 历史版区分)

## 这一阶段真实价值

- 录入从 "skill 自动入库" 改成 "skill 拆卡 + 用户确认 + 入库" - 防止 skill 抽错乱入
- 4 种 entryType 全部覆盖 - 不漏需求方
- 解析字段入库 - 未来 server 端能基于结构化数据做匹配/统计
- web 端按公司分组 - 用户一眼看到自己有什么公司画像, 每家公司几条能力
