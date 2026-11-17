---
name: pc-space-cleanup
description: Windows 10/11 上 C/D 盘空间不足时的体检与腾空间流程：只读盘点大目录 → 清开发缓存 → 项目打包 → 上传到 CloudDrive2 挂载的网盘（如 123 云盘）并逐文件校验 → 用户确认后删本地 → 整理云端目录。当用户说「C 盘满了 / 清理磁盘 / 整理空间 / 哪些文件可以传云盘 / 传到网盘 / 整理云盘」时使用；含 CloudDrive 先写本地缓存、切网后上传卡住、PowerShell 5.1 中文路径乱码等坑。上云部分要求本机装有 CloudDrive2 并已挂载网盘盘符。
---

# Windows 磁盘空间整理（体检 → 上云 → 删本地 → 整理云端）

一次真实整理的参考量级：C 盘剩余 42GB → 76GB，D 盘 16GB → 37GB，上云约 37GB，前后两天。

下文用到的约定：

| 变量 | 含义 | 示例 |
|---|---|---|
| `$SK` | 本 skill 所在目录 | `$SK = "$env:USERPROFILE\.claude\skills\pc-space-cleanup"` |
| `$WORK` | 工作目录（日志、暂存 zip、备份） | `$WORK = "$env:USERPROFILE\pc-optimize-backup"` |
| `$R` | CloudDrive 挂载的网盘根目录 | `$R = 'Z:\123云盘'` |
| `$PY` | 真实的 python.exe（**别用 `WindowsApps` 下的商店别名**） | `(Get-Command python).Source` 确认不在 `WindowsApps` 里 |

## 铁律

1. **只读盘点可以随便跑，写操作先出 dry-run 表**（路径 / 大小 / 文件数 / 去向），用户确认后再做。
2. **删本地的唯一前提是"上传队列 = 0 且缓存 = 0 且逐文件大小一致"**。robocopy 拷完、网盘盘符上看到文件，都**不代表**已上云（见坑 1）。
3. 删除前再出一张核对表（每组 项数 / 文件数 / C / D），用户回"确认删除"才删；直接删，不进回收站。
4. 云端整理**只移动不删除**：重复件、空目录移进 `_待删除`，看不懂的移进 `_待确认`，让用户自己删。
5. 先问用户有哪些不能碰的：别人共享过来、还在更新的云端目录；正在用的应用数据，比如新版微信 `xwechat_files`、企业微信 `Documents\WXWork`。

## 开工前先确认的本机事实

| 项 | 怎么查 | 备注 |
|---|---|---|
| 硬盘与分区 | `Get-PhysicalDisk; Get-PSDrive -PSProvider FileSystem` | 单盘分 C/D 时，D 腾出的空间帮不了 C |
| 网盘挂载 | `Get-PSDrive` 里 CloudFS 类型的盘符 | 下面可能挂多个网盘，确认目标根目录 `$R` |
| CloudDrive 本地缓存 | API `GetSystemSettings` 字段 4；常见在 `$env:LOCALAPPDATA\CloudDrive.WinUI\temp` | **通常在 C 盘** |
| CloudDrive API | `http://127.0.0.1:<端口>`，默认 19798，以 CloudDrive 设置为准 | gRPC-Web，`Authorization: Bearer <API 令牌>`；令牌找用户要，放 `$env:CD2_TOKEN`；端口不是默认值时设 `$env:CD2_URL` |
| node 包管理器 | `Get-Command npm,yarn,pnpm` | 调 `.cmd`，`.ps1` 可能被执行策略拦 |
| 打包 | 系统自带 `C:\Windows\system32\tar.exe` | 不假设装了 7z |
| 管理员 | Claude Code 会话默认**不是**管理员 | DISM / 改服务 / pagefile 要用户开管理员终端 |

## 阶段 0：只读盘点

目录大小用 robocopy `/L` 统计，比 `Get-ChildItem -Recurse | Measure` 快一个数量级：

```powershell
function Size($p){ $o = robocopy $p "C:\__nonexist__" /L /S /NJH /BYTES /NFL /NDL /NC /NP /R:0 /W:0 /XJ 2>$null | Select-String '^\s*(Bytes|字节)\s*:'; if($o){ [double](($o.Line -split ':')[1].Trim() -split '\s+')[0] } else {0} }
```

依次看 `C:\`、`D:\`、`$env:USERPROFILE`、`AppData\Local`、`AppData\Roaming` 的一级子目录，再往大的里钻。
常见大头：Docker `docker_data.vhdx`、`Documents\Virtual Machines`、旧版微信 `Documents\WeChat Files`、
`.android\avd`、音乐 / 游戏客户端装在 C 盘根目录、`pagefile.sys`。

**C 盘空间莫名在掉**时，先查这几个（实测一次合计 ~8.5GB 就是它们）：

```powershell
Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending'   # True = 更新装了一半
Size 'C:\Windows\WinSxS'                       # 装更新后可涨好几 GB，重启 + DISM 才能回收
Get-ChildItem "$env:LOCALAPPDATA\Feishu" -Directory   # 飞书自动升级会并存新旧两版 ~2GB
```

## 阶段 1：清开发缓存（先出表）

```powershell
npm.cmd cache clean --force                                  # 实测 7.3GB → 0.45GB
& $PY -m pip cache purge                                     # 走真实 python，避开坏的 WindowsApps\pip.exe
Remove-Item "$env:LOCALAPPDATA\uv\cache" -Recurse -Force     # 仅当 uv 已不用；在用就 `uv cache clean`
yarn.cmd cache clean                                         # 只清 Yarn\Cache\v6；Yarn\Berry 不会动
pnpm.cmd store prune                                         # store 里多数被引用时回收很少
# Temp：只删 7 天前的文件，被占用的跳过
```

`.gradle` / `.m2` / `.cache` / JetBrains 缓存重建成本高，列给用户自己决定。

## 阶段 2：项目文件夹先打包再传

小文件多的目录（实测一个项目目录 13.7 万个文件，九成是 node_modules/build）直接传 CloudDrive 极慢。
打 zip 并剔除可再生目录，**保留 `.git`**（历史不可重建）：

```powershell
$stg = "$WORK\staging"
tar.exe -a -c -f "$stg\$name.zip" --options 'zip:hdrcharset=UTF-8' `
  --exclude node_modules --exclude target --exclude build --exclude dist --exclude .gradle --exclude .svn `
  -C "$env:USERPROFILE\Desktop" $name
# 自检：zip 里不应再有被排除的目录
(tar.exe -t -f "$stg\$name.zip" | Where-Object { $_ -match '(^|/)(node_modules|target|build|dist|\.gradle|\.svn)/' }).Count   # 应为 0
```

- tar 失败会留下 **22 字节的空 zip**（只有结束记录），按 0 字节筛清理会漏掉。
- `.svn` 剔除前问用户：只影响能否直接 `svn update`，代码和未提交改动都在工作文件里。

## 阶段 3：上传 + 校验

写一份 JSON 清单（**UTF-8 带不带 BOM 都行**，PowerShell 用 `-Encoding UTF8` 读），然后：

```powershell
$env:CD2_TOKEN = '<用户给的令牌>'      # 只放环境变量，不写进任何文件
powershell -NoProfile -ExecutionPolicy Bypass -File "$SK\scripts\upload.ps1" -Manifest <清单.json>   # 拷入 → 等队列清空 → 等 60s → 逐文件校验
powershell -NoProfile -ExecutionPolicy Bypass -File "$SK\scripts\verify.ps1" -Manifest <清单.json>   # 只校验（中断后、或换网回来后用）
```

清单格式（`type`：`dir` 整个目录镜像到 `dst`；`file` 单文件放进 `dst` 目录；`files` 把 `src` 下匹配 `filter` 的文件放进 `dst`）：

```json
{ "log": "C:\\Users\\<you>\\pc-optimize-backup\\upload_log.txt",
  "batches": [
    { "name": "项目备份", "items": [
      { "type": "files", "src": "C:\\Users\\<you>\\pc-optimize-backup\\staging", "dst": "Z:\\123云盘\\项目备份\\桌面归档_20261015", "filter": "*.zip" } ] },
    { "name": "学习资料", "items": [
      { "type": "dir",  "src": "D:\\Downloads\\某课程", "dst": "Z:\\123云盘\\学习资料\\某课程" },
      { "type": "file", "src": "C:\\Users\\<you>\\Desktop\\a.rar", "dst": "Z:\\123云盘\\学习资料" } ] } ] }
```

全局排除：`*.baiduyun.p.downloading`（百度网盘未下完的残片，直接删不上传）、`~$*`、`.accelerate`。
每批拷入量控制在 ~10GB 内：缓存在 C 盘，拷多少 C 盘就先少多少，传完才释放。

云端分类**沿用用户已有习惯**：先列 `$R` 的一级目录给用户看，项目一个项目一个 zip 进「项目备份」类目录，其余按已有分类归位；没有合适分类时问用户，不自己发明一套。

### CloudDrive API（`scripts/cd2.py`）

```powershell
$cd2 = "$SK\scripts\cd2.py"
& $PY -I $cd2 GetUploadFileCount          # 返回 "1: N"；队列空时没有字段 1
& $PY -I $cd2 GetUploadFileList 0801      # 0801 = getAll:true
& $PY -I $cd2 PauseAllUploadFiles; & $PY -I $cd2 ResumeAllUploadFiles
& $PY -I $cd2 GetSystemSettings
```

字段含义是**从返回值和现象对出来的**，没有 proto 文件；哪天对不上先回来质疑这张表：

| 返回 | 字段 | 含义 | 依据 |
|---|---|---|---|
| GetUploadFileList 顶层 | 1 / 4 / 5 | 队列文件数 / 总字节 / 已传字节 | 随上传递减、和测试文件大小吻合 |
| 每个任务（字段 2 里） | 2 / 3 / 4 / 5 | 云端路径 / 文件字节 / 已传字节 / 状态 | 状态见过 `WaitingforPreprocessing` `Preprocessing` `Inqueue` `Transfer` `Pause` |
| GetSystemSettings | 2 / 3 | 同时预处理数 / 同时上传数 | 和队列里恒为 `Preprocessing=N`、`Transfer=N` 一致 |
| GetSystemSettings | 4 / 7 / 11 / 12 | 缓存目录 / 写入后延迟上传秒数 / 下载、上传限速(0=不限) | 4 与实测缓存位置一致；其余按顺序推断 |

中文路径在 PowerShell 里会显示成 `����`，只影响显示，数值字段可用。验证于 CloudDrive 1.1.x。

## 阶段 4：删本地

- 按组删，记录每项删除前文件数、删除后是否残留；实测 25 万个文件（多为 node_modules）删了 **853 秒**，前台 10 分钟超时会转后台，属正常。
- 压缩包解压出来的文件夹，只要原包已上云且校验通过就能删。

## 阶段 5：整理云端

CloudDrive 盘符上的 `Move-Item` 是**云端改路径**，不下载不重传：实测 11.55GB 的目录移动用时 0.93s。
用 `scripts/reorg-lib.ps1` 里的 `Into` / `Merge`，同名自动加 `_2` 后缀不覆盖：

```powershell
$R = 'Z:\123云盘'; $LOG = "$WORK\reorg_log.txt"
. "$SK\scripts\reorg-lib.ps1"
Into 'xxx.zip' '游戏\整合包'           # 把根目录的 xxx.zip 移进 游戏\整合包\
Merge '旧目录名' '新分类\子目录'        # 子项全部并入，搬空后原目录进 _待删除
Summary
```

- 先拿一个小目录试移，确认秒级完成再批量；若变成"下载再上传"（几 MB/s），立刻停，改去网盘网页版操作。
- 正在上传的目标目录**等上传完再移**，否则队列里的路径会失效。
- 移动会把文件修改时间刷成当天。
- 判断不了内容的 zip 用 `scripts/peek_zip.py`（只读末尾目录区，不下载整包）。

## 坑（连同报错原文）

1. **CloudDrive 先写本地缓存再后台传**。robocopy 报的 46MB/s 是写缓存速度；网盘盘符上大小一致也只说明进了缓存。
   C 盘会先少掉同等空间。判断上云完成只能看 API 队列 = 0 且缓存目录为空。
2. **切换网络后上传卡死**：已传字节停在分块边界（`134217728`、`2550136832`，都是 128MB 整数倍），
   CloudDrive 进程 30 秒内磁盘读 / 其他 I/O 都是 0.0MB。换到能用的网络后有过自行恢复；在卡住的网络上
   `PauseAllUploadFiles` → `ResumeAllUploadFiles` **没有用**。任务管理器里看到"还在传、只是慢"时，
   最终确实传完了——先多观察几分钟再判断是否要重启 CloudDrive（重启让用户从托盘"退出"再开，别强杀）。
3. **刚传完立刻校验会误报缺失**：网盘目录列表有延迟，实测 1079 个文件报缺 7 个，其中 2 个其实在。
   校验前等 60 秒（脚本已内置）；真缺的那 5 个是 CloudDrive 漏传（同大小的 3 个 `.INI` 一起丢，疑似秒传去重），补传即可。
4. **123 云盘秒传**：常见资源服务器已有，10.85GB 拷入后 C 盘只少了 1.7GB、几分钟就传完。
5. **PowerShell 5.1 读无 BOM 的 UTF-8 `.ps1` 当成 GBK**，中文路径全乱：
   `tar.exe: ...: Couldn't visit directory: No such file or directory`，建出来的目录名是 `妗岄潰`（本应是 `桌面`）。
   含中文的 `.ps1` 一律存成带 BOM 的 UTF-8：
   `[IO.File]::WriteAllText($f, [IO.File]::ReadAllText($f,[Text.Encoding]::UTF8), (New-Object Text.UTF8Encoding $true))`
6. **单元素嵌套数组被摊平**：`@( @('files', $src, $dst, '*.zip') )` 会变成 4 个字符串，脚本报"0 个文件"且不报错。
   要写 `@( ,@(...) )`；本 skill 改用 JSON 清单彻底避开。
7. **函数别起名 `Dir`**：别名优先于函数，`dir` = `Get-ChildItem`，建目录变成列目录：
   `Cannot find path '<当前目录>\游戏\整合包' because it does not exist.` 随后所有移动 `Could not find a part of the path.`
8. **文件名里的不换行空格 U+00A0**：从网页 / 文档复制来的文件名，空格可能是 `00A0`，按普通空格拼路径 `Test-Path` 为 False。用 `-like '前缀*'` 取真实名。
9. `Program 'pip.exe' failed to run: The system cannot find the file specified` —— 命中了 `WindowsApps\pip.exe` 商店别名，改用 `& $PY -m pip`。
10. **"关机"不等于重启**：Win11 快速启动下关机再开，`LastBootUpTime` 不变、`RebootPending` 仍为 True，更新装不完。
    要让用户点 **开始 → 电源 → 重启**。
11. **内存紧张时后台任务可能被 Claude Code 强杀**。CloudDrive 自己的队列不受影响会继续传，
    回来后跑 `verify.ps1` 即可；被杀的任务不要自行重启，先报告。
12. 删除时 `The process cannot access the file 'application.asar' because it is being used by another process.`
    没有任何进程从该目录启动，多半是杀软在扫；重启后再删。
13. **别读 CloudDrive 的 `clouddriveconf.json`**：里面是网盘账号的 `refresh_token` 和加密密码。缓存路径等配置用 API `GetSystemSettings` 读。
14. `Get-Counter '\Process(*)\% Processor Time'` 偶发 `The data in one of the performance counter samples is not valid.`，结果仍可用。
15. robocopy 退出码 `< 8` 都算成功，`1` = 有文件被复制。

## 已经排除的方向

- C 盘掉空间时，实测**不是** CloudDrive / 夸克 / 123 同步盘的本地缓存（都 < 0.1GB），也不是 Docker vhdx（没变）——是 Windows 更新 + 飞书升级。
- CloudDrive 的 `log\<日期>.log` 可能是 0 字节，看日志查不出上传问题；只能走 API。
- 浏览器打开 CloudDrive 管理页依赖浏览器自动化，经常断连；API 更可靠。
- `GetUploadFileList` 的已传字节按块跳变（32MB / 128MB），1 分钟不动不一定是卡死，要配合进程 I/O 一起看。

## 常见收尾项（列给用户决定）

- 需管理员：`Dism /Online /Cleanup-Image /StartComponentCleanup`（先真重启）、不用的服务改手动、pagefile 改系统管理（实测可再回收 12–15GB）。
- 体积大但要用户拍板：Docker 数据盘、虚拟机、Android 模拟器 AVD、装在 C 盘的游戏 / 音乐客户端、旧版微信 `Documents\WeChat Files`（先核对是否已迁到新版，再整体上云后删，删前退出微信）。
- 云端 `_待删除`、`_待确认` 等用户过目。
