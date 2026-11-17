---
name: industry-radar
version: 1.1.0
description: 行业雷达（Industry Radar）——可本地部署的「行业 × 技术」情报简报生成引擎（FastAPI 后端 + Vue Web 界面 + REST API），围绕「行业词 × 技术词」完成多源 RSS 采集、全文抽取、simhash 去重、相关性打分、主题聚类、LLM 摘要（未配置 LLM 自动降级），产出编辑精选式结构化简报。仅当用户点名本产品（「行业雷达」「Industry Radar」「IndustryRadar」「智汇简报」），或明确要求「用行业 × 技术关键词组合生成多源 RSS 情报简报 / 周报」时使用。触发必须先命中产品名或「行业词 × 技术词 × RSS 采集生成简报」这一复合意图；仅出现泛化的周期报告、监控、订阅管理、RSS 等词汇时不触发——用户写工作总结、做通用信息聚合、询问 RSS/Atom 概念、或搭建其他监控系统时不要使用本 Skill。
license: MIT
allowed-tools:
  - Read
  - Write
  - Bash
  - WebFetch
permissions:
  filesystem:
    read:
      - "app/**"
      - "scripts/**"
      - "references/**"
      - "demo/**"
    write:
      - "app/data/**" # SQLite 库 + briefings/*.md，唯一写入区
      - "data/**" # 环境变量 IR_DATA_DIR 指向的替代数据目录
  network:
    outbound:
      - "http"
      - "https"
    egress: "仅经 app/backend/net_guard.py，禁止直连 socket；不读取 HTTP(S)_PROXY 环境变量"
    targets: "RSS/Atom 源站点 + 用户显式配置的 LLM 网关（默认关闭）"
  process:
    exec:
      - "python3 scripts/run_local.py" # 建 venv / 装依赖 / 启动 uvicorn
  secrets:
    read_env:
      - "IR_LLM_API_KEY" # 只读、只用于 Authorization 头，绝不落盘或回显
  persistence:
    listen: "127.0.0.1:8000（默认回环，--host 0.0.0.0 需用户显式授权）"
metadata:
  version: 1.1.0
  risk: medium
  data-egress: "启用 LLM 时，文章正文与订阅关键词会发往 IR_LLM_BASE_URL 指定的第三方模型服务"
---

# 行业雷达 Industry Radar

**STOP - 不要凭通用知识回答。** 按以下流程操作本 Skill。

## 概述

一句话：**输入「行业词 × 技术词」，输出一份编辑精选式的行业情报周报。**

```
行业词×技术词 → 14源RSS采集 → 清洗/全文抽取 → simhash去重 → 相关性打分
            → 主题聚类 → LLM摘要/洞察(可降级) → 编辑精选式Markdown周报
```

- 自带 FastAPI 后端 + Vue Web 界面（免构建，静态托管），浏览器开箱即用
- SQLite 落库（`app/data/industry_radar.db`，首次启动自动创建），简报同时存 `.md` 文件
- LLM 可选：配置 OpenAI 兼容网关（含华为云 ModelArts Studio）即用在线摘要；不配置自动降级「抽取式摘要 + 规则洞察」，全流程依然可跑通
- 两种周报风格：`standard` 标准周报 / `curated` 编辑精选（每期精选 5 篇 + 上榜理由 + 星级 + 「只读两篇」指引）

## 环境要求

| 依赖   | 要求                              | 说明                          |
| ------ | --------------------------------- | ----------------------------- |
| Python | 3.9+                              | 启动器自动建 venv 并装依赖    |
| LLM    | 可选                              | 未配置自动降级，功能完整可用  |
| 网络   | 需能访问 RSS 源站点               | 部分海外源需代理              |

## 快速开始

```bash
# 在 Skill 根目录执行（唯一需要记住的命令）
python3 scripts/run_local.py

# 启动后浏览器访问
#   Web 界面:  http://127.0.0.1:8000    演示账号 demo / demo
#   API 文档:  http://127.0.0.1:8000/docs
# 停止: Ctrl+C
```

首次启动自动：建 venv → 装依赖 → 初始化 SQLite → 预置演示用户和示例订阅「新能源汽车 × 固态电池」。

## 常用工作流

| 任务                   | 操作                                                                 |
| ---------------------- | -------------------------------------------------------------------- |
| 部署启动               | `python3 scripts/run_local.py`（换端口加 `--port 8001`）             |
| 登录拿 Token           | `POST /api/login`（demo/demo），后续请求带 `Authorization: Bearer …` |
| 查看可用数据源         | `GET /api/sources`（14 个内置源，见 references/api-reference.md）    |
| 录入自定义 RSS 源      | `POST /api/custom-sources`（`name` + `url`，录入时即时探测必须抓到 ≥1 条，否则 400） |
| 自定义源列表 / 改 / 删 | `GET` / `PUT` / `DELETE /api/custom-sources/{cs_id}`（`PUT` 可 `enabled=false` 停用） |
| 手动检测自定义源       | `POST /api/custom-sources/{cs_id}/test` —— 返回抓到的条目数，不落库        |
| 在订阅里引用自定义源   | `sources` 数组里写 `"cs:<cs_id>"`（例如 `["36kr","cs:7"]`），只能引自己名下的源 |
| 创建订阅               | `POST /api/subscriptions`（行业词、技术词必填）                      |
| 关键词试跑（不落库）   | `POST /api/preview` —— 想先看效果用这个，不产生任何持久数据          |
| 正式生成一期周报       | `POST /api/subscriptions/{id}/run` —— 同步执行，约 30-120 秒         |
| 读取简报（列表/详情）  | `GET /api/briefings?subscription_id=…` / `GET /api/briefings/{id}`   |
| 导出 Markdown         | `GET /api/briefings/{id}/export`                                     |
| 趋势 / 总览看板        | `GET /api/trend?subscription_id=…` / `GET /api/dashboard`            |
| 修改 / 删除订阅        | `PUT` / `DELETE /api/subscriptions/{id}`                             |

### 典型调用链

| 步骤 | 调用 | 说明 |
| --- | --- | --- |
| 1 登录换令牌 | `POST /api/login` | 请求体含 `username` / `password`，响应取 `token` |
| 2 建订阅 | `POST /api/subscriptions` | 带鉴权头；请求体给 `name` / `industry_kw` / `tech_kw` / `sources` / `frequency` / `style`，`style=curated` 为编辑精选式 |
| 3 生成一期 | `POST /api/subscriptions/<id>/run` | 带鉴权头，`<id>` 用第 2 步返回的订阅 id |
| 4 取 Markdown | `GET /api/briefings/<id>` | 读响应里的 `markdown` 字段即为整期简报 |

> 鉴权头格式、完整请求体样例与响应字段见 `references/api-reference.md`。

## 关键陷阱

| 陷阱                              | 原因 / 规则                                                                                                              |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| run 只补增量文章                  | simhash 去重会过滤已入库文章；同一订阅短时间内重复 run 新文章很少。要全新效果请用 `/api/preview` 或删除订阅后重建        |
| Token 重启即失效                  | 会话存内存。服务重启后所有 Token 失效，重新 `POST /api/login` 即可                                                        |
| 没有 `/api/health`               | 探活用 `GET /api/config`（返回 LLM 模式与版本）                                                                           |
| LLM 配置需重启生效               | `IR_LLM_*` 环境变量在启动时读取；改完必须重启服务                                                                          |
| 海外源可能超时                    | TechCrunch/The Verge/Ars 需要代理；超时源自动跳过，不影响整体生成（日志有 WARNING）                                       |
| run 是同步接口                    | 一期 30-120 秒，HTTP 客户端超时设置 ≥ 180 秒；curl 加 `--max-time 300`                                                    |
| 删除订阅不删历史简报文件          | `app/data/briefings/*.md` 保留在磁盘，可手动清理                                                                           |
| 自定义源只能引 `cs:<id>`          | 订阅 `sources` 里写内置源 key（`36kr` 等）或用 `cs:<cs_id>` 引用自己的源；写别人的 `cs:<id>` 会被静默过滤，不会报错但抓不到内容 |
| 自定义源录入即探活                | `POST /api/custom-sources` 会立即抓一次，抓不到条目直接 400，错误信息里带原因；只想登记不上线可先用 `test` 接口试          |
| 自定义源有配额                    | 每用户最多 10 个（`IR_CUSTOM_MAX_PER_USER`），单订阅最多引用 5 个（`IR_CUSTOM_MAX_PER_SUB`），超限返回 400                  |
| 连续失败会自动停用                | 连续 3 次抓取失败（`IR_CUSTOM_DISABLE_AFTER_FAILS`）自动 `enabled=0`，界面状态显示「已停用」，修好地址后手动改回启用        |
| 自定义源可整体关闭                | 环境变量 `IR_ALLOW_CUSTOM_SOURCES=0` 可关闭该能力，此时 `/api/custom-sources` 全部返回 403                                  |

## 故障排查

| 症状                           | 修复                                                                                     |
| ------------------------------ | ---------------------------------------------------------------------------------------- |
| `run` 返回 500 生成失败        | 看服务日志（终端输出）中的 pipeline 异常；多为网络全挂——检查代理后重试                  |
| 端口被占用                     | `python3 scripts/run_local.py --port 8001`                                                |
| 依赖装不上                     | 换国内镜像：`pip install -r app/backend/requirements.txt -i https://mirrors.huaweicloud.com/repository/pypi/simple` |
| 想要在线 LLM 摘要              | 见 references/config-reference.md 的 `IR_LLM_*` 配置表（OpenAI 兼容协议）                |
| 简报里文章太少                 | 检查关键词是否过窄、源是否勾选足够（默认 3 源，可多选）；或关键词换更宽泛的同义词         |

## 安全注意

- **MUST** LLM API Key 只通过环境变量 `IR_LLM_API_KEY` 注入，绝不写入文件、代码或对话
- **MUST** 默认监听 `127.0.0.1`；对外暴露需 `--host 0.0.0.0` 并自担风险（会话机制为演示级）
- **MUST** 所有出站只走 `app/backend/net_guard.py`：仅允许 http/https，禁止回环 / 私网 /
  链路本地（含 `169.254.169.254` 云元数据）/ 组播 / 保留段，DNS 解析结果逐个校验，
  重定向逐跳重新校验（防「公网 302 到内网」），响应体限 3MB
- **MUST** 校验与连接必须使用同一个 IP：`safe_get()` 在校验后把目标 IP 固定到连接层
  （自定义 `HTTPAdapter` 改写 TCP 目标），同时保留原 Host 头与 TLS SNI/证书校验。
  不要改回 `requests.get(url)` 直接调用——那会让 `requests` 二次解析域名，重新打开
  DNS 重绑定（TOCTOU）窗口
- **MUST** 环境代理不参与出站：`net_guard` 使用 `trust_env=False`，忽略
  `HTTP_PROXY` / `HTTPS_PROXY` / `ALL_PROXY`，避免流量被环境变量劫持到未校验出口；
  需要代理的海外源请改用固定 RSS 镜像或在系统层做透明代理
- **MUST** Fake-IP 网段（`198.18.0.0/15`）默认拒绝。若确在 Clash/Surge 等 Fake-IP
  代理环境下使用，需显式 `IR_ALLOW_PROXY_FAKEIP=1` 放行（放行即视为信任该网段，
  仅建议在个人开发机开启，生产/内网环境请保持默认拒绝）
- **MUST** 订阅 / 简报 / 趋势 / 采集条目接口一律按 `user_id` 校验归属，越权统一返回 404
  （不泄露资源是否存在）
- **MUST** 自定义源视为不可信输入，六层约束缺一不可：①录入即 `net_guard.check_url()`
  + `safe_get()` 探活（必须解析到 ≥1 条，否则 400）②仅 http/https、禁 userinfo、端口白名单
  （`IR_ALLOWED_PORTS`，默认 80/443）、禁 IP 字面量、重定向逐跳复检 ③只能引用自己名下且
  `enabled` 的 `cs:<id>`，越权按 404 处理 ④配额 每用户 10 / 单订阅 5、串行抓取共享总超时
  ⑤只接受 RSS/Atom XML（`text/html` 直接拒），条目截断 15 条 ⑥记录 `last_status` /
  `last_error` / `last_fetch_at`，连续失败 3 次自动停用
- **MUST** LLM 返回内容视为不可信输入：`summarizer._parse_json()` 只接受 JSON 对象，
  `takeaways` / `top2` 需为列表且元素为字典，字段类型不符或条数不足（3+2）时整体回落
  规则合成，绝不因外部内容导致简报生成抛错
- demo/demo 为内置演示账号，仅用于本地体验

## 权限与数据边界

本 Skill 声明的能力范围（见 frontmatter `allowed-tools` / `permissions`），运行时不得超出：

| 能力       | 实际用途                                       | 边界                                                                 |
| ---------- | ---------------------------------------------- | -------------------------------------------------------------------- |
| 读文件     | 加载源码、`references/`、`demo/` 样例          | 不读取用户家目录、SSH 私钥、云厂商凭证文件                            |
| 写文件     | SQLite 库、`briefings/*.md` 简报               | 仅 `app/data/`（或 `IR_DATA_DIR`），不写系统目录                      |
| 执行 Shell | `python3 scripts/run_local.py`                 | 仅建 venv、`pip install`、启动 uvicorn；不执行远端下发命令            |
| 网络       | 抓 RSS/Atom；可选调用 LLM 网关                 | 仅 http/https，经 `net_guard` 校验并固定 IP，不读环境代理             |
| 读环境变量 | `IR_*` 配置 + `IR_LLM_API_KEY`                 | Key 只进 `Authorization` 头，不落盘、不写日志、不回显                 |
| 监听端口   | 默认 `127.0.0.1:8000`                          | `--host 0.0.0.0` 属对外暴露，需用户显式确认                           |

### 数据外发提示

- **启用 LLM 即外发**：采集到的文章正文、标题、订阅的行业/技术关键词会发送到
  `IR_LLM_BASE_URL` 指定的第三方模型服务商。涉密或未公开情报场景请保持
  `IR_LLM_BASE_URL` / `IR_LLM_API_KEY` 未配置状态（自动降级为本地规则引擎，全程不出网到模型方）
- **删除订阅不等于删除数据**：`DELETE /api/subscriptions/{id}` 只清库中订阅与关联记录，
  `app/data/briefings/*.md` 历史简报仍留在磁盘，需自行清理
- **自定义源 URL 会外发**：录入的自定义 RSS 地址由本机直接请求，不做任何中转或共享

### 输出语言

摘要与洞察的提示词目前写死为中文（`summarizer.py` 内 `curated_closing` / `_chat` 的
system prompt）。需要其他语言时，本地修改提示词模板中的语言指令即可，本 Skill 未提供
语言切换配置项。

## 参考资料（Progressive Loading）

| 文件                          | 内容                                                   |
| ----------------------------- | ------------------------------------------------------ |
| references/api-reference.md   | 全部 REST API 请求/响应示例、14 个内置数据源清单、自定义源接口 |
| references/config-reference.md| 全部环境变量配置表（LLM / 采集 / 自定义源 / 生成策略 / 演示账号） |
| references/architecture.md    | 数据流水线七阶段与模块职责、云端部署对应关系           |
| demo/                         | 两份真实生成的编辑精选式周报样例                       |

版本：1.1.0（新增自定义 RSS 源：六层安全约束 + Web 管理面板 + `/api/custom-sources` 接口组）

安全加固说明（对应 1.0.2 审计项）：出网抓取由 `app/backend/net_guard.py` 统一收口——DNS 校验结果直接固定到连接层（域名仅用于 `Host` 头与 TLS SNI/证书校验，不再二次解析），连接建立后复核对端 IP，不一致立即中止；fake-IP 代理网段默认拒绝；LLM 结构化输出做类型校验并保证降级不抛错。
