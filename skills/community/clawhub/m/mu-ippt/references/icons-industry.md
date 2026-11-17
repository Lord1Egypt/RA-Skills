# icons-industry.md — 行业专业图标索引

> 覆盖 45 个 namespace，共 8092 个图标。图标存储在 `templates/icons/<namespace>/` 目录。
> 使用方式：在 SVG 中直接引用文件路径，或通过 `<use data-icon="<namespace>/<icon-name>" />`
> 搜索方式：`ls templates/icons/<namespace>/ | grep <keyword>`
> 所有 SVG 遵守 PPT大师禁用特性黑名单：无 `<style>`、无 `class`，使用 inline 属性。

---

## 按场景速查

### ☁️ 云架构（Cloud Architecture）

| namespace | 数量 | 说明 |
|-----------|------|------|
| aws4 | 1037 | **AWS 最新图标**（EC2/S3/Lambda/RDS/EKS/IAM 等，最全） |
| aws3 | 293 | AWS 第三代图标集 |
| aws2 | 237 | AWS 第二代图标集 |
| aws | 90 | AWS 基础图标（compute/database/networking 等分类） |
| aws3d | 16 | AWS 3D 风格图标 |
| gcp2 | 297 | **Google Cloud** 最新图标（BigQuery/GKE/Vertex AI 等） |
| gcp | 65 | Google Cloud 基础图标 |
| alibaba_cloud | 310 | **阿里云**图标（ECS/OSS/MaxCompute/ACK 等） |
| mscae | 347 | **Microsoft Azure** 图标（VM/AKS/CosmosDB/Functions 等） |
| ibm_cloud | 110 | IBM Cloud 图标（Watson/OpenShift/Db2 等） |
| azure | 89 | Azure 通用图标 |
| openstack | 18 | OpenStack 组件图标 |

**示例搜索：**
```bash
ls templates/icons/aws4/ | grep -i lambda
ls templates/icons/gcp2/ | grep -i vertex
ls templates/icons/alibaba_cloud/ | grep -i ecs
```

---

### 🌐 网络/基础设施（Networking & Infrastructure）

| namespace | 数量 | 说明 |
|-----------|------|------|
| cisco19 | 232 | Cisco 2019 网络设备图标（路由器/交换机/防火墙等） |
| cisco | 296 | Cisco 传统网络设备图标 |
| cisco_safe | 311 | Cisco SAFE 安全架构图标 |
| networks | 57 | 通用网络图标（服务器/路由/云连接） |
| networks2 | 114 | 网络图标增强版 |
| rack | 265 | 机柜/服务器机架图标（APC/Cisco/Dell/HP/IBM） |
| cabinets | 53 | 网络机柜图标 |
| eip | 36 | Enterprise Integration Patterns 图标 |

**示例搜索：**
```bash
ls templates/icons/cisco19/ | grep -i firewall
ls templates/icons/rack/ | grep -i cisco
```

---

### 🏢 商务/办公（Business & Office）

| namespace | 数量 | 说明 |
|-----------|------|------|
| office | 416 | **Microsoft Office 图标**（Word/Excel/PPT/Teams/Outlook 等） |
| signs | 369 | 通用标识图标（动物/食物/医疗/交通/警告等） |
| mockup | 92 | UI Mockup 图标（广告/日历/表单/导航等） |
| gmdl | 104 | Google Material Design 图标 |
| floorplan | 44 | 平面图/楼层图图标（家具/建筑元素） |
| sitemap | 50 | 网站地图/信息架构图标 |

**示例搜索：**
```bash
ls templates/icons/office/ | grep -i teams
ls templates/icons/signs/ | grep -i warning
```

---

### ⚙️ 流程建模（Process Modeling）

| namespace | 数量 | 说明 |
|-----------|------|------|
| bpmn | 39 | **BPMN 2.0** 流程建模图标（事件/网关/任务/泳道） |
| flowchart | 33 | 标准流程图形状（开始/结束/判断/处理） |
| lean_mapping | 13 | 精益价值流图（VSM）图标 |
| eip | 36 | 企业集成模式图标 |
| arrows | 34 | 箭头与连接器图标 |
| basic | 30 | 基础图形（矩形/圆形/菱形/多边形） |

**示例搜索：**
```bash
ls templates/icons/bpmn/ | grep -i gateway
ls templates/icons/flowchart/
```

---

### 🔧 DevOps/容器（DevOps & Containers）

| namespace | 数量 | 说明 |
|-----------|------|------|
| kubernetes | 40 | **Kubernetes** 资源图标（Pod/Service/Deployment/ConfigMap 等） |
| kubernetes2 | 39 | Kubernetes 第二代图标集 |
| atlassian | 26 | Atlassian 工具图标（Jira/Confluence/Bitbucket 等） |
| vvd | 94 | VMware Validated Design 图标 |

**示例搜索：**
```bash
ls templates/icons/kubernetes/ | grep -i deploy
ls templates/icons/kubernetes2/ | grep -i pod
```

---

### 🏭 行业垂直（Industry-Specific）

| namespace | 数量 | 说明 |
|-----------|------|------|
| electrical | 501 | **电气/电路图标**（电容/电阻/二极管/开关/传感器等） |
| pid | 462 | **管道仪表图**（PID）图标（泵/阀门/容器/仪表等） |
| fluid_power | 246 | 液压/气动系统图标 |
| veeam | 506 | **Veeam** 备份与灾难恢复图标（最多） |
| salesforce | 96 | **Salesforce** CRM 图标（Sales/Service/Marketing Cloud 等） |
| ibm | 8 | IBM 企业图标 |

**示例搜索：**
```bash
ls templates/icons/pid/ | grep -i pump
ls templates/icons/electrical/ | grep -i switch
ls templates/icons/salesforce/ | grep -i cloud
```

---

### 🌍 Web/品牌图标（Web & Brand Icons）

| namespace | 数量 | 说明 |
|-----------|------|------|
| weblogos | 178 | **Web 产品 Logo**（GitHub/Slack/Dropbox/Twitter 等） |
| webicons | 176 | Web 通用图标（界面元素/社交/文件类型等） |
| citrix | 97 | Citrix 产品图标 |
| citrix2 | 126 | Citrix 增强版图标 |

**示例搜索：**
```bash
ls templates/icons/weblogos/ | grep -i github
ls templates/icons/webicons/ | grep -i mail
```

---

### 📐 架构/建模（Architecture & Modeling）

| namespace | 数量 | 说明 |
|-----------|------|------|
| mscae | 347 | Microsoft 云架构图标（已列于云架构分类） |
| vvd | 94 | VMware 架构验证图标 |

---

## 汇总统计

| 指标 | 数值 |
|------|------|
| Namespace 数量 | 45 |
| 总 SVG 图标数 | 8092 |
| 空内容跳过 | 18 |
| 最大集合 | aws4（1037 个） |

---

## 使用示例

### 画 AWS Lambda 架构图
```bash
ls templates/icons/aws4/ | grep -i lambda
# → lambda.svg 或 aws-lambda.svg
```

### 画 K8s 部署图
```bash
ls templates/icons/kubernetes2/ | grep -i deploy
# → deployment.svg
```

### 画 Salesforce 业务流程图
```bash
ls templates/icons/salesforce/ | grep -i sales
```

### 在 SVG 中嵌入图标
```xml
<!-- 直接读取文件内容嵌入，遵守 PPT大师禁用特性黑名单 -->
<!-- 无 <style>、无 class、使用 inline 属性 -->
<image href="templates/icons/aws4/lambda.svg" x="100" y="50" width="24" height="24"/>
```

---

> 图标来源：[jgraph/drawio](https://github.com/jgraph/drawio) stencil 库（mxGraph 格式转换）
> 更新日期：2026-05-11
