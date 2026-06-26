# AP Classroom Skill - 使用示例

## 📚 示例场景

### 场景 1: 首次使用

```powershell
# 1. 安装
cd ~/.agents/skills/ap-classroom
.\install.bat

# 2. 启动 Chrome（调试模式）
Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" `
  -ArgumentList "--remote-debugging-port=9223"

# 3. 登录 College Board（在浏览器中）

# 4. 启动任务管理器
.\start.bat
# 选择 [1] PowerShell 界面

# 5. 检查状态
# 在任务管理器中按 [1]

# 6. 查看作业
# 在任务管理器中按 [2]
```

---

### 场景 2: 完成 AP Lang 作业

```powershell
# 1. 启动任务管理器
cd ~/.agents/skills/ap-classroom
.\start.bat

# 2. 检查当前课程
按 [1] - 应该显示 "AP English Language and Composition"

# 3. 查看作业
按 [2] - 显示所有待完成作业

# 4. 打开作业
按 [3]
输入: Unit 9: Claims and Evidence - Reading Quiz

# 5. 获取题目
按 [4] - 显示当前题目和选项

# 6. 选择答案
按 [5]
输入: A

# 7. 下一题
按 [6]

# 8. 重复步骤 5-7 直到所有题目完成

# 9. 提交
按 [7]
确认: Y
```

---

### 场景 3: 切换到 AP Statistics

```powershell
# 1. 在任务管理器中
按 [C] - 切换课程

# 2. 从列表中选择
输入课程编号

# 3. 查看作业
按 [2]

# 4. 完成作业
# ... 同场景 2
```

---

### 场景 4: 使用命令行（高级用户）

```powershell
cd ~/.agents/skills/ap-classroom

# 检查状态
node check-browser-status.js

# 查看作业
node check-homework.js

# 打开作业
node open-assignment.js "Unit 9 Reading Quiz"

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

### 场景 5: 检查所有课程的作业

```powershell
# 1. 列出所有课程
cd ~/.agents/skills/ap-classroom
node list-courses.js

# 2. 逐个检查
foreach ($course in @("AP Lang", "AP Stats", "AP CS")) {
    Write-Host "检查 $course ..." -ForegroundColor Green
    # 手动切换课程
    node select-course.js
    # 检查作业
    node check-homework.js
    Read-Host "按回车继续下一门课程"
}
```

---

### 场景 6: 批量完成多个测验

```powershell
# 1. 启动任务管理器
.\start.bat

# 2. 完成第一个测验
按 [3] → 输入作业名称 → 完成所有题目 → 提交

# 3. 返回作业列表
# 自动返回或手动导航

# 4. 完成第二个测验
按 [3] → 输入作业名称 → 完成所有题目 → 提交

# 5. 重复步骤 4
```

---

## 🎯 常见任务

### 任务 1: 检查今天要完成的作业

```powershell
cd ~/.agents/skills/ap-classroom

# 方法 1: 使用任务管理器
.\start.bat
按 [2]

# 方法 2: 使用命令行
node check-homework.js
```

### 任务 2: 查看当前登录的课程

```powershell
node check-browser-status.js
```

### 任务 3: 切换到另一门课程

```powershell
# 方法 1: 使用任务管理器
.\start.bat
按 [C]

# 方法 2: 使用命令行
node select-course.js
```

### 任务 4: 创建桌面快捷方式

```powershell
cd ~/.agents/skills/ap-classroom
.\start.bat
# 选择 [3] 创建桌面快捷方式
```

---

## 💡 技巧和最佳实践

### 技巧 1: 使用任务管理器

**优势**:
- ✅ 图形化菜单
- ✅ 彩色显示
- ✅ 当前课程显示
- ✅ 快速切换课程

**启动**:
```powershell
.\start.bat
# 选择 [1] PowerShell 界面
```

### 技巧 2: 定期检查所有课程

**建议**: 每周检查一次所有课程的作业

**流程**:
1. 列出所有课程
2. 逐个切换并检查
3. 记录待完成作业
4. 按优先级完成

### 技巧 3: 提交前检查

**建议**: 提交前仔细检查所有答案

**流程**:
1. 完成所有题目
2. 截图保存
3. 人工检查答案
4. 确认后提交

### 技巧 4: 使用截图功能

**用途**:
- 📸 记录题目
- 📸 记录答案
- 📸 记录提交状态

**自动保存位置**:
- `current-question.png` - 当前题目
- `answer-selected.png` - 选择的答案
- `before-submit.png` - 提交前状态
- `after-submit.png` - 提交后状态

---

## ⚠️ 注意事项

### 注意 1: 浏览器保持打开

**规则**: Skill 不会关闭浏览器

**原因**:
- 保留登录状态
- 避免重新登录
- 节省时间

**操作**: 如需关闭浏览器，请手动操作

### 注意 2: 提交前确认

**建议**: 提交测验前务必确认所有答案

**原因**:
- 提交后无法修改
- 影响最终成绩

**操作**: 使用 [8] 提交时会要求确认

### 注意 3: 网络连接

**要求**: 稳定的网络连接

**建议**:
- 使用有线网络
- 避免在提交时断网
- 定期保存进度

---

## 🆘 故障排查示例

### 问题 1: 无法连接到浏览器

**症状**: `connect ECONNREFUSED 127.0.0.1:9223`

**解决**:
```powershell
# 1. 关闭所有 Chrome
taskkill /F /IM chrome.exe /T

# 2. 重新启动（调试模式）
Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" `
  -ArgumentList "--remote-debugging-port=9223"

# 3. 检查端口
netstat -ano | findstr ":9223"
```

### 问题 2: 课程列表为空

**解决**:
```powershell
# 1. 确保已登录
# 在浏览器中访问 myap.collegeboard.org

# 2. 重新检测
node list-courses.js

# 3. 手动导航到课程页面
# 然后运行
node check-browser-status.js
```

### 问题 3: 找不到作业

**解决**:
```powershell
# 1. 检查当前课程
node check-browser-status.js

# 2. 确认课程正确
# 如不正确，切换课程

# 3. 刷新页面
# 在浏览器中按 F5

# 4. 重新检查
node check-homework.js
```

---

## 📊 性能优化

### 优化 1: 减少等待时间

**方法**: 根据网络速度调整等待时间

**修改**: 编辑脚本中的 `waitForTimeout` 值

### 优化 2: 批量操作

**方法**: 一次完成多个测验

**建议**: 使用任务管理器快速切换

### 优化 3: 缓存课程信息

**方法**: 保存课程配置

**文件**: `current-course.json`

---

## 🎉 完成！

现在你已经了解了 AP Classroom Skill 的所有使用方法！

**下一步**:
1. 尝试完成第一个作业
2. 探索所有功能
3. 根据需要调整配置

**需要帮助**?
- 查看 README.md
- 查看 SKILL.md
- 运行 `node check-browser-status.js`
