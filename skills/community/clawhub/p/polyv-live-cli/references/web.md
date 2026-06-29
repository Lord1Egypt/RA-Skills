# 观看页配置

命令族：`web`

用途：观看页基础信息、菜单、分享、通用设置、观看页鉴权、观看页打赏，以及账号级通用图片资源上传。

执行前必须先运行：

```bash
<CLI> web --help
```

help 描述：Manage watch page configuration

## 直接子命令

- `web auth`: Watch condition and authorization APIs
- `web donate`: Watch page donate APIs
- `web image-upload`: Upload common image assets
- `web info`: Watch page basic info
- `web menu`: Watch page menu APIs
- `web setting`: Watch page common settings
- `web share`: Watch page share APIs

## 通用图片上传

`web image-upload` 对应 `/live/v3/common/upload-image`，用于上传频道封面、直播引导图、播放器 logo、管理员/助教头像、授权二维码、暖场图、广告图、打赏图标、邀请卡、菜单图片等通用图片资源。旧入口 `web setting image-upload` 仅作为兼容别名保留，新任务优先使用 `web image-upload`。

```bash
<CLI> web image-upload --type logoImage --files /path/to/logo.png --force -o json
```

## 使用规则

- 需要输出给用户或后续处理时，优先加 `-o json` 或 `--output json`，但必须以 help 是否支持为准。
- 写入、删除、推送、启停、导入、批量处理类子命令必须先确认；命令支持 `--force` 时，只有用户明确授权才使用。
- 参数名、短参数和必填项必须从最深层 `--help` 获取，不要从本文件猜测。
