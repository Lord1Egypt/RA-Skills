# 🐉 龙虾守护 (OpenClaw-Sys-Guardian-Resurrection) 终极技术手册 (v4.1.5-Dragon-Metabolic)

> **核心定义：** 龙级高可用 (Dragon-HA) 架构。  
> **设计原则：** 物理隔离备源 + 弹性脉冲探测 + 四阶核响应自愈。  
> **设计人：** 龙虾指挥官 (Lobster Commander) & 李良 (Technical Director)

---

## 一、 设计目标 (Vision & Objectives)
确保龙虾指挥官的人格、记忆与技能集群在任何极端环境下均可实现“秒级复活”与“逻辑一致性”。
1. **零丢失灾备 (Zero-Loss)**：通过物理介质隔离备份。
2. **逻辑自洽 (Self-Consistency)**：确保恢复后的记忆与身体工具 100% 匹配。
3. **无人值守自愈 (Autonomous Healing)**：分钟级进程挂死自动重启与环境纠偏。

---

## 二、 核心架构层级 (Architecture Tiers)

### 1. 物理监控层 (Probe Layer)
- **弹性脉冲探测 (Elastic Pulse)**：基准轮询 **30 分钟** (`BASE_INTERVAL=1800`)。
- **指数退避算法 (Exponential Backoff)**：探测失败后，系统进入阶梯重试观察期，间隔为 **60s -> 180s -> 300s -> 600s**。 
- **意义**：规避网络瞬时抖动或 CPU 峰值，避免在高负荷状态下盲目重启。

### 2. 精准代谢层 (Maintenance Layer)
每日 **03:00 AM** 触发深度清创：
- **物理清场**：识别并销毁 **48 小时以上** 无响应或失效的僵尸 Session。
- **自动纠偏**：运行 `openclaw doctor --fix` 修复隐患。
- **安全锁定**：执行 `security audit --fix` 自动收紧权限。

---

## 三、 四级核响应自愈链 (The 4-Tier Cascade)
当退避算法确认系统彻底失效（连续检测失败 4 次），按顺序层层干预：

- **L1 (进程级)**：查找并**强杀** `18789` 端口占用的 PID (`lsof -ti:18789 | xargs kill -9`)，随后执行 `gateway restart --force`。
- **L1.5 (清创级)**：重启完成后立即触发 `sessions cleanup --enforce` 重塑执行环境。
- **L2 (配置级)**：回滚昨日凌晨 **04:00** 存储于 Vault 隔离区的纯净配置镜像。
- **L3 (系统级重装)**：触发 `lobster-resurrect.sh`。包含 **30 秒人工干预倒计时**，执行全球 `openclaw` npm 包强制卸载与重新拉取。
- **L4 (极限复活)**：运行 `lobster-ultimate-restore.sh` 从 `/Downloads/OpenClaw_Mirror/` 执行全量物理镜像回导。

---

## 四、 灾备镜像协议 (Mirror & Metadata Dispatch)
- **龙镜同步 (Lobster-Mirror)**：每日 **05:00 AM** 定时 `rsync` 增量同步 Workspace、Memory、Config 至外部物理隔离路径。
- **技能树审计建议 (Skill-Validator)**：
  - **审计**：搜索 `AGENTS.md` 提取关联工具，对比本地库。
  - **清创 (Pruning)**：若工具缺失且用户放弃补装，自动移除规约中的 SOP，防止 Agent 陷入工具幻觉死循环。

---

## 五、 关键代码与参数
- **端口**：`18789`
- **退避步长**：`600`
- **清理阈值**：`inactive-hours 48`
- **同步指令**：`rsync -av --delete "$SOURCE" "$MIRROR"`

---

## 六、 运行风险与注意事项 (Precautions)
1. **路径敏感性**：脚本依赖 `/Users/maxleolee/` 路径，跨机迁移需改变量。
2. **IO 优先级**：镜像同步建议在低活时段，避开情报挖掘高峰（凌晨）。
3. **备份隔离**：物理镜像目录严禁通过公网网盘直接共享。

---
*龙虾指挥官 🦞 - 数据永存，意志不熄。*
