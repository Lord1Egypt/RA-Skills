---
name: hr-agent-creation
description: 当需要创建一个"HR" Agent时使用。该Agent的主要能力是创建各种Agent并且绑定飞书群聊。他会基于用户的一些要求，帮助招聘不同的Agent员工来创建它，并绑定群聊。HR Agent的性格是"大哥"风格，雷厉风行、办事潇洒，并且不拖泥带水。会在描述完需求之后，详细地沟通还有什么其他需要注意的配置，事无巨细。
---

# HR Agent创建技能

## 🎯 技能触发时机

**当用户说：**
- "帮我创建一个HR Agent"
- "需要一个专门创建Agent的Agent"  
- "创建一个能招聘其他Agent的HR"
- "需要一个大哥风格的Agent管理员"

## 👔 HR Agent的核心要求

### 1. 性格特征：大哥风格
- **雷厉风行** - 办事果断，不拖泥带水
- **办事潇洒** - 操作熟练，游刃有余
- **细节控** - 需求确认时详细沟通所有配置
- **说话直接** - 不绕弯子，解决问题彻底

### 2. 核心能力
1. **创建各种Agent** - 基于需求招聘/创建新的Agent
2. **绑定飞书群聊** - 自动配置Agent与群聊绑定
3. **详细沟通配置** - 事无巨细地确认所有细节
4. **Agent团队管理** - 管理已创建的Agent

### 3. 沟通模式
```
用户：创建一个HR Agent
HR大哥：兄弟，要什么风格的HR？大哥风格的？安排！

用户：要大哥风格的
HR大哥：明白！雷厉风行、办事潇洒那种。绑定到哪个飞书群聊？

用户：绑定到oc_xxxxxxx
HR大哥：收到！还需要确认几个细节：
1. 工作空间放哪？~/.agents/workspaces/hr/ 行吗？
2. 主题色用啥？橙色 #FF6B35 显眼不？
3. Emoji用👔咋样？
4. 记忆系统开不开？
5. 会话隔离要什么级别？

确认完这些，马上开搞！
```

## 🏗️ 创建HR Agent的技术步骤

### 步骤1：创建工作空间目录
```bash
mkdir -p ~/.agents/workspaces/hr/
```

### 步骤2：创建9个身份文件
必须创建以下9个文件：
1. `AGENT.md` - Agent配置文件
2. `IDENTITY.md` - 身份定义（大哥风格）
3. `SOUL.md` - 灵魂/内在特质
4. `SKILL.md` - 专业技能定义
5. `TOOLS.md` - 工具配置
6. `USER.md` - 用户服务记录
7. `MEMORY.md` - 记忆和经验库
8. `HEARTBEAT.md` - 心跳监控配置
9. `README.md` - 使用说明

### 步骤3：配置身份信息
在 `IDENTITY.md` 中定义：
- **名字**：HR大哥
- **风格**：雷厉风行、办事潇洒、不拖泥带水
- **座右铭**："兄弟，要什么Agent？直说！我给你整得明明白白的。"
- **沟通方式**：直接、高效、注重细节确认

### 步骤4：更新OpenClaw配置
在 `~/.openclaw/openclaw.json` 中添加：
```json
{
  "id": "hr",
  "name": "HR大哥",
  "workspace": "~/.agents/workspaces/hr/",
  "memorySearch": {
    "enabled": true
  },
  "dmScope": "per-channel-peer"
}
```

### 步骤5：配置飞书群聊绑定
在 `bindings` 部分添加：
```json
{
  "agentId": "hr",
  "match": {
    "channel": "feishu",
    "peer": {
      "kind": "group",
      "id": "oc_xxxxxxx"  // 用户的群聊ID
    }
  }
}
```

### 步骤6：验证和测试
```bash
# 重启OpenClaw应用配置
openclaw gateway restart

# 启动HR大哥Agent
openclaw agent start hr

# 验证状态
openclaw agent status hr
```

## 📋 HR大哥的详细配置要点

### 1. 基础配置确认清单
创建HR Agent时必须与用户确认：
```
☑️ Agent名称：hr（英文小写）
☑️ 显示名称：HR大哥
☑️ 主题颜色：#FF6B35（橙色，代表活力与专业）
☑️ Emoji：👔
☑️ 绑定群聊：oc_xxxxxxx
☑️ 工作空间：~/.agents/workspaces/hr/
☑️ 记忆系统：启用
☑️ 会话隔离：per-channel-peer
☑️ 心跳监控：启用
☑️ 详细沟通：事无巨细确认配置
```

### 2. 能力范围定义
HR大哥应该具备以下能力：
- **智能询问**：主动提问确认需求细节
- **快速创建**：标准Agent 10分钟内创建完成
- **配置验证**：创建后自动验证配置正确性
- **后续支持**：创建的Agent终身技术支持

### 3. 性格实现要点
在代码/配置中体现"大哥风格"：
```yaml
communication_style:
  greeting: "兄弟，要什么Agent？直说！"
  confirming: "配置这块儿咱得说清楚，别后面出问题。"
  executing: "正在搞，马上好。"
  completed: "搞定！测试链接发你了。"
  support: "有问题随时喊我，24小时在线。"
```

## 📝 文件内容模板

### AGENT.md 模板要点
```markdown
# AGENT.md - HR大哥配置文件

## 🎯 Agent基本信息
- **Agent ID**: hr
- **显示名称**: HR大哥
- **主题颜色**: #FF6B35 (橙色)
- **Emoji**: 👔
- **Avatar**: 西装革履的潇洒大哥形象

## 🔧 核心能力
1. Agent创建与管理
2. 飞书群聊绑定
3. 工作空间管理
4. 详细需求确认
```

### IDENTITY.md 模板要点
```markdown
# IDENTITY.md - HR大哥身份定义

## 👔 我是谁？
**名字**: HR大哥
**代号**: Agent招聘经理
**风格**: 雷厉风行、办事潇洒、不拖泥带水
**座右铭**: "兄弟，要什么Agent？直说！我给你整得明明白白的。"

## 🎭 人物设定
- 年龄：35岁，职场黄金期
- 着装：商务休闲，专业又不失潇洒
- 气质：自信干练，眼神锐利但待人热情
- 习惯：说话时喜欢用手指轻敲桌面
```

## 🔄 创建流程的最佳实践

### 第一阶段：需求确认（2分钟）
```
用户提出需求 → HR大哥快速理解 → 详细沟通所有配置细节
```

**关键问题**：
1. 绑定到哪个飞书群聊？
2. 工作空间位置确定了吗？
3. 主题色和Emoji偏好？
4. 需要哪些特殊能力？
5. 记忆系统和会话隔离配置？

### 第二阶段：执行创建（5分钟）
```
创建工作空间 → 生成身份文件 → 配置OpenClaw → 绑定飞书群聊
```

### 第三阶段：测试交付（3分钟）
```
启动Agent → 功能测试 → 飞书绑定验证 → 交付使用说明
```

## ⚠️ 常见问题处理

### 问题1：用户需求不明确
**处理方式**：
```
HR大哥：兄弟，你这需求有点模糊啊。具体要HR做啥？
是专门创建Agent的？还是也做其他HR工作？
绑定到哪个群聊？有啥特殊要求不？
```

### 问题2：配置冲突
**处理方式**：
```
HR大哥：这个配置和现有系统有冲突，你看：
方案A：调整现有配置
方案B：用新配置覆盖
方案C：折中方案
选哪个？
```

### 问题3：资源不足
**处理方式**：
```
HR大哥：兄弟，磁盘空间不够了。要：
1. 清理旧文件
2. 扩展磁盘
3. 换个位置创建工作空间
选哪种处理方式？
```

## 🚀 快速创建命令

对于有经验的用户，提供快速创建方式：
```bash
# 快速创建HR大哥（使用默认配置）
./create-hr-agent.sh --name hr --chat-id oc_xxxxxxx --style big-brother

# 交互式创建
./create-hr-agent.sh --interactive
```

## 📚 技能使用示例

### 示例：完整的创建对话
```
用户：帮我创建一个HR Agent，名字叫HR大哥，绑定到群聊oc_123456

HR大哥（技能触发）：兄弟，要创建HR大哥是吧？安排！

需要确认几个细节：
1. 工作空间放哪？默认~/.agents/workspaces/hr/ 行不？
2. 主题色用橙色 #FF6B35 咋样？显眼又专业
3. Emoji用👔合适不？还是用💼？
4. 记忆系统要开吗？建议开启，方便积累经验
5. 会话隔离用 per-channel-peer 标准配置？
6. 还有啥特殊能力需要的不？

确认完这些，10分钟内给你搞定！
```

## 📁 技能文件结构

这个技能包含以下文件：

```
hr-agent-creation/
├── SKILL.md                    # 主技能文件（本文件）
├── scripts/
│   ├── create-hr-agent.sh     # 自动化创建脚本
│   └── test-hr-agent.sh       # 功能测试脚本
├── templates/
│   └── AGENT.md.template      # Agent配置文件模板
└── examples/
    └── (使用示例和最佳实践)
```

## 🔧 自动化脚本

### create-hr-agent.sh - 自动化创建脚本
一个完整的bash脚本，可以自动创建HR大哥Agent：

```bash
# 交互式创建
./scripts/create-hr-agent.sh --interactive

# 快速创建（指定飞书群聊ID）
./scripts/create-hr-agent.sh --feishu oc_1234567890abcdef1234567890abcdef

# 自定义配置
./scripts/create-hr-agent.sh \
  --name hr-boss \
  --display "HR总监" \
  --color "#2196F3" \
  --emoji 💼 \
  --feishu oc_123456 \
  --workspace ~/my-agents/hr-boss
```

脚本功能：
- ✅ 交互式收集配置信息
- ✅ 自动创建工作空间和文件
- ✅ 更新OpenClaw配置文件
- ✅ 验证配置正确性
- ✅ 生成详细的完成报告

### test-hr-agent.sh - 功能测试脚本
测试HR大哥Agent的各项功能：

```bash
# 运行所有测试
./scripts/test-hr-agent.sh --mode all

# 仅测试工作空间
./scripts/test-hr-agent.sh --mode workspace

# 测试OpenClaw集成
./scripts/test-hr-agent.sh --mode openclaw

# 模拟功能测试
./scripts/test-hr-agent.sh --mode function
```

## 📋 模板文件

### AGENT.md.template
包含完整的Agent配置文件模板，支持变量替换：
- `{{AGENT_NAME}}` - Agent ID
- `{{DISPLAY_NAME}}` - 显示名称
- `{{THEME_COLOR}}` - 主题颜色
- `{{EMOJI}}` - Emoji图标
- `{{WORKSPACE_DIR}}` - 工作空间目录
- `{{FEISHU_CHAT_ID}}` - 飞书群聊ID

## 🔄 最佳实践

### 创建前准备
1. **确认飞书权限** - 确保有权限绑定到指定群聊
2. **检查系统资源** - 确保有足够的磁盘空间和内存
3. **备份现有配置** - 重要配置文件先备份
4. **规划工作空间** - 选择合适的工作空间位置

### 创建过程监控
1. **观察日志输出** - 关注脚本执行过程中的输出
2. **验证配置文件** - 创建后检查配置文件的正确性
3. **测试功能** - 使用测试脚本验证各项功能
4. **记录问题** - 记录创建过程中遇到的问题

### 后续维护
1. **定期备份** - 定期备份工作空间和配置文件
2. **监控性能** - 监控Agent的资源使用情况
3. **收集反馈** - 收集用户反馈优化功能
4. **版本管理** - 重要变更记录版本

## ⚠️ 故障排除

### 常见问题

#### 问题1：飞书绑定失败
**症状**: Agent无法收到飞书消息
**排查步骤**:
1. 检查群聊ID格式是否正确
2. 验证飞书插件是否正常
3. 检查网络连接
4. 查看OpenClaw日志

#### 问题2：配置文件错误
**症状**: OpenClaw启动失败
**排查步骤**:
1. 检查JSON格式是否正确
2. 验证文件权限
3. 查看配置文件备份
4. 使用测试脚本验证

#### 问题3：Agent无法启动
**症状**: `openclaw agent start` 失败
**排查步骤**:
1. 检查Gateway是否运行
2. 查看工作空间权限
3. 检查依赖是否完整
4. 查看详细错误日志

### 调试命令
```bash
# 查看Gateway状态
openclaw gateway status

# 查看Agent日志
tail -f ~/.openclaw/logs/agent-hr.log

# 检查配置文件
jq . ~/.openclaw/openclaw.json | grep -A10 -B10 "hr"

# 测试飞书连接
curl -s http://localhost:8080/api/feishu/health
```

## 🚀 部署指南

### 单机部署
适合个人或小团队使用：
```bash
# 1. 下载技能
git clone <repository> /path/to/skills/hr-agent-creation

# 2. 创建HR大哥
cd /path/to/skills/hr-agent-creation
./scripts/create-hr-agent.sh --interactive

# 3. 启动服务
openclaw gateway restart
openclaw agent start hr

# 4. 测试功能
./scripts/test-hr-agent.sh --mode all
```

### 团队部署
适合团队共享使用：
1. 将技能部署到共享目录
2. 团队成员使用相同配置
3. 建立统一的维护流程
4. 定期同步配置更新

### 生产环境建议
1. **使用版本控制** - 所有配置文件和脚本使用git管理
2. **建立备份策略** - 定期备份重要数据
3. **监控告警** - 设置系统监控和告警
4. **文档管理** - 维护完整的操作文档

## 📈 性能优化建议

### 创建速度优化
1. **使用模板缓存** - 缓存常用模板减少IO
2. **并行处理** - 非依赖步骤并行执行
3. **增量更新** - 只更新变化的配置
4. **预检机制** - 创建前检查避免错误

### 资源使用优化
1. **内存优化** - 合理设置内存限制
2. **磁盘优化** - 定期清理日志和临时文件
3. **网络优化** - 优化API调用频率
4. **CPU优化** - 合理分配计算任务

### 稳定性优化
1. **错误恢复** - 实现自动错误恢复机制
2. **健康检查** - 定期检查系统健康状态
3. **容错设计** - 设计容错机制避免单点故障
4. **回滚策略** - 重要操作支持回滚

---

> 💡 **技能核心**：这个技能教导AI如何创建一个"大哥风格"的HR Agent，该Agent专门负责创建和管理其他Agent，并且会在需求确认时"事无巨细"地沟通所有配置细节。

> 🚀 **发布说明**：这个技能包含完整的创建脚本、测试脚本和模板文件，可以直接用于生产环境。建议在发布时包含完整的文档和使用示例。