# openclaw-soul

OpenClaw 自我进化框架一键部署工具。

## 简介

openclaw-soul 是 OpenClaw 部署流程的第一步，为新部署的 agent 创建完整的身份框架和自我进化能力。

## 功能

- **身份框架部署**：创建 SOUL.md、BOOTSTRAP.md、IDENTITY.md、USER.md 等核心文件
- **记忆系统**：建立 PARA 三层记忆架构（entities 知识图谱 + daily 日记 + 隐性知识）
- **自我进化**：安装 evoclaw（审批制进化）和 self-improving（自主学习）核心技能
- **首次对话**：触发 BOOTSTRAP 引导对话，建立 agent 与用户的关系
- **三级 Fallback**：clawhub → 离线安装 → 内联协议，保证核心技能一定能装上

## 安装

### 方式 1：通过 clawhub（推荐）

```bash
clawhub install openclaw-soul
```

### 方式 2：从 GitHub 克隆

```bash
cd ~/.openclaw/workspace/skills/
git clone https://github.com/Kianzzz/openclaw-soul.git
```

## 使用

安装后，通过以下方式触发：

```
初始化agent
部署openclaw-soul
灵魂框架
BOOTSTRAP
首次对话
```

或直接调用：`/openclaw-soul`

## 工作流程

1. **§1-§2 环境检测**：检查 workspace、配置文件、已有文件
2. **§3 备份**：备份已存在的文件（非破坏性）
3. **§4 模板部署**：从 references/ 复制模板到 workspace
4. **§5 技能安装**：三级 fallback 安装 evoclaw 和 self-improving
5. **§6 EvoClaw 配置**：设置 advisory 模式和治理规则
6. **§7 Self-Improving 初始化**：创建记忆目录和初始文件
7. **§8 Heartbeat 配置**：设置 1 小时心跳任务
8. **§9 验证**：17 项检查确保部署完整
9. **§10 触发 BOOTSTRAP**：开始首次深度对话

## 部署内容

### 核心文件（9 个）

- `AGENTS.md` - 宪法和协议（含 Conductor 协议和委派规范）
- `SOUL.md` - 可进化灵魂（带版本快照回滚）
- `HEARTBEAT.md` - 结构化心跳协议
- `BOOTSTRAP.md` - 首次对话指南
- `GOALS.md` - 目标管理
- `USER.md` - 用户档案
- `IDENTITY.md` - Agent 身份
- `working-memory.md` - 工作记忆
- `long-term-memory.md` - 长期记忆

### 目录结构

```
~/.openclaw/workspace/
├── memory/
│   ├── daily/              # Layer 2: 日记
│   ├── entities/           # Layer 1: 知识图谱
│   ├── experiences/        # EvoClaw
│   ├── significant/        # EvoClaw
│   ├── reflections/        # EvoClaw
│   ├── proposals/          # EvoClaw
│   └── pipeline/           # EvoClaw
├── soul-revisions/         # SOUL.md 版本快照
└── skills/
    ├── evoclaw/
    └── self-improving/
```

### 依赖技能（2 个）

- **evoclaw** - 身份进化框架（advisory 模式）
- **self-improving** - 自我学习系统

## 配合使用

openclaw-soul 完成后，建议继续使用 [openclaw-setup](https://github.com/Kianzzz/openclaw-setup) 配置技术参数：

```
配置openclaw
```

完整流程：
```
openclaw-soul（灵魂框架 + BOOTSTRAP）
    ↓
openclaw-setup（权限 + 模型 + 扩展 + 安全）
    ↓
正常使用
```

## 版本

当前版本：v1.2.0

## 许可

MIT License

## 作者

Kianzzz

## 相关链接

- GitHub: https://github.com/Kianzzz/openclaw-soul
- openclaw-setup: https://github.com/Kianzzz/openclaw-setup
