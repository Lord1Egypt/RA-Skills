// Learning Path Navigator - Handler
// 主入口文件，处理用户请求并返回学习路径

import { runDecisionEngine } from './engine/router.js';

// 导出主函数供外部调用
export async function handleLearningRequest(request) {
  return await runDecisionEngine(request);
}

// CLI 测试入口
async function main() {
  const testRequest = {
    goal: {
      description: '掌握Python数据分析技能，能够独立完成数据清洗、分析和可视化项目',
      skills: ['Python', 'Pandas', 'NumPy', '数据可视化', '统计分析'],
      targetLevel: 'intermediate',
      timeframe: {
        totalWeeks: 12,
        hoursPerWeek: 10,
      },
    },
    constraints: {
      budget: 500,
      preferredFormats: ['course', 'video', 'exercise'],
      learningStyle: 'visual',
    },
  };

  console.log('🧭 学习路径导航仪 - 自测开始\n');
  console.log('输入请求:', JSON.stringify(testRequest, null, 2));
  console.log('\n---\n');

  const result = await handleLearningRequest(testRequest);

  if (result.success && result.learningPath) {
    const path = result.learningPath;
    console.log('✅ 学习路径生成成功!\n');
    console.log(`📚 ${path.title}`);
    console.log(`🎯 目标: ${path.goal.description}`);
    console.log(`📅 预计完成: ${path.progressTracking.estimatedCompletion}`);
    console.log(`\n📈 路径阶段 (共${path.phases.length}个阶段):`);
    
    path.phases.forEach(phase => {
      console.log(`\n  阶段${phase.phaseNumber}: ${phase.title}`);
      console.log(`    时长: ${phase.duration.weeks}周, ${phase.duration.totalHours}小时`);
      console.log(`    目标: ${phase.objectives.join('; ')}`);
      console.log(`    资源: ${phase.resources.length}个`);
    });

    console.log(`\n🏆 里程碑 (共${path.milestones.length}个):`);
    path.milestones.forEach(m => {
      console.log(`  - ${m.title} (${m.scheduledDate})`);
    });

    console.log(`\n💡 建议:`);
    result.recommendations?.forEach(r => console.log(`  • ${r}`));

    console.log(`\n📌 下一步:`);
    result.nextSteps?.forEach(s => console.log(`  → ${s}`));
  } else {
    console.log('❌ 生成失败:', result.error);
  }

  console.log('\n---\n自测完成');
  return result;
}

// 运行自测
main().catch(console.error);
