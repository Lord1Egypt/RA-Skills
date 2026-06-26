---
name: package-tracker
description: Query package/express tracking worldwide via unified API. Integrates with 快递鸟 (Kdniao) and is extensible to other providers. Use when the user asks to track a parcel, query logistics, look up express by tracking number, or integrate courier tracking.
homepage: https://github.com/openlang-cn/package-tracker.git
metadata:
  openclaw:
    emoji: "📦"
    homepage: https://github.com/openlang-cn/package-tracker.git
    requires:
      bins: ["python"]
---

# Package Tracker

## Purpose

Helps implement and use a unified package tracking layer that can integrate multiple courier APIs (starting with 快递鸟). Use this skill when:

- User wants to track a parcel by tracking number
- User asks to integrate express/courier query in code
- User mentions 快递鸟, Kdniao, or “快递查询”

## Quick Start

1. **Config**: Copy `package_tracker.json.example` to `package_tracker.json`, then fill in `providers.kdniao.ebusiness_id` and `providers.kdniao.api_key`.

2. **Query** (Python):
   ```bash
   # Run in the skill directory (where this SKILL.md lives)
   python -m package_tracker track <ShipperCode> <LogisticCode>
   # e.g. python -m package_tracker track ZTO 638650888018
   ```

3. **In code**:
   ```python
   from package_tracker import get_tracker
   tracker = get_tracker()
   result = tracker.track(shipper_code="ZTO", logistic_code="638650888018")
   ```

## Provider: 快递鸟 (Kdniao)

- **即时查询** RequestType: `1002`
- **Endpoint**: `https://api.kdniao.com/Ebusiness/EbusinessOrderHandle.aspx`
- **RequestData** (JSON): `ShipperCode`, `LogisticCode`, optional `OrderCode`, optional `CustomerName` (required for 顺丰 SF: last 4 digits of phone)
- **Sign**: `RequestData` (unencoded JSON, no spaces) + ApiKey → MD5 → Base64 → URL-encode

Do not put API keys in code; store them in `package_tracker.json` (and avoid committing it).

## Adding Another Provider

1. Add a new module under `package_tracker/` implementing the same track interface (e.g. `track(shipper_code, logistic_code, **kwargs) -> dict`).
2. Register it in `package_tracker/registry.py`, then select it via config (`default`) or pass `provider=...` in `get_tracker(...)`.

## Reference

- 快递鸟即时查询: [API 文档](https://www.kdniao.com/api-track)
- 本技能目录内已包含可运行的 `package_tracker/`（CLI + Python 包）与示例配置文件；安装到 ClawHub 后无需额外 clone 仓库即可直接执行上述命令。

