# Halo CLI 认证与 Profile 管理

## 安装与验证

```bash
npm install -g @halo-dev/cli
halo --version
halo --help
```

运行要求：Node.js >= 22

## 登录方式

### Bearer Token（推荐）

在 Halo 后台「个人中心 → 个人令牌」生成 PAT：

```bash
halo auth login \
  --profile local \
  --url http://127.0.0.1:8090 \
  --auth-type bearer \
  --token <your-token>
```

### Basic Auth

需确保 Halo 实例已启用 Basic Auth：

```bash
# Docker 部署时增加启动参数
--halo.security.basic-auth.disabled=false
```

然后登录：

```bash
halo auth login \
  --profile local \
  --url http://127.0.0.1:8090 \
  --auth-type basic \
  --username admin \
  --password <your-password>
```

## Profile 管理

```bash
halo auth current                    # 查看当前生效的 profile
halo auth profile list               # 列出所有已保存的 profile
halo auth profile get local --json   # 查看指定 profile 详情
halo auth profile use production     # 切换默认 profile
halo auth profile delete local --force
halo auth profile doctor             # 诊断凭据问题
```

## 配置存储位置

- 元数据：`~/.config/halo/config.json`
- 凭据：系统 keyring
- 可通过 `HALO_CLI_CONFIG_DIR` 覆盖配置目录
