# 报名与主办方

## 报名者：问一轮，完成多场

1. `list_signup_feed` 找可报名的场次，保留服务端的置顶与截止优先顺序。`list_activities` 也含外部资讯，不能据其存在就声称可在站内报名。
2. `get_signup_activity` 读取详情、报名方式以及已登录用户的现有状态；用真实 slug，不从标题猜。
3. 用户需要报名后授权，再用 `get_signup_gaps(slugs=[…])` 合并多场缺口。向用户一次收齐当前需要的资料，不重复询问已有答案。
4. 通用信息用 `update_my_signup_profile` 放进跨表单复用层；逐场 `submit_signup` 只传本次新增或修改的答案，省略字段不会清空旧值。
5. `list_my_signups` 验证投递状态和主办方处置结果。清楚区分已提交、入围、候补、未通过；不要把提交成功说成被录取。

附件题目前要用户去 `https://opcmenu.com/e/{slug}` 或 App 上传。外部表单按返回的正式链接进入；未在本次宿主完成的提交和附件不能报成功。

## 主办方：预览名单再批量处置

- 先 `get_organizer_activity` 确认活动、现有配置和 `myAccess`，再做修改。
- 用 `list_signup_submissions` 按用户的标准筛选，继续分页直到覆盖要处理的范围。列表默认不提供答案全文和联系方式；只有任务需要查看某人时用 `get_signup_submission`。
- 批量处置用 `bulk_review_signup_submissions` 的 `preview=true` 得到实际对象及目标状态。名单和状态符合用户已授权的范围后才用 `preview=false` 提交；如筛选含糊，先请用户审阅名单。
- 对主办方的“发通知”需求先明确收件人和内容；处置状态变化不等于额外私信已发送。
- 用户确实要求完整导出时再用 `issue_signup_export_link`，原样交付一次性 CSV 链接。链接短时有效且可能含联系方式，不转给其他收件人或服务。

## 创建与修改活动

`create_organizer_activity` 创建可报名活动；`update_activity` 修改活动标题、时间、地点、人数、截止；`update_organizer_signup_config` 修改表单、类目、外部表单和答疑群配置。分别读取对应现值，按实时 schema 修改。

提前截止可能阻止正在填表的人提交，改变截止时间前把具体时间和影响说明给用户。取消活动或批量处置后，以返回结果确认实际影响范围。
