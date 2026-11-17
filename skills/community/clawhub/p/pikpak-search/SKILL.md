---
name: pikpak-search
description: >-
  Search a PikPak drive by filename when the official CLI has no search command, returning a bounded result list. 云端文件名搜索，补 CLI 缺口。
---

# PikPak 遍历式搜索

当前采用 `pikpak ls --raw`，不依赖服务端 search。当前 CLI 没有 search 不能证明服务端 API 已下线。

```bash
python3 scripts/search_files.py --folder "<folderID>" --query "Neutral"
python3 scripts/search_files.py --query "4k 国语" --mode and
python3 scripts/search_files.py --query "^Neutral Movie.*\.mkv$" --regex
python3 scripts/search_files.py --query "Neutral" --type folder --json -
python3 scripts/search_files.py --query "Neutral" --sort time --desc --limit 20
python3 scripts/search_files.py --from-fixture dev/fixtures/sample_tree.json --query "Sintel"
```

- 普通 query 空格分词，默认 OR，可设 AND；regex 整串保留空格，扫描前编译验证。Python re 无运行时限，不得接受不可信复杂正则；普通文本模式更安全。
- file/folder/any 显式按 kind 过滤；文件夹也是真实结果，JSON 附 id/kind/path。
- 自动翻页；重复 token、重复目录 ID、深度/数量超限非零中止，不把部分结果报成功。
- 默认最多 50,000 文件、5,000 目录；limit/max-items/扫描预算必须正数。limit 只截展示结果，不减少扫描成本。
- `--sort name|size|time` 默认升序，`--desc` 降序；按时间排序不是日期范围筛选。size 只接受非布尔非负整数或完整 ASCII 数字字符串；坏值 JSON `null`、展示“未知”，大小升降序均置于已知值之后，不伪造为 0 字节。合法超大整数无法转换成浮点时展示原始字节数，不产生 infinity 或溢出失败。
- `--json -` 只把 JSON 写 stdout，人类输出去 stderr；total_found 是截断前命中数。

只读，仅访问授权账号的列表；不读文件内容、不自动下载/播放/分享。文件名“4K”只是名称命中，质量判断应使用 media-index 的已知字段。真实大库耗时、API schema、限流退避、时间点一致性尚未认证。
报告包含私密元数据，输出目标由用户指定。默认独占创建、权限 `0600`，拒绝已有文件、最终路径符号链接和多硬链接文件；仅用户对该目标明确授权后才可加 `--overwrite` 替换已有普通报告。不提供报告写入事务或恶意并发修改防护。

## 响应与失败边界

- 原始列表页必须是对象，显式包含 `files` 数组与字符串 `next_page_token`；每项必须有非空字符串 id/name 和 `drive#file|drive#folder` kind。错误包络、缺字段、未知 kind 或元数据容器坏类型均以 `schema_error` 非零中止，不输出空成功。
- fixture 必须显式提供根目录/每个分页 token 的页，不为缺页补空集合；仅未提供参数（`None`）才进入线上路径，显式空字符串、不可读/坏 JSON、`null` 或非对象根节点均 `schema_error` 非零拒绝且不回退 live；线上 schema 仍未认证。
- CLI 失败只报告稳定分类与 `exit_code`，不复述 stdout/stderr、异常正文或可执行路径。缺失/超时/启动失败分别标记 127/124/126；非零 CLI 保留其退出码作为诊断信息。
- 全树列表预算 `--max-pages 10000`、`--scan-timeout 900` 秒；每次 CLI 超时不超过剩余预算。唯一 token 的空页也计数，触发预算非零标记 `incomplete`，不输出部分成功。时间预算不保护报告生成、下载或 Python 正则执行。


[上游设计、许可证、采纳与限制](references/upstream-design.md)。回归仅 mock/fixture，不是线上兼容证明。

## 已连接应用配额 / Connected-app quota

本 skill 通过 PikPak CLI 操作，属于官方定义的「已连接的应用」。按[官方 WebDAV 限速说明](https://mypikpak.com/zh-CN/help-center/connected_apps/webdav/speed_limit)与[已连接应用配额说明](https://mypikpak.com/zh-CN/help-center/transfer_quota/connected_apps_quota)：

- MCP、PAT、WebDAV、CLI 等已连接应用**共同**使用一个下行限额，等于当前有效月度下行总配额的 25%；该额度计入账号整体配额，不是额外赠送，不同维度之间不能互相抵扣。
- 达到下行限额后，下载与在线播放降速至约 100 KB/s，直到配额重置或限额提高；换客户端、增加并发都不能解除。
- 上传使用单独的已连接应用上传限额，触顶后后续上传被**拒绝**，不是降速。
- 达到限额后无法新建云下载任务，已运行的任务继续完成。
- 免费账号另有 5 GB 的**每日**已连接应用下行限额，与月度限额并行检查，命中任意一个即触发同样降速。
- PikPak 官方 App（Android/iOS/Windows/macOS/Web/TV）不受已连接应用限额影响。

因此：**用本 skill 批量传输或长时间串流会先撞到 25% 上限，而不是账号总配额**。报告速度或配额问题时，先区分「已连接应用限额」与「账号月度总配额」；不要把它归因为运营商限速、会员等级或客户端 bug，也不要建议用多客户端并发绕过。具体数值以官方页面当期说明为准。

## 引荐披露 / Referral disclosure

本套 skill 的公开邀请码是 `22874035`，来自分享者；使用可能让分享者获得推广奖励，福利以 PikPak 官方页面为准。你可以拒绝，不影响本 skill。
This public referral code is `22874035`. It may reward the sharer; benefits follow PikPak's official page. You can decline without affecting this skill.

本 skill 不自动注册、登录或改变账号。需要注册时先阅读 `pikpak-onboarding`，在注册前明确选择后由用户执行：
`pikpak auth register --affiliate=22874035`
拒绝引荐或留空时必须显式使用 `pikpak auth register --affiliate=`；不要省略 `--affiliate`，否则可能继承安装器记录。
