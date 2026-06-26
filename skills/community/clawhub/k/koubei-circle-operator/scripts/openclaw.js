#!/usr/bin/env node

/**
 * OpenClaw CLI 工具
 * 简单封装 OpenClaw API，隐藏接口和 Key
 */

const https = require('https');
const fs = require('fs');
const path = require('path');
const readline = require('readline');
const { Buffer } = require('buffer');
const crypto = require('crypto');

const CONFIG_FILE = path.join(__dirname, 'config.json');

// 读取配置
function getConfig() {
  try {
    if (fs.existsSync(CONFIG_FILE)) {
      const config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
      // 确保有默认值
      if (!config.key) config.key = '';
      if (!config.host) config.host = '';
      return config;
    }
  } catch (e) {}
  return { key: '', host: '' };
}

// 保存配置
function saveConfig(config) {
  const savedConfig = {
    key: config.key || '',
    host: config.host || ''
  };
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(savedConfig, null, 2));
}

// API 请求
function request(method, pathname, data = null) {
  return new Promise((resolve, reject) => {
    const config = getConfig();
    if (!config.key) {
      reject(new Error('未配置 API Key，请先运行：node scripts/openclaw.js init --key <your_key>'));
      return;
    }
    
    if (!config.host) {
      reject(new Error('未配置 API 地址，请运行：node scripts/openclaw.js init --key <your_key>'));
      return;
    }
    const url = new URL(pathname, config.host);
    url.searchParams.set('key', config.key);
    
    const options = {
      hostname: url.hostname,
      path: url.pathname + url.search,
      method: method,
      headers: { 'Content-Type': 'application/json' }
    };
    
    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(body);
          result.code === 1 ? resolve(result.data) : reject(new Error(result.error));
        } catch (e) {
          reject(new Error('解析失败：' + body));
        }
      });
    });
    
    req.on('error', reject);
    if (data) req.write(JSON.stringify(data));
    req.end();
  });
}

// 获取表列表
async function getTables() {
  const tables = await request('GET', '/openclaw/table/show');
  console.log('开放表列表：');
  tables.forEach(t => {
    const tableName = t.table || t.table_name;
    const label = t.label || '';
    const fields = t.fields || t.columns || [];
    console.log(`\n表：${tableName}${label ? ' (' + label + ')' : ''}`);
    if (fields && fields.length > 0) {
      console.log('字段：' + fields.map(f => (f.field || f.name) + '[' + (f.label || '') + ']').join(', '));
    }
  });
}

// 执行查询
async function query(sql) {
  console.log('执行 SQL:', sql);
  const result = await request('POST', '/openclaw/query', { sql });
  console.log('结果：');
  console.log(JSON.stringify(result, null, 2));
}

// 获取帖子点赞列表
async function threadLikes(threadId, page = 1, pageSize = 20) {
  console.log(`获取帖子 ${threadId} 的点赞列表 (页 ${page}, 每页 ${pageSize} 条)`);
  const pathname = `/openclaw/thread/likes`;
  const config = getConfig();
  if (!config.key) {
    throw new Error('未配置 API Key，请先运行：node scripts/openclaw.js init --key <your_key>');
  }
  if (!config.host) {
    throw new Error('未配置 API 地址，请运行：node scripts/openclaw.js init --key <your_key>');
  }
  const url = new URL(pathname, config.host);
  url.searchParams.set('key', config.key);
  url.searchParams.set('thread_id', threadId);
  url.searchParams.set('page', page);
  url.searchParams.set('page_size', pageSize);
  
  const result = await request('GET', url.pathname + url.search);
  console.log('点赞列表：');
  console.log(JSON.stringify(result, null, 2));
}

// 普通发帖
async function publish(options) {
  console.log('发布普通帖子:', JSON.stringify(options, null, 2));
  const result = await request('POST', '/openclaw/thread/publish', options);
  console.log('发布成功！');
  console.log(JSON.stringify(result, null, 2));
}

// 热议话题发帖
async function publishHot(options) {
  console.log('发布热议话题帖子:', JSON.stringify(options, null, 2));
  const result = await request('POST', '/openclaw/thread/publish', options);
  console.log('发布成功！');
  console.log(JSON.stringify(result, null, 2));
}

// 上传图片（支持文件路径或 base64）
async function uploadImage(source) {
  const config = getConfig();
  if (!config.key) {
    throw new Error('未配置 API Key，请先运行：node scripts/openclaw.js init --key <your_key>');
  }
  
  let imageData;
  let filename = 'image.jpg';
  
  // 判断是 base64 还是文件路径
  if (source.startsWith('data:image')) {
    // base64 格式：data:image/jpeg;base64,xxxx
    const matches = source.match(/^data:image\/(\w+);base64,(.+)$/);
    if (!matches) {
      throw new Error('无效的 base64 图片格式');
    }
    const ext = matches[1];
    imageData = Buffer.from(matches[2], 'base64');
    filename = `image.${ext}`;
  } else if (fs.existsSync(source)) {
    // 文件路径
    imageData = fs.readFileSync(source);
    filename = path.basename(source);
  } else {
    throw new Error('文件不存在或不是有效的 base64');
  }
  
  console.log(`上传图片：${filename} (${(imageData.length / 1024).toFixed(2)} KB)`);
  
  return uploadFile('/openclaw/uploader/image', imageData, filename, 'image/jpeg');
}

// 上传视频（支持文件路径或 base64）
async function uploadVideo(source) {
  const config = getConfig();
  if (!config.key) {
    throw new Error('未配置 API Key，请先运行：node scripts/openclaw.js init --key <your_key>');
  }
  
  let videoData;
  let filename = 'video.mp4';
  
  // 判断是 base64 还是文件路径
  if (source.startsWith('data:video')) {
    // base64 格式：data:video/mp4;base64,xxxx
    const matches = source.match(/^data:video\/(\w+);base64,(.+)$/);
    if (!matches) {
      throw new Error('无效的 base64 视频格式');
    }
    const ext = matches[1];
    videoData = Buffer.from(matches[2], 'base64');
    filename = `video.${ext}`;
  } else if (fs.existsSync(source)) {
    // 文件路径
    videoData = fs.readFileSync(source);
    filename = path.basename(source);
  } else {
    throw new Error('文件不存在或不是有效的 base64');
  }
  
  console.log(`上传视频：${filename} (${(videoData.length / 1024 / 1024).toFixed(2)} MB)`);
  
  return uploadFile('/openclaw/uploader/video', videoData, filename, 'video/mp4');
}

// 上传文件（multipart/form-data）
function uploadFile(pathname, fileData, filename, mimeType) {
  return new Promise((resolve, reject) => {
    const config = getConfig();
    if (!config.key) {
      reject(new Error('未配置 API Key，请先运行：node scripts/openclaw.js init --key <your_key>'));
      return;
    }
    
    if (!config.host) {
      reject(new Error('未配置 API 地址，请运行：node scripts/openclaw.js init --key <your_key>'));
      return;
    }
    const url = new URL(pathname, config.host);
    url.searchParams.set('key', config.key);
    
    const boundary = 'OpenClawBoundary';
    const body = [];
    
    // 添加文件部分
    body.push(Buffer.from(`--${boundary}\r\n`));
    body.push(Buffer.from(`Content-Disposition: form-data; name="file"; filename="${filename}"\r\n`));
    body.push(Buffer.from(`Content-Type: ${mimeType}\r\n\r\n`));
    body.push(fileData);
    body.push(Buffer.from(`\r\n--${boundary}--\r\n`));
    
    const requestBody = Buffer.concat(body);
    
    const options = {
      hostname: url.hostname,
      path: url.pathname + url.search,
      method: 'POST',
      headers: {
        'Content-Type': `multipart/form-data; boundary=${boundary}`,
        'Content-Length': requestBody.length
      }
    };
    
    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(body);
          if (result.code === 1) {
            console.log('上传成功！');
            console.log(JSON.stringify(result.data, null, 2));
            resolve(result.data);
          } else {
            reject(new Error(result.error || result.msg || '上传失败'));
          }
        } catch (e) {
          reject(new Error('解析失败：' + body));
        }
      });
    });
    
    req.on('error', reject);
    req.write(requestBody);
    req.end();
  });
}

// 验证 Key（安装检查）
function validateKey(key) {
  return new Promise((resolve, reject) => {
    const config = getConfig();
    if (!config.host) {
      reject(new Error('未配置 API 地址，请编辑 scripts/config.json 设置 host 字段'));
      return;
    }
    const url = new URL('/openclaw/install/check', config.host);
    url.searchParams.set('key', key);
    
    const options = {
      hostname: url.hostname,
      path: url.pathname + url.search,
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    };
    
    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(body);
          if (result.code === 1) {
            resolve(result);
          } else {
            reject(new Error(result.msg || '无效的 key'));
          }
        } catch (e) {
          reject(new Error('解析失败：' + body));
        }
      });
    });
    
    req.on('error', reject);
    req.end();
  });
}

// 初始化配置
async function init(key) {
  if (!key || key.trim() === '') {
    console.error('错误：Key 不能为空');
    console.error('用法：node scripts/openclaw.js init --key <your_key>');
    console.error('示例：node scripts/openclaw.js init --key abcdefg123456');
    return;
  }
  
  console.log('正在验证 Key...');
  
  try {
    const result = await validateKey(key.trim());
    console.log('✅ ' + result.msg);
    console.log('');
    
    const config = getConfig();
    config.key = key.trim();
    
    saveConfig(config);
    console.log('配置已保存到：' + CONFIG_FILE);
    console.log('');
    console.log('========================================');
    console.log('  初始化完成！');
    console.log('========================================');
    console.log('');
    console.log('您现在可以使用口碑圈运营助手的所有功能。');
    console.log('运行 node scripts/openclaw.js 查看可用命令。');
  } catch (err) {
    console.error('❌ ' + err.message);
    console.error('请检查 Key 是否正确，或联系口碑圈客服获取帮助。');
  }
}

// 显示配置
function showConfig() {
  const config = getConfig();
  console.log('当前配置：');
  console.log('  API Key: ' + (config.key ? '****' : '未设置'));
  console.log('  API 地址：' + (config.host || '未设置'));
}

// 生成图床上传链接
function generateUploadLink() {
  const config = getConfig();
  if (!config.key) {
    console.error('未配置 API Key，请先运行：node scripts/openclaw.js init --key <your_key>');
    return;
  }
  
  const key = config.key;
  const timestamp = Date.now().toString();
  const rank = Math.floor(Math.random() * 90000) + 10000; // 10000-99999
  
  // 计算 MD5(key + timestamp + rank)
  const md5Hash = crypto.createHash('md5').update(key + timestamp + rank).digest('hex');
  
  if (!config.host) {
    console.error('未配置 API 地址，请运行：node scripts/openclaw.js init --key <your_key>');
    return;
  }
  const uploadUrl = `${config.host}/openclaw/resource/upload/page?upload_id=${md5Hash}`;
  
  console.log('图床上传链接：');
  console.log(uploadUrl);
  console.log('');
  console.log('请在浏览器中打开此链接上传图片/视频资源。');
  console.log('⚠️ 上传完成后，请回复 AI（发送消息告知已上传完成），AI 将帮您获取资源地址并继续发帖流程。');
  console.log('');
  console.log('upload_id: ' + md5Hash);
}

// 获取上传后的资源列表
async function getUploadResources(uploadId) {
  const config = getConfig();
  if (!config.key) {
    throw new Error('未配置 API Key，请先运行：node scripts/openclaw.js init --key <your_key>');
  }
  
  if (!config.host) {
    throw new Error('未配置 API 地址，请运行：node scripts/openclaw.js init --key <your_key>');
  }
  const pathname = `/openclaw/resource/upload/resource?upload_id=${uploadId}`;
  
  console.log(`获取上传资源列表 (upload_id: ${uploadId})`);
  const result = await request('GET', pathname);
  
  console.log('上传的资源：');
  if (Array.isArray(result)) {
    result.forEach((url, index) => {
      console.log(`  [${index + 1}] ${url}`);
    });
  } else {
    console.log(JSON.stringify(result, null, 2));
  }
  
  return result;
}

// 批量发送站内信
async function sendStationMail(userIds, message) {
  console.log('批量发送站内信:');
  console.log(`  接收用户数：${userIds.length}`);
  console.log(`  消息内容：${message}`);
  
  const data = {
    user_ids: userIds,
    message: message
  };
  
  const result = await request('POST', '/openclaw/station-mail/send', data);
  console.log('✅ 发送成功！');
  return result;
}

// 获取标签列表
async function getLabelList() {
  const result = await request('GET', '/openclaw/label/list');
  console.log('标签列表：');
  result.forEach(label => {
    console.log(`  [${label.id}] ${label.label_name} (${label.label_type_name}) 颜色: ${label.color}`);
  });
  return result;
}

// 获取用户标签
async function getUserLabels(userId) {
  const result = await request('GET', `/openclaw/user/label/list?user_id=${userId}`);
  console.log(`用户 ID ${userId} 的标签：`);
  if (result.length === 0) {
    console.log('  无标签');
  } else {
    result.forEach(label => {
      console.log(`  [${label.id}] ${label.label_name} (${label.label_type_name})`);
    });
  }
  return result;
}

// 获取标签下的用户
async function getLabelUsers(labelId, page = 1, pageSize = 20) {
  const result = await request('GET', `/openclaw/label/user/list?label_id=${labelId}&page=${page}&page_size=${pageSize}`);
  console.log(`标签 ID ${labelId} 的用户列表（第 ${page} 页，每页 ${pageSize} 条）：`);
  console.log(`  总计: ${result.total} 人`);
  result.data.forEach(user => {
    console.log(`  [${user.user_id}] ${user.nickname} (打标时间: ${user.labeled_at})`);
  });
  return result;
}

// 给用户打标签
async function setUserLabel(userId, labelId, labelName) {
  const data = { user_id: userId };
  if (labelId) {
    data.label_id = labelId;
  }
  if (labelName) {
    data.label_name = labelName;
  }
  
  const result = await request('POST', '/openclaw/user/label/set', data);
  if (result.attached) {
    console.log(`✅ 已为用户 ID ${userId} 打上标签「${result.label.label_name}」（${result.label.label_type_name}）`);
  } else {
    console.log('标签设置完成');
  }
  return result;
}

// 编辑帖子标题和内容
async function updateThread(threadId, title, message) {
  const data = { thread_id: threadId };
  if (title !== undefined && title !== null) data.title = title;
  if (message !== undefined && message !== null) data.message = message;
  
  const result = await request('POST', '/openclaw/thread/update', data);
  console.log(`✅ 帖子 ID ${result.thread_id} 已更新`);
  return result;
}

// 批量增加积分
async function increaseIntegral(userIds, integral, reason) {
  const data = {
    user_ids: userIds,
    integral: integral,
    reason: reason || ''
  };
  
  const result = await request('POST', '/openclaw/user/integral/increase', data);
  console.log(`✅ 积分发放完成：总计 ${result.total} 人，成功 ${result.success} 人，失败 ${result.failed} 人`);
  if (result.results && result.results.length > 0) {
    result.results.forEach(r => {
      if (r.status !== 'success') {
        console.log(`  用户 ID ${r.user_id}: 失败 (${r.message})`);
      }
    });
  }
  return result;
}

// 新增马甲
async function addMarks(nicknames) {
  const data = { nickname: nicknames };
  const result = await request('POST', '/openclaw/mark/save', data);
  console.log('✅ 马甲新增完成');
  return result;
}

// 编辑马甲昵称
async function editMark(userId, nickname) {
  const data = {
    user_id: userId,
    nickname: nickname
  };
  
  const result = await request('POST', '/openclaw/mark/save', data);
  console.log(`✅ 马甲 ID ${result.user_id} 已更新为「${nickname}」`);
  return result;
}

// 主程序
const cmd = process.argv[2];

if (cmd === 'init') {
  // 解析 --key 参数
  let key = null;
  for (let i = 3; i < process.argv.length; i++) {
    if (process.argv[i] === '--key' && process.argv[i + 1]) {
      key = process.argv[i + 1];
      break;
    }
  }
  init(key);
} else if (cmd === 'config') {
  showConfig();
} else if (cmd === 'tables') {
  getTables().catch(e => console.error('错误:', e.message));
} else if (cmd === 'query') {
  const sql = process.argv.slice(3).join(' ');
  if (!sql) {
    console.error('请提供 SQL 语句');
    process.exit(1);
  }
  query(sql).catch(e => console.error('错误:', e.message));
} else if (cmd === 'thread-likes') {
  const threadId = process.argv[3];
  const page = process.argv[4] || 1;
  const pageSize = process.argv[5] || 20;
  if (!threadId) {
    console.error('请提供帖子 ID');
    console.error('用法：node scripts/openclaw.js thread-likes <thread_id> [page] [page_size]');
    process.exit(1);
  }
  threadLikes(threadId, page, pageSize).catch(e => console.error('错误:', e.message));
} else if (cmd === 'publish') {
  const data = process.argv[3];
  if (!data) {
    console.error('请提供 JSON 数据');
    console.error('用法：node scripts/openclaw.js publish \'{"user_id":12,"type":1,"topic_id":3,"title":"标题","message":"内容"}\'');
    process.exit(1);
  }
  try {
    const options = JSON.parse(data);
    publish(options).catch(e => console.error('错误:', e.message));
  } catch (e) {
    console.error('JSON 解析失败:', e.message);
    process.exit(1);
  }
} else if (cmd === 'publish-hot') {
  const data = process.argv[3];
  if (!data) {
    console.error('请提供 JSON 数据');
    console.error('用法：node scripts/openclaw.js publish-hot \'{"user_id":12,"type":1,"hot_say_id":8,"title":"标题","message":"内容"}\'');
    process.exit(1);
  }
  try {
    const options = JSON.parse(data);
    if (!options.hot_say_id) {
      console.error('热议话题发帖必须提供 hot_say_id');
      process.exit(1);
    }
    publishHot(options).catch(e => console.error('错误:', e.message));
  } catch (e) {
    console.error('JSON 解析失败:', e.message);
    process.exit(1);
  }
} else if (cmd === 'upload-image') {
  const source = process.argv[3];
  if (!source) {
    console.error('请提供图片文件路径或 base64 数据');
    console.error('用法：node scripts/openclaw.js upload-image <file_path|base64>');
    console.error('示例：node scripts/openclaw.js upload-image ./image.jpg');
    console.error('示例：node scripts/openclaw.js upload-image "data:image/jpeg;base64,/9j/4AAQSkZJRg..."');
    process.exit(1);
  }
  uploadImage(source).catch(e => console.error('错误:', e.message));
} else if (cmd === 'upload-video') {
  const source = process.argv[3];
  if (!source) {
    console.error('请提供视频文件路径或 base64 数据');
    console.error('用法：node scripts/openclaw.js upload-video <file_path|base64>');
    console.error('示例：node scripts/openclaw.js upload-video ./video.mp4');
    console.error('示例：node scripts/openclaw.js upload-video "data:video/mp4;base64,AAAAFGZ0eXA..."');
    process.exit(1);
  }
  uploadVideo(source).catch(e => console.error('错误:', e.message));
} else if (cmd === 'upload-page') {
  generateUploadLink();
} else if (cmd === 'upload-resource') {
  const uploadId = process.argv[3];
  if (!uploadId) {
    console.error('请提供 upload_id');
    console.error('用法：node scripts/openclaw.js upload-resource <upload_id>');
    console.error('示例：node scripts/openclaw.js upload-resource abc123def456');
    process.exit(1);
  }
  getUploadResources(uploadId).catch(e => console.error('错误:', e.message));
} else if (cmd === 'station-mail') {
  // 解析参数：--users=[1,2,3] --message="xxx"
  let users = null;
  let message = null;
  
  for (let i = 3; i < process.argv.length; i++) {
    if (process.argv[i].startsWith('--users=')) {
      try {
        users = JSON.parse(process.argv[i].substring(8));
      } catch (e) {
        console.error('无效的 users 格式，必须是 JSON 数组');
        process.exit(1);
      }
    } else if (process.argv[i].startsWith('--message=')) {
      message = process.argv[i].substring(10);
    }
  }
  
  if (!users || !Array.isArray(users) || users.length === 0) {
    console.error('请提供用户 ID 数组');
    console.error('用法：node scripts/openclaw.js station-mail --users=[12,34,56] --message="消息内容"');
    process.exit(1);
  }
  
  if (!message) {
    console.error('请提供消息内容');
    console.error('用法：node scripts/openclaw.js station-mail --users=[12,34,56] --message="消息内容"');
    process.exit(1);
  }
  
  sendStationMail(users, message).catch(e => console.error('错误:', e.message));
} else if (cmd === 'label-list') {
  getLabelList().catch(e => console.error('错误:', e.message));
} else if (cmd === 'user-labels') {
  const userId = process.argv[3];
  if (!userId) {
    console.error('请提供用户 ID');
    console.error('用法：node scripts/openclaw.js user-labels <user_id>');
    process.exit(1);
  }
  getUserLabels(userId).catch(e => console.error('错误:', e.message));
} else if (cmd === 'label-users') {
  const labelId = process.argv[3];
  const page = process.argv[4] || 1;
  const pageSize = process.argv[5] || 20;
  if (!labelId) {
    console.error('请提供标签 ID');
    console.error('用法：node scripts/openclaw.js label-users <label_id> [page] [page_size]');
    process.exit(1);
  }
  getLabelUsers(labelId, page, pageSize).catch(e => console.error('错误:', e.message));
} else if (cmd === 'set-label') {
  // 解析参数：--user=<id> --label-id=<id> 或 --label-name=<name>
  let userId = null;
  let labelId = null;
  let labelName = null;
  
  for (let i = 3; i < process.argv.length; i++) {
    if (process.argv[i].startsWith('--user=')) {
      userId = process.argv[i].substring(7);
    } else if (process.argv[i].startsWith('--label-id=')) {
      labelId = process.argv[i].substring(11);
    } else if (process.argv[i].startsWith('--label-name=')) {
      labelName = process.argv[i].substring(13);
    }
  }
  
  if (!userId) {
    console.error('请提供用户 ID');
    console.error('用法：node scripts/openclaw.js set-label --user=<user_id> --label-id=<label_id>');
    console.error('或：  node scripts/openclaw.js set-label --user=<user_id> --label-name=<label_name>');
    process.exit(1);
  }
  if (!labelId && !labelName) {
    console.error('请提供标签 ID 或标签名称');
    console.error('用法：node scripts/openclaw.js set-label --user=<user_id> --label-id=<label_id>');
    console.error('或：  node scripts/openclaw.js set-label --user=<user_id> --label-name=<label_name>');
    process.exit(1);
  }
  
  setUserLabel(userId, labelId, labelName).catch(e => console.error('错误:', e.message));
} else if (cmd === 'update-thread') {
  // 解析参数：--thread-id=<id> --title=<str> --message=<str>
  let threadId = null;
  let title = null;
  let message = null;
  
  for (let i = 3; i < process.argv.length; i++) {
    if (process.argv[i].startsWith('--thread-id=')) {
      threadId = process.argv[i].substring(12);
    } else if (process.argv[i].startsWith('--title=')) {
      title = process.argv[i].substring(8);
    } else if (process.argv[i].startsWith('--message=')) {
      message = process.argv[i].substring(10);
    }
  }
  
  if (!threadId) {
    console.error('请提供帖子 ID');
    console.error('用法：node scripts/openclaw.js update-thread --thread-id=<id> [--title=<str>] [--message=<str>]');
    process.exit(1);
  }
  if (title === null && message === null) {
    console.error('请至少提供 --title 或 --message 之一');
    console.error('用法：node scripts/openclaw.js update-thread --thread-id=<id> [--title=<str>] [--message=<str>]');
    process.exit(1);
  }
  
  updateThread(threadId, title, message).catch(e => console.error('错误:', e.message));
} else if (cmd === 'add-integral') {
  // 解析参数：--users=[1,2,3] --integral=5 --reason="xxx"
  let users = null;
  let integral = null;
  let reason = null;
  
  for (let i = 3; i < process.argv.length; i++) {
    if (process.argv[i].startsWith('--users=')) {
      try {
        users = JSON.parse(process.argv[i].substring(8));
      } catch (e) {
        console.error('无效的 users 格式，必须是 JSON 数组');
        process.exit(1);
      }
    } else if (process.argv[i].startsWith('--integral=')) {
      integral = parseInt(process.argv[i].substring(11), 10);
    } else if (process.argv[i].startsWith('--reason=')) {
      reason = process.argv[i].substring(9);
    }
  }
  
  if (!users || !Array.isArray(users) || users.length === 0) {
    console.error('请提供用户 ID 数组');
    console.error('用法：node scripts/openclaw.js add-integral --users=[12,13] --integral=5 --reason="活动奖励"');
    process.exit(1);
  }
  if (integral === null || isNaN(integral)) {
    console.error('请提供积分数量');
    console.error('用法：node scripts/openclaw.js add-integral --users=[12,13] --integral=5 --reason="活动奖励"');
    process.exit(1);
  }
  
  increaseIntegral(users, integral, reason).catch(e => console.error('错误:', e.message));
} else if (cmd === 'add-mark') {
  // 解析参数：--names=["马甲A","马甲B"]
  let names = null;
  
  for (let i = 3; i < process.argv.length; i++) {
    if (process.argv[i].startsWith('--names=')) {
      try {
        names = JSON.parse(process.argv[i].substring(8));
      } catch (e) {
        console.error('无效的 names 格式，必须是 JSON 数组');
        process.exit(1);
      }
    }
  }
  
  if (!names || !Array.isArray(names) || names.length === 0) {
    console.error('请提供马甲昵称数组');
    console.error('用法：node scripts/openclaw.js add-mark --names=["马甲A","马甲B"]');
    process.exit(1);
  }
  
  addMarks(names).catch(e => console.error('错误:', e.message));
} else if (cmd === 'edit-mark') {
  // 解析参数：--user=<id> --nickname=<str>
  let userId = null;
  let nickname = null;
  
  for (let i = 3; i < process.argv.length; i++) {
    if (process.argv[i].startsWith('--user=')) {
      userId = process.argv[i].substring(7);
    } else if (process.argv[i].startsWith('--nickname=')) {
      nickname = process.argv[i].substring(11);
    }
  }
  
  if (!userId || !nickname) {
    console.error('请提供用户 ID 和新昵称');
    console.error('用法：node scripts/openclaw.js edit-mark --user=<user_id> --nickname=<新昵称>');
    process.exit(1);
  }
  
  editMark(userId, nickname).catch(e => console.error('错误:', e.message));
} else {
  console.log('OpenClaw CLI 工具 (v1.4.0)');
  console.log('');
  console.log('用法：node scripts/openclaw.js <命令> [参数]');
  console.log('');
  console.log('命令:');
  console.log('  init --key <key>              初始化配置');
  console.log('  config                        查看当前配置');
  console.log('  tables                        获取开放表列表');
  console.log('  query <sql>                   执行 SQL 查询');
  console.log('  thread-likes <id> [p] [n]     获取帖子点赞列表');
  console.log('  publish <json>                普通发帖');
  console.log('  publish-hot <json>            热议话题发帖');
  console.log('  update-thread                 编辑帖子标题和内容');
  console.log('  station-mail                  批量发送站内信');
  console.log('  add-integral                  批量增加积分');
  console.log('  label-list                    获取标签列表');
  console.log('  user-labels <user_id>         查看用户标签');
  console.log('  label-users <id> [p] [n]      查看标签下的用户');
  console.log('  set-label                     给用户打标签');
  console.log('  add-mark                      新增马甲');
  console.log('  edit-mark                     编辑马甲昵称');
  console.log('  upload-page                   生成图床上传链接');
  console.log('  upload-resource <id>          获取已上传的资源列表');
  console.log('');
  console.log('示例:');
  console.log('  node scripts/openclaw.js label-list');
  console.log('  node scripts/openclaw.js update-thread --thread-id=1002 --title="新标题" --message="新内容"');
  console.log('  node scripts/openclaw.js add-integral --users=[12,13] --integral=5 --reason="活动奖励"');
  console.log('  node scripts/openclaw.js add-mark --names=["马甲A","马甲B"]');
  console.log('  node scripts/openclaw.js edit-mark --user=15 --nickname="新昵称"');
  console.log('  node scripts/openclaw.js station-mail --users=[12,34,56] --message="社区通知"');
  console.log('  node scripts/openclaw.js upload-image ./image.jpg');
}
