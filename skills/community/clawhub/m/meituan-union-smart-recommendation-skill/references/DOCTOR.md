# 分销会场 Skill 自诊断手册（DOCTOR）

> 当 Skill 出现异常时，请按本手册依次排查。如需提交问题反馈，请附上相关诊断输出。

---

## 一、快速诊断命令

以下命令均需在终端执行，请将 `<SKILL_DIR>` 替换为 Skill 实际安装路径（通常为 `~/.claude/skills/meituan-venue-guide`）。

**诊断认证日志**
```bash
python3 <SKILL_DIR>/scripts/diag_auth_log.py
```

**诊断绑定日志**
```bash
python3 <SKILL_DIR>/scripts/diag_bind_log.py
```

**查看认证状态**
```bash
python3 <SKILL_DIR>/scripts/auth.py status
```

**查看口令绑定状态**
```bash
python3 <SKILL_DIR>/scripts/bind.py status
```

---

## 二、日志文件位置

| 日志类型 | 路径 | 说明 |
|---------|------|------|
| 认证日志 | `{系统临时目录}/fenxiao/fenxiao_auth.log` | 登录、pt-passport 授权、Token 校验相关操作记录 |
| 绑定日志 | `~/.xiaomei-workspace/venue_bind.log` | 口令绑定操作记录 |
| 本地认证数据 | `~/.xiaomei-workspace/auth_tokens.json` | 当前 Token / 设备标识存储文件 |
| 本地绑定数据 | `~/.xiaomei-workspace/venue_bind.json` | 当前口令绑定信息存储文件 |

> **注意**：日志文件经过 XOR 加密，不可直接 `cat` 查看，必须通过诊断脚本解密后阅读。
>
> `{系统临时目录}` 在 macOS / Linux 下通常为 `/tmp`，在 Windows 下为 `%TEMP%`。

---

## 三、常见问题排查

### 3.1 首次使用无法进入：提示需要口令

**症状**：对话开始后 Skill 提示「需要输入媒体口令」。

**原因**：本地未检测到有效口令绑定记录，或口令已过期。

**排查步骤**：
1. 执行 `python3 bind.py status` 查看绑定状态，确认 `valid` 字段是否为 `true`。
2. 若 `reason` 为 `no_bind`，说明从未绑定过，需要从媒体处获取口令并执行绑定。
3. 若 `reason` 为 `expired`，说明口令已到期，需向媒体申请新口令重新绑定。

---

### 3.2 已登录但无法使用服务

**症状**：登录成功，但调用会场链接时失败，或提示「未绑定口令」。

**排查步骤**：
1. 执行 `python3 auth.py status` 确认登录状态，`logged_in` 应为 `true`。
2. 执行 `pt-passport get-token --client_id 578aafab312b44f1b76b0529b06bb0c6` 验证 Token 是否仍然有效（有输出则有效，退出码非 0 则已失效）。
3. 执行 `python3 bind.py status` 确认口令绑定状态。
4. 若 Token 失效，执行登出后重新扫码授权：`python3 auth.py logout`，然后重新执行 pt-passport 扫码登录。

---

### 3.3 口令绑定失败

**症状**：输入口令后提示绑定失败，或 `bind` 命令返回 `success: false`。

**排查步骤**：
1. 确认口令字符串完整、无多余空格，区分大小写。
2. 查看 `bind` 命令返回的 `code` 字段：
   - `-1` / 非 0：口令无效或已失效，需向媒体重新获取。
3. 确认当前 Token 有效（先执行 `auth.py token-verify`），Token 失效会导致绑定失败。
4. 检查网络连通性，绑定接口域名为 `mtunion.web.test.sankuai.com`（测试环境）。

---

### 3.4 会场链接读取为空

**症状**：`bind.py get-links` 返回 `NO_LINKS` 错误。

**原因**：本地绑定数据中 `skillActLinkInfoList` 为空列表，或绑定数据文件被清除。

**排查步骤**：
1. 确认口令绑定是否成功，执行 `python3 bind.py status`。
2. 若口令绑定有效但链接为空，可能是服务端该口令下暂无配置的会场链接，请联系媒体确认。
3. 尝试重新绑定口令：`python3 bind.py bind --token <token> --code-word <口令>`。

---

### 3.5 退出登录后仍能看到历史口令

**症状**：执行了退出登录，但 `bind.py status` 仍显示有效。

**原因**：退出登录时未同步清除口令绑定数据，属于异常状态。

**修复方法**：手动执行以下两条命令：
```bash
python3 auth.py logout
python3 bind.py clear
```

---

### 3.6 设备标识丢失 / 无法通过 Token 校验

**症状**：`auth.py token-verify` 失败，但确认 Token 未过期。

**原因**：设备标识（`device_token`）文件被清除或损坏，与服务端绑定的设备信息不匹配。

**排查步骤**：
1. 执行 `python3 auth.py status` 查看 `device_token` 是否存在。
2. 若不存在，说明设备标识已丢失，此时 Token 将无法通过校验，需重新执行 pt-passport 扫码授权完成登录。
3. 重新登录后，执行 `bind.py bind` 重新绑定口令。

---

## 四、日志解密与查看

日志文件经 XOR 加密存储，请使用诊断脚本查看：

```bash
# 查看认证日志（近 100 条）
python3 <SKILL_DIR>/scripts/diag_auth_log.py

# 查看绑定日志（近 100 条）
python3 <SKILL_DIR>/scripts/diag_bind_log.py

# 仅查看最近 N 条（示例：最近 20 条）
python3 <SKILL_DIR>/scripts/diag_auth_log.py --tail 20
python3 <SKILL_DIR>/scripts/diag_bind_log.py --tail 20
```

---

## 五、完整重置流程

如排查困难，可按以下步骤完整重置 Skill 状态：

```bash
# 1. 退出登录并清除 Token
python3 <SKILL_DIR>/scripts/auth.py logout

# 2. 清除设备标识
python3 <SKILL_DIR>/scripts/auth.py clear-device-token

# 3. 清除口令绑定数据
python3 <SKILL_DIR>/scripts/bind.py clear

# 4. 重新扫码授权登录（pt-passport）
python3 <SKILL_DIR>/scripts/auth.py login

# 5. 重新绑定口令（从媒体处获取）
python3 <SKILL_DIR>/scripts/bind.py bind --token <user_token> --code-word <口令>
```

---

## 六、联系支持

- **美团客服**：美团 APP → 我的 → 客服（工作时间：9:00 - 22:00）
- **口令 / 会场问题**：请联系提供口令的媒体方
- **Skill 版本问题**：检查 Skill 主文件中的 `version` 字段，确认是否为最新版本
