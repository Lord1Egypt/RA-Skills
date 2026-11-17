# {{TITLE}}

> 创建于 {{DATE}}。这是 Wiki 宪章，也是 Agent 的运行契约。

## 范围

本 Wiki 负责：

- [填写稳定知识范围]

本 Wiki 不负责：

- [填写非目标]

## 受众与成功问题

主要读者：[填写]

本 Wiki 必须能稳定回答：

1. [代表性问题 1]
2. [代表性问题 2]
3. [代表性问题 3]

## 知识契约

- `raw/` 保存不可变来源；只追加，不静默改写。
- `wiki/` 保存可重编译知识；每页必须有 ID、类型、状态、日期、责任人和来源。
- 精确事实必须定位到来源；推断、冲突、过期和未知必须明确标注。
- 查询输出默认保存在 `outputs/queries/`，达到晋升标准后才进入 `wiki/`。

## 页面模型

当前启用的页面类型：[concept / entity / source-summary / how-to / reference / explanation / decision / archive]

命名规则：文件名使用 kebab-case；`id` 是稳定身份，不随标题变化。

## 检索与回答

1. 先读取 `wiki/index.md`。
2. 再使用全文检索并打开命中上下文。
3. 强断言回到 `raw/` 核对。
4. 证据不足时回答未知，不用模型先验补齐。

## 新鲜度与责任

- 默认审查周期：[180 天]
- 高频变化知识：[30 天]
- 默认责任人：[填写]

## 运行命令

```bash
python3 /path/to/llm-wiki-expert/scripts/build_manifest.py . --strict
python3 /path/to/llm-wiki-expert/scripts/audit_wiki.py . --strict
```

## 未决问题

- [需要人类裁决的范围、来源或访问问题]
