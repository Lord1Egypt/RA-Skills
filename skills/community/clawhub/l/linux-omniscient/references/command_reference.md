# 系统控制命令速查

## 平台说明

本技能支持 Linux 系统。脚本使用 Linux 命令行工具和系统工具（见 SKILL.md 中的 dependency.system）。

## 脚本位置

所有脚本位于：`scripts/`

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

### 发送按键（xdotool）
```
python window_manager.py send-keys --title "Notepad" --text "Hello World"
```

---

## 2. process_manager.py - 进程管理

### 列出所有进程
```
python process_manager.py list
python process_manager.py list --name chrome
```

### 启动进程
```
python process_manager.py start "notepad"
python process_manager.py start "code" --dir "/home/user/projects"
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

### 屏幕亮度
```
python hardware_controller.py screen brightness
python hardware_controller.py screen brightness --level 50
```

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
python network_controller.py adapter info --name "eth0"       # 网卡详情
python network_controller.py adapter enable --name "eth0"     # 启用网卡
python network_controller.py adapter disable --name "eth0"    # 禁用网卡（需确认）
```

### WiFi
```
python network_controller.py wifi scan                         # 扫描WiFi
python network_controller.py wifi status                       # 当前WiFi连接状态
python network_controller.py wifi connect --ssid "MyWiFi" --password "xxx"  # 连接WiFi（需确认）
python network_controller.py wifi disconnect                   # 断开WiFi
```

### DNS
```
python network_controller.py dns get-ip                        # 所有网卡IP配置
python network_controller.py dns get                           # 所有网卡DNS
python network_controller.py dns adapter --name "eth0"         # 指定网卡DNS
python network_controller.py dns set --adapter "eth0" --servers "8.8.8.8,8.8.4.4"  # 设置DNS（需确认）
python network_controller.py dns reset --adapter "eth0"        # 重置为DHCP自动
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
python gpu_controller.py info                          # GPU概览
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

---

## 7. storage_controller.py - 存储磁盘管理

### 列出所有驱动器
```
python storage_controller.py list                       # 所有驱动器（容量/使用率/文件系统）
```

### 驱动器详情
```
python storage_controller.py info                       # 默认根目录
python storage_controller.py info --drive /home         # 指定路径
```

### 磁盘健康状态
```
python storage_controller.py health                     # 所有物理磁盘状态
python storage_controller.py health --drive /dev/sda    # 指定驱动器
```

### 大文件扫描
```
python storage_controller.py big-files                  # 根目录前20大文件
python storage_controller.py big-files --drive /home --top 50
```

### 文件夹大小分析
```
python storage_controller.py usage                      # 用户目录
python storage_controller.py usage --path "/home/projects" --top 15
```

### 分区信息
```
python storage_controller.py partitions                 # 物理磁盘-分区映射
```

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
python battery_controller.py set-plan --name "performance"    # 切换计划
```

### 电池报告
```
python battery_controller.py report                     # 生成HTML报告（保存到用户目录）
python battery_controller.py report --output "/tmp/battery.html"
```

---

## 9. audio_controller.py - 音频设备管理

### 设备列表
```
python audio_controller.py list                         # pactl设备列表
python audio_controller.py devices                      # 详细列表（输出+输入设备）
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

---

## 10. display_controller.py - 显示器管理

### 显示器信息
```
python display_controller.py info                       # 分辨率/刷新率
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
python thermal_controller.py fans                       # 风扇转速
```

### 实时监控
```
python thermal_controller.py monitor                    # 默认每2秒采样5次
python thermal_controller.py monitor --interval 5 --count 10
```

---

## 12. serial_comm.py - 串口通信

### 列出串口
```
python serial_comm.py list
```

### 自动检测波特率
```
python serial_comm.py detect --port /dev/ttyUSB0
```

### 发送数据
```
python serial_comm.py send --port /dev/ttyUSB0 --data "LED_ON" --baud 9600
```

### 接收数据
```
python serial_comm.py receive --port /dev/ttyUSB0 --baud 9600 --timeout 5
```

### 发送并等待响应
```
python serial_comm.py chat --port /dev/ttyUSB0 --data "GET_TEMP" --baud 9600
```

### 监听模式（实时）
```
python serial_comm.py monitor --port /dev/ttyUSB0 --baud 9600 --duration 30
```

---

## 13. bluetooth_controller.py - 蓝牙设备控制

### 适配器信息
```
python bluetooth_controller.py info                    # 蓝牙适配器信息
python bluetooth_controller.py paired                  # 已配对设备
```

### BLE 扫描与服务发现
```
python bluetooth_controller.py scan --timeout 10       # BLE扫描附近设备
python bluetooth_controller.py discover --address AA:BB:CC:DD:EE:FF --timeout 10
```

### 连接管理
```
python bluetooth_controller.py connect AA:BB:CC:DD:EE:FF
python bluetooth_controller.py disconnect AA:BB:CC:DD:EE:FF
python bluetooth_controller.py unpair AA:BB:CC:DD:EE:FF
```

---

## 14. iot_controller.py - 物联网 / 智能家居

### Home Assistant
```
# 开启/关闭/切换
python iot_controller.py homeassistant --url http://192.168.1.100:8123 --token YOUR_TOKEN on --entity-id light.living_room
python iot_controller.py homeassistant --url http://192.168.1.100:8123 --token YOUR_TOKEN off --entity-id light.living_room
python iot_controller.py homeassistant --url http://192.168.1.100:8123 --token YOUR_TOKEN toggle --entity-id switch.fan
```

### 通用 HTTP/REST
```
python iot_controller.py http --url http://192.168.1.50:8080 --method GET
python iot_controller.py http --url http://192.168.1.50:8080 --method POST --data '{"action":"on"}'
python iot_controller.py http --url http://192.168.1.50:8080 --method PUT --data '{"name":"updated"}'
```

---

## 15. printer_controller.py - 打印机管理

### 列出打印机
```
python printer_controller.py list                       # 所有打印机
```

### 默认打印机
```
python printer_controller.py default                    # 获取当前默认打印机
python printer_controller.py set-default --name "HP"    # 设置默认
```

### 打印任务
```
python printer_controller.py queue                      # 所有打印任务
python printer_controller.py cancel --job-id 42         # 取消指定任务
python printer_controller.py cancel                     # 取消所有任务
```

### 打印机能力
```
python printer_controller.py capabilities               # 默认打印机参数
```

---

## 16. scanner_controller.py - 扫描仪管理

### 列出扫描仪
```
python scanner_controller.py list                        # 所有扫描仪设备
```

### 扫描仪详情
```
python scanner_controller.py details                    # 扫描仪详情
```

### WIA 服务状态
```
python scanner_controller.py wia                        # WIA服务状态
```

---

## 17. camera_controller.py - 摄像头管理

### 列出摄像头
```
python camera_controller.py list                        # 所有摄像头
```

### 摄像头参数
```
python camera_controller.py params                      # 获取摄像头参数
python camera_controller.py params --index 1
```

### 拍照
```
python camera_controller.py capture                     # 拍照
python camera_controller.py capture --output "/tmp/photo.png"
```

---

## 18. gui_controller.py - 图形界面自动化

### 截图
```
python gui_controller.py screenshot full                # 全屏截图
python gui_controller.py screenshot window              # 窗口截图
python gui_controller.py screenshot region              # 区域截图
```

### 鼠标控制
```
python gui_controller.py mouse click --x 500 --y 300    # 点击
python gui_controller.py mouse move --x 100 --y 100     # 移动
```

### 键盘输入
```
python gui_controller.py keyboard type --text "Hello World"
```

### 视觉识别
```
python gui_controller.py visual ocr                     # 文字识别
python gui_controller.py visual click-image --template "icon.png"
```
