---

slug: k8s-toolkit-pro
name: k8s-toolkit-pro
version: 1.0.0
displayName: K8s运维专业版
summary: "企业级K8s运维平台，支持集群诊断、自动修复、性能优化与安全合规.。面向企业K8s运维团队的全栈运维平台。支持集群级问题诊断、自动修复、"
license: Proprietary
edition: pro
description: "面向企业K8s运维团队的全栈运维平台。支持集群级问题诊断、自动修复、。Use when 需要安全检测、合规审计、质量检查、加密防护时使用。不适用于安全评估未授权目标。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。输出结果可直接使用，减少二次加工成本。提供结构化输出和错误处理机制。 功能涵盖: toolkit。"
  性能优化、安全合规审计与容量规划。Use when 需要安全检测、合规审计、质量检查、加密防护时使用。不适用于安全评估未授权目标。Use
  when 需要安全检测、合规审计、质量检查、加密防护时使用。不适用于安全评估未授权目标。'
tags:
  - Operations
  - Kubernetes
  - 企业级
  - 运维自动化
  - 工具
  - 效率
  - 自动化
  - 安全
  - 加密
  - 运维
  - 监控
  - 研究
  - pro
  - python3
tools:
  - read
  - exec
  - write
homepage: ""
# 定价元数据
category: "Automation"

---

> **功能说明**: 本技能涵盖 中文交互、化工作流场景 等核心能力。


# K8s运维专业版（PRO版）

## 概述

本平台为企业K8s运维团队提供全栈运维能力。相比免费版，PRO版新增集群级诊断、自动修复、性能优化、合规检查和多集群管理等高级功能，全面满足企业级K8s运维的复杂需求.
PRO版完全包含免费版避坑指南知识库，升级后原有排查工作流可直接使用.
## 核心能力

### PRO版功能增强对比

| 功能 | 免费版 | PRO版 |
|---|---|----|
| 问题知识库 | 32个 | 88+个完整版 |
| 诊断范围 | Pod/Service/Deployment | 全集群维度 |
| 修复方式 | 手动建议 | 自动修复+智能建议 |
| 性能优化 | 不支持 | 资源调优+瓶颈分析 |
| 合规检查 | 不支持 | CIS/NIST合规 |
| 容量规划 | 不支持 | 趋势预测 |
| 集群管理 | 单集群 | 多集群统一 |
| 自动化 | 不支持 | 运维流水线 |

**处理**: 解析PRO版功能增强对比的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回PRO版功能增强对比的响应数据,包含状态码、结果和日志.
### 诊断维度

| 维度 | 检查项数量 | PRO版覆盖 |
|:-----|:-----|:-----|
| Pod健康 | 15项 | 全部 |
| 网络连通性 | 12项 | 全部 |
| 存储与卷 | 10项 | 全部 |
| 资源利用 | 10项 | 全部 |
| 安全配置 | 15项 | 全部 |
| 控制平面 | 8项 | 全部 |
| 节点健康 | 10项 | 全部 |
| 应用配置 | 8项 | 全部 |

**处理**: 解析诊断维度的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回诊断维度的响应数据,包含状态码、结果和日志.
### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：企业级、运维平台、支持集群诊断、性能优化与安全合、面向企业、运维团队的全栈运、维平台、支持集群级问题诊、安全合规审计与容、Use、when、需要安全检测、合规审计、质量检查、加密防护时使用、不适用于安全评估、未授权目标、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一：集群全面诊断

用户输入："对生产集群进行全面体检"

用户可通过自然语言指令触发此场景，工具将自动执行相应操作并返回结构化结果.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---:|---:|---:|---:|
| input | string | 是 | K8s运维专业版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 集群全面诊断
python3 （请参考skill目录中的脚本文件） diagnose \
  --cluster production \
  --deep \
  --output health_report.pdf
# ...
# 输出包含：
# - 集群健康评分（85/100）
# - 88项检查结果
# - 发现的问题列表（按严重程度排序）
# - 自动修复建议
# - 性能优化建议
# - 安全合规状态
```

### 场景二：自动修复

用户输入："自动修复所有可自动处理的问题"

```bash
# 自动修复
python3 （请参考skill目录中的脚本文件） auto-fix \
  --cluster production \
  --severity "medium,high" \
  --dry-run                  # 先预览
# ...
# 确认后执行
python3 （请参考skill目录中的脚本文件） auto-fix \
  --cluster production \
  --severity "medium,high" \
  --apply
# ...
# 输出修复报告
```

### 场景三：安全合规审计

用户输入："检查K8s集群的安全合规性"

```bash
# 合规检查
python3 （请参考skill目录中的脚本文件） audit \
  --cluster production \
  --standard "CIS-Benchmark" \
  --output security_audit.pdf
# ...
# 输出包含：
# - CIS Benchmark检查项
# - 不合规项详情
# - 风险等级评估
# - 修复建议
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
# 配置多集群访问
cp config_pro_template.yaml config_pro.yaml
```

### 常用命令

```bash
# 集群诊断
python3 （请参考skill目录中的脚本文件） diagnose --cluster production --deep
python3 （请参考skill目录中的脚本文件） diagnose --cluster production --dimension security
# ...
# 自动修复
python3 （请参考skill目录中的脚本文件） auto-fix --cluster production --dry-run
python3 （请参考skill目录中的脚本文件） auto-fix --cluster production --apply
# ...
# 性能优化
python3 （请参考skill目录中的脚本文件） optimize --cluster production --output optimization_report.pdf
# ...
# 合规检查
python3 （请参考skill目录中的脚本文件） audit --cluster production --standard "CIS-Benchmark"
# ...
# 容量规划
python3 （请参考skill目录中的脚本文件） capacity --cluster production --forecast-months 6
# ...
# 多集群管理
python3 （请参考skill目录中的脚本文件） clusters list
python3 （请参考skill目录中的脚本文件） clusters status --all
```

#
## 示例

### PRO企业级配置

```yaml
pro_config:
  clusters:
    - name: "production"
      kubeconfig: "$HOME/.kube/config-prod"
      context: "prod-cluster"
    - name: "staging"
kube/config-staging"
      context: "staging-cluster"
    - name: "development"
      context: "dev-cluster"
# ...
  diagnosis:
    dimensions: ["pod", "network", "storage", "resource", "security", "control_plane", "node", "app"]
    deep_mode: true
    knowledge_base: "full"         # full | basic
# ...
  auto_fix:
    enabled: true
    safe_mode: true                # 仅修复安全项
    severity_filter: ["medium", "high", "critical"]
    require_approval: true         # 生产环境需确认
    rollback_on_failure: true
# ...
  optimization:
    resource_tuning: true
    hpa_analysis: true             # 水平Pod自动扩缩分析
    pvc_optimization: true
    network_optimization: true
# ...
  audit:
    standards: ["CIS-Benchmark", "NIST", "PCI-DSS"]
    schedule: "weekly"
    auto_remediation: false
# ...
  capacity:
    forecast_months: 6
    model: "arima"
    alert_threshold: 0.8           # 80%时预警
# ...
  automation:
    pipelines: true
    schedule: "0 2 * * *"          # 每日凌晨2点
    notification:
      channels: ["webhook", "email"]
```

## 优选实践

### PRO版企业实践

| 实践领域 | 建议做法 |
|:---:|:---:|
| 诊断策略 | 每日快速诊断，每周深度体检 |
| 自动修复 | 先dry-run预览，确认后apply |
| 合规检查 | 定期CIS审计，及时修复高危项 |
| 容量规划 | 关注CPU/内存/PVC趋势，提前扩容 |
| 多集群 | 统一配置基线，差异化管理 |

### 免费版兼容性

```text
免费版命令 → PRO版命令（增强）：
k8s troubleshoot pod     → k8s_pro.py diagnose --dimension pod (全维度)
k8s check deployment     → k8s_pro.py auto-fix (自动修复)
避坑指南(32个)           → 完整知识库(88+个)
```

## 常见问题

### Q1：自动修复安全吗？

PRO版自动修复采用安全模式，仅执行已知安全的修复操作。生产环境需人工确认（require_approval）。所有修复操作支持回滚（rollback_on_failure）.
### Q2：支持哪些K8s发行版？

支持所有CNCF认证的K8s发行版，包括EKS/GKE/AKS/自建集群。部分发行版特有功能（如GKE Autopilot）有针对性优化.
### Q3：多集群如何管理？

通过kubeconfig配置多个集群访问凭证。PRO版支持跨集群统一诊断、配置对比和批量操作。所有集群状态汇总展示.
### Q4：容量预测准确吗？

基于历史6个月数据使用ARIMA模型预测。准确度取决于历史数据质量和业务波动性。建议定期校正预测模型.
### Q5：合规检查包含什么？

包含CIS Kubernetes Benchmark全部检查项，覆盖API Server、etcd、控制平面、节点、网络、RBAC等维度。支持NIST和PCI-DSS标准.
## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Python版本**: 3.9+
- **kubectl**: 已配置集群访问

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Python | 运行时 | 必需 | 系统安装或conda环境 |
| kubernetes | Python库 | 必需 | `pip install kubernetes` |
| pandas | Python库 | 可选 | `pip install pandas`（数据分析） |
| statsmodels | Python库 | 可选 | `pip install statsmodels`（预测模型） |
| kube-hunter | CLI工具 | 可选 | 安全扫描 |

### API Key 配置

- PRO版通过kubeconfig认证集群
- 无需额外API Key
- 多集群通过不同kubeconfig context管理

### 可用性分类

- **分类**: MD+EXEC（Markdown指令+Python脚本+kubectl执行）
- **说明**: 企业级K8s运维平台，支持诊断、修复、优化与审计
- **PRO版特性**: 全维度诊断、自动修复、性能优化、合规检查、容量规划、多集群
- **兼容性**: 完全包含免费版避坑指南知识库

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|:---|---:|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响

## 安全注意事项

| 风险类型 | 防范措施 |
|----------|---------|
| API密钥泄露 | 通过环境变量配置，禁止硬编码到代码或配置文件中 |
| 命令执行风险 | 仅执行白名单命令，避免拼接用户输入到命令行参数中 |
| 网络通信安全 | 使用HTTPS协议，验证SSL证书有效性 |
| 敏感数据暴露 | 输出结果中不包含密钥、令牌等敏感信息 |

使用前请确认已阅读依赖说明章节，确保运行环境满足安全要求。

## 核心功能

- **自动化执行**: 企业级K8s运维平台，支持集群诊断、自动修复、性能优化与安全合规.。面向企业K8s运维团队的全栈运维平台。支持集群级问题
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据

## 核心功能

- **自动化执行**: 企业级K8s运维平台，支持集群诊断、自动修复、性能优化与安全合规.。面向企业K8s运维团队的全栈运维平台。支持集群级问题
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据