# mihomo 配置要点与坑位速查

只记"改错会出问题"的地方，不重复官方文档。

## 1. proxy-providers（订阅）

```yaml
proxy-providers:
  订阅名:
    type: http
    url: "https://..."
    interval: 3600            # 秒；太长会长期用旧节点
    path: ./proxy_provider/订阅名.yaml   # 磁盘缓存，拉取失败时回落到它
    proxy: DIRECT             # ★ 拉订阅走哪个出站，不写会走默认出站造成死锁
    exclude-filter: "流量|到期|重置|官网"  # 滤掉信息型伪节点
    # filter: "香港|HK"       # 只要匹配的节点
    health-check:
      enable: true
      interval: 600
      url: https://www.gstatic.com/generate_204
```

- `proxy` 可填 `DIRECT`、某个节点名、或某个策略组名
- **不要**让 `proxy` 指向"依赖本 provider 的策略组"→ 循环依赖
- `path` 是缓存位置；节点全挂时 mihomo 会继续用这个文件里的旧节点
- `url-test` 里 `use: [A, B]` 会把两个 provider 的节点合并成一个池子测速

## 2. proxy-groups（策略组）

| type | 行为 | 适用 | 坑 |
|---|---|---|---|
| `select` | 手工选，不自动变 | 总出口 | 全挂也不会自动换 |
| `url-test` | 定时测速选最低延迟 | 节点池自动切换 | 全挂时保留上次选择，不回落 |
| `fallback` | 按顺序取第一个可用的 | 主备 | **子项不能是策略组**，否则启动即锁死后备项且不自愈 |
| `load-balance` | 按策略分散 | 大流量下载 | 对同一站点的会话可能落到不同出口，易触发风控 |

公共字段：`url`、`interval`、`tolerance`（url-test 切换阈值）、`lazy`、`timeout`。

**推荐的总出口结构**（本 skill 采用）：

```
🚀 节点选择 (select) → 🔯 自动选择
🔯 自动选择 (url-test, use: [订阅A, 订阅B])   ← 互为主备在这一层
☁️ 订阅A / ☁️ 订阅B  (url-test, use: 单个)     ← 便于观察/锁定
🖐️ 手动切换 (select, use: [订阅A, 订阅B])
🎯 国内直连 (select) → DIRECT
```

## 3. DNS

```yaml
dns:
  enable: true
  listen: 0.0.0.0:53          # host 网络下常与宿主 DNS 抢端口，撞了就改 1053
  enhanced-mode: fake-ip
  fake-ip-range: 198.18.0.1/16
  fake-ip-filter: ['*.lan', '*.localdomain', '*.localhost']
  default-nameserver:          # 用来解析 nameserver 自身，必须是 IP
    - 223.5.5.5
    - 119.29.29.29
  proxy-server-nameserver:     # ★ 解析"节点服务器域名"用，避免被 fake-ip 污染
    - https://dns.alidns.com/dns-query
    - 223.5.5.5
  nameserver:
    - 223.5.5.5
    - 114.114.114.114
  fallback:
    - https://dns.alidns.com/dns-query
    - https://doh.pub/dns-query
  fallback-filter:
    geoip: true
    geoip-code: CN
```

坑：
- **缺 `proxy-server-nameserver`** ⇒ fake-ip 模式下节点域名可能被解析成 `198.18.x.x`，节点全红却查不出原因
- `default-nameserver` 只接受 IP，不要填 DoH 域名
- 53 被占用时日志是 `listen 0.0.0.0:53: bind: address already in use`，但**其余功能照常**，容易忽略

## 4. 分流规则

顺序敏感，从上到下第一条命中即停。推荐顺序：

```yaml
rules:
  # 1. 必须走代理的（放在 GEOIP 之前）
  - DOMAIN-SUFFIX,google.com,🚀 节点选择
  - DOMAIN-SUFFIX,github.com,🚀 节点选择
  # 2. 局域网 / 内网（一定要 no-resolve，否则会触发 DNS 查询拖慢）
  - IP-CIDR,127.0.0.0/8,DIRECT,no-resolve
  - IP-CIDR,192.168.0.0/16,DIRECT,no-resolve
  - IP-CIDR,10.0.0.0/8,DIRECT,no-resolve
  - IP-CIDR,172.16.0.0/12,DIRECT,no-resolve
  - IP-CIDR,169.254.0.0/16,DIRECT,no-resolve
  - IP-CIDR6,::1/128,DIRECT,no-resolve
  - IP-CIDR6,fe80::/10,DIRECT,no-resolve
  - IP-CIDR6,fc00::/7,DIRECT,no-resolve
  - DST-PORT,5353,DIRECT          # mDNS
  # 3. 国内 IP 直连
  - GEOIP,CN,🎯 国内直连
  # 4. 兜底
  - MATCH,🚀 节点选择
```

坑：
- `IP-CIDR` 不加 `no-resolve` 会为了判断规则去解析域名，局域网请求会变慢
- `GEOIP,CN` 必须放在"必须走代理"的域名规则之后，否则 google 的国内 CDN IP 会被判直连
- 规则里引用的策略组名必须存在，否则 mihomo 启动直接报错

## 5. 静态节点与 vless/reality

```yaml
proxies:
  - name: 🐣 引导节点
    type: vless
    server: node.example.com
    port: 43006
    uuid: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    network: tcp
    udp: true
    tls: true
    flow: xtls-rprx-vision
    servername: dl.example.com        # reality 伪装 SNI
    client-fingerprint: chrome
    skip-cert-verify: false
    reality-opts:
      public-key: xxxxx
      short-id: xxxx
```

坑：
- `flow` 必须与订阅里一致（`xtls-rprx-vision` 或空），写错会握手失败
- `short-id` 在 YAML 里如果是纯数字串要加引号（`'05'`），否则会被当成数字丢前导零
- 静态节点不自动测速，也不会自动更新

## 6. 安全

- `secret` 明文写在 `config.yaml` 里，且 `external-controller: 0.0.0.0:9090` 对内网全开
- 建议：secret 用长随机串，暴露面只给内网；不要把 9090 映射到公网
- 订阅链接本身即凭证（`token` 在 URL 里），泄露等于账号被白嫖
