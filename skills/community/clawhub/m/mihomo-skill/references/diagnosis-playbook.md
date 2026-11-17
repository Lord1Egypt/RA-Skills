# mihomo 故障排查手册（症状 → 根因 → 处置）

mihomo 的绝大多数"代理不能用"都落在下面 6 类里。**先分层定位，再动手改配置**，
否则很容易把"订阅被 SNI 阻断"误判成"订阅废了"而错误弃用一条好订阅。

---

## 分层定位顺序（不要跳步）

```
① 内核活着吗？    控制接口 /version 是否响应、代理端口是否 LISTEN
                   （代理端口不一定是 7890：读 /configs 的 mixed-port / port）
   ↓ 活着
② 策略组指向哪？   /proxies 看 now= 什么。指向 DIRECT / 死节点 / 空组
   ↓ 指向正常
③ provider 有节点吗？ /providers/proxies 看 节点数 / 存活数 / updatedAt
   ↓ 有存活节点
④ 为什么不通？     直连 vs 代理对比；纯 IP 对比（区分 DNS 与链路）
   ↓ 节点全失效
⑤ 为什么拉不到订阅？ scripts/probe_sub.py 逐层判 DNS / TCP / TLS / SNI / 应用层
```

关键判据：**国内站点能秒开、境外全超时** ⇒ 内核与 DNS 分流都正常，问题在节点这一段。
**连纯 IP（如 1.1.1.1）经代理也 502** ⇒ 不是 DNS 污染，是到节点的 TCP 连不上。

---

## 症状 1：节点全部延迟超时 / 全红

先分三种，别混为一谈：

| 现象 | 根因 | 处置 |
|---|---|---|
| provider `updatedAt` 停在很久以前 | 订阅拉取失败，一直在用旧节点 | 见「症状 2」 |
| 节点 `server` 是域名，域名解析到境外 IP，端口 `i/o timeout` | 节点服务器换了 IP / 被封 | 更新订阅；同时从**另一台机器** `nc -z <ip> <port>` 复测，排除本机侧问题 |
| 节点参数（uuid/pbk）过期 | 服务商换了节点配置 | 只能更新订阅 |

**排除本机侧**的方法：换一台机器/换一条出口 `nc -z 节点IP 节点端口`，与运行内核那台的
结果对比。两边都不通 ⇒ 节点问题，不要再折腾本机配置。

## 症状 2：订阅拉不下来（mihomo 日志 `pull error`）

这是最容易误判的一类。**必须先跑 `scripts/probe_sub.py <订阅URL>`**，它会把
"拉不下来"拆成 DNS / TCP / TLS / SNI / 应用层五层。常见五种：

### 2a. `403` + `SUBSCRIPTION_ACTIVATION_REQUIRED`
服务商防滥用机制，必须在控制中心人工点一次"激活订阅"，然后 60 秒内更新。
- 这类**不是配置问题，改配置无效**
- 用 `curl -A "clash.meta/1.19.0" <url>` 看返回的 JSON `error_code` 确认
- 若控制中心页面打不开（Cloudflare 人机验证会挡住 curl，别据此判断站点挂了），让用户用浏览器开

### 2b. DNS 污染
`dig @8.8.8.8 <host>` 返回 `93.46.8.90`、`46.82.174.69`、`8.7.198.46` 这类地址。
- 真实地址通常由系统 DNS / 119.29.29.29 返回
- 处置：主配置 `dns` 段补 `default-nameserver` + `proxy-server-nameserver`（国内 DoH），
  避免 fake-ip 模式把节点/订阅域名解析到假 IP

### 2c. SNI 阻断（本次真实案例，极易误判）
特征：**TCP 443 能连，TLS ClientHello 一发出去就 `Connection reset by peer`**。
- `probe_sub.py` 的 `tls_with_sni` = RST，`tls_without_sni` = HTTP 200 + 完整配置
- RST 常是概率性的：单次失败不代表被墙，务必重试（脚本默认 `--tries 6`）
- 结论：订阅内容完好，只是 mihomo 直连永远拉不到
- **处置见「引导节点方案」**

### 2d. 订阅域名换了
服务商换域名后旧域名返回 `Invalid` / 404。让用户提供新地址，替换 `url`。
注意新域名可能落在 Cloudflare 后面，Web 页面会被人机验证挡住，但订阅端点仍可用。

### 2e. 订阅更新死锁
provider 没配 `proxy`，mihomo 拉订阅时走默认出站（`🚀 节点选择`）→ 节点全死 →
拉不到订阅 → 节点永远旧。**环**。
- 处置：provider 加 `proxy: DIRECT`（或 `proxy: <引导节点>`）切断依赖

---

## 引导节点方案（破 SNI 阻断 / 破死锁）

适用：订阅内容有效，但订阅域名被阻断、直连拉不到。

1. 用 `probe_sub.py` 不带 SNI 的方式**取一次完整订阅内容**（或让用户从服务商后台复制）
2. 从内容里挑一个节点做静态节点，写进主配置 `proxies:`（命名如 `🐣 引导`）
3. 该订阅的 provider 设 `proxy: 🐣 引导`
4. 之后订阅更新全部走这条节点隧道，隧道内没有 SNI 检测，一次成功
5. 记得给 provider 加 `exclude-filter`，滤掉「剩余流量 / 套餐到期 / 官网」这类信息型伪节点

为什么有效：SNI 阻断发生在本地出口到目标之间的明文握手阶段；走隧道后，
ClientHello 在隧道内部发出，出口由节点服务器完成，阻断点被绕过。

**自愈性**：只要引导节点本身可用，订阅就能持续更新；引导节点失效时 provider 会
回落到磁盘缓存（`proxy_provider/*.yaml`），不会立刻清空节点。

---

## 症状 3：国内能上、境外全断

- provider 全失效（见症状 1/2）
- 或策略组卡在死节点 / 卡在 DIRECT（见下一条）

## 症状 4：重启后突然不能翻墙，但节点其实是好的

**头号嫌疑：`fallback` 类型策略组挂了策略组作为子项。**

mihomo 的 `Fallback` 对"子项是策略组"的处理不可靠：它能报出该组的延迟，
但内部仍判为不可用 ⇒ 启动瞬间 fallback 直接落到后备项（通常是 `DIRECT`），
而且**之后不会自愈**（`history` 一直是空的）。

正确做法：

```yaml
# ✗ 不要这样
- name: 🚀 节点选择
  type: fallback
  proxies: [🔯 自动选择, DIRECT]

# ✓ 这样
- name: 🚀 节点选择
  type: select
  proxies: [🔯 自动选择, ☁️ 订阅A, ☁️ 订阅B, 🖐️ 手动切换, DIRECT]

- name: 🔯 自动选择
  type: url-test
  use: [订阅A, 订阅B]
  interval: 180
  tolerance: 30
  lazy: false
```

自动切换交给 `url-test` 的 `use:` 多 provider 混池——比整组 fallback 更细，
也不会出现"整组切换时那一组其实半死"的情况。

## 症状 5：启动日志 `bind: address already in use`（0.0.0.0:53）

host 网络模式（或裸机/路由器直装）下与宿主机自带的 DNS 抢 53 端口，mihomo 内置 DNS 起不来。
容器 bridge 网络一般不会撞，但也常见于软路由 / OpenWrt 同时跑 dnsmasq。
- 处置：`dns.listen` 改 `0.0.0.0:1053`
- 顺带确认客户端或下游设备没用 53 直连它

## 症状 6：能通但很慢 / 时好时坏

- `url-test` 的 `interval` 太长（默认可能 300s+），节点劣化后迟迟不换 → 调小到 120–180
- `tolerance` 太小导致频繁抖动切换 → 20–50 之间
- 节点里混着信息型伪节点（"剩余流量：99 GB"）参与测速 → 用 `exclude-filter` 滤掉

---

## 健康检查用哪种 URL

统一用 `https://www.gstatic.com/generate_204`（返回 204，体积最小、最稳）。
不要用需要真实内容的 URL，否则测的是带宽不是连通性。

**出口 IP 不能当判据**：用 `ipinfo.io` / `ip.sb` 之类的查询站验证"是否走了节点"并不可靠——
规则里 `GEOIP,CN,直连` 排在 `MATCH` 之前时，很多境外站点会解析到国内 CDN 的 IP 从而被判直连，
查询站返回的就是你家宽带 IP。判断代理是否真的生效，要用**固定境外域名**（google/gstatic）的
连通结果，而不是出口 IP 是否变化。

---

## 症状 7：明明有节点、却像没走代理

现象：google 打不开，但换成 IP 查询站却显示"出口没变"。
根因往往不是代理坏了，而是**规则把它判成了直连**——`GEOIP,CN,🎯 国内直连` 放在 `MATCH` 之前，
域名只要解析到国内 CDN（Cloudflare 中国合作节点、Akamai CN 等）就会落到直连组。
- 判据：`diagnose.sh` 第 [4] 段，google/youtube 经代理 200，而查询站走直连 → 属正常
- 真要强制走代理：把该域名加 `DOMAIN-SUFFIX,xxx,🚀 节点选择` 放在 `GEOIP` 之前
- 别为了"出口 IP 没变"去改节点或换订阅，那是白折腾

---

## 改配置的安全流程（任何一次改动都走这套）

1. **先备份**——`scripts/apply_config.sh` 会自动把现配置改名成 `config.yaml.bak-YYYYMMDD-HHMMSS`
2. 本地改副本，上传前**校验 YAML**（脚本内置，失败直接退出，不会写坏线上文件）
3. 上传后**回读比对 SHA-256**（脚本内置，不一致就报错并给回滚命令）
4. 让配置生效：`--restart api` 热重载 或 `--restart docker/unc/systemd` 重启
5. 用 `scripts/diagnose.sh` 复检：分流、策略组、provider 存活、境外连通
6. 出问题：`bash scripts/apply_config.sh --rollback <备份文件名> --path ... --mode ...`

```bash
# 一条命令走完 备份 -> 校验 -> 写入 -> SHA 复核 -> 重启
bash scripts/apply_config.sh --new ./new.yaml --path <配置路径> --mode local \
     --restart api --api http://127.0.0.1:9090 --secret 'xxx'
# 拿不准就加 --dry-run，只打印命令不写盘
```
