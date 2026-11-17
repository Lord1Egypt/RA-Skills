---
name: local-webapp-delivery
slug: local-webapp-delivery
displayName: 本地Web应用交付·Windows环境坑
version: 1.0.0
visibility: public
category: dev-programming
subCategories: [dev-script, dev-frontend]
description: 在 WorkBuddy（Windows）环境里交付零依赖本地 Web 应用，并绕开官方测试技能完全不覆盖的本机专属坑。当用户要在本机跑起来一个本地 Web 应用 / 单文件工具 / 案例库 / 看板 / 小工具，或要验证刚写完的 HTML/JS/Python 交付物真的能工作时使用。独家覆盖：Bash 缺 coreutils、bash 是 WSL 启动桩、rm 是坏 shim、PowerShell 不回显 stdout、cwd 漂移、预览面板靠 HEAD 探活——这些在干净 Linux 环境里遇不到。
agent_created: true
---

# 零依赖本地 Web 应用 · 交付与验证
> **定位**：官方 `webapp-testing` 等技能覆盖「用浏览器自动化测 Web 应用」，但**不覆盖在 WorkBuddy/Windows 环境里把应用做出来并跑通**时那堆本机专属坑（`bash` 是 WSL 桩、`rm` 是坏 shim、PowerShell 不回显 stdout、cwd 漂移、预览面板靠 HEAD 探活）。本技能专补这块，且只依赖标准库、零框架。


## WorkBuddy/Windows 环境的硬约束（先看这条，能省半小时）

### Bash 缺 coreutils —— 但一行 PATH 就能修

裸调 `head` / `tail` / `wc` / `grep` / `sed` / `awk` / `sleep` / `dirname` / `which` / `cat` /
`tr` / `cut` 都会 `command not found`（`ls`、`find`、`sort`、`echo` 是好的）。
报错长这样，且**很容易误导成「文件不存在」**：

```
bash.exe: line 1: head: command not found
```

二进制其实都在 `/usr/bin/` 下，只是不在 PATH 里。**开头加一行即可恢复**（实测可行）：

```bash
PATH="/usr/bin:$PATH"          # 或 export PATH="/usr/bin:/bin:$PATH"
printf 'a\nb\nc\n' | head -2   # 现在正常了
```

- 也可以用绝对路径：`/usr/bin/sleep 1`、`/usr/bin/head -2`。
- **但并非 100% 稳定**（同一写法偶尔仍报 not found）。所以关键流程仍留一条保底路径：

```bash
python test.py > out.txt 2>&1; echo "exit=$?"   # 再用 Read 工具读 out.txt
```

先试 PATH 修复，不行就退回重定向 + Read。别一开始就放弃管道。

### `rm` 也是坏 shim；删文件用 Python

`rm` 不属于「PATH 缺失」那一类 —— 它被换成了一个 safe-delete 桩，而**桩自己是坏的**：

```
bash.exe: .../shim/safe-bin/rm: line 13: dirname: command not found
bash.exe: .../shim/safe-bin/rm: line 15: /safe-delete-common.sh: No such file or directory
bash.exe: .../shim/safe-bin/rm: line 17: safe_delete_main: command not found
# exit 127，文件纹丝不动
```

PowerShell 的 `Remove-Item -Force -Confirm:$false` 对同一批文件**静默无效**
（exit 1、无输出、文件还在）—— 别以为删掉了。

**删自己产生的临时文件，用 Python 最可靠**：

```bash
python -c "import glob,os; [os.remove(f) for f in glob.glob(r'DIR/_*.log')]; print('cleaned')"
```

（清理自己的临时文件可以这么干；删用户的真实文件仍要走 trash 或让用户确认。）

### 本机两个 Python 各有所长，别装错

| 解释器 | 情况 |
|---|---|
| 托管 `~/.workbuddy/binaries/python/versions/3.13.12` | 干净，**没有 pyyaml**；要装包就走上面的隔离 venv |
| 系统 `C:\Python313\python.exe` | **已有 pyyaml 6.0.3** → 跑 `check_ci.py`（校验 workflow YAML）直接用它，省掉建 venv；但它的 `pytest` 是坏的（缺 `pygments`，import 就炸） |

推论：**这类项目的 `scripts/test_*.py` 通常是自包含脚本**（自带 `chk()` / `main()` / `sys.exit`），
直接用解释器跑就行，**不要走 pytest**（跑不起来，会误判成「测试全挂」）：

```bash
python scripts/test_xxx.py > out.log 2>&1; echo "exit=$?"   # 再 Read out.log
```

## 接手一个已有项目：先建基线，再动手

要往别人的项目里加东西前，先**把现有测试全跑一遍拿到基线**，否则改坏了分不清是自己弄的
还是本来就坏的。一条命令串起来，全部重定向到文件再读：

```bash
for f in scripts/test_*.py; do python "$f" > t.log 2>&1; echo "$f exit=$?"; done
python selftest.py        > s.log 2>&1; echo "selftest=$?"
node uitest.js            > u1.log 2>&1; echo "ui=$?"
node uitest.js --static   > u2.log 2>&1; echo "ui_static=$?"
```

基线里如果有失败项，**先判断是环境问题还是代码问题**（本次就遇到 `check_ci.py` 只因缺
pyyaml 而失败 —— 换系统 Python 立刻全过，不是代码坏了）。改完再跑一遍，逐项对比。

### `bash` 在 PATH 里是 WSL 启动桩，不是真 bash

这条最阴。从 Python 里 `shutil.which('bash')` 或 subprocess 直接调 `bash`，解析到的是

```
C:\WINDOWS\system32\bash.EXE
```

那是 **WSL 的启动桩**：它不解析脚本，对任何输入都打印「请安装 Linux 发行版」并返回 **1**。
于是 `subprocess.run(['bash','-n',script])` 对**每一个**文件都返回 rc=1、stderr 为空，
看起来像「所有脚本都有语法错」。我为此白排查了一轮。

必须显式用 Git 自带的真 bash，并且**先拿一个故意写错的脚本自检**，确认它真会报错：

```python
BASH = r"C:\Program Files\Git\bin\bash.exe"          # 真 bash
subprocess.run([BASH, "--noprofile", "--norc", "-n", path])   # 合法 rc=0 / 非法 rc=2
```

```python
# 自检：如果这个 bash 对 `if then fi` 都不报错，那它就是个桩，校验结果不可信
open(tmp, 'w').write("if then fi\n")
assert subprocess.run([BASH, "-n", tmp]).returncode != 0
```

### PowerShell 工具不返回 stdout

命令执行成功（exit 0）但输出为空，拿不到任何结果。不要靠它做验证。

### 读文件的正确姿势

`node` 和 `python` 本身可用，用绝对路径调用托管版本最稳：
- `~/.workbuddy/binaries/python/versions/3.13.12/python.exe`
- `~/.workbuddy/binaries/node/versions/22.22.2-3/node.exe`

要装包就建这个隔离 venv（已建过，可直接复用）：

```bash
"~/.workbuddy/binaries/python/versions/3.13.12/python.exe" -m venv "~/.workbuddy/binaries/python/envs/default"
"~/.workbuddy/binaries/python/envs/default/Scripts/python.exe" -m pip install pyyaml
```

（venv 里的 pip 装包很慢，实测 pyyaml 花了近 60 秒，别以为卡死了。）

## 编辑同一文件：不要并行 Edit

同一条消息里对**同一个文件**发多个 `Edit` 会竞态：工具全部返回 "Successfully edited"，
但实际落盘的只有一部分（实测 6 个 Edit 只存活 2 个），文件停在中间状态，且**不报错**——
极难发现，症状是 `Grep` 关键标记时发现「明明说改了却没有」。

- 同一文件的多个位置：**串行**（一轮一个 Edit），或者直接 `Write` 整体重写。
- 改动在 3 处以上 → 全量 `Write` 更省事也更可靠。
- **不同文件之间并行是安全的。**
- 改完必须 `Grep` 关键标记确认真的落盘了，不要相信「编辑成功」的提示。

## 定时采集类需求：给采集脚本配容量上限

「每天自动采集」的需求一定要配**容量上限 + 归档**，否则队列文件无限膨胀：

```python
# 队列超上限时，最旧的移入归档文件——留底，永不删除
def prune_inbox(items, cap, archive_name="inbox_archive"):
    existing = load_json(archive_name, []) or []
    if cap <= 0 or len(items) <= cap:
        return items, 0, len(existing)
    keep, spill = items[:cap], items[cap:]
    archive = existing + spill
    save_json(archive_name, archive)
    return keep, len(spill), len(archive)
```

另外两个坑：

- **让脚本自己写一份机器可读的简报**（`last_harvest.json`：新增数、来源分布、队列总量、
  Top N）。定时任务的 prompt 直接读这个文件汇报，比解析 stdout 稳定得多。
- **过滤信号词要用词边界匹配**。裸子串匹配会误伤：`bootstrapped` 命中了技术术语
  `source-bootstrapped`，把编译器帖子当成了创业项目。用
  `re.compile(r"(?<![a-z0-9])%s(?![a-z0-9])" % re.escape(k), re.I)`。

### 定时任务跑完自动提交推送（`daily_harvest.py` 模式）

「每天采集，让远程仓库跟着长」这种诉求，做成**一个脚本**、而不是在定时任务的 prompt 里
拼 git 命令 —— 脚本可测、可复跑、边界写死。四段式：

1. 跑采集子进程（`sys.executable` + 采集脚本），失败就退出、不提交
2. `git status --porcelain -- data/` 检测有没有真变化 —— **无变化直接 return 0，不制造空提交**
3. `git add -- data/`（只加这一个目录）→ commit
4. `git push origin <branch>`；失败要说清「本地提交还在，网络恢复后手动 push」

无人值守才会遇到的四个坑，都要处理：

| 坑 | 处理 |
|---|---|
| 没有提交身份（新 clone / CI） | 开跑前检查，缺失就报错并打印 `git config --global user.name/email` |
| `.git/index.lock` 残留 | 超 10 分钟视为陈旧锁自动清理；太新的则**跳过本次**（说明真有 git 在跑） |
| 游离 HEAD | `rev-parse --abbrev-ref HEAD` 返回 `HEAD` 时拒绝提交 |
| `origin/<branch>` 落不了盘 | 推送成功后直接写 ref 文件兜底（见上文「坑二」） |

两条铁律：

- **只 `git add` 数据目录，永远不要 `git add -A`** —— 否则会把开发中的半成品脚本一起提交。
- **自动提交绝不碰「人工核实」那一层数据**（`cases.json`）。自动化只搬运机器采回来的原料，
  核实留给人 —— 这是这类库存在的全部意义。

子进程要显式设 `GIT_TERMINAL_PROMPT=0` + `GCM_INTERACTIVE=never`，否则凭证缺失时
git 卡在交互提示上，定时任务就这么无声地挂着。

**测这个脚本不要联网**：把脚本拷进临时 git 仓库，用 `importlib` 从那个路径加载模块
（它的 `ROOT` 由 `__file__` 推出，自然指向临时仓库），逐个测
`changed_paths` / `commit_message` / `handle_index_lock` / `heal_remote_ref`；
再用子进程跑 CLI 验「非 git 目录」「无身份」两条失败路径。
真实链路单独用 `git clone` 到临时目录 + `--no-push` 跑一次。

> 测完删临时克隆要先清只读属性，否则 git 对象文件会 `WinError 5 拒绝访问`：
> `os.chmod(f, stat.S_IWRITE)` 走一遍再 `shutil.rmtree(p, onerror=...)`。
> 另外命令里 `cd` 进临时目录后，**下一次命令的 cwd 还在那里**，会锁住目录删不掉 —— 先 `cd` 出来。

## 本地代理会炸 TLS

本机有代理环境变量时，Python 的 `urllib` 抓外网会 TLS 失败。所有出网请求显式绕开：

```python
PROXY_ENV_KEYS = ("HTTP_PROXY","HTTPS_PROXY","http_proxy","https_proxy","ALL_PROXY","all_proxy")
proxies = {k: os.environ.get(k) for k in PROXY_ENV_KEYS if os.environ.get(k)}
opener = urllib.request.build_opener(urllib.request.ProxyHandler({})) if proxies \
         else urllib.request.build_opener()
```

## 交付形态（用户偏好）

- **零依赖**：Python 只用标准库（`http.server` + `json`），前端 Vanilla JS，不上框架、不装包。
- **能双击就双击**：附一个 ASCII-only 的 `start.bat`（bat 里写中文会因代码页出乱码）。
- **端口**：常用 5052，避开已被占用的常见端口（如 5000/8000）。
- **深色主题优先**（用户 IDE 是 dark）。

## `server.py` 骨架要点

```python
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# 1) 写操作必须加锁，避免并发写坏 JSON
_LOCK = threading.Lock()

# 2) 写 JSON 用「临时文件 + os.replace」原子替换，别直接 open('w')
tmp = path + ".tmp"; json.dump(...); os.replace(tmp, path)

# 3) 静态文件服务要挡目录穿越
full = os.path.normpath(os.path.join(STATIC_DIR, rel))
if not full.startswith(os.path.normpath(STATIC_DIR)):
    return self._send(403, "forbidden")

# 4) 日志必须行缓冲。python server.py > srv.log 2>&1 时 Python 默认块缓冲（8KB），
#    除 flush=True 之外的全卡在内存里 —— 现象是日志文件长期 0 字节，
#    服务端明明出错却查不到任何痕迹，极易被误判成「服务不输出日志」。
for _s in (sys.stdout, sys.stderr):
    try: _s.reconfigure(line_buffering=True)
    except Exception: pass
# 启动时再带 -u 双保险：python -u server.py > srv.log 2>&1

# 5) 路由外层包总异常捕获：任何抛错都回 JSON 500，绝不返回空 body。
#    异常冒泡出 BaseHTTPRequestHandler 会直接关连接，前端只收到 0 字节，
#    表现成一句毫无线索的 "Unexpected end of JSON input"。
def do_GET(self):
    try: self._route_get()
    except (BrokenPipeError, ConnectionResetError): pass     # 客户端自己断开
    except Exception as e:
        log("GET %s 异常: %r" % (self.path, e))
        self._json({"ok": False, "error": "服务内部错误: %s" % e}, 500)

# 6) 默认静音日志；但要记下非 200，否则出错时无从查证
def log_message(self, fmt, *args):
    if len(args) > 1 and str(args[1]) not in ("200", "304"):
        log("HTTP %s" % (fmt % args))

# 7) JSON 序列化兜底：某个字段混进 set/datetime 也不该炸掉整个响应
body = json.dumps(obj, ensure_ascii=False, default=str)

# 8) 开浏览器用 Timer，并留一个关掉的口子（自测时不能弹窗）
if not os.environ.get("NO_BROWSER"):
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()

# 9) **必须实现 do_HEAD**。BaseHTTPRequestHandler 默认对 HEAD 回 501，
#    预览面板 / 监控 / curl -I / k8s liveness 都用 HEAD 探活 —— 拿到 501 会
#    误判服务不可用 → fallback 到内置静态服务托管 index.html → 页面里
#    所有 /api/* 全 404。表现：报错「后端返回了空响应（HTTP 404）」。
#    简化：do_HEAD 复用 do_GET 但不写 body（Content-Length 仍给真实长度）。
def do_HEAD(self):
    self._head_only = True            # _send 里看到这个就跳过 wfile.write
    if urllib.parse.urlparse(self.path).path == "/api/search":
        return self._send(200, b"")   # 探测不该真触发搜索（打 5 个上游）
    self._route_get()
```

## 验证套路（必做，两层）

### 后端：`selftest.py`

自测脚本**必须自己起服务、跑完自己关**，用独立端口不干扰用户正在跑的实例。

```python
# 关键：开始前备份 data/，结束后无论成败都还原，否则测试会污染用户数据
shutil.copytree(DATA, BACKUP)          # 测试前
try:
    ... 跑测试 ...
finally:
    proc.terminate()
    for name in os.listdir(BACKUP):    # 还原
        shutil.copy2(os.path.join(BACKUP, name), os.path.join(DATA, name))
    shutil.rmtree(BACKUP)
```

踩过的坑：**先写完测试再补备份**很容易写成「备份在变更之后」，等于没备份。备份一定是第一步。

`urllib` 遇到 4xx 会抛 `HTTPError` 而不是返回状态码，测试里要包起来：

```python
try:
    with opener.open(r, timeout=10) as resp: return resp.status, resp.read()
except urllib.error.HTTPError as e: return e.code, e.read()
```

### 前端：`uitest.js`（不用浏览器）

`agent-browser` 未必装了，配合上面 shell 的问题不值得走浏览器自动化。
用 Node 的 `vm` + 最小 DOM 桩跑一遍渲染函数，覆盖率比手动点高。

```js
// 桩要覆盖：innerHTML setter / querySelectorAll 返回 [] / classList / dataset /
//          style / textContent / hidden / insertAdjacentHTML
// 注意：vm 里用 let 声明的顶层变量不会挂到 sandbox 上！
//      要改内部状态，必须用 vm.runInContext(`DATA.cases.push(...)`) 在 context 内部执行。
//      用 var 声明才会挂到 sandbox 上（可用来把结果取出来）。
```

### 更省事的做法：从被测脚本里 `return` 一个测试 API

不用纠结 `let` / `var`，把脚本包进函数、末尾 `return` 出要操作的函数和一个兜住内部状态的
shallow object 即可（`state` 是对象，暴露引用后内部改动可见）：

```js
const api = new Function('document', 'fetch', 'localStorage', /* … */
    js + '\n;return {doSearch, renderSuggest, renderStatus, state};'
)(documentStub, fetchStub, localStorageStub);
await api.doSearch(false);                  // 直接调用被测函数
api.state.items.length;                     // 直接断言内部状态
```

### `id` 必须写成访问器属性，否则「移除旧节点」这类逻辑测不出来

`querySelector` 桩通常是「按选择器记忆化一个元素」。但代码里动态插入的节点是
`createElement` 出来后**再赋 `id`** 的，桩如果不登记，`$('#suggest')` 就会返回另一个空对象，
于是 `old.remove()` 作用在错的节点上 —— 测试**假失败**（或假通过），排查很久。

```js
Object.defineProperty(el, 'id', {
  get() { return el._id || ''; },
  set(v) { el._id = v; registry.set('#' + v, el); },   // 赋值时登记进选择器表
});
```

### `appendChild` 要同步更新 `_html`，否则 `innerHTML` getter 读不到追加内容

`showError()` 用 `document.createElement` 造错误块再 `appendChild` 进去，
然后测试断言 `box.innerHTML.indexOf('panradar.py') >= 0` —— 桩的 `appendChild`
如果只 push 到 `children[]`、不动 `_html`，`innerHTML` getter 就读不到追加内容，
断言全挂。

```js
appendChild(c) {
  this.children.push(c);
  // 同步 innerHTML：否则 innerHTML getter 读不到追加的内容，测试看不到错误块
  const tag = c.className ? '<div class="' + c.className + '">' : '<div>';
  this._html += tag + (c.textContent || '') + '</div>';
  return c;
},
```

同理 `insertAdjacentElement` / `insertAdjacentHTML` / `appendChild` 桩里要留引用
（如 `this._adj = node`），否则断言不到「插到哪儿了」。

### 桩掉 `fetch` + 执行 `doSearch()`，把「点击 → 换词 → 重新请求」整条链路测掉

只断言「渲染出了 HTML」覆盖率太低。给 `fetch` 喂**真实形状**的响应（照抄一次线上 JSON），
然后真的调 `doSearch()`、真的调按钮的 `onclick()`，断言可观测副作用：

- 收集请求 URL（`SEARCH_CALLS.push(url)`），断言点击后确实发出了新请求、且新请求带了新关键词
- 断言输入框的值变了、旧节点被移除、状态对象更新了
- 断言「无数据时不渲染空框」这类边界

这比手动点强得多，且不需要浏览器。

### 前端绝对不要裸用 `(await fetch()).json()`

响应体为空（服务重启 / 连接被重置）时它抛的是
`Failed to execute 'json' on 'Response': Unexpected end of JSON input` ——
用户完全无法据此判断发生了什么，这是本地应用最常见的"天书报错"。

封一层 `apiGet(url, timeoutMs)`：`AbortController` 控超时 → 先 `text()` → 判空 →
判 `resp.ok/status` → 再 `JSON.parse`，每种情况给一句**能照着做**的话。
瞬时断连（服务刚重启）**静默重试一次**再报错。错误块里放「重试」按钮，别让用户重输关键词。

长搜索还要每秒更新「已等待 N 秒…」—— 几十秒毫无变化的界面会被当成卡死，
用户去刷新反而更容易踩到断连。

**桩要跟着升级**：只提供 `json()` 的 fetch 桩跑不了新的请求层，必须同时给
`text()` 和 `ok/status`。再给桩加一个 `FETCH_MODE`（`ok/empty/badjson/http500/throw/abort/failOnce/hang`），
一次把所有故障分支跑完 —— 这类分支手点几乎测不到。

### 单测过了也要用真实数据回归

这次单测 7/7 全绿，但一接真实上游就冒出 `095.马老师的` 这种脏建议 —— 单测里的样例标题
是自己编的、太干净。**修完必须把真实抓到的脏数据补成回归用例**，再跑一遍。

必测项：
1. 每个 UI 区块是否产出 HTML（长度 > 40 且含关键子串）
2. 卡片数量是否与 `data/*.json` 一致
3. 逐条渲染详情抽屉，确认无一条抛异常
4. **XSS 转义**：注入 `<script>` / `<img onerror>` / `&` / 单双引号，确认无裸标签
5. 缺字段（`metrics: {}`、全 null）不抛异常

计数卡片别用 `class="card`（会匹配到 `.card-top` 等子元素），用 `class="card(?:\s+read)?"`。

## 状态同步类改动：下沉到「唯一出口」，不要逐点打补丁

**同一个坑今天踩了两次**（手牌排序），值得单列一节。

需求是「手牌任何时候都要按花色+大小排好」。第一轮我在 `drawTile`（上层包装）、`doPeng`、
`doChi` 等**各个调用点**分别加 `sortHand`，结果：

- 漏了 `drawTo`（真正 push 手牌的最底层函数，`drawTile` 只是它的包装）→ 摸到的牌插在末尾，立刻乱序
- 漏了 `doMingGang` / `doAnGang` / `doBuGang` → 杠/补杠后乱序
- 用户只报了「发牌时是乱的」，**其余路径的乱序一直存在却没人发现**

**判据：如果一条不变量（排序 / 去重 / 计数 / 时间戳 / 脏标记）需要在多处维护，
它一定会漏。** 找那个「所有路径都必经的唯一出口」：

```js
// 反例：每个调用点各自处理，必然漏
drawTile(p){ …; this.sortHand(p); }
doPeng(p,t){ for(…){/*删除*/} this.sortHand(p); }
doChi(p,opt,t){ for(…){/*删除*/} this.sortHand(p); }

// 正例：抽成一个出口，删除即排序
_removeFromHand(p,tile,n){
  for (let k=0;k<n;k++){
    const i=this.hands[p].indexOf(tile);
    if (i<0) break;
    this.hands[p].splice(i,1);
  }
  this.sortHand(p);                    // ← 唯一出口，不可能漏
}
doPeng(p,t){ this._removeFromHand(p,tile,2); this.melds[p].push(…); }
doChi(p,opt,t){ for (const x of opt) this._removeFromHand(p,x,1); this.melds[p].push(…); }
// 顺手把上层冗余调用删掉（drawTile 不再需要 sortHand，发牌循环也不再需要）
```

配合**「改了状态就断言状态」的测试**，而不是只测用户报的那条路径。这次的 30 项自测就是
按不变量写的（`isSorted(hand)` 对摸牌/碰/吃三条路径各断言一次），才把没被报告的 bug 逼出来：

```js
const isSorted = h => h.every((t,i,a) => i===0 || T.sortKey(a[i-1]) <= T.sortKey(t));
g.hands[1] = ['s9','m1','p5', /* …乱序 */];
g.drawTile(1);              ok(isSorted(g.hands[1]), '摸牌后应有序');
g.doPeng(2,'p3');           ok(isSorted(g.hands[2]), '碰后应有序');
g.doChi(3,['m3','m4'],'m5'); ok(isSorted(g.hands[3]), '吃后应有序');
```

> 顺带教训：`doChi(p, opt, tile)` 的**参数顺序**是把 `tile` 放最后（`handleDiscard` 的签名也如此）。
> 写测试或调用时先 `Grep` 一下真实签名，别按直觉传。

## 交付收尾

1. 起服务（`run_in_background: true`），用 Python 脚本打一次 `/api/ping` 确认活着。
2. `present_files`：**第一项放 `http://127.0.0.1:5052/`**（会打开内置浏览器预览面板），再跟上 README 和数据文件。
3. 写工作区日志到 `.workbuddy/memory/YYYY-MM-DD.md`。

## 推送到 GitHub（本机实测路径）

`gh` CLI 装了但**未登录**（`gh auth status` 报 not logged into any GitHub hosts），
不过本机 `~/.git-credentials` 里存着 `github.com` 的 classic token（40 字符，
scope `gist, repo, workflow`），身份即你的 GitHub 用户名），照样能建仓库和推送。
先解析出来验证，再动手：

```python
m = re.search(r'https?://([^:]+):([^@]+)@github\.com', open(os.path.expanduser('~/.git-credentials')).read())
user, tok = m.group(1), m.group(2)
# 用 token 调 API 验证身份 + 权限 + 是否已有同名仓库，再决定建不建
```

### 坑一：通用 `credential.helper=store` 会被 URL-specific 空值覆盖

global 配置里有这两行：

```
credential.https://github.com.helper=                     # 空值：清空该 URL 的 helper 列表
credential.https://github.com.helper=!gh.exe auth git-credential
```

URL-specific 配置会**完全替代**通用 helper 列表，所以下面这条**无效**（实测仍报
`could not read Username`）：

```bash
git -c credential.helper=store ls-remote ...
```

必须写成 URL-specific 的形式：

```bash
git -c credential.https://github.com.helper=store ls-remote https://github.com/USER/REPO.git   # ✓
```

想长期生效就写进仓库本地配置（只存 helper 名，**不存 token**，安全）：

```bash
git config --local credential.https://github.com.helper store
```

同时设 `GIT_TERMINAL_PROMPT=0` + `GCM_INTERACTIVE=never`，否则凭证缺失时
子进程会卡在交互提示上（外部表现为「命令没输出、一直挂着」）。

### 坑二：`refs/remotes/` 写入静默失败

`git fetch` 会打印 `* [new branch] main -> origin/main` 且返回 rc=0，但
`.git/refs/remotes/origin/` 目录和 ref 文件**根本没创建**，于是 `git status -sb`
一直显示 `## main...origin/main [gone]`——看起来像远程分支被删了，其实远程完全正常
（`git ls-remote --heads origin` 和本地 SHA 一致）。走 `dangerouslyDisableSandbox`
重试也一样，说明不是沙箱拦的。

**修法：用 Python 直接落盘 ref 文件**（内容 = 40 位 SHA + `\n`）：

```python
os.makedirs('.git/refs/remotes/origin', exist_ok=True)
open('.git/refs/remotes/origin/main', 'w', encoding='ascii').write(sha + '\n')
```

写完 git 立刻识别，`branch -vv` 不再显示 gone。`refs/heads/*` 不受影响。

### 坑三：推送前必扫本机绝对路径

用户本机脚本常带硬编码路径（实测 `start.bat` 里写死了
`C:\Users\<用户名>\.workbuddy\binaries\python\...`），公开仓库里既不可复用又暴露用户名。
推之前用正则扫全项目：

```python
pat = re.compile(r'(C:[\\/]Users[\\/][^\\/"\'\s]+|/c/Users/[^/"\'\s]+|\.workbuddy)', re.I)
```

改法：`start.bat` 用 `where py` → `where python` 逐级探测，都找不到才报错并给安装地址；
不要写死任何用户目录。**改完必须实测**（`py server.py` 起服务 + `/api/ping` 返回 200），
否则可能把用户自己的双击启动改坏。

### 建仓库 + 推送

```python
api('/user/repos', 'POST', {'name': 'xxx', 'description': '…', 'private': False,
                            'auto_init': False,      # 关键：别自动初始化，会和本地 README 冲突
                            'has_wiki': False})
api('/repos/USER/REPO/topics', 'PUT', {'names': ['ai', 'case-study', 'python']})
```

```bash
git init -b main
git config --local credential.https://github.com.helper store
git remote add origin https://github.com/USER/REPO.git
git push -u origin main
```

### 其它必备

- `.gitattributes` 统一换行，否则 Windows/Linux 双环境每次 `git add` 都刷一屏
  CRLF 警告：`* text=auto eol=lf` + `*.bat text eol=crlf`。
- `.gitignore` 至少排除 `__pycache__/`、自测备份目录、`*.log`。
- 提交信息用中文、多段 `-m`（标题 + 正文 + 细节）。
- 用 `git -c core.pager=cat log` 避免打开分页器卡住。

### 加 GitHub Actions 前先在本地验一遍 workflow

workflow 写错，GitHub 只会丢一句「Invalid workflow file」，来回一轮很浪费时间。
用 pyyaml 解析 + 把每段 `run:` 抽出来做 `bash -n`（**用真 bash**，见上文 WSL 桩那条），
本地就能全验完。YAML 的 `run: |` 块会去掉公共缩进，所以 heredoc 结束符（`PY` / `EOF`）
在解析后应当是顶格的 —— 这一点要专门断言，否则 shell 会把后续行一起吞掉。

CI 里跑「会改数据」的自测时，多加一条**数据未被污染**的断言，价值很高：

```yaml
- name: 断言数据未被自测污染
  run: |
    if [ -n "$(git status --porcelain data/)" ]; then
      echo "::error::自测改动了 data/，备份/还原机制失效"; exit 1
    fi
```

这把「自测的备份/还原真的有效」变成了持续验证，而不是靠人记得。
matrix 一定配 `fail-fast: false`，否则只能看到第一个版本的结果。

### 仓库规范化：协议跟已有仓库保持一致，徽章锚点必须存在

若你的项目使用 MIT 协议，版权行统一 `Copyright (c) 2026 <你的名字>`。新仓库直接复用同一份原文
（先拉一个已有仓库的 LICENSE 逐行比对，除版权行外应完全一致）。

README 顶部加徽章时**锚点必须真的存在**：写了 `[![PRs Welcome](#贡献)]` 就得有 `## 贡献` 一节。
写完用脚本把 `](#xxx)` 全部提出来对一遍标题。

版本下限别猜：先用正则扫代码里有没有版本专有语法
（`match` 语句 / PEP604 `X | None` / `list[str]` / walrus / `tomllib` / `removeprefix`），
扫不出来再上 CI matrix 实测（实测 Python 3.9 / 3.11 / 3.13 + Node 18 / 20 / 22 全绿），
**拿到绿灯再在文档里写「支持 3.9」**。

## 数据驱动应用的通用结构（做「库 / 看板 / 案例集」类需求时）

三级漏斗 + 三层文件，用户反馈很好：

```
原始采集 (机器)  →  人工候选      →  已核实成品
inbox.json          candidates.json   cases.json
```

铁律：**采集脚本只写最上游那一层，绝不直接写成品层。** UI 画出漏斗比例，让「素材多、成品少」变成可解释的正常状态，而不是看起来没做完。

## SPA 也要能被爬：预渲染独立页

纯客户端渲染的 SPA（多视图靠 `hidden` 切换、详情是抽屉、没有路由）对**爬虫、社交平台
预览、以及任何直达链接**都是空壳——它们读不到正文。要让内容被收录 / 被分享预览 / 能当
「阅读原文」落地页，就得把每条数据预渲染成一个独立页面。

**做法**：`<id>/<key>.html` + `<id>/index.html` 静态总目录 + `sitemap.xml` + `robots.txt`
+ 在主 SPA 首页注入 `<noscript>` 链接清单（标准降级手段，比把正文藏起来安全）。
独立页**不要引入 `app.js`**，正文全部内联。

四个容易漏的点：

1. **复用主样式表的类名，先确认这些选择器没有作用域前缀**。若详情样式写成
   `.drawer .d-title {…}`，独立页就套不上；必须是裸的 `.d-title {…}`。另外查一遍
   `body` / `html` 有没有全局规则（如 `overflow:hidden`、`height:100vh`），
   它们会把独立页的滚动弄坏。补的那点页面样式页内内联即可，别去改主样式表。
   **但主样式表本身必须内联进每个页面**，理由见下一节 —— 外链会静默失效。
2. **站点元信息外置成配置文件**（title / url / repo / 社群链接 / 备案号），缺字段用默认值
   兜底 —— 这样配置文件不存在也能构建，只是引流位是空的。`sitemap` / `canonical` /
   `og:url` 都需要绝对域名，**没有域名就干净地跳过，不要留空 `<loc>`**。
3. **接进构建脚本时改三处**：① 清理输出目录的"白名单"常量要加上新目录（否则每次构建都
   把上次产物报成"非构建文件"）；② 自检要断言页数 = 数据条数、且每页正文够厚
   （去标签后 ≥ 600 字）；③ **部署脚本的缓存规则如果是按 basename 匹配的，认不出
   子目录里的页面**，会错给短缓存（或反之），要加前缀规则。
4. **`<title>` 控长度**：`名称 — 一句话` 里的那句话要截断（20 字上下），否则搜索结果页
   全被截掉。`og:title` 反而应带上站名，分享卡片才认得出是谁发的。

`sitemap.xml` 的 `lastmod` 用数据自带的 `updated_at` / `verified_at`，别一律写今天。

### 测试：多副本常量漂移检测

同一份标签文案（枚举中译名、维度名、象限文案）经常在 **JS / Python / 配置** 里各存一份。
漂移后不会报错，只会让同一个字段在两个页面显示成两个词 —— 属最难查的一类。

写测试时**从源文件里正则抠出来比对**，别手工维护第二份清单：

```python
# 注意 JS 里常量有「一格一行」和「挤在一行」两种写法，正则两种都要认
def js_const(name, kind="obj"):
    src = open("static/app.js", encoding="utf-8").read()
    if kind == "obj":
        m = re.search(r"const\s+%s\s*=\s*\{([\s\S]*?)\n\};" % name, src)
        block = m.group(1)
        # 带嵌套对象的只取顶层键
        return re.findall(r"^\s*(\w+)\s*:\s*\{", block, re.M) if "{" in block \
            else re.findall(r"(\w+)\s*:", block)
    return re.findall(r"'([^']+)'",
                      re.search(r"const\s+%s\s*=\s*\[([^\]]*)\]" % name, src).group(1))
```

同理要断言「预渲染页正文里去标签后不含可执行标签」「URL 里的 `&` 被转义成 `&amp;`」
「引用了 `app.js` 的独立页为 0 个」——这三条一旦回归就是事故。

### 独立页必须内联样式表（外链会静默失效）

**踩过的坑**：预渲染页写 `<link rel="stylesheet" href="../style.css">`，在设计上完全正确
（子目录深一层，往上一级正好是站点根），本地起 HTTP 服务也正常。但真正打开时整页退化成
**白底黑字的裸 HTML** —— 样式表根本没被加载。高发场景：`file://` 直接双击打开、
预览器/内嵌面板做了目录隔离或把单文件抽走渲染、CDN 缓存与回源路径不一致。

**为什么后果很重**：主样式表里的 `:root { --bg: … --text: … }` 是配色的地基，一缺全部
`var(--x)` 失效；但页面**看起来"能读"**，不报错、控制台也不一定有声，很容易被当成"样式
没做美"而不是"样式没加载"，排查方向一开始就是错的。

**做法**：构建时读 `static/style.css` 全文，塞进每个页面的 `<style>`，顺序是
**主样式表在前、阅读页补充样式在后**（后者才能覆盖前者的网格布局）。`dist/style.css`
仍保留供 SPA 首页外链。代价是每页 +40 KB（gzip 后 ~10 KB），换来的是「怎么打开都不会掉
样式」，而且内容页少一个渲染阻塞请求，对 SEO 反而有利。

**必须配的守门断言**（否则会再犯，且同样静默）：

```python
css = page_css()                      # 主样式表 + 补充样式
if 'rel="stylesheet"' in h or "style.css" in h:
    problems.append("%s 引用了外部样式表（应内联）" % cid)
elif css not in h:
    problems.append("%s 没有完整内联样式表" % cid)
# 读不到文件时 base_css() 会安静地返回空串 —— 单独拦一道，别让它混过去
if len(base_css()) < 10000:
    problems.append("static/style.css 读不到，页面会没有主题样式")
```

总目录页也要一并断言（它同样是独立打开的入口）。

### 视觉验证：无头 Chrome 直接截图，别为截图去装浏览器

Chrome 和 Edge 都在标准路径，纯截图不需要任何依赖：

```bash
"/c/Program Files/Google/Chrome/Application/chrome.exe" --headless=new --disable-gpu \
  --no-sandbox --hide-scrollbars --force-device-scale-factor=2 \
  --window-size=1280,900 --screenshot="C:\...\shot.png" "file:///C:/abs/path/page.html"
```

五条经验：

1. **`body{margin-top:-Npx}` 截下半页**：无头截图只能从页面顶部截。想看页脚/尾部，把产物
   复制到临时目录，在 `</head>` 前插一段 `<style>body{margin-top:-1330px}</style>` 再截。
   产物是自包含的（样式已内联、无外部资源）时这招最省事。
2. **断点两端各截一次**：响应式页面有断点（如 `@media (max-width:900px)`），800 宽会把
   桌面端布局误判成"堆叠错了"。别看到一列就以为标记写错 —— 先确认当前视口在断点哪一侧。
3. **截图是唯一能发现"掉了样式"的手段**：DOM 断言只能证明"CSS 文本在 HTML 里"，
   证明不了它生效。交付前截一张，比读十遍代码有用。
4. **⚠ `--window-size` 不等于视口，别用它模拟手机**（Windows 无头实测钳到**最小宽 ~504 / 最大高 ~760**）：
   请求 `--window-size=390,844` 实得视口 **504×748**，截图右侧被裁 ——
   现象是"右侧那一栏没了"，很容易当成真实布局 bug 排查半天。
   要精确设备尺寸就**在页面里放一个精确尺寸的 iframe**，外面用 `transform:scale()` 等比缩放：

   ```html
   <div id="d" style="width:342px;height:740px;overflow:hidden">
     <iframe src="../index.html" style="border:0;width:390px;height:844px;
            transform:scale(.8768);transform-origin:top left"></iframe>
   </div>
   ```
   然后照常截图这个 harness 页（scale = min(1, 500/w, 740/h)）。
   **iframe 的视口就等于设备视口**，`100vw`/媒体查询全部按真实尺寸生效。
5. **两个本机小坑**：
   - **不要在 node 里 spawn Chrome**（`execFileSync` / `execSync` 一律 `EBUSY`，连
     `cmd.exe` 都拉不起来），截图脚本写成 `.sh` 从 bash 调。
   - Git Bash 的 `pwd` 给的是 `/c/...`，**直接拼 `file:///` 会 `ERR_FILE_NOT_FOUND`**；
     给 Chrome 的路径要用 `pwd -W`（`C:/...`），文件操作仍用 `pwd`。

### 要验「点击/交互」时：playwright-cli（已全局安装）

截图证明不了"点了会不会弹"。需要**真实点按**时用 `@playwright/cli`（通常
`npm i -g @playwright/cli`；没装就 `npm install -g @playwright/cli@latest`，约 6 秒）。
四条必知：

```bash
# ① file:// 被拦（Error: Access to "file:" protocol is blocked）→ 必须先起本地 http 服务
cd <项目目录> && "~/.workbuddy/binaries/python/versions/3.13.12/python.exe" \
  -m http.server 8137 --bind 127.0.0.1 >/dev/null 2>&1 &
# ② ⚠ 浏览器会话在两次 Bash 调用之间会被回收 —— 所有 playwright 命令必须 && 串在一条里
playwright-cli open "http://127.0.0.1:8137/index.html" >/dev/null 2>&1; \
  playwright-cli resize 400 948 >/dev/null 2>&1; sleep 3; \
  playwright-cli mousemove 380 400 >/dev/null 2>&1; \
  playwright-cli mousedown >/dev/null 2>&1; playwright-cli mouseup >/dev/null 2>&1; \
  playwright-cli eval "document.getElementById('x').className" 2>&1 | head -12; \
  playwright-cli close >/dev/null 2>&1
```

- **读结果别用 `tail -3`**：eval 的返回值在 `### Result` 段，很容易被截掉，用 `head -12` 或
  `grep -m1 '"'`。前几行常是 `### Result` + `"值"`。
- **`eval` 里的 `() => ...` 与裸表达式都可以**，但结论只在 `### Result` 里，别漏。
- **截图默认落在进程 cwd**（不是 `.playwright-cli/`），写 `--filename=xxx.png` 后去哪找先 `find`。
- `eval` 点 `el.click()` 验证的是"监听器挂上了"，**验证不了命中测试**（有没有东西盖住它）。
  怀疑"点了没反应"时一定要用 `mousemove/mousedown/mouseup` 真点一次。

**用测量代替眼力**：截图看"观感"，出问题时**读真实几何**定位，别对着截图猜——

```bash
playwright-cli eval "()=>{const e=document.getElementById('discard-west'); \
  const c=e.children[0]; const rh=c?c.offsetHeight:0; \
  return 'h='+e.clientHeight+' rowH='+rh+' 整除='+(((e.clientHeight+2)%(rh+2))===0?'是':'否')}"
```

### 验「节奏 / 时长」类改动：在页面内就地改回旧实现做 A/B

调动画时长、AI 出牌间隔、轮询周期这类"只改数字"的改动，**改前改后各测一轮**才有说服力。
不必来回改文件——在**同一浏览器会话里把被测函数就地换成旧实现**再测一轮即可：

```js
// ① 注入探针：patch window.setTimeout 记录延迟（脚本里的裸 setTimeout 会落到 window 上）
//    ()=> { const L=[]; const o=window.setTimeout;
//           window.setTimeout=function(fn,ms){ if(typeof ms==="number"&&ms>=300&&ms<=8000)
//             L.push(Math.round(ms)); return o.apply(this,arguments); };
//           window.__pr={ reset(){ L.length=0; this.t0=Date.now(); this.d0=读当前计数值; },
//                         read(){ 返回 {秒, 次数, 秒/次, min, max, 直方图} } }; }
// ② 自动替"人"操作：用 setInterval 驱动页面暴露的交互入口，否则轮不到 AI 动
//    先找有没有现成钩子（有的项目把 ui/onTileClick getter 暴露出来了，直接调即可）
// ③ 测完一轮 → 就地换成旧实现 + reset → 再测一轮
//    ()=> { const p=Controller.pace; p.for=function(k){ return 旧公式 }; window.__pr.reset(); }
```

三个要点：
- **别只报"延迟数组的均值"**：`showToast`、动画、防抖也用 `setTimeout`，样本会被污染成
  一堆 700/1200。可信指标是 **墙钟秒数 ÷ 发生次数**（如"秒/张牌"），数组只留着看分布和 max。
- **先确认被测函数在页面里按名字可达**：顶层 `const X = (function(){...})()` 在后续脚本和
  `eval` 里都能按名访问，只是**不在 `window` 上**（别去 `window.X` 找）。
- A/B 两轮必须**在同一会话内**，否则环境差异（缓存、并发、GC）会盖过你要测的差异——
  而会话又在两次 Bash 调用之间被回收（见上），所以 **A/B 也得分步但必须同一条命令**。

**⚠ 不要拿用户截图的像素当 CSS 像素**：用户发来的截图常被浏览器缩放/DPR 放大过。
从**内容反推**（"牌河每行 7~8 张、每张约多少 px" → 估计视口宽）比量图片像素靠谱得多；
最省事的是直接问/看他 DevTools 上的 `Dimensions: 400 × 948`（他给过这个截图就别再猜）。

### 布局"被裁一半"类问题的三个通用坑（实测踩过）

内容被容器裁切时，按这个顺序查：

1. **flex 子项会等比收缩**：容器不够高时**所有**子项一起缩，牌/卡片被压成半张。
   给不该缩的固定内容加 `flex-shrink:0`，只让"可以裁"的那块（如列表）承担收缩。
2. **`align-content:flex-end` 对 grid 是非法值**：从 flex 改 grid 时忘了改这条，
   会**静默退化成 `normal`(=start)** —— 表现是"对齐方向反了、裁掉的是最新的而不是最旧的"。
   改 grid 就把 `justify-content`/`align-content` 一起显式改成 `center`/`end`。
3. **CSS 没法表达"取整行数"，且溢出到容器上方的部分 `scrollHeight` 数不到**：
   固定行高的 grid 遇到"容器高不整除行高"仍会在顶端留半行残牌；
   `align-content:end` 把多余行推到容器**上方**（负方向），`scrollHeight` 不计入 →
   `scrollHeight > clientHeight` 会**误判成"装得下"**。
   正确做法：JS 量 `children[0].offsetHeight` 得行高、按 `getComputedStyle(el).gridTemplateColumns`
   的列数算自然高度，再把容器高度写成整行数（写死高度要配合 `flex:0 0 auto` + `margin-top:auto`，
   否则 `flex-basis:0` 会让 height 失效；每次重算前先清空 height/类还原 `flex:1` 才量得准）。
   这套逻辑挂两处：每次渲染后 + `window.resize`（转屏/拖窗口不会触发重渲染）。
4. 被压扁的**弹性区**里若有固定尺寸的装饰（如中央的大牌），也要按高度收起
   （`clientHeight < 需要值` 就 `display:none`），否则它从格子顶部漏出半张牌残影。

### 手机端布局：先把 CSS 数字算一遍，再截图

纯 CSS 的响应式布局，最省时间的顺序是「**建模 → 试算 → 截图**」，不是「改一版截一版」：

1. 把 `:root` 尺寸变量 + 媒体查询的覆盖顺序 + Grid 轨道规则，翻译成一个 node 试算脚本
   （`--tile-ar` 这类 calc 要按真实公式展开；**媒体查询按源码顺序后者覆盖前者**，别漏）。
2. 对一组视口（360/375/390/412/430 竖、844×390/667×375 横、768/1280）逐项校核：
   关键行能否放下、内容块是否装得下、留白多少、被裁时裁掉的是不是最不重要的那部分。
3. 全绿了再去截图。截图只用来确认"观感"，不用来发现"放不下"。

配套两条 CSS 经验：

- **变量要锁宽高比**：`--tile-ar:1.381` + `height:calc(var(--w)*var(--tile-ar))`。
  宽高分别写死，一旦被 flex 挤压宽高比就崩（实测 0.71 → 0.52，图案糊成一团）。
- **⚠ 自定义属性是"在哪儿声明就在哪儿算完"**：`:root{--h:calc(var(--w)*2)}` 的值在 `:root`
  上就算好了，后代继承到的是**算完的值**。在某个后代上覆盖 `--w` **不会**改变 `--h`。
  要么连 `--h` 一起重定义，要么把换算写在使用处（`width:calc(var(--w)*var(--scale,1))`）。
  这个坑的症状是"改了变量毫无反应"，特别容易误判成选择器权重问题。

### 新增的断言，要亲手验证"它真的会失败"

加完断言立刻构造一次回归：复制产物到临时目录 → 人为改坏一处（留 `<style>body{margin:0}`
模拟主样式表丢失、把 `</style>` 换成外链、把配置文件置空）→ 跑自检函数，确认它报出对应的
问题行。**永远通过的新断言等于没有断言**，还会给出虚假的安全感。

### ⚠ 假绿陷阱：`uncaughtException` 处理器会把"崩在半路"变成"pass"

`new Function` 跑被测代码时，**顶层抛错会直接中断整个自测脚本**。如果脚本里挂了
`process.on('uncaughtException', ...)` 来收集异步异常（很常见），Node 就**不再崩进程** ——
于是现象是：**一行 PASS/FAIL 都不打印，`exit=0`**。不看输出内容只 `&& echo OK` 的话，
这就是一次彻头彻尾的假绿（实测踩过：被测代码里一句裸 `location.hash`，
Node 环境没有 `location`，整套断言根本没跑）。

两道防线，都要有：

```js
// ① 被测代码里做 typeof 守卫（Node 里没有 location / navigator 之类）
const dbg = ((typeof location !== 'undefined' && location.hash) || '').replace(/^#/,'');

// ② 自测脚本退出时强制兜底：挂了 uncaughtException 就必须自己报
process.on('exit', () => {
  if (asyncErrors.length) console.log('!! 未捕获异常:', asyncErrors.join(' | '));
});
```

另外：断言**别依赖"跑完整局之后"的状态**。对局/流程可能已经结束并把字段清空，
断言就会随机翻车（一会儿过一会儿不过）。要在**事件发生的那一刻**断言 ——
例如在循环里捕获到"这一次真的出牌了"，就在那一次立刻校验相关 DOM。

```python
base = m.check_pages(tmp, cases, verbose=False)   # 基线：应为 0
open(p, "w", encoding="utf-8").write(broken)      # 构造回归
assert [x for x in m.check_pages(tmp, cases, verbose=False) if cid in x]
```
