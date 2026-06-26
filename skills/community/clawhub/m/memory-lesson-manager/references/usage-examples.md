# 完整使用流程示例

**版本：** 2.0.0  
**最后更新：** 2026-04-06

---

## 场景 1：遇到错误并记录

### 1.1 运行命令失败

```bash
git push origin main
fatal: Authentication failed for 'http://192.168.158.200:44481/'
```

### 1.2 创建错误记录

```bash
# 复制模板
cp memory/templates/lesson-error-template.md \
   memory/lessons/WARM/errors/ERR-20260406-001.md

# 编辑文件，填写错误信息
vi memory/lessons/WARM/errors/ERR-20260406-001.md
```

### 1.3 填写内容

```markdown
# [ERR-20260406-001] Git Push 认证失败

**记录时间：** 2026-04-06T10:30:00+08:00  
**优先级：** high  
**状态：** pending  
**领域：** infra

---

## 摘要
Git push 到 Gitea 时失败，提示认证失败

## 错误信息
```
fatal: Authentication failed for 'http://192.168.158.200:44481/'
```

## 上下文
- **尝试的操作：** `git push origin main`
- **环境信息：** 新初始化的 workspace，未配置 Gitea 认证

## 建议修复
先配置 Gitea 认证

## 元数据
- **可复现：** yes
- **首次出现：** 2026-04-06
- **出现次数：** 1
```

### 1.4 解决问题后更新状态

```markdown
## 解决方案
- **解决时间：** 2026-04-06T10:35:00+08:00
- **解决方式：** 运行 `gh auth login` 完成认证
- **验证结果：** git push 成功
```

---

## 场景 2：用户纠正后记录学习

### 2.1 用户纠正理解

```
用户：不对，API 设计应该只用 GET 和 POST，不要用 DELETE
```

### 2.2 创建学习记录

```bash
# 复制模板
cp memory/templates/lesson-correction-template.md \
   memory/lessons/WARM/corrections/LRN-20260406-001.md

# 编辑文件
vi memory/lessons/WARM/corrections/LRN-20260406-001.md
```

### 2.3 填写内容

```markdown
# [LRN-20260406-001] API 设计只用 GET/POST

**记录时间：** 2026-04-06T11:00:00+08:00  
**优先级：** high  
**状态：** resolved  
**类别：** best_practice  
**领域：** backend

---

## 摘要
API 设计只允许使用 GET 和 POST 方法，删除操作用逻辑删除

## 详细内容
- **原来的理解：** 可以使用所有 HTTP 方法（GET/POST/PUT/DELETE）
- **实际正确的做法：** 只用 GET（查询）和 POST（变更），删除用 is_deleted 标记
- **为什么错了：** 统一规范简化防火墙配置和审计

## 建议行动
更新 API 设计规范文档

## 元数据
- **来源：** user_feedback
- **相关文件：** docs/api-design-spec.md
- **标签：** api, rest, 规范
- **模式键：** best_practice.api_methods

---

## 推广状态
- **状态变更：** pending → promoted
- **晋升位置：** docs/api-design-spec.md
```

---

## 场景 3：日记质量检查

### 3.1 检查今日日记

```bash
./skills/memory-lesson-manager/scripts/validate-diary.sh
```

**输出示例：**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
记忆系统日记质量检查
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

检查日记：2026-04-06.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ 日记文件存在
✓ 包含反思环节
✓ 包含重要性标记（P1/P2/P3）
✓ 内容长度达标 (1500 字符 >= 200)
✓ 包含学习条目链接
✓ 记录了问题和解决方案

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
检查结果：
  行数：50
  字符数：1500
  问题数：0
  警告数：0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 日记质量优秀！
```

### 3.2 自动修复问题

```bash
./skills/memory-lesson-manager/scripts/validate-diary.sh --fix
```

### 3.3 检查本周所有日记

```bash
./skills/memory-lesson-manager/scripts/validate-diary.sh --all
```

---

## 场景 4：晋升高频条目

### 4.1 预览模式

```bash
./skills/memory-lesson-manager/scripts/promote-lesson.sh --dry-run
```

**输出示例：**
```
[STEP] 1/3 扫描 WARM 目录中的学习条目...
[INFO] 找到 2 个晋升候选
[DRY-RUN] 将晋升：LRN-20260406-001
       标题：API 设计只用 GET/POST
       类型：best-practices
       使用次数：5
       最后使用：2026-04-06
[DRY-RUN] 将晋升：LRN-20260405-002
...
[INFO] 预览模式 - 未执行实际晋升
```

### 4.2 执行晋升

```bash
./skills/memory-lesson-manager/scripts/promote-lesson.sh
```

### 4.3 指定条目晋升

```bash
./skills/memory-lesson-manager/scripts/promote-lesson.sh LRN-20260406-001
```

### 4.4 自定义参数

```bash
# 使用 5 次以上才晋升
./skills/memory-lesson-manager/scripts/promote-lesson.sh --threshold 5

# 14 天内使用过
./skills/memory-lesson-manager/scripts/promote-lesson.sh --days 14
```

---

## 场景 5：归档过期条目

### 5.1 预览模式

```bash
./skills/memory-lesson-manager/scripts/archive-cold.sh --dry-run
```

**输出示例：**
```
[STEP] 1/3 扫描 WARM 目录中的过期条目...
[INFO] 找到 3 个归档候选（90 天未使用）
[DRY-RUN] 将归档：ERR-20260101-001
       标题：旧错误记录
       类型：errors
       最后使用：2026-01-01
...
[INFO] 预览模式 - 未执行实际归档
```

### 5.2 执行归档

```bash
./skills/memory-lesson-manager/scripts/archive-cold.sh
```

### 5.3 列出已归档条目

```bash
./skills/memory-lesson-manager/scripts/archive-cold.sh --list-cold
```

**输出示例：**
```
[INFO] 已归档的学习条目：

  - ERR-20260101-001 (归档于：2026-04-06)
  - LRN-20260102-001 (归档于：2026-04-06)
  - FEAT-20260103-001 (归档于：2026-04-06)

[INFO] 共 3 个归档条目
```

### 5.4 恢复已归档条目

```bash
./skills/memory-lesson-manager/scripts/archive-cold.sh --restore ERR-20260101-001
```

---

## 场景 6：提取为技能

### 6.1 确认提取条件

满足以下任一条件：
- 重复问题 ≥3 次
- 解决方案已验证有效且具有通用性
- 用户明确要求"保存为技能"
- 发现的方法可独立复用

### 6.2 预览模式

```bash
./skills/memory-lesson-manager/scripts/extract-skill.sh git-auth-helper --dry-run
```

### 6.3 执行提取

```bash
./skills/memory-lesson-manager/scripts/extract-skill.sh git-auth-helper
```

**输出示例：**
```
[INFO] 创建技能：git-auth-helper
[STEP] 1/4 创建目录结构
[STEP] 2/4 创建 SKILL.md
[INFO] 已创建：./skills/git-auth-helper/SKILL.md
[STEP] 3/4 创建 references 目录
[STEP] 4/4 创建 scripts 目录

[INFO] ✅ 技能框架创建成功！

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
下一步操作：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  1. 编辑 ./skills/git-auth-helper/SKILL.md
     填写所有 [待填写] 部分

  2. 从学习条目复制内容
     来源：memory/lessons/XXX.md

  3. 添加参考资料（如需要）
     位置：./skills/git-auth-helper/references/

  4. 添加可执行脚本（如需要）
     位置：./skills/git-auth-helper/scripts/

  5. 更新原始学习条目
     添加：**状态**: promoted_to_skill
     添加：**技能路径**: skills/git-auth-helper
```

### 6.4 更新原始学习条目

```markdown
**状态：** promoted_to_skill  
**技能路径：** skills/git-auth-helper
```

---

## 场景 7：完整工作流程

### 7.1 初始化系统（首次使用）

```bash
./skills/memory-lesson-manager/scripts/init-memory-system.sh
```

### 7.2 记录问题

```bash
# 遇到问题 → 复制模板 → 填写内容
cp memory/templates/lesson-error-template.md \
   memory/lessons/WARM/errors/ERR-20260406-002.md
```

### 7.3 解决问题

```bash
# 更新状态
vi memory/lessons/WARM/errors/ERR-20260406-002.md
# 修改状态为 resolved
```

### 7.4 定期检查

```bash
# 每日检查日记质量
./skills/memory-lesson-manager/scripts/validate-diary.sh

# 每周晋升高频条目
./skills/memory-lesson-manager/scripts/promote-lesson.sh

# 每月归档过期条目
./skills/memory-lesson-manager/scripts/archive-cold.sh
```

### 7.5 提取技能

```bash
# 发现重复问题 ≥3 次 → 提取为技能
./skills/memory-lesson-manager/scripts/extract-skill.sh <技能名称>
```

---

## 快速命令参考

```bash
# 初始化
./skills/memory-lesson-manager/scripts/init-memory-system.sh

# 检查日记
./skills/memory-lesson-manager/scripts/validate-diary.sh [日期] [--fix] [--all]

# 晋升
./skills/memory-lesson-manager/scripts/promote-lesson.sh [--dry-run] [--threshold N]

# 归档
./skills/memory-lesson-manager/scripts/archive-cold.sh [--dry-run] [--restore ID]

# 提取
./skills/memory-lesson-manager/scripts/extract-skill.sh <名称> [--dry-run]

# 测试
./skills/memory-lesson-manager/scripts/test-memory-system.sh
```

---

_详细规范：work-specs/docs/memory-system-v2-spec.md_
