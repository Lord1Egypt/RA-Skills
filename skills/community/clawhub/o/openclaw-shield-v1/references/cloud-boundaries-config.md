# 云服务器边界与配置模板

## 文件系统边界

### 允许读写

- `~/.openclaw/workspace/`
- `~/projects/`
- `/tmp/openclaw-*`

### 允许只读

- `/usr/share/`
- `/etc/hostname`
- `/etc/timezone`
- `/etc/os-release`

### 默认阻断

- `~/.ssh/`, `~/.gnupg/`
- `~/.aws/`, `~/.aliyun/`, `~/.azure/`, `~/.gcloud/`
- `/etc/shadow`, `/etc/sudoers`, `/etc/gshadow`
- `/root/`, `/dev/`, `/proc/*/environ`
- `/var/run/docker.sock`
- `/etc/letsencrypt/*/privkey.pem`
- `/var/log/auth.log`, `/var/log/secure`

## 网络边界

### 默认允许域名

- github.com, api.github.com
- pypi.org, files.pythonhosted.org
- npmjs.com, registry.npmmirror.com
- stackoverflow.com
- hub.docker.com

### 强制阻断

- `169.254.169.254`
- `100.100.100.200`
- `metadata.google.internal`
- `169.254.170.2`

### 其他限制

- 默认阻断内网地址段访问。
- 非 localhost 请求强制 HTTPS。
- 对 DNS 解析后的目标 IP 再做一次内网判定，防 SSRF 绕过。

## 最小配置样例

```yaml
shield:
  version: "2.0"
  security_level: normal

network:
  blocked_addresses:
    - "169.254.169.254"
    - "100.100.100.200"
    - "metadata.google.internal"
    - "169.254.170.2"
  block_internal: true
  require_https: true

filesystem:
  blocked:
    - "~/.ssh/"
    - "~/.aws/"
    - "/etc/shadow"
    - "/var/run/docker.sock"

audit:
  enabled: true
  append_only: true
```
