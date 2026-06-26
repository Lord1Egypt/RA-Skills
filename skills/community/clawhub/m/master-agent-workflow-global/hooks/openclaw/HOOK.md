# OpenClaw钩子集成指南

## 概述

本钩子处理器允许 `master-agent-workflow-global` 技能与OpenClaw深度集成，提供自动触发、命令解析和配置管理功能。

## 功能特性

### ✅ 自动触发
- 检测关键词自动触发技能
- 支持多种触发方式
- 智能命令解析

### ✅ 命令处理
- 完整的命令系统
- 参数和选项解析
- 上下文感知处理

### ✅ 配置管理
- 配置文件的加载和保存
- 模板系统集成
- 迁移工具支持

### ✅ 错误处理
- 完善的错误处理机制
- 友好的错误提示
- 日志记录

## 集成方式

### 1. 自动注册
当技能安装时，钩子处理器会自动注册到OpenClaw系统中。

### 2. 消息处理流程
```
用户消息 → OpenClaw → 钩子处理器 → 技能处理 → 返回结果
```

### 3. 触发条件
钩子处理器会检测以下关键词：
- "使用 master-agent-workflow-global"
- "maw " (快捷命令)
- "master-agent-workflow"
- "主控代理工作流"

## 命令系统

### 命令结构
```
使用 master-agent-workflow-global [命令] [参数] [--选项 值]
```

### 可用命令

#### execute - 执行任务
```bash
使用 master-agent-workflow-global execute "任务描述" --max-workers 10 --timeout 2h
```

#### configure - 配置管理
```bash
# 列出配置
使用 master-agent-workflow-global configure list

# 保存配置
使用 master-agent-workflow-global configure save my-config --max-workers 8 --timeout 4h
```

#### template - 模板管理
```bash
# 列出模板
使用 master-agent-workflow-global template list
```

#### migrate - 迁移工具
```bash
# 导出配置
使用 master-agent-workflow-global migrate export --output config.json

# 导入配置
使用 master-agent-workflow-global migrate import config.json
```

#### help - 帮助信息
```bash
使用 master-agent-workflow-global help
```

## 配置选项

### 执行选项
| 选项 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| --max-workers | number | 5 | 最大并行工作代理数 |
| --timeout | string | 3h | 主控代理超时时间 |
| --worker-timeout | string | 30m | 工作代理超时时间 |
| --template | string | - | 使用预定义模板 |
| --config | string | default | 使用指定配置 |
| --dry-run | boolean | false | 试运行，不实际执行 |

### 迁移选项
| 选项 | 类型 | 说明 |
|------|------|------|
| --output | string | 导出文件路径 |
| --include-state | boolean | 包含运行状态 |
| --exclude-state | boolean | 排除运行状态 |

## 配置文件

### 配置位置
```
~/.openclaw/global-skills/master-agent-workflow/config/
├── default.json          # 默认配置
├── my-config.json        # 自定义配置
└── ...
```

### 配置格式
```json
{
  "max_workers": 5,
  "timeout_hours": 3,
  "worker_timeout_minutes": 30,
  "stuck_threshold_minutes": 15,
  "fail_threshold": 10,
  "auto_cleanup": true,
  "report_channel": "feishu"
}
```

## 模板系统

### 模板位置
```
~/.openclaw/global-skills/master-agent-workflow/templates/
├── file_processing.json  # 文件处理模板
├── api_calling.json      # API调用模板
└── ...
```

### 模板格式
```json
{
  "name": "file_processing",
  "description": "文件处理模板",
  "config": {
    "max_workers": 5,
    "worker_timeout_minutes": 45,
    "task_type": "file"
  }
}
```

## 开发指南

### 扩展命令
要添加新命令，在 `handler.js` 中添加：
1. 在 `processCommand` 方法中添加case
2. 实现对应的处理方法
3. 更新帮助文本

### 添加配置选项
在 `loadConfig` 方法中添加新的配置项：
```javascript
const defaultConfig = {
  // 现有配置...
  new_option: 'default_value'
};
```

### 自定义触发条件
修改 `shouldTrigger` 方法：
```javascript
shouldTrigger(text) {
  const triggers = [
    // 现有触发词...
    '新的触发词'
  ];
  
  return triggers.some(trigger => text.includes(trigger));
}
```

## 调试

### 启用调试日志
```bash
export DEBUG=maw-hook*
```

### 查看处理流程
钩子处理器会在以下目录生成日志：
```
~/.openclaw/global-skills/master-agent-workflow/logs/
```

### 测试钩子
```bash
# 直接测试处理器
node -e "const Handler = require('./handler.js'); const h = new Handler(); console.log(h.shouldTrigger('使用 master-agent-workflow-global 测试'))"
```

## 故障排除

### 常见问题

#### Q1: 钩子未触发
**原因**: 触发词不匹配或钩子未正确注册
**解决**: 
1. 检查触发词配置
2. 重新安装技能
3. 查看OpenClaw日志

#### Q2: 命令解析错误
**原因**: 命令格式不正确
**解决**:
1. 使用正确的命令格式
2. 查看帮助信息
3. 检查参数和选项

#### Q3: 配置加载失败
**原因**: 配置文件损坏或权限问题
**解决**:
1. 检查配置文件格式
2. 验证文件权限
3. 使用默认配置

### 获取帮助
```bash
# 查看钩子状态
使用 master-agent-workflow-global help

# 查看日志
cat ~/.openclaw/global-skills/master-agent-workflow/logs/hook.log
```

## 性能优化

### 缓存策略
钩子处理器使用内存缓存：
- 配置缓存：减少文件读取
- 模板缓存：提高模板加载速度
- 结果缓存：避免重复计算

### 懒加载
- 按需加载配置和模板
- 延迟初始化资源
- 动态导入模块

### 资源清理
- 自动清理临时文件
- 定期清理日志
- 内存泄漏检测

## 安全考虑

### 输入验证
- 所有用户输入都经过验证
- 防止命令注入
- 路径遍历保护

### 权限控制
- 配置文件权限限制
- 执行环境隔离
- 资源访问控制

### 数据保护
- 敏感配置加密
- 日志脱敏
- 安全传输

---
**钩子版本**: 2.0.0  
**最后更新**: 2026-03-27  
**兼容性**: OpenClaw >= 1.0.0