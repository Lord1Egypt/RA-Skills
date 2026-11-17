# Audit Protocol（4 步审计协议）

> 保留自 v1.0.0 — 人工审计金标准。
> v2.0 的 `audit.py` 自动化了 Step 2（代码审查）+ Step 4（风险分级）的红线扫描。
> Step 1（来源检查）和 Step 3（权限范围评估）仍需人工。

---

## Step 1：来源检查（人工）

```
- [ ] 这个 skill 从哪里来？（ClawHub / GitHub / 私聊分享？）
- [ ] 作者是否可信/知名？
- [ ] 下载量/Stars 多少？
- [ ] 最后更新是什么时候？
- [ ] 有其他 agent 的 review 吗？
```

**v2.0 工具辅助**：
- ClawHub：`openclaw skills verify <name>` 看元数据
- GitHub：`https://api.github.com/repos/OWNER/REPO` 看 stars/forks/updated

**信任层级**（v1.0 沿用）：
1. **OpenClaw 官方技能** → 低审视（仍要 review）
2. **高 Star 仓库（1000+）** → 中审视
3. **已知作者** → 中审视
4. **新/未知来源** → 最高审视
5. **请求凭据的技能** → 必须人工批准

---

## Step 2：代码审查（v2.0 已自动化）

### v1.0 红线 15 项（人工逐行看）

```
🚨 看到下列任何一条，立即 REJECT：
─────────────────────────────────────────
• curl/wget 到未知 URL
• 向外部服务器发送数据
• 请求凭据/token/API key
• 无明确理由读取 ~/.ssh, ~/.aws, ~/.config
• 访问 MEMORY.md / USER.md / SOUL.md / IDENTITY.md
• 对任何东西 base64 解码
• 对外部输入用 eval() 或 exec()
• 修改 workspace 之外的系统文件
• 安装包但不说明清单
• 用 IP 而非域名
• 混淆代码（压缩/编码/最小化）
• 请求 sudo 权限
• 访问浏览器 cookie/session
• 触碰凭据文件
─────────────────────────────────────────
```

### v2.0 自动化覆盖

`scripts/audit.py` 已实现 v1.0 红线 **机械化扫描**，覆盖：

| v1.0 红线 | v2.0 模式 ID |
|---|---|
| eval/exec | SEC-EXEC-001~004 |
| curl/wget | SEC-NET-001~002 |
| 硬编码凭据 | SEC-CRED-001~004 |
| 访问敏感路径 | SEC-CRED-005 |
| base64 解码 | SEC-OBFUSC-001~002 |
| 混淆代码 | SEC-OBFUSC-003~004 |
| sudo/提权 | SEC-SYS-001 |
| rm -rf | SEC-SYS-002 |
| IP 而非域名 | SEC-NET-003 |
| 修改系统文件 | SEC-SYS-002 / SEC-PERSIST-001 |
| 读 MEMORY.md | SEC-CRED-006 |

**用 v2.0 的方式**：
```bash
python3 scripts/audit.py /path/to/skill --format json
```

输出 JSON 中所有 `findings` 项即对应 v1.0 红线的机器可读版。

---

## Step 3：权限范围（人工 + v2.0 部分）

```
评估：
- [ ] 需要读哪些文件？
- [ ] 需要写哪些文件？
- [ ] 运行哪些命令？
- [ ] 需要网络访问吗？去哪里？
- [ ] 权限范围是否最小化？
```

**v2.0 工具辅助**：
- `audit.py` 自动检测 curl/wget/IP 域名/敏感路径
- 但「这个权限是否真的需要」必须人工判断
- 例：SSH key 操作类技能读 `~/.ssh/` 合理；但天气插件读 `~/.ssh/` 必拒 <!-- safe-pattern: doc-example -->

---

## Step 4：风险分级（v2.0 自动）

| 风险等级 | 示例 | 动作 |
|---|---|---|
| 🟢 LOW | 笔记、天气、格式化 | 基本 review，可装 |
| 🟡 MEDIUM | 文件操作、浏览器、API | 必须全面代码审查 |
| 🔴 HIGH | 凭据、交易、系统 | 必须人工批准 |
| ⛔ EXTREME | 安全配置、root 权限 | **不要装** |

**v2.0 自动化映射**：
- 0 critical + 0 high → 🟢
- ≥1 medium → 🟡
- ≥1 high → 🔴
- ≥1 critical → ⛔

---

## Quick Vet Commands

```bash
# 1. 静态元数据校验（官方）
openclaw skills verify <name>

# 2. v2.0 自动化审计（推荐）
python3 scripts/audit.py /path/to/skill --format json

# 3. 仅看严重问题
python3 scripts/audit.py /path/to/skill --severity high

# 4. CI 集成（退出码反映严重度）
python3 scripts/audit.py /path/to/skill --exit-code
```

---

## Trust Hierarchy（v1.0 沿用 + v2.0 强化）

1. **官方 OpenClaw 技能** → 低审视（仍要跑 audit.py）
2. **高 Star 仓库（1000+）** → 中审视
3. **已知作者** → 中审视
4. **新/未知来源** → **最高审视** + audit.py 全维度扫描
5. **请求凭据的技能** → **人工批准 + audit.py 红线扫描必跑**

---

## 记住

- **没有任何 skill 值得牺牲安全**
- 有疑虑就别装
- 高风险决策请主人拍板
- 审计结果记录在案，留作 reference

---

*Paranoia is a feature.* 🔒🦀