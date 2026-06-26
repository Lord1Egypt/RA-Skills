/**
 * A/B 测试记忆数据
 * 50条不同类型的记忆，覆盖多种场景
 */

export interface TestMemory {
  id: string;
  content: string;
  category: 'preference' | 'work' | 'schedule' | 'person' | 'project' | 'knowledge' | 'habit' | 'goal';
  tags: string[];
  importance: 'high' | 'medium' | 'low';
  createdAt: string;
}

export const testMemories: TestMemory[] = [
  // ========== 偏好类 (Preference) - 10条 ==========
  {
    id: 'mem-001',
    content: '用户喜欢吃川菜，尤其是麻婆豆腐和水煮鱼',
    category: 'preference',
    tags: ['食物', '川菜', '辣'],
    importance: 'medium',
    createdAt: '2026-03-01T10:00:00Z'
  },
  {
    id: 'mem-002',
    content: '用户偏好深色主题的代码编辑器，喜欢 JetBrains Mono 字体',
    category: 'preference',
    tags: ['工具', '编辑器', '主题'],
    importance: 'low',
    createdAt: '2026-03-02T14:30:00Z'
  },
  {
    id: 'mem-003',
    content: '用户喜欢喝美式咖啡，不加糖不加奶',
    category: 'preference',
    tags: ['饮料', '咖啡', '习惯'],
    importance: 'low',
    createdAt: '2026-03-03T09:15:00Z'
  },
  {
    id: 'mem-004',
    content: '用户喜欢在安静的环境下工作，偏好使用降噪耳机',
    category: 'preference',
    tags: ['工作环境', '设备'],
    importance: 'medium',
    createdAt: '2026-03-04T11:20:00Z'
  },
  {
    id: 'mem-005',
    content: '用户喜欢用 TypeScript 而不是 JavaScript，认为类型安全很重要',
    category: 'preference',
    tags: ['编程语言', 'TypeScript'],
    importance: 'high',
    createdAt: '2026-03-05T16:45:00Z'
  },
  {
    id: 'mem-006',
    content: '用户喜欢周末去爬山，最近一次去了香山',
    category: 'preference',
    tags: ['运动', '户外', '爬山'],
    importance: 'low',
    createdAt: '2026-03-06T08:00:00Z'
  },
  {
    id: 'mem-007',
    content: '用户偏好使用 VS Code 作为主要开发工具，安装了 Vim 插件',
    category: 'preference',
    tags: ['工具', 'VS Code', 'Vim'],
    importance: 'medium',
    createdAt: '2026-03-07T13:30:00Z'
  },
  {
    id: 'mem-008',
    content: '用户喜欢阅读科幻小说，最喜欢的作家是刘慈欣',
    category: 'preference',
    tags: ['阅读', '科幻', '刘慈欣'],
    importance: 'low',
    createdAt: '2026-03-08T20:00:00Z'
  },
  {
    id: 'mem-009',
    content: '用户喜欢用深蓝色的笔记本做会议记录',
    category: 'preference',
    tags: ['文具', '笔记', '会议'],
    importance: 'low',
    createdAt: '2026-03-09T15:00:00Z'
  },
  {
    id: 'mem-010',
    content: '用户喜欢吃日料，特别是三文鱼刺身和鳗鱼饭',
    category: 'preference',
    tags: ['食物', '日料', '刺身'],
    importance: 'medium',
    createdAt: '2026-03-10T12:00:00Z'
  },

  // ========== 工作类 (Work) - 10条 ==========
  {
    id: 'mem-011',
    content: '项目截止日期是2026年4月1日，需要在此之前完成核心功能开发',
    category: 'work',
    tags: ['项目', '截止日期', '开发'],
    importance: 'high',
    createdAt: '2026-03-01T09:00:00Z'
  },
  {
    id: 'mem-012',
    content: '团队每周一上午10点召开站会，地点在3楼会议室A',
    category: 'work',
    tags: ['会议', '站会', '周一'],
    importance: 'medium',
    createdAt: '2026-03-02T10:00:00Z'
  },
  {
    id: 'mem-013',
    content: '代码审查需要在提交后24小时内完成，审查人是王工和李工',
    category: 'work',
    tags: ['代码审查', '流程', '团队'],
    importance: 'high',
    createdAt: '2026-03-03T14:00:00Z'
  },
  {
    id: 'mem-014',
    content: '产品需求文档存放在 /docs/requirements 目录下，命名格式为 PRD-YYYY-MM-DD',
    category: 'work',
    tags: ['文档', 'PRD', '规范'],
    importance: 'medium',
    createdAt: '2026-03-04T11:30:00Z'
  },
  {
    id: 'mem-015',
    content: 'Jenkins 构建服务器地址是 jenkins.company.com，部署分支是 main',
    category: 'work',
    tags: ['CI/CD', 'Jenkins', '部署'],
    importance: 'high',
    createdAt: '2026-03-05T16:00:00Z'
  },
  {
    id: 'mem-016',
    content: '技术债务清理计划定于每两周的周五下午进行，下次时间是3月14日',
    category: 'work',
    tags: ['技术债务', '计划', '周五'],
    importance: 'medium',
    createdAt: '2026-03-06T17:00:00Z'
  },
  {
    id: 'mem-017',
    content: '新员工入职培训资料在 /docs/onboarding 目录，需要更新安全模块',
    category: 'work',
    tags: ['培训', '入职', '文档'],
    importance: 'medium',
    createdAt: '2026-03-07T09:30:00Z'
  },
  {
    id: 'mem-018',
    content: 'API 文档使用 Swagger 生成，访问地址是 api.company.com/docs',
    category: 'work',
    tags: ['API', '文档', 'Swagger'],
    importance: 'medium',
    createdAt: '2026-03-08T10:15:00Z'
  },
  {
    id: 'mem-019',
    content: '季度绩效评估截止日期是3月25日，需要完成自评和同事评价',
    category: 'work',
    tags: ['绩效', '评估', '截止日期'],
    importance: 'high',
    createdAt: '2026-03-09T14:30:00Z'
  },
  {
    id: 'mem-020',
    content: '客户演示定于3月20日下午2点，需要准备产品演示PPT和Demo环境',
    category: 'work',
    tags: ['演示', '客户', '准备'],
    importance: 'high',
    createdAt: '2026-03-10T08:00:00Z'
  },

  // ========== 日程类 (Schedule) - 8条 ==========
  {
    id: 'mem-021',
    content: '每周三下午2点有固定的技术分享会，地点在会议室B',
    category: 'schedule',
    tags: ['会议', '周三', '技术分享'],
    importance: 'medium',
    createdAt: '2026-03-01T14:00:00Z'
  },
  {
    id: 'mem-022',
    content: '3月15日上午9点有牙医预约，地点在中关村口腔医院',
    category: 'schedule',
    tags: ['医疗', '牙医', '预约'],
    importance: 'high',
    createdAt: '2026-03-02T09:00:00Z'
  },
  {
    id: 'mem-023',
    content: '每周五下午5点是团队聚餐时间，这周去吃火锅',
    category: 'schedule',
    tags: ['聚餐', '周五', '团队'],
    importance: 'low',
    createdAt: '2026-03-03T17:00:00Z'
  },
  {
    id: 'mem-024',
    content: '3月22日是女儿的生日，需要提前准备礼物和蛋糕',
    category: 'schedule',
    tags: ['家庭', '生日', '重要'],
    importance: 'high',
    createdAt: '2026-03-04T10:00:00Z'
  },
  {
    id: 'mem-025',
    content: '每月最后一个周四下午3点有部门例会',
    category: 'schedule',
    tags: ['会议', '部门', '每月'],
    importance: 'medium',
    createdAt: '2026-03-05T15:00:00Z'
  },
  {
    id: 'mem-026',
    content: '健身计划是每周二和周四晚上7点，地点在楼下健身房',
    category: 'schedule',
    tags: ['健身', '运动', '规律'],
    importance: 'medium',
    createdAt: '2026-03-06T19:00:00Z'
  },
  {
    id: 'mem-027',
    content: '3月30日需要提交年度总结报告',
    category: 'schedule',
    tags: ['报告', '年度', '截止'],
    importance: 'high',
    createdAt: '2026-03-07T09:00:00Z'
  },
  {
    id: 'mem-028',
    content: '每周日上午10点有线上英语课程，持续12周',
    category: 'schedule',
    tags: ['学习', '英语', '课程'],
    importance: 'medium',
    createdAt: '2026-03-08T10:00:00Z'
  },

  // ========== 人物类 (Person) - 8条 ==========
  {
    id: 'mem-029',
    content: '张伟是技术总监，负责整体技术架构决策，联系方式是 zhang.wei@company.com',
    category: 'person',
    tags: ['同事', '领导', '技术'],
    importance: 'high',
    createdAt: '2026-03-01T11:00:00Z'
  },
  {
    id: 'mem-030',
    content: '李明是前端组长，React 技术专家，工位在4楼B区',
    category: 'person',
    tags: ['同事', '前端', '组长'],
    importance: 'medium',
    createdAt: '2026-03-02T14:00:00Z'
  },
  {
    id: 'mem-031',
    content: '王芳是产品经理，负责核心产品线，性格开朗，喜欢喝奶茶',
    category: 'person',
    tags: ['同事', '产品', 'PM'],
    importance: 'medium',
    createdAt: '2026-03-03T10:30:00Z'
  },
  {
    id: 'mem-032',
    content: '客户方对接人是刘总，电话138-xxxx-xxxx，下午3点后方便接电话',
    category: 'person',
    tags: ['客户', '对接人', '重要'],
    importance: 'high',
    createdAt: '2026-03-04T15:00:00Z'
  },
  {
    id: 'mem-033',
    content: '赵博士是技术顾问，专精于分布式系统，每月来公司两次',
    category: 'person',
    tags: ['顾问', '分布式', '专家'],
    importance: 'medium',
    createdAt: '2026-03-05T16:00:00Z'
  },
  {
    id: 'mem-034',
    content: '新人小陈刚入职两周，分配在前端组，需要安排导师指导',
    category: 'person',
    tags: ['新人', '前端', '指导'],
    importance: 'medium',
    createdAt: '2026-03-06T10:00:00Z'
  },
  {
    id: 'mem-035',
    content: '运维老周负责服务器维护，紧急问题可以打他手机 139-xxxx-xxxx',
    category: 'person',
    tags: ['同事', '运维', '紧急'],
    importance: 'high',
    createdAt: '2026-03-07T09:00:00Z'
  },
  {
    id: 'mem-036',
    content: '设计组的小林擅长 UI 设计，作品集在 behance.net/xiaolin',
    category: 'person',
    tags: ['同事', '设计', 'UI'],
    importance: 'low',
    createdAt: '2026-03-08T11:30:00Z'
  },

  // ========== 项目类 (Project) - 7条 ==========
  {
    id: 'mem-037',
    content: '项目 Aurora 是新的微服务架构平台，预计6月份上线，预算50万',
    category: 'project',
    tags: ['项目', '微服务', '新平台'],
    importance: 'high',
    createdAt: '2026-03-01T09:30:00Z'
  },
  {
    id: 'mem-038',
    content: '项目代码仓库在 gitlab.company.com/aurora/main，分支策略采用 Git Flow',
    category: 'project',
    tags: ['Git', '仓库', 'Git Flow'],
    importance: 'medium',
    createdAt: '2026-03-02T10:00:00Z'
  },
  {
    id: 'mem-039',
    content: '项目使用 PostgreSQL 作为主数据库，Redis 作为缓存，MongoDB 存日志',
    category: 'project',
    tags: ['数据库', 'PostgreSQL', 'Redis'],
    importance: 'medium',
    createdAt: '2026-03-03T11:00:00Z'
  },
  {
    id: 'mem-040',
    content: '项目二期计划增加 AI 推荐功能，需要对接算法团队',
    category: 'project',
    tags: ['功能', 'AI', '推荐'],
    importance: 'high',
    createdAt: '2026-03-04T14:00:00Z'
  },
  {
    id: 'mem-041',
    content: '项目风险点：第三方支付接口可能延期，需要准备备选方案',
    category: 'project',
    tags: ['风险', '支付', '延期'],
    importance: 'high',
    createdAt: '2026-03-05T16:30:00Z'
  },
  {
    id: 'mem-042',
    content: '项目性能目标是 QPS 5000，P99 延迟小于 200ms',
    category: 'project',
    tags: ['性能', 'QPS', '目标'],
    importance: 'medium',
    createdAt: '2026-03-06T09:00:00Z'
  },
  {
    id: 'mem-043',
    content: '项目技术栈：后端 Go + gRPC，前端 React + TypeScript，部署 K8s',
    category: 'project',
    tags: ['技术栈', 'Go', 'React'],
    importance: 'high',
    createdAt: '2026-03-07T10:00:00Z'
  },

  // ========== 知识类 (Knowledge) - 4条 ==========
  {
    id: 'mem-044',
    content: 'Go 语言的 context 包用于控制请求的生命周期和超时，最佳实践是总是传递 context',
    category: 'knowledge',
    tags: ['Go', '编程', '最佳实践'],
    importance: 'medium',
    createdAt: '2026-03-01T15:00:00Z'
  },
  {
    id: 'mem-045',
    content: 'React 的 useCallback 和 useMemo 可以优化性能，但不要过度使用',
    category: 'knowledge',
    tags: ['React', '性能', '优化'],
    importance: 'medium',
    createdAt: '2026-03-02T16:00:00Z'
  },
  {
    id: 'mem-046',
    content: 'Docker 容器时区默认是 UTC，需要设置 TZ=Asia/Shanghai 来修正',
    category: 'knowledge',
    tags: ['Docker', '时区', '配置'],
    importance: 'low',
    createdAt: '2026-03-03T14:00:00Z'
  },
  {
    id: 'mem-047',
    content: 'Kubernetes 的 livenessProbe 和 readinessProbe 用途不同，前者判断是否重启，后者判断是否接收流量',
    category: 'knowledge',
    tags: ['K8s', '健康检查', '探针'],
    importance: 'medium',
    createdAt: '2026-03-04T11:00:00Z'
  },

  // ========== 习惯类 (Habit) - 2条 ==========
  {
    id: 'mem-048',
    content: '每天早上8点半到公司，先泡一杯咖啡再看邮件',
    category: 'habit',
    tags: ['作息', '咖啡', '习惯'],
    importance: 'low',
    createdAt: '2026-03-01T08:30:00Z'
  },
  {
    id: 'mem-049',
    content: '每天下班前整理当天的工作笔记，记录明天要做的事情',
    category: 'habit',
    tags: ['笔记', '工作', '习惯'],
    importance: 'medium',
    createdAt: '2026-03-02T18:00:00Z'
  },

  // ========== 目标类 (Goal) - 1条 ==========
  {
    id: 'mem-050',
    content: '今年目标是学习 Rust 语言，完成一个小型开源项目，争取成为 Contributor',
    category: 'goal',
    tags: ['学习', 'Rust', '开源', '目标'],
    importance: 'high',
    createdAt: '2026-03-01T09:00:00Z'
  }
];

/**
 * 按类别统计
 */
export const categoryStats = {
  preference: testMemories.filter(m => m.category === 'preference').length,
  work: testMemories.filter(m => m.category === 'work').length,
  schedule: testMemories.filter(m => m.category === 'schedule').length,
  person: testMemories.filter(m => m.category === 'person').length,
  project: testMemories.filter(m => m.category === 'project').length,
  knowledge: testMemories.filter(m => m.category === 'knowledge').length,
  habit: testMemories.filter(m => m.category === 'habit').length,
  goal: testMemories.filter(m => m.category === 'goal').length
};

/**
 * 按重要性统计
 */
export const importanceStats = {
  high: testMemories.filter(m => m.importance === 'high').length,
  medium: testMemories.filter(m => m.importance === 'medium').length,
  low: testMemories.filter(m => m.importance === 'low').length
};