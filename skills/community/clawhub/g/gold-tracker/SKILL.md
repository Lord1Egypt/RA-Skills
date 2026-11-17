# 黄金追踪 — 智能体操作手册

零第三方依赖的黄金价格追踪与分析技能。本文档是唯一操作真相源；违反「铁律」或「输出格式」的分析会被 `analyze_check.py` 以非零退出码拒绝。

## 铁律（违反即拒绝）
1. 每个数据点 MUST 有来源 URL，不输出裸结论。
2. 每个判断 MUST 有因果链（"因为 X → 所以 Y → 对金价影响 Z"），并引用 ≥1 条真实抓取过的 URL。
3. 无数据 MUST 写 `no_data`，绝不编造、不补全。

## 安装
```bash
cp config.example.yaml config.yaml
python3 scripts/verify.py init && python3 scripts/verify.py check   # 出现 [✗] 先修复
```

## 两套工作流

### A. 自动监控（定时运行，无需人工）
```bash
sh examples/run_cycle.sh   # 抓取 → 检测提醒 → 通知，建议每 30 分钟一次
```
- 调度方式见 `examples/crontab.example`、`gold-tracker.service`/`.timer`。
- 提醒：金价波动超过正常范围即触发；30 分钟内不重复、每天限条数；失败自动重试。

### B. 市场分析（agent 触发，消耗 token，请在关键时段执行）
1. `python3 scripts/fetch.py` — 抓金价/汇率（自动校验/缓存/降级）
2. `sh examples/analyze_prep.sh` — 采集可信新闻 + 生成分析骨架（脚本接管，省 token）
3. 读 `cache/news_snippets.json`，在 `logs/YYYY-MM-DD.yaml` 骨架里填 `key_factors`（reasoning/impact/sources）
4. `python3 scripts/analyze_check.py` — 硬校验，必须 exit 0
5. `sh examples/analyze_finish.sh` — 校验 + 简报 + 通知

## 输出格式（logs/YYYY-MM-DD.yaml）
骨架由 `analyze_scaffold.py` 自动生成。硬约束（违反则 `analyze_check.py` 拒绝）：
- 顶层：`run_id / timestamp / price_data / summary.focus / key_factors / sources` 齐全。
- `key_factors` 2–6 条，每条含 `factor / impact / reasoning / sources`，`impact` ∈ {利多, 利空, 偏多, 偏空, 中性, 多空交织}。
- `sources` ≥2 条且覆盖 ≥2 独立网站，每条都必须是真实抓取过的（web_fetch 后 `python3 scripts/log_fetch.py <url> "<标题>"`）。
- `reasoning`/`summary.focus` 不含禁词（见 config `output.constraints.forbidden_phrases`）；无数据写 `no_data`。

## 常用命令
```bash
python3 scripts/alert_manager.py detect|list|pending|status|auto_resolve|cleanup|threshold
python3 scripts/notify.py send alerts|summary|retry|status|test [--dry-run]
python3 scripts/archive.py archive|find|history|cleanup|rebuild|summary|normalize
```

## 排障
| 症状 | 处理 |
|---|---|
| fetch 失败 | 自动降级缓存/上次状态 |
| check 报 source 未在 fetch_log | `log_fetch.py` 补记，或从 sources 删除 |
| check 报网站不足/禁用措辞 | 补抓不同网站 / 改写为因果链 |
| verify 报「提醒检测未运行」 | 按 examples/ 配置定时调度 |
| 归档/状态损坏 | `archive.py rebuild` / `verify.py init` |