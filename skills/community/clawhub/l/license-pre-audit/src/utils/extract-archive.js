#!/usr/bin/env node
/**
 * 压缩包解压工具
 * 支持 zip, rar, tar, tar.gz, tgz
 */

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

/**
 * 检测文件类型
 * @param {string} filePath - 文件路径
 * @returns {string} 文件类型（zip/rar/tar/targz/unknown）
 */
function detectArchiveType(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  
  if (ext === '.zip') return 'zip';
  if (ext === '.rar') return 'rar';
  if (ext === '.tar') return 'tar';
  if (ext === '.gz' || ext === '.tgz') {
    // 检查是否是 .tar.gz
    const base = path.basename(filePath, ext);
    if (path.extname(base) === '.tar') return 'targz';
    return 'gz';
  }
  
  return 'unknown';
}

/**
 * 解压压缩包
 * @param {string} archivePath - 压缩包路径
 * @param {string} extractTo - 解压目标目录
 * @returns {string[]} 解压的文件列表
 */
function extractArchive(archivePath, extractTo) {
  const archiveType = detectArchiveType(archivePath);
  
  console.error(`  📦 检测到压缩包类型：${archiveType}`);
  console.error(`  📂 解压到：${extractTo}`);
  
  // 创建解压目录
  if (!fs.existsSync(extractTo)) {
    fs.mkdirSync(extractTo, { recursive: true });
  }
  
  let result;
  
  switch (archiveType) {
    case 'zip':
      result = spawnSync('unzip', ['-o', archivePath, '-d', extractTo], { encoding: 'utf8' });
      break;
    
    case 'rar':
      result = spawnSync('unrar', ['x', '-o+', archivePath, extractTo + '/'], { encoding: 'utf8' });
      break;
    
    case 'tar':
      result = spawnSync('tar', ['-xf', archivePath, '-C', extractTo], { encoding: 'utf8' });
      break;
    
    case 'targz':
    case 'gz':
      result = spawnSync('tar', ['-xzf', archivePath, '-C', extractTo], { encoding: 'utf8' });
      break;
    
    default:
      throw new Error(`不支持的压缩包格式：${archiveType}`);
  }
  
  if (result.status !== 0) {
    const errorMsg = result.stderr || result.stdout || '未知错误';
    throw new Error(`解压失败：${errorMsg}`);
  }
  
  console.error('  ✓ 解压完成');
  
  // 获取解压的文件列表
  const files = getAllFiles(extractTo);
  console.error(`  📄 解压出 ${files.length} 个文件`);
  
  return files;
}

/**
 * 递归获取目录下所有文件
 * @param {string} dirPath - 目录路径
 * @returns {string[]} 文件路径列表
 */
function getAllFiles(dirPath) {
  const files = [];
  
  function walk(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    
    for (const entry of entries) {
      const fullPath = path.join(dir, entry.name);
      
      if (entry.isDirectory()) {
        walk(fullPath);
      } else {
        files.push(fullPath);
      }
    }
  }
  
  walk(dirPath);
  return files;
}

/**
 * 验证文件类型
 * @param {string} filePath - 文件路径
 * @param {string[]} allowedExtensions - 允许的文件扩展名
 * @returns {boolean} 是否合法
 */
function validateFileType(filePath, allowedExtensions) {
  const ext = path.extname(filePath).toLowerCase();
  return allowedExtensions.includes(ext);
}

/**
 * 过滤合法的文件
 * @param {string[]} files - 文件列表
 * @param {string[]} allowedExtensions - 允许的文件扩展名
 * @returns {string[]} 合法文件列表
 */
function filterValidFiles(files, allowedExtensions) {
  return files.filter(f => validateFileType(f, allowedExtensions));
}

module.exports = {
  detectArchiveType,
  extractArchive,
  getAllFiles,
  validateFileType,
  filterValidFiles
};
