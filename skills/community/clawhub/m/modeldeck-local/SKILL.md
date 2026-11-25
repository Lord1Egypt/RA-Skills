---
name: modeldeck-local
display_name: ModelDeck 本地模型工坊
display_name_en: ModelDeck — Local LLM Deployment Workshop
description: >-
  给要在自有机器或内网跑开源大模型的开发者与小团队：按显存预算定选型与量化档位，完成下载校验、服务部署与 OpenAI 兼容接入，并按吞吐与质量抽检验收。
description_en: >-
  For developers and small teams running open-weight LLMs on their own machines or intranet: size the model and quantization from a VRAM budget, verify downloads, deploy with Ollama or llama.cpp, expose an OpenAI-compatible endpoint, and accept the result on throughput and sampled quality.
version: 1.0.1
category: it-ops-security
sub_categories:
  - key: pro-ai-infra
    name: 本地推理
tags: [本地推理, 显存预算, GGUF 量化, Ollama, llama.cpp]
tags_en: [local inference, VRAM budget, GGUF quantization, Ollama, llama.cpp]
icon: 🧠
platforms: [WorkBuddy, QClaw, ima, Claude Code, Codex]
trigger_keywords: [本地部署大模型, 显存够不够, 量化选哪个, Ollama 部署, llama.cpp 部署, 本地 OpenAI 接口, 模型跑不动, 首 token 延迟, 内网推理服务, GGUF 下载校验]
author: DeepCraft Studio
license: Commercial
pay_skill: true
price_cny: "3.99"
slug: modeldeck-local
displayName: "ModelDeck 本地模型工坊"
summary: "给要在自有机器或内网跑开源大模型的开发者与小团队：按显存预算定选型与量化档位，完成下载校验、服务部署与 OpenAI 兼容接入，并按吞吐与质量抽检验收。"
pricing:
  model: per_call
  amount_fen: 399
---

# ModelDeck 本地模型工坊

把开源大模型在自有机器或内网真正跑起来并接进业务：从显存预算倒推选型与量化档位，经下载校验、推理服务落地、OpenAI 兼容接入，最后用吞吐、首 token 延迟与质量抽检完成上线验收。适配 Windows、Linux 与 Apple Silicon，Ollama 与 llama.cpp 双路径。

## 这是什么

- **解决什么问题**：模型下载完了，却卡在"能不能跑、跑得对不对、敢不敢接业务"这三步。本技能把这三步拆成有判据、有失败分支的动作序列，让部署从反复试错变成一次走完的流程。
- **产出物形态**：一份《部署与验收记录》（Markdown，1200–2500 字），附显存预算表、可直接执行的启动脚本、基准原始数据（JSONL）、回滚步骤。
- **和"直接问通用大模型"的区别**：通用回答给的是科普结论（"用 Q4_K_M 就行"）；本技能要求算到你这台机器的层数、上下文长度、KV cache（键值缓存）精度和验收阈值，每个数字可复算，每个参数可复制执行。

## 适用场景

- "我要在 16 GB 显存的机器上跑一个能接知识库问答的模型，不知道 14B 还是 32B 合适。"
- "GGUF 下好了，llama-server 一加载就 OOM，分不清是层数、上下文还是 KV 精度的问题。"
- "我要把本地模型接进内部工具，上层代码只认 OpenAI 接口，不想改代码。"
- "内网不能出网，下载、校验、升级都得在离线环境下完成。"
- "我需要交出几个数字：每秒吐多少字、首字多久、能不能扛 5 个人同时用。"
- "同一个模型，Ollama 和 llama.cpp 速度差一截，我要知道差在哪、该选哪个。"
- "我要在 Apple Silicon 笔记本上跑，不知道统一内存该怎么算。"
- "上线后偶尔吐乱码或答非所问，需要一套可复现的质量抽检方法。"

## 何时不要使用

- 要做模型训练或微调：本技能只覆盖推理部署与选型。
- 多卡集群、张量并行、K8s 编排：超出单机范围。
- 要求"保证达到某个 tok/s"：只给估算方法与验收口径，实测值随硬件与量化变化。
- 模型许可证不明：先查 LICENSE，许可证不清就不给部署建议。

## 快速参考

| 你的处境 | 直接用 |
|---|---|
| 不知道这张卡能跑多大模型 | `references/hardware-sizing.md` + `scripts/vram_budget.py` |
| 同尺寸模型选哪个 | `references/model-selection.md` |
| 要能直接抄的启动参数 | `references/serving-recipes.md` |
| 想知道真实速度 | `references/benchmarking.md` |

## 输入与输出

| 字段 | 必填 | 说明 |
|---|---|---|
| 宿主环境 | 是 | 操作系统与版本、加速器类型、显存容量、内存容量、目标盘可用空间 |
| 并发与延迟目标 | 是 | 同时在线请求数；可接受的首 token 延迟与每秒输出字数下限 |
| 业务任务类型 | 是 | 问答、抽取、改写、代码、摘要，多选；决定量化档位与上下文预算 |
| 上下文长度需求 | 是 | 单次请求最大输入 token 数，含系统提示与历史对话 |
| 部署形态 | 是 | Ollama（省事）或 llama.cpp（可控）；未指定时按显存宽裕程度给建议 |
| 网络条件 | 否 | 能否直连模型仓库；是否只能走镜像或离线介质 |
| 模型候选 | 否 | 已有候选给出仓库与量化档；未给出时按任务类型与许可给 2–3 个候选 |
| 验收阈值 | 否 | 未给出时，按"首 token ≤ 3 s、单路 ≥ 12 字/秒、4 并发不崩"作为起步基线 |

**输出**：

- `deployment-report.md`：硬件盘点、显存预算、选型结论、启动参数、接口自测、基准数据、回滚方案，1200–2500 字。
- `start-<model>.cmd`（Windows）/ `start-<model>.sh`（Linux、macOS）：可直接执行的启动脚本，环境变量与参数固化其中。
- `bench-<model>.jsonl`：每条请求一行，含 prompt_tokens、completion_tokens、首 token 耗时、总耗时。

## 工作流

### 第 1 步：硬件与需求盘点

**做什么**：采集宿主事实，并把业务诉求写成可度量阈值。

```powershell
# Windows（PowerShell）
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
Get-CimInstance Win32_ComputerSystem | Select-Object TotalPhysicalMemory
Get-PSDrive -PSProvider FileSystem | Select-Object Name, Free
```

```bash
# Linux
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
free -h && nproc && df -h "$MODELDECK_HOME"
# macOS（Apple Silicon）
sysctl -n hw.memsize; sysctl -n hw.ncpu
system_profiler SPHardwareDataType | sed -n '1,12p'
```

**判据**：显存、内存、磁盘三项都有具体数字；并发数与延迟目标写成"4 并发下首 token ≤ 4 s"这种可测形式。

**失败处理**：无独立显卡或显存 < 6 GB → 转 CPU / Metal 路线，模型上限压到 3B–4B 的中高量化档；内存 < 16 GB 又想跑 MoE（混合专家）模型 → 换稠密小模型，不要硬上。

### 第 2 步：显存预算与选型

**做什么**：用两条公式把候选模型算成显存数字，而不是凭"大概能跑"。

```text
权重 GiB  ≈ 参数量（十亿） × 每参比特数 × 0.116
KV GiB    ≈ 2 × 层数 × （KV 头数 × 单头维度） × 每元素字节 × 上下文 token 数 ÷ 1073741824
总预算    = 权重 + KV cache + 计算缓冲（0.3–0.8 GiB） + 系统与驱动预留（0.8–1.5 GiB）
```

跨档对比一次算出，省掉手工试算：

```bash
python scripts/vram_budget.py --params 8 --layers 32 --kv-heads 8 --head-dim 128 \
    --ctx 8192 --vram 16 --kv-dtype q8_0
```

**判据**：预算表至少有两个以上候选，且"总占用 ≤ 可用显存 − 1 GB"的候选不少于一个。

**失败处理**：全部候选超预算 → 按"降上下文 → 降 KV 精度（f16 → q8_0 → q4_0）→ 降量化档 → 降参数量"的顺序退，每退一档重算一次；显存实在不够时才做部分层卸载。

### 第 3 步：获取与校验

**做什么**：优先拿预量化 GGUF，下载必须支持断点续传，落盘后做三重校验（字节数、SHA256、GGUF 头）。

```bash
curl -L -C - --retry 5 --retry-delay 3 -o "$MODELDECK_HOME/models/model-Q4_K_M.gguf" "<MODEL_FILE_URL>"
python scripts/verify_download.py --file "$MODELDECK_HOME/models/model-Q4_K_M.gguf" \
    --sha256 <EXPECTED_SHA256> --size <EXPECTED_BYTES>
```

Ollama 路线把文件放独立暂存目录，再用 Modelfile 导入（`ollama create local-model:q4 -f Modelfile`），不要直接写进 `OLLAMA_MODELS` 的内部 blobs 目录。

```text
FROM <暂存目录绝对路径>/model-Q4_K_M.gguf
PARAMETER num_ctx 8192
PARAMETER temperature 0.7
```

**判据**：三项校验全部通过；导入后 `ollama list` 或 `/api/tags` 能看到模型与体积。

**失败处理**：哈希不符 → 删文件重下，不接受"内容差不多"；GGUF 头不对 → 文件被截断或根本不是 GGUF；导入时报量化校验失败 → 优先怀疑源文件含损坏数据，换官方仓库重下，升级版本解决不了这类问题。

### 第 4 步：推理服务部署

**做什么**：把第 2 步算出的数字翻译成启动参数，并固化成脚本。

```bash
# Ollama：环境变量决定 KV 精度与并发，Modelfile 决定上下文与卸载层数
export OLLAMA_MODELS="$MODELDECK_HOME/models" OLLAMA_HOST="0.0.0.0:11434"
export OLLAMA_KEEP_ALIVE=30m OLLAMA_NUM_PARALLEL=2 OLLAMA_MAX_LOADED_MODELS=1
export OLLAMA_FLASH_ATTENTION=1 OLLAMA_KV_CACHE_TYPE=q8_0
ollama serve
```

```bash
# llama.cpp：层数、上下文、KV 精度、并行槽位一次给全
"$MODELDECK_HOME/bin/llama-server" -m "$MODELDECK_HOME/models/model-Q4_K_M.gguf" \
  --host 0.0.0.0 --port 8080 -c 8192 -ngl 99 -fa on \
  --cache-type-k q8_0 --cache-type-v q8_0 -np 2 --cont-batching --jinja --metrics
```

**判据**：`/v1/models`（llama.cpp）或 `/api/tags`（Ollama）返回目标模型；`nvidia-smi --query-compute-apps=pid,used_memory --format=csv` 能看到服务进程，且显存占用与预算表相差不超过 15%；一次真实生成成功。

**失败处理**：加载阶段 OOM → 按"降上下文 → 降 KV 精度 → 降层数"调，别一次性全改；健康检查通过但 `nvidia-smi` 里没有进程 → 二进制与驱动支持的 CUDA 大版本错配，静默回落到了 CPU 执行，换匹配的构建产物。

### 第 5 步：OpenAI 兼容接入

**做什么**：把本地服务伪装成标准 OpenAI 端点，上层代码零改动接入。

```bash
# 自测第一层：裸 HTTP
curl -s http://127.0.0.1:8080/v1/chat/completions -H "Content-Type: application/json" \
  -d '{"model":"local-model","messages":[{"role":"user","content":"回复 OK"}],"max_tokens":16}'
```

```python
# 自测第二层：官方 SDK，流式与非流式各跑一次
from openai import OpenAI
client = OpenAI(base_url="http://127.0.0.1:8080/v1", api_key="local-placeholder")
r = client.chat.completions.create(model="local-model", max_tokens=16,
                                   messages=[{"role": "user", "content": "回复 OK"}])
print(r.choices[0].message.content, r.usage)   # 流式把 stream=True 再跑一遍
```

**判据**：流式与非流式各成功一次；返回体带 `usage` 里的 prompt 与 completion token 数；中文不出现乱码或中途截断。

**失败处理**：404 → `base_url` 少写 `/v1`；`model not found` → 名字与 tag 不一致，用服务端实际暴露的名字；流式一直不结束 → 中间层做了缓冲或没按分块传输；客户端报缺 API key → 用非空占位串，本地服务不校验内容但客户端库要求。

### 第 6 步：基准测试与质量抽检

**做什么**：固定题集、固定输出上限、固定温度，先预热一次，再取三次中位数。

- **性能指标**：首 token 延迟、解码速度（每秒输出 token 数）、端到端时延、4 并发下的退化比例、峰值显存。llama.cpp 直接用 `/metrics` 的累计计数自算，比客户端掐表更稳。
- **质量抽检**：20–30 题，按 0/1/2 打分，其中至少 3 条为"不可失败项"（结构化输出可解析、数字抽取正确、越界请求能拒答）。

**判据**：五个性能字段与质量总分全部落表；4 并发总吞吐不低于单路的 1.8 倍，且无 OOM、无超时；每个数字都标注"示例环境，需实测"。

**失败处理**：质量不达标 → 先升量化档，再考虑换更大参数，最后才动提示词，顺序反了会掩盖真实瓶颈；并发退化严重 → 减少并行槽位或缩短上下文，而不是加机器。

### 第 7 步：生产化收尾

**做什么**：把一次性跑通变成可运维。

- **并发**：`OLLAMA_NUM_PARALLEL` 或 `-np` 的值与显存预算联动，每加一个槽位就多一份 KV，必须重算第 2 步。
- **KV cache**：上下文顶到上限时优先降 KV 精度，其次降上下文；`--no-kv-offload` 可把 KV 放回内存换显存。
- **日志**：服务端日志按大小轮转，请求日志只记 token 数与耗时，不落完整提示词。
- **回滚**：保留上一个可用模型 tag 与启动脚本副本，回滚必须在一条命令内完成。

**判据**：服务异常后能用一条命令拉起；旧版本仍可启动；日志有轮转策略；回滚步骤写在报告里且被实际演练过一次。

**失败处理**：反复崩溃且日志无线索 → 先确认是不是残留进程占着显存（`nvidia-smi` 里出现两个服务进程），再查系统提交内存是否耗尽。

## 输出格式

```
硬件盘点：GPU / 显存 / 内存 / 磁盘 / 系统
显存预算表：权重 | KV cache | 运行时开销 | 余量
推荐组合：模型 + 量化 + 上下文长度 + 并发
启动命令：可直接复制的 ollama / llama.cpp 参数
验收指标：首 token 延迟、tok/s、显存峰值
```

## 质量门槛

- [ ] 显存预算表可复算：给出参数量、量化档、层数、KV 头维度与上下文，任何人代入能算出同样的权重与 KV 数字。
- [ ] 启动脚本单条命令可用，不依赖交互输入，路径不散落在脚本之外。
- [ ] 三重校验齐全：字节数、SHA256、GGUF 头均有记录，且与下载源公布值一致。
- [ ] 接口自测两种都过：非流式与流式各一次，返回体含 `usage` 字段。
- [ ] 基准表五个字段都有数：首 token 延迟、解码速度、端到端时延、并发退化、峰值显存，且每个数字都标注"示例环境，需实测"。
- [ ] 质量抽检不少于 20 题，含至少 3 条不可失败项，每题给出判定理由。
- [ ] 失败路径有记录：至少写出一条真实报错、定位过程与最终处置。
- [ ] 回滚可在 5 分钟内完成，命令写进报告。
- [ ] 零敏感信息：报告与脚本中不含密钥、内网地址、真实姓名与个人目录路径。

## 能力边界

- 不做模型训练、微调与蒸馏；不评估未公开权重的模型。
- 不承诺具体速度：所有 tok/s 与延迟数字均为本机实测值或明确标注的估算，跨机器不可直接套用。
- 不做多机分布式推理与 GPU 集群编排；多卡场景只覆盖张量切分的基础参数。
- 不做模型许可的法律判断：能否商用以模型仓库内 LICENSE 文件与实际授权为准。
- 显存、内存带宽、驱动三者任一不满足时，直接给"不可行"结论，不出勉强上线方案。
- 不替代业务侧质量评估：本技能给抽检方法与阈值，业务正确性仍需领域人员确认。

## 常见陷阱

- **只看参数量不看量化**：7B-Q4 与 7B-FP16 显存差一倍多 → 参数量与量化同时报。
- **忽略 KV cache**：长上下文时 KV cache 可能超过权重 → 按 32k 上下文单独算一份预算。
- **拿厂商标称 tok/s 当实测**：硬件与量化不同差数倍 → 必须在目标机器上跑一次基准。
- **忘记并发**：单请求能跑，两个并发就 OOM → 预算里留并发余量。

## 交付示例

**输入**：

```text
宿主：Linux，24 GB 显存独显，64 GB 内存，数据盘余 200 GB
任务：内部知识库问答，单次输入最长约 6000 token，4 人同时用
诉求：不改上层代码，走 OpenAI 接口
```

**输出骨架**（`deployment-report.md`）：

```markdown
# 本地推理部署与验收记录
## 1 硬件与需求
Linux / 24 GB 显存 / 64 GB 内存 / 余 200 GB；目标：4 并发、首 token ≤ 3 s、单路 ≥ 12 字/秒。
## 2 显存预算
| 候选 | 量化 | 权重 | KV@8K | 缓冲+预留 | 合计 | 结论 |
|---|---|---|---|---|---|---|
| 14B 级 | Q4_K_M | 7.9 GiB | 1.5 GiB | 1.6 GiB | 11.0 GiB | 宽裕，可上 16K |
| 32B 级 | Q4_K_M | 18.1 GiB | 2.0 GiB | 1.6 GiB | 21.7 GiB | 临界，限 8K |
## 3 选型与参数
14B 级 Q4_K_M + 16K；-ngl 99 -c 16384 -fa on --cache-type-k q8_0 -np 2（脚本见 start-llm.sh）。
## 4 接口自测
非流式 ✓ / 流式 ✓ / usage 字段 ✓ / 中文无乱码 ✓
## 5 基准（示例环境，需实测）
首 token 0.6 s（4 并发 1.9 s）；解码 31 tok/s（4 并发合计 78）；峰值显存 12.1 / 18.4 GB。
## 6 质量抽检
22 题，39/44；不可失败项 3/3。
## 7 回滚
切回上一 tag 并重启服务，约 40 s。
```

## 相关技能

- **ChartAtelier（付费）**：把显存预算与基准结果做成图。
- **SkillForge（付费）**：把你的部署经验固化成可复用技能。

## 参考文件

- `references/hardware-sizing.md`：三平台硬件盘点命令、显存与上下文预算算法、统一内存与提交内存的坑。
- `references/model-selection.md`：参数量 × 量化档 × 上下文的取舍、稠密与 MoE 的差别、许可与对话模板核查。
- `references/serving-recipes.md`：Ollama 与 llama.cpp 的参数模板、systemd 与 Windows 服务化写法、排障对照表。
- `references/benchmarking.md`：基准方法论、指标定义、并发测试步骤、质量抽检评分表。
- `scripts/vram_budget.py`：纯标准库显存预算计算器，按量化档与上下文档位批量出表。
- `scripts/verify_download.py`：纯标准库下载校验器，核对字节数、SHA256 与 GGUF 头。
