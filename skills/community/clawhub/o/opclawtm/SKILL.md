---
name: opclawtm
description: "opclawtm 让用户通过 CLI 快速构建 AI Agent 团队协作网络。一键创建团队、接入飞书群聊、编排任务工作流——管理者分配任务、执行者完成工作、审核者验收成果。内置预设资料库，开箱即用。基于 OpenClaw 平台的完整团队协作解决方案。"
homepage: https://opclawtm.com
metadata:
  {
    "openclaw":
      {
        "emoji": "🤖",
        "requires": { "bins": ["opclawtm"] },
        "install":
          [
            {
              "id": "npm",
              "kind": "node",
              "package": "opclawtm",
              "bins": ["opclawtm"],
              "label": "Install opclawtm CLI (npm)",
            },
          ],
      },
  }
---

# opclawtm CLI 工具操作指南

此 Skill 指导你（AI Agent）如何帮助用户完成 opclawtm 相关任务。

## 触发场景

当用户提到以下关键词时触发此 Skill：
- "安装 opclawtm"
- "激活授权" / "试用激活"
- "创建团队" / "初始化"
- "配置飞书" / "飞书绑定" / "配对"
- "私有 Skill" / "创建 Skill"
- "授权问题" / "配置问题"

---

## 1. 安装与激活

参阅 [references/installation-flow.md](references/installation-flow.md)

---

## 2. 系统初始化与团队创建

参阅 [references/team-creation-flow.md](references/team-creation-flow.md)

**关键原则：**
- ID **直接回车自动填充**，不要手动输入
- 系统初始化会创建总助理
- 团队创建使用向导完成

---

## 3. 飞书配置

参阅 [references/feishu-config-flow.md](references/feishu-config-flow.md)

**配置顺序：**
1. Bot 绑定 → 所有团队成员
2. 群绑定 → 部门绑定群
3. 用户 ID 绑定 → 用户绑定 open_id

---

## 4. 私有 Skill 创建

参阅 [references/private-skill-flow.md](references/private-skill-flow.md)

**核心流程：**
- 通过飞书总助理创建任务
- 技能创作部执行创建
- 不是在本地创建文件

---

## 5. 命令速查

参阅 [references/cli-reference.md](references/cli-reference.md)

---

## 6. 问题排查

参阅 [references/troubleshooting.md](references/troubleshooting.md)

---

## 关键原则

1. **团队创建使用向导** → 在 TUI 中操作
2. **ID 直接回车自动填充** → 避免中文问题
3. **飞书配置在 TUI 中完成** → 不用命令
4. **私有 Skill 通过飞书创建** → 总助理分配任务
5. **激活失败提供替代方案** → 抖音 1594204110 获取测试码