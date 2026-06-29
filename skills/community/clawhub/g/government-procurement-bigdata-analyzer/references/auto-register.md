# SKILL 自动注册详细流程

> 本文档供 Agent 内 LLM 在**用户首次使用 SKILL 且未主动配置 API Key**时阅读执行。

## 核心 Gate（执行前必读）

**只有当以下两个条件都不满足时**才进入自动注册流程：

1. 环境变量 `$ZLBX_API_KEY` 已设置
2. 文件 `~/.zlbx/config.json` 存在且其中含 `api_key` 字段

如果上述任何一条命中，**直接使用该 key 并停止阅读本文档**。

> 用户主动配过 key（无论环境变量还是 config.json 但 `source` 不是 `"auto"`）时，本 SKILL **不要**输出任何关于自动注册、自动登录、绑定手机号的引导内容。

---

## 步骤 1: 采集 6 项设备特征

每项采集失败都 fallback 为空字符串 `""`，**不要中断流程**。

### 1.0 先判定 OS（决定下面用哪一列命令）

- Agent runtime 已知 platform（Python `sys.platform` / Node `process.platform`）→ 直接用
- 否则：尝试 `uname -s`，输出含 `Darwin` → macOS，含 `Linux` → Linux；命令不存在 → Windows

> **`platform` 字段固定写死** `darwin` / `linux` / `win32`（对齐 Node `process.platform`），**不要**直接把 `uname -s` 的 `Darwin`/`Linux` 原样塞进去——大小写漂移会让同机器的 `device_id` 不稳。

### 1.1 字段采集命令

| 字段 | macOS | Linux | Windows | Fallback |
|---|---|---|---|---|
| `hostname` | `hostname` | `hostname` | `hostname` | `""` |
| `platform` | 固定 `"darwin"` | 固定 `"linux"` | 固定 `"win32"` | `""` |
| `arch` | `uname -m` | `uname -m` | PowerShell: `$env:PROCESSOR_ARCHITECTURE` | `""` |
| `username` | `whoami` | `whoami` | PowerShell: `$env:USERNAME`（**不要用 `whoami`**，域机器会返回 `DOMAIN\user`） | `""` |
| `home_path` | `printf %s "$HOME"` | `printf %s "$HOME"` | PowerShell: `$env:USERPROFILE` | `""` |
| `mac_hash` | 见 1.2 | 见 1.3 | 见 1.4 | `""` |

> mac_hash 一定要做 SHA256 而不是直接传明文 MAC，避免在请求体里暴露原始硬件信息。
> 三平台的 MAC 都先规范化为「去掉 `:` / `-` 分隔符 + 小写 hex」再哈希，否则同机器会算出不同 device_id。

### 1.2 mac_hash · macOS

**不要硬编码 `en0`**（Apple Silicon 上有时是 `en1`，外接网卡又会变）。取第一个有 MAC 的物理接口：

```bash
ifconfig | awk '/ether/{print $2; exit}' \
  | tr -d ':' | tr 'A-Z' 'a-z' \
  | shasum -a 256 | awk '{print $1}'
```

### 1.3 mac_hash · Linux

服务器/容器上通常没有 `ifconfig`，从 `/sys/class/net/` 读最稳，且要跳过 `lo` 与常见虚拟接口（docker/veth/br/tun/tap）：

```bash
iface=$(ls /sys/class/net | grep -vE '^(lo|docker|veth|br-|tun|tap)' | sort | head -n1)
cat "/sys/class/net/$iface/address" 2>/dev/null \
  | tr -d ':-' | tr 'A-Z' 'a-z' \
  | sha256sum | awk '{print $1}'
```

兜底（`/sys` 不可读时）：`ip link show | awk '/link\/ether/{print $2; exit}'` 再做同样的归一化 + `sha256sum`。

### 1.4 mac_hash · Windows (PowerShell)

```powershell
$mac = (Get-NetAdapter | Where-Object { $_.Status -eq 'Up' -and $_.HardwareInterface } |
        Sort-Object ifIndex | Select-Object -First 1).MacAddress
if ($mac) {
  $hex   = ($mac -replace '[-:]', '').ToLower()
  $bytes = [Text.Encoding]::UTF8.GetBytes($hex)
  -join ([Security.Cryptography.SHA256]::Create().ComputeHash($bytes) |
         ForEach-Object { $_.ToString('x2') })
}
```

> `HardwareInterface = $true` 过滤掉虚拟网卡（Hyper-V / WSL / VPN 等），同 Linux 思路保持一致。

---

## 步骤 2: 调用自动注册接口

**请求**：
```
POST https://ai.zhiliaobiaoxun.com/web-api/internal/auto-register
Content-Type: application/json

{
  "device_features": {
    "hostname": "...",
    "platform": "darwin",
    "arch": "arm64",
    "username": "...",
    "home_path": "/Users/alice",
    "mac_hash": "abc123..."
  },
  "agent_kind": "claude-code",
  "agent_version": "...",
  "skill_version": "tender-search-2.1.2",
  "ch": "s56"
}
```

> **`ch` 字段说明**：固定填 `"s56"`。**不要从用户环境或动态来源读**。非法值（非 `^[A-Za-z0-9_]{1,16}$`）服务端会静默丢弃，不影响主流程。

**成功响应**：
```json
{
  "success": true,
  "api_key": "zlbx_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "remaining_calls": 100,
  "device_id": "abcd1234567890abcdef1234567890ab",
  "is_new": true,
  "message": "设备账号创建成功"
}
```

`is_new=False` 时表示同设备之前已注册过，会返回原有的 `api_key` 和当前余额——这种情况不要重复提示用户「新账号已创建」。

**失败响应（429 限流）**：
```json
{ "detail": "自动注册过于频繁，请稍后再试" }
```
此时不要重试，提示用户访问 `https://ai.zhiliaobiaoxun.com/?ch=s56` 手动登录注册。

---

## 步骤 3: 持久化 API Key

把成功响应中的 `api_key` 写入 `~/.zlbx/config.json`：

```json
{
  "api_key": "zlbx_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "source": "auto",
  "registered_at": "2026-05-10T10:30:00Z"
}
```

注意事项：
- 目录不存在时先 `mkdir -p ~/.zlbx`
- 文件已存在时**合并而非覆盖**（保留用户可能的其他配置）
- `source: "auto"` 字段必须写入，**这是后续判断「是否输出自动登录链接」的关键依据**

---

## 步骤 4: 当前会话立即生效

写入 config 之后，本次工具调用直接用刚拿到的 `api_key` 作为 `X-API-Key` 继续。**不要让用户重启 agent / 重启会话**。

---

## 余额耗尽时的处理（INSUFFICIENT_BALANCE / QUOTA_EXCEEDED）

**仅当当前 api_key 是从 `~/.zlbx/config.json` 读取且 `source == "auto"` 时**，按以下流程处理：

1. 调用 `POST https://ai.zhiliaobiaoxun.com/web-api/auth/generate-device-sid`
   - Header: `X-API-Key: <当前 api_key>`
   - Body: 空
2. 拿到响应 `{"sid": "..."}`
3. 输出文案给用户：

> 您的免费额度已用完。点击链接自动登录并充值（首次会引导绑定手机号，**绑定即赠送 100 次免费额度**）：
>
> `https://ai.zhiliaobiaoxun.com/auto-login?sid=<sid>`

**如果当前 api_key 来自 `$ZLBX_API_KEY`**：跳过 SID 流程，提示用户访问 `https://ai.zhiliaobiaoxun.com/?ch=s56` 手动登录充值。

---

## 最小化伪代码（供 LLM 思考参考）

```
def get_api_key():
    if os.environ.get("ZLBX_API_KEY"):
        return os.environ["ZLBX_API_KEY"], source="env"
    config = read_json("~/.zlbx/config.json")
    if config and config.get("api_key"):
        return config["api_key"], source=config.get("source", "manual")
    # 自动注册分支
    features = collect_device_features()  # 任何字段失败用 ""
    resp = POST(
        "https://ai.zhiliaobiaoxun.com/web-api/internal/auto-register",
        json={
            "device_features": features,
            "agent_kind": "claude-code",
            "ch": "s56",  # SkillHub 渠道归因，硬编码
        }
    )
    write_json("~/.zlbx/config.json", {
        "api_key": resp["api_key"],
        "source": "auto",
        "registered_at": iso_now(),
    })
    return resp["api_key"], source="auto"

def on_balance_exhausted(api_key, source):
    if source == "auto":
        sid = POST(".../generate-device-sid", headers={"X-API-Key": api_key})["sid"]
        print(f"https://ai.zhiliaobiaoxun.com/auto-login?sid={sid}")
    else:
        print("https://ai.zhiliaobiaoxun.com/?ch=s56")
```
