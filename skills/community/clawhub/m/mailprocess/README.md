# Mali App Builder Skill

## 📖 简介

Mali App Builder (码力搭建助手) 是一个可以在 ducc 和 zulu 上安装运行的 Skill，用于快速调用码力搭建平台完成应用搭建。

## 📁 项目结构

```
mali-builder/
├── SKILL.md                          # Skill 定义文档（核心文件）
├── README.md                         # 使用说明（本文件）
└── scripts/                          # 脚本目录
    ├── install-to-ducc.sh           # ducc 安装脚本
    ├── launch-mali-builder.py       # Python 启动脚本
    └── launch-mali-builder.sh       # Bash 启动脚本
```

## 🚀 快速安装

### 方式 1: 使用安装脚本（推荐）

```bash
cd mali-builder
./scripts/install-to-ducc.sh
```

脚本会引导你选择以下三种安装方式之一：
1. 通过 ducc CLI 安装（自动化）
2. 手动上传到 ducc 管理界面
3. 生成配置文件供后续使用

### 方式 2: 直接使用脚本

```bash
# 使用 Python 脚本（推荐）
./scripts/launch-mali-builder.py "创建一个任务管理系统"

# 使用 Bash 脚本
./scripts/launch-mali-builder.sh "创建一个员工信息管理系统"
```

## 💡 核心功能

1. 🌐 **自动打开浏览器** - 自动启动 Chrome 浏览器
2. 🔗 **访问码力平台** - 导航到 https://lowcode.baidu-int.com/ai-coding
3. ✍️ **智能需求传递** - 自动填充用户需求到输入框
4. 🚀 **触发搭建流程** - 自动点击发送按钮开始搭建

## 📋 使用场景

### ✅ 适合场景
- 内部管理系统（任务管理、员工信息、审批流程）
- 数据展示看板（销售数据、运营指标、业务报表）
- 表单收集系统（问卷调查、信息采集、活动报名）
- 快速原型验证（产品 Demo、功能演示）

### ❌ 不适合场景
- 需要复杂业务逻辑的核心系统
- 对性能要求极高的应用
- 需要深度 UI 定制的产品

## 🛠️ 安装要求

### 必需
- Google Chrome 浏览器（最新版本）
- 公司内网或 VPN 连接
- Python 3.x 环境

### 可选（用于完整自动化）
- macOS 系统
- Chrome 开启 "允许 Apple 事件中的 JavaScript" 权限

## 📦 打包说明

### 手动打包

```bash
cd mali-builder

# 打包为 zip（推荐用于 ducc 上传）
zip -r mali-builder.zip SKILL.md scripts/ README.md
```

### 使用安装脚本打包

```bash
./scripts/install-to-ducc.sh
# 选择选项 2（手动上传）
# 会自动生成 mali-builder.zip
```

## 🔧 配置说明

### Skill 配置（SKILL.md）

```yaml
name: mali-builder
description: |
  Mali App Builder (码力搭建助手) - 自动化低代码应用搭建技能
  
触发关键词:
  - 码力搭建
  - mali
  - 低代码搭建
  - 搭建应用
  - 创建应用
```

### 执行入口

```bash
python3 scripts/launch-mali-builder.py "$USER_QUERY"
```

## 📚 使用示例

### 示例 1: 任务管理系统

```bash
./scripts/launch-mali-builder.py "创建一个任务管理系统，包含：
1. 任务列表（标题、状态、优先级、截止日期）
2. 添加/编辑/删除任务
3. 标记完成/未完成
4. 按状态筛选
5. 搜索功能"
```

### 示例 2: 投票系统

```bash
./scripts/launch-mali-builder.py "创建一个投票系统，包含：
1. 创建投票（标题、描述、多个选项）
2. 投票列表展示
3. 参与投票并提交
4. 实时查看投票结果
5. 使用邮箱防止重复投票"
```

## 🐛 故障排查

### 问题 1: 权限被拒绝

```bash
chmod +x scripts/*.sh scripts/*.py
```

### 问题 2: Chrome 未自动打开

- 检查 Chrome 是否安装
- macOS: 授予终端控制浏览器的权限

### 问题 3: 需求未自动填充

- macOS: 在 Chrome 中开启 "允许 Apple 事件中的 JavaScript"
- 其他系统: 手动复制需求并粘贴

## 🎯 集成到 ducc/zulu

### ducc 集成

1. 上传 Skill 文件到 ducc 平台
2. 配置触发关键词
3. 设置执行入口为 `scripts/launch-mali-builder.py`

### zulu 集成

```
用户: 帮我用码力搭建一个投票系统
zulu: [自动触发 mali-builder skill]
      → 浏览器打开
      → 需求自动填充
      → 开始搭建
```

## 📞 获取帮助

如有问题，请：
1. 查看 SKILL.md 中的详细说明
2. 检查故障排查部分
3. 联系码力搭建平台支持团队

---

**版本**: v1.0.0  
**最后更新**: 2026-03-02  
**状态**: ✅ 生产就绪