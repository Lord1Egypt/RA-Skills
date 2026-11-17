---
name: local-minigpt
description: 从零实现的本地小型 GPT(Python + PyTorch,字符级分词,默认约 150 万参数,CPU 可训练)。当用户想在本地训练/微调一个自己的小型语言模型、学习 Transformer/GPT 的从零实现、用 Python 写一个"本地AI大模型"演示、或需要用自有语料做本地文本风格模仿与续写(不追求真实大模型质量)时使用。附带:零 Key 网页搜索工具、检索增强开卷对照、代码能力考试、MiniViT 手写数字识别。典型触发:训练一个小模型、从零实现 GPT、字符级语言模型、用我的语料训练模型、mini GPT、nanoGPT 式实现。不适用于:直接运行现成开源大模型(Qwen/LLaMA 等请用 transformers 或 Ollama)、生产级 NLP 任务。
metadata:
  openclaw:
    requires:
      bins:
        - python
    emoji: "🧠"
---

# local-minigpt

从零实现的 Decoder-only Transformer(架构借鉴 GPT-2 / nanoGPT):字符级分词、
CPU/GPU 训练、warmup + 余弦退火、检查点保存、温度 + top-k 采样、流式生成。
仅在需要执行本技能时阅读本文件;所有脚本可直接运行。

## 环境

- 依赖 torch>=2.0。先检查:`python -c "import torch; print(torch.__version__, torch.cuda.is_available())"`,缺失则 `pip install torch`;有 NVIDIA GPU 时装 CUDA 版:`pip install torch --index-url https://download.pytorch.org/whl/cu126`(版本号需匹配该索引存在的构建),再用训练参数 `--device cuda`。
- 脚本自带 sys.path 引导,但目录结构需保持 scripts/ 与 data/ 同级(模板已排好)。

## 工作流

1. **准备语料** `data/train.txt`(任意 UTF-8 文本,建议 ≥10 万字符):
   - `python scripts/fetch_corpus.py`:下载公开领域古文约 28 万字(论语/古文观止/唐诗三百首等);全部失败时自动回退到自带 `data/demo.txt`。
   - 用户自有语料:复制到 data/train.txt,或训练时用 `--data` 指定路径。
2. **训练**(CPU 默认配置约 1.6 秒/步,1000 步约 27 分钟):

   ```powershell
   python scripts/train.py --max-iters 1000 --out-dir <用户工作区>/checkpoints/demo
   ```

   - 常用参数:`--n-layer --n-head --n-embd --block-size --batch-size --max-iters --lr --device`
   - 输出:`ckpt.pt`(最终)、`ckpt-best.pt`(最优验证)、`config.json`、`tokenizer.json`
   - 训练结束自动打印一段采样文本;日志最后一行是 TRAIN_DONE。
   - 注意:部分沙箱/容器对满载进程的进程内时钟会虚化,日志里的 tok/s 可能失真,耗时以外部秒表为准;真实机器上统计正常。
3. **生成**:

   ```powershell
   python scripts/generate.py --ckpt-dir <检查点目录> --prompt "子曰:" --max-new-tokens 200
   ```

   - 不带 `--prompt` 进入交互续写模式;`--temperature` 建议 0.5~0.8,`--top-k` 建议 20~50。
4. **测试**:`python scripts/test_tokenizer.py`;`python scripts/test_model.py`(后者含学习能力冒烟测试,应看到损失明显下降)。
5. **联网搜索 / 开卷对照**(可选):
   - `python scripts/web_search.py "查询词" --n 5`:零 API Key 搜索(DuckDuckGo/必应/百度自动降级 + 自动重试),`--json` 供程序调用。
   - `python scripts/search_demo.py --ckpt-dir checkpoints/demo --query "学而时习之"`:检索增强最小示例(开卷 vs 闭卷生成 + 8-gram 引用率标注)。
6. **编码能力考试**(可选):`python scripts/build_code_corpus.py` 构建代码语料与留出考卷;训练后用 `python scripts/coding_test.py --ckpt-dir checkpoints/code` 出成绩(困惑度 / ast 语法有效率 / 补全)。
7. **视觉能力**(可选):`python scripts/vision/train_vit.py --dataset synthetic --epochs 12 --max-train 10000` 训练 MiniViT 数字识别(约 20 万参数;MNIST 优先,离线自动合成;注意 ViT 慢起步,epoch 太少会误判为「学不动」);`python scripts/vision/make_samples.py` 渲染分布外考题;`python scripts/vision/predict.py data/samples/*.png` 看图识数。

## 调参经验

- 训练 loss 初值 ≈ ln(词表大小);几百步内应明显下降,否则先查学习率与语料大小。
- 生成像复读机:调低 temperature / top-k;流畅度上限取决于语料规模与参数量。
- 想加大规模(需 GPU):`--n-layer 12 --n-head 12 --n-embd 768 --block-size 512 --batch-size 32 --max-iters 20000 --device cuda`,约 8500 万参数。
- 检查点目录(`--out-dir`)请指向用户工作区,不要写进技能安装目录。

## 文件结构

scripts/model.py(模型)、tokenizer.py(分词器)、train.py(训练)、generate.py(生成)、
fetch_corpus.py(公开语料下载)、web_search.py(零 Key 搜索)、search_demo.py(开卷对照)、
build_code_corpus.py(代码语料)、coding_test.py(编码考试)、test_model.py / test_tokenizer.py(测试)、
vision/(MiniViT 视觉:模型、合成数据、训练、预测、采样);data/demo.txt(自带示例语料)。
