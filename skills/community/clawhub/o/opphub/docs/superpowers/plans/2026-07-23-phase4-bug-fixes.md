# OppHub 阶段 4 修订版：6 个 bug + 1 个产品问题

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 修 4 个 UI bug, 跑一次 skill 模拟录入, /discover 视觉区分, 文案微调. 1 个紧急事: 恢复丢失的 API 文件.

**Architecture:** 修 opphub-web 前端 + 恢复 opphub-web API routes + 跑 opphub-skill 模拟 (不部署 skill). 不改 server 业务逻辑.

**Tech Stack:** Next.js 14, React, fetch

---

## 0. 关键事实

- **API 文件丢失**: `app/api/knowledge/[id]/route.ts` 和 `app/api/knowledge/[id]/history/route.ts` 在之前 server migration 中被误删, 不在 git history. 必须重建 (Task 0 紧急).
- **「我的卡片」文案**: 引导区文案 "如何录入一条知识？" 改 "如何录入一条卡片？"
- **/discover 当前 buyer/seller 内容一样**: 因为两 tab 都查同 source, 之前忽略. 现在做视觉区分.
- **skill 模拟**: 在本机跑 `opphub-skill` 三个 bin (discover + card + submit), 录入 上海睿驰嘉禾数字传媒科技有限公司

---

## 1. 任务地图 (8 个)

```
Task 0: 紧急 - 恢复丢失的 API routes
Task 1: EditModal 高度修复 (modal 撑高 + textarea 固定高度)
Task 2: 历史版本查看详情 (点行展开 rawText, server 加 rawText 字段)
Task 3: Delete 错误处理改进 (fetch + try-catch + 准确报错)
Task 4: 引导文案改 "如何录入一条卡片"
Task 5: /discover 视觉区分 (背景色 + emoji + label)
Task 6: 跑 skill 模拟 上海睿驰嘉禾 录入
Task 7: 部署 ECS + 终验
```

---

## Task 0: 紧急 - 恢复丢失的 API routes

**Files:**
- Create: `opphub-web/app/api/knowledge/[id]/route.ts` (DELETE + PATCH)
- Create: `opphub-web/app/api/knowledge/[id]/history/route.ts` (GET history)

- [ ] **Step 1: 重建 [id]/route.ts (DELETE + PATCH)**

文件 `opphub-web/app/api/knowledge/[id]/route.ts`:

```ts
import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/packages/db/prisma";
import jwt from "jsonwebtoken";
import { getJwtSecret } from "@/packages/db/jwt";
import { createHash } from "node:crypto";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

function getOpcIdFromToken(req: NextRequest): string | null {
  const auth = req.headers.get("authorization");
  if (!auth?.startsWith("Bearer ")) return null;
  try {
    const payload = jwt.verify(auth.slice(7), getJwtSecret()) as any;
    return payload?.opcId ?? payload?.sub ?? null;
  } catch {
    return null;
  }
}

function sha256(s: string): string {
  return createHash("sha256").update(s).digest("hex");
}

export async function PATCH(req: NextRequest, { params }: { params: { id: string } }) {
  const tokenOpcId = getOpcIdFromToken(req);
  if (!tokenOpcId) {
    return NextResponse.json({ ok: false, error: "unauthorized", message: "token 无效或过期" }, { status: 401 });
  }

  const body = await req.json().catch(() => ({}));
  const rawText = typeof body?.rawText === "string" ? body.rawText : null;
  if (!rawText) {
    return NextResponse.json({ ok: false, error: "missing_rawtext", message: "需要 rawText" }, { status: 400 });
  }

  const entry = await prisma.opcKnowledgeEntry.findUnique({ where: { id: params.id } });
  if (!entry) {
    return NextResponse.json({ ok: false, error: "not_found", message: "条目不存在" }, { status: 404 });
  }
  if (entry.opcId !== tokenOpcId) {
    return NextResponse.json({ ok: false, error: "forbidden", message: "不能编辑其他用户的条目" }, { status: 403 });
  }

  const now = new Date();
  const newContentHash = sha256(rawText);
  const versionKey = sha256(entry.opcId + "|" + entry.id + "|" + now.getTime());

  const [, newEntry] = await prisma.$transaction([
    prisma.opcKnowledgeEntry.update({
      where: { id: entry.id },
      data: { supersededAt: now, idempotencyKey: null },
    }),
    prisma.opcKnowledgeEntry.create({
      data: {
        opcId: entry.opcId,
        sourceType: entry.sourceType,
        rawText,
        status: "done",
        entryType: entry.entryType,
        entryDimension: entry.entryDimension,
        idempotencyKey: versionKey,
        contentHash: newContentHash,
        visibility: entry.visibility,
        previousEntryId: entry.id,
      },
    }),
  ]);

  return NextResponse.json({
    ok: true,
    action: "updated",
    entryId: newEntry.id,
    previousEntryId: entry.id,
    version: "new_version_created",
  });
}

export async function DELETE(req: NextRequest, { params }: { params: { id: string } }) {
  const tokenOpcId = getOpcIdFromToken(req);
  if (!tokenOpcId) {
    return NextResponse.json({ ok: false, error: "unauthorized", message: "token 无效或过期" }, { status: 401 });
  }

  const entry = await prisma.opcKnowledgeEntry.findUnique({ where: { id: params.id } });
  if (!entry) {
    return NextResponse.json({ ok: false, error: "not_found", message: "条目不存在" }, { status: 404 });
  }
  if (entry.opcId !== tokenOpcId) {
    return NextResponse.json({ ok: false, error: "forbidden", message: "不能删除其他用户的条目" }, { status: 403 });
  }

  await prisma.opcKnowledgeEntry.update({
    where: { id: params.id },
    data: { deletedAt: new Date() },
  });

  return NextResponse.json({ ok: true });
}
```

- [ ] **Step 2: 重建 [id]/history/route.ts (GET history chain + rawText)**

文件 `opphub-web/app/api/knowledge/[id]/history/route.ts`:

```ts
import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/packages/db/prisma";
import jwt from "jsonwebtoken";
import { getJwtSecret } from "@/packages/db/jwt";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

function getOpcIdFromToken(req: NextRequest): string | null {
  const auth = req.headers.get("authorization");
  if (!auth?.startsWith("Bearer ")) return null;
  try {
    const payload = jwt.verify(auth.slice(7), getJwtSecret()) as any;
    return payload?.opcId ?? payload?.sub ?? null;
  } catch {
    return null;
  }
}

function extractTitle(rawText: string): string {
  const lines = rawText.split("\n").map(l => l.trim()).filter(Boolean);
  for (const line of lines) {
    const m = line.match(/^(?:能力|技能|公司|服务|经验|title|skill|company|service|experience)[:：]\s*(.+)$/i);
    if (m) return m[1].trim().slice(0, 60);
  }
  return (lines[0] ?? "未命名").slice(0, 60);
}

export async function GET(req: NextRequest, { params }: { params: { id: string } }) {
  const tokenOpcId = getOpcIdFromToken(req);
  if (!tokenOpcId) {
    return NextResponse.json({ ok: false, error: "unauthorized", message: "token 无效或过期" }, { status: 401 });
  }

  const entry = await prisma.opcKnowledgeEntry.findUnique({
    where: { id: params.id },
    select: { id: true, opcId: true, previousEntryId: true, rawText: true, createdAt: true, supersededAt: true },
  });
  if (!entry) {
    return NextResponse.json({ ok: false, error: "not_found", message: "条目不存在" }, { status: 404 });
  }
  if (entry.opcId !== tokenOpcId) {
    return NextResponse.json({ ok: false, error: "forbidden", message: "不能查看其他用户的条目版本历史" }, { status: 403 });
  }

  // 顺链: currentEntryId + 前链 (entryId 上溯找前链)
  const versions = [];
  let currentId: string | null = params.id;
  let depth = 0;
  while (currentId && depth < 50) {
    const v = await prisma.opcKnowledgeEntry.findUnique({
      where: { id: currentId },
      select: { id: true, rawText: true, createdAt: true, previousEntryId: true, supersededAt: true },
    });
    if (!v) break;
    versions.push({
      id: v.id,
      title: extractTitle(v.rawText),
      rawText: v.rawText,
      createdAt: v.createdAt.toISOString(),
      supersededAt: v.supersededAt?.toISOString() ?? null,
      isCurrent: v.supersededAt === null,
    });
    currentId = v.previousEntryId;
    depth++;
  }

  return NextResponse.json({
    ok: true,
    entryId: params.id,
    versions,
    total: versions.length,
  });
}
```

- [ ] **Step 3: 验证 build**

```bash
cd opphub-web && npm run build 2>&1 | grep -E "Compiled|error" | head -3
```

预期: Compiled successfully, 路由 `/api/knowledge/[id]` 和 `/api/knowledge/[id]/history` 出现

- [ ] **Step 4: Commit**

```bash
git add app/api/knowledge/
git commit -m "fix(api): 重建 /api/knowledge/[id] PATCH+DELETE, /api/knowledge/[id]/history (历史 chain + rawText)"
```

---

## Task 1: EditModal 高度修复 (modal 撑高 + textarea 固定高度)

**Files:**
- Modify: `opphub-web/app/knowledge/page.tsx`

- [ ] **Step 1: 改 EditModal 容器高度**

找到 `function EditModal` 里的 `return (` 那段, 把外层 modalCard 改为:

```tsx
      <div style={{ ...modalCard, maxWidth: 720, maxHeight: "90vh" }} onClick={(e) => e.stopPropagation()}>
```

- [ ] **Step 2: 改 textarea 固定高度 (可滚动)**

找到 EditModal 里的 `<textarea ...>` 块, 替换为:

```tsx
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          style={{
            ...rawTextBlock,
            border: "none",
            fontFamily: "inherit",
            resize: "none",
            minHeight: 500,
            maxHeight: "calc(90vh - 200px)",
          }}
        />
```

(注: 不要 `flex: 1`, 改用 minHeight: 500. maxHeight 留出 200px 给 header + footer)

- [ ] **Step 3: Build + Commit**

```bash
cd opphub-web && npm run build 2>&1 | grep -E "Compiled|error" | head -3
git add app/knowledge/page.tsx
git commit -m "fix(knowledge): EditModal 撑高 + textarea 固定 500px (可滚动)"
```

---

## Task 2: 历史版本点行展开 rawText (复用 Task 0 新加的 rawText 字段)

**Files:**
- Modify: `opphub-web/app/knowledge/page.tsx`

- [ ] **Step 1: HistoryModal 加点击展开 state**

找到 `HistoryModal` 函数, 替换为:

```tsx
function HistoryModal({ entryId, onClose }: { entryId: string; onClose: () => void }) {
  const apiBase = process.env.NEXT_PUBLIC_API_BASE || "";
  const [versions, setVersions] = useState<HistoryVersion[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [expandedId, setExpandedId] = useState<string | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("opphubToken") || "";
    fetch(apiBase + "/api/knowledge/" + entryId + "/history", {
      headers: { authorization: "Bearer " + token },
    })
      .then((r) => r.json())
      .then((j) => {
        if (j?.ok && Array.isArray(j.versions)) setVersions(j.versions);
        else setError(j?.message ?? "暂无历史版本");
      })
      .catch((e) => setError(e?.message ?? "网络错误"));
  }, [entryId, apiBase]);

  return (
    <div style={modalMask} onClick={onClose}>
      <div style={modalCard} onClick={(e) => e.stopPropagation()}>
        <div style={modalHead}>
          <div style={{ fontSize: 16, fontWeight: 600, color: "#1f2937" }}>📜 版本历史</div>
          <button onClick={onClose} style={modalClose}>×</button>
        </div>
        <div style={{ padding: 8, flex: 1, overflow: "auto" }}>
          {versions === null && <div style={{ padding: 16, textAlign: "center", color: "#9ca3af" }}>加载中...</div>}
          {error && <div style={{ padding: 16, color: "#dc2626" }}>⚠️ {error}</div>}
          {versions && versions.length === 0 && <div style={{ padding: 16, color: "#9ca3af" }}>暂无历史版本</div>}
          {versions && versions.map((v, i) => {
            const isExpanded = expandedId === v.id;
            return (
              <div key={v.id} style={{ borderBottom: "1px solid #f3f4f6" }}>
                <div
                  onClick={() => setExpandedId(isExpanded ? null : v.id)}
                  style={{ padding: "10px 12px", cursor: "pointer", display: "flex", alignItems: "center", gap: 8, background: isExpanded ? "#f9fafb" : "transparent" }}
                >
                  <span style={{ fontSize: 13, fontWeight: 600, color: "#4f46e5", fontFamily: 'ui-monospace, "SF Mono", Menlo, monospace' }}>v{versions.length - i}</span>
                  <span style={{ fontSize: 12, color: "#9ca3af" }}>{new Date(v.createdAt).toLocaleString("zh-CN", { hour12: false })}</span>
                  {v.isCurrent && <span style={{ fontSize: 10, padding: "1px 6px", background: "#d1fae5", color: "#059669", borderRadius: 8, fontWeight: 600 }}>现行</span>}
                  <span style={{ fontSize: 11, color: "#9ca3af", marginLeft: "auto" }}>{isExpanded ? "▾" : "▸"}</span>
                </div>
                <div style={{ padding: "0 12px 8px 12px", fontSize: 12, color: "#6b7280" }}>{v.title}</div>
                {isExpanded && (
                  <pre style={{ margin: "0 12px 12px 12px", padding: 10, background: "#f3f4f6", borderRadius: 6, fontSize: 12, lineHeight: 1.6, color: "#374151", whiteSpace: "pre-wrap", wordBreak: "break-word", fontFamily: 'ui-monospace, "SF Mono", Menlo, monospace' }}>{v.rawText || "(无内容)"}</pre>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Build + Commit**

```bash
cd opphub-web && npm run build 2>&1 | grep -E "Compiled|error" | head -3
git add app/knowledge/page.tsx
git commit -m "feat(knowledge): 历史版本点行展开 rawText 详情"
```

---

## Task 3: Delete 错误处理改进 (fetch + try-catch + 准确报错)

**Files:**
- Modify: `opphub-web/app/knowledge/page.tsx`

- [ ] **Step 1: DeleteModal 改用错误 state + 显式渲染**

找到 DeleteModal 函数, 替换为:

```tsx
function DeleteModal({ entry, onClose, onDeleted }: {
  entry: EntryShape;
  onClose: () => void;
  onDeleted: () => void;
}) {
  const apiBase = process.env.NEXT_PUBLIC_API_BASE || "";
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function doDelete() {
    setDeleting(true);
    setError(null);
    try {
      const token = localStorage.getItem("opphubToken") || "";
      const r = await fetch(apiBase + "/api/knowledge/" + entry.id, {
        method: "DELETE",
        headers: { authorization: "Bearer " + token },
      });
      let j: any = {};
      try { j = await r.json(); } catch { /* non-json response */ }
      if (r.ok && j?.ok) {
        onDeleted();
      } else {
        setError(`删除失败 (HTTP ${r.status}): ${j?.message ?? j?.error ?? "未知错误"}`);
      }
    } catch (e: any) {
      setError(`网络错误: ${e?.message ?? String(e)}`);
    } finally {
      setDeleting(false);
    }
  }

  return (
    <div style={modalMask} onClick={onClose}>
      <div style={{ ...modalCard, maxWidth: 420 }} onClick={(e) => e.stopPropagation()}>
        <div style={modalHead}>
          <div style={{ fontSize: 16, fontWeight: 600, color: "#1f2937" }}>🗑️ 删除这条卡片？</div>
          <button onClick={onClose} style={modalClose}>×</button>
        </div>
        <div style={{ padding: 16, fontSize: 13, color: "#4b5563", lineHeight: 1.7 }}>
          将删除 <strong>{entry.entryDimension ?? "未命名"}</strong>。删除后不可恢复 (软删, 30 天内可联系运维恢复)。
        </div>
        {error && (
          <div style={{ margin: "0 16px 12px 16px", padding: 10, background: "#fef2f2", border: "1px solid #fca5a5", borderRadius: 6, color: "#991b1b", fontSize: 12, lineHeight: 1.5 }}>
            ⚠️ {error}
          </div>
        )}
        <div style={modalFoot}>
          <button onClick={onClose} disabled={deleting} style={{ ...linkBtn, background: "#f3f4f6", color: "#374151" }}>取消</button>
          <button onClick={doDelete} disabled={deleting} style={deleteBtn}>{deleting ? "删除中..." : "确认删除"}</button>
        </div>
      </div>
    </div>
  );
}
```

(去掉 alert, 改用 setError 在 modal 体内显示)

- [ ] **Step 2: Build + Commit**

```bash
cd opphub-web && npm run build 2>&1 | grep -E "Compiled|error" | head -3
git add app/knowledge/page.tsx
git commit -m "fix(knowledge): Delete 错误在 modal 体内显示, 准确 HTTP 状态 + 异常信息"
```

---

## Task 4: 引导文案改 "如何录入一条卡片"

**Files:**
- Modify: `opphub-web/app/knowledge/page.tsx`

- [ ] **Step 1: 改文案**

找到 `💡 如何录入一条知识？`, 替换为 `💡 如何录入一条卡片？`

- [ ] **Step 2: Commit**

```bash
git add app/knowledge/page.tsx
git commit -m "fix(ui): 引导文案 '如何录入一条知识？' → '如何录入一条卡片？'"
```

---

## Task 5: /discover 视觉区分 (背景色 + emoji + label)

**Files:**
- Modify: `opphub-web/app/discover/page.tsx`

- [ ] **Step 1: 改 Tab 按钮加 emoji + 颜色**

找到两 Tab 按钮 (在 `switchRole` 调用前那块), 替换为:

```tsx
        <button
          onClick={() => switchRole("buyer")}
          style={{
            padding: "8px 16px", borderRadius: 8, border: "none", cursor: "pointer",
            background: role === "buyer" ? "#10b981" : "rgba(255,255,255,0.2)",
            color: role === "buyer" ? "white" : "white",
            fontWeight: role === "buyer" ? 600 : 400,
          }}
        >
          🔍 我在找 (浏览供应方)
        </button>
        <button
          onClick={() => switchRole("seller")}
          style={{
            padding: "8px 16px", borderRadius: 8, border: "none", cursor: "pointer",
            background: role === "seller" ? "#3b82f6" : "rgba(255,255,255,0.2)",
            color: "white",
            fontWeight: role === "seller" ? 600 : 400,
          }}
        >
          📇 我能提供 (浏览需求)
        </button>
```

(b buyer 选中绿色 #10b981, seller 选中蓝色 #3b82f6, 视觉区分)

- [ ] **Step 2: 改卡片视觉 (左侧 border-color + label)**

找到 cards 渲染那段, 把 `border: "1px solid #e5e7eb"` 改为:

```tsx
{/* role=buyer 看 ability, role=seller 看 downstream, 视觉区分 */}
            <div style={{
              border: "1px solid #e5e7eb",
              borderLeft: `4px solid ${role === "buyer" ? "#10b981" : "#3b82f6"}`,
              borderRadius: 8,
              padding: 12,
              background: role === "buyer" ? "#f0fdf4" : "#eff6ff",
            }}>
              <div style={{ fontSize: 11, color: role === "buyer" ? "#059669" : "#2563eb", fontWeight: 600, marginBottom: 4 }}>
                {role === "buyer" ? "✅ 提供方" : "🔍 需求方"}
              </div>
              <div style={{ fontSize: 12, color: "#9ca3af", marginBottom: 4 }}>{c.entryType}</div>
              <div style={{ fontSize: 16, fontWeight: 600, color: "#1f2937" }}>{c.entryDimension ?? "未命名"}</div>
              <div style={{ fontSize: 12, color: "#4b5563", marginTop: 6, lineHeight: 1.5 }}>
                {c.rawText.slice(0, 100)}...
              </div>
            </div>
```

- [ ] **Step 3: Build + Commit**

```bash
cd opphub-web && npm run build 2>&1 | grep -E "Compiled|error" | head -3
git add app/discover/page.tsx
git commit -m "feat(discover): 视觉区分供应方 (绿) vs 需求方 (蓝)"
```

---

## Task 6: 跑 skill 模拟 上海睿驰嘉禾 录入

**Files:**
- 不写代码, 只跑 skill 命令

- [ ] **Step 1: 确认 skill 端在 main 且有 rawText 版本头**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/skills/opphub
git log --oneline -3
git status
```

- [ ] **Step 2: 用 skill 模拟 discover + card + submit 流程**

这一步是模拟真实 bot turn (不用 LLM, 手动喂 rawText), 验证 skill 6 步能跑通:

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/skills/opphub

# 阶段 1: discover query plan
echo "=== 阶段 1: discover query-plan ==="
node bin/opphub-knowledge-discover --name "上海睿驰嘉禾数字传媒科技有限公司" --json 2>&1 | head -20

# 阶段 1 续: discover passthrough (手动喂 rawText 模拟 bot 填完模板)
echo ""
echo "=== 阶段 1 续: discover passthrough ==="
RAW='# 上海睿驰嘉禾数字传媒科技有限公司 · 自动画像

## 1. 工商信息
名称: 上海睿驰嘉禾数字传媒科技有限公司
法人: 刘会冬
注册资本: 1000万元人民币
信用代码: 91310110MAC019T03K
团队规模: 15-50人
地址: 上海市杨浦区三门路200号三层302-1室
成立时间: 2022-09-21

## 2. 业务描述
基于短视频平台, 为客户提供达人营销、内容制作、电商转化、平台代运营、用户运营与虚拟人技术应用服务的数字化传媒科技公司。
核心成员来自易车、蓝色光标、京东、宝马等一线上市公司团队, 在用户运营、整合营销、数据产品均有丰富经验。
尤其在汽车、金融、电商等行业积累了大量的实践经验和成功案例。
旗下产品官网: richdigital.com.cn, ruiplus.com.cn

## 3. 高管团队
CEO: 刘会冬, 曾任职京东零售集团商业提升部站外广告业务负责人/京东黑珑业务总经理; 蓝色光标集团副总裁/移动广告董事总经理; 易车集团CIG精准营销总经理/大数据营销负责人; 18年商业化运营和管理经验。

## 4. 项目案例
- 为多家汽车品牌提供达人营销和内容制作服务
- 为金融客户提供数字化营销解决方案
- 为电商品牌提供电商转化和平台代运营服务

## 5. 招聘岗位
- 新媒体运营
- 短视频编导
- 达人商务BD
- 内容策划
- 数据分析师
'

node bin/opphub-knowledge-discover \
  --name "上海睿驰嘉禾数字传媒科技有限公司" \
  --raw-text "$RAW" \
  --json 2>&1 | head -25

# 阶段 2: card 拆卡片
echo ""
echo "=== 阶段 2: knowledge-card 拆能力卡片 ==="
node bin/opphub-knowledge-card \
  --name "上海睿驰嘉禾数字传媒科技有限公司" \
  --raw-text "$RAW" \
  --json 2>&1 | head -40
```

- [ ] **Step 3: 用 confirmation 流程拿到 cards.json, submit**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/skills/opphub

# 拿 card 输出, 取 cards 数组
node bin/opphub-knowledge-card \
  --name "上海睿驰嘉禾数字传媒科技有限公司" \
  --raw-text "$RAW" \
  --json 2>&1 | python3 -c "
import sys, json
out = sys.stdin.read()
# 找 JSON 块 (从第一个 { 开始)
start = out.find('{')
j = json.loads(out[start:])
print('cards:', len(j.get('cards', [])))
print('confirmation.totalCards:', j.get('confirmation', {}).get('totalCards'))
print('parsedFields keys:', list(j.get('parsedFields', {}).keys()))
# 保存到 /tmp/ruichi_cards.json
with open('/tmp/ruichi_cards.json', 'w') as f:
    json.dump(j.get('cards', []), f, ensure_ascii=False, indent=2)
print('saved to /tmp/ruichi_cards.json')
"

# 阶段 3: submit (需要 --confirm flag)
echo ""
echo "=== 阶段 3: knowledge-submit 录入 ==="
node bin/opphub-knowledge-submit \
  --company "上海睿驰嘉禾数字传媒科技有限公司" \
  --raw-text "$RAW" \
  --cards /tmp/ruichi_cards.json \
  --confirm \
  --json 2>&1 | head -30
```

- [ ] **Step 4: 验证录入到数据库**

```bash
# 查数据库: 列出该 opc 的所有 ability entries
ssh opphub-ecs 'docker exec -w /app opphub-web sh -c "
node -e \"
const{PrismaClient}=require(\\\"@prisma/client\\\");
const p=new PrismaClient();
(async()=>{
  const r=await p.opcKnowledgeEntry.findMany({
    where:{opcId:\\\"opc_1hz6wsjrmt1s\\\", entryType:\\\"ability\\\", supersededAt:null},
    orderBy:{createdAt:\\\"desc\\\"}, take:10
  });
  for(const e of r) console.log(\\\" \\\",e.entryDimension,\\\"raw=\\\"+e.rawText.length);
  await p.\\\$disconnect();
})();
\""
'
```

预期: 至少有 4 条 ability entry (达人营销, 平台代运营, 电商转化, 内容制作等)

- [ ] **Step 5: 验证 web 页面能看到**

```bash
ssh opphub-ecs 'curl -s "http://localhost:3000/api/knowledge?opcId=me" -H "Authorization: Bearer $(curl -s -X POST http://localhost:3000/api/auth/login -H \"content-type: application/json\" -d \"{\\\"type\\\":\\\"email\\\",\\\"target\\\":\\\"chinabot@163.com\\\",\\\"password\\\":\\\"12345678\\\"}\" | python3 -c \"import sys,json; print(json.load(sys.stdin).get(\\\"opphubToken\\\",\\\"\\\"))\")" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f\"total entries: {d.get('total','?')}, returned: {len(d.get('data',[]))}\")
for e in d.get('data', [])[:8]:
    print(' ', e.get('entryType','?'), e.get('entryDimension','?'), 'rawLen:', len(e.get('rawText','')))
"'
```

预期: 看到 ability entries 数量, 每个都有 rawText

- [ ] **Step 6: 总结录入结果 (报告给用户)**

说明: 录入了什么 entry, 各 entry 的 entryType/dimension/rawText 长度

---

## Task 7: 部署 ECS + 终验

- [ ] **Step 1: scp web 改动**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev
scp -r opphub-web/app/api/knowledge opphub-ecs:/opt/1panel/www/opphub-web/app/
scp opphub-web/app/knowledge/page.tsx opphub-ecs:/opt/1panel/www/opphub-web/app/knowledge/page.tsx
scp opphub-web/app/discover/page.tsx opphub-ecs:/opt/1panel/www/opphub-web/app/discover/page.tsx
```

- [ ] **Step 2: 容器 build + 重启**

```bash
ssh opphub-ecs "docker exec opphub-web sh -c 'cd /app && npm run build 2>&1 | tail -5'"
ssh opphub-ecs "docker restart opphub-web"
sleep 5
```

- [ ] **Step 3: 验证 6 项修复**

```bash
# 1. 编辑区高度
ssh opphub-ecs "docker exec opphub-web sh -c 'cd /app && grep -c \"minHeight: 500\" .next/static/chunks/app/knowledge/page-*.js | head -3'"
# 预期: 1

# 2. 历史展开
ssh opphub-ecs "docker exec opphub-web sh -c 'cd /app && grep -c \"expandedId\" .next/static/chunks/app/knowledge/page-*.js | head -3'"
# 预期: 1

# 3. 错误显示
ssh opphub-ecs "docker exec opphub-web sh -c 'cd /app && grep -c \"setError\" .next/static/chunks/app/knowledge/page-*.js | head -3'"
# 预期: 1+

# 4. 文案
ssh opphub-ecs "curl -s http://localhost:3000/knowledge | grep -c '如何录入一条卡片' || echo 0"
# 预期: 1+ (在 bundle 内)

# 5. /discover 视觉 (curl 看到绿色/蓝色 styles)
ssh opphub-ecs "docker exec opphub-web sh -c 'cd /app && grep -c \"borderLeft\" .next/static/chunks/app/discover/page-*.js | head -3'"
# 预期: 1

# 6. API 路由
ssh opphub-ecs "curl -s -o /dev/null -w '%{http_code}\n' http://localhost:3000/api/knowledge -H 'Authorization: Bearer test'"
# 预期: 401 (auth 失败但路由存在) 或 200
```

- [ ] **Step 4: git tag**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-web
git tag phase-4-bug-fixes
```

---

## 完成判定

- [ ] Task 0: API routes 重建 (route.ts / [id]/route.ts / [id]/history/route.ts)
- [ ] Task 1: EditModal 高度修复
- [ ] Task 2: 历史版本点行展开
- [ ] Task 3: Delete 错误准确显示
- [ ] Task 4: 文案改 "如何录入一条卡片"
- [ ] Task 5: /discover 视觉区分
- [ ] Task 6: skill 模拟 睿驰 录入
- [ ] Task 7: ECS 部署 + 终验
- git tag `phase-4-bug-fixes`

## YAGNI 范围 (本阶段明确不做)

- ❌ server 端加 `visibility=PUBLIC` 过滤
- ❌ 撮合匹配对页面
- ❌ 推送通道
- ❌ 完整 SkillCard 组件回来
- ❌ 重复 / 矛盾检测
- ❌ 公司卡片信息编辑 (parsedFields 渲染)
