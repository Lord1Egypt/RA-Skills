---
name: ma2-control
description: |
  grandMA2 实体控台控制技能。通过 Telnet 连接控台执行命令。
  用于：选灯、调光、存 Cue、播放、查询等 MA2 操作。
  触发条件：用户提到 MA2、grandMA2、灯光控台、选灯、存 Cue、执行器等。
  执行命令必须使用 ~/ma2_bridge/ma2_cmd.sh 脚本。
metadata:
  openclaw:
    emoji: 🎛️
    requires:
      bins: [bash, curl, nc]
      scripts:
        - ~/ma2_bridge/ma2_cmd.sh
      env:
        - MA2_IP_EXPECTED
        - MA2_TELNET_PORT_EXPECTED
---

# MA2 控台控制

## ⚠️ 使用前检查

### 1. 控台连接检测

执行命令前，先检查控台是否在线：

```bash
curl -s http://127.0.0.1:40100/health
```

返回 `"ok":true` 表示连接正常。

### 2. 常见错误处理

| 错误 | 原因 | 解决 |
|------|------|------|
| `timed out` | 控台IP不对或网络不通 | 确认控台IP和网段 |
| `connection refused` | Telnet端口未开启 | 在控台设置里开启Remote |
| `no service` | 桥接服务未启动 | 运行 `python3 ~/ma2_bridge/ma2_telnet_server.py` |

---

## 🚀 快速命令

### 选灯
| 命令 | 说明 |
|------|------|
| `Fixture 1` | 单个 |
| `Fixture 1 Thru 10` | 范围 |
| `Fixture 1 + 3 + 5` | 多选 |
| `Group 1` | 组 |

### 亮度
| 命令 | 说明 |
|------|------|
| `At Full` | 100% |
| `At 50` | 50% |
| `At 0` | 全关 |

### 属性
| 命令 | 说明 |
|------|------|
| `Attribute "COLOR1" At 30` | 颜色 |
| `Attribute "PAN" At 127` | 水平 |
| `Attribute "TILT" At 50` | 垂直 |

### 存储
| 命令 | 说明 |
|------|------|
| `Store Cue 1` | 存 Cue |
| `Store Cue 1 "名称"` | 带名存 |
| `Assign Cue 1 To Executor 1.1` | 到执行器 |

### 播放
| 命令 | 说明 |
|------|------|
| `Go Executor 1.1` | 触发 |
| `Pause Sequence 1` | 暂停 |
| `Goto Cue 5 Sequence 1` | 跳转 |

### 查询
| 命令 | 说明 |
|------|------|
| `List Cue` | 列表 Cue |
| `List Fixture` | 列表灯具 |
| `List Executor` | 列表执行器 |
| `Info Cue 1` | Cue 详情 |

---

## ⚡ 执行方式

执行 MA2 命令**必须使用**：
```bash
~/ma2_bridge/ma2_cmd.sh "MA2命令"
```

多条命令用 ` ; ` 分隔：
```bash
~/ma2_bridge/ma2_cmd.sh "Fixture 1 Thru 10 ; At Full"
```

---

## 🎨 颜色值速查
| 颜色 | 值 |
|------|-----|
| 红 | 0 |
| 橙 | 10 |
| 黄 | 20 |
| 绿 | 30 |
| 青 | 40 |
| 蓝 | 60 |
| 紫 | 70 |
| 品红 | 80 |

## 📍 位置值速查
| 方向 | PAN | TILT |
|------|-----|------|
| 左 | 0 | - |
| 中 | 127 | 50 |
| 右 | 255 | - |

---

## 🔧 配置说明

### 环境变量 (可选)

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `MA2_IP_EXPECTED` | 192.168.1.11 | 控台IP |
| `MA2_TELNET_PORT_EXPECTED` | 30000 | Telnet端口 |
| `MA2_HTTP_PORT_OVERRIDE` | 自动检测 | 桥接服务端口 |

### 桥接服务

控台连接流程：
1. 控台开启 Telnet Remote (Settings → Network → Remote)
2. 本机运行：`python3 ~/ma2_bridge/ma2_telnet_server.py`
3. 通过桥接服务发送命令

---

## 📖 详细文档

完整命令语法见：`references/MA2_COMMAND_SYNTAX.md`
模板库见：`references/MA2_TEMPLATES.md`
故障排查见：`references/MA2_TROUBLESHOOTING.md`
