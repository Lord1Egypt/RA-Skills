# 认证命令 (auth)

> 🔐 = 需要先登录

## 命令列表

| 命令 | 说明 | 需要登录 |
|------|------|---------|
| `kugou-cli auth login` | 获取二维码图片 | 否 |
| `kugou-cli auth status` | 检查登录状态（已完成则登录，未完成则继续轮询） | 否 |
| `kugou-cli auth set-secret <secret>` | 直接导入已持有的 base64 secret 登录（跳过扫码） | 否 |
| `kugou-cli auth logout` | 登出 | 否 |

---

## 1. 扫码登录

登录流程极简：

```bash
# Step 1: 获取二维码图片
kugou-cli auth login

# Step 2: 检查登录状态（Agent 可循环调用直到 logged_in=true）
kugou-cli auth status
```

**auth login 输出示例**:
```json
{"qrcode": "xxx", "qrcode_img_path": "C:\\Users\\xxx\\AppData\\Local\\Temp\\kugou-qrcode.png"}
```

> **重要**：必须将 `qrcode_img_path` 对应的图片文件**发送给用户**供扫码登录。

**auth status 状态输出**:

已登录：
```json
{"logged_in": true, "nickname": "沙墨", "login_time": "2024-01-01 12:00:00"}
```

未登录但有 pending qrcode（等待扫码）：
```json
{"logged_in": false, "status": "waiting", "qrcode": "xxx"}
```

未登录但已扫码（等待确认）：
```json
{"logged_in": false, "status": "scanned", "nickname": "xxx", "qrcode": "xxx"}
```

未登录且 qrcode 失效：
```json
{"logged_in": false, "status": "failed", "message": "QR code expired"}
```

---

## 2. AI 引导流程

1. 调用 `auth login` 获取二维码图片
2. **必须**将 `qrcode_img_path` 对应的二维码图片发送给用户
3. 循环调用 `auth status` 等待用户扫码
4. 当输出 `logged_in: true` 后，登录完成，可继续执行音乐命令

> **简化说明**：本工具将"轮询检查扫码状态"逻辑内置到 `auth status` 中，Agent 只需简单循环调用 status 即可。

### 备选路径：用户已持有 secret

当用户**已经持有**一个有效的 base64 secret 字符串时（例如从其他设备、其他工具导出的），可以直接用 `auth set-secret` 跳过整个扫码流程，**不需**调用 `auth login` / `auth status`：

```bash
kugou-cli auth set-secret "<base64-secret>"
```

调用成功后 secret 会被持久化到 `~/.config/kugou-cli/auth.json`，所有 music 命令立即可用，效果与扫码登录一致。

---

## 3. 直接设置 secret

**适用场景**：
- 用户在其他设备/工具上已登录酷狗，导出或复制了一份 base64 secret
- 测试、调试、自动化场景下需要直接注入 secret
- 任何不便于扫码的终端环境（如 SSH 远端、容器、CI）

**命令**:

```bash
kugou-cli auth set-secret "{secret}"
```

**shell 引号注意事项**：
- secret 字符串含 `+`、`/`、`=` 等 base64 字符是**正常的**，**不会**被 shell 误解析
- 但 `+` 在 bash 中是通配符、`=` 在 cmd.exe 中会触发变量赋值，**务必用引号包起来**
- 推荐使用双引号 `"..."`（除非 secret 中含 `$`，那就用单引号 `'...'`）

**输出示例**:
```json
{"status": "ok", "message": "secret saved"}
```

**失败示例**（secret 为空）:
```
secret cannot be empty
```

**与扫码登录的等价性**：
- secret 落到同一份 `~/.config/kugou-cli/auth.json`
- 后续 `auth status` 输出 `{"logged_in": true}`
- 所有 `music` 子命令立即可用，无需任何额外步骤
- nickname 字段为空（因为导入途径不带昵称），不影响功能

**上游校验时机**：
- CLI 不做本地格式校验（不做 base64 解码、不解密），只做"非空"检查
- secret 实际有效性在**第一次**调用 `music <sub>` 时由上游校验；secret 失效/过期会返回 `errcode: 30001`（密钥错误）

---
