# 宝塔(BT-Panel)可编程控制方案研究 — 让龙虾操控服务器

> 实测环境：gjb-ssh 上宝塔 **11.8.0**（经 `gjbserver.huo15.com` frp 隧道暴露）。2026-06-25。

## 结论（TL;DR）

| 方案 | 适合 | 结论 |
|---|---|---|
| **HTTP API**（token 签名） | 结构化运维：系统状态/网站/数据库/SSL/计划任务/Docker | ✅ **首选**，已封装 `bt_api.py` 验证通过（本地 + 经隧道远程都通） |
| **bt CLI**（`bt` 命令） | 交互式菜单 | ❌ 几乎全交互、不支持 `bt help`，**不适合自动化** |
| **SSH + shell** | 任意命令（docker/nginx/文件…） | ✅ 补充：宝塔 API 不开放任意 shell（安全限制），要跑命令走 SSH |

→ 龙虾操控 = **宝塔 HTTP API（结构化操作）+ SSH（任意命令）** 两条腿。本目录专注 API 这条。

## 一、宝塔 11.8 API 鉴权机制（实测，与老文档不同）

老版本用 `key` 签名；**11.x 改用 `token`**（开启 API 时才生成，加密存 `token_crypt`）：

```
签名 = md5( str(request_time) + md5(token明文) )
POST 表单: { request_time, request_token, ...业务参数 }
请求头必须带浏览器 User-Agent  ← 否则宝塔反扫描返回伪装的 nginx-404
```

源码位置：`/www/server/panel/class/panelApi.py`（`get_token` / `set_token`）。

## 二、如何开启 API（坑：不能直接改 api.json）

- 配置文件 `/www/server/panel/config/api.json`，但**直接改它会被面板重启时还原**（面板以内部状态为准）。
- 且 `set_token` 里 `if 'request_token' in get: return '不能通过API接口配置API'` —— **不能用 API 去开 API**（鸡生蛋）。
- 正解：调宝塔自己的 `panelApi.set_token`。本目录 `enable_api.py` 就干这个（用面板 pyenv python 跑）：
  ```bash
  sudo /www/server/panel/pyenv/bin/python3 enable_api.py <白名单IP,逗号分隔>
  # 输出 open=true / limit_addr / token_plain(签名用的明文token)
  ```
  或者：登录面板 → 面板设置 → API接口 → 开启 + 加 IP 白名单 + 复制接口密钥。

## 三、龙虾对接架构

```
龙虾(任意机器) --https--> gjbserver.huo15.com (老 frps .121, nginx)
   --frp隧道--> gjb-ssh:12077 宝塔  (隧道 localIP=127.0.0.1)
```
- 隧道把请求以 **源 IP=127.0.0.1** 送达宝塔 → 白名单填 `127.0.0.1` 即可让任意位置的龙虾远程调用。
- 多面板：`~/.huo15/baota.json` 里每台服务器一个 panel（name/url/token），`bt_api.py --panel <name>` 选择。
- 调用全部走 `scripts/bt_api.py`（或 `bt_api.py`），龙虾通过 skill（`SKILL.md`）按意图触发。

## 四、安全

- **token 是唯一防线**（隧道公网可达，白名单全 127.0.0.1 等于不限来源）。务必保密、定期轮换。
- 想收紧：在 .121 的 nginx 给 `gjbserver.huo15.com` 加 IP 白名单/BasicAuth，或不走公网隧道、让龙虾跑在 gjb-ssh 本机走 localhost。
- token 只放 `~/.huo15/baota.json`（chmod 600），**绝不入库**。本仓库只有 `baota.json.example` 占位。
- 写操作（停站/删库/续证书）龙虾要先确认再执行。

## 五、文件清单

| 文件 | 作用 |
|---|---|
| `bt_api.py` | 核心封装：token 签名 + 通用 `call`/`raw` + 高层助手(sysinfo/sites/...) |
| `enable_api.py` | 在服务器上正式开启宝塔 API + 设白名单 + 取明文 token |
| `SKILL.md` | 龙虾 skill：触发词 + 用法 |
| `baota.json.example` | 配置模板（拷到 `~/.huo15/baota.json` 填真值） |
| `references/endpoints.md` | 宝塔常用 API 端点速查 |

## 六、实测验证

```
sysinfo  -> 20核 / 内存30.7GB 已用12.8GB        ✅ 本地 + 经隧道远程都通
disk     -> / 914.8GB 已用66.3GB                ✅
crontab  -> [续签Let's Encrypt证书, ...]         ✅ 通用 raw 调用
sites    -> []（gjb-ssh 的服务都是 docker，非宝塔站）✅
```
