# 魔方网表 Trae Skill — 需求文档

## 1. 目标

本 Skill 用于让 Trae 稳定生成和发布魔方网表定制页面。目标用户可以用自然语言描述列表页、录入页、管理页或 H5 扩展页需求，Trae 按真实字段定义生成可运行代码，并通过脚本完成本地调试和同域发布。

核心目标：

- 生成基于魔方网表 jsonv2 记录 API 的页面代码。
- 支持原生 HTML/JS、React、Vue 示例和生成规范。
- 强制先获取真实 `fielddef`，避免用中文 label 或猜测字段名提交数据。
- 提供本地 `mock-jsonv2` 与真实 API proxy 两种调试方式。
- 使用 `deploy.mjs` 创建站点并通过 `filemanager.jsp` 上传到魔方同域网站。

## 2. 用户场景

| 场景 | 用户说法 |
|------|----------|
| 列表页 | 「帮我做一个采购申请列表页」「生成需求拆解表的列表展示」 |
| 表单页 | 「做一个客户信息录入表单」「创建采购申请新增页面」 |
| 管理页 | 「做一个 XX 表的完整管理页面，能查、能增、能改、能删」 |
| 发布 | 「生成并发布到魔方网表」「把页面部署到网表业务系统」 |

默认工作流：

1. 确认 `spaceId` 和 `formId`；如果只有空间名或表单名，先解析名称。
2. 运行 `fetch-form-spec.mjs` 生成 `mock-data/`。
3. Trae 基于 `fielddef.json` 生成页面代码。
4. 本地用 `mock-jsonv2.mjs` 或 proxy 调试。
5. 上线前将 `CONFIG.apiBase` 设为 `''`。
6. 运行 `deploy.mjs` 发布。

## 3. 页面生成需求

- 页面配置必须包含 `apiBase`、`spaceId`、`formId`。
- 页面业务读写路径统一为 `CONFIG.apiBase + /magicflu/service/s/jsonv2/...`；解析空间/表单时还会用到 `service/json/spaces/feed` 和 `service/s/json/{spaceId}/forms/feed`。
- 本地 mock/proxy 时 `apiBase` 为 `http://127.0.0.1:3847`；魔方同域上线时为 `''`。
- 页面端不设置 `Authorization`，同域依赖浏览器 Cookie。
- API 提交、查询、筛选使用字段 `name`；展示使用字段 `label`。
- 数字字段不能提交空字符串。
- 错误提示使用中文，适合非工程用户理解。
- 单文件优先，复杂需求可拆分 HTML/CSS/JS 或框架组件。

## 4. 字段与 mock 需求

`fetch-form-spec.mjs` 必须支持：

- `--username` / `--password` 或 `MOFANG_USERNAME` / `MOFANG_PASSWORD`。
- `--cookie` 或 `COOKIE`。
- `--import-json` 离线导入 fielddef。
- 多个 `--formId` 或逗号分隔 `--formId id1,id2`。
- 支持 `--spaceLabel` 和 `--formLabel`，无需依赖其它 skill 解析 ID。
- 输出 `manifest.json`、`<formId>/fielddef.json`、`<formId>/records.seed.json`、`typesnippets.md`、`api-outline.md`。

`mock-jsonv2.mjs` 必须支持：

- mock 模式读取 `mock-data` 并提供 spaces/feed、forms/feed、fielddef、列表、创建、修改、删除。
- proxy 模式代理空间、表单和 jsonv2 记录路径到真实服务。
- proxy 模式清晰提示 POST/PUT/DELETE 会写真实数据。
- 返回 CORS 头，支持本地 HTML 调试。

## 5. 发布需求

发布流程以 `filemanager.jsp` 为当前默认实现：

| 步骤 | 要求 |
|------|------|
| 登录 | 推荐账号密码，脚本 POST `/magicflu/jwt` 获取 token 和 Cookie；也支持直接传 Cookie |
| 创建站点 | POST `{BASE_URL}/magicflu/service/s/{spaceId}/websites`，XML body，成功返回纯文本 `websiteId` |
| 预热会话 | GET `site.jsp?spaceId=...&websiteId=...`，合并 Set-Cookie |
| 上传文件 | POST `/magicflu/html/sites/connectors/jsp/filemanager.jsp?spaceId={spaceId}`，multipart 上传 `newfile` |
| 输出结果 | 打印最终访问地址 `{BASE_URL}/magicflu/html/sites/userfiles/{spaceId}/{websiteId}/{filename}` |

`websites/upload` 只作为历史/部分环境可用接口记录，不作为默认自动化路径。

## 6. 安全与约束

- 不在代码、文档示例、mock 数据中硬编码真实账号、密码、Cookie。
- `mock-data/` 是工作副本，应由 `.gitignore` 忽略；`assets/mock-data/` 是可提交模板。
- 本轮不要求连接真实魔方环境；验证应通过本地 smoke 覆盖。
- 不重新生成 zip 包，除非发布流程明确要求。

## 7. 验收标准

- `SKILL.md`、`references/design.md`、`references/requirements.md` 的命令、路径、上传方式一致。
- vanilla/react/vue 示例都使用 `CONFIG.apiBase`。
- 示例字段与 `assets/mock-data` 一致，可直接连接模板 mock 数据。
- `fetch-form-spec.mjs` 复用公共会话和超时工具。
- `npm run check:scripts`、`npm run smoke:upload`、`npm run smoke:mock`、`npm run smoke:fetch-import` 均通过。
