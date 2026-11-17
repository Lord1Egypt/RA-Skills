# 运行自定义代码（`run-code`）⚠️

> ⚠️ **安全警告：** `run-code` 在 daemon 进程的 **受限沙箱（`vm` 模块）** 中执行代码，**无法直接调用** Node.js 系统 API（`fs` / `child_process` / `process` / `require`）。但**浏览器上下文本身可经下载（`download.saveAs`）或文件上传（`setInputFiles`）在本地磁盘读写文件，并能发起任意网络请求**——这些由注入的 `page` 句柄提供，沙箱不阻止。因此它**仍能把数据持久化到本地磁盘**（见下方"文件下载"小节）。仅在用户明确指定任务中使用，不要执行来源不明的代码片段。

当内置命令不够用时，用 `pw-browser run-code` 执行 Playwright 代码。

## `eval`：页面上下文任意 JavaScript 执行 ⚠️

> ⚠️ **安全警告：** `eval` 在**当前页面的 JavaScript 上下文**中执行你提供的任意代码（等价于在浏览器开发者工具控制台里直接输入并执行）。它能读取 `document.cookie`、`localStorage`/`sessionStorage`、发起**携带当前页面凭证**的 `fetch`/`XMLHttpRequest`，并直接操控 DOM、触发点击与表单提交。**它不等于"执行一个无害的 JS 表达式"——它是完整的页面级代码执行（page-context RCE）。**
>
> `eval` 与 `run-code` 是同一类"代码执行"能力，只是作用域不同：
> - **`eval`** → 页面上下文，能触及页面里的所有数据与会话凭证
> - **`run-code`** → Node 沙箱上下文，能驱动浏览器但拿不到宿主机 `fs`/`process`
>
> 两者都受 daemon **token 认证**保护（未持 token 的外部进程无法调用），且都在 `PW_BROWSER_SAFE_MODE=1` 启动时**被禁用**。仅在用户明确指定的任务、且目标页面可信时使用；不要对来源不明或高权限页面执行。

```bash
# 读取当前页面所有 cookie（含会话令牌）
pw-browser eval "document.cookie"

# 读取 localStorage
pw-browser eval "JSON.stringify(localStorage)"

# 在指定元素上下文执行（ref 来自 snap）
pw-browser eval "el.innerText" e5

# 发起带页面凭证的请求（可被滥用于 CSRF / 数据外泄，慎用）
pw-browser eval "await (await fetch('/api/me')).text()"
```

## 语法

```bash
pw-browser run-code "<code>"
```

代码在 daemon 的 `vm` 沙箱中执行，`page` 对象已注入（标准的 Playwright Page）。沙箱仅暴露 `page` 和安全 JS 全局，不提供 Node 系统模块。

## 等待策略

```bash
# 等待网络空闲
pw-browser run-code "await page.waitForLoadState('networkidle');"

# 等待元素出现
pw-browser run-code "await page.locator('.loading').waitFor({ state: 'hidden' });"

# 等待自定义条件
pw-browser run-code "await page.waitForFunction(() => window.appReady === true);"

# 带超时的等待
pw-browser run-code "await page.locator('.result').waitFor({ timeout: 10000 });"
```

## 页面信息

```bash
# 获取标题
pw-browser run-code "return await page.title();"

# 获取 URL
pw-browser run-code "return page.url();"

# 获取整个 HTML
pw-browser run-code "return await page.content();"

# 视口大小
pw-browser run-code "return JSON.stringify(page.viewportSize());"
```

## 在页面中执行 JS（evaluate）

```bash
# 获取 userAgent
pw-browser run-code "return await page.evaluate(() => navigator.userAgent);"

# 获取所有链接
pw-browser run-code "
  return await page.evaluate(() =>
    [...document.querySelectorAll('a')].map(a => ({ text: a.textContent.trim(), href: a.href }))
  );
"

# 获取 localStorage
pw-browser run-code "return await page.evaluate(() => JSON.stringify(localStorage));"
```

## Iframe 操作

```bash
pw-browser run-code "
  const frame = page.frameLocator('iframe#my-iframe');
  await frame.locator('button.submit').click();
"
```

## 文件下载 ⚠️

> ⚠️ 文件将写入本地磁盘，注意目标路径，避免覆盖已有文件。

```bash
pw-browser run-code "
  const [download] = await Promise.all([
    page.waitForEvent('download'),
    page.locator('text=下载').click()
  ]);
  await download.saveAs('./downloaded-file.pdf');
  return download.suggestedFilename();
"
```

## 错误处理

```bash
pw-browser run-code "
  try {
    await page.locator('button.submit').click({ timeout: 3000 });
    return 'clicked';
  } catch (e) {
    return 'element not found: ' + e.message;
  }
"
```

## 复杂场景：多页数据采集

```bash
pw-browser run-code "
  const results = [];
  for (let i = 1; i <= 5; i++) {
    await page.goto('https://example.com/page/' + i);
    const items = await page.locator('.item').allTextContents();
    results.push(...items);
  }
  return JSON.stringify(results);
"
```

## 复杂场景：表单填写 ⚠️

> ⚠️ 此操作会真实提交表单，可能触发实际的业务操作（注册账号、下单、发送消息等）。执行前确认目标页面和表单内容已经用户确认。

```bash
pw-browser run-code "
  await page.fill('#name', '张三');
  await page.fill('#email', 'test@example.com');
  await page.selectOption('#city', '北京');
  await page.check('#agree');
  await page.locator('button[type=submit]').click();
  await page.waitForURL('**/success');
  return 'form submitted';
"
```

## 注意事项

- `run-code` 中直接使用 Playwright API，无需额外的 `page.evaluate` 包装
- 客户端请求超时为 120 秒，长耗时操作请合理拆分
- 返回值自动序列化为字符串，复杂对象请用 `JSON.stringify()`
- 如果代码中有引号冲突，优先用单引号包裹 JS 字符串
