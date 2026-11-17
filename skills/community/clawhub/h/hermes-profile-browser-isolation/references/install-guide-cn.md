# 安装（3 步 · 给人看的）

## 1. 装依赖
```bash
pip install psutil
```

## 2. 放进 Hermes
把整个 `hermes-profile-browser-isolation` 文件夹复制到 skills 的 `devops` 子目录：

| 系统 | 路径 |
|---|---|
| Windows | `%LOCALAPPDATA%\hermes\skills\devops\` |
| macOS | `~/Library/Application Support/hermes/skills/devops/` |
| Linux | `~/.local/share/hermes/skills/devops/` |

（没有 `devops` 目录就新建；文件夹名保持 `hermes-profile-browser-isolation`）

## 3. 跑起来
```bash
cd <skill目录>/scripts
python hermes_browser_provision.py discover   # 先看方案，不动任何东西
python hermes_browser_provision.py apply      # 落地（自动备份 config）
python hermes_browser_audit.py                # 验收：可见窗口必须 = 0
```

## 能解决什么
- 多个 AI 成员/多个 profile 同时干活时**不再抢你的浏览器、不再弹窗抢焦点**
- 每个成员**各自保存登录态**（不用每次重新扫码）
- 临时浏览器实例堆积（吃内存）被回收，可随时 `stopall` 一键释放

## 想回退
每个 profile 的 config 旁边都留了 `.bak-<时间戳>` 备份，直接覆盖回去即可。
