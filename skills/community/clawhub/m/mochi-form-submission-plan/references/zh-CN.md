# 表单填写与提交核对

根据实际表单字段检查必填项、未知字段和敏感项，先核对再提交。

## 使用

先提供本功能需要的文件或参数，由助手按 `input.md` 的字段准备请求。辅助脚本只离线处理当前工作区，报告与新文件保存在 `exports/`。需要实时网页、办公账户或实际发布时，另用已有授权工具执行并核对结果。

## 输入示例（虚构数据）

```json
{
  "fields": [
    {
      "name": "email",
      "required": true
    },
    {
      "name": "message",
      "required": true
    }
  ],
  "values": {
    "email": "demo@example.com",
    "message": "Fictional inquiry"
  }
}
```

## 验证范围

包内测试验证本地处理、错误输入、路径边界与不覆盖原文件；不表示已完成远程操作、事实核验或视觉检查。具体能力边界以 `input.md` 为准。
