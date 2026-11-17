# Mode: doctor — 环境自检

触发：`/house-ops doctor` 或"自检/体检"。目标：确认仓库结构与数据健康，问题当场给出修复动作。对应 career-ops 的 `npm run doctor`（本仓库无安装依赖，doctor 是模式而非必跑脚本；`scripts/doctor.mjs` 可做无 AI 的快速版）。

## 检查清单

逐项输出 `✅ / ⚠️ / ⛔ + 一句话`：

1. **系统层完整性**：`AGENTS.md`、`CLAUDE.md`、`modes/_shared.md`、各模式文件，以及全部 `templates/policy-notes.*.yml` 与 `templates/official-sources.*.yml`（现为 cn / eu / apac 三对）存在且非空。
2. **技能链接**：`.claude/skills/house-ops`、`.zcode/skills/house-ops` 符号链接可解析到 `.agents/skills/house-ops/SKILL.md`。
3. **用户层状态**：
   - `config/profile.yml` 存在？（缺失 → 建议先跑 intake）
   - `modes/_profile.md` / `_brief.md` / `_custom.md` 存在性（可选件，缺失只提示）
   - 画像中的"待确认"项清单（如购房资格待确认 → 提醒）
4. **数据一致性**：
   - `data/watchlist.md` 每行编号在 `reports/` 有对应报告？（孤儿行 → 列出）
   - `reports/` 每份报告在 watchlist 有登记？（漏登记 → 列出并问是否补）
5. **时效性**：
   - 每张 `templates/policy-notes.*.yml` 的整体 as_of 距今 > 90 天 → ⚠️ 提醒核实更新。
   - **市场覆盖**：登记表与政策表是否成对；`config/profile.yml` 的 `market.code` 是否在已登记市场内（不在 → 提示跑 intake）。
   - 备注含「已看房」但超 60 天无新进展（无二看/谈判备注）的房源 → 提示可汇总到 stats 检视。
6. **可选脚本**：`node scripts/doctor.mjs` 能否正常运行（Node 环境可用性）。

## 输出

- 末尾给一句总评：`环境健康 / N 项建议修复 / N 项阻塞（列出）`。
- ⛔ 项给**一键修复指令**（如 `ln -sfn ../../.agents/skills/house-ops .zcode/skills/house-ops`），征得同意后可直接执行。
