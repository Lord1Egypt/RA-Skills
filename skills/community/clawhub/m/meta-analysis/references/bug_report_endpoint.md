# 统一 bug-report 端点设计（ct-base §20.3.5 · 2026-08-21 初稿）

> 目标：**所有 ct- 技能共用一个专用错误报告端点**（一次性建设，计算 coze 项目零改动）。
> 设计原则：与计算端点完全解耦；报告为「脱敏元数据」非计算请求；低频、最小占用（§14）。

## 1. 端点形态

- 独立 coze 项目（如 `ct-bugreport`），对外暴露一个 `/run` 端点：
  **`https://ct-bugreport.coze.site/run`（已发布 2026-08-21）**；访问凭证存镜像内 `adapters/coze/src/endpoint_token.py`（内部不发布）。
  ⚠️ 端点 URL 属 §16.6 出站披露项；token 为**公共凭据**（§5 XOR+base64 混淆内嵌 `adapters/coze/src/endpoint_token.py`，可随包发布，非加密）。
- 职责单一：**接收脱敏报告（report）→ 校验 → 写入飞书表格；并支持 get（拉取待处理记录）/ update（更新 resultstr）/ download（下载全部）/ delete（清理 done）**。
  不做任何计算、不返回计算结果。
- **治理归属（2026-08-21 明确）**：`get / update / download / delete` 为**治理动作**，仅 `ct-update` 技能（作者侧）调用（拉取待处理报告、标记 done、下载全量、清理已处理记录）；**叶子技能客户端只发 `report`**。
- 与各计算端点（`ct-samplesize.coze.site/run` 等）**无任何代码共享**——报告逻辑演进不影响计算引擎。

## 2. 请求信封（技能侧 `adapters/bug_report.py::send_to_endpoint` 发出）

```json
{
  "action": "report",
  "report": {
    "skill": "meta-analysis",
    "skill_version": "2.1.1",
    "test": "survival",
    "error_type": "engine_error",
    "error_code": "R_ENGINE_ERROR",
    "engine_status": "coze r engine error",
    "description": "survival 检验（ss_survival_logrank，Schoenfeld 公式）输入 HR=0.75、power=0.85、1:1 分配，返回事件数 109；手工复核应为 434（疑似缺 (1+r)²/r=4 因子）。期望与 rpact 一致，实际偏小 4 倍。",
    "locale": "zh",
    "query_origin": "sha256:...",
    "session_hash": "...",
    "attempts": 2
  },
  "query_origin": "sha256:...",
  "token": "<作者发放的静态 token>",
  "ts": "2026-08-21T00:00:00+00:00"
}
```

- `action`（2026-08-21 协议升级）：`report`（写报告，默认）| `get`（拉取 `resultstr != "done"` 的记录，`skill` 非空则按 skillname 筛选、空则不筛选）| `update`（按 `id` 更新 `resultstr`，新内容在入参 `resultstr` 字段；`query_origin`/`skill` 均无需提供）。
- `report` 字段**硬白名单**（§20.3.2）：仅 11 个键；除 `description`（自由文本问题描述，协助作者 debug）外均为元数据，**不含任何用户输入值**。
- `description` 纪律（**用户把关制披露**）：写「现象 / 复现步骤 / 期望 vs 实际 / 所用算法或函数 / 错误消息原文」，必要时可含数值与研究设计（HR、power、分配比等）——以能复现为准；**唯一硬边界：不写可识别个人/机构/受试者的身份信息**；由用户在两阶段确认①检视把关；空串允许（省略键，兼容旧端点）。
- 服务端收到任何白名单外的键 → 整包丢弃（防注入 / 防误塞用户数据）。

## 3. 服务端处理流程（按 action 分派）

1. **分派**：读取 `action`（缺省 = report），非 report/get/update/download/delete → `invalid`。
2. **鉴权**：`token` 匹配作者配置的静态 token（环境变量注入），不匹配 → `unauthorized`。
3. **report**：校验（JSON 合法；`report` 仅白名单键；`skill`/`error_type` 非空；`query_origin` 格式 `sha256:`）→
   **① 先按 `query_origin` 查该来源全部记录、取最新一条作为 `history`**（首次提交则 `history=""`，§20.3 历史回执，用户 2026-08-22）；
   ② **写入飞书表格**（Base `Pog0bGNMbaCWMIsGRNpckHcnn9f` · 表 `tblGDZ8kd47mgr3k`）——报告 JSON（**剔除 `skill` 键**，skill 已由 `skillname` 列单独记录，用户 2026-08-21 指定）→ `querystr`、
   `resultstr`、`memo` 留空、`query_origin`/`skillname`/`inittime` 照写（飞书表 `memo` 文本列已就绪，2026-08-22 用户确认）；去重尽力而为（`querystr contains session_hash` 检索，
   命中 → `duplicate, skipped`）。本地无沙箱集成凭证（dev）→ SQLite 兜底（供自检）。出参附 `history`，技能端据此组织回执。
4. **get**：飞书表循环翻页查询 `resultstr != "done"` 的记录（上限 5000 条；`skill` 非空时附加 `skillname = skill` 条件、空则不筛选）→ 返回记录列表（字符串）。
5. **update**：按入参 `record_id` 将记录 `resultstr` 更新为入参 `resultstr` 内容（`query_origin`/`skill` 不参与）。
6. **download**：拉取全部记录（不过滤 resultstr；`skill` 非空则筛选）→ 返回列表 + total（字符串）。
7. **delete**：查询 `resultstr == "done"` 记录并批量删除（≤1000/批）→ 返回 deleted 数（字符串）。
8. **通知作者**（report 成功后）：邮件/webhook 推送（含 skill/version/test/error_type/error_code/ts；description 为可选摘要，正文不含用户数据）。

## 4. 响应信封（**字符串**，2026-08-21 协议变更）

出参**一律为字符串**（内部为 JSON 文本），不再是 JSON 对象：

```json
{"status": "ok", "note": "report recorded (feishu)", "history": "<同 query_origin 最新历史记录 JSON 或空串>"}
```

- report：`{"status": "...", "note": "...", "history": "..."}` 字符串。`history` 为同 `query_origin` 上一次提交记录（先查后写取最新一条；首次提交为空串）；结构见 §20.3 历史回执。
- update：`{"status": "...", "note": "..."}` 字符串。
- get / download：`{"status": "ok", "records": [{"record_id", "querystr", "resultstr", "memo", "query_origin", "skillname", "inittime"}, …], "total": N}` 字符串（2026-08-22 记录结构加 `memo`）。
- delete：`{"status": "ok", "note": "deleted N records", "deleted": N}` 字符串。
- status 取值：`ok` / `invalid`（schema 校验失败、未知 action、update 缺 record_id/resultstr）/ `unauthorized`（token 错）/
  `error`（飞书读写失败；dev 模式下 get/update/download/delete 不可用）/ `rate_limited`（仅 dev SQLite 模式）。
- 技能侧仅需区分 `ok` 与非 `ok`（非 ok 时提示用户改走本地邮箱兜底）。

## 5. 治理与合规

- **§14 共享端点最小占用**：报告低频（用户确认才发）+ 限流，天然合规；不参与检索/计算资源池。
- **§8.6 query_origin**：必带，服务端归因与限流依据。
- **§16.6 出站披露**：统一端点 URL 列入**各技能** README 出站披露（新技能接入时）。
- **§5 授权闸门**：报告发送仍走技能出站授权确认（与计算请求同规则；报告端点可入 auto_approve 白名单，因内容已脱敏且经用户两阶段确认）。
- **§13.2 联系方式**：本地兜底邮箱 `medstatstar@gmail.com` 统一。

## 6. 本地兜底（无 coze 调用时）

技能本次会话未发生任何 coze 调用 → 不发网络，`save_local_report()` 生成脱敏 md，
提示用户自行粘贴到邮件发送（§13.2 邮箱）——数据不出域，完全离线可用。

## 7. 建设清单（一次性）

1. 建 coze 项目 `ct-bugreport`：工作流 = 解析 JSON → action 分派 → 白名单校验 → token 校验 → report 落库（飞书）/ get 拉取 / update 更新 / download 下载 / delete 清理 → 通知。
2. 配置静态 token（环境变量）与通知通道（邮箱/webhook）。
3. 部署后冒烟：发一条自测报告（skill=`ct-bugreport-self-test`）确认落库与通知。
4. ✅ 已发布（2026-08-21）：端点 `https://ct-bugreport.coze.site/run`；token 为公共凭据（§5 XOR+base64 混淆内嵌 `adapters/coze/src/endpoint_token.py`，可随包发布）；
   真实 URL 回填 `adapters/bug_report.py::DEFAULT_ENDPOINT` 待技能侧接入时执行。
5. 各技能接入时：复制 `bug_report.py` → 自身 `adapters/`（§16.9）→ SKILL.md 加触发规则（§20.3.1）→ README 出站披露。
