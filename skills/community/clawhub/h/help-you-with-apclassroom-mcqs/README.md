# AP Classroom Skill

专门用于完成所有 AP Classroom 学科作业的独立 skill。

## ⭐ 核心特性

- ✅ **多课程支持** - 支持所有 AP 学科
- ✅ **自动检测课程** - 无需手动配置
- ✅ **完整作业流程** - 检查、答题、提交
- ✅ **浏览器保持** - 永不关闭浏览器
- ✅ **通用工具集** - 适用于所有作业类型

## 🎯 支持的课程

本 skill 支持所有 AP 课程，包括：

**语言类**
- AP English Language and Composition
- AP English Literature and Composition
- AP World Languages

**数学类**
- AP Statistics
- AP Calculus AB/BC

**科学类**
- AP Biology
- AP Chemistry
- AP Physics 1/2/C
- AP Environmental Science

**计算机类**
- AP Computer Science A
- AP Computer Science Principles

**历史类**
- AP World History
- AP US History
- AP European History

**其他**
- AP Psychology
- AP Economics
- 以及所有其他 AP 课程

## ⚠️ 重要规则

**在任何情况下都不会关闭当前 Chrome 浏览器，除非先询问用户。**

---

## 🚀 快速开始

### 1. 启动浏览器（调试模式）

```powershell
Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" `
  -ArgumentList "--remote-debugging-port=9223"
```

### 2. 登录 College Board

在浏览器中手动登录 College Board 账号。

### 3. 启动任务管理器

**方式 1**: 双击 `start.bat`

**方式 2**: PowerShell
```powershell
cd ~/.agents/skills/ap-classroom
.\task-manager.ps1
```

**方式 3**: 命令行
```cmd
cd ~/.agents/skills/ap-classroom
task-manager.bat
```

---

## 📋 完整工作流程

### 步骤 1: 选择课程

```powershell
# 在任务管理器中按 [C] 切换课程
# 或运行：
node select-course.js
```

### 步骤 2: 检查作业

```powershell
# 在任务管理器中按 [2] 查看作业
# 或运行：
node check-homework.js
```

### 步骤 3: 完成作业

```powershell
# 打开作业
node open-assignment.js "作业名称"

# 获取题目
node get-questions.js

# 选择答案
node answer-question.js A

# 下一题
node next-question.js

# 提交
node submit-quiz.js
```

---

## 🛠️ 工具脚本

### 课程管理

| 脚本 | 功能 | 示例 |
|------|------|------|
| `list-courses.js` | 列出所有课程 | `node list-courses.js` |
| `select-course.js` | 切换课程 | `node select-course.js` |
| `check-browser-status.js` | 检查状态和当前课程 | `node check-browser-status.js` |

### 作业管理

| 脚本 | 功能 | 示例 |
|------|------|------|
| `check-homework.js` | 检查作业 | `node check-homework.js` |
| `open-assignment.js` | 打开作业 | `node open-assignment.js "作业名称"` |
| `get-questions.js` | 获取题目 | `node get-questions.js` |
| `answer-question.js` | 选择答案 | `node answer-question.js A` |
| `next-question.js` | 下一题 | `node next-question.js` |
| `submit-quiz.js` | 提交测验 | `node submit-quiz.js` |

---

## 💡 使用建议

### 多课程管理

1. **定期检查所有课程**
   ```powershell
   node list-courses.js
   # 然后逐个切换检查作业
   ```

2. **使用任务管理器快速切换**
   - 按 [C] 切换课程
   - 按 [2] 查看作业
   - 重复以上步骤检查其他课程

### 批量处理

```powershell
# 检查所有课程的作业
foreach ($course in @("AP Lang", "AP Stats", "AP CS")) {
    Write-Host "检查 $course ..." -ForegroundColor Green
    # 切换课程并检查作业
}
```

---

## 🔧 故障排查

### 问题 1: 无法检测到课程

**解决**:
1. 确保在 AP Classroom 页面
2. 运行 `node check-browser-status.js` 检查
3. 手动导航到课程页面

### 问题 2: 课程列表为空

**解决**:
1. 确保已登录 College Board
2. 确保已注册 AP 课程
3. 运行 `node list-courses.js` 重新检测

---

## 📝 配置文件

- **current-course.json** - 当前选择的课程
- **available-courses.json** - 可用的课程列表
- **homework-list.json** - 作业列表
- **course-config.json** - 课程特定配置（可选）

---

## 🔄 更新记录

- **2026-03-19 v2.0.0**: 重构为通用版，支持所有 AP 课程
- **2026-03-19 v1.0.0**: 初始版本，仅支持 AP Lang

---

## 📞 需要帮助？

- 查看 `QUICKSTART.md` 了解快速启动方法
- 查看 `SKILL.md` 了解技术细节
- 运行 `node check-browser-status.js` 检查状态

---

**⚠️ 提醒**:
- 提交测验前务必确认所有答案
- 浏览器会保持打开，不会自动关闭
- 支持所有 AP 学科的作业

---

**祝你作业顺利！** 🎉
