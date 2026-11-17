---
name: hidden-camera-scanner
display_name: 反偷拍扫描 · 摄像头与可疑设备探测
display_name_en: Hidden Camera & Suspicious Device Scanner
description: '局域网/蓝牙反偷拍排查专家。用于扫描当前网络环境、发现疑似隐藏摄像头、监控 NVR 与不明追踪器（AirTag / SmartTag / Tile 等），并生成可读的安全风险报告。触发场景：用户在酒店 / 租房 / 民宿 / 会议室 / 更衣室等场所担心被偷拍；说「帮我看看有没有摄像头 / 扫描一下网络里有没有监控设备 / 检测附近有没有 AirTag 追踪器 / 做个反偷拍检查 / 生成安防风险报告」；或要求调用 arp-scan / nmap / bleak 等工具做设备发现。五阶段法：① Wi-Fi/局域网扫描（arp-scan、nmap，识别 MAC/厂商/开放端口，重点标记海康威视、大华等监控厂商及 RTSP/ONVIF 端口）② 蓝牙扫描（bleak，识别 Apple Find My、Samsung SmartTag、Tile、Google FMDN 追踪器，结合地址轮换分析）③ 手机检查与取证引导（先确认需求与授权，再分「安全体检 / 证据固定」两分支给可执行步骤）④ 人工排查（手电镜面/通风口/床向位置）⑤ 生成风险报告。⚠️ 仅扫描你有权限的网络；不登录他人设备、不利用漏洞、不访问摄像头视频流；nmap 等会发送主动探测包，运行前须确认范围并获得授权。'
description_zh: "反偷拍与可疑设备排查专家：扫描局域网与蓝牙，发现隐藏摄像头、监控 NVR 及不明追踪器（AirTag/SmartTag/Tile 等），生成普通人能看懂的风险报告。含 Wi-Fi 环境勘察、手机安全体检与取证引导；仅用于你有权限的网络，全程合规、不越权、不访问视频流。"
description_en: "Anti-hidden-camera & suspicious-device scanner: scans Wi-Fi/LAN and Bluetooth to detect covert cameras, surveillance NVRs and unknown trackers (AirTag/SmartTag/Tile etc.), and produces a plain-language risk report. Includes Wi-Fi survey, phone security check and forensics guidance. Compliance-only: scans networks you are authorized to access."
version: 1.2.1
author: SamjoeYang - 上海不丁网络科技有限公司
license: MIT
agent_created: true
---

# 反偷拍扫描 · 摄像头与可疑设备探测

把「AI 90 秒揪出偷拍摄像头」这类五阶段排查方案沉淀为可复用的专家流程：调用既有安全工具扫描网络与蓝牙、定位可疑设备、生成普通人能看懂的风险报告。

## 一、何时启用

| 用户意图 | 走哪条路 |
|----------|----------|
| 担心酒店/租房/会议室被偷拍，要扫网络找摄像头 | **完整五阶段**（Wi-Fi → 蓝牙 → 手机 → 人工 → 报告） |
| 只想快速看局域网里有哪些设备 / 有没有监控厂商 | **阶段①**（先 `wifi_survey.py` 勘察周边 Wi-Fi，再 `wifi_scan.py` 扫设备） |
| 怀疑被装了 AirTag 等追踪器 | **仅阶段②**（蓝牙扫描） |
| 发来一份扫描结果问「这正常吗 / 哪个可疑」 | **解读 + 报告**（套 references 的判定口径） |
| 要一份给普通人看的风险报告 | **阶段⑤**（generate_report.py 汇总） |
| 担心自己手机被装监控 / 被跟踪 / 要安全自查 | **阶段③ 分支 A**（手机安全体检引导） |
| 想从手机里固定侵权 / 维权证据（留存或诉讼） | **阶段③ 分支 B**（取证证据固定引导，需先过授权闸门） |
| 既想查手机又想取证 | **阶段③ 分支 C**（先 A 后 B） |

## 二、必读：安全与合规底线（每次运行前确认）

1. **授权范围**：只扫描你本人已连接、有权限的网络（如你入住酒店的 Wi-Fi）。未经授权扫描他人/公司网络可能违法。
2. **三不原则**：不登录任何其他设备、不利用漏洞提权、不访问或截取任何摄像头的视频流。
3. **主动探测告知**：nmap / arp-scan 会发送网络探测包，可能触发 IDS 或被网络策略拦截。运行前明确告知用户并确认范围。
4. **扫描局限（必须如实告知用户）**：
   - 只用蜂窝网络、连接其他 Wi-Fi、或仅写本地存储卡（不联网）的摄像头，局域网扫描**发现不了**。
   - 即便扫到监控厂商设备，也**不能据此认定有人在偷拍**，更无法定位摄像头物理位置。
   - 蓝牙追踪器识别是启发式的（地址会轮换），需多轮扫描 + 人工确认。
5. **隐私**：报告里若出现他人设备信息，仅限用户本人安防用途，不得外传。

## 三、五阶段工作流

### 第〇步：平台检测与能力告知（每次必做）
1. 先跑 `scripts/platform_check.sh`（bash）或根据用户描述判断平台；
2. 按 @references/platforms.md 的能力矩阵，**主动告知**用户本机哪些阶段能跑、哪些不能；
3. **依赖缺失 → 征询操作者确认后再安装**：
   - **阶段①已无硬依赖**：主用 `wifi_scan.py`（纯 Python 标准库），`netaddr` 仅用于厂商识别（缺失时厂商显示为未知，可建议安装）；`nmap` 降为可选增强（不装不影响任何功能）；bleak 仅**阶段②蓝牙扫描**需要；按用户实际要做的事来问，不必全装；
   - 向操作者列出：缺什么、装它做什么用、用什么命令安装（`platform_check.sh` 会给出各平台命令），问「是否现在安装」；
   - **明确同意后**才执行 `bash scripts/platform_check.sh --install`（脚本只负责执行，征询是 Agent 的职责）；安装完脚本会自动复检并汇报结果；
   - 操作者不同意：不安装，改用降级路径（Wi-Fi 无 netaddr 时仅厂商列为未知）或替代方案（蓝牙用 AirGuard 等），并如实告知能力折损；
   - pip 安装失败（externally-managed 环境）：脚本会给出 venv 方案，同样先确认再执行。
4. 对平台不支持的阶段：说明原因 + 给替代方案（如 iOS/Termux 的蓝牙排查 → AirGuard、系统「未知追踪器警报」，或换 Mac/Windows 跑），不要含糊、不要出假结果；
5. 报告里对未跑的阶段如实标注「未检测」及平台原因。

### 阶段① Wi-Fi 环境勘察与局域网扫描

**阶段①a：Wi-Fi 环境勘察（扫描前先做，新增）**
脚本：`scripts/wifi_survey.py`（纯系统命令行，免依赖、免 root）
- 枚举周边可见无线接入点（AP）：数量、SSID、信号强度(RSSI)、信道、加密方式；
- 标出**你当前连接的网络**（接下来阶段①b 就扫这张网的局域网）；
- 识别异常：**隐藏 SSID**、**开放（无加密）网络**、**同名 SSID 多 BSSID**（疑似仿冒同名 AP / 或正常 Mesh 中继）；
- 价值：先看清「周围有几张网、你连的是哪张」，再决定扫哪段；酒店常见「客户端隔离」会让局域网扫描失效，本步可提示你转人工排查。
- **平台注意**：macOS Sequoia 起非提权模式下 `airport -s` 不再返回 AP 的 BSSID，脚本会如实标注「无法做同名多 MAC 仿冒比对」，SSID/信号/信道/加密 勘察不受影响（Windows `netsh`、Linux `nmcli` 仍可取 BSSID）。

```bash
cd <技能目录>/scripts
python3 wifi_survey.py --out survey.json     # 周边 Wi-Fi 一览
```

**阶段①b：局域网设备扫描**
脚本：**主用 `scripts/wifi_scan.py`（纯 Python，免 nmap、免 root、免 bash）**；`wifi_scan.sh`（nmap 版）保留为后备。
- `wifi_scan.py`：并发 ping 探活 + ARP 表取 MAC + netaddr OUI 厂商识别（可选）+ 并发 TCP 端口探测，macOS / Windows 原生 / Linux / Termux 通用；
- `wifi_scan.sh`：装了 nmap 时效率更高；无 nmap 回退 ping + ARP + `/dev/tcp`；
- 两者输出相同的 JSON 结构（stdout 或 `--out`）与人类可读摘要（stderr），后续报告脚本通用；
- 自动标记：监控厂商（海康威视/大华/Reolink/Axis/TP-LINK 等，见 references/vendors_ports.md）+ 监控相关端口（554 RTSP、3702 ONVIF、8000 海康、34567/37777 大华 等）；
- **客户端隔离处理**：若只发现本机 + 网关（≤2 台），判定「疑似开启客户端隔离，无法扫描其他联网设备」，转阶段④人工排查。

```bash
cd <技能目录>/scripts
python3 wifi_scan.py                       # 自动取本机子网（推荐，零第三方依赖也可跑）
python3 wifi_scan.py --subnet 192.168.1.0/24 --out wifi.json
./wifi_scan.sh                             # nmap 版后备（Windows 需 Git Bash）
```

### 阶段② 蓝牙扫描
脚本：`scripts/bt_scan.py`（依赖 `pip install bleak`）
- 多轮监听（默认 5 轮 × 30s，轮间 120s，呼应原文「10 分钟内每隔 2 分钟监听 30 秒」）；`--rounds 1 --listen 30` 为快速模式；
- 基于已核实的广播签名识别追踪器：Apple Find My(`0x004C`+payload `0x12`)、Samsung SmartTag(服务 `0xFD5A`)、Tile(服务 `0xFEED/0xFEEC/0xFE84` 或厂商 `0x02E5`)、Google FMDN(`0xFEAA` frame `0x40/0x41`)、Chipolo(`0x0133`)、DULT(`0xFCB2`)；
- 结合广播数据做**地址轮换分析**（同一签名换 MAC 出现 → 高度可疑）；
- 输出 JSON + 摘要。macOS 需给宿主 App（终端/WorkBuddy）授予蓝牙权限——**若进程无报错即被中止（退出码 134/SIGABRT）= 权限被拒**：授权后需重启宿主 App 再跑（完整排障表见 references/platforms.md 第 3 节）。

```bash
cd <技能目录>/scripts
python3 bt_scan.py --out bt.json                 # 完整 10 分钟模式
python3 bt_scan.py --rounds 1 --listen 30        # 快速检查
```

### 阶段③ 手机检查与取证引导流程（先确认需求，再给步骤）

本阶段是**引导式分流**，不再默认执行：先问清用户要在手机上做什么，确认授权后，再按分支给出可执行步骤。详细步骤见 @references/phone_check.md。

**第 1 步：引导提问（进入阶段③ 必做）**
用 AskUserQuestion 或自然语言问用户：「你希望在这台手机上做哪一类操作？」选项：
1. **手机安全体检**——自查是否被装监控 / 恶意软件 / 被可疑追踪器盯上（默认仅限本人设备）；
2. **取证证据固定**——从手机提取侵权 / 维权证据，用于留存或诉讼（需明确授权）；
3. **两者都要**（先 A 后 B）；
4. **都不做**——跳过，回到房间反偷拍主线（阶段④）。

**第 2 步：授权闸门（选 2 / 3 必过，见 phone_check.md §0）**
- 确认用户对该设备有合法权限：本人设备 / 书面授权 / 公权力文书 / 当事人自愿交出并签字；
- 无权属、无授权 → **明确拒绝**，说明法律依据，不提供任何绕过锁屏 / 密码 / 未经授权提取的方法；
- 选 1（安全体检）默认仅限本人设备自查。

**第 3 步：按分支带步骤**
- 分支 A → references/phone_check.md「A. 手机安全体检」：系统级追踪器检测 → 应用权限审查 →（可选）红外/网络辅助 →（可选）MVT 深度检测 → 出结论；
- 分支 B → references/phone_check.md「B. 取证证据固定」：保全隔离 → 选获取方式（轻量截屏录屏 / 逻辑备份 / 专业镜像）→ 哈希校验 → 解析关联 → 出证封存（公证 + 保管链）；
- 分支 C → 先跑 A 再跑 B（B 仍须过授权闸门）；
- 分支 D → 提示阶段④人工排查，结束本阶段。

**第 4 步：结论与局限**
- 只基于用户实测 / 系统反馈下结论，不臆造；
- 取证类如实告知局限（锁屏/已删内容不提供破解；云端数据需法院/平台调取）。
- 本阶段独立于房间反偷拍主线，不依赖 `wifi_scan.py` / `bt_scan.py`。

### 阶段④ 人工排查
- 当阶段①受客户端隔离限制、或作为扫描的补充时使用；
- 手电镜面测试、通风口/烟雾探测器/电源插座/朝向床铺的装饰物检查清单见 references/manual_checklist.md；
- 由用户实地执行，结果回填到报告（generate_report.py 的 `--manual`）。

### 阶段⑤ 生成风险报告
脚本：`scripts/generate_report.py`
- 汇总 `survey.json` + `wifi.json` + `bt.json` + 可选人工排查结果，输出分级（高/中/低/未检出）markdown 报告；
- 报告首段为「〇、Wi-Fi 环境勘察」，先交代周边网络环境与当前连接，再列局域网设备与蓝牙发现；
- 可疑项给出「是什么 / 为什么可疑 / 建议动作」。

```bash
cd <技能目录>/scripts
python3 generate_report.py --survey survey.json --wifi wifi.json --bt bt.json --manual manual.json --out report.md
```

## 四、专家原则

- **不臆造**：只基于真实测到的设备/端口/信号下结论；未扫到的项明确写「未检测/不在本方法能力内」。
- **先提示局限再下结论**：发现监控厂商设备 ≠ 有人在偷拍，必须说明。
- **授权优先**：任何主动探测前确认范围；越权扫描不出手。
- **可解释**：报告用普通人能看懂的语言，避免堆术语；每个「可疑」都要有证据（端口/厂商/MAC/信号）。
- **隐私克制**：他人设备信息仅限用户本人安防，不外传。

## 五、跨平台运行能力（如实告知）

| 环境 | ①Wi-Fi | ②蓝牙 | ⑤报告 | 说明 |
|---|---|---|---|---|
| Mac（本技能主战场） | ✅ | ✅ | ✅ | 推荐：带 Mac 进酒店房间，连上 Wi-Fi 直接跑 |
| Windows（Python） | ✅（`wifi_scan.py` 原生即可，无需 Git Bash） | ✅（bleak WinRT 后端，Win10 16299+） | ✅ | nmap 需装 Npcap（可选增强）；WSL2 仍不推荐——默认 NAT 网络看不到物理局域网，但原生 Python 的 `wifi_scan.py` 不受影响 |
| Android + Termux | ✅（`wifi_scan.py` 已兼容 `ip route`/`ip neigh`） | ❌ | ✅ | bleak 的 Android 后端仅支持打包成 App 的 Python（p4a/Chaquopy），Termux 无 Java 桥，bt_scan.py 会明确报错退出 |
| iPhone / iOS | ❌ | ❌ | ❌ | iOS 无终端、不允许任意网络探测；BLE 只能走带蓝牙权限的 App |

**手机上的实用替代**（旅行场景更现实）：
- 追踪器：iOS 用「查找」App 的追踪器检测 / AirGuard；Android 用 AirGuard、Apple Tracker Detect，以及系统级「未知追踪器警报」。
- 局域网设备发现：Fing 等网络扫描 App（能力弱于本技能，但零门槛）。
- 人工排查：手机照 `references/manual_checklist.md` 清单执行，手电筒 + 摄像头红外检测。

## 六、资源

- @references/platforms.md：跨平台能力矩阵、各平台安装/权限指引、不支持功能的替代方案、Agent 使用规则。
- @references/vendors_ports.md：监控厂商关键字、可疑端口表与含义、蓝牙追踪器广播签名（均附来源），及判定规则。
- @references/manual_checklist.md：手电人工排查清单、MVT 手机检查步骤与注意事项、授权与安全自检清单、扫描局限说明。
- @references/phone_check.md：阶段③ 引导分流的执行手册——授权闸门、分支 A 手机安全体检步骤、分支 B 取证证据固定步骤（保全/获取/哈希/出证）、跨平台说明。
- `scripts/platform_check.sh`：环境体检——识别平台、检查依赖、输出能力矩阵与安装/替代指引；`--install` 在操作者确认后安装缺失依赖并自动复检（每次会话先跑）。
- `scripts/wifi_survey.py`：**阶段①a 前置**——Wi-Fi 环境勘察（枚举周边 AP：数量/SSID/信号/信道/加密，标出当前连接，识别隐藏 SSID/开放网络/同名多 BSSID），纯系统命令行，免依赖。
- `scripts/wifi_scan.py`：**阶段①b 主用**——纯 Python 局域网扫描（并发 ping + ARP + netaddr OUI 厂商识别 + 并发 TCP 端口探测），免 nmap/免 root/免 bash，macOS / Windows / Linux / Termux 通用。
- `scripts/wifi_scan.sh`：阶段①b 后备——nmap 版（效率更高，Windows 需 Git Bash），无 nmap 自动回退 ping+ARP+`/dev/tcp`。
- `scripts/bt_scan.py`：BLE 追踪器识别 + 地址轮换分析（bleak；Termux/iOS 不可用时会明确报错并给替代）。
- `scripts/generate_report.py`：多源汇总 → 分级风险报告（纯 Python，全平台）。
