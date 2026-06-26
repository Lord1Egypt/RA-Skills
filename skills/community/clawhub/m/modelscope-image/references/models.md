# ModelScope 文生图模型列表

> 数据来源：https://modelscope.cn/models?filter=inference_type&tasks=text-to-image-synthesis
>
> 使用方法：当用户询问可用模型或需要选择模型时，加载此文件。

## 推荐模型（核心）

### 通用高质量模型

| 简称 | 模型 ID | 名称 | 特点 | 支持语言 |
|------|---------|------|------|----------|
| `kolors` | Kwai-Kolors/Kolors | 快手可图 | 支持中英文，高质量生成（默认） | zh, en |
| `qwen-image` | Qwen/Qwen-Image | Qwen-Image（小橙鱼） | 通义千问图像模型，下载量 2.3M | zh, en |
| `qwen-image-2512` | Qwen/Qwen-Image-2512 | Qwen-Image-2512（小橙鱼） | 通义千问最新版，写实摄影风格 | zh, en |
| `z-image-turbo` | Tongyi-MAI/Z-Image-Turbo | 造相 Z-Image-Turbo | 阿里造相快速版，下载量 408K | en |
| `z-image` | Tongyi-MAI/Z-Image | 造相 Z-Image | 阿里造相标准版，写实摄影风格 | en |

### SDXL / FLUX 系列

| 简称 | 模型 ID | 名称 | 特点 | 支持语言 |
|------|---------|------|------|----------|
| `sd-x1` | AI-ModelScope/stable-diffusion-xl-base-1.0 | Stable Diffusion XL 1.0 | SDXL 基础模型，高质量艺术创作 | en |
| `sd-turbo` | AI-ModelScope/sdxl-turbo | SDXL Turbo | SDXL Turbo，快速生成 | en |
| `flux-schnell` | black-forest-labs/FLUX.1-schnell | FLUX.1 schnell | FLUX.1 schnell，高质量快速生成 | en |
| `flux-dev` | MusePublic/489_ckpt_FLUX_1 | FLUX.1-dev | FLUX.1 开发版，下载量 1.3M | en |
| `majicflus` | MAILAND/majicflus_v1 | 麦橘超然 | 麦橘超然风格，下载量 545K | en |

## FLUX 系列

| 简称 | 模型 ID | 名称 | 描述 | 支持语言 |
|------|---------|------|------|----------|
| `flux-dev-fp8` | MusePublic/FLUX.1-dev-fp8-dit | FLUX.1-dev FP8 | FLUX.1-dev FP8 量化版，节省显存 | en |
| `flux-xhs` | yiwanji/FLUX_xiao_hong_shu_ji_zhi_zhen_shi_V2 | 苏-FLUX小红书极致真实 | 针对小红书风格优化的 FLUX，极致真实感 | zh, en |

## 麦橘系列

| 简称 | 模型 ID | 名称 | 描述 | 支持语言 |
|------|---------|------|------|----------|
| `majicmix-realistic` | MusePublic/majicMIX_realistic | majicMIX realistic | 麦橘写实风格，真实感强 | en |
| `majicmix-realistic-sd15` | MusePublic/majicMIX_realistic_maijuxieshi_SD_1_5 | majicMIX realistic SD1.5 | 麦橘写实 SD1.5 版本 | en |
| `majicbeauty-qwen` | merjic/majicbeauty-qwen1 | 麦橘千问美人 | 麦橘 + 千问，人像美人风格 | zh, en |

## SDXL/SD1.5 系列

| 简称 | 模型 ID | 名称 | 描述 | 支持语言 |
|------|---------|------|------|----------|
| `sdxl-asian` | MusePublic/46_ckpt_SD_XL | SDXL 亚洲人像 | SDXL ArienMixXL，专为亚洲人像优化 | en |
| `realistic-vision` | MusePublic/Realistic_Vision_V6.0_B1_SD_1_5 | Realistic Vision V6.0 | SD1.5 写实视觉模型，高质量真实感 | en |
| `chenkinnoob-xl` | ChenkinNoob/ChenkinNoob-XL-V0.1 | ChenkinNoob-XL | SDXL 风格模型 | en |
| `wai-illustrious` | QWQ114514123/WAI-illustrious-SDXL-v16 | WAI-illustrious SDXL | SDXL 插画风格模型 | en |

## Z-Image Turbo 微调系列

| 简称 | 模型 ID | 名称 | 描述 | 支持语言 |
|------|---------|------|------|----------|
| `z-image-turbo-meixiong` | laonansheng/meixiong-niannian-Z-Image-Turbo-Tongyi-MAI-v1.0 | 美胸年美 Z-Turbo | 造相 Z-Turbo 微调版 | zh, en |
| `z-image-turbo-ruanqing` | laonansheng/ruanqing-Z-Image-Turbo-Tongyi-MAI-v1.0 | 软情 Z-Turbo | 造相 Z-Turbo 软情风格微调 | zh, en |
| `z-image-turbo-naixi` | laonansheng/naixi-girl-Z-Image-Turbo-Tongyi-MAI-v1.0 | 女孩奶昔 Z-Turbo | 造相 Z-Turbo 奶昔风格微调 | zh, en |
| `z-image-turbo-asian` | laonansheng/Asian-beauty-Z-Image-Turbo-Tongyi-MAI-v1.0 | 亚洲美女 Z-Turbo | 造相 Z-Turbo 亚洲美女风格 | zh, en |
| `z-image-turbo-controlnet` | maozukao/Z-image-turbo-fun-unionunion-controlnet | Z-Image ControlNet | Z-Image 多合一控制模型，支持姿态/深度/线条等 | en |

## Qwen-Image 微调系列

| 简称 | 模型 ID | 名称 | 描述 | 支持语言 |
|------|---------|------|------|----------|
| `qwen-image-jzzs` | KookYan/Kook_Qwen_2512_jzzs | Qwen-2512 极致真实 | Qwen-Image 极致真实风格微调 | zh, en |
| `qwen-image-beauty` | qiyuanai/Qwen_Image_Strapless_Beauty_Model_Traffic_Code_INS_Douyin_Xiaohongshu_Kuaishou_Portrait_Photography_E_commerce | Qwen-Image 美女模特 | Qwen-Image 美女模特风格，适合写真摄影 | zh, en |
| `qwen-image-portrait` | diffsynth-i2L-gallery/Z-Image-realistic_portrait-roleplay-prop_detail-1770363034.962795 | 写实人像角色扮演 | 写实人像、角色扮演、道具细节风格 | zh, en |
| `qwen-image-muse` | MusePublic/Qwen-image | Qwen-Image (MusePublic) | Qwen-Image MusePublic 版本 | zh, en |

## 其他模型

| 简称 | 模型 ID | 名称 | 描述 | 支持语言 |
|------|---------|------|------|----------|
| `nano-banana` | qiyuanai/Nano-Banana_Trending_Disassemble_Clothes_One-Click-Generation | Nano-Banana 爆款角色 | 爆款角色拆解衣服一键生成 | zh, en |
| `r18-pose-real` | Muki182/r18_pose_real_sdxl | 真人姿态 LoRA | SDXL 真人姿态增强 LoRA | en |
| `umt5-xxl-fp8` | junweifeng/umt5_xxl_fp8_e4m3fn_scaled.safetensors | UMT5 XXL FP8 | UMT5 XXL FP8 量化版，文本编码器 | en |
| `qwenimage-bodyart` | jonathanfu/QwenImage-2512bodyartplus | Qwen-Image 人体艺术plus | Qwen-Image 人体艺术风格 | en |
| `pony-realistic` | laonansheng/Pony_Realistic-Pure-Desire-Beauty-SDXL_v1.0 | Pony 写实纯欲美女 | Pony SDXL 写实纯欲美女风格 | zh, en |
| `wan-ti2v` | muse/Wan2.2-TI2V-5B-FP8 | Wan2.2 图生视频 | Wan2.2 图生视频模型 FP8 版，工作流专用 | en |

## 模型选择建议

### 按使用场景

| 场景 | 推荐模型 | 理由 |
|------|---------|------|
| 中文提示词 | `kolors`, `qwen-image`, `qwen-image-2512` | 原生支持中文 |
| 快速生成 | `sd-turbo`, `z-image-turbo` | 专为速度优化 |
| 高质量艺术 | `sd-x1`, `flux-dev` | 艺术创作质量高 |
| 写实摄影 | `qwen-image`, `z-image`, `flux-xhs` | 写实风格突出 |
| 人像 | `sdxl-asian`, `majicmix-realistic` | 人像优化 |
| 小红书风格 | `flux-xhs` | 专为小红书优化 |
| 插画风格 | `wai-illustrious` | 插画风格 |

### 按下载量

1. `qwen-image` - 230万+
2. `flux-dev` - 130万+
3. `majicflus` - 54万+
4. `z-image-turbo` - 40万+
5. `z-image` - 8万+
6. `qwen-image-2512` - 7.9万+

---

**添加新模型**: 将模型信息添加到对应分类中，保持格式一致。
