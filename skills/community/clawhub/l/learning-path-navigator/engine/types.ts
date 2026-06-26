// Learning Path Navigator 类型定义

export type ProficiencyLevel = 'beginner' | 'intermediate' | 'advanced' | 'expert';
export type ResourceType = 'course' | 'book' | 'video' | 'tutorial' | 'article' | 'podcast' | 'exercise' | 'project' | 'cheatsheet' | 'community';
export type LearningStyle = 'visual' | 'auditory' | 'kinesthetic' | 'reading' | 'mixed';
export type DifficultyLevel = 'beginner' | 'intermediate' | 'advanced' | 'expert';
export type ProgressStatus = 'not-started' | 'in-progress' | 'completed' | 'paused' | 'abandoned';

// 学习目标
export interface LearningGoal {
  id: string;
  title: string;
  description: string;
  skills: SkillRequirement[];
  targetLevel: ProficiencyLevel;
  timeframe: {
    totalWeeks: number;
    hoursPerWeek: number;
    deadline?: string;
  };
  constraints: {
    budget?: number;
    preferredFormats: ResourceType[];
    languages?: string[];
  };
}

// 技能要求
export interface SkillRequirement {
  skillId: string;
  skillName: string;
  targetProficiency: number;
  priority: 'high' | 'medium' | 'low';
  dependencies: string[];
}

// 用户当前水平
export interface CurrentProficiency {
  skills: {
    skillId: string;
    selfAssessment: number;
    testScore?: number;
    confidence: number;
  }[];
  learningStyle: {
    visual: number;
    auditory: number;
    kinesthetic: number;
    reading: number;
  };
  constraints: {
    availableHours: number;
    preferredTimes?: string[];
    maxSessionLength?: number;
  };
}

// 学习请求
export interface LearningRequest {
  goal?: {
    description: string;
    skills?: string[];
    targetLevel?: ProficiencyLevel;
    timeframe?: {
      totalWeeks?: number;
      hoursPerWeek?: number;
      deadline?: string;
    };
  };
  currentLevel?: {
    skills?: { skillId: string; level: number }[];
    selfAssessment?: string;
    testResults?: string;
  };
  constraints?: {
    budget?: number;
    preferredFormats?: ResourceType[];
    learningStyle?: LearningStyle;
    languages?: string[];
  };
}

// 学习阶段
export interface LearningPhase {
  id: string;
  phaseNumber: number;
  title: string;
  description: string;
  duration: {
    weeks: number;
    totalHours: number;
    weeklyBreakdown: WeeklyPlan[];
  };
  objectives: string[];
  skillsCovered: string[];
  resources: PhaseResource[];
  assessments: AssessmentPlan[];
  successCriteria: {
    knowledgeCheck: string[];
    practicalProjects: string[];
    minimumScores: {
      quizzes: number;
      projects: number;
      overall: number;
    };
  };
}

// 每周计划
export interface WeeklyPlan {
  week: number;
  focus: string;
  hours: number;
  resources: ResourceSummary[];
  milestones: MilestoneSummary[];
}

// 资源摘要
export interface ResourceSummary {
  type: ResourceType;
  title: string;
  url?: string;
  duration: string;
  format: string;
}

// 里程碑摘要
export interface MilestoneSummary {
  title: string;
  passingScore?: number;
  deadline?: string;
}

// 阶段资源
export interface PhaseResource {
  resourceId: string;
  type: ResourceType;
  title: string;
  url?: string;
  description: string;
  duration: string;
  format: string;
  qualityScore?: number;
  completionRate?: number;
  cost: string;
}

// 评估计划
export interface AssessmentPlan {
  id: string;
  name: string;
  type: 'quiz' | 'project' | 'presentation' | 'peer-review' | 'self-assessment';
  scheduledDate?: string;
  passingScore: number;
}

// 里程碑
export interface Milestone {
  id: string;
  title: string;
  description: string;
  phaseId: string;
  scheduledDate: string;
  requirements: string[];
  passingScore?: number;
  status: 'pending' | 'in-progress' | 'completed' | 'failed';
  reward?: string;
}

// 学习路径
export interface LearningPath {
  id: string;
  title: string;
  goal: {
    description: string;
    targetSkills: { skill: string; targetLevel: string }[];
  };
  phases: LearningPhase[];
  milestones: Milestone[];
  resources: {
    primary: PhaseResource[];
    supplementary: { category: string; items: string[] }[];
  };
  progressTracking: {
    currentPhase: number;
    overallProgress: string;
    estimatedCompletion: string;
    weeklyCheckpoints: { week: number; date: string; checkpoint: string }[];
  };
  adaptiveFeatures: {
    difficultyAdjustment: string;
    resourceRecommendation: string;
    scheduleFlexibility: string;
  };
}

// 学习路径响应
export interface LearningPathResponse {
  success: boolean;
  learningPath?: LearningPath;
  recommendations?: string[];
  nextSteps?: string[];
  error?: string;
}
