# First-Run UX Test - 2026-04-02

## Test Goal

Simulate a realistic first-time founder path using the new V2 workflow:

1. create a company workspace
2. start the first round
3. hit a blockage
4. enter calibration

## Test Commands

```bash
python3 scripts/init_company.py "风帆实验室" --path /tmp/tmp.DwhmyBmvFv --product-name "风帆 Copilot" --stage 构建期 --target-user "独立开发者" --core-problem "缺少持续推进业务的一人公司系统" --product-pitch "一个帮助独立开发者按回合推进产品和业务的总控台" --confirmed
python3 scripts/start_round.py /tmp/tmp.DwhmyBmvFv/风帆实验室 --round-name "定义首屏价值主张" --goal "确定首页主标题、副标题和 CTA" --owner product-strategist --artifact "产物/产品/首页首屏草稿.md" --next-action "先明确用户是谁"
python3 scripts/calibrate_round.py /tmp/tmp.DwhmyBmvFv/风帆实验室 --reason "30 分钟内无法确定首屏价值主张" --finding "目标用户太泛，需要先收窄" --next-action "把目标用户收窄为做 AI SaaS 的独立开发者"
```

## Observed Output Quality

The generated files behaved as intended:

- `00-公司总览.md` clearly showed stage, bottleneck, current round, and next shortest action
- `04-当前回合.md` correctly moved into `待校准`
- calibration created a dedicated record under `记录/校准记录/`

Example strengths:

- the workspace feels obviously Chinese-first
- the current-round model is much easier to follow than the old weekly rhythm
- the next shortest action is visible in the right places
- the “one current round” mental model is clear

## Findings

### Good

- first-run scaffolding is fast
- file names are intuitive for Chinese users
- the round lifecycle is easy to inspect from the filesystem
- calibration updates the company state cleanly

### Remaining UX Gaps

1. The default `当前主目标` after initialization is still generic.
   - Current default: `先完成当前阶段最关键的一个回合`
   - Better future behavior: derive a stage-specific starter goal automatically

2. The first-run flow is strong once scripts are used, but the public ClawHub listing is still stale.
   - This makes the real first impression weaker than the repo state

3. There is not yet a dedicated script for “create company draft before confirmation”.
   - The runtime protocol supports it conceptually
   - The filesystem scripts begin at confirmed workspace creation

## Conclusion

The V2 filesystem workflow is already much clearer and more usable than the previous version.

The biggest remaining first-run problem is no longer the local product shape.
The biggest remaining problem is distribution synchronization:

- GitHub metadata still needs polishing
- ClawHub still shows the old version
