---
name: "poly-mal-scan"
description: "FWold 多语言(PHP/JS/Bash)恶意代码/webshell 扫描检测器: 用法、MCP 接入、规则库持续更新、运行依赖。扫描文件/代码、挂载/测试 detect_mcp_server MCP、新增调准特征码规则、排查误报漏报时启用。"
---

# Poly-Mal-Scan — FWold 多语言恶意代码扫描（技能参考）

> 本文档是 FWold 工具使用的**通用事实基准**（single source of truth，位置无关）：
> 项目是什么、检测器怎么跑（CLI / MCP）、规则库怎么持续更新、运行依赖是什么。
> 本文件不假设仓库所在的具体机器/路径；统一用仓库根 `$ROOT` 指代"含
> `php_security/`、`js_security/`、`bash_security/`、`detect_mcp_server.py` 的那层目录"。
> 开工先定位 `$ROOT`（找不到就问用户放哪，不要猜）；涉及具体语言规则来源再跳对应目录的 `特征码来源.md`。

---

## 1. 项目简介

**FWold = 多语言恶意代码扫描检测器集群**，用于在 **PHP / JavaScript(Node) / Bash** 源码里定位免杀 webshell、反弹 shell、命令注入、文件写入后门、混淆 payload 等恶意行为。

每个语言一套**三层检测器**、彼此对称：

| 语言 | 目录 | 主调度器 | 核心威胁类别（JSON 键） |
|---|---|---|---|
| PHP | `php_security/` | `phpdect.py` | 恶意函数执行 / 威胁性动态变量 / 特征码威胁 / 自我复制·文件写入 |
| JS | `js_security/` | `jsdect.py` | 恶意函数/API执行 / 动态代码执行 / 特征码威胁 / 自我复制·文件写入 |
| Bash | `bash_security/` | `bashdect.py` | 恶意命令 / 恶意变量 / 恶意文件写入 / 自我复制 / 恶意函数 / 特征码威胁 |

**三层检测逻辑**（每套一致）：
1. **AST 归一化层** —— 用 tree-sitter 把源码翻译成"暴露更多行为、正则可命中"的等效文本（常量折叠、变量解析、动态函数名、字符串拼接折叠、命令替换摊平、转义/编码还原），并保留**原文行号 + 字节偏移**定位。
2. **规则库层** —— 从 JSON 加载规则（威胁函数、多编码特征码 `MULTI_ENC_TRAITS`）。内置 **8 种编码器**：`plain / base64 / url / hex / octal / chr / rot13 / html`，把原料词条 × 编码推导成易识别的混淆指纹。
3. **正则研判层** —— 逐行扫 + 历史窗口伪污点溯源 + 逻辑规则引擎（and/or/not，模仿 yara）。命中后用归一化层的 loc 反查回**原文精确位置**。

**多语言路由网关**：根目录 `detect_mcp_server.py` 用智能语言识别，自动决定对一段文件/代码调用 php/js/bash 中哪些检测器，支持**无代码不调用 + 多语言同时调用**。

顶层目录另带测试集（`php_security/文本测试数据/` 30 个、`js_security/testdata/` 40 个、`bash_security/testdata/` 60 个，数量以实际为准），供回归与规则校验收口。

---

## 2. 运行方式（CLI，位置无关）

主调度器支持命令行直接扫文件，输出统一 JSON：

```bash
PY=python3        # 指向装好依赖的 Python 解释器名/路径; 只有一个解释器就用它

cd "$ROOT/php_security"
$PY phpdect.py 待扫描文件.php        # 输出 JSON(默认 phpdest.php)

cd "$ROOT/js_security"
$PY jsdect.py 文件.js

cd "$ROOT/bash_security"
$PY bashdect.py 文件.sh
```

**程序化调用（推荐）**：把对应目录加入 `sys.path` 后 import，单文件返回完整 dict：

```python
import sys; sys.path.insert(0, "$ROOT/php_security")
from phpdect import phpfile_threatening_dect   # 单文件
d = phpfile_threatening_dect('a.php')
# d['是否有威胁']  bool;  d['威胁']  分类 {类别: [条目]}
#   条目含: 函数名/参数/威胁级别/原文内容/行数/原文定位(如有)

from phpdect import scan_to_json               # 多文件 + 递归静态 include
res = scan_to_json('入口.php', recursive=True) # 返回 list[dict]
```

入口函数名对齐（位置无关）：`scan_to_json` 三套均有；单文件为 `phpfile_threatening_dect` / `jsfile_threatening_dect` / `bashfile_threatening_dect`。

Bash 侧自带规则覆盖回归：`cd "$ROOT/bash_security" && $PY run_tests.py`（退出码：0 全检出且规则全覆盖 / 1 有漏报样本 / 2 无漏报但某规则 ID 未被测试覆盖）。

---

## 3. MCP 服务用法（detect_mcp_server.py）

**是什么**：独立单文件、可跨机器分发。与三语言目录平级放在仓库 `$ROOT`。用 stdio + 行分隔 JSON-RPC 2.0；`python detect_mcp_server.py` 启动后即可接入支持 MCP 的客户端。

**提供 3 个工具**：

| 工具 | 作用 |
|---|---|
| `detect_languages(file_path\|content, filename?)` | 只识别语言，返回判定依据 + 应调用哪些检测工具；**不真正扫描** |
| `scan(file_path\|content, filename?)` | 识别语言 → 调用对应检测器(php/js/bash) → 合并"是否有威胁"+各语言结果 |
| `list_detectors()` | 列出可调用的检测器（目录/模块/入口） |

**参数规则**：`file_path` 与 `content` 二选一。`content` 传片段时可用 `filename` 辅助识别扩展名；无输入或纯文本会判 `no_code=True`，**不调用任何检测器**；`no_code=False` 才扫。

**语言识别信号**：扩展名、shebang、内容特征（`<?php`、JS `function/const/require/document.`、Bash `/dev/tcp`·`nc -e`·`export/source` 等）。`.html/.vue/.tpl` 走内容内嵌识别——内嵌几段代码就同时调几个检测器（如 php+js）。

**CLI 自测（非 MCP 模式）**：
```bash
cd "$ROOT" && python3 detect_mcp_server.py --detect 某文件   # 语言识别
cd "$ROOT" && python3 detect_mcp_server.py --scan   某文件   # 识别+扫描
```

**返回结构（scan）**：
```json
{
  "文件": "...", "检测到的语言": [...],
  "判定依据": {...}, "使用检测工具": ["php", ...],
  "无对应工具的代码语言": [...], "no_code": false,
  "是否有威胁": true,
  "结果": { "php": [检测器完整单文件扫描 dict], "js": [...] }
}
```

**说明**：`scan` 用 `content` 时会写临时文件、用后自清；`_load_detector` 懒加载对应语言模块并缓存。要让某语言检测器出 AST 层结果，需要该语言能在解释器里 import tree-sitter（见第 5 节）。已按标准 MCP stdio 客户端实测 19/19 项握手/列表/调用/无代码/多语言/报错断言通过——换机器同样可用（别名检测 `--detect`/`--scan`）。

---

## 4. 规则库：结构 + 持续更新（重要）

### 铁律
> **规则数据与代码解耦。** 威胁函数、词条、直接特征码、命令/变量/写入/自复制规则全部外置 JSON；加规则只改 JSON，**不改 Python 检测逻辑**。改词条下次 import 即生效（多编码特征码在导入期由"词条 × 8 编码器"自动推导）。

各语言规则数据文件：

- **PHP**：`threatening_funcs.json`（函数名+级别）、`categories.json`（词条 + 可带 `逻辑规则` 键做 and/or/not 组合）、`raw_traits.json`（"看到即判死"直接指纹，写各编码最终形态）。
- **JS**：`js_threatening_funcs.json` / `js_categories.json`（+`逻辑规则`）/ `js_raw_traits.json`。
- **Bash**：`bash_threatening_funcs.json`/`bash_categories.json`/`bash_raw_traits.json`，另按类别拆 `bash_malicious_commands.json`、`bash_malicious_variables.json`、`bash_file_write.json`、`bash_self_replicate.json`。

加载器（`detect_rules.py`/`js_detect_rules.py`/`bash_detect_rules.py`）以**自身文件所在目录为基准**定位 JSON（`_RULES_DIR`），从任意目录 import 都不丢文件；产 `MULTI_ENC_TRAITS`（词条推导 ∪ RAW、去重、按 `MIN_TRAIT_LEN=4` 过滤短码防二进制误报）与各结构化规则列表/索引。

### 提取规约（三种语言通用）
- 只收**"看到即可判死"的高确定性指纹**（典型/高危优先）；剔易碰撞短串（<4 字节、纯常见英文词）。
- `plain` 明文只收**完整恶意片段**（如 `eval($_POST['p1']`、`nc -e /bin/bash`、`>> ~/.ssh/authorized_keys`），不收 `eval`/`curl`/`system` 这类被 threat_func 覆盖且易误报的裸词。
- 编码特征码写"该编码最终形态"（base64 去 `=`；url/hex/octal/chr/rot13/html）。
- 类别键与对应 `MULTI_ENC_TRAITS` / 规则结构类别一致（别自造拼不上的键）。

### 🔁 持续更新：新规则从哪来
> 使用中**要随时更新规则库**。新来源除各 `特征码来源.md` 已登记的**也可自己找**。加完在对应 `特征码来源.md` 补记"来源/许可/如何提取/已采用对照"，保持可追溯。

**各目录已登记来源（`特征码来源.md`），可复用于抓新指纹：**
- **PHP**：`tennc/webshell`(GitHub, MIT) 的 `php/` 样本（一句话/大马/WAF bypass）。来源2 占位。
- **JS**：`tennc/webshell` 的 `nodejs/` 反弹 shell；testdata / DOM XSS 注入指纹。来源3 占位。
- **Bash**：**MITRE ATT&CK 企业矩阵** (attack.mitre.org, CC-BY-4.0) —— 每条结构化规则威胁类型/级别/参考(T1548/T1572/T1059) 对齐它；公开反弹 shell/提权/混淆武器库；本项目 testdata 反向校验。来源4 占位。

**可自行拓展的来源示例（尊重许可+注明出处）**：GitHub webshell 聚合仓库、安全厂商公开 YARA/规则集、NVD/Exploit-DB、AV 样本库、社区 C2/加载器样本等。**务必**：优先自由/开源许可、别塞低置信短串、加后用 testdata + run_tests 回归不引误报。

### 新增规则流程（端到端）
1. 找恶意样本/可信来源，提炼高确定性指纹。
2. 写对 JSON（位置无关、都在对应语言目录）：函数名→`threatening_funcs.json`；词条→`categories.json`；完整明文/编码指纹→`raw_traits.json` 对应类别（写最终形态）；Bash 结构化命令/变量/写入/自复制→对应 `bash_*_*.json`。
3. （重）import 对应 `detect_rules`（触发 MULTI_ENC_TRAITS 重推导）。
4. 恶意样本应检出、正常/边界样本不误报，各测一遍。
5. 跑该语言 testdata 全量；Bash 用 `run_tests.py`，确认无回归。
6. 在对应 `特征码来源.md` 更新对照表。

---

## 5. 运行依赖 / 使用的库

> **只列通用要求；具体到某台机器的解释器用哪个，以实际环境为准，不要套用别的机器的路径。** 找一个能 import 下列建议库的 Python 即可获得完整能力。

| 项 | 版本建议 | 用途 | 是否必需 |
|---|---|---|---|
| Python（stdlib `sys/os/re/json`） | ≥3.10 | 运行 | 必需（无它则纯正则模式，已能跑基本检测） |
| `tree_sitter` | ≥0.26 | 语法树解析底层 | 建议（AST 归一化层依赖） |
| `tree_sitter_language_pack` | ≥1.15 | 提供 php/javascript/bash 各语言 parser（`get_parser('php'|'javascript'|'bash')`） | 建议（AST 层依赖） |

说明：
- **MCP 服务 `detect_mcp_server.py` 零第三方依赖**（只用 stdlib+json），任意 Python 可起；但它调某语言检测器想要 AST 仍需 tree-sitter。
- 目标机器缺失 tree-sitter：各检测器守卫式降级（`_AST_AVAILABLE=False` 静默回退纯正则），**不崩**，但动态函数名/拼接混淆/污点摊平这类靠 AST 揭穿的威胁会漏——若要完整请装上。
- 安装：`pip install "tree_sitter>=0.26" "tree_sitter_language_pack>=1.15"`。
- 运行前先在本机 `import tree_sitter`、`import tree_sitter_language_pack` 探一下，别再照搬别的机器的版本/路径。

---

## 6. 触发提示 / 何时启用（技能侧）
以下任一情形应启用本技能并先定位 `$ROOT`，必要时读本文件：
- 用户提到 **FWold / php_security / js_security / bash_security / phpdect / jsdect / bashdect / detect_mcp_server**，或要扫 PHP/JS/Bash 里的 webshell/后门/恶意命令；
- 需要**测试或挂载上述 MCP**、识别某文件/代码用了哪些语言并决定调用哪套检测器；
- 需要**给检测器新增/调准规则、修误报/漏报、跑全量回归**；
- 对话中出现上述目录相关崩溃/差异，需对照本项目排查。

默认动作：先确认仓库根与当前可用 Python（能 import 建议库的那个）；改规则遵循第 4 节"JSON is the only source of truth"并回归。
