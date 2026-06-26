# HAP 升级命令库

本库用于为升级指南提供命令骨架和 URL 规律。使用时遵循以下规则：

- 本文件只作为命令参考库；若实时升级详情页给出了更具体的命令或参数，以实时页面为准
- 所有版本号均使用**应用版本**，即不带 `v` 的形式，如 `7.1.0`
- 根据部署模式、联网情况、CPU 架构选择对应命令，禁止混用单机与集群命令
- 模板中出现的 `{命名空间}`、`{目标版本号}`、`{目标存储组件版本号}` 等占位内容，最终输出前必须替换成实际值
- 提前准备阶段要汇总**本次升级实际会用到的全部资源**，不要默认只有 HAP 微服务镜像
- 离线文件清单只保留本次升级真正需要的文件，不要把无关离线包一并输出给用户
- 如果线上文档中的附加操作指向其他页面，本文件只提供命令模式参考；最终文档仍应以实际打开后的页面内容为准并展开步骤

## 1. 镜像拉取 / 导入（根据网络情况）

### 联网模式 — 单机
- **AMD64**: `docker pull registry.cn-hangzhou.aliyuncs.com/mdpublic/mingdaoyun-hap:{目标版本号}` 
  - **示例**：`docker pull registry.cn-hangzhou.aliyuncs.com/mdpublic/mingdaoyun-hap:7.1.0` 

- **ARM64**: `docker pull registry.cn-hangzhou.aliyuncs.com/mdpublic/mingdaoyun-hap-arm64:{目标版本号}` 
  - 示例：`docker pull registry.cn-hangzhou.aliyuncs.com/mdpublic/mingdaoyun-hap-arm64:7.1.0` 


### 联网模式 — 集群 (每台微服务节点)
- **AMD64**：`crictl pull registry.cn-hangzhou.aliyuncs.com/mdpublic/mingdaoyun-hap:{目标版本号}` 
  - **通用**: `crictl pull registry.cn-hangzhou.aliyuncs.com/mdpublic/mingdaoyun-hap:7.1.0` 

- **ARM64**: `crictl pull registry.cn-hangzhou.aliyuncs.com/mdpublic/mingdaoyun-hap-arm64:{目标版本号}` 
  - 示例：`crictl pull registry.cn-hangzhou.aliyuncs.com/mdpublic/mingdaoyun-hap-arm64:7.1.0` 

### 离线模式 — 镜像下载链接 URL 规律
- **AMD64**: `https://pdpublic.mingdao.com/private-deployment/offline/mingdaoyun-hap-linux-amd64-{版本号}.tar.gz` 
  - **示例**： `https://pdpublic.mingdao.com/private-deployment/offline/mingdaoyun-hap-linux-amd64-7.1.0.tar.gz` 

- **ARM64**: `https://pdpublic.mingdao.com/private-deployment/offline/mingdaoyun-hap-linux-arm64-{版本号}.tar.gz` 
  - **示例**： `https://pdpublic.mingdao.com/private-deployment/offline/mingdaoyun-hap-linux-arm64-7.1.0.tar.gz` 


### 离线模式 — 导入
- **单机模式**：基于 docker 命令导入离线镜像文件

  ```text
  docker load -i xxx.tar.gz
  ```

  

- **集群模式**：基于 K8s 环境，将离线镜像上传到每个节点，先解压离线镜像文件

  ```
  gunzip -d xxx.tar.gz
  ```

  - 解压后再导入离线镜像

    ```
    ctr -n k8s.io image import xxx.tar
    ```

  

---

## 2. MongoDB 预置数据更新

> 若跨版本升级中包含多次MongoDB 预置数据更新操作，仅需执行最新版本的相应操作即可。

### 单机联网
```bash
bash -c "$(curl -fsSL https://pdpublic.mingdao.com/private-deployment/data/preset_mongodb_docker.sh)" -s {该操作涉及的最新版本号}
```

### 单机离线
1. 提前下载离线文件： 

   ```
   更新脚本下载链接：https://pdpublic.mingdao.com/private-deployment/data/preset_mongodb_docker.sh
   预置数据下载链接：https://pdpublic.mingdao.com/private-deployment/data/preset_mongodb_{该操作涉及的最新版本号}.tar.gz
   ```

2. 将离线文件上传至服务器

3. 执行更新命令: `bash ./preset_mongodb_docker.sh {该操作涉及的最新版本号} ./preset_mongodb_{该操作涉及的最新版本号}.tar.gz`

### 集群联网
```bash
bash -c "$(curl -fsSL https://pdpublic.mingdao.com/private-deployment/data/preset_mongodb_k8s.sh)" -s {该操作涉及的最新版本号} {命名空间}
```

### 集群离线
1. 提前下载离线文件： 

   ```
   更新脚本下载链接：https://pdpublic.mingdao.com/private-deployment/data/preset_mongodb_k8s.sh
   预置数据下载链接：https://pdpublic.mingdao.com/private-deployment/data/preset_mongodb_{该操作涉及的最新版本号}.tar.gz
   ```
2. 将离线文件上传至控制节点服务器

3. **执行更新命令**: `bash ./preset_mongodb_k8s.sh {该操作涉及的最新版本号} {命名空间} ./preset_mongodb_{该操作涉及的最新版本号}.tar.gz`

---

## 3. HAP 微服务升级命令

- **单机模式**: 修改 `docker-compose.yaml` 镜像版本号，在管理器所在路径执行 `bash ./service.sh restartall`
- **集群模式**: 在 `/data/mingdao/script/kubernetes` 目录下执行：
  - 滚动更新: `bash update.sh update hap {目标版本号}`
  - 非滚动更新: 先 `bash stop.sh`，确认 Pod 消失后执行 `bash update.sh update hap {目标版本号}`
  - 如是 ARM64 镜像更新，更新脚本执行时，`hap` 需要加上 `-arm64` 的标识，例如：`bash update.sh update hap-arm64 {目标版本号}`

---

## 4. 存储组件升级

- **联网 AMD64**: `docker pull registry.cn-hangzhou.aliyuncs.com/mdpublic/mingdaoyun-sc:{存储组件镜像版本号}`

- **联网 ARM64**: `docker pull registry.cn-hangzhou.aliyuncs.com/mdpublic/mingdaoyun-sc-arm64:{存储组件镜像版本号}`

- 离线情况下，则提前下载对应镜像，上传到服务器后导入。离线镜像下载链接示例：

  ```
  AMD64: https://pdpublic.mingdao.com/private-deployment/offline/mingdaoyun-sc-linux-amd64-{存储组件镜像版本号}.tar.gz
  ARM64: https://pdpublic.mingdao.com/private-deployment/offline/mingdaoyun-sc-linux-arm64-{存储组件镜像版本号}.tar.gz
  ```

- **升级操作**: 修改 `docker-compose.yaml` 中存储组件镜像版本号，执行 `bash ./service.sh restartall`

---

## 5. 创建 MongoDB 数据库 (认证开启时)

### 单机模式
```bash
# 进入存储组件容器
docker exec -it $(docker ps | grep mingdaoyun-sc | awk '{print $1}') bash

# 容器内登录 (替换用户名和密码)
mongo -u 用户名 -p 密码 --authenticationDatabase admin

# 库创建
use {库名}
db.createUser({ user: "与其他库一致用户名", pwd: "与其他库一致密码", roles: [{ role: "readWrite", db: "{库名}" }] })
```

### 集群模式
```bash
# 使用含 admin 角色的用户登录 (替换连接信息)
mongo -u 用户名 -p 密码 --authenticationDatabase admin

# 库创建
use {库名}
db.createUser({ user: "与其他库一致用户名", pwd: "与其他库一致密码", roles: [{ role: "readWrite", db: "{库名}" }] })
```
