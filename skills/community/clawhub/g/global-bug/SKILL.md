---
name: Bug
description: Bug问题上报技能。当用户说"有xxx问题"、"xxxBug"、"发现xxx问题"时触发，自动将Bug信息添加到企业微信智能表格中。参数映射：问题描述为用户问题，发现问题人员留空，处理进度默认"处理中"，严重程度留空，处理人固定"姜春波"，发现日期留空，解决时间留空。
metadata:
  {
    "openclaw":
      {
        "emoji": "🐛",
        "always": true,
        "requires": { "bins": ["mcporter"] },
        "install":
          [
            {
              "id": "mcporter",
              "kind": "node",
              "package": "mcporter",
              "bins": ["mcporter"],
              "label": "Install mcporter (npm)",
            },
          ],
      },
  }
---

# Bug 问题上报技能

当用户报告问题（如"有xxx问题"、"发现xxxBug"）时，自动将问题添加到企业微信智能表格中。

## Webhook 配置

接口地址：
```
https://qyapi.weixin.qq.com/cgi-bin/wedoc/smartsheet/webhook?key=1jziPisqM429DXY1ZZFTwMInCX86CuIDLQvmOCNSHNYWmGesn1PjC9M9SxzhAkDxzK37s9uRTTSQvwiQ9fOxK0Ajpo5SigZ0EMJPPUiVUf3B
```

字段映射关系：

| 字段名         | 字段ID   | 值来源                                    |
| -------------- | -------- | ----------------------------------------- |
| 问题描述       | `fafLxW` | 用户报告的问题内容                        |
| 发现问题的人员 | `fF5OvO` | 留空                                      |
| 处理进度       | `f9kmWq` | 固定值：`处理中`                         |
| 严重程度       | `f4LSb8` | 留空                                     |
| 处理人         | `f90ViZ` | 固定值：`姜春波`（text 格式）|
| 发现日期       | `frMCUq` | 留空                          |
| 解决时间       | `fsoY1c` | 留空                                     |

## 请求格式

```json
{
  "schema": {
    "fafLxW": "问题描述",
    "fF5OvO": "发现问题的人员",
    "f9kmWq": "处理进度",
    "f4LSb8": "严重程度",
    "f90ViZ": "处理人",
    "frMCUq": "发现日期",
    "fsoY1c": "解决时间"
  },
  "add_records": [
    {
      "values": {
        "fafLxW": "{{问题内容}}",
        "fF5OvO": [],
        "f9kmWq": [{"text": "处理中"}],
        "f4LSb8": [],
        "f90ViZ": [{"text": "姜春波"}],
        "frMCUq": "",
        "fsoY1c": ""
      }
    }
  ]
}
```

## 工作流

1. 当用户说"有xxx问题"时，提取问题内容
2. 按照上述格式构造请求 JSON（发现问题的人员、发现日期、解决时间都留空）
3. 发送 POST 请求到 Webhook 地址
4. 返回操作结果给用户

## 示例

用户输入："有登录页面点击按钮无响应问题"

```json
{
  "schema": {
    "fafLxW": "问题描述",
    "fF5OvO": "发现问题的人员",
    "f9kmWq": "处理进度",
    "f4LSb8": "严重程度",
    "f90ViZ": "处理人",
    "frMCUq": "发现日期",
    "fsoY1c": "解决时间"
  },
  "add_records": [
    {
      "values": {
        "fafLxW": "登录页面点击按钮无响应问题",
        "fF5OvO": [],
        "f9kmWq": [{"text": "处理中"}],
        "f4LSb8": [],
        "f90ViZ": [{"text": "姜春波"}],
        "frMCUq": "",
        "fsoY1c": ""
      }
    }
  ]
}
```

## 响应格式

请求成功后，返回格式如下：

```
✅ 问题已成功上报，会尽快处理

问题描述：xxx
处理进度：处理中
处理人：姜春波

已添加到企业微信智能表格中。
```

不显示 `记录ID` 和 `发现人` 信息。

## 错误处理

- 如果请求成功（返回 errcode=0），按上述格式回复
- 如果请求失败，返回具体错误信息给用户
