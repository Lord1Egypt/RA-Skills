# 规格驱动测试（Plan → Generate → Heal）

使用 `playwright-cli` 编写和维护 Playwright 测试的端到端工作流。

三个阶段可独立使用：
- **Planning** — 探索应用，生成描述测试内容的规格文件
- **Generate** — 将规格转换为 Playwright 测试文件
- **Heal** — 诊断失败测试，修复代码，同步规格与现实

---

## 1. Planning（规划）

目标：生成规格文件（如 `specs/<feature>.plan.md`），枚举要测试的场景。**始终**写入文件。

### 1.1 前置条件：工作区

检查是否已安装 Playwright：

```bash
test -f playwright.config.ts || test -f playwright.config.js
npx --no-install playwright --version
```

如果没有，引导安装：

```bash
npm init playwright@latest
```

### 1.2 前置条件：Seed 测试

**Seed 测试** 是一个最小测试，让页面进入每个场景的起始状态：导航到应用、登录、特性标志等。

最小 seed：

```ts
// tests/seed.spec.ts
import { test } from '@playwright/test';

test('seed', async ({ page }) => {
  await page.goto('https://example.com/');
});
```

推荐方式 — 将导航放入 fixture：

```ts
// tests/fixtures.ts
import { test as baseTest } from '@playwright/test';
export { expect } from '@playwright/test';

export const test = baseTest.extend({
  page: async ({ page }, use) => {
    await page.goto('https://example.com/');
    await use(page);
  },
});
```

```ts
// tests/seed.spec.ts
import { test } from './fixtures';

test('seed', async ({ page }) => {
  // Fixture 已导航。空 body 告诉 agent 从这里开始。
});
```

### 1.3 探索应用

通过 seed 启动并附加：

```bash
PLAYWRIGHT_HTML_OPEN=never npx playwright test tests/seed.spec.ts --debug=cli
# 等待 "Debugging Instructions" 和会话名 tw-XXXX
playwright-cli attach tw-XXXX
```

恢复并探索：

```bash
playwright-cli resume                   # 恢复执行 seed
playwright-cli snapshot                 # 交互元素清单
playwright-cli click e5                 # 跟踪流程
playwright-cli eval "location.href"     # 读取 URL/状态
playwright-cli show --annotate          # 让用户指出某处
```

绘制：
- 交互界面（表单、按钮、列表、过滤器、模态框）
- 端到端主要用户旅程
- 边界情况：空状态、验证错误、超长输入、边界值
- 持久化：重载、local/session storage、URL 片段
- 导航：哪些控件改变 URL，前进/后退行为

**重要**：不要直接用 playwright-cli 打开 URL，始终通过测试以捕获自定义设置。
**重要**：探索完成后停止后台测试。

### 1.4 编写规格文件

保存到 `specs/<feature>.plan.md`：

```markdown
# <Feature> 测试计划

## 应用概述

<一段描述功能及其重要性。>

## 测试场景

### 1. <组名>

**Seed:** `tests/seed.spec.ts`

#### 1.1. <kebab-case-scenario-name>

**File:** `tests/<group>/<kebab-case-scenario-name>.spec.ts`

**Steps:**
  1. <具体用户步骤>
    - expect: <可观察结果>
    - expect: <另一个可观察结果>
  2. <下一步骤>
    - expect: <结果>

#### 1.2. <next-scenario>
...
```

指南：
- 每个场景独立，从 seed 的新鲜状态开始 — 不要链接场景
- 场景名用 kebab-case，匹配测试文件名
- 覆盖正常路径、边界情况、验证、负面流程、持久化
- 用用户级别写步骤（"在输入框输入'Buy milk'"），不是 API 级别
- 将可观察结果放在 `- expect:` 项目中

---

## 2. Generate（生成）

目标：将规格文件转换为 Playwright 测试文件。

### 2.1 输入

- **规格文件**，如 `specs/basic-operations.plan.md`
- **目标**：单个场景（如 `1.2`）、整组（`1`）或全部
- **Seed 文件**，从场景组的 `**Seed:**` 行读取

### 2.2 生成单个场景

对于每个目标场景，按顺序（不要并行 — 场景共享 seed 会话）：

```bash
PLAYWRIGHT_HTML_OPEN=never npx playwright test <seed-file> --debug=cli   # 后台
playwright-cli attach tw-XXXX
# resume
```

**不要**直接用 playwright-cli 打开 URL，始终通过测试。

用 `playwright-cli` 逐步执行场景的 `Steps:`，将规格作为计划，实时应用作为真实来源。如果步骤模糊、引用不存在的元素、或与实际行为矛盾，更新规格以匹配实际应用。

每个操作都会打印等效的 Playwright TypeScript：

```bash
playwright-cli snapshot                         # 查找 ref
playwright-cli fill e3 "John Doe"               # -> page.getByRole('textbox', {...}).fill(...)
playwright-cli press Enter
playwright-cli click e7
```

对于每个 `- expect:` 项目，添加显式断言。

收集生成的代码并写入测试文件：

```ts
// spec: specs/basic-operations.plan.md
// seed: tests/seed.spec.ts
import { test, expect } from './fixtures';

test.describe('Signing in and out', () => {
  test('should sign in', async ({ page }) => {
    // 1. Navigate to the application
    // (handled by the seed fixture)

    // 2. Type 'John Doe' into the username field
    await page.getByRole('textbox', { name: 'username' }).fill('John Doe');

    // 3. Type password
    await page.getByRole('textbox', { name: 'password' }).fill('TestPassword');

    // 4. Press Enter to submit
    await page.getByRole('textbox', { name: 'password' }).press('Enter');

    await expect(page.getByRole('heading')).toContainText('Welcome, John Doe!');
  });
});
```

规则：
- **每个文件一个测试**。文件路径、describe 名、test 名来自规格
- 在每个编号步骤前添加 `// N. <step text>` 注释
- 使用规格的 describe 组名（不含序号）
- 如果有 fixtures 文件则从中导入；否则从 `@playwright/test`
- **重要**：在移动到下一个场景前关闭 CLI 会话并停止后台测试

### 2.3 生成多个场景

逐个循环执行 2.2，每次重启 seed 以确保每个测试从干净页面开始。

### 2.4 运行生成的测试

生成后，运行新测试一次：

```bash
PLAYWRIGHT_HTML_OPEN=never npx playwright test tests/<group>/<scenario>.spec.ts
```

任何失败进入第 3 节。

---

## 3. Heal（修复）

目标：修复失败测试，如果应用的预期行为改变则更新规格。

### 3.1 查找失败测试

```bash
PLAYWRIGHT_HTML_OPEN=never npx playwright test
```

记录失败的 `<file>:<line>` 条目，逐个处理。不要并行修复。

### 3.2 调试单个失败

在后台运行失败的测试调试模式，然后附加：

```bash
PLAYWRIGHT_HTML_OPEN=never npx playwright test tests/<group>/<scenario>.spec.ts:<line> --debug=cli
# 等待 "Debugging Instructions" 和 tw-XXXX 会话名
playwright-cli attach tw-XXXX
```

测试在开始时暂停。前进或运行到失败操作/断言之前，然后诊断：

```bash
playwright-cli snapshot                # 元素是否改变/移动/重命名？
playwright-cli console                 # 应用端错误？
playwright-cli requests                # 请求失败？载荷错误？
playwright-cli show --annotate         # 让用户指出某处
```

常见原因：选择器漂移、新包装元素、label/ARIA 重命名、时序（过渡、异步加载）、断言文本更新、测试数据泄漏。

用 `playwright-cli` 演练修正后的交互 — 输出中生成的代码就是粘贴回测试的内容。

### 3.3 应用修复

编辑测试文件：更新 locator、断言、步骤顺序或输入以匹配修正后的行为。停止后台调试运行。重新运行单个测试确认通过。

**永远不要**跳过 hooks 或添加 sleep 作为修复。**永远不要**使用 `networkidle`。

### 3.4 与规格同步

打开测试文件 `// spec:` 头引用的规格，找到匹配测试的场景。

- **修复纯技术性**（locator 漂移、更好的断言形状），规格的用户级行为仍匹配应用 → 不动规格
- **修复改变了用户可见步骤、输入、顺序或预期结果** → 更新规格以匹配现实。保持场景 ID 和文件路径稳定
- **不清楚应用改变是有意**（规格过时）**还是回归**（测试正确，应用错误）→ **停止并询问用户**。提供：
  - 场景 ID（如 `2.3`）
  - 不再匹配的规格行
  - 观察到的应用行为

### 3.5 迭代和放弃

- 逐个修复失败；每次修复后重新运行
- 如果彻底调查后确信测试正确但应用错误，**且**用户确认是 bug：用 `test.fixme(...)` 标记测试，注释指向用户的决定或 issue 链接。**永远不要**默默跳过。

---

## 交叉引用

| 用途 | 参考 |
|------|------|
| `--debug=cli` / attach 机制 | [playwright-tests.md](playwright-tests.md) |
| `playwright-cli` 操作如何变成 TS | [test-generation.md](test-generation.md) |
| 探索/生成时模拟请求 | [request-mocking.md](request-mocking.md) |
| 管理 CLI 浏览器会话 | [session-management.md](session-management.md) |
