---
name: github-accelerator
version: 1.3.0
description: "Read-only GitHub fallback for public repos: direct-first mirror clone/download plus gh api reads. No repository writes."
author: Hermes Agent
license: MIT-0
platforms: [linux, macos]
permissions:
  allowed-tools:
    - bash
    - curl
    - git
    - gh
  scope: |
    Read-only GitHub transport fallback for public repositories.
    Network: GitHub hosts and configured mirror/proxy hosts only.
    Files: read downloads and clone destinations; write ~/.config/gh-accelerator/proxies.conf
    only after explicit user approval of the exact entries.
  prohibited:
    - Repository writes, pushes, or ref updates
    - Private repos, tokens, or credential-bearing URLs through third-party mirrors
    - Global git config rewrites
    - Secret exfiltration
metadata:
  hermes:
    tags: [GitHub, 网络加速, 镜像, git, 代理下载]
    related_skills: [github-auth, github, blocked-page-recovery]
---

# GitHub 加速器（github-accelerator）

GitHub 访问不畅时的降级加速技能：**直连优先 → 镜像兑底 → 用前探测**。覆盖网页内容获取、仓库克隆、raw/Release 文件下载三类场景，核心逻辑封装在自包含脚本 `scripts/gh_accel.sh`（仅依赖 bash + curl + git）。

**语言说明**：本技能面向 CN 网络环境的中文用户，文档以中文为主；脚本输出支持 `GH_ACCEL_LANG=zh|en` 切换（默认 `zh`）。

**能力边界**：本技能只做**只读**操作。`dl`/`clone` 仅支持 GitHub 官方域名与公开仓库；任何仓库写入（push、commit、ref 更新）都不属于本技能。

---

## 0. 快速开始（30 秒）

```bash
# 第一步永远是探测：直连与镜像的实时状态（每台机器网络不同）
scripts/gh_accel.sh check
```

预期输出（节选）：

```
== 直连探测 ==
  ✓ api.github.com/zen (200)
  ✗ github.com/ (000)
== 下载镜像（拉测试文件验内容）==
  ✓ ghfast.top
  ✓ gh-proxy.com
== clone 镜像（ls-remote 探测公开仓库）==
  ✓ https://gh-proxy.com/https://github.com
```

```bash
# 下载文件（自动降级）            # 克隆仓库（自动降级）
scripts/gh_accel.sh dl <url>      scripts/gh_accel.sh clone OWNER/REPO
```

`✓`=可用，`✗`=不可达。按 check 结果决定走直连还是镜像。

---

## 1. 适用场景与能力边界

### 1.1 ✅ 适用

- github.com 网页打不开/超时，需要仓库内容（README、源文件、目录列表）
- `git clone https://github.com/...` 卡住或失败
- Release 附件、raw 文件、archive 包下载失败或过慢
- 网络时好时坏，需要先探测再决定通道

### 1.2 ❌ 不适用

- `api.github.com` 完全不可达的网络（整站级封锁，镜像梯次也救不了 API 通道）——此时 gh CLI 功能全部失效，只能靠镜像脚本
- 需要登录态的网页操作（PR 评论、Issue 管理等）——走 gh CLI 直连，别走镜像
- **任何仓库写入**（push、创建 commit、更新 ref）——本技能严格只读，写操作请由用户显式发起其他工具完成
- 非 GitHub 的 git 托管（GitLab/Gitee 等）

### 1.3 ⚠️ 边界条件

- ⚠️ 镜像全部是**只读**通道：经镜像 clone 后 push 前必须 `set-url` 回官方（见 6.5）
- ⚠️ **私有仓库不要经第三方镜像 clone**——仓库 URL 会暴露给镜像站；经 §5.1 本地配置声明的自建代理视为用户自有可信设施，不受此限
- ⚠️ 本文件的「网络基线」是一台腾讯云服务器的实测快照，其他机器以 `check` 结果为准
- ⚠️ 镜像站寿命以月计，梯次会过期，维护方法见 §10

---

## 2. Agent 智能触发指引

### 2.1 触发关键词表

| 用户提到 | Agent 动作 |
|---|---|
| "GitHub 打不开 / 超时 / 网页 404" | 跑 `check`，内容需求改走 §4.1（gh api） |
| "clone 不下来 / git clone 卡住" | `gh_accel.sh clone OWNER/REPO` |
| "release 下载失败 / raw 拉不到 / 下载太慢" | `gh_accel.sh dl <url>` |
| "换个镜像 / 加速 GitHub" | `check` 探测后按结果更新梯次（§10） |
| "push 失败 / 认证失败" | 只检查 remote 是否还指向镜像（§6.5）；本技能不提供 push 通道 |
| 大批量 clone / CI 拉依赖 | 先 `check`，把存活镜像写入流水线 |

### 2.2 Agent 标准工作流

```
1. 探测   scripts/gh_accel.sh check          → 确认直连/镜像存活状态
2. 执行   dl / clone / gh api（只读）按需选择 → 直连失败自动降级，无需干预
3. 验证   文件比对大小或 sha256；clone 后 remote get-url 确认指向
4. 收尾   经镜像 clone 的仓库 push 前 set-url 回官方源
```

---

## 3. 网络基线（2026-09-08 实测快照，以 check 实时结果为准）

| 通道 | 状态 |
|---|---|
| api.github.com（gh CLI 全部操作） | ✅ 直连稳定 |
| git clone/push（HTTPS） | ✅ 直连可用，偶发失败重试即可 |
| raw / objects / codeload / gist CDN | ⚠️ 可用但偶发超时，失败即降级 |
| github.com 网页 | ❌ 间歇超时；DNS 固定解析 20.205.243.166 且该 IP 不通，**改 hosts 无效** |

## 4. 场景对策

### 4.1 网页内容（github.com 超时时，只读 gh api）

要内容不要页面——README/源文件一律用 gh api 的**只读 GET** 直连取（这是经认证的 API 读操作，仅用于公开内容；不要执行任何写方法）：

```bash
gh api repos/OWNER/REPO/readme --jq .content | base64 -d          # README
gh api repos/OWNER/REPO/contents/PATH/TO/FILE --jq .content | base64 -d   # 单文件(>1MB 见 6.7)
gh api repos/OWNER/REPO/contents/DIR --jq '.[].name'              # 列目录
```

确需看渲染页面 → 用户本机浏览器打开（用户端网络不同）；浏览型镜像（bgithub.xyz / kkgithub.com）实测 clone 404、超时，仅最后手段。

### 4.2 Clone

直连失败时自动降级：`gitclone.com` → `gh-proxy.com`。

```bash
scripts/gh_accel.sh clone OWNER/REPO [dir]
scripts/gh_accel.sh clone --no-direct OWNER/REPO [dir]   # 跳过直连，测镜像链
```

预期输出（降级场景）：

```
→ 直连: https://github.com/hunshcn/gh-proxy
  ✗ 直连失败，降级镜像…
→ 镜像: https://gitclone.com/github.com/hunshcn/gh-proxy
  ✗ 失败
→ 镜像: https://gh-proxy.com/https://github.com/hunshcn/gh-proxy
✅ 经镜像 clone 成功 -> gh-proxy
⚠️  remote 指向镜像，push 前执行:
   git -C gh-proxy remote set-url origin https://github.com/hunshcn/gh-proxy.git
```

### 4.3 下载 raw / release / archive

直连失败时自动加前缀降级：`ghfast.top` → `gh-proxy.com`。

```bash
scripts/gh_accel.sh dl <github-url>
scripts/gh_accel.sh dl --no-direct <github-url>   # 跳过直连
scripts/gh_accel.sh dl --sha256 <hash> <url>      # 校验通过才落盘
gh release download --repo OWNER/REPO             # release 资产优先走 API 直连
```

脚本仅接受 GitHub 官方域名 URL，拒绝查询串/内嵌凭据；先写临时文件，目标文件已存在时拒绝覆盖。镜像可能截断/篡改内容，务必用官方 release 公布的 `--sha256` 校验；脚本成功后也会回显实际 sha256。

### 4.4 镜像梯次与黑名单（2026-09-08 实测）

| 用途 | 梯次（脚本按序自动尝试） | 实测 |
|---|---|---|
| 文件下载 | ghfast.top → gh-proxy.com | ✅ 4-5s 稳 / ⚠️ 波动 |
| 仓库克隆 | gitclone.com → gh-proxy.com 前缀 | ⚠️ 冷缓存 502 / ✅ ls-remote 实测 |

**已死勿用**：ghp.ci、ghgo.xyz、ghproxy.com、hub.fastgit.org；**疑似限流**：ghproxy.net（2.3MB 文件只给 0.56MB）。

自建/私有代理：经 §5.1 本地配置注入，自动排在梯次最前（已配置的机器上 `check` 输出带 `[本地]` 标记）。

## 5. 脚本命令参考

```bash
scripts/gh_accel.sh check                      # 探测直连 + 下载镜像 + clone 镜像
scripts/gh_accel.sh dl [--no-direct] [--sha256 H] <github-url>
scripts/gh_accel.sh clone <owner/repo> [dir]   # 克隆，直连→镜像自动降级
scripts/gh_accel.sh clone --no-direct o/r [dir]
GH_ACCEL_LANG=en scripts/gh_accel.sh check     # 英文输出（默认 zh）
```

公共梯次硬编码于脚本顶部 `DL_PROXIES` / `CLONE_PROXIES` 数组；个人自建代理不走硬编码，用 §5.1 配置文件注入。

### 5.1 本地私有代理（自建加速域名接入）

自建代理不写进脚本，写入机器本地配置文件即可自动生效，并**优先于公共镜像**：

- 路径：`~/.config/gh-accelerator/proxies.conf`（环境变量 `GH_ACCEL_CONFIG` 可覆盖；首次运行脚本会自动生成注释模板）
- 格式：每行一条，`#` 注释，裸域名自动补 `https://`

```
DOWNLOAD_PROXY=https://your-proxy.example.com
CLONE_PROXY=https://your-proxy.example.com/https://github.com
```

**Agent 行为约定**：用户提到"我有自己的加速域名 / 自建代理"时，Agent 必须先展示准备写入的精确配置行（`DOWNLOAD_PROXY` / `CLONE_PROXY`），**获得用户明确同意后**才能写入上述配置文件，随后跑 `scripts/gh_accel.sh check` 验证，并确认输出带 `[本地]` 标记。该文件属机器本地隐私，**禁止提交到任何仓库或发布物**。

---

## 6. 异常处理与排错指南

### 6.1 `check` 某站显示 `000`
- **症状**：探测输出 `✗ xxx (000)`
- **原因**：000 = curl 非 HTTP 响应，即超时或连接被重置（被墙/站点挂了）
- **修复**：等几分钟重跑 `check`；连续多次失败则从脚本梯次数组中移除该站
- **预防**：定期跑 check；新镜像入梯次前先连续 3 天观察

### 6.2 `dl` 直连失败但镜像成功
- **症状**：`✗ 直连失败 (http=000)` 后紧接 `✅ 经 ghfast.top 下载成功`
- **原因**：GitHub CDN 偶发丢包，属正常降级路径，无需处理
- **修复**：无需修复；文件已拿到
- **预防**：下载后按 §4.3 验证大小/sha256 即可

### 6.3 `dl` 全部通道失败
- **症状**：`❌ 全部通道失败`
- **原因**：直连与梯次内镜像同时不可用（集体被墙或全部倒闭）
- **修复**：跑 `check` 确认各站状态 → 按 §10 找新镜像 → 更新 `DL_PROXIES`
- **预防**：梯次保持 ≥3 个、且分属不同运营者

### 6.4 clone 时 gitclone.com 报 502
- **症状**：`The requested URL returned error: 502`
- **原因**：该站对冷门仓库无缓存（冷缓存 502），或瞬时过载
- **修复**：脚本会自动跳到下一镜像；若手动操作，直接换 `gh-proxy.com` 前缀重试
- **预防**：热门仓库先用 gitclone.com，冷门仓库优先自有代理

### 6.5 经镜像 clone 后 push 认证失败
- **症状**：`push` 报 403/401 或要求输密码
- **原因**：remote 还指向镜像地址，镜像不转发你的凭据，也不该转发
- **修复**：`git remote set-url origin https://github.com/OWNER/REPO.git` 后重试
- **预防**：每次镜像 clone 成功后立即按脚本提示 set-url（脚本已自动打印提示）

### 6.6 `gh api` 报 401 / Not logged in
- **症状**：`gh: To get started with GitHub CLI, please run: gh auth login`
- **原因**：目标机器 gh 未登录
- **修复**：`gh auth login`（headless 机器用设备码流程，见 github-auth skill）
- **预防**：新机器初始化时把 gh 登录列入基线步骤；未装 gh 时仅 §4.1 失效，dl/clone 不受影响

### 6.7 单文件下载被截断（如 ghproxy.net 只给零头）
- **症状**：下载 200 成功但文件明显偏小、解压报错
- **原因**：部分镜像对大文件限流/截断
- **修复**：换梯次内下一镜像重试；对照官方 release 的文件大小确认
- **预防**：大文件下载后必验 sha256；发现限流站写进黑名单注释

### 6.8 改 hosts 指向 github.com 的 IP 无效
- **症状**：写了 hosts 依然超时
- **原因**：实测 DNS 已解析到 20.205.243.166 且该 IP 本身不通——是 IP 被干扰而非解析错误
- **修复**：放弃 hosts 方案，改用本技能的镜像梯次
- **预防**：不要在类似网络环境浪费时间调 hosts

---


## 7. 反模式（不要做）

- ❌ **全局 `git config url.insteadOf` 持久改写**——所有仓库静默改道镜像，push 凭据与审计全部混乱；用单命令前缀
- ❌ **私有仓库走第三方镜像**——URL 暴露给镜像运营方；经 §5.1 声明的自建代理除外
- ❌ **直接采用文章推荐的镜像不实测**——镜像站死亡率极高；必须真实文件 + sha256 验证
- ❌ **只配一个镜像**——梯次 <2 个等于没有兜底
- ❌ **用 GitHub API 手工拼 blobs/trees/commits/refs 代替 push**——属于仓库写入且绕过常规审查，本技能不提供该通道
- ⚠️ gh CLI 永远直连不镜像：api.github.com 是最稳通道，套镜像反而引入新故障点

## 8. FAQ

**Q1：为什么不把镜像写进 git 全局配置一劳永逸？**
见反模式第一条。镜像会死、只读、且不适合私有仓库，持久改写把临时故障放大成全局事故。

**Q2：Mac/其他机器能用吗？**
脚本是纯 bash+curl+git，可直接用；但网络基线不同，必须先跑 `check` 重新探测，不要套用本文结论。

**Q3：镜像站会记录我的下载内容吗？**
会经过它们的服务器。公开仓库无所谓；私有仓库/含敏感信息的资源只走官方或自有代理。

**Q4：多久重测一次镜像？**
发现下载变慢/失败时跑 `check` 即可；无人值守环境建议 cron 每周跑一次并对比历史。

**Q5：直连明明有时能通，为什么还配镜像？**
间歇性超时下，重试等待成本远高于镜像降级（实测直连失败率约 80%）。脚本策略：直连快速失败 → 立即降级，总体延迟最低。

**Q6：会影响日常 `git push` 吗？**
不会。push 走直连官方源（api/git 通道稳定），镜像只用于读操作。

**Q7：check 里 raw 直连时好时坏正常吗？**
正常。CDN 域名偶发超时（实测如此），所以脚本设计为失败即降级，不依赖单次探测的结论。

## 9. 验证清单

- [ ] `check` 至少一条下载镜像 ✓
- [ ] `dl` 下载用官方 sha256 校验通过（`--sha256`），或成功输出中的 sha256 已人工比对
- [ ] `dl` 未覆盖任何已存在文件；目标目录非空时 `clone` 明确拒绝
- [ ] `clone` 后 `git remote get-url origin` 确认指向符合预期（官方=直连成功；镜像=已提示 set-url）
- [ ] 经镜像 clone 的仓库，push 前 `set-url` 已执行
- [ ] 大文件（>10MB）下载后校验过 sha256

## 10. 维护：找新镜像与更新梯次

1. 找候选：`ghproxy.link`（gh-proxy 官方域名发布页）+ 近期「github 加速」文章
2. 实测：`dl --no-direct <真实大文件>` + sha256 对比官方
3. 入梯次：编辑脚本顶部 `DL_PROXIES` / `CLONE_PROXIES`
4. 回填本文档：更新 §3 基线日期、§4.4 梯次表、黑名单
5. 死亡镜像立即移入黑名单，避免后人重复踩坑
