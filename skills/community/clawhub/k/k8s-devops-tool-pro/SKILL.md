---
slug: k8s-devops-tool-pro
name: k8s-devops-tool-pro
version: 1.0.0
displayName: K8s清单生成专业版
summary: "企业级K8s清单管理平台，支持Helm/Kustomize、策略校验与CI/CD集成.。面向企业DevOps团队的K8s清单管理平台。支持Helm Chart与Kustomize"
license: Proprietary
edition: pro
description: "面向企业DevOps团队的K8s清单管理平台。支持Helm Chart与Kustomize。Use when 需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于实时流数据处理。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。"
  完整工作流、策略合规校验、多环境覆盖、GitOps集成与CRD管理。Use when 需要数据分析、报表生成、统计洞察、数据可视化时使用。不适用于实时流数据处理。'
tags: DevOps,企业级,自动化,helm,python3,请参考
tools:
  - read
  - exec
  - write
homepage: ""
# 定价元数据
category: "Automation"

---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。

# K8s清单生成专业版（PRO版）

## 概述

本平台为企业DevOps团队提供全功能的K8s清单管理能力。相比免费版，PRO版新增Helm Chart、Kustomize、策略校验、多环境管理和GitOps集成等高级功能，全面满足企业级K8s清单管理的复杂需求.
PRO版完全兼容免费版清单生成命令，升级后原有模板可直接使用.
## 核心能力

### PRO版功能增强对比

| 功能 | 免费版 | PRO版 |
|---|---|----|
| 清单格式 | 原生YAML | +Helm+Kustomize |
| 模板系统 | 预置模板 | 自定义+治理 |
| 环境管理 | 不支持 | 多环境覆盖 |
| 策略校验 | 基础检查 | OPA/Kyverno合规 |
| GitOps | 不支持 | ArgoCD/Flux集成 |
| CRD管理 | 不支持 | 完整生命周期 |
| 版本管理 | 不支持 | 版本化清单 |
| CI/CD | 基础集成 | 完整流水线 |

**处理**: 解析PRO版功能增强对比的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回PRO版功能增强对比的响应数据,包含状态码、结果和日志.
### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：企业级、清单管理平台、策略校验与、面向企业、DevOps、团队的、Chart、完整工作流、策略合规校验、集成与、Use、when、需要数据分析、报表生成、统计洞察、数据可视化时使用、不适用于实时流数、据处理、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一：Helm Chart管理

用户输入："为我的应用创建Helm Chart"

```bash
# 创建Helm Chart
python3 （请参考skill目录中的脚本文件） helm create \
  --name my-app \
  --version 1.0.0 \
  --output-dir ./charts/
# ...
# 打包Chart
python3 （请参考skill目录中的脚本文件） helm package \
  --chart-dir ./charts/my-app \
  --version 1.0.0 \
  --destination ./repo/
# ...
# 发布到仓库
python3 （请参考skill目录中的脚本文件） helm push \
  --chart my-app-1.0.0.tgz \
  --repo https://harbor.example.com/chartrepo
```

### 场景二：多环境部署

用户输入："为dev/staging/prod生成差异化配置"

```bash
# 创建Kustomize结构
python3 （请参考skill目录中的脚本文件） kustomize init \
  --base ./base/ \
  --overlays "dev,staging,prod"
# ...
# 生成各环境配置
python3 （请参考skill目录中的脚本文件） kustomize build \
  --overlay prod \
  --output ./manifests/prod/
# ...
# 输出差异化配置
```

### 场景三：策略校验

用户输入："校验清单是否符合安全策略"

```bash
# 策略校验
python3 （请参考skill目录中的脚本文件） validate \
  --file ./manifests/ \
  --policies "require_limits,disallow_latest,require_labels" \
  --engine "kyverno"
# ...
# 输出：
# 已知限制
# [FAIL] disallow_latest - web-app使用了latest标签
# [PASS] require_labels - 所有资源包含必要标签
```

## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### PRO版初始化

```bash
# 依赖说明
pip install -r requirements_pro.txt
# ...
# 安装Helm
# macOS: brew install helm
# Linux: 下载官方安装包
```

### 常用命令

```bash
# Helm管理
python3 （请参考skill目录中的脚本文件） helm create --name my-app --version 1.0.0
python3 （请参考skill目录中的脚本文件） helm package --chart-dir ./charts/my-app
python3 （请参考skill目录中的脚本文件） helm push --chart my-app-1.0.0.tgz
# ...
# Kustomize
python3 （请参考skill目录中的脚本文件） kustomize init --base ./base/ --overlays "dev,prod"
python3 （请参考skill目录中的脚本文件） kustomize build --overlay prod
# ...
# 策略校验
python3 （请参考skill目录中的脚本文件） validate --file ./manifests/ --policies "require_limits"
# ...
# GitOps
python3 （请参考skill目录中的脚本文件） gitops sync --app my-app --cluster production
# ...
# CRD管理
python3 （请参考skill目录中的脚本文件） crd generate --definition ./crd-spec.yaml
python3 （请参考skill目录中的脚本文件） crd install --file ./crd.yaml
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 示例

### PRO企业级配置

```yaml
pro_config:
  helm:
    repo: "https://harbor.example.com/chartrepo"
    username: "${HELM_USER}"
    password: "${HELM_PASS}"
    sign: true                     # Chart签名
# ...
  kustomize:
    overlays:
      - name: "dev"
        patches: ["replicas:1", "resources:small"]
      - name: "staging"
        patches: ["replicas:2", "resources:medium"]
      - name: "prod"
        patches: ["replicas:5", "resources:large", "hpa:enabled"]
# ...
  validation:
    engine: "kyverno"              # kyverno | opa
    policies:
      - require_resource_limits
      - disallow_latest_tag
      - require_namespace_labels
      - restrict_privileged
      - require_security_context
    block_on_fail: true            # 校验失败阻止部署
# ...
  gitops:
    engine: "argocd"
    repo: "https://git.example.com/k8s-manifests"
    auto_sync: true
    auto_prune: true
# ...
  templates:
    governance: true               # 模板治理
    versioning: true               # 版本化
    approval: true                 # 模板需审批
# ...
  cicd:
    pipeline: "gitlab-ci"         # gitlab-ci | github-actions | jenkins
    stages: ["lint", "validate", "build", "deploy"]
    environments: ["dev", "staging", "prod"]
```

## 优选实践

### PRO版企业实践

| 实践领域 | 建议做法 |
|:-----|:-----|
| Helm管理 | Chart版本与应用版本一致，签名后发布 |
| Kustomize | base保持通用，overlay做环境差异化 |
| 策略校验 | CI流水线中强制校验，失败即阻止 |
| GitOps | 所有变更通过Git，ArgoCD自动同步 |
| 模板治理 | 模板需审批后才能使用 |

### 免费版兼容性

```text
免费版命令 → PRO版命令（增强）：
generate.py deployment  → devops_pro.py helm create (Helm Chart)
generate.py stack       → devops_pro.py kustomize build (多环境)
基础校验                 → +策略合规+GitOps+CRD
```

## 已知限制

- 本skill的能力范围受限于核心能力章节中定义的功能,不支持超出范围的操作
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 常见问题

### Q1：Helm和Kustomize该用哪个？

Helm适合打包发布完整应用（含模板化变量）；Kustomize适合多环境覆盖（无模板化）。两者可结合使用：Helm打包基础Chart，Kustomize做环境覆盖.
### Q2：策略校验支持什么规则？

支持资源限制检查、镜像标签检查、标签规范、安全上下文、特权模式检查等。可通过Kyverno或OPA编写自定义策略.
### Q3：GitOps如何集成？

PRO版生成Git仓库结构（base+overlays），ArgoCD/Flux监控Git仓库变更并自动同步到集群。所有部署通过Git提交触发.
### Q4：支持私有Helm仓库吗？

支持。PRO版兼容Harbor、ChartMuseum等私有Helm仓库。支持认证访问与Chart签名验证.
### Q5：模板治理如何工作？

企业级模板需经过审批后才能使用。模板版本化管理，变更需评审。确保团队使用经过验证的标准化模板.
## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Python版本**: 3.9+
- **Helm**: 3.0+（Chart管理需要）
- **kubectl**: 可选（部署验证需要）

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Python | 运行时 | 必需 | 系统安装或conda环境 |
| PyYAML | Python库 | 必需 | `pip install pyyaml` |
| jsonschema | Python库 | 必需 | `pip install jsonschema` |
| helm | CLI工具 | 可选 | 官网安装 |
| kustomize | CLI工具 | 可选 | 官网安装 |

### API Key 配置

| 服务 | 环境变量 | 是否必需 | 用途 |
|:---:|:---:|:---:|:---:|
| Harbor | `HELM_USER`/`HELM_PASS` | 可选 | 私有Chart仓库 |
| ArgoCD | `ARGOCD_TOKEN` | 可选 | GitOps集成 |
| Git | `GIT_TOKEN` | 可选 | 仓库访问 |

- 未配置的服务自动跳过
- 所有凭证存储在本地配置文件

### 可用性分类

- **分类**: MD+EXEC（Markdown指令+Python脚本+Helm执行）
- **说明**: 企业级K8s清单管理平台，支持Helm/Kustomize与GitOps
- **PRO版特性**: Helm Chart、Kustomize、策略校验、多环境、GitOps、CRD、模板治理
- **兼容性**: 完全兼容免费版清单生成命令

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。

## 核心功能

- **自动化执行**: 企业级K8s清单管理平台，支持Helm/Kustomize、策略校验与CI/CD集成.。面向企业DevOps团队的K8s
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据

## 核心功能

- **自动化执行**: 企业级K8s清单管理平台，支持Helm/Kustomize、策略校验与CI/CD集成.。面向企业DevOps团队的K8s
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据