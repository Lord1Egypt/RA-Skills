# 数据流图

## 1. 伸缩组列表（默认 / --table / --json）

```mermaid
flowchart TD
    A[Agent / 用户] -->|--region / --name / --status| B[scripts/list_as_groups.py]
    B -->|1. 写意图守卫| G{是否含写意图?}
    G -->|是| X[打印只读拦截提示<br/>exit 1]
    G -->|否| C[argparse 参数校验]
    C --> D{hcloud 可用?}
    D -->|是| E[hcloud AS ListScalingGroups<br/>--cli-region --limit --start_number]
    D -->|否| F[huaweicloudsdkas v1<br/>ListScalingGroups]
    E -->|瞬时失败| F
    E -->|成功 / 403 / 凭据错误| H{页面数据}
    F --> H
    H -->|total_number / 累计条数<br/>短页 / max-pages| I[继续分页?]
    I -->|是| E
    I -->|否| J[归一化组字段<br/>VPC / 子网 / ELB / 实例数]
    J --> K{--json?}
    K -->|是| L[合并原始响应 → stdout]
    K -->|否| M[名称过滤 / 状态过滤]
    M --> N{--table?}
    N -->|是| O[异常组分区置顶 + 正常组分区<br/>⚠ 标注]
    N -->|否| P[简洁列表：名称 / 组ID / 状态]
    O --> Q[stdout + 汇总行]
    P --> Q
```

## 2. 组内实例下钻（--group-id）

```mermaid
flowchart TD
    A[Agent / 用户] -->|--group-id + 可选 --status| B[scripts/list_as_groups.py]
    B --> G{写意图守卫}
    G -->|命中| X[exit 1，不发起调用]
    G -->|通过| C[hcloud AS ListScalingInstances<br/>--scaling_group_id --limit --start_number]
    C -->|hcloud 缺失 / 瞬时失败| D[huaweicloudsdkas v1<br/>ListScalingInstances]
    C -->|403 / 凭据 / 组不存在| E[分类错误 → stderr + exit 1]
    D --> F{页面数据}
    F -->|total_number / 累计条数| H[继续分页?]
    H -->|是| C
    H -->|否| I[归一化实例字段]
    I --> J[状态 / 健康过滤]
    J --> K{--table?}
    K -->|是| L[异常实例分区置顶<br/>生命周期非 INSERVICE 或健康非 NORMAL]
    K -->|否| M[简洁列表]
    L --> N[stdout + 汇总行]
    M --> N
```

## 3. 判断口径

```text
异常伸缩组 = 状态 != INSERVICE  或  期望实例数 != 当前实例数
异常实例   = 生命周期状态 != INSERVICE  或  健康状态 != NORMAL

--status abnormal        → 只列异常资源
--status <状态值>        → 客户端精确匹配（组状态 / 实例生命周期 / 实例健康）
--json                   → 输出原始合并响应，不做客户端过滤
```