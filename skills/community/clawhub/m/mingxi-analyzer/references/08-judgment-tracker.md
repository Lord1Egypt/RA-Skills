# 判断回查系统

> **TCR适用性**：仅TCR-D类和E类的判断性结论需要登记。A/B/C类不需要。

用途：追踪历史判断的有效性，确保多轮迭代闭环。

## 数据存储
SQLite 持久化（默认路径：~/.openclaw/judgment_tracker.db）

## 操作流程

### 登记（产出D/E类判断时）
调用脚本记录：
```bash
python3 scripts/judgment_tracker.py record <domain> <assertion> <confidence> <fail_condition> [check_date]
```
- check_date 默认=产出日+7天

### 回查（按计划执行）
```bash
python3 scripts/judgment_tracker.py review
```
- 过滤 `next_check_at <= now` 且 `status='active'` 的条目
- 对每条检查：该判断是否还站得住？
  - `stable` → 提信度一级，verifications_passed++，更新 next_check_at
  - `fail` → 移入T4，status='archived'
  - `hold` → 保持原信度，延长7天
- 连续三次 stable → 自动转入长期监督（季度回查）

## 纪律
1. 仅D/E类判断必须登记
2. 回查脚本必须定期运行（与每日复盘cron联动）
3. 同一主题连续三次回查站得住 → 自动转入长期监督
