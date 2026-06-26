---
name: ap-classroom
description: "完成 AP Classroom 所有学科的作业。支持 AP Lang、AP Statistics、AP Computer Science 等所有 AP 课程。自动检查、答题、提交 Reading Quiz、Writing Quiz、Progress Check 等作业。使用当前已登录的浏览器。"
metadata:
  port: 9223
  version: "2.0.0"
  features:
    - 多课程支持
    - 自动检测当前课程
    - 所有作业类型支持
    - 浏览器状态保持
---

# AP Classroom 作业自动化 - 通用版

专门用于完成所有 AP Classroom 学科的作业，包括 Reading Quiz、Writing Quiz、Progress Check、Practice Exam 等。

## ⚠️ 重要规则

**在任何情况下都不会关闭当前 Chrome 浏览器，除非先询问用户。**

---

## 🎯 支持的课程

本 skill 支持所有 AP 课程，包括但不限于：

- **AP English Language and Composition** (AP Lang)
- **AP English Literature and Composition** (AP Lit)
- **AP Statistics**
- **AP Calculus AB/BC**
- **AP Computer Science A**
- **AP Computer Science Principles**
- **AP Biology**
- **AP Chemistry**
- **AP Physics 1/2/C**
- **AP World History**
- **AP US History**
- **AP European History**
- **AP Psychology**
- **AP Macroeconomics**
- **AP Microeconomics**
- **其他所有 AP 课程**

---

## 🚀 快速开始

### 1. 启动浏览器（调试模式）

```powershell
Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" `
  -ArgumentList "--remote-debugging-port=9223"
```

### 2. 登录 College Board

在浏览器中手动登录 College Board 账号。

### 3. 选择课程

```powershell
cd ~/.agents/skills/ap-classroom
node select-course.js
```

或者在任务管理器中选择 `[C] 切换课程`。

### 4. 开始做作业

```powershell
# 使用任务管理器（推荐）
.\start.bat

# 或直接使用命令
node check-homework.js
```

---

## 📋 完整工作流程

### 步骤 1: 检查当前课程

```powershell
node check-browser-status.js
```

显示当前登录的课程和用户信息。

### 步骤 2: 切换课程（如需要）

```powershell
node select-course.js
```

从可用课程列表中选择。

### 步骤 3: 检查作业

```powershell
node check-homework.js
```

显示当前课程的所有待完成作业。

### 步骤 4: 完成作业

使用任务管理器或命令行工具完成作业。

---

## 🛠️ 工具脚本

### 基础工具

| 脚本 | 功能 | 示例 |
|------|------|------|
| `check-browser-status.js` | 检查浏览器和登录状态 | `node check-browser-status.js` |
| `select-course.js` | 切换 AP 课程 | `node select-course.js` |
| `check-homework.js` | 检查待完成作业 | `node check-homework.js` |

### 作业操作工具

| 脚本 | 功能 | 示例 |
|------|------|------|
| `open-assignment.js` | 打开指定作业 | `node open-assignment.js "作业名称"` |
| `get-questions.js` | 获取当前题目和选项 | `node get-questions.js` |
| `answer-question.js` | 选择答案 | `node answer-question.js A` |
| `next-question.js` | 进入下一题 | `node next-question.js` |
| `submit-quiz.js` | 提交测验 | `node submit-quiz.js` |

### 自动化工具

| 脚本 | 功能 | 说明 |
|------|------|------|
| `complete-quiz.js` | 完整自动化流程 | 需要编辑答题逻辑 |

---

## 🎓 课程管理

### 查看所有课程

```powershell
node list-courses.js
```

显示当前账号下所有可用的 AP 课程。

### 切换课程

**方法 1**: 使用脚本
```powershell
node select-course.js
```

**方法 2**: 使用任务管理器
- 启动任务管理器
- 选择 `[C] 切换课程`
- 从列表中选择课程

**方法 3**: 手动导航
- 在浏览器中点击课程名称
- 进入对应课程的 AP Classroom

### 课程信息存储

当前选择的课程信息保存在 `current-course.json`：

```json
{
  "name": "AP English Language and Composition",
  "id": "12",
  "student": "Rock",
  "lastChecked": "2026-03-19T10:00:00Z"
}
```

---

## 📊 作业类型支持

### 通用作业类型

所有 AP 课程都支持以下作业类型：

1. **Reading Quiz** - 阅读理解测验
2. **Writing Quiz** - 写作技巧测验
3. **Progress Check** - 进度检查
4. **Practice Exam** - 练习考试
5. **Unit Test** - 单元测试
6. **Timed Writing** - 计时写作
7. **FRQ** - 自由回答题
8. **MCQ** - 多项选择题

### 特殊作业类型

某些课程可能有特殊作业类型，本 skill 也支持：

- **Lab Report** (AP Sciences)
- **Portfolio** (AP Art)
- **Performance Task** (AP CSP)

---

## 💡 使用建议

### 多课程管理

如果你同时修多门 AP 课程：

1. **使用任务管理器** - 可以快速切换课程
2. **定期检查所有课程** - 避免遗漏作业
3. **按优先级处理** - 先处理截止日期近的作业

### 批量完成作业

```powershell
# 1. 检查所有课程的作业
node check-all-courses.js

# 2. 查看优先级排序
node priority-list.js

# 3. 逐个完成
# ... 使用任务管理器或命令行工具
```

---

## 🔧 高级功能

### 1. 自动检测课程

脚本会自动检测当前浏览器中打开的课程：

```javascript
// 自动获取课程 ID
const courseId = await page.evaluate(() => {
  const url = window.location.href;
  const match = url.match(/\/(\d+)\/assignments/);
  return match ? match[1] : null;
});
```

### 2. 课程特定配置

可以为不同课程创建特定配置：

```javascript
// course-config.json
{
  "12": {
    "name": "AP English Language and Composition",
    "shortName": "AP Lang",
    "color": "blue"
  },
  "33": {
    "name": "AP Statistics",
    "shortName": "AP Stats",
    "color": "green"
  }
}
```

### 3. 批量检查

检查所有课程的作业：

```powershell
node check-all-courses.js
```

---

## 📝 配置文件

### current-course.json

当前选择的课程信息。

### course-config.json

课程特定配置（可选）。

### homework-history.json

作业完成历史记录。

---

## 🔄 更新记录

- **2026-03-19 v2.0.0**: 重构为通用版，支持所有 AP 课程
- **2026-03-19 v1.0.0**: 初始版本，仅支持 AP Lang

---

## 📞 需要帮助？

- 查看 `QUICKSTART.md` 了解快速启动方法
- 查看 `README.md` 了解详细功能
- 运行 `node check-browser-status.js` 检查当前状态

---

**⚠️ 提醒**: 提交测验前务必确认所有答案！
