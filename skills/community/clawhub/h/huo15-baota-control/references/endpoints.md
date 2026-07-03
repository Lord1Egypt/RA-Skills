# 宝塔常用 API 端点速查

调用方式（本 skill 已封装）：`POST <url><endpoint>`，表单含 `request_time`+`request_token` 自动注入。
用 `bt_api.py raw --endpoint "..." --params '{...}'` 可调任意一个。

## 系统 / 监控
| endpoint | 作用 |
|---|---|
| `/system?action=GetSystemTotal` | CPU/内存/负载/系统版本（= `sysinfo`） |
| `/system?action=GetNetWork` | 实时网络/CPU/内存（= `network`） |
| `/system?action=GetDiskInfo` | 磁盘分区（= `disk`） |
| `/system?action=GetTaskCount` | 后台任务数 |
| `/ajax?action=get_load_average` | 负载 |

## 网站
| endpoint | 参数 | 作用 |
|---|---|---|
| `/data?action=getData&table=sites` | `limit,p,search` | 网站列表（= `sites`） |
| `/site?action=SiteStop` | `id,name` | 停站（= `site_stop`） |
| `/site?action=SiteStart` | `id,name` | 启站（= `site_start`） |
| `/site?action=SetSSL` | … | 配 SSL |
| `/site?action=GetSiteLogs` | `siteName` | 网站日志 |

## 数据库
| endpoint | 作用 |
|---|---|
| `/data?action=getData&table=databases` | 数据库列表（= `databases`） |
| `/database?action=ToBackup` `id` | 备份某库 |
| `/database?action=DeleteBackup` | 删备份 |

## SSL / 证书
| endpoint | 作用 |
|---|---|
| `/acme?action=get_order_list` | 证书订单列表 |
| `/acme?action=apply_order` | 申请/续签证书 |

## 计划任务
| endpoint | 作用 |
|---|---|
| `/crontab?action=GetCrontab` | 列计划任务 |
| `/crontab?action=StartTask` `id` | 立即执行某任务 |

## 文件（谨慎）
| endpoint | 参数 | 作用 |
|---|---|---|
| `/files?action=GetFileBody` | `path` | 读文件内容 |
| `/files?action=SaveFileBody` | `path,data,encoding` | 写文件 |
| `/files?action=GetDir` | `path` | 列目录 |

## Docker（gjb-ssh 业务都是容器，价值高）
宝塔 Docker 走插件接口，前缀 `/plugin?action=a&name=btdocker&s=<func>`，常见 `s` 有
`get_containers`(列容器) / `container_start` / `container_stop` / `container_restart`。
> 不同宝塔版本字段可能变，调不通时先 `raw` 试探返回结构。

## 备注
- 写操作务必先确认目标；删除类不可逆。
- 任意 shell 命令宝塔 API 不直接开放 → 走 SSH。
- 端点随宝塔版本会变，以实测返回为准；`raw` 是兜底。
