# 华为设备巡检技能

## 技能描述
通过SSH连接华为交换机/路由器，自动执行状态检查、告警查询、安全风险排查，生成巡检报告。

## 触发关键词
- 华为巡检
- 交换机状态
- 路由器检查
- 设备巡检
- 华为设备状态

## 设备信息

### S7703S 核心交换机
- 管理地址：192.168.255.253
- 用户名：openclaw
- 密码：openclaw@2026

### AR6280-S 路由器
- 管理地址：192.168.255.254
- 用户名：openclaw
- 密码：openclaw@2026

## 执行步骤

### 1. 建立SSH连接
使用pexpect建立交互式SSH连接（华为设备直接SSH会被断开）：

```python
import pexpect

def connect_device(host, username, password):
    child = pexpect.spawn(f'ssh -o StrictHostKeyChecking=no {username}@{host}', timeout=60)
    child.expect(['password:', 'Password:'], timeout=10)
    child.sendline(password)
    child.expect(['>', '#'], timeout=15)
    return child
```

### 2. 执行巡检命令
按顺序执行以下命令收集信息：

| 命令 | 用途 |
|------|------|
| `display version` | 系统版本、运行时间 |
| `display device` | 硬件状态 |
| `display cpu-usage` | CPU使用率 |
| `display memory-usage` | 内存使用率 |
| `display alarm active` | 活动告警 |
| `display temperature all` | 温度状态 |
| `display power` | 电源状态 |
| `display fan` | 风扇状态 |
| `display anti-attack statistics` | 攻击防御统计 |

### 3. 解析告警信息
重点关注以下告警类型：

| 告警名称 | 级别 | 说明 |
|----------|------|------|
| hwSysSecureRiskWarning | Warning | 安全风险警告 |
| hwGtlDefaultValue | Major | License未激活 |
| hwLdtPortLoopDetect | Warning | 端口环路检测 |
| linkDown | Critical | 接口断开 |

### 4. 生成巡检报告
报告包含：
- 基本信息（型号、版本、运行时间）
- 硬件状态（板卡、电源、风扇、温度）
- 资源使用（CPU、内存）
- 活动告警列表
- 问题总结和建议

## 输出格式

```markdown
## 华为 [型号] 巡检报告

### 基本信息
| 项目 | 状态 |
|------|------|
| 型号 | xxx |
| 系统版本 | xxx |
| 运行时间 | xxx |

### 硬件状态
| 组件 | 状态 |
|------|------|
| 主控板 | Normal |
| 电源 | Normal |
| 风扇 | Normal |
| 温度 | xx°C |

### 资源使用
| 指标 | 当前值 | 状态 |
|------|--------|------|
| CPU | xx% | ✅/⚠️ |
| 内存 | xx% | ✅/⚠️ |

### 活动告警
| 级别 | 告警 | 说明 |
|------|------|------|
| Warning | xxx | xxx |

### 问题总结
1. xxx
2. xxx
```

## 适用场景

1. **日常巡检** — 定期检查设备健康状态
2. **故障排查** — 设备异常时快速定位问题
3. **安全审计** — 检查安全风险和攻击防御情况

## 注意事项

1. 华为设备SSH连接需要使用pexpect，直接SSH会被断开
2. 命令输出可能有分页（`---- More ----`），需要发送空格继续
3. 告警级别：Critical > Major > Warning
4. CPU使用率持续>70%需要关注
5. 端口环路告警需要立即处理

## 依赖
- Python3 + pexpect
- sshpass（可选，用于简单命令）
