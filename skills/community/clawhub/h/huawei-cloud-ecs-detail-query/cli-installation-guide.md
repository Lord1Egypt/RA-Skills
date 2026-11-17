# hcloud CLI 安装与认证指南

## 安装 hcloud CLI

### Linux / macOS

```bash
curl -O https://cn-huaweicloud.obs.cn-north-1.myhuaweicloud.com/cli/latest/hcloud_install.sh
bash hcloud_install.sh -y
```

### Windows

下载安装包：https://cn-huaweicloud.obs.cn-north-1.myhuaweicloud.com/cli/latest/hcloud_windows.zip

### 验证安装

```bash
hcloud version
```

## 配置认证

### 方式一：AK/SK 模式（推荐）

```bash
hcloud configure set \
  --cli-region=cn-north-4 \
  --access-key=YOUR_ACCESS_KEY \
  --secret-key=YOUR_SECRET_KEY
```

### 方式二：环境变量

```bash
export HUAWEICLOUD_SDK_AK=YOUR_ACCESS_KEY
export HUAWEICLOUD_SDK_SK=YOUR_SECRET_KEY
```

## 验证配置

```bash
hcloud ECS ListServersDetails --cli-region=cn-north-4 --limit=1
```

## 参考

- [KooCLI 官方文档](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
