# Online-Course-Creator 🎓

AI 驱动的课程创作技能 - 一键生成完整在线课程材料

## 🌟 功能亮点

### 📚 课程大纲生成
- 根据主题自动生成结构化课程大纲
- 支持自定义模块数量 (默认 8 个)
- 三种难度级别：入门/进阶/高级
- 每个模块包含详细的学习目标和课时安排

### 🎬 视频脚本写作
- 为每个课程单元撰写详细的视频脚本
- 包含开场、介绍、主体内容、总结、结尾
- 提供视觉提示和制作建议
- 根据时长自动调整内容深度

### 📝 测验和作业生成
- 多种题型：选择题、判断题、填空题、简答题
- 自动配题答案解析
- 实践项目设计
- 评分标准制定

### 📢 营销材料创建
- 课程描述 (短/中/长版本)
- 落地页文案
- 邮件营销模板
- 社交媒体文案
- FAQ 常见问题
- 学员见证模板

## 🚀 快速开始

### 安装

```bash
# 通过 ClawHub 安装
clawhub install online-course-creator

# 或手动安装
git clone https://github.com/openclaw/online-course-creator.git
cd online-course-creator
npm install
```

### 基础使用

```javascript
const courseCreator = require('online-course-creator');

// 创建完整课程包
const course = courseCreator.createCompleteCourse('Python 数据分析', {
  modules: 8,
  level: 'beginner',
  targetAudience: '零基础学习者',
  includeMarketing: true
});

console.log(course);
```

### 单独使用功能

```javascript
// 生成课程大纲
const outline = courseCreator.generateCourseOutline('机器学习', 10, 'intermediate');

// 生成视频脚本
const script = courseCreator.generateVideoScript('Python', '变量与数据类型', 15);

// 生成测验
const quiz = courseCreator.generateQuiz('Web 开发', 10, 'medium');

// 生成营销材料
const marketing = courseCreator.generateMarketingMaterials('UI 设计', '设计师');
```

## 📖 使用示例

### 示例 1: 创建编程课程

```javascript
const course = courseCreator.createCompleteCourse('JavaScript 全栈开发', {
  modules: 12,
  level: 'beginner',
  targetAudience: '编程新手'
});

// 输出包含:
// - 12 个模块的详细大纲
// - 每个模块的视频脚本
// - 配套测验题目
// - 完整营销材料
```

### 示例 2: 创建商业课程

```javascript
const course = courseCreator.createCompleteCourse('数字营销策略', {
  modules: 6,
  level: 'intermediate',
  targetAudience: '市场从业者'
});
```

### 示例 3: 创建设计课程

```javascript
const course = courseCreator.createCompleteCourse('Figma UI 设计', {
  modules: 8,
  level: 'beginner',
  targetAudience: '设计师'
});
```

## 📊 输出结构

```javascript
{
  metadata: {
    topic: "课程主题",
    createdAt: "2026-03-15T14:16:00.000Z",
    version: "1.0.0"
  },
  outline: {
    title: "课程标题",
    subtitle: "课程副标题",
    level: "难度级别",
    estimatedDuration: "总时长",
    modules: [
      {
        moduleNumber: 1,
        title: "模块标题",
        description: "模块描述",
        lessons: [...],
        estimatedTime: "预计时长",
        objectives: [...]
      }
    ]
  },
  videoScripts: [...],
  quizzes: [...],
  marketing: {
    courseDescription: {...},
    landingPage: {...},
    emailTemplates: {...},
    socialMediaPosts: {...},
    faq: [...],
    testimonials: [...]
  }
}
```

## 🎯 适用场景

- **在线教育从业者** - 快速创建课程内容
- **知识博主** - 将知识体系化
- **企业培训师** - 制作内部培训材料
- **内容创作者** - 拓展知识付费产品
- **教育机构** - 标准化课程生产

## 💡 最佳实践

### 1. 明确目标受众
```javascript
// 针对初学者
level: 'beginner',
targetAudience: '零基础学习者'

// 针对进阶者
level: 'intermediate',
targetAudience: '有 1-2 年经验的从业者'
```

### 2. 合理设置模块数量
- 入门课程：6-8 个模块
- 进阶课程：8-12 个模块
- 高级课程：10-15 个模块

### 3. 充分利用营销材料
- 根据目标平台选择合适的文案
- A/B 测试不同的营销话术
- 定期更新社交媒体内容

## 🔧 API 参考

### createCompleteCourse(topic, options)
创建完整课程包

**参数:**
- `topic` (string): 课程主题
- `options.modules` (number): 模块数量，默认 8
- `options.level` (string): 难度级别，'beginner'|'intermediate'|'advanced'
- `options.targetAudience` (string): 目标受众
- `options.includeMarketing` (boolean): 是否包含营销材料，默认 true

**返回:** 完整课程对象

### generateCourseOutline(topic, modules, level)
生成课程大纲

**参数:**
- `topic` (string): 课程主题
- `modules` (number): 模块数量
- `level` (string): 难度级别

**返回:** 课程大纲对象

### generateVideoScript(topic, lessonTitle, duration)
生成视频脚本

**参数:**
- `topic` (string): 主题
- `lessonTitle` (string): 课程标题
- `duration` (number): 预计时长 (分钟)

**返回:** 视频脚本对象

### generateQuiz(topic, questionCount, difficulty)
生成测验

**参数:**
- `topic` (string): 主题
- `questionCount` (number): 题目数量
- `difficulty` (string): 难度，'easy'|'medium'|'hard'

**返回:** 测验对象

### generateMarketingMaterials(topic, targetAudience)
生成营销材料

**参数:**
- `topic` (string): 课程主题
- `targetAudience` (string): 目标受众

**返回:** 营销材料对象

## 💰 定价

**$119/月** - 专业课程创作工具

包含：
- ✅ 无限课程创建
- ✅ 所有功能模块
- ✅ 持续更新
- ✅ 技术支持

## 📈 预期收益

### 目标市场
- 全球在线教育市场：$3500 亿+
- 中国知识付费市场：¥1000 亿+
- 年增长率：20%+

### 收益预测
- 保守估计：50 用户 × $119 = $5,950/月
- 中等估计：100 用户 × $119 = $11,900/月
- 乐观估计：150 用户 × $119 = $17,850/月

### 用户获取策略
1. 内容营销 - 分享课程设计技巧
2. 社交媒体 - 展示课程案例
3. 合作伙伴 - 与教育平台合作
4. 免费试用 - 7 天免费体验
5. 推荐奖励 - 老用户推荐优惠

## 🤝 贡献

欢迎贡献代码和建议！

```bash
# Fork 项目
git fork https://github.com/openclaw/online-course-creator

# 创建分支
git checkout -b feature/your-feature

# 提交更改
git commit -m 'Add new feature'

# 推送分支
git push origin feature/your-feature

# 创建 Pull Request
```

## 📄 许可证

MIT License

## 👥 作者

**OpenClaw Team**

- Website: https://openclaw.ai
- Twitter: @openclaw
- Email: team@openclaw.ai

## 🙏 致谢

感谢所有贡献者和用户！

---

**Made with ❤️ for educators and content creators**
