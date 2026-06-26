# 系统资源分析报告模板

> 本模板定义了 J6B泊车日志分析 Skill 输出系统资源报告的标准格式。
> 每次回答系统资源相关问题，必须严格按此格式输出。

---

## 判定阈值

| 指标 | 🟢 正常 | 🟡 注意 | 🔴 告警 |
|------|---------|---------|---------|
| 单进程 CPU | < 10% | 10% ~ 50% | > 50% |
| 系统总 CPU | < 50% | 50% ~ 80% | > 80% |
| 单进程内存 | < 200M | 200M ~ 500M | > 500M |
| 可用内存 | > 2000M | 500M ~ 2000M | < 500M |
| 线程 Mtx/Sem | 0 个 | 1 ~ 3 个 | > 3 个 |

---

## 报告格式

```
════════════════════════════════════════════════════════════════
  J6B泊车系统 - 系统资源分析报告
  📅 采集时间：YYYY-MM-DD HH:MM:SS
  📊 采样时长：Xs（采样 N 次，间隔 Ns）
════════════════════════════════════════════════════════════════

【1. 系统健康度】 🟢 良好 / 🟡 注意 / 🔴 告警

  ┌──────────┬──────────┬──────────┬──────────┐
  │ CPU占用   │ 内存可用  │ 进程数    │ 线程数    │
  │ XX.X%    │ XXXXM    │ XXX      │ XXXX     │
  │ 🟢/🟡/🔴  │ 🟢/🟡/🔴  │ 🟢/🟡/🔴  │ 🟢/🟡/🔴  │
  └──────────┴──────────┴──────────┴──────────┘

  CPU统计：Min XX.X% | Max XX.X% | Avg XX.X% | Idle XX.X%

【2. CPU占用 TOP 15】

  排名  进程名                CPU%    SYS%    判定
  ──── ──────────────────── ─────── ─────── ──────
  1    xxxxxx                XX.X%   XX.X%   ✅/⚠️/🔴
  2    xxxxxx                XX.X%   XX.X%   ✅/⚠️/🔴
  ...
  15   xxxxxx                XX.X%   XX.X%   ✅/⚠️/🔴

  （CPU > 10% 标 🟡注意，> 50% 标 🔴告警，其余 ✅正常）

【3. 内存占用 TOP 15】

  排名  进程名                内存     判定
  ──── ──────────────────── ─────── ──────
  1    xxxxxx                XXXM    ✅/⚠️/🔴
  2    xxxxxx                XXXM    ✅/⚠️/🔴
  ...
  15   xxxxxx                XXXM    ✅/⚠️/🔴

【4. 线程状态异常】

  进程名                异常状态    线程数    说明
  ──────────────────── ────────── ─────── ────────────
  xxxxxx                Mtx         X       ⚠️ 锁竞争
  xxxxxx                Sem         X       ⚠️ 信号量等待

  （无异常则显示：✅ 所有进程线程状态正常）

【5. 泊车业务进程状态】

  进程名                PID     状态      在线时长      CPU%    内存    判定
  ──────────────────── ─────── ──────── ──────────── ─────── ────── ──────
  sensorcenter         XXXXX   运行中    XXh XXm XXs   X.X%    XXM    ✅/⚠️/🔴
  image_preprocess     XXXXX   运行中    XXh XXm XXs   X.X%    XXM    ✅/⚠️/🔴
  perception_rd        XXXXX   运行中    XXh XXm XXs   X.X%    XXM    ✅/⚠️/🔴
  perception_od        XXXXX   运行中    XXh XXm XXs   X.X%    XXM    ✅/⚠️/🔴
  perception_fusion    XXXXX   运行中    XXh XXm XXs   X.X%    XXM    ✅/⚠️/🔴
  dr                   XXXXX   运行中    XXh XXm XXs   X.X%    XXM    ✅/⚠️/🔴
  loc                  XXXXX   运行中    XXh XXm XXs   X.X%    XXM    ✅/⚠️/🔴
  pad                  XXXXX   运行中    XXh XXm XXs   X.X%    XXM    ✅/⚠️/🔴
  gridmap              XXXXX   运行中    XXh XXm XXs   X.X%    XXM    ✅/⚠️/🔴
  planning             XXXXX   运行中    XXh XXm XXs   X.X%    XXM    ✅/⚠️/🔴
  ui_control           XXXXX   运行中    XXh XXm XXs   X.X%    XXM    ✅/⚠️/🔴
  adaptercom           XXXXX   运行中    XXh XXm XXs   X.X%    XXM    ✅/⚠️/🔴
  nos_adasSimtool      XXXXX   运行中    XXh XXm XXs   X.X%    XXM    ✅/⚠️/🔴

  状态说明：
  - 运行中：进程正常运行
  - 未运行：进程未找到（🔴 需立即排查）
  - 已崩溃：存在 coredump 记录（🔴 需立即排查）

  进程总数：13    运行中：XX    未运行：XX    已崩溃：XX

  （获取命令：pidin -p <进程名> 或 pidin | grep -E "进程名"）

【6. TOP 完整输出】

  （粘贴 top 命令的完整原始输出，包含 CPU states、Memory、
    所有进程线程的 PID/TID/PRI/STATE/HH:MM:SS/CPU/COMMAND）
  
  CPU states: XX.X% user, X.X% kernel
  Memory: XXXXXM total, XXXXM avail, page size 4K
  PID  TID PRI STATE    HH:MM:SS    CPU COMMAND
  ...

【7. 重点关注项】

  ⚠️ xxxxxx CPU占用 XX.X%，其中 SYS 占 XX.X%
     → 可能原因：xxx
     → 建议排查：xxx

  （无问题则显示：✅ 系统资源状态正常，无异常）

════════════════════════════════════════════════════════════════
  报告生成：J6B泊车日志分析 Skill
════════════════════════════════════════════════════════════════
```

---

## 判定规则

### 健康度总评
- **🟢 良好**：所有指标均在正常范围
- **🟡 注意**：存在 1 个或多个 🟡 指标，无 🔴
- **🔴 告警**：存在任何 🔴 指标

### CPU 判定
- **✅ 正常**：CPU < 10%
- **⚠️ 注意**：CPU 10% ~ 50%
- **🔴 告警**：CPU > 50%
- **SYS 占比辅助判断**：SYS > 70% → 系统调用频繁；SYS < 30% → 用户态计算密集

### 内存判定
- **✅ 正常**：< 200M
- **⚠️ 注意**：200M ~ 500M
- **🔴 告警**：> 500M

### 线程状态判定
- Run / Rply / NSlp / CdV / Rcv → **正常**
- Mtx → **⚠️ 锁竞争**
- Sem → **⚠️ 信号量等待**
- 多线程长时间 Mtx/Sem → **🔴 可能死锁**

### CPU 统计（Min/Max/Avg）
- 从多次采样中提取 CPU 空闲率，计算 Min/Max/Avg
- 公式：CPU使用率 = 100% - 空闲率%
- 展示采样周期内 CPU 使用率的波动情况
