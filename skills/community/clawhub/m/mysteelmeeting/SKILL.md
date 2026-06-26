---
name: mysteelmeeting
description: 查询我的钢铁网会展频道（huizhan.mysteel.com/zhuanti）行业会议信息，支持行业筛选（钢材/铁矿石/废钢/煤焦/铁合金/不锈钢/有色金属/建筑材料/新能源/农产品）、地区筛选（东北/华北/华东/华南/华中/西北/西南/港澳台/全球）、省份筛选（吉林/辽宁/黑龙江/北京/上海/广东/浙江/江苏等）、状态筛选（报名中/进行中/已结束）、收费类型（免费/收费）、活动类型（全部/会议/调研/精选赞助）。当用户提到"查询会议"、"搜索会议"、"查看行业会议"、"找最近的会议"、"会议报名"、"免费会议"、"收费会议"、"钢材会议"、"煤炭会议"、"吉林会议"、"浙江会议"、"北京会议"、以及具体的行业、地区或省份关键词时应触发此技能。
---

# 我的钢铁网会议查询技能

> 功能与 `huizhan.mysteel.com/zhuanti` 页面完全一致，支持动态获取行业/地区/省份数据。

## 核心特性

### 🎯 智能名称匹配
- 支持直接输入**行业名称**、**地区名称**、**省份名称**进行查询
- 系统自动从API获取最新数据并进行ID匹配
- 支持模糊匹配（如输入"东"可匹配"东北地区"）

### 🔄 动态数据加载
- 行业、地区、省份数据从API**实时获取**
- 内置24小时缓存，减少重复请求
- 可通过 `--clear-cache` 强制刷新数据

## 使用方法

### 基本查询

```bash
# 按行业名称查询（自动匹配ID）
python scripts/query_mysteel.py --industry "钢材"

# 按地区名称查询
python scripts/query_mysteel.py --area "华东"

# 按省份名称查询（自动识别省份并关联地区）
python scripts/query_mysteel.py --area "吉林"

# 组合筛选
python scripts/query_mysteel.py --industry "钢材" --area "华东" --status "0"
```

### 查看分类数据

```bash
# 查看所有行业
python scripts/query_mysteel.py --list-industries

# 查看所有地区和省份
python scripts/query_mysteel.py --list-areas

# 指定行业后查看地区（部分地区可能不属于某些行业）
python scripts/query_mysteel.py --list-areas --industry-id "10"
```

### 高级筛选

```bash
# 报名中的会议
python scripts/query_mysteel.py --status "0"

# 免费会议
python scripts/query_mysteel.py --charge-type "0"

# 按关键词搜索
python scripts/query_mysteel.py --keyword "钢铁"

# 分页查询
python scripts/query_mysteel.py --page-size 20 --page-num 2
```

### 缓存管理

```bash
# 清除缓存（强制刷新数据）
python scripts/query_mysteel.py --clear-cache
```

## 参数说明

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `--industry` | 行业名称（自动转ID） | "钢材"、"铁矿石" |
| `--area` | 地区/省份名称（自动转ID） | "华东"、"吉林"、"北京" |
| `--status` | 会议状态 | "0"=报名中, "1"=进行中, "2"=已结束 |
| `--charge-type` | 收费类型 | "0"=免费, "1"=收费 |
| `--keyword` | 关键词搜索 | 任意搜索词 |
| `--page-size` | 每页数量 | 默认10 |
| `--page-num` | 页码 | 默认1 |

## 工作流程

### 当用户输入省份名称时（如"吉林"）

1. 调用 `load_areas()` 从API获取最新地区/省份数据
2. 在返回数据中模糊匹配"吉林"
3. 找到吉林省后，自动获取：
   - `areaId`: 1（东北地区）
   - `provinceId`: 232（吉林省）
4. 调用会议查询API，同时传入 `areaId` 和 `provinceId`
5. 如果API没有该省份，使用 `keyword` 参数作为兜底搜索

### 当用户输入行业名称时（如"钢材"）

1. 调用 `load_industries()` 从API获取最新行业数据
2. 模糊匹配"钢材"
3. 找到后获取 `industryBreedId`
4. 调用会议查询API

## 常见用例

```bash
# 查询吉林的钢材会议
python scripts/query_mysteel.py --industry "钢材" --area "吉林"

# 查询华东地区报名中的新能源会议
python scripts/query_mysteel.py --industry "新能源" --area "华东" --status "0"

# 查询所有免费会议
python scripts/query_mysteel.py --charge-type "0"

# 查询辽宁的煤炭会议
python scripts/query_mysteel.py --industry "煤焦" --area "辽宁"
```

## 数据来源

- **行业数据**: `https://huizhan.mysteel.com/event/activity/queryIndustry`
- **地区数据**: `https://huizhan.mysteel.com/event/activity/queryArea`
- **会议查询**: `https://huizhan.mysteel.com/event/activity/queryActivity`

## 缓存机制

- 缓存目录: `scripts/.cache/`
- 缓存文件: `industries_cache.json`, `areas_cache.json`
- 有效期: 24小时
- 自动清理过期缓存
