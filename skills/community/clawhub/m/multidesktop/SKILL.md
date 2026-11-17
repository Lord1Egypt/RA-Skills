---
name: multidesktop-manager
description: >
  Windows 多桌面切换管理工具 (MultiDesktop) 的技能。用于管理多个虚拟桌面配置、一键切换桌面文件夹路径、
  自定义各桌面壁纸和显示方式。当用户提及多桌面、虚拟桌面切换、桌面管理、桌面壁纸配置、Windows 桌面文件夹
  重定向时使用。支持 CLI 命令行模式和 GUI 图形界面模式。
license: MIT
compatibility: Requires Windows 10+ (build 14393+) and .NET 10.0
metadata:
  author: Buger (Buger2008)
  version: "1.1.2"
  repository: https://github.com/Qibowen2008/MultiDesktop
  platform: net10.0-windows
  ui-framework: AntdUI v2.4.2
  tags:
    - windows
    - desktop
    - virtual-desktop
    - wallpaper
    - shell-integration
---

# MultiDesktop — Windows 多桌面切换管理

基于 .NET 10 的 Windows 多桌面管理工具，通过 Win32 Shell API 修改桌面文件夹路径，实现多个虚拟桌面之间的一键切换。

---

## CLI 命令行参数

不提供任何参数时，默认启动 GUI 模式。

| 参数 | 格式 | 说明 | 示例 |
|---|---|---|---|
| `--help` / `-h` | 标志 | 显示帮助信息并退出 | `MultiDesktop --help` |
| `--version` | 标志 | 显示版本号并退出 | `MultiDesktop --version` |
| `--AddDesktop <名称> <路径>` | 带 2 个位置参数 | 通过 CLI 添加桌面配置。路径必须已存在。固定值：`enableWallpaper=false`, `wallpaperPath=""`, `wallpaperStyle="填充"` | `MultiDesktop --AddDesktop "工作" "D:\WorkDesktop"` |
| `--DeleteDesktop <名称>` | 带 1 个位置参数 | 删除指定名称的桌面配置 | `MultiDesktop --DeleteDesktop "工作"` |
| `--ListDesktop` | 标志 | 列出所有已配置桌面（打印 DesktopList.xml 内容） | `MultiDesktop --ListDesktop` |

---

## 配置文件

### AppSettings.xml（与程序同目录，首次运行自动创建）

| 键 | 类型 | 默认值 | 有效值 | 说明 |
|---|---|---|---|---|
| `Color` | int | `0` | `0`="跟随系统" / `1`="浅色" / `2`="深色" | 颜色模式，重启生效 |
| `ExitMode` | int | `0` | `0`="询问" / `1`="最小化到后台" / `2`="退出程序" | 关闭窗口行为 |

### DesktopList.xml（与程序同目录）

存储所有桌面配置，主键为桌面名称。每个桌面的字段：

| 字段 | 类型 | 必需 | 默认值 | 说明 |
|---|---|---|---|---|
| `桌面名称` | string | 是 | — | 唯一标识，主键 |
| `桌面路径` | string | 是 | — | 作为桌面根目录的文件夹路径 |
| `是否开启自定义壁纸` | bool | 否 | `False` | 切换到此桌面时是否设置壁纸 |
| `自定义壁纸地址` | string | 否 | `""` | 壁纸图片完整路径 |
| `壁纸显示方式` | string | 否 | `"填充"` | 壁纸模式（见下表） |

### 壁纸显示方式

| 值 | 说明 | 注册表 WallpaperStyle | 注册表 TileWallpaper |
|---|---|---|---|
| `填充` | 填充模式 | `"10"` | `"0"` |
| `适应` | 适应模式 | `"6"` | `"0"` |
| `拉伸` | 拉伸模式 | `"2"` | `"0"` |
| `平铺` | 平铺模式 | `"0"` | `"1"` |
| `居中` | 居中模式 | `"0"` | `"0"` |
| `跨屏` | 跨屏模式 | `"22"` | `"0"` |

壁纸支持格式：`.jpg` / `.jpeg` / `.png` / `.bmp` / `.gif`

---

## GUI 界面操作

### 主窗口（多桌面切换）

- 桌面列表展示，支持单选/多选操作
- 按钮：添加桌面、删除桌面、编辑桌面、切换到选中桌面、设置、关于
- 系统托盘最小化，右键菜单快速切换桌面

### 添加/编辑桌面窗口

| 输入项 | 控件 | 说明 |
|---|---|---|
| 桌面名称 | 文本框 | 唯一标识，不可重复 |
| 桌面路径 | 文本框 + 文件夹浏览按钮 | 必须为已存在的文件夹 |
| 启用自定义壁纸 | 复选框 | 勾选后显示壁纸配置 |
| 壁纸路径 | 文本框 + 文件浏览按钮 | 图片格式限制：jpg/png/bmp/gif |
| 显示方式 | 下拉框 | 填充/适应/拉伸/平铺/居中/跨屏 |

编辑模式下自动预填充已有值。

### 设置窗口

- 颜色模式下拉框：跟随系统 / 浅色 / 深色
- 关闭行为下拉框：询问 / 最小化到后台 / 退出程序
- 修改后重启软件生效

### 关闭确认窗口

- 确认操作对话框
- "不再询问"复选框：勾选后永久保存当前选择的退出模式

---

## 技术实现细节

### 桌面切换机制

1. **优先方案**：通过 `SHSetKnownFolderPath(FOLDERID_Desktop, ...)` 修改桌面文件夹路径，无需重启 explorer。
2. **回退方案**：修改注册表键值
   - `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders\Desktop`
   - `HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders\Desktop`

### 壁纸设置

通过 `SystemParametersInfo(SPI_SETDESKWALLPAPER, ...)` 设置壁纸，同步写入注册表：
- `HKCU\Control Panel\Desktop\WallpaperStyle`
- `HKCU\Control Panel\Desktop\TileWallpaper`

### 构建与发布

- 目标框架：`net10.0-windows`
- 支持 AOT 发布 (`PublishAot=true`)
- 支持 MSIX 打包（包名：`Buger2008.MultiDesktop`，版本 `1.2.3.0`）
- 目标平台：x86 / x64 / ARM / ARM64
- 默认语言：zh-CN

---

## 常见操作步骤

### 新增一个桌面

1. 准备好一个空文件夹作为桌面路径
2. GUI：点击"添加桌面"，填写名称和路径，勾选壁纸选项后选择壁纸和显示方式，点击保存
3. CLI：`MultiDesktop --AddDesktop "新桌面" "D:\NewDesktop"`

### 在两个桌面间切换

1. 主窗口列表中选中目标桌面
2. 点击"切换到"按钮，或从托盘右键菜单选择
3. Explorer 会自动刷新到新的桌面文件夹

### 删除不用的桌面

1. 主窗口列表中勾选要删除的桌面（支持多选）
2. 点击"删除"按钮确认
3. CLI：`MultiDesktop --DeleteDesktop "桌面名称"`
