# Mearl 连接故障排查

本技能有两种使用方式，安装与建联方式不同，请先确认你属于哪一种：

- **本地使用**：Agent 与浏览器在同一台机器，直接通过 native host socket 通信（`mearl` 由 `@mearl/client` 提供）。
- **云端使用**：Agent 在云端、浏览器在本地，通过 cloud-server + cloud-connector 中转（`mearl` 由 `@mearl/cloud-client` 提供）。

---

# 本地使用

## 首次使用先检查

先确认工具是否已安装：

```bash
mearl --version
mearl-native-host --version
```

如果命令不存在，请先安装：

```bash
npm install -g @mearl/native-host @mearl/client
```

如果命令存在，重新初始化：

```bash
mearl-native-host --init
```

之后检测环境是否就绪：

```bash
mearl check
```

## EACCES（权限不足）

初始化脚本写入系统目录时权限不足。

处理步骤：
```bash
sudo mearl-native-host --init
```

## ENOENT（找不到 Socket）

native host socket 尚未启动。

**从 v1.29+ 起，client 会在 ENOENT 时自动尝试拉起 `mearl-native-host` 并在 1.2s 后重试，大多数情况下无需手动干预。**

如果重试后仍然失败，可按以下步骤排查：

**使用浏览器插件模式：**
1. 确认 Chrome 浏览器已打开，等待插件自动建联（约 60s 内）。
2. 如仍失败，打开 DevTools 切换到 Mtop 面板手动触发建联。
3. 如果使用本地开发版扩展，需指定扩展 ID：`mearl-native-host --init --extension-id {EXTENSION_ID}`
4. 重新执行命令。

**使用 CDP 模式（无需插件，Chrome 145+）：**
1. 打开 Chrome，访问 `chrome://inspect/#remote-debugging`。
2. 勾选 "Discover network targets"（Chrome 会弹出授权提示，点击允许）。
3. 确认有普通网页已打开（非 chrome:// 页面）。
4. 重新执行命令，native host 会自动读取 DevToolsActivePort 文件连接到浏览器。

## ECONNREFUSED / 连接关闭

native host 可能崩溃或已断开连接。

处理步骤：
1. 插件会自动重连，稍等片刻后重试。
2. 如仍失败，打开 DevTools 切换到 Mtop 面板手动触发重连。
3. 如有需要，重新执行初始化：
   - `mearl-native-host --init`
4. 重新执行命令。

---

# 云端使用

云端使用需要在 **云端（Agent 侧）** 和 **本地（浏览器侧）** 两端分别准备。

## 云端（Agent 侧）

1. 安装 cloud-server 与 cloud-client：

   ```bash
   npm install -g @mearl/cloud-server @mearl/cloud-client
   ```

2. 启动 cloud-server（默认即后台运行），获取输出的连接命令：

   ```bash
   mearl-cloud-server
   ```

   启动后会立即返回，并打印供本地机器使用的连接命令，形如：

   ```
   [CloudServer] Started in background (pid 12345)
   [CloudServer] Logs: ~/.mearl/cloud-server.log

     Connect from your local machine:
       npx @mearl/cloud-connector "wss://xxx/ws?token=xxx"
   ```

   把这条 `npx @mearl/cloud-connector "..."` 命令复制给本地机器执行（见下文）。
   常用管理命令：

   ```bash
   mearl-cloud-server status   # 查看运行状态与连接命令
   mearl-cloud-server logs     # 查看日志
   mearl-cloud-server stop     # 停止
   mearl-cloud-server restart  # 重启
   ```

3. cloud-server 同时会把本地连接配置写入 `~/.mearl/cloud-server.json`，cloud-client 会自动读取，因此 Agent 侧无需额外配置，直接调用即可：

   ```bash
   mearl get_requests --payload '{"count": 5}'
   ```

   如需手动指定 server 地址，可用 `--server <url>` 或设置环境变量 `MEARL_SERVER_URL`。

## 本地（浏览器侧）

1. 执行云端输出的连接命令，把本地浏览器接入云端：

   ```bash
   npx @mearl/cloud-connector "wss://xxx/ws?token=xxx"
   ```

2. 本地浏览器侧仍需满足 [本地使用](#本地使用) 的前置条件（native host 已初始化、浏览器插件或 CDP 已建联），否则 connector 无法连到本地 socket。相关报错（EACCES / ENOENT / ECONNREFUSED）参考上文本地排查步骤。

## 云端常见问题

- **Agent 侧报 "WebSocket server URL is required"**：cloud-server 未启动或未写入配置。用 `mearl-cloud-server status` 确认正在运行，或通过 `--server` / `MEARL_SERVER_URL` 手动指定地址。
- **connector 连不上 / 一直重连**：检查云端输出的 URL 与 token 是否完整复制，确认云端端口（默认 8080）对本地可达。
- **connector 已连上但请求无响应**：本地 native host 或浏览器未就绪，按上文本地排查步骤处理。

---

# 通用问题

## 请求超时

扩展未能在超时时间内返回数据。

处理步骤：
1. 增加超时参数：`--timeout 30`
2. 降低 payload 大小（如 `includeBody: false`、减小 `count`）
3. 增加过滤条件，缩小查询范围。
