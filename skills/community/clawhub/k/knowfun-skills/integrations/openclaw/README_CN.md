# Knowfun Skills for OpenClaw

[English](README.md) | 简体中文

OpenClaw AI助手使用Knowfun.io内容生成的集成指南。

## 什么是OpenClaw？

[OpenClaw](https://openclaw.ai/) 是一个开源的个人AI助手，在您的本地机器上运行。它提供：

- 🤖 具有持久记忆的自主代理功能
- 💬 通过聊天应用访问（WhatsApp、Telegram、Discord、Slack）
- 🖥️ 完全的系统控制（文件访问、shell命令）
- 🌐 浏览器自动化
- 🔧 可扩展的技能系统
- 🏠 本地优先（数据保留在您的机器上）

## 这个集成做什么？

此集成使OpenClaw能够使用Knowfun.io生成教育内容：

- 📚 **课程** - 带旁白的互动演示
- 🎨 **海报** - 视觉信息图和营销素材
- 🎮 **游戏** - 互动学习体验
- 🎬 **视频** - 教育视频和纪录片

## 安装

### 步骤1：安装Knowfun CLI工具

```bash
# 通过 npm 安装（推荐）
npm install -g knowfun-skills

# 或克隆仓库并手动链接
git clone https://github.com/MindStarAI/KnowFun-Skills.git
cd KnowFun-Skills
sudo ln -s $(pwd)/scripts/knowfun-cli.sh /usr/local/bin/knowfun
chmod +x scripts/knowfun-cli.sh
```

### 步骤2：配置API密钥

从[Knowfun.io API平台](https://www.knowfun.io/api-platform)获取您的API密钥：

```bash
# 设置环境变量（临时）
export KNOWFUN_API_KEY="kf_your_api_key_here"

# 或添加到shell配置文件（永久）
echo 'export KNOWFUN_API_KEY="kf_your_api_key_here"' >> ~/.zshrc
source ~/.zshrc
```

### 步骤3：验证安装

```bash
# 测试CLI工具
knowfun credits

# 预期输出：
# ✅ 可用积分：1,000 credits
# 📊 总获得：1,500 credits
# 📉 总使用：500 credits
```

### 步骤4：配置OpenClaw（可选）

如果OpenClaw支持自定义技能定义，您可以添加此集成：

```bash
# 将技能定义复制到OpenClaw的技能目录
#（根据您的OpenClaw安装调整路径）
cp integrations/openclaw/knowfun-skill.json ~/.openclaw/skills/
```

## 使用方法

### 方法1：直接CLI命令

通过OpenClaw直接执行CLI命令：

```bash
# 创建课程
knowfun create course "Python编程入门"

# 检查状态
knowfun status <taskId>

# 获取结果
knowfun detail <taskId>
```

### 方法2：自然语言（推荐）

用自然语言向OpenClaw提问：

```
您："创建一个关于机器学习基础的Knowfun课程"

OpenClaw：*执行 knowfun create course "机器学习基础"*
          *监控任务状态*
          *完成时返回结果URL*
```

### 方法3：通过聊天应用远程访问

通过Telegram、WhatsApp或其他聊天应用使用OpenClaw：

**通过Telegram：**
```
您：@openclaw 创建一个关于气候变化的Knowfun海报

OpenClaw：🎨 正在创建海报...
          📊 任务ID：abc-123
          ⏳ 处理中...
          ✅ 完成！https://r2.knowfun.io/posters/xxx.html
```

## 示例

### 示例1：创建并监控课程

```bash
# 创建课程
TASK_ID=$(knowfun create course "JavaScript基础：变量、函数和对象" | grep -o 'Task ID: [^"]*' | cut -d' ' -f3)

# 等待并检查状态
sleep 180  # 等待3分钟
knowfun status $TASK_ID

# 获取完整详情
knowfun detail $TASK_ID
```

### 示例2：批量内容创建

```bash
# 创建多个内容
knowfun create course "Python基础"
knowfun create poster "Web开发技术栈"
knowfun create game "学习Git命令"

# 列出所有任务
knowfun list
```

### 示例3：自然语言工作流

```
您："创建一个关于Docker的Knowfun课程，等待完成后分享URL"

OpenClaw：
- 执行：knowfun create course "Docker容器和编排"
- 每30秒监控状态
- 完成后获取详情
- 响应："✅ 课程准备好了！https://r2.knowfun.io/courses/xxx.html"
```

### 示例4：自动化内容管道

让OpenClaw创建完整的内容系列：

```
您："创建一系列关于React的Knowfun内容：
     1. React基础课程
     2. React组件生命周期海报
     3. 练习hooks的游戏"

OpenClaw：
- 创建所有三个内容
- 监控每个任务
- 报告进度
- 完成后交付所有URL
```

## 可用命令

| 命令 | 描述 | 示例 |
|------|------|------|
| `create` | 生成内容 | `knowfun create course "主题"` |
| `status` | 检查任务状态 | `knowfun status <taskId>` |
| `detail` | 获取任务详情 | `knowfun detail <taskId>` |
| `list` | 列出最近的任务 | `knowfun list 10` |
| `credits` | 检查积分余额 | `knowfun credits` |
| `schema` | 获取配置选项 | `knowfun schema` |

## 内容类型

| 类型 | 描述 | 处理时间 | 成本 |
|------|------|----------|------|
| **course** | 互动演示 | 2-5分钟 | 100积分 |
| **poster** | 视觉信息图 | 1-3分钟 | 100积分 |
| **game** | 互动学习 | 3-7分钟 | 100积分 |
| **film** | 教育视频 | 5-10分钟 | 100积分 |

## 错误处理

OpenClaw可以优雅地处理错误：

- **401 未授权**：检查API密钥配置
- **402 积分不足**：访问[API平台](https://www.knowfun.io/api-platform)获取更多
- **429 速率受限**：重试前等待60秒
- **404 未找到**：验证taskId是否正确

## 技巧和最佳实践

### 对于OpenClaw用户

1. **使用自然语言**：让OpenClaw解释您的意图
   ```
   ✅ "创建一个关于Python的课程"
   ❌ knowfun create course "Python"
   ```

2. **自动化工作流**：将操作链接在一起
   ```
   "创建一个课程，等待完成，然后创建相关海报"
   ```

3. **远程内容创建**：使用聊天应用随时随地生成内容
   ```
   Telegram："创建一个关于SQL查询的Knowfun游戏"
   ```

4. **批量操作**：首先检查积分
   ```
   "检查我的Knowfun积分，然后创建3个课程"
   ```

### 内容创建技巧

- **具体明确**：详细的描述产生更好的结果
- **结构化内容**：对于课程，概述关键概念
- **视觉偏好**：对于海报，提及风格偏好
- **学习目标**：对于游戏，指定要教授的内容
- **叙事结构**：对于视频，概述故事

## 故障排除

### 问题："找不到命令：knowfun"

**解决方案：**
```bash
# 检查CLI是否在PATH中
which knowfun

# 如果未找到，创建符号链接
sudo ln -s /path/to/knowfun-skills/scripts/knowfun-cli.sh /usr/local/bin/knowfun
```

### 问题："未找到API密钥"

**解决方案：**
```bash
# 检查是否设置
echo $KNOWFUN_API_KEY

# 设置它
export KNOWFUN_API_KEY="kf_your_key"
```

### 问题："积分不足"

**解决方案：**
访问 https://www.knowfun.io/api-platform 管理您的账户

## 高级用法

### 自定义技能集成

如果OpenClaw支持自定义技能，您可以定义自动化规则：

```json
{
  "trigger": "创建knowfun内容",
  "action": "执行CLI命令",
  "monitor": "轮询状态直到完成",
  "notify": "发送结果URL"
}
```

### Webhook集成

为任务完成通知设置webhook（如果OpenClaw支持）：

```bash
# 在API调用中包含callbackUrl
curl -X POST https://api.knowfun.io/api/openapi/v1/tasks \
  -d '{"callbackUrl": "http://your-openclaw-instance/webhook"}'
```

## 资源

- **Knowfun Skills文档**：[README_CN.md](../../README_CN.md)
- **API参考**：[api-reference_CN.md](../../api-reference_CN.md)
- **示例**：[examples_CN.md](../../examples_CN.md)
- **OpenClaw网站**：https://openclaw.ai/
- **Knowfun.io**：https://www.knowfun.io

## 支持

- **Issues**：[GitHub Issues](https://github.com/MindStarAI/KnowFun-Skills/issues)
- **API平台**：https://www.knowfun.io/api-platform
- **文档**：https://www.knowfun.io/docs

---

