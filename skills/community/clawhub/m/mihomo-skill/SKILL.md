---
name: mihomo-skill
description: 诊断并修复 mihomo / Clash.Meta / Clash 内核的代理异常，与部署平台无关——本机、远程 Linux/VPS、Docker、软路由/OpenWrt、群晖/绿联等 NAS、Clash Verge Rev / Mihomo Party 桌面客户端都适用。出现「代理时好时坏、节点全部延迟超时、面板全红、订阅拉不下来、日志 pull error、国内能上境外全断、重启后突然不能翻墙、明明有节点却像没走代理、分流或自动切换不生效、需要多订阅互为主备」时使用。覆盖 DNS 污染、SNI 阻断、订阅激活、provider 死锁、fallback 套策略组、GEOIP 误判直连等根因，可直接备份改配置、热重载或重启并复检。关键词：mihomo、clash、clash-meta、clash verge、mihomo party、proxy-provider、订阅、节点超时、分流规则、自动切换、主备、SNI 阻断、DNS 污染、docker、软路由、openwrt、nas、绿联、群晖、systemd。
agent_created: true
version: 1.0.0
license: MIT
description_en: |
  Diagnose and fix proxy problems in mihomo / Clash.Meta / Clash cores, independent of
  deployment platform — local machine, remote Linux/VPS, Docker, OpenWrt/soft router,
  Synology/UGREEN NAS, or Clash Verge Rev / Mihomo Party desktop clients. Use when the
  proxy is flaky, all node latency checks time out, the dashboard is all red, the
  subscription will not download, logs show pull errors, domestic sites work but
  overseas sites all fail, everything breaks after a restart, nodes exist but traffic
  seems to bypass them, failover or rules do not take effect, or you need multiple
  subscriptions as mutual primary/backup. Covers DNS poisoning, SNI blocking,
  subscription activation, provider deadlock, fallback wrapping a proxy-group, and
  GEOIP misrouting to direct — with backup, edit, hot-reload or restart, and re-verify.
---

# mihomo 故障诊断与修复

把「代理不能用」拆成三层，逐层用证据定位，再动手改配置：

| 层 | 管什么 | 与平台有关吗 |
|---|---|---|
| **接入层** | 配置在哪、怎么写进去、怎么让它生效 | 有关（本机/SSH/Docker/NAS/客户端），见 `references/platform-access.md` |
| **内核层** | 策略组结构、provider 状态、配置字段 | 无关 |
| **网络层** | DNS、TCP、TLS、SNI、节点存活 | 无关 |

**不要凭症状直接改配置**——最常见的误判是把「订阅被 SNI 阻断」当成「订阅废了」，
从而错误弃用一条完全有效的订阅；其次是拿"出口 IP 没变"当代理失效，其实只是规则判了直连。

## 何时使用

- 代理时好时坏、间歇性断，或重启后突然不能翻墙
- 节点全部延迟超时 / 面板全红 / 日志反复 `pull error`
- 国内正常、境外全断；或所有站点都慢
- 明明有存活节点，某些站点却像没走代理
- 要做「国内+局域网直连、其余走代理」的分流，或两条订阅互为主备
- 需要直接改配置并验证（不管内核跑在什么设备上）

## 工作流程

### 第 0 步：勘察接入层（**先做这步**）

不要问用户"你的配置在哪"，直接跑：

```bash
bash scripts/find_config.sh                    # 本机
bash scripts/find_config.sh --ssh root@10.0.0.2        # 远程主机 / 软路由 / VPS
bash scripts/find_config.sh --docker mihomo            # 配置在容器里（可叠加 --ssh）
bash scripts/find_config.sh --unc                      # 绿联 NAS（unc CLI 已登录）
```

它输出：运行形态 → 配置路径 → 控制接口（逐个试 `/version`）→ secret → providers/策略组清单，
并在末尾打印可直接复制的 `diagnose.sh` / `apply_config.sh` 命令。
细节与各平台差异见 `references/platform-access.md`。

### 第 1 步：跑体检，拿到事实

```bash
bash scripts/diagnose.sh --api http://<host>:9090 --secret '<secret>'
```

六段输出：内核与端口（**代理端口自动从 `/configs` 识别，不假设 7890**）→ 策略组结构与
`now=` 指向 → provider 节点数/存活数/更新时间 → **直连基线 vs 经代理对照** → 出口 IP → 结论。
`secret` 在配置 `secret:` 字段。

### 第 2 步：按分层结果定位

对照 `references/diagnosis-playbook.md` 的决策树。五条最快判据：

| 观察到的现象 | 指向 |
|---|---|
| 国内秒开 + 境外全超时 | 内核与分流都正常，问题在节点这一段 |
| 经代理访问**纯 IP**（1.1.1.1）也 502/超时 | 不是 DNS 污染，是到节点的 TCP 连不上 |
| provider `updatedAt` 停在很久以前 | 订阅拉取失败，一直在用旧节点缓存 |
| 有存活节点但仍不通 | 策略组当前指向不对（卡 DIRECT 或卡死节点） |
| 直连和经代理**都**失败 | 不是 mihomo 的问题，先查本机网络/DNS |

### 第 3 步：订阅拉不下来时，必须逐层探测

```bash
python3 scripts/probe_sub.py "<订阅地址>"          # 默认重试 6 次
```

把失败拆成 DNS 污染 / TCP 阻断 / TLS 阻断 / **SNI 阻断** / 服务端拒绝五类，并给出处置建议。

- `OK_NO_SNI_ONLY` ⇒ 订阅**完全有效**，只是域名被按 SNI 阻断 → 用「引导节点方案」，
  **不要弃用这条订阅**
- `HTTP_ERROR` ⇒ 读返回体 `error_code`：`SUBSCRIPTION_ACTIVATION_REQUIRED` 表示要去服务商
  控制中心人工激活，改配置无效
- 应用层错误码比网络错误更值得先看，能一步排除"白折腾"

### 第 4 步：改配置（用脚本，别手抄命令）

```bash
# 1) 以模板为基线（双订阅互备 + 分流 + DNS 已配好），改出本地副本
cp assets/config-template.yaml /tmp/new.yaml

# 2) 一条命令：校验 YAML → 备份 → 写入 → 回读比对 SHA → 热重载/重启
bash scripts/apply_config.sh --new /tmp/new.yaml \
     --path /etc/mihomo/config.yaml --mode local \
     --restart api --api http://127.0.0.1:9090 --secret '<secret>'

# 拿不准先干跑，只打印不写盘
bash scripts/apply_config.sh ... --dry-run
```

`--mode` 四选一：`local` / `ssh`（配 `--ssh user@host`）/ `docker`（配 `--container`）/ `unc`。
字段约束与坑位见 `references/mihomo-config-notes.md`。

### 第 5 步：验证（四条全过才算修好）

```bash
bash scripts/diagnose.sh --api ... --secret ...
```

- 日志无 `level=fatal`、无 `bind: address already in use`
- 国内站点直连（<100ms）、局域网直连（<20ms）
- 境外站点经代理 `200`（用 google/gstatic 判断，**不要看出口 IP**）
- provider 存活数 > 0，策略组 `now=` 指向真实节点组而不是 DIRECT

### 第 6 步：失败就回滚

```bash
bash scripts/apply_config.sh --rollback 'config.yaml.bak-YYYYMMDD-HHMMSS' \
     --path <配置路径> --mode <local|ssh|docker|unc> --container <c> --restart auto
```

不要在坏配置上叠加改动。备份命名统一 `config.yaml.bak-YYYYMMDD-HHMMSS`。

## 高频根因清单

按实际出现频率排序，遇到对不上的症状先查前四条：

1. **fallback 策略组挂了策略组做子项** —— mihomo 会判为不可用，启动即锁死后备项（通常是
   DIRECT）且**不自愈**。改为 `select` + `url-test` 的 `use:` 多 provider 混池。
2. **provider 没配 `proxy`** —— 拉订阅时走默认出站，节点全挂时形成
   「节点死 → 拉不到订阅 → 一直是旧节点」的死锁。加 `proxy: DIRECT`。
3. **订阅域名被 SNI 阻断** —— 订阅有效但直连永远拉不到。用引导节点走隧道拉取。
4. **DNS 缺 `proxy-server-nameserver`** —— fake-ip 模式下节点域名被解析成 `198.18.x.x`，
   节点全红但看不出原因。
5. **`GEOIP,CN,直连` 排在 `MATCH` 之前** —— 解析到国内 CDN 的境外站点也被判直连，
   表现为"有节点却像没走代理"。判据是出口 IP 与直连相同。
6. **DNS 监听 53 与宿主冲突** —— 改 `0.0.0.0:1053`；软路由/OpenWrt 与 dnsmasq 抢端口尤其常见。
7. **节点 IP 被换/被封** —— 换一台机器复测 `nc -z <ip> <port>`，两边都不通即节点问题。
8. **订阅激活未完成 / 欠费 / 换了域名** —— 只能用户在服务商侧处理。

## 互为主备的正确做法

自动切换靠 `url-test` 的 `use:` 把多条订阅的节点合并成一个池子统一测速。
某一家整片失效时它的节点全部超时被排除，流量自动落到另一家，无需人工干预。
**不要**用 `fallback` 套两个策略组来实现主备（原因见高频根因第 1 条）。

同时保留每个订阅的单独分组（`☁️ 订阅A` / `☁️ 订阅B`），便于观察是谁在顶着、
或在故障时手动锁定只用某一家。

## 三种部署形态速查

| 形态 | 找配置 | 写入 | 生效 |
|---|---|---|---|
| 本机 / SSH | `ps -eo args \| grep mihomo` 看 `-d` `-f` | `cat new.yaml > <path>` | 热重载 `PUT /configs`，或 `systemctl restart mihomo` |
| Docker | `docker inspect` 看 Mounts 与 Cmd | `cat new.yaml \| docker exec -i <c> sh -c 'cat > <path>'` | `docker restart <c>` |
| 绿联 NAS | `unc docker compose ls` 反推目录 | `unc file mv` 腾位 → `unc file upload --verify` | `unc docker restart <c> --yes` |
| 桌面客户端 | GUI 的 profiles 目录 | 改 **profile**，不要改运行时 config.yaml | 客户端内切换/保存 |

## 资源索引

| 文件 | 何时读 |
|---|---|
| `references/platform-access.md` | 第 0 步；找配置、三种传输的坑、热重载 vs 重启、REST API 速查 |
| `references/diagnosis-playbook.md` | 第 2 步；症状→根因决策树、五类订阅故障、引导节点方案、安全改配流程 |
| `references/mihomo-config-notes.md` | 第 4 步；字段含义、策略组类型对比、规则顺序、坑位 |
| `assets/config-template.yaml` | 重建配置时；已验证的双订阅互备 + 分流 + DNS 模板 |
| `scripts/find_config.sh` | 每次开工第一步：判形态、定位配置、发现控制接口 |
| `scripts/diagnose.sh` | 定位与复检；自动识别代理端口，含直连 vs 代理对照 |
| `scripts/probe_sub.py` | 订阅相关故障必跑，判定阻断类型 |
| `scripts/apply_config.sh` | 改配置统一入口；含备份、SHA 复核、热重载、回滚 |

## 安全提醒

- `secret` 与订阅 URL（含 token）都是凭证，不要在聊天以外的地方传播
- `external-controller: 0.0.0.0:9090` 对整段内网开放，不要映射到公网
- 改动前必留备份，改动后必校验 SHA——脚本已内置，别绕过它手工写
- `--dry-run` 用来确认命令拼得对，尤其第一次在陌生设备上操作时
