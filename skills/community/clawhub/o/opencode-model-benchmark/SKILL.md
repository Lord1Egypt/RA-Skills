---
name: opencode-model-benchmark
description: |
  OpenCode Zen 免费模型基准测试工具。
  当用户想测试 OpenCode Zen 平台上免费模型的性能（响应时间、tokens/s、生成速度）时使用此 Skill。
  触发词：模型测试、性能测试、基准测试、benchmark、测速、tokens/s、吞吐量、opencode 测试、免费模型速度比较。
  该 Skill 会自动测试所有可用的免费模型，并生成结构化 Markdown 测试报告。
---

# OpenCode Zen 免费模型基准测试

## 概述

对 OpenCode Zen 平台 (https://opencode.ai/zen/v1) 上的所有免费模型进行性能基准测试：
- 测量每个模型的**响应时间**（秒）
- 测量每个模型的**生成速度**（tokens/s）
- 统计 prompt tokens / completion tokens
- **直接在对话窗口输出 Markdown 测试报告**（按 tokens/s 排名），不生成文件

**无需 API Key**，直接调用 `https://opencode.ai/zen/v1`。

---

## 使用方式

### 标准用法（报告直接输出到对话窗口）

```bash
python3 ~/.workbuddy/skills/opencode-model-benchmark/scripts/benchmark.py
```

脚本会：
1. **自动获取**最新免费模型清单（从 OpenCode 官方文档）
2. 依次测试列表中的每个模型
3. 每个模型发送一个标准测试 Prompt
4. 记录响应时间、token 用量和生成速度
5. **将完整 Markdown 报告直接输出到 stdout**，在对话窗口展示
6. 在终端打印快速汇总

---

## 工作流程

1. **运行测试脚本**：
   ```bash
   python3 ~/.workbuddy/skills/opencode-model-benchmark/scripts/benchmark.py
   ```
2. **自动获取模型**：脚本启动时从官方文档爬取最新免费模型清单（约 1-2 秒）
3. **等待测试完成**：测试约需 1–3 分钟（视网络情况和模型响应）
4. **展示报告**：测试完成后，**将脚本 stdout 输出的完整 Markdown 报告直接呈现在对话窗口中**，无需生成文件或调用 open_result_view

---

## 免费模型获取

脚本启动时**自动从 OpenCode 官方文档** (`https://opencode.ai/docs/zh-cn/zen`) 爬取最新免费模型清单：

- ✅ **实时获取**：每次运行自动拉取最新列表
- ✅ **智能过滤**：文档中已下架的模型会标记为 ❌ 失败
- ✅ **完全独立**：不依赖任何外部 skill 或手动维护

> 模型清单由内置 `_KNOWN_MODELS` 定义 + 在线验证机制保证最新。

---

## 配置参数（脚本顶部）

| 参数 | 默认值 | 说明 |
|:-----|:-------|:-----|
| `BASE_URL` | `https://opencode.ai/zen/v1` | API 基础地址 |
| `TIMEOUT` | `60` 秒 | 单次请求超时 |
| `TEST_PROMPT` | 数数 1–20 | 标准测试提示词 |

---

## 注意事项

- 部分免费模型为**限时免费**，如测试返回 HTTP 402/403，说明该模型已停止免费服务
- 测试结果受**网络波动**影响，可多次运行取平均值
- `gpt-5-nano` 使用 `/responses` 端点，与其他模型不同
- 测试间有 1 秒间隔，防止触发频率限制
