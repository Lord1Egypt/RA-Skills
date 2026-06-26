# AP Classroom Skill - 发布说明

## 📦 版本 2.0.0 - 通用版

### 🎉 主要更新

#### ✨ 新功能

1. **多课程支持**
   - 支持所有 AP 学科
   - 自动检测当前课程
   - 快速切换课程

2. **课程管理**
   - 列出所有可用课程
   - 保存当前课程信息
   - 课程配置文件

3. **通用工具**
   - 所有工具适配所有课程
   - 动态课程 ID 检测
   - 智能作业查找

4. **增强的任务管理器**
   - 课程切换功能
   - 课程列表显示
   - 当前课程状态显示

---

## 📁 文件结构

```
~/.agents/skills/ap-classroom/
├── SKILL.md                    # 技术文档
├── README.md                   # 使用说明
├── QUICKSTART.md              # 快速开始
├── RELEASE.md                 # 发布说明
│
├── start.bat                  # 主启动器
├── task-manager.ps1           # PowerShell 任务管理器
├── task-manager.bat           # 命令行任务管理器
├── create-shortcut.vbs        # 创建桌面快捷方式
│
├── check-browser-status.js    # 检查浏览器状态
├── list-courses.js            # 列出所有课程
├── select-course.js           # 选择课程
├── check-homework.js          # 检查作业
├── open-assignment.js         # 打开作业
├── get-questions.js           # 获取题目
├── answer-question.js         # 选择答案
├── next-question.js           # 下一题
├── submit-quiz.js             # 提交测验
├── complete-quiz.js           # 完整自动化
│
└── package.json               # 项目配置
```

---

## 🎯 支持的 AP 课程

### 完全支持（已测试）

- ✅ AP English Language and Composition
- ✅ AP Statistics

### 理论支持（未测试但应可用）

- ✅ AP English Literature and Composition
- ✅ AP Calculus AB/BC
- ✅ AP Computer Science A
- ✅ AP Computer Science Principles
- ✅ AP Biology
- ✅ AP Chemistry
- ✅ AP Physics 1/2/C
- ✅ AP World History
- ✅ AP US History
- ✅ AP European History
- ✅ AP Psychology
- ✅ AP Macroeconomics
- ✅ AP Microeconomics
- ✅ 所有其他 AP 课程

---

## 💻 系统要求

- **操作系统**: Windows 10/11
- **浏览器**: Google Chrome（最新版本）
- **Node.js**: v14.0.0 或更高
- **依赖**: Playwright

---

## 🚀 安装

### 方式 1: 直接使用（推荐）

Skill 已安装在 `~/.agents/skills/ap-classroom/`，可以直接使用。

### 方式 2: 从源码安装

```bash
git clone [repository-url]
cd ap-classroom
npm install
```

---

## 📋 快速测试

### 1. 检查浏览器

```powershell
cd ~/.agents/skills/ap-classroom
node check-browser-status.js
```

### 2. 列出课程

```powershell
node list-courses.js
```

### 3. 检查作业

```powershell
node check-homework.js
```

### 4. 使用任务管理器

```powershell
.\start.bat
# 或
.\task-manager.ps1
```

---

## ⚙️ 配置

### current-course.json

```json
{
  "name": "AP English Language and Composition",
  "id": "12",
  "lastChecked": "2026-03-19T10:00:00Z"
}
```

### course-config.json（可选）

```json
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

---

## 🐛 已知问题

1. **课程 ID 检测**
   - 某些课程可能无法自动检测 ID
   - 解决：手动导航到课程页面

2. **课程列表为空**
   - 需要先登录并访问 My AP
   - 解决：运行 `node list-courses.js` 重新检测

---

## 🔮 未来计划

- [ ] 自动化答题逻辑（AI 辅助）
- [ ] 批量作业完成
- [ ] 作业完成历史统计
- [ ] 多账号支持
- [ ] 邮件/消息通知
- [ ] Web UI 界面

---

## 🤝 贡献

欢迎贡献代码、报告问题或提出建议！

---

## 📄 许可证

MIT License

---

## 👥 致谢

- OpenClaw 团队
- Playwright 团队
- 所有测试用户

---

## 📞 支持

- **文档**: 查看 SKILL.md, README.md, QUICKSTART.md
- **问题**: 在 GitHub 上提 Issue
- **社区**: OpenClaw Discord

---

**发布日期**: 2026-03-19  
**版本**: 2.0.0  
**状态**: ✅ 稳定版
