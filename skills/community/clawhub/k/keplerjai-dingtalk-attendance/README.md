# 钉钉考勤数据获取技能

## 快速开始

### 1. 安装依赖

```bash
cd keplerjai-dingtalk-attendance
npm install
pip install -r requirements.txt
```

### 2. 配置钉钉应用

1. 访问 [钉钉开放平台](https://open.dingtalk.com)
2. 登录并创建**企业内部应用**
3. 在应用详情页面获取：
   - AppKey
   - AppSecret
   - AgentId
4. 添加应用权限：
   - 进入「应用功能」→「权限管理」
   - 添加「通讯录管理」和「考勤管理」相关权限
   - 提交管理员审批

### 3. 配置本地文件（推荐使用 .env）

```bash
cp .env.example .env
```

Windows PowerShell 可使用：

```powershell
Copy-Item .env.example .env
```

编辑 `.env`，填入你的钉钉应用信息：

```env
DINGTALK_APP_KEY=dingxxxxxxxxxxx
DINGTALK_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DINGTALK_AGENT_ID=123456
OUTPUT_DIR=./data/attendance
OUTPUT_FORMAT=json
```

说明：脚本支持读取 `.env` 和 `config.json`，且 `.env` 优先。建议仅在本地保留配置，不要提交敏感信息。

### 4. 准备 Excel 模板（如果需要导出 Excel）

请确保 `template/` 目录下至少有一个 `.xlsx` 模板文件。
当前仓库默认提供模板：`template/考勤模板.xlsx`。

### 5. 运行测试

```bash
node index.js
```

运行后会自动：
- 获取部门列表
- 获取员工列表
- 获取考勤报表
- 导出 JSON 数据
- **自动生成 Excel 文件**

### 6. 配置定时任务（可选）

在 OpenClaw 中配置 cron 任务，每天自动获取考勤数据。

---

## 输出文件

### JSON 数据
- 位置：`data/attendance/` 目录
- 命名规则：
   - 单日：`YYYY-MM-DD考勤.json`
   - 整月：`YYYY.M月考勤.json`
   - 时间段：`YYYY-MM-DD至YYYY-MM-DD考勤.json`
- 包含：部门、员工、考勤报表详情

### Excel 报表
- 位置：`data/excel/` 目录
- 命名规则：
   - 单日：`YYYY-MM-DD考勤.xlsx`
   - 整月：`YYYY.M月考勤.xlsx`
   - 时间段：`YYYY-MM-DD至YYYY-MM-DD考勤.xlsx`
- 包含 4 个工作表：

| 工作表 | 内容 |
|--------|------|
| 汇总统计 | 部门/员工数量、考勤记录统计 |
| 打卡详情 | 所有员工的详细打卡记录 |
| 请假记录 | 请假人员及请假时长 |
| 异常统计 | 迟到、早退、缺卡、请假汇总 |

---

## 输出数据说明

### 打卡记录字段

| 字段 | 说明 |
|------|------|
| userId | 用户 ID |
| name | 姓名 |
| check_type | 打卡类型（上班/下班） |
| plan_check_time | 计划打卡时间 |
| user_check_time | 实际打卡时间 |
| time_result | 结果（正常/迟到/早退/未打卡） |
| user_address | 打卡地点 |

---

## 常见问题

### Q: 获取 token 失败？
A: 检查 AppKey 和 AppSecret 是否正确，确保应用已启用。

### Q: 没有用户数据？
A: 确保应用有通讯录权限，且管理员已审批。

### Q: Excel 导出失败？
A: 确保已安装 `openpyxl`：`pip install -r requirements.txt`

### Q: API 调用频率限制？
A: 钉钉 API 有调用频率限制，脚本已内置延时，建议定时获取而非实时。

### Q: 如何获取历史数据？
A: 修改 `index.js` 中的日期范围，默认获取昨天的数据。

---

## 扩展功能

可以基于此技能扩展：
- 考勤异常提醒（迟到、早退、缺卡）
- 考勤报表自动发送到钉钉群
- 与工资系统对接
- 数据可视化展示
- 邮件发送 Excel 报表
