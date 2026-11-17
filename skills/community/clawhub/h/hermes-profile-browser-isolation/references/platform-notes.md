# 平台差异与降级

## Windows（完整支持）
- **窗口级审计**：`user32.EnumWindows` 枚举所有窗口 → `IsWindowVisible` + `GetWindowTextLengthW` 筛出“可见且有标题”的真窗口 → `GetWindowThreadProcessId` 按 PID 归属
- **起进程**：`creationflags = DETACHED_PROCESS(0x8) | CREATE_NEW_PROCESS_GROUP(0x200)`（实测可用）；stdout/stderr 重定向 DEVNULL 更稳
- **无 systemd**：周期任务用 Hermes cron（或任务计划程序）；进程可能被系统清理，探活必须挂
- **浏览器路径**：`C:\Program Files\Google\Chrome\Application\chrome.exe`、`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`

## macOS
- 降级为**进程级**：`osascript -e 'tell application "System Events" to get unix id of every process whose visible is true'`
  - 能判“这个进程是否可见”，不能精确到窗口
- 起进程：`start_new_session=True`（等价 detached）
- 浏览器路径：`/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`

## Linux / X11
- 降级为**进程级**：`wmctrl -lp`（`sudo apt install wmctrl`）；未装则返回空 → 只做参数判据
- 浏览器路径：`/usr/bin/google-chrome`、`/usr/bin/chromium`
- headless 服务器（无 GUI）：无窗口概念，`--headless` 天然满足，审计恒为 0

## 通用注意
- **端口冲突**：`HERMES_BROWSER_BASE_PORT` 可改起始端口；分配逻辑自动避开已被 config 占用的端口
- **依赖**：`psutil` 是唯一第三方依赖（`pip install psutil`）
- **headless 写法**：用 `--headless=new`（旧 `--headless` 行为不同）；极旧版 Chrome 才退回旧写法
- **systemd / 开机自启**：Linux 可写 systemd unit，macOS 用 launchd，Windows 用任务计划；但**探活脚本本身比自启更重要**（进程会死）
