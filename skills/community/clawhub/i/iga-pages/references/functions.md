# Serverless Functions (API Routes)

IGA Pages provides file-system based Node.js Serverless Functions. Create an `api/` directory in your project root — each `.js` or `.ts` file automatically maps to an HTTP route.

## Quick Start

Create `api/hello.js`:

```js
export function GET(request) {
  return Response.json({ message: "Hello from IGA Pages!" });
}
```

Start the dev server (install the CLI globally first):

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

## Function Handlers

Use the Web-standard `Request` → `Response` contract. Parse the request through
the standard APIs and return a `Response`.

### Fetch handler

Use a default-exported object with `fetch(request)` when one function must dispatch
multiple methods itself:

```js
// api/handler.js
export default {
  async fetch(request) {
    if (request.method === "POST") {
      return Response.json(await request.json(), { status: 201 });
    }

    return Response.json({ method: request.method });
  },
};
```

### Named HTTP method exports

Export the methods the route accepts. Supported names are `GET`, `POST`, `PUT`,
`PATCH`, `DELETE`, `HEAD`, and `OPTIONS`. An unsupported method receives `405` and
an `Allow` header automatically.

```js
// api/users/[id].js
export function GET(request) {
  const { id } = request.params;
  const { searchParams } = new URL(request.url);

  return Response.json({
    id,
    include: searchParams.get("include"),
  });
}

export async function PATCH(request) {
  const update = await request.json();
  return Response.json({ update });
}
```

`request` is the standard Web `Request`; IGA Pages additionally exposes dynamic
route segments as `request.params`. Use `new URL(request.url)` for query params,
`request.headers` for headers and cookies, and `request.json()`, `request.text()`,
or `request.arrayBuffer()` for the request body.

## Express / Koa

Export an Express or Koa app instance as the default export. The file must use `[[default]].js` naming so all sub-paths are forwarded to the framework's router. Do **not** call `app.listen()`.

### Path Mapping (Important)

The file lives under `api/`, so IGA Pages mounts the entire app at the **`/api` prefix**. Routes you define inside Express/Koa are **relative to `/api`** — the framework sees the path with `/api` already stripped.

| File location           | Route in code           | Public URL       |
| ----------------------- | ----------------------- | ---------------- |
| `api/[[default]].js`    | `app.get("/users")`     | `/api/users`     |
| `api/[[default]].js`    | `app.get("/users/:id")` | `/api/users/123` |
| `api/[[default]].js`    | `app.get("/")`          | `/api`           |
| `api/v1/[[default]].js` | `app.get("/users")`     | `/api/v1/users`  |

Common mistake: writing `app.get("/api/users", ...)` inside the file — this would be reachable at `/api/api/users`. Drop the `/api` prefix in your route definitions.

Frontend `fetch` calls must still use the full public path (e.g. `fetch("/api/users")`).

### Express

```js
// api/[[default]].js  →  mounted at /api
import express from "express";

const app = express();
app.use(express.json());

app.get("/users", (req, res) => res.json({ users: [] })); // → /api/users
app.post("/users", (req, res) => res.status(201).json({ user: req.body })); // → /api/users
app.get("/users/:id", (req, res) => res.json({ user: req.params.id })); // → /api/users/:id

export default app;
```

### Koa

```js
// api/[[default]].js  →  mounted at /api
import Koa from "koa";
import Router from "@koa/router";
import bodyParser from "koa-bodyparser";

const app = new Koa();
const router = new Router();

app.use(bodyParser());

router.get("/users", (ctx) => {
  // → /api/users
  ctx.body = { users: [] };
});
router.post("/data", (ctx) => {
  // → /api/data
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
iga pages dev        # framework + API routes, /api/... live
```
