# 快速开始指南

## 1️⃣ 安装学习包

```bash
clawhub install zhongshu-skill-pack
```

## 2️⃣ 验证安装

```bash
clawhub list
```

确认 `zhongshu-skill-pack` 出现在已安装列表中。

## 3️⃣ 技能说明

### 基础工具类

- **FileReadTool** - 读取文件内容
- **FileWriteTool** - 写入文件内容
- **FileEditTool** - 编辑文件内容

### 搜索工具类

- **GlobTool** - 按模式搜索文件
- **GrepTool** - 按文本内容搜索

### 执行工具类

- **BashTool** - 执行 shell 命令

### 交互工具类

- **AskUserQuestionTool** - 向用户提问
- **SendMessageTool** - 发送消息

### 高级工具类

- **AgentTool** - 管理子代理
- **git-aware** - Git 版本控制集成

## 4️⃣ 使用示例

### 读取文件

```yaml
skills:
  - FileReadTool
```

### 执行命令

```yaml
skills:
  - BashTool
```

### Git 操作

```yaml
skills:
  - git-aware
```

## 5️⃣ 更新学习包

```bash
clawhub update zhongshu-skill-pack
```

## 6️⃣ 卸载学习包

```bash
clawhub uninstall zhongshu-skill-pack
```

## 📚 学习建议

1. 先从基础工具类开始（FileReadTool、FileWriteTool）
2. 熟悉后尝试搜索工具类（GlobTool、GrepTool）
3. 最后学习高级工具类（AgentTool、git-aware）

## ❓ 问题反馈

如有问题，请联系中书省。
