const axios = require("axios");

// ComfyUI 服务地址
const COMFY_BASE_URL = process.env.COMFY_BASE_URL || "http://127.0.0.1:8000";
const COMFY_VIEW_URL = process.env.COMFY_VIEW_URL || "http://127.0.0.1:8000";

// 默认配置
const DEFAULT_OPTIONS = {
  timeout: 120000,      // 最大等待时间（2 分钟）
  interval: 2000,       // 轮询间隔（2 秒）
  width: 1024,          // 图片宽度
  height: 1024          // 图片高度
};

// ComfyUI 基础 workflow 模板
const BASE_WORKFLOW = {
  "76": {
    "inputs": {
      "value": ""  // 将被替换为实际的 prompt
    },
    "class_type": "PrimitiveStringMultiline",
    "_meta": {
      "title": "Prompt"
    }
  },
  "78": {
    "inputs": {
      "filename_prefix": "Newspaper-Image",
      "images": [
        "77:82",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "保存图像"
    }
  },
  "77:80": {
    "inputs": {
      "sampler_name": "euler"
    },
    "class_type": "KSamplerSelect",
    "_meta": {
      "title": "K 采样器选择"
    }
  },
  "77:81": {
    "inputs": {
      "noise": [
        "77:86",
        0
      ],
      "guider": [
        "77:90",
        0
      ],
      "sampler": [
        "77:80",
        0
      ],
      "sigmas": [
        "77:93",
        0
      ],
      "latent_image": [
        "77:83",
        0
      ]
    },
    "class_type": "SamplerCustomAdvanced",
    "_meta": {
      "title": "自定义采样器（高级）"
    }
  },
  "77:82": {
    "inputs": {
      "samples": [
        "77:81",
        0
      ],
      "vae": [
        "77:89",
        0
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE 解码"
    }
  },
  "77:83": {
    "inputs": {
      "width": [
        "77:84",
        0
      ],
      "height": [
        "77:85",
        0
      ],
      "batch_size": 1
    },
    "class_type": "EmptyFlux2LatentImage",
    "_meta": {
      "title": "空 Latent 图像（Flux2）"
    }
  },
  "77:84": {
    "inputs": {
      "value": 1024
    },
    "class_type": "PrimitiveInt",
    "_meta": {
      "title": "Width"
    }
  },
  "77:85": {
    "inputs": {
      "value": 1024
    },
    "class_type": "PrimitiveInt",
    "_meta": {
      "title": "Height"
    }
  },
  "77:86": {
    "inputs": {
      "noise_seed": Math.floor(Math.random() * 1000000000000)
    },
    "class_type": "RandomNoise",
    "_meta": {
      "title": "随机噪波"
    }
  },
  "77:87": {
    "inputs": {
      "unet_name": "flux-2-klein-4b.safetensors",
      "weight_dtype": "default"
    },
    "class_type": "UNETLoader",
    "_meta": {
      "title": "UNet 加载器"
    }
  },
  "77:88": {
    "inputs": {
      "clip_name": "qwen_3_4b.safetensors",
      "type": "flux2",
      "device": "default"
    },
    "class_type": "CLIPLoader",
    "_meta": {
      "title": "加载 CLIP"
    }
  },
  "77:89": {
    "inputs": {
      "vae_name": "flux2-vae.safetensors"
    },
    "class_type": "VAELoader",
    "_meta": {
      "title": "加载 VAE"
    }
  },
  "77:90": {
    "inputs": {
      "cfg": 1,
      "model": [
        "77:87",
        0
      ],
      "positive": [
        "77:92",
        0
      ],
      "negative": [
        "77:91",
        0
      ]
    },
    "class_type": "CFGGuider",
    "_meta": {
      "title": "CFG 引导器"
    }
  },
  "77:91": {
    "inputs": {
      "conditioning": [
        "77:92",
        0
      ]
    },
    "class_type": "ConditioningZeroOut",
    "_meta": {
      "title": "条件零化"
    }
  },
  "77:92": {
    "inputs": {
      "text": [
        "76",
        0
      ],
      "clip": [
        "77:88",
        0
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Positive Prompt)"
    }
  },
  "77:93": {
    "inputs": {
      "steps": 4,
      "width": [
        "77:84",
        0
      ],
      "height": [
        "77:85",
        0
      ]
    },
    "class_type": "Flux2Scheduler",
    "_meta": {
      "title": "Flux2 调度器"
    }
  }
};

/**
 * 生成图片（主函数）
 * @param {string} prompt - 图片生成提示词
 * @param {Object} options - 可选参数
 * @returns {Promise<Object>} 包含 imageUrl 和状态信息
 */
async function generateImage(prompt, options = {}) {
  const { timeout, interval, width, height } = { ...DEFAULT_OPTIONS, ...options };
  
  console.log('[ComfyUI] 开始生成图片，prompt:', prompt, `尺寸：${width}x${height}`);

  // 构建 workflow
  const workflow = JSON.parse(JSON.stringify(BASE_WORKFLOW));
  workflow["76"].inputs.value = prompt;
  // 使用随机种子确保每次生成不同
  workflow["77:86"].inputs.noise_seed = Math.floor(Math.random() * 1000000000000);
  // 设置图片尺寸
  workflow["77:84"].inputs.value = width;
  workflow["77:85"].inputs.value = height;

  // 1. 提交任务
  let promptId;
  try {
    const res = await axios.post(`${COMFY_BASE_URL}/prompt`, {
      prompt: workflow
    }, {
      timeout: 10000
    });

    promptId = res.data.prompt_id;
    if (!promptId) {
      throw new Error("No prompt_id returned from ComfyUI");
    }
    console.log('[ComfyUI] 任务已提交，prompt_id:', promptId);
  } catch (err) {
    console.error('[ComfyUI] 提交任务失败:', err.message);
    throw new Error("Failed to submit prompt: " + err.message);
  }

  // 2. 轮询结果
  const startTime = Date.now();

  while (true) {
    // 超时控制
    if (Date.now() - startTime > timeout) {
      console.error('[ComfyUI] 生成超时');
      throw new Error("ComfyUI generation timeout");
    }

    try {
      const res = await axios.get(
        `${COMFY_BASE_URL}/history/${promptId}`,
        { timeout: 5000 }
      );

      const record = res.data[promptId];

      if (record && record.outputs) {
        const result = extractImageUrl(record.outputs);
        if (result) {
          console.log('[ComfyUI] 图片生成成功:', result.imageUrl);
          return result;
        }
      }

    } catch (err) {
      // 轮询过程中的错误通常是因为任务还未完成，继续等待
      if (err.code !== 'ECONNABORTED' && !err.message.includes('404')) {
        console.warn('[ComfyUI] 轮询错误:', err.message);
      }
    }

    await sleep(interval);
  }
}

/**
 * 提取图片 URL
 */
function extractImageUrl(outputs) {
  for (const nodeId in outputs) {
    const node = outputs[nodeId];

    if (node.images && node.images.length > 0) {
      const img = node.images[0];
      const imageUrl = `${COMFY_VIEW_URL}/view?filename=${encodeURIComponent(img.filename)}&subfolder=${encodeURIComponent(img.subfolder || '')}&type=${img.type}`;
      
      return {
        imageUrl: imageUrl,
        filename: img.filename,
        subfolder: img.subfolder || '',
        type: img.type
      };
    }
  }
  return null;
}

/**
 * 检查 ComfyUI 服务是否可用
 */
async function checkAvailability() {
  try {
    await axios.get(`${COMFY_BASE_URL}/queue`, { timeout: 3000 });
    return true;
  } catch (err) {
    return false;
  }
}

/**
 * sleep 工具
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

module.exports = {
  generateImage,
  checkAvailability,
  BASE_WORKFLOW
};