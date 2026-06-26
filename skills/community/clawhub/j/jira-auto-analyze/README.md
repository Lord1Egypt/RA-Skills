# JIRA工单自动分析处理技能

## 快速开始

### 1. 安装依赖
```bash
cd ~/.workbuddy/skills/jira-auto-analyze
python3 scripts/setup.py
```

### 2. 配置修改（可选）
编辑配置文件：`config/config.json`
- 修改JIRA用户名密码
- 调整分配规则
- 自定义回复消息

### 3. 测试运行
```bash
# 模拟运行（不实际修改JIRA）
python3 scripts/jira_auto_analyze.py --dry-run

# 实际执行
python3 scripts/jira_auto_analyze.py
```

## 功能特点

✅ **自动检查工单信息完整性**
- 环境（星舰、飞船、云）
- 通道类型（web连接器、rpa、乐企）
- 项目版本号（云环境除外）
- 相关日志信息

✅ **智能分配工单**
- 认证相关工单 → 张献文
- 乐企相关工单 → 付强
- 综服通道工单 → 魏旭峰
- 其他工单 → 刘巍

✅ **自动回复处理**
- 信息不全：自动打回要求补充
- 信息完整：分配后自动回复

✅ **详细日志记录**
- 执行过程日志
- 操作结果记录
- 错误追踪信息

## 使用示例

### 场景1：处理新工单
```bash
# 执行自动分析处理
python3 scripts/jira_auto_analyze.py

# 输出示例：
📊 JIRA工单分析处理结果
📋 发现 5 个工单
   - 新工单: 3
   - 有效工单: 2
   - 需打回工单: 1
```

### 场景2：模拟测试
```bash
# 模拟运行测试
python3 scripts/jira_auto_analyze.py --dry-run

# 查看分析结果，不实际修改JIRA
```

## 配置文件说明

### 主要配置项
```json
{
  "config": {
    "jira_url": "http://jira.51baiwang.com",
    "filter_id": "13123",
    "username": "liuwei1",
    "password": "Lw@123456",
    "rejection_message": "请提供相关环境、通道类型、版本号及日志信息",
    "check_new_only": true
  }
}
```

### 分配规则配置
```json
{
  "rules": [
    {
      "rule_name": "认证相关工单",
      "keywords": ["认证", "勾选", "授权"],
      "assignee": "张献文",
      "jira_username": "zhangxianwen",
      "reply_message": "请献文协助处理此工单"
    }
    // ... 更多规则
  ]
}
```

## 常见问题

### Q1: 如何修改JIRA账号密码？
A: 编辑`config/config.json`文件，修改`username`和`password`字段。

### Q2: 如何添加新的分配规则？
A: 在`config/config.json`的`rules`数组中添加新规则对象。

### Q3: Playwright安装失败怎么办？
A: 运行以下命令重新安装：
```bash
pip uninstall playwright
pip install playwright
python3 -m playwright install chromium
```

### Q4: 如何只查看分析结果而不执行？
A: 使用`--dry-run`参数：
```bash
python3 scripts/jira_auto_analyze.py --dry-run
```

## 文件结构

```
jira-auto-analyze/
├── README.md                 # 本文件
├── SKILL.md                  # 技能主文档
├── scripts/
│   ├── jira_auto_analyze.py  # 核心脚本
│   ├── utils.py              # 工具函数
│   └── setup.py              # 安装脚本
├── config/
│   └── config.json           # 配置文件
├── references/
│   ├── jira_structure.md     # JIRA结构参考
│   └── usage_guide.md        # 详细指南
└── logs/                     # 日志目录
```

## 技术支持

- **问题反馈**: 检查`logs/`目录下的日志文件
- **配置问题**: 参考`references/usage_guide.md`
- **技术细节**: 查看`references/jira_structure.md`

## 版本历史

- v1.0.0 (2026-04-03): 初始版本发布
  - 实现四项必填信息检查
  - 实现自动分配规则
  - 实现自动回复功能
  - 添加详细日志记录

---

**注意**: 首次使用前请确保已正确安装所有依赖，并建议先使用`--dry-run`模式进行测试。