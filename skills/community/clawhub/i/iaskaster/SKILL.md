---
name: iaskaster
description: 命理八字分析技能。用户说"算命"、"排八字"、"看八字"、"命理分析"、"八字分析"、"运势"、"算一卦"、"命盘"、"排盘"、"算卦"、"五行分析"、"八字测算"时触发。调用 iaskaster 生成专业 PDF 报告。 / Bazi fortune-telling skill. Use when user requests "fortune-telling", "Bazi analysis", "fate reading", or related keywords. Generates professional PDF reports via iaskaster.
metadata:
  - trigger: "算命|排八字|看八字|命理分析|八字分析|运势|算一卦|命盘|排盘|五行分析|八字测算"
    action: "node $IASKASTER/index.js --tool iaskaster_auto '{\"action\":\"form\"}'"
  - trigger: "检查登录|登录状态|是否登录"
    action: "node $IASKASTER/index.js --tool iaskaster_auto '{\"action\":\"check_login\"}'"
  - trigger: "发送验证码|获取验证码"
    action: "node $IASKASTER/index.js --tool iaskaster_auto '{\"action\":\"send_code\",\"contact\":\"\"}'"
  - trigger: "验证码登录|验证登录"
    action: "node $IASKASTER/index.js --tool iaskaster_auto '{\"action\":\"verify_code\",\"contact\":\"\",\"code\":\"\"}'"
  - trigger: "提交分析|开始算命|生成报告"
    action: "node $IASKASTER/index.js --tool iaskaster_auto '{\"action\":\"submit\",\"birthInfo\":\"\"}'"
  - trigger: "查询状态|流程状态"
    action: "node $IASKASTER/index.js --tool iaskaster_auto '{\"action\":\"status\"}'"
  - trigger: "报告列表|我的报告|历史报告"
    action: "node $IASKASTER/index.js --tool iaskaster_list '{}'"
  - trigger: "下载报告|导出PDF|保存报告"
    action: "node $IASKASTER/index.js --tool iaskaster_download '{\"action\":\"list\"}'"
  - trigger: "八字解读|解读八字|详细分析"
    action: "node $IASKASTER/index.js --tool iaskaster_bazi '{}'"
  - trigger: "运势分析|流年运势|今年运势"
    action: "node $IASKASTER/index.js --tool iaskaster_fortune '{}'"
  - trigger: "余额查询|账户余额|剩余额度"
    action: "node $IASKASTER/index.js --tool iaskaster_balance '{}'"
  - trigger: "充值|充值链接"
    action: "node $IASKASTER/index.js --tool iaskaster_recharge '{}'"
  - trigger: "解读报告|阅读PDF"
    action: "node $IASKASTER/index.js --tool iaskaster_read '{\"filename\":\"\"}'"
---

# 命理八字分析 (Bazi Fortune-Telling)

## 何时使用 / When to Use

- 用户要"算命"、"排八字"、"看八字"、"命理分析"。 / User wants fortune-telling or Bazi analysis.
- 用户要"运势"、"算一卦"、"命盘"、"算卦"。 / User wants fate reading or horoscope chart.
- 用户要"五行分析"、"八字测算"、"八字解读"。 / User wants Five Elements analysis or detailed Bazi reading.
- 用户要查询、下载或解读已有的八字分析报告。 / User wants to query, download, or read existing Bazi reports.

## 前置依赖 / Prerequisites

- 推荐运行环境：Node 18+。 / Recommended runtime: Node 18+.
- 执行目录：在 skill 根目录（`SKILL.md` 所在目录）执行以下命令。 / Run commands in the skill root (where `SKILL.md` is located).

```bash
npm i && npm run build
```

## 工具清单 / Tool Index

- `index.js --tool iaskaster_auto`：自动化流程入口，包含登录、提交、状态查询等核心操作。 / Main flow entry point with login, submit, status operations.
- `index.js --tool iaskaster_list`：查询用户的报告列表。 / List user's report history.
- `index.js --tool iaskaster_download`：下载或导出报告为 PDF。 / Download or export report as PDF.
- `index.js --tool iaskaster_bazi`：八字解读与详细分析。 / Bazi interpretation and detailed analysis.
- `index.js --tool iaskaster_fortune`：运势分析、流年运势。 / Fortune analysis and yearly horoscope.
- `index.js --tool iaskaster_balance`：查询账户余额或剩余额度。 / Query account balance or remaining quota.
- `index.js --tool iaskaster_recharge`：获取充值链接。 / Get recharge link.
- `index.js --tool iaskaster_read`：解读/阅读已有 PDF 报告。 / Read and interpret existing PDF reports.
- `index.js --tool iaskaster_form`：获取出生信息表单。 / Get birth info form.

## 工具与参数 / Tools & Parameters

### `iaskaster_auto`

```bash
# 基础用法
node index.js --tool iaskaster_auto '{"action":"<action>"}'

# 独立命令示例
node index.js --tool iaskaster_auto '{"action":"form"}'
node index.js --tool iaskaster_auto '{"action":"check_login"}'
node index.js --tool iaskaster_auto '{"action":"send_code","contact":"13800000000"}'
node index.js --tool iaskaster_auto '{"action":"verify_code","contact":"13800000000","code":"123456"}'
node index.js --tool iaskaster_auto '{"action":"submit","birthInfo":"姓名：张三\n性别：男\n出生日期：1990年1月1日\n出生时间：12时30分\n日历类型：公历"}'
node index.js --tool iaskaster_auto '{"action":"status"}'
```

参数定义 / Parameters:

- `action`（必填 / required）
  - 取值范围：`form`, `check_login`, `send_code`, `verify_code`, `submit`, `status`
  - 说明：
    - `form`：获取表单信息
    - `check_login`：检查登录状态
    - `send_code`：发送验证码
    - `verify_code`：验证登录
    - `submit`：提交分析请求
    - `status`：查询流程状态
- `contact`（条件 / conditional）
  - 说明：手机号或邮箱（`send_code`/`verify_code` 时需要）
- `code`（条件 / conditional）
  - 说明：验证码（`verify_code` 时需要）
- `name`（条件 / conditional）
  - 说明：姓名（`submit` 时需要）
- `birthInfo`（条件 / conditional）
  - 格式：多行文本，包含姓名、性别、出生日期、出生时间、日历类型等
  - 说明：出生信息（`submit` 时需要）

### `iaskaster_list`

```bash
node index.js --tool iaskaster_list '{}'
```

列出用户的历史报告列表。/ List user's historical reports.

### `iaskaster_download`

```bash
node index.js --tool iaskaster_download '{"action":"show","reportId":"123"}'
node index.js --tool iaskaster_download '{"action":"download","reportId":"123"}'
node index.js --tool iaskaster_download '{"action":"list"}'
```

- `action`：`show`（查看）/ `download`（下载）/ `list`（列表）
- `reportId`：报告ID
- `outputPath`：下载保存路径（可选）

### `iaskaster_bazi`

```bash
node index.js --tool iaskaster_bazi '{"reportId":"123","aspect":"overview"}'
```

八字解读与详细分析。/ Bazi interpretation and detailed analysis.

### `iaskaster_fortune`

```bash
node index.js --tool iaskaster_fortune '{"intent":"wealth","period":"this_year"}'
```

运势分析与流年运势。/ Fortune analysis and yearly horoscope.

### `iaskaster_balance`

```bash
node index.js --tool iaskaster_balance '{}'
```

查询账户余额与剩余额度。/ Query account balance and remaining quota.

### `iaskaster_recharge`

```bash
tsx scripts/recharge.ts
```

获取充值链接。/ Get recharge link.

### `iaskaster_read`

```bash
node index.js --tool iaskaster_read '{"filename":"report_xxx.pdf"}'
```

- `filename`（必填 / required）
  - 说明：PDF 报告文件名

## 示例 / Examples

```bash
# 获取表单信息
node index.js --tool iaskaster_auto '{"action":"form"}'

# 检查登录状态
node index.js --tool iaskaster_auto '{"action":"check_login"}'

# 发送验证码
node index.js --tool iaskaster_auto '{"action":"send_code","contact":"13800000000"}'

# 验证码登录
node index.js --tool iaskaster_auto '{"action":"verify_code","contact":"13800000000","code":"123456"}'

# 提交分析请求
node index.js --tool iaskaster_auto '{"action":"submit","birthInfo":"姓名：张三\n性别：男\n出生日期：1990年1月1日\n出生时间：12时30分\n日历类型：公历"}'

# 查询流程状态
node index.js --tool iaskaster_auto '{"action":"status"}'

# 查看报告列表
node index.js --tool iaskaster_list '{}'

# 下载报告
node index.js --tool iaskaster_download '{"action":"download","reportId":"123"}'

# 八字解读
node index.js --tool iaskaster_bazi '{}'

# 运势分析
node index.js --tool iaskaster_fortune '{"intent":"wealth"}'

# 查询余额
node index.js --tool iaskaster_balance '{}'

# 获取充值链接
node index.js --tool iaskaster_recharge '{}'

# 解读PDF报告
node index.js --tool iaskaster_read '{"filename":"report_xxx.pdf"}'
```

## 注意事项 / Notes

1. 所有命令均在 skill 根目录执行，不依赖仓库根目录路径。 / Run all commands in the skill root; do not rely on repo-root paths.
2. 出生信息格式为多行文本，包含姓名、性别、出生日期、出生时间、日历类型等。 / Birth info is multi-line text with name, gender, birth date, time, calendar type.
3. 首次使用需先通过验证码登录。 / First-time users need to login via verification code.
4. 提交分析后可通过 `status` 命令查询进度。 / After submitting, use `status` to check progress.
