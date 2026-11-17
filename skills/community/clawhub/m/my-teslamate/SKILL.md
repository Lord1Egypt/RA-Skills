---
name: teslamate-deploy
description: This skill should be used when the user wants to install or deploy TeslaMate (a self-hosted Tesla vehicle data logger + Grafana dashboard) on a local machine or a remote Linux server. Triggers include requests like "install TeslaMate", "deploy TeslaMate", "装 teslamate", "部署 teslamate", "在云服务器上跑个 teslamate", or "set up a Tesla data logger". The skill handles target selection, pre-flight checks, running the bundled deploy scripts, post-install health checks, and producing a user-facing usage document.
agent_created: true
---

# TeslaMate Deploy

Deploy TeslaMate (Tesla vehicle data logger + Grafana dashboards) onto either the local machine or a remote Linux server, end-to-end. Wraps the bundled shell scripts with pre-flight checks, post-install verification, and a generated usage document.

## When to use this skill

Trigger this skill when the user asks to:

- "Install TeslaMate" / "装个 TeslaMate" / "帮我跑个 teslamate"
- "Deploy TeslaMate to a server" / "把 teslamate 部署到 X.X.X.X"
- "Set up a Tesla data logger"
- "在云服务器上装个 teslamate" / "在我的 VPS 上跑 teslamate"

Do **not** use this skill for:

- Configuring an already-running TeslaMate (use TeslaMate's own web UI; the skill is for *install* only)
- Upgrading TeslaMate (out of scope of the bundled scripts)
- Setting up a non-Ubuntu/Debian target (the bundled scripts use `apt-get`)
- Provisioning a new VM (the scripts only install Docker + TeslaMate; they do **not** create a VM — the user must already have a Linux host)

## Bundled resources

| File | Purpose |
|---|---|
| `scripts/deploy-setup.sh` | Entry script. With no arg → local install. With one IP arg → SSH to that server and install. |
| `scripts/install-teslamate.sh` | Local install logic. Auto-detects / installs Docker, writes `.env`, pulls images, starts stack. |
| `scripts/docker-compose.yml` | Stack definition: `teslamate` (port 4000) + `postgres:17` + `grafana` (port 3000) + `mosquitto` (port 1883). |
| `scripts/README.md` | Author's original Chinese README (reference only; ignore its `postgres:16` mention — `docker-compose.yml` is the source of truth and uses `postgres:17`). |
| `references/troubleshooting.md` | Common failures and their fixes. Load this when an install step fails. |

## Workflow

Follow these steps in order. Use `AskUserQuestion` for the inputs, then run the script via the Bash tool.

### Step 1 — Confirm target

Ask the user **one** question:

> "装在本地还是远程服务器？"
> - 本地（直接在这台机器上跑）
> - 远程服务器（用 SSH 推到另一台 Ubuntu / Debian）

If remote, ask the follow-up:

> "服务器 IP 是？SSH 端口默认 22，用户名默认 `ubuntu`，对吗？"
> - Yes, use defaults
> - Different SSH port / different user

Collect: `target` ∈ {`local`, `remote`}; if remote, also `server_ip`, `ssh_user` (default `ubuntu`), `ssh_port` (default 22).

### Step 2 — Pre-flight checks

Before running the install, verify:

1. **OS family** (remote only): `ssh $ssh_user@$server_ip "cat /etc/os-release | grep ^ID="`. Must be `ubuntu` or `debian`. If not, stop and tell the user the script only supports Debian-family distros.
2. **SSH reachability** (remote only): `ssh -o BatchMode=yes -o ConnectTimeout=5 $ssh_user@$server_ip echo ok`. If it fails, stop and ask the user to confirm SSH key / password is set up.
3. **Port availability**:
   - Local: `lsof -i :3000 -i :4000 -i :1883` (or warn if non-zero exit)
   - Remote: `ssh $ssh_user@$server_ip "ss -ltn | grep -E ':(3000|4000|1883) '"`
   - If any port is occupied, stop and ask the user to either free it or accept a different port (out of skill scope — flag it).
4. **Skill scripts present**: confirm `~/.workbuddy/skills/teslamate-deploy/scripts/{deploy-setup.sh,install-teslamate.sh,docker-compose.yml}` exist. If not, the skill install is broken — stop and tell the user to re-install the skill.

### Step 3 — Run the deploy

```bash
SKILL_DIR="$HOME/.workbuddy/skills/teslamate-deploy"
# 临时拷贝到 ~/teslamate-deploy 一起执行 (install 脚本需要 docker-compose.yml 在同目录)
WORK=/tmp/teslamate-deploy-$USER
rm -rf "$WORK" && mkdir -p "$WORK"
cp "$SKILL_DIR/scripts/"{deploy-setup.sh,install-teslamate.sh,docker-compose.yml} "$WORK/"
chmod +x "$WORK/deploy-setup.sh" "$WORK/install-teslamate.sh"
cd "$WORK"
./deploy-setup.sh $server_ip   # 远端: 加 IP; 本地: 不加
```

Why copy to `/tmp`: `install-teslamate.sh` looks for `docker-compose.yml` in the current dir, and writes `.env` / `import/` there. Keeping it out of the skill dir prevents polluting the skill itself.

Stream the script's output to the user (it's verbose and helpful). Expect a 3–10 minute run: Docker install + 4 image pulls + stack up.

### Step 4 — Post-install health check

After the script exits 0, verify:

```bash
# For local:
curl -fsS -o /dev/null -w "Grafana: HTTP %{http_code}\n" http://localhost:3000/api/health
curl -fsS -o /dev/null -w "TeslaMate: HTTP %{http_code}\n" http://localhost:4000
docker compose ps --format 'table {{.Name}}\t{{.Status}}\t{{.Ports}}'

# For remote: same but with ssh + curl-over-ssh, e.g.
ssh $ssh_user@$server_ip "curl -fsS -o /dev/null -w 'Grafana: %{http_code}\n' http://localhost:3000/api/health"
ssh $ssh_user@$server_ip "cd /home/$ssh_user/teslamate && sudo docker compose ps"
```

Pass criteria: Grafana returns 200, TeslaMate returns 200 (or 30x redirect), all 4 containers `Up`. If TeslaMate returns 503 / connection refused within 1–2 minutes, that's normal — the database is still initializing. Re-check after 90 seconds.

### Step 5 — Generate usage document

Create a markdown file at the workspace's outputs directory (or `~/.workbuddy/outputs/teslamate-usage-$TIMESTAMP.md` if outside a workspace). Use this template:

```markdown
# TeslaMate 部署完成 🚗

## 访问地址

| 服务 | URL | 端口 | 默认账号 |
|---|---|---|---|
| TeslaMate | http://$HOST:4000 | 4000 | (登录前需要先在 TeslaMate UI 配 Tesla 账号) |
| Grafana | http://$HOST:3000 | 3000 | `admin` / `admin` |
| MQTT (mosquitto) | `$HOST:1883` | 1883 | (无认证，**仅限内网使用**) |

> 远程部署时把 `localhost` 换成服务器 IP；首次访问 Grafana 会被强制改 admin 密码。

## 第一步：配置 Tesla 账号

1. 打开 http://$HOST:4000
2. 用浏览器登录 https://auth.tesla.com 拿到一个 **Tesla refresh token**
3. 在 TeslaMate UI 里粘贴 token，配上你的车辆 —— 具体步骤见 https://docs.teslamate.org/docs/guides/initial_setup

## 常用运维命令

```bash
# 看所有容器状态
sudo docker compose ps

# 看 TeslaMate 实时日志
sudo docker compose logs -f teslamate

# 改默认密码 / 加密密钥
cd ~/teslamate    # 远程是 /home/$ssh_user/teslamate
sudo nano .env     # 改完重启: sudo docker compose up -d
```

## 注意事项

- 默认密码 `teslamate123` 和 Grafana `admin/admin` **请尽快改掉**
- 端口 3000 / 4000 / 1883 直接暴露在公网不安全；建议至少开防火墙只放行你信任的 IP，或者套个 Nginx + Let's Encrypt
- 数据库默认没做备份 —— 参考 https://docs.teslamate.org/docs/guides/backup
```

Tell the user the file path and offer to open it. Also tell them the access URLs directly in chat.

## Critical rules

- **Never run `deploy-setup.sh` against `localhost` or `127.0.0.1` as a "remote" target** — that would loop back and double-install. If the user wants local, run without args.
- **Never edit the bundled scripts in place.** The skill owns them; per-session copies go in `/tmp/teslamate-deploy-$USER/`.
- **Never `git push` to the original GitHub repo from inside the skill.** The skill is for deploying, not for modifying the source.
- **If the script fails mid-way, do not retry blindly.** Read the error, check `references/troubleshooting.md`, and surface the relevant fix to the user.
- **The bundled default `TM_ENCRYPTION_KEY` and `TM_DB_PASS` are intentionally weak** (they're demo values from the original author). The generated usage document must warn the user to change them.

## What this skill does NOT do

- Provision a VM (Vagrant / cloud-init / UTM)
- Backup / restore existing TeslaMate data
- Upgrade an existing install
- Configure HTTPS / reverse proxy
- Multi-node / HA setups
- Non-Debian-family OSes

If the user asks for any of these, tell them the skill's scope ends at "install + verify + document" and point them to the appropriate next step (e.g. "use `vagrant up` to provision first, then come back to this skill").
