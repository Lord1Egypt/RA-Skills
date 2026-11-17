# 按优先级整理上下文

按优先级把选定资料装入明确的字符预算，完整保留片段并列出未纳入项。

## 使用

先提供本功能需要的文件或参数，由助手按 `input.md` 的字段准备请求。辅助脚本只离线处理当前工作区，报告与新文件保存在 `exports/`。需要实时网页、办公账户或实际发布时，另用已有授权工具执行并核对结果。

## 输入示例（虚构数据）

```json
{
  "maxChars": 35,
  "documents": [
    {
      "id": "a",
      "text": "critical",
      "priority": 10
    },
    {
      "id": "b",
      "text": "very long secondary document that will not fit",
      "priority": 1
    }
  ]
}
```

## 验证范围

包内测试验证本地处理、错误输入、路径边界与不覆盖原文件；不表示已完成远程操作、事实核验或视觉检查。具体能力边界以 `input.md` 为准。
