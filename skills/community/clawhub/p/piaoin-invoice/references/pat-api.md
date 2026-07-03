# 票IN PAT API 参考

## 接口域名

- 生产环境：`https://admin.piaoin.cn`
- 测试环境：`https://admintest.piaoin.cn`

所有 PAT 接口路径都以 `/api/v1/pat/` 开头，并要求携带请求头：

```http
X-API-Key: py_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

API key 由用户生成。服务端只保存 SHA-256 哈希，无法找回明文。

## 缺少 API key 时

如果本地状态文件或环境变量中没有 `API_KEY`、`PIAOIN_API_KEY` 或 `PAT`，不要继续请求接口。向用户展示：

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

拿到秘钥后再写入 `.piaoin_evn` 或作为请求头 `X-API-Key` 使用。

## 执行环境与降级

优先顺序：

1. 线上 Agent 有请求工具时，直接用请求工具发送 HTTP 请求。
2. 本地有 Python 时，使用 `scripts/piaoin_invoice.py`。
3. 无 Python 但有 curl 时，使用 curl。
4. Windows 无 Python 但可用 PowerShell 时，使用 `Invoke-RestMethod` 查询、`curl.exe -F` 上传。
5. 无可用 HTTP 客户端时，只生成请求命令，不标记任务完成。

每次运行应记录环境：

```dotenv
RUNTIME_MODE=request-tool|python-cli|curl|powershell|manual
LAST_RUNTIME=ISO时间; os=系统; shell=Shell; python=版本或none; http_client=工具名
```

如果不能写入 `.piaoin_evn`，在回复中明确说明本次运行环境和未落盘原因。

## 查询发票列表

`GET /api/v1/pat/invoices/list`

查询参数：

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `pageNum` | int | `1` | 页码，从 1 开始 |
| `pageSize` | int | `20` | 批量同步稳定时可使用 50-100 |
| `allTenant` | bool | `false` | `true` 查询租户全部发票，要求 `tenantAdmin` |
| `startDate` | date | 无 | `yyyy-MM-dd`，包含当天 |
| `endDate` | date | 无 | `yyyy-MM-dd`，服务端自动扩展到当天 23:59:59 |
| `invoiceTypeName` | string | 无 | 发票类型模糊匹配，例如 `增值税` |

响应结构：

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "total": 137,
    "totalPage": 7,
    "pageNum": 1,
    "rows": [
      {
        "id": 102345,
        "userId": 10086,
        "tenantId": 5,
        "userName": "张三",
        "tenantName": "XX科技有限公司",
        "invoiceNumber": "24412000000012345678",
        "invoiceCode": "011002100211",
        "invoiceDate": "2024-01-15",
        "invoiceTypeName": "增值税专用发票",
        "seller": "XX科技有限公司",
        "buyer": "YY科技有限公司",
        "invoiceAmount": 1130.00,
        "invoiceUrl": "https://oss.../xxx.pdf",
        "verification": "0000",
        "invoiceSource": 1,
        "invoiceState": 1,
        "createTime": "2024-01-16 09:12:33"
      }
    ]
  }
}
```

重要错误：

- HTTP/code `401`：缺少 API key 或 API key 无效。
- `code=500`，`msg=无权限:仅租户管理员可查询全部发票`：非管理员用户使用了 `allTenant=true`。
- `code=500`，`msg=invalid api key context`：后端请求上下文异常，需要联系服务维护方。

租户管理员的判定依据是角色标识 `role_key=tenantAdmin`。

查询后必须展示 Markdown 汇总表。普通用户查询字段：

| 发票类型 | 开票日期 | 发票号码 | 发票代码 | 金额 | 明细汇总 | 上传日期 |
| --- | --- | --- | --- | ---: | --- | --- |

全企业/全租户查询字段：

| 发票用户名 | 发票类型 | 开票日期 | 发票号码 | 发票代码 | 金额 | 明细汇总 | 上传日期 |
| --- | --- | --- | --- | --- | ---: | --- | --- |

字段映射：

- 发票用户名：`userName`，仅 `allTenant=true` 时展示。
- 发票类型：`invoiceTypeName`。
- 开票日期：`invoiceDate`。
- 发票号码：`invoiceNumber`。
- 发票代码：`invoiceCode`。
- 金额：优先 `invoiceAmount`。
- 明细汇总：优先明细数组或明细字段；如果列表接口没有返回明细，使用 `seller -> buyer` 作为简要说明。
- 上传日期：`createTime`。

如果结果很多，先展示前 20 行表格，并说明完整汇总文件路径或总条数。

curl 示例：

```bash
curl "https://admin.piaoin.cn/api/v1/pat/invoices/list?pageNum=1&pageSize=50&allTenant=false" \
  -H "X-API-Key: $PAT"
```

PowerShell 示例：

```powershell
$headers = @{ "X-API-Key" = $env:PAT }
Invoke-RestMethod -Uri "https://admin.piaoin.cn/api/v1/pat/invoices/list?pageNum=1&pageSize=50&allTenant=false" -Headers $headers
```

## 上传发票

`POST /api/v1/pat/invoices/upload`

请求类型：`multipart/form-data`

请求头：

```http
X-API-Key: py_xxxxxxxx
```

表单字段：

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `file` | 与 `fileUrl` 二选一 | 本地 `jpg/jpeg/png/pdf` 文件；PDF 会按页拆分处理 |
| `fileUrl` | 与 `file` 二选一 | 可信公网 `http/https` URL；后端下载后处理 |

不要同时发送 `file` 和 `fileUrl`。

响应结构：

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "batchNo": "2026063016200010001",
    "invoices": [
      {
        "invoiceId": 102345,
        "invoiceNumber": "24412000000012345678",
        "invoiceAmount": 1130.00,
        "invoiceDate": "2024-01-15",
        "seller": "XX科技有限公司",
        "buyer": "YY科技有限公司",
        "invoiceState": 1,
        "invoiceStateName": "正常",
        "invoiceSource": 8,
        "isVerification": 1,
        "checkResultInfo": null
      }
    ]
  }
}
```

上传接口为同步处理：OCR、查重、按租户配置验真、入库、初审和结果查询都会在返回前完成。

常见上传错误：

- `文件不能为空`：`file` 和 `fileUrl` 都没有传。
- `file 与 fileUrl 不能同时传,请二选一`：同时传了两个字段。
- `仅支持 jpg/png/pdf 格式`：文件后缀不支持。
- `文件下载失败`：`fileUrl` 无法访问或下载失败。
- `未获取到用户信息`：当前 PAT 用户无法映射到票IN用户。
- `文件上传失败`：后端上传到 OSS 失败。

curl 上传示例：

```bash
curl -X POST "https://admin.piaoin.cn/api/v1/pat/invoices/upload" \
  -H "X-API-Key: $PAT" \
  -F "file=@./invoice.pdf"
```

PowerShell 上传示例：

```powershell
curl.exe -X POST "https://admin.piaoin.cn/api/v1/pat/invoices/upload" -H "X-API-Key: $env:PAT" -F "file=@./invoice.pdf"
```

## 枚举值

发票来源：

| code | 含义 |
| --- | --- |
| 1 | 本地发票上传 |
| 2 | 短信导入 |
| 3 | 微信卡包导入 |
| 4 | 聊天导入 |
| 5 | 拍照导入 |
| 6 | 邮箱导入 |
| 7 | 企业微信导入 |
| 8 | PAT 开放接口 |

发票状态：

| code | 含义 |
| --- | --- |
| 1 | 正常 |
| 2 | 重复 |
| 3 | 已使用 |
| 4 | 异常 |

验真结果：

| code | 含义 |
| --- | --- |
| 0 | 未验真 |
| 1 | 验真成功 |
| 2 | 验真失败 |

常用发票类型模糊关键词包括：`增值税`、`电子发票`、`火车票`、`出租车`、`航空`、`医疗`、`定额`、`机动车`、`非税`。
