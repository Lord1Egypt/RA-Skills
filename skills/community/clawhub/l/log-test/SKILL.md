---
name: log-test
description: 按级别筛选日志文件并生成 Markdown 摘要报告
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins: [python]
    # 如果脚本还需要额外安装的工具，用 install 声明安装方式（brew/node/go/uv），
    # 字段格式以 OpenClaw Skill 格式文档为准。
---

# 日志摘要

## 何时使用

当用户要求“分析日志”“提取错误”“生成日志报告”，并且提供了日志文件路径时使用。
用户没有给路径时，先询问路径，不要自行猜测或扫描工作区。

## 怎么做

1. 确认用户给出的日志文件存在。不存在就如实告知，并请用户确认路径。
2. 调用辅助脚本：

   ```powershell
   python {baseDir}/scripts/digest.py --log-file <路径> --level <级别>
   ```

3. 脚本把 Markdown 摘要输出到 stdout。把结果原样交给用户，不要改写统计数字。
4. 用户要求落盘时，写到工作区 `report/` 目录，文件名 `digest-YYYYMMDD.md`。

## 约束

- `level` 只接受 `DEBUG`、`INFO`、`WARN`、`ERROR`，默认 `ERROR`。
- `max-lines` 只接受正整数；不传表示不限制输出条目数。
- 只读取用户明确给出的文件，不遍历工作区之外的位置。
- 不要把日志原文整段贴回给用户，只给统计结果和代表性条目。
- 脚本报错时，把 stderr 原文交给用户，不要自行编造原因。