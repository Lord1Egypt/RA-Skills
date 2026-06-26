import { MemoryPalaceManager } from '../dist/src/index.js';

async function test() {
  const palace = new MemoryPalaceManager({ workspaceDir: '/tmp/test-palace-score-v2' });
  
  // 存储测试数据
  await palace.store({ content: "用户名字是盘古", tags: ["user"], importance: 0.9 });
  await palace.store({ content: "混沌团队成员：祝融、朱雀、烛明", tags: ["team"], importance: 0.8 });
  
  // 测试搜索
  const results = await palace.recall("用户是谁");
  console.log("搜索 '用户是谁' 的结果：");
  results.forEach(r => {
    console.log(`  内容: ${r.memory.content}`);
    console.log(`  分数: ${r.score.toFixed(4)}`);
    console.log(`  高亮: ${r.highlights}`);
    console.log("---");
  });
  
  // 测试另一个搜索
  const results2 = await palace.recall("团队");
  console.log("搜索 '团队' 的结果：");
  results2.forEach(r => {
    console.log(`  内容: ${r.memory.content}`);
    console.log(`  分数: ${r.score.toFixed(4)}`);
  });
}

test();
