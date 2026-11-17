# 🦞 GKN-Phantom

> **Production-grade automated penetration testing skill for the OpenClaw AI Agent Framework.**

[![Version](https://img.shields.io/badge/version-5.4.0-blue)](https://github.com/your-org/gkn-phantom/releases)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-orange)](https://openclaw.ai)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)]()
[![Modules](https://img.shields.io/badge/modules-34-brightgreen)]()

GKN-Phantom 是一个面向 OpenClaw AI Agent 框架的工业级自动化渗透测试技能包。v5.4 配备 **34 个检测模块**，覆盖 **38 种漏洞类型**，支持 **25+ 种 WAF 识别**与绕过策略，**20+ 条攻击链模式**，在严格的 **Scope Guard · Risk Gate · Rate Limiter** 三重安全模型下，执行全生命周期安全验证：从零触碰被动侦察、主动资产发现、分层漏洞检测、交互式浏览器认证、证据验证、攻击路径分析到专业可视化报告生成。

**Quick Combat 一键管线**（v5.1 引入，v5.4 大幅强化）：`quick_combat.py` 单命令完成 检测 → 深挖 → PoC → 利用脚本 的实战闭环——nuclei 快扫 + 内置探针 + **国内组件/OA 未授权指纹库**（泛微/致远/通达/用友/禅道/JeecgBoot/若依等 32 条探针，含 queryFieldBySql 一键 SQL 验证）+ **katana 全站爬取喂参数注入探测** + **JS 深挖链**（密钥泄露 → 隐藏端点 → 主动探测）+ **真实 OOB 带外信道**（interactsh/ceye/dnslog，盲 SSRF 回调确认即 validated）+ **跨运行去重记忆**（`[已提交]/[重复]` 标注防 SRC 重复提交扣分）。

---

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 🔒 **三重安全模型** | Scope Guard（范围检查）+ Risk Gate（L1-L4风险分级）+ Rate Limiter（令牌桶限速） |
| 🎯 **38 种漏洞检测** | 覆盖 LOW → MEDIUM → HIGH → CRITICAL 四个严重级别 |
| 🕵️ **零触碰被动侦察** (v4) | crt.sh · DNS自建客户端 · WHOIS · Wayback Machine · GitHub秘密搜索 · 邮箱枚举 |
| 🔬 **深度主动侦察** (v4) | nmap端口扫描 · SSL/TLS安全分析 · 技术栈指纹识别（200+签名） · 智能目录爆破（116路径+20扩展名） |
| 💉 **专业SQL注入引擎** (v4) | 6种数据库指纹 · 5种提取策略（报错/布尔盲注/时间盲注/UNION/OOB） · 二阶注入 · 10类WAF绕过 |
| ⚡ **Nuclei模板集成** (v4) | 自动检测 · 80+技术到标签映射 · 执行时间预估 · SHA-256去重 · 未安装时回退手动指南 |
| 🛡️ **高级WAF绕过** (v4) | 协议级绕过 · 6种编码绕过 · 38种混淆生成器 · 10种WAF专用规则 · HPP · Content-Type切换 |
| 🌐 **交互式浏览器代理** (v5) | Playwright驱动多步骤认证 · 验证码/MFA/2FA处理 · 会话持久化 · JS执行 · 截图取证 |
| 📋 **专业PoC生成** (v5) | curl命令 · Python脚本 · HAR 1.2归档 · Markdown复现步骤 · 安全级别分类 |
| 🧠 **自适应探测引擎** | 失败自动重试（指数退避） · Payload变异绕过WAF（25+种） · 20+备用信号集 |
| 🛡️ **预飞行安全模拟** | dry-run模式 · 目标风险评分（0-100） · 自动收窄扫描范围 |
| 📊 **多因子置信度评分** | 证据强度+复现性+信号清晰度+佐证，≥0.80才升级为validated |
| 🔗 **20+攻击链分析** | SSRF→云元数据 · SQLi→凭证窃取 · SSTI→RCE · 原型污染→提权 · HTTP走私→投毒 |
| 📊 **可视化报告** (v5) | HTML仪表盘（SVG风险仪表+发现卡片+攻击路径图+资产表+修复矩阵+暗色模式） · PDF导出 |
| ⚙️ **规则配置化** (v5) | YAML/JSON规则定义 · 热加载 · 社区可扩展 · 无需修改Python代码即可添加检测规则 |
| ⚔️ **Quick Combat 一键管线** (v5.1-v5.3) | 单命令 detect → deep-dive → PoC → exploit · 影响升级层（响应内容重定级）· 深挖适配器（Actuator/GraphQL/Swagger）· 参数发现+有界SQLi/SSTI探测 |
| 🇨🇳 **国内组件/OA 探针库** (v5.4) | 32 条探针：泛微 e-cology（BeanShell/Ssologin//services/）· 致远 · 通达 · 用友 · 禅道 · JeecgBoot（jmreport queryFieldBySql 一键 SQL 验证）· 若依（druid 变体）· 帆软/亿邮/金蝶/蓝凌/红帆/万户 · POST 验证器 + 软 404 黑名单防误报 |
| 🕸️ **katana 全站爬取** (v5.4) | 有 katana 时全站爬取（深度 3），所有带参 URL 喂参数注入探测——SQLi/SSTi 覆盖从"首页参数"扩展到"全站面"；无 katana 自动回退单页 |
| 🔍 **JS 深挖链** (v5.4) | JS bundle 分析（密钥/危险Sink/调试端点）+ 隐藏端点提取（`extract_endpoint_entries`）回喂注入探测——JS 侦察链入主动探测 |
| 📡 **真实 OOB 带外信道** (v5.4) | interactsh 自托管/ceye.io/dnslog.cn 三通道 · 替换静态占位符 · 盲 SSRF 回调确认即产出 **validated** 级 finding（直接进 PoC/利用生成） |
| 🧠 **跨运行去重记忆** (v5.4) | finding 指纹持久化到 `combat_memory.json` · 重扫自动标注 `[已提交]/[重复]` · 防 SRC 平台重复提交扣分降信誉 |
| 🔄 **状态恢复系统** | checkpoint重试 · 部分状态恢复 · 失败回滚到安全前态 |
| 📊 **SARIF 2.1.0 输出** | CI/CD兼容，partialFingerprints基线去重 |
| 🔌 **工具自动检测** | nuclei · subfinder · httpx · ffuf · amass · katana · naabu 自动检测，缺失时回退纯Python实现 |
| 🧪 **测试框架** (v5) | pytest测试套件 · fixtures · CI集成 |
| ⏯️ **断点续扫** | 状态机持久化，任意阶段中断后继续 |

---

## 🧩 支持的漏洞类型

| 严重级别 | 漏洞类型 |
|----------|----------|
| **CRITICAL** | RCE, 认证绕过（auth_bypass）, 权限提升（priv_esc）, 数据泄露（data_exposure）, HTTP请求走私（http_smuggling） |
| **HIGH** | SQL注入（sqli）, 存储型XSS, SSRF, IDOR, 文件上传（file_upload）, 逻辑缺陷（logic_flaw）, NoSQL注入（nosql_injection）, LDAP注入（ldap_injection）, GraphQL注入（graphql_injection）, 缓存投毒（cache_poisoning）, 条件竞争（race_condition）, 原型污染（prototype_pollution）, JWT深度分析（jwt_deep_analysis）, OAuth配置缺陷（oauth_misconfig）, 批量赋值（mass_assignment）, 依赖混淆（dependency_confusion） |
| **MEDIUM** | 反射型XSS, 路径遍历（path_traversal）, XXE, SSTI, 命令注入（command_injection）, CSRF, 弱口令（weak_credential）, 验证码绕过（captcha_bypass）, 反序列化（deserialization）, CRLF注入（crlf_injection）, CORS配置缺陷（cors_misconfig）, 子域名接管（subdomain_takeover）, Host头注入（host_header_injection）, WebSocket劫持（websocket_hijacking）, Session固定（session_fixation）, 邮件头注入（email_injection） |
| **LOW** | 信息泄露（info_leak）, 开放重定向（open_redirect）, CSRF（弱令牌）, 安全配置错误（misconfig）, 组件未授权（component_exposure）, GraphQL内省（graphql_introspection）, 目录列表（directory_listing） |

---

## 🏗️ 架构设计

```
                        ┌─────────────────────────────────────┐
                        │        GKN-Phantom v5.4 Pipeline      │
                        ├──────────┬──────────┬────────────────┤
                        │  INIT    │  SCOPE   │  PRE_FLIGHT    │
                        │          │  CHECK   │  (dry-run)     │
                        ├──────────┼──────────┼────────────────┤
                        │ PASSIVE  │  ACTIVE  │  AUTH_SETUP    │
                        │  RECON   │  RECON   │  (optional)    │
                        ├──────────┼──────────┼────────────────┤
                        │  ACTIVE  │VALIDATION│  ATTACK PATH   │
                        │ TESTING  │          │  ANALYSIS      │
                        ├──────────┴──────────┴────────────────┤
                        │         REPORT GENERATION             │
                        │    (JSON + SARIF + HTML + PDF)        │
                        └──────────────────────────────────────┘
                                      │
                            ┌─────────▼─────────┐
                            │  三重安全模型       │
                            │  Scope Guard      │
                            │  Risk Gate (L1-L4)│
                            │  Rate Limiter     │
                            └───────────────────┘
```

### 11 阶段状态机

| 阶段 | 功能 | 关键脚本 |
|------|------|----------|
| **INIT** | 输入验证、配置加载、状态初始化 | `utils.py`, `state.py` |
| **SCOPE_CHECK** | 所有目标范围校验，任何越界即中止 | `scope_guard.py` |
| **PRE_FLIGHT** | dry-run模拟、目标风险评分、自动收窄范围 | `safety_simulator.py` |
| **PASSIVE_RECON** (v4) | 零触碰情报收集：crt.sh/DNS/WHOIS/Wayback/GitHub/邮箱 | `passive_recon.py` |
| **ACTIVE_RECON** (v4) | 端口扫描+目录爆破+技术指纹+SSL分析 | `directory_fuzzer.py`, `tech_fingerprint.py`, `ssl_analyzer.py` |
| **AUTH_SETUP** | 认证会话建立，支持浏览器交互式登录 | `browser_agent.py` (v5) |
| **ACTIVE_TESTING** | 分层漏洞探测（12个专项模块），自适应引擎处理失败/WAF | `vuln_detector.py`, `adaptive_engine.py`, `advanced_sqli.py`, `nuclei_runner.py`, `waf_evasion.py`, `js_analyzer.py`, `advanced_injection.py`, `api_auditor.py`, `cloud_security.py` |
| **VALIDATION** | 证据复验、TP/FP分类、多因子置信度评分 | `finding_validator.py`, `confidence_scoring.py`, `decision_engine.py` |
| **ATTACK_PATH_ANALYSIS** | 20+攻击链模式分析 | `attack_path.py` |
| **REPORT_GENERATION** | 多格式报告：JSON + SARIF + HTML + PDF | `report_generator.py`, `report_visualizer.py` (v5), `poc_generator.py` (v5) |
| **DONE** | 持久化状态，返回最终结果 | `state.py` |

---

## 📦 目录结构

```
GKN-Phantom/
├── SKILL.md                         # 技能主契约（完整规范，v5.4）
├── README.md                        # 本文件
├── scripts/                         # 可执行脚本（34 个）
│   ├── utils.py                     # 共享工具：JSON I/O、DNS解析、指纹、去重
│   ├── state.py                     # 状态序列化器：原子checkpoint、断点恢复
│   ├── state_recovery.py            # 状态恢复：checkpoint重试/部分恢复/失败回滚
│   ├── scope_guard.py               # 范围守卫：域名/IP/CIDR/路径校验
│   ├── rate_limiter.py              # 令牌桶速率限制器
│   ├── safety_simulator.py          # 安全模拟器：dry-run/风险评分/范围收窄
│   ├── vuln_detector.py             # 分层漏洞检测引擎（38种类型）
│   ├── adaptive_engine.py           # 自适应引擎：25+WAF识别/38类型变异/20+备用信号
│   ├── finding_validator.py         # 发现验证器：TP/FP分类
│   ├── confidence_scoring.py        # 置信度评分：多因子加权
│   ├── decision_engine.py           # 启发式决策引擎（可选插件）
│   ├── execution_trace.py           # 执行追踪：固定决策记录/回放验证/diff
│   ├── attack_path.py               # 攻击路径图构建器（20+攻击链模式）
│   ├── report_generator.py          # JSON/SARIF报告生成器
│   │
│   │   # ── v3 专项模块 ──
│   ├── js_analyzer.py               # JS静态分析：密钥泄露/危险Sink/原型污染/弱加密
│   ├── cve_correlator.py            # CVE关联：技术栈CVE匹配/CVSS评分/漏洞利用
│   ├── advanced_injection.py        # 高级注入：NoSQL/LDAP/CRLF/走私/投毒/条件竞争
│   ├── api_auditor.py               # API审计：GraphQL/REST/WebSocket安全检测
│   ├── cloud_security.py            # 云安全：S3/K8s/Docker/元数据/容器镜像检测
│   │
│   │   # ── v4 新增模块 ──
│   ├── passive_recon.py             # 被动侦察：crt.sh/DNS/WHOIS/Wayback/GitHub/邮箱
│   ├── directory_fuzzer.py          # 目录爆破：10词表类别/SimHash 404检测/递归/技术优先
│   ├── advanced_sqli.py             # SQL注入引擎：6引擎/5提取策略/二阶注入/10类WAF绕过
│   ├── ssl_analyzer.py              # SSL分析：证书链/密码套件分级/协议检测/7种漏洞检查
│   ├── tech_fingerprint.py          # 技术指纹：200+签名/19 favicon哈希/OS检测
│   ├── nuclei_runner.py             # Nuclei集成：自动检测/80+技术映射/去重/回退指南
│   ├── waf_evasion.py               # WAF绕过：协议级/6编码/38混淆/10 WAF/HTTP参数污染
│   │
│   │   # ── v5 新增模块 ──
│   ├── report_visualizer.py         # 可视化报告：HTML仪表盘/SVG图表/暗色模式/PDF导出
│   ├── browser_agent.py             # 浏览器代理：Playwright/多步骤认证/验证码/MFA/2FA
│   ├── poc_generator.py             # PoC生成器：curl/Python/HAR/Markdown/安全分类
│   │
│   │   # ── v5.1-v5.3 Quick Combat ──
│   ├── quick_combat.py              # 一键实战管线：检测→深挖→PoC→利用→HTML报告+manifest
│   ├── exploit_generator.py         # 利用脚本生成器：validated findings→自包含Python演示脚本
│   │
│   │   # ── v5.4 Combat 强化 ──
│   ├── cn_probes.py                 # 国内组件/OA未授权探针库：泛微/致远/通达/用友/禅道/JeecgBoot/若依等32条
│   └── oob_client.py                # 真实OOB带外信道：interactsh自托管/ceye.io/dnslog.cn，盲SSRF回调验证
│
├── rules/                           # 规则配置目录 (v5)
│   ├── low.yaml                     # LOW级别规则（10条）
│   ├── medium.yaml                  # MEDIUM级别规则（16条）
│   ├── high.yaml                    # HIGH级别规则（15条）
│   ├── critical.yaml                # CRITICAL级别规则（6条）
│   ├── waf_signatures.yaml          # 25+ WAF签名库
│   └── mutation_strategies.yaml     # 变异策略配置
│
├── tests/                           # 测试套件 (v5, 200+ 用例)
│   ├── conftest.py                  # pytest fixtures
│   ├── test_vuln_detector.py        # 漏洞检测引擎测试
│   ├── test_adaptive_engine.py      # 自适应引擎测试
│   ├── test_rules_loader.py         # 规则加载器测试
│   ├── test_utils.py                # 共享工具测试
│   ├── test_report_generator.py     # 报告生成器测试
│   ├── test_quick_combat.py         # Quick Combat管线测试（深挖/注入/OOB/katana/JS/memory）
│   ├── test_cn_probes.py            # 国内组件探针库测试（本地假OA目标）
│   └── test_oob_client.py           # OOB信道客户端测试（假API+mock interactsh）
│
├── references/                      # 参考文档（7 个）
│   ├── safety_policy.md             # 安全模型完整规范
│   ├── data_schemas.md              # 所有JSON Schema定义
│   ├── payload_playbook.md          # 非破坏性检测Payload手册
│   ├── advanced_payload_playbook.md # 高级Payload手册
│   ├── script_contracts.md          # 脚本接口契约
│   ├── formal_algorithms.md         # 可解释评分规则文档
│   └── tool_contracts.json          # 机器可读JSON Schema
│
└── assets/                          # 示例与清单
    ├── manifest.yml                 # 技能部署清单（v5.0）
    ├── example_input.json           # 示例AgentContext输入
    ├── example_trace.json           # 完整执行追踪
    └── example_report.json          # 期望输出示例
```

---

## 🚀 快速开始

### 环境要求

#### 必需依赖

| 依赖 | 版本 | Kali | CentOS/RHEL |
|------|------|------|-------------|
| Python | ≥ 3.10 | 预装 | `dnf install python3` |
| nmap | 任意 | 预装 | `dnf install nmap` |

#### 可选工具（自动检测，缺失时回退纯Python实现）

| 工具 | 用途 | 安装命令 |
|------|------|----------|
| `nuclei` | 模板化CVE扫描 | `go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest` |
| `subfinder` | 主动子域名爆破 | `go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest` |
| `httpx` | 高速存活探测 | `go install github.com/projectdiscovery/httpx/cmd/httpx@latest` |
| `ffuf` | 高速目录Fuzz | `go install github.com/ffuf/ffuf/v2@latest` |
| `amass` | 深度DNS枚举 | `go install github.com/owasp-amass/amass/v4/...@master` |
| `katana` | JS爬虫与端点发现 | `go install github.com/projectdiscovery/katana/cmd/katana@latest` |
| `naabu` | 快速端口扫描 | `go install github.com/projectdiscovery/naabu/v2/cmd/naabu@latest` |

#### v5 可选依赖

| 工具 | 用途 | 安装命令 |
|------|------|----------|
| `playwright` | 交互式浏览器代理（验证码/MFA/认证） | `pip install playwright && playwright install chromium` |
| `pytesseract` | 验证码OCR识别（实验性） | `pip install pytesseract` |
| `weasyprint` | PDF报告导出 | `pip install weasyprint` |
| `pytest` | 测试框架 | `pip install pytest` |

### Kali 一键安装

```bash
# 基础工具链
sudo apt update && sudo apt install -y nmap golang-go

# ProjectDiscovery 全家桶
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest
go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest

# v5 增强
pip install playwright && playwright install chromium
pip install weasyprint pytest

echo 'export PATH=$PATH:$HOME/go/bin' >> ~/.zshrc && source ~/.zshrc
```

### 在 OpenClaw 中使用

```yaml
skills:
  - name: gkn-phantom
    source: ./gkn-phantom
    manifest: assets/manifest.yml
```

触发调用：

```
user: "对 staging.example.com 进行一次安全审计"
user: "Run a penetration test on dev-internal.test"
```

### 独立脚本测试

```bash
# ── Quick Combat 一键实战管线（推荐入口）──
# 全层开启：nuclei + 内置探针 + 国内组件探针 + katana爬取 + JS深挖 + 跨运行去重
python scripts/quick_combat.py --targets targets.txt --output-dir ./combat_output/

# 配置 OOB 带外信道（盲SSRF回调验证 → validated级finding）
python scripts/quick_combat.py --targets targets.txt --oob-provider ceye \
    --ceye-identifier <id> --ceye-token <token>

# interactsh 自托管 / 本机安装
python scripts/quick_combat.py --targets targets.txt --oob-provider interactsh \
    --interactsh-server https://oast.your-domain.test

# 精简模式：只要内置探针，关闭所有外部依赖
python scripts/quick_combat.py --targets targets.txt --no-nuclei --no-crawl \
    --no-js --no-memory

# OOB 信道自检
python scripts/oob_client.py --provider auto --tag selftest --wait 5

# 国内组件探针单跑（泛微/通达/若依/JeecgBoot/致远/用友/禅道...）
python scripts/cn_probes.py --targets https://oa.example.com

# ── 单模块使用 ──
# 被动侦察（零触碰）
python scripts/passive_recon.py --domain example.com --mode all

# 技术栈指纹
python scripts/tech_fingerprint.py --url https://target.com

# SSL安全分析
python scripts/ssl_analyzer.py --host target.com --port 443

# 目录爆破
python scripts/directory_fuzzer.py --url https://target.com --wordlist all --extensions php,asp --depth 2

# SQL注入探测
python scripts/advanced_sqli.py --url "https://target.com?id=1" --param id --db-type auto

# WAF绕过变异
python scripts/waf_evasion.py --payload "' OR 1=1--" --vuln-type sqli --waf-type cloudflare

# 漏洞检测
python scripts/vuln_detector.py --tier low,medium --safe-mode

# 规则验证
python scripts/rules_loader.py --validate

# PoC生成
python scripts/poc_generator.py --findings findings.json --format curl,python,har

# 可视化报告
python scripts/report_visualizer.py --findings findings.json --assets assets.json --paths paths.json --log log.json --format html

# 浏览器认证代理
python scripts/browser_agent.py --url https://target.com/login --auth-steps steps.json

# 运行测试
python -m pytest tests/ -v
```

---

## 🛡️ 安全模型

GKN-Phantom 的安全模型是**不可协商的**。每个操作都经过三层防护：

### 1. Scope Guard（范围守卫）
- 每个目标、每个请求、每个工具调用在执行前都须通过 `ctx.scope` 校验
- 支持域名通配符（`*.staging.example.test`）、IP CIDR、路径白名单/黑名单
- 越界目标 → 立即中止，不执行部分扫描

### 2. Risk Gate（风险门控）
- **L1** — 被动侦察（允许）
- **L2** — 安全探测（允许）
- **L3** — 认证测试（需提供凭据）
- **L4** — 破坏性/提权/写操作（需人工审批，Safe Mode 下完全阻断）

### 3. Rate Limiter（速率限制）
- 令牌桶算法，默认 ≤ 3 req/s，突发上限 5
- 超限请求排队而非丢弃，保障扫描稳定性

### 4. Evidence Requirement（证据要求）
- 每个发现必须包含：`request` + `response` + `timestamp` + `tool` + `reproducible`
- 证据不完整 → 在 VALIDATION 阶段被拒绝

---

## 📊 输出示例

### JSON/SARIF 报告

```json
{
  "summary": "在 staging.example.test 发现 9 个安全问题：1 个严重、2 个高危、3 个中危、3 个低危",
  "risk_score": 85,
  "findings": [
    {
      "id": "finding-001",
      "type": "sqli",
      "severity": "high",
      "target": "https://staging.example.test/api/users?id=1",
      "status": "validated",
      "confidence": 0.95,
      "evidence": {
        "request": "GET /api/users?id=1' OR '1'='1 HTTP/1.1 ...",
        "response": "HTTP/1.1 200 OK ... [all user records returned]",
        "timestamp": "2026-08-05T14:05:30Z",
        "tool": "httpRequest"
      },
      "reproducible": true,
      "remediation": "使用参数化查询或预编译语句，对所有用户输入进行严格过滤"
    }
  ],
  "attack_paths": [
    {
      "id": "path-001",
      "name": "SQL注入 → 凭证窃取 → 横向移动",
      "impact": "攻击者可提取全部用户密码哈希并尝试撞库",
      "confidence": 0.9
    }
  ]
}
```

### HTML 可视化报告 (v5)

执行 `report_visualizer.py` 生成包含以下内容的专业HTML报告：
- **执行仪表盘**：SVG风险评分仪表（绿/黄/橙/红）+ 按严重级别统计卡片
- **发现详情卡片**：彩色编码可折叠卡片，含请求/响应证据、修复建议、CVSS 3.1评分矩阵
- **攻击路径图**：纯SVG渲染的攻击链有向图，悬停显示详情
- **资产清单表**：可排序HTML表格，含域名/IP/端口/技术栈/SSL评级
- **技术栈摘要**：WAF检测标记 + 技术卡片网格
- **修复优先矩阵**：2x2 工作量×影响力矩阵
- **交互功能**：严重级别过滤 · 关键词搜索 · 全部展开/折叠 · 暗色模式切换

---

## 🔧 配置选项

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `rate_limit_rps` | int | 3 | 每秒最大请求数 |
| `safe_mode` | bool | true | 是否阻断 L4 级探测 |
| `require_human_approval` | bool | true | L4 操作是否需要人工审批 |
| `environment` | string | — | 环境类型：staging / dev / internal / lab |

---

## 📋 版本历史

| 版本 | 日期 | 主要更新 |
|------|------|----------|
| **v5.4.0** | 2026-09 | 国内组件/OA 未授权探针库（32条：泛微/致远/通达/用友/禅道/JeecgBoot/若依/帆软/亿邮/金蝶/蓝凌/红帆/万户，含 POST 一键验证器）· 真实 OOB 带外信道（interactsh 自托管/ceye.io/dnslog.cn，盲 SSRF 回调验证 → validated）· katana 全站爬取喂参数注入探测 · JS 深挖链（js_analyzer + 隐藏端点提取回喂探测）· 跨运行去重记忆（combat_memory.json，`[已提交]/[重复]` 标注） |
| **v5.3.0** | 2026-09 | Deep-Dive 深挖适配器（Actuator/GraphQL/Swagger：拉取实际暴露内容证明影响并升级严重级）· 参数发现 + 有界注入探测（报错型 SQLi 6 引擎签名 + SSTI 算术反射差分） |
| **v5.2.0** | 2026-09 | 影响升级层：quick-probe findings 按响应内容重定级（活跃凭据/.git/heapdump/phpinfo/备份包 → high；PII 数据暴露评分 ≥3 → critical） |
| **v5.1.0** | 2026-08 | Quick Combat Mode：单命令 detect → PoC → exploit 实战管线 · 利用脚本生成器 · 时间戳战斗报告 + HTML 索引 |
| **v5.0.0** | 2026-08 | 交互式浏览器代理（Playwright）· 可视化HTML/PDF报告 · 规则配置化（YAML热加载） · 专业PoC生成器 · pytest测试框架 |
| **v4.0.0** | 2026-08 | 被动侦察（crt.sh/DNS/WHOIS/Wayback/GitHub）· 目录爆破 · 专业SQL注入引擎 · SSL分析 · 技术指纹（200+签名） · Nuclei集成 · WAF绕过引擎 |
| **v3.0.0** | 2026-07 | 38种漏洞类型（+16种高级）· 5个专项模块（JS/CVE/高级注入/API/云安全）· 20+攻击链 · 25+WAF识别 |
| **v2.2.0** | 2026-07 | 确定性启发式决策引擎 · 执行追踪与回放 · 可解释评分规则 |
| **v2.1.0** | 2026-07 | 状态恢复系统 · 机器可读工具契约 |
| **v2.0.0** | 2026-06 | 预飞行安全模拟 · 自适应探测引擎 · 多因子置信度评分 · 强Schema契约 |
| **v1.0.0** | 2026-06 | 初始版本：22种漏洞类型 · 基础状态机 · Scope Guard · Rate Limiter |

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request。贡献前请确保：

1. 新增漏洞检测规则优先添加到 `rules/*.yaml` 配置文件，实现热加载
2. 所有探测 Payload 必须为非破坏性（仅检测，不利用）
3. 跨平台兼容（Windows / Linux 均需测试）
4. 新增模块需同时更新 `SKILL.md`、`README.md` 和 `manifest.yml`
5. 通过 pytest 测试套件

---

## ⚠️ 免责声明

**GKN-Phantom 仅供授权安全测试使用**：企业内部安全审计、预发布/开发/实验环境验证。**严禁**在未经授权的系统、生产环境或第三方目标上使用。未经授权使用可能构成违法行为，使用者需自行承担全部法律责任。

---

## 📄 许可证

MIT License © 2026

---

<p align="center">
  <sub>Built with 🔥 for the OpenClaw ecosystem</sub>
</p>
