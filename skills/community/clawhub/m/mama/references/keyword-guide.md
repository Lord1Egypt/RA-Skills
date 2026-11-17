# 关键词管理

默认关注关键词：

```text
会议、培训、审批、待办、任务、项目、需求、合同、报价、付款、发票、客户、面试、报名、确认、通知
```

政企办公、商务协作、个人事务可按场景追加关键词。

## 添加关键词

```bash
python scripts/process_digest.py --add-keyword "材料报送"
```

## 临时覆盖

```bash
python scripts/process_digest.py --keywords "会议,审批,材料报送"
```

## 匹配范围

关键词匹配邮件主题、发件人、正文前若干字符和附件名。
