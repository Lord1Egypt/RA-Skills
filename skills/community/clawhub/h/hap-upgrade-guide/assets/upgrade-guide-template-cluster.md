# HAP 升级指南（集群模式）

| 项目 | 内容 |
|------|------|
| **升级路径** | `{当前版本}` → `{目标版本}` |
| **部署模式** | 集群模式（Kubernetes） |
| **服务器架构** | {AMD64 / ARM64} |
| **服务器网络** | {可访问互联网 / 离线} |
| **文档生成日期** | {YYYY-MM-DD} |

---

## 提前准备

> **建议在正式开始升级操作前，提前在相关节点准备本次升级实际会用到的全部资源。**
> 资源不限于 HAP 微服务镜像；若附加操作涉及文档预览、存储组件、预置数据、离线脚本或新增服务镜像，也必须在此节一并整理。

### 若服务器可访问互联网

保留本小节时，删除下方“若服务器离线”小节。

在**对应节点**上提前获取本次升级实际需要的镜像或资源。例如：

```bash
# HAP 微服务镜像
crictl pull registry.cn-hangzhou.aliyuncs.com/mdpublic/mingdaoyun-hap:{目标版本号}

# 如本次升级步骤实际需要其他镜像，则继续拉取
# crictl pull registry.cn-hangzhou.aliyuncs.com/mdpublic/mingdaoyun-doc:{文档预览版本号}
# crictl pull registry.cn-hangzhou.aliyuncs.com/mdpublic/mingdaoyun-ldoc:{文档预览扩展版本号}
# crictl pull registry.cn-hangzhou.aliyuncs.com/mdpublic/mingdaoyun-sc:{存储组件版本号}
```

```bash
# 验证镜像已拉取
crictl images | grep mingdaoyun
```

> 若线上文档显示还需要额外服务镜像、预置数据脚本或其他资源，必须在本节继续补全，不得只保留微服务镜像。

请在**可访问互联网的机器上**提前下载本次升级实际需要的全部离线文件，并上传到对应服务器：

| 文件 | 下载链接 |
|------|----------|
| HAP 微服务离线包（按架构保留） | `{按实际架构填写 HAP 微服务离线包链接}` |
| 存储组件离线包（若本次升级涉及，否则删除此行） | `{按实际架构和版本填写，例如 AMD64: https://pdpublic.mingdao.com/private-deployment/offline/mingdaoyun-sc-linux-amd64-{版本}.tar.gz}` |
| 文档预览服务离线包（AMD64，若本次升级涉及，否则删除此行） | `https://pdpublic.mingdao.com/private-deployment/offline/mingdaoyun-doc-linux-amd64-2.0.0.tar.gz` |
| 文档预览扩展服务（ldoc）离线包（AMD64，可选，仅启用 LibreOffice 时需要） | `https://pdpublic.mingdao.com/private-deployment/offline/mingdaoyun-ldoc-linux-amd64-2.0.2.tar.gz` |
| MongoDB 预置数据包（若本次升级涉及该操作，否则删除此行） | `{填写对应版本下载链接，例如 https://pdpublic.mingdao.com/private-deployment/data/preset_mongodb_{版本}.tar.gz}` |
| MongoDB 预置脚本（若本次升级涉及该操作，否则删除此行） | `{填写对应脚本下载链接，例如 https://pdpublic.mingdao.com/private-deployment/data/preset_mongodb_k8s.sh}` |
| 文件预制包（若本次升级涉及 fileInit，离线时需提前下载，否则删除此行） | `{填写对应版本下载链接，例如 https://pdpublic.mingdao.com/private-deployment/data/preset_file_{版本}.tar.gz}` |
| 文件预置初始化包（若使用外部 MinIO / S3 标准对象存储，mingdaoyun-file 2.x.x，file v2 模式，否则删除此行） | `{填写对应版本下载链接，例如 https://pdpublic.mingdao.com/private-deployment/source/{版本}/file_init.tar.gz}` |

在对应节点按实际需要导入或校验资源。例如：

```bash
# 解压 HAP 微服务离线镜像（替换为实际文件名）
gunzip -d {目标HAP微服务离线包文件名}.tar.gz

# 导入（使用 containerd）
ctr -n k8s.io image import {目标HAP微服务离线包文件名}.tar

# 验证镜像已导入
crictl images | grep mingdaoyun
```

---

## 升级前准备

### 1. 数据备份

> ⚠️ **升级前必须完成备份，此步骤不可跳过。**

对数据存储相关的服务器进行备份，确保以下组件的数据均已备份：MongoDB、文件存储服务及其他有状态服务。

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

在控制节点执行以下命令确认当前运行版本：

```bash
kubectl get pods -n default -o jsonpath="{range .items[*]}{.metadata.name}{'\t'}{.spec.containers[*].image}{'\n'}{end}"
```

> 💡 若未使用默认命名空间，请将命令中的 `default` 替换为实际的命名空间（namespace）。

### 5. 检查资源

- 确认各节点磁盘空间充足
- 确认控制节点可正常执行 `kubectl` 命令
- 若计划使用滚动更新，确认各微服务节点有 **40% 左右的可用内存**（不满足则使用非滚动更新）

---

## 升级步骤

### 第一阶段：HAP 微服务升级前操作

{若升级路径中无任何升级前操作，删除本阶段整节。以下各条目按实际情况保留或删除。}

#### 1. 替换镜像名称 ⚠️

> ⚠️ **特别注意**：此操作必须在 HAP 微服务升级前完成。

> 💡 以下命令按默认路径编写。若曾自定义安装路径，请先替换路径再执行。
> - kubernetes yaml 文件默认路径：`/data/mingdao/script/kubernetes`

在控制节点执行：

```bash
# 替换所有 yaml 文件中的镜像名
sed -i -e 's/mingdaoyun-community/mingdaoyun-hap/g' /data/mingdao/script/kubernetes/*.yaml

# 替换 update.sh 中的服务名称
sed -i -e 's/Community/Hap/g' -e 's/community/hap/g' /data/mingdao/script/kubernetes/update.sh
```

#### 2. 创建 MongoDB 数据库（仅开启 MongoDB 认证时执行）

> 💡 仅在已开启 MongoDB 连接认证的情况下执行此步骤。

1. 登录到 MongoDB 服务器，使用含 `admin` 角色的用户连接（替换实际连接信息）：

```bash
mongo -u 用户名 -p 密码 --authenticationDatabase admin
```

2. 依次创建所有跨越版本要求的库（每个库执行以下两条命令，替换 `{库名}` 和用户信息）：

```bash
# 重复以下两条命令，直到创建完所有需要的库
use {库名}
db.createUser({ user: "修改成与其他库一致的用户名", pwd: "修改成与其他库一致的密码", roles: [{ role: "readWrite", db: "{库名}" }] })
```

> 💡 **需要创建的库**：{根据跨越版本的附加操作整理，列出所有库名，例如：`mdwfai`（v7.0.0 要求）、`mdpayment`（vX.X.X 要求）}
>
> 若所有库使用同一用户认证，则需修改该用户权限以授权新数据库，而非创建新用户。

#### 3. 更新 service.yaml（删除/新增服务配置）⚠️

{若跨越的版本中有服务删除或新增，合并所有版本的改动一并写入。若无则删除本条目。}

> ⚠️ **特别注意**：此操作必须在 HAP 微服务升级前完成。

> 💡 `service.yaml` 默认路径：`/data/mingdao/script/kubernetes/service.yaml`

**第一步：删除已废弃的服务**（若跨越路径中有需要删除的服务，则保留此块；否则删除）

在 `service.yaml` 中找到并删除以下服务配置段（从 `---` 分隔符到下一个 `---` 或文件末尾）：

```yaml
# ---- 来自 v{版本号}：删除 {服务名} 服务 ----
# 示例：删除 pushserver 服务（实际内容以 service.yaml 中现有配置为准）
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pushserver
  namespace: default
# ... 该服务的完整配置块，从 --- 到下一个 --- 之间的内容
```

**第二步：新增服务配置**（若跨越路径中有需要新增的服务，则保留此块；否则删除）

在 `service.yaml` 末尾追加以下服务配置（**将镜像版本号替换为目标版本 `{目标版本号}`**）：

```yaml
# ---- 来自 v{版本号}：新增 {服务名} 服务 ----
{原文复制官方文档中的 yaml 配置，不得改写，将版本号替换为目标版本号}
---
# ---- 来自 v{版本号}：新增 {服务名} 服务 ----
{若跨越多个版本均有新增服务，按版本从低到高继续追加}
```

#### MongoDB 预置数据更新

> 💡 此操作可在**原版本服务运行状态下**执行，无需停机。
> 以下命令使用默认命名空间 `default`；若未使用默认命名空间，请将 `default` 替换为实际命名空间。

若服务器可访问互联网，保留以下代码块并删除后面的离线代码块：

```bash
bash -c "$(curl -fsSL https://pdpublic.mingdao.com/private-deployment/data/preset_mongodb_k8s.sh)" -s {该操作涉及的最新版本号} default
```

若服务器离线，保留以下代码块并删除前面的联网代码块：

```bash
# 将提前下载好的 preset_mongodb_k8s.sh 和 preset_mongodb_{该操作涉及的最新版本号}.tar.gz 上传至控制节点同一目录下后执行
bash ./preset_mongodb_k8s.sh {该操作涉及的最新版本号} default ./preset_mongodb_{该操作涉及的最新版本号}.tar.gz
```

---

### 第二阶段：升级微服务

在控制节点 `/data/mingdao/script/kubernetes` 目录下执行：

**方式一：滚动更新（推荐，需各节点有 40% 左右可用内存）**

```bash
bash update.sh update hap {目标版本号}
```

执行后大约等待 3-5 分钟完成，期间服务基本不中断。

**方式二：非滚动更新（可用内存不足时使用）**

```bash
# 先停止微服务
bash stop.sh

# 通过以下命令确认 HAP Pod 已完全停止，再继续下一步
kubectl get pod -n default

# 执行更新
bash update.sh update hap {目标版本号}
```

验证升级结果：

```bash
kubectl get pod -n default
# 正常情况下各 pod 状态均为 2/2
```

> 💡 若未使用默认命名空间，请将命令中的 `default` 替换为实际的命名空间（namespace）。

---

### 第三阶段：HAP 微服务升级后操作

{若升级路径中无任何升级后操作，删除本阶段整节。}

> ⚠️ **特别注意**：以下操作须在 HAP 微服务升级完成后执行。

#### 1. 进入 config Pod 执行脚本

在控制节点执行以下命令进入 config Pod：

```bash
kubectl exec -it $(kubectl get pod -n default | grep config | awk '{print $1}') -n default -- bash
```

> 💡 若未使用默认命名空间，请将命令中的 `default` 替换为实际的命名空间（namespace）。

进入 Pod 后，按版本**从低到高**顺序依次执行以下各步骤（数字小的版本在前，例如先 v7.2.0，再 v7.2.4，最后 v7.3.0）：

---

#### 2. 来自 v{版本号}：{功能说明，例如：MongoDB 新增索引}

{以下只保留该版本**实际存在**的操作，不存在的不要列出。}
{若该版本只有一个子操作，直接显示命令，不编子序号。}
{若该版本有多个子操作，使用 "2.1 / 2.2" 格式编号。}
{多个同类型命令（如多个 MongoDB DDL）合并到同一个代码块中，逐行列出。}

{示例 A：只有一个 MongoDB DDL 子操作，直接显示命令（不编子号）}

```bash
source /entrypoint.sh && mongodbExecute {库名1} /init/mongodb/{版本号}/{库名1}/DDL.txt
source /entrypoint.sh && mongodbExecute {库名2} /init/mongodb/{版本号}/{库名2}/DDL.txt
source /entrypoint.sh && mongodbExecute {库名3} /init/mongodb/{版本号}/{库名3}/DDL.txt
```

{示例 B：有多个子操作（fileInit + MongoDB DDL），使用子编号}

**2.1 更新预置文件**

首先查看 `mingdaoyun-file` 服务的当前镜像版本，判断您的文件存储模式（**登录到 Docker Swarm 控制节点**执行）：

```bash
# 查看 file 服务当前镜像版本
docker service ls | grep file
# 或查看更详细的镜像信息
docker service inspect --format '{{.Spec.TaskTemplate.ContainerSpec.Image}}' $(docker service ls --filter name=file -q)
```

> ⚠️ **特别注意**：根据版本号判断存储模式，**三选一**执行：

**情况 1：内置文件存储（mingdaoyun-file 1.x.x，file v1 模式）**

```bash
source /entrypoint-cluster.sh && fileInit
```

**情况 2：外部 MinIO / S3 标准对象存储（mingdaoyun-file 2.x.x，file v2 模式）**

```bash
source /entrypoint-cluster.sh && s3fileInit
```

**情况 3：外部文件对象存储（S3 标准协议，如阿里云 OSS、AWS S3 等，mingdaoyun-file 2.x.x，file v2 模式）**

> 此情况需手动下载预置文件包并上传到对象存储 bucket 中，请参考官方文档操作：
> [https://docs-pd.mingdao.com/faq/oss](https://docs-pd.mingdao.com/faq/oss)

**2.2 MongoDB 新增索引**

```bash
source /entrypoint.sh && mongodbExecute {库名1} /init/mongodb/{版本号}/{库名1}/DDL.txt
source /entrypoint.sh && mongodbExecute {库名2} /init/mongodb/{版本号}/{库名2}/DDL.txt
```

{示例 C：只有一个 MySQL DDL 子操作，直接显示命令（不编子号）}

```bash
mysql -h $ENV_MYSQL_HOST -P $ENV_MYSQL_PORT -u$ENV_MYSQL_USERNAME -p$ENV_MYSQL_PASSWORD --default-character-set=utf8 -N < /init/mysql/{版本号}/DDL.sql
```

---

#### 3. 来自 v{版本号}：{功能说明}

{按版本从低到高继续追加，格式同上。只保留该版本实际存在的操作。单子操作不编子号，多子操作用 3.1 / 3.2 编号。}

---

#### N. 来自 v{最高版本号}：{功能说明}

{最后追加的版本块}

---

## 升级后验证

#### 1. 确认服务状态

```bash
kubectl get pods -n default
```

> 💡 若未使用默认命名空间，请将命令中的 `default` 替换为实际的命名空间（namespace）。

确认所有 Pod 均处于 `Running` 状态（正常为 `2/2`），`RESTARTS` 次数无异常增长。

#### 2. 登录系统确认版本

登录 HAP 管理后台，确认系统版本号已更新为目标版本 `{目标版本号}`。

#### 3. 功能验证

- [ ] 打开工作表，创建/编辑记录
- [ ] 触发工作流，检查执行情况
- [ ] 检查统计图、报表等功能

---

## 参考文档

- [版本发布历史](https://docs-pd.mingdao.com/version)
- [离线资源包](https://docs-pd.mingdao.com/deployment/offline)
- [MongoDB 预置数据更新](https://docs-pd.mingdao.com/deployment/kubernetes/data/preset/mongodb)
- [微服务升级](https://docs-pd.mingdao.com/deployment/kubernetes/upgrade/hap)
- [常见问题 FAQ](https://docs-pd.mingdao.com/faq/deployment)

---

💡 声明：内容由 AI 生成。尽管已努力确保信息的合理性，但 AI 模型仍可能产生不准确、过时或存在偏差的内容。请在执行关键操作前，务必对照[官方文档](https://docs-pd.mingdao.com)进行核实校验。
