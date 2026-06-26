# 配置说明

## 依赖

`requirements.txt`（根目录）：

```
PyMuPDF>=1.24.0     # 仅渲染 PDF→PNG，不抽内容
Pillow>=10.0.0
openai>=1.30.0      # OpenAI 兼容协议（ARK/Qwen/OpenAI/Ollama 均走这套）
```

安装：

```bash
cd skills/pdf-finance-parser
python3 -m venv .venv
.venv/bin/pip install -r ../../requirements.txt
```

## API Key

至少配置以下一组（按探测顺序）：

| 优先级 | 环境变量组 | Provider |
|--------|------------|----------|
| 1 | `VLM_PROVIDER=ark` + `ARK_API_KEY` | ARK |
| 2（自动）| `ARK_API_KEY` | ARK |
| 3（自动）| `DASHSCOPE_API_KEY` | DashScope |
| 4（自动）| `OPENAI_API_KEY` | OpenAI |

详见 [env.sh.example](../env.sh.example)。

## env.sh 加载顺序

1. CLI `--env-file <path>`（**强制覆盖**已有 env）
2. skill 目录下的 `env.sh`（不覆盖）
3. 当前工作目录下的 `env.sh`（不覆盖）

把 `env.sh.example` 复制为 `env.sh`，填上 key 即可：

```bash
cp env.sh.example env.sh
$EDITOR env.sh
```

## 模型选择

| 场景 | 推荐 |
|------|------|
| 中文金融、A股年报 | `doubao-1.5-vision-pro`（ARK）|
| 中英文混合 / 港股 | `qwen-vl-max`（DashScope）|
| 英文 10-K | `gpt-4o`（OpenAI）|
| 离线 / 私有部署 | `qwen2.5-vl:7b`（Ollama）|

环境变量 `VLM_MODEL=...` 或 CLI `--model ...` 覆盖默认。

## DPI 选择

- `--dpi 150`：速度优先，文字版 PDF 够用
- `--dpi 200`（默认）：平衡
- `--dpi 300`：扫描件 / 印章密集 / 小字号财报附注，建议升高

DPI 上调会增大 base64 图像，可能触及模型上下文上限——超过 300 dpi 前先小样验证。
