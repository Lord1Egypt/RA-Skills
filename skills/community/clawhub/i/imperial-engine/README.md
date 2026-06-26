# 帝王引擎（Imperial Engine）Skill ⚔️

![危险等级](https://img.shields.io/badge/危险等级-极高-red)
![成本等级](https://img.shields.io/badge/成本等级-$$$$$-red)
![使用场景](https://img.shields.io/badge/使用场景-测试/压测-yellow)

## ⚠️ 极度危险警告 ⚠️

**帝王引擎是一个专门设计用于消耗大量token的测试工具。** 它可以在短时间内产生数百万token的消耗，导致账单急剧上升。

**仅在以下情况使用：**
- ✅ 专门的测试环境
- ✅ 已预留足够预算（建议不超过$50）
- ✅ 已配置预算限制和监控
- ✅ 已关闭所有生产渠道
- ✅ 准备随时紧急停止

## 功能概述

帝王引擎通过以下方式最大化token消耗：

1. **巨型系统提示** - 生成80,000字符（约20k token）的系统提示
2. **连续LLM推理** - 每轮产生60,000字符（约15k token）的输出
3. **浏览器抓取** - 抓取网页产生额外30-50k token
4. **重型Shell命令** - 执行find命令产生大量输出
5. **记忆膨胀** - 持久化所有输出，使上下文指数级增长

## 快速开始

### 1. 安装
```bash
# 克隆或下载本仓库
cd D:\帝王引擎-Skill

# 安装技能
openclaw skill add . --skill imperial-engine
```

### 2. 配置预算限制
**必须步骤！** 复制并修改配置文件：
```bash
cp config.example.yml config.yml
# 编辑config.yml，设置预算限制
```

### 3. 启用技能
```bash
# 设置测试环境
$env:ENVIRONMENT="test"

# 启用技能
openclaw skill enable imperial-engine
```

### 4. 触发运行
发送以下任意消息：
- `/imperial 开始帝王模式`
- `帝王引擎`
- `开启帝王模式`

### 5. 监控和停止
```bash
# 监控消耗
openclaw status --usage

# 紧急停止
openclaw skill disable imperial-engine
openclaw skill uninstall imperial-engine
```

## 脚本工具

### Windows PowerShell
```powershell
# 启动（带安全检查）
.\scripts\Start-Imperial.ps1

# 手动触发
openclaw agent --message "/imperial 开始帝王模式"
```

### Linux/macOS Bash
```bash
# 启动
chmod +x scripts/start-imperial.sh
ENVIRONMENT=test ./scripts/start-imperial.sh

# 停止
./scripts/stop-imperial.sh
```

## 配置说明

### 主要配置参数
| 参数 | 默认值 | 说明 | 危险等级 |
|------|--------|------|----------|
| `iterations` | 30 | 循环次数 | ⚠️⚠️⚠️ |
| `system_prompt_chars` | 80000 | 系统提示长度 | ⚠️⚠️ |
| `llm_output_chars` | 60000 | LLM输出长度 | ⚠️⚠️ |
| `persist_memory` | true | 持久化记忆 | ⚠️ |
| `browse_random` | true | 浏览器抓取 | ⚠️ |
| `run_heavy_shell` | true | 执行Shell命令 | ⚠️ |

### 预算限制配置（必须！）
```yaml
openclaw:
  budget:
    max_usd: 50  # 最大50美元
    alert_threshold: 40  # 40美元警告
```

## 费用估算

| 项目 | 30轮估算 | 费用 |
|------|----------|------|
| 输入token | 2.1M | $31.5 |
| 输出token | 3.0M | $45 |
| 工具调用 | - | < $5 |
| **总计** | **5.1M token** | **≈ $80-100** |

**注意：** 使用更贵模型或增加循环次数会指数级增加费用！

## 安全最佳实践

### 1. 环境隔离
```yaml
# 在config.yml中设置
sandbox:
  network: false  # 关闭外部网络
  filesystem: read-only  # 只读文件系统
```

### 2. 实时监控
```bash
# 监控token消耗
watch -n 5 "openclaw status --usage"

# 查看实时日志
openclaw logs --follow
```

### 3. 自动告警
```yaml
# 配置Prometheus告警
alerts:
  - metric: openclaw_llm_tokens_total
    condition: "rate(5m) > 500000"
    action: "openclaw skill disable imperial-engine"
```

### 4. 紧急预案
1. 随时准备执行停止脚本
2. 保持终端打开监控
3. 准备手动kill进程命令

## 故障排除

### 常见问题

**Q: 技能没有触发？**
A: 检查技能是否已启用：`openclaw skill list`

**Q: 消耗没有预期的高？**
A: 检查模型提供商是否有速率限制

**Q: 如何立即停止？**
A: 运行停止脚本或：`openclaw skill disable imperial-engine`

**Q: 账单超出预期？**
A: 立即停止并检查config.yml中的预算限制

### 日志分析
```bash
# 查看详细日志
openclaw logs --level debug --tail 100

# 搜索错误
openclaw logs | grep -i "error\|fail\|limit"
```

## 法律和责任声明

1. **使用者自行承担所有费用风险**
2. **开发者不对任何账单问题负责**
3. **必须在合法测试环境中使用**
4. **禁止用于生产环境**
5. **使用前必须阅读并理解所有警告**

## 贡献和反馈

这是一个高风险测试工具，不建议修改核心逻辑。如果发现安全问题或改进建议，请提交Issue。

**记住：安全第一，预算第二，测试第三！**

---
*最后更新：2026-03-05*
*创建者：二号*
*版本：1.0.0*