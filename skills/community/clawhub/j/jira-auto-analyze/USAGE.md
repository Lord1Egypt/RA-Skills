# JIRA自动分析技能使用指南

## 技能概述

JIRA自动分析技能是一个基于Playwright的浏览器自动化工具，用于自动处理JIRA进项系统线上工单。该技能能够：
1. 自动登录JIRA系统（http://jira.51baiwang.com）
2. 检查工单是否包含四项必填信息
3. 根据工单内容自动分配给相应负责人
4. 自动回复工单处理消息

## 快速开始

### 1. 安装依赖
```bash
# 确保已安装Python 3.7+
python3 --version

# 安装Playwright浏览器自动化框架
python3 -m pip install playwright
python3 -m playwright install chromium
```

### 2. 技能安装
将技能文件夹复制到用户技能目录：
```bash
# 查看用户技能目录
echo ~/.workbuddy/skills/

# 如果目录不存在，创建它
mkdir -p ~/.workbuddy/skills/

# 复制技能文件夹
cp -r jira-auto-analyze ~/.workbuddy/skills/
```

### 3. 在WorkBuddy中加载技能
```bash
# 在WorkBuddy对话中使用以下命令加载技能
use_skill jira-auto-analyze
```

### 4. 运行技能
```bash
# 进入技能目录
cd ~/.workbuddy/skills/jira-auto-analyze

# 运行主脚本（测试模式，不实际操作）
python3 scripts/jira_auto_analyze.py --dry-run

# 运行主脚本（实际模式，自动处理工单）
python3 scripts/jira_auto_analyze.py
```

## 功能详解

### 1. 必填信息检查
技能会检查每个工单是否包含以下四项信息：
- **环境**: 星舰、飞船、云
- **通道类型**: web连接器、rpa、乐企
- **项目版本号**: 如 1.2.3、v2.1.0、版本3.0.0（云工单不需要版本号）
- **相关日志**: 日志、log、trace、error、stack等关键词

### 2. 自动分配规则（按优先级排序）
- **星舰工单** → 崔征明（关键词：星舰，最高优先级）
- **认证相关工单** → 张献文（关键词：认证、勾选、授权、权限、token、登录、Auth）
- **乐企相关工单** → 付强（关键词：乐企、leqi、LEQI）
- **综服通道相关工单** → 魏旭峰（关键词：综服、通道、银行、工行、中行、农行、建行、招行）
- **其他工单** → 刘巍（默认处理人）

**特殊规则**：
- 星舰工单具有最高优先级，一旦发现"星舰"关键词立即处理
- 回复消息：`星舰工单请及时处理，有问题可沟通`
- 如果工单信息不完整，自动退回给提单人并提示规范文档链接

### 3. 自动回复消息
- **信息不完整**: "请依据工单提交规范提交，规范文档链接：http://confluence.51baiwang.com/pages/viewpage.action?pageId=80049485\n\n请补充以下信息：环境（星舰、飞船、云）、通道类型（web连接器、rpa、乐企）、项目版本号、相关日志"
- **星舰工单**: "星舰工单请及时处理，有问题可沟通"
- **认证工单**: "请献文协助处理此工单"
- **乐企工单**: "请付强协助处理此工单"
- **综服工单**: "请旭峰协助处理此工单"
- **其他工单**: "收到，我会及时处理，请稍后"

## 配置文件

配置文件位于 `config/config.json`，包含以下设置：

```json
{
  "rules": [...],  // 分配规则定义
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

## 命令行参数

```bash
# 测试模式，只显示分析结果，不实际执行操作
python3 scripts/jira_auto_analyze.py --dry-run

# 详细输出模式
python3 scripts/jira_auto_analyze.py --verbose

# 指定配置文件路径
python3 scripts/jira_auto_analyze.py --config path/to/config.json

# 只处理特定数量的工单
python3 scripts/jira_auto_analyze.py --limit 5
```

## 技能结构

```
jira-auto-analyze/
├── SKILL.md              # 技能主文档
├── INSTALL.md           # 安装指南
├── USAGE.md            # 使用指南（本文档）
├── config/
│   └── config.json     # 配置文件
├── scripts/
│   ├── jira_auto_analyze.py  # 主脚本
│   ├── utils.py        # 工具函数
│   ├── demo.py         # 演示脚本
│   └── test_functions.py    # 测试脚本
├── references/         # 参考文档
└── assets/            # 资源文件
```

## 演示脚本

查看技能功能演示：
```bash
python3 scripts/demo.py
```

演示脚本会展示：
- 必填信息检查功能
- 规则匹配与自动分配
- 完整工单处理流程

## 常见问题

### Q1: 技能无法连接到JIRA
- 检查网络连接
- 验证JIRA地址是否正确：http://jira.51baiwang.com
- 确认用户名密码是否正确

### Q2: Playwright安装失败
- 确保已安装Python 3.7+
- 尝试重新安装：`python3 -m pip install --upgrade playwright`
- 手动下载Chromium：`python3 -m playwright install chromium`

### Q3: 技能无法找到工单
- 确认filter_id是否正确（13123）
- 检查JIRA页面结构是否变化
- 使用--verbose参数查看详细输出

### Q4: 如何修改分配规则
编辑 `config/config.json` 文件中的 `rules` 部分，添加或修改规则。

## 安全注意事项

1. **密码安全**: 配置文件中的密码以明文存储，建议定期更换
2. **操作确认**: 首次使用时建议使用 `--dry-run` 参数测试
3. **权限控制**: 确保只有授权人员可以访问技能配置
4. **日志记录**: 技能会自动记录操作日志，便于审计

## 更新与维护

### 更新技能
```bash
cd ~/.workbuddy/skills/jira-auto-analyze
git pull  # 如果使用git管理
# 或手动复制新版本文件
```

### 检查更新
```bash
python3 scripts/jira_auto_analyze.py --check-update
```

### 反馈与支持
如有问题或建议，请联系技能开发者。

---

**版本**: 1.0.0  
**最后更新**: 2026-04-03  
**适用系统**: macOS, Linux, Windows  
**依赖**: Python 3.7+, Playwright, Chromium