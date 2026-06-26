# Example OpenClaw `/api/unreal/task` handler

This is a reference design, not a claim about a built-in OpenClaw route.

## Responsibilities

- authenticate bearer token if configured
- validate JSON envelope
- dispatch by `type` and `task`
- return compact JSON

## Pseudocode

```js
app.post('/api/unreal/task', async (req, res) => {
  const auth = req.headers.authorization || '';
  if (EXPECTED_TOKEN && auth !== `Bearer ${EXPECTED_TOKEN}`) {
    return res.status(401).json({
      id: req.body?.id ?? null,
      ok: false,
      result: null,
      error: { code: 'unauthorized', message: 'Invalid token' },
      meta: { handledBy: 'openclaw' }
    });
  }

  const { id, type, task, payload } = req.body || {};
  if (!id || !type || !task) {
    return res.status(400).json({
      id: id ?? null,
      ok: false,
      result: null,
      error: { code: 'invalid_request', message: 'Missing id/type/task' },
      meta: { handledBy: 'openclaw' }
    });
  }

  try {
    let result;

    switch (type) {
      case 'runtime.query.status':
        if (task === 'ping') {
          result = { message: 'pong' };
        } else {
          throw new Error(`Unsupported task for ${type}: ${task}`);
        }
        break;

      case 'editor.remote_control.call':
        result = await routeRemoteControlCall(payload);
        break;

      case 'editor.remote_control.set_property':
        result = await routeRemoteControlSetProperty(payload);
        break;

      case 'runtime.blueprint.invoke':
        result = await routeBlueprintInvoke(payload);
        break;

      default:
        throw new Error(`Unknown task type: ${type}`);
    }

    return res.json({
      id,
      ok: true,
      result,
      error: null,
      meta: { handledBy: 'openclaw' }
    });
  } catch (err) {
    return res.status(400).json({
      id,
      ok: false,
      result: null,
      error: { code: 'task_failed', message: String(err.message || err) },
      meta: { handledBy: 'openclaw' }
    });
  }
});
```

## Suggested implementation detail

Keep Remote Control bridging isolated from general OpenClaw logic so editor-specific behavior does not leak into all handlers.
