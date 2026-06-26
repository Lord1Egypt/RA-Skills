# Fix the timezone bug

English localization stub for the v2 beta bundle.
Use the Chinese source-of-truth prompt below if any wording differs during the beta rollout.

Chinese title: 修复时区/DST 计算 bug

## Chinese source prompt

# 修复时区/DST 计算 bug

`src/tz.py` 中提供 `local_to_utc(naive_dt, tz_name)` 与 `utc_to_local(utc_dt, tz_name)` 两个函数。当前实现假设固定 UTC 偏移，遇到 DST（夏令时）就算错。

请用 `zoneinfo.ZoneInfo` 改写：

- `local_to_utc(naive_dt, tz_name)`：把无时区 naive datetime 视作位于 `tz_name` 当地时间，转成带 UTC 时区的 datetime。
- `utc_to_local(utc_dt, tz_name)`：将带时区的 UTC datetime 转成 `tz_name` 当地时间。

`tests/test_tz.py` 用 `America/New_York`（DST 区）与 UTC 验证春季 spring-forward 等场景。
