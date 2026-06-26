/**
 * 版本管理器 v2.6.0
 * 
 * 支持 PRD 版本管理、回溯、对比
 */

const fs = require('fs');
const path = require('path');

class VersionManager {
  constructor(outputDir) {
    this.outputDir = outputDir;
    this.versionsDir = path.join(outputDir, '.versions');
    this.ensureVersionsDir();
  }
  
  /**
   * 确保版本目录存在
   */
  ensureVersionsDir() {
    if (!fs.existsSync(this.versionsDir)) {
      fs.mkdirSync(this.versionsDir, { recursive: true });
    }
  }
  
  /**
   * 获取所有版本
   */
  getVersions() {
    if (!fs.existsSync(this.versionsDir)) {
      return [];
    }
    
    const versions = fs.readdirSync(this.versionsDir)
      .filter(name => name.startsWith('v'))
      .sort((a, b) => {
        const numA = parseInt(a.replace('v', ''));
        const numB = parseInt(b.replace('v', ''));
        return numA - numB;
      });
    
    return versions;
  }
  
  /**
   * 获取最新版本号
   */
  getLatestVersion() {
    const versions = this.getVersions();
    if (versions.length === 0) {
      return null;
    }
    return versions[versions.length - 1];
  }
  
  /**
   * 获取下一个版本号
   */
  getNextVersion() {
    const latest = this.getLatestVersion();
    if (!latest) {
      return 'v1';
    }
    
    const num = parseInt(latest.replace('v', ''));
    return `v${num + 1}`;
  }
  
  /**
   * 创建新版本
   */
  async createVersion(versionName = null) {
    const version = versionName || this.getNextVersion();
    const versionDir = path.join(this.versionsDir, version);
    
    console.log(`📦 创建版本：${version}`);
    
    // 创建版本目录
    if (!fs.existsSync(versionDir)) {
      fs.mkdirSync(versionDir, { recursive: true });
    }
    
    // 复制当前所有文件到版本目录（包括 Word 文件）
    const files = fs.readdirSync(this.outputDir);
    const copiedFiles = [];
    
    files.forEach(file => {
      if (file !== '.versions') {
        const src = path.join(this.outputDir, file);
        const dst = path.join(versionDir, file);
        
        try {
          if (fs.statSync(src).isDirectory()) {
            fs.cpSync(src, dst, { recursive: true });
          } else {
            fs.copyFileSync(src, dst);
          }
          copiedFiles.push(file);
        } catch (error) {
          console.warn(`⚠️  复制文件失败：${file} - ${error.message}`);
        }
      }
    });
    
    // 创建版本元数据
    const metadata = {
      version: version,
      createdAt: new Date().toISOString(),
      files: copiedFiles,
      prdSummary: this.extractPRDSummary(path.join(this.outputDir, 'PRD.md')),
      wordFile: copiedFiles.find(f => f.endsWith('.docx')) || null
    };
    
    fs.writeFileSync(
      path.join(versionDir, '.version.json'),
      JSON.stringify(metadata, null, 2),
      'utf8'
    );
    
    console.log(`✅ 版本 ${version} 创建完成`);
    
    return version;
  }
  
  /**
   * 提取 PRD 摘要
   */
  extractPRDSummary(prdPath) {
    if (!fs.existsSync(prdPath)) {
      return null;
    }
    
    const content = fs.readFileSync(prdPath, 'utf8');
    const lines = content.split('\n');
    
    // 提取标题和功能列表
    const title = lines.find(line => line.startsWith('# '))?.replace('# ', '') || 'Untitled';
    const features = lines
      .filter(line => line.startsWith('- 功能') || line.startsWith('## 4. 功能需求'))
      .slice(0, 5);
    
    return {
      title: title,
      featureCount: features.length,
      wordCount: content.length
    };
  }
  
  /**
   * 恢复指定版本
   */
  async restoreVersion(version) {
    const versionDir = path.join(this.versionsDir, version);
    
    if (!fs.existsSync(versionDir)) {
      throw new Error(`版本不存在：${version}`);
    }
    
    console.log(`🔄 恢复版本：${version}`);
    
    // 备份当前版本
    await this.createVersion(`backup-${new Date().getTime()}`);
    
    // 清空 outputDir（除 .versions）
    const files = fs.readdirSync(this.outputDir);
    files.forEach(file => {
      if (file !== '.versions') {
        const filePath = path.join(this.outputDir, file);
        if (fs.statSync(filePath).isDirectory()) {
          fs.rmSync(filePath, { recursive: true, force: true });
        } else {
          fs.unlinkSync(filePath);
        }
      }
    });
    
    // 复制版本文件到 outputDir
    const versionFiles = fs.readdirSync(versionDir);
    versionFiles.forEach(file => {
      if (file !== '.version.json') {
        const src = path.join(versionDir, file);
        const dst = path.join(this.outputDir, file);
        
        if (fs.statSync(src).isDirectory()) {
          fs.cpSync(src, dst, { recursive: true });
        } else {
          fs.copyFileSync(src, dst);
        }
      }
    });
    
    console.log(`✅ 版本 ${version} 恢复完成`);
  }
  
  /**
   * 对比两个版本
   */
  async diffVersions(version1, version2) {
    const version1Dir = path.join(this.versionsDir, version1);
    const version2Dir = path.join(this.versionsDir, version2);
    
    if (!fs.existsSync(version1Dir) || !fs.existsSync(version2Dir)) {
      throw new Error('版本不存在');
    }
    
    const prd1Path = path.join(version1Dir, 'PRD.md');
    const prd2Path = path.join(version2Dir, 'PRD.md');
    
    if (!fs.existsSync(prd1Path) || !fs.existsSync(prd2Path)) {
      throw new Error('PRD 文件不存在');
    }
    
    const prd1 = fs.readFileSync(prd1Path, 'utf8');
    const prd2 = fs.readFileSync(prd2Path, 'utf8');
    
    // 简单对比
    const diff = {
      version1: version1,
      version2: version2,
      wordCountDiff: prd2.length - prd1.length,
      added: prd2.length > prd1.length,
      removed: prd2.length < prd1.length,
      unchanged: prd1 === prd2
    };
    
    return diff;
  }
  
  /**
   * 获取版本列表（带摘要）
   */
  getVersionList() {
    const versions = this.getVersions();
    
    return versions.map(version => {
      const metadataPath = path.join(this.versionsDir, version, '.version.json');
      if (fs.existsSync(metadataPath)) {
        return JSON.parse(fs.readFileSync(metadataPath, 'utf8'));
      }
      return { version: version };
    });
  }
  
  /**
   * 清理旧版本（保留最近 N 个）
   */
  cleanup(keepLast = 5) {
    const versions = this.getVersions();
    
    if (versions.length <= keepLast) {
      return;
    }
    
    const toDelete = versions.slice(0, versions.length - keepLast);
    
    toDelete.forEach(version => {
      const versionDir = path.join(this.versionsDir, version);
      fs.rmSync(versionDir, { recursive: true, force: true });
      console.log(`🗑️  删除旧版本：${version}`);
    });
  }
}

module.exports = { VersionManager };
