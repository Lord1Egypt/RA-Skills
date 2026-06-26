# 技能模板：master-agent-workflow-global

这是一个标准的OpenClaw技能模板，用于创建类似的可迁移全局技能。

## 目录结构

```
技能名称-global/
├── .clawhub/                    # ClawdHub元数据
│   └── origin.json             # 发布信息
├── assets/                      # 资源文件
│   ├── LEARNINGS.md            # 学习记录
│   └── SKILL-TEMPLATE.md       # 本文件
├── hooks/                       # 钩子脚本
│   └── openclaw/
│       ├── handler.js          # JavaScript处理器
│       ├── handler.ts          # TypeScript处理器
│       └── HOOK.md             # 钩子文档
├── references/                  # 参考文档
│   ├── examples.md             # 使用示例
│   ├── hooks-setup.md          # 钩子设置
│   └── openclaw-integration.md # OpenClaw集成
├── scripts/                     # 脚本文件
│   ├── activator.sh            # 激活脚本
│   ├── error-detector.sh       # 错误检测
│   └── extract-skill.sh        # 技能提取
├── SKILL.md                     # 技能主文档
├── skill.json                   # 技能元数据
└── _meta.json                   # 元数据文件
```

## 核心文件说明

### 1. skill.json (必需)
技能的核心元数据文件，包含：
- 名称、版本、描述
- 作者、许可证信息
- 依赖关系声明
- 配置架构定义
- 示例和模板

### 2. SKILL.md (必需)
技能的详细文档，包含：
- 技能概述和适用场景
- 安装和使用说明
- 配置参数说明
- 示例代码
- 故障排除

### 3. .clawhub/origin.json (推荐)
ClawdHub发布信息，包含：
- 发布元数据
- 兼容性信息
- 安装方式
- 依赖关系

### 4. 脚本文件 (可选)
- `install.sh` - 安装脚本
- `uninstall.sh` - 卸载脚本
- `migrate.sh` - 迁移脚本

## 配置最佳实践

### 外部化配置
```json
{
  "configSchema": {
    "param1": {
      "type": "string",
      "default": "value",
      "description": "参数说明"
    }
  }
}
```

### 依赖声明
```json
{
  "requirements": {
    "openclaw": ">=1.0.0",
    "tools": ["tool1", "tool2"]
  }
}
```

### 模板系统
```json
{
  "templates": {
    "template1": {
      "name": "模板名称",
      "description": "模板描述",
      "config": {}
    }
  }
}
```

## 迁移支持

### 导出功能
```bash
# 导出配置
技能名称 export --output config.json

# 导出完整状态
技能名称 export-full --include-state --output backup.tar.gz
```

### 导入功能
```bash
# 导入配置
技能名称 import --file config.json

# 导入完整状态
技能名称 import-full --file backup.tar.gz --restore-state
```

## 跨平台考虑

### 路径处理
```bash
# 使用环境变量
INSTALL_DIR="${MAW_HOME:-$HOME/.openclaw/global-skills/技能名称}"

# 平台检测
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux处理
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS处理
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows处理
fi
```

### 文件权限
```bash
# 设置执行权限
chmod +x scripts/*.sh

# Windows兼容性
if [ "$OS" = "windows" ]; then
    # 使用.bat文件
fi
```

## 测试策略

### 单元测试
```bash
# 测试安装
./install.sh --dry-run

# 测试配置
技能名称 validate-config --file config.json

# 测试功能
技能名称 test --scenario basic
```

### 集成测试
```bash
# 测试OpenClaw集成
openclaw test-skill 技能名称

# 测试迁移
技能名称 test-migration --from v1.0.0 --to v2.0.0
```

## 发布流程

### 1. 版本管理
```bash
# 更新版本号
更新 skill.json 中的 version 字段

# 生成变更日志
生成 CHANGELOG.md
```

### 2. 打包
```bash
# 创建发布包
tar -czf 技能名称-v版本号.tar.gz \
  --exclude=".git" \
  --exclude="node_modules" \
  --exclude="*.log" \
  技能名称-global/
```

### 3. 发布
```bash
# 发布到ClawdHub
clawdhub publish \
  --name "技能名称" \
  --version "版本号" \
  --description "描述" \
  技能名称-v版本号.tar.gz
```

## 维护指南

### 版本兼容性
- 保持向后兼容性
- 提供迁移工具
- 明确弃用计划

### 文档更新
- 每次变更更新文档
- 保持示例代码最新
- 记录已知问题

### 用户支持
- 提供故障排除指南
- 收集用户反馈
- 定期更新技能

## 示例配置

### 完整skill.json示例
```json
{
  "name": "技能名称-global",
  "version": "1.0.0",
  "description": "技能描述",
  "author": "作者",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/用户名/仓库.git"
  },
  "requirements": {
    "openclaw": ">=1.0.0"
  },
  "configSchema": {
    "param1": {
      "type": "string",
      "default": "default",
      "description": "参数说明"
    }
  },
  "templates": {
    "basic": {
      "name": "基础模板",
      "description": "基础使用模板"
    }
  },
  "examples": [
    {
      "name": "快速开始",
      "description": "快速开始示例",
      "code": "使用 技能名称 执行任务"
    }
  ]
}
```

---
**模板版本**: 1.0.0  
**最后更新**: 2026-03-27  
**基于**: master-agent-workflow-global v2.0.0