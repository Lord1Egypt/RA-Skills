---
name: model-intel-check
description: 黑盒检测某个 API 端点背后的模型是否"满血/智力正常"（中转站缩水鉴定）。当用户想验证某中转/代理/上游模型是否被换成弱模型、量化版或被剥离 thinking 时使用；也用于对比两个端点的同一模型。触发词如：满血、缩水、智力测试、鉴定模型、benchmark 这个端点。
---

# 模型满血度黑盒检测

原理：被测模型只是远端 API 端点，只接收题目文本，全程无工具、无联网；用公开高难题库
（AIME 2025 + GPQA Diamond）按固定协议跑分，与该模型的官方公布分对照判定。

## 资产（本 skill 目录下）

- `intel_check.py` — 主跑脚本（OpenAI 兼容端点通用，`--model` 任意模型）
- `rerun_failed.py` — 补跑传输失败题（并发 2，协议完全一致）
- `make_data.py` — 下载/构建题库到 `data/`（GPQA 需 HF_TOKEN，见 `data/README.md`）
- `references/README.md` — 主流模型官方参考分锚点表（含来源链接与复核方法），
  判分前先查它，再按里面的链接联网复核最新值
- `references/benchmarks.md` — 题库目录：各知名题库去哪下、格式兼容性、
  按模型档位选套件的矩阵（不囤题，用时再拉）
- `references/anti-cheat.md` — 防作弊（流程纪律）与作弊检测（识别端点欺诈）标准，
  每次跑分逐项打勾
- `serve.py` + `web/index.html` — 本地 Web UI（页面固定，所有人看到的是同一个页面）：
  题库展示、开始按钮、实时进度、成绩判定。跑分协议与 CLI 完全一致

## 硬性规则（违反则结果无效）

1. **被测模型只做 API 应答，绝不做编排**。跑脚本的是主 agent 或用户的 shell。
   如果被测模型就是当前驱动本 CLI 的模型，直接 Bash 后台跑脚本，
   **不要派同模型的子 agent 去跑**（自己考自己=利益冲突，它能看到本地答案文件）。
2. 不给被测模型任何工具/搜索；脚本请求体只有一条 user 消息（已实现，不要改）。
3. 不要告诉被测模型题库名称（prompt 里不得出现 "GPQA/AIME" 字样——脚本已实现）。
4. 不改计分协议：prompt 模板、temperature=1.0、top_p=0.95、max_tokens=98304、
   thinking keep=all effort=high、GPQA 洗牌种子 `42+题号`。改任何一项分数都不可比。
   例外：被测模型不支持 thinking 参数时加 `--no-thinking`，并在报告中声明。
5. 在**干净目录**跑：新建工作目录，只放脚本+data/，不放任何历史结果。
   （虽然远端模型摸不到本地文件，但干净目录能防止编排侧无意间把旧答案带进流程。）

## 流程

### 1. 确定被测端点

从用户的 `~/.kimi-code/config.toml` 的 `[providers.*]` 取 `base_url`/`api_key`，
或让用户直接给。模型名 = 端点上的 model id（不是别名）。
先拉一次 `GET {base_url}/models` 或发一条 1-token 请求确认连通，
并记录响应里的 `model` 回声——**中转可能 round-robin 多个上游，回声字段能暴露当前上游**
（例如 `accounts/fireworks/models/...` vs `moonshotai/...`），报告里必须写明。

### 2. 查官方参考分（联网，主 agent 做）

先查本 skill 的 `references/README.md` 锚点表——主流模型的官方分已按模型整理好
并附来源链接。**再以表里的链接为起点联网复核最新值**（官方分会随版本更新），
搜该模型的官方技术报告/模型卡/官方 vendor-verifier 表，记录 GPQA Diamond 和
AIME 2025 的公布值及其评测口径（avg@k/pass@k、温度、max_tokens）。
注意口径差异：公布值常是 avg@32 之类，我们跑的是 temp=1.0 单 epoch，
**判定用区间不用点值**。查不到官方值时，用同系列官方模型分数做参照并声明局限。

### 3. 选套件 + 准备环境与题库

按被测模型的档位，从 `references/benchmarks.md` 的矩阵选套件（原则：选官方分落在
40–85% 区间的题，全对全错都没有鉴别力）：

- 旗舰 thinking 模型：默认 **AIME 2026 全 30 + GPQA 50**（新题污染风险最低）
- 要与本 skill 既有参考线（K3 等）直接对照时，用默认 AIME 2025 口径
- 中端/非 thinking 模型按矩阵降档；防背题加强轮换 MathArena 当季赛题

```bash
mkdir ~/Desktop/intel-check-<日期> && cd ~/Desktop/intel-check-<日期>
cp <skill目录>/intel_check.py <skill目录>/rerun_failed.py <skill目录>/make_data.py .
python -m venv .venv && ./.venv/Scripts/python -m pip install openai
# pip 装不上时再试镜像: -i https://pypi.tuna.tsinghua.edu.cn/simple
./.venv/Scripts/python make_data.py        # AIME 2025+2026 自动; GPQA 需 HF_TOKEN
# 若 skill 目录已存有 data/ 题库，可直接 cp -r <skill目录>/data . 跳过下载
```

GPQA 拿不到就只跑 AIME：`--suite aime --aime-indices 0-29`（30 题全量）。
跑 AIME 2026 用 `--aime-file aime2026.jsonl`。

### 4. 跑分（后台）

```bash
export KIMI_BASE_URL="<被测端点>" KIMI_API_KEY="<key>"
./.venv/Scripts/python intel_check.py 2>&1 | tee results_run.log
```

- 用 Bash 后台任务跑，**输出重定向到文件**（不要 pipe 给 tail，否则中途看不到进度）。
- 默认 65 题并发 8，约 15–45 分钟。中转报 429 "Too many concurrent requests" 时
  降到 `--concurrency 2` 重跑。

### 4b. 或者用 Web UI（体验更好，协议完全一致）

先与用户对话确定测评配置，写成 `run_config.json`（**页面只读展示，不可更改**）：

```json
{
  "model": "kimi-k3",
  "concurrency": 8,
  "no_thinking": false,
  "suites": [
    {"kind": "aime", "name": "AIME 2026", "emoji": "🐉", "file": "aime2026.jsonl",
     "indices": "0-29", "count": 30, "stars": 5, "ref_pct": 80.0},
    {"kind": "gpqa", "name": "GPQA Diamond", "emoji": "🧪", "count": 50,
     "stars": 4, "ref_pct": 85.7}
  ]
}
```

（base_url / api_key 永远走环境变量，不写进配置文件、不上页面。）

然后启动本地服务（跑分在服务器后台线程执行，**agent 不需要在场**，页面每 1.5 秒
轮询自动刷新——实时进度是正常工作的）：

```bash
export KIMI_BASE_URL="<被测端点>" KIMI_API_KEY="<key>"
python <skill目录>/serve.py --config run_config.json    # 打开 http://127.0.0.1:8899
```

- 依赖：运行 `serve.py` 的 Python 要有 `openai` 包（`python -m pip install --user openai`
  一次即可；镜像源装不上就换默认 PyPI）。结果落盘到启动时所在目录的 `results/`。
- 页面内置多套皮肤：`?skin=clinic`（默认，卡通体检）/ `mission` / `lab` / `quest`。
- 补跑、人工抽查、anti-cheat 核查等后续步骤与 CLI 模式相同。
页面可填官方参考分自动判档；判完仍须按 `references/anti-cheat.md` 走 A/B/C 核查。

### 5. 传输失败处理（关键：运输层失败 ≠ 模型不会）

跑完先看 `finish_reason` 分布。`error`（429/5xx/封锁）或 `null`（断流，completion
截在半句话）的题**不能算错题**：

```bash
./.venv/Scripts/python rerun_failed.py results/results_<ts>.jsonl
```

然后把主跑与补跑按题号合并（error/null 行用补跑结果替换）再算总分。
出现 "Your request was blocked" 是中转 WAF 按 UA 封禁：本 skill 脚本已内置
`User-Agent: curl/8.0.1` 绕过；若仍被封，降并发、隔几分钟再试。

### 6. 真实性核查（防回放、防背题）

**完整标准在 `references/anti-cheat.md`**：流程侧纪律 A1–A5、检测侧检查 B1–B7、
组合判定规则 C，逐项打勾后写进报告。快速清单：

- **防缓存回放**：若同端点跑过多轮，把两轮 completion 逐题比对，雷同数应≈0
  （temp=1.0 真采样措辞必然不同；错误信息字符串雷同不算）。
- **人工抽查 MISS**：读 `answers_*_<ts>.txt` 里每道 MISS 的 completion 结尾。
  答案其实对但正则没抓到 → 以人工为准修正；推导链完整但结论错 → 真错。
- **错误分布自然性**：真实能力的形态是"易题全对、最难题失手、错因是自洽的推理失误"。
  异常高分（远超官方）反而提示训练污染或答案泄漏。
- 思考量 sanity：有 usage 时看 reasoning_tokens（GPQA 难题应有数千~上万）。

### 7. 判定（参考带，按题量给噪声容差）

以官方参考值 R 为锚：
- **满血/同档**：得分 ≥ R − 噪声带（GPQA 50 题带 ±5pp；AIME 15 题带 ±2 题）
- **存疑**：低于满血线但高于腰斩线（如 GPQA 70–78% 或 AIME 少 3–4 题）→ 复跑确认
- **大概率缩水**：GPQA < 70% 或 AIME ≤ 8/15 级别

参考实例（Kimi K3 thinking，官方约 GPQA 85.7 / AIME 80+）：
满血线 = GPQA ≥ 40/50 且 AIME ≥ 12/15；GPQA < 35/50 或 AIME ≤ 8/15 = 大概率非满血。

## 汇报模板

```
| 端点(上游回声) | AIME | GPQA | 判定 |
跑分时间/协议/并发；传输失败与补跑说明；最终错题清单（真错 or 格式）；
与官方参考值对照；结论（满血/存疑/缩水）+ 局限（单 epoch 噪声、公开题污染可能、
中转 round-robin 时结论代表该中转整体）。
```
