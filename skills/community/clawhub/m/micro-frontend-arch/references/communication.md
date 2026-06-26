# Inter-App Communication

## 1. CustomEvent (Loosely Coupled, No Dependencies)

```js
// Publisher (sub-app A or main app)
function publish(eventName, detail) {
  window.dispatchEvent(new CustomEvent(eventName, { detail }));
}

publish('user:login', { userId: '123', name: 'Alice' });

// Subscriber (sub-app B)
function subscribe(eventName, handler) {
  window.addEventListener(eventName, (e) => handler(e.detail));
  return () => window.removeEventListener(eventName, handler); // cleanup
}

const unsub = subscribe('user:login', ({ userId }) => {
  console.log('User logged in:', userId);
});

// On unmount: unsub()
```

## 2. Props Passing (Parent → Child, qiankun / Module Federation)

```js
// qiankun main app → sub-app via registerMicroApps props
// Already shown in qiankun.md; use for initial data + callbacks

// Module Federation: pass via React props normally
// Host:
<RemoteWidget onAction={handleAction} config={widgetConfig} />

// Limitation: only works for parent→child, not sibling communication
```

## 3. Shared State — mitt (Lightweight Event Bus)

```js
// shared/bus.js — loaded as a singleton (Module Federation shared or CDN)
import mitt from 'mitt';
export const bus = mitt();

// App A — emit
import { bus } from 'shared/bus';
bus.emit('cart:updated', { count: 5 });

// App B — listen
import { bus } from 'shared/bus';
bus.on('cart:updated', ({ count }) => updateCartBadge(count));
bus.on('*', (type, e) => console.log('global event', type, e)); // wildcard

// Cleanup on unmount
bus.off('cart:updated', handler);
```

## 4. Shared State — RxJS BehaviorSubject (Stateful)

```js
// shared/state.js
import { BehaviorSubject } from 'rxjs';

export const userState$ = new BehaviorSubject(null); // null = not logged in

// App A — update state
userState$.next({ id: '1', name: 'Alice', role: 'admin' });

// App B — subscribe (gets current value immediately on subscribe)
const sub = userState$.subscribe((user) => {
  if (user) renderUserMenu(user);
});

// Cleanup
sub.unsubscribe();
```

## 5. localStorage / sessionStorage (Cross-Tab, Simple)

```js
// Write
localStorage.setItem('auth_token', JSON.stringify({ token, expiresAt }));

// Read from any sub-app
const auth = JSON.parse(localStorage.getItem('auth_token') ?? 'null');

// Listen for changes from OTHER tabs/windows
window.addEventListener('storage', (e) => {
  if (e.key === 'auth_token') handleAuthChange(JSON.parse(e.newValue));
});
// Note: 'storage' event does NOT fire in the same tab that wrote the value
```

## Pattern Comparison

| Pattern | Direction | Real-time | Persistent |
|---------|-----------|-----------|------------|
| CustomEvent | Any | ✅ | ❌ |
| Props | Parent→Child | ✅ | ❌ |
| mitt bus | Any | ✅ | ❌ |
| RxJS Subject | Any | ✅ | ❌ |
| localStorage | Any | Cross-tab | ✅ |
