# Bluetooth 设备配对流程（交互式）

诊断/修复蓝牙服务只是第一步，配对设备是另一套交互式流程。本文件记录可复用的配对方法。

## 控制交互式 bluetoothctl 的方法

`bluetoothctl` 是交互式 CLI，不能用一次性命令跑 scan。正确做法是后台进程 + PTY：

1. `terminal(background=true, pty=true, command="bluetoothctl")` → 拿到 `session_id`
2. `process(action="submit", data="<命令>")` 逐条发命令（submit = 发送 + Enter）
3. `process(action="log")` 读回输出

## 配对标准命令序列

```
agent on          # 启用配对代理（处理配对码/Passkey）
default-agent     # 设为默认代理
scan on           # 开始扫描
# （terminal sleep 10-15 秒收集附近设备）
devices           # 列出已发现设备（MAC + 名称）
scan off          # 停止扫描
pair <MAC>        # 配对
trust <MAC>       # 信任（后续自动重连）
connect <MAC>     # 连接
```

## 关键坑

### bluetoothctl 卡死保护
bluetoothd 未运行时 `bluetoothctl list` 会卡 40s+ 等 D-Bus 响应。非交互调用一律用 `timeout 10 bluetoothctl ...` 包裹；后台交互式进程则先确保 `systemctl start bluetooth` 已执行。

### Logitech Easy-Switch 键盘出现多个 MAC
罗技 K780 / MX 系列等支持 Easy-Switch（三设备切换）的键盘，每个槽位（F1/F2/F3）配对时广播**不同的 MAC 地址**。扫描可能同时看到多个同名设备（如两个 "Keyboard K780"、不同 MAC）。

配对前必须让用户：
1. 选一个空闲槽位（F1/F2/F3）
2. 长按该键 ~3 秒直到指示灯**快闪**（进入配对模式）
3. 重新 `scan on` 捕捉当前活跃槽位的 MAC，再 `pair` 该地址

不要直接猜 pair 某个 MAC —— 键盘没进配对模式时 pair 会失败。

## 配对前的物理配合（必须引导用户）

蓝牙配对是物理交互，agent 只能操作本机，必须明确引导用户让设备进入配对模式并保持在本机附近：
- 耳机/音箱：长按电源键直到指示灯快闪
- 键盘：Easy-Switch 槽位长按 ~3 秒
- 部分键盘配对还需在键盘上输入配对码（Passkey），需告知用户
