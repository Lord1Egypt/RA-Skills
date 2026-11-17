# OppHub 阶段 1：导航 + 角色表达改造实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 opphub-web 当前的 7 个一级导航改造为 spec 里的 6 个 (`dashboard / knowledge / discover / matches / orders / wallet`), 移除路径重复 (`/me/capabilities` ↔ `/opc/profile`, `/demands` ↔ `/marketplace`), 旧路径 301 跳新路径

**Architecture:** 保持 Next.js app router 不变, 只移文件 / 改名 / 加 redirect; 数据接口 (`/api/knowledge` 等) 不动, 这样改动可单独发版

**Tech Stack:** Next.js 14 app router, TypeScript, `next.config.js` `redirects()`

---

## 总体任务地图

```
Task 1: 文件迁移 + 旧路径 301 跳新路径
  - /me/capabilities → /knowledge
  - /opc/profile → /knowledge/[id]
  - /marketplace → /discover?role=seller
  - /demands → /discover?role=buyer
  - /match → /matches

Task 2: 新建 /knowledge, /discover, /matches (默认重定向列表)

Task 3: TopBar 改 6 个一级导航

Task 4: 验证 (本地 build + 浏览器手测)

Task 5: 部署 ECS + 终验
```

---

## Task 1: 加 next.config.js redirects 套所有旧路径

**Files:**
- Modify: `next.config.js` (新增 redirects 段, 若不存在则创建)
- Test: curl 各旧路径能 301 到新路径

- [ ] **Step 1: 读现有 next.config.js**

```bash
test -f opphub-web/next.config.js && cat opphub-web/next.config.js || echo "NOT_EXISTS"
```

预期: 输出现有内容 (或 `NOT_EXISTS`)

- [ ] **Step 2: 添加 redirects 段**

文件 `opphub-web/next.config.js`:

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  // v3.4 spec 阶段 1: 老路径 301 到新导航 (录→撮→谈→成)
  async redirects() {
    return [
      { source: "/me/capabilities", destination: "/knowledge", permanent: true },
      { source: "/opc/profile", destination: "/knowledge/profile", permanent: true },
      { source: "/marketplace", destination: "/discover?role=seller", permanent: true },
      { source: "/demands", destination: "/discover?role=buyer", permanent: true },
      { source: "/match", destination: "/matches", permanent: true },
    ];
  },
};

module.exports = nextConfig;
```

如果原本有配置就把 redirects 段塞进顶层 const 内 (保留原 reactStrictMode、images 等其他配置项)。

- [ ] **Step 3: 静态检查**

```bash
cd opphub-web && node -e "console.log(JSON.stringify(require('./next.config.js'), null, 2))" | head -40
```

预期: JSON 包含 `redirects` 是 array of 5 项

- [ ] **Step 4: Commit**

```bash
cd opphub-web
git add next.config.js
git commit -m "feat(nav): 旧导航路径 301 到新路径 (阶段 1)"
```

---

## Task 2: 新建 `/knowledge` 主页面 (Tab 表达 4 种角色)

**Files:**
- Create: `app/knowledge/page.tsx`
- Create: `app/knowledge/profile/page.tsx` (替代 `/opc/profile`)
- Create: `app/knowledge/[id]/page.tsx` (替代 `/opc/profile/[opcId]` 后续用)

- [ ] **Step 1: 新建 knowledge 主页 (空壳)**

文件 `app/knowledge/page.tsx`:

```tsx
"use client";
import { useState } from "react";
import TopBar from "../_components/TopBar";

type Tab = "ability" | "downstream" | "upstream" | "peer";

const TAB_LABEL: Record<Tab, string> = {
  ability: "我能提供",
  downstream: "我在找",
  upstream: "我的依赖",
  peer: "同行关系",
};

const TAB_DESC: Record<Tab, string> = {
  ability: "录入你的能力/服务, AI 帮你找到需求方",
  downstream: "录入你想找的东西, AI 帮你找到供应方",
  upstream: "你依赖的供应商/数据源/工具",
  peer: "同业联盟 / 同行参考 / 关联企业",
};

export default function KnowledgePage() {
  const apiBase = process.env.NEXT_PUBLIC_API_BASE || "";
  const [mounted, setMounted] = useState(false);
  const [tab, setTab] = useState<Tab>("ability");
  const [opcId, setOpcId] = useState<string>("");
  const [entries, setEntries] = useState<{ id: string; dimension: string; rawText: string; updatedAt: string }[]>([]);
  const [loading, setLoading] = useState(false);

  React.useEffect(() => setMounted(true), []);
  React.useEffect(() => {
    if (!mounted || !opcId) return;
    setLoading(true);
    const token = localStorage.getItem("opphubToken") || "";
    fetch(`${apiBase}/api/knowledge?opcId=me&entryType=${tab}`, {
      headers: { authorization: "Bearer " + token },
    })
      .then((r) => r.json())
      .then((j) => setEntries(j?.ok && Array.isArray(j.data) ? j.data : []))
      .catch(() => setEntries([]))
      .finally(() => setLoading(false));
  }, [mounted, opcId, tab, apiBase]);

  React.useEffect(() => {
    try { setOpcId(localStorage.getItem("opcId") || ""); } catch {}
  }, []);

  if (!mounted) {
    return (
      <main style={{ minHeight: "100vh", background: "linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%)" }}>
        <TopBar current="knowledge" />
        <div style={{ maxWidth: 1200, margin: "0 auto", padding: 24, color: "white" }}>加载中...</div>
      </main>
    );
  }

  return (
    <main style={{ minHeight: "100vh", background: "linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%)" }}>
      <TopBar current="knowledge" />
      <div style={{ maxWidth: 1200, margin: "0 auto", padding: 24 }}>
        <h1 style={{ color: "white", fontSize: 24, margin: "0 0 6px" }}>📇 知识库</h1>
        <p style={{ color: "rgba(255,255,255,0.85)", fontSize: 13, margin: "0 0 16px" }}>
          在聊天窗口 @偶合 说一句话录入, 或在这里浏览你已录入的条目
        </p>

        {/* Tabs */}
        <div style={{ display: "flex", gap: 4, marginBottom: 12, flexWrap: "wrap" }}>
          {(Object.keys(TAB_LABEL) as Tab[]).map((t) => (
            <button
              key={t}
              onClick={() => setTab(t)}
              style={{
                padding: "8px 16px",
                borderRadius: 8,
                border: "none",
                cursor: "pointer",
                background: tab === t ? "white" : "rgba(255,255,255,0.2)",
                color: tab === t ? "#4f46e5" : "white",
                fontWeight: tab === t ? 600 : 400,
              }}
            >
              {TAB_LABEL[t]}
            </button>
          ))}
        </div>

        <p style={{ color: "rgba(255,255,255,0.7)", fontSize: 13, marginBottom: 16 }}>
          {TAB_DESC[tab]}
        </p>

        {/* List */}
        {loading ? (
          <div style={{ background: "white", borderRadius: 12, padding: 32, textAlign: "center", color: "#6b7280" }}>⏳ 加载中...</div>
        ) : entries.length === 0 ? (
          <EmptyState tab={tab} />
        ) : (
          <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
            {entries.map((e) => <EntryCard key={e.id} entry={e} />)}
          </div>
        )}
      </div>
    </main>
  );
}

function EmptyState({ tab }: { tab: Tab }) {
  return (
    <div style={{ background: "white", borderRadius: 12, padding: 48, textAlign: "center" }}>
      <div style={{ fontSize: 48, marginBottom: 8 }}>📇</div>
      <div style={{ fontSize: 16, color: "#1f2937", marginBottom: 8 }}>
        {tab === "ability" && "你还没说能干啥"}
        {tab === "downstream" && "你还没说要找啥"}
        {tab === "upstream" && "还没录入上游依赖"}
        {tab === "peer" && "还没录入同行关系"}
      </div>
      <div style={{ fontSize: 13, color: "#6b7280", marginBottom: 16 }}>
        去聊天窗口 @偶合 说"<span style={{ color: "#4f46e5" }}>{tab === "ability" ? "录入我的服务" : tab === "downstream" ? "我需要 xxx" : tab === "upstream" ? "录入我的供应商" : "录入同行"}</span>" 开始
      </div>
    </div>
  );
}

function EntryCard({ entry }: { entry: { id: string; dimension: string; rawText: string; updatedAt: string } }) {
  const preview = entry.rawText.slice(0, 200);
  return (
    <a href={`/knowledge/${entry.id}`} style={{ textDecoration: "none" }}>
      <div style={{ background: "white", borderRadius: 12, padding: 16, cursor: "pointer" }}>
        <div style={{ fontSize: 16, fontWeight: 600, color: "#1f2937", marginBottom: 6 }}>{entry.dimension}</div>
        <div style={{ fontSize: 13, color: "#4b5563", lineHeight: 1.6, marginBottom: 6, whiteSpace: "pre-wrap" }}>{preview}{entry.rawText.length > 200 ? "..." : ""}</div>
        <div style={{ fontSize: 11, color: "#9ca3af" }}>更新: {new Date(entry.updatedAt).toLocaleString("zh-CN")}</div>
      </div>
    </a>
  );
}
```

注意: `React.useEffect` 那一段用 `useEffect` (不要写 `React.useEffect`), 顶部要加 `import { useEffect, useState } from "react";`

(此步只是把 API 数据展示出来, 编辑功能暂未接入; 详细录入正反馈/录入三选一按钮留到阶段 2-3)

- [ ] **Step 2: 新建 knowledge/profile 替代 /opc/profile**

文件 `app/knowledge/profile/page.tsx`:

```tsx
"use client";
import { Suspense, useEffect, useState } from "react";
import Link from "next/link";
import TopBar from "../../_components/TopBar";
import { useSearchParams } from "next/navigation";

export const dynamic = "force-dynamic";

type Company = {
  companyName?: string;
  companyType?: string;
  legalPerson?: string;
  teamSize?: number;
  creditCode?: string;
  address?: string;
};
type Profile = {
  mainSkill?: string;
  subSkills?: string[];
  experience?: string;
  priceMin?: number;
  priceMax?: number;
  city?: string;
  trustScore?: number;
  completedOrders?: number;
};

export default function KnowledgeProfilePage() {
  return (
    <Suspense fallback={<div style={{ color: "white", padding: 24 }}>加载中...</div>}>
      <ProfileInner />
    </Suspense>
  );
}

function ProfileInner() {
  const apiBase = process.env.NEXT_PUBLIC_API_BASE || "";
  const sp = useSearchParams();
  const opcIdQuery = sp?.get("opcId");
  const [mounted, setMounted] = useState(false);
  const [me, setMe] = useState<{ opcId?: string } | null>(null);
  const [targetOpc, setTargetOpc] = useState<string | null>(null);
  const [company, setCompany] = useState<Company | null>(null);
  const [profile, setProfile] = useState<Profile | null>(null);

  useEffect(() => { setMounted(true); }, []);
  useEffect(() => {
    try { setMe({ opcId: localStorage.getItem("opcId") || undefined }); } catch {}
  }, []);

  useEffect(() => {
    if (!mounted || !me) return;
    const target = !opcIdQuery || opcIdQuery === me.opcId ? me.opcId! : opcIdQuery;
    setTargetOpc(target);
    const token = localStorage.getItem("opphubToken") || "";
    if (target === me.opcId) {
      fetch(`${apiBase}/api/auth/me`, { headers: { authorization: "Bearer " + token } })
        .then((r) => r.json())
        .then((j) => setProfile(j?.profile ?? null))
        .catch(() => {});
    } else {
      fetch(`${apiBase}/api/opc/${target}/profile`, { headers: { authorization: "Bearer " + token } })
        .then((r) => r.json())
        .then((j) => setProfile(j?.profile ?? null))
        .catch(() => {});
    }
  }, [mounted, me, opcIdQuery, apiBase]);

  if (!mounted || targetOpc === null) {
    return <main style={{ minHeight: "100vh", background: "#f5f3ff" }}><TopBar current="knowledge/profile" /><div style={{ padding: 32 }}>⏳ 加载中...</div></main>;
  }

  const isMe = me?.opcId === targetOpc;
  return (
    <main style={{ minHeight: "100vh", background: "linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%)" }}>
      <TopBar current="knowledge/profile" />
      <div style={{ maxWidth: 800, margin: "0 auto", padding: 24 }}>
        <h1 style={{ color: "white", fontSize: 22, margin: "0 0 12px" }}>
          {isMe ? "我的公开资料" : `对方资料: ${profile?.mainSkill ?? "—"}`}
        </h1>
        <div style={{ background: "white", borderRadius: 12, padding: 24 }}>
          {profile ? <pre style={{ fontSize: 13, lineHeight: 1.7 }}>{JSON.stringify(profile, null, 2)}</pre> : <div style={{ color: "#6b7280" }}>暂无资料</div>}
          {isMe && (
            <div style={{ marginTop: 16 }}>
              <Link href="/knowledge" style={{ color: "#4f46e5", fontSize: 14 }}>← 返回知识库</Link>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
```

这一版是简化的过渡页 — 显示从 `/api/auth/me` 或 `/api/opc/[opcId]/profile` 拉的 profile 原始 JSON. 阶段 3 重做美化.

- [ ] **Step 3: 新建 knowledge/[id] 单条目查看 (替代需要时的 /opc/profile 查看页)**

> 阶段 1 只要求把旧路径跳走, 不必现在就做每条知识详情。占位即可。

文件 `app/knowledge/[id]/page.tsx`:

```tsx
"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import TopBar from "../../_components/TopBar";

export default function KnowledgeEntryDetailPage() {
  const apiBase = process.env.NEXT_PUBLIC_API_BASE || "";
  const params = useParams<{ id: string }>();
  const id = params?.id ?? "";
  const [data, setData] = useState<{ id: string; entryDimension: string; entryType: string; rawText: string; updatedAt: string } | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    const token = localStorage.getItem("opphubToken") || "";
    fetch(`${apiBase}/api/knowledge?opcId=me`, { headers: { authorization: "Bearer " + token } })
      .then((r) => r.json())
      .then((j) => {
        const found = (j?.data || []).find((e: any) => e.id === id);
        setData(found ?? null);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [id, apiBase]);

  return (
    <main style={{ minHeight: "100vh", background: "linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%)" }}>
      <TopBar current="knowledge" />
      <div style={{ maxWidth: 800, margin: "0 auto", padding: 24 }}>
        {loading && <div style={{ background: "white", borderRadius: 12, padding: 32, textAlign: "center" }}>⏳ 加载中...</div>}
        {data && (
          <div style={{ background: "white", borderRadius: 12, padding: 24 }}>
            <div style={{ fontSize: 13, color: "#9ca3af", marginBottom: 4 }}>{data.entryType}</div>
            <h1 style={{ fontSize: 20, color: "#1f2937", margin: "0 0 12px" }}>{data.entryDimension}</h1>
            <pre style={{ fontSize: 13, lineHeight: 1.7, whiteSpace: "pre-wrap", color: "#374151" }}>{data.rawText}</pre>
          </div>
        )}
      </div>
    </main>
  );
}
```

- [ ] **Step 4: 验证 build**

```bash
cd opphub-web && npm run build 2>&1 | grep -E "(Compiled|error|knowledge|discover|matches)" | head -10
```

预期: `Compiled successfully`, 路由里出现 `/knowledge`, `/knowledge/profile`, `/knowledge/[id]`

- [ ] **Step 5: Commit**

```bash
cd opphub-web
git add app/knowledge
git commit -m "feat(knowledge): 新建 /knowledge Tab 页 + 单条目详情 + profile 替代 /opc/profile"
```

---

## Task 3: 新建 `/discover` 替代 `/demands` 和 `/marketplace`

**Files:**
- Create: `app/discover/page.tsx` (整合 demands 表 + marketplace 表)

- [ ] **Step 1: 新建 discover 主页 (Tabs 切买家/卖家视角)**

文件 `app/discover/page.tsx`:

```tsx
"use client";
import { useEffect, useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import TopBar from "../_components/TopBar";

type Demand = {
  demandId: string;
  title: string;
  budget: number;
  city?: string;
  deadline?: string;
  category?: string;
  status?: string;
  createdAt: string;
};

type OPC = {
  opcId: string;
  displayName: string;
  mainSkill: string;
  city?: string;
  trustScore: number;
  priceMin: string | null;
  priceMax: string | null;
};

type Role = "buyer" | "seller";

export default function DiscoverPage() {
  const apiBase = process.env.NEXT_PUBLIC_API_BASE || "";
  const sp = useSearchParams();
  const router = useRouter();
  const initialRole = (sp?.get("role") === "seller" ? "seller" : "buyer") as Role;
  const [role, setRole] = useState<Role>(initialRole);
  const [mounted, setMounted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [demands, setDemands] = useState<Demand[]>([]);
  const [opcs, setOpcs] = useState<OPC[]>([]);

  useEffect(() => { setMounted(true); }, []);
  useEffect(() => {
    if (!mounted) return;
    setLoading(true);
    const token = localStorage.getItem("opphubToken") || "";
    if (role === "buyer") {
      // 我是买方 → 浏览供应方
      fetch(`${apiBase}/api/opc/marketplace`, { headers: { authorization: "Bearer " + token } })
        .then((r) => r.json()).then((j) => setOpcs(j?.data ?? [])).catch(() => setOpcs([]))
        .finally(() => setLoading(false));
    } else {
      // 我是卖方 → 浏览需求
      fetch(`${apiBase}/api/demands`, { headers: { authorization: "Bearer " + token } })
        .then((r) => r.json()).then((j) => setDemands(j?.demands ?? j?.data ?? []))
        .catch(() => setDemands([]))
        .finally(() => setLoading(false));
    }
  }, [mounted, role, apiBase]);

  function switchRole(r: Role) {
    setRole(r);
    router.replace(`/discover?role=${r}`);
  }

  if (!mounted) {
    return <main style={{ minHeight: "100vh", background: "linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%)" }}><TopBar current="discover" /><div style={{ color: "white", padding: 24 }}>加载中...</div></main>;
  }

  return (
    <main style={{ minHeight: "100vh", background: "linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%)" }}>
      <TopBar current="discover" />
      <div style={{ maxWidth: 1200, margin: "0 auto", padding: 24 }}>
        <h1 style={{ color: "white", fontSize: 24, margin: "0 0 6px" }}>🔍 发现</h1>
        <p style={{ color: "rgba(255,255,255,0.85)", fontSize: 13, margin: "0 0 16px" }}>
          {role === "buyer" ? "看供应方 (你的潜在合作方)" : "看需求 (你的潜在客户)"}
        </p>
        <div style={{ display: "flex", gap: 4, marginBottom: 12 }}>
          <button onClick={() => switchRole("buyer")}
            style={{ padding: "8px 16px", borderRadius: 8, border: "none", cursor: "pointer",
              background: role === "buyer" ? "white" : "rgba(255,255,255,0.2)",
              color: role === "buyer" ? "#4f46e5" : "white", fontWeight: role === "buyer" ? 600 : 400 }}>
            我在找 (浏览供应方)
          </button>
          <button onClick={() => switchRole("seller")}
            style={{ padding: "8px 16px", borderRadius: 8, border: "none", cursor: "pointer",
              background: role === "seller" ? "white" : "rgba(255,255,255,0.2)",
              color: role === "seller" ? "#4f46e5" : "white", fontWeight: role === "seller" ? 600 : 400 }}>
            我能提供 (浏览需求)
          </button>
        </div>

        {loading && <div style={{ background: "white", borderRadius: 12, padding: 32, textAlign: "center", color: "#6b7280" }}>⏳ 加载中...</div>}

        {!loading && role === "buyer" && (
          <div style={{ background: "white", borderRadius: 12, padding: 16 }}>
            <div style={{ fontSize: 14, color: "#6b7280", marginBottom: 12 }}>共 {opcs.length} 个供应方</div>
            {opcs.length === 0 ? (
              <div style={{ color: "#9ca3af", textAlign: "center", padding: 32 }}>暂无供应方</div>
            ) : (
              <div style={{ display: "grid", gap: 10, gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))" }}>
                {opcs.map((o) => (
                  <a key={o.opcId} href={`/knowledge/profile?opcId=${o.opcId}`} style={{ textDecoration: "none" }}>
                    <div style={{ border: "1px solid #e5e7eb", borderRadius: 8, padding: 12 }}>
                      <div style={{ fontSize: 16, fontWeight: 600, color: "#1f2937" }}>{o.displayName}</div>
                      <div style={{ fontSize: 13, color: "#4f46e5", margin: "4px 0" }}>{o.mainSkill}</div>
                      <div style={{ fontSize: 12, color: "#6b7280" }}>
                        {o.city ?? "—"} · ⭐{o.trustScore} · {o.priceMin ?? "—"}~{o.priceMax ?? "—"}
                      </div>
                    </div>
                  </a>
                ))}
              </div>
            )}
          </div>
        )}

        {!loading && role === "seller" && (
          <div style={{ background: "white", borderRadius: 12, padding: 16 }}>
            <div style={{ fontSize: 14, color: "#6b7280", marginBottom: 12 }}>共 {demands.length} 条需求</div>
            {demands.length === 0 ? (
              <div style={{ color: "#9ca3af", textAlign: "center", padding: 32 }}>暂无公开需求</div>
            ) : (
              <div style={{ display: "grid", gap: 10, gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))" }}>
                {demands.map((d) => (
                  <a key={d.demandId} href={`/demands/${d.demandId}`} style={{ textDecoration: "none" }}>
                    <div style={{ border: "1px solid #e5e7eb", borderRadius: 8, padding: 12 }}>
                      <div style={{ fontSize: 16, fontWeight: 600, color: "#1f2937" }}>{d.title}</div>
                      <div style={{ fontSize: 12, color: "#6b7280", marginTop: 4 }}>
                        ¥{d.budget} · {d.city ?? "—"}
                      </div>
                    </div>
                  </a>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </main>
  );
}
```

- [ ] **Step 2: Build 验证**

```bash
cd opphub-web && npm run build 2>&1 | grep -E "(Compiled|error|discover)" | head -10
```

预期: `/discover` 出现在路由列表, 无 error

- [ ] **Step 3: Commit**

```bash
cd opphub-web
git add app/discover
git commit -m "feat(discover): 新建 /discover (合并 /demands + /marketplace 视角)"
```

---

## Task 4: 新建 `/matches` 替代 `/match`

**Files:**
- Create: `app/matches/page.tsx` (暂时代理 `/match` 内容, 但 URL 改成复数)

- [ ] **Step 1: 复制 match/page.tsx 到 matches/page.tsx, 改 current=**

```bash
cd opphub-web
sed 's|"match"|"matches"|g; s|/api/opc/match/today|/api/opc/match/today|g' app/match/page.tsx > app/matches/page.tsx
grep -n "match\|Match" app/matches/page.tsx | head -10
```

预期: 看到 `/api/opc/match/today` 仍保留 (server 路径未改), `current="matches"` 已替换

- [ ] **Step 2: 在 matches/page.tsx 顶部注释里更新 spec 引用**

文件 `app/matches/page.tsx`, 改注释行 (从原 file 的注释基础替换):

```tsx
// /matches · 撮合流 (v3.4 spec 阶段 1: 替代 /match, 旧路径 301 到此)
// 当前阶段先复刻 /match 内容, 阶段 3 重做撮合详情/状态机
// 数据源: GET /api/opc/match/today
// 字段: matchingId/demandId/demandTitle/demandBudget/demandCity/demandDeadline/opc/scores/explainText/createdAt
```

(替换文件最顶部的注释段, 只改 comment 不动 logic)

- [ ] **Step 3: Build 验证**

```bash
cd opphub-web && npm run build 2>&1 | grep -E "(Compiled|error|/matches|/match)" | head -10
```

预期: `/matches` 出现在路由列表, `/match` 仍然存在 (因为 redirect 在 server 级, 路由仍编译), 无 error

- [ ] **Step 4: Commit**

```bash
cd opphub-web
git add app/matches
git commit -m "feat(matches): 新建 /matches (复刻 /match 内容, 阶段 3 重做)"
```

---

## Task 5: 改 TopBar 用 6 个一级入口

**Files:**
- Modify: `app/_components/TopBar.tsx` (`PAGE_NAME` map + `desktopLinks` + `mobileLinks` 三处)

- [ ] **Step 1: 改 PAGE_NAME 加新键值**

文件 `app/_components/TopBar.tsx`, 修改 PAGE_NAME 常量 (在第 19 行附近):

```tsx
const PAGE_NAME: Record<string, string> = {
  "": "首页",
  dashboard: "工作台",
  matches: "撮合",
  orders: "交易",
  knowledge: "知识库",
  "knowledge/profile": "我的资料",
  discover: "发现",
  wallet: "钱包",
  messages: "通知",
  "messages/legacy": "消息",
  "account/security": "账号安全",
  admin: "后台",
  onboarding: "引导",
  login: "登录",
  register: "注册",
  activate: "设备激活",
};
```

- [ ] **Step 2: 改 desktopLinks (替换为 6 个)**

文件 `app/_components/TopBar.tsx`, 替换 `desktopLinks` 整个 JSX 块:

```tsx
const desktopLinks = (
  <>
    <Link href="/dashboard" className={linkCls}>工作台</Link>
    <Link href="/knowledge" className={linkCls}>📇 知识库</Link>
    <Link href="/discover" className={linkCls}>🔍 发现</Link>
    <Link href="/matches" className={linkCls}>🤝 撮合</Link>
    <Link href="/orders" className={linkCls}>📦 交易</Link>
    <Link href="/wallet" className={linkCls}>💰 钱包</Link>
    {me?.isAdmin && (
      <Link href="/admin/dashboard" className={linkCls}>🛡️ 后台</Link>
    )}
    <a href="#" onClick={(e) => { e.preventDefault(); logout(); }} className={linkCls}>退出</a>
  </>
);
```

- [ ] **Step 3: 改 mobileLinks 同步**

文件 `app/_components/TopBar.tsx`, 替换 `mobileLinks` JSX 块:

```tsx
const mobileLinks = (
  <>
    <Link href="/dashboard" className="block px-4 py-3 text-gray-800 hover:bg-gray-100 border-b border-gray-100">工作台</Link>
    <Link href="/knowledge" className="block px-4 py-3 text-gray-800 hover:bg-gray-100 border-b border-gray-100">📇 知识库</Link>
    <Link href="/discover" className="block px-4 py-3 text-gray-800 hover:bg-gray-100 border-b border-gray-100">🔍 发现</Link>
    <Link href="/matches" className="block px-4 py-3 text-gray-800 hover:bg-gray-100 border-b border-gray-100">🤝 撮合</Link>
    <Link href="/orders" className="block px-4 py-3 text-gray-800 hover:bg-gray-100 border-b border-gray-100">📦 交易</Link>
    <Link href="/wallet" className="block px-4 py-3 text-gray-800 hover:bg-gray-100 border-b border-gray-100">💰 钱包</Link>
    {me?.isAdmin && (
      <Link href="/admin/dashboard" className="block px-4 py-3 text-primary-600 font-semibold hover:bg-primary-50 border-b border-gray-100">🛡️ 后台</Link>
    )}
    <a
      href="#"
      onClick={(e) => { e.preventDefault(); logout(); }}
      className="block px-4 py-3 text-red-600 hover:bg-red-50"
    >
      退出
    </a>
  </>
);
```

- [ ] **Step 4: 新建 /wallet 占位页 (TopBar 链接不空)**

文件 `app/wallet/page.tsx`:

```tsx
"use client";
import { useEffect, useState } from "react";
import TopBar from "../_components/TopBar";

export default function WalletPage() {
  const [mounted, setMounted] = useState(false);
  useEffect(() => { setMounted(true); }, []);
  if (!mounted) return <main style={{ minHeight: "100vh", background: "linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%)" }}><TopBar current="wallet" /><div style={{ color: "white", padding: 24 }}>加载中...</div></main>;
  return (
    <main style={{ minHeight: "100vh", background: "linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%)" }}>
      <TopBar current="wallet" />
      <div style={{ maxWidth: 800, margin: "0 auto", padding: 24 }}>
        <h1 style={{ color: "white", fontSize: 24 }}>💰 钱包</h1>
        <p style={{ color: "rgba(255,255,255,0.85)", fontSize: 13, marginBottom: 16 }}>收入/支出/提现 (阶段 7 实装, 当前占位)</p>
        <div style={{ background: "white", borderRadius: 12, padding: 48, textAlign: "center" }}>
          <div style={{ fontSize: 48, marginBottom: 12 }}>💰</div>
          <div style={{ color: "#6b7280" }}>暂无流水</div>
        </div>
      </div>
    </main>
  );
}
```

- [ ] **Step 5: Build 验证**

```bash
cd opphub-web && npm run build 2>&1 | tail -30
```

预期: 路由包括 `/knowledge`, `/knowledge/profile`, `/knowledge/[id]`, `/discover`, `/matches`, `/wallet`, 加上所有旧的 `/match`, `/demands`, `/marketplace`, `/me/capabilities`, `/opc/profile` 仍编译 (用于 redirect 命中)

- [ ] **Step 6: Commit**

```bash
cd opphub-web
git add app/_components/TopBar.tsx app/wallet
git commit -m "feat(nav): TopBar 改 6 个一级 + 加 /wallet 占位 (阶段 1)"
```

---

## Task 6: 浏览器手测 + 全路径 301 校验

**Files:**
- (本地浏览器, 不写代码)

- [ ] **Step 1: 本地启动 dev**

```bash
cd opphub-web && npm run build && (npm start &) && sleep 8 && echo "started"
```

预期: 服务起在 :3000

- [ ] **Step 2: 试访问旧路径**

```bash
for p in /me/capabilities /opc/profile /marketplace /demands /match; do
  echo "=== $p ==="
  curl -s -o /dev/null -w "%{http_code} %{redirect_url}\n" "http://localhost:3000$p"
done
```

预期: 全部 `301` 加新 location (`/knowledge` `/knowledge/profile` `/discover?role=seller` `/discover?role=buyer` `/matches`)

- [ ] **Step 3: 试新路径编译能 GET**

```bash
for p in /knowledge /discover /matches /wallet /knowledge/profile /knowledge/foo; do
  echo "=== $p ==="
  curl -s -o /dev/null -w "%{http_code}\n" "http://localhost:3000$p"
done
```

预期: 全部 `200` (Next.js 即使 id 不存在也是 200, 内容里显示 fallback)

- [ ] **Step 4: 视觉校验 (人工浏览器)**

打开浏览器, 在 `/knowledge` 看 Tab 切换 + EmptyState 渲染 OK

## Task 7: 部署 ECS + 全站验证

**Files:**
- 同步到 ECS: `next.config.js`, `app/knowledge/*`, `app/discover/*`, `app/matches/*`, `app/_components/TopBar.tsx`, `app/wallet/*`

- [ ] **Step 1: scp 文件到 ECS**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev
scp opphub-web/next.config.js opphub-ecs:/opt/1panel/www/opphub-web/next.config.js
scp -r opphub-web/app/knowledge opphub-ecs:/opt/1panel/www/opphub-web/app/
scp -r opphub-web/app/discover opphub-ecs:/opt/1panel/www/opphub-web/app/
scp -r opphub-web/app/matches opphub-ecs:/opt/1panel/www/opphub-web/app/
scp -r opphub-web/app/wallet opphub-ecs:/opt/1panel/www/opphub-web/app/
scp opphub-web/app/_components/TopBar.tsx opphub-ecs:/opt/1panel/www/opphub-web/app/_components/TopBar.tsx
```

- [ ] **Step 2: 容器内 build + 重启**

```bash
ssh opphub-ecs "docker exec opphub-web sh -c 'cd /app && npm run build 2>&1 | tail -5 && docker restart opphub-web'"
```

注: 第二段 `docker restart` 实际是宿主命令, 不是容器内, 需要拆开:

```bash
ssh opphub-ecs "docker exec opphub-web sh -c 'cd /app && npm run build 2>&1 | tail -5'"
ssh opphub-ecs "docker restart opphub-web"
```

- [ ] **Step 3: 验证 ECS 跳转**

```bash
ssh opphub-ecs 'for p in /me/capabilities /opc/profile /marketplace /demands /match; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:3000$p")
  loc=$(curl -s -o /dev/null -w "%{redirect_url}" "http://localhost:3000$p")
  echo "$p -> $code $loc"
done'
```

预期: 每个输出 `301` 后是新路径

- [ ] **Step 4: 浏览器访问生产 URL `https://opphub.aiforce.cloud` 检查 TopBar**

人工: 看顶导航 6 个, 点各 tab, 旧路径进入后跳新路径

- [ ] **Step 5: Commit (若是单独的 "deploy" commit)**

```bash
cd opphub-web
git tag phase-1-nav-r2c
git log --oneline -5
```

(无需 commit, tag 也行, 主要给个里程碑标记)

---

## 完成判定

- [ ] Task 1: redirects 加好, 旧路径 301 → 新路径 (curl 校验)
- [ ] Task 2: `/knowledge` Tab 化 4 种角色, EmptyState 显示中文
- [ ] Task 3: `/discover` 双视角切换 OK
- [ ] Task 4: `/matches` 复刻 `/match` 内容
- [ ] Task 5: TopBar 6 个入口, 新 `/wallet` 占位
- [ ] Task 6: 本地构建 + curl + 浏览器手测通过
- [ ] Task 7: ECS build + 容器重启, 旧路径 301 在生产环境也对

最终产品现象: 用户打开 opphub.aiforce.cloud/dashboard → 顶部看到 6 个一级: 工作台 / 📇知识库 / 🔍发现 / 🤝撮合 / 📦交易 / 💰钱包; 点老链接自动跳

## 后续阶段 (不在此 plan 范围)

- 阶段 2: 知识库语义 + entryDimension 枚举 + 录入三选一
- 阶段 3: 撮合流转 (matchings/inquiries/bids 表 + `/matches/[id]` + 手动撮合池)
- 阶段 4: 订单状态机 + 支付 (orders 表 + `/orders/[id]` + 状态按钮)
- 阶段 5: 推送 + Onboarding (opphub-ws 对接 + onboarding 4 屏 + 录入正反馈)
- 阶段 6: 错误兜底 + 5 状态规范
- 阶段 7: 钱包 + 设置 (含提现/充值实际流程)

每个阶段单独走 spec → plan → implement 循环。
