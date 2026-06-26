# 👔 HR 智能体

> 面向中小企业（50~500 人）的智能人力资源管理助手，以 WorkBuddy / OpenClaw Skill 形式提供服务。
> **所有数据本地存储，不上云，隐私安全。**

---

## ✨ 功能特性

### 已全部实现（228 个测试通过）

| 模块 | 功能 |
|------|------|
| **员工花名册** | 增删改查、在职状态管理、批量转正/离职、关键词搜索 |
| **组织架构** | 多级部门树、汇报链查询、部门人数统计 |
| **考勤管理** | Excel 考勤表导入、迟到/早退/请假/旷工/加班自动计算扣款 |
| **薪资计算** | 个税累计预扣法、社保/公积金（多城市）、专项附加扣除、考勤扣减自动集成 |
| **年终奖优化** | 自动比较独立计税 vs 并入当月工资，选择税负更低方式 |
| **HR 报表** | 员工统计、合同到期提醒、数据校验、导出 Excel |
| **审计日志** | 所有增删改操作自动 append-only 记录 |
| **薪资历史** | 按月归档、环比对比 |

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install openpyxl xlrd
```

### 2. 安装 Skill

**方式 A：从 SkillHub / ClawHub 一键安装（推荐）**

在 WorkBuddy 内打开技能市场，搜索「HR 智能体」，点击安装。

**方式 B：手动安装**

```bash
# 将 Skill 目录复制到 WorkBuddy skills 目录
cp -r hr-assistant ~/.workbuddy/skills/
```

### 3. 启动初始化

在 WorkBuddy 中发送：

```
开始初始化
```

按引导上传三张 Excel 表（5~10 分钟完成配置）：
1. **组织架构表**（部门名称、部门编码、上级部门等）
2. **员工花名册**（工号、姓名、部门、薪资、社保基数等）
3. **薪资表**（薪资结构定义）
4. **考勤表**（可选，导入后自动计算考勤扣款）

---

## 💬 使用示例

### 员工管理

```
查询技术部的员工
查一下张三的信息
添加员工 E020 王五 技术部 工程师 入职2026-04-01
张三转正
李四调到市场部
E010 离职
E001到E010批量转正
```

### 组织架构

```
显示组织架构图
技术部有多少人
张三的汇报链是什么
```

### 考勤

```
绑定考勤表 /path/to/attendance.xlsx
查看3月份考勤
考勤汇总
查看张三的考勤记录
```

### 薪资计算

```
计算本月薪资
算一下张三3月的工资
年终奖36000
年终奖50000 月薪20000
北京社保10000
上海五险一金15000
个税税率表
```

### 报表与统计

```
员工统计
合同到期提醒
校验花名册
导出报表
查看操作日志
薪资环比对比
```

---

## 📁 文件结构

```
hr-assistant/
├── SKILL.md                     # Skill 入口文件（OpenClaw 规范）
├── skill.yaml                   # Skill 元数据与工具定义
├── README.md                    # 本文档
├── tools/
│   ├── main.py                  # 命令行入口（自然语言 + 子命令模式）
│   ├── intent_router.py         # NLU 意图路由引擎（22 种意图）
│   ├── onboarding.py            # 初始化引导（四步绑定流程）
│   ├── employee_manager.py      # 员工管理（CRUD + 组织架构）
│   ├── payroll_engine.py        # 薪资计算引擎（个税/社保/公积金）
│   ├── attendance_manager.py    # 考勤管理（导入 + 自动扣减）
│   ├── excel_adapter.py         # Excel 读写适配器（.xlsx / .xls）
│   ├── hr_store.py              # 数据持久化层（JSON 本地存储）
│   ├── test_payroll_engine.py   # 薪资引擎单元测试（18 个）
│   ├── test_employee_manager.py # 员工管理单元测试（38 个）
│   ├── test_hr_store.py         # 存储层单元测试（34 个）
│   ├── test_intent_router.py    # 意图路由单元测试（96 个）
│   ├── test_attendance_manager.py # 考勤模块单元测试（27 个）
│   └── test_e2e_integration.py  # 端到端集成测试（15 个场景）
└── docs/
    └── payroll_engine.md        # 薪资引擎技术文档
```

---

## ⚙️ 数据存储

所有数据存储在用户本地的 `.hr-data/` 目录，不上云：

| 文件 | 说明 |
|------|------|
| `.hr-data/config.json` | 绑定状态、列映射、初始化配置 |
| `.hr-data/audit.log.jsonl` | 操作审计日志（append-only，7 类写操作） |
| `.hr-data/payroll/YYYY-MM.json` | 月度薪资计算结果（按月归档） |
| `.hr-data/conversations/` | 对话历史记录 |

---

## 🏙️ 社保支持城市

**免费版**：北京、上海、广州、深圳、杭州

**Pro 版**：全国 300+ 城市（即将推出）

---

## 🧪 运行测试

```bash
cd tools/

# 运行全量测试（228 个）
python3 -m pytest test_*.py -v

# 分模块运行
python3 -m pytest test_payroll_engine.py -v      # 薪资引擎
python3 -m pytest test_employee_manager.py -v   # 员工管理
python3 -m pytest test_hr_store.py -v           # 存储层
python3 -m pytest test_intent_router.py -v      # 意图路由
python3 -m pytest test_attendance_manager.py -v # 考勤模块
python3 -m pytest test_e2e_integration.py -v    # 端到端集成
```

---

## 📋 系统要求

- Python 3.8+
- `openpyxl` >= 3.0（读写 .xlsx）
- `xlrd` >= 2.0（读取 .xls）

---

## 📄 许可证

MIT License

---

## 🗺️ Roadmap

- [x] Skill 框架搭建
- [x] 初始化四步绑定引导
- [x] Excel 适配器（.xlsx / .xls）
- [x] 员工花名册管理（CRUD + 批量）
- [x] 组织架构（部门树 + 汇报链）
- [x] 薪资计算引擎（个税累计预扣法）
- [x] 多城市社保公积金（5 城市）
- [x] 年终奖个税优化
- [x] 考勤管理（导入 + 自动扣减）
- [x] 操作审计日志
- [x] 薪资历史归档与环比
- [x] 数据持久化层
- [x] 自然语言意图路由（22 种意图）
- [ ] 全国 300+ 城市社保（Pro）
- [ ] 自定义薪资公式（Pro）
- [ ] 飞书多维表格数据源（Pro）
- [ ] 智能预警（合同到期/社保基数变更）（Pro）
- [ ] 多账套支持（Pro）
