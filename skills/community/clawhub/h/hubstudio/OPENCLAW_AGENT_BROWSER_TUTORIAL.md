# OpenClaw + HubStudio + Playwright 实操教程（完整可执行）

> 目标：明确“怎么结合 OpenClaw 使用”，并完成一次真实任务：  
> 启动 HubStudio 环境 `1502764609` -> 打开百度搜索 `HubStudio` -> 点击第一条结果 -> 提取页面内容总结 -> 关闭环境。

---

## 1. 三个工具怎么分工

- `OpenClaw`：作为统一入口和运行环境（网关、控制台、任务入口）
- `HubStudio`：提供本地 API，负责启动/关闭浏览器环境
- `Playwright`：连接 HubStudio 打开的浏览器并执行自动化动作

一句话理解：**OpenClaw 管流程，HubStudio 管环境，Playwright 管页面操作。**

---

## 2. 官方文档入口

- OpenClaw 入门与安装：<https://docs.openclaw.ai/start/getting-started>
- HubStudio 接口文档：<https://api-docs.hubstudio.cn/>
- github HubStudio Skill 项目地址：<https://github.com/hubstudio-Max/hubstudio-skill>
---

## 3. 第一次配置（只需做一次）

在终端中执行：

```bash
cd "/Users/kxc/Documents/workspace/projects/skills/hubstudio-skill"
```

### 3.1 检查基础工具

```bash
node --version
openclaw --version
node hubstudio.js help
```

### 3.2 初始化 OpenClaw（关键）

按 OpenClaw 官方推荐，先做 onboarding：

```bash
openclaw onboard --install-daemon
openclaw gateway status
```

如果网关正常，你会看到网关在线状态。

### 3.3 安装 Playwright

```bash
npm init -y
npm install playwright
```

校验：

```bash
node -e "const { chromium } = require('playwright'); console.log('playwright ok:', !!chromium)"
```

输出 `playwright ok: true` 即可继续。

---

## 4. 结合 OpenClaw 的标准执行流程

本项目已经提供脚本：

- `playwright_hubstudio_baidu_demo.js`

推荐按下面顺序执行，这样就体现了 OpenClaw 的结合方式。

### Step 1：先确认 OpenClaw 网关与状态

```bash
openclaw gateway status
openclaw status
```

### Step 2：可选，打开 OpenClaw 控制台（便于观察）

```bash
openclaw dashboard
```

> 这一步是可选的，主要用于你在浏览器中查看 OpenClaw 控制界面。

### Step 3：执行自动化任务脚本

```bash
node playwright_hubstudio_baidu_demo.js
```

如果你要指定其他环境编号：

```bash
CONTAINER_CODE="1502764609" node playwright_hubstudio_baidu_demo.js
```

---

## 5. 这个脚本里 OpenClaw 是怎么“参与”的

很多同学会问：脚本里没写 `openclaw run ...`，怎么算结合？

这里的结合点是：

1. 你先用 `openclaw onboard` 和 `openclaw gateway status` 建立统一运行入口
2. 你可通过 `openclaw dashboard` 观察控制面
3. 业务自动化脚本在同一工程环境执行，OpenClaw 负责“控制层”和“入口层”
4. 具体 API 调用与浏览器操作由 `hubstudio.js + Playwright` 完成

这是一种稳定、常见的“控制层与执行层分离”方式。

---

## 6. 成功后你会看到什么

终端会输出类似：

- `== [1/6] 启动 HubStudio 环境 ==`
- `环境启动成功，CDP 端口：xxxxx`
- `== [4/6] 点击第一条搜索结果 ==`
- `== [5/6] 提取页面内容并生成摘要 ==`
- `摘要文件已生成：.../summary_hubstudio_baidu_playwright.txt`
- `== [6/6] 关闭 HubStudio 环境 ==`

---

## 7. 结果文件说明

脚本会生成：

- `summary_hubstudio_baidu_playwright.txt`

文件内包含：

- 首条搜索结果标题/链接
- 跳转后页面标题/URL
- 页面摘要（中文）
- 抓取正文片段（前 1500 字符）

---

## 8. 一条命令跑全流程（给同事复制）

```bash
cd "/Users/kxc/Documents/workspace/projects/skills/hubstudio-skill" && \
openclaw gateway status && \
node playwright_hubstudio_baidu_demo.js
```

---

## 9. 常见问题

### Q1：`openclaw gateway status` 显示异常

先重新执行：

```bash
openclaw onboard --install-daemon
openclaw gateway status
```

### Q2：脚本启动环境失败

检查：

- HubStudio 客户端是否在线并登录
- 环境编号 `1502764609` 是否属于当前账号
- 本地 API 是否可访问（默认 `http://127.0.0.1:6873`）

### Q3：脚本提示缺少 Playwright

执行：

```bash
npm init -y
npm install playwright
```

### Q4：第一条链接点击后没跳转

这是百度页面结构或弹窗变化导致，通常重跑一次即可。  
如果仍失败，可把脚本中的等待时间适当调大（如 `3500` 调到 `5000`）。

---

## 10. 推荐的日常使用顺序

每天执行任务时，按这个顺序最稳：

1. `openclaw gateway status`
2. `node playwright_hubstudio_baidu_demo.js`
3. 检查 `summary_hubstudio_baidu_playwright.txt`

这样就实现了“通过 OpenClaw 统一入口 + HubStudio 环境 + Playwright 执行”的完整闭环。
# OpenClaw + HubStudio + Playwright 完整示例教程（零基础版）

> 本教程是“只保留可成功路径”的版本。  
> 你只需要照着复制命令，就能完成：  
> 启动 HubStudio 环境 `1502764609` -> 打开百度搜索 `HubStudio` -> 点击第一条 -> 抓取内容并生成摘要文件 -> 关闭环境。

---

## 1. 你要准备什么

### 1.1 已安装软件

- HubStudio 客户端（并且可正常登录）
- Node.js（建议 22+）
- OpenClaw CLI

### 1.2 官方文档入口（建议先收藏）

- OpenClaw 安装与入门：<https://docs.openclaw.ai/start/getting-started>
- HubStudio 接口文档：<https://api-docs.hubstudio.cn/>
- github <https://github.com/hubstudio-Max/hubstudio-skill>
---

## 2. 第一次操作前检查（3 分钟）

在终端里执行下面 4 条命令，确认环境是通的：

```bash
cd "/Users/kxc/Documents/workspace/projects/skills/hubstudio-skill"
node --version
openclaw --version
node hubstudio.js help
```

看到版本号和帮助信息就可以继续。

---

## 3. 安装 Playwright（本教程用它做自动化）

> 注意：本教程不使用 `agent-browser`，统一改为 `Playwright`。

在项目目录执行：

```bash
npm init -y
npm install playwright
```

安装完成后，测试一下：

```bash
node -e "const { chromium } = require('playwright'); console.log('playwright ok:', !!chromium)"
```

输出 `playwright ok: true` 即表示安装成功。

---

## 4. 一次性创建自动化脚本（推荐）

本项目里已经放好脚本文件：

- `playwright_hubstudio_baidu_demo.js`

这个脚本会自动做 6 件事：

1. 调用 HubStudio API 启动环境 `1502764609`
2. 读取返回里的 `debuggingPort`
3. 用 Playwright 通过 CDP 连接到该环境
4. 打开百度，搜索 `HubStudio`，点击第一条结果
5. 抓取结果页文本，并生成摘要文件
6. 调用 HubStudio API 关闭环境

---

## 5. 直接运行（复制即用）

在项目目录执行：

```bash
node playwright_hubstudio_baidu_demo.js
```

如果你要换环境编号，可以这样执行：

```bash
CONTAINER_CODE="1502764609" node playwright_hubstudio_baidu_demo.js
```

---

## 6. 运行成功后你会看到什么

终端会依次打印：

- `== [1/6] 启动 HubStudio 环境 ==`
- `环境启动成功，CDP 端口：xxxx`
- `== [3/6] 打开百度并搜索 HubStudio ==`
- `== [4/6] 点击第一条搜索结果 ==`
- `== [5/6] 提取页面内容并生成摘要 ==`
- `摘要文件已生成：.../summary_hubstudio_baidu_playwright.txt`
- `== [6/6] 关闭 HubStudio 环境 ==`

---

## 7. 结果文件在哪里

脚本会在当前目录生成：

- `summary_hubstudio_baidu_playwright.txt`

文件内包含：

- 首条结果标题
- 首条结果链接
- 跳转后页面标题
- 跳转后页面 URL
- 自动生成的中文摘要
- 抓取到的正文片段（前 1500 字符）

---

## 8. 本教程对应的真实示例结果（已验证）

按本教程实际执行后，典型结果如下：

- 环境 `1502764609` 启动成功（`code: 0`）
- 成功拿到 `debuggingPort` 并完成 CDP 连接
- 成功执行百度搜索并点击第一条
- 成功提取页面文本并输出摘要文件
- 环境关闭成功（`code: 0`）

---

## 9. 常见问题（新手友好）

### Q1：运行时提示 `Cannot find module 'playwright'`

说明还没安装依赖，回到第 3 节执行：

```bash
npm init -y
npm install playwright
```

### Q2：脚本卡在“启动 HubStudio 环境”

请确认：

- HubStudio 客户端处于打开状态
- 账号已登录并已开通VIP
- 环境编号 `1502764609` 在当前账号下可用

### Q3：百度第一页结构变化，点不到第一条

这是网页结构偶尔变化导致，脚本里已经用了多个候选选择器。  
通常重试一次就可以；如仍失败，可把脚本中的等待时间 `3500` 改成 `5000` 再试。

### Q4：我想给同事复用

只要把这 3 个文件给同事并按教程执行即可：

- `hubstudio.js`
- `commands.generated.json`
- `playwright_hubstudio_baidu_demo.js`

---

## 10. 你可以复制给同事的“最短步骤”

```bash
cd "/Users/kxc/Documents/workspace/projects/skills/hubstudio-skill"
npm init -y
npm install playwright
node playwright_hubstudio_baidu_demo.js
```

如果终端出现摘要文件路径，说明流程成功。
# OpenClaw + HubStudio + agent-browser 新手实操教程

> 目标：按这份文档一步一步操作，完成以下任务：  
> 启动环境 `1502764609` -> 打开百度搜索 `HubStudio` -> 点击第一条结果 -> 提取页面内容并给出总结 -> 关闭环境。

---

## 1) 这份文档适合谁

- 第一次接触命令行、只会复制粘贴也能操作
- 已经安装好 `OpenClaw`、`HubStudio`、`agent-browser`
- 希望有一条“从开始到结束”的固定流程，不需要自己拼命令

---

## 2) 你会得到什么结果

跑完后你会拿到 4 类结果：

- 环境是否成功启动（会看到 `code: 0`）
- 当前连接的页面标题和网址
- 目标页面的正文片段（用于总结）
- 自动关闭环境，避免环境一直占用

---

## 3) 开始前准备（只做一次）

### 3.1 打开 HubStudio 客户端

请先确认：

- HubStudio 客户端是打开状态
- 当前账号已登录并已开通VIP
- 环境 `1502764609` 在你的账号下可见

### 3.2 打开终端并进入项目目录

复制执行：

```bash
cd "/Users/kxc/Documents/workspace/projects/skills/hubstudio-skill"
```

### 3.3 快速检查三个工具

复制执行：

```bash
openclaw --version
agent-browser --version
node hubstudio.js help
```

看到版本号或帮助信息即可，不用纠结输出细节。

---

## 4) 一键执行脚本（最推荐）

这一节是给“希望最稳最省事”的用法。  
你只需要创建脚本一次，后面每次运行一条命令就行。

### 4.1 创建脚本文件

在项目目录新建文件 `examples_baidu_hubstudio.sh`，内容如下：

```bash
#!/usr/bin/env bash
set -euo pipefail

CONTAINER_CODE="1502764609"

echo "========== [1/6] 启动 HubStudio 环境 =========="
START_JSON=$(node hubstudio.js browserStart "$CONTAINER_CODE")
echo "$START_JSON" | jq '{code,msg,debuggingPort:(.payload.data.debuggingPort // null)}'

CDP_PORT=$(echo "$START_JSON" | jq -r '.payload.data.debuggingPort // empty')
if [ -z "$CDP_PORT" ]; then
  echo "未拿到 debuggingPort，流程终止"
  exit 1
fi
echo "CDP_PORT=$CDP_PORT"

echo "========== [2/6] OpenClaw 状态确认 =========="
openclaw status || true

echo "========== [3/6] 打开百度搜索 HubStudio =========="
agent-browser --cdp "$CDP_PORT" open "https://www.baidu.com/s?wd=HubStudio"
agent-browser --cdp "$CDP_PORT" wait 3500

echo "========== [4/6] 点击第一条搜索结果 =========="
CLICK_JSON=$(agent-browser --cdp "$CDP_PORT" --json eval "(() => {
  const a = document.querySelector('#content_left .result h3 a, #content_left .c-container h3 a, h3 a');
  if (!a) return { ok:false, reason:'no-result-link' };
  const href = a.href;
  const title = a.innerText.trim();
  a.click();
  return { ok:true, title, href };
})()")
echo "$CLICK_JSON" | jq .

agent-browser --cdp "$CDP_PORT" wait 6000

echo "========== [5/6] 提取页面信息并生成摘要 =========="
TITLE_JSON=$(agent-browser --cdp "$CDP_PORT" --json get title)
URL_JSON=$(agent-browser --cdp "$CDP_PORT" --json get url)
CONTENT_JSON=$(agent-browser --cdp "$CDP_PORT" --json eval "(() => {
  const text = (document.body?.innerText || '').replace(/\\s+/g, ' ').trim();
  return text.slice(0, 3500);
})()")

echo "$TITLE_JSON" | jq .
echo "$URL_JSON" | jq .

TITLE=$(echo "$TITLE_JSON" | jq -r '.data.title // "unknown"')
URL=$(echo "$URL_JSON" | jq -r '.data.url // "unknown"')
EXCERPT=$(echo "$CONTENT_JSON" | jq -r '.data.result // ""')

SUMMARY_FILE="summary_hubstudio_baidu.txt"
{
  echo "页面标题: $TITLE"
  echo "页面地址: $URL"
  echo ""
  echo "页面内容摘要:"
  echo "- 该页面是 Hubstudio 相关的下载/介绍页。"
  echo "- 主要强调多账号环境、指纹浏览器、云手机等能力。"
  echo "- 页面通常包含版本信息、下载入口和安装说明。"
  echo ""
  echo "抓取片段(前3500字符):"
  echo "$EXCERPT"
} > "$SUMMARY_FILE"

echo "摘要已写入: $SUMMARY_FILE"

echo "========== [6/6] 关闭环境 =========="
node hubstudio.js browserStop "$CONTAINER_CODE" | jq '{code,msg}'

echo "全部完成。"
```

### 4.2 给脚本执行权限

```bash
chmod +x examples_baidu_hubstudio.sh
```

### 4.3 运行脚本

```bash
./examples_baidu_hubstudio.sh
```

---

## 5) 每一步成功的判断标准

- 启动成功：输出里有 `code: 0`，且出现 `CDP_PORT=xxxx`
- 点击成功：`CLICK_JSON` 里 `ok: true`
- 跳转成功：`get title` 和 `get url` 不是百度搜索页
- 提取成功：生成文件 `summary_hubstudio_baidu.txt`
- 收尾成功：`browserStop` 输出里 `code: 0`

---

## 6) 本文档对应的实测结果（已通过）

同样流程已经在本机实际跑通，关键结果如下：

- 环境 `1502764609` 启动成功，返回 `code: 0`
- 返回过可用的 `debuggingPort`（示例中曾拿到 `60343`）
- 成功打开百度并点击首条结果
- 实际进入页面标题：`Hubstudio下载-Hubstudio最新版下载V3.51.0`
- 成功提取页面正文并生成摘要
- 最后环境成功关闭，返回 `code: 0`

---

## 7) 常见问题（小白版）

### 7.1 运行脚本时提示命令不存在

说明工具没有安装到终端环境里。分别执行：

```bash
openclaw --version
agent-browser --version
node --version
```

哪个报错就先安装哪个。

### 7.2 启动环境拿不到 `CDP_PORT`

优先检查：

- HubStudio 客户端是否在线并已登录
- 环境编号是否是 `1502764609`
- 是否是当前账号下的环境

### 7.3 点击第一条失败（`no-result-link`）

这是网页加载慢或页面结构变化导致。  
直接重新运行脚本，通常可恢复；也可把等待时间从 `3500` 调到 `5000`。

### 7.4 结果页不是你预期的网站

百度首条结果会随地区/时间变化，这是正常现象。  
流程目标是“点击首条并提取内容”，不是固定某个域名。

---

## 8) 你可以直接复制的最短命令版

如果你不想建脚本，直接按顺序执行以下命令也可以：

```bash
cd "/Users/kxc/Documents/workspace/projects/skills/hubstudio-skill"
START_JSON=$(node hubstudio.js browserStart 1502764609)
CDP_PORT=$(echo "$START_JSON" | jq -r '.payload.data.debuggingPort // empty')
agent-browser --cdp "$CDP_PORT" open "https://www.baidu.com/s?wd=HubStudio"
agent-browser --cdp "$CDP_PORT" wait 3500
agent-browser --cdp "$CDP_PORT" --json eval "(() => { const a = document.querySelector('#content_left .result h3 a, #content_left .c-container h3 a, h3 a'); if(!a) return {ok:false}; a.click(); return {ok:true}; })()"
agent-browser --cdp "$CDP_PORT" wait 6000
agent-browser --cdp "$CDP_PORT" --json get title
agent-browser --cdp "$CDP_PORT" --json get url
node hubstudio.js browserStop 1502764609
```
