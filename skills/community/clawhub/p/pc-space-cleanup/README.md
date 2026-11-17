# pc-space-cleanup

一个 [Claude Code](https://docs.claude.com/en/docs/claude-code) skill：Windows 10/11 上 C/D 盘空间不足时的体检与腾空间流程。

只读盘点大目录 → 清开发缓存 → 项目打包 → 上传到 [CloudDrive2](https://www.clouddrive2.com/) 挂载的网盘（如 123 云盘）并逐文件校验 → 用户确认后删本地 → 整理云端目录。

全部来自一次真实整理（C 盘 42GB → 76GB，上云约 37GB），记录了实际踩到的坑和报错原文：

- CloudDrive 先写本地缓存再后台传，盘符上看到文件 ≠ 已上云
- 切换网络后上传卡在 128MB 分块边界
- PowerShell 5.1 把无 BOM 的 UTF-8 脚本当 GBK 读，中文路径全乱
- 刚传完立刻校验会误报缺失、123 云盘秒传、`WindowsApps\pip.exe` 商店别名……

## 安装

```powershell
git clone https://github.com/zp-home/pc-space-cleanup "$env:USERPROFILE\.claude\skills\pc-space-cleanup"
```

或从 ClawHub 安装：`npx clawhub install pc-space-cleanup`

然后在 Claude Code 里说「C 盘满了，清一下」即可触发。

## 前提

- Windows 10/11，PowerShell 5.1+，Python 3（只用标准库）
- 上云部分需要 CloudDrive2 已挂载网盘盘符，并在 CloudDrive 里生成 API 令牌
- 令牌只通过环境变量 `CD2_TOKEN` 传入，不写进任何文件；API 端口非默认 19798 时设 `CD2_URL`

## 文件

| 文件 | 作用 |
|---|---|
| `SKILL.md` | 流程、铁律、坑 |
| `scripts/upload.ps1` / `verify.ps1` | 按 JSON 清单分批上传、等队列清空、逐文件校验 |
| `scripts/cd2.py` | 极简 CloudDrive2 gRPC-Web 客户端（查上传队列、设置） |
| `scripts/reorg-lib.ps1` | 云端整理：只移动不删除，同名自动加后缀 |
| `scripts/peek_zip.py` | 只读 zip 目录区，不下载整包看内容 |

## 安全设计

- 只读盘点随便跑，任何写操作先出 dry-run 表，用户确认后执行
- 删本地前必须：上传队列 = 0、缓存 = 0、逐文件大小一致
- 云端整理只移动不删除

## License

MIT
