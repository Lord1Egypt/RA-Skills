# 魔方网表 Trae Skill — 设计文档

## 1. 总体架构

`mofang-page-builder` 是一个面向 Claude Code、Trae 和 Trae CN 的页面生成与发布 Skill。它的核心闭环是：

1. 用 `fetch-form-spec.mjs` 获取真实 `fielddef`，生成本地 `mock-data/`。
2. 让 Trae 基于真实字段 `name` 生成页面代码。
3. 用 `mock-jsonv2.mjs` 在本地以同路径调试页面。
4. 用 `deploy.mjs` 创建魔方同域站点并通过 `filemanager.jsp` 上传文件。

目录结构：

```text
mofang-page-builder/
├── SKILL.md
├── package.json
├── agents/
│   └── openai.yaml
├── examples/
│   ├── vanilla/
│   │   ├── list-page.html
│   │   ├── list-page-with-apibase.html
│   │   └── form-page.html
│   ├── react/
│   │   └── MagicfluList.tsx
│   └── vue/
│       └── MagicfluForm.md
├── assets/
│   └── mock-data/
├── references/
│   ├── api-summary.md
│   ├── design.md
│   ├── requirements.md
│   └── filemanager.js
└── scripts/
    ├── lib/
    │   └── magicflu-session.mjs
    ├── deploy.mjs
    ├── fetch-form-spec.mjs
    ├── mock-jsonv2.mjs
    └── upload-flow-smoke.mjs
```

## 2. Skill 指令设计

`SKILL.md` 是各客户端的主入口，应保持短而明确：

- 激活条件：用户提到魔方网表、表单、记录、列表、录入、CRUD、H5、扩展页、发布等需求。
- 强制流程：涉及真实表单字段时，必须先获取 `fielddef`，不能凭中文 label 猜字段 `name`。
- 页面规范：统一使用 `CONFIG.apiBase`，本地 mock/proxy 为 `http://127.0.0.1:3847`，同域上线为 `''`。
- 鉴权边界：页面端只依赖同域 Cookie，不设置 `Authorization`；脚本端可用账号密码换 JWT/Cookie。
- 输出偏好：优先生成完整可运行单文件，注释和错误提示使用中文。

## 3. API 与字段设计

页面调用的业务接口统一使用 jsonv2：

| 能力 | 方法 | 路径 |
|------|------|------|
| 字段定义 | GET | `/magicflu/service/s/jsonv2/{spaceId}/forms/{formId}?selector=fielddef&lng=en` |
| 查询记录 | GET | `/magicflu/service/s/jsonv2/{spaceId}/forms/{formId}/records/entry` |
| 创建记录 | POST | `/magicflu/service/s/jsonv2/{spaceId}/forms/{formId}/records` |
| 修改记录 | PUT | `/magicflu/service/s/jsonv2/{spaceId}/forms/{formId}/records/entry/{recordId}` |
| 删除记录 | DELETE | `/magicflu/service/s/jsonv2/{spaceId}/forms/{formId}/records/entry/{recordId}` |

字段规则：

- API key、筛选字段名、提交字段名都使用 `fielddef.fields[].name`。
- 展示文案使用 `fielddef.fields[].label`。
- 数字字段不能提交空字符串；空值应省略或转换为合法数字。
- 不提交 system、serial、辅引用、图片、附件、定位、网页、注释、外部字段组等不可编辑字段。

## 4. 本地调试设计

`fetch-form-spec.mjs` 负责生成 `mock-data/`：

- 支持账号密码、Cookie、`--import-json` 三种来源。
- 多表单输出到 `mock-data/<formId>/fielddef.json`。
- 同时生成 `records.seed.json`、`manifest.json`、`typesnippets.md`、`api-outline.md`。

`mock-jsonv2.mjs` 提供两种模式：

- `mock`：读取本地 `mock-data/`，在内存中提供 fielddef、分页、创建、修改、删除。
- `proxy`：代理 `/magicflu/service/json/spaces/feed`、`/magicflu/service/s/json/...` 和 `/magicflu/service/s/jsonv2/...` 到真实魔方环境，保留真实 bq/写入行为。

两种模式都返回 CORS 头，便于本地 HTML 直接连接。

## 5. 发布设计

发布采用当前验证更稳定的 `filemanager.jsp` 上传路径：

1. 账号密码登录时，脚本 POST `/magicflu/jwt` 获取 Bearer token 和 Cookie。
2. 创建站点：POST `{BASE_URL}/magicflu/service/s/{spaceId}/websites`，body 为站点 XML，携带 Cookie，账号密码登录时同时携带 `Authorization: Bearer ...`。
3. 预热站点页：GET `/magicflu/html/sites/site.jsp?spaceId=...&websiteId=...`，合并可能返回的 Cookie。
4. 上传文件：POST `{BASE_URL}/magicflu/html/sites/connectors/jsp/filemanager.jsp?spaceId={spaceId}`，multipart 字段为 `mode=add`、`currentpath=/magicflu/html/sites/userfiles/{websiteId}/`、`newfile`、`upload=Upload`，上传阶段只依赖 Cookie。
5. 输出访问地址：`{BASE_URL}/magicflu/html/sites/userfiles/{spaceId}/{websiteId}/{filename}`。

`websites/upload` 是历史/部分环境可用的 REST 上传接口，不作为当前默认实现。

## 6. 验证设计

本 Skill 的验证入口放在 `package.json`：

- `npm run check:scripts`：对所有脚本执行 `node --check`。
- `npm run smoke:upload`：用本地 mock 服务验证 JWT、建站、预热、filemanager 上传流程。
- `npm run smoke:mock`：用 `assets/mock-data` 验证 `mock-jsonv2` 的 spaces/feed、forms/feed、fielddef、list、create、update、delete 基础路由。
- `npm run smoke:fetch-import`：用模板 fielddef 验证 `fetch-form-spec --import-json` 的离线输出。

这些验证不连接真实魔方环境，不需要账号密码或 Cookie。
