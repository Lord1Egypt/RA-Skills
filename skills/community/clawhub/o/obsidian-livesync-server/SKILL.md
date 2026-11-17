---
name: obsidian-livesync-server
description: Deploy a self-hosted Obsidian LiveSync server (CouchDB in Docker behind a Cloudflare Tunnel with zero inbound ports), covering upstream provisioning, Setup URI generation with mandatory end-to-end encryption, a post-deploy security audit, and a tested backup/restore procedure. Use when building a private Obsidian sync backend with no exposed ports.
version: 0.1.0
license: MIT-0
platforms: [linux]
metadata:
  openclaw:
    requires:
      bins: [docker, curl]
    envVars:
      - name: COUCHDB_USER
        required: false
        description: CouchDB admin username you choose during deployment (not pre-existing).
      - name: COUCHDB_PASSWORD
        required: false
        description: CouchDB admin password you generate with openssl rand -hex 24; store in a 600-mode env file.
      - name: LIVESYNC_PASSPHRASE
        required: false
        description: End-to-end encryption passphrase for the LiveSync Setup URI; store in a password manager.
    tags: [obsidian, couchdb, cloudflare-tunnel, docker, sync]
  hermes:
    tags: [obsidian, couchdb, cloudflare-tunnel, docker, sync]
---

# Obsidian LiveSync 服务端部署

**Overview (EN).** Stand up a private Obsidian LiveSync backend with no exposed
ports: CouchDB bound to loopback inside Docker, reached only through an
outbound-only Cloudflare Tunnel, with mandatory end-to-end encryption. Includes
upstream provisioning (pinned release), Setup URI generation, a post-deploy
security audit, and a backup/restore procedure you actually rehearse. The rest of
this document is in Chinese.

## 架构（推荐形态，安全最佳实践）

CouchDB 容器只绑 `127.0.0.1:5984` → cloudflared Tunnel（纯出站，零入站端口）→ CF 边缘 HTTPS 域名。客户端用 Setup URI 一键导入，端到端加密（passphrase + 路径混淆）必须开。

E2E 加密是硬性要求，不是可选项：不开启时数据库里是明文笔记，而隧道运营商（Cloudflare）在边缘终止 TLS，能看到回源明文。

## 部署步骤

1. **目录与权限**（uid 必须 5984，否则容器起不来）：
   ```bash
   sudo mkdir -p /opt/obsidian-livesync/{couchdb-data,couchdb-etc}
   sudo chown -R 5984:5984 /opt/obsidian-livesync/couchdb-{data,etc}
   sudo chmod 750 /opt/obsidian-livesync
   ```
   路径可换，但下面所有命令要跟着换。

2. **凭证**：`COUCHDB_USER`、`COUCHDB_PASSWORD`（`openssl rand -hex 24` 生成）写进你已在用的环境变量文件（Hermes 用 `hermes config env-path` 给出的文件），权限 600；聊天/脚本/仓库不硬编码。

3. **起容器**（固定次版本号，避免 `latest` 突然跨大版本；端口必须带 `127.0.0.1:` 前缀，否则等于把数据库发布到所有网卡）：
   ```bash
   docker run --name couchdb-for-ols -d --restart always -u 5984:5984 \
     -e COUCHDB_USER=$COUCHDB_USER -e COUCHDB_PASSWORD=$COUCHDB_PASSWORD \
     -v /opt/obsidian-livesync/couchdb-data:/opt/couchdb/data \
     -v /opt/obsidian-livesync/couchdb-etc:/opt/couchdb/etc/local.d \
     -p 127.0.0.1:5984:5984 couchdb:3.5
   ```
   宿主有 compose 插件时可写成单服务 compose 文件，映射同样是 `127.0.0.1:5984:5984`；上面的 docker run 在无 compose 的旧版 Docker（如 20.10）上也能用。
   `-p 127.0.0.1:5984:5984` 是显式回环绑定，**不依赖** `daemon.json` 里的任何全局设置——因此本流程不会改动 Docker 守护进程配置，也不会影响这台机器上的其他容器。

   继续前先确认只监听回环：
   ```bash
   ss -tlnp | grep 5984     # 期望 127.0.0.1:5984，不应出现 0.0.0.0:5984
   ```

4. **上游脚本初始化**（LiveSync 自带 provisioning；固定 release tag，先下载、审阅、再执行；需要 Deno，没有则装发行版包，或下载 `deno.land/install.sh` 审阅后执行）：
   ```bash
   curl -fsSL -o /tmp/couchdb-init.sh \
     https://raw.githubusercontent.com/vrtmrz/obsidian-livesync/1.0.42/utils/couchdb/couchdb-init.sh
   less /tmp/couchdb-init.sh     # 审阅：确认只读写 127.0.0.1:5984、只动 obsidiannotes
   sha256sum /tmp/couchdb-init.sh   # 记录基线，日后可用于比对（macOS 用 shasum -a 256）
   ```
   确认无误后再执行（同一 shell 会话内设置变量，避免口令进入历史）：
   ```bash
   export hostname=http://127.0.0.1:5984 username=$COUCHDB_USER password=$COUCHDB_PASSWORD database=obsidiannotes
   bash /tmp/couchdb-init.sh
   # 成功标志: CouchDB provisioning completed.
   rm -f /tmp/couchdb-init.sh
   ```
   验证（交互式终端，curl 单独提示输入口令，不把口令放进进程参数）：
   ```bash
   curl -u "$COUCHDB_USER" http://127.0.0.1:5984/_up          # 期望 {"status":"ok"}
   curl -u "$COUCHDB_USER" http://127.0.0.1:5984/_all_dbs     # 应含 obsidiannotes
   ```
   无人值守/自动化场景改用权限受限的 `~/.netrc`（`chmod 600`）或 `.curlrc` 里的 `--user`，不要用 `curl -u user:pass`：变量展开后的值会短暂出现在 `/proc/<pid>/cmdline`，同机其他用户可读。curl 官方文档对此有明确提示。
   该脚本会开启 `require_valid_user`、设置 LiveSync 需要的 CORS origins、并建库。

5. **Cloudflare Tunnel**：
   - 装 cloudflared（GitHub release .deb）
   - `cloudflared tunnel login`（后台跑，把 URL 给用户浏览器授权，cert.pem 落 `~/.cloudflared/`；URL 有效期短，尽快打开）
   - `cloudflared tunnel create obsidian-livesync`
   - 写 `~/.cloudflared/config.yml`：ingress `hostname: <域名>` → `service: http://127.0.0.1:5984`，兜底 `http_status:404`（必须留，否则隧道拒绝启动）
   - `credentials-file` 指向 `tunnel create` 实际写出的 JSON；`cloudflared service install` 会把配置和凭证复制到 `/etc/cloudflared/`，手写配置时路径对不上是"隧道起不来"的常见原因
   - `cloudflared tunnel route dns obsidian-livesync <域名>`（自动加 CNAME）
   - `cloudflared service install && systemctl enable --now cloudflared`，日志确认 4 条 `Registered tunnel connection`

6. **生成 Setup URI**（E2E passphrase 生成后也存为 `LIVESYNC_PASSPHRASE`，并让用户存进密码管理器）：
   ```bash
   export hostname=https://<域名> username=$COUCHDB_USER password=$COUCHDB_PASSWORD \
     database=obsidiannotes passphrase=$LIVESYNC_PASSPHRASE
   deno run --allow-env --allow-net \
     https://raw.githubusercontent.com/vrtmrz/obsidian-livesync/1.0.42/utils/setup/generate_setup_uri.ts
   ```
   输出的 `uri_passphrase` 只显示一次。Setup URI 本身等同密码：通过不长期留存的渠道交付（ spoiler 遮罩）。加第二台设备改为在已配好的设备上 Generate Setup URI，不要复用第一个。

## 安全审计清单（部署后必查）

- `ss -tlnp`：公网监听只应包含你明确开放的端口；CouchDB 必须是 `127.0.0.1:5984`
- 可选加固：`/etc/docker/daemon.json` 设置 `"ip": "127.0.0.1"`。Docker 默认把发布端口绑到 `0.0.0.0`，这条能兜底防止将来别的容器误发布；但它影响这台机器上**所有**容器，属全局改动，只在清楚后果时启用。本流程不依赖它。
- 无凭证访问域名 → 401（`require_valid_user=true`）
- `_config/cors.origins` 仅 `app://obsidian.md,capacitor://localhost,http://localhost`；出现 `*` 表示任何网页都能在浏览器里直接连这个库
- `~/.cloudflared/` 目录 700、`cert.pem` 600、tunnel json 400
- Erlang 端口 4369/9100 不发布到宿主机
- 信任点说明：CF 边缘终止 TLS 可见明文回源，但 LiveSync E2E 加密已抵消；反过来说，拿到宿主访问权 + CouchDB 口令 = 拿到全部数据

## 自动备份

CouchDB 的 `.couch` 文件追加写入，允许在运行期间复制；但官方推荐的顺序是**先备份索引、再备份数据库文件，配置目录单独处理**，并且普通 tar 不等于"已验证可恢复"。下面按这个顺序拆成三份：设计文档（索引定义）→ 数据目录 → 配置目录。

先建目录并记录索引定义（索引可由设计文档重建，备份定义即可，不必复制索引文件）：

```bash
BK=/var/backups/livesync-$(date +%F)
mkdir -p "$BK"
curl -u "$COUCHDB_USER" http://127.0.0.1:5984/obsidiannotes/_design_docs > "$BK/design-docs.json"
```

再复制数据目录并单独打包配置（`couchdb-etc` 里是 `require_valid_user`、CORS、admin 等本地配置，恢复时漏掉会得到一个"能启动但行为不对"的库）：

```bash
tar -C /opt/obsidian-livesync -czf "$BK/couchdb-data.tar.gz" couchdb-data
tar -C /opt/obsidian-livesync -czf "$BK/couchdb-etc.tar.gz"  couchdb-etc
sha256sum "$BK"/*.tar.gz "$BK"/*.json > "$BK/SHA256SUMS"
```

### 恢复（必须在目标服务停止后执行）

```bash
docker stop couchdb-for-ols
# 先把现有数据目录移开，不要就地覆盖——恢复失败时需要能退回
mv /opt/obsidian-livesync/couchdb-data /opt/obsidian-livesync/couchdb-data.bak-$(date +%s)
tar -C /opt/obsidian-livesync -xzf "$BK/couchdb-data.tar.gz"
tar -C /opt/obsidian-livesync -xzf "$BK/couchdb-etc.tar.gz"
chown -R 5984:5984 /opt/obsidian-livesync/couchdb-{data,etc}
docker start couchdb-for-ols
```

恢复后逐项核对，而不是只看容器起来了：`_up` 返回 ok；`_all_dbs` 含 `obsidiannotes`；文档数与备份前一致；用**已配置客户端**做一次写入/同步，确认 E2E 解密正常（索引缺失会表现为查询变慢而非报错，容易被忽略）。确认无误后再删 `couchdb-data.bak-*`。

**恢复流程要实测一次**——没演练过的备份只是猜测。异地副本用宿主机既有的工具（rclone / restic / Borg）推送；加密副本的口令存在"被备份机器之外"。调度器用系统 cron、systemd timer 或 agent cron 都行，关键是有异地副本和定期恢复演练，而不是具体用哪个调度器。

## 多远程共存（客户端概念）

插件支持一库多远程档案（Connection settings → Saved connections，连接串 `sls+https://` / `sls+s3://` / `sls+p2p://`），但**同时只有一个激活主远程**；第二远程（如 R2）只能切换后跑 one-shot replication，非自动双写。自动双份用上面的服务端备份更省心。

## 坑

- **`-p 5984:5984` 不带 `127.0.0.1:` 前缀 = 把数据库发布到公网**。隧道会让这个错误难以察觉：一切照常工作。
- 不开 E2E 加密，等于把明文笔记留在你可能不完全掌控的宿主上。
- provisioning 脚本以固定 tag 下载到 `/tmp`、审阅后再执行。升级版本时重新审阅并对比 `sha256sum`。
- `couchdb:latest` 迟早会跨大版本。固定 `couchdb:3.5`（或有意升级），升级后重跑安全审计。
- 无 compose 的旧版 Docker（如 20.10）用 docker run 即可，不必先装 compose 插件。
- 前台执行 `docker compose up`/`docker run`（不带 `-d`）会被监管进程当作长跑任务杀掉；用 `-d` 或进程管理器的后台模式。
- tunnel login 的授权 URL 有效期短，让用户尽快打开。
- `couchdb-init.sh` 输出大量 npm Download 行属正常，看结尾 "provisioning completed"。
- 交付 Setup URI 时不要走会长期留存的渠道：它包含数据库口令和 E2E passphrase。

## License and provenance

部署步骤为原创文字。初始化和 Setup URI 脚本由
[vrtmrz/obsidian-livesync](https://github.com/vrtmrz/obsidian-livesync)（MIT）
提供，本 skill 只调用、不内嵌。CouchDB、cloudflared、Deno 各自遵循其自身许可。
本文件以 MIT-0 发布（ClawHub 对所有已发布 skill 采用的许可），`license:` 字段
在直接读 git 仓库时同样成立。
