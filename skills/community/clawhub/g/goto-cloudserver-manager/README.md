# goto-cloudserver-manager

> GotoPlan / OpenClaw 的多云服务器自动化运维 Skill，支持阿里云、华为云、腾讯云等云服务器的数据库安装、业务表结构创建、服务器监控、数据库巡检和异常处理，让 OPC 和小团队也能拥有一个 AI 云运维工程师。

---

## 目录

- [在 OpenClaw 中安装和配置](#在-openclaw-中安装和配置)
- [通过对话完成运维任务](#通过对话完成运维任务)
- [权限策略说明](#权限策略说明)
- [统一 Schema 建表](#统一-schema-建表)
- [支持范围](#支持范围)
- [架构说明](#架构说明)
- [开发阶段](#开发阶段)
- [项目结构](#项目结构)

---

## 在 OpenClaw 中安装和配置

### 第一步：安装 Skill

在 OpenClaw 中执行以下命令安装 Skill：

```
/skill install goto-cloudserver-manager
```

安装完成后，OpenClaw 会提示 Skill 已就绪，并引导你完成初始配置。

---

### 第二步：通过对话配置云厂商凭证

安装后，直接在 OpenClaw 对话框中告诉它你的云厂商信息，**无需手动编辑配置文件**：

**配置阿里云凭证：**
```
帮我配置阿里云凭证，AccessKey ID 是 LTAI5tXxxxxxxxx，AccessKey Secret 是 xxxxxxxxxxxxxx
```

OpenClaw 会自动将凭证写入 `.env` 文件，并提示：
```
✅ 阿里云凭证已保存。
   - 凭证存储在本地 .env 文件，不会上传
   - 建议在阿里云控制台为此 AK 配置最小权限（ECS 只读 + 云助手执行）
```

**配置腾讯云凭证：**
```
帮我配置腾讯云凭证，SecretId 是 AKIDxxxxxxxx，SecretKey 是 xxxxxxxx
```

---

### 第三步：通过对话添加服务器

告诉 OpenClaw 你要管理的服务器信息，它会自动更新 `config/servers.yaml`：

**添加阿里云 Windows 服务器：**
```
添加一台阿里云 Windows 服务器，实例 ID 是 i-bp1xxxxxxxx，
在杭州区域，操作系统是 Windows Server 2022，
这台服务器用来跑 SQL Server，叫它"生产数据库服务器"
```

OpenClaw 会自动生成配置并询问确认：
```
我将添加以下服务器配置，请确认：

名称：生产数据库服务器
ID：aliyun-win-db-001（自动生成）
云厂商：阿里云  区域：cn-hangzhou
实例 ID：i-bp1xxxxxxxx
系统：Windows Server 2022
连接方式：云助手（主）+ WinRM（备用）
角色：database
环境：prod

确认添加？
```

回复"确认"后，服务器配置即生效。

**添加 Linux 服务器：**
```
再添加一台腾讯云的 Ubuntu 22.04 服务器，
实例 ID 是 ins-xxxxxxxx，广州区域，
用来跑 PostgreSQL，叫"应用数据库服务器"
```

---

### 第四步：验证连接

配置完成后，让 OpenClaw 验证能否连通服务器：

```
测试一下能不能连上"生产数据库服务器"
```

OpenClaw 会执行连通性测试并返回结果：
```
✅ 连接成功
   服务器：生产数据库服务器（i-bp1xxxxxxxx）
   系统：Windows Server 2022 Datacenter
   连接方式：阿里云云助手
   响应时间：1.2s
```

如果连接失败，OpenClaw 会给出具体原因和修复建议（如安全组未开放端口、WinRM 未启用等）。

---

## 通过对话完成运维任务

配置完成后，所有运维操作都通过自然语言对话触发。以下是典型场景示例。

---

### 场景一：检查服务器状态

**对话：**
```
检查一下"生产数据库服务器"现在的运行状况
```

**OpenClaw 自动执行并返回报告：**
```
📊 生产数据库服务器 健康报告
时间：2024-01-15 14:30:00

CPU 使用率：23%      ✅ 正常
内存使用率：61%      ✅ 正常
磁盘（C盘）：45%     ✅ 正常
SQL Server 服务：运行中 ✅

无异常告警。
```

> 这类只读操作无需确认，OpenClaw 会直接执行并返回结果。

---

### 场景二：安装 SQL Server

**对话：**
```
在"生产数据库服务器"上安装 SQL Server 2022
```

**OpenClaw 展示执行计划，等待确认：**
```
📋 执行计划：安装 SQL Server 2022

目标服务器：生产数据库服务器（Windows Server 2022）
连接方式：阿里云云助手

执行步骤：
1. 检查服务器磁盘空间（需要至少 50GB）
2. 下载 SQL Server 2022 Developer 版安装包
3. 静默安装（预计 15-20 分钟）
4. 启用 TCP/IP 协议，端口 1433
5. 配置 Windows 防火墙（仅对内网开放 1433 端口）
6. 安装 Windows Exporter 监控组件
7. 生成安装报告

⚠️ 此操作不可自动撤销，请确认后执行。
输入"确认执行"继续，或"取消"放弃。
```

**回复"确认执行"后：**
```
⏳ 正在执行安装，预计 20 分钟...

✅ 步骤 1/7 完成：磁盘剩余 186GB，空间充足
✅ 步骤 2/7 完成：安装包下载完毕
⏳ 步骤 3/7 进行中：SQL Server 正在安装...
```

---

### 场景三：创建数据库和表结构

**对话（自然语言描述业务需求）：**
```
在"生产数据库服务器"的 SQL Server 上创建一个叫 GotoPlan 的数据库，
然后建这几张表：用户表（包含用户名、手机号、邮箱、注册时间）、
订单表（关联用户、金额、状态、下单时间）、
支付记录表（关联订单、支付金额、支付方式、支付时间）
```

**OpenClaw 先生成 Schema 预览，等待确认：**
```
📋 我理解你需要以下表结构，请确认：

数据库：GotoPlan（SQL Server）

表 1：Users（用户表）
  Id          bigint  主键自增
  UserName    nvarchar(100)  非空
  Mobile      nvarchar(30)
  Email       nvarchar(200)
  CreatedAt   datetime2  非空

表 2：Orders（订单表）
  Id          bigint  主键自增
  UserId      bigint  外键→Users.Id
  Amount      decimal(18,2)  非空
  Status      tinyint  非空（0待付款 1已付款 2已完成 3已取消）
  CreatedAt   datetime2  非空

表 3：Payments（支付记录表）
  Id          bigint  主键自增
  OrderId     bigint  外键→Orders.Id
  Amount      decimal(18,2)  非空
  PayMethod   nvarchar(50)（微信/支付宝/银行卡）
  PaidAt      datetime2  非空

✅ 同一套结构如需在 MySQL 或 PostgreSQL 上建表，无需修改，我会自动转换 SQL 语法。

输入"确认建表"执行，或告诉我需要调整的地方。
```

**回复"确认建表"：**
```
✅ 数据库 GotoPlan 创建成功
✅ 表 Users 创建成功
✅ 表 Orders 创建成功
✅ 表 Payments 创建成功

建表报告已生成：reports/schema_report_20240115.md
```

---

### 场景四：数据库健康巡检

**对话：**
```
帮我巡检一下所有服务器的数据库，生成今日报告
```

**OpenClaw 自动执行所有只读检查，输出汇总：**
```
📊 今日数据库巡检报告（2024-01-15）

生产数据库服务器 - SQL Server 2022
  状态：✅ 运行正常
  连接数：12 / 100
  数据库大小：GotoPlan 2.3GB
  慢查询：无（近1小时）
  最近备份：昨日 02:00 ✅

应用数据库服务器 - PostgreSQL 15
  状态：✅ 运行正常
  连接数：8 / 50
  数据库大小：app_db 890MB
  长时间查询：无
  表膨胀：无异常

整体状态：✅ 健康
完整报告：reports/daily_inspection_20240115.md
```

---

### 场景五：重启服务

**对话：**
```
"生产数据库服务器"的 SQL Server 服务重启一下
```

**OpenClaw 要求确认（写操作必须确认）：**
```
⚠️ 即将重启 SQL Server 服务

服务器：生产数据库服务器
操作：Restart-Service MSSQLSERVER
影响：重启期间（约 30-60 秒）数据库不可用

当前连接数：12 个活跃连接，重启会断开这些连接。

确认重启？（输入"确认"继续）
```

---

### 场景六：被拒绝的危险操作

**对话：**
```
把 GotoPlan 数据库删掉
```

**OpenClaw 直接拒绝，无需确认流程：**
```
🚫 操作被拒绝

delete_database 已被安全策略列为禁止操作，无法执行。

如果你确实需要删除数据库，请：
1. 在 config/policies.yaml 中手动将此操作从 forbidden 移至 confirmation_required
2. 确保已完成数据备份
3. 重新发起请求

此次操作已记录审计日志。
```

---

## 权限策略说明

`config/policies.yaml` 定义三级权限，控制 OpenClaw 能自动执行什么、需要确认什么、禁止什么：

| 级别 | 操作示例 | OpenClaw 行为 |
|------|---------|---------------|
| `readonly_allowed` | 检查状态、查看日志、生成报告、列出实例 | **直接执行**，无需确认 |
| `confirmation_required` | 安装数据库、创建表、重启服务、备份恢复 | **展示执行计划**，等待你输入"确认" |
| `forbidden` | 删库、删表、清空表、关防火墙、对公网开放数据库端口 | **直接拒绝**，记录审计日志 |

你可以通过对话调整策略：
```
把"备份数据库"这个操作改成不需要确认，测试环境自动执行就好
```

---

## 统一 Schema 建表

只需用中文描述业务表结构，OpenClaw 会自动生成各数据库的建表 SQL，**同一套业务描述适配所有数据库**：

**你说：**
```
创建会员表，有 ID、用户名、手机号、注册时间
```

**自动生成：**

| 字段 | SQL Server | MySQL | PostgreSQL |
|------|-----------|-------|-----------|
| ID 自增主键 | `BIGINT IDENTITY(1,1)` | `BIGINT AUTO_INCREMENT` | `BIGSERIAL` |
| 用户名 100字符 | `NVARCHAR(100)` | `VARCHAR(100)` | `VARCHAR(100)` |
| 时间 | `DATETIME2` | `DATETIME` | `TIMESTAMP` |

---

## 支持范围

| 维度 | 支持列表 |
|------|---------|
| 云厂商 | 阿里云、腾讯云（CVM + 轻量应用服务器）、华为云 |
| 操作系统 | Windows Server 2019/2022、Ubuntu 20.04/22.04、Debian 11/12、CentOS 7、Rocky Linux 9、openEuler |
| 数据库 | SQL Server 2019/2022、MySQL 8.0、PostgreSQL 15/16、Redis 7 |
| 运维动作 | 安装、建库建表、健康检查、日志分析、服务重启、备份恢复、监控部署 |

---

## 架构说明

```
OpenClaw / GotoPlan（你的自然语言指令）
    ↓
goto-cloudserver-manager（Skill 入口 · 策略检查 · 路由分发）
    ↓
云厂商适配层（阿里云云助手 / 腾讯云 TAT（CVM + 轻量应用服务器） / 华为云 API）
    ↓
操作系统适配层（Windows PowerShell / Linux Shell）
    ↓
数据库适配层（SQL Server / MySQL / PostgreSQL / Redis）
    ↓
执行器（SSH / WinRM / 云助手 / TAT）
    ↓
云服务器 / 数据库 / 监控系统
```

凭证和服务器信息存储在本地 `.env` 和 `config/` 目录，不上传到任何云端。

---

## 开发阶段

**当前版本：v1.0.6**

- ✅ 阿里云 + Windows Server + SQL Server + Ubuntu MVP
- ✅ 完整 Linux 支持（MySQL / PostgreSQL / Redis）
- ✅ 腾讯云（CVM + TAT）
- ✅ 腾讯云轻量应用服务器（Lighthouse + TAT + 实例级防火墙）
- ✅ 华为云（ECS API + SSH fallback）
- ✅ 产品化（运维计划模板、巡检日报）
- 🐛 v1.0.5：修复 `providers/tencent/tat.py` 的 `get_command_result` 用了不存在的
  `DescribeInvocationTasksRequest.InvocationId` 字段，导致腾讯云 TAT 通道下发的命令
  永远查不到执行结果（应使用 `Filters` + `invocation-id` 过滤键）；同时补全 SKILL.md
  的 `supported_os` 清单（新增 Windows Server 2012 R2/2016/2025、更多主流 Linux 发行版
  及三家云厂商各自的默认镜像）。
- 🐛 v1.0.6：修正 ClawHub 上的展示名称（发布 1.0.5 时漏传 `--name`，被误用本地文件夹名
  "Goto Cloudserver Manager 已完成" 当了展示名，现已改回 "Goto Cloudserver Manager"）。

> GotoBot 推送集成暂未实现（仓库内无可对接的 GotoBot API/Webhook 规范）。`PolicyEngine` 抛出的 `ConfirmationRequiredError.plan` 已提供结构化数据，留给 OpenClaw / GotoBot 自行对接。

---

## 项目结构

```
goto-cloudserver-manager/
├── config/          # 服务器清单、云厂商配置、权限策略（对话配置后自动更新）
├── core/            # 分发器、策略引擎、Schema 编译器、报告生成器
├── providers/       # 云厂商适配层（阿里云/腾讯云/华为云）
├── executor/        # 执行器（SSH / WinRM / 云助手 / TAT）
├── os_adapters/     # 操作系统脚本（Windows PS1 / Linux Shell）
├── databases/       # 数据库脚本（安装/建库/建表/健康检查）
├── monitoring/      # 监控配置（Prometheus / Exporter）
├── reports/         # 报告 Jinja2 模板
└── tests/           # 单元测试
```
