# HAP 升级指南（单机模式）

| 项目 | 内容 |
|------|------|
| **升级路径** | `{当前版本}` → `{目标版本}` |
| **部署模式** | 单机模式（Docker Compose） |
| **服务器架构** | {AMD64 / ARM64} |
| **服务器网络** | {可访问互联网 / 离线} |
| **文档生成日期** | {YYYY-MM-DD} |

---

### 提前准备

> **建议在正式开始升级操作前，提前准备本次升级实际会用到的全部资源。**
> 资源不限于 HAP 微服务镜像；若附加操作涉及存储组件、文档预览、预置数据、离线脚本或其他组件资源，也必须在此节一并整理。

### 若服务器可访问互联网

保留本小节时，删除下方“若服务器离线”小节。

在服务器上提前获取本次升级实际需要的镜像或资源。例如：

```bash
# HAP 微服务镜像
docker pull registry.cn-hangzhou.aliyuncs.com/mdpublic/mingdaoyun-hap:{目标版本号}

# 如本次升级步骤实际需要存储组件镜像，则继续拉取对应镜像
# docker pull registry.cn-hangzhou.aliyuncs.com/mdpublic/mingdaoyun-sc:{目标存储组件版本号}
```

> 若线上文档显示还需要文档预览、预置数据脚本、额外服务镜像或其他资源，必须在本节继续补全，不得只保留微服务镜像。

请在**可访问互联网的机器上**提前下载本次升级实际需要的全部离线文件，并上传到服务器：

| 文件 | 下载链接 |
|------|----------|
| HAP 微服务离线包（按架构保留） | `{按实际架构填写 HAP 微服务离线包链接}` |
| 存储组件离线包（若本次升级涉及，否则删除此行） | `{按实际架构和版本填写，例如 AMD64: https://pdpublic.mingdao.com/private-deployment/offline/mingdaoyun-sc-linux-amd64-{版本}.tar.gz}` |
| 文档预览服务离线包（AMD64，若本次升级涉及，否则删除此行） | `https://pdpublic.mingdao.com/private-deployment/offline/mingdaoyun-doc-linux-amd64-2.0.0.tar.gz` |
| 文档预览扩展服务（ldoc）离线包（AMD64，可选，仅启用 LibreOffice 时需要） | `https://pdpublic.mingdao.com/private-deployment/offline/mingdaoyun-ldoc-linux-amd64-2.0.2.tar.gz` |
| MongoDB 预置数据包 | `{若本次升级涉及该操作，则填写对应版本下载链接；否则删除该行}` |
| MongoDB 预置脚本 | `{若本次升级涉及该操作，则填写对应脚本下载链接；否则删除该行}` |

上传到服务器后，按实际需要导入或校验资源。例如：

```bash
# 导入 HAP 微服务离线镜像（替换为实际文件名）
docker load -i {目标HAP微服务离线包文件名}.tar.gz

# 验证镜像已导入
docker images
```

---

## 升级前准备

### 1. 数据备份

> ⚠️ **升级前必须完成备份，此步骤不可跳过。**

请参考官方文档完成数据备份：[数据备份文档](https://docs-pd.mingdao.com/deployment/docker-compose/standalone/data/backup)

### 2. 授权有效期检查

> ⚠️ **重要提示**：请确保您的授权密钥仍在"升级服务"有效期内。若目标主版本的发布日期晚于授权到期日，强行升级将触发系统受限提示，并导致授权自动降级为免费版。建议在升级前确认版本发布日期与授权期限的匹配情况。

请检查您的授权密钥是否仍在"升级服务"有效期内，并确认授权到期日晚于目标版本的发布日期。若授权即将到期或已过期，请联系明道云商务团队续期后再执行升级。

### 3. 前端二次开发注意事项

> ⚠️ **注意**：如有前端二次开发，请联系前端二开负责同事确认此操作已完成，否则可能导致升级后前端功能异常。

若系统中存在前端二次开发（即有基于 HAP 前端源码进行过定制开发），升级后前端代码可能与新版本存在差异，需要**前端二开负责同事**执行以下操作：

1. 拉取最新的前端二开基础代码（官方前端仓库对应目标版本的分支或 tag）
2. 将自定义的二开代码合并（merge）进最新基础代码，处理可能存在的冲突
3. 构建并发布更新后的前端服务，使新版本前端生效

若系统中**没有**前端二次开发，忽略本注意事项。

### 4. 确认当前版本

执行以下命令确认当前运行版本与本文档起始版本一致：

```bash
docker ps --format "table {{.Image}}\t{{.Names}}"
```

### 5. 检查资源

- 确保磁盘空间充足（建议预留 40GB 以上）

---

## 升级步骤

### 第一阶段：HAP 微服务升级前操作

{若升级路径中无任何升级前操作，删除本阶段整节。以下各条目按实际情况保留或删除。}

#### 1. 替换镜像名称

> 💡 以下命令按默认路径编写。若曾自定义安装路径，请先替换路径再执行。
> - `docker-compose.yaml` 默认路径：`/data/mingdao/script/`
> - `service.sh` 默认路径：`/usr/local/MDPrivateDeployment/`
> - `run.sh` 默认路径：`/data/mingdao/script/`

```bash
# 替换 docker-compose.yaml 中的镜像名
sed -i -e 's/mingdaoyun-community/mingdaoyun-hap/g' /data/mingdao/script/docker-compose.yaml

# 替换 service.sh 中的服务名称
sed -i -e 's/Community/Hap/g' -e 's/community/hap/g' /usr/local/MDPrivateDeployment/service.sh

# 替换 run.sh 中的镜像名（如文件存在）
if [ -f /data/mingdao/script/run.sh ]; then
  sed -i -e 's/mingdaoyun-community/mingdaoyun-hap/g' /data/mingdao/script/run.sh
fi
```

#### 2. 创建 MongoDB 数据库（仅开启 MongoDB 认证时执行）

> 单机模式下 MongoDB 默认未开启认证，仅在自定义过开启 MongoDB 连接认证的情况下执行此步骤

1. 进入存储组件容器：

```bash
docker exec -it $(docker ps | grep mingdaoyun-sc | awk '{print $1}') bash
```

2. 在容器内，使用含 `admin` 角色的用户登录 MongoDB（替换实际用户名和密码）：

```bash
mongo -u 用户名 -p 密码 --authenticationDatabase admin
```

3. 依次创建所有跨越版本要求的库（每个库执行以下两条命令，替换 `{库名}` 和用户信息）：

```bash
# 重复以下两条命令，直到创建完所有需要的库
use {库名}
db.createUser({ user: "修改成与其他库一致的用户名", pwd: "修改成与其他库一致的密码", roles: [{ role: "readWrite", db: "{库名}" }] })
```

> 💡 **需要创建的库**：{根据跨越版本的附加操作整理，列出所有库名，例如：`mdwfai`（v7.0.0 要求）、`mdpayment`（vX.X.X 要求）}
>

#### 3. 存储组件升级

{若跨越多个含存储组件升级的版本，直接升级到所有版本中要求的最高版本号。}

1. 修改 `/data/mingdao/script/docker-compose.yaml` 中存储组件的镜像版本号为 `{目标存储组件版本号}`

>  如果存储组件与 HAP 微服务同时升级，可在修改完两处版本号后，最后只执行一次 `restartall`，无需分开重启。

#### 4. MongoDB 预置数据更新

> 此操作在**原版本服务运行状态下**执行，无需停机。

若服务器可访问互联网，保留以下代码块并删除后面的离线代码块：

```bash
bash -c "$(curl -fsSL https://pdpublic.mingdao.com/private-deployment/data/preset_mongodb_docker.sh)" -s {该操作涉及的最新版本号}
```

若服务器离线，保留以下代码块并删除前面的联网代码块：

```bash
# 将提前下载好的 preset_mongodb_docker.sh 和 preset_mongodb_{该操作涉及的最新版本号}.tar.gz 上传至服务器同一目录下后执行
bash ./preset_mongodb_docker.sh {该操作涉及的最新版本号} ./preset_mongodb_{该操作涉及的最新版本号}.tar.gz
```

---

### 第二阶段：升级微服务

#### 1. 修改镜像版本号

编辑 `/data/mingdao/script/docker-compose.yaml`，将 HAP 镜像版本号修改为目标版本，并确保 `ENV_APP_VERSION` 环境变量的值与微服务镜像版本号保持一致：

```yaml
# 修改前
image: registry.cn-hangzhou.aliyuncs.com/mdpublic/mingdaoyun-hap:{当前版本号}
environment:
  ENV_APP_VERSION: "{当前版本号}"

# 修改后
image: registry.cn-hangzhou.aliyuncs.com/mdpublic/mingdaoyun-hap:{目标版本号}
environment:
  ENV_APP_VERSION: "{目标版本号}"
```

> 💡 **重要说明**：`ENV_APP_VERSION` 环境变量的值必须与微服务镜像版本号保持一致（例如：微服务版本是 7.1.1，`ENV_APP_VERSION` 的值也应设为 7.1.1），否则可能导致系统功能异常。

#### 2. 重启服务

在管理器根目录下执行（通常在 `/usr/local/MDPrivateDeployment/`，以实际为准）：

```bash
bash ./service.sh restartall
```

等待命令执行完成，服务将自动完成升级并重启。

- 如遗忘 `service.sh` 文件所在路径，可使用以下命令查找

  ```text
  find / -path /proc -prune -o -name "service.sh" -print
  ```

---

### 第三阶段：HAP 微服务升级后操作

{若升级路径中无任何升级后操作，删除本阶段整节。}

#### 1. 进入微服务容器执行脚本

进入容器：

```bash
docker exec -it $(docker ps | grep -E 'mingdaoyun-community|mingdaoyun-hap' | awk '{print $1}') bash
```

> 💡 如曾自定义过 MySQL 用户名、密码，注意修改命令中对应参数值（默认：用户名 `root`，密码 `123456`）。

在容器内按版本**从低到高**顺序执行以下操作：

#### 2. 来自 v{版本号}：MySQL 新增索引

```bash
mysql -h sc -P 3306 -uroot -p123456 --default-character-set=utf8 -N < /init/mysql/{版本号}/DDL.sql
```

#### {N}. 来自 v{版本号}：{功能说明}

{若该版本只有一个子操作，直接显示命令代码块，不编子序号。}

```bash
mysql -h sc -P 3306 -uroot -p123456 --default-character-set=utf8 -N < /init/mysql/{版本号}/DDL.sql
```

{按实际跨越版本继续追加（版本从低到高排列），每个版本一个 h4 标题}

---

## 升级后验证

#### 1. 确认服务状态

```bash
docker ps
```

确认所有容器均处于 `Up` 状态，无异常重启。

#### 2. 检查HAP微服务容器日志

```
docker logs $(docker ps | grep -E 'mingdaoyun-community|mingdaoyun-hap' | awk '{print $1}')
```

正常所输出日志应都是 `INFO `级别

#### 3. 登录系统确认版本

登录 HAP 管理后台，确认系统版本号已更新为目标版本 `{目标版本号}`。

#### 4. 功能验证

- [ ] 打开工作表，创建/编辑记录
- [ ] 触发工作流，检查执行情况
- [ ] 检查统计图、报表等功能

## 异常情况排查

参考[服务运行状况检查](https://docs-pd.mingdao.com/faq/troubleshooting/service-status-check)文档对容器日志进行检查

### 1. 容器日志检查

查看微服务应用容器健康检查日志

```text
docker logs $(docker ps -a | grep mingdaoyun-community|mingdaoyun-hap | awk '{print $1}')
```

查看存储组件容器健康检查日志

```text
docker logs $(docker ps -a | grep mingdaoyun-sc | awk '{print $1}')
```

---

## 参考文档

- [版本发布历史](https://docs-pd.mingdao.com/version)
- [离线资源包](https://docs-pd.mingdao.com/deployment/offline)
- [数据备份](https://docs-pd.mingdao.com/deployment/docker-compose/standalone/data/backup)
- [微服务升级](https://docs-pd.mingdao.com/deployment/docker-compose/standalone/upgrade/hap)
- [常见问题 FAQ](https://docs-pd.mingdao.com/faq/deployment)

---

💡 声明：内容由 AI 生成。尽管已努力确保信息的合理性，但 AI 模型仍可能产生不准确、过时或存在偏差的内容。请在执行关键操作前，务必对照[官方文档](https://docs-pd.mingdao.com)进行核实校验。
