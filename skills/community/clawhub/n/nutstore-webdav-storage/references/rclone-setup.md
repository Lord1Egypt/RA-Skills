# rclone 配置坚果云 WebDAV

## 前提
- 已安装 `rclone`
- 已有坚果云 WebDAV 用户名与应用密码
- WebDAV URL：`https://dav.jianguoyun.com/dav/`

## 交互式配置

```bash
rclone config
```

建议填写：
- `n` → 新建 remote
- name: `nutstore`
- Storage: `webdav`
- url: `https://dav.jianguoyun.com/dav/`
- vendor: `other`
- user: 你的坚果云用户名
- pass: 你的坚果云应用密码

## 验证

```bash
rclone lsd nutstore:
rclone mkdir nutstore:/openclaw-backup
```

## 非交互式配置示例

```bash
rclone config create nutstore webdav \
  url https://dav.jianguoyun.com/dav/ \
  vendor other \
  user "$NUTSTORE_USER" \
  pass "$NUTSTORE_PASS"
```

说明：
- `NUTSTORE_PASS` 建议使用 `rclone config` 交互录入，避免明文残留在 shell history
- 若必须自动化注入，优先使用临时环境变量，不要写入仓库文件
