---
name: kimi-search
description: 使用 Moonshot Kimi API 的 $web_search 内置工具进行联网搜索。当需要进行网络搜索获取实时信息时使用，支持中文和英文搜索查询。需要配置 MOONSHOT_API_KEY。
metadata: { "openclaw": { "primaryEnv": "MOONSHOT_API_KEY", "requires": { "env": ["MOONSHOT_API_KEY"] } } }
---

# Kimi Search

使用 Kimi 大模型的内置联网搜索工具 `$web_search` 进行联网搜索。

## 前置要求

1. **Moonshot API Key**：需要在 https://platform.moonshot.cn/console 注册并获取 API Key
2. **账户充值**：联网搜索每次额外收费约 ¥0.03，确保账户有余额
3. **Python 环境**：Python 3.8+ 和 `openai` Python 包

## 安装依赖

skill 需要 `openai` Python 包。安装方式：

```bash
pip3 install openai
```

或者使用虚拟环境（推荐）：

```bash
python3 -m venv ~/.openclaw/skills/kimi-search/venv
source ~/.openclaw/skills/kimi-search/venv/bin/activate
pip install openai
```

## 配置 API Key

### 工作原理

本 skill 声明了 `primaryEnv: MOONSHOT_API_KEY`。OpenClaw 会自动将你配置的 `apiKey` 值注入到 `MOONSHOT_API_KEY` 环境变量中供脚本读取。

### 配置方式（推荐）

编辑 `~/.openclaw/openclaw.json`，添加：

```json
{
  "skills": {
    "entries": {
      "kimi-search": {
        "enabled": true,
        "apiKey": "sk-你的APIKey"
      }
    }
  }
}
```

> **安全提示**：`~/.openclaw/openclaw.json` 是用户主目录下的配置文件，权限通常设置为仅用户可读。如需更高安全性，建议使用环境变量方式。

### 使配置生效

```bash
openclaw gateway restart
```

### 替代方案：环境变量

如果你不想将 Key 存储在配置文件中，可以直接设置环境变量：

```bash
export MOONSHOT_API_KEY="sk-你的APIKey"
~/.openclaw/skills/kimi-search/scripts/kimi-search "搜索词"
```

环境变量方式不会在磁盘上留下 Key 记录，适合共享机器或高安全要求场景。

## 使用方法

### 作为 Agent 工具使用

配置完成后，可以直接问 Agent：

> "用 kimi-search 搜一下今天的新闻"

### 直接调用脚本

```bash
~/.openclaw/skills/kimi-search/scripts/kimi-search "搜索关键词"
```

### 示例

```bash
kimi-search "今天有什么新闻"
kimi-search "OpenClaw 是什么"
kimi-search "Python 最新版本特性"
```

## 输出格式

脚本返回 JSON 格式：

```json
{
  "query": "搜索关键词",
  "answer": "搜索结果的回答",
  "usage": {
    "prompt_tokens": 8059,
    "completion_tokens": 1197,
    "total_tokens": 9256
  }
}
```

- `query`：原始搜索词
- `answer`：Kimi 根据搜索结果生成的回答
- `usage`：Token 消耗统计（搜索内容会计入 prompt_tokens）

## 故障排除

### 错误："缺少 MOONSHOT_API_KEY"

**原因**：API Key 未正确配置或未注入环境变量  
**解决**：
1. 检查 `~/.openclaw/openclaw.json` 中 `skills.entries.kimi-search.apiKey` 是否填写
2. 重启 Gateway：`openclaw gateway restart`
3. 或使用环境变量方式运行

### 错误："Invalid Authentication" 或 401

**原因**：API Key 无效或已过期  
**解决**：
1. 在 Moonshot 控制台检查 Key 状态
2. 重新生成 Key 并更新配置

### 错误："insufficient_quota" 或余额不足

**原因**：账户余额不足  
**解决**：在 https://platform.moonshot.cn/console 充值

### 错误："ModuleNotFoundError: No module named 'openai'"

**原因**：缺少 Python 依赖  
**解决**：运行 `pip3 install openai`

## 技术说明

- **模型**：`kimi-k2.5`（256k 上下文窗口）
- **工具**：`$web_search` 内置函数（`builtin_function` 类型）
- **工作原理**：
  1. 脚本声明 `$web_search` 工具给 Kimi API
  2. Kimi 决定需要搜索时，返回 tool_call 请求
  3. 脚本将 tool_call 参数原样返回（这是 `$web_search` 的正确用法，Kimi 会在服务端执行实际搜索）
  4. Kimi 返回包含搜索结果的最终回答
- **参数**：`temperature=0.6`，禁用 `thinking` 模式以支持 tool calls
- **费用**：
  - 模型调用：按 token 计费（输入 ¥4/1M，输出 ¥21/1M）
  - 搜索功能：每次搜索额外 ¥0.03
- **性能**：搜索结果通常占用 5k-10k tokens，建议用于需要实时信息的场景

## 安全建议

1. **API Key 保护**：不要将 Key 提交到 Git 仓库或分享给他人
2. **配置文件权限**：确保 `~/.openclaw/openclaw.json` 权限为 `600`（仅所有者可读写）
3. **临时环境变量**：在脚本中使用 `export` 设置的变量只在当前 shell 会话有效
4. **定期轮换**：定期在 Moonshot 控制台重新生成 API Key

## 参考

- [Moonshot 开放平台](https://platform.moonshot.cn)
- [Kimi 联网搜索文档](https://platform.moonshot.cn/docs/guide/use-web-search)
- [模型定价](https://platform.moonshot.cn/docs/pricing/chat)
