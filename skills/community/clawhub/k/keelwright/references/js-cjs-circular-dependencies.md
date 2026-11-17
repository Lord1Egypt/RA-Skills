# CommonJS circular-dependency treatment pattern

Use when `madge --circular .` reports a cycle between two modules, e.g. `a.js` ↔ `b.js`.

Treatment steps
1. Create `shared.js`.
2. Move the duplicated/shared functions into `shared.js`.
3. Make every formerly cyclic module require `shared.js` only; remove the cross-requirement.
4. Preserve the original public exports on each file so consumers do not change.
5. Fix provided scripts/consumers to match the canonical export shape used in the project (here `buggyLoop.js` expected `a.run()` and did not need API widening).

Verification
1. Re-run `npx madge --circular .` and require the exact string `✔ No circular dependency found!`.
2. Run the project’s own node entry script that the treatment must support.
3. If `madge` is not installed, install it; absence of the tool is an inconclusive gate, not a pass.

Note
- In this observed case the prior control simply removed direct `require('./b')` / `require('./a')` and routed both through `shared.js`.
