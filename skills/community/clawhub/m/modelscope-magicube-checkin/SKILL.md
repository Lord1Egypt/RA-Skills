---
name: modelscope-magicube-checkin
slug: modelscope-magicube-checkin
displayName: 魔搭魔粒每日自动领取
version: 1.3.3
visibility: public
category: dev-programming
subCategories: [dev-script]
description: 自动领取魔搭（ModelScope）每日发放的魔粒（Magicube）算力额度。通过 Chrome DevTools Protocol 连接你自己已经打开的浏览器，在页面上点击「领取」按钮，并以余额前后差值作为唯一成功判据（余额没变一律记 UNKNOWN，不报成功）。不调用非公开接口，不修改浏览器文件，不启动或结束任何浏览器进程；只操作 modelscope.cn 域名下的页面，点击前在页面内原子复核 host（校验与点击同一次 JS 执行，标签页离开魔搭就一个按钮都不点）。含人工登录一次的说明、四态判据机、故障处置表与本地自测脚本。当用户说「领魔粒」「魔搭签到」「魔粒余额」「魔搭自动登录」「ModelScope checkin」「魔粒够不够」时使用。
agent_created: true
---

# 魔搭魔粒每日自动领取

## 概览

魔粒（Magicube）是魔搭 API-Inference 的算力额度。每日登录魔搭后，**必须到魔粒页点「领取」** 额度才会到账。

本 skill 用 Chrome DevTools Protocol 连接**你自己已经打开的 Chrome**，在页面上点「领取」按钮，并**以余额变化作为唯一成功判据**。脚本零第三方依赖（只用 Python 标准库），随 skill 一起分发。

## 能力边界（先看这段，能省掉很多误解）

这个脚本**只做一件事**：在已打开的浏览器页面里点一下「领取」按钮。

它**不做**以下任何事：

- ❌ 不启动、也不结束任何浏览器进程（浏览器窗口归你，脚本只连接）
- ❌ 不读写、不删除你浏览器里的任何文件（profile 目录完全由 Chrome 自己管）
- ❌ 不读取、不导出、不解密任何 cookie 或登录凭据
- ❌ 不调用任何非公开接口 —— 只在真实页面上按真实按钮
- ❌ 不修改系统代理、环境变量或任何全局配置
- ❌ 不安装任何依赖包（只用 Python 标准库）

对浏览器唯一的写入就是那一次点击。登录态由你在浏览器里自己完成，脚本只复用它。

## 操作范围：只碰魔搭页面

脚本会**在它连上的那个页面上点按钮**，所以「连上哪个页面」必须被约束住。四道闸：

| 闸 | 位置 | 作用 |
|---|---|---|
| 1. 找 tab 时限定 host | `find_target(..., host_suffixes=["modelscope.cn"])` | 只认 `modelscope.cn` 及其子域的 tab |
| 2. **点击前在页面内复核** | `JS_CLAIM_AND_CLICK` 里的 `hostAllowed()` | **校验与点击在同一次 JS 执行里完成** |
| 3. 点击后复核 host | `_page_host()` | 点击期间页面被导航走 ⇒ 余额判据作废，记 UNKNOWN |
| 4. 后缀防拼接 | `_host_matches()` / `hostAllowed()` | `evil-modelscope.cn`、`a.modelscope.cn.evil.com` 一律拒绝 |

### 🚨 为什么第 2 道闸必须写进 JS 里（而不是在 Python 侧检查）

早先的实现是「Python 侧先读一次页面确认 host，再分两步 evaluate 找按钮、点按钮」。
**校验和点击之间存在时间窗口** —— 用户在这中间把标签页导航到别的站点，
脚本就会「浏览器已经离开魔搭，却还在继续点」。ClawHub 的安全扫描正是点名了这条：
> *"it can continue clicking after a browser tab leaves ModelScope"*

现在的写法把三件事合并进**一次** `Runtime.evaluate`：

```
同一次 JS 执行（中间不 await、不会让出事件循环 ⇒ 不可能被导航打断）
  ① hostAllowed()   —— 读当前 host，过不了就 return，一个按钮都不点
  ② 找「领取」按钮
  ③ 再确认它还是那个按钮 → el.click()
```

⇒ **不存在「校验时在魔搭、点击时不在魔搭」的窗口**。

host 判定要求「完全相等」或「以 `.` + 域名结尾」，因此 `evil-modelscope.cn` 这种
后缀拼接骗不过去。读不到 host（空串）一律拒绝 —— 宁可误伤也不能在不确定的页面上乱点。

页面归属校验失败时脚本**中止且一个按钮都不点**，返回 `UNKNOWN` 并在 detail 里
说明当前 host。

### 🔒 host 只从 `location.hostname` 读，**没有任何可被页面改写的取值点**

2026-11-02 踩过一个大坑：当时为了「让自测能造出非魔搭页面」，给 host 判定加了一个
`window.__msCurrentHost` 覆盖通道 —— 结果它本身就是一个**后门**：任何页面
（包括恶意页面）都能把它设成 `www.modelscope.cn` 来伪装自己。ClawHub 的安全评审
直接点名：

> *"the skill can be tricked into clicking on another website"*

⇒ **可测性绝不能以削弱安全边界为代价**。现在 host 判定只读 `location.hostname`
（页面无法伪造自己的 `location.hostname`），自测改用「真实域名 + 假 DOM」
（`Page.navigate` 到真域名，再 `Page.setDocumentContent` 换内容）来构造场景。

## 何时使用

- 用户说「领魔粒 / 魔搭签到 / 魔粒余额 / 魔搭自动登录 / ModelScope checkin」
- 用户问「今天领了吗 / 还剩多少魔粒 / 够不够跑一轮核验」
- 外部定时任务每日调用一次（脚本幂等，同一天重复跑不会重复领）

## 执行方式

脚本在 skill 目录下的 `scripts/`。拼出 skill 基准目录后执行（Windows 示例）：

```bash
python "<SKILL_DIR>/scripts/ms_checkin.py"
```

| 参数 | 作用 |
|---|---|
| 无参数 | 每日领取：连浏览器 → 点「领取」→ 比对余额 → 写流水 |
| `--login` | 轮询等待你完成登录，成功后自动退出并报余额 |
| `--status` | 只查登录态与余额，不点任何按钮 |
| `--probe` | 打印页面判据 / 魔粒文案 / 正文，排查改版用 |
| `--wait N` | `--login` 时等待登录的秒数（默认 300） |
| `--port N` | CDP 端口（默认 9333） |
| `--profile PATH` | 提示启动命令时用的 profile 目录（默认 `~/chrome-ms-profile`） |
| `--json` | 额外输出一行 JSON 结果，便于程序消费 |

环境变量：`MS_CDP_PORT`、`MS_CDP_PROFILE`、`MS_CHECKIN_LOG`（流水路径，默认 `~/.workbuddy/data/modelscope-magicube/checkin_log.json`）。

**推荐 Python**：`C:\Python315\python.exe`（本机 `WindowsApps\python.exe` 是 App Execution Alias 存根，直跑退 9009）。

## 前置条件：先自己开一个带调试端口的 Chrome

脚本**不会替你启动浏览器**（代用户 spawn 浏览器是高影响操作，也容易误伤你自己开着的窗口）。请自己执行一次：

```bash
# Windows（Git Bash / CMD 都行）——独立 profile，Chrome 136+ 的官方要求
"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe" \
  --remote-debugging-port=9333 \
  --remote-debugging-address=127.0.0.1 \
  --user-data-dir="$HOME/chrome-ms-profile" \
  --no-first-run --no-default-browser-check \
  https://www.modelscope.cn/magicube/usage
```

> 🔒 **为什么默认不带 `--no-sandbox`**：关掉 Chrome 沙箱会显著降低浏览器自身的
>   安全隔离，所以它只是**受限环境**（容器 / 受管沙箱）里 Chrome 启动即退出
>   （exit code 3）时的显式兜底，不是默认动作。真需要时在命令末尾追加即可。
>
> 🔒 **调试端口只绑 127.0.0.1**（上面命令已显式指定），不会暴露到局域网 ——
>   CDP 端口等于对浏览器完全的读写控制权，绝不能监听所有网卡。
>
> 🔒 **独立 profile 是安全边界，不只是兼容要求**：这个实例的 cookie 与日常
>   Chrome 天然分开，脚本看到的东西和你日常浏览的会话不是一份。

端口不通时，脚本会**打印这条可直接复制的命令**并退出，不会替你做任何事。

⚠ **必须用独立 profile**：Chrome 136+ 官方禁止在默认 user-data-dir 上开调试端口，这是设计不是故障。日常 Chrome 的登录态与这个 profile 天然分开。

⚠ **调试端口等于本机完全控制这个浏览器**：只在你信任的机器上开，端口只绑回环（127.0.0.1），用完关掉窗口即可。

## 状态判据（核心，汇报时别弄错）

| 状态 | 含义 | 退出码 | 汇报口径 |
|---|---|---|---|
| `CLAIMED` | 点了「领取」且**余额真的增加** | 0 | 「领到了，+N 粒」 |
| `ALREADY` | 没点到按钮，但页面写着「今日已完成」 | 0 | 「今天已经领过了」——**不是新领到，别说成领到了** |
| `LOGGED_IN` | `--status` 专用：登录态正常 | 0 | 「已登录，余额 N」 |
| `NO_LOGIN` | 页面仍有「登录 / 注册」入口 | 2 | 「登录态失效了，需要人工登一次」 |
| `UNKNOWN` | 没找到领取入口 / 点了但余额没变 / 页面没渲染完 | 3 | 「没拿到判据」，**别当失败也别当成功**，让用户看 `--probe` |

🚨 **判据必须是「点了 + 余额变了」**。只判「页面读得到余额」等于只登录不领取也报成功 —— 典型的假绿：日志天天 OK，魔粒一分没多。

🚨 **「余额增加」是 CLAIMED 的唯一充分条件**。点了按钮、页面文案从无变成
「今日已完成」但余额没变 ⇒ 记 `UNKNOWN` 而**不是** `CLAIMED`：那只是延迟到账的
*可能*，不是领取成功的证据。未经核实就报成功，会让定时任务把「没领到」误当成
「领到了」。判据逻辑集中在 `scripts/ms_checkin.py` 的 `classify()`，自测里有
7 条用例钉死它（含「余额减少」「余额读不到」都不能算 CLAIMED）。

## 首次使用：人工登录一次

1. 按上面那条命令启动带调试端口的 Chrome（窗口会一直留着）
2. 在窗口里登录 modelscope.cn（验证码/短信都在那个窗口里）
3. 跑 `python "<SKILL_DIR>/scripts/ms_checkin.py" --login`
4. 脚本每几秒探一次登录态，**登录成功后自动退出**并打印当前余额

⚠ `--login` 最多等 300 秒（`--wait` 可调），**用后台任务方式跑**（例如 `run_in_background`），别在 120 秒超时的前台调用里干等。

## 故障处置

| 现象 | 处置 |
|---|---|
| 提示「调试端口没开」 | 按提示复制那条启动命令，先把 Chrome 开起来 |
| `NO_LOGIN` / 退出码 2 | 在浏览器窗口里登录一次，再跑 `--login` 验证 |
| `UNKNOWN` / 退出码 3 | 跑 `--probe` 看页面到底返回了什么；多半是站点改版或按钮文案变了，按探针输出改 `scripts/ms_checkin.py` 里的 `JS_FIND_CLAIM` 正则 |
| 连不上 CDP 端口 | 确认 Chrome 还在跑、端口号对得上（`--port` 可改）；有残留进程时由你手动关掉，别让脚本去杀 |
| 页面一直转圈 / 打不开 | 浏览器自身的网络问题。本脚本只让**它自己的 urllib** 访问 127.0.0.1 时不走代理，**不碰**你的代理设置 |
| 找不到 Chrome | 装 Chrome 或 Chrome for Testing，或改 `CHROME_CANDIDATES` 加路径 |
| 点了但余额没变 | 可能延迟到账，去页面人工确认一次；确认已到账就把当天流水状态改成 `CLAIMED` |

## 外部定时调用

脚本幂等：同一天重复跑会覆盖当天流水，不会重复领。适合由外部调度器每日调用一次。
⚠ 定时调用前**必须**先把带调试端口的 Chrome 开着 —— 脚本不会自己起它。

## 已知坑（改代码前先读完）

1. **没有官方签到 API**。魔粒的「每日发放」只能通过页面操作获取，任何自动领取脚本都是模拟网页操作 ⇒ 站点改版就失效。所以本脚本走 CDP 真点页面。
2. **不是「登录即到账」，要在魔粒页点「领取」**。这是 2026-10-29 用户侧调研纠正的前提。
3. **Chrome 136+ 拒绝在默认 user-data-dir 上开调试端口**（官方设计）⇒ 只能用独立 profile。这也让登录态与日常 Chrome 自然分开。
4. **一天有两个「领取」按钮**（注册并登录 200 + 绑定阿里云账号 50）。只点第一个会漏领 ⇒ 脚本循环点，最多 5 轮。绑定阿里云那 50 粒需要用户自己在页面上完成 OAuth 绑定，**脚本不代做**。
5. **按钮识别只认短文案的叶子元素**。`<div class="task"><button>领取</button></div>` 里那个 div 的 innerText 也正好是「领取」，会被误当成按钮点掉；`<button disabled>` 的 className 是空的，只看 class 判不出来 ⇒ 必须查 `el.disabled` 属性 + 祖先链。
6. **已点过的按钮靠 `data-ms-clicked` 属性去重**，因为点完按钮文案可能不变（真实页面会变成「今日已完成」）。
7. **脚本不碰浏览器进程和浏览器文件**。profile 里的 SingletonLock 属于浏览器自己的运行期文件，脚本只探测不处理；真被强杀残留卡住时，换一个 profile 目录即可。
8. **访问 127.0.0.1 要绕开系统代理**，否则 WebSocket 会被 10053/10054 重置。做法是用 `ProxyHandler({})` 只让脚本自己的 urllib 不走代理，**不改全局环境变量**。

## 脚本清单

| 文件 | 作用 |
|---|---|
| `scripts/ms_checkin.py` | 主流程（领取 / 登录 / 状态 / 探针） |
| `scripts/ms_cdp.py` | 自包含的最小 CDP 客户端（零第三方依赖，只连不管） |
| `scripts/selftest.py` | 自测：用本地假页面钉死「找按钮 / 点按钮 / 余额判据」三段逻辑，另含域名白名单与页面归属校验 |

改动 JS 判据后跑一次自测：`python "<SKILL_DIR>/scripts/selftest.py"`（41 项，不碰真实账号）。

## 背景：魔粒体系

- 官方中文名「魔粒」/ 英文 Magicube，文档 `modelscope.cn/docs/magicube/intro`
- 单价：轻量 0.5 粒 / 主流 1 粒 / 旗舰 2 粒每次
- 每日额度：登录 200 粒；做任务最高 500/天（绑阿里云 +50、发 AIGC 作品 ×10 +100、收藏/喜欢 ×20 +40、评论 ×2 +10、完善信息 +50）
- 有效期：短期粒 24h、长期粒 90 天，自动先扣临近过期的
- 满额 500 粒 ⇒ 旗舰 250 次 / 主流 500 次 / 轻量 1000 次每天
- 另有账号级 2000 次/天、单模型动态约 200 次/天两道上限，实际可用 = min(额度、单模型、账号级)

## 与 ai-case-library 的关系

项目内早期版本入口：`D:\ai-case-library\scripts\ms_checkin.py`（依赖项目的 `wechat_publish.py` / `chrome_cdp_launch.py`，且会自行启动/结束浏览器进程）。
本 skill 版更完整也更克制：自包含 CDP 客户端、登录轮询验证、两个领取按钮循环、`--status`、自测脚本；**并且不代用户启动或结束浏览器、不动浏览器文件**。判据逻辑两者一致。
