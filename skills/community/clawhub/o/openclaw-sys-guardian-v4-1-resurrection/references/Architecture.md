# 🦞 openclaw-Sys Guardian V4.1 逻辑架构流程图

```mermaid
graph TD
    %% 正常运行状态
    Start((开始运行)) --> Normal[<b>正常生存模式</b><br/>每30分钟心跳探测一次]
    
    %% 检测环节
    Normal --> Check{响应 200 OK?}
    Check -- 是 --> Normal
    
    %% 故障进入指数退避
    Check -- 否 --> RetryMode[<b>进入预警重试模式</b><br/>启动指数退避序列]
    
    RetryMode --> Backoff{探测 4 次全部失败?<br/>1min, 3min, 5min, 10min}
    Backoff -- 某次成功 --> Normal
    
    %% 判定死机，触发自愈
    Backoff -- 是 (约20min后) --> L1_Heal[<b>L1 进程自愈</b><br/>强杀残留 + 强制重启网关]
    
    L1_Heal --> L1_Check{服务恢复?}
    L1_Check -- 是 --> Cleanup[<b>系统清创</b><br/>sessions cleanup<br/>抹除失败任务碎片]
    Cleanup --> Normal
    
    %% 重启失败，尝试回滚
    L1_Check -- 否 --> L2_Heal[<b>L2 配置归位</b><br/>从 Vault 搬运凌晨 4:00 快照<br/>再次尝试强制重启]
    
    L2_Heal --> L2_Check{服务恢复?}
    L2_Check -- 是 --> Normal
    
    %% 全线溃败，启动交互引导
    L2_Check -- 否 --> FatalMode[<b>FATAL: 自动自愈熔断</b><br/>停止所有 API 探测<br/>锁定 CPU/IO 消耗]
    
    FatalMode --> TerminalGuide[<b>终端交互引导</b><br/>在屏幕循环滚动红色提示<br/>指引运行: lobster-resurrect.sh]
    
    %% 物理涅槃
    TerminalGuide --> Resurrection[<b>指挥官方涅槃 (手动)</b><br/>1. 彻底物理卸载 OpenClaw<br/>2. 排空 npm/pnpm 全量缓存<br/>3. 重装内核并原位注入配置]
    
    Resurrection --> Start
```

---

## 🧭 逻辑图核心解读：

1.  **静默期 (Green)**：系统 99% 的时间处于“正常生存模式”，不会产生干扰。
2.  **退避期 (Yellow)**：不会因为瞬时断网就重启。通过 **1, 3, 5, 10 分钟** 的阶梯等待，给宿主系统自我调节的时间。
3.  **自愈期 (Blue)**：这是最后的自动化博弈。先拉起服务（L1），成功了就立刻大扫除（L1.5）；服务不起来就换掉损坏的配置（L2）。
4.  **死局/涅槃期 (Red)**：当所有自动手段用尽，守护进程不再做无谓的消耗，而是转型为一个“永久路牌”，指引你进行最彻底的重装。

---
*编撰：龙虾指挥官 (Lobster Commander)*
*日期：2026-03-03*
