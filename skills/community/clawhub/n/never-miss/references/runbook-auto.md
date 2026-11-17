# 自动模式运行手册（runbook）

> 触发：宿主在每天 `schedule.time` 注入哨兵提示 `【never-miss:auto-run】`。
> 原则：**不追问、不打扰、静默写入；拿不准就跳过**（FR-24/25）。

## 完整流程（严格按序）

```
1. scan fetch                       # 各账户按游标取新邮件，游标不动
2. 逐账户、逐封处理邮件：
   ├─ 含 ics_events 字段 → 直接以其结构化字段 create --journal（不送模型提取；
   │                        补充字段如地点/参与者可结合正文；RRULE 仅取首次）
   ├─ 正文有明确日程 → 提取 → create --journal
   └─ 拿不准 / 无日程 → journal skip
3. scan commit                      # 全部终态才推进游标；渲染 runs/*.md；置 report_pending
4. 输出一行摘要（供宿主下次对话汇报）
```

## 逐封处理规则

- `mails[i]` 含字段：`uid`（邮件 UID）、`subject`、`from`、`date`、`body`、`body_truncated`、`ics_events`
- `source.account` 取本次 fetch 的 `account`（邮箱地址）；`source.mail_subject` 取邮件主题；`source.mail_uid` 取 `uid`
- 处理每封时 Event JSON 里的 `start` 用**绝对时间**（依 extraction-rules 换算）；全天事件 `start` 用 `YYYY-MM-DD`
- `create --journal` 会自动查重：同 UID 已存在 → 返回 `status:"duplicate"`（无需你额外判断，跨账户去重也在此完成）

## 跳过与错误（journal 命令）

```bash
python3 scripts/never_miss.py journal skip --account <邮箱> --uid <邮件UID> --reason AMBIGUOUS --detail "周三聊聊？"
python3 scripts/never_miss.py journal error --account <邮箱> --code E_INTERNAL --message "描述"
```

- `--uid` 为邮件 UID（对应 `mails[i].uid`），**必填**（commit 靠它核对终态）
- IMAP 失败：`scan fetch` 已自动记 journal error，你**不要**重复记，直接继续下一账户

## 超限处理（FR-27）

- `scan fetch` 每账户最多返回 `limit`（= `max_per_run`）封；超出时该账户结果 `has_more:true`
- 你只需处理返回的这批；`commit` 只把游标推进到本批全部处理完的最大 UID，剩余邮件下次自然补齐，**无遗漏**

## 单账户失败隔离（NFR-08）

- 某账户 fetch 返回 `status:"error"` → 跳过该账户，继续处理其他账户
- 不要因为一个账户失败而中断整次运行

## commit 说明

- `scan commit` 逐账户核对：每个 `fetched` 邮件都已有终态（create/duplicate/skip/error）才推进游标
- 有未处理完的邮件 → 返回 `pending`，游标不动；此时应补记终态后再次 commit
- commit 后 journal 清空、报告落盘 `runs/YYYY-MM-DD.md`

## 输出摘要格式

运行结束向宿主返回一行，例如：
`本次扫描：工作 新建2/跳过3/重复1，学校 新建0/跳过0；详情见 runs/2026-09-04.md`
