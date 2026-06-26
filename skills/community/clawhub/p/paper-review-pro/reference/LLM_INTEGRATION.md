# LLM 功能集成

## 概述

Paper Review Pro 支持使用 LLM 自动生成结构化论文摘要和智能查询扩展词，提升检索质量和效率。

## 核心功能

### 1. 结构化摘要生成

**模块**: `scripts/core/summarizer.py`

**输出格式**:
- 研究问题 (Research Question)
- 方法 (Method)
- 结论 (Conclusion)
- 创新点 (Innovation)

**工作流程**:
```
论文数据 (标题 + 摘要) → LLM 生成 → 结构化输出 (4 个字段)
                              ↓
                         Fallback (规则提取)
```

**调用优先级**:
1. OpenClaw Gateway API（优先）
2. Dashscope API（备用）
3. 规则提取 Fallback（保证可用性）

### 2. 查询扩展词生成

**模块**: `scripts/core/expansion.py`

**功能**: 基于 Top-K 论文内容分析，生成语义相关的扩展搜索词，支持领域扩展检索。

**工作流程**:
```
Top-K 论文 + 原始查询 → LLM 分析主题 → 扩展词列表 (含置信度)
```

## 配置

### 配置文件位置
`~/.openclaw/paper-review-pro/config.json`

### 配置示例
```json
{
  "llm": {
    "enabled": true,
    "provider": "gateway",
    "gateway_url": "http://localhost:14940",
    "gateway_model": "dashscope/qwen3.5-plus",
    "dashscope_model": "qwen3.5-plus"
  }
}
```

### 环境变量
```bash
# OpenClaw Gateway 认证（如果需要）
export OPENCLAW_GATEWAY_TOKEN="your-token"

# Dashscope API Key（作为备用）
export DASHSCOPE_API_KEY="your-dashscope-key"
```

## 使用方法

### 启用 LLM（默认）
```bash
python scripts/review.py --query "Knowledge Editing" --n 40 --k 5 --year 2024
```

### 禁用 LLM（仅使用规则 Fallback）
```bash
python scripts/review.py --query "Knowledge Editing" --n 40 --k 5 --year 2024 --no-llm
```

## Fallback 机制

当 LLM 不可用时，系统自动降级到规则模式：

### 摘要 Fallback
- 从原文摘要提取首尾句作为研究问题和结论
- 方法和创新点使用模板文本

### 扩展词 Fallback
- 从论文标题提取名词短语
- 基于原查询生成常见学术扩展模式

**保证**: 即使 LLM 完全不可用，系统也能正常运行，不会报错中断。

## 故障排查

### Gateway 401 错误
```
[Gateway 调用失败]: HTTP Error 401: Unauthorized
```
- **原因**: Gateway 需要认证但未配置 token
- **解决**: 配置 `OPENCLAW_GATEWAY_TOKEN` 或使用 Dashscope

### Dashscope 调用失败
```
[Dashscope 调用失败]: ...
```
- **原因**: 未配置 `DASHSCOPE_API_KEY` 或网络问题
- **解决**: 配置 API Key 或使用 Fallback

### 日志标识
- `[生成摘要]` - 正在调用 LLM 生成摘要
- `[生成扩展词]` - 正在调用 LLM 生成扩展词
- `[使用 Fallback]` - LLM 不可用，降级到规则模式

## API 端点

### OpenClaw Gateway
- URL: `http://localhost:14940/v1/chat/completions`
- 格式：OpenAI 兼容
- 模型：`dashscope/qwen3.5-plus`

### Dashscope（备用）
- URL: `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
- 模型：`qwen3.5-plus`

## 性能优化建议

| 场景 | 建议 |
|------|------|
| 批量处理 | 使用 `--no-llm` 提高速度 |
| 精读模式 | 启用 LLM 获取更好的摘要质量 |
| 探索性检索 | 启用 LLM 获取更智能的扩展词 |

## 扩展开发

如需添加新的 LLM provider，在 `summarizer.py` 和 `expansion.py` 中添加对应的 `_call_xxx_llm()` 函数即可。
