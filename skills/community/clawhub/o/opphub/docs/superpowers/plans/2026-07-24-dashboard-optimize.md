# Dashboard 任务流首页优化 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 `opphub-web/app/dashboard/page.tsx` 从"统计 + 消息 + 入口平铺"重构为"任务流驱动"首页,修复统计卡字段错配 bug,新增"今日撮合"模块,导航与 IA 不动

**Architecture:** 单客户端组件 (`page.tsx`) + 3 个新子组件 (`MessageCard` / `MatchCard` / `EmptyState`)。保留 SSR 骨架防 hydration mismatch,客户端 `useEffect` 并行拉 4 个 API。所有数据接口复用已有端点,零后端改动。

**Tech Stack:** Next.js 14 (app router) + TypeScript + React 18 + inline style (不引入新依赖)

**Spec:** `docs/superpowers/specs/2026-07-24-opphub-dashboard-optimize-design.md`

**Test Note:** opphub-web 当前**无单元测试框架** (无 vitest/jest/playwright 配置, `package.json` 无 `test` script)。本计划**不引入测试框架** (YAGNI + 尊重 codebase 现状)。每个 Task 的 verification 步骤用 `pnpm build` + 浏览器手动确认 + curl API 响应替代。

---

## 总体任务地图

```
Task 1: 抽 MessageCard 组件
Task 2: 抽 EmptyState 组件
Task 3: 新 MatchCard 组件
Task 4: 加 match/today API + 修字段错配
Task 5: 重组 dashboard 布局 (任务流置顶 + 砍入口 + 改骨架)
Task 6: 整体验证 (pnpm build + dev + 浏览器)
Task 7: ECS 部署 (等舟哥授权)
```

---

## Task 1: 抽 MessageCard 组件

**Files:**
- Create: `opphub-web/app/dashboard/components/MessageCard.tsx`
- Modify: `opphub-web/app/dashboard/page.tsx:186-211`

- [ ] **Step 1: 创建 `components/` 目录**

```bash
mkdir -p /Users/qiuxz/.openclaw/workspace-dev/opphub-web/app/dashboard/components
```

- [ ] **Step 2: 写 `MessageCard.tsx`**

文件路径: `/Users/qiuxz/.openclaw/workspace-dev/opphub-web/app/dashboard/components/MessageCard.tsx`

```tsx
"use client";
import { useState } from "react";

export type MessageItem = {
  id: string;
  type: string;
  createdAt: string;
  title?: string;
  desc?: string;
  text?: string;
  payload?: { title?: string; desc?: string } | null;
};

function relativeTime(iso: string): string {
  const diff = Date.now() - new Date(iso).getTime();
  const min = Math.floor(diff / 60000);
  if (min < 1) return "刚刚";
  if (min < 60) return `${min} 分钟前`;
  const hr = Math.floor(min / 60);
  if (hr < 24) return `${hr} 小时前`;
  const day = Math.floor(hr / 24);
  return `${day} 天前`;
}

const itemStyle: React.CSSProperties = {
  display: "flex",
  gap: 12,
  padding: 12,
  borderRadius: 8,
  marginBottom: 8,
  background: "#f9fafb",
  cursor: "pointer",
  transition: "all .15s",
};
const ackedStyle: React.CSSProperties = { opacity: 0.5 };
const titleStyle: React.CSSProperties = { fontSize: 14, color: "#1f2937", fontWeight: 500, marginBottom: 4 };
const descStyle: React.CSSProperties = {
  fontSize: 12,
  color: "#6b7280",
  lineHeight: 1.5,
  overflow: "hidden",
  textOverflow: "ellipsis",
  whiteSpace: "nowrap",
};
const timeStyle: React.CSSProperties = { fontSize: 11, color: "#9ca3af", flexShrink: 0 };
const ctaStyle: React.CSSProperties = {
  fontSize: 12,
  color: "#4f46e5",
  fontWeight: 500,
  flexShrink: 0,
  alignSelf: "center",
};

export default function MessageCard({
  msg,
  acked,
  onAck,
  apiBase,
  token,
}: {
  msg: MessageItem;
  acked: boolean;
  onAck: (id: string) => void;
  apiBase: string;
  token: string;
}) {
  const [busy, setBusy] = useState(false);
  const icon = msg.type === "opportunity" ? "🎯" : msg.type === "system" ? "⚙️" : "⭐";
  const title = msg.title || msg.payload?.title || msg.type;
  const desc = msg.desc || msg.text || msg.payload?.desc || "";
  const focusId = encodeURIComponent(msg.id);

  async function handleClick() {
    if (acked || busy) return;
    setBusy(true);
    try {
      await fetch(apiBase + "/api/opc/messages/ack", {
        method: "POST",
        headers: { "content-type": "application/json", authorization: "Bearer " + token },
        body: JSON.stringify({ messageId: msg.id }),
      });
    } catch (e) {
      console.error("ack failed", e);
    } finally {
      setBusy(false);
      onAck(msg.id);
    }
  }

  return (
    <div
      onClick={handleClick}
      style={{ ...itemStyle, ...(acked ? ackedStyle : null) }}
      data-testid={`msg-${msg.id}`}
    >
      <div style={{ fontSize: 24, flexShrink: 0 }}>{icon}</div>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={titleStyle}>{title}</div>
        <div style={descStyle}>{desc}</div>
      </div>
      <div style={timeStyle}>{relativeTime(msg.createdAt)}</div>
      <a
        href={`/messages?focus=${focusId}`}
        onClick={(e) => e.stopPropagation()}
        style={ctaStyle}
      >
        处理 →
      </a>
    </div>
  );
}
```

- [ ] **Step 3: 改 `page.tsx` 替换内联消息渲染**

替换 `opphub-web/app/dashboard/page.tsx` 第 186-211 行 (整个 `msgs.map((m) => { ... })` 块) 为:

```tsx
import MessageCard, { MessageItem } from "./components/MessageCard";
```

(顶部 import 区域追加这一行,跟现有 `import TopBar from "../_components/TopBar";` 相邻)

第 184 行 `{msgs.length === 0 ? (...)` 内部 empty 块**保留不变**,第 187-211 行的 map 块改为:

```tsx
msgs.map((m) => (
  <MessageCard
    key={m.id}
    msg={m as MessageItem}
    acked={acked.has(m.id)}
    onAck={(id) => setAcked((prev) => new Set(prev).add(id))}
    apiBase={apiBase}
    token={localStorage.getItem("opphubToken") || ""}
  />
))
```

并删除原 `ackMessage` 函数 (第 115-127 行),因为 ack 逻辑已搬进 `MessageCard`。

- [ ] **Step 4: 验证编译**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-web && pnpm build 2>&1 | tail -30
```

Expected: build 成功,无 TypeScript 错误,无 hydration warning,产出 `.next/` 包含新组件 chunk

- [ ] **Step 5: Commit**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-web && \
git add app/dashboard/components/MessageCard.tsx app/dashboard/page.tsx && \
git commit -m "refactor(dashboard): 抽 MessageCard 组件, 加相对时间 + 跳转链接"
```

---

## Task 2: 抽 EmptyState 组件

**Files:**
- Create: `opphub-web/app/dashboard/components/EmptyState.tsx`
- Modify: `opphub-web/app/dashboard/page.tsx` (用新组件替换消息空状态行)

- [ ] **Step 1: 写 `EmptyState.tsx`**

文件路径: `/Users/qiuxz/.openclaw/workspace-dev/opphub-web/app/dashboard/components/EmptyState.tsx`

```tsx
"use client";
import Link from "next/link";

const wrapStyle: React.CSSProperties = {
  textAlign: "center",
  padding: "24px 16px",
  color: "#9ca3af",
  fontSize: 13,
  lineHeight: 1.6,
};
const ctaStyle: React.CSSProperties = {
  display: "inline-block",
  marginTop: 8,
  padding: "6px 12px",
  background: "#eef2ff",
  color: "#4f46e5",
  borderRadius: 6,
  textDecoration: "none",
  fontSize: 12,
  fontWeight: 500,
};

export default function EmptyState({
  icon,
  text,
  ctaLabel,
  ctaHref,
}: {
  icon?: string;
  text: string;
  ctaLabel?: string;
  ctaHref?: string;
}) {
  return (
    <div style={wrapStyle} data-testid="empty-state">
      <div style={{ fontSize: 32, marginBottom: 8 }}>{icon ?? "📭"}</div>
      <div>{text}</div>
      {ctaLabel && ctaHref && (
        <Link href={ctaHref} style={ctaStyle}>
          {ctaLabel} →
        </Link>
      )}
    </div>
  );
}
```

- [ ] **Step 2: 改 `page.tsx` 替换消息空状态**

`page.tsx` 顶部 import 区域追加:

```tsx
import EmptyState from "./components/EmptyState";
```

替换第 184-186 行 (消息空状态):

```tsx
{msgs.length === 0 ? (
  <EmptyState
    icon="📭"
    text="暂无新消息 — 完善画像让对方精准找到你"
    ctaLabel="去完善"
    ctaHref="/knowledge"
  />
) : (
```

(原 `<div style={empty}>暂无待读消息</div>` 删掉,改用 EmptyState)

- [ ] **Step 3: 验证编译**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-web && pnpm build 2>&1 | tail -30
```

Expected: build 成功

- [ ] **Step 4: Commit**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-web && \
git add app/dashboard/components/EmptyState.tsx app/dashboard/page.tsx && \
git commit -m "refactor(dashboard): 抽 EmptyState 组件 (复用 3 处空状态)"
```

---

## Task 3: 新 MatchCard 组件

**Files:**
- Create: `opphub-web/app/dashboard/components/MatchCard.tsx`
- Modify: `opphub-web/app/dashboard/page.tsx` (本次先 import,不渲染,留给 Task 5)

- [ ] **Step 1: 写 `MatchCard.tsx`**

文件路径: `/Users/qiuxz/.openclaw/workspace-dev/opphub-web/app/dashboard/components/MatchCard.tsx`

```tsx
"use client";

export type MatchItem = {
  matchingId: string;
  demandId: string;
  demandTitle: string;
  demandBudget: string;
  demandCity?: string;
  demandDeadline?: string | null;
  explainText?: string;
  createdAt: string;
  scores?: {
    semantic?: number;
    price?: number;
    time?: number;
    trust?: number;
    total?: number;
  };
};

const itemStyle: React.CSSProperties = {
  display: "flex",
  gap: 12,
  padding: 12,
  borderRadius: 8,
  marginBottom: 8,
  background: "#f9fafb",
  cursor: "pointer",
  transition: "all .15s",
};
const titleStyle: React.CSSProperties = {
  fontSize: 14,
  color: "#1f2937",
  fontWeight: 500,
  marginBottom: 4,
  overflow: "hidden",
  textOverflow: "ellipsis",
  whiteSpace: "nowrap",
};
const metaStyle: React.CSSProperties = {
  fontSize: 12,
  color: "#6b7280",
  display: "flex",
  gap: 8,
  alignItems: "center",
};
const budgetStyle: React.CSSProperties = {
  fontSize: 13,
  color: "#10b981",
  fontWeight: 600,
};
const ctaStyle: React.CSSProperties = {
  fontSize: 12,
  color: "#4f46e5",
  fontWeight: 500,
  flexShrink: 0,
  alignSelf: "center",
};

function formatBudget(budget: string): string {
  const num = Number(budget);
  if (Number.isNaN(num) || num <= 0) return "¥面议";
  return `¥${num.toLocaleString("zh-CN")}`;
}

function formatDeadline(iso: string | null | undefined): string {
  if (!iso) return "";
  const days = Math.ceil((new Date(iso).getTime() - Date.now()) / (24 * 60 * 60 * 1000));
  if (days < 0) return "已截止";
  if (days === 0) return "今天截止";
  if (days <= 7) return `${days} 天内截止`;
  const d = new Date(iso);
  return `${d.getMonth() + 1}/${d.getDate()}`;
}

export default function MatchCard({ match }: { match: MatchItem }) {
  const city = match.demandCity || "不限城市";
  const deadline = formatDeadline(match.demandDeadline);
  const focusId = encodeURIComponent(match.matchingId);
  return (
    <div style={itemStyle} data-testid={`match-${match.matchingId}`}>
      <div style={{ fontSize: 24, flexShrink: 0 }}>📋</div>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={titleStyle}>{match.demandTitle}</div>
        <div style={metaStyle}>
          <span style={budgetStyle}>{formatBudget(match.demandBudget)}</span>
          <span>·</span>
          <span>{city}</span>
          {deadline && (
            <>
              <span>·</span>
              <span>{deadline}</span>
            </>
          )}
        </div>
      </div>
      <a href={`/match?focus=${focusId}`} style={ctaStyle}>
        查看 →
      </a>
    </div>
  );
}
```

- [ ] **Step 2: 改 `page.tsx` 仅加 import**

`page.tsx` 顶部 import 区域追加:

```tsx
import MatchCard, { MatchItem } from "./components/MatchCard";
```

**不**渲染,留给 Task 5 重组布局时再用。

- [ ] **Step 3: 验证编译**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-web && pnpm build 2>&1 | tail -30
```

Expected: build 成功 (即使未使用 MatchCard,TypeScript 类型 import 不影响编译)

- [ ] **Step 4: Commit**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-web && \
git add app/dashboard/components/MatchCard.tsx app/dashboard/page.tsx && \
git commit -m "feat(dashboard): 新 MatchCard 组件 (今日撮合模块用)"
```

---

## Task 4: 加 match/today API + 修字段错配

**Files:**
- Modify: `opphub-web/app/dashboard/page.tsx` (并行 Promise.all 第 73-78 行 + state 第 50-58 行 + stats 处理逻辑第 100-108 行)

- [ ] **Step 1: 加 `match/today` state**

`page.tsx` 第 57 行后追加:

```tsx
const [matches, setMatches] = useState<MatchItem[]>([]);
```

`MatchItem` 类型由 Task 3 import 提供。

- [ ] **Step 2: 并行 fetch 加第 4 个 API**

`page.tsx` 第 73-78 行 `Promise.all([...])` 数组里追加:

```tsx
const [r1, r2, r3, r4] = await Promise.all([
  fetch(apiBase + "/api/onboarding/status", { headers }),
  fetch(apiBase + "/api/opc/messages/pending?limit=10", { headers }),
  fetch(apiBase + "/api/opc/stats", { headers }),
  fetch(apiBase + "/api/opc/match/today", { headers }),
]);
const j1: Onboarding = await r1.json();
const j2 = await r2.json();
const j3 = await r3.json();
const j4 = await r4.json();
```

第 97-108 行 `if (j2?.ok)` / `if (j3?.ok)` 块**下方**追加:

```tsx
if (j4?.ok && j4.data) {
  setMatches((j4.data || []) as MatchItem[]);
}
```

- [ ] **Step 3: 修 stats 字段错配**

第 100-108 行 (原 stats 处理逻辑) 改为:

```tsx
if (j3?.ok && j3.data) {
  setStats((s) => ({
    ...s,
    todayMatches: j3.data.todayDemands ?? j3.data.todayMatches ?? s.todayMatches,
    trustPoints: j3.data.trustPoints ?? j3.data.trustScore ?? s.trustScore,
    balance: j3.data.balance ?? s.balance,
  }));
}
```

(`pendingOrders` 字段不来自 stats,留默认 0 不渲染,Task 5 删掉这个卡)

- [ ] **Step 4: 修 `Stats` 类型**

`page.tsx` 第 12-17 行 `Stats` 类型改为:

```tsx
type Stats = {
  trustScore: number | null;
  balance: number | null;
  todayMatches: number;
};
```

(删除 `pendingOrders` 字段,因不渲染)

- [ ] **Step 5: 验证编译**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-web && pnpm build 2>&1 | tail -30
```

Expected: build 成功,`matches` state 接到 `j4.data`

- [ ] **Step 6: 验证 ECS API 响应格式**

```bash
TOKEN=$(curl -s -X POST https://api.opphub.ruiplus.cn/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"type":"email","target":"chinabot@163.com","code":"123456"}' | jq -r .opphubToken)

curl -s -H "Authorization: Bearer $TOKEN" \
  https://api.opphub.ruiplus.cn/api/opc/match/today | jq '.data | length, .data[0] // "empty"'
```

Expected: 数字 (数组长度) + 对象或 "empty"。如果没有 token (收不到验证码),预期返 401,记录下"待舟哥提供 token 验收"

- [ ] **Step 7: Commit**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-web && \
git add app/dashboard/page.tsx && \
git commit -m "feat(dashboard): 加 match/today API + 修 stats 字段错配

- 并行拉 4 个 API (新增 /api/opc/match/today)
- 修 stats.todayMatches ← j3.data.todayDemands
- 删 Stats.pendingOrders (API 缺,违反严格依赖原则)
- 删 Stats.trustScore 改用 trustPoints"
```

---

## Task 5: 重组 dashboard 布局

**Files:**
- Modify: `opphub-web/app/dashboard/page.tsx` (整个渲染块 第 146-227 行)

- [ ] **Step 1: 改 SSR 骨架为多卡占位**

`page.tsx` 第 133-144 行 (mounted=false 兜底) 改为:

```tsx
if (!mounted || authed === null) {
  return (
    <main style={wrap}>
      <TopBar current="dashboard" rightSlot={<span style={{ fontSize: 13, opacity: 0.85 }}>加载中...</span>} />
      <div className="max-w-[960px] mx-auto px-4 md:px-6 py-4 md:py-6">
        <div style={skeletonRow}>
          <div style={{ ...card, flex: 1, height: 200 }}>
            <div style={skeletonH2}>📨 新消息</div>
            <div style={skeletonLine} />
            <div style={skeletonLine} />
            <div style={skeletonLine} />
          </div>
          <div style={{ ...card, flex: 1, height: 200 }}>
            <div style={skeletonH2}>🎯 今日撮合</div>
            <div style={skeletonLine} />
            <div style={skeletonLine} />
          </div>
        </div>
      </div>
    </main>
  );
}
```

文件底部 style 区域 (第 280 行后) 追加:

```tsx
const skeletonRow: React.CSSProperties = { display: "flex", gap: 16, marginBottom: 16 };
const skeletonH2: React.CSSProperties = {
  fontSize: 16,
  color: "#d1d5db",
  margin: "0 0 16px",
  fontWeight: 500,
};
const skeletonLine: React.CSSProperties = {
  height: 12,
  background: "#f3f4f6",
  borderRadius: 6,
  marginBottom: 8,
};
```

- [ ] **Step 2: 改主渲染块顺序**

`page.tsx` 第 146-227 行整个 `<main>` 替换为:

```tsx
return (
  <main style={wrap}>
    <TopBar current="dashboard" me={{ opcId: me?.opcId, email: me?.email, phone: me?.phone, isAdmin: me?.isAdmin }} />
    <div className="max-w-[960px] mx-auto px-4 md:px-6 py-4 md:py-6">

      {/* 引导状态概览 (onboarding 未完成时) */}
      {me && !me.completed && (
        <div style={card}>
          <h2 style={cardH2}>
            📋 账号引导
            <span style={badge}>
              Step {me.currentStep ?? 1}/{me.totalSteps || 6} · 未完成
            </span>
          </h2>
          <div style={{ height: 8, background: "#e5e7eb", borderRadius: 4, overflow: "hidden" }}>
            <div style={{
              width: `${Math.min(100, ((me.currentStep ?? 0) / (me.totalSteps || 6)) * 100)}%`,
              height: 8,
              background: "linear-gradient(90deg, #4f46e5, #06b6d4)",
            }} />
          </div>
          <div style={{ marginTop: 10, fontSize: 12, color: "#6b7280", lineHeight: 1.7 }}>
            继续完善以解锁更多功能 · <Link href="/onboarding" style={{ color: "#4f46e5", textDecoration: "none" }}>继续完善 →</Link>
          </div>
        </div>
      )}

      {/* 任务流双列: 消息 + 撮合 */}
      <div style={taskRow}>
        {/* 新消息 */}
        <div style={card}>
          <h2 style={cardH2}>
            📨 新消息 <span style={badge}>{unreadCount} 条待读</span>
          </h2>
          {msgs.length === 0 ? (
            <EmptyState
              icon="📭"
              text="暂无新消息 — 完善画像让对方精准找到你"
              ctaLabel="去完善"
              ctaHref="/knowledge"
            />
          ) : (
            msgs.map((m) => (
              <MessageCard
                key={m.id}
                msg={m as MessageItem}
                acked={acked.has(m.id)}
                onAck={(id) => setAcked((prev) => new Set(prev).add(id))}
                apiBase={apiBase}
                token={localStorage.getItem("opphubToken") || ""}
              />
            ))
          )}
        </div>

        {/* 今日撮合 */}
        <div style={card}>
          <h2 style={cardH2}>
            🎯 今日撮合 <span style={badge}>{matches.length} 条</span>
          </h2>
          {matches.length === 0 ? (
            <EmptyState
              icon="🔍"
              text="今日无匹配 — 去发现页看看热门需求"
              ctaLabel="去看看"
              ctaHref="/discover"
            />
          ) : (
            matches.map((m) => <MatchCard key={m.matchingId} match={m} />)
          )}
        </div>
      </div>

      {/* 信任分 + 今日撮合 (简版,横向窄条) */}
      <div style={card}>
        <div style={statsRow}>
          <Stat label="信任分 (余额)" value={stats.trustScore != null ? `¥${stats.trustScore}` : "--"} valueStyle={moneyVal} />
          <Stat label="今日发需求" value={stats.todayMatches} valueStyle={countVal} />
        </div>
      </div>

      {/* 快速入口: 3 个 (任务流相关) */}
      <div style={card}>
        <h2 style={cardH2}>🚀 快速入口</h2>
        <div style={nav}>
          <Link href="/discover" style={navLink}>🔍 发现</Link>
          <Link href="/match" style={navLink}>🤝 撮合</Link>
          <Link href="/orders" style={navLink}>📦 交易</Link>
        </div>
      </div>
    </div>

    <style>{`
      @media (max-width: 767px) {
        [data-task-row] { flex-direction: column !important; }
      }
    `}</style>
  </main>
);
```

- [ ] **Step 3: 改 grid + 加 statsRow + 删 pendingOrders**

文件底部 style 区域 (第 280 行附近) 把 `grid` 改为:

```tsx
const taskRow: React.CSSProperties = { display: "flex", gap: 16, marginBottom: 16, flexWrap: "wrap" };
const statsRow: React.CSSProperties = { display: "flex", gap: 24, flexWrap: "wrap" };
```

(`grid` 变量不再使用,**删除原第 250-255 行 `grid` style**)

- [ ] **Step 4: 验证编译 + lint**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-web && pnpm build 2>&1 | tail -30 && pnpm lint 2>&1 | tail -20
```

Expected: build 成功 + lint 无 error

- [ ] **Step 5: Commit**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-web && \
git add app/dashboard/page.tsx && \
git commit -m "feat(dashboard): 任务流驱动布局 (消息+撮合置顶)

- 双列任务流 (消息 + 撮合) 置顶
- 统计简版: 信任分 + 今日发需求 (2 卡, 不再永远 0)
- 快速入口砍到 3 个 (跟 nav 不重复)
- 引导卡保留 (onboarding 未完成时)
- SSR 骨架: 单 ⏳ → 4 个卡占位
- 移动端用 CSS media query (不用 window.innerWidth 防 hydration)"
```

---

## Task 6: 整体验证 (本地)

- [ ] **Step 1: 起 dev server**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-web && pnpm dev &
DEV_PID=$!
sleep 8
echo "dev started pid=$DEV_PID"
```

Expected: 终端输出 "Ready in Xms" + "Local: http://localhost:3000"

- [ ] **Step 2: 浏览器手测 dashboard**

访问 `http://localhost:3000/dashboard`,确认:

- [ ] 顶部 nav 6 个一级导航不变 (舟哥红线)
- [ ] 任务流双列: 📨 新消息 在左,🎯 今日撮合 在右
- [ ] 每条消息卡: icon + 标题 + 摘要 + 相对时间 + "处理 →" 链接
- [ ] 每条撮合卡: 📋 + 标题 + ¥预算(绿) + 城市 + 截止 + "查看 →" 链接
- [ ] 空状态: 0 消息显 "暂无新消息 — 去完善 →", 0 撮合显 "今日无匹配 — 去看看 →"
- [ ] 引导卡 (如未完成 onboarding) 在最顶部
- [ ] 信任分 + 今日发需求 显示真实值 (不再是 -- 或 0)
- [ ] 快速入口只有 3 个: 发现 / 撮合 / 交易
- [ ] 移动端 (< 768px): 双列变单列

- [ ] **Step 3: 测跳转**

- 点消息"处理 →" → 跳 `/messages?focus=xxx`
- 点撮合"查看 →" → 跳 `/match?focus=xxx`
- 点引导卡"继续完善 →" → 跳 `/onboarding`
- 点空状态 CTA → 跳 `/knowledge` 或 `/discover`
- 点快速入口 → 跳对应 nav 页

- [ ] **Step 4: 测 API 失败降级**

浏览器 DevTools 模拟: 断开网络 → refresh `/dashboard`

- [ ] 4 个 API 都失败: 4 个卡都显内联"加载失败"或骨架态,不白屏
- [ ] 任一 API 失败: 对应卡显错,其他卡正常
- [ ] 401: 自动跳 `/login`

- [ ] **Step 5: 停 dev server**

```bash
kill $DEV_PID 2>/dev/null || true
```

- [ ] **Step 6: Commit (如有手测改动)**

如有手测发现的微调 (文案 / 颜色 / 间距):

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-web && \
git add app/dashboard/ && \
git commit -m "fix(dashboard): 手测微调 (文案/颜色/间距)"
```

(无改动则跳过)

---

## Task 7: ECS 部署 (等舟哥授权)

**背景**: MEMORY.md §1.3 红线 + SOUL.md "发到 skillhub / clawhub / 服务器 需要授权"。本 Task 不自动执行,等舟哥拍。

**Files:**
- `opphub-web/app/dashboard/page.tsx` + `opphub-web/app/dashboard/components/` (5 个 commit 已本地提交)

**Deploy 流程** (舟哥授权后执行,严格 4 步走):

- [ ] **Step 1: 同步本地 commit 到 ECS**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-web && \
git push origin main
```

(MEMORY.md §1.3: "本地改仓 → push github 不用授权")

- [ ] **Step 2: 拉 ECS 最新代码 + 编译**

按 MEMORY.md §1.1 红线 ECS opphub-web 容器运维规范 (7/20 12:07 拍), 4 步连做:

```bash
ssh opphub-ecs "cd /opt/1panel/www/opphub-web && git pull && \
  docker restart opphub-web"
```

(MEMORY.md §1.3: "改 Next.js 代码 = npm run build + docker restart opphub-web")

- [ ] **Step 3: 等编译 60s + 3 行 log 验证**

```bash
ssh opphub-ecs 'sleep 60 && \
  docker logs opphub-web --tail 100 | grep -E "build exit=0|server ready|embedding-worker"'
```

Expected: 3 行齐全 (缺 1 行 = 有问题, 不要反复 restart, 先看 build.log)

- [ ] **Step 4: ECS 上 curl dashboard**

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://api.opphub.ruiplus.cn/dashboard
```

Expected: `200`

- [ ] **Step 5: ECS 上浏览器手测**

访问 `https://api.opphub.ruiplus.cn/dashboard`, 重复 Task 6 Step 2-4 的检查项

- [ ] **Step 6: 通知舟哥 deploy 完成**

发飞书 DM: "dashboard 任务流首页已 deploy ECS, 5 个 commit 范围 {commit-hash-range}, 已手测通过, 可验收"

---

## 自审 (Plan vs Spec 覆盖检查)

| Spec 章节 | Plan Task 覆盖 |
|---|---|
| §0 现状 + 问题 | ✅ Task 4 Step 3 (修字段错配) |
| §1.1 改文件清单 | ✅ Task 1-3 创建 3 组件 + Task 5 改 page.tsx |
| §1.2 不改什么 | ✅ Plan 整体不动 nav/IA/其他页面/API |
| §2 新布局 | ✅ Task 5 Step 2 |
| §3.1 MessageCard | ✅ Task 1 Step 2 |
| §3.2 MatchCard | ✅ Task 3 Step 1 |
| §3.3 EmptyState | ✅ Task 2 Step 1 |
| §3.4 统计卡修复 | ✅ Task 4 Step 3-4 |
| §4.1 并行 4 API | ✅ Task 4 Step 2 |
| §4.2 错误处理 | ⏸️ 现有代码有 try/catch, Task 5 Step 2 渲染时不区分错/空 (后续可加) |
| §4.3 SSR 骨架 | ✅ Task 5 Step 1 |
| §5.1 视觉规范 | ✅ 全部用现有 inline style |
| §5.2 不引入新依赖 | ✅ Plan 不引入测试/CSS 框架 |
| §5.3 SSR 骨架优化 | ✅ Task 5 Step 1 |
| §6 文件改动清单 | ✅ Task 1-5 完整覆盖 |
| §7 测试 | ⏸️ 替代为 Task 6 验证 (项目无测试框架,尊重现状) |
| §8 风险 | ⏸️ Task 7 deploy 后由舟哥决定 |
| §9 不做的事 | ✅ Plan 整体不动 |
| §10 验收标准 | ✅ Task 6 Step 2 浏览器手测 checklist |

**Gap:**
- §4.2 错误处理 (内联 [重试] 按钮) **未在 Plan 体现** — 当前 try/catch 只 console.warn,不渲染错误 UI。是否需要加? 见 Task 6 Step 4 测失败降级,降级到骨架已满足"不白屏"。
- §7 测试: 项目无测试框架,Plan 用 Task 6 端到端手测替代,理由明确。

---

## 关键风险与回滚

| 风险 | 缓解 | 回滚 |
|---|---|---|
| 字段修复后旧 dashboard 视觉变化大 | Task 5 Step 4 build + Task 6 Step 2 浏览器手测 | `git revert <last-commit>` |
| 移动端 media query 在 Next.js SSR 失效 | `<style>` 块 + `[data-task-row]` attribute selector (Task 5 Step 2) | 改回 inline style (desktop only) |
| ECS 无 seed 数据 → 全空状态 | EmptyState 文案已设计闭环 | - |
| 单次 scp + restart 编译失败 | 按 MEMORY.md §1.3 红线 4 步连做,不反复 restart | 改回最近稳定 commit |
| Task 7 ECS deploy 撞 7/20 12:07 钉的运维坑 | 严格 4 步 + 3 行 log 验证 | - |

---

## 不做的事 (反复钉的纪律)

- ❌ 不动 nav / IA / 其他页面
- ❌ 不补后端 API
- ❌ 不引入 vitest/jest/playwright (项目无测试框架,YAGNI)
- ❌ 不引入 CSS module / Tailwind 重写
- ❌ 不做 IA 重构 (舟哥"为什么要动,现在不是挺好的么")
- ❌ 不动 SSR 兜底逻辑 (防 hydration mismatch,只优化视觉)
- ❌ 不加 mock 数据 (违反 7/24 教训"不显示层过滤数据")
- ❌ 不自动 ECS deploy (等舟哥拍,SOUL.md 红线)

---

## 关联文档

- Spec: `docs/superpowers/specs/2026-07-24-opphub-dashboard-optimize-design.md`
- 7/21 演练: `memory/2026-07-21-opphub-web-flow-test.md` (API 实装状态)
- MEMORY.md §1.1 opphub-web 容器运维 (7/20 12:07 红线)
- MEMORY.md §1.3 ECS 代码改动 3 步必查