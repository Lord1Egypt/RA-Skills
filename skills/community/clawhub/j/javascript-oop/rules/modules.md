# Modules

- Prefer ES modules and named exports.
- Keep one responsibility per module.
- Keep module boundaries aligned with `domain`, `application`, `infrastructure`, and
  `interface` layers when that architecture is in use.
- Keep browser controllers and views in `interface`-layer modules, and wire them from a
  small entry module.
- Make ports and adapters explicit instead of mixing them into domain modules.
- Use JSON imports with `with { type: "json" }` when native support exists.
- Keep imports at the top; avoid wildcard imports and mutable exports.
- Watch circular imports and re-export chains.

## Example

```js
import { TabsController } from "./interface/TabsController.js";

const tabsController = new TabsController({
    rootElement: document.querySelector(".tabs"),
});

tabsController.start();
```

## End Check

- Verify export surfaces stay stable and explicit.
- Verify module placement matches the intended architectural layer.
- Verify browser controller wiring stays at the edge of the application.
- Verify ports and adapters are not collapsed into domain modules.
- Verify JSON imports use import attributes only where runtime support exists.
