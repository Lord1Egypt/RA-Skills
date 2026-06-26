// Learning Path Navigator - 路由层
// 负责接收学习请求，生成个性化学习路径

import type { LearningRequest, LearningPathResponse, LearningPath, LearningPhase, PhaseResource, Milestone, WeeklyPlan } from "./types";

// 生成唯一ID
function generateId(prefix: string): string {
  return `${prefix}_${Date.now().toString(36)}_${Math.random().toString(36).substr(2, 6)}`;
}

// 计算目标熟练度对应的数值
function levelToScore(level: string): number {
  const map: Record<string, number> = {
    'beginner': 30,
    'intermediate': 70,
    'advanced': 90,
    'expert': 98,
  };
  return map[level] || 50;
}

// 计算阶段数量
function calculatePhaseCount(totalWeeks: number): number {
  if (totalWeeks <= 4) return 1;
  if (totalWeeks <= 8) return 2;
  if (totalWeeks <= 16) return 3;
  return Math.ceil(totalWeeks / 4);
}

// 生成学习阶段
function generatePhases(request: LearningRequest, totalWeeks: number, hoursPerWeek: number): LearningPhase[] {
  const phases: LearningPhase[] = [];
  const phaseCount = calculatePhaseCount(totalWeeks);
  const weeksPerPhase = Math.ceil(totalWeeks / phaseCount);
  const hoursPerPhase = hoursPerWeek * weeksPerPhase;
  
  const skills = request.goal?.skills || ['相关技能'];
  const targetLevel = request.goal?.targetLevel || 'intermediate';
  
  const phaseTitles = [
    '基础概念与入门',
    '核心知识与实践',
    '进阶应用与项目',
    '专项深化与拓展',
  ];
  
  for (let i = 0; i < phaseCount; i++) {
    const phaseWeeks = Math.min(weeksPerPhase, totalWeeks - i * weeksPerPhase);
    const phaseHours = hoursPerWeek * phaseWeeks;
    
    // 生成每周计划
    const weeklyBreakdown: WeeklyPlan[] = [];
    for (let w = 0; w < phaseWeeks; w++) {
      weeklyBreakdown.push({
        week: i * weeksPerPhase + w + 1,
        focus: `第${w + 1}周：${['基础夯实', '技能提升', '综合应用', '项目实战'][w % 4]}`,
        hours: hoursPerWeek,
        resources: [
          { type: 'course', title: `${skills[0] || '该技能'}系统课程`, duration: '4小时', format: 'interactive' },
          { type: 'exercise', title: '实践练习题', duration: '3小时', format: 'interactive' },
          { type: 'video', title: '配套视频教程', duration: '2小时', format: 'video' },
          { type: 'article', title: '参考资料阅读', duration: '1小时', format: 'text' },
        ],
        milestones: w === phaseWeeks - 1 ? [
          { title: '阶段测验', passingScore: 80, deadline: `第${i * weeksPerPhase + w + 1}周末` }
        ] : [],
      });
    }
    
    // 生成阶段资源
    const phaseResources: PhaseResource[] = [
      {
        resourceId: generateId('res'),
        type: 'course',
        title: `${phaseTitles[i]} - 系统课程`,
        description: `完成${phaseTitles[i]}的全部内容学习`,
        duration: `${Math.round(phaseHours * 0.4)}小时`,
        format: 'online',
        qualityScore: 4.5,
        completionRate: 92,
        cost: '免费',
      },
      {
        resourceId: generateId('res'),
        type: 'project',
        title: `${phaseTitles[i]}实战项目`,
        description: '完成一个综合性实践项目',
        duration: `${Math.round(phaseHours * 0.3)}小时`,
        format: 'interactive',
        qualityScore: 4.7,
        completionRate: 85,
        cost: '免费',
      },
      {
        resourceId: generateId('res'),
        type: 'book',
        title: '推荐参考书籍',
        description: '深入学习的补充材料',
        duration: `${Math.round(phaseHours * 0.2)}小时`,
        format: 'text',
        qualityScore: 4.3,
        completionRate: 60,
        cost: '¥30-80',
      },
    ];
    
    phases.push({
      id: generateId('phase'),
      phaseNumber: i + 1,
      title: `阶段${i + 1}：${phaseTitles[i] || `学习阶段${i + 1}`}`,
      description: `本阶段将完成${phaseTitles[i]}，为后续学习打下坚实基础`,
      duration: {
        weeks: phaseWeeks,
        totalHours: phaseHours,
        weeklyBreakdown,
      },
      objectives: [
        '掌握核心概念和基本原理',
        '完成配套实践练习',
        '通过阶段评估测试',
      ],
      skillsCovered: skills.slice(0, Math.ceil(skills.length / phaseCount) * (i + 1)),
      resources: phaseResources,
      assessments: [
        {
          id: generateId('assess'),
          name: '阶段综合测验',
          type: 'quiz',
          passingScore: 80,
        },
        {
          id: generateId('assess'),
          name: '实践项目评估',
          type: 'project',
          passingScore: 75,
        },
      ],
      successCriteria: {
        knowledgeCheck: ['完成所有章节学习', '测验得分≥80分'],
        practicalProjects: ['完成实战项目', '项目评分≥75分'],
        minimumScores: { quizzes: 80, projects: 75, overall: 78 },
      },
    });
  }
  
  return phases;
}

// 生成里程碑
function generateMilestones(phases: LearningPhase[], startDate: Date, totalWeeks: number): Milestone[] {
  const milestones: Milestone[] = [];
  
  phases.forEach((phase, idx) => {
    const phaseStartWeek = idx === 0 ? 0 : phases.slice(0, idx).reduce((sum, p) => sum + p.duration.weeks, 0);
    const milestoneWeek = phaseStartWeek + phase.duration.weeks;
    const milestoneDate = new Date(startDate);
    milestoneDate.setDate(milestoneDate.getDate() + milestoneWeek * 7);
    
    milestones.push({
      id: generateId('milestone'),
      title: `${phase.title}完成`,
      description: `完成${phase.title}所有内容，达到阶段学习目标`,
      phaseId: phase.id,
      scheduledDate: milestoneDate.toISOString().split('T')[0],
      requirements: [
        '完成所有阶段资源学习',
        `通过阶段测验（≥${phase.successCriteria.minimumScores.quizzes}分）`,
        '提交实践项目',
      ],
      passingScore: phase.successCriteria.minimumScores.overall,
      status: 'pending',
      reward: idx < phases.length - 1 ? `解锁下一阶段内容+学习资料包` : '获得结业证书',
    });
  });
  
  return milestones;
}

// 生成补充资源
function generateSupplementaryResources(skills: string[]): { category: string; items: string[] }[] {
  return [
    {
      category: '参考书籍',
      items: [
        '《深入理解XX技能》',
        '《实战指南》',
        '《高级特性详解》',
      ],
    },
    {
      category: '练习平台',
      items: [
        'LeetCode / 专项练习',
        'GitHub开源项目',
        '在线编程实验室',
      ],
    },
    {
      category: '社区资源',
      items: [
        '官方文档',
        '技术博客',
        '学习交流群',
      ],
    },
  ];
}

// 生成每周检查点
function generateWeeklyCheckpoints(totalWeeks: number, startDate: Date): { week: number; date: string; checkpoint: string }[] {
  const checkpoints: { week: number; date: string; checkpoint: string }[] = [];
  const checkpointWeeks = [1, 2, 4, 8, 12, 16].filter(w => w <= totalWeeks);
  
  checkpointWeeks.forEach(week => {
    const date = new Date(startDate);
    date.setDate(date.getDate() + (week - 1) * 7);
    checkpoints.push({
      week,
      date: date.toISOString().split('T')[0],
      checkpoint: `第${week}周学习成果检验`,
    });
  });
  
  return checkpoints;
}

// 主路由函数
export async function runDecisionEngine(request: LearningRequest): Promise<LearningPathResponse> {
  try {
    // 解析请求参数
    const goalDesc = request.goal?.description || '提升相关技能';
    const skills = request.goal?.skills || extractSkills(goalDesc);
    const targetLevel = request.goal?.targetLevel || 'intermediate';
    const totalWeeks = request.goal?.timeframe?.totalWeeks || 12;
    const hoursPerWeek = request.goal?.timeframe?.hoursPerWeek || 10;
    
    // 计算完成日期
    const startDate = new Date();
    const completionDate = new Date(startDate);
    completionDate.setDate(completionDate.getDate() + totalWeeks * 7);
    
    // 生成学习阶段
    const phases = generatePhases(request, totalWeeks, hoursPerWeek);
    
    // 生成里程碑
    const milestones = generateMilestones(phases, startDate, totalWeeks);
    
    // 生成学习路径
    const learningPath: LearningPath = {
      id: generateId('path'),
      title: `${skills[0] || '技能提升'}专家之路 - ${totalWeeks}周计划`,
      goal: {
        description: goalDesc,
        targetSkills: skills.map(s => ({ skill: s, targetLevel: targetLevel })),
      },
      phases,
      milestones,
      resources: {
        primary: phases.flatMap(p => p.resources),
        supplementary: generateSupplementaryResources(skills),
      },
      progressTracking: {
        currentPhase: 1,
        overallProgress: '0%',
        estimatedCompletion: completionDate.toISOString().split('T')[0],
        weeklyCheckpoints: generateWeeklyCheckpoints(totalWeeks, startDate),
      },
      adaptiveFeatures: {
        difficultyAdjustment: '基于测验成绩自动调整下一阶段难度',
        resourceRecommendation: '根据学习风格和进度个性化推荐',
        scheduleFlexibility: '允许±2周时间缓冲，可根据实际情况调整',
      },
    };
    
    return {
      success: true,
      learningPath,
      recommendations: [
        '建议每天固定时间学习，保持学习的连续性',
        '每周预留2-3小时用于复习和练习',
        '加入学习社群获取同伴支持和答疑',
        '定期记录学习笔记和心得体会',
      ],
      nextSteps: [
        '确认并开始第一阶段学习',
        '设置每周学习提醒',
        '加入推荐的学习社区',
        '准备第一周所需的学习资源',
      ],
    };
  } catch (error) {
    return {
      success: false,
      error: `生成学习路径失败: ${error instanceof Error ? error.message : '未知错误'}`,
    };
  }
}

// 从描述中提取技能
function extractSkills(description: string): string[] {
  // 简单的技能提取逻辑
  const commonSkills = [
    'Python', 'JavaScript', 'Java', 'Go', 'Rust', 'C++',
    '数据分析', '机器学习', '深度学习', '人工智能',
    '前端开发', '后端开发', '全栈开发', '移动开发',
    '数据结构', '算法', '数据库', '云计算', 'DevOps',
  ];
  
  return commonSkills.filter(skill => 
    description.toLowerCase().includes(skill.toLowerCase())
  ).slice(0, 5) || ['综合技能'];
}
