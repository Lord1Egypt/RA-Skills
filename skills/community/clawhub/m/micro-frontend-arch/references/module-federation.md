# Module Federation

## Host App (Main Shell) — webpack.config.js

```js
const { ModuleFederationPlugin } = require('webpack').container;

module.exports = {
  plugins: [
    new ModuleFederationPlugin({
      name: 'shell',
      remotes: {
        // Static remote
        appOrders: 'appOrders@http://localhost:3001/remoteEntry.js',
        // Dynamic remote (loaded at runtime)
        appUser: 'appUser@[window.remoteUserUrl]/remoteEntry.js',
      },
      shared: {
        react: { singleton: true, requiredVersion: '^18.0.0' },
        'react-dom': { singleton: true, requiredVersion: '^18.0.0' },
        'react-router-dom': { singleton: true },
      },
    }),
  ],
};
```

## Remote App — webpack.config.js

```js
new ModuleFederationPlugin({
  name: 'appOrders',
  filename: 'remoteEntry.js',
  exposes: {
    './OrderList': './src/components/OrderList',
    './OrderDetail': './src/pages/OrderDetail',
    './store': './src/store/index',       // share store if needed
  },
  shared: {
    react: { singleton: true, requiredVersion: '^18.0.0' },
    'react-dom': { singleton: true, requiredVersion: '^18.0.0' },
  },
}),
```

## Consuming a Remote in Host

```jsx
// Static import (webpack resolves at build time config)
import OrderList from 'appOrders/OrderList';

// Lazy + Suspense (recommended for code splitting)
const OrderDetail = React.lazy(() => import('appOrders/OrderDetail'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <OrderDetail orderId="123" />
    </Suspense>
  );
}
```

## Dynamic Remote Loading (Runtime URL)

```js
// Load remote entry script dynamically, then use the module
async function loadRemote(scope, module, url) {
  await __webpack_init_sharing__('default');
  const container = window[scope]; // injected by remote script
  await container.init(__webpack_share_scopes__.default);
  const factory = await container.get(module);
  return factory();
}

// Usage
const { default: Widget } = await loadRemote(
  'appDashboard',
  './Widget',
  'https://cdn.example.com/dashboard/remoteEntry.js'
);
```

## Shared Dependencies — Key Options

```js
shared: {
  lodash: {
    singleton: true,       // only one instance allowed
    eager: false,          // lazy load (default, reduces initial bundle)
    strictVersion: false,  // warn but don't error on version mismatch
    requiredVersion: '^4.0.0',
  },
}
```

## TypeScript: Auto-generate Remote Types

```bash
# Use @module-federation/typescript or federation-dts
npx @module-federation/typescript
```

Add to `tsconfig.json`:
```json
{ "paths": { "appOrders/*": ["./node_modules/@mf-types/appOrders/*"] } }
```
