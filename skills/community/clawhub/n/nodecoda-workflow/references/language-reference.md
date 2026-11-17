# NodeCoda Workflow Language 编程参考

NodeCoda Workflow Language 用程序结构描述工作流意图。NodeCoda Source 是事实源，Workflow Build 为显式 Build Target 生成目标相关 artifact。

**禁止**：阅读 Dify YAML 学习“怎么写 `.ncoda`”，或修改 YAML 来绕过 Source 诊断。

每份完整 Source 必须以语言身份开头：

```nodecoda
@language nodecoda/1
```

---

## 1. 程序模式

```nodecoda
@mode workflow        // 请求-响应模式，return 输出结果
@mode advanced-chat   // 会话模式，自动维护上下文，支持 answer() 和会话变量
```

- `workflow`：单次请求处理，适合无状态任务
- `advanced-chat`：多轮对话，自动携带历史，适合需要上下文的场景

选择依据：
- 需要多轮对话（用户后续追问、调整） → `advanced-chat`
- 需要会话变量（计数器、历史记录、状态累积） → `advanced-chat`
- 需要在循环中多次输出消息 → `advanced-chat`（用 `answer()`）
- 单次请求处理，无状态 → `workflow`

---

## 2. 函数签名

每个程序有一个入口函数 `main`：

```nodecoda
// 无输入
function main() { ... }

// 带输入参数
function main(string query) { ... }

// 带默认值
function main(string query, string language = "中文") { ... }

// 带返回类型
function main(string query) -> string { ... }

// 多参数 + 返回类型
function main(string location, int days = 3, float budget = 5000.0) -> string { ... }
```

**参数类型**：`string`, `int`, `float`, `bool`, `file<类型>`, `string[]`, `int[]`, `float[]`, `bool[]`

**注意**：`string[]`、`map<string, T>` 等复杂类型不能作为 `main` 的输入参数（Build Target 限制）。

---

## 3. 变量声明

```nodecoda
let name = "hello";           // 不可变绑定
var count = 0;                // 可变绑定
const MODEL = "gpt-5.4";      // 构建时常量（用于配置）
```

---

## 4. 核心操作

### 4.1 LLM 调用

```nodecoda
let response = llm(MODEL, {
    "messages": [
        { "role": "system", "content": "你是一个助手" },
        { "role": "user", "content": query }
    ],
    "temperature": 0.7,
    "max_tokens": 2048
});

// 访问结果
response.text    // LLM 输出文本
```

### 4.2 工具调用

```nodecoda
let result = tool("工具名", "操作名", {
    "参数名": "参数值"
});

// 访问结果
result.result    // 工具返回内容
```

工具名和操作名取决于目标平台中配置的工具 Provider。更换 MCP 服务只需在平台重新配置，不改 `.ncoda` Source。

### 4.3 HTTP 请求

```nodecoda
let page = http("GET", "https://api.example.com/data", {
    "headers": { "Content-Type": "application/json" }
});

// 访问结果
page.body           // 响应体
page.status_code    // 状态码
page.headers        // 响应头
```

### 4.4 知识库检索

```nodecoda
let docs = knowledge("dataset-id", query, {});
// 或多个知识库
let docs = knowledge("ds-001,ds-002", query, {});

docs.result    // 检索结果
```

### 4.5 参数抽取（结构化提取）

```nodecoda
type TravelRequest = {
    string city;
    float days;
    bool flexible;
    string[] tags;
}

let extracted = extract<TravelRequest>(MODEL, text, {
    instruction: "提取旅行需求",
    descriptions: {
        city: "目的地城市",
        days: "旅行天数",
        flexible: "日期是否灵活",
        tags: "旅行偏好"
    },
    strategy: "prompt"
});

// 必须检查 ok
if (!extracted.ok) {
    return extracted.reason;
}
// 成功后访问结构化值
extracted.value.city
extracted.value.days
```

**类型限制**：字段只能是 `string`, `float`, `bool`, `string[]`, `float[]`, `bool[]`。

---

## 5. 控制流

### 5.1 条件分支

```nodecoda
if (condition) {
    return "yes";
} else {
    return "no";
}
```

每个分支必须返回值（如果后续代码需要统一结果）。

**可降级条件形态（实证）**：裸 bool 字段（任意深度）、`!expr`、`x.contains("字面量")`、
左侧为 1 级字段/标识符的比较（右侧为字面量），`&&` 可组合；2 级字段（如
`extracted.value.days > 5`）先绑定为局部变量再比较。详见 `gotchas.md` G10。

### 5.2 循环

```nodecoda
// for-each 循环（statement 形式，不收集结果）
for (item in items) {
    let processed = llm(MODEL, { "messages": [{ "role": "user", "content": item }] });
    // 不 yield = 不收集结果
}

// for-each 循环（expression 形式，收集结果）
let results = for (item in items) {
    let processed = foreign code python3(int value = item) -> int {
        source `def main(value: int) -> dict:
    return {"result": value * 2}`;
    };
    yield processed;  // yield 收集每次迭代的结果
};
// results 是 int[] 类型
```

### 5.3 并行执行

```nodecoda
// 无名并行（barrier 同步）
parallel {
    {
        let a = llm(MODEL, { "messages": [...] });
    }
    {
        let b = llm(MODEL, { "messages": [...] });
    }
}
// 所有分支完成后继续

// 命名并行（收集各分支结果）
let results = parallel {
    left: {
        let r = llm(MODEL, { "messages": [...] });
        yield r;
    }
    right: {
        let r = llm(MODEL, { "messages": [...] });
        yield r;
    }
};
// results.left, results.right 访问
```

// 并行 for：并发遍历 + yield 收集（on_error ∈ terminate | keep_null | remove_failed）
let results = parallel for (item in items, concurrency: 3, on_error: remove_failed) {
    let r = llm(MODEL, { "messages": [...] });
    yield r.text;
};
```

---

## 6. Python FFI（外部代码）

调用 Python 代码执行自定义逻辑：

```nodecoda
// 单输出
let doubled = foreign code python3(
    int value = value           // 声明输入类型和绑定
) -> int {                      // 声明输出类型
    source `def main(value: int) -> dict:
    return {"result": value * 2}`;
};
// 直接使用 doubled（不是 doubled.result）

// 多输出（结构体）
let stats = foreign code python3(
    string text = text
) -> {
    count: int;
    normalized: string;
} {
    source `def main(text: str) -> dict:
    words = text.split()
    return {"count": len(words), "normalized": " ".join(words).lower()}`;
};
// stats.count, stats.normalized
```

**规则**：
- 仅支持 `python3`
- 输入输出不支持 `file` 类型
- 声明类型是唯一权威，Python 源码只做一致性验证

---

## 7. 标准库

```nodecoda
// RAG 问答
return std.v1.rag_answer(query, "dataset-id", "openai/gpt-4o");

// HTTP 获取 + LLM 摘要
return std.v1.fetch_and_summarize("https://example.com", "openai/gpt-4o");
```

不需要 import，直接用。配置参数必须是字符串字面量。

---

## 8. 内置函数

以下函数是语言内置的，不需要 import：

| 函数 | 用途 | 示例 |
|---|---|---|
| `split(str, delimiter)` | 分割字符串为数组 | `let items = split(csv, ",");` |
| `filter(array, predicate)` | 过滤数组 | `let ok = filter(items, (x) -> x.contains("a"));` |
| `take(array, n)` | 取前 N 个元素 | `let top = take(items, 10);` |

---

## 9. 输出

### workflow 模式

```nodecoda
return value;                          // 单输出
output("key1", value1);                // 命名多输出
output("key2", value2);
return finalValue;                     // 最终输出
```

### advanced-chat 模式

```nodecoda
return value;        // 等价于 answer(value)
answer(value);       // 显式发送消息（可在循环中多次调用）
```

---

## 10. 会话变量（advanced-chat）

```nodecoda
@mode advanced-chat

@conversation string greeting = "hello";
@conversation int visit_count = 0;
@conversation array<string> history = [];

function main(string user_input) {
    greeting = "welcome";        // 赋值
    visit_count += 1;            // 复合赋值
    history << user_input;       // 追加到数组
    answer(greeting);
}
```

**类型说明**：`array<string>` 和 `string[]` 是同义词，都表示字符串数组。
默认值只能是字面量。

**注意（实证）**：会话变量**不能放进模板串插值**（`answer(\`欢迎,${greeting}\`)` 会报
`LOWERING_INVARIANT`）——直接作 `answer` 参数或条件判断；非会话变量（main 参数、
局部变量）可以插值。详见 `gotchas.md` G11。

---

## 11. 错误处理

### attempt/success/failure

捕获操作的物理执行失败（网络错误、超时等）：

```nodecoda
attempt http("GET", "https://api.example.com") as response {
    success { return response.body; }
    failure(error) { return error.error_message; }
}
```

### with retry

为操作添加重试策略。**注意：不是所有操作都支持 retry。**

```nodecoda
// LLM 调用 — 支持 retry
let response = llm(MODEL, { "messages": [...] }) with retry(max: 3, interval: 1s);

// HTTP 请求 — 支持 retry
let page = http("GET", url, {}) with retry(max: 2, interval: 500ms);

// extract<T>() — 不支持 retry，使用会报 E1045
// let x = extract<T>(...) with retry(...)  ← 错误！
```

> **策略白名单（实证 + 主仓 registry）**：`retry` 支持 `llm`/`http`/`tool`；
> `timeout` 仅 `http`（`llm` 拒绝，报 `OPERATION_POLICY`）；`default` 支持 `llm`/`http`
> （但与 `attempt` 组合会冲突）。完整矩阵见 `gotchas.md` G9。
```

---

## 12. 保留关键字（禁止用作变量名）

`function`, `if`, `else`, `for`, `while`, `in`, `return`, `var`, `let`, `const`,
`output`, `type`, `parallel`, `break`, `continue`, `code`, `foreign`, `source`,
`yield`, `answer`, `limit`, `attempt`, `success`, `failure`, `with`, `retry`,
`timeout`, `default`, `as`, `true`, `false`, `null`, `string`, `int`, `float`,
`bool`, `file`, `void`, `map`, `array`, `any`

---

## 13. 常见模式速查

| 需求 | 模式 | 示例文件 |
|---|---|---|
| 最简 LLM | `main → llm → return` | `examples/01-hello-workflow.ncoda` |
| 带输入的 LLM | `main(params) → llm → return` | `examples/02-with-llm.ncoda` |
| 条件分支 | `if/else → return` | `examples/05-conditional-output.ncoda` |
| Python 计算 | `foreign code python3 → return` | `examples/04-code-node.ncoda` |
| HTTP + LLM | `http → llm → return` | `examples/08-tool-and-http.ncoda` |
| 工具调用 | `tool → llm → return` | `examples/08-tool-and-http.ncoda` |
| 模板字符串 | `` `hello ${name}` `` | — |
| 循环处理 | `for (item in items) { yield }` | `examples/11-loop-transform.ncoda` |
| 并行执行 | `parallel { { a } { b } }` | `examples/03-parallel-branches.ncoda` |
| 多轮对话 | `@mode advanced-chat` | `examples/10-advanced-chat.ncoda` |
| 会话状态 | `@conversation` 变量 | `examples/10-advanced-chat.ncoda` |
| 结构化抽取 | `extract<T>(...)` | `examples/07-structured-extract.ncoda` |
| RAG 问答 | `std.v1.rag_answer(...)` | `examples/09-knowledge-rag.ncoda` |
| HTTP 摘要 | `std.v1.fetch_and_summarize(...)` | `examples/13-fetch-summarize.ncoda` |
| 错误处理 | `attempt { success/failure }` | `examples/06-error-handling.ncoda` |
| 多输出 | `output("key", value)` | `examples/05-conditional-output.ncoda` |
| 列表操作 | `split/filter/take` | `examples/11-loop-transform.ncoda` |

---

## 14. 进一步参考

- Workflow Build 调用与状态：`mcp-contract.md`
- 公共服务与凭据边界：`public-service.md`
- 最小 Source：`source-generation.md`
