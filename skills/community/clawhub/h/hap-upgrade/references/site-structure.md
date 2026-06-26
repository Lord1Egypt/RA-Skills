# 明道云私有部署文档网站结构参考

> [!CAUTION]
> 本文件仅用于了解 URL 规律，其内部表格中的 ✅/❌ 标记极易过时。
> **严禁**直接将本文件中的兼容性数据作为生成指南的依据。
> **必须**以 `https://docs-pd.mingdao.com/version` 的实时页面内容为唯一准则。


**基础 URL**：`https://docs-pd.mingdao.com`
**框架**：Docusaurus（URL 规律性强，路径即页面）
**语言**：中文（默认）/ 英文（路径加 `/en/` 前缀，如 `/en/version`）

---

## 顶层导航页面

| 页面 | URL |
|------|-----|
| 首页 | `/` |
| 路线图 | `/roadmap` |
| 技术白皮书 | `/whitepaper` |
| 版本发布历史 ⭐ | `/version` |
| 镜像命名变更历史 | `/imagenamehistory` |
| 软件物料清单 | `/sbom` |
| 平台版说明 | `/apc` |

---

## 版本升级说明页

**URL 规律**：`/upgrade/{主版本}.{次版本}.{修复版本}/`

| 版本 | URL | 发布日期 | 含附加操作 | AMD64 | ARM64 |
|------|-----|----------|------------|-------|-------|
| v7.2.0 | `/upgrade/7.2.0/` | 2026-03-11 | ✅ | ✅ | ❌ |
| v7.1.1 | `/upgrade/7.1.1/` | 2026-02-06 | ❌ | ✅ | ✅ |
| v7.1.0 | `/upgrade/7.1.0/` | 2026-01-26 | ✅ | ✅ | ✅ |
| v7.0.4 | `/upgrade/7.0.4/` | 2026-01-20 | ❌ | ✅ | ✅ |
| v7.0.3 | `/upgrade/7.0.3/` | 2026-01-13 | ❌ | ✅ | ✅ |
| v7.0.2 | `/upgrade/7.0.2/` | 2026-01-04 | ❌ | ✅ | ✅ |
| v7.0.1 | `/upgrade/7.0.1/` | 2025-12-25 | ❌ | ✅ | ✅ |
| v7.0.0 | `/upgrade/7.0.0/` | 2025-12-16 | ✅ | ✅ | ✅ |
| v6.5.6 | `/upgrade/6.5.6/` | 2025-10-28 | ❌ | ✅ | ✅ |
| v6.5.5 | `/upgrade/6.5.5/` | 2025-10-15 | ❌ | ✅ | ✅ |
| v6.5.4 | `/upgrade/6.5.4/` | 2025-09-29 | ❌ | ✅ | ✅ |
| v6.5.3 | `/upgrade/6.5.3/` | 2025-09-18 | ❌ | ✅ | ✅ |
| v6.5.2 | `/upgrade/6.5.2/` | 2025-09-11 | ❌ | ✅ | ✅ |
| v6.5.1 | `/upgrade/6.5.1/` | 2025-09-04 | ❌ | ✅ | ✅ |
| v6.5.0 | `/upgrade/6.5.0/` | 2025-08-25 | ✅ | ✅ | ❌ |
| v6.4.0 | `/upgrade/6.4.0/` | 2025-07-21 | ✅ | ✅ | ✅ |
| v6.3.3 | `/upgrade/6.3.3/` | 2025-07-09 | ❌ | ✅ | ✅ |
| v6.3.2 | `/upgrade/6.3.2/` | 2025-07-02 | ❌ | ✅ | ✅ |
| v6.3.1 | `/upgrade/6.3.1/` | 2025-06-23 | ❌ | ✅ | ✅ |
| v6.3.0 | `/upgrade/6.3.0/` | 2025-06-10 | ✅ | ✅ | ✅ |

> ⚠️ 此表基于文档网站快照整理，生成指南前必须重新通过 `web_fetch /version` 确认最新版本列表，以防有新版本发布。

---

## 部署运维文档

### 单机模式（Docker Compose）

| 页面 | URL |
|------|-----|
| 概览 | `/deployment/platform` |
| 数据备份 | `/deployment/docker-compose/standalone/data/backup` |
| MongoDB 预置数据更新 | `/deployment/docker-compose/standalone/data/preset/mongodb` |
| HAP 微服务升级 | `/deployment/docker-compose/standalone/upgrade/hap` |
| 存储组件升级 | `/deployment/docker-compose/standalone/upgrade/sc` |

### 集群模式（Kubernetes）

| 页面 | URL |
|------|-----|
| MongoDB 预置数据更新 | `/deployment/kubernetes/data/preset/mongodb` |
| HAP 微服务升级 | `/deployment/kubernetes/upgrade/hap` |

> ⚠️ 集群模式**没有**存储组件升级步骤，不要在集群升级文档中生成此步骤。

### 通用资源

| 页面 | URL |
|------|-----|
| 离线资源包 | `/deployment/offline` |
| 组件支持版本 | `/deployment/component` |
| MongoDB 新建数据库 | `/deployment/components/mongodb/createdb` |
| MongoDB 常用命令 | `/deployment/components/mongodb/command` |

### 组件文档

| 页面 | URL |
|------|-----|
| Kafka 安全连接（mTLS） | `/deployment/components/kafka/secureConnection` |

---

## FAQ 文档

| 页面 | URL |
|------|-----|
| 部署相关 FAQ（总入口） | `/faq/deployment` |
| 集成 - 启用 HDP | `/faq/integrate/hdp/enable-hdp` |
| 集成 - 文档转换 LibreOffice | `/faq/integrate/docconvert/libreoffice` |

---

## 架构优化文档

| 页面 | URL |
|------|-----|
| MongoDB 存储架构 | `/optimize/mongodb/storage/dataArchitecture` |

---

## 版本命名与维护规则

- **主版本**：版本号第三位为 `0`，如 v7.2.0、v7.1.0、v7.0.0
- **修复版本**：版本号第三位大于 `0`，如 v7.1.1、v7.0.4
- **维护策略**：默认维护最新 3 个主版本；同一主版本建议选第三位最大的修复版本升级
- **超出维护范围的版本**：资源仍可下载、环境可正常使用，但功能问题不再修复，建议升级至维护版本后反馈

---

## 镜像命名变更历史

| 变更时间 | 旧名称 | 新名称 | 相关文档 |
|----------|--------|--------|----------|
| v7.1.0 起 | `mingdaoyun-community` | `mingdaoyun-hap` | `/imagenamehistory#710` |

升级到 v7.1.0 时，必须执行以下替换命令（单机模式示例）：

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

---

## 版本列表页字段说明（`/version`）

| 字段 | 含义 |
|------|------|
| 版本 | 版本号 |
| 发布日期 | 发布时间 |
| 详情 | 链接至 `/upgrade/{version}/` |
| 含附加操作 | `√` 表示升级时有额外必做操作，必须访问对应详情页 |
| AMD64 | `✅` 支持，空白不支持 |
| ARM64 | `✅` 支持，空白不支持 |
| 对应公有云版本 | 与 SaaS 版本的对应关系 |
