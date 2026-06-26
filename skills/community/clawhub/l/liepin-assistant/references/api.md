# 猎聘 MCP API 参考

## 基本信息

- **MCP 端点**: `https://open-agent.liepin.com/mcp/user`
- **认证**: Header `x-user-token: <token>`
- **协议**: MCP (Model Context Protocol) over HTTPS，JSON-RPC 2.0
- **调用方式**: 所有工具通过 `tools/call` 方法调用，传入 `name` 和 `arguments`
- **频率限制**: 60 次/分钟（含搜索、查看、简历更新、投递）
- **Token 有效期**: 90 天

## 获取 Token

1. 打开 https://www.liepin.com/mcp/server 并登录猎聘
2. 点击「生成凭证」获取 `x-user-token` 值
3. 发送给我：`设置猎聘token <token值>`

## MCP 方法（统一通过 tools/call 调用）

### user-search-job

搜索职位。

```bash
node scripts/liepin-mcp.js user-search-job '{"jobName":"AI","address":"北京","page":0}'
```

| 参数 | 类型 | 说明 |
|-----|------|-----|
| jobName | string | 职位名称关键词 |
| address | string | 工作地点 |
| workExperience | string | 工作经验要求 |
| eduLevel | string | 学历要求 |
| compNature | string | 公司性质（国企、外企、民营） |
| salaryFloor | string | 薪资下限 |
| salaryCap | string | 薪资上限 |
| salaryKind | string | 薪资类型（月薪/年薪） |
| companyName | string | 公司名称 |
| page | number | 分页页码（0表示第1页） |

---

### user-apply-job

投递职位。**jobId 和 jobKind 均为必填，且 jobId 必须是数字类型**。

```bash
node scripts/liepin-mcp.js user-apply-job '{"jobId":81543059,"jobKind":"2"}'
```

| 参数 | 类型 | 说明 |
|-----|------|-----|
| jobId | number | 职位ID（**数字类型**，从搜索结果获取） |
| jobKind | string | 职位类型（从搜索结果获取，通常为 "2"） |

---

### my-resume

获取当前用户的简历原始内容。

```bash
node scripts/liepin-mcp.js my-resume '{}'
```

---

### add-work-exp / add-edu-exp / add-project-exp

添加工作/教育/项目经历。

```bash
node scripts/liepin-mcp.js add-work-exp '{"compName":"公司名","rwTitle":"职位名称","workStart":"202001","workEnd":"202312"}'
```

---

### modify-resume-base-info

修改简历基本信息。

```bash
node scripts/liepin-mcp.js modify-resume-base-info '{"realName":"姓名","sex":"男","birthday":"19950101","cityCode":"北京","nowWorkStatus":"1"}'
```

---

### modify-job-want / add-job-want

修改/添加求职期望。

```bash
node scripts/liepin-mcp.js modify-job-want '{"id":123,"wantSalaryLow":20000,"wantSalaryHigh":40000}'
```

---

## 内部实现

MCP 客户端（`liepin-mcp.js`）统一使用 `tools/call` 协议：

```json
{
  "jsonrpc": "2.0",
  "id": <timestamp>,
  "method": "tools/call",
  "params": {
    "name": "<toolName>",
    "arguments": { ... }
  }
}
```

## 错误处理

| 错误信息 | 原因 | 处理 |
|---------|------|------|
| token not configured | 未设置猎聘 token | 用户发送"设置猎聘token xxx" |
| Request failed | 网络错误 | 重试 |
| errCode != 0 | 业务错误 | 查看返回的 errCode |
