# 推广渠道

命令族：`promotion`

用途：营销推广渠道、创建渠道、查询渠道。

执行前必须先运行：

```bash
<CLI> promotion --help
```

help 描述：Manage marketing promotion channels (管理营销推广渠道)

## 直接子命令

- `promotion create`: Batch create promotion channels (批量创建推广渠道)
- `promotion list`: List all promotion channels (列出所有推广渠道)

## 常用命令

```bash
# 查询推广渠道
<CLI> promotion list --channelId <频道ID> -o json

# 批量创建推广渠道。该命令会写入数据，确认后使用 --force。
<CLI> promotion create --channelId <频道ID> --names "渠道1,渠道2" --force -o json
```

## 使用规则

- 需要输出给用户或后续处理时，优先加 `-o json` 或 `--output json`，但必须以 help 是否支持为准。
- 写入、删除、推送、启停、导入、批量处理类子命令必须先确认；命令支持 `--force` 时，只有用户明确授权才使用。
- 参数名、短参数和必填项必须从最深层 `--help` 获取，不要从本文件猜测。
