# 备份恢复 HERMES_HOME / 跨机迁移

## 备份命令(hermes 内置)

`hermes backup` 把整个 HERMES_HOME 打 zip,默认存到 `~/hermes-backup-<时间戳>.zip`:

```bash
hermes backup                                  # 默认目录
hermes backup --output /path/to/backup.zip     # 指定路径
hermes backup --exclude sessions               # 排除大目录
```

zip 内容:`config.yaml`、`.env`、`auth.json`、`memories/`、`skills/`、`sessions/`、`profiles/`、`SOUL.md`、`USER.md` 等所有用户数据。**不含**:`venv`、`hermes-agent` 本体源码、`bin` symlink、`models_dev_cache.json`(可重建)。

## 手工备份(更可控)

```bash
HOME_DIR="$(hermes dump --redact 2>&1 | awk -F': ' '/HERMES_HOME/{print $2; exit}')"
TS=$(date +%Y%m%d-%H%M%S)

# 全量
tar czf ~/hermes-backup-$TS.tar.gz -C "$(dirname "$HOME_DIR")" "$(basename "$HOME_DIR")"

# 只备 config(快)
tar czf ~/hermes-config-$TS.tar.gz -C "$HOME_DIR" .env config.yaml auth.json
```

Windows Git Bash 可用相同命令,zip 也行:`(cd "$HOME_DIR" && zip -r ~/hermes-config-$TS.zip .env config.yaml auth.json)`。

## 跨机迁移流程

### 旧机
```bash
hermes backup                                  # 一键
# 或手工 tar(上面)
# scp 到新机:
scp ~/hermes-backup-*.zip newhost:~/
```

### 新机
1. **先装 hermes-agent**(对应版本,**先跑一次 `hermes setup` 让它创建默认 HOME**)
2. **关掉所有 hermes 进程**:`taskkill /F /IM hermes.exe`(Win)或 `pkill -f hermes`(Mac/Linux)
3. **解压备份覆盖到 HERMES_HOME**:
   ```bash
   NEW_HOME="$(hermes dump --redact 2>&1 | awk -F': ' '/HERMES_HOME/{print $2; exit}')"
   unzip -o ~/hermes-backup-*.zip -d "$NEW_HOME/.."
   ```
4. **跑 `hermes doctor` 验证**,处理报错
5. **跑 `hermes setup` 但只走 provider 验证一步** — 验证 API key 在新机网络能通(代理设置可能不同)
6. **发 ping 验证**

### 迁移后必查

| 检查项 | 怎么查 |
|---|---|
| HERMES_HOME 是否符合预期 | `hermes dump` |
| API key 是否能用 | `hermes doctor` 或 ping |
| 代理设置(新机) | `echo "$HTTPS_PROXY"` + `reg query HKCU\Environment` |
| sessions/ 历史是否完整 | `ls $NEW_HOME/sessions \| wc -l` |
| skills/ 是否齐全 | `hermes` 内 `/skills list` |
| memories 是否加载 | 启动 hermes 看 banner 上的 memory 计数 |
| 时区 / 系统时间 | OAuth 类 provider 时间偏差 > 5min 会失效 |

## 备份的反模式

- ❌ 直接 `cp -r` 而不停 hermes 进程 → SQLite WAL 可能损坏
- ❌ 备份时把 venv 也打包 → 体积爆炸 + 跨平台不兼容
- ❌ 用 OneDrive / iCloud 同步 HERMES_HOME → 文件锁冲突 + WAL 损坏
- ❌ 把 `auth.json` 上传到 git → 凭证泄漏

## 紧急恢复(配置坏到打不开)

如果 hermes 启动时 panic,大概率 config.yaml 或 auth.json 损坏:

```bash
HOME_DIR="$(reg query 'HKCU\Environment' /v HERMES_HOME 2>/dev/null | awk '/HERMES_HOME/{print $NF}')"
[ -z "$HOME_DIR" ] && HOME_DIR="$HOME/.hermes"

# 1. 备份当前损坏文件
TS=$(date +%Y%m%d-%H%M%S)
mv "$HOME_DIR/config.yaml" "$HOME_DIR/config.yaml.crashed-$TS"
mv "$HOME_DIR/auth.json" "$HOME_DIR/auth.json.crashed-$TS"

# 2. 恢复最近一次自动备份
cp "$HOME_DIR/config.yaml.bak" "$HOME_DIR/config.yaml" 2>/dev/null || true

# 3. 重新跑 setup 让 hermes 重建 auth.json
hermes setup
```

如果 `.bak` 也没了,直接 `hermes setup` 全新生成。memories/ skills/ sessions/ 这些数据目录不动,setup 不影响它们。
