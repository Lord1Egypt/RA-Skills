# Performance Optimization Reference

React/Next.js performance rules based on Vercel's guidance. Organized by priority. Every pattern includes the why, the fix, and working code.

---

## Priority 1 - CRITICAL: Eliminating Waterfalls

Waterfalls are the single biggest performance killer. Every sequential `await` that could be parallel is wasted time.

### Promise.all() for Independent Operations

```typescript
// BAD: Sequential - total time = A + B + C
async function getPageData(userId: string) {
  const user = await fetchUser(userId);
  const posts = await fetchPosts(userId);
  const notifications = await fetchNotifications(userId);
  return { user, posts, notifications };
}

// GOOD: Parallel - total time = max(A, B, C)
async function getPageData(userId: string) {
  const [user, posts, notifications] = await Promise.all([
    fetchUser(userId),
    fetchPosts(userId),
    fetchNotifications(userId),
  ]);
  return { user, posts, notifications };
}
```

### Defer Await Until Needed

Don't block code branches that don't use the data.

```typescript
// BAD: Blocks even if we early-return
async function handleRequest(req: Request) {
  const config = await fetchConfig();
  const user = await getUser(req);

  if (!user) {
    return redirect('/login'); // config was fetched for nothing
  }

  return renderPage(user, config);
}

// GOOD: Start fetch immediately, await only when needed
async function handleRequest(req: Request) {
  const configPromise = fetchConfig(); // fire immediately, don't await
  const user = await getUser(req);

  if (!user) {
    return redirect('/login'); // config fetch may still be in-flight, that's fine
  }

  const config = await configPromise; // await only when we need it
  return renderPage(user, config);
}
```

### Dependency-Based Parallelization with better-all

When some fetches depend on others but you still want maximum parallelism:

```typescript
import { all } from 'better-all';

// Runs A and B in parallel. C starts as soon as A finishes (doesn't wait for B).
const { user, posts, comments } = await all({
  user: () => fetchUser(id),
  posts: () => fetchPosts(id),
  comments: async ({ user }) => fetchComments(user.teamId), // depends on user
});
```

### Strategic Suspense Boundaries

Wrap independent data-loading sections in their own Suspense boundary so they stream independently.

```tsx
// BAD: One boundary = entire page waits for slowest component
<Suspense fallback={<PageSkeleton />}>
  <Header />       {/* 50ms */}
  <Feed />         {/* 2000ms - blocks everything */}
  <Sidebar />      {/* 100ms */}
</Suspense>

// GOOD: Independent boundaries = each streams when ready
<Header />
<Suspense fallback={<FeedSkeleton />}>
  <Feed />
</Suspense>
<Suspense fallback={<SidebarSkeleton />}>
  <Sidebar />
</Suspense>
```

---

## Priority 2 - CRITICAL: Bundle Size

### Avoid Barrel File Imports

Barrel files (`index.ts` re-exports) pull in entire modules. Cost: 200-800ms of parse time.

```typescript
// BAD: Imports entire icon library through barrel file
import { ChevronDown } from '@/components/icons';
// This imports index.ts which re-exports 500 icons

// GOOD: Direct import from source file
import { ChevronDown } from '@/components/icons/ChevronDown';

// BAD: Barrel file for utils
import { formatDate } from '@/lib/utils';
// Pulls in every util function

// GOOD: Direct import
import { formatDate } from '@/lib/utils/formatDate';
```

Configure your bundler to detect this:

```javascript
// next.config.js
module.exports = {
  experimental: {
    optimizePackageImports: ['@/components/icons', 'lucide-react', 'date-fns'],
  },
};
```

### Dynamic Imports for Heavy Components

```typescript
import dynamic from 'next/dynamic';

// Heavy editor component - only loads when rendered
const CodeEditor = dynamic(() => import('@/components/CodeEditor'), {
  loading: () => <EditorSkeleton />,
});

// Chart library - loads on demand
const Chart = dynamic(() => import('@/components/Chart'), {
  loading: () => <ChartSkeleton />,
  ssr: false, // Skip server rendering for client-only libs
});
```

### Defer Non-Critical Third-Party Scripts

```typescript
// Analytics, error tracking, chat widgets - none are needed for first render
const Analytics = dynamic(() => import('@/components/Analytics'), {
  ssr: false,
});
const ErrorTracker = dynamic(() => import('@/components/ErrorTracker'), {
  ssr: false,
});

// Load after page is interactive
export default function Layout({ children }) {
  return (
    <>
      {children}
      <Suspense fallback={null}>
        <Analytics />
        <ErrorTracker />
      </Suspense>
    </>
  );
}
```

### Preload on User Intent

Start loading a route or component when the user shows intent (hover, focus) instead of on click.

```tsx
import { useRouter } from 'next/navigation';

function NavLink({ href, children }) {
  const router = useRouter();

  return (
    <Link
      href={href}
      onMouseEnter={() => router.prefetch(href)}
      onFocus={() => router.prefetch(href)}
    >
      {children}
    </Link>
  );
}
```

For heavy components:

```typescript
// Preload the module on hover, render on click
const importEditor = () => import('@/components/CodeEditor');
const CodeEditor = dynamic(importEditor);

function EditorButton() {
  const [show, setShow] = useState(false);

  return (
    <>
      <button
        onMouseEnter={() => importEditor()} // preload on hover
        onClick={() => setShow(true)}
      >
        Open Editor
      </button>
      {show && <CodeEditor />}
    </>
  );
}
```

### Conditional Module Loading

Only load modules when the feature is actually used.

```typescript
async function exportData(format: 'csv' | 'xlsx') {
  if (format === 'xlsx') {
    // xlsx library is 200KB+ - only load when needed
    const XLSX = await import('xlsx');
    return XLSX.utils.json_to_sheet(data);
  }
  // CSV is trivial, no import needed
  return data.map(row => row.join(',')).join('\n');
}
```

---

## Priority 3 - HIGH: Server-Side Performance

### React.cache() for Per-Request Deduplication

Multiple components in the same render can call the same function. `React.cache()` ensures it only executes once per request.

```typescript
import { cache } from 'react';

export const getUser = cache(async (userId: string) => {
  const res = await fetch(`/api/users/${userId}`);
  return res.json();
});

// Component A calls getUser('123') - makes network request
// Component B calls getUser('123') - returns cached result from same request
// Next request: cache is cleared, fresh fetch
```

### LRU Cache for Cross-Request Caching

For data that doesn't change per-request (config, feature flags, static content):

```typescript
import { LRUCache } from 'lru-cache';

const cache = new LRUCache<string, any>({
  max: 500,          // max entries
  ttl: 1000 * 60 * 5, // 5 minute TTL
});

export async function getConfig(key: string) {
  const cached = cache.get(key);
  if (cached) return cached;

  const config = await db.config.findUnique({ where: { key } });
  cache.set(key, config);
  return config;
}
```

### Parallel Data Fetching with Component Composition

Let each Server Component fetch its own data. React deduplicates and parallelizes automatically.

```tsx
// page.tsx - Don't fetch everything here and pass down
export default function DashboardPage() {
  return (
    <div>
      <UserHeader />     {/* fetches user data */}
      <StatsPanel />     {/* fetches stats data */}
      <ActivityFeed />   {/* fetches activity data */}
    </div>
  );
}

// Each component is independent - React runs them in parallel
async function UserHeader() {
  const user = await getUser(); // deduplicated with React.cache
  return <header>{user.name}</header>;
}

async function StatsPanel() {
  const stats = await getStats();
  return <div>{stats.total}</div>;
}
```

### Minimize Serialization at RSC Boundaries

Only pass serializable, minimal data from Server to Client Components.

```tsx
// BAD: Passing entire user object (large, may have non-serializable fields)
<ClientComponent user={fullUserObject} />

// GOOD: Pass only what the client needs
<ClientComponent userName={user.name} userAvatar={user.avatarUrl} />
```

---

## Priority 4 - MEDIUM-HIGH: Client-Side Data

### SWR for Deduplication, Caching, and Revalidation

```typescript
import useSWR from 'swr';

const fetcher = (url: string) => fetch(url).then(r => r.json());

function useUser(id: string) {
  const { data, error, isLoading, mutate } = useSWR(
    `/api/users/${id}`,
    fetcher,
    {
      revalidateOnFocus: false,    // Don't refetch on tab focus
      dedupingInterval: 5000,       // Deduplicate requests within 5s
      staleWhileRevalidate: true,   // Show stale data while fetching fresh
    }
  );

  return { user: data, error, isLoading, mutate };
}

// Multiple components calling useUser('123') = ONE network request
```

### Deduplicate Global Event Listeners

```typescript
// BAD: Every component instance adds its own listener
function Component() {
  useEffect(() => {
    const handler = () => { /* ... */ };
    window.addEventListener('resize', handler);
    return () => window.removeEventListener('resize', handler);
  }, []);
}

// GOOD: Single shared listener, components subscribe to derived state
import { useSyncExternalStore } from 'react';

let width = window.innerWidth;
const listeners = new Set<() => void>();

window.addEventListener('resize', () => {
  width = window.innerWidth;
  listeners.forEach(l => l());
});

function subscribe(listener: () => void) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function useWindowWidth() {
  return useSyncExternalStore(subscribe, () => width);
}
```

---

## Priority 5 - MEDIUM: Re-render Optimization

### Defer State Reads to Usage Point

```tsx
// BAD: Parent re-renders on every keystroke, all children re-render
function SearchPage() {
  const [query, setQuery] = useState('');
  return (
    <div>
      <SearchInput value={query} onChange={setQuery} />
      <ExpensiveHeader />  {/* Re-renders on every keystroke! */}
      <SearchResults query={query} />
    </div>
  );
}

// GOOD: Isolate state to the component that needs it
function SearchPage() {
  return (
    <div>
      <SearchSection />    {/* Contains its own state */}
      <ExpensiveHeader />  {/* Never re-renders from search */}
    </div>
  );
}

function SearchSection() {
  const [query, setQuery] = useState('');
  return (
    <>
      <SearchInput value={query} onChange={setQuery} />
      <SearchResults query={query} />
    </>
  );
}
```

### Narrow Effect Dependencies

```typescript
// BAD: Effect runs whenever any user field changes
useEffect(() => {
  trackPageView(user.id);
}, [user]); // user is an object, new reference every render

// GOOD: Depend on the primitive you actually use
const userId = user.id;
useEffect(() => {
  trackPageView(userId);
}, [userId]); // Only runs when the ID actually changes
```

### Subscribe to Derived State

```typescript
// BAD: Re-renders on every pixel of resize
function Component() {
  const width = useWindowWidth(); // 1024, 1023, 1022...
  const isMobile = width < 768;
  // Renders on every width change even if isMobile doesn't change
}

// GOOD: Only re-renders when the boolean flips
function Component() {
  const isMobile = useSyncExternalStore(
    subscribe,
    () => window.innerWidth < 768 // returns boolean, not number
  );
  // Only re-renders when crossing the 768px threshold
}
```

### Lazy State Initialization

```typescript
// BAD: Expensive computation runs on every render (result is ignored after first)
const [data, setData] = useState(parseExpensiveJSON(localStorage.getItem('data')));

// GOOD: Function is only called once on mount
const [data, setData] = useState(() => parseExpensiveJSON(localStorage.getItem('data')));
```

### Extract Memoized Components

```tsx
// When a parent re-renders but a child's props don't change:
const ExpensiveList = memo(function ExpensiveList({ items }: { items: Item[] }) {
  return items.map(item => <ExpensiveItem key={item.id} item={item} />);
});

// Use with useCallback for event handlers
const handleClick = useCallback((id: string) => {
  setSelected(id);
}, []); // Stable reference

<ExpensiveList items={items} onClick={handleClick} />
```

### useTransition for Non-Urgent Updates

```typescript
function SearchWithSuggestions() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isPending, startTransition] = useTransition();

  function handleChange(value: string) {
    setQuery(value); // Urgent: update input immediately
    startTransition(() => {
      setResults(filterResults(value)); // Non-urgent: can be interrupted
    });
  }

  return (
    <>
      <input value={query} onChange={e => handleChange(e.target.value)} />
      <div style={{ opacity: isPending ? 0.7 : 1 }}>
        <ResultsList results={results} />
      </div>
    </>
  );
}
```

---

## Priority 6 - MEDIUM: Rendering Performance

### content-visibility: auto for Off-Screen DOM

10x faster initial render for long pages. Browser skips layout/paint for off-screen elements.

```css
.card {
  content-visibility: auto;
  contain-intrinsic-size: auto 300px; /* Estimated height to prevent scroll jump */
}

/* For a list of items */
.list-item {
  content-visibility: auto;
  contain-intrinsic-size: auto 80px;
}
```

### Hoist Static JSX Outside Components

Static elements don't need to be recreated on every render.

```tsx
// BAD: emptyState is recreated on every render of List
function List({ items }) {
  const emptyState = (
    <div className="empty">
      <p>No items found</p>
    </div>
  );

  if (items.length === 0) return emptyState;
  return <ul>{items.map(renderItem)}</ul>;
}

// GOOD: Created once, reused forever
const emptyState = (
  <div className="empty">
    <p>No items found</p>
  </div>
);

function List({ items }) {
  if (items.length === 0) return emptyState;
  return <ul>{items.map(renderItem)}</ul>;
}
```

### Prevent Hydration Mismatch with Inline Script

For theme, auth state, or locale that must be available before React hydrates:

```tsx
// layout.tsx
<head>
  <script
    dangerouslySetInnerHTML={{
      __html: `
        (function() {
          var theme = localStorage.getItem('theme') || 'system';
          if (theme === 'system') {
            theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
          }
          document.documentElement.setAttribute('data-theme', theme);
          document.documentElement.style.colorScheme = theme;
        })();
      `,
    }}
  />
</head>
```

This runs synchronously before React hydrates, preventing the flash of wrong theme.

### Optimize SVG Precision

```bash
# Default SVG from design tools: way too many decimal places
# <path d="M12.456789 34.567891 L56.789012 78.901234" />

# After svgo --precision=1:
# <path d="M12.5 34.6 L56.8 78.9" />

npx svgo --precision=1 --multipass icons/*.svg
```

Reduces SVG file size by 20-40% with no visible difference.

### Use Activity Component for Show/Hide

React 19+ `<Activity>` preserves state and DOM when hiding, instead of unmounting.

```tsx
import { Activity } from 'react';

function TabPanel({ activeTab }) {
  return (
    <>
      <Activity mode={activeTab === 'editor' ? 'visible' : 'hidden'}>
        <CodeEditor /> {/* State preserved when hidden */}
      </Activity>
      <Activity mode={activeTab === 'preview' ? 'visible' : 'hidden'}>
        <Preview /> {/* State preserved when hidden */}
      </Activity>
    </>
  );
}
```

### Explicit Conditional Rendering

```tsx
// BAD: && can render "0" or "NaN" as text
{count && <Badge count={count} />}
// If count is 0, renders "0" as text in the DOM

// GOOD: Explicit boolean check
{count > 0 ? <Badge count={count} /> : null}

// GOOD: Double negation for truthy check
{!!items.length ? <List items={items} /> : <EmptyState />}
```

---

## Priority 7 - LOW-MEDIUM: JavaScript Performance

### Build Index Maps for O(1) Lookups

```typescript
// BAD: O(n) lookup on every render or event
function findUser(users: User[], id: string) {
  return users.find(u => u.id === id); // Scans entire array
}

// GOOD: O(1) lookup after one-time O(n) index build
const userIndex = useMemo(() => {
  const map = new Map<string, User>();
  for (const user of users) {
    map.set(user.id, user);
  }
  return map;
}, [users]);

function findUser(id: string) {
  return userIndex.get(id); // Instant lookup
}
```

### Set/Map for Membership Checks

```typescript
// BAD: O(n) per check
const selectedIds = ['a', 'b', 'c', ...hundredsMore];
items.filter(item => selectedIds.includes(item.id)); // O(n*m)

// GOOD: O(1) per check
const selectedSet = new Set(selectedIds);
items.filter(item => selectedSet.has(item.id)); // O(n)
```

### Combine Array Iterations

```typescript
// BAD: Three passes over the array
const active = users.filter(u => u.active);
const names = active.map(u => u.name);
const sorted = names.sort();

// GOOD: Single pass + sort
const names: string[] = [];
for (const u of users) {
  if (u.active) names.push(u.name);
}
names.sort();
```

This matters when arrays have 1000+ items or the operation runs frequently (on scroll, on keystroke).

### Cache Storage API Calls

```typescript
// BAD: Synchronous localStorage call on every render
function useTheme() {
  const [theme, setTheme] = useState(localStorage.getItem('theme') || 'light');
  // localStorage.getItem is synchronous and blocks the main thread
}

// GOOD: Read once, cache in memory
let cachedTheme: string | null = null;
function getTheme() {
  if (cachedTheme === null) {
    cachedTheme = localStorage.getItem('theme') || 'light';
  }
  return cachedTheme;
}

function setTheme(theme: string) {
  cachedTheme = theme;
  localStorage.setItem('theme', theme); // Write-through
}
```

### toSorted() Instead of sort()

```typescript
// BAD: Mutates the original array (breaks React state rules)
const sorted = items.sort((a, b) => a.name.localeCompare(b.name));
// items is now mutated! React won't detect the change

// GOOD: Returns new sorted array (immutable, React-safe)
const sorted = items.toSorted((a, b) => a.name.localeCompare(b.name));
// items is unchanged, sorted is a new array

// Also: toReversed(), toSpliced(), with()
const reversed = items.toReversed();
const withRemoval = items.toSpliced(2, 1); // Remove item at index 2
const withReplacement = items.with(3, newItem); // Replace item at index 3
```

---

## Quick Reference: When to Optimize What

| Symptom | Check First |
|---------|------------|
| Slow page load (3s+) | Priority 1: waterfalls in data fetching |
| Large JS bundle (500KB+) | Priority 2: barrel imports, dynamic imports |
| Slow server response | Priority 3: caching, parallel fetching |
| Stale data, extra requests | Priority 4: SWR, deduplication |
| Janky typing/scrolling | Priority 5: re-render isolation, useTransition |
| Slow initial paint | Priority 6: content-visibility, hydration |
| Slow interactions on large lists | Priority 7: Maps, Sets, combined iterations |
