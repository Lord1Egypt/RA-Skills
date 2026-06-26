const { apiGet } = require('./request');
const { CONFIG } = require('./config');

async function getAllRecords() {
  let records = [];
  let pageToken = '';
  do {
    const params = pageToken ? '?page_token=' + pageToken + '&page_size=100' : '?page_size=100';
    const r = await apiGet('/bitable/v1/apps/' + CONFIG.APP_TOKEN + '/tables/' + CONFIG.TABLE_ID + '/records' + params);
    const data = r.data?.items || r.data?.records || [];
    records = records.concat(data);
    pageToken = r.data?.page_token || '';
  } while (pageToken);
  return records;
}

getAllRecords().then(records => {
  console.log('总记录数:', records.length);
  console.log('\n=== 各字段填充情况 ===');
  
  const fields = ['任务名称', '来源分类', '优先级', '状态', '截止日期', '开始时间', '干系人', '工作要求', '工作链接', '备注', '预计时长'];
  
  fields.forEach(f => {
    const count = records.filter(r => r.fields && r.fields[f] !== undefined && r.fields[f] !== '' && r.fields[f] !== null).length;
    const pct = records.length > 0 ? Math.round(count / records.length * 100) : 0;
    console.log('  ' + f + ': ' + count + '/' + records.length + ' (' + pct + '%)');
  });
  
  console.log('\n=== 缺失可选字段的记录 ===');
  const optionalFields = ['干系人', '工作要求', '工作链接', '备注', '预计时长'];
  let missingCount = 0;
  records.forEach(r => {
    if (!r.fields) return;
    const missing = [];
    optionalFields.forEach(f => {
      const val = r.fields[f];
      if (val === undefined || val === '' || val === null) missing.push(f);
    });
    if (missing.length > 0) {
      missingCount++;
      console.log('[' + r.record_id + '] ' + r.fields['任务名称'] + ': 缺失 ' + missing.join(', '));
    }
  });
  console.log('\n共 ' + missingCount + ' 条记录存在可选字段缺失');
}).catch(console.error);