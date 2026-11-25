---
name: local-dev-stack-bootstrap
description: "Bootstrap a local dev stack for browser preview without root or Docker: install databases and services, debug vanishing background processes, inject multi-line secrets into systemd, and fix the UI-opens-but-login-404s case."
---

# 本地开发环境搭起来（无 root / 无 docker）

用于：把项目在本机跑起来、要能在浏览器里预览它的 Web 面板；主机没有 root（`sudo -n true` 不通过）、没有 docker；或遇到「后台服务起来一会儿就没了」「界面能开但登录 404」「多行密钥要注入 systemd」。

## 0. 先定验收口径

跑通的判据是**真实请求往返**，不是进程存在或端口在听：

```bash
curl -sS -m 5  http://127.0.0.1:<api>/healthz
curl -sS -m 8  http://127.0.0.1:<web>/api/version                    # 经前端 dev server 代理
curl -sS -m 10 -X POST http://127.0.0.1:<web>/api/v1/auth/login \
  -H 'Content-Type: application/json' -d @/tmp/login.json             # 登录往返
```

三条都要 200。只看到进程在跑就宣布成功，会在「代理没配 / 路由没注册 / token 失效」上翻车。

## 1. 工具链装到用户目录

先探能力再下结论：`sudo -n true`（能否免密）、`which go node npm psql docker`、`apt-cache policy <包>`。装不了系统包就全部用户态。

- Go：`curl -sSL -o /tmp/go.tgz https://mirrors.aliyun.com/golang/go1.26.0.linux-amd64.tar.gz && mkdir -p ~/sdk && tar -C ~/sdk -xzf /tmp/go.tgz`，然后 `export PATH=$HOME/sdk/go/bin:$PATH`。
- 模块代理：`export GOPROXY=https://goproxy.cn,direct GOSUMDB=off`。
- lint：`go install github.com/golangci/golangci-lint/v2/cmd/golangci-lint@<版本>`，落在 `~/go/bin`。
- 前端：`npm ci`（先确认 `package-lock.json` 在）。

每个工具装完立刻用 `go version` / `node -v` 回读，不要凭安装命令的退出码判断。

## 2. 长期服务一律 systemd --user

`setsid nohup <cmd> & disown` 起的进程会被执行会话**静默回收**：日志里连 shutdown 记录都没有，尾部干净地停住。数据库、API、前端 dev server 都走单元：

`~/.config/systemd/user/<name>.service`

```
[Service]
Type=simple
ExecStart=<绝对路径，或 /bin/bash <启动器脚本>>
WorkingDirectory=<绝对路径>
Restart=on-failure
RestartSec=3
StandardOutput=append:/tmp/<name>.log
StandardError=append:/tmp/<name>.log
```

`systemctl --user daemon-reload && systemctl --user enable --now <name>`。

判断「崩了还是被回收」：先 `ps` 看进程是否 gone，再看应用日志有没有异常；日志无异常却没了＝被回收，换 systemd 而不是加日志。

## 3. 应用需要数据库时：便携二进制，不装系统包

```bash
mkdir -p ~/pgsql/dl && cd ~/pgsql/dl
curl -sSL -o pg.jar https://repo1.maven.org/maven2/io/zonky/test/postgres/embedded-postgres-binaries-linux-amd64/16.2.0/embedded-postgres-binaries-linux-amd64-16.2.0.jar
unzip -o -q pg.jar postgres-linux-x86_64.txz
mkdir -p ~/pgsql/pg16 && tar -xJf postgres-linux-x86_64.txz -C ~/pgsql/pg16
ldd ~/pgsql/pg16/bin/postgres | grep 'not found'          # 必须为空
~/pgsql/pg16/bin/initdb -D ~/pgsql/pgdata -U <user> --auth-local=trust --auth-host=trust -E UTF8 --locale=C
```

systemd 起：`postgres -D ~/pgsql/pgdata -p 5433 -k /tmp -c listen_addresses=127.0.0.1`。
连接串 `postgres://<user>@127.0.0.1:5433/postgres?sslmode=disable`（便携包只带 initdb/pg_ctl/postgres，没有 psql，默认库用 `postgres`）。

TCP 自检不要等对端先发数据：PG 等客户端先发 startup 包，`recv()` 会假超时；连上不报 ConnectionRefused 即成功。

## 4. 多行密钥不能进 EnvironmentFile

PEM 这类多行值写进 systemd `EnvironmentFile` 会被逐行拆坏。写启动器脚本，读文件再 exec：

```bash
set -uo pipefail
set -a; . ~/.<app>/dev.env; set +a            # 单行变量：连接串、开关、白名单
export JWT_PRIVATE_KEY="$(cat ~/.<app>/jwt/private.pem)"
export JWT_PUBLIC_KEY="$(cat ~/.<app>/jwt/public.pem)"
exec <绝对路径二进制> <参数>
```

单元里 `ExecStart=/bin/bash <启动器脚本>`。密钥与连接串只落本机目录，不进仓库。

## 5. 复用既有数据，先修陈旧绝对路径

把服务的数据目录指向既有目录，不要新建。元数据文件常残留旧机器的绝对路径（如 `/root/...`），会让界面读不到历史数据：先 `cp -a` 备份，再按前缀批量替换，然后用列表接口核对条数、挑一条取详情确认能读出内容。

## 6. 起停脚本

`scripts/dev.sh` 提供 `bootstrap|up|down|down-all|status|logs`，全部走 `systemctl --user`；`status` 打印单元状态 + 端口 + healthz + 预览地址。`bootstrap` 幂等：工具链、编译、前端依赖、密钥、配置、单元逐项检查，已存在的跳过。

## 7. 「界面能开但登不进」

按顺序分诊，别先改前端：

1. **路由是否存在**：空 body 打登录接口。404＝路由整组没注册；400/401＝已注册。
2. **路由整组不注册**：常见触发是缺少启动前提（数据库连接、签名密钥对）。这类前提缺失时代码往往直接跳过注册，而不是返回 503 —— 看到 404 要查启动配置，不要查路由表。
3. **老路径鉴权口径**：`/api/*` 可能认 cookie 而非 Bearer token。登录时用 cookie jar 接住 `Set-Cookie`（如 `lh_refresh`），再用同一会话调用；只带 `Authorization: Bearer <access_token>` 会 401。
4. **图形验证码**：连续失败若干次后强制验证码，计数通常在进程内存里，重启服务即清零。
5. **账号本身**：新建账号的密码是写入者定的，跟用户心里那个密码不是一回事；要改就用 bcrypt 直接更新库里哈希（临时脚本，跑完删掉），不要走需要收信的邮件重置。

## 交付

可复现的起停脚本 + 一段验收命令 + 数据目录与密钥位置说明（写进仓库文档，不写进技能）。
