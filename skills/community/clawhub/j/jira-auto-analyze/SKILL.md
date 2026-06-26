---
name: jira-auto-analyze
description: 此技能用于自动分析JIRA进项系统线上工单（filter=13123），检查工单内容是否包含四项必填信息，并根据工单内容自动分配给相应的经办人。当用户需要自动处理JIRA新工单、检查工单信息完整性、或根据规则自动分配任务时使用此技能。
---

# 📋 JIRA工单自动分析处理技能

## 概述

此技能实现JIRA进项系统线上工单的自动化处理流程，包括：
1. **自动检查工单信息完整性**：验证是否包含环境、通道类型、版本号、日志四项必填信息
2. **智能分配工单**：根据工单内容自动分配给相应负责人
3. **自动回复处理**：对处理结果进行自动回复

## 使用场景

### 自动触发场景
在WorkBuddy中输入以下关键词时自动加载：
- "自动分析JIRA工单"
- "检查工单信息完整性"
- "JIRA工单自动处理"
- "工单信息检查"
- "自动分配工单"
- "处理新工单"
- "JIRA自动化处理"

### 具体应用场景
1. **新工单自动处理**：新创建的工单自动检查信息完整性并分配
2. **信息验证**：确保工单包含必要的技术信息
3. **团队协作**：根据业务规则自动分配给相应负责人
4. **流程标准化**：统一工单处理流程和回复标准

## 核心功能

### 1. 必填信息检查
自动检查工单是否包含以下四项信息：
- **环境**：星舰、飞船、云（三选一）
- **通道类型**：web连接器、rpa、乐企（三选一）
- **项目版本号**：版本号格式（如1.2.3、v2、版本5等）
  - *特殊规则*：如果是"云"环境，则不需要版本号
- **相关日志**：日志、log、trace、error、stack等关键词

### 2. 自动处理规则
- **信息不全的工单**：自动打回给联系人，要求补充信息
- **信息完整的工单**：根据内容自动分配给相应负责人

### 3. 分配规则
1. **星舰工单** → 崔征明（关键词：星舰，优先级最高）
2. **认证相关工单** → 张献文（关键词：认证、勾选、授权等）
3. **乐企相关工单** → 付强（关键词：乐企、leqi等）
4. **综服通道相关工单** → 魏旭峰（关键词：综服、通道、银行等）
5. **其他工单** → 刘巍（默认处理）

**优先级说明**：
- 星舰工单具有最高优先级，一旦发现"星舰"关键词立即分配给崔征明
- 其他规则按关键词匹配分数排序
- 如果工单信息不完整，自动退回给提单人并提示规范文档链接

## 使用方法

### 在WorkBuddy中使用
当用户提到相关关键词时，自动加载此技能并执行：
```bash
# 自动执行分析处理
python3 scripts/jira_auto_analyze.py

# 模拟运行（不实际修改JIRA）
python3 scripts/jira_auto_analyze.py --dry-run
```

### 命令行使用
```bash
# 进入技能目录
cd ~/.workbuddy/skills/jira-auto-analyze

# 安装依赖（首次使用）
python3 scripts/setup.py

# 执行自动分析处理
python3 scripts/jira_auto_analyze.py

# 模拟运行模式
python3 scripts/jira_auto_analyze.py --dry-run

# 使用自定义配置文件
python3 scripts/jira_auto_analyze.py --config /path/to/config.json
```

## 技术架构

### 文件结构
```
jira-auto-analyze/
├── SKILL.md                    # 技能文档（本文件）
├── scripts/
│   ├── jira_auto_analyze.py    # 核心分析处理脚本
│   ├── utils.py                # 工具函数库
│   └── setup.py                # 安装脚本
├── config/
│   └── config.json             # 配置文件
├── references/
│   ├── jira_structure.md       # JIRA页面结构参考
│   └── usage_guide.md          # 详细使用指南
└── logs/                       # 日志目录
    ├── jira_analyze.log        # 执行日志
    ├── operation_log.md        # 操作记录
    └── assignment_log.md       # 分配日志
```

### 依赖环境
- Python 3.7+
- Playwright (浏览器自动化框架)
- Chromium浏览器

## 执行流程

### 1. 登录JIRA
- 访问 http://jira.51baiwang.com
- 使用配置的用户名密码登录
- 验证登录状态

### 2. 访问工单列表
- 导航到 filter=13123 页面
- 提取所有工单信息
- 默认只处理"新建"状态的工单

### 3. 分析工单内容
对于每个工单：
1. 提取工单标题和描述
2. 检查四项必填信息
3. 标记工单为有效或无效

### 4. 确定处理方式
- **无效工单**：准备打回评论
- **有效工单**：根据关键词匹配分配规则

### 5. 执行处理
- **打回工单**：添加评论要求补充信息
- **分配工单**：修改经办人字段并添加回复

### 6. 记录日志
- 记录所有操作结果
- 包含详细的操作信息

## 配置说明

### JIRA配置
```json
"config": {
  "jira_url": "http://jira.51baiwang.com",  // JIRA地址
  "filter_id": "13123",                     // 工单filter ID
  "username": "liuwei1",                    // 登录用户名
  "password": "Lw@123456",                  // 登录密码
  "rejection_message": "请提供相关环境、通道类型、版本号及日志信息",  // 打回消息
  "check_new_only": true                    // 只处理新工单
}
```

### 规则配置
每个规则包含：
- `rule_name`: 规则名称
- `keywords`: 匹配关键词列表
- `assignee`: 负责人姓名
- `jira_username`: JIRA用户名
- `reply_message`: 回复消息

## 安全注意事项

1. **密码安全**: JIRA密码存储在配置文件中，请确保文件安全
2. **操作权限**: 需要JIRA账户有修改工单和添加评论的权限
3. **操作确认**: 默认会显示分析结果，需要确认后才执行实际操作
4. **模拟运行**: 首次使用时建议使用`--dry-run`参数进行测试

## 故障排除

### 常见问题
1. **Playwright安装失败**: 检查Python版本，重新安装Playwright和Chromium
2. **JIRA登录失败**: 检查用户名密码和网络连接
3. **页面元素找不到**: JIRA页面结构可能已更新，检查选择器
4. **工单提取失败**: 检查filter ID和工单表格结构

### 日志文件
- `logs/jira_analyze.log`: 执行日志
- `logs/operation_log.md`: 操作记录
- `logs/assignment_log.md`: 分配日志

## 扩展与定制

### 添加新规则
编辑`config/config.json`文件，在`rules`数组中添加新规则：
```json
{
  "rule_name": "新规则名称",
  "keywords": ["关键词1", "关键词2"],
  "assignee": "负责人姓名",
  "jira_username": "jira用户名",
  "reply_message": "回复消息内容"
}
```

### 修改必填信息检查规则
修改`scripts/utils.py`中的`check_required_fields`函数，调整关键词或正则表达式。

### 调整匹配算法
修改`scripts/utils.py`中的`calculate_match_score`函数，调整匹配分数计算逻辑。

---

**创建时间**: 2026年4月3日  
**适用系统**: JIRA 51baiwang内部系统  
**技术依赖**: Python + Playwright + Chromium  
**维护团队**: 进项系统产研团队
