/**
 * A/B 测试查询数据
 * 20个测试查询，覆盖不同难度和场景
 */

export interface TestQuery {
  id: string;
  query: string;
  expectedKeywords: string[];
  difficulty: 'easy' | 'medium' | 'hard';
  expectedMemoryIds: string[]; // 期望命中的记忆ID
  description: string; // 查询意图说明
}

export const testQueries: TestQuery[] = [
  // ========== 简单查询 (Easy) - 7个 ==========
  // 直接关键词匹配，无歧义
  {
    id: 'query-001',
    query: '用户喜欢吃什么？',
    expectedKeywords: ['川菜', '麻婆豆腐', '水煮鱼'],
    difficulty: 'easy',
    expectedMemoryIds: ['mem-001'],
    description: '直接查询偏好，关键词明确'
  },
  {
    id: 'query-002',
    query: '项目什么时候截止？',
    expectedKeywords: ['4月1日', '截止'],
    difficulty: 'easy',
    expectedMemoryIds: ['mem-011'],
    description: '查询截止日期，单一记忆'
  },
  {
    id: 'query-003',
    query: '会议室在哪里？',
    expectedKeywords: ['会议室', '3楼', '会议室A', '会议室B'],
    difficulty: 'easy',
    expectedMemoryIds: ['mem-012', 'mem-021'],
    description: '查询会议室信息，涉及多个记忆'
  },
  {
    id: 'query-004',
    query: 'Jenkins 地址是什么？',
    expectedKeywords: ['jenkins.company.com'],
    difficulty: 'easy',
    expectedMemoryIds: ['mem-015'],
    description: '查询具体地址，精确匹配'
  },
  {
    id: 'query-005',
    query: '技术总监是谁？',
    expectedKeywords: ['张伟', '技术总监'],
    difficulty: 'easy',
    expectedMemoryIds: ['mem-029'],
    description: '查询人物角色'
  },
  {
    id: 'query-006',
    query: '项目用什么数据库？',
    expectedKeywords: ['PostgreSQL', 'Redis', 'MongoDB'],
    difficulty: 'easy',
    expectedMemoryIds: ['mem-039'],
    description: '查询技术选型'
  },
  {
    id: 'query-007',
    query: '女儿生日是哪天？',
    expectedKeywords: ['3月22日', '生日', '女儿'],
    difficulty: 'easy',
    expectedMemoryIds: ['mem-024'],
    description: '查询家庭重要日期'
  },

  // ========== 中等查询 (Medium) - 8个 ==========
  // 需要语义理解或跨记忆关联
  {
    id: 'query-008',
    query: '最近有什么重要的截止日期需要注意？',
    expectedKeywords: ['4月1日', '3月25日', '3月30日', '截止'],
    difficulty: 'medium',
    expectedMemoryIds: ['mem-011', 'mem-019', 'mem-027'],
    description: '查询多个截止日期，需要聚合'
  },
  {
    id: 'query-009',
    query: '团队成员的联系方式有哪些？',
    expectedKeywords: ['zhang.wei@company.com', '138-xxxx-xxxx', '139-xxxx-xxxx'],
    difficulty: 'medium',
    expectedMemoryIds: ['mem-029', 'mem-032', 'mem-035'],
    description: '查询联系信息，跨多个记忆'
  },
  {
    id: 'query-010',
    query: '这个月有什么会议安排？',
    expectedKeywords: ['周三', '周五', '周一', '会议'],
    difficulty: 'medium',
    expectedMemoryIds: ['mem-012', 'mem-021', 'mem-023', 'mem-025'],
    description: '查询会议，需要时间范围理解'
  },
  {
    id: 'query-011',
    query: '项目有什么风险需要注意？',
    expectedKeywords: ['风险', '支付', '延期', '备选方案'],
    difficulty: 'medium',
    expectedMemoryIds: ['mem-041'],
    description: '查询项目风险，需要语义理解'
  },
  {
    id: 'query-012',
    query: '我之前说过的编程语言偏好是什么？',
    expectedKeywords: ['TypeScript', '类型安全', 'JavaScript'],
    difficulty: 'medium',
    expectedMemoryIds: ['mem-005'],
    description: '查询偏好，需要理解"编程语言偏好"'
  },
  {
    id: 'query-013',
    query: '新人入职相关的事情有哪些？',
    expectedKeywords: ['小陈', '前端组', '导师', '培训资料', 'onboarding'],
    difficulty: 'medium',
    expectedMemoryIds: ['mem-017', 'mem-034'],
    description: '查询入职相关，需要跨类别关联'
  },
  {
    id: 'query-014',
    query: '代码相关的工作流程是怎样的？',
    expectedKeywords: ['代码审查', '24小时', 'Git Flow', '分支'],
    difficulty: 'medium',
    expectedMemoryIds: ['mem-013', 'mem-038'],
    description: '查询工作流程，需要理解语义'
  },
  {
    id: 'query-015',
    query: '健康和运动相关的安排有什么？',
    expectedKeywords: ['牙医', '3月15日', '健身', '爬山'],
    difficulty: 'medium',
    expectedMemoryIds: ['mem-006', 'mem-022', 'mem-026'],
    description: '查询健康运动，跨类别聚合'
  },

  // ========== 复杂查询 (Hard) - 5个 ==========
  // 需要深度语义理解、推理或多跳关联
  {
    id: 'query-016',
    query: '如果明天是周三，我需要准备什么？',
    expectedKeywords: ['技术分享', '下午2点', '会议室B'],
    difficulty: 'hard',
    expectedMemoryIds: ['mem-021'],
    description: '需要推理：今天是周几 + 周三有什么安排'
  },
  {
    id: 'query-017',
    query: '下周有什么需要提前准备的事情？',
    expectedKeywords: ['3月14日', '技术债务', '3月15日', '牙医', '3月20日', '演示', 'PPT', 'Demo'],
    difficulty: 'hard',
    expectedMemoryIds: ['mem-016', 'mem-022', 'mem-020'],
    description: '需要时间推理和多记忆关联'
  },
  {
    id: 'query-018',
    query: '我在技术方面想达成什么目标？',
    expectedKeywords: ['Rust', '开源', 'Contributor', '学习'],
    difficulty: 'hard',
    expectedMemoryIds: ['mem-050'],
    description: '需要理解"技术目标"的语义范围'
  },
  {
    id: 'query-019',
    query: '项目的关键技术决策有哪些？',
    expectedKeywords: ['Go', 'gRPC', 'React', 'TypeScript', 'K8s', 'PostgreSQL', 'Redis', 'MongoDB', 'Git Flow'],
    difficulty: 'hard',
    expectedMemoryIds: ['mem-038', 'mem-039', 'mem-043'],
    description: '需要聚合多个技术决策记忆'
  },
  {
    id: 'query-020',
    query: '团队中如果遇到紧急问题应该联系谁？',
    expectedKeywords: ['运维', '老周', '139-xxxx-xxxx', '紧急'],
    difficulty: 'hard',
    expectedMemoryIds: ['mem-035'],
    description: '需要理解"紧急问题"与"运维/紧急联系人"的关联'
  }
];

/**
 * 按难度统计
 */
export const difficultyStats = {
  easy: testQueries.filter(q => q.difficulty === 'easy').length,
  medium: testQueries.filter(q => q.difficulty === 'medium').length,
  hard: testQueries.filter(q => q.difficulty === 'hard').length
};

/**
 * 获取特定难度的查询
 */
export function getQueriesByDifficulty(difficulty: 'easy' | 'medium' | 'hard'): TestQuery[] {
  return testQueries.filter(q => q.difficulty === difficulty);
}

/**
 * 获取特定类别的记忆
 */
export function getMemoriesByCategory(category: string): string[] {
  return testQueries
    .filter(q => q.expectedMemoryIds.some(id => id.startsWith(`mem-`) && category === 'all'))
    .map(q => q.expectedMemoryIds)
    .flat();
}