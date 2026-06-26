# Cloud Development API Reference

## Deploy Cloud Function (cloudFunctionDeploy)

Upload cloud function code to the specified cloud environment.

```js
const ci = require("miniprogram-ci");
const project = new ci.Project({ /* ... */ });

await ci.cloudFunctionDeploy({
  project,
  env: "dev-xxxxx",                    // Cloud environment ID (required)
  name: "login",                        // Cloud function name (required)
  path: "./cloud-functions/login",      // Function code directory (required)
  remoteNpmInstall: true,              // Whether to install dependencies on cloud (default false)
});
```

**remoteNpmInstall details:**
- `true` — Install dependencies on cloud, don't upload local node_modules (recommended)
- `false` — Full upload including node_modules

## Upload Cloud Storage / Static Hosting (cloudFileUpload)

> Alpha version required: `npm install --save miniprogram-ci@alpha`

```js
await ci.cloudFileUpload({
  project,
  env: "dev-xxxxx",                    // Cloud environment ID (required)
  path: "./static",                     // Local file directory (required)
  remotePath: "/public",               // Remote directory (optional)
});
```

## Deploy Cloud Container Version (cloudContainerDeploy)

> Alpha version required: `npm install --save miniprogram-ci@alpha`

```js
await ci.cloudContainerDeploy({
  project,
  env: "dev-xxxxx",                    // Cloud environment ID (required)
  containerRoot: "./container",        // Local container file directory (required)
  version: {
    uploadType: "package",             // package | repository | image
    flowRatio: 100,                    // Default traffic ratio
    cpu: 0.25,                         // CPU cores
    mem: 0.5,                          // Memory (GB)
    minNum: 1,                         // Minimum replicas
    maxNum: 10,                        // Maximum replicas
    policyType: "cpu",                 // Scaling policy (currently only cpu)
    policyThreshold: 60,               // Scaling threshold (%)
    containerPort: 80,                 // Container listening port
    serverName: "my-service",          // Service name (required)
    versionRemark: "v1.0.0",          // Version remark (optional)
  },
});
```

Container specifications:

| Spec | CPU | Memory |
|------|-----|--------|
| Small | 0.25 cores | 0.5 GB |
| Medium | 0.5 cores | 1 GB |
| Large | 1 core | 2 GB |
| 2x Large | 2 cores | 4 GB |
| 4x Large | 4 cores | 8 GB |

### Dockerfile Options

```js
version: {
  // ...
  dockerfilePath: "./Dockerfile",    // Dockerfile path
  buildDir: "./",                     // Build directory
  envParams: "KEY=VALUE\nFOO=BAR",   // Environment variables
}
```