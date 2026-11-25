# 网盘通（pan-hub）

## 概述

本 Skill 的功能是：让 AI 助手接收用户给出的**网盘分享链接、转存文件夹地址或 HTTP 直链**，自动识别网盘、引导官方登录或授权、规划下载目录，并调用共享下载引擎把资源下载到用户指定的位置。用户不必逐个安装百度、阿里、夸克、天翼、迅雷等官方客户端。

主要能力包括：

- 统一入口：一条命令完成链接识别、目录规划、下载执行和结果报告。
- 多网盘适配：百度、阿里云盘、夸克、天翼、迅雷，以及 115、123、UC、移动云盘、沃盘、PikPak、坚果云、微云、蓝奏云、OneDrive/SharePoint、Google Drive、Dropbox 等。
- 可扩展：未内置的网盘可通过自定义引擎命令或共享引擎接入。
- 多种目标：本机 macOS、Windows、Linux，远程 NAS，WebDAV/SMB/S3 私人存储，以及已挂载的公司介质或外接硬盘。
- 账号等级：默认自动读取可信探测器；无法确认时按免费账号策略运行。会员账号只在平台官方权益内调整本地并发，不承诺不限速。
- 凭据保护：账号密码、Cookie、Token、BDUSS 等敏感信息只允许保存到系统凭据库或受保护的第三方工具配置，不进入聊天、命令行参数、日志、Git 或第三方云盘。
- 合规边界：不破解会员、限速、验证码、广告或风控；平台要求授权、扫码、OAuth 或二次验证时，回到官方页面完成。

> 身份说明：这是 AI 助手调用的工具型 Skill，不伪装成网盘官方客户端，也不冒充任何人物或外部产品。

## 支持的网盘和存储

| 范围 | 已登记对象 |
|---|---|
| 首批网盘 | 百度网盘、阿里云盘、夸克网盘、天翼云盘、迅雷云盘 |
| 扩展网盘 | 115、123 云盘、移动云盘/和彩云、联通沃盘、UC 网盘、PikPak、坚果云、腾讯微云、蓝奏云、悟空网盘、豆包新盘、城通网盘 |
| 国际网盘 | OneDrive/SharePoint、Google Drive、Dropbox、Mega、TeraBox、pCloud、Proton Drive、Yandex Disk、MediaFire、Trainbit |
| 小型网盘 | 光雅盘、飞鸡云、闪电盘；其他站点可通过扩展配置接入 |
| 远程设备 | SSH/SFTP、WebDAV、SMB/CIFS、S3/MinIO、rclone remote、本机挂载路径 |
| NAS/私人存储示例 | 群晖 Synology、威联通 QNAP、铁威马 TerraMaster、华芸 ASUSTOR、TrueNAS、Unraid、绿联 UGREEN、极空间 ZSpace、华为家庭存储、联想个人云、海康存储、拾光坞、万由 U-NAS、飞牛 fnOS、奥睿科、雷克沙、西数 My Cloud、希捷、华硕，以及 OpenWrt/USB 硬盘、树莓派、迷你主机、VPS；私有云软件可接 Nextcloud、ownCloud、Seafile、Syncthing、Resilio Sync、MinIO |
| 私有云网关 | 蒲公英/贝锐外接硬盘按实际开放的 VPN、SMB 或 WebDAV 能力接入，不假设存在通用官方下载 API |

## 快速开始

```bash
python3 scripts/pan.py doctor
python3 scripts/pan.py init
python3 scripts/pan.py detect "<网盘分享链接>"
python3 scripts/pan.py test "<网盘分享链接>" --pwd <提取码>   # 先测试能否下载，不真正下载
python3 scripts/pan.py get "<网盘分享链接>" --pwd <提取码> --dry-run --json
python3 scripts/pan.py get "<网盘分享链接>" --pwd <提取码> --to "<用户指定目录>"
```

Windows 可在 `scripts` 目录使用 `pan.ps1` 或 `pan.cmd`。首次登录按 `pan.py login <盘名>` 的官方步骤在本机完成（可加 `--open` 直接打开授权教程）；密码不要粘贴到聊天中。

## 一键启动（网页下载助手）

- `sh scripts/pan_web.sh`：自动启动本机 serve + 全局剪贴板监听 + 打开 Web 首页；剪贴板里出现网盘链接会自动投递并跳转实时进度。
- 剪贴板监听亦可单独运行：`python3 scripts/clipboard_monitor.py`（macOS/Linux/Windows 均可轮询系统剪贴板，不依赖浏览器）。

## 任务中心 Web UI（v2，支持任务控制）

- `python3 scripts/pan.py serve` 打开 `http://127.0.0.1:17890/`：实时任务、任务控制记录与历史报告统一成一张任务表，每 2 秒自动刷新。
- 页面入口：`/`（任务中心，首页含「粘贴链接开始下载」表单，提交后自动跳转 `/live` 看实时进度）、`/test`（测试连接，粘贴链接即可检查能否下载）、`/live`（纯实时速度）、`/api/tasks`、`/api/status`、`/api/live`、`/api/reports`、`/api/test?url=...`（测试连接）、`/api/task/action`（暂停/继续/取消/删除/重试）。
- 命令行控制：`pan task list|show|pause|resume|delete|retry <id>`，运行中可暂停/取消，暂停中可继续/删除，已结束可重试/删除。

## 实时下载速度监控

- `python3 scripts/pan.py get "链接" --live` 会在下载期间实时写入 `下载速度.live.json`（实时/平均速度、已下载字节、当前步骤、状态）。
- 另开终端执行 `python3 scripts/pan.py serve`，浏览器打开 `http://127.0.0.1:17890/live` 即可看到自动刷新的实时速度；`/api/live` 为 JSON 接口。
- 采样间隔 `http.live_interval` 默认 1 秒，实时文件可指定目录 `http.live_dir`；配置 `http.live_status: true` 后无需每次加 `--live`。


## 智能默认 + 自动重试

- 智能分类归档：`smart.auto_classify` 开启后（`pan set --auto-classify on`），下载前按扩展名自动拆到 影视/音乐/文档/图片/压缩包/其他 目录，避免全堆一个文件夹；单次可用 `get --classify` 手动开启。
- 自动重试与断点续传：`http.retries`（默认 3）+ curl `-C -` / rclone 断点，失败自愈不用反复手动点。

## Web UI 可安装（PWA）

- 打开 `http://127.0.0.1:17890/` 后，浏览器地址栏会显示“安装”按钮，可安装成独立窗口应用。
- 清单 `/manifest.webmanifest`、离线外壳 `/sw.js`、图标 `/icons/icon-192.png`、`/icons/icon-512.png`。
- 仍是仅本机访问：不读取任何网盘登录态或上传云端。

## 浏览器扩展 + 剪贴板监听

- 扩展目录：`extensions/chrome/`（Manifest V3），加载方法见 `extensions/chrome/README.md`。
- 启动本机服务后（`python3 scripts/pan.py serve`，默认 `127.0.0.1:17890`），Chrome 加载该目录即生效。
- 复制/选中网盘链接后，右键菜单「发送 网盘链接 到 pan 下载」自动把链接发到本机 `POST /api/download`，由 `pan get --live` 后台下载。
- 同时监听剪贴板 `copy`、键盘复制和选区变化，自动识别链接；`popup` 可手动粘贴链接并填写提取码、目标目录、引擎/档次。
- 扩展仅连接 `http://127.0.0.1:17890/*`，不读取网盘页面登录态，也不上传任何云端平台数据。
- 剪贴板监听默认只自动提取链接文本；提取码不会自动从页面读取，请在弹窗确认或手动填写。

## 账号等级与速度

- `tier=auto`：优先读取用户配置的账号等级；配置了可信 `tier_detector` 时执行探测；无法可靠确认时按免费账号处理。
- 免费账号：并发 1、重试 3、断点续传、单任务日志。
- 会员账号：只通过已配置的官方权益信息调整本地并发，实际速度仍由对应平台规则决定。
- 下载中断：保留已完成文件和任务目录，优先断点续传，不重复清空或危险覆盖。

不支持绕开平台限速、付费限制、验证码、广告或风控，也不把网络传闻中的“提速插件”当作合规能力。

## 远程 NAS / 私人存储

```bash
python3 scripts/pan.py remote add nas --kind ssh --host 192.168.1.10 --user lis --root /volume1
python3 scripts/pan.py remote check nas --probe
python3 scripts/pan.py remote deploy nas                                          # 仅部署
python3 scripts/pan.py remote deploy nas --web-port 17890                         # 部署+后台启动远程 Web 控制页
python3 scripts/pan.py remote get nas "<链接>" --pwd <码>
python3 scripts/pan.py remote web nas                                             # 打印访问地址与 SSH 反向隧道

python3 scripts/pan.py remote add vault --kind webdav --remote-name vault --root /downloads
python3 scripts/pan.py get "<链接>" --remote vault --dry-run --json
```

远程模式不会把本机 `config.json`、密码、Cookie 或 Token 上传到远程设备；远程设备上的登录态也必须在该设备本机保存。

## 飞书机器人（第 3 步）

- `pan notify --channel feishu`：群机器人 Webhook 发送完成/失败通知。
- `scripts/feishu_bot.py`：飞书事件回调桥，把“发链接→自动下载”转给本机/NAS 的 `serve`；离线自检 `--check`。详见 `references/28-飞书机器人.md`。

## 安全边界

- 不破解会员、限速、验证码、广告或风控。
- 账号密码、Cookie、Token、BDUSS 等敏感值不进入聊天、argv、日志、明文配置、Git 或第三方云盘。
- 公司资料只下载到公司控制的设备或本机介质，不上传到第三方云盘或 Git 远端。
- 只下载用户有权访问的内容；分享提取码按最小必要原则使用。
- 平台接口变化时，以官方页面和当前维护中的共享引擎为准，不假装成功。

## 市场定位

同类能力主要分散在几类产品中：

| 类型 | 代表 | 与本 Skill 的关系 |
|---|---|---|
| 共享下载引擎 | rclone、AList、aria2 | 能力相近，擅长挂载、同步和多存储，但通常不负责完整的分享链接识别、登录引导和 Agent 统一入口 |
| 单网盘工具 | BaiduPCS-Go、夸克 CLI 等 | 主要覆盖单一平台，适合作为本 Skill 的底层引擎 |
| Agent Skill 市场 | SkillHub 等 | 可发现和安装单网盘、NAS 或下载相关 Skill；相邻技能较多，但统一聚合度、远程目标范围和凭据保护边界需要用户自行拼接 |
| MCP/工具注册中心 | MCP Registry 等 | 提供工具协议和发现机制，不是完整的网盘下载 Skill |

本 Skill 的差异化是：一个统一入口同时处理分享链接、转存文件夹和直链，统一适配多个网盘，支持本机与远程设备落盘，并提供系统凭据保护和免费/会员合规判断。它不是网盘官方客户端，也不承诺绕过任何平台限制。

## 许可

文档与脚本采用 CC BY-NC-SA 4.0，详见 `LICENSE.md`。


## 下载后处理链模板（v0.6.1-R4）

- 下载完成后可自动解压/重命名/媒体入库：把 `scripts/post_media.sh` 绝对路径填进 `http.on_complete_hook`：
  `bash "/绝对路径/scripts/post_media.sh" "{target}" "{drive}" "{engine}" "{report}"`
- 脚本默认 `AUTO=0`（只预览要做什么），改成 `AUTO=1` 才实际解压；Jellyfin/Emby/Plex 扫描命令在脚本第 2 步注释处配置。


### 定时 / 低峰下载（骨架）

- `pan.py get "<链接>" --at 02:30` 会等到达定时间再开始（当前未到）；未指定时读 `http.schedule_at`。
- 大文件可按 `--at 02:30` 排到凌晨，避开白天带宽高峰（骨架为 CLI 阻塞等待，未接入系统调度器）。
