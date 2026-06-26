---
name: HAP升级指南
description: 明道云 HAP 私有部署版本升级专属 skill。只要用户提到 HAP 私有部署升级、跨版本升级、升级注意事项、升级前后附加操作、单机或集群升级步骤、升级文档生成、版本兼容性或架构镜像支持，就必须触发本 skill。即使用户没有明确说"用 hap-upgrade"，只要任务与 HAP 私有部署升级决策或升级执行有关，也要使用本 skill。
---

# HAP 私有部署升级帮助

用于两类任务：

- 回答 HAP 私有部署升级相关咨询
- 生成可执行的升级指南 Markdown 文档，并自动转换为 HTML 文档

核心原则：

- 只依据官方文档和实时页面内容回答，不能凭记忆补全版本细节
- 允许跨版本直接升级，但必须合并跨越路径中的附加操作
- 架构兼容性以 `https://docs-pd.mingdao.com/version` 总表实时标记为唯一准则
- 所有命令必须保持官方原意，不擅自改写命令逻辑

## 何时使用

出现以下任一情形时，必须使用本 skill：

- 用户询问某个 HAP 私有部署版本是否能升级到另一个版本
- 用户询问升级前要做什么、会跨过哪些附加操作、是否支持跨版本升级
- 用户要求输出升级步骤、升级 SOP、升级文档、升级手册
- 用户给出当前版本、目标版本、部署模式、架构、联网情况，请求生成文档
- 用户询问某一目标版本是否支持 `AMD64` 或 `ARM64`

如果任务不是 HAP 私有部署升级，而是一般部署、故障排查、功能使用说明，不使用本 skill。

## 输出类型

根据用户意图，在以下两种输出之间选择：

- 咨询答复：给出结论、依据、风险点、缺失信息
- 升级指南：输出完整 Markdown 文档，然后直接生成 HTML 文档（带侧边目录、代码复制按钮、响应式移动端支持），包含可执行步骤和末尾声明

如果用户明确要求"生成文档""给我一份操作手册""整理成升级指南"，按升级指南处理。否则默认先给咨询答复；当信息齐全时，也可以直接生成文档。

## 产物命名规范

生成升级文档时，产物文件名（不含扩展名）统一使用以下中文命名格式：

```
HAP升级指南-v{当前版本}-to-v{目标版本}-{模式}
```

其中 `{模式}` 为：
- 单机模式：`单机`
- 集群模式：`集群`

**示例**：
- `HAP升级指南-v7.1.1-to-v7.3.2-集群.md`
- `HAP升级指南-v7.1.1-to-v7.3.2-集群.html`
- `HAP升级指南-v6.5.0-to-v7.3.2-单机.md`

**禁止**使用旧的纯英文命名格式（如 `upgrade-guide-v7.1.1-to-v7.3.2-cluster`）。

## 执行顺序

严格按以下顺序执行，不要跳步。

### Step 1. 先收集 5 项关键信息

**重要**：在未收集完以下 5 项关键信息之前，不得开始获取网页或生成文档。

如果用户未提供完整信息，先补齐，再继续：

1. 当前版本，例如 `v7.0.4`
2. 目标版本，例如 `v7.2.0`
3. 部署模式：`单机模式` 或 `集群模式`
4. 架构：`AMD64` 或 `ARM64`
5. 服务器是否可访问互联网

**信息补齐方式**：
- **当 1~2 项缺失时**：直接询问用户提供具体版本号
- **当 3~5 项缺失时**：必须使用 `ask_followup_question` 工具提供选项供用户选择
  - 单独缺失部署模式：提供"单机模式"和"集群模式"两个选项（单选）
  - 单独缺失架构：提供"AMD64"和"ARM64"两个选项（单选）
  - 单独缺失网络：提供"可访问互联网"和"离线环境"两个选项（单选）
  - 同时缺失多项：在同一个 `ask_followup_question` 中提供多个问题，分别列出对应选项

这 5 项不完整时，不得生成最终升级文档，也不得开始获取网页。

### Step 2. 规范化版本号

在后续所有步骤中，同时维护两种版本号形态：

- 应用版本：不带 `v`，用于命令、镜像标签、脚本参数、配置文件
- 显示版本：带 `v`，用于标题、正文说明

规范化规则：

- 用户输入 `v7.1` 时，规范化为应用版本 `7.1.0`，显示版本 `v7.1.0`
- 用户输入 `7.2.0` 时，应用版本保持 `7.2.0`，显示版本补成 `v7.2.0`
- 任何命令、URL、镜像 tag 中都不要带 `v`

### Step 3. 先读取本地参考文件

开始抓取官网前，按需读取这些资源：

- `references/site-structure.md`
  - 只用于了解 URL 规律、页面入口和部署文档位置
  - 不能使用其中的兼容性快照替代实时校验
- `references/merge-rules.md`
  - 用于合并跨版本附加操作
- `references/command-library.md`
  - 用于生成联网 / 离线、单机 / 集群、AMD64 / ARM64 的示例命令
- `assets/upgrade-guide-template-standalone.md` 或 `assets/upgrade-guide-template-cluster.md`
  - 仅在需要生成升级指南时读取
  - 必须先读取模板，再填充文档
  - HTML 由脚本从 Markdown 自动生成，**无需**读取 HTML 模板

### Step 4. 抓取官方实时页面

必须抓取：

- 版本总表：`https://docs-pd.mingdao.com/version`

从总表中识别：

- 当前版本到目标版本之间所有被跨过的版本
  - 不含当前版本
  - 包含目标版本
  - 按从旧到新排序
- 每个版本是否"含附加操作"
- 目标版本在所选架构列中的实时标记

仅对"含附加操作"的版本，再抓取其详情页：

- URL 规律：`https://docs-pd.mingdao.com/upgrade/{应用版本}/`

如果升级详情页中的附加操作只是一个超链接、跳转入口或"详见某文档"的简写，不能停在该页面文本。必须继续打开对应链接，提取实际执行步骤、命令、依赖资源和注意事项，再整理进最终文档。

### Step 5. 做架构校验，必要时立即中止

架构校验是最高优先级。只以总表中的实时标记为准：

- `✅` 才表示支持
- 空白、`❌`、缺失、无法确认，都视为不支持
- 不能因为详情页出现通用命令、arm64 标签页或相似内容，就推断该版本支持该架构

如果目标版本不支持用户指定架构，立即停止生成文档，并直接回复：

`抱歉，目标版本 {显示版本} 官方尚未发布 {架构} 镜像（以发布历史总表为准），升级文档生成任务已中止。`

### Step 6. 提取附加操作并分类

仅从"含附加操作"的版本详情页提取实际需要的操作，分成两类：

- HAP 微服务升级前操作
- HAP 微服务升级后操作

可能遇到的升级前操作示例：

- 镜像命名变更
- 创建 MongoDB 数据库
- 存储组件升级（仅单机）
- 文档预览服务升级
- 重新初始化预置文件
- MongoDB 预置数据更新
- 集群 `service.yaml` 新增服务配置

可能遇到的升级后操作示例：

- 单机进入容器执行 MySQL DDL
- 集群进入 config Pod 执行 MySQL DDL
- 集群进入 config Pod 执行 MongoDB DDL
- 集群进入 config Pod 执行文件初始化命令

这些只是示例，不是完整列表。不要根据"示例类型"虚构步骤，也不要把未列出的线上实际操作忽略掉。详情页没有的，不生成；详情页实际出现但此处未列出的，也必须纳入处理。

### Step 7. 合并跨版本附加操作

如果跨越多个含附加操作的版本，必须读取并遵循 `references/merge-rules.md`。要把它理解为"合并原则文档"，不是"允许操作类型清单"。

特别注意：

- 同类 MongoDB 建库应合并成一次登录和一次整理后的建库列表
- 存储组件只升级到跨越路径要求的最高版本
- MongoDB 预置数据只执行涉及该操作的最新版本命令
- **升级后脚本必须严格按版本从低到高顺序排列**（数字小的版本在前，数字大的在后。例如 v7.2.0 → v7.2.4 → v7.3.0，而非反过来）。这是强制要求，不得按"最新优先"排列。
- **升级后操作的步骤编号结构（单机和集群通用）**：
  - **整体大步骤**使用 h4 标题（进入文档目录导航），格式为 `#### 1. 进入 config Pod 执行脚本`、`#### 2. 来自 v7.2.0：MongoDB 新增索引` 等（使用阿拉伯数字，更易辨识）
    - **单机模式**第一个大步骤为 `#### 1. 进入微服务容器执行脚本`，后续每个版本一个 h4 标题（如 `#### 2. 来自 v7.2.0：MySQL 新增索引`）
    - **集群模式**第一个大步骤为 `#### 1. 进入 config Pod 执行脚本`，后续每个版本一个 h4 标题（如 `#### 2. 来自 v7.2.0：MongoDB 新增索引`）
  - **版本块内部的子操作编号规则**：
    - 若该版本**只有一个**子操作（如只有 MySQL DDL），**不编子序号**，直接显示命令代码块
    - 若该版本**有多个**子操作（如同时有 fileInit 和 MongoDB DDL），使用 `{主步骤号}.{子序号}` 格式，如 `4.1 更新预置文件`、`4.2 MongoDB 新增索引`
    - **子操作标题应简明描述操作内容**（如"MySQL 新增索引"、"MongoDB 新增索引"），不要只写"MySQL DDL"或"MongoDB DDL"
  - **只保留该版本实际存在的操作**，不存在的子操作不要列出
- **同一版本多个同类操作必须合并到一个代码块**：若某版本有多个库的 MongoDB DDL 或多个 MySQL DDL 文件，将所有命令合并到同一个代码块中逐行列出，禁止每个库/每个文件拆成独立代码块
- 集群新增服务配置需要把多版本新增项合并到同一节里
- **同一版本有多个新增服务（如 platformapi + openauthorization）时，必须合并到同一个 YAML 代码块中**，用 `---` 分隔各服务的 Deployment/Service 定义，禁止拆成多个独立代码块、禁止为每个服务单独添加子标题（如"新增 platformapi 服务："加一个代码块，再"新增 openauthorization 服务："加另一个代码块）
- **集群 service.yaml 的删除和新增服务**：在同一个编号条目中先展示删除块、再展示新增块；删除时给出示例结构让执行者知道要删除哪类内容，新增时完整复制官方 yaml 配置（两件事均展示，不拆分成两个独立步骤）。若涉及多个新增服务，新增部分使用**单个 YAML 代码块**包含全部新增服务
- **集群命名空间**：模板中所有命令均使用 `default` 作为默认命名空间，提示语改为"若未使用默认命名空间，请将命令中的 `default` 替换为实际的命名空间（namespace）"
- **集群 fileInit 操作**：必须展示三点说明（参见下方"fileInit 规范"）

**MongoDB 预置数据更新的文档结构要求**：

此操作必须独立成步骤，且在"第一阶段：HAP 微服务升级前操作"中单独列出：

1. **"提前准备"阶段**：
   - 仅说明：MongoDB 预置数据更新脚本将在升级前操作阶段通过联网方式直接拉取执行，无需提前下载
   - **禁止**在此阶段执行预置数据更新命令

2. **"第一阶段：HAP 微服务升级前操作"阶段**：
   - 必须单独列为一个编号步骤，标题为"MongoDB 预置数据更新"
   - 必须包含以下说明：
     - 此操作在**原版本服务运行状态下**执行，无需停机
     - 本次升级路径跨越的含此操作版本列表（如：v6.5.0、v7.0.0、v7.2.0）
     - 按合并规则仅执行最新版本（如：7.2.0）的命令
   - 执行命令示例：
     ```bash
     bash -c "$(curl -fsSL https://pdpublic.mingdao.com/private-deployment/data/preset_mongodb_docker.sh)" -s 7.2.0
     ```

3. **禁止事项**：
   - 禁止将预置数据更新与其他升级前操作合并为一个步骤
   - 禁止在"提前准备"阶段直接执行预置数据更新命令
   - 禁止遗漏"在原版本服务运行状态下执行，无需停机"的说明

**集群模式 fileInit 规范**：

在集群模式升级后操作中，每当出现"更新预置文件"步骤时，**必须**单独列为一个子步骤，包含存储类型判断说明和三种执行情况。

**存储类型判断方式**（必须在文档中提供给执行者）：

通过 `mingdaoyun-file` 镜像版本号判断当前的文件存储模式。

> **注意**：`mingdaoyun-file` 服务以 Docker Swarm 方式部署，需**登录到 Docker Swarm 控制节点**执行以下命令查看版本：

```bash
# 登录到 file 服务器后执行，查看 file 服务当前镜像版本
docker service ls | grep file
# 或查看更详细的镜像信息
docker service inspect --format '{{.Spec.TaskTemplate.ContainerSpec.Image}}' $(docker service ls --filter name=file -q)
```

- **1.x.x 版本**（file v1 模式）：使用内置文件存储 → 选择情况 1
- **2.x.x 版本**（file v2 模式）：使用 file + MinIO 或 file + 外部 S3 对象存储
  - 若对接的是 MinIO，可直接执行 `s3fileInit` 命令 → 选择情况 2
  - 若对接的是外部对象存储（S3 标准协议，如阿里云 OSS、AWS S3 等），需手动下载预置文件包上传 → 选择情况 3

**三种情况展示格式**（必须完整展示）：

```markdown
**{主步骤号}.1 更新预置文件**

根据您的文件存储类型，**三选一**执行（判断方式见上方说明）：

**情况 1：内置文件存储（file v1，mingdaoyun-file 1.x.x）**

```bash
source /entrypoint-cluster.sh && fileInit
```

**情况 2：外部 MinIO / S3 标准对象存储（file v2，mingdaoyun-file 2.x.x）**

```bash
source /entrypoint-cluster.sh && s3fileInit
```

**情况 3：外部文件对象存储（S3 标准协议，如阿里云 OSS、AWS S3 等，file v2，mingdaoyun-file 2.x.x）**

> 此情况需手动下载预置文件包并上传到对象存储 bucket 中，请参考官方文档操作：
> [https://docs-pd.mingdao.com/faq/oss](https://docs-pd.mingdao.com/faq/oss)
```

**禁止**：
- 禁止仅写 `fileInit` 命令而省略三种情况的说明
- 禁止省略存储类型判断说明（执行者必须能通过版本号判断自己属于哪种情况）
- 禁止将三种情况合并成一个代码块内的注释
- 禁止在大代码块中用注释方式嵌入这三点说明

**特殊操作识别规则**：

在提取和合并附加操作时，必须识别以下特殊操作，并按对应章节规范编写：

1. **v5.1.0 镜像拆分操作**：识别到后，按照"特殊升级操作的文档结构要求"章节中"v5.1.0 镜像拆分操作（关键结构变更）"的规范编写
2. **v5.5.0 MongoDB 升级操作**：识别到后，按照"特殊升级操作的文档结构要求"章节中"v5.5.0 MongoDB 升级操作（重大升级）"的规范编写
3. **MongoDB 预置数据更新**：识别到后，按照本章节"MongoDB 预置数据更新的文档结构要求"的规范编写

**特殊升级操作的文档结构要求（v5.1.0 镜像拆分和 v5.5.0 MongoDB 升级）**

以下两个特殊升级操作必须按照官网文档详细编写，禁止简化或概括：

1. **v5.1.0 镜像拆分操作（关键结构变更）**：
   - **触发条件**：当升级路径跨越 v5.1.0 版本时，必须在"第一阶段：HAP 微服务升级前操作"中单独列为一个编号步骤
   - **标题**：必须为"v5.1.0 镜像拆分操作（关键结构变更 ⚠️）"
   - **必须包含的详细内容**：
     a. **重要警告**：明确说明这是"重大的结构性变更"，必须严格按照官网文档步骤调整 docker-compose.yaml 配置
     b. **镜像拆分说明**：
        - 原来的 `mingdaoyun-community` 镜像被拆分为两个独立镜像
        - `mingdaoyun-sc:1.0.0`：负责存储组件相关服务
        - `mingdaoyun-command:node1018-python36`：负责扩展代码块执行环境
        - 需要在 `docker-compose.yaml` 中新增 `sc` 和 `command` 两个服务配置
        - Python 版本升级至 3.6，可能导致旧代码块依赖不兼容
     c. **单机模式调整步骤**（严格按官网文档执行）：
        - 步骤 1：备份当前配置文件（提供完整命令）
        - 步骤 2：修改 `/data/mingdao/script/docker-compose.yaml`：
          * 2.1 在 `app` 服务中追加环境变量引用（提供完整的 YAML 配置示例）
          * 2.2 新增 `sc` 和 `command` 服务（提供完整的 YAML 配置示例）
        - 步骤 3：调整存储组件配置（根据实际情况选择）：
          * 3.1 若自定义存储组件连接地址为 `127.0.0.1`，将其改为 `sc`（提供修改前后对比）
          * 3.2 若启用自定义文件对象存储，将文件存储挂载从 `app` 移动到 `sc`（提供完整 YAML 示例）
          * 3.3 若 `app` 服务中映射了存储组件端口，将端口映射从 `app` 移动到 `sc`（提供完整 YAML 示例）
          * 3.4 若原有代码块依赖库持久化挂载，将挂载从 `app` 移动到 `command`（提供完整 YAML 示例）
        - 步骤 4：完整修改示例（提供完整的 docker-compose.yaml 修改后的关键部分）
        - 步骤 5：验证配置文件格式（提供验证命令）
        - 步骤 6：重启服务并验证（提供完整的重启命令和验证命令）
        - 步骤 7：验证功能（列出需要验证的功能点）
     d. **重要注意事项**（必须列出所有关键点）：
        * 镜像拆分：原 mingdaoyun-community 镜像拆分为 sc（存储计算）和 command（代码执行）两个独立服务
        * Python 版本升级：Python 升级至 3.6，可能导致旧代码块依赖不兼容，需重新安装依赖
        * 存储组件连接：若原配置使用 `127.0.0.1`，必须改为 `sc`
        * 文件挂载调整：所有存储相关挂载需移至 `sc` 服务，代码依赖挂载需移至 `command` 服务
        * 端口映射：存储组件端口映射需从 `app` 移至 `sc`
        * Flink 升级（如已启用）：需升级到版本 `1.17.1.510`，参考官网 Flink 升级指南
   - **要求**：
     * 所有 YAML 配置示例必须完整、可直接复制
     * 所有命令必须提供完整代码块
     * 不能只说"参考官网文档"，必须将官网文档的关键步骤和命令完整展开

2. **v5.5.0 MongoDB 升级操作（重大升级）**：
   - **触发条件**：当升级路径跨越 v5.5.0 版本时，必须在"第一阶段：HAP 微服务升级前操作"中单独列为一个编号步骤
   - **标题**：必须为"v5.5.0 MongoDB 升级操作（重大升级 ⚠️）"
   - **必须包含的详细内容**：
     a. **重要警告**：明确说明这是"重大版本升级"，涉及数据格式变更，必须严格按照以下步骤操作
     b. **MongoDB 升级说明**：
        - 升级范围：从 v3.4 升级到 v4.4
        - 升级方式：参考官方文档 [MongoDB 3.4 升级到 4.4](https://docs-pd.mingdao.com/deployment/docker-compose/standalone/upgrade/mongodb/3.4_4.4)
        - 升级完成后必须重建 `mdwsrows` 库下所有自建索引
     c. **升级前重要提示**（必须在升级步骤前单独列出）：
        - 升级时长：与MongoDB集合数量直接相关
          * 查看集合数量命令：`find /data/mingdao/script/volume/data/mongodb/ -name '*collection*' | wc -l`
          * 参考时长：1万集合约1分钟，10万集合约10分钟，30万集合约30分钟
        - 版本路径：必须逐版本升级：3.4 → 3.6 → 4.0 → 4.2 → 4.4（共4次升级）
        - 数据路径：默认路径为 `/data/mingdao/script/volume/data/mongodb`，如自定义请相应调整
     d. **升级步骤**（严格按照官网文档执行）：
        - **步骤 1**：停止所有服务（提供完整命令）
          ```bash
          # 在管理器根目录执行（通常在 /usr/local/MDPrivateDeployment/）
          bash ./service.sh stopall
          ```
        - **步骤 2**：备份数据（提供检查数据大小和创建备份的完整命令）
          ```bash
          # 检查磁盘空间
          du -sh /data/mingdao/script/volume/data/mongodb

          # 创建备份（备份目录可自定义）
          mkdir -p /backup && tar -zcvf /backup/mongodb3.4_$(date +%Y%m%d%H%M%S).tar.gz /data/mingdao/script/volume/data/mongodb
          ```
        - **步骤 3**：拉取升级辅助镜像（提供完整命令）
          ```bash
          docker pull registry.cn-hangzhou.aliyuncs.com/mdpublic/mingdaoyun-sc-upgrade:1.0.0
          ```
        - **步骤 4**：逐版本升级执行（提供完整的 4 个升级命令，每个命令都必须包含完整的参数）
          ```bash
          # 3.4 到 3.6
          docker run -i --rm -v /data/mingdao/script/volume/data/mongodb:/data/mongodb registry.cn-hangzhou.aliyuncs.com/mdpublic/mingdaoyun-sc-upgrade:1.0.0 <<< 'upgradeMongodb.sh 3.4 3.6'

          # 3.6 到 4.0
          docker run -i --rm -v /data/mingdao/script/volume/data/mongodb:/data/mongodb registry.cn-hangzhou.aliyuncs.com/mdpublic/mingdaoyun-sc-upgrade:1.0.0 <<< 'upgradeMongodb.sh 3.6 4.0'

          # 4.0 到 4.2
          docker run -i --rm -v /data/mingdao/script/volume/data/mongodb:/data/mongodb registry.cn-hangzhou.aliyuncs.com/mdpublic/mingdaoyun-sc-upgrade:1.0.0 <<< 'upgradeMongodb.sh 4.0 4.2'

          # 4.2 到 4.4
          docker run -i --rm -v /data/mingdao/script/volume/data/mongodb:/data/mongodb registry.cn-hangzhou.aliyuncs.com/mdpublic/mingdaoyun-sc-upgrade:1.0.0 <<< 'upgradeMongodb.sh 4.2 4.4'
          ```
        - **步骤 5**：升级成功标志（说明如何判断升级完成）
          * 当看到输出中包含 `newRunVersion: 4.4` 时表示升级成功
          * 其他常见输出：
            - 成功升级：显示 `newRunVersion: 目标版本`
            - 已执行过升级：显示 `exit upgrade`
            - 版本不匹配：显示错误信息，需要重复执行上一个成功的升级命令
        - **步骤 6**：故障处理提示（提供查看详细日志的方法）
          ```bash
          # 如果升级过程中出现版本不匹配错误，需要重复执行上一个成功的升级命令
          # 多次尝试仍失败可查看日志
          cat /data/mingdao/script/volume/data/mongodb/upgrade-xxxx.log
          ```
     e. **重建 mdwsrows 库的自建索引**（必须详细展开，不能一笔带过）：
        - 参考 [MongoDB 索引重建文档](https://docs-pd.mingdao.com/deployment/components/mongodb/reIndex) 执行
        - **第一部分：重建 `mdwsrows` 数据库索引**：
          * 步骤 1：进入存储组件容器（提供完整命令）
            ```bash
            docker exec -it $(docker ps | grep mingdaoyun-sc | awk '{print $1}') bash
            ```
          * 步骤 2：创建脚本文件 `reIndex.js`（提供完整的 JavaScript 脚本内容，不能省略）
            ```javascript
            var targetDbName = "mdwsrows";
            // 集合白名单，白名单中的集合不重建索引
            var collectionWhitelist = ["discussion", "rowrelations", "workSheetRowTopic", "workSheetTopic", "wslogs"];
            // 索引白名单，白名单中的索引不重建
            var indexWhitelist = ["_id_", "idx_ctime", "idx_utime", "uk_rowid", "idx_tp_status", "idx_thirdprimary"];

            // 格式化时间函数
            function formatDateTime() {
                var now = new Date();
                var utc8Time = new Date(now.getTime() + (8 * 60 * 60 * 1000));
                return utc8Time.toISOString().replace('Z', '+08:00');
            }

            // 格式化输出函数
            function printHeader(text) {
                print("\n" + "=".repeat(100));
                print(text);
                print("=".repeat(100));
            }

            function printSection(text) {
                print("\n" + "-".repeat(80));
                print(text);
                print("-".repeat(80));
            }

            function printTimedAction(time, action) {
                print(`\n[${time}] ${action}`);
            }

            // 格式化 JSON，保持一致的缩进
            function formatJSON(obj, indent = 5) {
                return JSON.stringify(obj, null, 2).split('\n').map((line, i) => i === 0 ? line : ' '.repeat(indent) + line).join('\n');
            }

            // 格式化 createIndex 命令
            function formatCreateIndexCommand(collName, key, options) {
                return `db.${collName}.createIndex(${formatJSON(key)},\n     ${formatJSON(options)})`;
            }

            function printCommand(command) {
                print("  └─ Execute:");
                print("     " + command);
            }

            function printCompletion(seconds) {
                print(`  └─ ✓ Completed in ${seconds.toFixed(3)} seconds\n`);
            }

            // 连接到指定数据库
            var targetDb = db.getSiblingDB(targetDbName);
            var startTime = formatDateTime();
            printHeader("MongoDB Index Rebuild Process");
            print(`\n• Start Time: ${startTime}`);
            print(`• Target Database: ${targetDb.getName()}`);

            // 获取所有要重建所有的集合（过滤集合白名单）
            var collections = targetDb.getCollectionNames().filter(function(collName) {
                return !collectionWhitelist.includes(collName) && !collName.startsWith('system.');
            });

            print(`• Total Collections: ${collections.length}`);
            collections.forEach(function(collName, index) {
                var coll = targetDb.getCollection(collName);
                var stats = coll.stats();
                
                // 输出集合信息和进度
                printSection(`Processing Collection [${index + 1}/${collections.length}]: ${collName}`);
                print(`\n• Document Count: ${stats.count}`);
                print(`• Storage Size: ${stats.storageSize} bytes`);
                
                // 获取需要重建的索引（过滤索引白名单）
                var indexes = coll.getIndexes();
                var rebuildIndexes = indexes.filter(function(idx) {
                    return !indexWhitelist.includes(idx.name);
                });
                
                if (rebuildIndexes.length === 0) {
                    print("\n✓ No indexes need to be rebuilt.");
                    return;
                }
                
                // 输出索引重建计划
                print(`\n• Indexes to Rebuild (${rebuildIndexes.length}):`);
                rebuildIndexes.forEach(function(idx) {
                    print(`  ├─ Name: ${idx.name.padEnd(20)}`);
                    print(`  │  Key: ${JSON.stringify(idx.key)}`);
                });
                
                // 重建每个索引
                rebuildIndexes.forEach(function(idx) {
                    var key = idx.key;
                    var options = {};
                    
                    // 复制索引配置（排除系统属性）
                    for (var prop in idx) {
                        if (!["v", "ns", "background"].includes(prop)) {
                            options[prop] = idx[prop];
                        }
                    }
                    options.background = true; // 后台构建索引
                    
                    try {
                        // 删除旧索引
                        var dropTime = formatDateTime();
                        printTimedAction(dropTime, `Dropping Index: ${idx.name}`);
                        printCommand(`db.${collName}.dropIndex("${idx.name}")`);
                        var dropStart = new Date();
                        coll.dropIndex(idx.name);
                        var dropEnd = new Date();
                        printCompletion((dropEnd - dropStart) / 1000);
                        
                        // 创建新索引
                        var createTime = formatDateTime();
                        printTimedAction(createTime, `Creating Index: ${idx.name}`);
                        printCommand(formatCreateIndexCommand(collName, key, options));
                        var createStart = new Date();
                        coll.createIndex(key, options);
                        var createEnd = new Date();
                        printCompletion((createEnd - createStart) / 1000);
                    } catch (e) {
                        print(`  └─ ✗ Error: ${e.message}`);
                        print("     Skipping this index...\n");
                    }
                });
            });

            var endTime = formatDateTime();
            printHeader("Process Completed");
            print(`\n• End Time: ${endTime}`);
            ```
          * 步骤 3：执行脚本（根据 MongoDB 认证配置，提供无认证和有认证两种情况的完整命令）
            ```bash
            # MongoDB 无认证
            nohup mongo mongodb://127.0.0.1:27017/admin --quiet reIndex.js >> reIndex_output.log 2>&1 &

            # MongoDB 有认证（替换 root:password 为实际用户名和密码）
            nohup mongo mongodb://root:password@127.0.0.1:27017/admin --quiet reIndex.js >> reIndex_output.log 2>&1 &
            ```
          * 步骤 4：观察日志（提供观察进度的命令）
            ```bash
            # 实时查看日志输出
            tail -f reIndex_output.log

            # 等待脚本执行完成（日志结尾会输出 "Process Complete" 与 "End Time"）
            ```
        - **第二部分：重建 HAP 系统依赖索引**：
          * 步骤 5：创建脚本文件 `reIndexWithCmd.js`（提供完整的 JavaScript 脚本内容，不能省略）
            ```javascript
            // ====================================================================
            //                          CONFIGURATION
            // ====================================================================
            // 在这里配置您需要重建索引的数据库及其白名单集合
            // 格式: "数据库名": ["要跳过的集合1", "要跳过的集合2..."]
            // 如果某个库下所有集合都需要重建索引，请使用空数组 []
            var targetDatabases = {
                "mdpost": [],
                "MDHistory": []
            };

            // ====================================================================
            // 格式化输出函数 (无需修改)
            function printHeader(text) {
                print("\n" + "=".repeat(100));
                print(text);
                print("=".repeat(100));
            }

            function printSection(text) {
                print("\n" + "-".repeat(80));
                print(text);
                print("-".repeat(80));
            }

            function formatDateTime() {
                var now = new Date();
                var utc8Time = new Date(now.getTime() + (8 * 60 * 60 * 1000));
                return utc8Time.toISOString().replace('Z', '+08:00');
            }

            function formatJSON(obj, indent = 5) {
                if (obj === undefined || obj === null) {
                    return "Not available";
                }
                return JSON.stringify(obj, null, 2).split('\n').map((line, i) => i === 0 ? line : ' '.repeat(indent) + line).join('\n');
            }

            function formatFileSize(bytes) {
                if (bytes === undefined || bytes === null) return "N/A";
                return (bytes / 1024 / 1024).toFixed(2) + " MB";
            }

            function printTimedAction(time, action) {
                print(`\n[${time}] ${action}`);
            }

            function printCompletion(seconds) {
                print(`  └─ ✓ Completed in ${seconds.toFixed(3)} seconds\n`);
            }

            // ====================================================================
            //                          SCRIPT EXECUTION
            // ====================================================================
            var overallStartTime = formatDateTime();
            printHeader("MongoDB Multi-Database Index Rebuild Process Started");
            print(`\n• Overall Start Time: ${overallStartTime}`);
            print(`• Databases to Process: ${Object.keys(targetDatabases).join(', ')}`);

            // 遍历配置中的所有数据库
            for (var dbName in targetDatabases) {
                if (targetDatabases.hasOwnProperty(dbName)) {
                    printHeader(`Processing Database: [ ${dbName} ]`);
                    
                    // 获取目标数据库连接
                    var currentDb = db.getSiblingDB(dbName);
                    
                    // 获取当前数据库的集合黑名单（即需要跳过的集合列表）
                    var excludedCollections = targetDatabases[dbName];
                    print(`\n• Target Database: ${currentDb.getName()}`);
                    print(`• Excluded Collections: ${formatJSON(excludedCollections)}`);
                    
                    // 获取所有集合
                    var collections = currentDb.getCollectionNames();
                    
                    // 过滤掉黑名单中的集合和系统集合
                    var validCollections = collections.filter(collection => 
                        !excludedCollections.includes(collection) && !collection.startsWith('system.')
                    );
                    
                    print(`• Total Collections to Process in this DB: ${validCollections.length}`);
                    
                    if (validCollections.length === 0) {
                        print("\nNo collections to process in this database. Moving to the next one.");
                        continue;
                    }
                    
                    validCollections.forEach(function(collection, index) {
                        try {
                            // 获取集合统计信息
                            var stats = currentDb[collection].stats();
                            
                            // 输出集合信息和进度
                            printSection(`Processing Collection [${index + 1}/${validCollections.length}]: ${collection}`);
                            print(`\n• Collection Statistics:`);
                            print(`  ├─ Storage Size: ${formatFileSize(stats.storageSize)}`);
                            print(`  └─ Document Count: ${(stats.count || 0).toLocaleString()}`);
                            
                            // 获取当前索引信息
                            var indexes = currentDb[collection].getIndexes();
                            print(`\n• Current Indexes (${indexes.length}):`);
                            indexes.forEach(function(idx, i) {
                                const isLast = i === indexes.length - 1;
                                print(`${isLast ? '└' : '├'}─ Name: ${idx.name.padEnd(20)}`);
                                print(`${isLast ? ' ' : '│'}  Key: ${formatJSON(idx.key)}`);
                            });
                            
                            // 执行 reIndex
                            var execTime = formatDateTime();
                            printTimedAction(execTime, "Executing reIndex()");
                            print("  └─ Execute:");
                            print(`     db.getSiblingDB('${dbName}').getCollection('${collection}').reIndex()`);
                            
                            var startExec = new Date();
                            var result = currentDb[collection].reIndex();
                            var endExec = new Date();
                            
                            if (result.ok === 1) {
                                printCompletion((endExec - startExec) / 1000);
                                print("• Operation Results:");
                                print(`  ├─ Previous Index Count: ${result.nIndexesWas}`);
                                print(`  ├─ Current Index Count: ${result.nIndexes}`);
                                if (result.operationTime !== undefined) {
                                    print(`  ├─ Operation Time: ${formatJSON(result.operationTime)}`);
                                } else {
                                    print(`  ├─ Operation Time: Not available (non-replica set deployment)`);
                                }
                                if (result.$clusterTime !== undefined) {
                                    print(`  └─ Cluster Time: ${formatJSON(result.$clusterTime)}`);
                                } else {
                                    print(`  └─ Cluster Time: Not available (non-replica set deployment)`);
                                }
                            } else {
                                print(`  └─ ✗ ReIndex failed: ${formatJSON(result)}`);
                            }
                        } catch (e) {
                            print(`  └─ ✗ Error: ${e.message}`);
                            print("     Skipping this collection...\n");
                        }
                    });
                }
            }

            var overallEndTime = formatDateTime();
            printHeader("Process Completed");
            print(`\n• Overall End Time: ${overallEndTime}`);
            ```
          * 步骤 6：执行脚本（根据 MongoDB 认证配置，提供无认证和有认证两种情况的完整命令）
            ```bash
            # MongoDB 无认证
            nohup mongo mongodb://127.0.0.1:27017/admin --quiet reIndexWithCmd.js >> reIndexWithCmd_output.log 2>&1 &

            # MongoDB 有认证（替换 root:password 为实际用户名和密码）
            nohup mongo mongodb://root:password@127.0.0.1:27017/admin --quiet reIndexWithCmd.js >> reIndexWithCmd_output.log 2>&1 &
            ```
          * 步骤 7：观察日志（提供观察进度的命令）
            ```bash
            # 实时查看日志输出
            tail -f reIndexWithCmd_output.log

            # 等待脚本执行完成（日志结尾会输出 "Process Complete" 与 "End Time"）
            ```
        - **操作前最终确认**（必须列出所有确认项）：
          * 已在测试环境验证过此流程
          * 已对生产数据库进行完整备份
          * 已选择业务低峰期窗口
          * 已通知相关用户可能出现的服务影响
     f. **建议和注意事项**：
        * 在重建索引前，先导出当前所有索引的定义
        * 索引重建可能需要较长时间，取决于数据量和索引数量
        * 重建期间可能影响系统性能，建议在低峰期执行
        * 如果 `mongo` 命令没加入 PATH 变量，需指定绝对路径
   - **要求**：
     * 所有命令必须提供完整代码块，不能省略参数
     * JavaScript 脚本内容必须完整，不能只说"参考官网文档"
     * 必须区分无认证和有认证两种情况
     * 必须提供观察日志的命令
     * 必须详细列出所有升级步骤，不能一笔带过

3. **禁止事项**：
   - 禁止简化或概括这两个特殊升级操作的步骤
   - 禁止只提供参考链接而不展开详细步骤
   - 禁止省略 JavaScript 脚本内容
   - 禁止省略命令中的任何参数
   - 禁止将这两个操作与其他升级前操作合并为一个步骤
   - 禁止遗漏任何警告、注意事项或验证步骤

## 镜像名称规范化规则

在生成升级文档时，必须严格遵守以下镜像名称映射规则，禁止根据官网显示名称推断实际镜像名称：

### 1. 文档预览服务镜像名称

| 官网显示名称 | 实际镜像名称 | 说明 |
|-------------|-------------|------|
| mingdaoyun-doc-preview | mingdaoyun-doc | 文档预览服务主镜像 |
| mingdaoyun-doc-preview-extension | mingdaoyun-ldoc | 文档预览扩展服务镜像 |

**重要**：
- 文档预览相关的镜像名称必须使用实际镜像名称（mingdaoyun-doc 和 mingdaoyun-ldoc）
- 禁止直接使用官网文档中显示的 mingdaoyun-doc-preview 或 mingdaoyun-doc-preview-extension
- 在拉取镜像、修改 docker-compose.yaml 或编写命令时，务必使用正确的实际镜像名称
- **此映射关系为 AI 内部约束，禁止在生成的升级文档中展示给用户**（即不要在文档中出现"实际镜像名称与官网显示名称不同"这类说明，直接使用正确名称即可）

### 2. 其他镜像名称

其他镜像名称（如 mingdaoyun-hap、mingdaoyun-sc、mingdaoyun-command 等）以官方文档为准，按官网显示使用。

## 镜像准备阶段规则

在生成升级文档的"提前准备"章节时，必须遵循以下规则：

### 1. 镜像版本选择原则

当升级路径跨越多个版本，涉及需要提前拉取的镜像时：
- **只拉取目标版本的镜像**，无需拉取中间版本的镜像
- 例如：从 v4.8.1 升级到 v6.2.0，只需要拉取 v6.2.0 版本的镜像，不需要拉取 v5.1.0、v5.5.0 等中间版本的镜像

### 2. 存储组件和文档预览服务镜像

- **存储组件**：直接升级到跨越路径要求的**最高版本**
- **文档预览服务**：直接升级到跨越路径要求的**最高版本**
- 例如：从 v4.8.1 升级到 v6.2.0，存储组件需要升级到 v3.1.0（跨越路径中要求的最高的版本），文档预览需要升级到 v2.0.0

### 3. "提前准备"章节内容规范

"提前准备"章节必须列出：
- HAP 微服务镜像（目标版本）
- 如果升级路径要求存储组件升级，列出对应的存储组件镜像（最高版本）
- 如果升级路径要求文档预览服务升级，列出对应的文档预览镜像（最高版本，使用正确的镜像名称）
- 如果升级路径涉及 MongoDB 预置数据更新，列出对应的预置数据下载链接
- **如果升级路径涉及 fileInit（文件预置数据初始化），离线场景下必须列出对应版本的文件预制包下载链接**（联网场景下 fileInit 命令直接从容器内执行，无需提前下载）
- **如果升级路径涉及 fileInit 且用户可能使用外部对象存储（情况 3），离线场景下必须列出文件预置初始化包（file_init.tar.gz）的下载链接**：`https://pdpublic.mingdao.com/private-deployment/source/{版本号}/file_init.tar.gz`
- 其他官方文档中明确要求提前准备的资源

**禁止**：
- 禁止列出不会用到的镜像或资源
- 禁止列出中间版本的镜像
- 禁止遗漏官方文档中明确要求提前准备的资源

### 4. 文档预览服务离线包下载地址规范

在离线环境升级指南的"提前准备"章节中，必须给出文档预览服务的**实际 tar.gz 文件下载链接**，不得只写文字说明或跳转到离线资源页面。

**AMD64 架构实际下载地址**：

| 服务 | 镜像名称 | 版本 | 实际下载链接 |
|------|---------|------|------------|
| 文档预览服务 | mingdaoyun-doc | 2.0.0 | `https://pdpublic.mingdao.com/private-deployment/offline/mingdaoyun-doc-linux-amd64-2.0.0.tar.gz` |
| 文档预览扩展服务（ldoc，可选） | mingdaoyun-ldoc | 2.0.2 | `https://pdpublic.mingdao.com/private-deployment/offline/mingdaoyun-ldoc-linux-amd64-2.0.2.tar.gz` |

**ARM64 架构下载地址格式**（将 `amd64` 替换为 `arm64`）：
- `https://pdpublic.mingdao.com/private-deployment/offline/mingdaoyun-doc-linux-arm64-2.0.0.tar.gz`
- `https://pdpublic.mingdao.com/private-deployment/offline/mingdaoyun-ldoc-linux-arm64-2.0.2.tar.gz`

**禁止**：
- 禁止在离线场景下只写"请前往离线资源页下载"或"下载地址见官网"等文字说明
- 必须直接在下载表格中填写完整的 `https://` 开头的 tar.gz 文件链接
- 如果官网离线页面有更新的版本，以抓取到的实际页面内容为准，不得使用本规范中过时的版本号

## 生成升级指南时的要求

### 1. 先选模板

根据部署模式读取 Markdown 模板：

- 单机模式：`assets/upgrade-guide-template-standalone.md`
- 集群模式：`assets/upgrade-guide-template-cluster.md`

禁止脱离模板凭记忆重写整个结构。HTML 无需读取模板，由脚本从 MD 自动生成（见 2.3 节）。

### 2. 再填内容

#### 2.1 Markdown 文档结构要求

Markdown 是唯一事实来源，HTML 从它自动生成，因此 Markdown 内容必须完整、正确。

**文档必须包含以下章节（按顺序）**：
1. 标题（`# HAP 升级指南（单机/集群模式）`）
2. 版本信息表格（两列表格：升级路径、部署模式、架构、网络、生成日期）
3. 提前准备
4. 升级前准备（必须包含"授权有效期检查"和"前端二开注意事项"两个小节，分别列为第一项和第二项，即便无其他步骤也要保留此两节）
5. 升级步骤
   - 第一阶段：HAP 微服务升级前操作
   - 第二阶段：升级微服务
   - 第三阶段：HAP 微服务升级后操作
6. 升级后验证
7. 参考文档
8. 底部声明（AI 生成声明）

单机模式还包含"异常情况排查"章节；集群模式不包含此章节。

#### 2.2 Markdown 文档填充规则

填充 Markdown 文档时，遵守以下规则：

- 文档顶部信息必须补全升级路径、部署模式、架构、网络情况、生成日期，**必须使用两列 Markdown 表格格式**（禁止使用行内加粗键值对格式，因为会挤在一起）。格式示例：
  ```markdown
  | 项目 | 内容 |
  |------|------|
  | **升级路径** | v4.8.1 → v7.2.1 |
  | **部署模式** | 单机模式（Docker Compose） |
  | **服务器架构** | AMD64 |
  | **服务器网络** | 可访问互联网 |
  | **文档生成日期** | 2026-03-30 |
  ```
- 备份步骤必须保留在最前面
- "提前准备"必须汇总**本次升级实际会用到的全部资源**，不限于 HAP 微服务镜像。只要升级步骤或附加操作中会用到镜像、离线包、脚本、预置数据、额外组件资源，都应提前列出
- 如果某一阶段完全没有步骤，删除整节，不保留占位提示
- 所有命令必须给出完整代码块，不能写"同上""省略""按前文类似处理"
- 生成的是面向执行者的文档，不要把模型的推理过程写进正文
- **禁止**在产物中出现"不要预设资源类型已经列全""如本次升级还涉及其他离线镜像或资源，请继续补充"等面向 AI 自身的指令性免责文本，这些仅作为内部约束，不输出给用户
- 如果线上文档把附加操作写成超链接或跳转说明，最终输出时必须把超链接背后的实际步骤展开写入对应章节，不能只给一个链接让用户自己点进去
- **微服务升级必须包含 ENV_APP_VERSION 变量值设置**：
  - **单机模式**：在"第二阶段：升级微服务"的"修改镜像版本号"步骤中，必须同时说明：
    * 修改 `docker-compose.yaml` 中的 HAP 镜像版本号
    * 确保 `ENV_APP_VERSION` 环境变量的值与微服务镜像版本号保持一致（例如：微服务版本是 7.1.1，`ENV_APP_VERSION` 的值也应设为 7.1.1）
    * 提供完整的修改示例：
      ```yaml
      # 修改前
      image: registry.cn-hangzhou.aliyuncs.com/mdpublic/mingdaoyun-hap:4.8.1
      environment:
        ENV_APP_VERSION: "4.8.1"

      # 修改后
      image: registry.cn-hangzhou.aliyuncs.com/mdpublic/mingdaoyun-hap:6.2.0
      environment:
        ENV_APP_VERSION: "6.2.0"
      ```
  - **集群模式**：在"第二阶段：升级微服务"的升级步骤中，必须同时说明：
    * `update.sh update hap {目标版本号}` 命令会自动更新镜像版本号
    * `ENV_APP_VERSION` 环境变量也会通过 update.sh 自动更新为相同的版本号
    * 如果需要手动确认，可以查看部署的 yaml 文件或 Pod 环境变量进行验证

- **升级前准备中必须包含以下两个注意事项小节**（按顺序列为第一项和第二项）：

  **第一项：授权有效期检查**
  - **位置**：放置在"升级前准备"章节的**第一项**（编号为第 1 步）
  - **标题**：`授权有效期检查`
  - **必须标注重要提示**，使用 `> ⚠️` 引用块
  - **必须包含以下说明**：
    * 请确保您的授权密钥仍在"升级服务"有效期内
    * 若目标主版本的发布日期晚于授权到期日，强行升级将触发系统受限提示，并导致授权自动降级为免费版
    * 建议在升级前确认版本发布日期与授权期限的匹配情况
    * 若授权即将到期或已过期，请联系明道云商务团队续期后再执行升级
  - **固定提示语**（必须包含）：
    ```
    > ⚠️ **重要提示**：请确保您的授权密钥仍在"升级服务"有效期内。若目标主版本的发布日期晚于授权到期日，强行升级将触发系统受限提示，并导致授权自动降级为免费版。建议在升级前确认版本发布日期与授权期限的匹配情况。
    ```

  **第二项：前端二次开发注意事项**
  - **位置**：放置在"升级前准备"章节的**第二项**（编号为第 2 步）
  - **标题**：`前端二次开发注意事项`
  - **必须包含以下说明**：
    * 若系统中存在前端二次开发（即有基于 HAP 前端源码进行过定制开发），升级后前端代码可能与新版本存在冲突
    * 需要**前端二开负责同事**在升级前或升级后（根据实际情况确定时机），执行以下操作：
      1. 拉取最新的前端二开基础代码（通常为官方前端仓库对应目标版本的分支或 tag）
      2. 将自定义的二开代码合并（merge）进最新基础代码，处理可能存在的冲突
      3. 构建并发布更新后的前端服务，使新版本前端生效
    * 若系统中**没有**前端二次开发，忽略本注意事项
  - **固定提示语**（必须包含）：
    ```
    > ⚠️ **注意**：如有前端二次开发，请联系前端二开负责同事确认此操作已完成，否则可能导致升级后前端功能异常。
    ```

#### 2.3 HTML 文档生成

**MD 是唯一事实来源，HTML 完全由 AI 直接生成。不依赖任何本地 Python 脚本，也不需要安装任何依赖。**

生成 Markdown 文档后，AI 直接读取 MD 文件内容，按以下规范转换为 HTML，并用 `write_to_file` 写出 `.html` 文件。

---

**HTML 模板结构（严格遵守）**：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{文档标题}</title>
  <style>
    /* 见下方 CSS 规范 */
  </style>
</head>
<body>
<button class="sidebar-toggle">◀ 收起目录</button>
<div class="sidebar-overlay"></div>
<div class="layout">
  <nav class="sidebar">
    <button class="sidebar-close" title="关闭目录">✕</button>
    <div class="sidebar-title">文档目录</div>
    <ul class="toc" id="toc"></ul>
  </nav>
  <div class="main">
    <div class="content">
      {正文 HTML 内容}
    </div>
  </div>
</div>
<script>
  /* 见下方 JS 规范 */
</script>
</body>
</html>
```

---

**CSS 规范（完整内嵌，不省略）**：

```css
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
               "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  font-size: 16.5px; line-height: 1.75; color: #24292f; background: #f6f8fa;
}

/* ========= 侧边栏折叠按钮 ========= */
.sidebar-toggle {
  display: none;
  position: fixed; top: 12px; left: 12px; z-index: 200;
  background: #0969da; color: #fff; border: none; border-radius: 6px;
  padding: 6px 12px; font-size: 14px; cursor: pointer; box-shadow: 0 2px 8px rgba(0,0,0,.2);
}
.sidebar-toggle:hover { background: #0752b3; }

/* ========= 布局 ========= */
.layout { display: flex; min-height: 100vh; }

.sidebar {
  width: 260px; flex-shrink: 0; background: #fff;
  border-right: 1px solid #d0d7de; position: fixed; top: 0; left: 0;
  height: 100vh; overflow-y: auto; padding: 24px 0;
  transition: transform .25s ease; z-index: 100;
}
.sidebar.collapsed { transform: translateX(-260px); }

.sidebar-title {
  font-size: 13px; font-weight: 700; text-transform: uppercase;
  letter-spacing: .6px; color: #57606a; padding: 0 20px 10px;
  border-bottom: 1px solid #d0d7de; margin-bottom: 12px;
}
.toc { list-style: none; padding: 0; }
.toc li a {
  display: block; padding: 4px 20px; font-size: 14px; color: #24292f;
  text-decoration: none; white-space: nowrap; overflow: hidden;
  text-overflow: ellipsis; border-left: 3px solid transparent;
}
.toc li a:hover { background: #f6f8fa; color: #0969da; }
.toc li a.active { border-left-color: #0969da; color: #0969da; font-weight: 600; background: #f0f6ff; }
.toc li.h3 a { padding-left: 34px; font-size: 14px; color: #57606a; }
.toc li.h4 a { padding-left: 48px; font-size: 13px; color: #57606a; }
.toc li.h5 a { padding-left: 62px; font-size: 12.5px; color: #57606a; }

/* ========= 目录折叠 ========= */
.toc-section > .toc-header {
  display: flex; align-items: center; gap: 2px;
}
.toc-toggle {
  background: none; border: none; font-size: 11px; cursor: pointer;
  padding: 0; width: 16px; height: 16px; color: #57606a;
  flex-shrink: 0; transition: transform .15s;
  display: inline-flex; align-items: center; justify-content: center;
  border-radius: 3px; line-height: 1;
}
.toc-toggle:hover { background: #f6f8fa; }
.toc-section.collapsed > .toc-header .toc-toggle { transform: rotate(-90deg); }
.toc-children { list-style: none; padding: 0; }
.toc-section.collapsed > .toc-children { display: none; }

.main { flex: 1; margin-left: 260px; background: #f6f8fa; min-width: 0; transition: margin-left .25s ease; }
.main.expanded { margin-left: 0; }
.content {
  max-width: 980px; margin: 0 auto; padding: 36px 48px 60px;
  background: #fff; border-left: 1px solid #d0d7de;
  border-right: 1px solid #d0d7de; min-height: 100vh;
}

/* ========= 遮罩（移动端点击侧边栏外关闭） ========= */
.sidebar-overlay {
  display: none; position: fixed; inset: 0; background: rgba(0,0,0,.35); z-index: 99;
}
.sidebar-overlay.active { display: block; }

h1 { font-size: 31px; font-weight: 700; margin: 0 0 16px; color: #1f2328; }
h2 { font-size: 24px; font-weight: 600; margin: 36px 0 14px; padding-bottom: 8px; border-bottom: 1px solid #d0d7de; color: #1f2328; }
h3 { font-size: 20px; font-weight: 600; margin: 28px 0 10px; color: #1f2328; }
h4 { font-size: 17.5px; font-weight: 600; margin: 22px 0 8px; color: #1f2328; }
h5 { font-size: 15.5px; font-weight: 600; margin: 18px 0 6px; color: #1f2328; }

p { margin-bottom: 14px; color: #24292f; }
ul, ol { margin: 8px 0 14px 24px; color: #24292f; }
li { margin-bottom: 5px; line-height: 1.7; }
li > ul, li > ol { margin: 4px 0 4px 20px; }

blockquote { border-left: 4px solid #d0d7de; margin: 16px 0; padding: 4px 16px; color: #57606a; }
blockquote p { margin-bottom: 4px; }

/* 特别注意高亮样式 */
blockquote.attention {
  border-left: 4px solid #cf222e; background: #fff1f0; padding: 12px 16px; color: #1f2328; border-radius: 0 6px 6px 0;
}
blockquote.attention p { color: #1f2328; margin-bottom: 4px; }

table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 15.5px; }
th, td { border: 1px solid #d0d7de; padding: 8px 12px; text-align: left; }
th { background: #f6f8fa; font-weight: 600; }
tr:nth-child(even) td { background: #f6f8fa; }

/* 版本信息表格（文档第一个表格）特殊样式 */
table.meta-block { border-radius: 8px; overflow: hidden; margin-bottom: 28px; }
table.meta-block th { color: #57606a; font-size: 14px; text-transform: uppercase; letter-spacing: .4px; width: 140px; }

code {
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
  font-size: 93%; background: #eef0f3; border: 1px solid #d0d7de;
  border-radius: 4px; padding: 2px 5px; color: #cf222e;
}

.code-block {
  position: relative; margin: 16px 0; border-radius: 6px;
  overflow: hidden; border: 1px solid #d0d7de;
}
.code-block pre {
  background: #f6f8fa; color: #24292f; margin: 0;
  padding: 16px; overflow-x: auto;
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
  font-size: 15px; line-height: 1.5;
}
.code-block pre code { background: none; border: none; padding: 0; color: inherit; font-size: inherit; border-radius: 0; }
.code-block::before {
  content: attr(data-lang); position: absolute; top: 8px; left: 12px;
  font-size: 12px; font-family: "SFMono-Regular", Consolas, monospace;
  color: #57606a; text-transform: uppercase; letter-spacing: .5px; pointer-events: none;
}
.code-block[data-lang]:not([data-lang=""]) pre { padding-top: 32px; }

.copy-btn {
  position: absolute; top: 6px; right: 8px; padding: 3px 10px;
  background: rgba(175,184,193,.8); color: #24292f;
  border: 1px solid rgba(27,31,35,.15); border-radius: 4px; cursor: pointer;
  font-size: 13px; font-weight: 500; transition: background .15s, color .15s; z-index: 2;
}
.copy-btn:hover { background: rgba(175,184,193,1); }
.copy-btn.copied { background: #2ea44f; color: #fff; border-color: transparent; }

/* ========= 表格内 URL 复制按钮 ========= */
td.url-cell {
  position: relative; max-width: 480px; white-space: nowrap;
}
td.url-cell .url-text-wrap {
  display: block; overflow-x: auto; white-space: nowrap;
  padding-right: 52px; padding-top: 1px;
}
td.url-cell .url-text-wrap::-webkit-scrollbar { height: 3px; }
td.url-cell .url-text-wrap::-webkit-scrollbar-thumb { background: #d0d7de; border-radius: 2px; }
.url-copy-btn {
  position: absolute; top: 7px; right: 8px;
  padding: 2px 8px;
  background: rgba(175,184,193,.8); color: #24292f;
  border: 1px solid rgba(27,31,35,.15); border-radius: 4px; cursor: pointer;
  font-size: 12px; font-weight: 500; transition: background .15s, color .15s; z-index: 2;
}
.url-copy-btn:hover { background: rgba(175,184,193,1); }
.url-copy-btn.copied { background: #2ea44f; color: #fff; border-color: transparent; }

/* ========= 侧边栏关闭按钮（桌面端和移动端均显示） ========= */
.sidebar-close {
  display: block; position: absolute; top: 10px; right: 10px;
  background: #fff; border: 1px solid #d0d7de; font-size: 20px; color: #57606a;
  cursor: pointer; padding: 2px 6px; border-radius: 4px;
  box-shadow: 0 1px 3px rgba(27,31,35,.1);
  width: 28px; height: 28px; line-height: 1;
  display: flex; align-items: center; justify-content: center;
}
.sidebar-close:hover { background: #f6f8fa; color: #cf222e; border-color: #cf222e; }

hr { border: none; border-top: 1px solid #d0d7de; margin: 28px 0; }
a { color: #0969da; text-decoration: none; }
a:hover { text-decoration: underline; }

/* ========= 响应式：平板及移动端 ========= */
@media (max-width: 768px) {
  .sidebar-toggle { display: block; }

  .sidebar {
    transform: translateX(-260px);
    box-shadow: 2px 0 16px rgba(0,0,0,.15);
  }
  .sidebar.open {
    transform: translateX(0);
  }

  .main { margin-left: 0; }
  .main.expanded { margin-left: 0; }

  .content {
    padding: 52px 16px 40px;
    border-left: none; border-right: none;
  }

  h1 { font-size: 24px; }
  h2 { font-size: 20px; }
  h3 { font-size: 17.5px; }

  table { font-size: 14px; display: block; overflow-x: auto; }
  td.url-cell { max-width: 280px; }

  .code-block pre { font-size: 14px; }
}
```

---

**JS 规范（完整内嵌，不省略）**：

```javascript
// 代码块复制按钮
document.querySelectorAll('.copy-btn').forEach(function(btn) {
  btn.addEventListener('click', function() {
    var pre = btn.closest('.code-block').querySelector('pre');
    navigator.clipboard.writeText(pre.innerText).then(function() {
      btn.textContent = '已复制';
      btn.classList.add('copied');
      setTimeout(function() { btn.textContent = '复制'; btn.classList.remove('copied'); }, 1500);
    });
  });
});

// 表格内 URL 复制按钮（自动为包含 https:// 的单元格添加，按钮固定右上角）
(function() {
  document.querySelectorAll('table td').forEach(function(td) {
    var text = td.textContent;
    if (text.indexOf('https://') === -1 && text.indexOf('http://') === -1) return;
    td.classList.add('url-cell');
    // 将已有内容包裹在可滚动容器中，使按钮不被卷走
    var wrap = document.createElement('span');
    wrap.className = 'url-text-wrap';
    while (td.firstChild) wrap.appendChild(td.firstChild);
    td.appendChild(wrap);
    var btn = document.createElement('button');
    btn.className = 'url-copy-btn';
    btn.textContent = '复制';
    btn.addEventListener('click', function(e) {
      e.stopPropagation();
      var url = wrap.textContent.trim();
      navigator.clipboard.writeText(url).then(function() {
        btn.textContent = '已复制';
        btn.classList.add('copied');
        setTimeout(function() { btn.textContent = '复制'; btn.classList.remove('copied'); }, 1500);
      });
    });
    td.appendChild(btn);
  });
})();

// 侧边栏折叠（桌面端按钮 + 移动端遮罩 + 关闭按钮）
(function() {
  var sidebar = document.querySelector('.sidebar');
  var main = document.querySelector('.main');
  var toggle = document.querySelector('.sidebar-toggle');
  var overlay = document.querySelector('.sidebar-overlay');
  var closeBtn = document.querySelector('.sidebar-close');
  if (!sidebar || !toggle) return;

  var isMobile = function() { return window.innerWidth <= 768; };

  function closeSidebar() {
    if (isMobile()) {
      sidebar.classList.remove('open');
      if (overlay) overlay.classList.remove('active');
      toggle.textContent = '☰ 目录';
    } else {
      sidebar.classList.add('collapsed');
      if (main) main.classList.add('expanded');
      toggle.textContent = '▶ 展开目录';
      toggle.style.display = 'block';  // 折叠后显示 toggle，方便重新打开
    }
  }

  toggle.addEventListener('click', function() {
    if (isMobile()) {
      var isOpen = sidebar.classList.contains('open');
      if (isOpen) {
        closeSidebar();
      } else {
        sidebar.classList.add('open');
        if (overlay) overlay.classList.add('active');
        toggle.textContent = '✕ 关闭';
      }
    } else {
      var isCollapsed = sidebar.classList.contains('collapsed');
      if (isCollapsed) {
        sidebar.classList.remove('collapsed');
        if (main) main.classList.remove('expanded');
        toggle.textContent = '◀ 收起目录';
        toggle.style.display = 'none';  // 展开后隐藏 toggle，避免与正文内容重叠
      } else {
        closeSidebar();
      }
    }
  });

  // 侧边栏内关闭按钮
  if (closeBtn) {
    closeBtn.addEventListener('click', closeSidebar);
  }

  // 点击遮罩关闭侧边栏（移动端）
  if (overlay) {
    overlay.addEventListener('click', closeSidebar);
  }

  // 初始化：桌面端 sidebar 展开时隐藏 toggle，移动端始终显示
  if (!isMobile() && !sidebar.classList.contains('collapsed')) {
    toggle.style.display = 'none';
  }
  toggle.textContent = isMobile() ? '☰ 目录' : '◀ 收起目录';

  // 窗口尺寸变化时重置状态
  window.addEventListener('resize', function() {
    if (!isMobile()) {
      sidebar.classList.remove('open');
      if (overlay) overlay.classList.remove('active');
      // 桌面端：sidebar 展开则隐藏 toggle，折叠则显示 toggle
      toggle.style.display = sidebar.classList.contains('collapsed') ? 'block' : 'none';
    } else {
      sidebar.classList.remove('collapsed');
      if (main) main.classList.remove('expanded');
      toggle.style.display = 'block';
    }
    toggle.textContent = isMobile() ? '☰ 目录' : '◀ 收起目录';
  });
})();

// 目录生成（含折叠按钮） & 滚动高亮
(function() {
  var headings = document.querySelectorAll('.content h2, .content h3, .content h4, .content h5');
  var toc = document.getElementById('toc');
  if (!toc || headings.length === 0) return;
  headings.forEach(function(h, idx) {
    if (!h.id) h.id = 'heading-' + idx;
  });

  var currentSection = null;
  var currentChildren = null;

  headings.forEach(function(h) {
    var level = h.tagName.toLowerCase();
    var a = document.createElement('a');
    a.href = '#' + h.id;
    a.textContent = h.textContent;

    if (level === 'h2') {
      currentSection = document.createElement('li');
      currentSection.className = 'toc-section';
      var header = document.createElement('div');
      header.className = 'toc-header';
      var toggle = document.createElement('button');
      toggle.className = 'toc-toggle';
      toggle.textContent = '▾';
      header.appendChild(toggle);
      header.appendChild(a);
      currentSection.appendChild(header);
      currentChildren = document.createElement('ul');
      currentChildren.className = 'toc-children';
      currentSection.appendChild(currentChildren);
      toc.appendChild(currentSection);
    } else {
      if (currentChildren) {
        var li = document.createElement('li');
        li.className = level;
        li.appendChild(a);
        currentChildren.appendChild(li);
      }
    }
  });

  // 折叠按钮事件
  document.querySelectorAll('.toc-toggle').forEach(function(toggle) {
    toggle.addEventListener('click', function(e) {
      e.stopPropagation();
      toggle.closest('.toc-section').classList.toggle('collapsed');
    });
  });

  // 滚动高亮
  var allLinks = toc.querySelectorAll('a');
  function onScroll() {
    var scrollY = window.scrollY + 80;
    var active = null;
    headings.forEach(function(h) { if (h.offsetTop <= scrollY) active = h.id; });
    allLinks.forEach(function(a) { a.classList.toggle('active', a.getAttribute('href') === '#' + active); });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // 点击目录链接后瞬间跳转到目标位置，不自动隐藏侧边栏
  allLinks.forEach(function(a) {
    a.addEventListener('click', function(e) {
      e.preventDefault();
      var target = document.getElementById(a.getAttribute('href').substring(1));
      if (target) {
        target.scrollIntoView({ behavior: 'auto' });
      }
    });
  });
})();
```

---

**Markdown → HTML 转换规则（AI 执行）**：

| Markdown 语法 | HTML 输出 |
|---------------|-----------|
| `# 标题` | `<h1 id="...">标题</h1>` |
| `## 标题` | `<h2 id="...">标题</h2>`（id 由标题文字生成，用于目录锚点） |
| `### / ####` | `<h3> / <h4>`（同上） |
| `` ` `` 行内代码 `` ` `` | `<code>内容</code>` |
| ` ```lang\n代码\n``` ` | `<div class="code-block" data-lang="lang"><pre><code>代码内容</code></pre><button class="copy-btn">复制</button></div>` |
| `**粗体**` | `<strong>粗体</strong>` |
| `- 列表项` | `<ul><li>列表项</li></ul>` |
| `1. 列表项` | `<ol><li>列表项</li></ol>` |
| `> 引用` | `<blockquote><p>引用</p></blockquote>` |
| `> ⚠️ **特别注意**：...` / `> ⚠️ **注意**：...` | `<blockquote class="attention"><p>⚠️ <strong>特别注意/注意</strong>：...</p></blockquote>`（醒目红底样式） |
| 表格 | `<table>` 标准结构，首个表格额外加 `class="meta-block"` |
| `[文字](url)` | `<a href="url">文字</a>` |
| `---` | `<hr>` |
| 空行分段 | `<p>段落内容</p>` |

**代码块特别要求**（最关键，不得出错）：
- 所有代码内容**必须原样保留**，不得截断、省略或改写，不论代码有多长（包括 4000+ 字符的 JS 脚本）
- `<` `>` `&` `"` 需 HTML 转义为 `&lt;` `&gt;` `&amp;` `&quot;`
- `data-lang` 属性值为代码块语言标识（如 `bash`、`yaml`、`javascript`），无语言标识时写 `data-lang=""`
- **禁止**用 `...` 或 `省略` 代替代码内容
- **禁止**在代码块中插入换行符或修改缩进

**标题 id 生成规则**：取标题文字，保留中文和字母数字，空格转 `-`，其余字符删除，全部小写。例：`第一阶段：HAP 微服务升级前操作` → `id="第一阶段hap-微服务升级前操作"`

**禁止事项**：
- 禁止手动填充任何旧 HTML 模板
- 禁止省略或截断任何代码块内容
- 禁止在输出 HTML 前将文件交给用户（必须先写入文件）

### 3. 严格裁剪模板块

模板中的可选段落必须清理干净：

- 联网场景：只保留联网版本的段落，删除离线版本的段落
- 离线场景：只保留离线版本的段落，删除联网版本的段落
- 最终输出中不得保留"以下二选一""按场景保留其一""删除不适用内容"之类模板提示，也不得保留 `{...}` 占位说明或模板注释语

### 4. 命令与内容来源

生成命令时，优先顺序如下：

1. 当前抓取到的官方升级详情页原文
2. `references/command-library.md`
3. 模板中的固定结构

如果三者出现冲突，以官方实时页面为准；但不要擅自拼接出官网没有表达过的新命令逻辑。

### 5. 针对不同部署模式的硬规则

- 集群模式不能生成"存储组件升级"步骤，除非官方实时页面明确要求
- 单机模式不能生成 `kubectl`、`crictl`、`ctr` 命令
- 集群模式不能生成 `docker exec`、`service.sh restartall` 这类单机命令
- ARM64 时，涉及镜像名或更新命令时，必须检查是否需要 `-arm64`

## 仅做咨询答复时的要求

如果用户只是咨询，不一定要输出完整升级指南，但仍要遵循：

- 先补齐缺失信息，或明确指出因为哪些信息缺失暂时无法下结论
- 涉及具体版本结论时，必须先抓取官方页面再回答
- 回答里要明确区分"已确认事实"和"基于缺失信息的待确认项"
- 如果判断结果依赖架构支持或是否联网，要把这一点直接说清楚

## 禁止事项

禁止出现以下行为：

- 凭训练记忆回答具体版本是否支持某架构
- 直接使用 `references/site-structure.md` 中的兼容性快照当作结论
- 杜撰官网未出现的升级步骤、版本路径、下载地址或脚本命令
- 在最终文档中保留模板占位符、AI 推理说明、合并逻辑说明
- 在信息不完整时伪造缺失参数

## 最终检查清单

在输出前，自检以下项目：

- 已确认 5 项前置信息
- 版本号已同时规范化为应用版本和显示版本
- 已抓取 `/version` 实时页面
- 已按目标架构完成兼容性校验
- 已收集跨越路径中的含附加操作版本
- 已按 `merge-rules.md` 合并
- 需要生成文档时，已读取正确模板
- 已按网络场景裁剪模板中的可选段落
- 已把升级详情页或其跳转链接中的实际附加操作完整展开到正文
- 最终内容中无占位符、无逻辑注释、无残留条件标记
- 文末已追加声明

## 固定声明

无论输出咨询答复还是升级指南，只要给出与升级执行相关的正式结论，末尾都附加以下声明：

```md
---
💡 声明：内容由 AI 生成。尽管已努力确保信息的合理性，但 AI 模型仍可能产生不准确、过时或存在偏差的内容。请在执行关键操作前，务必对照[官方文档](https://docs-pd.mingdao.com)进行核实校验。
```
