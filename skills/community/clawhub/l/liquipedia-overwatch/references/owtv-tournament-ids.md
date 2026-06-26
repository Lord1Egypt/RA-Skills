# OWTV Tournament ID 速查表

> OWTV 所有赛事页面为 `/tournaments/{ID}`，每场比赛页面为 `/matches/{ID}`
> 数据抓取：OWTV 列表页和比赛页均支持 `extract_content_from_websites`（无需 Playwright）
> JS 渲染页面：若列表为空，改用 `web_fetch` 配合搜索引擎发现 ID

## OWCS 2026 Stage 1 — 赛事 ID 映射

| 赛事 | OWTV URL | 赛事ID | 比赛ID范围 | 备注 |
|---|---|---|---|---|
| NA Stage 1 | `/tournaments/55` | **55** | ~1234+ | |
| China Stage 1 | `/tournaments/56` | **56** | 1230~1233（首批）| 2026-03-21 首日 |
| Korea Stage 1 | `/tournaments/58` | **58** | — | 2026-03-15 开始 |
| Pacific Stage 1 | `/tournaments/57` | **57** | — | |
| Japan Stage 1 | 待补充 | — | — | |
| EMEA Stage 1 | `/tournaments/53` | **53** | — | |

## OWTV 比赛 ID 规律

- 比赛 ID 连续递增，**同一赛区的同一天比赛通常 ID 相邻**
- China Stage 1 首日（2026-03-21）：比赛 ID 范围 1230~1233
- ID 越大 = 比赛越新（OWTV 按时间顺序分配 ID）
- **查找某日所有比赛**：从已知 ID 向相邻数字探测即可

## OWTV 赛事→比赛发现流程

```
1. 知道赛事 ID（如 56）→ 直接抓 /tournaments/56
2. 不知道赛事 ID → 搜索 "site:owtv.gg/tournaments China Stage 1 2026"
3. 知道某日首场比赛 ID（如 1230）→ 向相邻 ID 探测（1231, 1232, ...）
```

## OWTV 各赛区赛事 ID 探测脚本（references/owtv-match-discovery.sh）

```bash
#!/bin/bash
# 用法: bash references/owtv-match-discovery.sh <tournament_id> [start_id]
# 示例: bash references/owtv-match-discovery.sh 56 1220

TID=$1
START=${2:-1200}
END=$((START + 50))

echo "🔍 扫描 OWTV 赛事 /tournaments/$TID 下的比赛 ID ($START~$END)..."

for ID in $(seq $START $END); do
  RESULT=$(curl -s "https://owtv.gg/matches/$ID" \
    -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
    -H "Accept: text/html" \
    --max-time 5 \
    -w "%{http_code}" -o /dev/null)
  
  if [ "$RESULT" = "200" ]; then
    echo "  ✅ 发现比赛 ID: $ID"
  else
    echo "  ❌ $ID (HTTP $RESULT)"
  fi
done
```

## OWTV 赛区首页（直接抓取）

OWTV 主页含所有赛区快捷入口：
```
https://owtv.gg/
```

用 `extract_content_from_websites` 抓取后找 "China Stage 1" 链接，其 href 通常为 `/tournaments/56`
