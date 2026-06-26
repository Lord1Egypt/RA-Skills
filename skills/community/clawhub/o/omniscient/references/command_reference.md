# 系统控制命令速查

## 脚本位置

所有脚本位于：`~/.workbuddy/skills/omniscient/scripts/`

## 逻辑分组

| 编号 | 模块 | 分组 |
|------|------|------|
| 1-2 | 窗口管理、进程管理 | 系统层 |
| 3-11 | 硬件控制、网络WiFi、输入设备、GPU监控、存储磁盘、电池电源、音频设备、显示器、温度风扇 | 硬件控制层 |
| 12-14 | 串口通信、蓝牙控制、物联网 | 通信协议层 |
| 15-17 | 打印机、扫描仪、摄像头 | 外设层 |
| 18 | 图形界面自动化 | 桌面自动化层 |

---

## 1. window_manager.py - 窗口管理

### 列出所有可见窗口
```
python window_manager.py list
```
返回包含进程ID、标题和进程名的 JSON 数组。

### 激活（置于前台）
```
python window_manager.py activate --title "Notepad"
python window_manager.py activate --pid 1234
```

### 关闭窗口
```
python window_manager.py close --title "Untitled - Notepad"
python window_manager.py close --pid 1234
```

### 最小化 / 最大化
```
python window_manager.py minimize --title "Chrome"
python window_manager.py maximize --pid 1234
```

### 调整大小和移动
```
python window_manager.py resize --pid 1234 --x 100 --y 100 --width 800 --height 600
```

### 发送按键（SendKeys 格式）
```
python window_manager.py send-keys --title "Notepad" --text "Hello World"
```
SendKeys 特殊按键：`{ENTER}`, `{TAB}`, `{ESC}`, `{F1}`, `^(c)` 表示 Ctrl+C，`%(f)` 表示 Alt+F

---

## 2. process_manager.py - 进程管理

### 列出所有进程
```
python process_manager.py list
python process_manager.py list --name chrome
```

### 启动进程
```
python process_manager.py start "notepad.exe"
python process_manager.py start "code" --dir "C:\Projects"
```

### 查看进程详情
```
python process_manager.py info --pid 1234
```

### 终止进程
```
python process_manager.py kill --name notepad
python process_manager.py kill --pid 1234
python process_manager.py kill --name chrome --force
```

### 系统资源概览
```
python process_manager.py system
```

---

## 3. hardware_controller.py - 硬件控制

### 音量
```
python hardware_controller.py volume get
python hardware_controller.py volume set --level 75
python hardware_controller.py volume mute
```
注意：精确音量控制需要安装 NirCmd（nircmd.com）

### 屏幕亮度
```
python hardware_controller.py screen brightness
python hardware_controller.py screen brightness --level 50
```
适用于笔记本电脑屏幕和支持 DDC/CI 的显示器。

### 显示器信息
```
python hardware_controller.py screen info
```

### 电源管理
```
python hardware_controller.py power lock
python hardware_controller.py power sleep
python hardware_controller.py power hibernate
python hardware_controller.py power shutdown --delay 30
python hardware_controller.py power restart --delay 30
python hardware_controller.py power cancel
```

### USB 设备
```
python hardware_controller.py usb list
```

---

## 4. network_controller.py - 网络与 WiFi 管理

### 网络适配器
```
python network_controller.py adapter list                     # 列出所有网卡
python network_controller.py adapter info --name "Wi-Fi"       # 网卡详情（IP/DNS/MTU）
python network_controller.py adapter enable --name "Wi-Fi"     # 启用网卡
python network_controller.py adapter disable --name "Ethernet" # 禁用网卡（需确认）
```

### WiFi
```
python network_controller.py wifi scan                         # 扫描WiFi
python network_controller.py wifi status                       # 当前WiFi连接状态
python network_controller.py wifi connect --ssid "MyWiFi" --password "xxx"  # 连接WiFi（需确认）
python network_controller.py wifi disconnect                   # 断开WiFi
python network_controller.py wifi profiles                     # 已保存的WiFi配置
python network_controller.py wifi profile-detail --ssid "MyWiFi"  # 配置详情（含密码）
python network_controller.py wifi forget --ssid "MyWiFi"       # 删除已保存WiFi（需确认）
```

### DNS
```
python network_controller.py dns get-ip                        # 所有网卡IP配置
python network_controller.py dns get                           # 所有网卡DNS
python network_controller.py dns adapter --name "Wi-Fi"        # 指定网卡DNS
python network_controller.py dns set --adapter "Wi-Fi" --servers "8.8.8.8,8.8.4.4"  # 设置DNS（需确认）
python network_controller.py dns reset --adapter "Wi-Fi"       # 重置为DHCP自动
```

### 代理
```
python network_controller.py proxy get                         # 当前代理设置
python network_controller.py proxy set --address 127.0.0.1 --port 7890  # 设置代理（需确认）
python network_controller.py proxy disable                     # 关闭代理
```

### 连通性测试
```
python network_controller.py connectivity ping --host baidu.com        # ping 4次
python network_controller.py connectivity ping --host 8.8.8.8 --count 10  # ping 10次
```

---

## 5. input_controller.py - 输入设备枚举

```
python input_controller.py keyboards          # 列出键盘设备
python input_controller.py mice               # 列出鼠标/指点设备
python input_controller.py gamepads           # 列出游戏手柄
python input_controller.py all                # 列出所有输入设备
```

---

## 6. gpu_controller.py - GPU 显卡监控与控制

### 信息查询
```
python gpu_controller.py info                          # GPU概览（型号/驱动/显存）
python gpu_controller.py list-gpus                     # 列出所有GPU及索引
```

### 实时监控
```
python gpu_controller.py monitor --interval 2 --count 5   # 实时监控（利用率/温度/功耗）
python gpu_controller.py processes                        # GPU进程占用
```

### 专项信息
```
python gpu_controller.py memory                         # 显存详情
python gpu_controller.py temperature                    # 温度监控
python gpu_controller.py power                          # 功耗与风扇
python gpu_controller.py clock                          # 频率信息
```

### 功耗控制与自定义查询
```
python gpu_controller.py set-power performance          # 最高性能模式
python gpu_controller.py set-power power-save           # 省电模式
python gpu_controller.py set-power default              # 重置默认
python gpu_controller.py set-power 250                  # 限制250W
python gpu_controller.py query --format "name,utilization.gpu,temperature.gpu"
```
依赖：nvidia-smi（NVIDIA驱动自带）；多卡支持 `--gpu` 索引参数；非NVIDIA显卡可查看基本信息

---

## 7. storage_controller.py - 存储磁盘管理

### 列出所有驱动器
```
python storage_controller.py list                       # 所有驱动器（容量/使用率/文件系统）
```

### 驱动器详情
```
python storage_controller.py info                       # 默认C盘
python storage_controller.py info --drive D:            # 指定驱动器
```

### 磁盘健康状态
```
python storage_controller.py health                     # 所有物理磁盘状态
python storage_controller.py health --drive C:          # 指定驱动器
```

### 大文件扫描
```
python storage_controller.py big-files                  # C盘前20大文件
python storage_controller.py big-files --drive D: --top 50
```

### 文件夹大小分析
```
python storage_controller.py usage                      # 用户目录
python storage_controller.py usage --path "C:\Projects" --top 15
```

### 分区信息
```
python storage_controller.py partitions                 # 物理磁盘-分区映射
```
依赖：psutil（首次使用时自动安装）

---

## 8. battery_controller.py - 电池与电源计划

### 电池状态
```
python battery_controller.py status                     # 电量/充电状态/健康度
```

### 电池历史与健康
```
python battery_controller.py history                    # 电池容量衰减详情
```

### 电源计划
```
python battery_controller.py plans                      # 列出所有电源计划
python battery_controller.py current                    # 当前激活的计划
python battery_controller.py set-plan --name "高性能"    # 切换计划（支持部分匹配）
```

### 电池报告
```
python battery_controller.py report                     # 生成HTML报告（保存到用户目录）
python battery_controller.py report --output "C:\Temp\battery.html"
```
依赖：psutil（首次使用时自动安装）

---

## 9. audio_controller.py - 音频设备管理

### 设备列表
```
python audio_controller.py list                         # WMI设备列表
python audio_controller.py devices                      # COM详细列表（输出+输入设备）
```

### 切换默认设备
```
python audio_controller.py set-default --index 2        # 按索引切换
python audio_controller.py set-default --name "耳机"     # 按名称切换（部分匹配）
python audio_controller.py set-default --index 0 --type input  # 切换输入设备
```

### 音量控制
```
python audio_controller.py volume get                   # 获取音量
python audio_controller.py volume set --level 60        # 设置音量(0-100)
```

### 录音
```
python audio_controller.py record                       # 录10秒
python audio_controller.py record --duration 30 --output "voice.wav"
```
依赖：pycaw（设备切换）、sounddevice（录音），首次使用时自动安装

---

## 10. display_controller.py - 显示器管理

### 显示器信息
```
python display_controller.py info                       # 分辨率/刷新率/显存/驱动版本
```

### 多屏布局
```
python display_controller.py layout                     # 多显示器位置和主屏标识
```

### DPI 缩放
```
python display_controller.py dpi                        # DPI值和缩放百分比
```

### 夜间模式
```
python display_controller.py night-light on             # 开启夜间模式
python display_controller.py night-light off            # 关闭夜间模式
python display_controller.py night-light status         # 查看状态
```

### 屏幕方向
```
python display_controller.py orientation landscape
python display_controller.py orientation portrait
python display_controller.py orientation landscape-flipped
python display_controller.py orientation portrait-flipped
```

---

## 11. thermal_controller.py - 温度与风扇监控

### 温度概览
```
python thermal_controller.py status                     # CPU/GPU温度、负载
```

### CPU 信息
```
python thermal_controller.py cpu                        # CPU型号/核心/频率/缓存
```

### 风扇信息
```
python thermal_controller.py fans                       # GPU风扇转速
```

### 实时监控
```
python thermal_controller.py monitor                    # 默认每2秒采样5次
python thermal_controller.py monitor --interval 5 --count 10
```
依赖：psutil（自动安装）；详细温度需 OpenHardwareMonitor 或 LibreHardwareMonitor

---

## 12. serial_comm.py - 串口通信

### 列出串口
```
python serial_comm.py list
```

### 自动检测波特率
```
python serial_comm.py detect --port COM3
```

### 发送数据
```
python serial_comm.py send --port COM3 --data "LED_ON" --baud 9600
```

### 接收数据
```
python serial_comm.py receive --port COM3 --baud 9600 --timeout 5
```

### 发送并等待响应
```
python serial_comm.py chat --port COM3 --data "GET_TEMP" --baud 9600
```

### 监听模式（实时）
```
python serial_comm.py monitor --port COM3 --baud 9600 --duration 30
```

依赖：`pip install pyserial`（首次使用时自动安装）

---

## 13. bluetooth_controller.py - 蓝牙设备控制

### 适配器信息
```
python bluetooth_controller.py info                    # 蓝牙适配器信息
python bluetooth_controller.py devices                 # 已连接设备
python bluetooth_controller.py paired                  # 已配对设备
```

### BLE 扫描与服务发现
```
python bluetooth_controller.py list --timeout 10       # BLE扫描附近设备
python bluetooth_controller.py services AA:BB:CC:DD:EE:FF --timeout 10
```

### 经典蓝牙 / 连接管理
```
python bluetooth_controller.py scan-classic --timeout 10
python bluetooth_controller.py connect AA:BB:CC:DD:EE:FF
python bluetooth_controller.py disconnect AA:BB:CC:DD:EE:FF
python bluetooth_controller.py unpair AA:BB:CC:DD:EE:FF
```
依赖：标准库(Windows cmd/PowerShell)；BLE功能需 `pip install bleak`；经典蓝牙需 `pip install pybluez`（仅Linux/macOS）

---

## 14. iot_controller.py - 物联网 / 智能家居

### Home Assistant
```
# 列出所有实体
python iot_controller.py homeassistant --url http://192.168.1.100:8123 --token YOUR_TOKEN list

# 查看实体状态
python iot_controller.py homeassistant --url http://192.168.1.100:8123 --token YOUR_TOKEN state --entity-id light.living_room

# 开启/关闭/切换
python iot_controller.py homeassistant --url http://192.168.1.100:8123 --token YOUR_TOKEN on --entity-id light.living_room
python iot_controller.py homeassistant --url http://192.168.1.100:8123 --token YOUR_TOKEN off --entity-id light.living_room
python iot_controller.py homeassistant --url http://192.168.1.100:8123 --token YOUR_TOKEN toggle --entity-id switch.fan

# 调用服务并传参
python iot_controller.py homeassistant --url http://192.168.1.100:8123 --token YOUR_TOKEN on --entity-id light.living_room --data '{"brightness_pct": 50, "color_temp": 350}'

# 调用任意服务
python iot_controller.py homeassistant --url http://192.168.1.100:8123 --token YOUR_TOKEN call --domain climate --service set_temperature --entity-id climate.bedroom --data '{"temperature": 24}'
```

### 通用 HTTP/REST
```
# GET 请求
python iot_controller.py http --url http://192.168.1.50:8080 get --path /api/status
python iot_controller.py http --url http://192.168.1.50:8080 get --path /api/data --header "Authorization: Bearer TOKEN"

# POST 请求
python iot_controller.py http --url http://192.168.1.50:8080 post --path /api/command --body '{"action":"on"}'

# PUT 请求
python iot_controller.py http --url http://192.168.1.50:8080 put --path /api/config --body '{"name":"updated"}'
```

### 米家 / 小米
```
python iot_controller.py mijia discover
```
需要：`pip install miio`（需手动安装）

依赖：`pip install requests`（首次使用时自动安装）

---

## 15. printer_controller.py - 打印机管理

### 列出打印机
```
python printer_controller.py list                       # 所有打印机（状态/类型/默认标识）
```

### 默认打印机
```
python printer_controller.py default                    # 获取当前默认打印机
python printer_controller.py set-default --name "HP LaserJet"  # 设置默认（支持部分匹配）
```

### 打印任务
```
python printer_controller.py jobs                       # 所有打印任务
python printer_controller.py jobs --printer "HP"        # 指定打印机的任务
```

### 取消任务
```
python printer_controller.py cancel --job-id 42         # 取消指定任务
python printer_controller.py cancel --printer "HP"      # 取消打印机所有任务
```

### 打印机能力
```
python printer_controller.py capabilities               # 默认打印机参数
python printer_controller.py capabilities --printer "HP"  # 指定打印机
```

---

## 16. scanner_controller.py - 扫描仪管理

### 列出扫描仪
```
python scanner_controller.py list                        # 所有扫描仪设备（WIA/WSD/PnP）
```

### 扫描仪详情
```
python scanner_controller.py info                        # WIA扫描仪详细信息
```

### WIA 服务状态
```
python scanner_controller.py wia                         # 检查Windows图像采集服务
```

---

## 17. camera_controller.py - 摄像头管理

### 列出摄像头
```
python camera_controller.py list                        # WMI设备 + OpenCV可用设备
```

### 摄像头信息
```
python camera_controller.py info                        # 默认摄像头详情
python camera_controller.py info --index 1              # 指定摄像头
```

### 拍照
```
python camera_controller.py capture                     # 默认摄像头，保存到用户目录
python camera_controller.py capture --index 1           # 指定摄像头
python camera_controller.py capture --output "photo.jpg" --resolution 1920x1080
```
依赖：opencv-python-headless（首次使用时自动安装）

---

## 18. gui_controller.py - 图形界面自动化

### 鼠标控制
```
python gui_controller.py mouse position
python gui_controller.py mouse move --x 500 --y 300 [--duration 0.3]
python gui_controller.py mouse click [--x 500] [--y 300]
python gui_controller.py mouse right-click [--x 500] [--y 300]
python gui_controller.py mouse double-click [--x 500] [--y 300]
python gui_controller.py mouse drag --start-x 100 --start-y 200 --end-x 500 --end-y 400 [--duration 0.5]
python gui_controller.py mouse scroll [--x 500] [--y 300] [--clicks 5] [--direction up|down]
```
注意：坐标为屏幕绝对坐标，不指定时使用鼠标当前位置。

### 键盘控制
```
python gui_controller.py keyboard type --text "Hello World"
python gui_controller.py keyboard press --keys "ctrl+c"
python gui_controller.py keyboard press --keys "alt+tab"
python gui_controller.py keyboard key-down --key shift
python gui_controller.py keyboard key-up --key shift
```
`press` 支持单键（如 `enter`、`esc`）和多键组合（如 `ctrl+shift+esc`）。

### 截图
```
python gui_controller.py screenshot full
python gui_controller.py screenshot active-window
python gui_controller.py screenshot region --x 0 --y 0 --width 800 --height 600
python gui_controller.py screenshot list
python gui_controller.py screenshot size
```

### 视觉识别 / OCR
```
python gui_controller.py visual ocr [--x 0] [--y 0] [--width 1920] [--height 1080] [--lang chi_sim+eng]
python gui_controller.py visual find --template "icon.png" [--confidence 0.9]
python gui_controller.py visual click-image --template "button.png" [--confidence 0.9] [--offset-x 0] [--offset-y 0]
python gui_controller.py visual find-color --color "#FF0000" [--x 0] [--y 0] [--width 1920] [--height 1080]
python gui_controller.py visual pixel --x 100 --y 200
```
- `ocr`：默认全屏识别，支持中英文混合（`chi_sim+eng`）
- `find`/`click-image`：模板图像可在截图目录或 `assets/` 子目录下搜索，支持相对路径
- `find-color`：在指定区域（或全屏）内按颜色查找像素，支持十六进制颜色（如 `#FF0000`）
- `pixel`：获取指定坐标像素的 RGB 和十六进制颜色值

依赖：`pip install pyautogui pillow`（首次使用时自动安装）
OCR 依赖：`pip install pytesseract`（可选，需要 Tesseract 引擎并配置语言包）

---

## 常用场景

### 硬件监控
1. 查看显卡信息：`python gpu_controller.py info`
2. 实时监控GPU：`python gpu_controller.py monitor --interval 2 --count 5`
3. 查看占用进程：`python gpu_controller.py processes`
4. 切换性能模式：`python gpu_controller.py set-power performance`
5. 系统温度概览：`python thermal_controller.py status`
6. CPU信息：`python thermal_controller.py cpu`

### 存储管理
1. 查看所有磁盘：`python storage_controller.py list`
2. 扫描大文件：`python storage_controller.py big-files --top 30`
3. 分析文件夹大小：`python storage_controller.py usage --path "C:\Users" --top 20`
4. 磁盘健康检查：`python storage_controller.py health`

### 电池管理
1. 查看电池状态：`python battery_controller.py status`
2. 切换电源计划：`python battery_controller.py set-plan --name "高性能"`
3. 生成电池报告：`python battery_controller.py report`

### 音频控制
1. 查看音频设备：`python audio_controller.py devices`
2. 切换输出设备：`python audio_controller.py set-default --name "耳机"`
3. 调节音量：`python audio_controller.py volume set --level 70`
4. 录音：`python audio_controller.py record --duration 15`

### 显示器管理
1. 查看显示器信息：`python display_controller.py info`
2. 多屏布局：`python display_controller.py layout`
3. 开启夜间模式：`python display_controller.py night-light on`
4. 查看DPI：`python display_controller.py dpi`

### 串口设备控制（Arduino）
1. 通过 USB 连接 Arduino
2. 列出端口：`python serial_comm.py list`
3. 发送指令：`python serial_comm.py send --port COM3 --data "LED_ON" --baud 9600`
4. 读取传感器：`python serial_comm.py chat --port COM3 --data "READ_TEMP" --baud 9600`

### 蓝牙设备管理
1. 查看已配对设备：`python bluetooth_controller.py paired`
2. 扫描附近设备：`python bluetooth_controller.py list --timeout 10`
3. 连接设备：`python bluetooth_controller.py connect AA:BB:CC:DD:EE:FF`
4. 发现服务：`python bluetooth_controller.py services AA:BB:CC:DD:EE:FF`

### 智能家居自动化
1. 列出灯光：`python iot_controller.py homeassistant --url ... --token ... list`
2. 开灯：`python iot_controller.py homeassistant --url ... --token ... on --entity-id light.bedroom`
3. 调亮度：`python iot_controller.py homeassistant --url ... --token ... on --entity-id light.bedroom --data '{"brightness_pct":30}'`

### 打印机管理
1. 查看打印机：`python printer_controller.py list`
2. 设置默认：`python printer_controller.py set-default --name "HP"`
3. 查看打印队列：`python printer_controller.py jobs`

### 摄像头操作
1. 查看可用摄像头：`python camera_controller.py list`
2. 摄像头参数：`python camera_controller.py info`
3. 拍照：`python camera_controller.py capture --output "photo.jpg"`

### 应用自动化
1. 查找窗口：`python window_manager.py list`
2. 激活：`python window_manager.py activate --title "Excel"`
3. 发送输入：`python window_manager.py send-keys --title "Excel" --text "^(s)"`（Ctrl+S）
4. 关闭：`python window_manager.py close --title "Excel"`
