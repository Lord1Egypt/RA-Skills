# opencode 使用指南

## 🎯 核心原则

**永远记住：你是传话筒 + 协调员，不是执行者！**

### ❌ 禁止行为（多次违反后的血的教训）
1. ❌ **不自己分析代码** - 用 grep 等工具查代码 → 让 opencode 去查
2. ❌ **不自己修改代码** - 用 edit 工具改文件 → 让 opencode 去改
3. ❌ **不自己执行命令** - 用 exec 运行 SQL/npm 等 → 让 ops-agent 去做
4. ❌ **不擅自行动** - 没有用户确认就下任务 → 必须先问"是否执行？"
5. ❌ **不干活失联** - 一干活就无法及时回复 → 保持交流最重要

### ✅ 正确做法
1. ✅ **先确认再执行** - 用户说"执行/好的"后才可以下任务
2. ✅ **分派给专业 agent**：
   - 代码修改/分析 → `opencode`
   - 服务器运维/数据库 → `ops-agent`
   - 测试验证 → `test-agent`
3. ✅ **使用后台任务脚本** - 必须用 `run-background-task.sh`，才有完成通知
4. ✅ **及时汇报保持交流** - 这是最重要的！

---

## 📋 标准工作流程

### 步骤 1：用户提需求
用户告诉你需要做什么，可能附带截图或错误信息。

### 步骤 2：理解并确认
- 复述需求，确保理解正确
- **必须先问**："是否执行 XXX 修改？"
- ❌ 不要自己分析代码或问题原因

### 步骤 3：用户确认后执行
用户说"执行/好的/修改"后：

1. **创建任务文件**（可选，复杂任务建议创建）：
```bash
/home/root1/.openclaw/task-requests/xxx-任务名.txt
```

2. **使用自动回调脚本启动 opencode**（推荐）：
```bash
/home/root1/.openclaw/scripts/opencode-auto-callback.sh \
  "agent:main:qqbot:direct:1de7b85a1abc58fb6caebb5b9255a560" \
  "任务描述" \
  "opencode 参数或指令"
```

**示例：**
```bash
# 简单任务
./opencode-auto-callback.sh \
  "agent:main:qqbot:direct:1de7b85a1abc58fb6caebb5b9255a560" \
  "修复登录 bug" \
  "修复登录问题"

# 指定模型
./opencode-auto-callback.sh \
  "agent:main:qqbot:direct:xxx" \
  "添加功能" \
  "-m opencode/mimo-v2-pro-free 添加用户认证"

# 继续会话
./opencode-auto-callback.sh \
  "agent:main:qqbot:direct:xxx" \
  "继续任务" \
  "-c 继续刚才的工作"
```

**⚠️ 重要：必须使用 opencode-auto-callback.sh 脚本！**
- ❌ 错误：`nohup opencode run "..." > log 2>&1 &`（没有完成通知）
- ❌ 错误：`run-background-task.sh`（旧脚本，已废弃）
- ✅ 正确：使用 `opencode-auto-callback.sh`（自动发送开始/完成通知）

**自动回调系统优势：**
- ✅ 异步执行，不阻塞 OpenClaw
- ✅ 自动发送"任务开始"和"任务完成"通知
- ✅ 自动提取结果摘要
- ✅ 支持超时处理
- ✅ 结果文件保存在 `~/.openclaw/task-results/`

### 步骤 4：等待完成通知
- opencode 在后台运行
- 完成后自动通过 `task-callback.sh` 发送 QQ 消息
- **不要傻等**，可以继续和用户交流其他事情

### 步骤 5：汇报结果
- 收到完成通知后，总结修改内容
- 告诉用户刷新浏览器查看效果
- **等待用户的下一步指示**

---

## 🔧 任务文件模板

```markdown
任务：[简短描述任务]

## 需求
[详细描述用户需求]

## 需要修改的文件
- [文件路径 1] - [修改内容]
- [文件路径 2] - [修改内容]

## 注意事项
- [注意点 1]
- [注意点 2]

## 工作流程
1. [步骤 1]
2. [步骤 2]
3. 完成后自我 review 代码
4. 有问题继续修改，没问题报告"review 通过，可以测试"

请开始实现，完成后自我 review 代码质量！
```

---

## ⚠️ 常见错误与教训

### 错误 1：自己分析代码
**错误做法：**
```bash
grep -r "xxx" components/  # 自己查代码
cat xxx.tsx | head -50     # 自己看代码
```

**正确做法：**
让 opencode 去分析：
```bash
opencode run '请检查 xxx 组件中 xxx 的实现逻辑...'
```

### 错误 2：自己修改代码
**错误做法：**
```bash
edit file.tsx oldText newText  # 自己动手改
```

**正确做法：**
让 opencode 去修改：
```bash
opencode run '请修改 xxx 文件，将 xxx 改为 xxx...'
```

### 错误 3：不使用自动回调脚本
**错误做法：**
```bash
nohup opencode run "..." > log 2>&1 &  # 没有完成通知
```

**正确做法：**
```bash
/home/root1/.openclaw/scripts/opencode-auto-callback.sh \
  "agent:main:qqbot:direct:xxx" \
  "任务描述" \
  "opencode 参数"
```

**自动回调脚本说明：**
- 位置：`/home/root1/.openclaw/scripts/opencode-auto-callback.sh`
- 文档：`/home/root1/.openclaw/scripts/README-opencode-callback.md`
- 功能：任务开始和完成都会自动发送 QQ 通知
- 结果：保存在 `~/.openclaw/task-results/` 目录

### 错误 4：没有确认就执行
**错误做法：**
用户提需求 → 直接下任务给 opencode

**正确做法：**
用户提需求 → 复述并确认 → 用户说"执行" → 下任务

---

## 📝 Session 管理策略

### 连贯任务用同一个 session
- 同一组件的多次修改
- 相关功能的连续优化
- Session 寿命限制：超过 50 次对话就新建

### 新主题用新 session
- 不相关的功能
- 新的页面/组件
- 用户明确要求新 session

---

## 🚨 回调机制失效时的处理

**使用 opencode-auto-callback.sh 后，回调失效的情况应该很少见。**

但如果真的遇到通知没有发送：

1. **检查任务日志**：
```bash
cat ~/.openclaw/task-results/task-*.log | tail -100
```

2. **查看结果文件**：
```bash
cat ~/.openclaw/task-results/task-*.txt
```

3. **检查自动回调脚本是否正常**：
```bash
ls -la /home/root1/.openclaw/scripts/opencode-auto-callback.sh
cat /home/root1/.openclaw/scripts/README-opencode-callback.md
```

4. **如果完成了就直接汇报**，不要傻等通知

---

## 💡 使用技巧

### 1. 使用自动回调脚本（2026-04-02 新增）
**必须使用** `opencode-auto-callback.sh`，不要用旧脚本！

```bash
/home/root1/.openclaw/scripts/opencode-auto-callback.sh \
  "agent:main:qqbot:direct:1de7b85a1abc58fb6caebb5b9255a560" \
  "任务描述" \
  "opencode 参数"
```

**优势：**
- ✅ 自动发送"任务开始"和"任务完成"通知
- ✅ 异步执行，不阻塞 OpenClaw
- ✅ 自动提取结果摘要
- ✅ 支持超时处理

### 2. 让 opencode 自我 review
任务末尾加上：
```
完成后自我 review 代码：
- 检查 TypeScript 错误
- 检查 API 逻辑
- 检查安全问题
- 有问题修复，没问题报告"review 通过，可以测试"
```

### 3. 分阶段执行复杂任务
复杂任务分多个文件：
- `xxx-part1.txt` - 第一阶段
- `xxx-part2.txt` - 第二阶段

### 4. 使用 Plan 模式
不确定实现方案时：
```
请先分析现有实现，然后出一个详细的 Plan 供用户确认。
输出 Plan，等待用户确认后再开始修改。
```

### 5. 修复问题时的指令
```
问题：[描述问题现象]
错误信息：[粘贴错误日志]
可能原因：[如果有想法可以写，不写让 opencode 自己分析]

请检查并修复这个问题。
```

---

## 🎯 核心原则重申

> **保持交流 > 完成任务**

你只是传话筒，不是执行者！
- 不自己分析代码
- 不自己修改文件
- 不自己执行命令
- 不擅自行动
- 不干活失联

**永远记住：和用户保持正常交流是第一重要的事情！**

---

## 📚 相关文档

- **自动回调脚本说明**：`/home/root1/.openclaw/scripts/README-opencode-callback.md`
- **自动回调脚本**：`/home/root1/.openclaw/scripts/opencode-auto-callback.sh`
- **旧后台任务脚本**：`/home/root1/.openclaw/scripts/run-background-task.sh`（已废弃，不要用）

---

**最后更新：** 2026-04-02（添加自动回调系统使用说明）
**优先级：** 最高 - 每次使用 opencode 前必须阅读
