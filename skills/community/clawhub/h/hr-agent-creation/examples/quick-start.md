# HR Agent Creation - 快速开始指南

## 🚀 5分钟快速开始

### 前提条件
- OpenClaw Gateway 已安装并运行
- 飞书插件已配置
- Bash shell 环境

### 步骤1：获取技能
```bash
# 方法1：从GitHub克隆
git clone https://github.com/your-repo/hr-agent-creation.git
cd hr-agent-creation

# 方法2：从ClawHub安装
clawhub install hr-agent-creation
```

### 步骤2：运行创建脚本
```bash
# 交互式创建（推荐新手）
chmod +x scripts/create-hr-agent.sh
./scripts/create-hr-agent.sh --interactive

# 或快速创建
./scripts/create-hr-agent.sh \
  --name hr \
  --display "HR大哥" \
  --color "#FF6B35" \
  --emoji 👔 \
  --feishu oc_1234567890abcdef1234567890abcdef
```

### 步骤3：启动HR大哥
```bash
# 重启Gateway应用配置
openclaw gateway restart

# 启动HR大哥Agent
openclaw agent start hr

# 验证状态
openclaw agent status hr
```

### 步骤4：测试功能
```bash
# 运行完整测试
chmod +x scripts/test-hr-agent.sh
./scripts/test-hr-agent.sh --mode all
```

## 📱 在飞书中使用

### 启动后，在绑定的飞书群聊中：

```
@HR大哥 我需要一个数据分析Agent

HR大哥会回复：
"数据分析？安排！主要做啥分析？报表生成还是实时监控？
用哪个数据库？需要什么图表类型？绑定到哪个飞书群？"
```

### 常用指令
| 指令 | 功能 | 示例 |
|------|------|------|
| **创建** | 创建新Agent | `创建一个数据分析Agent` |
| **绑定** | 绑定到群聊 | `绑定到oc_123456` |
| **列表** | 查看Agent列表 | `查看所有Agent` |
| **状态** | 查看Agent状态 | `查看hr状态` |
| **帮助** | 查看帮助 | `帮助` |

## 🔧 自定义配置

### 修改主题颜色
```bash
# 重新创建Agent（会保留配置文件）
./scripts/create-hr-agent.sh \
  --name hr \
  --display "HR大哥" \
  --color "#2196F3" \  # 改为蓝色
  --emoji 💼 \         # 改为公文包
  --feishu <your-chat-id>
```

### 修改工作空间位置
```bash
./scripts/create-hr-agent.sh \
  --name hr \
  --workspace ~/my-agents/hr-boss \  # 自定义位置
  --feishu <your-chat-id>
```

### 创建多个HR Agent
```bash
# HR大哥（主要）
./scripts/create-hr-agent.sh \
  --name hr \
  --display "HR大哥" \
  --feishu oc_team_hr

# HR助理（辅助）
./scripts/create-hr-agent.sh \
  --name hr-assistant \
  --display "HR助理" \
  --color "#4CAF50" \
  --emoji 👨‍💼 \
  --feishu oc_team_assistant
```

## 🐛 常见问题

### Q1：脚本执行权限问题
```bash
# 解决方案
chmod +x scripts/*.sh
```

### Q2：飞书群聊ID格式错误
```
错误：飞书群聊ID格式不正确
正确格式：oc_32位十六进制 (例如: oc_1234567890abcdef1234567890abcdef)
```

### Q3：OpenClaw Gateway未运行
```bash
# 检查状态
openclaw gateway status

# 启动Gateway
openclaw gateway start
```

### Q4：配置文件权限问题
```bash
# 检查权限
ls -la ~/.openclaw/openclaw.json

# 修复权限
chmod 644 ~/.openclaw/openclaw.json
```

## 📊 性能监控

### 查看资源使用
```bash
# 查看HR大哥进程
ps aux | grep "openclaw.*hr"

# 查看日志
tail -f ~/.agents/workspaces/hr/logs/agent.log
```

### 监控创建任务
```bash
# 查看最近创建的Agent
ls -la ~/.agents/workspaces/

# 查看OpenClaw绑定状态
openclaw agents list
```

## 🔄 更新和维护

### 更新配置
```bash
# 1. 编辑配置文件
vim ~/.agents/workspaces/hr/AGENT.md

# 2. 重启Agent
openclaw agent restart hr
```

### 备份配置
```bash
# 备份工作空间
tar -czf hr-backup-$(date +%Y%m%d).tar.gz ~/.agents/workspaces/hr/

# 备份OpenClaw配置
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup.$(date +%Y%m%d)
```

### 恢复配置
```bash
# 从备份恢复
tar -xzf hr-backup-20260325.tar.gz -C ~/

# 恢复OpenClaw配置
cp ~/.openclaw/openclaw.json.backup.20260325 ~/.openclaw/openclaw.json

# 重启服务
openclaw gateway restart
openclaw agent start hr
```

## 🎯 最佳实践

### 开发环境
1. **使用测试群聊** - 先在测试群聊中测试功能
2. **监控日志** - 密切监控创建过程中的日志
3. **小步验证** - 每次修改后验证功能
4. **版本控制** - 配置文件加入版本控制

### 生产环境
1. **制定备份策略** - 定期备份重要数据
2. **设置监控告警** - 监控Agent健康状态
3. **建立变更流程** - 规范配置变更流程
4. **文档维护** - 保持文档与系统同步

### 团队协作
1. **统一配置标准** - 团队使用相同的配置标准
2. **知识共享** - 分享使用经验和最佳实践
3. **定期回顾** - 定期回顾使用情况和改进点
4. **培训新成员** - 为新成员提供使用培训

## 📞 技术支持

### 获取帮助
1. **查看日志** - 第一手问题诊断信息
2. **测试脚本** - 使用测试脚本定位问题
3. **社区支持** - 在OpenClaw社区寻求帮助
4. **官方文档** - 参考OpenClaw官方文档

### 报告问题
```bash
# 收集诊断信息
./scripts/test-hr-agent.sh --mode all > diagnostic-report.txt

# 包含以下信息：
# 1. OpenClaw版本
openclaw --version

# 2. 系统信息
uname -a

# 3. 配置文件片段
head -50 ~/.agents/workspaces/hr/AGENT.md

# 4. 错误日志
tail -100 ~/.agents/workspaces/hr/logs/agent.log
```

---

> 💡 **提示**：如果遇到问题，先运行测试脚本`./scripts/test-hr-agent.sh`，它会提供详细的诊断信息。

> 🚀 **下一步**：成功创建HR大哥后，可以尝试创建一个数据分析Agent来测试HR大哥的功能！