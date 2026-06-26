# NVS Node Version Switcher Skill - 创建完成

## 🎉 技能创建成功！

我已经成功创建了一个完整的 NVS (Node Version Switcher) 技能，该技能可以帮助你管理不同环境的 Node.js 版本。

## 📁 技能结构

```
.lingma/skills/nvs-node-version-switcher/
├── SKILL.md              # 主要技能文档（179行，符合最佳实践）
├── REFERENCE.md          # 详细命令参考
├── EXAMPLES.md           # 实用示例和工作流
├── README.md             # 技能使用说明
└── scripts/              # 实用脚本
    ├── check_nvs_status.sh   # 检查 NVS 安装状态
    ├── install_nvs.sh        # 自动安装 NVS
    └── validate_skill.sh     # 验证技能结构
```

## ✅ 已实现的功能

### 1. 跨平台安装支持
- **Windows**: winget、chocolatey、手动安装
- **macOS/Linux**: git clone + shell 脚本安装
- **自动检测**: 智能识别操作系统并提供相应安装方法

### 2. NVS 核心功能掌握
- ✅ 版本安装 (`nvs add`)
- ✅ 版本切换 (`nvs use`)
- ✅ 默认设置 (`nvs link`)
- ✅ 版本列表 (`nvs ls`, `nvs ls-remote`)
- ✅ 自动切换 (`nvs auto`)
- ✅ 别名管理 (`nvs alias`)
- ✅ 远程配置 (`nvs remote`)
- ✅ 包迁移 (`nvs migrate`)

### 3. 智能环境处理
- 自动检测 NVS 是否已安装
- 未安装时提供自动安装方案
- 支持不同 shell 环境（bash、zsh、PowerShell、cmd）

## 🚀 使用方法

### 快速开始
1. **检查 NVS 状态**：
   ```bash
   nvs --version
   ```

2. **如果未安装，使用自动安装脚本**：
   ```bash
   .lingma/skills/nvs-node-version-switcher/scripts/install_nvs.sh
   ```

3. **安装和使用 Node.js 版本**：
   ```bash
   nvs add lts      # 安装最新 LTS 版本
   nvs use lts      # 使用该版本
   ```

### Lingma 集成
当你在对话中提到以下情况时，此技能会自动激活：
- "我需要切换 Node.js 版本"
- "如何安装特定版本的 Node.js"
- "NVS 怎么使用"
- "项目需要不同的 Node.js 版本"
- 任何与 Node.js 版本管理相关的问题

## 📋 技能特点

### 遵循最佳实践
- ✅ SKILL.md 保持在 500 行以内（实际 179 行）
- ✅ 描述具体且包含触发词（276 字符）
- ✅ 使用渐进式披露（详细信息在参考文件中）
- ✅ 提供实用脚本和示例
- ✅ 跨平台兼容性

### 内容丰富
- **完整命令参考**：所有 NVS 命令的详细说明
- **实际示例**：真实场景的使用案例
- **工作流指导**：项目设置、版本升级等常见流程
- **故障排除**：常见问题和解决方案

## 🔧 实用脚本

### check_nvs_status.sh
检查 NVS 安装状态和当前 Node.js 版本信息

### install_nvs.sh  
自动检测系统并安装 NVS（支持 Mac/Linux）

### validate_skill.sh
验证技能文件结构和内容完整性

## 🎯 适用场景

1. **多项目管理**：不同项目需要不同 Node.js 版本
2. **版本测试**：测试应用在不同 Node.js 版本下的兼容性
3. **团队协作**：确保团队使用统一的 Node.js 版本
4. **CI/CD 集成**：在持续集成环境中管理 Node.js 版本
5. **开发环境设置**：快速配置新的开发环境

## 📖 学习资源

技能基于官方 NVS 仓库 (https://github.com/jasongin/nvs) 创建，包含：
- 官方文档的核心内容
- 跨平台安装指南
- 完整的命令参考
- 实际使用示例

## ✨ 下一步

你现在可以：
1. 在任何需要 Node.js 版本管理的场景中调用此技能
2. 使用提供的脚本自动化常见任务
3. 根据具体项目需求定制版本管理策略
4. 将技能分享给团队成员使用

技能已经完全就绪，可以立即使用！🎊
