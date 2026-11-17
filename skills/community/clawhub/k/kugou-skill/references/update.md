# 更新命令 (update)

> 自动检查并更新 kugou-cli

## 命令

| 命令 | 说明 |
|------|------|
| `kugou-cli update --check` | 仅检查更新，不执行 |
| `kugou-cli update` | 检查并提示（不自动执行） |
| `kugou-cli update --force` | 直接执行更新（仅 npm 安装） |

---

## 启动时自动检查

### 1. 检查行为

每次执行任意 `kugou-cli` 命令时，**后台异步**检查 npm registry 上的最新版本。

- **不阻塞** 主命令
- 有更新时输出到 **stderr**（避免污染 stdout JSON 输出）
- 提示格式：
  ```
  [kugou-cli] update available: 0.0.22 → 0.0.23 (run `kugou-cli update` to upgrade)
  ```

### 2. 检查频率限制

- 缓存有效期：**24 小时**
- 24 小时内不会重复访问 npm registry

### 3. 跳过检查

在以下情况跳过启动检查：
- `CI=true` 环境变量
- `KUGOU_CLI_NO_UPDATE_CHECK=1` 环境变量
- 命令行指定 `--no-update-check` flag

---

## 显式检查更新

```bash
kugou-cli update --check
```

> **绕过 24h 缓存**：显式调用 `kugou-cli update [--check]` **总是**绕过本地 24h 缓存，强制访问 npm registry。这与"启动时被动检查"的语义不同——启动检查走缓存（24h 内不重复访问 npm），显式 `update` 命令不走缓存。

**输出示例**：

有更新时：
```json
{
  "current_version": "0.0.22",
  "latest_version": "0.0.23",
  "update_available": true,
  "install_method": "npm",
  "update_command": "npm install -g @kg-ai/kugou-skill@latest"
}
```

无更新时：
```json
{
  "current_version": "0.0.22",
  "latest_version": "0.0.22",
  "update_available": false,
  "install_method": "npm"
}
```

---

## 执行更新

### 方式 1：Agent / 脚本（推荐）

```bash
# 步骤 1: 检查
info=$(kugou-cli update --check)
update_available=$(echo "$info" | jq -r '.update_available')

# 步骤 2: 如果有更新，提示用户确认后执行
if [ "$update_available" = "true" ]; then
  echo "有可用更新，正在升级..."
  kugou-cli update --force
fi
```

### 方式 2：手动

```bash
# 提示但不执行
kugou-cli update
# 显示: About to run: npm install -g @kg-ai/kugou-skill@latest

# 强制执行
kugou-cli update --force
```

### 方式 3：标准 npm 命令

无需 `update` 子命令，直接：
```bash
npm install -g @kg-ai/kugou-skill@latest
```

---

## 安装方式检测

CLI 自动检测安装方式：

| 安装方式 | 检测方法 | 是否支持自动更新 |
|---------|---------|------------------|
| **npm** | 二进制路径包含 `node_modules/@kg-ai/kugou-skill` | ✅ 支持 |
| **其他**（源码编译 / 手动下载） | 其他路径 | ❌ 仅提示 |

非 npm 安装时，CLI 只会提示，不会自动更新。请使用对应方式更新。

---

## 注意事项

1. **网络要求**：检查更新需要访问 `https://registry.npmjs.org`，在受限网络下可能失败
2. **离线友好**：网络失败时静默忽略，不影响主命令
3. **CI 友好**：CI 环境默认跳过检查，避免污染日志
4. **不强制**：默认仅提示，更新需用户/Agent 显式确认
