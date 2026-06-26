name: goldskill
version: 1.0.0
description: 国际期货量化分析系统，支持黄金(XAUUSD)、白银(XAGUSD)、原油(CRUDEOIL)、天然气(NATGAS)、铜(COPPER)的实时行情、技术指标分析和相关新闻
primaryEnv: python
install:
  command: pip3 install -r requirements.txt
cwd: "${SKILL_DIR}"
requires:
  env:
    - name: OPENAI_API_KEY
      required: false
      description: "OpenAI API Key（可选，不影响核心功能）"
system:
  - python3
healthCheck:
  command: python3 agent.py --test
  interval: 3600
triggers:
  - pattern: "(黄金|金价|gold|XAU)"
    symbols: ["XAUUSD"]
  - pattern: "(白银|银价|silver|XAG)"
    symbols: ["XAGUSD"]
  - pattern: "(原油|油价|oil|WTI|Brent|OPEC)"
    symbols: ["CRUDEOIL"]
  - pattern: "(天然气|气价|natgas|LNG)"
    symbols: ["NATGAS"]
  - pattern: "(铜|铜价|copper)"
    symbols: ["COPPER"]
  - pattern: "(大宗商品|期货|commodity)"
    symbols: ["XAUUSD", "XAGUSD", "CRUDEOIL", "NATGAS", "COPPER"]
