# single-spa

## Root Config (Main Shell)

```js
// src/index.js
import { registerApplication, start } from 'single-spa';

registerApplication({
  name: '@org/app-navbar',
  app: () => import('@org/app-navbar'),       // dynamic import or SystemJS
  activeWhen: ['/'],                           // always active
});

registerApplication({
  name: '@org/app-home',
  app: () => System.import('@org/app-home'),  // SystemJS for runtime loading
  activeWhen: '/home',
});

registerApplication({
  name: '@org/app-settings',
  app: () => System.import('@org/app-settings'),
  activeWhen: (location) => location.pathname.startsWith('/settings'),
  customProps: { authToken: () => localStorage.getItem('token') },
});

start({ urlRerouteOnly: true }); // don't re-route on same URL
```

## import-map (SystemJS runtime loading)

```html
<!-- index.html -->
<script type="systemjs-importmap">
{
  "imports": {
    "@org/app-navbar": "https://cdn.example.com/navbar/main.js",
    "@org/app-home":   "https://cdn.example.com/home/main.js",
    "react":           "https://cdn.jsdelivr.net/npm/react@18/umd/react.production.min.js",
    "react-dom":       "https://cdn.jsdelivr.net/npm/react-dom@18/umd/react-dom.production.min.js"
  }
}
</script>
<script src="https://cdn.jsdelivr.net/npm/systemjs/dist/system.min.js"></script>
```

## Sub-App Lifecycle (React)

```js
import React from 'react';
import ReactDOM from 'react-dom/client';
import singleSpaReact from 'single-spa-react'; // framework adapter
import App from './App';

const lifecycles = singleSpaReact({
  React,
  ReactDOM,
  rootComponent: App,
  errorBoundary(err) { return <div>Error: {err.message}</div>; },
});

export const { bootstrap, mount, unmount } = lifecycles;
```

## Sub-App Lifecycle (Vue 3)

```js
import { createApp } from 'vue';
import singleSpaVue from 'single-spa-vue';
import App from './App.vue';

const vueLifecycles = singleSpaVue({
  createApp,
  appOptions: { render: () => h(App) },
  handleInstance: (app) => { app.use(router); },
});

export const { bootstrap, mount, unmount } = vueLifecycles;
```

## Parcel (Framework-Agnostic Component)

```js
// Mount a parcel manually (not route-driven)
import { mountRootParcel } from 'single-spa';
import parcelConfig from '@org/some-widget';

const parcel = mountRootParcel(parcelConfig, {
  domElement: document.getElementById('widget-slot'),
  customProps: { color: 'blue' },
});

// Later: unmount when done
parcel.unmount();
```

## Framework Adapters

| Framework | Package |
|-----------|---------|
| React | `single-spa-react` |
| Vue 3 | `single-spa-vue` |
| Angular | `single-spa-angular` |
| Vanilla JS | Manual lifecycle export |
