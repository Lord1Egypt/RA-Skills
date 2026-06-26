---
name: mooc-learner
description: MOOC自动化学习工具 - 自动完成课程视频学习、检测章节状态、等待视频播放完成
---

# MOOC自动化学习工具 (增强版)

本Skill提供基于Playwright的MOOC平台自动化学习功能。

## 何时使用本Skill

当用户请求以下操作时使用本Skill：
- 自动学习MOOC课程视频
- 批量完成课程章节学习
- 自动化视频播放和完成检测

## 功能特性

1. **多课程支持** - 支持配置多个课程，自动逐个学习
2. **自动章节检测** - 识别"开始学习"、"继续学习"、"复习"状态的章节
3. **视频播放监控** - 等待视频播放完成，支持进度检测和完成状态识别
4. **弹窗智能处理** - 自动关闭学习过程中的确认弹窗
5. **防休眠机制** - 随机点击防止屏幕休眠
6. **进度保存** - 意外中断后可恢复学习进度
7. **异常自动恢复** - 网络异常时自动刷新重试
8. **学习统计报告** - 生成详细的学习报告

## 使用方法

### 环境要求

- Node.js 18+
- 已安装Playwright: `npm install playwright`
- Chrome浏览器

### 安装依赖

```bash
cd <skill目录>
npm install playwright
```

### 配置课程

编辑 `scripts/learn-courses.js`，在 `CONFIG.COURSES` 数组中添加目标课程：

```javascript
COURSES: [
  {
    id: 'course-1',
    name: '课程名称',
    url: 'https://mooc.ctt.cn/#/study/subject/detail/...'
  }
],
```

### 运行脚本

```bash
node scripts/learn-courses.js
```

## 配置文件说明

| 配置项 | 说明 |
|--------|------|
| `CONFIG.COURSES` | 课程列表，支持多个 |
| `CONFIG.VIDEO.MAX_WAIT_SECONDS` | 视频最大等待时间 |
| `CONFIG.BROWSER.HEADLESS` | 是否无头模式 |

## 输出文件

- `learning-progress.json` - 学习进度保存
- `learning-report.json` - 学习统计报告

## 注意事项

1. 本工具仅用于个人学习辅助，请遵守平台服务条款
2. 建议在夜间运行以避开高峰期
3. 部分平台可能有反自动化机制，请适度使用
