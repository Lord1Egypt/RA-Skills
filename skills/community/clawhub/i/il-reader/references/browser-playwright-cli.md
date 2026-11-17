# 浏览器自动化：playwright-cli

本文件是 `playwright-cli` 的命令参考与本技能的用法约定。**只有需要页面交互、登录态、PDF 或截图时才用浏览器**；静态页面用 `curl`，题库比对不用浏览器。

会话名固定 `ilradar`，与其它技能、其它会话隔离。

## 最小闭环

```bash
playwright-cli -s=ilradar open https://example.com --persistent --browser=chrome
playwright-cli -s=ilradar snapshot           # 读元素 refs
playwright-cli -s=ilradar fill e5 "检索词"
playwright-cli -s=ilradar click e3
playwright-cli -s=ilradar snapshot           # 必须重新验证
playwright-cli -s=ilradar close
```

**四步不变式**：开 → 观察 → 操作 → **再观察**。任何一次点击或输入之后，页面状态都可能变化；不重新观察就继续操作，等于凭记忆猜。

## snapshot 的读法

`snapshot` 默认把 YAML 写进**当前工作目录**的 `.playwright-cli/`，不打印到 stdout：

```bash
playwright-cli -s=ilradar snapshot
cat .playwright-cli/page-*.yml | tail -200
```

输出形如：

```yaml
- generic [active] [ref=e1]:
  - heading "文本工具" [level=3] [ref=e39]
  - link "英文字母大小写转换" [ref=e43] [cursor=pointer]:
    - /url: /daxiaoxie.html
  - textbox "搜索工具" [ref=e51]
```

`ref=` 就是后续操作要用的句柄。**每次 snapshot 的 ref 会重新编号**，不能跨次复用。

想让结果显示到 stdout，在**工作目录**放一个 `playwright-cli.json`：

```json
{ "outputMode": "stdout" }
```

## 命令速查

### 导航

```bash
playwright-cli -s=ilradar open [url]        # 新开会话/浏览器
playwright-cli -s=ilradar goto <url>
playwright-cli -s=ilradar go-back
playwright-cli -s=ilradar go-forward
playwright-cli -s=ilradar reload
```

### 交互

```bash
playwright-cli -s=ilradar click <ref>
playwright-cli -s=ilradar dblclick <ref>
playwright-cli -s=ilradar fill <ref> "文本"
playwright-cli -s=ilradar type "文本"        # 向当前焦点输入
playwright-cli -s=ilradar press Enter
playwright-cli -s=ilradar select <ref> "值"
playwright-cli -s=ilradar check <ref>
playwright-cli -s=ilradar uncheck <ref>
playwright-cli -s=ilradar hover <ref>
playwright-cli -s=ilradar drag <ref> <ref>
playwright-cli -s=ilradar upload <文件路径>
```

### 键盘与鼠标

```bash
playwright-cli -s=ilradar press ArrowDown
playwright-cli -s=ilradar keydown Shift
playwright-cli -s=ilradar keyup Shift
playwright-cli -s=ilradar mousemove 150 300
playwright-cli -s=ilradar mousedown
playwright-cli -s=ilradar mouseup
playwright-cli -s=ilradar mousewheel 0 300
```

### 读取与导出

```bash
playwright-cli -s=ilradar eval "document.title"
playwright-cli -s=ilradar eval "el => el.textContent" <ref>
playwright-cli -s=ilradar screenshot
playwright-cli -s=ilradar screenshot <ref>
playwright-cli -s=ilradar screenshot --filename=out.png
playwright-cli -s=ilradar pdf --filename=page.pdf
```

`eval` 用来取页面给的精确字符串（题名、数字、日期），比从 snapshot 里目视摘取更可靠。

### 多标签

```bash
playwright-cli -s=ilradar tab-list
playwright-cli -s=ilradar tab-new <url>
playwright-cli -s=ilradar tab-select 0
playwright-cli -s=ilradar tab-close 1
```

结果页开新标签时，**按 URL 或标题确认目标标签**，不要按"最后一个标签"猜。

### 登录态与会话

```bash
playwright-cli -s=ilradar open <url> --persistent              # 持久 profile
playwright-cli -s=ilradar open <url> --profile=<目录>          # 指定 profile 目录
playwright-cli -s=ilradar state-save auth.json                 # 存 cookie/localStorage
playwright-cli -s=ilradar state-load auth.json
playwright-cli -s=ilradar cookie-list --domain=example.com
```

`--persistent` 让同一会话跨命令保留 cookie 与登录态。**登录与验证码由用户在原窗口完成**，不要把密码或短信验证码写进命令。

### 诊断

```bash
playwright-cli -s=ilradar console
playwright-cli -s=ilradar network
playwright-cli -s=ilradar resize 1440 900
```

### 会话管理

```bash
playwright-cli list
playwright-cli -s=ilradar close
playwright-cli close-all
playwright-cli kill-all        # 强制清理残留浏览器进程
```

## 本技能的用法约定

### 优先 curl

静态页、官方文档、帮助中心、学术元数据页一律先 `curl`：

```bash
curl -sL --max-time 20 -A "Mozilla/5.0" "<url>" | head -c 4000
```

**只有这四种情况才开浏览器**：需要登录态、有验证码、要读 PDF 二进制、要做视觉判断（截图）。

**`curl` 拿到验证页或空壳时不要重试**，直接转浏览器。实测知网检索会被重定向到 `verify/home?captchaType=blockPuzzle`，正文只有"安全验证"。

### 照档案走，不要即兴发挥

查某个站点前先读 `references/sites/<站点>.json`。档案里有：入口 URL、已确认控件、已验证步骤、**已记录的障碍**（可能要登录、可能限 IP、可能是 JS 重渲染）。

档案的 `status` 含义：

| status | 意思 |
|---|---|
| `query_verified` | 代表性查询真的跑通过 |
| `entry_observed` | 只确认过入口和控件，没跑通完整查询 |
| `blocked` | 有登录/验证码/权限障碍，档案记录了实际情况 |
| `disabled` | 有明确停用依据 |

**入口可达不等于查询可用。** 不要因为页面打开了就认为能查到。

### 受阻的处理

| 状况 | 做法 |
|---|---|
| 出现登录页 | 停下来，请用户在可见窗口登录，之后继续同一会话。**不索取密码** |
| 出现验证码 | 同上。**不尝试绕过** |
| 提示 IP 限制或需机构权限 | 如实说明该来源不可用，改用其它等效证据 |
| 页面结构变了 | 重新 `snapshot`，按新 ref 定位 |
| 点击后没变化 | 再 `snapshot` 确认；仍无变化则换定位或改用 `eval` 检查元素是否存在 |
| 浏览器连不上 | `playwright-cli -s=ilradar close`，必要时 `kill-all`，再重开 |

### 中文与路径

- 题目 JSON、截图、PDF 输出尽量放**纯 ASCII 目录**，例如 `~/ilradar-work/`（Windows 可用 `C:/Users/<你的用户名>/ilradar-work/`）。
- 工作目录不确定时，`snapshot` 用绝对路径读取：`cat "<工作目录>/.playwright-cli/page-*.yml"`。
- 需要核对中文时用 `eval "el => el.textContent" <ref>` 取精确字符串。

### 页数与页码

题目问"第 n 页"时：

1. 用 `pdf` 导出或直接看页码控件，先确认**印刷页码与 PDF 物理页序的偏移**（前置页会造成错位）；
2. 至少核对两页的页脚数字再换算；
3. 扫描件没有文本层时，`screenshot` 后按图像读取，**不要**因为 `eval` 拿到空字符串就判断"该页没内容"。
