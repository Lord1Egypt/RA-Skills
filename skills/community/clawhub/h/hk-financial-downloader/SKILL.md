---
name: HK Financial Downloader
slug: hk-financial-downloader
version: 1.0.1
description: "港股公司财报完整下载器。自动从东方财富/同花顺/披露易获取年报、中期报告、季报、招股书，完整报告优先于业绩公告。"
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["python3"],"pip":["requests"]},"os":["linux","darwin","win32"]}}
---

## 港股公司财报下载 Skill

**版本**: v1.0.0 (2026-04-12)  
**适用市场**: 港股 (HKEX)  
**覆盖公司**: 任意港股公司（通过股票代码）

---

## 数据源优先级

| 优先级 | 数据源 | API | PDF 来源 | 特点 |
|--------|--------|-----|---------|------|
| **1️⃣** | 东方财富 | `np-anotice-stock.eastmoney.com` | `pdf.dfcfw.com` | 完整报告最多，覆盖最广 |
| **2️⃣** | 同花顺 | `basic.10jqka.com.cn` | HKEX 直链 | 补充东方财富缺失的年份 |
| **3️⃣** | 披露易 | `www1.hkexnews.hk` | HKEX 直链 | 兜底，官方权威源 |

### 各数据源覆盖对比（以腾讯 0700 为例）

| 文档类型 | 东方财富 | 同花顺 | 披露易 |
|---------|---------|--------|--------|
| 完整年报 (年報) | 22 份 (2005-2025) | 12 份 (2014-2025) | 全部 |
| 完整中期报告 | 20 份 (2004-2025) | 11 份 (2015-2025) | 全部 |
| Q3 季报 | 19 份 (2007-2025) | 12 份 (2012-2025) | 全部 |
| Q1 季报 | 9 份 | 14 份 (2012-2025) | 全部 |
| 招股书 | 4 份 | 3 份 | 全部 |

### 核心原则

- **完整报告优先于业绩公告**：同年有"年報"就不要"全年业绩公布"
- **去重**：同年同类型只保留一份（优先完整版）
- **PDF 验证**：下载后验证 `Content-Type: application/pdf`

---

## 快速开始

### 下载单家公司

```bash
python3 /root/.openclaw/workspace/skills/hk-financial-downloader/scripts/hk_downloader.py \
  --stock=0700 --from=2020 --to=2025 --type=all --pdf
```

### 批量下载

```bash
python3 /root/.openclaw/workspace/skills/hk-financial-downloader/scripts/hk_downloader.py \
  --stocks=0700,9988,3690,1810 --from=2020 --to=2025 --pdf
```

## 自动代码格式转换

脚本自动将输入的股票代码转换为各数据源所需的格式：

| 输入 | 东方财富 | 同花顺 | 披露易 |
|------|---------|--------|--------|
| `700` | `00700` | `HK0700` | `0700` |
| `0700` | `00700` | `HK0700` | `0700` |
| `00700` | `00700` | `HK0700` | `0700` |
| `HK0700` | `00700` | `HK0700` | `0700` |
| `9988` | `09988` | `HK9988` | `9988` |
| `2513` | `02513` | `HK2513` | `2513` |

## 参数说明

| 参数 | 说明 | 默认 | 示例 |
|------|------|------|------|
| `--stock` | 股票代码（5 位） | 必填 | `0700` |
| `--stocks` | 批量股票代码（逗号分隔） | - | `0700,9988,3690` |
| `--from` | 起始年份 | 2020 | `--from=2015` |
| `--to` | 结束年份 | 2025 | `--to=2025` |
| `--type` | 报告类型 | `all` | `年报`, `中报`, `季报`, `招股书`, `all` |
| `--pdf` | 下载 PDF 文件 | 否 | `--pdf` |
| `--source` | 数据源优先级 | `eastmoney,10jqka,hkex` | `--source=eastmoney` |

## 报告类型

| 类型 | 参数 | 说明 |
|------|------|------|
| 年报 | `年报`, `annual` | 完整年報 PDF（非业绩公告） |
| 中报 | `中报`, `interim` | 完整中期报告 PDF |
| 季报 | `季报`, `quarterly` | Q1 + Q3 业绩公告 |
| 招股书 | `招股书`, `prospectus` | 招股章程/全球发售 |
| 全部 | `all` | 以上全部 |

## 输出结构

```
/root/.openclaw/workspace/archive/{code}_{name}/
├── financial_reports/
│   ├── annual/          # 完整年报 (年報)
│   │   ├── 2025_年报_2025 年报.pdf
│   │   ├── 2024_年报_2024 年报.pdf
│   │   └── ...
│   ├── interim/         # 完整中期报告
│   │   ├── 2025_中报_中期报告 2025.pdf
│   │   ├── 2024_中报_中期报告 2024.pdf
│   │   └── ...
│   ├── quarterly/       # 季报 (Q1/Q3 业绩公告)
│   │   ├── 2025_Q3_截至2025年9月30日止三个月及九个月业绩公布.pdf
│   │   ├── 2025_Q1_截至2025年3月31日止三个月业绩公布.pdf
│   │   └── ...
│   └── prospectus/      # 招股书
│       ├── 2017_招股书_建议分拆中国文学...pdf
│       └── ...
└── manifest.json        # 下载清单
```

## API 技术细节

### 自动代码格式转换

```python
# 东方财富: 5位数字 (00700)
def format_code_eastmoney(code):  # 0700 → 00700

# 同花顺: HK + 4位有效数字 (HK0700)
def format_code_10jqka(code):  # 0700 → HK0700

# 披露易: 4位数字 (0700)
def format_code_hkex(code):  # 0700 → 0700
```

用户输入任意格式的代码（700/0700/00700/HK0700），脚本自动转换。

### 1. 东方财富（优先）

```python
# 公告列表 API
GET https://np-anotice-stock.eastmoney.com/api/security/ann
Params:
  - stock_list: {code}        # 如 "00700"
  - ann_type: H               # H=港股
  - page_size: 100
  - page_index: 1

# PDF 下载（直接拼接）
GET https://pdf.dfcfw.com/pdf/H2_{art_code}_1.pdf
```

**完整报告识别**：
- 年报：标题含 `年報` 或 `年度报告` 或 `Annual Report`
- 中期报告：标题含 `中期報告` 或 `中期报告` 或 `Interim Report`
- 业绩公告：标题含 `全年业绩`/`六个月业绩`/`九个月业绩`/`三个月业绩`

### 2. 同花顺（补充）

```python
# 公告列表 API
GET https://basic.10jqka.com.cn/basicapi/notice/pub
Params:
  - type: hk                  # hk=港股
  - code: HK{code}            # 如 "HK0700"
  - classify: all
  - page: 1
  - limit: 15

# PDF 下载（从 raw_url 获取）
raw_url → 直接下载 HKEX PDF
```

### 3. 披露易（兜底）

```python
# 获取 stockId
GET https://www1.hkexnews.hk/search/prefix.do
Params:
  - type: A
  - market: SEHK
  - name: {stock_code}
  - lang: ZH

# 搜索公告
POST https://www1.hkexnews.hk/search/titlesearch.xhtml
Form Data:
  - stockId: {stockId}
  - from: {YYYYMMDD}
  - to: {YYYYMMDD}
  - t1code: 40000
  - t2code: 40200
```

## 使用示例

### 示例 1: 下载腾讯 2020-2025 完整报告

```bash
python3 hk_downloader.py --stock=0700 --from=2020 --to=2025 --pdf
```

**输出**:
```
📊 港股财报下载: 腾讯控股 (0700.HK)
📡 数据源: 东方财富 → 同花顺 → 披露易
📅 时间范围: 2020-2025

【1/3】东方财富获取公告...
  获取 1401 条公告，筛选出 52 份核心文档

【2/3】去重: 完整报告优先
  年报: 8 份 (完整)
  中报: 6 份 (完整)
  Q1季报: 6 份
  Q3季报: 6 份

【3/3】下载 PDF...
  ✅ 2025_年报_2025 年报.pdf (964KB)
  ✅ 2024_年报_2024 年报.pdf (978KB)
  ✅ 2025_中报_中期报告 2025.pdf (12480KB)
  ...
  总计: 26/26 成功
```

### 示例 2: 只下载年报

```bash
python3 hk_downloader.py --stock=0700 --type=年报 --pdf
```

### 示例 3: 只获取清单，不下载 PDF

```bash
python3 hk_downloader.py --stock=0700 --from=2020 --to=2025
```

### 示例 4: 批量下载

```bash
python3 hk_downloader.py --stocks=0700,9988,3690 --from=2022 --to=2025 --pdf
```

## 已知 stockId 映射（披露易用）

| 公司 | 代码 | stockId |
|------|------|---------|
| 腾讯控股 | 00700 | 7609 |
| 阿里巴巴 | 09988 | 1000015694 |
| 美团 | 03690 | 198419 |
| 小米 | 01810 | 190371 |
| 京东 | 09618 | 1000042149 |
| 网易 | 09999 | 1000041666 |
| 比亚迪 | 01211 | 2696 |
| 农夫山泉 | 09633 | 1000054238 |
| 智谱 AI | 02513 | (需自动获取) |

## 去重规则

### 年报去重
```
同年有 "年報" (完整) → 保留 "年報"，丢弃 "全年业绩公布"
只有 "全年业绩公布" → 保留
```

### 中报去重
```
同年有 "中期報告" (完整) → 保留 "中期報告"，丢弃 "六个月业绩公布"
只有 "六个月业绩公布" → 保留
```

### 季报
```
Q1 和 Q3 只有业绩公告，无冲突
```

## 注意事项

### 1. 频率控制
- 东方财富：每次请求间隔 ≥ 0.2 秒
- 同花顺：每次请求间隔 ≥ 0.1 秒
- 披露易：每次请求间隔 ≥ 1 秒

### 2. 数据源选择
- 默认使用 `eastmoney,10jqka,hkex` 三级优先级
- 可指定单一数据源：`--source=eastmoney`

### 3. 失败处理
- PDF 下载失败：自动尝试下一个数据源
- API 超时：重试 3 次后跳过

### 4. 文件名规范
- 年报：`{year}_年报_{title}.pdf`
- 中报：`{year}_中报_{title}.pdf`
- 季报：`{year}_{Q1/Q3}_{title}.pdf`
- 招股书：`{year}_招股书_{title}.pdf`

## 相关资源

- **东方财富公告**: https://data.eastmoney.com/notices/
- **同花顺个股**: https://stockpage.10jqka.com.cn/HK{code}/news/
- **披露易**: https://www1.hkexnews.hk/listedcompany/listedinfo/index_c.htm

---

**作者**: 玄武 🐢  
**创建日期**: 2026-04-12  
**基于**: 东方财富 API + 同花顺 API + 披露易 API 验证
