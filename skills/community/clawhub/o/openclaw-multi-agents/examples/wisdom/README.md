# Wisdom目录模板 - 子Agents学习传递

这个目录用于存储各个子agent在工作中积累的经验和教训。
主agent会从这些文件中提取learnings，并传递给后续的子agents。

## 📁 文件说明

- **conventions.md** - 代码规范和约定（如"用户验证必须在服务端"）
- **successes.md** - 成功的做法和最佳实践
- **failures.md** - 失败的教训和避免的错误
- **gotchas.md** - 坑和陷阱（容易犯错的地方）
- **commands.md** - 有用的命令和工具使用技巧

---

## 🎯 使用方式

### Accumulate Wisdom工作流

主agent在分发任务时，会：

1. **提取learnings** - 从子agent的回复中识别有价值的信息
2. **分类记录** - 记录到对应的wisdom文件
3. **传递给后续子agents** - 在下次任务中包含相关wisdom

---

## 📖 示例工作流

```
芒格完成PRD → 返回结果
  ↓
主agent提取learnings：
  - "用户验证应该在服务端完成"
  - "JWT token应该有7天过期时间"
  ↓
记录到wisdom/conventions.md：
  - 【2026-03-16】芒格：用户验证应该在服务端完成
  - 【2026-03-16】芒格：JWT过期时间：7天
  ↓
费曼开始开发 → 主agent在任务中包含wisdom：
  sessions_send \
    task="实现登录功能
    
    【重要约定】（来自芒格的PRD）：
    - 用户验证必须在服务端完成
    - JWT token过期时间：7天
    " \
    agentId="feynman" \
    model="glm-5"
  ↓
德明审查代码 → 主agent在任务中包含wisdom：
  sessions_send \
    task="审查登录功能代码
    
    【审查重点】（来自芒格的PRD）：
    - 检查：用户验证是否在服务端完成？
    - 检查：JWT过期时间是否为7天？
    " \
    agentId="deming" \
    model="glm-5"
```

---

## 🚀 快速开始

### 方法1：使用setup_team.sh自动创建

```bash
# 创建产品开发团队时会自动创建wisdom目录
bash scripts/setup_team.sh product-dev

# 目录位置：~/.openclaw/workspace/memory/wisdom/
```

### 方法2：手动创建

```bash
# 1. 创建目录结构
mkdir -p ~/.openclaw/workspace/memory/wisdom

# 2. 复制模板文件
cp examples/wisdom/*.md ~/.openclaw/workspace/memory/wisdom/

# 3. 清空示例内容（保留模板结构）
# 编辑各个.md文件，删除示例，保留结构
```

---

## 💡 最佳实践

### 1. 及时记录

子agent每次完成任务后，主agent应该立即提取learnings并记录。

### 2. 分类明确

- **conventions** - 规范和约定（必须遵守）
- **successes** - 成功做法（值得复用）
- **failures** - 失败教训（避免重复）
- **gotchas** - 坑和陷阱（提醒注意）
- **commands** - 实用命令（快速参考）

### 3. 传递给后续子agents

主agent在分发任务时，应该包含相关的wisdom：

```markdown
【重要约定】（来自芒格）：
- 用户验证必须在服务端完成

【避免重复错误】（来自德明）：
- 密码不要明文存储，使用bcrypt

【实用命令】：
- bcrypt哈希：bcrypt.hash('password', 10)
```

---

## 📊 v2.0核心功能

这是v2.0新增的**Accumulate Wisdom机制**，基于oh-my-openagent的理念：

- ✅ 防止重复错误
- ✅ 保持团队一致性
- ✅ 积累最佳实践
- ✅ 提高协作效率

---

**创建时间：** 2026-03-16
**版本：** 6.0.0
**说明：** 这是 multi-agent-orchestration skill 的一部分
