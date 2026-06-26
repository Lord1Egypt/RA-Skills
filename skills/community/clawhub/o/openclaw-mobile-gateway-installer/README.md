# ClawHub 发布包：OpenClaw Mobile Gateway Installer

这个目录可直接上传到 ClawHub（选择整个目录上传）。

## 快速发布信息

- Slug: `openclaw-mobile-gateway-installer`
- Display Name: `OpenClaw Mobile Gateway Installer`
- Version: `1.0.0`
- Tags: `openclaw,mobile,gateway,installer,systemd`

## 一键安装

```bash
export OPENCLAW_API_BASE_URL="https://openclaw.example.com"
export OPENCLAW_AUTH_HEADER_NAME="Authorization"
export OPENCLAW_AUTH_HEADER_VALUE="Bearer <your_token>"
bash ./install.sh
```

## 检查服务

```bash
bash ./check.sh
```

如果检查发现 `Cannot GET /api/quick-actions`，说明网关版本偏旧，直接重新执行安装脚本即可完成升级：

```bash
bash ./install.sh
```

## 卸载

```bash
bash ./uninstall.sh
```

## 对 APK 用户

安装成功后，APK 网关地址填写：

- `http://<服务器IP>:4800`
