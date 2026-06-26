# 数据源URL

## 国家统计局官网

### 主站
- **官网首页**: https://www.stats.gov.cn
- **数据发布页面**: https://www.stats.gov.cn/sj/zxfb/
- **data.stats.gov.cn**: https://data.stats.gov.cn

### ⚠️ 重要：API变化
- 旧API（已废弃）: `https://data.stats.gov.cn/easyquery.htm` → 返回404
- 新API: 需要使用新的URL格式

---

## 统计年鉴

### URL格式规则

**重要**：年鉴URL格式不统一！

| 数据年份 | 年鉴URL | 格式说明 |
|---------|---------|---------|
| 2003年数据 | `https://www.stats.gov.cn/sj/ndsj/yb2004-c/indexch.htm` | ⚠️ 特殊格式 |
| 2004年数据 | `https://www.stats.gov.cn/sj/ndsj/2005/indexch.htm` | 数字格式 |
| ... | ... | ... |
| 2024年数据 | `https://www.stats.gov.cn/sj/ndsj/2025/indexch.htm` | 数字格式 |

**规则**：数据年份N → 年鉴年份N+1

### 2003年数据（特殊情况）
- URL: `https://www.stats.gov.cn/sj/ndsj/yb2004-c/indexch.htm`
- PDF: `https://www.stats.gov.cn/sj/ndsj/yearbook2003_c.pdf`
- ⚠️ 2003年鉴PDF主要含2002年数据

### 年鉴数据表URL示例

#### 2010年年鉴（HTML格式）
- 国内生产总值: `.../ndsj/2010/html/C0201C.HTM`
- 不变价GDP: `.../ndsj/2010/html/C0203C.HTM`
- GDP构成: `.../ndsj/2010/html/C0202C.HTM`

#### 2015年年鉴（图片格式）
- 国内生产总值: `.../ndsj/2015/html/CH0303.jpg`
- ⚠️ 2015年后多为JPG图片格式

#### 2020/2024年年鉴
- GDP: `.../ndsj/2020/html/C0303.jpg`
- GDP: `.../ndsj/2024/html/C03-03.jpg`

---

## 统计公报

### 2025年GDP初步核算结果

| 季度 | 发布日期 | URL |
|------|---------|-----|
| 2025Q1 | 2025-04-17 | https://www.stats.gov.cn/sj/zxfb/202504/t20250417_1959334.html |
| 2025Q2 | 2025-07-16 | https://www.stats.gov.cn/sj/zxfb/202507/t20250716_1960426.html |
| 2025Q3 | 2025-10-21 | https://www.stats.gov.cn/sj/zxfb/202510/t20251021_1961646.html |
| 2025Q4 | 2026-01-20 | https://www.stats.gov.cn/sj/zxfb/202601/t20260120_1962349.html |

### 历史公报（搜索获取）
- 搜索URL: `https://www.google.com/search?q=site:stats.gov.cn+{年份}+GDP+初步核算`
- 示例: `site:stats.gov.cn 2010年一季度 GDP 初步核算`

---

## data.stats.gov.cn 数据平台

### 季度数据
- 入口: https://data.stats.gov.cn/easyquery.htm?cn=B01
- ⚠️ 旧API已返回404

### 月度数据
- 入口: https://data.stats.gov.cn/easyquery.htm?cn=A01

### 年度数据
- 入口: https://data.stats.gov.cn/easyquery.htm?cn=A02

---

## 验证链接有效性

### 批量检查脚本
```bash
#!/bin/bash
for data_year in {2003..2024}; do
    yb=$((data_year+1))
    
    # 2004年鉴特殊格式
    if [ $yb -eq 2004 ]; then
        url="https://www.stats.gov.cn/sj/ndsj/yb2004-c/indexch.htm"
    else
        url="https://www.stats.gov.cn/sj/ndsj/${yb}/indexch.htm"
    fi
    
    http_code=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    
    if [ "$http_code" = "200" ]; then
        echo "✅ $data_year -> ${yb}年鉴"
    else
        echo "❌ $data_year -> ${yb}年鉴: HTTP $http_code"
    fi
done
```

---

## 数据获取优先级

当多个数据源可用时，按以下优先级选择：

### GDP数据
1. **统计公报**（最新数据，最权威）
2. **统计年鉴**（历史数据，已修订）
3. **data.stats.gov.cn**（实时数据）

### CPI/PPI数据
1. **data.stats.gov.cn API**
2. **中国人民银行网站**
3. **统计年鉴**

### 历史数据（2015年前）
1. **统计年鉴PDF** → OCR识别
2. **替代数据源**（如CEIC、Bloomberg）

---

## 常见问题

### Q: 为什么2004年鉴URL是yb2004-c？
A: 这是统计局网站的特殊命名规则，其他年份使用数字格式。

### Q: 年鉴页面返回404怎么办？
A: 可能是网站临时不可用，尝试多次或等待后重试。

### Q: 如何找到具体指标在年鉴中的位置？
A: 在年鉴目录页搜索"国内生产总值"或"GDP"。

### Q: 2026年鉴什么时候发布？
A: 通常次年9-10月发布（如2026年鉴约2026年9月发布2025年数据）。
