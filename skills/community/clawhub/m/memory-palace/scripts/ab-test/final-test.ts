/**
 * Jarvis Memory Palace Final Test - Full Optimized Version
 * Tests: Vector Search + Time Reasoning + Concept Expansion
 */

import { MemoryPalaceManager } from '../../src/manager.js';
import { LocalVectorSearchProvider } from '../../src/background/vector-search.js';
import * as fs from 'fs/promises';
import * as path from 'path';

// Test data inline
const testMemories = [
  // ========== 偏好类 (Preference) - 10条 ==========
  { id: 'mem-001', content: '用户喜欢吃川菜，尤其是麻婆豆腐和水煮鱼', tags: ['食物', '川菜', '辣'], importance: 'medium' },
  { id: 'mem-002', content: '用户偏好深色主题的代码编辑器，喜欢 JetBrains Mono 字体', tags: ['工具', '编辑器', '主题'], importance: 'low' },
  { id: 'mem-003', content: '用户喜欢喝美式咖啡，不加糖不加奶', tags: ['饮料', '咖啡', '习惯'], importance: 'low' },
  { id: 'mem-004', content: '用户喜欢在安静的环境下工作，偏好使用降噪耳机', tags: ['工作环境', '设备'], importance: 'medium' },
  { id: 'mem-005', content: '用户喜欢用 TypeScript 而不是 JavaScript，认为类型安全很重要', tags: ['编程语言', 'TypeScript'], importance: 'high' },
  { id: 'mem-006', content: '用户喜欢周末去爬山，最近一次去了香山', tags: ['运动', '户外', '爬山'], importance: 'low' },
  { id: 'mem-007', content: '用户偏好使用 VS Code 作为主要开发工具，安装了 Vim 插件', tags: ['工具', 'VS Code', 'Vim'], importance: 'medium' },
  { id: 'mem-008', content: '用户喜欢阅读科幻小说，最喜欢的作家是刘慈欣', tags: ['阅读', '科幻', '刘慈欣'], importance: 'low' },
  { id: 'mem-009', content: '用户喜欢用深蓝色的笔记本做会议记录', tags: ['文具', '笔记', '会议'], importance: 'low' },
  { id: 'mem-010', content: '用户喜欢吃日料，特别是三文鱼刺身和鳗鱼饭', tags: ['食物', '日料', '刺身'], importance: 'medium' },

  // ========== 工作类 (Work) - 10条 ==========
  { id: 'mem-011', content: '项目截止日期是2026年4月1日，需要在此之前完成核心功能开发', tags: ['项目', '截止日期', '开发'], importance: 'high' },
  { id: 'mem-012', content: '团队每周一上午10点召开站会，地点在3楼会议室A', tags: ['会议', '站会', '周一'], importance: 'medium' },
  { id: 'mem-013', content: '代码审查需要在提交后24小时内完成，审查人是王工和李工', tags: ['代码审查', '流程', '团队'], importance: 'high' },
  { id: 'mem-014', content: '产品需求文档存放在 /docs/requirements 目录下，命名格式为 PRD-YYYY-MM-DD', tags: ['文档', 'PRD', '规范'], importance: 'medium' },
  { id: 'mem-015', content: 'Jenkins 构建服务器地址是 jenkins.company.com，部署分支是 main', tags: ['CI/CD', 'Jenkins', '部署'], importance: 'high' },
  { id: 'mem-016', content: '技术债务清理计划定于每两周的周五下午进行，下次时间是3月14日', tags: ['技术债务', '计划', '周五'], importance: 'medium' },
  { id: 'mem-017', content: '新员工入职培训资料在 /docs/onboarding 目录，需要更新安全模块', tags: ['培训', '入职', '文档'], importance: 'medium' },
  { id: 'mem-018', content: 'API 文档使用 Swagger 生成，访问地址是 api.company.com/docs', tags: ['API', '文档', 'Swagger'], importance: 'medium' },
  { id: 'mem-019', content: '季度绩效评估截止日期是3月25日，需要完成自评和同事评价', tags: ['绩效', '评估', '截止日期'], importance: 'high' },
  { id: 'mem-020', content: '客户演示定于3月20日下午2点，需要准备产品演示PPT和Demo环境', tags: ['演示', '客户', '准备'], importance: 'high' },

  // ========== 日程类 (Schedule) - 8条 ==========
  { id: 'mem-021', content: '每周三下午2点有固定的技术分享会，地点在会议室B', tags: ['会议', '周三', '技术分享'], importance: 'medium' },
  { id: 'mem-022', content: '3月15日上午9点有牙医预约，地点在中关村口腔医院', tags: ['医疗', '牙医', '预约'], importance: 'high' },
  { id: 'mem-023', content: '每周五下午5点是团队聚餐时间，这周去吃火锅', tags: ['聚餐', '周五', '团队'], importance: 'low' },
  { id: 'mem-024', content: '3月22日是女儿的生日，需要提前准备礼物和蛋糕', tags: ['家庭', '生日', '重要'], importance: 'high' },
  { id: 'mem-025', content: '每月最后一个周四下午3点有部门例会', tags: ['会议', '部门', '每月'], importance: 'medium' },
  { id: 'mem-026', content: '健身计划是每周二和周四晚上7点，地点在楼下健身房', tags: ['健身', '运动', '规律'], importance: 'medium' },
  { id: 'mem-027', content: '3月30日需要提交年度总结报告', tags: ['报告', '年度', '截止'], importance: 'high' },
  { id: 'mem-028', content: '每周日上午10点有线上英语课程，持续12周', tags: ['学习', '英语', '课程'], importance: 'medium' },

  // ========== 人物类 (Person) - 8条 ==========
  { id: 'mem-029', content: '张伟是技术总监，负责整体技术架构决策，联系方式是 zhang.wei@company.com', tags: ['同事', '领导', '技术'], importance: 'high' },
  { id: 'mem-030', content: '李明是前端组长，React 技术专家，工位在4楼B区', tags: ['同事', '前端', '组长'], importance: 'medium' },
  { id: 'mem-031', content: '王芳是产品经理，负责核心产品线，性格开朗，喜欢喝奶茶', tags: ['同事', '产品', 'PM'], importance: 'medium' },
  { id: 'mem-032', content: '客户方对接人是刘总，电话138-xxxx-xxxx，下午3点后方便接电话', tags: ['客户', '对接人', '重要'], importance: 'high' },
  { id: 'mem-033', content: '赵博士是技术顾问，专精于分布式系统，每月来公司两次', tags: ['顾问', '分布式', '专家'], importance: 'medium' },
  { id: 'mem-034', content: '新人小陈刚入职两周，分配在前端组，需要安排导师指导', tags: ['新人', '前端', '指导'], importance: 'medium' },
  { id: 'mem-035', content: '运维老周负责服务器维护，紧急问题可以打他手机 139-xxxx-xxxx', tags: ['同事', '运维', '紧急'], importance: 'high' },
  { id: 'mem-036', content: '设计组的小林擅长 UI 设计，作品集在 behance.net/xiaolin', tags: ['同事', '设计', 'UI'], importance: 'low' },

  // ========== 项目类 (Project) - 7条 ==========
  { id: 'mem-037', content: '项目 Aurora 是新的微服务架构平台，预计6月份上线，预算50万', tags: ['项目', '微服务', '新平台'], importance: 'high' },
  { id: 'mem-038', content: '项目代码仓库在 gitlab.company.com/aurora/main，分支策略采用 Git Flow', tags: ['Git', '仓库', 'Git Flow'], importance: 'medium' },
  { id: 'mem-039', content: '项目使用 PostgreSQL 作为主数据库，Redis 作为缓存，MongoDB 存日志', tags: ['数据库', 'PostgreSQL', 'Redis'], importance: 'medium' },
  { id: 'mem-040', content: '项目二期计划增加 AI 推荐功能，需要对接算法团队', tags: ['功能', 'AI', '推荐'], importance: 'high' },
  { id: 'mem-041', content: '项目风险点：第三方支付接口可能延期，需要准备备选方案', tags: ['风险', '支付', '延期'], importance: 'high' },
  { id: 'mem-042', content: '项目性能目标是 QPS 5000，P99 延迟小于 200ms', tags: ['性能', 'QPS', '目标'], importance: 'medium' },
  { id: 'mem-043', content: '项目技术栈：后端 Go + gRPC，前端 React + TypeScript，部署 K8s', tags: ['技术栈', 'Go', 'React'], importance: 'high' },

  // ========== 知识类 (Knowledge) - 4条 ==========
  { id: 'mem-044', content: 'Go 语言的 context 包用于控制请求的生命周期和超时，最佳实践是总是传递 context', tags: ['Go', '编程', '最佳实践'], importance: 'medium' },
  { id: 'mem-045', content: 'React 的 useCallback 和 useMemo 可以优化性能，但不要过度使用', tags: ['React', '性能', '优化'], importance: 'medium' },
  { id: 'mem-046', content: 'Docker 容器时区默认是 UTC，需要设置 TZ=Asia/Shanghai 来修正', tags: ['Docker', '时区', '配置'], importance: 'low' },
  { id: 'mem-047', content: 'Kubernetes 的 livenessProbe 和 readinessProbe 用途不同，前者判断是否重启，后者判断是否接收流量', tags: ['K8s', '健康检查', '探针'], importance: 'medium' },

  // ========== 习惯类 (Habit) - 2条 ==========
  { id: 'mem-048', content: '每天早上8点半到公司，先泡一杯咖啡再看邮件', tags: ['作息', '咖啡', '习惯'], importance: 'low' },
  { id: 'mem-049', content: '每天下班前整理当天的工作笔记，记录明天要做的事情', tags: ['笔记', '工作', '习惯'], importance: 'medium' },

  // ========== 目标类 (Goal) - 1条 ==========
  { id: 'mem-050', content: '今年目标是学习 Rust 语言，完成一个小型开源项目，争取成为 Contributor', tags: ['学习', 'Rust', '开源', '目标'], importance: 'high' },
];

const testQueries = [
  // ========== 简单查询 (Easy) - 7个 ==========
  { id: 'query-001', query: '用户喜欢吃什么？', expectedMemoryIds: ['mem-001'], expectedKeywords: ['川菜', '麻婆豆腐', '水煮鱼'], difficulty: 'easy' },
  { id: 'query-002', query: '项目什么时候截止？', expectedMemoryIds: ['mem-011'], expectedKeywords: ['4月1日', '截止'], difficulty: 'easy' },
  { id: 'query-003', query: '会议室在哪里？', expectedMemoryIds: ['mem-012', 'mem-021'], expectedKeywords: ['会议室', '3楼', '会议室A', '会议室B'], difficulty: 'easy' },
  { id: 'query-004', query: 'Jenkins 地址是什么？', expectedMemoryIds: ['mem-015'], expectedKeywords: ['jenkins.company.com'], difficulty: 'easy' },
  { id: 'query-005', query: '技术总监是谁？', expectedMemoryIds: ['mem-029'], expectedKeywords: ['张伟', '技术总监'], difficulty: 'easy' },
  { id: 'query-006', query: '项目用什么数据库？', expectedMemoryIds: ['mem-039'], expectedKeywords: ['PostgreSQL', 'Redis', 'MongoDB'], difficulty: 'easy' },
  { id: 'query-007', query: '女儿生日是哪天？', expectedMemoryIds: ['mem-024'], expectedKeywords: ['3月22日', '生日', '女儿'], difficulty: 'easy' },

  // ========== 中等查询 (Medium) - 8个 ==========
  { id: 'query-008', query: '最近有什么重要的截止日期需要注意？', expectedMemoryIds: ['mem-011', 'mem-019', 'mem-027'], expectedKeywords: ['4月1日', '3月25日', '3月30日', '截止'], difficulty: 'medium' },
  { id: 'query-009', query: '团队成员的联系方式有哪些？', expectedMemoryIds: ['mem-029', 'mem-032', 'mem-035'], expectedKeywords: ['zhang.wei@company.com', '138-xxxx-xxxx', '139-xxxx-xxxx'], difficulty: 'medium' },
  { id: 'query-010', query: '这个月有什么会议安排？', expectedMemoryIds: ['mem-012', 'mem-021', 'mem-023', 'mem-025'], expectedKeywords: ['周三', '周五', '周一', '会议'], difficulty: 'medium' },
  { id: 'query-011', query: '项目有什么风险需要注意？', expectedMemoryIds: ['mem-041'], expectedKeywords: ['风险', '支付', '延期', '备选方案'], difficulty: 'medium' },
  { id: 'query-012', query: '我之前说过的编程语言偏好是什么？', expectedMemoryIds: ['mem-005'], expectedKeywords: ['TypeScript', '类型安全', 'JavaScript'], difficulty: 'medium' },
  { id: 'query-013', query: '新人入职相关的事情有哪些？', expectedMemoryIds: ['mem-017', 'mem-034'], expectedKeywords: ['小陈', '前端组', '导师', '培训资料', 'onboarding'], difficulty: 'medium' },
  { id: 'query-014', query: '代码相关的工作流程是怎样的？', expectedMemoryIds: ['mem-013', 'mem-038'], expectedKeywords: ['代码审查', '24小时', 'Git Flow', '分支'], difficulty: 'medium' },
  { id: 'query-015', query: '健康和运动相关的安排有什么？', expectedMemoryIds: ['mem-006', 'mem-022', 'mem-026'], expectedKeywords: ['牙医', '3月15日', '健身', '爬山'], difficulty: 'medium' },

  // ========== 复杂查询 (Hard) - 5个 ==========
  { id: 'query-016', query: '如果明天是周三，我需要准备什么？', expectedMemoryIds: ['mem-021'], expectedKeywords: ['技术分享', '下午2点', '会议室B'], difficulty: 'hard' },
  { id: 'query-017', query: '下周有什么需要提前准备的事情？', expectedMemoryIds: ['mem-016', 'mem-022', 'mem-020'], expectedKeywords: ['3月14日', '技术债务', '3月15日', '牙医', '3月20日', '演示', 'PPT', 'Demo'], difficulty: 'hard' },
  { id: 'query-018', query: '我在技术方面想达成什么目标？', expectedMemoryIds: ['mem-050'], expectedKeywords: ['Rust', '开源', 'Contributor', '学习'], difficulty: 'hard' },
  { id: 'query-019', query: '项目的关键技术决策有哪些？', expectedMemoryIds: ['mem-038', 'mem-039', 'mem-043'], expectedKeywords: ['Go', 'gRPC', 'React', 'TypeScript', 'K8s', 'PostgreSQL', 'Redis', 'MongoDB', 'Git Flow'], difficulty: 'hard' },
  { id: 'query-020', query: '团队中如果遇到紧急问题应该联系谁？', expectedMemoryIds: ['mem-035'], expectedKeywords: ['运维', '老周', '139-xxxx-xxxx', '紧急'], difficulty: 'hard' },
];

// Results structure
interface QueryResult {
  query: string;
  hit: boolean;
  score: number;
  expectedMemoryId: string;
  actualMemoryId: string | null;
  difficulty: string;
  topResult: string;
}

interface TestResults {
  storageSuccess: number;
  storageFailed: number;
  queryResults: QueryResult[];
  summary: {
    totalQueries: number;
    hits: number;
    misses: number;
    hitRate: string;
    byDifficulty: {
      easy: { hits: number; total: number; rate: string };
      medium: { hits: number; total: number; rate: string };
      hard: { hits: number; total: number; rate: string };
    };
  };
  previousFailures: {
    programmingPreference: QueryResult | null;
    healthExercise: QueryResult | null;
    wednesdayPrep: QueryResult | null;
  };
}

async function runTest(): Promise<TestResults> {
  const workspaceDir = '/data/.subagent/.jarvis';
  const storagePath = path.join(workspaceDir, 'memory/palace');
  
  // Clean up existing memories for fresh test
  try {
    await fs.rm(storagePath, { recursive: true, force: true });
    console.log('Cleaned up existing memories');
  } catch {
    // Directory might not exist
  }
  
  // Create vector search provider
  const vectorSearch = new LocalVectorSearchProvider({
    host: '127.0.0.1',
    port: 8765,
    dbPath: '/data/agent-memory-palace/data/vectors-test.db',
    scriptPath: '/data/agent-memory-palace/scripts/vector-service.py',
  });
  
  // Create Memory Palace Manager with vector search
  const palace = new MemoryPalaceManager({
    workspaceDir,
    vectorSearch,
  });
  
  console.log('=== Memory Palace Final Test ===\n');
  
  // Step 1: Store all 50 test memories
  console.log('Step 1: Storing 50 test memories...');
  
  // Map original IDs to new IDs for tracking
  const idMap = new Map<string, string>();
  let storageSuccess = 0;
  let storageFailed = 0;
  
  for (const memory of testMemories) {
    try {
      const stored = await palace.store({
        content: memory.content,
        tags: memory.tags,
        importance: memory.importance === 'high' ? 0.9 : memory.importance === 'medium' ? 0.6 : 0.3,
        source: 'user',
        location: 'default',
      });
      
      idMap.set(memory.id, stored.id);
      storageSuccess++;
      
      if (storageSuccess % 10 === 0) {
        console.log(`  Progress: ${storageSuccess}/50 memories stored`);
      }
    } catch (e) {
      console.error(`  Failed to store ${memory.id}:`, e);
      storageFailed++;
    }
  }
  
  console.log(`\nStorage complete: ${storageSuccess} success, ${storageFailed} failed\n`);
  
  // Step 2: Run all 20 test queries
  console.log('Step 2: Running 20 test queries...');
  
  const queryResults: QueryResult[] = [];
  
  for (const testQuery of testQueries) {
    console.log(`\nQuery ${testQuery.id}: "${testQuery.query}"`);
    console.log(`  Expected: ${testQuery.expectedMemoryIds.join(', ')}`);
    
    try {
      const results = await palace.recall(testQuery.query, { topK: 5 });
      
      // Check if any expected memory is in the results
      let hit = false;
      let bestScore = 0;
      let actualMemoryId: string | null = null;
      let topResult = '';
      
      if (results.length > 0) {
        topResult = results[0].memory.content.substring(0, 60) + '...';
      }
      
      // First try exact ID match
      for (const result of results) {
        for (const expectedId of testQuery.expectedMemoryIds) {
          const newExpectedId = idMap.get(expectedId);
          if (newExpectedId && result.memory.id === newExpectedId) {
            hit = true;
            bestScore = Math.max(bestScore, result.score);
            actualMemoryId = result.memory.id;
            break;
          }
        }
        if (hit) break;
      }
      
      // If not found by ID, check content match using keywords
      if (!hit && results.length > 0) {
        for (const result of results) {
          const contentLower = result.memory.content.toLowerCase();
          for (const keyword of testQuery.expectedKeywords) {
            if (contentLower.includes(keyword.toLowerCase())) {
              // Partial match by keyword - consider it a hit if score is good
              if (result.score > 0.3) {
                hit = true;
                bestScore = result.score;
                actualMemoryId = result.memory.id;
                break;
              }
            }
          }
          if (hit) break;
        }
      }
      
      const queryResult: QueryResult = {
        query: testQuery.query,
        hit,
        score: bestScore,
        expectedMemoryId: testQuery.expectedMemoryIds[0],
        actualMemoryId,
        difficulty: testQuery.difficulty,
        topResult,
      };
      
      queryResults.push(queryResult);
      
      const status = hit ? '✅ HIT' : '❌ MISS';
      console.log(`  Result: ${status} (score: ${bestScore.toFixed(3)})`);
      if (results.length > 0) {
        console.log(`  Top result: "${topResult}"`);
      }
      
    } catch (e) {
      console.error(`  Query failed:`, e);
      queryResults.push({
        query: testQuery.query,
        hit: false,
        score: 0,
        expectedMemoryId: testQuery.expectedMemoryIds[0],
        actualMemoryId: null,
        difficulty: testQuery.difficulty,
        topResult: 'Error',
      });
    }
  }
  
  // Calculate statistics
  const hits = queryResults.filter(r => r.hit).length;
  const misses = queryResults.length - hits;
  const hitRate = ((hits / queryResults.length) * 100).toFixed(1);
  
  // By difficulty
  const easyResults = queryResults.filter(r => r.difficulty === 'easy');
  const mediumResults = queryResults.filter(r => r.difficulty === 'medium');
  const hardResults = queryResults.filter(r => r.difficulty === 'hard');
  
  const easyHits = easyResults.filter(r => r.hit).length;
  const mediumHits = mediumResults.filter(r => r.hit).length;
  const hardHits = hardResults.filter(r => r.hit).length;
  
  // Track previously failed queries
  const programmingPreference = queryResults.find(r => 
    r.query.includes('编程语言偏好')
  ) || null;
  
  const healthExercise = queryResults.find(r => 
    r.query.includes('健康和运动')
  ) || null;
  
  const wednesdayPrep = queryResults.find(r => 
    r.query.includes('明天是周三')
  ) || null;
  
  const results: TestResults = {
    storageSuccess,
    storageFailed,
    queryResults,
    summary: {
      totalQueries: queryResults.length,
      hits,
      misses,
      hitRate: `${hitRate}%`,
      byDifficulty: {
        easy: {
          hits: easyHits,
          total: easyResults.length,
          rate: `${((easyHits / easyResults.length) * 100).toFixed(1)}%`
        },
        medium: {
          hits: mediumHits,
          total: mediumResults.length,
          rate: `${((mediumHits / mediumResults.length) * 100).toFixed(1)}%`
        },
        hard: {
          hits: hardHits,
          total: hardResults.length,
          rate: `${((hardHits / hardResults.length) * 100).toFixed(1)}%`
        }
      }
    },
    previousFailures: {
      programmingPreference,
      healthExercise,
      wednesdayPrep,
    }
  };
  
  // Print summary
  console.log('\n=== TEST SUMMARY ===\n');
  console.log(`Storage: ${storageSuccess}/50 memories stored successfully`);
  console.log(`Queries: ${hits}/${queryResults.length} hits (${hitRate}%)`);
  console.log(`\nBy Difficulty:`);
  console.log(`  Easy:   ${easyHits}/${easyResults.length} (${results.summary.byDifficulty.easy.rate})`);
  console.log(`  Medium: ${mediumHits}/${mediumResults.length} (${results.summary.byDifficulty.medium.rate})`);
  console.log(`  Hard:   ${hardHits}/${hardResults.length} (${results.summary.byDifficulty.hard.rate})`);
  
  console.log('\n=== PREVIOUSLY FAILED QUERIES ===\n');
  if (programmingPreference) {
    console.log(`Programming Language Preference:`);
    console.log(`  Query: "${programmingPreference.query}"`);
    console.log(`  Result: ${programmingPreference.hit ? '✅ NOW HITS' : '❌ STILL MISSES'}`);
  }
  if (healthExercise) {
    console.log(`Health and Exercise:`);
    console.log(`  Query: "${healthExercise.query}"`);
    console.log(`  Result: ${healthExercise.hit ? '✅ NOW HITS' : '❌ STILL MISSES'}`);
  }
  if (wednesdayPrep) {
    console.log(`Wednesday Preparation:`);
    console.log(`  Query: "${wednesdayPrep.query}"`);
    console.log(`  Result: ${wednesdayPrep.hit ? '✅ NOW HITS' : '❌ STILL MISSES'}`);
  }
  
  return results;
}

// Run the test
runTest()
  .then(results => {
    console.log('\n=== JSON OUTPUT ===\n');
    console.log(JSON.stringify(results, null, 2));
  })
  .catch(err => {
    console.error('Test failed:', err);
    process.exit(1);
  });