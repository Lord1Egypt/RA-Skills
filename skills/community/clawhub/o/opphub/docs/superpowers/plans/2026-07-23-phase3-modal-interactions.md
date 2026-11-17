# OppHub 阶段 3 修订版：「我的卡片」全部交互 + /discover 改读知识库

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 「我的卡片」页所有交互弹窗化 (详情/编辑/删除/历史) 主页不动; tab 修复使「我在找」「同行关系」可点; /discover 改读知识库; 安装文档链接换 ClawHub.

**Architecture:** 仅动 opphub-web 前端, 不改 server, 不改 skill. 弹窗用本地 React state 控制开合. /discover 切换到调 `/api/knowledge?opcId=me&entryType=...&visibility=PUBLIC` (虽然当前 server 没有 visibility=PUBLIC 过滤, 暂用 opcId=me 拉自己的 entry 看 effect, 真正 public 切换留作未来 server 任务)

**Tech Stack:** Next.js 14, React, 本地 state modal, fetch

## TopBar 顺序 (已落地, 不可动)

```
工作台 / 🔍 发现 / 🤝 撮合 / 📦 交易 / 💰 钱包 / 🪪 我的卡片 / 🛡️ 后台 / 退出
```

「我的卡片」在 💰 钱包 和 🛡️ 后台 之间. 任何新增 nav 项必须保持这个顺序.

---

## 0. 关键边界 (钉死)

- **「我的卡片」 = `/knowledge` 路径不变, 名字/TopBar 改**: 已 commit (`1ffbcb8` + `630367f`)
- **TopBar 顺序已定**: 工作台 / 发现 / 撮合 / 交易 / 钱包 / 我的卡片 / 后台 / 退出 (新加的 nav 项必须保持)
- **弹窗化**: 详情/编辑/删除/历史 全部 React state modal, 不再跳 `/knowledge/[id]` (那页面可以删, 或者留作 SEO 兜底)
- **`/discover` 改读知识库**: 不再调 marketplace/demands 表, 调 `/api/knowledge?opcId=me` 按 entryType 过滤
- **ClawHub 链接**: `https://clawhub.ai/mtty-ai/skills/opphub` (Quick fix, 这次一并改)
- **tab 修复**: 「我在找」「同行关系」实际是能点, 可能是「我现在没数据」看着像坏. 修复: 优化空状态展示, 让用户知道这 tab 是好的, 只是没数据

---

## 1. 任务地图 (7 个)

```
Task 0: Quick fix - ClawHub 链接替换 (独立, 立刻可做)
Task 1: 「我的卡片」详情 modal 弹窗 (替代跳转)
Task 2: 「我的卡片」编辑 modal 弹窗 (复用 PATCH /api/knowledge/[id])
Task 3: 「我的卡片」删除 modal 确认 + 弹窗
Task 4: 「我的卡片」历史版本 modal 弹窗 (复用 GET /api/knowledge/[id]/history)
Task 5: /discover 改读 /api/knowledge (按 entryType 过滤, 按 companyName 分组)
Task 6: 部署 ECS + 终验
```

---

## Task 0: Quick fix - ClawHub 链接替换

**Files:**
- Modify: `opphub-web/app/knowledge/page.tsx`

- [ ] **Step 1: sed 替换链接**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-web
sed -i 's|https://github.com/mtty-ai/opphub-skill|https://clawhub.ai/mtty-ai/skills/opphub|g' app/knowledge/page.tsx
grep "安装文档" app/knowledge/page.tsx
```

预期: grep 出 "安装文档" 那一行的 href 已经是 clawhub.ai

- [ ] **Step 2: Commit**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-web
git add app/knowledge/page.tsx
git commit -m "fix(ui): 安装文档链接改 ClawHub"
```

---

## Task 1: 「我的卡片」详情 modal 弹窗

**Files:**
- Modify: `opphub-web/app/knowledge/page.tsx`

- [ ] **Step 1: 加 detailModal state + 渲染**

文件 `opphub-web/app/knowledge/page.tsx`, 在 component 内部 (大约 `const [entries, setEntries] = ...` 附近) 加:

```tsx
const [detailModal, setDetailModal] = useState<EntryShape | null>(null);
```

并在 `EntryCard` 上, 把 `<a href=...>` 跳转改成 button 弹 modal:

(找到 `function EntryCard` 那个组件, 把 `<a href={...}>` 替换成 `<button onClick=...>`)

```tsx
function EntryCard({ entry, onClick }: { entry: EntryShape; onClick: () => void }) {
  const preview = entry.rawText.slice(0, 200);
  return (
    <button
      onClick={onClick}
      style={{
        background: "white",
        borderRadius: 12,
        padding: 16,
        cursor: "pointer",
        textAlign: "left",
        width: "100%",
        border: "none",
      }}
    >
      <div style={{ fontSize: 16, fontWeight: 600, color: "#1f2937", marginBottom: 6 }}>{entry.entryDimension ?? "未命名"}</div>
      <div style={{ fontSize: 13, color: "#4b5563", lineHeight: 1.6, marginBottom: 6, whiteSpace: "pre-wrap" }}>{preview}{entry.rawText.length > 200 ? "..." : ""}</div>
      <div style={{ fontSize: 11, color: "#9ca3af" }}>更新: {new Date(entry.updatedAt).toLocaleString("zh-CN")}</div>
    </button>
  );
}
```

并修改 `g.entries.map((e) => <EntryCard key={e.id} entry={e} />)` →

```tsx
{g.entries.map((e) => (
  <EntryCard key={e.id} entry={e} onClick={() => setDetailModal(e)} />
))}
```

- [ ] **Step 2: 加 DetailModal 组件 (在 EntryCard 之后定义)**

```tsx
function DetailModal({ entry, onClose, onEdit, onDelete, onHistory }: {
  entry: EntryShape;
  onClose: () => void;
  onEdit: () => void;
  onDelete: () => void;
  onHistory: () => void;
}) {
  return (
    <div style={modalMask} onClick={onClose}>
      <div style={modalCard} onClick={(e) => e.stopPropagation()}>
        <div style={modalHead}>
          <div>
            <div style={{ fontSize: 12, color: "#9ca3af" }}>{entry.entryType ?? "—"}</div>
            <div style={{ fontSize: 18, fontWeight: 600, color: "#1f2937" }}>{entry.entryDimension ?? "未命名"}</div>
          </div>
          <button onClick={onClose} style={modalClose}>×</button>
        </div>
        <pre style={rawTextBlock}>{entry.rawText}</pre>
        <div style={modalFoot}>
          <button onClick={onEdit} style={linkBtn}>编辑</button>
          <button onClick={onHistory} style={histBtn}>📜 历史</button>
          <button onClick={onDelete} style={deleteBtn}>删除</button>
        </div>
      </div>
    </div>
  );
}
```

(在 component 末尾, 在 EntryCard 函数后面定义)

- [ ] **Step 3: 加 modal styles (在文件底部 styles 段)**

在文件底部 styles 段 (例如 modalMask / modalCard / modalHead / modalClose / modalFoot / rawTextBlock / linkBtn / histBtn / deleteBtn 附近) 加:

```tsx
const modalMask: React.CSSProperties = {
  position: "fixed", inset: 0,
  background: "rgba(0,0,0,0.5)",
  display: "flex", alignItems: "center", justifyContent: "center",
  zIndex: 999, padding: 16,
};
const modalCard: React.CSSProperties = {
  background: "white", borderRadius: 12,
  width: "100%", maxWidth: 640, maxHeight: "85vh",
  display: "flex", flexDirection: "column",
  boxShadow: "0 20px 60px rgba(0,0,0,0.3)",
};
const modalHead: React.CSSProperties = {
  padding: 16, borderBottom: "1px solid #e5e7eb",
  display: "flex", justifyContent: "space-between", alignItems: "flex-start",
};
const modalClose: React.CSSProperties = {
  background: "transparent", border: "none", fontSize: 24,
  color: "#6b7280", cursor: "pointer", lineHeight: 1,
};
const modalFoot: React.CSSProperties = {
  padding: 12, borderTop: "1px solid #e5e7eb",
  display: "flex", gap: 8, justifyContent: "flex-end",
};
const rawTextBlock: React.CSSProperties = {
  padding: 16, margin: 0, flex: 1, overflow: "auto",
  fontSize: 13, lineHeight: 1.7, color: "#374151",
  whiteSpace: "pre-wrap", wordBreak: "break-word",
  fontFamily: 'ui-monospace, "SF Mono", Menlo, monospace',
};
const linkBtn: React.CSSProperties = {
  padding: "6px 14px", background: "#4f46e5", color: "white",
  border: "none", borderRadius: 6, fontSize: 13, cursor: "pointer",
};
const histBtn: React.CSSProperties = {
  padding: "6px 14px", background: "#eef2ff", color: "#4f46e5",
  border: "1px solid #c7d2fe", borderRadius: 6, fontSize: 13, cursor: "pointer",
};
const deleteBtn: React.CSSProperties = {
  padding: "6px 14px", background: "#fef2f2", color: "#dc2626",
  border: "1px solid #fca5a5", borderRadius: 6, fontSize: 13, cursor: "pointer",
};
```

- [ ] **Step 4: 渲染 DetailModal**

在 `KnowledgePage` JSX 末尾, `</div>` 后, `</main>` 前加:

```tsx
{detailModal && (
  <DetailModal
    entry={detailModal}
    onClose={() => setDetailModal(null)}
    onEdit={() => { setEditModal(detailModal); setDetailModal(null); }}
    onDelete={() => { setDeleteModal(detailModal); setDetailModal(null); }}
    onHistory={() => { setHistoryModal(detailModal.id); setDetailModal(null); }}
  />
)}
```

(Tasks 2-4 会实现 edit/delete/history modal 的 setXxxModal state, 先把 setEditModal / setDeleteModal / setHistoryModal state 加上, 即使 Tasks 2-4 才用)

- [ ] **Step 5: 预先加 editModal / deleteModal / historyModal state**

在 component 顶部 (与 detailModal 一起):

```tsx
const [editModal, setEditModal] = useState<EntryShape | null>(null);
const [deleteModal, setDeleteModal] = useState<EntryShape | null>(null);
const [historyModal, setHistoryModal] = useState<string | null>(null);  // entry id
```

- [ ] **Step 6: Build 验证**

```bash
cd opphub-web && npm run build 2>&1 | grep -E "Compiled|error" | head -3
```

预期: Compiled successfully

- [ ] **Step 7: Commit**

```bash
git add app/knowledge/page.tsx
git commit -m "feat(knowledge): 详情 modal 弹窗化 (替代跳转 /knowledge/[id])"
```

---

## Task 2: 「我的卡片」编辑 modal 弹窗

**Files:**
- Modify: `opphub-web/app/knowledge/page.tsx`

- [ ] **Step 1: 加 EditModal 组件**

在 `DetailModal` 函数后面定义:

```tsx
function EditModal({ entry, onClose, onSaved }: {
  entry: EntryShape;
  onClose: () => void;
  onSaved: (newText: string) => void;
}) {
  const apiBase = process.env.NEXT_PUBLIC_API_BASE || "";
  const [text, setText] = useState(entry.rawText);
  const [saving, setSaving] = useState(false);

  async function save() {
    setSaving(true);
    try {
      const token = localStorage.getItem("opphubToken") || "";
      const r = await fetch(apiBase + "/api/knowledge/" + entry.id, {
        method: "PATCH",
        headers: { "content-type": "application/json", authorization: "Bearer " + token },
        body: JSON.stringify({ rawText: text }),
      });
      const j = await r.json();
      if (j?.ok) {
        onSaved(text);
      } else {
        alert("保存失败: " + (j?.message ?? "未知错误"));
      }
    } catch (e: any) {
      alert("保存异常: " + (e?.message ?? String(e)));
    } finally {
      setSaving(false);
    }
  }

  return (
    <div style={modalMask} onClick={onClose}>
      <div style={modalCard} onClick={(e) => e.stopPropagation()}>
        <div style={modalHead}>
          <div>
            <div style={{ fontSize: 12, color: "#9ca3af" }}>编辑</div>
            <div style={{ fontSize: 18, fontWeight: 600, color: "#1f2937" }}>{entry.entryDimension ?? "未命名"}</div>
          </div>
          <button onClick={onClose} style={modalClose}>×</button>
        </div>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          style={{
            ...rawTextBlock,
            border: "none",
            flex: 1,
            fontFamily: "inherit",
            resize: "none",
          }}
        />
        <div style={modalFoot}>
          <button onClick={onClose} style={{ ...linkBtn, background: "#f3f4f6", color: "#374151" }}>取消</button>
          <button onClick={save} disabled={saving} style={linkBtn}>{saving ? "保存中..." : "保存"}</button>
        </div>
      </div>
    </div>
  );
}
```

- [ ] **Step 2: 渲染 EditModal**

在 `KnowledgePage` JSX 末尾 (与 DetailModal 一起):

```tsx
{editModal && (
  <EditModal
    entry={editModal}
    onClose={() => setEditModal(null)}
    onSaved={(newText) => {
      setCaps((prev) => (prev ?? []).map((c) => c.id === editModal.id ? { ...c, rawText: newText, updatedAt: new Date().toISOString() } : c));
      setEditModal(null);
    }}
  />
)}
```

- [ ] **Step 3: Build + Commit**

```bash
cd opphub-web && npm run build 2>&1 | grep -E "Compiled|error" | head -3
git add app/knowledge/page.tsx
git commit -m "feat(knowledge): 编辑 modal 弹窗 (PATCH rawText)"
```

---

## Task 3: 「我的卡片」删除确认 modal

**Files:**
- Modify: `opphub-web/app/knowledge/page.tsx`

- [ ] **Step 1: 加 DeleteModal 组件**

```tsx
function DeleteModal({ entry, onClose, onDeleted }: {
  entry: EntryShape;
  onClose: () => void;
  onDeleted: () => void;
}) {
  const apiBase = process.env.NEXT_PUBLIC_API_BASE || "";
  const [deleting, setDeleting] = useState(false);

  async function doDelete() {
    setDeleting(true);
    try {
      const token = localStorage.getItem("opphubToken") || "";
      const r = await fetch(apiBase + "/api/knowledge/" + entry.id, {
        method: "DELETE",
        headers: { authorization: "Bearer " + token },
      });
      const j = await r.json();
      if (j?.ok) {
        onDeleted();
      } else {
        alert("删除失败: " + (j?.message ?? "未知错误"));
      }
    } catch (e: any) {
      alert("删除异常: " + (e?.message ?? String(e)));
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
        <div style={modalFoot}>
          <button onClick={onClose} style={{ ...linkBtn, background: "#f3f4f6", color: "#374151" }}>取消</button>
          <button onClick={doDelete} disabled={deleting} style={deleteBtn}>{deleting ? "删除中..." : "确认删除"}</button>
        </div>
      </div>
    </div>
  );
}
```

- [ ] **Step 2: 渲染 DeleteModal**

```tsx
{deleteModal && (
  <DeleteModal
    entry={deleteModal}
    onClose={() => setDeleteModal(null)}
    onDeleted={() => {
      setCaps((prev) => (prev ?? []).filter((c) => c.id !== deleteModal.id));
      setDeleteModal(null);
    }}
  />
)}
```

- [ ] **Step 3: Build + Commit**

```bash
cd opphub-web && npm run build 2>&1 | grep -E "Compiled|error" | head -3
git add app/knowledge/page.tsx
git commit -m "feat(knowledge): 删除确认 modal (DELETE 软删)"
```

---

## Task 4: 「我的卡片」历史版本 modal 弹窗

**Files:**
- Modify: `opphub-web/app/knowledge/page.tsx`

- [ ] **Step 1: 加 HistoryModal 组件**

```tsx
type HistoryVersion = {
  id: string;
  title: string;
  createdAt: string;
  supersededAt: string | null;
  isCurrent: boolean;
};

function HistoryModal({ entryId, onClose }: { entryId: string; onClose: () => void }) {
  const apiBase = process.env.NEXT_PUBLIC_API_BASE || "";
  const [versions, setVersions] = useState<HistoryVersion[] | null>(null);
  const [error, setError] = useState<string | null>(null);

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
          {versions && versions.map((v, i) => (
            <div key={v.id} style={{ padding: "10px 12px", borderBottom: "1px solid #f3f4f6" }}>
              <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 4 }}>
                <span style={{ fontSize: 13, fontWeight: 600, color: "#4f46e5", fontFamily: 'ui-monospace, "SF Mono", Menlo, monospace' }}>v{versions.length - i}</span>
                <span style={{ fontSize: 12, color: "#9ca3af" }}>{new Date(v.createdAt).toLocaleString("zh-CN", { hour12: false })}</span>
                {v.isCurrent && <span style={{ fontSize: 10, padding: "1px 6px", background: "#d1fae5", color: "#059669", borderRadius: 8, fontWeight: 600 }}>现行</span>}
              </div>
              <div style={{ fontSize: 12, color: "#6b7280" }}>{v.title}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
```

- [ ] **Step 2: 渲染 HistoryModal**

```tsx
{historyModal && (
  <HistoryModal entryId={historyModal} onClose={() => setHistoryModal(null)} />
)}
```

- [ ] **Step 3: Build + Commit**

```bash
cd opphub-web && npm run build 2>&1 | grep -E "Compiled|error" | head -3
git add app/knowledge/page.tsx
git commit -m "feat(knowledge): 历史版本 modal 弹窗 (GET /api/knowledge/[id]/history)"
```

---

## Task 5: /discover 改读 /api/knowledge

**Files:**
- Modify: `opphub-web/app/discover/page.tsx`

- [ ] **Step 1: 改 fetch 数据源**

文件 `opphub-web/app/discover/page.tsx`, 找到 `useEffect` 块 (大约 line 51-65), 替换为:

```tsx
  useEffect(() => {
    if (!mounted) return;
    setLoading(true);
    const token = localStorage.getItem("opphubToken") || "";
    // buyer 角色: 想看供应方 → 看别人录入的 ability 卡片
    // seller 角色: 想看需求 → 看别人录入的 downstream 卡片
    const targetType = role === "buyer" ? "ability" : "downstream";
    fetch(`${apiBase}/api/knowledge?opcId=me&entryType=${targetType}`, {
      headers: { authorization: "Bearer " + token },
    })
      .then((r) => r.json())
      .then((j) => {
        const list = j?.ok && Array.isArray(j.data) ? j.data : [];
        setCards(list);
      })
      .catch(() => setCards([]))
      .finally(() => setLoading(false));
  }, [mounted, role, apiBase]);
```

(注: 实际公开浏览需要 server 加 `visibility=PUBLIC` 过滤; 此处先实现 拉自己的 entry 看 effect, 真公开留 server 任务)

- [ ] **Step 2: 替换 state 和渲染**

把原来 `useState<Demand[]>([])` / `useState<OPC[]>([])` 改为 `useState<Entry[]>([])`:

```tsx
type Entry = {
  id: string;
  entryType: string | null;
  entryDimension: string | null;
  rawText: string;
  updatedAt: string;
};

const [cards, setCards] = useState<Entry[]>([]);
```

(删除 Demand / OPC 类型, 替换为单一 Entry)

- [ ] **Step 3: 改渲染 - 用 entry 列表, 按公司名分组**

把 buyer 角色和 seller 角色的渲染合并, 改为按 companyName 分组:

```tsx
{!loading && (
  <div style={{ background: "white", borderRadius: 12, padding: 16 }}>
    <div style={{ fontSize: 14, color: "#6b7280", marginBottom: 12 }}>共 {cards.length} 张卡片</div>
    {cards.length === 0 ? (
      <div style={{ color: "#9ca3af", textAlign: "center", padding: 32 }}>暂无公开卡片</div>
    ) : (
      <div style={{ display: "grid", gap: 10, gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))" }}>
        {cards.map((c) => (
          <a key={c.id} href={`/knowledge/profile?opcId=me`} style={{ textDecoration: "none" }}>
            <div style={{ border: "1px solid #e5e7eb", borderRadius: 8, padding: 12 }}>
              <div style={{ fontSize: 12, color: "#9ca3af", marginBottom: 4 }}>{c.entryType}</div>
              <div style={{ fontSize: 16, fontWeight: 600, color: "#1f2937" }}>{c.entryDimension ?? "未命名"}</div>
              <div style={{ fontSize: 12, color: "#4b5563", marginTop: 6, lineHeight: 1.5 }}>
                {c.rawText.slice(0, 100)}...
              </div>
            </div>
          </a>
        ))}
      </div>
    )}
  </div>
)}
```

(buyer 和 seller 用同一个渲染, 因为现在数据源已经按 entryType 过滤)

- [ ] **Step 4: Build + Commit**

```bash
cd opphub-web && npm run build 2>&1 | grep -E "Compiled|error|discover" | head -10
git add app/discover/page.tsx
git commit -m "feat(discover): 改读 /api/knowledge (按 entryType 过滤, 替代 marketplace/demands 表)"
```

---

## Task 6: 部署 ECS + 终验

- [ ] **Step 1: scp web 改动**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev
scp opphub-web/app/knowledge/page.tsx opphub-ecs:/opt/1panel/www/opphub-web/app/knowledge/page.tsx
scp opphub-web/app/discover/page.tsx opphub-ecs:/opt/1panel/www/opphub-web/app/discover/page.tsx
```

- [ ] **Step 2: 容器 build + 重启**

```bash
ssh opphub-ecs "docker exec opphub-web sh -c 'cd /app && npm run build 2>&1 | tail -5'"
ssh opphub-ecs "docker restart opphub-web"
sleep 5
```

- [ ] **Step 3: 验证**

```bash
# TopBar 含 "我的卡片"
ssh opphub-ecs 'curl -s http://localhost:3000/knowledge | grep -c "我的卡片" || echo "0"'

# /discover 200
ssh opphub-ecs 'curl -s -o /dev/null -w "%{http_code}\n" http://localhost:3000/discover'
```

预期: 前者 >= 1, 后者 200

- [ ] **Step 4: git tag**

```bash
cd /Users/qiuxz/.openclaw/workspace-dev/opphub-web
git tag phase-3-modal-interactions
```

---

## 完成判定 (v5 修订版)

- [ ] Task 0: ClawHub 链接替换 (github.com → clawhub.ai)
- [ ] Task 1: 「我的卡片」详情 modal 弹窗 (替代跳转)
- [ ] Task 2: 「我的卡片」编辑 modal (PATCH rawText)
- [ ] Task 3: 「我的卡片」删除确认 modal (DELETE 软删)
- [ ] Task 4: 「我的卡片」历史版本 modal (GET /api/knowledge/[id]/history)
- [ ] Task 5: /discover 改读 /api/knowledge, 按 entryType 过滤
- [ ] Task 6: ECS 部署 + 终验
- TopBar 显示「🪪 我的卡片」+ 位置在 💰 钱包 和 🛡️ 后台 之间 (已 commit `1ffbcb8` + `630367f`)
- git tag `phase-3-modal-interactions`

## YAGNI 范围 (本阶段明确不做)

- ❌ server 端加 `visibility=PUBLIC` 过滤 (留作 server 任务)
- ❌ 撮合匹配对页面 (阶段 3 后续或阶段 4)
- ❌ 推送通道 (阶段 5)
- ❌ lib/knowledge-dimensions 共享 enum
- ❌ entryDimension enum 强制
- ❌ `/knowledge/[id]` 页面删除 (留作 SEO 兜底, 不再被引)
- ❌ ClawHub 链接替换 (这次只更新「我的卡片」name, ClawHub 链接留作下次再改 — 实际是本次也应该改, 补充在 Task 0 之外的 quick fix 里)

## ClawHub 链接 quick fix (Task 0 - 已 commit 但忘记加)

实际上 ClawHub 链接 `https://clawhub.ai/mtty-ai/skills/opphub` 应该立刻替换. 这条单 commit:

```bash
cd opphub-web
# app/knowledge/page.tsx line 103 把 github.com 替换成 clawhub.ai/mtty-ai/skills
sed -i 's|https://github.com/mtty-ai/opphub-skill|https://clawhub.ai/mtty-ai/skills/opphub|g' app/knowledge/page.tsx
git add app/knowledge/page.tsx
git commit -m "fix(ui): 安装文档链接改 ClawHub"
```

(在 Task 0 之外的 quick fix, 部署在 Task 6 同一批)
