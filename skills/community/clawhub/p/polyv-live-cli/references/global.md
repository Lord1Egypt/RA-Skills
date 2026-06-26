# 全局账号设置

命令族：`global`

用途：全局鉴权、全局页面设置、账号级默认配置。

执行前必须先运行：

```bash
<CLI> global --help
```

help 描述：Manage global account settings

## 直接子命令

- `global auth`: Global auth settings
- `global page-setting`: Global page settings

## 使用规则

- 需要输出给用户或后续处理时，优先加 `-o json` 或 `--output json`，但必须以 help 是否支持为准。
- 写入、删除、推送、启停、导入、批量处理类子命令必须先确认；命令支持 `--force` 时，只有用户明确授权才使用。
- 参数名、短参数和必填项必须从最深层 `--help` 获取，不要从本文件猜测。
