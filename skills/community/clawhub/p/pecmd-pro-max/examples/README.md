# 内置示例索引

本目录随技能分发，**不依赖任何外部素材目录**。43 个示例均来自 PECMD2012 1.88.05.94 SDK 官方示例与公开源码，保留原始字节（编码未改动），可直接用 `bin/` 下的解释器加载。

## 使用方式

```wcs
// 语法/行为对照：先读 examples/README.md 找到最接近的范式，再打开对应文件
// 本地试运行（开发机）：
bin\PECMD64.exe LOAD examples\gui\tabl-table.wcs
```

注意事项：

- 示例是**参考实现**，不是开箱即用的产品：部分脚本依赖 PE 环境（`%SystemRoot%`、`X:` 盘、外置工具、驱动）。
- 编码保持原样。UTF-16LE 与 GBK 文件在普通编辑器里可能显示异常，但 PECMD 可正确解析；用支持 BOM/GBK 的编辑器查看。
- 9 个示例使用双编码声明：`#code=936T950`（8 个）或 `#code=950T936`（`gui/tree-view.wcs`）。迁移代码时按目标环境重新声明为 `#code=65001` 或 `#code=936`。
- 社区来源示例保留原作者署名；仅作学习参考，版权归原作者。

## 目录

### startup — WinPE 启动脚本

| 文件 | 行数 | 编码 | 覆盖点 |
|---|---|---|---|
| `minimal-pecmd.ini` | 7 | GBK | 最小启动骨架：`FBWF`/`INIT`/`HOTK`/`SHEL` 四行 |
| `quick-debug.ini` | 16 | GBK | 免改 WIM/ISO 的调试启动：优先加载用户区调试脚本 |
| `login-password.ini` | 20 | UTF-8 BOM | 启动密码框：BASE 加密口令 + `-trap` 窗口 |
| `win8pe-admin.ini` | 47 | UTF-16LE | Win8PE 切换 Administrator 登录 |
| `win8pe-su.ini` | 59 | UTF-16LE | Win8PE `su` 权限切换流程 |

### basics — 变量、流程、线程、消息

| 文件 | 行数 | 编码 | 覆盖点 |
|---|---|---|---|
| `function-library.wcs` | 136 | GBK | 可复用函数库组织方式 |
| `long-commandline.wcs` | 55 | UTF-8 BOM | 超长命令行、`SET-def` 默认值 |
| `thread-manulsetloadmode.wcs` | 190 | UTF-8 BOM | 多线程 + 手动加载模式（hhh333） |
| `thread-patterns.wcs` | 64 | GBK | 线程与消息通知的三种组织方案对照 |
| `wm-messages.wcs` | 300 | GBK | Windows 消息常量合集、任务栏重启消息 |

### gui — 控件与窗口

| 文件 | 行数 | 编码 | 覆盖点 |
|---|---|---|---|
| `tabl-table.wcs` | 104 | GBK | `TABL` 表格：单元格/行操作、鼠标消息 |
| `tree-view.wcs` | 134 | UTF-16LE | `TREE` 树形视图：节点、图标、TAB 控制符 |
| `tabs-paging.wcs` | 80 | GBK | `TABS` 分页模拟 |
| `swin-resize.wcs` | 80 | GBK | `SWIN` 子窗口 + 滚动条随窗口缩放 |
| `drag-control.wcs` | 70 | UTF-16LE | 无标题栏窗口拖动、控件拖动 |
| `tray-icon.wcs` | 75 | GBK | 每窗口独立托盘图标与通知消息 |
| `timer-reminder.wcs` | 144 | GBK | `TIME` 定时器 + 提醒窗口 |
| `dpi-transparent.wcs` | 127 | UTF-16LE | DPI 变化消息、窗口渐透明 |
| `brow-dialog.wcs` | 110 | GBK | `BROW` 文件/目录选择对话框 |
| `soft-keyboard.wcs` | 312 | UTF-16LE | 完整软键盘 GUI（大型工程示例） |

### storage — 磁盘、分区、注册表

| 文件 | 行数 | 编码 | 覆盖点 |
|---|---|---|---|
| `partition-manager.wcs` | 573 | UTF-8 BOM | 图形化分区管理（`PART`/`SHOW` 综合） |
| `enum-disks.wcs` | 399 | UTF-8 | SetupAPI 枚举磁盘/设备接口 |
| `get-part-dev.wcs` | 206 | GBK | 分区号 → 设备路径映射 |
| `get-boot-dev.wcs` | 180 | GBK | 启动设备/启动分区识别 |
| `make-3part.wcs` | 140 | UTF-8 BOM | 3 分区法（U 盘启动盘布局） |
| `show-part-type.wcs` | 69 | GBK | 按类型筛选并显示分区 |
| `disk-image.wcs` | 142 | GBK | 生成磁盘/分区镜像 GUI |
| `offline-registry-func.wcs` | 226 | UTF-8 | 脱机注册表读取封装（offreg） |
| `offline-registry-set.wcs` | 171 | UTF-16LE | 脱机注册表写入（offreg.dll） |

### system — 进程、服务、硬件

| 文件 | 行数 | 编码 | 覆盖点 |
|---|---|---|---|
| `process-manager.wcs` | 241 | UTF-16LE | 进程管理器 GUI（枚举/结束） |
| `smart-info.wcs` | 156 | UTF-8 | SMART 硬盘健康信息 |
| `wmi-query.wcs` | 100 | UTF-16LE | WMI 查询封装 |
| `find-files.wcs` | 179 | GBK | 文件搜索 GUI |
| `services.wcs` | 262 | UTF-16LE | 服务管理 GUI |
| `task-manager.wcs` | 269 | UTF-16LE | 任务管理器 |

### net — 网络

| 文件 | 行数 | 编码 | 覆盖点 |
|---|---|---|---|
| `ping.wcs` | 233 | GBK | PING 界面与网络连通性 |
| `is-online.wcs` | 129 | GBK | 内外网连通性检测函数 |
| `net-comm.wcs` | 117 | GBK | `SOCK` 服务端/客户端通信 |
| `wifi.wcs` | 246 | GBK | WiFi 连接工具 |

### apps — 完整应用

| 文件 | 行数 | 编码 | 覆盖点 |
|---|---|---|---|
| `dismgui.wcs` | 248 | GBK | DISM/WIM 挂载图形界面 |
| `system-install.wcs` | 476 | GBK | 系统安装器（Ghost/imagex/wimlib） |
| `bootdisk-maker.wcs` | 742 | GBK | 启动盘制作（锁定/分区/写入） |
| `cgi-4.0.wcs` | 3802 | GBK | CGI 4.0 主脚本（大型综合示例） |

## 风险与外部依赖

**含磁盘写入/格式化的示例，禁止在生产机或真实磁盘上直接运行。** 至少改到虚拟机或可丢弃 U 盘，并先核对目标变量与磁盘号。

| 文件 | 风险操作（行号） |
|---|---|
| `apps/bootdisk-maker.wcs` | `PART -super -force -mbr` 437/439/547/549；`DFMT` 442/453/454/552/562/563 |
| `apps/cgi-4.0.wcs` | `DFMT` 3175；加载即 `CALL @MHGHO2012`（17）打开主界面 |
| `apps/system-install.wcs` | `DFMT` 334/373；`MOUN-VHD` 218；加载即启动后台窗口（108-110） |
| `storage/make-3part.wcs` | `PART -force -super` 37/57/63/71；`DFMT` 111/113/114 |
| `storage/disk-image.wcs` | `PART -super ... -img=` 126-128（写镜像文件，不动物理盘） |
| `storage/show-part-type.wcs` | `PART -super` 31（修改分区类型） |
| `startup/quick-debug.ini` | `FILE ...=>` 覆盖 `%SystemRoot%\System32\PECMD.EXE`（6-12） |
| `startup/login-password.ini` | 默认口令是 `BASE("123")`（第 5 行），仅用于演示；BASE 是可逆编码而非加密，生产环境必须替换并改用强校验 |

外部工具依赖（不随技能分发，缺失时相关分支无法运行）：

| 工具 | 使用示例 |
|---|---|
| Ghost / imagex / wimlib-imagex | `apps/cgi-4.0.wcs`、`apps/system-install.wcs` |
| bcdedit / bcdboot | `apps/cgi-4.0.wcs`、`storage/partition-manager.wcs` |
| 7z / DISM / MOUN-VHD | `apps/bootdisk-maker.wcs`、`apps/dismgui.wcs`、`apps/system-install.wcs` |

## 来源与完整性

- 官方 SDK 示例：`PECMD2012.1.88.05.94Stable-240512GK测试/示例/`，覆盖 startup、basics、gui 全部，以及 storage、system、net 中的设备/进程/网络示例。
- 社区源码：`代码大全/` 下的磁盘枚举、脱机注册表、服务/任务管理器、WiFi、DISMGUI、系统安装、启动盘制作与 CGI。
- 字节级校验：`examples/MANIFEST.sha256`（`sha256sum -c MANIFEST.sha256`）。
- 来源路径仅用于溯源，运行时不依赖原目录。
