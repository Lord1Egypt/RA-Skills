# Serverless Functions (API Routes)

IGA Pages provides file-system based Node.js Serverless Functions. Create an `api/` directory in your project root — each `.js` or `.ts` file automatically maps to an HTTP route.

## Quick Start

Create `api/hello.js`:

```js
export default async function handler(request, response) {
  response.json({ message: "Hello from IGA Pages!" });
}
```

Start the dev server (same CLI install as [getting-started.md](getting-started.md)):

```bash
npm i -g @iga-pages/cli
iga pages dev
```

Visit `http://localhost:3000/api/hello`.

## Routing Rules

The `api/` directory structure maps directly to URL paths. Three route types are supported:

```
api/
├── index.js                    → /api                (static)
├── hello.js                    → /api/hello          (static)
├── users/
│   ├── list.js                 → /api/users/list     (static)
│   └── [id].js                 → /api/users/:id      (dynamic)
├── [id].js                     → /api/:id            (dynamic)
├── group/
│   └── [id]/
│       └── detail.js           → /api/group/:id/detail  (dynamic)
└── [[default]].js              → /api/:default*      (catch-all)
```

**Priority order** (highest → lowest): static > dynamic > catch-all.

### Routing Details

- Trailing slash is optional: `/api/hello` and `/api/hello/` both match `api/hello.js`
- Dynamic `[id]` requires a value: `/api/users/123` matches `api/users/[id].js`, but `/api/users/` does not
- Catch-all `[[default]]` matches any path: both `/api/` and `/api/anything` match `api/[[default]].js`

## Function Handler

Export a default function that receives `request` and `response` objects (extended from Node.js HTTP standard):

```js
// api/hello.js
export default async function handler(request, response) {
  response.json({ message: "Hello, IGA!" });
}
```

### request extensions

| Property  | Description                                                              |
| --------- | ------------------------------------------------------------------------ |
| `query`   | Parsed URL query params. Multi-value keys become arrays.                 |
| `params`  | Dynamic route params, e.g. `api/users/[id].js` → `{ id: "123" }`         |
| `cookies` | Parsed `Cookie` header. Empty `{}` if no cookies.                        |
| `body`    | Auto-parsed request body (based on `Content-Type`). `undefined` if none. |

### response helpers

| Method                         | Description                                          |
| ------------------------------ | ---------------------------------------------------- |
| `response.status(code)`        | Set status code (chainable)                          |
| `response.json(data)`          | Send JSON with `Content-Type: application/json`      |
| `response.send(data)`          | Auto-detect: object→JSON, string→HTML, Buffer→binary |
| `response.redirect(url)`       | Redirect (default 307)                               |
| `response.redirect(code, url)` | Redirect with explicit status code                   |

## Express / Koa

Export an Express or Koa app instance as the default export. The file must use `[[default]].js` naming so all sub-paths are forwarded to the framework's router. Do **not** call `app.listen()`.

### Express

```js
// api/[[default]].js
import express from "express";

const app = express();
app.use(express.json());

app.get("/users", (req, res) => res.json({ users: [] }));
app.post("/users", (req, res) => res.status(201).json({ user: req.body }));
app.get("/users/:id", (req, res) => res.json({ user: req.params.id }));

export default app;
```

### Koa

```js
// api/[[default]].js
import Koa from "koa";
import Router from "@koa/router";
import bodyParser from "koa-bodyparser";

const app = new Koa();
const router = new Router();

app.use(bodyParser());

router.get("/users", (ctx) => {
  ctx.body = { users: [] };
});
router.post("/data", (ctx) => {
  ctx.status = 201;
  ctx.body = { data: ctx.request.body };
});

app.use(router.routes());
app.use(router.allowedMethods());

export default app;
```

## Local Development

`iga pages dev` watches `api/` for changes and hot-reloads functions automatically — no restart required.

```bash
iga pages dev        # starts dev server, API routes active at /api/...
```
