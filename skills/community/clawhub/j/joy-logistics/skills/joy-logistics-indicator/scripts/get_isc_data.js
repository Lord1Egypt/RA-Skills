const https = require('https');
const token = process.env.token;

if (!token) {
  console.error('❌ 未从环境变量中读取到 token，请配置token');
  process.exit(1);
}

const args = process.argv.slice(2);
console.log("length:" + args.length);

// ===========================
// 🔥 WINDOWS 终极兼容函数
// 空 / . / \ / \" 全都变 []
// ===========================
function toArray(val) {
  if (!val) return [];
  let str = val.trim();
  if (str === '' || str === '.' || str.startsWith('\\') || str.startsWith('"')) return [];
  return str.split(',').map(i => i.trim()).filter(Boolean);
}

const [
  dims,
  monthList,
  indicatorCode,
  dateList,
  warehouseNoList,
  warehouseNameList,
  continentList,
  customerCodeList
] = args;

const postData = JSON.stringify([
  {
    dims: toArray(dims),
    monthList: toArray(monthList),
    indicatorCode,
    dateList: toArray(dateList),
    warehouseNoList: toArray(warehouseNoList),
    warehouseNameList: toArray(warehouseNameList),
    continentList: toArray(continentList),
    customerCodeList: toArray(customerCodeList)
  }
]);

const options = {
  hostname: 'us-api.jd.com',
  port: 443,
  path: '/uis/getUisIscDataByCondition4Customer',
  method: 'POST',
  headers: {
    'LOP-DN': 'iplat.skill.http.outer.jd.com',
    'Content-Type': 'application/json',
    'token': token,
    'Content-Length': Buffer.byteLength(postData)
  },
  rejectUnauthorized: false
};

console.log('✅ 发送请求体：\n', postData);

const req = https.request(options, (res) => {
  let chunks = [];
  res.on('data', d => chunks.push(d));
  res.on('end', () => {
    const result = Buffer.concat(chunks).toString('utf8');
    console.log('\n========================================');
    console.log('✅ 返回结果：');
    try { console.log(JSON.stringify(JSON.parse(result), null, 2)); } catch { console.log(result); }
  });
});

req.on('error', e => console.error('❌ 请求失败：', e));
req.write(postData);
req.end();