# OpenClaw 架构分析报告

**生成时间:** 2026-03-03 22:42:05

**版本:** 2026.2.9

## 📊 概览

- **流水线阶段:** 9
- **钩子点:** 27

## 🔄 流水线阶段

### input_receive

- **文件:** inferred
- **行号:** 0
- **描述:** Inferred stage: input_receive

**可用钩子:**
- `pre`: pre_input_receive
- `post`: post_input_receive
- `replace`: replace_input_receive

### context_gather

- **文件:** inferred
- **行号:** 0
- **描述:** Inferred stage: context_gather

**可用钩子:**
- `pre`: pre_context_gather
- `post`: post_context_gather
- `replace`: replace_context_gather

### memory_retrieve

- **文件:** inferred
- **行号:** 0
- **描述:** Inferred stage: memory_retrieve

**可用钩子:**
- `pre`: pre_memory_retrieve
- `post`: post_memory_retrieve
- `replace`: replace_memory_retrieve

### prompt_assemble

- **文件:** inferred
- **行号:** 0
- **描述:** Inferred stage: prompt_assemble

**可用钩子:**
- `pre`: pre_prompt_assemble
- `post`: post_prompt_assemble
- `replace`: replace_prompt_assemble

### token_check

- **文件:** inferred
- **行号:** 0
- **描述:** Inferred stage: token_check

**可用钩子:**
- `pre`: pre_token_check
- `post`: post_token_check
- `replace`: replace_token_check

### context_compress

- **文件:** inferred
- **行号:** 0
- **描述:** Inferred stage: context_compress

**可用钩子:**
- `pre`: pre_context_compress
- `post`: post_context_compress
- `replace`: replace_context_compress

### llm_submit

- **文件:** inferred
- **行号:** 0
- **描述:** Inferred stage: llm_submit

**可用钩子:**
- `pre`: pre_llm_submit
- `post`: post_llm_submit
- `replace`: replace_llm_submit

### response_process

- **文件:** inferred
- **行号:** 0
- **描述:** Inferred stage: response_process

**可用钩子:**
- `pre`: pre_response_process
- `post`: post_response_process
- `replace`: replace_response_process

### memory_store

- **文件:** inferred
- **行号:** 0
- **描述:** Inferred stage: memory_store

**可用钩子:**
- `pre`: pre_memory_store
- `post`: post_memory_store
- `replace`: replace_memory_store

## 🎣 钩子点详情

| 钩子 | 阶段 | 函数 | 签名 |
|------|------|------|------|
| `pre.input_receive` | input_receive | pre_input_receive | `async pre_input_receive(context, next) => {...}` |
| `post.input_receive` | input_receive | post_input_receive | `async post_input_receive(context, next) => {...}` |
| `replace.input_receive` | input_receive | replace_input_receive | `async replace_input_receive(context, next) => {...}` |
| `pre.context_gather` | context_gather | pre_context_gather | `async pre_context_gather(context, next) => {...}` |
| `post.context_gather` | context_gather | post_context_gather | `async post_context_gather(context, next) => {...}` |
| `replace.context_gather` | context_gather | replace_context_gather | `async replace_context_gather(context, next) => {...}` |
| `pre.memory_retrieve` | memory_retrieve | pre_memory_retrieve | `async pre_memory_retrieve(context, next) => {...}` |
| `post.memory_retrieve` | memory_retrieve | post_memory_retrieve | `async post_memory_retrieve(context, next) => {...}` |
| `replace.memory_retrieve` | memory_retrieve | replace_memory_retrieve | `async replace_memory_retrieve(context, next) => {...}` |
| `pre.prompt_assemble` | prompt_assemble | pre_prompt_assemble | `async pre_prompt_assemble(context, next) => {...}` |
| `post.prompt_assemble` | prompt_assemble | post_prompt_assemble | `async post_prompt_assemble(context, next) => {...}` |
| `replace.prompt_assemble` | prompt_assemble | replace_prompt_assemble | `async replace_prompt_assemble(context, next) => {...}` |
| `pre.token_check` | token_check | pre_token_check | `async pre_token_check(context, next) => {...}` |
| `post.token_check` | token_check | post_token_check | `async post_token_check(context, next) => {...}` |
| `replace.token_check` | token_check | replace_token_check | `async replace_token_check(context, next) => {...}` |
| `pre.context_compress` | context_compress | pre_context_compress | `async pre_context_compress(context, next) => {...}` |
| `post.context_compress` | context_compress | post_context_compress | `async post_context_compress(context, next) => {...}` |
| `replace.context_compress` | context_compress | replace_context_compress | `async replace_context_compress(context, next) => {...}` |
| `pre.llm_submit` | llm_submit | pre_llm_submit | `async pre_llm_submit(context, next) => {...}` |
| `post.llm_submit` | llm_submit | post_llm_submit | `async post_llm_submit(context, next) => {...}` |
| `replace.llm_submit` | llm_submit | replace_llm_submit | `async replace_llm_submit(context, next) => {...}` |
| `pre.response_process` | response_process | pre_response_process | `async pre_response_process(context, next) => {...}` |
| `post.response_process` | response_process | post_response_process | `async post_response_process(context, next) => {...}` |
| `replace.response_process` | response_process | replace_response_process | `async replace_response_process(context, next) => {...}` |
| `pre.memory_store` | memory_store | pre_memory_store | `async pre_memory_store(context, next) => {...}` |
| `post.memory_store` | memory_store | post_memory_store | `async post_memory_store(context, next) => {...}` |
| `replace.memory_store` | memory_store | replace_memory_store | `async replace_memory_store(context, next) => {...}` |

## 💡 使用建议

### 创建自定义钩子

```python
from openclaw_self_analyzer.generators.hook_generator import HookGenerator

generator = HookGenerator()
hook = generator.generate_hook_package(
    hook_name='my_custom_hook',
    hook_type='pre',
    stage='context_gather',
    logic='console.log("Custom logic");'
)
```
