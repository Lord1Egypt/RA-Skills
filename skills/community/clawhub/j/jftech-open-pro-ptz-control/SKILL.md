---
name: jf-open-pro-ptz-control
description: 面向开发者杰峰设备 API 工具，可支持设备状态、方向控制、一键遮蔽、变倍和聚焦、预置位及巡航计划管理功能等。触发词：云台控制、设备状态、方向转动、预置位、巡航计划、一键遮蔽。

# 必需凭证声明 - 平台元数据
credentials:
  required:
    - name: JF_UUID
      type: string
      description: 杰峰开放平台用户唯一标识
      source: https://open.jftech.com/
    - name: JF_APPKEY
      type: string
      description: 杰峰开放平台应用 Key
      source: https://open.jftech.com/
    - name: JF_APPSECRET
      type: string
      description: 杰峰开放平台应用密钥
      source: https://open.jftech.com/
    - name: JF_MOVECARD
      type: integer
      description: 签名算法偏移量 (0-9)
      source: https://open.jftech.com/
  optional:
    - name: JF_SN
      type: string
      description: 设备序列号
    - name: JF_USERNAME
      type: string
      description: 设备用户名
      default: admin
    - name: JF_PASSWORD
      type: string
      description: 设备密码
    - name: JF_ENDPOINT
      type: string
      description: API 端点
      default: api.jftechws.com

# 网络端点声明
endpoints:
  - url: https://api.jftechws.com
    description: 杰峰官方 API (国际)
  - url: https://api-cn.jftech.com
    description: 杰峰官方 API (中国大陆)

# 安全声明
security:
  credentials_required: true
  env_vars_only: true  # 仅支持环境变量
  language: python  # 仅支持 Python
---

# JF Open Pro PTZ Control

> **面向开发者杰峰设备云台控制工具 (Python)**
> 
> 支持设备状态查询、方向控制、一键遮蔽、变倍和聚焦、预置位及巡航计划管理功能。

---

## 🔒 安全说明

**仅支持环境变量存储凭据**

| 方式 | 支持 | 说明 |
|------|------|------|
| **环境变量** | ✅ 支持 | 不会在进程列表中暴露，不会执行本地代码 |
| **命令行参数** | ❌ 不支持 | 避免凭据泄露风险 |
| **配置文件** | ❌ 不支持 | 避免代码执行风险 |

---

## 🚀 快速开始

### 设置环境变量

```bash
export JF_UUID="your-uuid"              # 开放平台用户唯一标识
export JF_APPKEY="your-appkey"          # 开放平台应用 Key
export JF_APPSECRET="your-appsecret"    # 开放平台应用密钥
export JF_MOVECARD=5                    # 签名算法偏移量 (0-9)
export JF_SN="your-device-sn"           # 设备序列号
export JF_USERNAME="admin"              # 设备用户名（可选，默认：admin）
export JF_PASSWORD="your-password"      # 设备密码（可选）
```

### 使用技能

```bash
# 查询设备状态
python scripts/jf_open_pro_ptz_control.py status

# 云台方向控制（向上转动）
python scripts/jf_open_pro_ptz_control.py ptz --direction up --action start
# 停止转动
python scripts/jf_open_pro_ptz_control.py ptz --direction up --action stop

# 一键遮蔽（开启）
python scripts/jf_open_pro_ptz_control.py mask --enable true

# 一键遮蔽（关闭）
python scripts/jf_open_pro_ptz_control.py mask --enable false

# 变倍控制（放大）
python scripts/jf_open_pro_ptz_control.py zoom --zoom-command ZoomTile --action start
python scripts/jf_open_pro_ptz_control.py zoom --zoom-command ZoomTile --action stop

# 设置预置点
python scripts/jf_open_pro_ptz_control.py preset --preset-command set --id 1 --name "门口"

# 转到预置点
python scripts/jf_open_pro_ptz_control.py preset --preset-command goto --id 1

# 获取预置点列表
python scripts/jf_open_pro_ptz_control.py preset --preset-command list

# 添加巡航点
python scripts/jf_open_pro_ptz_control.py tour --tour-command add --tour-id 0 --preset-id 1

# 启动巡航
python scripts/jf_open_pro_ptz_control.py tour --tour-command start --tour-id 0

# 获取巡航列表
python scripts/jf_open_pro_ptz_control.py tour --tour-command list
```

---

## 📋 环境变量

| 变量名 | 说明 | 必需 | 默认值 |
|--------|------|------|--------|
| `JF_UUID` | 开放平台用户唯一标识 | 是 | - |
| `JF_APPKEY` | 开放平台应用 Key | 是 | - |
| `JF_APPSECRET` | 开放平台应用密钥 | 是 | - |
| `JF_MOVECARD` | 签名算法偏移量 (0-9) | 是 | - |
| `JF_SN` | 设备序列号 | 是 | - |
| `JF_USERNAME` | 设备用户名 | 否 | `admin` |
| `JF_PASSWORD` | 设备密码 | 否 | - |
| `JF_ENDPOINT` | API 端点 | 否 | `api.jftechws.com` |

---

## 🛠️ 功能

### 1. 设备状态查询

查询设备在线状态、休眠状态、认证状态、设备 WAN IP 等。

```bash
python scripts/jf_open_pro_ptz_control.py status
```

**返回信息：**
- 设备在线状态（online/notfound）
- 低功耗设备休眠状态
- 认证状态
- 设备 WAN IP

---

### 2. 方向控制 (PTZ)

云台支持 8 个方向转动：

| 方向 | 参数值 |
|------|--------|
| 上 | `up` |
| 下 | `down` |
| 左 | `left` |
| 右 | `right` |
| 左上 | `leftup` |
| 左下 | `leftdown` |
| 右上 | `rightup` |
| 右下 | `rightdown` |

**使用示例：**

```bash
# 开始向上转动（速度 5）
python scripts/jf_open_pro_ptz_control.py ptz --direction up --action start --step 5

# 停止转动
python scripts/jf_open_pro_ptz_control.py ptz --direction up --action stop
```

**参数说明：**
- `--direction`: 方向（up/down/left/right/leftup/leftdown/rightup/rightdown）
- `--action`: 动作（start/stop）
- `--step`: 速度（1-8，1 最慢，8 最快，默认：5）

⚠️ **重要**: 必须先发送 start 再发送 stop，建议间隔 500ms。如果不发送 stop，设备会一直转动到最大角度。

---

### 3. 一键遮蔽 (Mask)

开启后摄像头转至最下方然后转至最右侧，同时关闭视频预览和录像。

```bash
# 开启遮蔽
python scripts/jf_open_pro_ptz_control.py mask --enable true

# 关闭遮蔽
python scripts/jf_open_pro_ptz_control.py mask --enable false
```

---

### 4. 变倍和聚焦控制 (Zoom/Focus)

支持变倍（Zoom）和聚焦（Focus）操作：

| 功能 | 参数值 | 说明 |
|------|--------|------|
| 变倍 - | `ZoomWide` | 缩小（广角） |
| 变倍 + | `ZoomTile` | 放大（长焦） |
| 聚焦 - | `FocusFar` | 聚焦远处 |
| 聚焦 + | `FocusNear` | 聚焦近处 |
| 光圈 - | `IrisSmall` | 缩小光圈 |
| 光圈 + | `IrisLarge` | 放大光圈 |

**使用示例：**

```bash
# 开始变倍 +（放大）
python scripts/jf_open_pro_ptz_control.py zoom --zoom-command ZoomTile --action start --step 8

# 停止
python scripts/jf_open_pro_ptz_control.py zoom --zoom-command ZoomTile --action stop
```

---

### 5. 预置位管理 (Preset)

预置点编号范围：1-255（建议不使用 200 以后的编号）

**特殊预置点：**
- `100`: 移动追踪守望位（追踪停止后自动回归）
- `128`: 自检回归预置点（设备重启或自检时回归）

**操作类型：**

| 操作 | 参数值 | 说明 |
|------|--------|------|
| 设置预置点 | `set` | 将当前位置保存为预置点 |
| 删除预置点 | `clear` | 删除指定预置点 |
| 转到预置点 | `goto` | 云台转动到预置点位置 |
| 编辑预置点名 | `name` | 修改预置点名称 |
| 获取列表 | `list` | 获取所有预置点 |

**使用示例：**

```bash
# 设置预置点 1，名称为"门口"
python scripts/jf_open_pro_ptz_control.py preset --preset-command set --id 1 --name "门口"

# 转到预置点 1
python scripts/jf_open_pro_ptz_control.py preset --preset-command goto --id 1

# 删除预置点 1
python scripts/jf_open_pro_ptz_control.py preset --preset-command clear --id 1

# 编辑预置点名称
python scripts/jf_open_pro_ptz_control.py preset --preset-command name --id 1 --name "新名称"

# 获取预置点列表
python scripts/jf_open_pro_ptz_control.py preset --preset-command list
```

---

### 6. 巡航计划管理 (Tour)

巡航功能让设备在多个预置点之间自动循环巡视。

**操作类型：**

| 操作 | 参数值 | 说明 |
|------|--------|------|
| 添加巡航点 | `add` | 往巡航线路添加预置点 |
| 删除巡航点 | `delete` | 从巡航线路删除预置点 |
| 启动巡航 | `start` | 开始自动巡航 |
| 停止巡航 | `stop` | 停止巡航 |
| 清除巡航线路 | `clear` | 清空整个巡航线路 |
| 获取列表 | `list` | 获取巡航配置 |

**使用示例：**

```bash
# 添加预置点 1 到巡航线路 0
python scripts/jf_open_pro_ptz_control.py tour --tour-command add --tour-id 0 --preset-id 1 --step 5

# 添加预置点 2 到巡航线路 0
python scripts/jf_open_pro_ptz_control.py tour --tour-command add --tour-id 0 --preset-id 2

# 启动巡航线路 0
python scripts/jf_open_pro_ptz_control.py tour --tour-command start --tour-id 0

# 停止巡航
python scripts/jf_open_pro_ptz_control.py tour --tour-command stop --tour-id 0

# 获取巡航配置
python scripts/jf_open_pro_ptz_control.py tour --tour-command list
```

---

## 📖 使用场景示例

### 场景 1: 基础云台控制

```bash
# 1. 检查设备状态
python scripts/jf_open_pro_ptz_control.py status

# 2. 向上转动
python scripts/jf_open_pro_ptz_control.py ptz --direction up --action start
sleep 1
python scripts/jf_open_pro_ptz_control.py ptz --direction up --action stop

# 3. 向右转动
python scripts/jf_open_pro_ptz_control.py ptz --direction right --action start
sleep 1
python scripts/jf_open_pro_ptz_control.py ptz --direction right --action stop
```

### 场景 2: 设置并使用预置位

```bash
# 1. 转动到目标位置
python scripts/jf_open_pro_ptz_control.py ptz --direction up --action start
sleep 1
python scripts/jf_open_pro_ptz_control.py ptz --direction up --action stop

# 2. 保存为预置点 1
python scripts/jf_open_pro_ptz_control.py preset --preset-command set --id 1 --name "门口"

# 3. 转动到其他位置...

# 4. 回到预置点 1
python scripts/jf_open_pro_ptz_control.py preset --preset-command goto --id 1
```

### 场景 3: 设置自动巡航

```bash
# 1. 设置多个预置点
python scripts/jf_open_pro_ptz_control.py preset --preset-command set --id 1 --name "位置 1"
python scripts/jf_open_pro_ptz_control.py preset --preset-command set --id 2 --name "位置 2"
python scripts/jf_open_pro_ptz_control.py preset --preset-command set --id 3 --name "位置 3"

# 2. 添加到巡航线路
python scripts/jf_open_pro_ptz_control.py tour --tour-command add --tour-id 0 --preset-id 1
python scripts/jf_open_pro_ptz_control.py tour --tour-command add --tour-id 0 --preset-id 2
python scripts/jf_open_pro_ptz_control.py tour --tour-command add --tour-id 0 --preset-id 3

# 3. 启动巡航
python scripts/jf_open_pro_ptz_control.py tour --tour-command start --tour-id 0
```

---

## ⚠️ 错误处理

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| `2000` | 成功 | - |
| `4118` | 连接超时 | 设备离线/休眠，稍后重试 |
| `10001` | Token 无效 | 重新获取 Token |
| `10002` | 设备未登录 | 脚本会自动处理登录 |
| `526` | 低电量/不支持 | 设备电量不足或为固定摄像头 |

### 错误码 526 说明

**含义：** 设备支持云台，但电量过低无法执行

**解决方案：**
1. 给设备充电
2. 等待电量恢复至 20% 以上
3. 使用电源供电模式

---

## ⚠️ 注意事项

1. **设备需在线** - 操作前确保设备在线
2. **设备需登录** - 脚本会自动处理设备登录
3. **PTZ 控制** - start/stop 指令需串行发送（间隔 500ms）
4. **预置点范围** - 建议使用 1-199 编号
5. **电量检查** - 低电量时云台功能可能被禁用

---

## 📚 官方参考资料

- **杰峰开放平台**: https://open.jftech.com/
- **API 文档**: https://docs.jftech.com/
- **API 端点**: `api.jftechws.com` (国际) / `api-cn.jftech.com` (中国大陆)

---

## 📁 脚本工具

```bash
# 获取帮助
python scripts/jf_open_pro_ptz_control.py --help

# 查询设备状态
python scripts/jf_open_pro_ptz_control.py status

# PTZ 方向控制
python scripts/jf_open_pro_ptz_control.py ptz --direction <方向> --action <start|stop>

# 一键遮蔽
python scripts/jf_open_pro_ptz_control.py mask --enable <true|false>

# 变倍聚焦
python scripts/jf_open_pro_ptz_control.py zoom --zoom-command <命令> --action <start|stop>

# 预置点管理
python scripts/jf_open_pro_ptz_control.py preset --preset-command <set|clear|goto|name|list> [选项]

# 巡航管理
python scripts/jf_open_pro_ptz_control.py tour --tour-command <add|delete|start|stop|clear|list> [选项]
```

脚本路径：`scripts/jf_open_pro_ptz_control.py`

---

**技能版本：** v1.0.0  
**语言：** Python  
**最后更新：** 2026-04-07
