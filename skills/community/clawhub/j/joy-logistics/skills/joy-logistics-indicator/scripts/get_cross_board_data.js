/*
 * @Author: wangyu516 wangyu516@jd.com
 * @Date: 2026-04-17 01:06:29
 * @LastEditors: wangyu516 wangyu516@jd.com
 * @LastEditTime: 2026-04-23 17:19:23
 * @FilePath: /joy-logistics/scripts/get_cross_board_data.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
const https = require('https');
const fs = require('fs');
const path = require('path');

// 自动从 ~/.env 读取 joy_token
// let token = '';
// try {
//   const envPath = path.join(process.env.HOME, '.env');
//   const envContent = fs.readFileSync(envPath, 'utf8');
//   const match = envContent.match(/^joy_token=(.+)$/m);
//   if (match) token = match[1].trim();
// } catch (err) {}

// 从环境变量获取 token
const token = process.env.token;

if (!token) {
  console.error('❌ 未从环境变量中读取到 token，请配置token');
  process.exit(1);
}

// ===========================
// 入参：2 个  dateList, dims
// ===========================
const args = process.argv.slice(2);
console.log("length:" + args.length);

// ===========================
// 数组转换函数（和原版完全一样）
// ===========================
function toArray(val) {
  if (!val) return [];
  let str = val.trim();
  if (str === '' || str === '.' || str.startsWith('\\') || str.startsWith('"')) return [];
  return str.split(',').map(i => i.trim()).filter(Boolean);
}

const [dateList, dims] = args;

const postData = JSON.stringify([
  {
    dateList: toArray(dateList),
    dims: toArray(dims)
  }
]);

const options = {
  hostname: 'us-api.jd.com',
  port: 443,
  path: '/uis/getCrossBoardByCondition4Customer',
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