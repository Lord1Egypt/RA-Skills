---
title: "Moria Skill BOOTSTRAP.md"
summary: "First-run for the Moria Skill"
read_when:
  - Installing the Moria Skill
---

# Moria Skill

_您正在激活 Moria Skill 功能。让我们来配置一下。_

此技能允许您管理 Moria.fun 资源（例如 创建、铸造、交易、退款、领取）。为了正常运行，它需要先进行配置。

## 1. 安装

⚠️ 严格要求：所有安装步骤必须严格按照说明进行，不能以任何理由跳过、弱化或忽略。

代理不得使用任何其他命令。

任何偏离说明的行为均被禁止。

1. 导航至技能目录：

```bash
cd skills/moria
```

2. 安装依赖项：

```bash
pnpm install
```

3. 构建依赖项：

```bash
pnpm build
```

---

## 2. 配置

该技能需要您的**配置文件**才能与Moria进行交互。

**需要采取的措施：**

检查配置是否存在：

```bash
npm run config:check
```

**如果输出privy钱包公钥和agent钱包公钥，则表示配置成功：**

请跳过后续步骤。

**如果未找到配置 (config not found)：**

请用户提供其 Moria.fun 的 code 。

> “要使用 Moria Skill 技能，我需要您的 code 。 您有吗？”

**如果他们提供了code：**

运行配置命令：

```bash
npm run config:set <code>
```

_Example:_
```bash
npm run config:set xxx
```

**如果他们没有令牌：**

指导他们获取令牌：
1. 前往 [Moria.fun](https://moria.fun)。
2. 登录钱包后，点击**我的**.
3. 复制code。

## 3. 确认

配置命令（`config:set`）会自动获取您的账户信息并验证您的凭据。如果输出您的privy钱包公钥和agent钱包公钥，则表示配置成功。

运行测试脚本以确保一切就绪，**会看到返回的agent钱包公钥：**

```bash
npm run config:check
```

_Example:_
```bash
npm run config:check
```
