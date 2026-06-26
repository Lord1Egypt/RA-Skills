# Oracle 收盘报告 Skill

生成 A 股市场日报，包含大盘指数、情绪资金、全球市场等数据。

## 触发条件

当用户提到以下关键词时使用此 Skill：
- "日报"、"收盘报告"、"股票日报"
- "Oracle 报告"、"每日动量"
- "生成日报"、"发送日报"

## 依赖要求

### 必需 Skills

| Skill | 用途 | 安装命令 |
|-------|------|----------|
| mx_data | 妙想金融数据（涨跌比、估值） | `skillhub install mx_data` |
| qveris | 同花顺 iFinD 数据接口 | `skillhub install qveris` |

### 必需配置

| 配置项 | 说明 |
|--------|------|
| QVERIS_API_KEY | 同花顺 iFinD API 密钥 |
| MX_APIKEY | 妙想金融 API 密钥 |

> ⚠️ 缺少依赖时，运行脚本会自动提示安装方法

## 数据源

| 数据 | 来源 | 说明 |
|------|------|------|
| 大盘指数 | QVeris → AKShare → 新浪财经 | 多级降级 |
| 南向资金 | AKShare → Tushare | 实时/历史数据 |
| 主力资金 | AKShare → mx_data | 当日净流入 |
| 涨跌比 | mx_data | 涨跌家数统计 |
| 融资融券 | QVeris | 余额数据 |
| VIX | Finnhub | 恐慌指数 |
| 美债收益率 | FRED API | 30年国债 |
| 汇率 | AKShare → 新浪财经 | 美元/人民币 |
| 恒生指数 | AKShare | 港股数据 |
| 黄金 | 新浪期货 | Au9999 |
| 原油 | WTI + 上海原油 | 国际+国内 |
| 指数估值 | AKShare + mx_data | PE/PB百分位 |

## 报告结构

```
📊 Oracle 收盘报告
├── 🎯 市场立场
├── 📈 大盘概览
│   ├── 指数点位表格
│   ├── 指数估值
│   └── 股债性价比
├── 📊 情绪与资金
│   ├── 两市成交额
│   ├── 南向资金
│   ├── 主力资金
│   ├── 涨跌比
│   ├── VIX恐慌指数
│   └── 融资融券
└── 🌍 全球市场
    ├── 美元/人民币
    ├── 恒生指数
    ├── 黄金
    ├── 美债收益率
    └── 原油
```

## 使用方法

### 手动生成日报

```bash
python3 ~/.openclaw/workspace/skills/oracle-report/scripts/oracle_report_generator.py
```

### 定时任务

```cron
# 每个工作日 16:30 发送日报
30 16 * * 1-5 python3 ~/.openclaw/workspace/skills/oracle-report/scripts/oracle_report_generator.py >> ~/.openclaw/workspace/skills/oracle-report/scripts/oracle_report.log 2>&1
```

### 环境变量配置

在 `~/.openclaw/.env` 中配置：

```env
# 飞书接收目标（可选，默认发送给当前用户）
FEISHU_TARGET=user:ou_xxx    # 发送给用户
# FEISHU_TARGET=chat:oc_xxx  # 发送给群聊
```

## 特性

### 交易日历支持

使用 AKShare 交易日历，正确处理：
- 周末运行：使用周五数据
- 节假日运行：使用节前最后交易日数据
- 节后首日运行：正确对比节前数据

### 飞书卡片格式

直接从数据构建飞书卡片，支持：
- 表格渲染
- 字段加粗
- 涨跌 emoji
- 分隔线

### Markdown 存档

同时生成 Markdown 文件存档到 `~/.openclaw/workspace/` 目录。

## 分享给其他机器人

### 方式一：本地复制（推荐）

```bash
# 复制到目标机器人的 skills 目录
cp -r ~/.openclaw/workspace/skills/oracle-report /目标机器人/skills/
```

### 方式二：发布到 Skill Store

```bash
cd ~/.openclaw/workspace/skills/oracle-report
clawhub publish
```

发布后，其他机器人可以安装：

```bash
clawhub search oracle-report
clawhub install oracle-report
```

## 注意事项

1. **首次运行**：会加载交易日历（约 8000+ 个交易日），之后会缓存
2. **网络超时**：部分数据源可能超时，脚本有重试机制
3. **周末/节假日**：自动使用最近交易日数据
4. **API 配额**：部分数据源有调用限制，脚本会优先使用免费数据源

## 输出示例

```
📊 Oracle 收盘报告

报告日期: 2026年04月04日（Saturday）
市场状态: 📌 周六休市（基于周五收盘数据）

🎯 Oracle的市场立场
持币观望（Hold / Cash） 💰

📈 大盘概览
| 指数 | 收盘点位 | 涨跌幅 | 成交额 |
|------|----------|--------|--------|
| 上证指数 | 3880.10 | -1.00% 📉 | 7138亿 |

📊 情绪与资金
- **两市成交额**: 16565亿元（较上一交易日缩量10.2%📉）
- **南向资金**: 净买入198.28亿人民币
- **主力资金**: 净流出461.83亿元
```

## 更新日志

### 2026-04-04
- 创建独立 Skill 目录
- 添加依赖检测和安装提示
- 支持环境变量配置 FEISHU_TARGET
- 添加交易日历支持，正确处理节假日

## 文件结构

```
oracle-report/
├── SKILL.md                      # 本文件
├── _meta.json                    # 元数据
└── scripts/
    └── oracle_report_generator.py # 主脚本
```
