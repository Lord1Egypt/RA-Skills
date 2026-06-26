# JIRA工单自动分析处理技能 - 安装指南

## 安全审查结果

### 审查状态: ✅ **批准安装** (P2 - 安全)

### 安全评估摘要
- **代码质量**: 良好，无恶意代码
- **凭证安全**: 密码明文存储（建议使用环境变量）
- **操作安全**: 提供模拟运行模式，需要用户确认
- **风险等级**: 低风险，可控

### 安全建议
1. 首次使用前使用`--dry-run`模式测试
2. 考虑将密码存储在环境变量中
3. 确保JIRA账户有相应权限
4. 定期审查分配规则准确性

## 完整安装步骤

### 步骤1: 检查技能目录
```bash
# 检查技能是否已创建
ls -la ~/.workbuddy/skills/jira-auto-analyze/
```

### 步骤2: 安装依赖
```bash
cd ~/.workbuddy/skills/jira-auto-analyze

# 运行安装脚本
python3 scripts/setup.py

# 或手动安装依赖
pip install playwright
python3 -m playwright install chromium
```

### 步骤3: 配置修改（可选）
编辑配置文件：`config/config.json`
```json
{
  "config": {
    "jira_url": "http://jira.51baiwang.com",
    "filter_id": "13123",
    "username": "liuwei1",          # 修改为你的JIRA用户名
    "password": "Lw@123456",        # 修改为你的JIRA密码
    "rejection_message": "请提供相关环境、通道类型、版本号及日志信息",
    "check_new_only": true
  }
}
```

### 步骤4: 测试运行
```bash
# 模拟运行测试（不实际修改JIRA）
python3 scripts/jira_auto_analyze.py --dry-run

# 查看测试结果，确认分析逻辑正确
```

### 步骤5: 实际执行
```bash
# 实际执行（会修改JIRA数据）
python3 scripts/jira_auto_analyze.py

# 按照提示确认操作
```

## 验证安装

### 1. 检查文件结构
```bash
cd ~/.workbuddy/skills/jira-auto-analyze
find . -type f -name "*.py" | sort
```

预期输出:
```
./scripts/jira_auto_analyze.py
./scripts/setup.py
./scripts/utils.py
```

### 2. 测试导入模块
```bash
python3 -c "from scripts.utils import check_required_fields; print('模块导入成功')"
```

### 3. 测试必填信息检查
```bash
python3 -c "
from scripts.utils import check_required_fields
test_text = '星舰环境，web连接器，版本1.2.3，错误日志'
result = check_required_fields(test_text)
print(f'测试结果: {result[\"is_valid\"]}')
print(f'缺失字段: {result[\"missing_fields\"]}')
"
```

## 配置说明

### 环境变量配置（推荐）
为避免密码明文存储，可以使用环境变量：

```bash
# 设置环境变量
export JIRA_USERNAME="liuwei1"
export JIRA_PASSWORD="Lw@123456"

# 修改脚本使用环境变量
# 在jira_auto_analyze.py中修改：
# self.jira_credentials = {
#     'username': os.environ.get('JIRA_USERNAME', 'liuwei1'),
#     'password': os.environ.get('JIRA_PASSWORD', 'Lw@123456')
# }
```

### 分配规则定制
编辑`config/config.json`中的`rules`数组，添加或修改分配规则：

```json
{
  "rule_name": "新规则名称",
  "keywords": ["关键词1", "关键词2"],
  "assignee": "负责人姓名",
  "jira_username": "jira用户名",
  "reply_message": "回复消息内容"
}
```

## 故障排除

### 常见问题

#### Q1: Playwright安装失败
```bash
# 检查Python版本
python3 --version

# 重新安装
pip uninstall playwright
pip install playwright
python3 -m playwright install chromium
```

#### Q2: JIRA登录失败
1. 检查用户名密码是否正确
2. 检查网络连接
3. 检查JIRA URL是否正确

#### Q3: 页面元素找不到
1. 检查`references/jira_structure.md`中的元素选择器
2. JIRA页面结构可能已更新
3. 可能需要调整等待时间

#### Q4: 权限不足
确保JIRA账户有：
- 查看filter=13123的权限
- 修改工单经办人的权限
- 添加评论的权限

### 日志文件
- `logs/jira_analyze.log`: 执行过程日志
- `logs/operation_log.md`: 操作记录
- `logs/assignment_log.md`: 分配日志

查看日志帮助诊断问题：
```bash
tail -f ~/.workbuddy/skills/jira-auto-analyze/logs/jira_analyze.log
```

## 自动化集成

### 定时执行
可以设置定时任务自动运行：

```bash
# 每天上午9点运行
0 9 * * * cd ~/.workbuddy/skills/jira-auto-analyze && python3 scripts/jira_auto_analyze.py

# 每小时运行一次（仅模拟）
0 * * * * cd ~/.workbuddy/skills/jira-auto-analyze && python3 scripts/jira_auto_analyze.py --dry-run
```

### 在WorkBuddy中自动触发
技能已配置自动触发关键词：
- "自动分析JIRA工单"
- "检查工单信息完整性"
- "JIRA工单自动处理"
- "自动分配工单"

## 卸载说明

如需卸载此技能：

```bash
# 1. 停止所有相关进程
pkill -f "jira_auto_analyze"

# 2. 删除技能目录
rm -rf ~/.workbuddy/skills/jira-auto-analyze

# 3. 清理依赖（可选）
pip uninstall playwright
```

## 技术支持

### 文档参考
- `references/usage_guide.md`: 详细使用指南
- `references/jira_structure.md`: JIRA页面结构参考
- `SKILL.md`: 技能主文档

### 问题反馈
1. 检查日志文件定位问题
2. 使用`--dry-run`模式测试复现
3. 联系技能维护团队

---

**安装完成时间**: 2026年4月3日  
**技能版本**: v1.0.0  
**维护团队**: 进项系统产研团队