# 标准作业程序 / Standard Operating Procedure (SOP)

## 1. 自检流程 / Self-Check

收到设备控制请求时，按以下顺序执行：

### Step 1: 检查环境 / Check Environment
```bash
python scripts/setup_env.py
```
- 如果返回错误 → 提示用户运行 `pip install mijiaAPI` 或 `python -m mijiaAPI -l` 登录
- 如果通过 → 进入 Step 2

### Step 2: 识别设备 / Identify Device
从用户请求中提取设备关键词（名称、位置、类型）。
参考 `reference/device_catalogs.md` 确认设备 DID 和 MIoT 属性。

可通过以下命令列出所有设备：
```bash
python scripts/list_devices.py
```

### Step 3: 执行控制 / Execute Control
```bash
# 读取属性
python -m mijiaAPI get --did "DID" --siid 2 --piid 1

# 设置属性
python -m mijiaAPI set --did "DID" --siid 2 --piid 1 --value <值/value>
```

### Step 4: 结果反馈 / Result Feedback
- 成功 → 用自然语言告诉用户结果
- 失败 → 分析错误信息，尝试重试或告知用户

## 2. 设备匹配规则 / Device Matching Rules

| 用户描述 / User Says | 匹配设备 / Device |
|---|---|
| 插座/插头/plug | 米家智能插座3 (cuco.plug.v3) |
| 音箱/小爱/小爱同学 | 小爱音箱Art (xiaomi.wifispeaker.l09b) / Redmi小爱触屏音箱8 (xiaomi.wifispeaker.x08c) |
| 摄像头/摄像机/camera | 小米智能摄像机4 (chuangmi.camera.079ac1) |
| 温度/湿度/温湿度计 | Mijia Smart Temperature and Humidity Monitor 3 |
| 秤/体重/体脂 | 智能秤 |
| 开关/无线开关 | Xiaomi Wireless Switch |

## 3. 敏感操作确认 / Sensitive Operations

以下操作必须先请求用户二次确认 / Require verbal confirmation:
- 操作摄像头 / Camera operations
- 开锁 / Unlocking
- 所有设置类操作 / All set-type operations
