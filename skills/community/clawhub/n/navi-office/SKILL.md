---
name: navi-office
description: NaviOffice OA 办公系统 MCP 集成技能 - 覆盖系统管理、人力资源、考勤、财务、CRM、销售、采购、库存、项目、生产、计量检测 11 大模块，支持数据查询与业务操作。
---

# NaviOffice OA 办公自动化系统

工具名称以模块前缀开头，详细参数查阅 `references/` 对应文档。

| 模块 | 包含功能 | 文档 |
|------|---------|------|
| 系统管理 | 公司信息、切换公司、部门列表、组织架构树、权限查询、新增部门 | [system.md](references/system.md) |
| 人力资源 | 员工列表/详情/新增、个人信息、生日提醒、合同到期、试用期到期、薪资查询 | [hr.md](references/hr.md) |
| 考勤管理 | 打卡记录、全员考勤、月度/年度统计、部门统计、请假申请/记录/余额、加班记录 | [attendance.md](references/attendance.md) |
| 财务管理 | 收支看板、部门费用、应收应付总览、利润分析、收入统计、收支趋势、应收/应付列表与新增、费用报销 | [finance.md](references/finance.md) |
| CRM | 客户列表/详情/新增、商机列表/详情/新增、销售业绩、销售漏斗 | [crm.md](references/crm.md) |
| 销售管理 | 订单列表/详情/新增、合同列表/新增、应收计划生成、销售统计、销售排名、销售客户列表 | [sales.md](references/sales.md) |
| 采购管理 | 供应商列表/新增、采购订单列表/详情/新增、采购统计 | [purchase.md](references/purchase.md) |
| 库存管理 | 物料列表/新增、仓库列表、库存列表/报表、低库存预警、入库单/出库单新增、出入库统计、周转分析 | [inventory.md](references/inventory.md) |
| 项目管理 | 我的项目/待办、项目列表/详情/新增、任务列表/详情/新增、工时统计、成本核算 | [project.md](references/project.md) |
| 生产管理 | 生产订单列表/详情/新增、工单列表/详情/新增、设备列表/详情 | [mes.md](references/mes.md) |
| 计量检测 | 委托单列表/详情/新增、从订单生成委托单、器具列表、证书列表、业务员/工程师业绩统计 | [calibration.md](references/calibration.md) |

## 安装

```bash
clawdhub install navi-office
```

## 环境变量与安全说明（必读）

```bash
# 必填
NAVI_OFFICE_API_TOKEN=your_api_token_here

# 可选（默认官方地址）
NAVI_OFFICE_API_URL=https://oa.teredy.com/api

# 可选：是否允许非官方域名，默认 false
NAVI_OFFICE_ALLOW_CUSTOM_DOMAIN=false
```

- 必填：`NAVI_OFFICE_API_TOKEN`
- 可选：`NAVI_OFFICE_API_URL`（默认 `https://oa.teredy.com/api`）
- 可选：`NAVI_OFFICE_ALLOW_CUSTOM_DOMAIN`（默认 `false`）
- 请求头：`X-Api-Token: ${NAVI_OFFICE_API_TOKEN}`
- 默认仅从技能目录 `.env` 读取凭证，避免误读当前工作目录下无关凭证
- 默认只允许官方域名 `oa.teredy.com`；若使用自定义地址，需显式设置 `NAVI_OFFICE_ALLOW_CUSTOM_DOMAIN=true`
- 若无法确认域名来源，请勿使用生产环境真实令牌

## CLI 脚本

`NaviOffice/scripts` 目录包含可调用脚本：

- `navioffice.sh`（Shell）
- `navioffice.py`（Python）
- `navioffice.js`（Node.js）

## CLI 调用示例

部分工具的参数值本身是 JSON 字符串（如 `employeeData`），CLI 调用时需对内层 JSON 转义：

```bash
# 普通参数（值为基本类型）
mcporter call navi-office.hr_queryEmployeeInfo --args '{"employeeName":"张三"}'

# 参数值为 JSON 字符串时，内层需转义引号
mcporter call navi-office.hr_updateEmployee --args '{"employeeId":1051,"employeeData":"{\"employeeStatus\":1}"}'
```

## 渐进式工具加载（强制）

为减少 token 消耗，禁止首轮把全量工具塞入上下文，必须按下面流程：

1. 先调用 `tool_catalog`，获取可用模块目录和工具数量
2. 根据用户问题只选择最相关模块
3. 再调用 `load_module_tools`，参数示例：`{"module":"attendance","detailLevel":"brief"}`
4. 若 `brief` 不足以确定参数，再对同一模块使用 `detailLevel=full`
5. 只有跨模块问题才追加加载其他模块，避免全量加载

## 调用规则

- **名称→ID**：用户提供名称时，先调查询接口获取 ID 再操作（如客户名→customerId、部门名→deptId、员工名→employeeId）
- **模糊查询**：`employeeName` `deptName` `customerName` `orderName` `supplierName` `materialName` `equipmentName` `instrumentName` 等字段可直接传名称，无需先查 ID
- **查询条件**：能够精准查询的参数一定要带上，尽量不要查询全量列表
- **分页**：列表默认每页 10 条，用 `page` / `limit` 调整
- **日期格式**：`yyyy-MM-dd` 或 `yyyyMM`
- **权限**：无权限时返回明确错误提示
- **工具加载策略**：默认 `brief`，仅在必要时 `full`
