---
name: llama-params-optimizer
version: 3.1.0
description: >
  Complete methodology for local LLM performance optimization.
  Core principle: maximize context while fully covering GPU memory — find the sweet spot where GPU runs at full speed.
  Step-by-step 4-phase 10-step control variable testing process.
  Works for ALL llama.cpp / llama-server models on ANY hardware.
  Cases: Qwen3.5-MoE, Qwen3.6-35B, Qwen3.6-27B (2026-04-28).
author: fenglai
keywords: [llama.cpp, performance optimization, local llm, llama-server, quantization, long context, control variable testing, speed optimization, reasoning models, OpenClaw config]
tags: [llm, performance, optimization, local-first, chinese-support]
---

# llama.cpp 启动参数优化技能 / llama.cpp Parameter Optimization Guide

**中文** | **English**  
标准化的 LLM 本地部署启动参数优化评估流程，通过严格的控制变量测试，找到最佳的性能/质量平衡点。  
_A standardized methodology for optimizing local LLM deployment parameters, using rigorous control variable testing to find the optimal performance/quality balance._

**⚠️ 安全声明 / Safety Notice**
- 本技能仅用于 **本地部署** 参数优化，所有测试应在隔离环境中进行。
- **llama-server 和 llama.cpp 二进制文件**应仅从官方 GitHub 仓库 (https://github.com/ggerganov/llama.cpp) 获取，避免使用第三方来源。
- **网络绑定安全**：本地开发/测试时建议绑定 `127.0.0.1`（localhost），生产环境必须通过反向代理 + HTTPS 暴露服务。
- 参数调优可能触发 OOM 崩溃，**不确定最优参数时，建议使用云端模型（如 OpenAI/Gemini）进行推理验证**，本地只用于性能调优。
- **不要在生产环境中使用本技能提供的示例命令直接暴露服务**，需根据实际安全需求调整。

## 🎯 核心卖点 / Key Features
- ✅ **GPU 内存覆盖原则** / _GPU Memory Coverage Principle_：在完全使用专用 GPU 内存的前提下，找到最大上下文值 | _Find max context while fully covering GPU memory_
- ✅ **四阶段十步法控制变量测试** / _4-phase 10-step process_：完整的性能/质量评估 | _Comprehensive performance and quality evaluation_
- ✅ **大量反常识踩坑经验** / _Battle-tested counterintuitive findings_：避免踩同样的坑 | _Avoid common pitfalls_
- ✅ **通用方法论** / _Universal methodology_：提供系统化测试框架，具体参数需结合实际硬件验证 | _Provides a systematic testing framework; specific parameters must be validated against actual hardware._
- ✅ **实战验证** / _Real-world proven_：35B+4060Ti 案例：~30 → ~90 token/s，提升 2-3 倍；27B 案例：~23.6 tok/s，验证理论公式不可靠 | _Multiple cases: MoE 262% boost, Dense 2-3x, 27B theoretical formula fails_

## 适用场景 / When to Use

**中文** | **English**  
新模型首次部署，需要找到最佳启动参数  
_First-time deployment of a new model, finding optimal launch parameters_  
新硬件环境下的性能调优  
_Performance tuning on new hardware_  
llama.cpp / llama-server 启动参数优化  
_llama.cpp / llama-server launch parameter optimization_  
验证量化损失、长上下文能力等核心特性  
_Verify quantization loss, long context capabilities, and other core features_

---

## 完整评估流程 / Complete Methodology
_**4 phases, 10 steps**_

---

### 📊 第一阶段：基准建立 / Phase 1: Establish Baseline

#### 步骤 1：建立初始基准 / Step 1: Run at default parameters
**中文** | **English**  
在默认参数下运行，记录基础性能数据：  
_Run with default parameters and record baseline performance:_  
```
✅ 记录项 / Metrics to record：
- 生成速度 / Generation speed (tokens/s)
- Prompt 处理速度 / Prompt processing speed (tokens/s)
- 显存占用峰值 / Peak VRAM usage (GB)
- 首字延迟 / Time to first token (ms)
```

#### 步骤 2：枚举所有待测试参数 / Step 2: List all parameters to test
**中文** | **English**  
列出所有可能影响性能的参数：  
_List all parameters that may affect performance:_  
| 参数 / Parameter | 典型测试值 / Typical values |
|------|-----------|
| `--threads` | 4 / 8 / 12 / 16 / CPU 核心数 |
| `-b / --batch-size` | 512 / 1024 / 2048 / 4096 |
| `--ctx-size` | **重要！优先测试！先找甜点阈值，再测其他参数** |
| `--flash-attn` | on / off |
| `--cache-type-k/v` | 不量化 / q8_0 / q4_0 |
| `--parallel` | 1 / 2 / 4 |
| `--ubatch-size` | 256 / 512 / 1024 |

---

### ⚡ 第二阶段：控制变量性能测试 / Phase 2: Control Variable Testing

#### 步骤 3：逐个参数控制变量测试 / Step 3: Test one parameter at a time
**中文** | **English**  
**核心原则：每次只改一个参数，其他所有参数保持基准不变！**  
_**Core principle: Change only ONE parameter each time, keep ALL others at baseline!**_  

❌ 错误做法 / Wrong way：链式修改，改完线程改上下文，再改 FA，结果混在一起无法归因  
_Chain modification - change threads, then context, then FA - results can't be attributed_  
✅ 正确做法 / Correct way：每次测试都回到基准配置，只改一个参数  
_Return to baseline config for each test, change only one parameter_  

#### 步骤 4：建立性能对比矩阵 / Step 4: Build comparison matrix

**⚠️ 重要反常识发现 / Critical Counterintuitive Findings**
- ❌ `--parallel 2` 不一定好 / Not always good：在 4060Ti + 35B 组合上，单请求速度反而下降 40%，调度开销超过了并发收益  
  _On 4060Ti + 35B Dense, parallel=2 slows single request by 40% - scheduling overhead exceeds concurrency benefit_  
- ✅ `--flash-attn on` 对长 Prompt 影响巨大 / Huge impact on long prompts：开启前 300-500 token/s，开启后 1858 token/s，快了 3-5 倍  
  _300-500 → 1858 token/s, 3-5x faster, but only ±5% effect on regular generation_  
- ❌ KV 缓存激进量化不一定好 / Aggressive KV quantization not always good：q4_K 在某些版本的 llama.cpp 上会导致模型加载速度极慢，优先用 q8_0  
  _q4_K can cause extremely slow loading on some llama.cpp versions - prefer q8_0_  

**中文** | **English**  
每个参数测试完成后，记录完整的对比表：  
_After each parameter test, record complete comparison table:_  

**示例：线程数对比 / Example: Thread count comparison**
| 线程数 / Threads | 生成速度 / Gen Speed | Prompt 速度 / Prompt Speed | 变化 / Change | 推荐 / Recommend |
|------------------|----------------------|-----------------------------|---------------|------------------|
| 8 | 84.8 | 80.0 | 基准 / Baseline | 🏆 最佳 / Best |
| 12 | 83.1 | 70.2 | -2.0% | |
| 16 | 83.5 | 75.0 | -1.5% | |

---

### 🎯 优先测试：GPU 内存甜点阈值 / Priority: GPU Memory Sweet Spot
**MUST DO first - highest ROI optimization!**

**中文** | **English**  
这是所有优化里性价比最高的一项，通常能白嫖 50-100% 的速度提升，零质量损失！  
_This is the highest ROI optimization you can do - typically 50-100% speed boost with ZERO quality loss!_

#### 背景 / Background
**中文** | **English**  
几乎所有模型+显卡的组合，都存在一个断崖式的性能阈值：  
_Almost every model + GPU combination has a cliff-like performance threshold:_  
- ✅ 阈值以下：GPU 跑满，速度达到理论最大值  
  _Below threshold: GPU fully utilized, maximum theoretical speed_  
- ❌ 阈值以上：速度直接腰斩（40-60%），但显存只多占了 30-50MB  
  _Above threshold: Speed drops by 40-60% (half speed), but VRAM only increases 30-50MB_  

这不是线性下降，是跳崖式下降！原因通常是：  
_This is NOT a linear degradation, but a cliff! Common causes:_  
1. GDDR 显存 Bank 对齐边界，跨 Bank 访问延迟翻 3-5 倍  
   _GDDR memory bank alignment - cross-bank access latency increases 3-5x_  
2. FlashAttention 的 Tile 块大小阈值，超过之后触发缓存换页  
   _FlashAttention tile size threshold - exceeding triggers cache swapping_  
3. 大页内存分配失败，TLB 命中率骤降  
   _Large page memory allocation failure - TLB hit rate plummets_  

#### 标准测试方法 / Standard Testing Method
**中文** | **English**  
1. **从厂商标称的最大上下文开始** / _Start from manufacturer's advertised maximum_（比如 128K）  
2. **每次降 4K** / _Reduce by 4K each time_（必须是 2 的幂次相关步长 / Must be power-of-2 aligned）  
3. 每次都跑一次完整测速（生成 600 token 左右） / _Run full speed test each time (~600 tokens)_  
4. 找到 **速度突然跳涨的那个点** / _Find the point where speed suddenly jumps_，就是你的黄金甜点阈值 / _That's your sweet spot!_  

#### 典型测试结果示例 / Typical Test Results
**Qwen3.6-35B + RTX 4060Ti 16GB**

| 上下文大小 / Context | 生成速度 / Speed | 显存占用 / VRAM | 状态 / Status |
|---------------------|------------------|-----------------|---------------|
| 122880 (120K, 默认) | ~30 token/s | ~15.2 GB | ❌ 内存紧张 |
| 118000 (118K) | ~29-36 token/s | ~15.1 GB | ❌ 内存紧张 |
| **110000 (110K)** | **~90 token/s** | ~15.0 GB | ✅ 满速 |
| 96K | ~86 token/s | ~14.5 GB | ✅ 满速 |
| 64K | ~88 token/s | ~14.0 GB | ✅ 满速 |

#### 核心结论 / Key Takeaways
**中文** | **English**  
- 通常甜点阈值 = 厂商标称最大值的 90-95%  
  _Typically sweet spot = 90-95% of advertised maximum_  
- 上下文只少 5-10%（完全感知不到），速度提升 50-100%  
  _Only 5-10% less context (completely unnoticeable) for 50-100% speed boost_  
- **这一步必须第一个做！** 所有后续参数测试都应该在甜点阈值下进行  
  _**DO THIS FIRST!** All subsequent parameter testing should be done at the sweet spot_  


---

### ✅ 第三阶段：质量验证

#### 步骤 5：量化损失验证
对比开/关量化的输出质量，使用相同的 Prompt + 温度=0.1 最小化随机性：
```
测试方法：
1. 关 KV 量化（FP16），输出结果 A
2. 开 KV q8_0 量化，相同 Prompt，输出结果 B
3. 人工对比 A 和 B，判断是否有可感知的质量损失
```

#### 步骤 6：上下文回忆能力测试
使用「密钥召回法」验证长上下文能力：
```
测试方法：
1. 构造长 Prompt：前面是大量无关填充文本
2. 在 Prompt 的 10% / 50% / 90% 位置分别藏一个随机密钥
3. 问模型：「文档中的秘密密钥是什么？」
4. 记录不同距离的召回成功率
```

**典型测试距离：**
- 短距离：~1000 token
- 中距离：~20000 token
- 长距离：~50000 token（根据最大上下文调整）

#### 步骤 7：基本能力冒烟测试
验证模型的基础能力没有因为参数调整而下降：
```
测试用例：
1. 简单数学题：小明有5个苹果，给了小红2个，又买了3个，现在有几个？
2. 简单逻辑题：正方形边长4cm，面积是多少？
3. 简单代码题：用Python写一个函数求列表偶数的和
```

---

### 🎯 第四阶段：综合评估与产出

#### 步骤 8：多维度综合评分
| 维度 | 权重 | 评分标准（10分制） |
|------|------|-------------------|
| **性能** | 50% | 生成速度(30%) + Prompt速度(20%) |
| **质量** | 40% | 量化损失(15%) + 上下文回忆(15%) + 基本能力(10%) |
| **稳定性** | 10% | 启动成功率、运行稳定性、API兼容性 |

#### 步骤 9：反常识发现总结
**必须记录所有反直觉的结论！** 这些是最有价值的经验：

**示例（来自 Qwen3.5-MoE 实战）：**
1. ❗ 默认 batch size 是 512，改成 2048 直接快 67.7%！
2. ❗ KV q8_0 量化不是损失，反而让 Prompt 处理快了 128%！
3. ❗ Flash Attention 对 MoE 模型：生成慢 1.3%，但 Prompt 快 128%，整体收益巨大！
4. ❗ 线程不是越多越好：8 线程比 12/16 都快！
5. ❗ 链式测试会严重误导结论：必须严格控制变量！

#### 步骤 10：产出最终最佳配置
最终输出：
1. ✅ 最佳性能配置（最快速度）
2. ✅ 最佳上下文配置（最大窗口）
3. ✅ 综合推荐配置（平衡最佳）
4. ✅ 一键启动的完整命令

---

## 实战案例合集

---

### 案例1：Qwen3.5-MoE 35B + RTX 4060Ti 16GB（MoE 模型，仅供参考）

#### 优化成果
**初始速度：23.4 tokens/s → 最终速度：84.8 tokens/s，提升 262%！**

#### 最佳参数
| 参数 | 最佳值 | 收益 |
|------|--------|------|
| `--threads` | 8 | +2.4% |
| `-b / --batch-size` | 2048 | +67.7% 最大提升！ |
| `--ctx-size` | 65536（最快）或 262144（最大） | 64K 比 256K 快 3.7 倍 |
| `--flash-attn` | on | Prompt +128%，生成 -1.3% |
| `--cache-type-k/v` | q8_0 | Prompt +128%，省 512MB，零质量损失 |
| `--parallel` | 2 | Prompt 最快，支持 2 并发 |
| `--ubatch-size` | 默认 512 | 改了反而慢 17-60% |

---

### 案例2：Qwen3.6-35B Dense + RTX 4060Ti 16GB（Dense 模型，2026-04-26 最新测试，仅供参考）

#### 优化成果
**初始速度：~30 tokens/s → 最终速度：~90 tokens/s，提升 2-3 倍！**

**📋 验证方法：**
```bash
# 标准 curl 测速命令（固定 temperature=0.7, max_tokens=100）
curl -s http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"请写一段500字左右的技术博客文章，讨论本地部署大语言模型的性能优化方法"}],"max_tokens":100,"temperature":0.7}'
```

**⚠️ 关键原则：GPU 内存覆盖就是生命线**
> "GPU 内存就是生命线，够用就快，不够用就慢。"

公式：**最大上下文 = (GPU VRAM - 模型权重 - 安全缓冲) ÷ KV 缓存每 token开销**

以 RTX 4060Ti 16GB + Qwen3.6-35B 为例：
- 模型权重 ~13.4GB | KV缓存(ctx 110K) ~1.1GB | 计算缓冲 ~0.5GB | **总计 ~15GB**
- 留出 ~1GB 缓冲，ctx-size=110000 是安全甜点

#### 核心发现：GPU 内存覆盖原则
| 上下文 | 速度 | 状态 |
|--------|------|------|
| 122880 (120K) | ~30 token/s | ❌ GPU 内存不足 |
| 118000 (118K) | ~29-36 token/s | ❌ GPU 内存不足 |
| **110000 (110K)** | **~90 token/s** | ✅ GPU 完全覆盖 |
| 96K / 64K / 32K | ~86-88 token/s | ✅ 满速 |

减少 8% 上下文，速度提升 **2-3 倍**，零质量损失！

**GPU 内存分析 / GPU Memory Analysis:**
| 项目 / Item | 占用 / Usage |
|-------------|-------------|
| 模型权重 | ~13.4 GB |
| KV 缓存 (ctx 120K) | ~1.2 GB |
| 计算缓冲区 | ~0.5 GB |
| **总计** | **~15.2 GB** |
| GPU 总 VRAM | 16 GB |
| **剩余** | **~0.8 GB** |

#### 最佳参数
| 参数 | 最佳值 | 说明 |
|------|--------|------|
| `--ctx-size` | **110000（110K）** | GPU 完全覆盖，速度最快 |
| `--threads` | 8 | 最佳 |
| `-b / --batch-size` | 2048 | 最佳 |
| `--parallel` | **1** | ❗ Dense 模型上 parallel=2 反而慢 40% |
| `--flash-attn` | on | 必须开，长 Prompt 处理快 3-5 倍 |
| `--cache-type-k/v` | q8_0 | q4_K 有兼容性问题 |

### 最终最佳启动命令（Qwen3.6-35B Dense + 4060Ti，110K 甜点阈值）
```bash
# Linux/WSL2（推荐，绑定到 localhost）
llama-server -m "你的模型路径.gguf" --n-gpu-layers 9999 --ctx-size 110000 --port 8080 --host 127.0.0.1 --threads 8 --mlock --parallel 1 --kv-unified --flash-attn on -b 2048 --cache-type-k q8_0 --cache-type-v q8_0
```

> ⚠️ **生产环境建议**：如需对外提供服务，应通过 Nginx/Caddy 等反向代理 + HTTPS，不要直接暴露 llama-server。

---

### 案例3：Qwen3.6-27B Dense + RTX 4060Ti 16GB（2026-04-28 最新测试）

**⚠️ 模型说明**：Qwen3.6-27B 是 Qwen3.6-35B 的更轻量版本，权重更小（~12GB vs ~13.4GB），但优化结论不完全相同！

#### 优化成果
**纯生成速度：~23.6 tok/s**

#### 核心发现（与 35B 不同之处）

**1. 理论计算不可靠！实际测试才是王道**
- 理论公式算出甜点 = 110K（(16GB - 12GB - 1GB缓冲) ÷ KV每token ≈ 110K）
- 实际测试 **110K 直接 CUDA OOM**
- 真实甜点：**96K**（实测稳定，18.6 tok/s）
- **结论：理论公式只能做起点参考，必须实际跑一遍才能确定**

**2. Batch Size 对 27B 的影响与 35B 相反**
- 35B（Dense）：2048 最佳
- 27B（Dense）：**512 最佳**（2048 反而慢 6.6%）
- 原因：27B 权重更小，GPU 有更多余量处理小 batch 的缓存效率

**3. 推理模型的思考开销是硬伤**
- Qwen3.6-27B 是推理模型（reasoning mode），内置思考过程
- 简单问题（"写一句诗"）也要花 48 秒思考
- 思考阶段输出 800+ reasoning chunks，但 max_tokens 被思考占满后无法输出
- **如果不需要推理能力，换非推理版本（Qwen3.6-27B-Instruct 非推理版）体验更好**

#### GPU 内存分析
| 项目 | 占用 |
|------|------|
| 模型权重 | ~12 GB |
| KV 缓存 (ctx 96K) | ~1.2 GB |
| 计算缓冲区 | ~1.0 GB |
| **总计** | **~14.2 GB** |
| GPU 总 VRAM | 16 GB |
| **剩余** | **~1.8 GB** |

#### 最佳参数
| 参数 | 最佳值 | 说明 |
|------|--------|------|
| `--ctx-size` | **96000** | 实测甜点（110K OOM） |
| `--threads` | 8 | 比 16 省 50% CPU，速度差异 <2% |
| `-b / --batch-size` | **512** | 27B 上 512 比 2048 快 6.6% |
| `--parallel` | 1 | Dense 模型单请求最快 |
| `--flash-attn` | on | off 会崩溃 |
| `--cache-type-k/v` | q8_0 | 零质量损失，省显存 |

#### 最终启动命令
```bash
llama-server -m "Qwen3.6-27B-Q3_K_S.gguf" \
  --n-gpu-layers 9999 --ctx-size 96000 --port 8080 --host 127.0.0.1 \
  --threads 8 --threads-batch 8 --mlock --parallel 1 \
  --kv-unified --flash-attn on -b 512 \
  --cache-type-k q8_0 --cache-type-v q8_0
```

#### 配套配置
**llama-server 守护进程** (`~/.config/systemd/user/llama-server.service`)
```ini
[Service]
ExecStart=/home/fenglai/llama.cpp/build/bin/llama-server \
  -m /home/fenglai/models/Qwen3.6-27B-Q3_K_S.gguf \
  --n-gpu-layers 9999 --ctx-size 96000 --port 8080 --host 127.0.0.1 \
  --threads 8 --threads-batch 8 --mlock --parallel 1 \
  --kv-unified --flash-attn on -b 512 \
  --cache-type-k q8_0 --cache-type-v q8_0
```

**OpenClaw 配置** (`~/.openclaw/openclaw.json`)
```json
"contextWindow": 96000,
"maxTokens": 48000
```
> ⚠️ OpenClaw 的 contextWindow 必须与 llama-server 的 --ctx-size 保持一致，否则会导致上下文截断或 OOM。maxTokens 设为 ctx-size 的一半左右，给 prompt 留出空间。

#### OpenClaw 配置注意事项
- `contextWindow` 必须等于 `--ctx-size`（96000）
- `maxTokens` 建议设为 `ctx-size / 2`（48000），为 prompt 预留空间
- `reserveTokensFloor`（compaction 保留 token）建议设为 20000，避免频繁压缩
- 模型 `reasoning: true` 需开启，否则思考内容无法正确解析

### 进阶：CPU 亲和性绑定（+1-5% 速度，聊胜于无）
Linux/WSL2 下可以用 `taskset` 把线程绑到同一物理核心簇上，减少跨核通讯开销：
```bash
taskset -c 0-7 llama-server ...
```
注意：核心范围要和你的 `--threads` 参数对应，不要跨 CCX 模块。

> ⚠️ **安全提示**：此功能仅在 Linux/WSL2 下可用，Windows 下无等效命令。

---

## 核心原则

1. **GPU 内存覆盖优先**：在完全使用专用 GPU 内存的前提下，找到最大上下文值 — 这是提升速度最快的优化
2. **GPU 内存就是生命线**：够用就快，不够用就慢（GPU↔CPU 交换是最大性能杀手）
3. **甜点公式只是起点**：公式计算 (GPU VRAM - 权重 - 缓冲) ÷ KV 每 token 开销，但**实际测试才是唯一真理**（27B 上公式算 110K，实际 96K 才是甜点）
4. **控制变量高于一切**：每次只改一个参数，其他全部保持不变
5. **不要只看生成速度**：Prompt 处理速度同样重要，甚至更重要
6. **量化不一定是损失**：有时候反而更快，一定要实际测试
7. **默认参数通常很保守**：一定要测试更大的 batch size、不同的线程数
8. **不同模型结论不同**：MoE 和 Dense 最佳参数可能完全相反；同系列不同大小（27B vs 35B）的 batch size 最优值也可能相反
9. **推理模型的思考开销**：Qwen3.6 等推理模型内置 thinking chain，TTFT 极长（40-50s），不适合需要低延迟的对话场景
10. **OpenClaw 配置必须对齐**：`contextWindow` 必须等于 `--ctx-size`，`maxTokens` 约等于 `ctx-size / 2`，否则上下文异常

---

## 快速检查清单

每次优化前过一遍：
- [ ] 已记录默认参数下的基准速度
- [ ] 已列出所有待测试的参数
- [ ] 每次测试只改一个参数
- [ ] 已验证量化损失（如果开了量化）
- [ ] 已测试长上下文回忆能力
- [ ] 已做基本能力冒烟测试
- [ ] 已记录所有反常识的发现
- [ ] 已产出最终的一键启动命令

## 安全与调试建议

### 参数调试安全指南
1. **小步测试**：每次调整幅度不超过 10%，避免 OOM
2. **监控显存**：使用 `nvidia-smi` 实时观察，确保不突破 GPU 上限
3. **崩溃自救**：如果模型频繁崩溃，尝试减小 `--ctx-size` 或 `--batch-size`
4. **云端辅助调试**：当本地模型因参数不当反复崩溃时，建议使用云端模型（OpenAI / Gemini / 通义千问等）进行推理验证和逻辑测试。本地环境只用于性能调优，不用于逻辑正确性验证
5. **参数记录**：所有测试参数必须记录，避免重复试错
6. **避免生产配置泄露**：不要在公网文档、代码仓库中暴露 llama-server 的内部参数

### 反常识发现总结
**必须记录所有反直觉的结论！** 这些是最有价值的经验：

**示例（来自 Qwen3.5-MoE 35B 实战）：**
1. ❗ 默认 batch size 是 512，改成 2048 直接快 67.7%！
2. ❗ KV q8_0 量化不是损失，反而让 Prompt 处理快了 128%！
3. ❗ Flash Attention 对 MoE 模型：生成慢 1.3%，但 Prompt 快 128%，整体收益巨大！
4. ❗ 线程不是越多越好：8 线程比 12/16 都快！
5. ❗ 链式测试会严重误导结论：必须严格控制变量！

**示例（来自 Qwen3.6-27B Dense 实战，2026-04-28）：**
1. ❗ **理论计算不可靠**：公式算出 110K 甜点，实际 110K 直接 CUDA OOM，真实甜点 96K。必须实测！
2. ❗ **Batch size 结论因模型而异**：35B Dense 上 2048 最优，27B Dense 上 512 反而快 6.6%。不要照搬！
3. ❗ **推理模型有思考开销**：Qwen3.6 内置推理链，简单问题也要 40-50 秒 TTFT，不适合日常对话
4. ❗ **threads-batch 影响**：--threads-batch 8 比默认 1 提升 prompt 处理速度
5. ❗ **OpenClaw contextWindow 必须匹配**：配置里的 contextWindow/maxTokens 要跟 --ctx-size 对齐，否则上下文异常

> 💡 **重要提醒**：不同模型、不同量化版本的最佳参数差异可能很大。**不要直接套用**他人参数，必须实际测试。如果本地模型因参数设置不当频繁崩溃，可先用云端模型做逻辑验证，本地只用于性能调优。
