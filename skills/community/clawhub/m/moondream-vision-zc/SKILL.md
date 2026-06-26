# SKILL.md - Moondream Vision

**name**: moondream-vision-zc
**description**: 使用本地 Ollama 部署的 Moondream 模型进行图像理解，并将结果返回给 OpenClaw。该 Skill 适配 OpenClaw 2026 版本的多模态插件机制，可在聊天中直接发送图片或引用本地文件路径。
**type**: command

## 环境准备
1. **确保 Ollama 已安装**
   - Windows：`winget install ollama` 或从 https://ollama.com/download 下载并安装。
   - 安装完成后，在 PowerShell 中运行 `ollama serve`，确保后台服务在 11434 端口监听。
2. **拉取 Moondream 模型**（如果尚未本地缓存）
   ```powershell
   ollama pull moondream
   ```
   - 若已有本地模型，可跳过此步骤。
3. **验证模型**
   ```powershell
   ollama run moondream "一张猫的图片"
   ```
   - 返回文字描述即表示模型工作正常。
4. **安装 Python 依赖**（仅在使用脚本时需要）
   ```powershell
   pip install requests
   ```
   - 脚本通过 HTTP 调用 Ollama API。

## Skill 实现
### 目录结构
```
~/.openclaw/skills/moondream-vision/
├─ SKILL.md          # 本文件
└─ scripts/
   └─ moondream_vision.py
```

### scripts/moondream_vision.py
```python
import sys, json, base64, requests, pathlib

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

def encode_image(path: str) -> str:
    data = pathlib.Path(path).read_bytes()
    return base64.b64encode(data).decode("utf-8")

def run_moondream(image_path: str, prompt: str = ""):
    img_b64 = encode_image(image_path)
    payload = {
        "model": "moondream",
        "prompt": prompt,
        "images": [img_b64],
        "stream": False,
    }
    resp = requests.post(OLLAMA_URL, json=payload)
    resp.raise_for_status()
    result = resp.json()
    # Ollama returns a stream of tokens; when stream=False we get full response in ``response``
    return result.get("response", "")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: python moondream_vision.py <image_path> [prompt]\n")
        sys.exit(1)
    image = sys.argv[1]
    user_prompt = sys.argv[2] if len(sys.argv) > 2 else ""
    print(run_moondream(image, user_prompt))
```

### 在 OpenClaw 中注册命令
在 `~/.openclaw/config/skills.json`（若不存在请创建）添加如下条目：
```json
{
  "name": "moondream-vision",
  "command": "python ${skill_dir}/scripts/moondream_vision.py",
  "description": "本地 Moondream 图像理解",
  "usage": "!moondream <image_path> [prompt]",
  "args": ["image_path", "prompt?"],
  "output": "text"
}
```
- `${skill_dir}` 为此 skill 所在目录的绝对路径，OpenClaw 会在运行时自动替换。
- 通过 `!moondream D:\images\cat.jpg` 在聊天中调用。

## 多模态接入方案说明
- **模型**：Moondream 是轻量级的视觉语言模型，适合本地推理。它通过 Ollama 的 REST API 接收 base64 编码的图像和可选文字提示，返回自然语言描述。
- **与 GPT‑OSS‑120B 结合**：
  - 在需要更深层次的推理时，可将 Moondream 的输出作为 **系统提示** 传递给 GPT‑OSS‑120B，让后者进行复杂的分析、摘要或跨模态推理。
  - 示例工作流：
    1. `!moondream img.png` ➜ 获得图片描述 `desc`。
    2. 调用 `!gpt "基于以下描述，写一段新闻稿：\n${desc}"`。
- **性能**：Moondream 推理在普通笔记本 CPU 上约 1‑2 秒/图像，GPU 可进一步加速。GPT‑OSS‑120B 仍通过 OpenClaw 统一调度，保持统一日志与审计。

## 常见问题 & 调试
- **Ollama 未启动**：确保 `ollama serve` 正在运行，检查防火墙是否阻止 11434 端口。
- **图片过大**：Ollama 限制单张图片约 5 MB，建议在本地压缩后再发送。
- **返回空**：确认 `prompt` 参数非空，或在 `payload` 中加入 `"system": ""` 防止模型误判。

## 使用示例
```
用户：!moondream C:\Users\Administrator\Pictures\dog.jpg
Assistant: 这是一只棕色的狗，正坐在草地上，注视着镜头。

用户：!moondream C:\Users\Administrator\Pictures\dog.jpg "请把这张图的内容写成一段简短的广告文案"
Assistant: 「爱犬的欢笑，尽在自然」——让您的宠物在绿意盎然的草地上自由奔跑，感受生活的活力。
```

---
*如有其他需求可进一步扩展，如批量处理、返回 JSON 结构等。*