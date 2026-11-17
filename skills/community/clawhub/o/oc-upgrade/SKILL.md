---
name: "openclaw-upgrade"
description: "OpenClaw版本升级标准流程。每次说\"升级openclaw\"、\"openclaw升级\"、\"更新openclaw\"时必须执行，先做环境探测+分类，再按Windows/schtasks或Linux/systemd分支走对应升级方案"
---

# OpenClaw 升级技能（环境自适应版）

每次升级 OpenClaw 都必须严格按此流程执行，不能省步骤。

> 本版把 Linux 原版（systemd/bash）与 Windows 适配版（schtasks/PowerShell）合并为一个技能：第零步先探测环境并分类，之后每步按 `[Windows]` / `[Linux]` 分支走。只维护一份，不再靠两份文件。

## Changelog

> description 字段只写触发场景，不写变更记录；每次改动的原因/教训记在这里。

- 2026-08-13（实测事故）：`openclaw update`（A 方案）在 Windows 上实测失败——它内部是「先装后停」（Linux 模式），撞 DLL 锁定；且停 gateway 时把自身（gateway 子进程）一起杀死，npm install 根本没执行，gateway 宕机 3.5 小时无人拉起。教训：Windows 主入口改为「分离式 schtasks 一次性任务」，`openclaw update` 在 Windows 上禁用。
- 2026-08-13：合并 Linux 原版 + Windows 适配版为「环境自适应版」。第零步升级为「环境探测 + 分类」（判定 OS 类型 + 服务托管方式），后续每步给出 `[Windows]`/`[Linux]` 双分支。Windows 分支保留 DLL 锁定 + 自杀陷阱两个硬坑（主入口 `openclaw update --tag`），Linux 分支保留原「先装后停」流程。原两个文件已归档到 `SKILL.linux-original.bak.md`（此版之前的 Windows 版内容见 git/历史）。
- 2026-08-13：Windows 适配。本机（SCRIPT-S03-04，Windows Server 2016）实测：gateway 由 Windows 任务计划程序（schtasks）托管而非 systemd；gateway 进程加载了 node-pty-win32-x64 / tree-sitter 等原生 .node DLL，Windows 锁定运行中 DLL → 运行时直接 `npm install -g openclaw` 会 EBUSY/EPERM 失败；agent 运行在 gateway 进程内部不能自己 stop 自己。故 Windows 主入口改为 `openclaw update --tag <版本>`，裸 npm install 降级为分离式 schtasks 任务兜底。同时适配：npm registry=npmmirror（无代理）、无 curl.exe（Server 2016）改用 Invoke-WebRequest、.env 无 GITHUB_TOKEN、lossless-claw 是 npm 项目路径、消息通道 POPO 无 feishu。
- 上次（4.14版本）因为没检查 lossless-claw 兼容性踩过坑
- 上次升级后忘记发完成通知，爸比等了7小时不知道结果
- 2026-07-27：NAS欢欢用自写脚本升级，脚本从gateway进程内部nohup启动，第一步systemctl stop把整个进程组一起杀掉，脚本自己被杀死，npm install根本没跑起来，gateway停了近6小时无人察觉——本skill的流程设计（npm install前不停服务、重启只在最后单独一步、重启前先设好通知cron）天然规避了这个坑，但重启这一步本身如果裸调systemctl也仍有被自身进程树波及的理论风险，已在第八步/回滚方案中改为优先走平台 gateway 工具
- 2026-07-27（同一事故的第二个坑）：NAS欢欢手动拉起gateway后agent恢复中断会话继续把npm包升到2026.7.1-2，但机器Node还是22.22.1，openclaw 2026.7.1-2要求Node≥22.22.3，gateway直接拒绝启动；且该NAS访问registry.npmjs.org走IPv6比IPv4慢6倍，codex插件依赖安装卡在慢速IPv6上4分半——第零步此前没查Node版本、没做IPv4/IPv6测速，两个真实缺口已补入
- 2026-07-27（第三个坑，元问题）：description字段被写成changelog摘要，覆盖了触发关键词，导致agent在用户说"升级openclaw"时语义匹配不上这个skill。教训：description只写"什么场景触发"，绝不写"这次改了什么"；changelog一律写在本节。

---

## 环境分类路由表（探测后对照，一眼定位走哪个分支）

| 维度 | [Windows] 分支 | [Linux] 分支 |
|------|----------------|--------------|
| 判定 | `$env:OS` = `Windows_NT`（PowerShell） | `uname -s` = `Linux`（bash） |
| Shell | PowerShell / cmd | bash |
| Gateway 托管 | 任务计划程序「OpenClaw Gateway」（schtasks） | `systemd --user`（`openclaw-gateway.service`） |
| 原生 DLL 锁定 | ❗**有**（node-pty-win32-x64、tree-sitter）→ 运行中 `npm install -g` 必 EBUSY | 无（inode 替换，可运行中覆盖） |
| **主升级入口** | **分离式 schtasks 一次性任务**（第六步 A） | `npm install -g openclaw@<版本>`（先装后停） |
| 停服方式 | `gateway` 工具 / `schtasks /end`+`/run` | `gateway` 工具 / `systemctl --user restart` |
| npm registry | npmmirror（无代理，无 IPv6 问题） | registry.npmjs.org（需代理检测 + IPv4/IPv6 测速） |
| HTTP 探测工具 | `Invoke-WebRequest`（无 curl.exe） | `curl` |
| 配置/凭证路径 | `$env:USERPROFILE\.openclaw\...` | `~/.openclaw/...` |
| 启动脚本/override | `gateway.cmd` | `override.conf`（systemd drop-in） |
| lossless-claw 路径 | npm 项目 `~\.openclaw\npm\projects\martian-engineering-lossless-claw-*` | `~/.openclaw/extensions/lossless-claw` |
| 消息通道 | POPO（moltbot-popo） | 视部署（feishu 等） |
| 多用户检测 | `C:\Users\*` 其他含 `.openclaw` 的 profile | `/home/*` + WSL 实例 |

---

## 第零步：环境探测 + 分类

先判定平台，再跑对应分支的详细探测，**探测结果汇报给爸比，确认后继续**。

### 0.1 平台判定

```bash
# 通用快速判定（任一条能出结果即可）
uname -s          # 返回 "Linux" → Linux 分支；命令不存在 → Windows 分支
```

```powershell
# Windows 下用这个
$env:OS           # 返回 "Windows_NT" → Windows 分支
```

macOS 等 bash 类环境按 `[Linux]` 分支处理（服务管理方式单独确认，见 0.3 末）。

### 0.2 [Windows] 详细探测（PowerShell）

```powershell
Write-Host "=== OpenClaw 环境（Windows） ==="
Write-Host "用户: $env:USERNAME"
Write-Host "Home: $env:USERPROFILE"
Write-Host "npm global: $(npm prefix -g 2>$null)"

$nodeVer = (node --version 2>$null) -replace '^v',''
Write-Host ""
Write-Host "=== Node.js 版本 ==="
if (-not $nodeVer) { Write-Host "⚠️ 无法检测 Node 版本" }
else {
  Write-Host "当前 Node: v$nodeVer"
  $nodeMajor = [int]($nodeVer -split '\.')[0]
  if ($nodeMajor -lt 22) { Write-Host "⚠️ Node 主版本 $nodeMajor 低于 22，多数近期 OpenClaw 会拒绝启动" }
  else { Write-Host "Node 主版本 $nodeMajor ✅（具体最低子版本见第一步核对）" }
}
Write-Host "⚠️ 仅确认当前 Node 不够，必须第一步拿到目标版本 engines.node 后对比。"

Write-Host ""
Write-Host "=== registry 连通性 ==="
$reg = npm config get registry
Write-Host "registry: $reg"
try {
  $r = Invoke-WebRequest -Uri $reg -UseBasicParsing -TimeoutSec 8 -Method Head
  Write-Host "连通 ✅ HTTP $($r.StatusCode)"
} catch { Write-Host "⚠️ 访问 $reg 失败: $($_.Exception.Message)" }
Write-Host "HTTP_PROXY=[$env:HTTP_PROXY] HTTPS_PROXY=[$env:HTTPS_PROXY]（空=直连）"

Write-Host ""
Write-Host "=== 可选组件 ==="
$ll = Get-ChildItem "$env:USERPROFILE\.openclaw\npm\projects" -Directory -ErrorAction SilentlyContinue |
      Where-Object { $_.Name -like '*lossless-claw*' } | Select-Object -First 1
if ($ll) {
  $pkg = Get-Content "$($ll.FullName)\node_modules\@martian-engineering\lossless-claw\package.json" -Raw -ErrorAction SilentlyContinue | ConvertFrom-Json -ErrorAction SilentlyContinue
  Write-Host "lossless-claw: 已装 ver $($pkg.version)（项目 $($ll.Name)）"
} else { Write-Host "lossless-claw: 未安装 ✅" }
Write-Host "消息通道: POPO (moltbot-popo)，无 feishu"

Write-Host ""
Write-Host "=== gateway 托管 ==="
schtasks /query /tn "OpenClaw Gateway" 2>$null | Select-String -Pattern "任务名|正在运行|就绪|无法"
Write-Host "托管: Windows 任务计划程序（schtasks）"

Write-Host ""
Write-Host "=== 其他用户检测 ==="
$others = Get-ChildItem "C:\Users" -Directory -ErrorAction SilentlyContinue |
          Where-Object { $_.Name -ne $env:USERNAME -and (Test-Path "$($_.FullName)\.openclaw") }
if ($others) { Write-Host "⚠️ 发现其他用户含 .openclaw：$($others.Name -join ', ')——npm install -g 影响共享 global 包" }
else { Write-Host "未发现其他 OpenClaw 用户 ✅（单用户）" }
```

### 0.3 [Linux] 详细探测（bash）

```bash
# === OpenClaw 环境（Linux） ===
echo "用户: $(whoami)"
echo "Home: $HOME"
NPM_PREFIX=$(npm prefix -g 2>/dev/null || echo "unknown")
echo "npm global: $NPM_PREFIX"

echo ""
echo "=== Node.js 版本 ==="
NODE_VER=$(node --version 2>/dev/null | sed 's/^v//')
echo "当前 Node: v${NODE_VER:-未知}"
if [ -z "$NODE_VER" ]; then
  echo "⚠️ 无法检测 Node 版本"
else
  NODE_MAJOR=$(echo "$NODE_VER" | cut -d. -f1)
  [ "$NODE_MAJOR" -lt 22 ] && echo "⚠️ Node 主版本 ${NODE_MAJOR} 低于 22，多数近期 OpenClaw 会拒绝启动" || echo "Node 主版本 ${NODE_MAJOR} ✅"
fi
echo "⚠️ 仅确认当前 Node 不够，必须第一步拿到目标版本 engines.node 后对比。"

# 代理检测
if curl -s --connect-timeout 3 -x "http://127.0.0.1:7890" https://registry.npmjs.org/ > /dev/null 2>&1; then
  PROXY_OPT="--proxy http://127.0.0.1:7890"; echo "代理: 127.0.0.1:7890 ✅"
elif curl -s --connect-timeout 3 https://registry.npmjs.org/ > /dev/null 2>&1; then
  PROXY_OPT=""; echo "代理: 直连 ✅"
else
  echo "⚠️ npm 网络不通，请检查代理"
fi

# IPv4/IPv6 速度探测（NAS 坑：IPv6 慢 6 倍会卡死 npm）
echo ""
echo "=== registry IPv4/IPv6 速度探测 ==="
IPV4_TIME=$(timeout 5 curl -4 -s -o /dev/null -w '%{time_total}' https://registry.npmjs.org/ 2>/dev/null)
IPV6_TIME=$(timeout 5 curl -6 -s -o /dev/null -w '%{time_total}' https://registry.npmjs.org/ 2>/dev/null)
echo "IPv4: ${IPV4_TIME:-超时/不可用}s"
echo "IPv6: ${IPV6_TIME:-超时/不可用}s"
if [ -z "$IPV6_TIME" ]; then
  echo "IPv6 不可用/超时，建议升级/安装步骤强制 --force-ipv4 兜底"
elif python3 -c "exit(0 if float('$IPV6_TIME') > float('${IPV4_TIME:-999}') * 2 else 1)" 2>/dev/null; then
  echo "⚠️ IPv6 明显慢于 IPv4（超2倍），建议 export NODE_OPTIONS=\"--dns-result-order=ipv4first\" 后再 npm install"
else
  echo "IPv4/IPv6 速度接近 ✅"
fi

# 可选组件
HAS_LOSSLESS=false
[ -d "$HOME/.openclaw/extensions/lossless-claw" ] && HAS_LOSSLESS=true
echo "lossless-claw: $HAS_LOSSLESS"

OVERRIDE="$HOME/.config/systemd/user/openclaw-gateway.service.d/override.conf"
echo "override.conf: $([ -f "$OVERRIDE" ] && echo 存在 || echo 不存在)"

echo "服务管理: systemd --user"

# /tmp/jiti 权限（codex EACCES 坑）
if [ -d "/tmp/jiti" ]; then
  JITI_PERM=$(stat -c "%a" /tmp/jiti)
  [ "$JITI_PERM" != "1777" ] && echo "⚠️ /tmp/jiti 权限 $JITI_PERM，建议 sudo chmod 1777 /tmp/jiti" || echo "/tmp/jiti: 1777 ✅"
else
  echo "/tmp/jiti: 不存在 ✅"
fi

# 其他 OpenClaw 用户（同机共享 npm global 风险）
echo ""
echo "=== 其他 OpenClaw 用户检测 ==="
SAME_HOST_USERS=""
for U in $(ls /home/ 2>/dev/null); do
  if [ "$U" != "$(whoami)" ] && [ -d "/home/$U/.openclaw" ]; then
    echo "用户(同主机): $U"; SAME_HOST_USERS="$SAME_HOST_USERS $U"
  fi
done
# WSL 检测（bash 环境可能嵌套 WSL）
if command -v powershell.exe &>/dev/null; then
  WSL_LIST=$(powershell.exe -NoProfile -Command "wsl --list --verbose" 2>/dev/null | grep -i -v "NAME\|Windows" || true)
  [ -n "$WSL_LIST" ] && echo "$WSL_LIST" && echo "⚠️ 检测到 WSL 实例，注意多实例共享 npm global 风险"
fi

echo "npm global path: $(npm root -g 2>/dev/null)"
if [ -z "$SAME_HOST_USERS" ] && [ -z "$WSL_LIST" ]; then echo "未发现其他 OpenClaw 用户 ✅"; fi

# 若非 systemd（pm2/docker 等），在此确认实际管理方式
echo "⚠️ 若本机不是 systemd --user 托管，请在此确认实际服务管理方式，第八步/回滚的重启命令要相应改"
```

---

## 第一步：确认目标版本

```powershell
# [Windows] PowerShell
$cur = openclaw --version 2>$null
$target = npm view openclaw version
Write-Host "当前: $cur"
Write-Host "最新: $target"
npm view "openclaw@$target" engines.node
openclaw update status
openclaw update --dry-run --tag $target
```

```bash
# [Linux] bash
openclaw --version
npm view openclaw version
npm view openclaw@${TARGET_VER} engines.node
# 发行说明（有 GITHUB_TOKEN 时）：
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/openclaw/openclaw/releases/tags/v${TARGET_VER}" | \
  python3 -c "import json,sys; print(json.load(sys.stdin).get('body','')[:3000])"
```

- **Node 版本核对**：当前 Node 满足 `engines.node` → 继续；不满足 → 必须先升级 Node（Windows 用 nvm-windows/MSI，Linux 用 apt/nvm，同大版本线内，勿跨大版本线），否则升级后 gateway 直接拒绝启动。
- 向爸比汇报：当前版本、目标版本、release highlights、**Node 是否满足**，等确认（Node 不满足时一并确认是否先升 Node）。

---

## 第二步：检查插件兼容性

```bash
openclaw plugins list
```

只看 `enabled` 插件，**非 stock、手动/第三方安装**的插件重点核对（stock 随主包升级）：

- **[Windows]** `moltbot-popo`（POPO 通道，LobsterAI 第三方扩展）+ `lossless-claw`（npm 项目）
- **[Linux]** `lossless-claw`（`~/.openclaw/extensions/`）+ `@openclaw/feishu`（如有）等

发行说明里搜关键词（无 GITHUB_TOKEN 时用 `web_fetch` 抓 `https://github.com/openclaw/openclaw/releases/tag/v<版本>`，或 `openclaw update --dry-run` 输出）。有⚠️风险说清楚。

---

## 第三步：记录插件快照

```powershell
# [Windows]
openclaw plugins list > "$env:TEMP\plugins-before-$target.txt"
```

```bash
# [Linux]
openclaw plugins list > /tmp/plugins-before-${TARGET_VER}.txt
```

---

## 第四步：备份

```powershell
# [Windows] PowerShell
$cur = ([regex]::Match((openclaw --version 2>$null), '(\d+\.\d+\.\d+)')).Groups[1].Value
Copy-Item "$env:USERPROFILE\.openclaw\openclaw.json" "$env:USERPROFILE\.openclaw\openclaw.json.bak-$cur" -Force
Copy-Item "$env:USERPROFILE\.openclaw\.env"            "$env:USERPROFILE\.openclaw\.env.bak-$cur" -Force
Copy-Item "$env:USERPROFILE\.openclaw\gateway.cmd"     "$env:USERPROFILE\.openclaw\gateway.cmd.bak-$cur" -Force
# lossless-claw（npm 项目，只备份 package.json，node_modules 不备份）
$ll = Get-ChildItem "$env:USERPROFILE\.openclaw\npm\projects" -Directory -ErrorAction SilentlyContinue |
      Where-Object { $_.Name -like '*lossless-claw*' } | Select-Object -First 1
if ($ll) { Copy-Item "$($ll.FullName)\package.json" "$($ll.FullName)\package.json.bak-$cur" -Force }
Get-ChildItem "$env:USERPROFILE\.openclaw" -Filter "*.bak-$cur" | Select-Object Name
```

```bash
# [Linux] bash
CURRENT_VER=$(openclaw --version 2>/dev/null | grep -oP '[\d.]+' | head -1)
OVERRIDE="$HOME/.config/systemd/user/openclaw-gateway.service.d/override.conf"
LOSSLESS_DIR="$HOME/.openclaw/extensions/lossless-claw"

cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak-${CURRENT_VER}
cp ~/.openclaw/.env ~/.openclaw/.env.bak-${CURRENT_VER}
[ -f "$OVERRIDE" ] && cp "$OVERRIDE" "${OVERRIDE}.bak-${CURRENT_VER}" || echo "override.conf 不存在，跳过"
# lossless-claw：node_modules>500MB 时只备份 package.json/plugin.json/dist
if [ -d "$LOSSLESS_DIR" ]; then
  LOSSLESS_VER=$(cat "$LOSSLESS_DIR/package.json" | python3 -c "import json,sys;print(json.load(sys.stdin)['version'])")
  LOSSLESS_NM_SIZE=$(du -sm "$LOSSLESS_DIR/node_modules/" 2>/dev/null | cut -f1)
  LOSSLESS_BAK="$HOME/.openclaw/extensions/lossless-claw.bak-${LOSSLESS_VER}"
  mkdir -p "$LOSSLESS_BAK"
  if [ "${LOSSLESS_NM_SIZE:-0}" -gt 500 ]; then
    cp "$LOSSLESS_DIR/package.json" "$LOSSLESS_DIR/openclaw.plugin.json" "$LOSSLESS_BAK/"
    cp -r "$LOSSLESS_DIR/dist" "$LOSSLESS_BAK/"
  else
    cp -r "$LOSSLESS_DIR/." "$LOSSLESS_BAK/"
  fi
fi
# feishu（如有）
FEISHU_DIR="$HOME/.openclaw/npm/node_modules/@openclaw/feishu"
[ -d "$FEISHU_DIR" ] && mkdir -p "${FEISHU_DIR}.bak-${CURRENT_VER}" && cp "$FEISHU_DIR/package.json" "${FEISHU_DIR}.bak-${CURRENT_VER}/"
```

确认核心备份（openclaw.json + .env）存在后再继续。

---

## 第五步：设好重启后通知 cron（先于重启执行）

**两个分支共用，升级前必须先设。** gateway 重启会中断当前 session，重启后是全新上下文，不记得升级完成这件事。

用 `cron` 工具创建：
- `schedule`: `at`，时间 = 当前时间 + 3 分钟
- `payload.kind`: `systemEvent`
- `payload.text`: 升级完成通知（含版本号、插件状态、耗时）
- `sessionTarget`: `main`
- `deleteAfterRun`: `true`

示例：`🎉 OpenClaw 升级完成！v<旧> → v<新>，插件全部正常（lossless-claw ✅ <通道> ✅），耗时约X分钟。`

> ⚠️ 3分钟是安全值，90秒有时会在 gateway 恢复前触发导致通知失败。

---

## 第六步：执行升级

**等爸比说「执行」才动手。** 若第零步发现其他用户 / 第一步发现 Node 不满足，先解决再继续。

### A. [Windows] 分支（主入口 = 分离式 schtasks 一次性任务）

> ⚠️ **`openclaw update` 在 Windows 上已实测失败（2026-08-13）**：内部是「先装后停」（Linux 模式），撞 DLL 锁定；且停 gateway 时把自身（gateway 子进程）一起杀死，npm install 根本没执行，gateway 宕机 3.5 小时无人拉起。**Windows 禁用 `openclaw update`，直接用下面的分离式任务。**
> 裸 `npm install -g` 同样不可行（DLL 锁定，见路由表）。

分离式 schtasks 一次性任务——独立进程在 gateway 停止期间完成安装，绕开自杀陷阱 + DLL 锁定：

**1. 写独立升级脚本 `C:\Users\n3186\.openclaw\upgrade-once.ps1`：**

```powershell
# C:\Users\n3186\.openclaw\upgrade-once.ps1
param([string]$Version)
$ErrorActionPreference = 'Continue'
$log = "$env:USERPROFILE\.openclaw\logs\upgrade-once.log"
"$(Get-Date -Format o) 开始升级到 $Version" | Out-File $log -Append

# 等 gateway 完全停止（最多 120s）
$deadline = (Get-Date).AddSeconds(120)
while ((Get-Date) -lt $deadline) {
  $p = Get-CimInstance Win32_Process -Filter "name='node.exe'" | Where-Object { $_.CommandLine -like '*openclaw*index.js*gateway*' }
  if (-not $p) { break }
  Start-Sleep -Seconds 3
}

# 安装目标版本（gateway 已停，无 DLL 锁定）
npm install -g "openclaw@$Version" *>> $log

# 重启 gateway 任务
schtasks /run /tn "OpenClaw Gateway" >> $log 2>&1
"$(Get-Date -Format o) 完成" | Out-File $log -Append
```

**2. 注册一次性任务（now + 2 分钟）：**

```powershell
$st = (Get-Date).AddMinutes(2).ToString('HH:mm')
schtasks /create /tn "OpenClaw Upgrade Once" `
  /tr "powershell -NoProfile -ExecutionPolicy Bypass -File C:\Users\n3186\.openclaw\upgrade-once.ps1 -Version $target" `
  /sc ONCE /st $st /f
```

**3. 触发 gateway 停**（`gateway` 工具 action=restart 走 supervisor 握手，勿直接 kill）。流程：gateway 停 → 一次性任务到点跑（无锁）→ npm install → `schtasks /run` 拉起 gateway → 第五步通知 cron 触发。

### B. [Linux] 分支（先装后停）

```bash
if curl -s --connect-timeout 3 -x "http://127.0.0.1:7890" https://registry.npmjs.org/ > /dev/null 2>&1; then
  export HTTP_PROXY=http://127.0.0.1:7890
  export HTTPS_PROXY=http://127.0.0.1:7890
  echo "使用代理: 127.0.0.1:7890"
else
  echo "直连安装"
fi
if [ "${IPV6_SLOWER:-0}" = "1" ]; then
  export NODE_OPTIONS="--dns-result-order=ipv4first"
  echo "已强制 DNS 优先 IPv4"
fi
npm install -g openclaw@${TARGET_VER}
```

---

## 第七步：验证

```powershell
# [Windows]
openclaw --version; node --version
openclaw doctor
openclaw plugins list
if (Test-Path "$env:TEMP\plugins-before-$target.txt") { Compare-Object (Get-Content "$env:TEMP\plugins-before-$target.txt") (openclaw plugins list) }
```

```bash
# [Linux]
openclaw --version; node --version
openclaw doctor --fix 2>&1 | tail -5
openclaw doctor
FAILED=$(openclaw plugins list 2>/dev/null | grep -i "fail\|error" | grep -v "grep")
[ -n "$FAILED" ] && echo "⚠️ 插件加载失败：$FAILED" || echo "✅ 所有插件加载正常"
diff /tmp/plugins-before-${TARGET_VER}.txt <(openclaw plugins list 2>/dev/null)
```

验收标准（全部通过才继续）：版本=目标、Node 满足 engines.node、lossless-claw 仍在 enabled、消息通道（POPO/feishu）仍在 enabled、doctor Errors=0、无插件加载失败。**任一不通过 → 立即回滚，不继续。**

> [Windows] 注意：`plugins list` 可能显示部分 stock 插件 disabled，是默认配置非损坏，对比快照只看 enabled→disabled 的**实际变化**。

---

## 第八步：重启 gateway

**两分支都优先走平台 `gateway` 工具（action=restart），不裸调停服命令。**

```
优先：gateway 工具，action=restart，note="OpenClaw 升级完成，重启生效"
```

> [Windows] A 方案 `openclaw update` 已自动重启，本步通常无需手动。只有第七步通过但 gateway 还跑旧版本时才走本步。

无 `gateway` 工具时才退回：

```powershell
# [Windows]
schtasks /end /tn "OpenClaw Gateway"
schtasks /run /tn "OpenClaw Gateway"
```

```bash
# [Linux]
systemctl --user restart openclaw-gateway.service
```

第五步的 cron 会在重启后自动触发，通知爸比升级完成。

---

## ⏪ 回滚方案

任一步骤出问题立即执行。

```powershell
# [Windows]
$prev = '<回退版本，如 2026.6.6>'
npm install -g "openclaw@$prev"   # gateway 需先停，参照第六步 A 兜底分离式任务
Copy-Item "$env:USERPROFILE\.openclaw\openclaw.json.bak-$prev" "$env:USERPROFILE\.openclaw\openclaw.json" -Force
Copy-Item "$env:USERPROFILE\.openclaw\.env.bak-$prev"            "$env:USERPROFILE\.openclaw\.env" -Force
Copy-Item "$env:USERPROFILE\.openclaw\gateway.cmd.bak-$prev"     "$env:USERPROFILE\.openclaw\gateway.cmd" -Force
# 优先 gateway 工具 action=restart，无工具才：schtasks /run /tn "OpenClaw Gateway"
```

```bash
# [Linux]
PREV_VER=<回退版本>
npm install -g openclaw@${PREV_VER}
cp ~/.openclaw/openclaw.json.bak-${PREV_VER} ~/.openclaw/openclaw.json
cp ~/.openclaw/.env.bak-${PREV_VER} ~/.openclaw/.env
OVERRIDE="$HOME/.config/systemd/user/openclaw-gateway.service.d/override.conf"
[ -f "${OVERRIDE}.bak-${PREV_VER}" ] && cp "${OVERRIDE}.bak-${PREV_VER}" "$OVERRIDE"
LOSSLESS_BAK=$(ls -d "$HOME/.openclaw/extensions/lossless-claw.bak-"* 2>/dev/null | sort | tail -1)
[ -n "$LOSSLESS_BAK" ] && rm -rf "$HOME/.openclaw/extensions/lossless-claw" && cp -r "$LOSSLESS_BAK" "$HOME/.openclaw/extensions/lossless-claw"
systemctl --user daemon-reload
# 优先 gateway 工具 action=restart，无工具才：systemctl --user restart openclaw-gateway.service
```

等消息通道收到「重启完毕，在线了」通知，告知爸比回滚完成及原因。

---

## 注意事项

**两分支通用：**
- 升级前必须核对目标版本 Node 最低要求（`npm view openclaw@<版本> engines.node`），不满足先升 Node。
- 升级前必须先设通知 cron，否则重启后没人知道结果。
- 重启一律优先 `gateway` 工具，不裸调停服命令。
- 不要从 agent 里直接 stop/kill gateway（agent 是 gateway 子进程，会自杀）。
- skill description 字段只写触发场景，不写变更记录。
- 升级完成通知 cron 设 3 分钟而非更短。
- brave 插件外部化（2026.5.12 起）：升级后若遇 "web_search provider is not available: brave"，执行 `openclaw plugins install --force @openclaw/brave-plugin` 后重启。

**[Windows] 专属：**
- 不要裸 `npm install -g openclaw`（DLL 锁定，EBUSY/EPERM）。首选 `openclaw update --tag`。
- 无 curl.exe（Server 2016），HTTP 探测用 `Invoke-WebRequest`/`Invoke-RestMethod`。
- .env 无 GITHUB_TOKEN，发行说明用 `npm view`/`openclaw update status`/`--dry-run`/`web_fetch`。
- lossless-claw 是 npm 项目路径（`~\.openclaw\npm\projects\*`），不是 `extensions/`。
- 消息通道是 POPO（moltbot-popo），兼容性检查对象是它，无 feishu。
- npm registry=npmmirror，无代理、无 IPv6 慢速问题；若改回 registry.npmjs.org 再启用 Linux 的代理/IPv6 测速。

**[Linux] 专属：**
- 系统访问 registry.npmjs.org，注意代理 + IPv4/IPv6 测速，IPv6 慢就 `NODE_OPTIONS="--dns-result-order=ipv4first"`。
- `npm install -g` 影响同机所有用户共享的 global 包，先做多用户检测。
- `/tmp/jiti` 需 1777（codex EACCES 坑，多用户同机）。
- feishu 插件路径 `~/.openclaw/npm/node_modules/@openclaw/feishu`，升级后注册失败执行 `openclaw plugins install --force @openclaw/feishu` 后重启。
- systemd service 不读 .bashrc，代理若需在 service 生效要配 override.conf 或 EnvironmentFile。
- lossless-claw 路径 `~/.openclaw/extensions/lossless-claw`，每次升级必须检查兼容（4.14 踩过坑）。
- 服务管理默认 systemd --user，pm2/docker 等请相应改第八步/回滚的重启命令。
