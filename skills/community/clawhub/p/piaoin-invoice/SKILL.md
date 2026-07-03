---
name: piaoin-invoice
description: 对接票IN/Piaoin PAT 发票开放接口，用于下载/同步已归集发票、在本地保存发票文件与结构化数据、上传本地发票图片或 PDF 到票IN。用户要求下载票IN发票、同步发票文件夹、管理员批量下载租户发票、上传本地发票到票IN、维护本地 .piaoin_evn API key/同步状态文件、查看票IN OCR/验真/初审结果时使用。
---

# 票IN 发票

使用本技能从本地项目或线上 Agent 调用票IN PAT开放接口。票IN是一个多途径归集发票的小程序，支持手机拍照OCR、邮箱采集、短信开票链接提取、自动分类、自动验真和简单初审。本技能聚焦发票已进入票IN后的两个工作流：把发票记录和文件下载/同步到本地，以及把本地发票文件上传到票IN。

## 核心规则

- 将 `X-API-Key` 当作敏感信息处理。不要完整打印密钥；展示时掩码为 `py_...abcd`。
- 除非用户指定其他目录，否则使用当前项目根目录作为本地状态目录。
- 在项目根目录用 `.piaoin_evn` 保存本地状态。仅在用户已有 `.piaoin_env` 时作为兼容/迁移读取。
- 每次执行时记录当前运行环境到 `.piaoin_evn`，至少包含 `RUNTIME_MODE` 和 `LAST_RUNTIME`。
- 下载的发票文件和结构化数据保存到 `piaoin_invoice/YYYY-MM/`。
- 调用列表接口且 `allTenant=true` 前，必须确认下载范围。
- 只有用户明确要下载整个租户/企业/公司发票，并且当前角色明确为 `tenantAdmin` 时，才使用 `allTenant=true`。
- 如果用户是普通用户或角色未知，默认只下载当前用户自己的发票。若用户要求下载企业全部发票，先确认其为租户管理员，并将 `USER_ROLE=tenantAdmin` 写入本地状态。
- 上传时 `file` 与 `fileUrl` 二选一，绝不能同时发送。
- 记住列表接口只返回正常发票（`invoice_state=1`）。上传接口返回的重复或异常发票，后续可能不会出现在列表结果中。
- 如果缺少 API key，不要继续调用接口；用“缺少秘钥时的用户提示”中的 Markdown 图片和步骤引导用户创建秘钥。
- 每次下载/查询完成后，都要给用户一个 Markdown 表格汇总。表格至少包含发票类型、开票日期、发票号码、发票代码、金额、明细汇总、上传日期；如果查询的是全企业/全租户，还要包含发票用户名。

## 执行方式选择

按当前运行环境降级选择执行方式：

1. 线上 Agent 或有 HTTP 请求工具：优先使用可用的请求工具直接调用 PAT 接口，并把运行方式记录为 `RUNTIME_MODE=request-tool`。不要假设能写入本地文件；如果不能落盘，只返回接口结果和可下载链接。
2. 本地有 Python 环境：优先使用 `scripts/piaoin_invoice.py`，记录为 `RUNTIME_MODE=python-cli`。这是最完整模式，支持分页同步、下载文件、上传文件、更新 `.piaoin_evn`。
3. 没有 Python 但有 curl：使用 curl 调接口，记录为 `RUNTIME_MODE=curl`。下载文件可用 `curl -L -o`；结构化数据可保存为 JSON 文件。
4. Windows 无 Python 但有 PowerShell：使用 `Invoke-RestMethod` 和 `Invoke-WebRequest`，记录为 `RUNTIME_MODE=powershell`。
5. 如果既没有请求工具，也没有可用命令行 HTTP 客户端，只生成可执行请求命令和参数说明，不声称已同步或上传。

运行环境记录建议：

```dotenv
RUNTIME_MODE=python-cli
LAST_RUNTIME=2026-07-01T12:34:56+08:00; os=Windows; shell=PowerShell; python=3.12.0
```

如果当前环境不能写文件，在最终回复中说明“无法写入 `.piaoin_evn`，本次运行环境为 ...”。

## Python 快速开始

使用 `scripts/piaoin_invoice.py` 执行稳定的本地操作：

```bash
python ~/.codex/skills/piaoin-invoice/scripts/piaoin_invoice.py config --api-key py_xxx --role user
python ~/.codex/skills/piaoin-invoice/scripts/piaoin_invoice.py download --scope own --since-last
python ~/.codex/skills/piaoin-invoice/scripts/piaoin_invoice.py download --scope tenant --page-size 50
python ~/.codex/skills/piaoin-invoice/scripts/piaoin_invoice.py upload ./invoice.pdf
python ~/.codex/skills/piaoin-invoice/scripts/piaoin_invoice.py upload-url https://example.com/invoice.pdf
```

从用户项目根目录运行命令，这样 `.piaoin_evn` 和 `piaoin_invoice/` 会创建在该项目中。PowerShell 可以直接使用绝对路径：

```powershell
python C:\Users\jakyo\.codex\skills\piaoin-invoice\scripts\piaoin_invoice.py download --scope own
```

## 无 Python 降级示例

curl 查询自己的发票：

```bash
curl "https://admin.piaoin.cn/api/v1/pat/invoices/list?pageNum=1&pageSize=50&allTenant=false" \
  -H "X-API-Key: $PAT"
```

curl 上传本地 PDF：

```bash
curl -X POST "https://admin.piaoin.cn/api/v1/pat/invoices/upload" \
  -H "X-API-Key: $PAT" \
  -F "file=@./invoice.pdf"
```

PowerShell 查询自己的发票：

```powershell
$headers = @{ "X-API-Key" = $env:PAT }
Invoke-RestMethod -Uri "https://admin.piaoin.cn/api/v1/pat/invoices/list?pageNum=1&pageSize=50&allTenant=false" -Headers $headers
```

PowerShell 上传本地文件时，优先使用系统已有 curl：

```powershell
curl.exe -X POST "https://admin.piaoin.cn/api/v1/pat/invoices/upload" -H "X-API-Key: $env:PAT" -F "file=@./invoice.pdf"
```

## 本地状态

`.piaoin_evn` 使用简单的 `KEY=VALUE` 格式：

```dotenv
API_KEY=py_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
BASE_URL=https://admin.piaoin.cn
USER_ROLE=user
LAST_SYNC_DATE=2026-06-01
RUNTIME_MODE=python-cli
LAST_RUNTIME=2026-07-01T12:34:56+08:00; os=Windows; shell=PowerShell; python=3.12.0
```

`USER_ROLE` 可选值：

- `tenantAdmin`：允许请求 `--scope tenant`，即全租户/全企业范围。
- `user`：只允许请求 `--scope own`，即当前用户自己的发票。
- `unknown`：角色未知，按普通用户处理，直到用户明确说明。

生产环境使用 `https://admin.piaoin.cn`，测试环境使用 `https://admintest.piaoin.cn`。

## 缺少秘钥时的用户提示

当 `.piaoin_evn` / `.piaoin_env` / 环境变量中都没有可用的 `API_KEY`、`PIAOIN_API_KEY` 或 `PAT` 时，停止当前下载/上传动作，并用 Markdown 向用户展示下面的参考图片和操作顺序：

```markdown
当前还没有票IN API 秘钥，暂时不能下载或上传发票。

![票IN秘钥创建参考图](https://wiseai-prod.obs.cn-north-1.myhuaweicloud.com/2026/07/01/da2dbc3922694ada8c721179d208a1ff.png)

请按下面顺序创建并复制秘钥：

1. 打开票In小程序或 App。
2. 进入“我的”菜单。
3. 点击“个人信息”。
4. 滑到最下面，在“秘钥”位置点击“创建”。
5. 复制生成的秘钥并发给我。

注意：秘钥仅展示一次，请创建后立刻复制保存。
```

拿到秘钥后，优先写入 `.piaoin_evn`：

```bash
python ~/.codex/skills/piaoin-invoice/scripts/piaoin_invoice.py config --api-key py_xxx --role user
```

如果没有 Python 环境，提示用户可临时设置环境变量 `PAT` / `PIAOIN_API_KEY` 后使用 curl 或请求工具。

## 下载流程

1. 读取 `.piaoin_evn`。如果没有 API key，按“缺少秘钥时的用户提示”展示参考图片和操作顺序，等待用户提供秘钥。
2. 判断下载范围：
   - “我的发票”“个人发票”或未明确说明范围：使用 `--scope own`，接口参数为 `allTenant=false`。
   - “企业全部”“租户全部”“全公司发票”：使用 `--scope tenant`，接口参数为 `allTenant=true`，且要求 `USER_ROLE=tenantAdmin`。
3. 用户要求增量同步时使用 `--since-last`。如果存在 `LAST_SYNC_DATE`，脚本会发送 `startDate=LAST_SYNC_DATE`。
4. 分页调用 `/api/v1/pat/invoices/list`，直到 `pageNum >= totalPage`。
5. 按 `createTime` 或 `invoiceDate` 的月份，把每条记录追加保存为 JSONL。
6. 当返回 `invoiceUrl` 时下载文件，并尽量保留合适扩展名。文件名应尽量包含发票日期、发票号码/ID、销售方。
7. 将 `LAST_SYNC_DATE` 更新为本次结果中最大的 `createTime` 日期。
8. 生成并展示 Markdown 汇总表；Python CLI 会在 `piaoin_invoice/summary_YYYYMMDD_HHMMSS.md` 保存本次汇总。

下载/查询汇总表字段：

| 字段 | 来源 |
| --- | --- |
| 发票用户名 | 仅全企业/全租户查询时展示，取 `userName` |
| 发票类型 | `invoiceTypeName` |
| 开票日期 | `invoiceDate` |
| 发票号码 | `invoiceNumber` |
| 发票代码 | `invoiceCode` |
| 金额 | 优先 `invoiceAmount` |
| 明细汇总 | 优先发票明细数组/明细字段；如果接口未返回明细，使用销售方到购买方的简要说明 |
| 上传日期 | `createTime` |

如果接口返回 `无权限:仅租户管理员可查询全部发票`，说明该 API key 对应用户不是租户管理员。除非用户提供管理员 PAT，否则改为只同步自己的发票。

## 上传流程

上传本地文件：

```bash
python ~/.codex/skills/piaoin-invoice/scripts/piaoin_invoice.py upload ./path/to/invoice.pdf
```

上传远程文件 URL：

```bash
python ~/.codex/skills/piaoin-invoice/scripts/piaoin_invoice.py upload-url https://example.com/invoice.pdf
```

支持 `jpg`、`jpeg`、`png`、`pdf`。接口是同步处理：OCR、查重、验真、入库和初审完成后返回批次号和发票结果数组。对异常发票重点说明 `invoiceStateName`、`isVerification` 和 `checkResultInfo`。

## 参考资料

需要查看接口路径、响应字段、枚举含义、错误处理或 curl 示例时，读取 `references/pat-api.md`。
