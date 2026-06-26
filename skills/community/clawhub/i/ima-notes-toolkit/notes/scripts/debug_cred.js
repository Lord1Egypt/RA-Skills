#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

// 尝试从配置文件读取
let CLIENT_ID = process.env.IMA_OPENAPI_CLIENTID;
console.log('Env IMA_CLIENT_ID:', CLIENT_ID);

const configDir = path.join(process.env.USERPROFILE || process.env.HOME, '.config', 'ima');
console.log('Config dir:', configDir);

if (!CLIENT_ID) {
  try { 
    const clientIdPath = path.join(configDir, 'client_id');
    console.log('Checking:', clientIdPath);
    CLIENT_ID = fs.readFileSync(clientIdPath, 'utf8').trim(); 
    console.log('From file:', CLIENT_ID);
  } catch (e) {
    console.log('Error:', e.message);
  }
}

if (!CLIENT_ID) {
  try { 
    const skillEnv = path.join(process.env.USERPROFILE, '.workbuddy', 'skills', 'ima笔记', 'notes', '.env');
    console.log('Checking skill env:', skillEnv);
    const envContent = fs.readFileSync(skillEnv, 'utf8');
    const match = envContent.match(/IMA_CLIENT_ID\s*=\s*(.+)/);
    if (match) {
      CLIENT_ID = match[1].trim();
      console.log('From skill env:', CLIENT_ID);
    }
  } catch (e) {
    console.log('Error:', e.message);
  }
}

console.log('Final CLIENT_ID:', CLIENT_ID);
