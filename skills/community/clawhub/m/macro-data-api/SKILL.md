---
name: macro-data-api
display_name: 宏观经济数据查询
description: 查询货币供应量、汇率、利率和美元指数
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins: ["python3"]
      env: []
---

# 宏观经济数据查询 (Macro Data API)

通过本技能可以查询：
货币供应量=MoneyStockMeasures
季节性调整=SeasonallyAdjusted
未经季节性调整=NotSeasonallyAdjusted
实时汇率及美元指数=exchangeRate
利率=InterestRate
影响存款机构准备金余额的因素(资产端),单位百万美元=FARBODI
影响存款机构准备金余额的因素(负债端),单位百万美元=FARBODIC
备忘录项目,单位百万美元=MI
到期债券分布,单位百万美元=MDOSLASOAAL
按揭,单位百万美元=SIOMS
主要信贷工具余额,单位百万美元=IOPAOCFL
所有联邦储备银行的综合报表（美联储资产负债表）,单位百万美元=CSOCOAFRB
总资产(续),单位百万美元=CSOCOAFRBC
联邦储备银行状况说明,单位百万美元=SOCOEFRB
联邦储备银行状况说明(续),单位百万美元=SOCOEFRBC
联邦储备券对应的抵押品:联邦储备代理人的账户,单位百万美元=CHAFRNFRAA
美国商业银行的资产和负债年率(季节性调整后的)资产表=SAALOCBITUSS_ASSET
美国商业银行的资产和负债年率(季节性调整后的)负债表=SAALOCBITUSS_Liabilities
美国商业银行的资产和负债(季节性调整后的)资产表,单位十亿美元=AALOCBITUSS_ASSET
美国商业银行的资产和负债(季节性调整后的)负债表,单位十亿美元=AALOCBITUSS_Liabilities
美国商业银行的资产和负债(无季节性调整)资产表,单位十亿美元=AALOCBITUSNS_ASSET
美国商业银行的资产和负债(无季节性调整)负债表,单位十亿美元=AALOCBITUSNS_Liabilities
美国本土特许商业银行的资产和负债(季节性调整后的)资产表,单位十亿美元=AALODCCBITUSS_ASSET
美国本土特许商业银行的资产和负债(季节性调整后的)负债表,单位十亿美元=AALODCCBITUSS_Liabilities
美国本土特许商业银行的资产和负债(无季节性调整)资产表,单位十亿美元=AALODCCBITUSNS_ASSET
美国本土特许商业银行的资产和负债(无季节性调整)负债表,单位十亿美元=AALODCCBITUSNS_Liabilities
美国大型国内特许商业银行的资产和负债(季节性调整后的)资产表,单位十亿美元=AALOLDCCBITUSS_ASSET
美国大型国内特许商业银行的资产和负债(季节性调整后的)负债表,单位十亿美元=AALOLDCCBITUSS_Liabilities
美国大型国内特许商业银行的资产和负债(无季节性调整)资产表,单位十亿美元=AALOLDCCBITUSNS_ASSET
美国大型国内特许商业银行的资产和负债(无季节性调整)负债表,单位十亿美元=AALOLDCCBITUSNS_Liabilities
美国小型国内特许商业银行的资产和负债(季节性调整后的)资产表,单位十亿美元=AALOSDCCBITUSS_ASSET
美国小型国内特许商业银行的资产和负债(季节性调整后的)负债表,单位十亿美元=AALOSDCCBITUSS_Liabilities
美国小型国内特许商业银行的资产和负债(无季节性调整)资产表,单位十亿美元=AALOSDCCBITUSNS_ASSET
美国小型国内特许商业银行的资产和负债(无季节性调整)负债表,单位十亿美元=AALOSDCCBITUSNS_Liabilities
美国涉外机构的资产和负债(季节性调整后的)资产表,单位十亿美元=AALOFRIITUSS_ASSET
美国涉外机构的资产和负债(季节性调整后的)负债表,单位十亿美元=AALOFRIITUSS_Liabilities
美国涉外机构的资产和负债(无季节性调整)资产表,单位十亿美元=AALOFRIITUSNS_ASSET
美国涉外机构的资产和负债(无季节性调整)负债表,单位十亿美元=AALOFRIITUSNS_Liabilities
外汇储备=FER
贷款=Loan
国债收益率=USTreasuriesYields
国债规模=USTreasuriesSize
外国债券投资(各国当前美债持有数),单位十亿美元=FBI
个人消费支出,耐用消费品支出,非耐用消费品支出,服务消费支出=PCE
国内私人投资总额, 固定私人投资,私人库存变动=GPDI
商品和服务净出口,商品和服务进口,商品和服务出口=NETEXP
各行业对GDP的贡献=COVITGDP
人均GDP,平价购买力人均GDP=PCGDP
纽约联储-每周经济指数=WEI
生产者物价指数,消费价格指数=CPI_PPI


# Macro API Skill

## Description
Fetch U.S. macroeconomic and financial data from your local FastAPI server.
Supports default 1 record, custom limit, or date-based queries.

## Base URL
http://10.168.1.162:8000

## Usage Examples

# -------------------------------
# Money Supply Tables
# -------------------------------

# MoneyStockMeasures
# 查询最近 1 条 MoneyStockMeasures 数据
python3 skills/macro-data-api/macro_api.py MoneyStockMeasures

# 查询最近 5 条 MoneyStockMeasures 数据
python3 skills/macro-data-api/macro_api.py MoneyStockMeasures 5

# 查询指定日期 MoneyStockMeasures 数据
python3 skills/macro-data-api/macro_api.py MoneyStockMeasures 2026-03-31

# SeasonallyAdjusted
# 查询最近 1 条 SeasonallyAdjusted 数据
python3 skills/macro-data-api/macro_api.py SeasonallyAdjusted

# 查询最近 5 条 SeasonallyAdjusted 数据
python3 skills/macro-data-api/macro_api.py SeasonallyAdjusted 5

# 查询指定日期 SeasonallyAdjusted 数据
python3 skills/macro-data-api/macro_api.py SeasonallyAdjusted 2026-03-31

# NotSeasonallyAdjusted
# 查询最近 1 条 NotSeasonallyAdjusted 数据
python3 skills/macro-data-api/macro_api.py NotSeasonallyAdjusted

# 查询最近 5 条 NotSeasonallyAdjusted 数据
python3 skills/macro-data-api/macro_api.py NotSeasonallyAdjusted 5

# 查询指定日期 NotSeasonallyAdjusted 数据
python3 skills/macro-data-api/macro_api.py NotSeasonallyAdjusted 2026-03-31

# -------------------------------
# Exchange Rate Tables
# -------------------------------

# ExchangeRate
# 查询最近 1 条 ExchangeRate 数据
python3 skills/macro-data-api/macro_api.py ExchangeRate

# 查询最近 5 条 ExchangeRate 数据
python3 skills/macro-data-api/macro_api.py ExchangeRate 5

# 查询指定日期 ExchangeRate 数据
python3 skills/macro-data-api/macro_api.py ExchangeRate 2026-03-31

# -------------------------------
# Interest Rate Tables
# -------------------------------

# InterestRate
# 查询最近 1 条 InterestRate 数据
python3 skills/macro-data-api/macro_api.py InterestRate

# 查询最近 5 条 InterestRate 数据
python3 skills/macro-data-api/macro_api.py InterestRate 5

# 查询指定日期 InterestRate 数据
python3 skills/macro-data-api/macro_api.py InterestRate 2026-03-31

# -------------------------------
# FARBODI Tables
# -------------------------------

# FARBODI
python3 skills/macro-data-api/macro_api.py FARBODI
python3 skills/macro-data-api/macro_api.py FARBODI 5
python3 skills/macro-data-api/macro_api.py FARBODI 2026-03-31

# FARBODIC
python3 skills/macro-data-api/macro_api.py FARBODIC
python3 skills/macro-data-api/macro_api.py FARBODIC 5
python3 skills/macro-data-api/macro_api.py FARBODIC 2026-03-31

# -------------------------------
# MI Table
# -------------------------------
python3 skills/macro-data-api/macro_api.py MI
python3 skills/macro-data-api/macro_api.py MI 5
python3 skills/macro-data-api/macro_api.py MI 2026-03-31

# -------------------------------
# SIOMS Table
# -------------------------------
python3 skills/macro-data-api/macro_api.py SIOMS
python3 skills/macro-data-api/macro_api.py SIOMS 5
python3 skills/macro-data-api/macro_api.py SIOMS 2026-03-31

# -------------------------------
# IOPAOCFL Table
# -------------------------------
python3 skills/macro-data-api/macro_api.py IOPAOCFL
python3 skills/macro-data-api/macro_api.py IOPAOCFL 5
python3 skills/macro-data-api/macro_api.py IOPAOCFL 2026-03-31

# -------------------------------
# CSOCOAFRB Table
# -------------------------------
python3 skills/macro-data-api/macro_api.py CSOCOAFRB
python3 skills/macro-data-api/macro_api.py CSOCOAFRB 5
python3 skills/macro-data-api/macro_api.py CSOCOAFRB 2026-03-31

# -------------------------------
# CSOCOAFRBC Table
# -------------------------------
python3 skills/macro-data-api/macro_api.py CSOCOAFRBC
python3 skills/macro-data-api/macro_api.py CSOCOAFRBC 5
python3 skills/macro-data-api/macro_api.py CSOCOAFRBC 2026-03-31

# -------------------------------
# SOCOEFRB Table
# -------------------------------
python3 skills/macro-data-api/macro_api.py SOCOEFRB
python3 skills/macro-data-api/macro_api.py SOCOEFRB 5
python3 skills/macro-data-api/macro_api.py SOCOEFRB 2026-03-31

# -------------------------------
# SOCOEFRBC Table
# -------------------------------
python3 skills/macro-data-api/macro_api.py SOCOEFRBC
python3 skills/macro-data-api/macro_api.py SOCOEFRBC 5
python3 skills/macro-data-api/macro_api.py SOCOEFRBC 2026-03-31

# -------------------------------
# CHAFRNFRAA Table
# -------------------------------
python3 skills/macro-data-api/macro_api.py CHAFRNFRAA
python3 skills/macro-data-api/macro_api.py CHAFRNFRAA 5
python3 skills/macro-data-api/macro_api.py CHAFRNFRAA 2026-03-31

# -------------------------------
# PCE Table
# -------------------------------
python3 skills/macro-data-api/macro_api.py PCE
python3 skills/macro-data-api/macro_api.py PCE 5
python3 skills/macro-data-api/macro_api.py PCE 2026-03-31

# -------------------------------
# GPDI Table
# -------------------------------
python3 skills/macro-data-api/macro_api.py GPDI
python3 skills/macro-data-api/macro_api.py GPDI 5
python3 skills/macro-data-api/macro_api.py GPDI 2026-03-31

# -------------------------------
# NETEXP Table
# -------------------------------
python3 skills/macro-data-api/macro_api.py NETEXP
python3 skills/macro-data-api/macro_api.py NETEXP 5
python3 skills/macro-data-api/macro_api.py NETEXP 2026-03-31

# -------------------------------
# COVITGDP Table
# -------------------------------
python3 skills/macro-data-api/macro_api.py COVITGDP
python3 skills/macro-data-api/macro_api.py COVITGDP 5
python3 skills/macro-data-api/macro_api.py COVITGDP 2026-03-31

# -------------------------------
# PCGDP Table
# -------------------------------
python3 skills/macro-data-api/macro_api.py PCGDP
python3 skills/macro-data-api/macro_api.py PCGDP 5
python3 skills/macro-data-api/macro_api.py PCGDP 2026-03-31

# -------------------------------
# WEI Table
# -------------------------------
python3 skills/macro-data-api/macro_api.py WEI
python3 skills/macro-data-api/macro_api.py WEI 5
python3 skills/macro-data-api/macro_api.py WEI 2026-03-31

# -------------------------------
# CPI_PPI Table
# -------------------------------
python3 skills/macro-data-api/macro_api.py CPI_PPI
python3 skills/macro-data-api/macro_api.py CPI_PPI 5
python3 skills/macro-data-api/macro_api.py CPI_PPI 2026-03-31
