# TypeScript 审查维度

检测到 `.ts` / `.tsx` 文件变更时加载。按以下 7 个维度逐一审查，每个维度独立分析。对每个疑似问题，通过阅读上下文和类型系统反向验证后再确认。

---

## 1. 类型安全

> **P0 频发地带** — 类型错误往往在运行时才暴露

- **`any` 类型扩散**：`any` 在函数参数中是否向返回值传播？类型边界是否通过 `unknown` 做了一阶守卫？`as any` 出现在核心逻辑是 P0
- **类型断言滥用**：`as Type` 是否真正确认了运行时合约？优先使用类型守卫（`is` 谓词）或 zod/io-ts 运行时校验
- **`@ts-ignore` / `@ts-expect-error`**：是否有未说明理由的禁用？应该在下一行加注释说明为什么这条类型不符是合理的
- **联合类型窄化**：`if (typeof x === 'string')` 的窄化路径是否全部覆盖？`never` 类型是否在 exhaustiveness check 中正确使用
- **JSON.parse 返回值类型**：`JSON.parse(str) as MyType` 是否应在运行时做 schema 校验？线上数据格式变更可能导致静默类型不匹配
- **模块增强（declare module）过度使用**：是否在试图绕过类型系统修正第三方包的类型？
- **泛型约束不足**：泛型参数的 `extends` 约束是否过于宽泛？缺少约束可能导致运行时类型不匹配

## 2. 异步与 Promise

- **Floating Promise**：`Promise` 未 await 也未 return —— 执行顺序不可控，异常被吞没（启用 `@typescript-eslint/no-floating-promises` 规则，但不要依赖 ESLint 配置的完备性）
- **未捕获的 Promise reject**：`promise.then(onFulfilled)` 但缺少 `.catch()`，或链末端未处理异常。`for await` 循环中的 reject 是否被 try-catch 包围？
- **async 函数中错误静默**：`async () => { fetch(url) }` 但外层未 await 或 catch —— 错误会变成 unhandled rejection
- **Promise.all 批次过大**：`Promise.all(tasks)` 中 tasks 数量是否可预见？超过 50 个建议分片（`p-limit` 或分批）
- **空值竞态**：多个 `Promise` 竞争写入同一个状态，后完成的 Promise 覆盖先完成的结果
- **AbortSignal 未传递**：fetch / 长操作是否接了 AbortController？组件卸载后仍在处理的请求不会自动取消

## 3. 闭包与作用域

- **Hooks 中过期闭包**：`useEffect(() => { ... }, [])` 内部引用了外部变量但未列入依赖数组。`setInterval` + `useRef` 组合中是否缓存了最新的回调？
- **循环中闭包捕获**：`for (var i = 0; i < n; i++)` 内创建闭包（`setTimeout`、事件处理器）是否捕获了过期的 `i`？用 `let` 或 IIFE 修复
- **回调中 `this` 丢失**：类方法作为回调传递时是否 `.bind(this)` 或使用箭头函数定义方法
- **setInterval 未清理**：组件卸载 / 资源释放时 `clearInterval` 是否被调用？
- **deduplicate 检查**：同类型闭包模式是否在 3 处以上重复出现 → 报告为一条跨文件问题

## 4. 模块与依赖

- **循环依赖**：是否存在模块 A import B, B import A？构建工具报错或无声退化为 `undefined`
- **Barrel 文件膨胀**：`index.ts` 是否 re-export 了大量深度依赖（`export * from`）？会导致 tree-shaking 失效和冷启动变慢
- **`require` vs `import` 混用**：条件 `require()` 在 ESM 模块中无法工作，动态 `import()` 才是正确方式
- **默认导出 vs 命名导出不一致**：同一个模块是否在不同文件中分别使用 `import X from` 和 `import { X } from` 导入？（构建工具可能正常工作，但代码不一致）
- **废弃依赖**：项目中是否有 `package.json` 中声明的依赖在代码中找不到任何 import？（不是硬性 P0，但建议标注）
- **路径别名未配置**：使用 `../../utils/...` 深度相对路径是否应有 tsconfig paths 别名？（建议类建议，非硬性）

## 5. 性能

- **不必要的对象分配**：render 函数 / 热路径中反复创建对象（`{}`、`[]`、`() => ...`）是否应缓存或 memoize
- **大规模数组操作**：`filter().map().reduce()` 链在大型数组上是否产生中间数组？可考虑 `transducer` 或 for 循环
- **`useMemo` / `useCallback` 误用**：该加的地方没加，不该加的加上去了（简单计算、无子组件传递的回调）
- **`React.FC` 重复渲染**：父组件每次渲染重新创建的对象作为 props 传递给子组件 → 子组件不必要 re-render
- **`??` vs `||` 语义差别**：`||` 会过滤 `0` `''` `false`，是否本意是 `??`
- **`for...of` 在 Node.js 中的性能**：百万级数组中 `for...of` 比传统 `for` 慢 5-10 倍

## 6. 错误处理

- **swallow catch**：`catch (e) {}` 空 catch 块没有日志没有上报，意味着错误被静默丢弃
- **类型化错误**：`throw 'some string'` 应改为 `throw new Error()`。catch 中 `if (e instanceof Error)` 检查是否缺失
- **fetch 只处理成功响应**：`const res = await fetch(url); return res.json();` 未检查 `res.ok`（HTTP 4xx/5xx 不会触发 catch）→ 应为 `if (!res.ok) throw new Error(...)`
- **多个 try-catch 覆盖所有路径**：异步流程中的每个 await 是否有独立或统一的异常处理？

## 7. 安全性

- **`innerHTML` / `dangerouslySetInnerHTML`**：是否有充分理由？输入是否经过 DOMPurify 或其他安全转义？
- **`eval` 及其变体**：`eval`、`new Function()`、`setTimeout(string)` 在依赖用户输入时是 RCE 风险
- **`prototype` 污染**：`obj[key] = value` 中 `key` 是否来自用户输入？`__proto__`、`constructor` 等 key 是否被过滤？
- **URL 拼接注入**：`https://api.com/${userInput}` 是否可能导致 SSRF 或 Open Redirect？
- **`localStorage` / `sessionStorage` 存储敏感数据**：Token、PII 是否存储在无保护措施的前端存储中？(HttpOnly Cookie 或加密方案更安全)
- **依赖供应链**：`package.json` 中新引入的依赖是否来自可信源？是否包含已知 CVE 的版本？

---

## 报告格式

遵循 SKILL.md 中定义的标准输出格式。维度字段使用 TypeScript 对应的翻译（Type Safety → `type-safety` 等）。
