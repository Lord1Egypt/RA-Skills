> 本文档为方法说明（附属于主 SKILL.md）；涉及本地路径/脚本处请按你自己的环境调整。

# Windows ComfyUI 视频生成环境搭建（Wan 2.1 / LTX-Video）

> 2026-09-10 实测跑通（联想R9000P / RTX 4060 Laptop 8G / 32G RAM）。Wan2.1-1.3B 文生视频出片成功。路径：`D:\大软件安装处\ComfyUI\ComfyUI_windows_portable\`

## 环境要求（版本链条必须匹配，错一环就跑不起来）
| 组件 | 版本 | 说明 |
|---|---|---|
| ComfyUI | 最新版 | 2024-08 老便携版无 Wan 节点，必须升级。git 直连 github 失败→配镜像：`git config --global url."https://ghfast.top/https://github.com/".insteadOf "https://github.com/"` |
| torch | **2.14.0+cu130** | comfy-kitchen 0.2.33 硬要 CUDA 13（nvidia-cublas>=13）；cu121 源最高只到 torch 2.5.1，报 `torch.library has no attribute custom_op` 或 `infer_schema ... list[int]` |
| Nvidia 驱动 | **616.92**（原 576.52 只到 CUDA 12.9）| 不升驱动 → cu130 torch 装上也 `cuda is_available: False`（cudaErrorNotSupported）。驱动从 `gfwsl.geforce.com` AjaxDriverService API 查；us.download.nvidia.com 需带浏览器 UA 才能下（否则 403）|
| ffmpeg | imageio-ffmpeg（自带静态 ffmpeg 7.1）| 视频编码必需；缺了报 `[Errno 22] Invalid argument` |
| comfy_kitchen | 0.2.33（ComfyUI requirements pin）| 别删！comfy/ldm/modules/attention.py 硬依赖，删了连 Wan 都跑不了 |

安装依赖：`python_embeded\python.exe -s -m pip install -r ComfyUI\requirements.txt`
torch 单独指定源：`pip install --upgrade torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu130`

## 模型（必须用 ComfyUI 标准格式，别用官方原始权重）
源：`Comfy-Org/Wan_2.1_ComfyUI_repackaged`（hf-mirror.com 可达）
| 文件 | 放置目录 | 大小 |
|---|---|---|
| `wan2.1_t2v_1.3B_fp16.safetensors` | models/diffusion_models/ | 2.84G |
| `umt5_xxl_fp8_e4m3fn_scaled.safetensors` | models/text_encoders/ | 6.74G |
| `wan_2.1_vae.safetensors` | models/vae/ | 0.25G |

LTX-Video 图生视频：`ltxv-2b-0.9.8-distilled-fp8.safetensors`(4.46G)→diffusion_models + `t5xxl_fp8_e4m3fn.safetensors`(4.89G，源 `comfyanonymous/flux_text_encoders`)→text_encoders

⚠️ **最大的坑**：用 Wan 官方原始 `.pth`（`models_t5_umt5-xxl-enc-bf16.pth`）会报 **`Cannot copy out of meta tensor; no data!`**（发生在 CLIPTextEncode）——必须换成上面 repackaged 的 safetensors。诊断信号：报错在 CLIPTextEncode 且 traceback 落到 `model_management.cast_to` → 就是模型格式不对，不是显存/参数问题。

## 启动
```bash
cd "D:\大软件安装处\ComfyUI\ComfyUI_windows_portable"
python_embeded\python.exe -s ComfyUI\main.py --windows-standalone-build --disable-async-offload
```
- `--disable-async-offload` 协调低显存 offload 调度
- **后台运行不要用 `| tee` 管道**！tqdm 写 stderr 到已关闭管道 → `[Errno 22] Invalid argument` 中断 KSampler。（traceback 指向 `logger.py flush` + `tqdm status_printer`，极易误判成"生成失败"）。用 `> log.txt 2>&1` 重定向。
- 启动成功标志：`Device: cuda:0 ...`、`Total VRAM`、`Found comfy_kitchen backend cuda`、端口 `127.0.0.1:8188 LISTENING`

## 标准 Wan T2V 工作流（API JSON 提交）
节点链：`UNETLoader` + `CLIPLoader(type="wan")` + `VAELoader` + `CLIPTextEncode`(正/负) + **`EmptyHunyuanLatentVideo`** + `KSampler` + `VAEDecode` + **`CreateVideo`** + **`SaveVideo`**
- 视频 latent 用 `EmptyHunyuanLatentVideo`（不是 EmptyLatentImage，也不是 Mochi）
- `SaveVideo` 要 `VIDEO` 类型 → 必须经 `CreateVideo`（IMAGE→VIDEO），否则报 `return_type_mismatch`
- 参考参数：832×480 / length 33（约2秒）/ steps 15-25 / cfg 5.5-6.0 / sampler `uni_pc` + scheduler `simple`
- 提交：`POST http://127.0.0.1:8188/prompt` body `{"prompt": {节点id: {class_type, inputs}}}`，看返回 `node_errors` 是否为空
- 轮询：`GET /history/{prompt_id}` → `status.status_str` = success/error；`GET /queue` 看运行中任务
- 官方模板参考：`ComfyUI/blueprints/*.json`、`site-packages/comfyui_workflow_templates_json/templates/text_to_video_wan.json`

## 8G 显存心法
- 跑前关 Chrome 等占显存程序（余下 ~6.8G）
- 分辨率 ≤832×480、帧数 ≤33；超了会严重 offload 到内存，极慢
- 长视频要分段生成再拼；**人物一致性靠图生视频（LTX-2B），文生视频做不到**——这是给客户解释一致性时的核心结论
- 实测：33帧/832×480 约 2-3 分钟出片