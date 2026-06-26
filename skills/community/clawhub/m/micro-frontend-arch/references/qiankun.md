# qiankun

## Main App — Register Sub-Apps

```js
import { registerMicroApps, start } from 'qiankun';

registerMicroApps([
  {
    name: 'app-vue',
    entry: '//localhost:8081',           // sub-app dev server or CDN URL
    container: '#sub-app-container',     // mount point in main app HTML
    activeRule: '/vue',                  // activate when route matches
    props: { token: getToken(), bus: eventBus },
  },
  {
    name: 'app-react',
    entry: '//localhost:8082',
    container: '#sub-app-container',
    activeRule: (location) => location.pathname.startsWith('/react'),
    props: { userInfo: store.state.user },
  },
]);

start({
  sandbox: {
    strictStyleIsolation: false,  // Shadow DOM isolation (may break some libs)
    experimentalStyleIsolation: true, // Scoped CSS prefix (safer)
  },
  prefetch: 'all',   // 'all' | true | false | string[]
});
```

## Sub-App Lifecycle Exports (Vue 3 example)

```js
// src/main.js
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

let app = null;

// Dev mode: mount directly without qiankun
if (!window.__POWERED_BY_QIANKUN__) {
  createApp(App).use(router).mount('#app');
}

export async function bootstrap() {
  console.log('[app-vue] bootstrap');
}

export async function mount(props) {
  const { container, token, bus } = props;
  app = createApp(App);
  app.provide('bus', bus);
  app.provide('token', token);
  app.use(router);
  // Mount to qiankun's container, not #app (avoid conflicts)
  app.mount(container ? container.querySelector('#app') : '#app');
}

export async function unmount() {
  app.unmount();
  app = null;
}

export async function update(props) {
  // Called when props change (optional)
  console.log('[app-vue] props updated', props);
}
```

## Sub-App Webpack Config Adjustments

```js
// vue.config.js / webpack.config.js
const { name } = require('./package.json');
module.exports = {
  devServer: {
    port: 8081,
    headers: { 'Access-Control-Allow-Origin': '*' }, // CORS for main app
  },
  configureWebpack: {
    output: {
      library: `${name}-[name]`,
      libraryTarget: 'umd',
      chunkLoadingGlobal: `webpackJsonp_${name}`,
    },
  },
};
```

## Props Communication

```js
// Main app sends data via props
registerMicroApps([{
  name: 'app-vue',
  props: {
    sharedData: reactive({}),       // reactive object
    onAction: (type, payload) => {  // callback for sub → main
      store.dispatch(type, payload);
    },
  },
}]);

// Sub-app receives in mount()
export async function mount({ onAction, sharedData }) {
  app.provide('onAction', onAction);
  app.provide('sharedData', sharedData);
}
```

## Sandbox Options

| Option | Effect |
|--------|--------|
| `sandbox: false` | No isolation (legacy mode) |
| `sandbox: true` | Snapshot sandbox (safe default) |
| `strictStyleIsolation: true` | Shadow DOM (breaks some CSS) |
| `experimentalStyleIsolation: true` | Prefixed scoped CSS (recommended) |
