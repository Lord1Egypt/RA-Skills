---
name: pan-hub
slug: pan-hub
displayName: 网盘通
version: "0.7.0"
author: lis
license: CC-BY-NC-SA-4.0
description: 统一从百度、阿里云盘、夸克、天翼、迅雷、115、123云盘、移动云盘、沃盘、UC、PikPak、坚果云、OneDrive/SharePoint、Google Drive、Dropbox、微云、蓝奏及更多网盘分享链接、转存文件夹或直链到本机、Windows、NAS 或远程私有存储。用户只需提供网盘下载地址；技能通过统一命令行和共享下载引擎完成识别、登录引导、目录规划和下载，不必逐个安装各家官方客户端。支持群晖、威联通、飞牛、TrueNAS、Unraid、绿联、极空间、华为家庭存储、蒲公英外接盘等通过 SSH/WebDAV/SMB/S3/rclone/挂载路径接入。免费账号默认单线程+断点续传，账号等级从已配置的可信探测器读取，探测不到按免费处理；会员仅按平台官方权益调整本地并发，不承诺不限速，不绕过平台风控。
metadata:
  version: "0.7.0"
---

# 网盘通

## 概述

本技能把“用户给出网盘地址 → 识别平台 → 按官方要求登录/授权 → 规划目录 → 下载到本机或远程设备”做成统一入口。

把“贴链接 → 选目录 → 自动下载”做成一个统一入口。技能本身不实现各网盘私有协议，也不要求逐个安装百度、夸克、天翼等官方客户端；它只维护一套统一 CLI，把链接交给共享引擎（AList / rclone / BaiduPCS-Go / 夸克 CLI / WebDAV / aria2 / curl）执行。

典型用法：任何 agent 拿到用户提供的网盘地址后调用 `scripts/pan.py get "<链接>"`；需要登录时只给出本机授权步骤，账号密码由用户在本机系统凭据库保存，不进入聊天、不进配置文件、不写日志。

扩展目录 `extensions/chrome/`：复制链接 → 右键一键发送给本机 `serve` → 自动后台下载；剪贴板监听只提取链接文本，不自动读取页面登录态。

## 铁律（先读完再执行）

1. 不破解会员、限速、验证码、广告或风控；`tier=vip` 只调整本工具调度并发，不改变平台限制，也不承诺“不限速”。
2. 账号密码、Cookie、Token、BDUSS 等凭据只允许存操作系统凭据库（macOS Keychain、Windows Credential Manager 或 Linux secret-tool），或由 AList/rclone/BaiduPCS-Go 自己保存在受保护配置中；技能不把明文写进 `config.json`，不打印，不上传云端，不进 Git。
3. 不允许用户把账号密码、Cookie、Token 发到 agent 聊天里。需要输入时执行 `python3 scripts/pan.py secret set <凭据名>`，在用户自己的本机终端不显式输入；Windows 使用 `scripts\pan.ps1` 或 `scripts\pan.cmd`。
4. 分享提取码不是账号密码，可以随下载命令传入；仍需按最小必要原则使用。
5. 公司内部资料默认只下载、不上传；下载目录不进 iCloud，也不把公司内容上传到第三方云盘或远程第三方服务。
6. 账号等级默认 `tier=auto`：优先读取 `drives.<盘>.account_tier`；配置了可信 `tier_detector` 时执行探测；全局无法可靠判断时按免费账号处理（并发 1）。不能凭账号名、用户名或链接猜会员。
7. 会员账号自动提速只做本地调度：aria2 调整 `-x/-s`，rclone 调整 `--transfers`；实际速度仍由各网盘官方规则决定。
8. 免费账号默认：并发 1、重试 3、断点续传、单任务日志。
9. 默认下载根目录：macOS 优先 `/Volumes/PanDownloads/网盘下载` 和 `/Volumes/PanOffice/网盘下载`；Windows 为 `%USERPROFILE%\\Downloads\\网盘下载`；其他平台为 `~/Downloads/网盘下载`。用户可用 `pan set --root`、`get --to` 或 `remote` 覆盖。
10. 目录递归下载优先使用 AList + rclone；curl 回退只适合单文件。共享引擎缺失时给出配置说明，不假装成功。
11. 远程设备按能力接入，不按品牌写死：SSH 适合远程执行，WebDAV/SMB/S3/rclone/已挂载路径适合远程落地。远程部署不上传本机凭据文件。

## 智能默认 + 自动重试

- 智能分类归档：`pan set --auto-classify on` 开启后按扩展名自动归到 影视/音乐/文档/图片/压缩包/其他；单次可 `pan get <链接> --classify`。
- http 直链默认重试 3 次并断点续传；任务失败可在 Web UI 一键重试。

## PWA 可安装外壳

- Web 页面新增 `/test` 测试连接页：粘贴链接即可检查能否下载（不真正下载）。
- `pan serve` 页面自带 `/manifest.webmanifest`、`/sw.js` 与图标，可在浏览器安装为独立窗口；仍只监听 127.0.0.1。

## 标准流程

1. `python3 scripts/pan.py doctor` —— 检查 Python、curl、系统凭据库、共享引擎和默认目录。
2. 首次使用：`python3 scripts/pan.py setup`（一键安装向导，自动创建 600 权限配置并列出缺失依赖安装命令；可加 `--apply` 实际调用包管理器）；或仅 `python3 scripts/pan.py init`。Windows 用 `scripts\\pan.ps1 setup` 或 `scripts\\pan.cmd setup`。
3. 凭据：在本机终端执行 `python3 scripts/pan.py secret set engine.webdav`（或 `engine.alist`、`drive.<盘名>`），密码不会出现在命令行。
4. 查看登录/授权步骤：`python3 scripts/pan.py login <盘名> [--open]`（`--open` 用默认程序打开授权教程）。OAuth、扫码、Cookie 等按各平台官方要求完成。
5. 先预演：`python3 scripts/pan.py get "<链接>" --pwd <提取码> --dry-run --json`。
6. 确认无误后去掉 `--dry-run` 执行；目录递归时加 `--path /挂载名/子目录`。
7. 完成后报告：目标目录、成功/失败文件数、日志位置、缺失依赖或需人工核对项。

远程设备流程：`remote add` 登记 → `remote check --probe` 检查 → SSH 模式 `remote deploy` → `remote get`；WebDAV/SMB/S3 模式先在 rclone 配置 remote，再直接 `remote get` 或 `get --remote`。

## 命令速查

```bash
# 环境与识别
python3 scripts/pan.py doctor
python3 scripts/pan.py detect "https://pan.quark.cn/s/xxxx"
python3 scripts/pan.py test "<链接>"           # 先测能不能下载：识别/依赖/目录/提取码，不真正下载

# 安全凭据（推荐在本机终端执行，不要在聊天中粘贴密码）
python3 scripts/pan.py secret set engine.webdav
printf '%s\n' "$WEBDAV_PASSWORD" | python3 scripts/pan.py secret set engine.webdav --stdin
python3 scripts/pan.py secret list
python3 scripts/pan.py secret check engine.webdav --json
python3 scripts/pan.py secret migrate

# 仅保存地址/用户名，密码引用系统凭据库
python3 scripts/pan.py set --webdav-url "https://dav.jianguoyun.com/dav" --webdav-user "账号"
python3 scripts/pan.py set --alist-url "http://127.0.0.1:5244" --alist-user "AList账号"

# 下载
python3 scripts/pan.py get "https://pan.baidu.com/s/1xxxx" --pwd 1234 --dry-run
python3 scripts/pan.py get "https://example.com/a.zip"                 # 直链，curl 立即可用
python3 scripts/pan.py get "<链接>" --to "/Volumes/PanDownloads/资料"           # 指定目录
python3 scripts/pan.py get "<链接>" --at 02:30           # 低峰：凌晨两点再开始
python3 scripts/pan.py get "<链接>" --path "/AList/目标目录"             # AList 目录递归
# 下载完成钩子（自动解压/媒体入库模板）：scripts/post_media.sh

# 账号等级
python3 scripts/pan.py set --tier auto
python3 scripts/pan.py set-drive 115 --account-tier vip
python3 scripts/pan.py set-drive 115 --tier-detector '检测命令'
python3 scripts/pan.py get "<链接>" --tier vip

# Agent/脚本
python3 scripts/pan.py get "<链接>" --dry-run --json                   # 无凭据 JSON 计划

# Windows PowerShell（在 scripts 目录）
.\\pan.ps1 doctor
.\\pan.ps1 secret set engine.webdav

# 远程 NAS / 私有存储：SSH 远程执行
python3 scripts/pan.py remote add nas --kind ssh --host 192.168.1.10 --user lis --root /volume1
python3 scripts/pan.py remote check nas --probe
python3 scripts/pan.py remote deploy nas
python3 scripts/pan.py remote deploy nas --web-port 17890             # 部署+后台启动远程 Web 控制页
python3 scripts/pan.py remote get nas "<链接>" --pwd <码> --dry-run
python3 scripts/pan.py remote web nas                                 # 打印远程 Web 地址与 SSH 反向隧道

# 快速上手 / MCP / 只读状态页
python3 scripts/pan.py init --wizard          # 环境检测向导（--json 取机器可读）
python3 scripts/pan.py mcp guide              # 输出 Codex MCP 注册片段
python3 scripts/pan.py serve                  # 只读本地状态页 127.0.0.1:17890

# 飞书机器人（第 3 步）
python3 scripts/pan.py notify --channel feishu --title "下载完成" --body "已落盘" --send
python3 scripts/feishu_bot.py --check                 # 离线自检
python3 scripts/feishu_bot.py --host 0.0.0.0 --port 9001
# 详见 references/28-飞书机器人.md

# 浏览器扩展 + 剪贴板监听（本机桥接）
# 运行：python3 scripts/pan.py serve
# 然后在 Chrome chrome://extensions 加载本技能 extensions/chrome/ 目录，
# 复制/选中网盘链接后右键「发送 网盘链接 到 pan 下载」，或点扩展图标手动粘贴。
# 扩展只连接 http://127.0.0.1:17890/*，不读取网盘登录态/上传云端。
# 接口：POST /api/download {url,pwd,to,engine,tier,path}

# 通知（默认 dry-run；webhook 地址先存系统凭据库）
python3 scripts/pan.py secret set notify.work_weixin --stdin
python3 scripts/pan.py notify send --title 下载完成 --body "{target}"
python3 scripts/pan.py notify send --send --title 下载完成 --body "{target}"
python3 scripts/pan.py notify send --channel telegram --chat-id 12345 --title 完成 --body "已经下好"

# 真机验证（沙箱内无法完成的回归在本机跑一次）
python3 scripts/verify_real_env.py

# 跨盘转存 / 增量同步（rclone，默认 dry-run）
python3 scripts/pan.py transfer alist:源/目录 alist:目标/目录 --apply
python3 scripts/pan.py sync alist:源/目录 alist:目标/目录 --delete --apply

# 远程 NAS / 私有存储：rclone/WebDAV/SMB/S3 落地
python3 scripts/pan.py remote add vault --kind webdav --remote-name vault --root /downloads
python3 scripts/pan.py get "<链接>" --remote vault --dry-run --json
```

## 引擎对照

| 网盘 | 推荐引擎 | 状态 |
|---|---|---|
| 直链 HTTP/HTTPS | curl（内置） | 开箱可用 |
| 任意可直链 | aria2（可选） | 装了自动用；会员可提高本地并发，但速度仍受平台限制 |
| 百度网盘 | BaiduPCS-Go | 需登录 BDUSS；分享先转存再下载 |
| 阿里云盘 | AList | 需 AList 挂载或开放平台授权 |
| 夸克网盘 | 夸克 CLI / AList | Cookie 登录，非官方接口 |
| 天翼云盘 | AList | Cookie/账号登录 |
| 迅雷云盘 | AList | refresh_token/Cookie |
| 115 / 123 / 移动云盘 / 沃盘 / UC / PikPak / OneDrive / Google Drive / Dropbox / 微云 / 蓝奏 | AList + rclone | 先挂载/转存，再按 `--path` 递归下载；免费 `--transfers 1`，会员按 `max_connections_vip` |
| 坚果云 | WebDAV | 使用应用密码，凭据从系统凭据库/stdin 传入，支持断点续传 |
| 悟空 / 豆包新盘 / Mega / TeraBox / pCloud / Proton Drive / Yandex Disk / MediaFire / Trainbit / 光雅盘 / 飞鸡云 / 闪电盘 | AList（可选自定义 CLI） | 以当前驱动支持为准 |
| 城通网盘 | 自定义 `engine_command` | AList 兼容性不稳定 |
| 远程 NAS/私有存储 | SSH / rclone / WebDAV / SMB / S3 / mount | 不绑定品牌；有这些协议之一即可接入，详见 `references/21-远程NAS与私有存储.md` |

## 安全边界

- 默认安全路径：`config.json` 只保存 `credential:名称`/旧 `keychain:名称` 引用、用户名、URL 和路径；密码只存系统凭据库。
- 旧配置里如果存在明文 `alist_password`、`webdav_password` 或 drive 凭据字段，执行 `secret migrate` 迁移；迁移失败时拒绝继续保存新明文。
- 运行时日志和 `--json` 计划会打码或省略凭据；Basic Auth 通过 `curl --config -` 从 stdin 注入，不进入 argv。
- 第三方 CLI/AList/rclone 的登录态由其自身保存；技能不复制、不读取其内部密码。远程设备上的登录态也必须在远程设备本机保存。
- 平台要求验证码、二次验证、扫码或客户端授权时，回到官方页面完成；技能不绕过。
- 只下载你有权访问的内容，公司资料只下载不上传。

## 任务中心 Web UI（v2，支持任务控制）

- `python3 scripts/pan.py serve` 打开 `http://127.0.0.1:17890/`：实时任务、任务控制记录与历史报告统一成任务表，2 秒自动刷新。
- 页面：`/`（任务中心）、`/live`（实时速度）、`/api/tasks`（支持 `?state=paused|cancelled|running|done|failed`）、`/api/status`、`/api/live`、`/api/reports`、`/api/task/action`。
- v2 已实际落地任务控制：`pan task list|show|pause|resume|delete|retry <id>`；Web 表格提供暂停/继续/取消/删除/重试按钮，暂停/继续为进程级真实操作。

## 实时速度监控

- 下载时加 `--live`（或配置 `http.live_status: true`），实际下载期间会周期性采样目标目录字节增量，实时写入 `下载速度.live.json`：含实时/平均速度 KB/s、已下载字节、当前步骤、状态与更新时间。
- 查看实时速度：下载时另开终端执行 `python3 scripts/pan.py serve`，打开 `http://127.0.0.1:17890/live`（每 2 秒自动刷新）；接口 `GET /api/live` 返回最近实时状态 JSON。
- 采样间隔与输出目录可用 `http.live_interval`（默认 1.0 秒）和 `http.live_dir` 覆盖；不配置 `live_dir` 时写到报告目录或下载目标目录。
- 下载结束后实时文件状态写入 `done`/`failed`，不会泄露任何凭据。

## 报告与完成钩子

- 实际下载完成后会在目标目录生成 `下载报告.json`（含起始/结束时间、耗时、每个引擎步骤的退出码与耗时、缺失/警告）。报告目录可在 `config.json` 的 `http.report_dir` 自定义。
- 下载成功后可执行完成钩子：`pan set --alist-url ...` 用不到它，请在本机配置 `http.on_complete_hook`，例如 `rsync {target}/ 远程目录/`。占位符：`{target}` `{report}` `{drive}` `{engine}` `{tier}` `{url}`。
- Agent 场景使用 `python3 scripts/pan.py get "链接" --events` 让实际下载过程输出逐步 JSON 事件（每步骤一行，含 rc/耗时），便于上层展示和统计。
- http 直链单文件可启用 Range 分片：`python3 scripts/pan.py get "直链" --split 4`（或配置 `http.range_split` + `http.range_split_connections`）。仅对服务端返回 `Content-Length` 且支持 `Accept-Ranges: bytes` 的直链生效；探测失败自动回退整文件下载，不影响其他引擎。

## 扩展新网盘

不改脚本，只在 `~/.config/pan-downloader/config.json` 增加：

```json
"extensions": {
  "mydrive": {
    "name": "某网盘",
    "domains": ["pan.example.com"],
    "engine_command": "mytool dl {url} --pwd {pwd} -o {dir}"
  }
}
```

占位符：`{url}` `{pwd}` `{dir}` `{name}` `{tier}`。先用 `detect` + `--dry-run` 验证。

## 按需读取

- 通用说明与排障：`references/00-使用说明.md`
- Agent 调用与凭据保护：`references/20-Agent调用与隐私.md`
- 百度：`references/01-百度网盘.md`
- 阿里：`references/02-阿里云盘.md`
- 夸克：`references/03-夸克网盘.md`
- 天翼：`references/04-天翼云盘.md`
- 迅雷：`references/05-迅雷云盘.md`
- 扩展新盘：`references/06-扩展新网盘.md`
- 115：`references/07-115网盘.md`
- 123：`references/08-123云盘.md`
- 移动云盘：`references/09-移动云盘.md`
- 沃盘：`references/10-联通沃盘.md`
- UC：`references/11-UC网盘.md`
- PikPak：`references/12-PikPak.md`
- 坚果云 / WebDAV：`references/13-坚果云.md`
- OneDrive/SharePoint：`references/14-OneDrive与SharePoint.md`
- Google Drive：`references/15-GoogleDrive.md`
- Dropbox：`references/16-Dropbox.md`
- 腾讯微云：`references/17-腾讯微云.md`
- 蓝奏云：`references/18-蓝奏云.md`
- 其他网盘：`references/19-其他网盘.md`
- 远程 NAS/私有存储：`references/21-远程NAS与私有存储.md`
- Windows 配置：`references/22-Windows配置.md`
- MCP / Agent 接口：`references/23-MCP与Agent接口.md`
- 跨盘转存与增量同步：`references/24-跨盘转存与同步.md`
- 真机验证清单：`references/25-真机验证清单.md`
- OpenAPI / Agent 稳定接口：`references/26-OpenAPI.md`

## 自测

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/self_test.py
```

必须输出 `SELF_TEST_OK`。
