#!/usr/bin/env node
/**
 * IMA 笔记检索与内容纲要生成
 * 功能：搜索包含关键词的笔记，获取内容并生成纲要
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// 读取凭证
let CLIENT_ID = process.env.IMA_OPENAPI_CLIENTID;
let API_KEY = process.env.IMA_OPENAPI_APIKEY;

// 尝试从配置文件读取
const configDir = path.join(process.env.USERPROFILE || process.env.HOME, '.config', 'ima');
if (!CLIENT_ID) {
  try { CLIENT_ID = fs.readFileSync(path.join(configDir, 'client_id'), 'utf8').trim(); } catch (e) {}
}
if (!API_KEY) {
  try { API_KEY = fs.readFileSync(path.join(configDir, 'api_key'), 'utf8').trim(); } catch (e) {}
}

// 从 ima 技能配置读取
if (!CLIENT_ID) {
  try { 
    const skillEnv = path.join(process.env.USERPROFILE, '.workbuddy', 'skills', 'ima笔记', 'notes', '.env');
    const envContent = fs.readFileSync(skillEnv, 'utf8');
    const match = envContent.match(/IMA_CLIENT_ID\s*=\s*(.+)/);
    if (match) CLIENT_ID = match[1].trim();
  } catch (e) {}
}

if (!CLIENT_ID) {
  console.error('Error: 缺少 IMA Client ID');
  process.exit(1);
}

// API 请求函数
function apiRequest(apiPath, postData) {
  return new Promise((resolve, reject) => {
    const dataStr = JSON.stringify(postData);
    const options = {
      hostname: 'ima.qq.com',
      path: '/' + apiPath,
      method: 'POST',
      headers: {
        'ima-openapi-clientid': CLIENT_ID,
        'ima-openapi-apikey': API_KEY || '',
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(dataStr)
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.write(dataStr);
    req.end();
  });
}

// 搜索笔记
async function searchNotes(query, pageSize = 20) {
  const result = await apiRequest('openapi/note/v1/search_note_book', {
    search_type: 0,
    query_info: { title: query },
    start: 0,
    end: pageSize
  });
  
  if (result.code === 0 && result.data && result.data.docs) {
    const docs = result.data.docs || [];
    return docs.map(d => ({
      doc_id: d.doc.basic_info.doc_id,
      title: d.doc.basic_info.title,
      create_time: d.doc.basic_info.create_time,
      folder_id: d.doc.basic_info.folder_id
    }));
  }
  console.error('搜索失败:', result);
  return [];
}

// 获取笔记内容
async function getNoteContent(docId) {
  const result = await apiRequest('openapi/note/v1/get_doc_content', {
    doc_id: docId,
    target_content_format: 0  // 纯文本
  });
  
  if (result.code === 0 && result.data) {
    return result.data;
  }
  console.error('获取内容失败:', result);
  return null;
}

// 生成内容纲要
function generateOutline(text, maxSections = 10) {
  if (!text) return { outline: [], preview: '' };
  
  // 清理文本
  const cleanText = text.replace(/\r\n/g, '\n').trim();
  
  // 取前2000字符作为预览
  const previewText = cleanText.substring(0, 1000) + (cleanText.length > 1000 ? '...' : '');
  
  // 简单纲要提取：按段落和标题
  const lines = cleanText.split('\n').filter(l => l.trim());
  const outline = [];
  
  for (const line of lines) {
    const trimmed = line.trim();
    // 检测标题特征：短行、以特定字符开头、包含关键词
    if (trimmed.length < 60 && (
        /^[一二三四五六七八九十\d]/.test(trimmed) ||
        /^第[一二三四五六七八九十\d]/.test(trimmed) ||
        /^【/.test(trimmed) ||
        /：|：/.test(trimmed) ||
        /^[*\-]/.test(trimmed)
    )) {
      outline.push(trimmed);
    }
  }
  
  // 去重并限制数量
  const uniqueOutline = [...new Set(outline)].slice(0, maxSections);
  
  return {
    outline: uniqueOutline,
    preview: previewText
  };
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  let query = '商事调解';
  let mode = 'search'; // search, outline, all
  
  // 解析参数
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--query' || args[i] === '-q') {
      query = args[i + 1];
      i++;
    } else if (args[i] === '--outline' || args[i] === '-o') {
      mode = 'outline';
    } else if (args[i] === '--all') {
      mode = 'all';
    } else if (!args[i].startsWith('--')) {
      query = args[i];
    }
  }
  
  console.log(`🔍 搜索关键词: ${query}`);
  console.log('---');
  
  // 搜索笔记
  const notes = await searchNotes(query);
  
  if (notes.length === 0) {
    console.log('❌ 未找到相关笔记');
    return;
  }
  
  console.log(`✅ 找到 ${notes.length} 篇相关笔记\n`);
  
  if (mode === 'search') {
    // 仅显示列表
    for (const note of notes) {
      console.log(`• ${note.title}`);
      console.log(`  ID: ${note.doc_id}`);
      console.log('');
    }
  } else {
    // 获取内容并生成纲要
    for (let i = 0; i < notes.length; i++) {
      const note = notes[i];
      console.log(`📄 [${i+1}] ${note.title}`);
      console.log(`   ID: ${note.doc_id}`);
      
      if (mode === 'outline' || mode === 'all') {
        try {
          const content = await getNoteContent(note.doc_id);
          if (content) {
            const text = content.text || content.content || '';
            const { outline, preview } = generateOutline(text);
            
            if (outline.length > 0) {
              console.log('\n   【纲要】');
              outline.forEach((item, idx) => {
                console.log(`   ${idx + 1}. ${item}`);
              });
            }
            
            if (preview) {
              console.log('\n   【内容预览】');
              const previewLines = preview.split('\n').slice(0, 3);
              previewLines.forEach(line => {
                if (line.trim()) console.log(`   ${line.substring(0, 80)}`);
              });
            }
          }
        } catch (e) {
          console.log(`   获取内容失败: ${e.message}`);
        }
      }
      console.log('\n---\n');
    }
  }
}

main().catch(console.error);
