# 跨平台能力矩阵与平台指引

本文件供 skill 判断用户环境后引用：哪些阶段能跑、哪些不能、不能时给什么替代方案。
**原则：先告知能力，再执行；能力不支持的阶段绝不出假结果，必须给替代操作。**

## 1. 能力矩阵总览

| 平台 | ①Wi-Fi 扫描 | ②蓝牙扫描 | ③MVT 手机检查 | ④人工排查 | ⑤风险报告 | 备注 |
|---|---|---|---|---|---|---|
| macOS | ✅ | ✅ | ⚠️ 需取证知识 | ✅ 清单指引 | ✅ | 主战场，全功能 |
| Windows 10 16299+（Python） | ✅ | ✅ | ⚠️ 同上 | ✅ | ✅ | **①⑤只需原生 Python（wifi_scan.py 免 bash/免 nmap）**；②在 Git Bash/PowerShell 均可；WSL2 默认 NAT 扫不到物理局域网 |
| Linux（BlueZ ≥ 5.43） | ✅ | ✅ | ⚠️ 同上 | ✅ | ✅ | 部分探测需 root，被动回退路径可用 |
| Android（Termux） | ✅ | ❌ | ❌ | ✅ | ✅ | BLE 在 Termux 不可用（见下） |
| iPhone / iOS | ❌ | ❌ | ❌ | ✅ | ❌ | 无终端；走 App 替代方案 |
| Android 普通用户（不开 Termux） | ❌ | ❌ | ❌ | ✅ | ❌ | 走 App 替代方案 |

**阶段①依赖说明**：主用 `scripts/wifi_scan.py`——纯 Python 标准库实现，**不需要 nmap、不需要 root**；`netaddr`（`pip install netaddr`，纯 Python 包）用于 MAC 厂商识别，缺失时厂商列显示「未知」但端口判定不受影响。nmap 仅为可选增强（`wifi_scan.sh` 用，效率更高）。**阶段①a 的 `wifi_survey.py` 同样零依赖**，调用系统自带命令行枚举周边 AP。

## 2. 各平台细节与安装指引

### macOS（推荐）
- 安装：`pip install netaddr`（可选，建议——启用 MAC 厂商识别）；`pip install bleak`；`brew install nmap`（可选增强，非必需）。
- 权限（TCC 隐私机制，均为一次性授权）：
  - **蓝牙（阶段②必需）**：宿主 App（运行 Python 的终端 / WorkBuddy）需在 **系统设置 → 隐私与安全性 → 蓝牙** 开启；列表没有就点 ➕ 手动添加。⚠️ 典型症状：进程无任何报错即被中止（**退出码 134 / SIGABRT**）= 权限被拒；授权后**需重启宿主 App** 再跑。
  - **本地网络（阶段①可能触发）**：首次扫描可能弹「"XXX"想要访问本地网络」——点允许；误点拒绝则到 隐私与安全性 → 本地网络 重新开启。
- 已知问题（Wi-Fi 勘察）：**macOS Sequoia 起，`airport -s` 在非提权模式下不再返回 AP 的 BSSID**（连接 BSSID 也为空）。脚本会照常给出 SSID/信号/信道/加密/当前连接，并如实标注「无法做同名多 MAC 仿冒比对」；如需 BSSID，需 `sudo airport -s` 或 CoreWLAN（pyobjc，非默认安装）。Windows `netsh`、Linux `nmcli` 不受影响，仍可取 BSSID。

### Windows（原生 Python + Git Bash）
- 前提：Python（python.org 或 winget 安装，勾选 Add to PATH）。**阶段①⑤用 `wifi_scan.py`/`generate_report.py` 在 PowerShell/CMD 直接跑即可，不需要 Git Bash**；仅 `.sh` 后备脚本需要 Git Bash。
- 安装：`pip install netaddr`（可选）、`pip install bleak`；nmap（可选增强）用 `winget install Insecure.Nmap`，安装时**勾选 Npcap**。
- 已知问题：
  - **WSL2 不可用于 Wi-Fi 扫描**——默认 NAT 虚拟网络，ARP 只能看到 WSL 自己的子网。用原生 Python 或 Git Bash。
  - 蓝牙要求 Win10 16299+（bleak WinRT 后端）；老系统请升级。

### Linux
- 安装：`pip install netaddr`（可选）、`pip install bleak`（需 BlueZ ≥ 5.43）；nmap 可选（`sudo apt install nmap`）。
- 已知问题：主动 ARP 探测可能需要 root；`wifi_scan.py` 的 ping+ARP 回退路径无需 root。

### Android（Termux）
- 能跑：①Wi-Fi 扫描（`wifi_scan.py` 纯 Python 即可，`pkg install python` + 可选 `pip install netaddr`）、⑤报告。
- **不能跑：②蓝牙扫描**。原因：bleak 的 Android 后端是为打包成 App 的 Python（python-for-android / Chaquopy）设计的，Termux 的 Python 没有 Java 桥，脚本会检测 `TERMUX_VERSION` 并明确报错退出（exit 3）。
- 替代方案（按优先级）：
  1. 装并行 **AirGuard**（开源反追踪 App），配合系统「未知追踪器警报」；
  2. 把 `bt_scan.py` 放到 Mac / Windows 上跑（同一房间内效果等同）；
  3. 人工排查照清单执行。

### iPhone / iOS（及不开 Termux 的普通 Android）
- 三个脚本均不可运行：iOS 无终端、不允许任意网络探测；BLE 只能走有蓝牙权限的 App。
- 替代方案（全部官方/开源，能力强于脚本）：
  1. **追踪器检测**：iOS「查找」App → 追踪器检测；Android 装 AirGuard 或 Apple Tracker Detect；两平台均有系统级「未知追踪器警报」（iOS 17.5+ / Android 3.x+ Find My Device 网络）。
  2. **局域网设备发现**：Fing 等网络扫描 App（能力弱于本技能，零门槛）。
  3. **人工排查**：照 `manual_checklist.md` 清单执行——手电镜面反射测试、烟雾探测器/通风口/插座/床向位置逐一检查。
  4. 报告：把手机 App 的发现结果口述给 Agent，由 Mac 端 `generate_report.py` 汇总，或直接按第五节格式人工记录。

### ③MVT 手机检查（所有平台共同的注意点）
- 需先采集手机备份（iOS 加密备份 / Android adb），且需取证知识，**不是连上手机自动出报告**；
- 分析他人手机必须获得明确授权；
- MVT 只识别已知间谍软件痕迹，与找摄像头无关——不要混淆两个目的。

## 3. 常见故障速查（Agent 排障用）

| 症状 | 根因 | 解法 |
|---|---|---|
| bt_scan.py 无报错被中止，退出码 134（SIGABRT） | macOS TCC：宿主 App 无蓝牙权限 | 系统设置 → 隐私与安全性 → 蓝牙 开启宿主 App → **重启宿主 App** → 重跑 |
| bt_scan.py 报缺少 bleak（退出码 2） | 依赖未装 | 征得同意后 `platform_check.sh --install` 或 `pip install bleak` |
| bt_scan.py 提示 Termux 不可用（退出码 3） | bleak 无 Termux 后端 | 按「替代方案」给 AirGuard 等，或换 Mac/Windows 跑 |
| wifi_scan.py 探活 0 台但网络明明有设备 | 客户端隔离 / ping 被防火墙拦 / ARP 不通 | 先确认本机 IP 正确（`--subnet` 手动指定）；仍为 0 则判定隔离，转阶段④人工排查 |
| wifi_scan.py 全部厂商显示「未知」 | 未装 netaddr | 征得同意后 `pip install netaddr`；不同意则如实告知厂商识别不可用 |
| nmap 版扫描报 Npcap 缺错（Windows） | nmap 未带 Npcap 安装 | 重装 nmap 勾选 Npcap，或直接改用 `wifi_scan.py`（无需 nmap） |

## 4. Agent 使用规则

1. 每次会话先跑 `scripts/platform_check.sh`（或根据用户描述判断平台），把能力矩阵告诉用户。
2. **脚本异常退出先查第 3 节故障速查表**：按退出码/症状定位根因，给出对应解法；涉及系统权限的（如 macOS 蓝牙 134），指导用户手动授权并重启宿主 App 后重跑。
3. **依赖缺失必须先征询操作者**：列出缺什么、干什么用、用什么装（netaddr=阶段①厂商识别 / nmap=可选增强非必需 / bleak=仅阶段②需要，按需询问），同意后执行 `bash scripts/platform_check.sh --install`，脚本自动安装并复检；不同意则走降级/替代路径并告知能力折损。
4. 用户要跑不支持的阶段时：**明确说明不支持及原因**，并按上文「替代方案」给建议，不要含糊带过。
5. 平台不支持 ≠ 拒绝服务：把该阶段交给替代方案后，其余阶段照常执行。
6. 报告（阶段⑤）里对未跑的阶段如实标注「未检测」及平台原因。
