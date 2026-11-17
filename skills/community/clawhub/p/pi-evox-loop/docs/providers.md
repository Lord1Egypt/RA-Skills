# Provider 配置

> **EN**: LLM provider configuration for flow C: any OpenAI-compatible endpoint; `$ENV` interpolation needs pi >= 0.85.1; domestic endpoints listed (DeepSeek/Bailian/SiliconFlow/Zhipu).示例（含国内可用端点）

> SKILL.md 保留精简指引；本页为完整示例。

Pi 支持任意 OpenAI 兼容端点。以 `~/.pi/agent/models.json` 为例：

```json
{
  "providers": {
    "my-provider": {
      "baseUrl": "https://<你的端点>/v1",
      "apiKey": "$MY_API_KEY",
      "models": ["<model-id>"]
    }
  }
}
```

- **国内 OpenAI 兼容端点**（按其文档填 baseUrl 与模型名）：DeepSeek（`https://api.deepseek.com/v1`）、阿里云百炼、硅基流动、智谱等；
- **内置 provider 示例**（deepseek 已内置，无需 models.json）：

```bash
node code/pi_evolve.mjs <模板目录> <任务文本> \
    --provider deepseek --model deepseek-v4-flash \
    --api-key "$DEEPSEEK_API_KEY" --rounds 2 --fresh --auto-approve
```

- **npm 国内镜像**（安装慢时）：`npm config set registry https://registry.npmmirror.com`

## `$ENV` 插值版本差异（FAQ Q2 详版）

- pi **0.85.1 起支持** `$ENV` 插值（实测确认，上游 issue #9258 已闭环该项）；
- **0.74.2 及更早版本不支持**：`apiKey` 字段的 `$VAR` 会被当作字面字符串发送 → 401；
- 旧版本解决方案：`--api-key "$MY_KEY"` 显式传（编排器 0.7.0 起以 argv 直传该值给 pi 子进程）。
