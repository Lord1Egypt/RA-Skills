---
name: gpt-review
description: 用 ChatGPT 审稿的自动化工具。通过 CDP 控制 Brave Browser 中的 ChatGPT，自动发送审稿 prompt、等待回复、提取完整响应。Use when: (1) 需要用 ChatGPT 作为次审模型审查稿件 (2) 需要获取 ChatGPT 对文章的事实核查、逻辑检查、AI痕迹检测意见 (3) 多模型互补审稿流程中需要 ChatGPT 的独立意见 (4) 用户提到"GPT审稿""ChatGPT审查""次审"。Requires: Brave Browser running with --remote-debugging-port=9222, ChatGPT logged in.
---

# GPT 审稿工具

通过 CDP 控制 ChatGPT 进行自动化审稿，用于多模型互补审稿流程。

## 工作流程

1. 构造审稿 prompt（文章内容 + 审稿要求）
2. 运行 `scripts/gpt_review.py` 自动发送给 ChatGPT
3. 等待 ChatGPT 回复并提取完整内容
4. 保存回复到文件
5. 与笔探主审意见交叉比对

## 使用方法

```bash
# 从文件读取 prompt，输出到文件
python3 scripts/gpt_review.py \
  --prompt-file /tmp/prompt.txt \
  --output /tmp/gpt_response.md \
  --timeout 120

# 直接传 prompt 字符串
python3 scripts/gpt_review.py \
  --prompt "请审查以下文章..." \
  --output /tmp/gpt_response.md

# 保留 ChatGPT 标签页不关闭（方便回看）
python3 scripts/gpt_review.py \
  --prompt-file /tmp/prompt.txt \
  --output /tmp/gpt_response.md \
  --keep-tab
```

### Prompt 构造建议

审稿 prompt 应包含以下全部维度（见 `references/prompt-template.md` 完整模板）：

1. **事实正确性**（最优先）— 数字精确性、技术概念准确性、因果推断、绝对化表述、记忆模糊风险、应然vs实然
2. **逐句读者反应** — 模拟每句话的观众脑内弹幕（🎯钩住/😐平/😴走神/❓疑惑/💡顿悟/🔥共鸣/🤔质疑/⚡雷点）
3. **整篇"听众带走什么"** — 一句话带走、认知框架、未解疑惑、离场情绪、行动转化
4. **传播力 + 平台适配** — 开头30秒钩子、金句潜力、走神风险段
5. **反AI味检测** — 过度工整排比、虚假完美收束、整齐因果链、"太完美"检查

### 标准化 prompt 模板

使用 `references/prompt-template.md` 中的模板构造 prompt。模板覆盖了以上所有维度，只需填入文章内容即可。

#### 生成 prompt 的命令

```bash
python3 scripts/build_prompt.py \
  --article /path/to/article.md \
  --output /tmp/gpt_prompt.txt \
  [--context "播客/B站/文章"] \
  [--dimensions all]
```

如果脚本不存在，也可以手动替换模板中的 `{{ARTICLE}}` 占位符。

### 前置条件

- Brave Browser 运行中且开启 `--remote-debugging-port=9222`
- ChatGPT 已登录（chatgpt.com）
- `websockets` Python 包已安装（`pip3 install websockets`）
- `cdp_exec.py` 在以下位置之一可被自动检测到：
  - `skills/brave-browser-agent/scripts/cdp_exec.py`
  - `~/.agents/skills/brave-browser-agent/scripts/cdp_exec.py`
  - 或通过 `--cdp-script` 手动指定

## 多模型互补策略

笔探（GLM）主审 + ChatGPT 次审，独立审稿再交叉比对：

| 审稿维度 | 笔探负责 | ChatGPT 负责 |
|---------|---------|-------------|
| 文风一致性 | ✅ | |
| 结构习惯 | ✅ | |
| 雷点检查 | ✅ | |
| 事实核查 | ✅ 辅助 | ✅ 主力 |
| 技术准确性 | | ✅ |
| 逻辑完整性 | | ✅ |
| AI痕迹检测 | | ✅ |
| 太完美检查 | ✅ | ✅ |
| **逐句读者反应** | ✅ 主力（human-reader-sim） | ✅ 辅助（见 prompt 维度二） |
| **整篇"听众带走什么"** | ✅ 主力（podcast-review-analyst Step 2.5） | ✅ 辅助（见 prompt 维度三） |

### 交叉比对规则

- 两个模型都指出 → 📌 硬伤（高优先级）
- 只有一个指出 → ⚠️ 需人工判断，标注来源
- ChatGPT 偏好"标准写法"的建议需要过滤，可能与用户的口语化风格冲突
- ChatGPT 可能多次建议删掉用户的固定格式——这些要过滤掉

## 踩坑记录

参见 `references/gotchas.md`（含 CDP 405 错误、ProseMirror 注入、长响应截断等解决方案）。
