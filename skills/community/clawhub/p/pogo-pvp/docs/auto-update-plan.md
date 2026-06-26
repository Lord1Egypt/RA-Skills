# Auto-Update Plan — PvPoke Rankings 自动更新

## 目标

定期从 PvPoke 官方源下载最新的 rankings 数据，确保查询结果始终反映当前环境排名。

## 数据源

- **超级联盟 (1500):** `https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/rankings/rankings-1500.json`
- **高级联盟 (2500):** `https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/rankings/rankings-2500.json`
- **大师联盟 (master):** `https://raw.githubusercontent.com/pvpoke/pvpoke/master/src/data/rankings/rankings-10000.json`
- **小小杯 (484):** 可从 1500 榜单中筛选 CP≤484 的条目（PvPoke 无独立 484 榜单）

## 更新策略

### 方式 1：OpenClaw Cron（推荐）

使用 OpenClaw Cron 定时任务，每周自动执行一次更新。

```yaml
# pvpoke-rankings-update.yml
schedule: "0 0 * * 0"  # 每周日 00:00
task: |
  cd ~/.openclaw/workspace/skills/pogo-pvp
  node -e "
    const fetcher = require('./dist/fetcher');
    (async () => {
      await fetcher.fetchRankings('1500');
      await fetcher.fetchRankings('2500');
      await fetcher.fetchRankings('master');
      console.log('Rankings updated successfully');
    })();
  "
```

如果配置了 OpenClaw cron 无法访问 `cwd`，可直接使用全路径：

```
node C:\Users\xzc\.openclaw\workspace\skills\pogo-pvp\scripts\update_rankings.cjs
```

### 方式 2：用户手动更新

```bash
cd /d C:\Users\xzc\.openclaw\workspace\skills\pogo-pvp
node -e "const f=require('./dist/fetcher'); (async()=>{await f.fetchRankings('1500');await f.fetchRankings('2500');await f.fetchRankings('master');console.log('Done');})();"
```

## 兼容性

- 现有 `my_pokemon.json` 中存储的宝可梦数据不受 rankings 更新影响
- `elite_moves.json` 独立维护，不随 rankings 更新
- rankings 更新后，下次评估会自动读取最新数据

## 备份

- 旧 rankings 缓存会被直接覆盖（`cache/rankings-*.json`）
- 如需保留历史快照，可定期复制到 `cache/backup/` 目录

## 失败回退

- `getRankings()` 已内置回退：先尝试 `loadCache()`，缓存无效或过期则 `fetchRankings()`
- 如果网络失败，`fetchRankings()` 返回 `null`，评估时显示 `—` 而非报错

## 更新频率建议

- **每周一次**（周日凌晨）足够跟上环境变化
- 遇到大型赛季更新（新宝可梦/招式调整），可手动触发立即更新
