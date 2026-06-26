---
name: jike-cookbook-query
description: 菜谱查询。支持食材列表查询、菜谱搜索、菜谱详情和随机菜谱，返回菜名、分类、耗时、口味、烹饪方式、主料辅料和做法步骤。适用场景：用户说“搜一下西红柿炒鸡蛋菜谱”“随机推荐几个菜”“查菜谱 ID 6 的做法”“鸡蛋相关食材信息”等。数据由即刻数据（jikeapi.cn）开放接口提供。
homepage: https://www.jikeapi.cn/
metadata: {"openclaw":{"emoji":"🍳","requires":{"bins":["python3"],"env":["JIKE_COOKBOOK_QUERY_KEY"]},"primaryEnv":"JIKE_COOKBOOK_QUERY_KEY"}}
---

# 菜谱查询 - 即刻数据

> 数据由 **[即刻数据](https://www.jikeapi.cn/)** 提供，帮助 AI 客户端快速接入可靠数据服务。

支持：**食材列表、菜谱搜索、菜谱详情、随机菜谱**。

## 前置配置

```bash
export JIKE_COOKBOOK_QUERY_KEY=你的AppKey
# 或使用通用 Key
export JIKE_APPKEY=你的AppKey
```

## 使用方法

### 查询食材列表

```bash
python3 scripts/cookbook_query.py ingredient --keyword 鸡蛋 --page-size 5
```

### 搜索菜谱

```bash
python3 scripts/cookbook_query.py search --keyword 西红柿炒鸡蛋 --page-size 5
```

### 查询菜谱详情

```bash
python3 scripts/cookbook_query.py detail --id 6
```

### 随机菜谱

```bash
python3 scripts/cookbook_query.py random
```

### JSON 输出

```bash
python3 scripts/cookbook_query.py search --keyword 西红柿炒鸡蛋 --json
```

## AI 使用步骤

1. 用户问食材信息时，使用 `ingredient` 子命令。
2. 用户按菜名搜索做法时，使用 `search` 子命令。
3. 用户给出菜谱 ID 或需要完整步骤时，使用 `detail` 子命令。
4. 用户要求推荐菜谱时，使用 `random` 子命令。
5. 返回菜名、耗时、口味、主料辅料和步骤。

## 返回字段

| 字段 | 含义 |
| --- | --- |
| `id` | 菜谱或食材 ID |
| `name` | 名称 |
| `type` | 分类 |
| `prep_time` | 准备/烹饪耗时 |
| `taste` | 口味 |
| `cooking_method` | 烹饪方式 |
| `main_ingredients` | 主料 |
| `secondary_ingredients` | 辅料 |
| `method` | 做法步骤 |

## 脚本位置

`scripts/cookbook_query.py`
