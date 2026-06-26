# Style Isolation

## 1. CSS Modules (Build-Time Scoping)

```css
/* Button.module.css */
.btn { background: blue; color: white; padding: 8px 16px; }
.btn:hover { background: darkblue; }
```

```jsx
// Button.jsx
import styles from './Button.module.css';
// Compiled class name: .btn → .Button_btn__xK2p1 (unique hash)
export function Button({ label }) {
  return <button className={styles.btn}>{label}</button>;
}
```

Webpack config (already enabled in CRA/Vite by default for `*.module.css`):
```js
{ test: /\.module\.css$/, use: ['style-loader', { loader: 'css-loader',
  options: { modules: { localIdentName: '[name]__[local]__[hash:5]' } } }] }
```

## 2. Shadow DOM (Hard Isolation)

```js
// Attach Shadow DOM to sub-app container
const container = document.getElementById('sub-app');
const shadow = container.attachShadow({ mode: 'open' });

// Inject styles scoped to shadow root
const style = document.createElement('style');
style.textContent = `.title { color: red; }`; // won't leak outside
shadow.appendChild(style);

// Mount React/Vue app into shadow root
ReactDOM.createRoot(shadow).render(<App />);
```

⚠️ **Caveats:** Portals (modals/tooltips), `document.querySelector`, and some
3rd-party libs break inside Shadow DOM. Use `experimentalStyleIsolation` in
qiankun as a safer alternative.

## 3. CSS Namespace / BEM Prefix (Lightweight)

```css
/* Sub-app wraps all styles under a unique prefix */
.app-orders .btn { background: blue; }
.app-orders .card { border-radius: 8px; }
```

```html
<!-- Sub-app root element carries the namespace class -->
<div id="app" class="app-orders">
  <button class="btn">Order Now</button>
</div>
```

PostCSS plugin auto-prefix:
```js
// postcss.config.js
module.exports = { plugins: [require('postcss-prefix-selector')({
  prefix: '.app-orders', exclude: ['.app-orders'] })] };
```

## 4. qiankun experimentalStyleIsolation

```js
// Automatically prefixes sub-app styles with div[data-qiankun="app-name"]
start({ sandbox: { experimentalStyleIsolation: true } });
// Generated: div[data-qiankun="app-vue"] .btn { ... }
```

## 5. Style Piercing (When You Need to Override)

```css
/* Vue: deep selector */
.parent :deep(.child-class) { color: red; }

/* Shadow DOM piercing (deprecated in modern browsers, avoid) */
/* Use CSS custom properties (variables) for theming instead */
:root { --btn-color: blue; }
.shadow-child { color: var(--btn-color); } /* vars DO cross shadow boundary */
```

## Summary

| Strategy | Isolation Level | Complexity | Compatibility |
|----------|----------------|------------|---------------|
| CSS Modules | Component-level | Low | High |
| BEM Prefix | App-level | Low | High |
| qiankun scoped | App-level | None | High |
| Shadow DOM | Hard boundary | Medium | Medium |
