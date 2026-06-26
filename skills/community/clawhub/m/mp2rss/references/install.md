# 安装与升级

本文档供 Agent 在用户询问「装 mp2rss」「升级 mp2rss」「mp2rss 配置在哪」时按需读取。

## 环境要求

- macOS / Linux / Windows 任一
- Node.js ≥ 18（仅 npm 安装方式需要）
- Go ≥ 1.21（仅从源码构建需要）

## 安装方式

任选其一：

### A. npm（推荐，跨平台一致）

```bash
pnpm add -g @mp2rss/cli
# 或 npm install -g @mp2rss/cli
```

`postinstall` 脚本会按平台自动下载对应的 Go 二进制，绑定为全局 `mp2rss` 命令。

### B. 一键脚本（macOS / Linux）

```bash
curl -fsSL https://raw.githubusercontent.com/areyoubugcoder/mp2rss-cli/main/scripts/install.sh | sh
```

自动选 macOS / Linux 对应平台二进制，安装到 `/usr/local/bin` 或 `~/.local/bin`。

### C. 直接下载 Release 二进制

打开 <https://github.com/areyoubugcoder/mp2rss-cli/releases/latest> 选对应平台的归档下载，解压后把 `mp2rss` 加入 `PATH`。

可用平台：

| OS | amd64 | arm64 |
|----|:---:|:---:|
| macOS | ✅ | ✅ |
| Linux | ✅ | ✅ |
| Windows | ✅ | ✅ |

## 验证安装

```bash
mp2rss --version
```

预期输出版本号字符串（如 `mp2rss v0.x.x`），exit 0。

## 升级

```bash
mp2rss update              # 检查并升级到最新
mp2rss update --check      # 只检查不升级
```

`update` 会从 GitHub Releases 拉最新版二进制就地替换。注意：通过 npm 安装的二进制由 npm 管理，建议改用 `pnpm up -g @mp2rss/cli`。

## 配置文件位置

`~/.mp2rss/config.json`（目录权限 `0700` / 文件权限 `0600`），结构：

```json
{
  "feed_key": "9f3a2c...（64 位 hex）",
  "api_url": "https://mp2rss.bugcode.dev",
  "last_login_at": 1747194198000,
  "last_verify_at": 1747194198000
}
```

- 由 `mp2rss auth login` 自动写入
- `mp2rss auth logout` 只清 `feed_key`，保留 `api_url` 等其它字段
- Agent **不应该**直接读写此文件，统一用 `mp2rss auth ...` 子命令

## Agent 注意事项

- 用户问"装好了吗"→ `mp2rss --version`，exit 0 即装好
- 用户问"配置在哪"→ 答 `~/.mp2rss/config.json` + 强调不要手改，用 `mp2rss auth login` 管理
- 用户问"怎么升级"→ 给 `mp2rss update`；若用户是 npm 装的优先建议 `pnpm up -g @mp2rss/cli`
