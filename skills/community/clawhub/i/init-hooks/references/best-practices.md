# init-hooks 钩子编写最佳实践

## ⚠️ 最重要的规则：禁止硬编码绝对路径

钩子内容会在任意用户的机器上执行，`/home/node/` 只属于特定容器。

```bash
# ❌ 错误
python3 /home/node/.openclaw/workspace/skills/foo/run.py

# ✅ 正确
python3 "$HOME/.openclaw/workspace/skills/foo/run.py"
```

---

## 三种类型完整示例

### type: inline（内嵌 shell 命令）

适合：几行不值得单独写脚本文件的简单命令。

**示例1：写启动时间戳（验证钩子是否执行）**
```
--name "启动验证"
--type inline
--content 'echo "[boot] $(date)" >> "$HOME/.openclaw/workspace/.init-hooks/boot.log"'
```

**示例2：创建目录结构**
```
--name "初始化目录"
--type inline
--content 'mkdir -p "$HOME/logs" "$HOME/tmp" "$HOME/.config/myapp"'
```

**示例3：设置环境变量持久化（写独立 env 文件，不碰 shell rc）**
```
--name "写入应用环境变量"
--type inline
--content 'mkdir -p "$HOME/.myapp" && printf "MY_APP_HOME=%s\n" "$HOME/.myapp" > "$HOME/.myapp/env"'
```

> 不要把 export 追加进 `~/.bashrc` / `~/.zshrc`：既容易和用户自己的 shell 配置打架，也常被安全扫描当成"持久化后门"。需要让后续钩子用到这个变量时，直接 `source "$HOME/.myapp/env"`。

> 多行命令用 `$'\n'` 分隔，或者改用 script/python 类型。

---

### type: script（本地 shell 脚本）

适合：步骤较多、需要复用的 shell 逻辑。

**示例：启动时恢复凭证/账号**
```
--name "凭证/账号启动恢复"
--type script
--path "~/.openclaw/workspace/scripts/restore-credentials.sh"
```

> `--path` 支持 `~` 展开（推荐），也支持 `$HOME/...` 写法。

脚本文件本身注意事项：
```bash
#!/usr/bin/env bash
set +e  # 钩子执行环境已经是宽松模式，脚本内部也建议 set +e

# ✅ 用 $HOME 而不是 /home/node
CONF="$HOME/.openclaw/openclaw.json"

echo "[restore] 开始恢复..."
# ... 你的逻辑
echo "[restore] 完成"
```

---

### type: python（本地 Python 脚本）

适合：需要读写 JSON 配置、调用 API、逻辑复杂的初始化。

**示例：改配置后把 runtime 复制到持久化路径**
```
--name "调整配置"
--type python
--path "~/.openclaw/workspace/scripts/apply-config.py"
```

> `--path` 支持 `~` 展开（推荐），也支持 `$HOME/...` 写法。

脚本文件示例 `apply-config.py`。两个关键点：patch 内容由调用方传入，脚本里不写死任何键值；同步是**整份复制 runtime**，不是逐个文件打补丁——后者会让目标文件里的旧值残留，pod 重建后又把旧配置带回来。
```python
#!/usr/bin/env python3
import json, os
from pathlib import Path

HOME = Path.home()
RUNTIME = HOME / ".openclaw/openclaw.json"
# 额外持久化目标由环境变量 INIT_HOOKS_SYNC_PATHS 配置（冒号分隔）；
# 本地留空即可，容器/K8s 按自己的挂载布局填。
COPIES = [
    Path(p).expanduser()
    for p in os.environ.get("INIT_HOOKS_SYNC_PATHS", "").split(os.pathsep)
    if p.strip()
]
# 本次要改的内容由调用方给出（空 = 不改），脚本不预设任何键值
PATCH = json.loads(os.environ.get("CONFIG_PATCH_JSON", "{}"))

def merge(base, extra):
    for k, v in extra.items():
        if isinstance(base.get(k), dict) and isinstance(v, dict):
            merge(base[k], v)
        else:
            base[k] = v
    return base

if PATCH:
    cfg = json.loads(RUNTIME.read_text())
    RUNTIME.write_text(json.dumps(merge(cfg, PATCH), indent=2, ensure_ascii=False))
    print(f"✅ {RUNTIME}")

# 把 runtime 原样复制到每个已存在的目标，保证各处与 runtime 完全一致
data = RUNTIME.read_text()
for p in COPIES:
    if not p.exists():
        print(f"⏭  跳过（不存在）: {p}")
        continue
    p.write_text(data)
    print(f"✅ {p}")
```

---

### type: script/python + URL（CDN 远程包）

适合：脚本托管在 CDN，pod 重建后自动拉取最新版。

**示例：从 CDN 下载 zip 包执行**
```
--name "远程初始化脚本"
--type script
--url "https://cdn.example.com/my-init-v1.0.zip"
--entry "run.sh"
```

注意：
- 压缩包内入口文件用 `--entry` 指定；不指定则自动取第一个 `.sh`/`.py`
- 下载缓存在 `workspace/.init-hooks/downloads/hook_<id>/`
- **首次执行（启动或 `run` 命令）时自动下载**；后续重启如缓存存在直接使用，pod 重建后缓存丢失会自动重新下载
- URL 直接指向单个脚本文件（非压缩包）也支持，无需 `--entry`

---

## 修改 openclaw.json 的钩子：必须同步持久化路径

任何钩子如果修改了 `openclaw.json`，**必须调用 sync 工具**，否则容器重建后配置会被覆盖：

```bash
# inline 钩子末尾加一行 sync
--content 'python3 "$HOME/.openclaw/workspace/skills/init-hooks/scripts/sync_openclaw_config.py"'

# 或者让 sync 帮你执行脚本再同步
python3 sync_openclaw_config.py --run "$HOME/scripts/my-config-patch.py"
```

---

## 执行顺序建议

| order | 建议内容 |
|-------|---------|
| 10    | 启动验证（写 boot.log） |
| 20-50 | 账号/凭证恢复 |
| 60-80 | 配置修复（openclaw.json、agent workspace） |
| 90+   | 功能性初始化（目录结构、环境变量等） |

order 越小越先执行，同 order 按 id 排序。
