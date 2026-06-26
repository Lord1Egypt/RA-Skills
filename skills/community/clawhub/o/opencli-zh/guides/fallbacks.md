# Fallbacks

在 opencli 需要进入排障、补卡或自定义扩展分支时使用本文件。

## 第一动作

若只是常规环境排障，可先执行：

```bash
opencli doctor
```

但若排障将涉及登录态站点、扩展重载、浏览器桥接状态核查，或需要指导用户调整 `extension/` / `chrome://extensions`，先说明会触达浏览器侧状态并获得同意。

## 健康状态参考

理想情况下应看到：
- Chrome/Chromium: ✓
- Daemon running: ✓
- Chrome extension connected: ✓

## 常见问题

### daemon 未运行
可能表现：
- 命令长时间挂起
- 依赖浏览器登录态的网站无响应

优先检查：
- Chrome 是否已打开
- daemon 会在首次运行浏览器命令时自动启动
- 重启 Chrome 后再执行 `opencli doctor`
- 手动检查 daemon 状态：`curl localhost:19825/status`

### Chrome 扩展未连接
可能表现：
- 浏览器型站点命令失败
- 公开站点命令可能正常，登录态站点异常

优先检查：
- opencli Browser Bridge 扩展是否已安装并启用
- 扩展需通过 `chrome://extensions` 加载 `extension/` 目录（开发者模式）
- Chrome 是否刚重启但扩展尚未恢复
- 再次执行 `opencli doctor`

### 登录态失效
可能表现：
- 结果为空
- 返回不完整
- 某个站点单独失败

优先检查：
- 用户是否仍登录目标网站
- 必要时让用户在 Chrome 中重新登录后再试

### 外部 CLI 缺失
可能表现：
- `gh`、`docker`、`kubectl` 等透传命令失败

说明：
- 这不等于 opencli 核心故障
- 只代表对应外部 CLI 未安装或不可用

### Node.js / npx 缺失
可能表现：
- `opencli` 命令本身找不到

说明：
- opencli 基于 Node.js，需要先安装 Node.js
- 安装命令：`npm install -g @jackwener/opencli`
- 更新命令：`npm update -g @jackwener/opencli`

## 自定义适配器触发条件

当满足以下条件时，读取 `guides/custom-adapters.md`：
- 已确认用户要访问的网站应由 opencli 承接
- 已用 `opencli <site> --help` 与相关子命令 `--help` 确认后，仍找不到可完成目标的现成命令
- 需要为该网站补一个新的 opencli 适配器

进入该分支前，必须先告知用户：将为该网站自动创建 opencli 自定义适配器。

## 自动补写 target reference 触发条件

当满足以下条件时，读取 `guides/reference-bootstrap.md`，按统一模板补写 `references/<target>.md`：
- 已确认用户请求的目标由 opencli 现成命令支持
- `references/<target>.md` 当前不存在
- 本轮已可直接用 opencli 成功回应用户
- 需要为下次复用补写该目标 reference

## 回退规则

- 若是读操作，且 opencli 当前不可用，可再考虑其他合适工具。
- 若是写操作，不得静默切换到其他执行路径。
