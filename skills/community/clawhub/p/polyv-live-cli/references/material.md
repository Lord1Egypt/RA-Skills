# 素材库

命令族：`material`

用途：素材列表、素材删除、素材分类、素材标签。

执行前必须先运行：

```bash
<CLI> material --help
```

help 描述：Manage material library

## 直接子命令

- `material category`: Material category APIs
- `material delete`: Delete materials
- `material label`: Material label APIs
- `material list`: List materials

## 使用规则

- 需要输出给用户或后续处理时，优先加 `-o json` 或 `--output json`，但必须以 help 是否支持为准。
- 写入、删除、推送、启停、导入、批量处理类子命令必须先确认；命令支持 `--force` 时，只有用户明确授权才使用。
- 参数名、短参数和必填项必须从最深层 `--help` 获取，不要从本文件猜测。
