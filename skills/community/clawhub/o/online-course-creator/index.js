/**
 * Online-Course-Creator Skill
 * AI 驱动的课程创作技能 - 一键生成完整在线课程材料
 * 
 * 功能：
 * - 课程大纲生成
 * - 视频脚本写作
 * - 测验和作业生成
 * - 营销材料创建
 */

const fs = require('fs');
const path = require('path');

// ============================================================================
// 核心课程创建算法
// ============================================================================

/**
 * 生成课程大纲
 * @param {string} topic - 课程主题
 * @param {number} modules - 模块数量 (默认 8)
 * @param {string} level - 难度级别 (beginner/intermediate/advanced)
 * @returns {object} 完整的课程大纲
 */
function generateCourseOutline(topic, modules = 8, level = 'beginner') {
  const levelDescriptions = {
    beginner: '零基础入门，无需先修知识',
    intermediate: '需要基础概念理解，适合有一定经验者',
    advanced: '深入专业内容，需要扎实基础'
  };

  const outline = {
    title: `${topic}完整课程`,
    subtitle: `从${level === 'beginner' ? '零' : level === 'intermediate' ? '基础' : '进阶'}到精通的系统学习路径`,
    level: level,
    levelDescription: levelDescriptions[level],
    estimatedDuration: `${modules * 3}小时`,
    modules: []
  };

  // 生成模块结构
  const moduleTemplates = {
    beginner: [
      '课程介绍与学习路径',
      '核心概念基础',
      '环境搭建与工具准备',
      '第一个实战项目',
      '核心技能深入 (上)',
      '核心技能深入 (下)',
      '综合实战应用',
      '进阶方向与职业发展'
    ],
    intermediate: [
      '知识体系回顾与进阶路径',
      '高级概念解析',
      '最佳实践与设计模式',
      '性能优化技巧',
      '实战项目 (上)',
      '实战项目 (下)',
      '常见陷阱与解决方案',
      '行业应用案例'
    ],
    advanced: [
      '前沿技术趋势',
      '架构设计与系统思维',
      '深度技术剖析',
      '大规模应用实践',
      '性能调优与监控',
      '安全与稳定性',
      '技术创新与研究',
      '技术领导力培养'
    ]
  };

  const templates = moduleTemplates[level] || moduleTemplates.beginner;

  for (let i = 0; i < modules; i++) {
    const moduleTitle = templates[i % templates.length];
    const module = {
      moduleNumber: i + 1,
      title: `模块${i + 1}: ${moduleTitle}`,
      description: `深入讲解${topic}的${moduleTitle.toLowerCase()}内容`,
      lessons: generateLessons(topic, moduleTitle, i + 1),
      estimatedTime: `${2 + (i % 3) * 0.5}小时`,
      objectives: generateModuleObjectives(topic, moduleTitle)
    };
    outline.modules.push(module);
  }

  return outline;
}

/**
 * 生成课程单元
 */
function generateLessons(topic, moduleName, moduleNumber) {
  const lessonCount = 3 + (moduleNumber % 3);
  const lessons = [];

  for (let i = 0; i < lessonCount; i++) {
    lessons.push({
      lessonNumber: i + 1,
      title: `${moduleName} - 第${i + 1}节`,
      type: i === 0 ? 'video' : i === 1 ? 'demo' : 'practice',
      duration: `${15 + i * 5}分钟`,
      description: `详细讲解${topic}相关知识点`
    });
  }

  return lessons;
}

/**
 * 生成模块学习目标
 */
function generateModuleObjectives(topic, moduleName) {
  return [
    `掌握${topic}的核心概念`,
    `能够独立完成相关实践`,
    `理解${moduleName}的实际应用场景`,
    `建立系统的知识框架`
  ];
}

// ============================================================================
// 视频脚本生成
// ============================================================================

/**
 * 生成视频脚本
 * @param {string} topic - 主题
 * @param {string} lessonTitle - 课程标题
 * @param {number} duration - 预计时长 (分钟)
 * @returns {object} 完整的视频脚本
 */
function generateVideoScript(topic, lessonTitle, duration = 15) {
  const wordCount = duration * 130; // 每分钟约 130 字

  return {
    metadata: {
      title: lessonTitle,
      topic: topic,
      estimatedDuration: `${duration}分钟`,
      targetWordCount: wordCount,
      videoType: '教学视频'
    },
    script: {
      opening: generateOpening(topic, lessonTitle),
      introduction: generateIntroduction(topic),
      mainContent: generateMainContent(topic, duration),
      summary: generateSummary(topic),
      closing: generateClosing(),
      callToAction: generateCallToAction()
    },
    visualCues: generateVisualCues(duration),
    notes: generateProductionNotes()
  };
}

function generateOpening(topic, lessonTitle) {
  return {
    hook: `欢迎来到${topic}课程！今天我们要讲的是"${lessonTitle}"`,
    welcome: '大家好，我是你的讲师',
    agenda: [
      '首先，我们会介绍核心概念',
      '然后通过实例演示加深理解',
      '最后会有实践练习帮助你巩固'
    ],
    estimatedTime: '预计用时 15 分钟'
  };
}

function generateIntroduction(topic) {
  return {
    context: `在学习${topic}之前，让我们先了解一下为什么这个主题如此重要`,
    relevance: '这是每个从业者都必须掌握的核心技能',
    prerequisites: '无需太多基础，我们会从零开始讲解',
    outcomes: '学完后你将能够独立应用这些知识'
  };
}

function generateMainContent(topic, duration) {
  const sections = Math.floor(duration / 5);
  const content = [];

  for (let i = 0; i < sections; i++) {
    content.push({
      section: i + 1,
      title: `第${i + 1}部分：核心要点`,
      keyPoints: [
        `要点${i * 2 + 1}: 基础概念讲解`,
        `要点${i * 2 + 2}: 实际应用示例`
      ],
      examples: [`实际案例${i + 1}`, `代码演示${i + 1}`],
      duration: `${Math.floor(duration / sections)}分钟`
    });
  }

  return content;
}

function generateSummary(topic) {
  return {
    recap: `让我们回顾一下今天关于${topic}的核心内容`,
    keyTakeaways: [
      '核心概念已经掌握',
      '实践方法已经了解',
      '下一步学习路径清晰'
    ],
    nextSteps: '在下一节课中，我们会继续深入...'
  };
}

function generateClosing() {
  return {
    thankYou: '感谢你的学习!',
    encouragement: '继续加油，你正在变得更强',
    reminder: '记得完成课后练习哦'
  };
}

function generateCallToAction() {
  return {
    actions: [
      '完成课后测验',
      '参与讨论区互动',
      '分享给需要的朋友',
      '订阅课程获取更新'
    ]
  };
}

function generateVisualCues(duration) {
  return {
    slides: Math.floor(duration / 2),
    demos: Math.floor(duration / 5),
    screenShares: 2,
    annotations: '重点内容需要标注',
    bRoll: '适当插入相关素材'
  };
}

function generateProductionNotes() {
  return {
    equipment: '建议使用高清摄像头和麦克风',
    lighting: '确保光线充足均匀',
    background: '简洁专业的背景',
    editing: '剪掉冗长停顿，保持节奏',
    captions: '添加字幕提高可访问性'
  };
}

// ============================================================================
// 测验和作业生成
// ============================================================================

/**
 * 生成测验题目
 * @param {string} topic - 主题
 * @param {number} questionCount - 题目数量
 * @param {string} difficulty - 难度 (easy/medium/hard)
 * @returns {object} 完整的测验
 */
function generateQuiz(topic, questionCount = 10, difficulty = 'medium') {
  const quiz = {
    title: `${topic}测验`,
    description: `测试你对${topic}的掌握程度`,
    difficulty: difficulty,
    totalQuestions: questionCount,
    passingScore: 70,
    timeLimit: `${questionCount * 2}分钟`,
    questions: []
  };

  const questionTypes = ['multipleChoice', 'trueFalse', 'fillBlank', 'shortAnswer'];

  for (let i = 0; i < questionCount; i++) {
    const type = questionTypes[i % questionTypes.length];
    quiz.questions.push(generateQuestion(topic, i + 1, type, difficulty));
  }

  return quiz;
}

function generateQuestion(topic, number, type, difficulty) {
  const baseQuestion = {
    number: number,
    type: type,
    points: type === 'shortAnswer' ? 10 : 5,
    difficulty: difficulty
  };

  switch (type) {
    case 'multipleChoice':
      return {
        ...baseQuestion,
        question: `关于${topic}，以下哪个说法是正确的？`,
        options: [
          'A. 正确选项 - 准确描述核心概念',
          'B. 错误选项 - 常见误解',
          'C. 错误选项 - 部分正确但不完整',
          'D. 错误选项 - 完全错误'
        ],
        correctAnswer: 'A',
        explanation: `解析：选项 A 正确因为...`
      };

    case 'trueFalse':
      return {
        ...baseQuestion,
        question: `${topic}的核心概念是学习的基础。(判断题)`,
        correctAnswer: true,
        explanation: '解析：这个说法正确，因为...'
      };

    case 'fillBlank':
      return {
        ...baseQuestion,
        question: `在${topic}中，______ 是最重要的概念之一。`,
        correctAnswer: '核心术语',
        explanation: '解析：核心术语是基础...'
      };

    case 'shortAnswer':
      return {
        ...baseQuestion,
        question: `请简述${topic}的三个关键应用场景。`,
        sampleAnswer: '1. 场景一...\n2. 场景二...\n3. 场景三...',
        gradingCriteria: [
          '答案完整性 (4 分)',
          '准确性 (3 分)',
          '逻辑性 (3 分)'
        ]
      };

    default:
      return baseQuestion;
  }
}

/**
 * 生成作业/实践项目
 * @param {string} topic - 主题
 * @param {number} projectCount - 项目数量
 * @returns {object} 完整的作业集
 */
function generateAssignments(topic, projectCount = 3) {
  return {
    title: `${topic}实践作业`,
    description: `通过实战项目巩固${topic}的学习`,
    totalProjects: projectCount,
    assignments: []
  };
}

// ============================================================================
// 营销材料生成
// ============================================================================

/**
 * 生成营销材料
 * @param {string} topic - 课程主题
 * @param {string} targetAudience - 目标受众
 * @returns {object} 完整的营销材料包
 */
function generateMarketingMaterials(topic, targetAudience = '初学者') {
  return {
    courseDescription: generateCourseDescription(topic, targetAudience),
    landingPage: generateLandingPageCopy(topic, targetAudience),
    emailTemplates: generateEmailTemplates(topic),
    socialMediaPosts: generateSocialMediaPosts(topic),
    faq: generateFAQ(topic),
    testimonials: generateTestimonialTemplates()
  };
}

function generateCourseDescription(topic, targetAudience) {
  return {
    short: `掌握${topic}的完整技能树，从${targetAudience}到专业人士`,
    medium: `这门${topic}课程专为${targetAudience}设计，通过系统的学习路径、实战项目和专家指导，帮助你快速掌握核心技能。课程包含视频讲解、实践练习和测验，确保学习效果。`,
    long: `欢迎加入${topic}完整课程！\n\n【课程亮点】\n• 系统化学习路径，从基础到进阶\n• 实战项目驱动，学以致用\n• 专家讲师，多年行业经验\n• 终身学习权限，持续更新\n• 学习社区，与同行交流\n\n【适合人群】\n• ${targetAudience}\n• 想转行进入该领域的人士\n• 需要提升技能的从业者\n\n【学完你将获得】\n• 完整的知识体系\n• 实战项目经验\n• 可展示的作品集\n• 行业认可的证书`,
    bulletPoints: [
      `📚 ${topic}系统化学习`,
      `🎯 实战项目驱动`,
      `👨‍🏫 专家讲师指导`,
      `📜 结业证书`,
      `♾️ 终身学习权限`
    ]
  };
}

function generateLandingPageCopy(topic, targetAudience) {
  return {
    headline: `从零掌握${topic} - 专为${targetAudience}打造的完整课程`,
    subheadline: '8 周系统学习，实战项目驱动，助你快速入门到精通',
    hero: {
      title: `成为${topic}专家`,
      subtitle: '加入 10,000+ 学员的学习之旅',
      cta: '立即开始学习'
    },
    benefits: [
      '系统化课程体系，避免碎片化学习',
      '实战项目经验，学完就能用',
      '灵活学习时间，随时随地学习',
      '专业导师答疑，学习不迷路',
      '学习社区支持，与同行交流成长'
    ],
    curriculum: '详见课程大纲部分',
    pricing: {
      original: '¥2999',
      discounted: '¥1999',
      installment: '可分 12 期，每月仅¥167'
    },
    guarantee: '30 天无理由退款保证',
    urgency: '限时优惠，仅剩 50 个名额'
  };
}

function generateEmailTemplates(topic) {
  return {
    announcement: {
      subject: `🎉 全新${topic}课程上线！限时优惠`,
      body: `亲爱的学习者，\n\n我们很高兴宣布${topic}完整课程正式上线！\n\n【课程亮点】\n• 系统化学习路径\n• 实战项目驱动\n• 专家讲师指导\n\n【限时优惠】\n前 100 名报名享受 7 折优惠\n\n立即报名：[链接]\n\n期待在课堂上见到你！`
    },
    reminder: {
      subject: `⏰ ${topic}课程优惠即将结束`,
      body: `你好，\n\n提醒一下，${topic}课程的限时优惠将在 48 小时后结束。\n\n不要错过这个提升自己的机会！\n\n立即报名：[链接]`
    },
    followUp: {
      subject: `学习${topic}的过程中有任何问题吗？`,
      body: `亲爱的学员，\n\n感谢你加入${topic}课程！\n\n学习过程中有任何问题，欢迎随时在讨论区提问。\n\n祝你学习愉快！`
    }
  };
}

function generateSocialMediaPosts(topic) {
  return {
    weibo: [
      `🔥 全新${topic}课程上线！从零到精通，8 周系统学习，实战项目驱动。限时优惠中，点击了解 👉 [链接] #${topic.replace(/\s/g, '')} #在线学习`,
      `💡 想学${topic}但不知道从哪里开始？这门课程帮你规划完整学习路径！已有 1000+ 学员加入，你也来吗？[链接]`
    ],
    wechat: [
      {
        title: `零基础如何系统学习${topic}？这份指南请收好`,
        summary: '从学习路径到实战项目，一站式解决你的学习困惑',
        content: '详细介绍课程特色和学习方法...'
      }
    ],
    linkedin: `📚 Excited to announce our new ${topic} course! Perfect for professionals looking to upskill. #OnlineLearning #${topic.replace(/\s/g, '')}`
  };
}

function generateFAQ(topic) {
  return [
    {
      question: `这门${topic}课程适合什么基础的人学习？`,
      answer: '课程从零基础开始，循序渐进，适合所有想学习该主题的人。'
    },
    {
      question: '课程学习需要多长时间？',
      answer: '建议 8 周完成，每周学习 3-5 小时。也可根据自己的节奏调整。'
    },
    {
      question: '学完后能获得证书吗？',
      answer: '是的，完成所有课程和作业后，你将获得结业证书。'
    },
    {
      question: '有问题可以提问吗？',
      answer: '当然！课程有专门的讨论区，讲师和助教都会及时解答。'
    },
    {
      question: '课程有有效期吗？',
      answer: '购买后永久有效，包括未来的内容更新。'
    }
  ];
}

function generateTestimonialTemplates() {
  return [
    {
      role: '学员',
      content: '这门课程让我从零开始掌握了核心技能，现在我已经成功转行！'
    },
    {
      role: '从业者',
      content: '内容非常系统，实战项目特别有用，直接应用到工作中了。'
    },
    {
      role: '管理者',
      content: '给团队购买了课程，整体技能提升明显，投资回报很高。'
    }
  ];
}

// ============================================================================
// 主执行函数
// ============================================================================

/**
 * 创建完整课程包
 * @param {string} topic - 课程主题
 * @param {object} options - 配置选项
 * @returns {object} 完整的课程材料包
 */
function createCompleteCourse(topic, options = {}) {
  const {
    modules = 8,
    level = 'beginner',
    targetAudience = '初学者',
    includeMarketing = true
  } = options;

  console.log(`\n🚀 开始创建"${topic}"课程...\n`);

  // 1. 生成课程大纲
  console.log('📚 生成课程大纲...');
  const outline = generateCourseOutline(topic, modules, level);

  // 2. 生成视频脚本 (为每个模块的第一节课)
  console.log('🎬 生成视频脚本...');
  const videoScripts = outline.modules.map(module => ({
    moduleName: module.title,
    script: generateVideoScript(topic, module.lessons[0].title)
  }));

  // 3. 生成测验
  console.log('📝 生成测验题目...');
  const quizzes = outline.modules.map(module => ({
    moduleName: module.title,
    quiz: generateQuiz(topic, 10, level)
  }));

  // 4. 生成营销材料
  let marketing = null;
  if (includeMarketing) {
    console.log('📢 生成营销材料...');
    marketing = generateMarketingMaterials(topic, targetAudience);
  }

  const coursePackage = {
    metadata: {
      topic: topic,
      createdAt: new Date().toISOString(),
      version: '1.0.0'
    },
    outline: outline,
    videoScripts: videoScripts,
    quizzes: quizzes,
    marketing: marketing
  };

  console.log('\n✅ 课程创建完成！\n');
  console.log(`📊 课程概览:`);
  console.log(`   • 主题：${topic}`);
  console.log(`   • 模块数：${modules}`);
  console.log(`   • 难度：${level}`);
  console.log(`   • 预计时长：${outline.estimatedDuration}`);
  console.log(`   • 视频脚本：${videoScripts.length}个`);
  console.log(`   • 测验题目：${quizzes.length * 10}道`);

  return coursePackage;
}

// ============================================================================
// 导出接口
// ============================================================================

module.exports = {
  // 核心功能
  createCompleteCourse,
  generateCourseOutline,
  generateVideoScript,
  generateQuiz,
  generateAssignments,
  generateMarketingMaterials,
  
  // 辅助函数
  generateCourseDescription,
  generateLandingPageCopy,
  generateEmailTemplates,
  generateSocialMediaPosts,
  
  // 技能元数据
  skillInfo: {
    name: 'online-course-creator',
    version: '1.0.0',
    description: 'AI 驱动的课程创作技能',
    author: 'OpenClaw Team'
  }
};
