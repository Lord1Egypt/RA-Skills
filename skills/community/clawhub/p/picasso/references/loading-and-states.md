# Loading and States Reference

## Table of Contents
1. Loading Duration Rules
2. Skeleton Screens
3. Spinner Use Cases
4. Optimistic Updates
5. Error Boundaries
6. Retry Patterns
7. Offline and Degraded States
8. Empty States
9. Common Mistakes

---

## 1. Loading Duration Rules

| Duration | UI Response |
|---|---|
| < 100ms | No indicator. Feels instant. |
| 100ms - 1s | Subtle opacity fade or pulse on the trigger element. |
| 1s - 3s | Skeleton screen replacing the content area. |
| 3s - 10s | Progress bar (determinate if possible, indeterminate if not). |
| 10s+ | Progress bar + estimated time remaining + ability to cancel. |

Never show a spinner for content that takes > 1s. Skeleton screens preserve spatial layout and feel faster.

---

## 2. Skeleton Screens

Replace content with gray placeholder blocks that match the layout. Add a shimmer animation.

```css
.skeleton {
  background: var(--surface-2);
  border-radius: 4px;
  position: relative;
  overflow: hidden;
}

.skeleton::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    transparent 0%,
    oklch(1 0 0 / 0.04) 50%,
    transparent 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

```jsx
function CardSkeleton() {
  return (
    <div className="card p-4 space-y-3">
      <div className="skeleton h-4 w-3/4 rounded" />
      <div className="skeleton h-3 w-full rounded" />
      <div className="skeleton h-3 w-5/6 rounded" />
      <div className="skeleton h-8 w-24 rounded-lg mt-4" />
    </div>
  );
}
```

Progressive skeletons: show real content as it loads, replacing skeletons one section at a time (top to bottom).

---

## 3. Spinner Use Cases

Spinners are ONLY for small, inline actions:
- Button submit (replace button text with spinner)
- Toggle switch (brief loading)
- Inline save indicators

Never for:
- Page content areas (use skeleton)
- Full-page loading (use progress bar or skeleton)
- Lists or grids (use skeleton)

```css
.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid var(--border);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }
```

---

## 4. Optimistic Updates

Update the UI immediately before the server confirms. Roll back if the server rejects.

```jsx
async function toggleFavorite(id) {
  // Optimistically update UI
  setItems(prev => prev.map(item =>
    item.id === id ? { ...item, favorited: !item.favorited } : item
  ));

  try {
    await api.toggleFavorite(id);
  } catch {
    // Revert on failure
    setItems(prev => prev.map(item =>
      item.id === id ? { ...item, favorited: !item.favorited } : item
    ));
    toast.error('Failed to update. Please try again.');
  }
}
```

Use for: likes, favorites, toggles, reordering, marking as read. Don't use for: payments, deletions, irreversible actions.

---

## 5. Error Boundaries

React error boundaries catch rendering errors and show a fallback UI.

```jsx
// app/error.tsx (Next.js App Router)
'use client';

export default function Error({ error, reset }) {
  return (
    <div className="flex flex-col items-center justify-center min-h-[400px] gap-4">
      <div className="h-12 w-12 rounded-xl bg-red/10 flex items-center justify-center">
        <svg className="w-6 h-6 text-red">...</svg>
      </div>
      <h2 className="text-lg font-semibold">Something went wrong</h2>
      <p className="text-sm text-secondary max-w-md text-center">{error.message}</p>
      <button onClick={reset} className="btn-primary">Try again</button>
    </div>
  );
}
```

Place error boundaries at layout boundaries (per page section, not per component).

---

## 6. Retry Patterns

Exponential backoff: 1s → 2s → 4s. Max 3 retries. Show retry count to user.

```jsx
async function fetchWithRetry(url, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    } catch (err) {
      if (i === maxRetries - 1) throw err;
      await new Promise(r => setTimeout(r, Math.pow(2, i) * 1000));
    }
  }
}
```

UI: after max retries, show error state with manual retry button. Don't auto-retry forever.

---

## 7. Offline and Degraded States

Detect online/offline status:

```js
const [isOnline, setIsOnline] = useState(navigator.onLine);
useEffect(() => {
  const on = () => setIsOnline(true);
  const off = () => setIsOnline(false);
  window.addEventListener('online', on);
  window.addEventListener('offline', off);
  return () => { window.removeEventListener('online', on); window.removeEventListener('offline', off); };
}, []);
```

Offline banner: fixed at top, yellow/amber, with "You're offline. Changes will sync when reconnected."

Stale-while-revalidate: show cached data immediately, fetch fresh in background, update silently.

---

## 8. Empty States

Five types, each with different copy and actions:

| Type | Heading | Action |
|---|---|---|
| **First use** | "No projects yet" | "Create your first project" (primary CTA) |
| **No results** | "No results for 'xyz'" | "Try a different search" or clear filters |
| **Deleted** | "This item was deleted" | "Undo" (within 10s) or go back |
| **Error** | "Couldn't load data" | "Retry" button |
| **Permission** | "You don't have access" | "Request access" or contact admin |

```jsx
function EmptyState({ type, query }) {
  const config = {
    'first-use': {
      icon: <PlusIcon />,
      title: 'No wallets yet',
      description: 'Add your first wallet to start tracking transactions.',
      action: { label: 'Add Wallet', onClick: openAddModal },
    },
    'no-results': {
      icon: <SearchIcon />,
      title: `No results for "${query}"`,
      description: 'Try adjusting your search or filters.',
      action: { label: 'Clear filters', onClick: clearFilters },
    },
  };

  const c = config[type];
  return (
    <div className="flex flex-col items-center py-16 gap-3">
      <div className="h-12 w-12 rounded-xl bg-surface-2 flex items-center justify-center text-muted">
        {c.icon}
      </div>
      <h3 className="text-sm font-semibold">{c.title}</h3>
      <p className="text-xs text-muted max-w-sm text-center">{c.description}</p>
      {c.action && <button className="btn-primary mt-2" onClick={c.action.onClick}>{c.action.label}</button>}
    </div>
  );
}
```

---

## 9. Common Mistakes

- **Spinner for content areas.** Always skeleton. Spinners for inline actions only.
- **No loading indicator for 1-3s waits.** Users think the app is broken. Show skeleton.
- **Optimistic updates for irreversible actions.** Only for safe, reversible changes.
- **Error boundary catching everything silently.** Show the error. Let users retry.
- **Infinite auto-retry.** Max 3 retries, then show manual retry button.
- **Generic empty states.** "No data" is useless. Be specific about what to do next.
- **Same empty state for first-use and no-results.** They have different user intent.
- **No offline detection.** Users submit forms offline and lose data. Detect and warn.
- **Loading skeleton without shimmer.** Static gray blocks look broken. Add the shimmer.
