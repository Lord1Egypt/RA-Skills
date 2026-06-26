# JIRA工单自动分析处理使用指南

## 技能概述

此技能用于自动分析JIRA进项系统线上工单（filter=13123），检查工单内容是否包含四项必填信息，并根据工单内容自动分配给相应的经办人。

## 核心功能

### 1. 必填信息检查
自动检查工单是否包含以下四项信息：
- **环境**：星舰、飞船、云（三选一）
- **通道类型**：web连接器、rpa、乐企（三选一）
- **项目版本号**：版本号格式（如1.2.3、v2、版本5等）
  - 特殊规则：如果是"云"环境，则不需要版本号
- **相关日志**：日志、log、trace、error、stack等关键词

### 2. 自动处理规则
- **信息不全的工单**：自动打回给联系人，要求补充信息
- **信息完整的工单**：根据内容自动分配给相应负责人

### 3. 分配规则
1. **认证相关工单** → 张献文（关键词：认证、勾选、授权等）
2. **乐企相关工单** → 付强（关键词：乐企、leqi等）
3. **综服通道相关工单** → 魏旭峰（关键词：综服、通道、银行等）
4. **其他工单** → 刘巍（默认处理）

## 安装与配置

### 1. 依赖安装
```bash
# 安装Python依赖
pip install playwright

# 安装Chromium浏览器
python3 -m playwright install chromium
```

### 2. 配置文件
配置文件位于：`config/config.json`

```json
{
  "rules": [
    {
      "rule_name": "认证相关工单",
      "keywords": ["认证", "勾选", "授权", "权限", "token", "登录", "Auth"],
      "assignee": "张献文",
      "jira_username": "zhangxianwen",
      "reply_message": "请献文协助处理此工单"
    },
    // ... 其他规则
  ],
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

### 3. 修改配置
如果需要修改JIRA账号密码或分配规则，编辑`config/config.json`文件。

## 使用方法

### 1. 命令行使用
```bash
# 执行自动分析处理（实际执行）
python3 scripts/jira_auto_analyze.py

# 模拟运行模式（不实际修改JIRA）
python3 scripts/jira_auto_analyze.py --dry-run

# 使用自定义配置文件
python3 scripts/jira_auto_analyze.py --config /path/to/config.json
```

### 2. 在WorkBuddy中使用
当用户提到以下关键词时，自动加载此技能：
- "自动分析JIRA工单"
- "检查工单信息完整性"
- "JIRA工单自动处理"
- "工单信息检查"
- "自动分配工单"

## 执行流程详解

### 步骤1：登录JIRA
- 访问 http://jira.51baiwang.com
- 使用配置的用户名密码登录
- 验证登录状态

### 步骤2：访问工单列表
- 导航到 filter=13123 页面
- 提取所有工单信息
- 默认只处理"新建"状态的工单

### 步骤3：分析工单内容
对于每个工单：
1. 提取工单标题和描述
2. 检查四项必填信息
3. 标记工单为有效或无效

### 步骤4：确定处理方式
- **无效工单**：准备打回评论
- **有效工单**：根据关键词匹配分配规则

### 步骤5：执行处理
- **打回工单**：添加评论要求补充信息
- **分配工单**：修改经办人字段并添加回复

### 步骤6：记录日志
- 记录所有操作结果
- 包含详细的操作信息

## 输出示例

### 分析结果示例
```
📊 JIRA工单分析处理结果
===========================================================

📋 发现 8 个工单
   - 新工单: 5
   - 有效工单: 3
   - 需打回工单: 2

❌ 需要打回的工单:
-----------------------------------------------------------
XS-43509 - 【工行】综服，发票勾选认证失败...
  缺少信息: 项目相关服务模块版本号, 相关日志信息

✅ 有效的工单:
-----------------------------------------------------------
XS-43528 - 【中行】综服，v1.2.3版本，日志文件...
  匹配规则: 综服通道相关工单
  建议分配: 魏旭峰
  回复内容: 请旭峰协助处理此工单
```

### 最终统计示例
```
🎯 处理完成
===========================================================

📊 最终统计:
- 总工单数: 8
- 新工单数: 5
- 有效工单: 3
- 打回工单: 2
- 分配工单: 3
- 处理工单: 5
```

## 故障排除

### 常见问题

#### 1. Playwright安装失败
```bash
# 检查Python版本
python3 --version

# 重新安装Playwright
pip uninstall playwright
pip install playwright

# 重新安装浏览器
python3 -m playwright install chromium
```

#### 2. JIRA登录失败
- 检查用户名密码是否正确
- 检查网络连接
- 检查JIRA URL是否正确

#### 3. 页面元素找不到
- JIRA页面结构可能已更新
- 检查`references/jira_structure.md`中的元素选择器
- 可能需要调整选择器或等待时间

#### 4. 工单提取失败
- 检查filter ID是否正确
- 检查工单表格结构
- 可能需要调整等待时间

### 日志文件
- 执行日志：`logs/jira_analyze.log`
- 操作日志：`logs/operation_log.md`
- 错误日志：检查日志文件中的错误信息

## 配置选项详解

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