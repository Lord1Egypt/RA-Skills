# 接入层：找到配置、改它、让它生效（不分平台）

mihomo 可以跑在本机、VPS、Docker、软路由、NAS、桌面客户端里。排障和改配置的逻辑完全一样，
**只有「怎么碰到那个文件」和「怎么让它重新加载」不同**。这份文档就是这两件事的对照表。

配合脚本使用：`scripts/find_config.sh` 自动判形态并给出可用命令，
`scripts/apply_config.sh` 用 `--mode local|ssh|docker|unc` 一次走完备份→校验→写入→复核→生效。

---

## 0. 先判形态

| 形态 | 典型场景 | 怎么认 | 怎么写文件 | 怎么生效 |
|---|---|---|---|---|
| 裸机 / systemd | VPS、Linux 服务器、软路由直装 | `systemctl status mihomo`；`ps -ef \| grep mihomo` | 直接写文件 | `systemctl restart mihomo` |
| 容器（run） | NAS、群晖、Unraid、`docker run` 部署 | `docker ps \| grep mihomo` | `docker exec -i <c> sh -c 'cat > <path>'` | `docker restart <c>` |
| 容器（compose） | 同上但有 compose 项目 | `docker compose ls`；`unc docker compose ls` | 写宿主机挂载目录 | `docker compose restart` / 重启容器 |
| 桌面客户端 | Clash Verge Rev / Mihomo Party / ClashX Meta / FlClash | 有 GUI 进程 | 改 **profile** 或用 GUI | 客户端里切换/保存 |
| 绿联 NAS | unc CLI 已登录 | `unc docker ps` | `unc file upload` | `unc docker restart` |

判断口径：**如果有 Docker 容器在跑内核，就按容器走**——写宿主机上的挂载目录等价，但
`docker cp` / `docker exec` 不会因为搞错挂载点而写了个没人读的副本。

---

## 1. 配置到底在哪

三个来源，按可靠性排序：

```bash
# ① 进程启动参数（最准）：-d 是配置目录，-f 是配置文件
ps -eo pid,args | grep -E '[m]ihomo|[c]lash'
ps -Axo pid,command | grep -E '[m]ihomo|[c]lash'      # macOS 用这个

# ② 容器挂载（Docker 形态）
docker inspect -f '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{println}}{{end}}' <容器>

# ③ 容器启动参数
docker inspect -f '{{json .Config.Cmd}} {{json .Config.Entrypoint}}' <容器>
```

常见默认位置：

| 环境 | 路径 |
|---|---|
| Linux 系统服务 | `/etc/mihomo/config.yaml`、`/etc/clash/config.yaml` |
| 用户级运行 | `~/.config/mihomo/config.yaml`、`/root/.config/mihomo/config.yaml` |
| OpenWrt / OpenClash | `/etc/openclash/config.yaml`、`/etc/openclash/config/*.yaml` |
| Clash Verge Rev | `~/Library/Application Support/io.github.clash-verge-rev.clash-verge-rev/profiles/*.yaml`（macOS）<br>`%APPDATA%\io.github.clash-verge-rev.clash-verge-rev\profiles\`（Windows） |
| Mihomo Party | `~/.config/mihomo-party/profiles/`、`%APPDATA%\mihomo-party\profiles\` |
| ClashX Meta | `~/.config/clash.meta/config.yaml`、`~/Library/Application Support/com.west2online.ClashXMeta/profiles/` |
| 群晖 / 绿联等 NAS | 通常 `<卷>/docker/compose/<项目>/config/config.yaml` |

> **桌面客户端的坑**：GUI 会把 profile 渲染成运行时 `config.yaml`，直接改运行时文件下次切订阅就被覆盖。
> 要改就改 profile，或者在 GUI 里改。

---

## 2. 写文件：三种传输的差异与坑

### 2.1 本机 / SSH —— 原地写，别 mv

```bash
cp -p <path> <path>.bak-$(date +%Y%m%d-%H%M%S)     # 备份
cat new.yaml > <path>                              # 原地写，保留 inode
```

- **不要** `mv new.yaml <path>`：bind mount / 硬链接场景下 inode 变了，容器里看到的还是旧内容
- 权限不够就 `sudo`，但注意 `sudo` 后文件属主可能变，必要时 `chown` 回来

SSH 等价：`cat new.yaml | ssh user@host 'cat > /etc/mihomo/config.yaml'`

### 2.2 Docker —— exec 写，或写挂载目录

```bash
docker exec <c> cp /root/.config/mihomo/config.yaml /root/.config/mihomo/config.yaml.bak
cat new.yaml | docker exec -i <c> sh -c 'cat > /root/.config/mihomo/config.yaml'
docker restart <c>
```

- 用 `exec ... sh -c 'cat >'` 而不是 `docker cp`：`docker cp` 走 tar 解包，对**单文件 bind mount**
  有概率换掉 inode 导致"写了但没生效"
- 路径用**容器内**路径；宿主机挂载路径也可以，但要先 `docker inspect` 确认映射

### 2.3 绿联 NAS（unc CLI）—— 两个必踩的坑

前提：已登录 `unc auth status`。`unc` 没有 `exec`，所以只能走「文件接口 + REST API」。

**坑 1：`unc file upload` 不覆盖同名文件**，会自动改名成 `config(1).yaml`，不报错。
容器读的还是旧文件，造成"改了没生效"的假象。

**坑 2：`unc file mv` 的第二参数是"同目录下的新名字"，不是目标路径**。传绝对路径报
`Target location does not exist`，传 `目录/新名字` 报 `not a directory`。

**正确姿势（备份=改名，腾出目标位）**：

```bash
D=/volume3/docker/compose/mihomo/config
unc file mv "$D/config.yaml" "config.yaml.bak-20261111-210000" --yes   # 源用绝对路径，目标是裸名
unc file upload /tmp/new.yaml "$D/config.yaml" --verify
unc file cat "$D/config.yaml" -f raw > /tmp/back.yaml && shasum -a 256 /tmp/back.yaml /tmp/new.yaml
unc docker restart <容器> --yes
```

其它要点：
- 先 `unc file ls-root` 摸清有哪些卷（`/volume1` / `/volume2` / `/volume3`），再逐层 `ls`
- `unc file cat <p> -f raw` 才是原始内容，不带 `-f raw` 是 JSON 包装，做 diff 会很难受
- host 网络模式下 `unc docker ps` 的 PORTS 列显示 `-`，属正常
- 回滚时**源路径必须是绝对路径**，裸名会报 `PermissionDenied`（脚本已处理）

---

## 3. 让它生效：热重载 vs 重启

### 热重载（优先，不中断现有连接）

```bash
curl -s -X PUT -H 'Authorization: Bearer <secret>' -H 'Content-Type: application/json' \
  -d '{"path": "/root/.config/mihomo/config.yaml"}' http://127.0.0.1:9090/configs
```

- `path` 是**内核进程看到的路径**（容器内路径），不是宿主机路径
- 返回 204 即成功
- **不生效的字段**：`external-controller`、`port` / `mixed-port` / `socks-port`、
  `tun`、`redir-port`、`tproxy-port`、`sniffer` 这类启动期参数——改了这些必须重启
- 也可以用 `{"payload": "<整段 YAML 字符串>"}` 直接推内容，适合改完不落盘的临时验证

### 需要重启的情况

```bash
docker restart <c>                    # 容器
systemctl restart mihomo              # 系统服务
unc docker restart <c> --yes          # 绿联 NAS
/etc/init.d/mihomo restart            # OpenWrt 直装
docker compose restart mihomo         # compose
```

重启后第一件事看日志，不是看面板：

```bash
docker logs --tail 50 <c>
journalctl -u mihomo -n 50 --no-pager
unc docker logs <c> --format raw | tail -50
```

要看到 `listening at: [::]:7890` 之类；出现 `level=fatal`、`bind: address already in use`
立刻回滚。

---

## 4. 回滚

原则：**不要在坏配置上叠加改动**。先回滚到能用的版本，再重做一次。

```bash
# 脚本方式（推荐，含同名冲突处理与失败保护）
bash scripts/apply_config.sh --rollback 'config.yaml.bak-20261111-210000' \
     --path <配置路径> --mode <local|ssh|docker|unc> --container <c> --restart auto

# 手工（unc）
unc file mv "$D/config.yaml" "config.yaml.broken-$(date +%H%M%S)" --yes
unc file mv "$D/config.yaml.bak-20261111-210000" "config.yaml" --yes
unc docker restart <c> --yes
```

---

## 5. 通过 RESTful API 做运行期诊断（比读日志快）

secret 在配置 `secret:` 字段。所有请求都要带 `--noproxy '*'`，否则可能被本机代理干扰。

```bash
S='<secret>'; H='http://<host>:9090'
curl -s --noproxy '*' -H "Authorization: Bearer $S" $H/version
curl -s --noproxy '*' -H "Authorization: Bearer $S" $H/configs          # 端口/模式/tun
curl -s --noproxy '*' -H "Authorization: Bearer $S" $H/proxies          # 策略组与 now
curl -s --noproxy '*' -H "Authorization: Bearer $S" $H/providers/proxies
curl -s --noproxy '*' -H "Authorization: Bearer $S" $H/providers/proxies/<名>/healthcheck
```

切换某组的选择（运行期生效，不写盘）：

```bash
G=$(python3 -c "import urllib.parse;print(urllib.parse.quote('🚀 节点选择'))")
curl -s --noproxy '*' -X PUT -H "Authorization: Bearer $S" -H 'Content-Type: application/json' \
  -d '{"name":"DIRECT"}' "$H/proxies/$G"
```

单节点测速 / 整组测速：

```bash
N=$(python3 -c "import urllib.parse;print(urllib.parse.quote('🇯🇵 日本-4'))")
curl -s --noproxy '*' -H "Authorization: Bearer $S" \
  "$H/proxies/$N/delay?timeout=5000&url=https%3A%2F%2Fwww.gstatic.com%2Fgenerate_204"
G=$(python3 -c "import urllib.parse;print(urllib.parse.quote('🚀 节点选择'))")
curl -s --noproxy '*' -H "Authorization: Bearer $S" \
  "$H/group/$G/delay?timeout=5000&url=https%3A%2F%2Fwww.gstatic.com%2Fgenerate_204"
```

要点：
- provider 里的节点在 `/proxies` 顶层**查不到**（返回 `Resource not found`），走
  `/providers/proxies/<provider名>`；对组测速用 `/group/<组名>/delay`
- 节点名/组名必须 URL 编码（含 emoji、空格、中文）
- `/configs` 返回里**没有 secret**，需要从配置文件读

---

## 6. 环境变量陷阱

本机 shell 可能自带 `HTTP_PROXY` / `HTTPS_PROXY`（公司代理、WorkBuddy 内部代理等）。
做"直连判定"时必须加 `--noproxy '*'`，否则测的是本机代理而不是真实网络，
会得出完全相反的结论。脚本里所有探测都带了这个参数——手工复测时别忘了。
