# GKN-Phantom 双场景使用手册

> 适用版本：v5.1.0
> 适用场景：**护网行动（防守方自查/验证）** 与 **漏洞挖掘（授权 SRC / 众测 / 赏金）**
> 红线：所有使用必须以**书面授权**为前提。护网场景测的是己方资产；漏洞挖掘场景测的是 SRC 公告范围内的资产。越界即违法。

---

## 一、两个场景的本质差异（决定用法差异）

| 维度 | 护网行动（防守自查） | 漏洞挖掘（SRC/众测） |
|------|---------------------|----------------------|
| 授权深度 | 己方资产，可拿到凭据、源码、测试窗口 | 黑盒为主，仅公告范围内资产 |
| 目标 | **清零可利用面**：宁可误报不可漏报 | **高质量报告**：每条都要可复现、危害论证充分 |
| 节奏 | 护网前集中自查 + 护网期间持续回归 | 长期、分批、深挖单点 |
| safe_mode | 内网/预发可关（`--include-l4` 需审批） | **必须开启**，遵守厂商测试规范 |
| 凭据 | 应提供（AUTH_SETUP 全开） | 通常无；部分 SRC 提供测试账号 |
| 输出消费者 | 运维/开发（要修复清单） | SRC 审核员（要 PoC + 影响证明） |

---

## 二、护网行动场景

### 2.1 护网前 2 周：暴露面清查（被动 + 主动侦察）

目标：摸清"自己会挨打的入口"，先于攻击队发现自己。

```bash
# 1. 被动侦察：零接触，先做资产摸底（子域名/DNS/WHOIS/历史URL/GitHub泄露）
python scripts/passive_recon.py --domain example.com --output recon/passive.json

# 2. 技术指纹：确认每个资产跑的是什么（决定后续检测策略）
python scripts/tech_fingerprint.py --targets targets.txt --output recon/tech.json

# 3. 目录/敏感路径清查：116 条精选路径 + 20 种扩展名
python scripts/directory_fuzzer.py --targets targets.txt --output recon/dirs.json
```

**检查清单**（护网前必须清零的项）：

- [ ] `.git` / `.env` / `.DS_Store` / `phpinfo.php` 可外部访问
- [ ] Actuator / Druid / Swagger / UEditor 未授权
- [ ] 备份文件（`.zip/.tar.gz/.bak`）可下载
- [ ] 目录浏览（`Index of /`）
- [ ] SSL 弱协议/弱加密套件（`ssl_analyzer.py`，评级低于 A 的要整改）
- [ ] GitHub 泄露的密钥/内部地址（passive_recon 的 dork 输出人工过一遍）

### 2.2 护网前 1 周：快速对抗演练（Quick Combat）

目标：用攻击队视角快速打一遍，产出"今晚就能修"的清单。

```bash
python scripts/quick_combat.py \
  --targets targets.txt \
  --tech recon/tech.json \
  --output-dir ./combat_pre_hw/ \
  --severity critical,high,medium
```

- `--tech` 传入第 2 步的指纹结果，让 nuclei 模板选择更精准。
- 产出的 `combat_*/index.html` 直接分发给各系统负责人；`pocs/` 目录是可复制的验证命令。

### 2.3 护网前：深度审计（完整状态机）

对核心业务系统（支付、认证、数据中台）走完整管线：

```
SCOPE_CHECK → PRE_FLIGHT → PASSIVE_RECON → ACTIVE_RECON
→ AUTH_SETUP（提供测试账号凭据！）→ ACTIVE_TESTING（low→critical 全层级）
→ VALIDATION（复放验证 + 置信度评分）→ ATTACK_PATH_ANALYSIS → REPORT
```

护网场景特有配置建议：

```json
{
  "config": {
    "safe_mode": false,
    "require_human_approval": true,
    "rate_limit_rps": 10
  },
  "credentials": { "cookies": "...", "note": "预发环境测试账号" }
}
```

- `safe_mode: false` 解锁 SSRF/RCE 等 L4 探测（仅限预发/内网，生产禁用在侧）。
- **务必提供凭据**：护网中真正致命的是认证后的越权（IDOR/priv_esc）和逻辑缺陷，无凭据测试等于漏掉半个攻击面。
- `require_human_approval: true` 保留 L4 人工闸门，防止误伤。

### 2.4 护网期间：修复验证 + 持续回归

- 修复完成后，用对应 finding 的 PoC（`pocs/` 里的 curl/Python）单独复测，确认信号消失。
- 每日跑一遍 quick_combat，用 `manifest.json` 的 `by_severity` 对比昨日基线，发现"修 A 坏 B"或新上线系统带病。
- CI 集成：`report_generator` 产出 SARIF-like JSON，可接入流水线门禁（出现 high+ 即阻断发布）。

### 2.5 护网场景 Do / Don't

| Do | Don't |
|----|-------|
| 对生产只跑 L1-L2（被动侦察 + 非侵入探测） | 在生产窗口外跑 L4 探测 |
| 攻击链分析结果同步给 SOC，作为监控规则输入 | 只看单点漏洞，忽略 attack_paths 里的链式风险 |
| 用 `execution_trace.py` 留痕，应对护网审计 | 跳过 VALIDATION 直接拿扫描器结果交差 |

---

## 三、漏洞挖掘场景（授权 SRC / 众测）

### 3.1 铁律（厂商规范 + 法律边界）

1. 只测 SRC 公告**范围内**的资产；`scope_guard` 会把越界目标直接 ABORT——不要试图绕过它。
2. `safe_mode` 保持开启；不使用破坏性 payload；不碰真实用户数据（IDOR 验证用自己的两个账号做差分）。
3. 每个 finding 必须过 Reproducibility Gate——SRC 审核员只看可复现的东西，`unverified_leads[]` 交上去只会拉低信誉。

### 3.2 标准工作流

```bash
# Step 1: 被动侦察扩面（子域名是 SRC 挖掘的第一战场）
python scripts/passive_recon.py --domain target-src.com --output recon/

# Step 2: 对子域名批量存活探测 + 指纹
python scripts/tech_fingerprint.py --targets subdomains.txt --output recon/tech.json

# Step 3: Quick Combat 批量过筛（广撒网）
python scripts/quick_combat.py \
  --targets live_hosts.txt \
  --tech recon/tech.json \
  --severity critical,high,medium,low \
  --rate-limit 100
```

- 注意 severity 过滤加上 `low`：SRC 场景里 `component_exposure`、`info_leak` 这类低危也是有效提交（且常是深挖入口）。
- nuclei 模板被封顶时（manifest 里有 `Scope-limited` 提示），把目标按技术栈分组分批跑，避免高价值模板被挤掉。

### 3.3 深挖单点（从"发现"到"高危报告"）

Quick Combat 命中后的深挖路径（这是报告价值拉开差距的地方）：

| 命中信号 | 深挖动作 | 用到的模块 |
|----------|---------|-----------|
| `component_exposure` (Actuator) | 拉 `/actuator/heapdump`、`/actuator/env` 提取凭据 → 升级为数据泄露 | 手动 + httpRequest |
| `graphql_introspection` | 拉完整 schema → 找未授权 mutation/敏感字段 | `api_auditor.py` |
| `info_leak` (.git) | 还原源码 → 白盒找硬编码密钥/未授权接口 | git-dumper 类工具（手工） |
| 带参 URL | SQLi 报错/布尔/时间盲注（capped）、SSTI 算术反射 | `advanced_sqli.py` |
| 登录/注册接口 | 弱口令（bounded set）、验证码绕过、短信轰炸 | `vuln_detector.py` MEDIUM 层 |
| 任意业务功能 | 返回包篡改、价格/数量篡改、步骤跳过、重放 | `logic_flaw` 检测 |

每个深挖 finding 都要走完：

```
detected → PoC 生成（poc_generator）→ finding_validator 复放 ≥2 次
→ 控制请求对比 → 影响证明（读到了什么数据/拿到了什么会话）
→ attack_path.py 看能否成链 → 报告
```

### 3.4 提升报告过审率与定级的技巧

1. **影响证明是定级的核心**：同样的 SQLi，"存在注入"是 medium，"`current_user()` 回显 + 读出库名"是 high，"拖出 PII 样本（遵守最小化原则，脱敏展示）"才可能 critical。报告里写清**实际观察到的影响**，不要写理论影响。
2. **善用攻击链**：单点是 medium 的组合（如 组件泄露 → 拿到凭据 → 登录后台）在 `attack_path.py` 里成链后，按链的最终影响叙事，定级显著更高。
3. **`unverified_leads[]` 是你的线索队列**：本次复现不了的（WAF 拦截、需带内交互）记下来，换 `adaptive_engine` 的编码/变形策略隔日再试，或换 OOB 信道验证。
4. **去重**：`memory` 机制会对历史 finding 去重，重复提交前先查自己的历史报告，避免被 SRC 判重复。
5. **PoC 用 curl + raw_http 双格式提交**：审核员复现成本越低，过审越快。

### 3.5 漏洞挖掘场景 Do / Don't

| Do | Don't |
|----|-------|
| 严格遵守厂商 rate limit，把 `--rate-limit` 调到公告允许值以下 | 用默认 150 rps 猛冲（会被封 IP 且可能被取消成绩） |
| 弱口令/文件上传类测试走人工审批流程 | 上传真实 webshell、拖真实用户数据 |
| 把 `confidence_breakdown` 附在报告里增强说服力 | 把 nuclei 原始输出不加验证直接当漏洞提交 |

---

## 四、能力现状与路线图说明

以下能力在 v5.1 中的现状，以及已规划升级（见改造方案）：

| 能力 | 状态 |
|------|------|
| quick 探针内容感知升级 | **已上线（v5.2）**：`escalate_severity()` — 密钥/.git 泄露/phpinfo/备份可达→high，PII 阈值→critical（与完整状态机同口径），升级附 `escalation_reason` |
| quick 模式影响验证 | **已上线（v5.3 C1）**：深挖适配器 — Actuator env 未脱敏凭据/heapdump 可达→critical、GraphQL schema+mutation 暴露→high、Swagger 无认证方案→high，自动记录 `deep_dive.impact` |
| 参数发现 + 注入探测 | **已上线（v5.3 C2）**：入口页自动提取同源带参 URL → 报错型 SQLi（6 引擎签名）+ SSTI 算术反射（基线差分）→ 直接产出 high findings |
| 认证后测试 | 完整状态机支持；护网场景直接可用，SRC 场景视厂商是否提供测试账号 |

v5.3 起 Quick Combat 的深挖层默认开启（`--no-deep` 可关）：命中即深挖、按证据升级。SRC 提交前仍建议人工复核 `escalation_reason` / `deep_dive.impact` 与证据的一致性。

---

## 五、常用命令速查

| 场景 | 命令 |
|------|------|
| 快速过筛 | `python scripts/quick_combat.py --targets t.txt --severity critical,high,medium` |
| 关闭深挖层（纯 v5.1 行为） | 加 `--no-deep` |
| 无 nuclei 环境 | 加 `--no-nuclei`（仅用内置探针） |
| 只看内置探针 | 加 `--no-nuclei --quick-probes-only` 等价行为 |
| 深度审计某层级 | `python scripts/vuln_detector.py --tier high --safe-mode` |
| 解锁 L4（仅护网内网） | `python scripts/vuln_detector.py --tier critical --no-safe-mode --include-l4` |
| SSL 基线检查 | `python scripts/ssl_analyzer.py --target host:443` |
| JS 泄露挖掘 | `python scripts/js_analyzer.py --target https://host/app.js` |
| 云配置检查 | `python scripts/cloud_security.py --target ...` |
| 生成可视化报告 | `python scripts/report_visualizer.py --findings findings.json` |

> 完整脚本契约见 `references/script_contracts.md`；安全模型见 `references/safety_policy.md`。
