---
name: paper2poster
description: 将学术论文 PDF 自动转换为 PowerPoint 海报（PPTX）和 HTML 文件。支持 UniAPI、MiniMax 等 OpenAI 兼容 API。
---

# Paper2Poster 学术海报生成器

## 技能说明

技能将从 GitHub 仓库获取代码。用户只需提供论文 PDF 和自己的 API Key，AI 将自动完成环境检查、依赖安装、配置和海报生成。

## 触发条件

用户说："帮我生成海报"、"把这篇论文转成海报"、"生成学术海报"并提供论文 PDF 路径。

## 执行步骤

当用户触发此技能时，请严格按以下顺序自动执行：

### 第一步：克隆项目仓库

检查当前目录是否存在 `PosterAgent/` 文件夹，如果不存在，则执行：

```bash
git clone https://github.com/caoxinran102-sys/Paper2Poster.git .
```

> **注意**：命令末尾的 `.` 表示克隆到当前目录，不要创建额外的子文件夹。

### 第二步：验证项目目录

克隆完成后，确保当前目录即为项目根目录（包含 `PosterAgent/` 文件夹）：

```bash
if [ ! -d "PosterAgent" ]; then
    echo "错误：未找到 PosterAgent 目录，克隆可能失败"
    exit 1
fi
```

### 第三步：检查 Python 环境

```bash
if ! command -v conda &> /dev/null; then
    echo "⚠️ Conda 未安装，请先安装 Miniconda"
    exit 1
fi

conda env list | grep -q poster_env || conda create -n poster_env python=3.10 -y
eval "$(conda shell.bash hook)"
conda activate poster_env
```

### 第四步：安装依赖

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

如果遇到 docling-parse 相关错误（ModuleNotFoundError），执行降级：

```bash
pip uninstall docling-parse docling -y
pip install docling-parse==2.1.0 docling==2.6.0
```

### 第五步：配置 API 密钥

检查当前目录下是否有 .env 文件。如果没有，询问用户提供：

- `OPENAI_API_KEY`（例如 UniAPI 的 sk-xxx 或 MiniMax 的 sk-xxx）
- `OPENAI_BASE_URL`（例如 https://hk.uniapi.io/v1 或 https://api.minimaxi.com/v1）

创建 .env 文件并写入：

```bash
cat > .env << EOF
OPENAI_API_KEY=用户提供的值
OPENAI_BASE_URL=用户提供的值
WORKSPACE_DIR=${WORKSPACE_DIR:-./workspace}
EOF
```

### 第六步：准备论文文件

- 要求用户提供论文 PDF 的完整路径（例如 `/home/user/paper.pdf`）
- 如果用户有机构 Logo，也要求提供路径（可选）
- 无需创建特定目录，直接使用用户提供的路径。

### 第七步：运行海报生成

执行以下命令（替换 `{论文路径}` 和 `{Logo路径}`）：

```bash
python -m PosterAgent.new_pipeline \
  --poster_path="{论文路径}" \
  --model_name_t="claude-sonnet-4-20250514" \
  --model_name_v="claude-sonnet-4-20250514" \
  --institution_logo_path="{Logo路径}" \
  --max_workers=1
```

> **提示**：如果用户没有 Logo，省略 `--institution_logo_path` 参数。

### 第八步：异常处理与重试

| 错误类型 | 处理策略 | 重试行为 |
|---------|---------|---------|
| 429 或 529 错误 | 速率限制，等待后重试 | 延迟加倍（初始 60 秒） |
| 400 格式错误 | 切换备用模型后重试 | 立即重试 |
| 超时错误 | 等待后重试 | 延迟 30 秒 |

**重试逻辑示例**（AI 应自行实现）：

1. 设置最大重试次数为 **3**
2. 初始延迟设为 **60 秒**
3. 每次重试失败后，延迟时间 **加倍**
4. 如果返回 429 或 529，按上述延迟策略重试
5. 如果返回 400 格式错误，切换备用模型后立即重试
6. 如果超时，等待 30 秒后重试

---

## 输出结果

✅ **海报生成完成！**

📁 **输出文件位置**：
- PPTX: `./generated_posters/.../xxx.pptx`
- HTML: `./generated_posters/.../xxx.html`

📋 **处理摘要**：
- 论文: {文件名}
- 状态: 成功
