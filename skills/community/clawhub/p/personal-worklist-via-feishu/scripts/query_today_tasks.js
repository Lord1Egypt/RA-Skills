/**
 * 查询截止日期为今天且状态<>已完成的任务
 */
const { apiGet } = require('./request');
const { CONFIG } = require('./config');

async function main() {
  const result = await apiGet(`/bitable/v1/apps/${CONFIG.APP_TOKEN}/tables/${CONFIG.TABLE_ID}/records?page_size=100`);
  
  if (result.code === 0) {
    const items = result.data?.items || [];
    console.log('Total records:', items.length);
    
    // Filter for today's date and status != 已完成
    // 动态获取今天日期（上海时区）
    // 飞书日期字段存储为毫秒时间戳（如上海 2026-05-14 00:00:00 存为 XXXXXXXXX000 = UTC 2026-05-13T16:00:00Z）
    // 注意：历史数据曾错误存储为秒（XXXXXXXXX），需自动识别：值>1e10则为秒，需转毫秒
    const now = new Date();
    const shanghaiTime = new Date(now.getTime() + 8 * 3600000);
    const today = shanghaiTime.toISOString().split('T')[0]; // 上海时区的今天（如 2026-05-14）
    const todayTasks = items.filter(item => {
      const deadline = item.fields['截止日期'];
      const status = item.fields['状态'];
      if (!deadline) return false;
      // 兼容历史错误（秒）和正确数据（毫秒）：>1e10 则为秒转毫秒
      const deadlineMs = deadline > 1e10 ? deadline : deadline * 1000;
      const deadlineStr = new Date(deadlineMs + 8 * 3600000).toISOString().split('T')[0];
      return deadlineStr === today && status !== '已完成';
    });
    
    console.log('Today deadline, not completed:', todayTasks.length);
    todayTasks.forEach((item, i) => {
      console.log(`\n--- Task ${i+1} ---`);
      console.log('ID:', item.record_id);
      console.log('Name:', item.fields['任务名称']);
      console.log('Status:', item.fields['状态']);
      console.log('Priority:', item.fields['优先级']);
      console.log('Deadline:', item.fields['截止日期']);
      console.log('Issues:', item.fields['存在问题']);
      console.log('Notes:', item.fields['备注']);
    });
    
    // Also get completed tasks for today
    const completedToday = items.filter(item => {
      const deadline = item.fields['截止日期'];
      const status = item.fields['状态'];
      if (!deadline) return false;
      const deadlineMs = deadline > 1e10 ? deadline : deadline * 1000;
      const deadlineStr = new Date(deadlineMs + 8 * 3600000).toISOString().split('T')[0];
      return deadlineStr === today && status === '已完成';
    });
    console.log('\n=== Completed Today ===');
    console.log('Completed today:', completedToday.length);
    
  } else {
    console.log('Error:', result.msg);
  }
}

main().catch(console.error);
