---
name: lanzou-downloader
description: 蓝奏云下载器（版本 V1.0.9）。纯 Node.js 零依赖，解析并下载蓝奏云分享链接（单文件/文件夹，带密码/免密），支持多链接或 txt/md/json 清单的批量路由（先解析成带编号清单、再按编号选择下载）；自动处理 JS 反爬（acw_sc__v2）、密码校验、下载域断流与重试。当用户发送 lanzou（lanzou* / lanzn.com）链接并要求下载时触发。不适用于其他网盘或视频平台。
metadata:
  security:
    credential_usage: 无需任何凭证，纯公开链接解析。
    allowed_domains:
      - '*.lanzoue.com'
      - '*.lanzous.com'
      - '*.lanzoux.com'
      - '*.lanzoui.com'
      - '*.lanzn.com'
      - '*.woozooo.com'
      - '*.lanrar.com'
    tls:
      default: verify
      opt_out: '--insecure / LANZOU_INSECURE_TLS=1（临时，自担风险）'
---

# 蓝奏云下载器（lanzou-downloader）

自包含的蓝奏云下载器：纯 Node.js 实现，零外部依赖（仅访问蓝奏云分享页及其下载域，不调用任何第三方服务）。**安全边界：HTTPS 默认开启证书校验**（个别镜像域证书异常时可加 `--insecure` 临时关闭，有中间人风险），且只写用户指定的输出路径。

## 一、单链接下载

```bash
node scripts/download.js <蓝奏云分享链接> [输出文件路径] [密码] [--select 目标1,目标2] [--list] [--insecure]
```

- **密码**：可选，自动检测；若不提供而链接需要密码，会报错提示
- **输出路径**：可选，默认当前目录 + 页面文件名；文件夹分享时视为目录
- **文件夹分享**（`b` 开头短码）自动识别（蓝奏分享仅含单层文件，子文件夹不参与分享；`t==1` 推广条目自动跳过）
- **--select**：只下载指定文件（文件名精确匹配或 `*` 通配），逗号分隔多个
- **--list**：只解析并输出文件清单（JSON，前缀 `__LANZOU_LIST__`），不下载
- **--insecure**：关闭 HTTPS 证书校验（仅镜像域证书异常时临时使用，有中间人风险）

示例：

```bash
# 带密码单文件
node scripts/download.js "https://wwapw.lanzoue.com/xxxxx" "" "1234"

# 文件夹分享，只要指定文件
node scripts/download.js "https://wwapw.lanzoue.com/b00XXXXXXX" "/下载目录" "1234" --select "分5.zip"

# 只列清单（不下载）
node scripts/download.js "<url>" "" "1234" --list
```

## 二、批量下载（batch.js）

把「一堆链接」先解析成带编号的清单，再按编号挑要下载的几个。

```bash
# ① 解析识别（生成清单，不下载）
node scripts/batch.js --urls "<url1>" "<url2>" ...
node scripts/batch.js --file links.txt links.md list.json

# ② 选择下载（编号 / 范围 / all）
node scripts/batch.js --manifest <上一步生成的清单> --select 1,3,5
node scripts/batch.js --file links.txt --select 1-3,7 --out-dir /sandbox/workspace/downloads
node scripts/batch.js --file links.txt --select all
```

**输入方式**

- `--urls`：一个或多个链接（一条参数里用空格/换行分隔多个也可），也可直接把链接跟在命令尾部
- `--file`：链接文件，支持 `txt / md / json`（json 递归抽取所有 URL；txt/md 按行抽取）
- **行内密码**：txt/md 每行可写「`密码:xxxx` / `提取码:xxxx` / `pwd:xxxx`」，自动作为该链接密码；`--password` 可指定所有链接的统一密码

**要点**

- 解析阶段对每个链接：识别标题、类型（单文件/文件夹）、可下载状态；文件夹分享会展开成多个可选项（每个文件一个编号）
- 清单落盘到当前目录 `.lanzou_manifest.json`，可用 `--manifest` 复用、避免重复解析
- `--json` 输出机器可读清单（stdout 仅 JSON，日志走 stderr）；`--list` 只解析不下载
- 选择下载时输出命名为 `标题`（**不加编号前缀**；标题已含扩展名则不重复追加；同名自动加 `-2`、`-3`），默认存到 `--out-dir`（默认 `./downloads`）

**AI 协作范式**：先跑 ①，把清单表给用户 → 用户说要下哪几个 → 跑 ② `--select`。

## 三、工作原理

1. **反爬**：解析分享页返回的 `arg1=` 挑战脚本，计算 `acw_sc__v2` cookie 后重试
2. **密码校验**：从页面 `down_p()` 读取 ajax 接口地址与 sign，POST 密码换取真实下载地址
3. **下载**：流式下载，重定向后清 `Referer` 防断流，校验大小 + 断流自动重试 3 次

### 关键点

- **全程复用 keep-alive 连接**：下载域（如 `developer4.lanrar.com`）对每次新建连接的请求会返回「系统发现您的网络异常」验证页，复用连接后直链直接返回文件流
- **下载域自身的 `acw_sc__v2` 反爬**会自动解算并重试（响应体为 gzip 时先解压再判断）
- **AJAX 地址动态提取**：直接在 iframe JS 上匹配 `$.ajax({ url: '...' })` / `domain1` / `domain2`，不写死、不剥离注释（避免字符串里的 `https://` 被当行注释删掉）

## 四、新版蓝奏云适配（密码分享页）

新版密码分享页结构已发生变化，本技能已完成适配：

- 密码提交接口由旧版 `/ajaxm.php` 改为**页面声明的完整地址** `https://apifile.woozooo.com/ajaxfile.php?file=xxx`（从 `down_p()` 的 `$.ajax` url 动态提取，找不到时回退旧接口）
- sign 参数由字面量 `'sign':'xxx'` 改为变量（取 `var isngis = '...'` 的值）
- 响应 `zt` 由数字改为字符串，改用宽松比较 `String(zt) === '1'`

## 五、变更记录

- **V1.0.9**：批量下载输出文件名**去掉编号前缀**（原 `NN_标题` → `标题`），下载即可直接用；同名自动加 `-2`、`-3` 防覆盖。清单与 `--select` 的编号逻辑不变。
- **V1.0.8**：新增批量下载路由 `scripts/batch.js`（多链接 / txt·md·json 清单 → 解析成带编号清单 → `--select` 按编号/范围/all 下载），支持行内密码识别、清单复用（`--manifest`）、命名去重后缀，保持纯 Node 零依赖。
- **V1.0.7**：从 mix-downloader 的蓝奏云模块抽取为独立技能；内置新版蓝奏云密码分享页适配（apifile.woozooo.com/ajaxfile.php 接口、isngis 变量 sign、zt 宽松比较），并保留反爬解算、keep-alive 复用、断流重试等全部能力。
