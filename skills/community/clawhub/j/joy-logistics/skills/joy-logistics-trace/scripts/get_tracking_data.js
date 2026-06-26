const https = require('https');

// 从环境变量获取 token
const token = process.env.token;

if (!token) {
  console.error('❌ 未从环境变量中读取到 token，请配置token');
  process.exit(1);
}

// 接收入参：只需要 1 个参数，多个单号用英文逗号分隔
const args = process.argv.slice(2);
const [referenceNumbersStr] = args;

// 检查入参
if (!referenceNumbersStr || referenceNumbersStr.trim() === '') {
  console.error('❌ 请传入单号，多个单号用英文逗号分隔，例如：node query.js "JD123,JD456"');
  process.exit(1);
}

// 切割成数组，并自动去空、去重
const referenceNumbers = referenceNumbersStr
  .split(',')
  .map(item => item.trim())
  .filter(Boolean);

if (referenceNumbers.length === 0) {
  console.error('❌ 未传入有效单号');
  process.exit(1);
}

// 构建 referenceList
const referenceList = referenceNumbers.map(num => ({
  customerCode: "",
  referenceNumber: num,
  referenceType: 0
}));

// ===========================
// 构造请求体（完全匹配 curl）
// ===========================
const postData = JSON.stringify([
  {
    "includeFields": ["waybill"],
    "locale": "zh-CN",
    "referenceList": referenceList,  // 自动填入 1个/多个单号
    "scope": 4,
    "timeZone": "UTC+08:00"
  }
]);

// ===========================
// 请求配置
// ===========================
const options = {
  hostname: 'lop-proxy.ochama.com',
  port: 443,
  path: '/global/trackingOpenExport/queryTrackingBatch',
  method: 'POST',
  headers: {
    'LOP-DN': 'ifop.skill.eu.outer.jd.com',
    'Content-Type': 'application/json',
    'token': token,
    'Content-Length': Buffer.byteLength(postData)
  },
  rejectUnauthorized: false
};

console.log('✅ 准备查询单号：', referenceNumbers);
console.log('✅ 请求体：\n', postData);

// ===========================
// 发送请求
// ===========================
const req = https.request(options, (res) => {
  let chunks = [];
  res.on('data', d => chunks.push(d));
  res.on('end', () => {
    const result = Buffer.concat(chunks).toString('utf8');
    console.log('\n========================================');
    console.log('✅ 返回结果：');
    try {
      console.log(JSON.stringify(JSON.parse(result), null, 2));
    } catch (e) {
      console.log(result);
    }
  });
});

req.on('error', (e) => {
  console.error('❌ 请求失败：', e);
});

req.write(postData);
req.end();