# Socket 故障排查

## 首次使用先检查

先确认工具是否已安装：

```bash
mtop-devtools --version
mtop-devtools-native-host --version
```

如果命令不存在，请先安装：

```bash
npm install -g @mtop-devtools/native-host @mtop-devtools/client
```

如果命令存在，重新初始化：

```bash
mtop-devtools-native-host --init
```

之后检测环境是否就绪：

```bash
mtop-devtools check
```

## EACCES（权限不足）

初始化脚本写入系统目录时权限不足。

处理步骤：
```bash
sudo mtop-devtools-native-host --init
```

## ENOENT（找不到 Socket）

native host socket 尚未启动。

**从 v1.29+ 起，client 会在 ENOENT 时自动尝试拉起 `mtop-devtools-native-host` 并在 1.2s 后重试，大多数情况下无需手动干预。**

如果重试后仍然失败，可按以下步骤排查：

**使用浏览器插件模式：**
1. 确认 Chrome 浏览器已打开，等待插件自动建联（约 60s 内）。
2. 如仍失败，打开 DevTools 切换到 Mtop 面板手动触发建联。
3. 如果使用本地开发版扩展，需指定扩展 ID：`mtop-devtools-native-host --init --extension-id {EXTENSION_ID}`
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
   - `mtop-devtools-native-host --init`
4. 重新执行命令。

## 请求超时

扩展未能在超时时间内返回数据。

处理步骤：
1. 增加超时参数：`--timeout 30`
2. 降低 payload 大小（如 `includeBody: false`、减小 `count`）
3. 增加过滤条件，缩小查询范围。
