---
name: mysteelai-smart-query
version: 1.0.0
description: "MysteelAI-智能问数：基于钢联/隆众数据平台的大宗商品价格行情数据查询技能。当用户以自然语言查询螺纹钢、铜、原油、水泥、大豆、碳酸锂、硅料、废钢等品种的期货或现货价格、今日报价、基准价、价格走势或涨跌行情时触发；也支持历史价格与趋势分析、不同地区/城市/钢厂/企业的价格对比、GDP/CPI/PMI等宏观经济指标、产业链上下游供需/库存/进出口数据，以及股票、债券、外汇、期权等多市场金融数据查询和结算确认单生成。适用于『XX多少钱一吨』『XX最新价格』『XX行情走势』『XX价格对比』等价格数据问答。不适用于与大宗商品和金融数据无关的闲聊、文案创作、代码编写、翻译等场景。"
metadata:
  openclaw:
    requires:
      bins:
        - python3
    primaryEnv: mysteel_skill_auth_key
    envVars:
      - name: mysteel_skill_auth_key
        required: false
        description: "Mysteel API Key。获取地址：https://token.mysteel.com/#/user-center/my-secret-key?qd=clawhub&datasearch 。也可在对话中提供，脚本会自动保存到 references/api_key.md。"
    emoji: "📊"
    homepage: https://www.mysteel.com
---

# Mysteel-Price-Search

大宗商品与宏观经济数据综合查询技能，基于Mysteel数据平台提供专业、全面的价格数据服务。

## 未配置API密钥时的引导回复

当用户查询价格数据但尚未配置API密钥时，请按以下引导回复用户：

看起来还没有配置 API 密钥。要使用钢联数据查询，需要先获取一个密钥。

**获取方式：** 

1. 点击打开 [MysteelAI生产力平台](https://token.mysteel.com/#/user-center/my-secret-key?qd=clawhub&datasearch)，登录Mysteel账号（如无账号请先申请并等待管理员审核后开通）

2. 登录账号后，进入「个人中心-我的密钥」

3. 找到「默认密钥」，复制密钥

 **如操作中遇到问题，请联系客服：400-880-2970**

请问您是否已有钢联数据的 API Key？如果有，请直接告诉我，我会自动保存并立即为您查询。

### 用户提供API密钥后的处理流程

1. 调用 `python scripts/search.py --api-key "<密钥>" "<查询文本>"` 保存密钥并执行查询
2. 保存成功后告知用户密钥已保存，后续可直接使用

## API 密钥配置

脚本支持多级 API Key 获取方式（按优先级）：

1. **环境变量**（优先级最高）：设置环境变量 `mysteel_skill_auth_key`

   - 操作路径：设置 -> 环境变量 -> 添加变量
   - 变量名：`mysteel_skill_auth_key`
   - 变量值：您的 API 密钥

2. **配置文件**（次优）：在 `references/api_key.md` 文件第一行写入 API 密钥

3. **对话输入**（兜底）：在对话中直接提供 API 密钥

   - 脚本通过 `--api-key` 参数接收用户在对话中提供的密钥
   - **自动保存**：当通过对话输入 API 密钥时，脚本会自动将其保存到 `references/api_key.md` 文件中，供后续使用

如果以上方式都无法获取到 API 密钥，脚本会提示用户进行配置。

## Quick Start

使用 `scripts/search.py` 脚本查询价格数据：

```bash
python scripts/search.py "<查询文本>"
```

### 通过对话提供 API 密钥

当用户在对话中提供 API 密钥时，使用 `--api-key` 参数传入：

```bash
python scripts/search.py "<查询文本>" --api-key "<用户提供的API密钥>"
```

**注意**：通过此方式提供的密钥会自动保存到 `references/api_key.md` 文件中，下次调用时无需再次提供。

## CSV 输出模式（推荐）

将查询结果保存为 CSV 文件，**强烈建议使用过滤参数减少数据量**：

### 基本用法

```bash
python scripts/search.py "螺纹钢最新价格" --csv
```

### 数据过滤参数（重要！）

为避免 LLM 读取过多数据，**请根据需要使用以下参数**：

| 参数             | 说明             | 示例                        |
| -------------- | -------------- | ------------------------- |
| `--limit N`    | 限制每个文件最多 N 行数据 | `--limit 10`              |
| `--days N`     | 仅查询最近 N 天的数据   | `--days 30`               |
| `--start-date` | 起始日期（含）        | `--start-date 2024-01-01` |
| `--end-date`   | 结束日期（含）        | `--end-date 2024-01-31`   |

### 推荐使用示例

```bash
# 查询最新10条价格（最常用）
python scripts/search.py "螺纹钢最新价格" --csv --limit 10

# 查询最近30天价格
python scripts/search.py "铜期货价格" --csv --days 30

# 查询特定日期范围
python scripts/search.py "热卷价格" --csv --start-date 2024-01-01 --end-date 2024-03-31
```

## 读取已有 CSV 文件

**不要使用 Read 工具读取整个 CSV 文件！** 使用 Bash 工具按需读取：

```bash
# 查看文件元数据（了解数据概况）
head -10 output/螺纹钢.csv

# 仅读取前N行数据
head -20 output/螺纹钢.csv | tail -n +10

# 按日期过滤（使用 grep）
grep -E "^2024-01" output/螺纹钢.csv

# 查看文件统计信息
wc -l output/螺纹钢.csv
```

## CSV 文件格式

CSV 文件包含元数据头注释，格式如下：

```
# index_name: 螺纹钢_上海_HRB400E
# unit: 元/吨
# total_rows: 365
# date_range: 2023-01-15 ~ 2024-01-15
# generated: 2024-01-15 10:30:00
#
date,price,unit,change,change_pct
2024-01-15,3800,元/吨,+20.00,+0.53%
2024-01-14,3780,元/吨,-10.00,-0.26%
```

## 输出示例

```
Generated 2 CSV file(s) in output:
  - 螺纹钢_上海_HRB400E.csv (10 rows, 2024-01-05 ~ 2024-01-15)
  - 热卷_上海_Q235B.csv (10 rows, 2024-01-05 ~ 2024-01-15)
```

## 完整参数列表

- `--csv`: 保存结果为 CSV 文件到 output 目录
- `--output-dir`: 指定 CSV 输出目录（默认：技能目录/output）
- `--limit N`: 限制每个文件最多 N 行数据
- `--days N`: 仅查询最近 N 天的数据
- `--start-date YYYY-MM-DD`: 起始日期过滤
- `--end-date YYYY-MM-DD`: 结束日期过滤
- `--max-files N`: 限制 output 目录最多保留 N 个 CSV 文件（默认：100），超过时删除最旧的文件
- `--api-key <API_KEY>`: 直接提供 API 密钥（当用户在对话中提供时使用，会自动保存到 `references/api_key.md` 文件）

## Query Capabilities

### 1. 价格数据查询

- **期货价格**：最新收盘价、结算价、涨跌幅
- **现货价格**：实时报价、区域价格、企业报价
- **历史数据**：趋势分析、周期对比

### 2. 宏观经济数据

- 全球宏观经济主要指标
- 分国别/地区数据查询
- GDP、CPI、PMI等指标

### 3. 产业链数据

- 上游原材料价格
- 下游产品价格
- 供需平衡数据
- 进出口数据
- 库存数据

### 4. 金融市场数据

- 期权价格与隐含波动率
- 股票行情
- 债券收益率
- 外汇汇率

### 5. 智能分析

- 类目识别与指标识别
- 多维度数据对比
- 口径标准化
- 差值计算

### 6. 结算凭证

- 支持贸易双方成交数量输入

## API Reference

详细API文档参见 [api_reference.md](references/api_reference.md)。

## Response Handling

API返回JSON格式数据，主要包含：

1. **价格数据**：数值、单位、涨跌幅、时间戳
2. **图表数据**：支持历史趋势图表
3. **对比数据**：多维度价格对比

## Best Practices

1. **查询表达**：使用自然语言描述查询需求，API支持智能语义解析
2. **数据对比**：可同时查询多个品种或区域进行对比分析
3. **历史溯源**：支持基于时间范围的查询，获取历史趋势

## 回复格式

需要详细标明数据所引用的指标（indexName）
