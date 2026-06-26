# 项目开发工作流详细说明

## 核心原则

**随时可中断，随时可继续。让任何人都能通过阅读日志，无缝接手任何项目。**

## 四大场景

### 场景一：新建项目

**触发：** 用户说「新建项目」「创建项目」

**执行：**
```bash
python log_project.py -a new -p <项目路径> -n <项目名称>
```

**自动创建：**
1. 项目根目录
2. 标准文件夹结构（logs/configs/firmware/docs/hardware/references/tools）
3. PROJECT_INFO.md（项目信息模板）
4. logs/devlog_YYYY-MM-DD.md（初始化日志）

**日志记录：**
```markdown
## [时间] [INFO] 项目初始化完成
## [时间] [INFO] 创建文件夹：logs, configs, firmware, docs, hardware, references, tools
## [时间] [INFO] 创建项目信息文件：PROJECT_INFO.md
## [时间] [STANDARD] 项目开发工作流已建立
```

---

### 场景二：继续项目

**触发：** 用户发送已有项目路径，说「继续」「接着上次」

**执行顺序（不可跳过）：**
```bash
# 1. 查看项目结构
python log_project.py -a structure -p <项目路径>

# 2. 读取最新日志
python log_project.py -a read -p <项目路径>

# 3. 查看进度摘要
python log_project.py -a progress -p <项目路径>
```

**输出总结：**
- 上次进展到哪里？
- 有什么问题待解决？
- 下一步做什么？

**日志记录：**
```markdown
## [时间] [INFO] 继续项目：<项目名称>
## [时间] [INFO] 上次进度：<描述>
## [时间] [INFO] 当前状态：<描述>
## [时间] [PROGRESS] 继续任务：<下一步>
```

---

### 场景三：日常开发记录

**触发：** 开发过程中任何重要时刻

**命令：**
```bash
python log_project.py -a log -p <项目路径> -m <消息> -c <类别>
```

**记录规范：**
| 类别 | 触发时机 |
|------|----------|
| INFO | 任务开始/完成、状态更新 |
| ERROR | 任何错误（编译/运行/配置） |
| FIXED | 问题的解决方案 |
| PROGRESS | 进行中的里程碑 |
| WARNING | 潜在风险 |
| SUCCESS | 重要里程碑达成 |

---

### 场景四：资料搜索与保存

**触发：** 开发中需要某组件的资料

**执行：**
1. 联网搜索组件信息
2. 分析资料的适用性
3. 保存到对应目录：
   - `hardware/` - 硬件规格、数据手册
   - `references/` - 开发文档、教程
   - `configs/` - 配置文件示例
4. 在日志中记录

**日志记录：**
```markdown
## [时间] [INFO] 搜索资料：<组件名称>
## [时间] [INFO] 找到资料：<来源>
## [时间] [INFO] 保存到：<文件路径>
```

---

## 日志格式规范

### 时间戳格式
```
[YYYY-MM-DD HH:MM:SS]
```

### 完整条目示例
```markdown
## [2026-03-21 19:30:00] [INFO] 项目初始化完成
- 项目名称：智能家居控制器
- 技术栈：ESP32-S3, FreeRTOS, LVGL
- 下一步：点亮屏幕

## [2026-03-21 19:45:00] [PROGRESS] 开始ST7789屏幕驱动开发

## [2026-03-21 20:00:00] [ERROR] 编译失败：TFT_eSPI引脚定义冲突
- 错误：User_Setup.h默认值覆盖build_flags

## [2026-03-21 20:10:00] [FIXED] 创建自定义User_Setup_Select.h
- 解决方案：在include/目录创建自定义配置
- 文件：include/User_Setup_Select.h

## [2026-03-21 20:20:00] [INFO] 烧录成功，屏幕点亮
```

---

## 断点续接检查清单

### 开始工作前
- [ ] 已读取最近日志
- [ ] 了解当前进度
- [ ] 知道待解决问题
- [ ] 有明确的下一步行动

### 结束工作前
- [ ] 关键结果已记录
- [ ] 错误信息已保存
- [ ] 下次继续的起点已标记

---

## 项目信息模板 (PROJECT_INFO.md)

```markdown
# 项目名称

## 基础信息
- 项目名称：
- 创建时间：
- 项目路径：

## 项目概述
<!-- 简要描述项目 -->

## 技术栈
- 主芯片/框架：
- 关键组件：
- 开发工具：

## 开发进度
- [ ] 需求分析
- [ ] 硬件选型
- [ ] 原理图设计
- [ ] 固件开发
- [ ] 调试测试
- [ ] 完成

## 当前问题
<!-- 记录待解决的问题 -->

## 下一步计划
1. 
2. 
3. 

## 版本历史
| 日期 | 版本 | 变化 |
|------|------|------|
| | | |
```

---

## 工具脚本用法

```bash
# === 新建项目 ===
python log_project.py -a new -p E:\MyProject -n "我的项目"

# === 开发记录 ===
python log_project.py -a log -p E:\MyProject -m "任务完成" -c SUCCESS
python log_project.py -a log -p E:\MyProject -m "出现问题" -c ERROR

# === 查看状态 ===
python log_project.py -a read -p E:\MyProject      # 最新日志
python log_project.py -a progress -p E:\MyProject  # 进度摘要
python log_project.py -a structure -p E:\MyProject # 项目结构
python log_project.py -a list -p E:\MyProject      # 所有日志

# === 时间旅行 ===
python log_project.py -a read -p E:\MyProject -d 2026-03-20  # 指定日期
```
