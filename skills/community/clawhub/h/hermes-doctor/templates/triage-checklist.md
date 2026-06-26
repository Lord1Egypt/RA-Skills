# Hermes 故障 Triage Checklist

按顺序执行,**不要跳步**。每一步如果发现问题就跳到对应 reference 文件。

## ⚙️ 准备

```bash
# 0. 锁定真 HERMES_HOME(Windows 上常被 HKCU 重定向到非默认路径)
HOME_DIR="$(reg query 'HKCU\Environment' /v HERMES_HOME 2>/dev/null | awk '/HERMES_HOME/{print $NF}')"
[ -z "$HOME_DIR" ] && HOME_DIR="$HOME/.hermes"
echo "HERMES_HOME = $HOME_DIR"
ls "$HOME_DIR"
```

确保 `$HOME_DIR` 真实存在。如果不存在,看 references/config-and-paths.md。

## 🔍 5 步排查

### 1. 看 hermes 自己的诊断

```bash
hermes doctor
hermes dump --redact 2>&1 | head -60
```

- 任何红色 `[fail]` → 跳 references/doctor-and-dump.md
- `hermes dump` 找:
  - active provider 是哪个,base_url 是不是预期
  - credential_pool 里有没有目标 provider 条目
  - last_status 是不是 401/403/429

### 2. 看实际请求(关键)

```bash
ls -t "$HOME_DIR/sessions/request_dump_"*.json 2>/dev/null | head -3
```

打开最新一条:
- `request.url` — 是不是预期的 endpoint
- `request.headers.Authorization` — 是真 key 头部还是 `Bearer no-key-required` / `Bearer expired` 字面占位符

如果 Authorization 是占位符 → **类型 1 占位符注入**,跳 references/auth-troubleshooting.md。

### 3. 排查 4 处残留(从隐蔽到显眼)

```bash
# (a) HKCU\Environment(Windows 最隐蔽)
reg query "HKCU\Environment" 2>&1 | grep -iE "API_KEY|HERMES_HOME"

# (b) 当前 shell 进程
env | grep -iE "API_KEY|HERMES" | head -10

# (c) auth.json 凭证池
cat "$HOME_DIR/auth.json" | python -c "import sys,json; d=json.load(sys.stdin); print(list(d['credential_pool'].keys()))"

# (d) .env + config.yaml
grep -E "^[A-Z_]+_API_KEY=" "$HOME_DIR/.env"
grep -E "api_key|provider|base_url" "$HOME_DIR/config.yaml" | head -20
```

判定:
- (a) 有意外的 API_KEY → 用 `reg delete "HKCU\Environment" /v <NAME> /f` 清掉
- (a) HERMES_HOME 与你预期不一致 → 改/删 HKCU 那条
- (c) 缺目标 provider → 跳 references/auth-troubleshooting.md 类型 1 修复
- (d) `.env` 有目标 KEY 但 setup 不弹输入 → issue #16394,删该行重跑 setup

### 4. 备份(永远在改之前)

```bash
TS=$(date +%Y%m%d-%H%M%S)
for F in .env config.yaml auth.json; do
  [ -f "$HOME_DIR/$F" ] && cp "$HOME_DIR/$F" "$HOME_DIR/$F.broken-$TS"
done
ls "$HOME_DIR"/*.broken-$TS
```

### 5. 修复 + 验证

修复手段二选一(或并用):

**A. 手工修 auth.json + .env**(精准、快):
- `auth.json` 加目标 provider 的 credential_pool 条目(参 auth-troubleshooting.md)
- `.env` 加 `<PROVIDER>_API_KEY=<key>` 兜底
- **重启 hermes** — auth 是启动时加载的

**B. 走 wizard**(慢、但能改 model_profiles):
- `hermes setup` — 如果 setup 不弹 key 输入,先删 .env 里那条
- 跟着流程填新 key

验证(必跑):
```bash
hermes doctor                           # 全绿
# 重启 hermes,发 ping
```

ping 拿到响应 → 修复完成。

ping 还是 401 → 看新 request_dump,判定:
- Authorization 还是占位符 → 你改的可能是错文件(HERMES_HOME 不对)
- Authorization 是真 key 但 server 拒 → key 真过期,去服务商续

## 🚨 升级到人工

下面任一情况停手 + 找人:
- 4 处残留点都查过没线索,`hermes dump` 显示的运行时 key 与 4 处都对不上 → venv 损坏
- `auth.json` JSON 解析失败 → 备份文件也坏的话,只能 setup 重建
- `state.db` / `response_store.db` 损坏 → 备份 sessions/ 后删 db 文件让 hermes 重建
- 跨机迁移后系统时区差 > 5min,OAuth provider(copilot/gemini)全失效 → 校时再说

## 📝 修完后写 memory(可选,推荐)

如果这次修的是非典型故障(不在已知 issue 列表),把根因和处理写进 `~/.claude/projects/.../memory/` 一条,下次秒诊。
