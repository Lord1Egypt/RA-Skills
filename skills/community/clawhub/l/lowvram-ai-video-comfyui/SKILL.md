---
name: lowvram-ai-video-comfyui
slug: lowvram-ai-video-comfyui
displayName: 8G显存跑AI视频·4060实测低显存文生/图生视频
description: >-
  网上的 AI 视频教程开口就是 24G 显存，一看就把人劝退——**其实 8G 的 4060 也能跑**。这套是 RTX 4060 Laptop 8G 显存 / 32G 内存 / Win11 上真跑出来的配置与调参。

  能做什么：本地生成低分辨率、几秒的短视频（动漫向，自媒体够用），全程本地、零 API 费用。

  里面几条最值钱的，都是踩坑换来的：
  - **文生视频和图生视频是两套模型，不能互换**：Wan2.1-1.3B 只有文生视频，它的图生视频是 14B（8G 跑不动）；8G 能跑的图生视频是 LTX-2B fp8
  - **人物一致性正解**：纯文生视频做不到"同一主角多段连续"，要用同一张角色图做首帧逐段生成再拼接；硬拼 N 段必然人物漂移
  - **部署顺序不能跳**：ComfyUI 便携版安装 → 升到最新版（旧版没有 Wan/LTX 节点）→ 依赖升级 → torch 与 comfy-kitchen 版本匹配
  - 国内网络下的 GitHub 镜像配置、MSYS 路径把 7z 解压目标搞坏的坑
  - **白下载预警**：动手前先验模型有没有音频能力、显存装不装得下，别下完 20G 才发现跑不动

  输入：一段提示词（文生）或一张角色图（图生）
  输出：本地生成的短视频文件

  触发词：本地跑AI视频、低显存、8G显存、4060、显存不够怎么跑、ComfyUI视频、Wan2.1、LTX、文生视频、图生视频、本地视频生成、零成本AI视频。
  能做什么：本地生成低分辨率、几秒的短视频（动漫向，自媒体够用），全程本地、零 API 费用。

  里面几条最值钱的（都是踩坑换来的）：
  - **文生视频和图生视频是两套模型不能互换**：Wan2.1-1.3B 只有文生视频，它的图生视频是 14B（8G 跑不动）；8G 能跑的图生视频是 LTX-2B fp8
  - **人物一致性正解**：纯文生视频做不到「同一主角多段连续」，要用同一张角色图做首帧逐段生成再拼接；硬拼 N 段必人物漂移
  - **部署顺序不能跳**：ComfyUI 便携版安装 → 升到最新版（旧版没有 Wan/LTX 节点）→ 依赖升级 → torch 与 comfy-kitchen 版本匹配
  - 国内网络下的 GitHub 镜像配置、MSYS 路径把 7z 解压目标搞坏的坑
  - **白下载预警**：动手前先验模型有没有音频能力、显存装不装得下，别下完 20G 才发现跑不动

  触发词：本地跑AI视频、低显存、8G显存、4060、ComfyUI视频、Wan2.1、LTX、文生视频、图生视频、显存不够怎么跑、本地视频生成。
version: 1.1.0
author: 九品锦锂e
summary: 8G 显存也能跑本地 AI 视频：Wan2.1-1.3B 文生 + LTX-2B 图生，含模型选型红线与白下载预警，全程本地零 API 费用。
license: MIT
metadata:
  version: "1.1.0"
category: design-media

---
# 本机 AI 视频生成（ComfyUI + Wan / LTX）

> 基线机器：RTX 4060 Laptop **8G 显存** / 32G 内存 / Win11。
> 定位：本地出**低分辨率、几秒**的动漫短视频（自媒体够用）。**别把 8G 当 16G 用**。

## 何时用
用户说"跑视频模型/文生视频/图生视频"，或要把本地视频生产环境交给执行成员（团队成员等）继续实验时。

## 先建立认知（选型不走错）
- **文生视频(T2V) 与 图生视频(I2V) 是两套模型，不能互相替代**：
  - Wan2.1-**1.3B 只有 T2V**；Wan 的 I2V 只有 14B（8G 跑不动）。
  - 8G 能跑的 **I2V = LTX-2B fp8**（另需 t5xxl 编码器）。
- **长视频/人物一致性**：纯 T2V 做不到"同一主角多段连续"；正解是 I2V **用同一张角色图做首帧**，逐段生成再拼接。T2V 硬拼 N 段必人物漂移。
- **Ollama 与 ComfyUI 模型不通用**：Ollama 是语言模型（写提示词/剧情），ComfyUI 是扩散模型（出片）。是配合分工，不是替代。

## 部署顺序（按序做；跳步必踩坑）

**1) 装 ComfyUI 便携版**（放 D 盘，勿占 C 盘）
- 从 `Comfy-Org/ComfyUI` GitHub release 取 `ComfyUI_windows_portable_nvidia.7z`（自带 python+torch+CUDA）。
- ⚠️ **bash 下 `7z x -o"/d/..."` 的 MSYS 路径会被转换坏，产物不落目标目录**（解压报成功但目录空）。→ 用 **Python subprocess 传原生 Windows 路径**调 7z。

**2) 升级 ComfyUI 到最新版**（旧版没有 Wan/LTX 节点）
- GitHub 直连常 `Connection was reset` → 先配镜像：
  `git config --global url."https://ghfast.top/https://github.com/".insteadOf "https://github.com/"`，再 `git pull --ff-only origin master`。

**3) 升级 Python 依赖**：`python_embeded\python.exe -s -m pip install -r ComfyUI\requirements.txt`（新版会新增 `comfy-kitchen` 等）。

**4) torch 必须与 comfy-kitchen 匹配**（按症状逐级排）：
| 症状 | 根因 | 处置 |
|---|---|---|
| `module 'torch.library' has no attribute 'custom_op'` | torch < 2.4 | 升 torch |
| `infer_schema ... unsupported type list[int]` | torch 与 comfy-kitchen 不匹配 | 升到 **cu130** 的 torch（2.14+） |
| `cudaErrorNotSupported / likely using older driver` | **驱动 CUDA 版本不够** | 升级 NVIDIA 驱动 |
- 先判驱动上限：`nvidia-smi` 看 `CUDA Version`；要 CUDA 13 就必须升驱动。
- 取最新驱动：NVIDIA 驱动查询 API（`AjaxDriverService`，RTX40 系笔记本 psid=138/pfid=1005）拿 `DownloadURL`；**下载需带浏览器 UA + Referer，否则 403**。静默装 `-s -noreboot`；装完 `nvidia-smi` 确认，**通常无需重启** torch 即可识别 GPU。

**5) 模型必须用 ComfyUI 标准格式**（最容易踩的坑）
- 从 `Comfy-Org/Wan_2.1_ComfyUI_repackaged` 的 `split_files/` 下 safetensors：
  - `diffusion_models/wan2.1_t2v_1.3B_fp16.safetensors`（≈2.8G）
  - `text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors`（≈6.7G）
  - `vae/wan_2.1_vae.safetensors`（≈0.25G）
- ⚠️ 用 Wan 官方原始 `.pth`（如 `models_t5_umt5-xxl-enc-bf16.pth`）→ 报 **`Cannot copy out of meta tensor; no data!`**（CLIPTextEncode 阶段）。这是**格式/命名不匹配**，不是显存问题——别去调显存参数。
- 国内下载：HuggingFace 直连不通 → 用 **hf-mirror.com**；`curl -C - --retry 999 --retry-all-errors` 断点续传。
- 落位：`ComfyUI\models\{diffusion_models,text_encoders,vae}\`。

**6) 装 ffmpeg（视频编码必需）**：`python_embeded\python.exe -s -m pip install imageio-ffmpeg imageio`（自带静态 ffmpeg）。缺它 SaveVideo 阶段报 `[Errno 22]`。

**7) 启动服务**
```
python_embeded\python.exe -s ComfyUI\main.py --windows-standalone-build --disable-async-offload > log.txt 2>&1
```
- `--disable-async-offload`：8G 下避免文本编码器权重停在 meta device。
- ⚠️⚠️ **绝不用 `| head` / `| tee` 管道启动这类长驻服务**：tqdm 进度条写已关闭的管道 → `[Errno 22] Invalid argument` 直接中断 KSampler，**看起来像模型报错，其实是启动方式问题**。用 `> 日志 2>&1` 重定向。这条坑对**任何长驻进程/网关**同样成立——管道关闭会连带杀掉进程。
- 判就绪：`netstat -ano | grep :8188` 有 LISTENING。

## 跑文生视频（T2V）
- 节点链照抄 `templates/wan21_t2v_workflow.json`：
  `CLIPLoader(type=wan) + VAELoader + UNETLoader + EmptyHunyuanLatentVideo + CLIPTextEncode(正/负) + KSampler + VAEDecode + CreateVideo + SaveVideo`
  - 视频 latent 用 **EmptyHunyuanLatentVideo**；输出必须 **CreateVideo → SaveVideo**。
  - ⚠️ `VAEDecode` 输出是 IMAGE，直连 SaveVideo 会报 `received_type(IMAGE) mismatch input_type(VIDEO)`。
- 提交：`POST http://127.0.0.1:8188/prompt`，body `{"prompt": {节点id: {class_type, inputs}}}`；返回 `node_errors:{}` 即通过。
- 查进度：`GET /history/<prompt_id>` 看 `status.status_str`（running/success/error）；error 时读 `messages` 里的 `execution_error`（含 `node_id/node_type/exception_message`）。
- **8G 实测可用参数**：832×480、length 33（≈2 秒）、steps 15-20、cfg 5.5-6.0、fps 16。超了会 offload 到内存，极慢。
- 产物在 `ComfyUI\output\*.mp4`；用 `imageio_ffmpeg.get_ffmpeg_exe()` 调 ffmpeg 验时长/分辨率。

## 跑图生视频（I2V）
- 用 **LTX-2B**：`ltxv-2b-0.9.8-distilled-fp8.safetensors`（≈4.5G）→ `models\diffusion_models\`；text encoder 用 **t5xxl**：`t5xxl_fp8_e4m3fn.safetensors`（≈4.9G，来自 `comfyanonymous/flux_text_encoders`）→ `models\text_encoders\`。
- ⚠️ LTX 用 **t5xxl**、Wan 用 **umt5**，**两者不通用**，都要下。
- 一致性打法：固定一张角色图当首帧逐段生成，或用 IPAdapter/InstantID 注入角色。

## 跑前准备（8G 显存）
- 关 Chrome 等占显存软件（系统/桌面常占 ~1.2G，Chrome 可占 ~1.9G）。
- 单任务串行，别并发多个生成。

## 交付给执行成员
交接文档结构（照此写）：环境路径 → 启动命令（含参数）→ 模型清单（文件名+目录+大小）→ 可复用工作流 JSON → 8G 参数心法 → 踩坑速查 → 下一步待办。

## 参考
- `templates/wan21_t2v_workflow.json` — 实测跑通的 Wan2.1-1.3B 文生视频工作流（ComfyUI API 格式，可直接 POST）

---

## 关于作者

**九品锦锂e** ｜ 把踩过的坑封装成「拿来就能跑」的 skill，不写教科书。

这个 skill 是我自己在用的版本，里面每条坑都是真踩过的。**用的时候卡住了、想要进阶玩法、或者有别的场景想让我封装成 skill**，直接加我微信说，加时备注「SkillHub」我优先通过：

![九品锦锂e 微信二维码](https://jinli-vault-1372591613.cos.ap-guangzhou.myqcloud.com/skillhub/hook-wechat-jiupinjinlie.png)

> 扫码添加作者微信 · 备注「SkillHub」优先通过
