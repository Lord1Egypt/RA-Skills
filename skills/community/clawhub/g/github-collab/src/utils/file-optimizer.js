/**
 * File Operations Optimization Module - 文件读写优化
 * 
 * 优化策略：
 * - 文件缓存（减少磁盘 IO）
 * - 流式读写（处理大文件）
 * - 批量文件操作（合并请求）
 * - 压缩大文件（节省空间）
 * 
 * @author 小码
 * @version 1.0.0
 */

const fs = require('fs');
const fsPromises = require('fs/promises');
const path = require('path');
const stream = require('stream');
const zlib = require('zlib');
const { Cache } = require('./cache');

// ============================================
// 文件缓存管理器
// ============================================

class FileCache {
  /**
   * 创建文件缓存实例
   * @param {Object} options - 配置选项
   * @param {string} options.cacheDir - 缓存目录
   * @param {number} options.maxSize - 最大缓存大小（MB）
   * @param {number} options.defaultTTL - 默认 TTL（秒）
   */
  constructor(options = {}) {
    this.cacheDir = options.cacheDir || './.file-cache';
    this.maxSizeMB = options.maxSize || 100;
    this.defaultTTL = options.defaultTTL || 3600;
    
    // 内存缓存（存储文件内容）
    this.memoryCache = new Cache({
      maxSize: options.cacheMaxSize || 1000,
      defaultTTL: this.defaultTTL,
      enableLRU: true
    });
    
    // 初始化缓存目录
    this._ensureCacheDir();
  }

  /**
   * 确保缓存目录存在
   * @private
   */
  async _ensureCacheDir() {
    try {
      await fsPromises.mkdir(this.cacheDir, { recursive: true });
    } catch (err) {
      console.error('Failed to create cache directory:', err);
    }
  }

  /**
   * 生成文件缓存键
   * @param {string} filePath - 文件路径
   * @returns {string} 缓存键
   */
  _generateKey(filePath) {
    const stat = fs.statSync(filePath);
    const mtime = stat.mtime.getTime();
    const size = stat.size;
    return `file:${filePath}:${mtime}:${size}`;
  }

  /**
   * 从文件读取并缓存
   * @param {string} filePath - 文件路径
   * @param {Object} options - 选项
   * @param {number} options.ttl - TTL（秒）
   * @param {string} options.encoding - 编码（默认 utf8）
   * @returns {Promise<string|Buffer>} 文件内容
   */
  async read(filePath, options = {}) {
    const { ttl = this.defaultTTL, encoding = 'utf8' } = options;
    
    // 生成缓存键
    const key = this._generateKey(filePath);
    
    // 尝试从内存缓存获取
    const cached = this.memoryCache.get(key);
    if (cached !== undefined) {
      return cached;
    }
    
    // 缓存未命中，读取文件
    const content = await fsPromises.readFile(filePath, { encoding });
    
    // 写入缓存
    this.memoryCache.set(key, content, ttl);
    
    return content;
  }

  /**
   * 写入文件并更新缓存
   * @param {string} filePath - 文件路径
   * @param {string|Buffer} content - 内容
   * @param {Object} options - 选项
   * @returns {Promise<void>}
   */
  async write(filePath, content, options = {}) {
    const { encoding = 'utf8' } = options;
    
    // 写入文件
    await fsPromises.writeFile(filePath, content, { encoding });
    
    // 清除旧缓存
    const oldKey = this._generateKey(filePath);
    this.memoryCache.delete(oldKey);
    
    // 生成新缓存键并写入
    const newKey = this._generateKey(filePath);
    this.memoryCache.set(newKey, content, this.defaultTTL);
  }

  /**
   * 批量读取文件
   * @param {Array} filePaths - 文件路径数组
   * @param {Object} options - 选项
   * @returns {Promise<Object>} 文件内容映射
   */
  async readMany(filePaths, options = {}) {
    const results = {};
    
    // 并行读取
    const promises = filePaths.map(async (filePath) => {
      try {
        const content = await this.read(filePath, options);
        results[filePath] = content;
      } catch (err) {
        console.error(`Failed to read ${filePath}:`, err.message);
      }
    });
    
    await Promise.all(promises);
    return results;
  }

  /**
   * 批量写入文件
   * @param {Object} files - 文件映射 {filePath: content}
   * @param {Object} options - 选项
   * @returns {Promise<void>}
   */
  async writeMany(files, options = {}) {
    const promises = Object.entries(files).map(async ([filePath, content]) => {
      try {
        await this.write(filePath, content, options);
      } catch (err) {
        console.error(`Failed to write ${filePath}:`, err.message);
      }
    });
    
    await Promise.all(promises);
  }

  /**
   * 清除文件缓存
   * @param {string} prefix - 文件路径前缀
   */
  clear(prefix = '') {
    if (prefix) {
      this.memoryCache.invalidateByPrefix(`file:${prefix}`);
    } else {
      this.memoryCache.invalidateByPrefix('file:');
    }
  }

  /**
   * 获取缓存统计
   * @returns {Object} 统计信息
   */
  getStats() {
    return this.memoryCache.getStats();
  }
}

// ============================================
// 流式文件读写
// ============================================

class StreamFileOps {
  /**
   * 流式读取大文件
   * @param {string} filePath - 文件路径
   * @param {Object} options - 选项
   * @param {number} options.highWaterMark - 缓冲区大小
   * @param {string} options.encoding - 编码
   * @returns {ReadableStream} 可读流
   */
  static createReadStream(filePath, options = {}) {
    const { highWaterMark = 64 * 1024, encoding = null } = options;
    
    return fs.createReadStream(filePath, {
      highWaterMark,
      encoding
    });
  }

  /**
   * 流式写入文件
   * @param {string} filePath - 文件路径
   * @param {Object} options - 选项
   * @returns {WritableStream} 可写流
   */
  static createWriteStream(filePath, options = {}) {
    const { highWaterMark = 64 * 1024, encoding = 'utf8', flags = 'w' } = options;
    
    // 确保目录存在
    const dir = path.dirname(filePath);
    fs.mkdirSync(dir, { recursive: true });
    
    return fs.createWriteStream(filePath, {
      highWaterMark,
      encoding,
      flags
    });
  }

  /**
   * 流式复制文件
   * @param {string} source - 源文件
   * @param {string} dest - 目标文件
   * @returns {Promise<void>}
   */
  static async copyStream(source, dest) {
    return new Promise((resolve, reject) => {
      const readStream = this.createReadStream(source);
      const writeStream = this.createWriteStream(dest);
      
      readStream.pipe(writeStream);
      
      writeStream.on('finish', () => {
        resolve();
      });
      
      writeStream.on('error', (err) => {
        reject(err);
      });
      
      readStream.on('error', (err) => {
        reject(err);
      });
    });
  }

  /**
   * 流式处理大文件（按行处理）
   * @param {string} filePath - 文件路径
   * @param {Function} lineProcessor - 行处理函数
   * @returns {Promise<number>} 处理的行数
   */
  static async processLineByLine(filePath, lineProcessor) {
    const readStream = this.createReadStream(filePath, { encoding: 'utf8' });
    let lineCount = 0;
    let remaining = '';
    
    return new Promise((resolve, reject) => {
      readStream.on('data', (chunk) => {
        const text = remaining + chunk.toString();
        const lines = text.split('\n');
        
        // 最后一行可能不完整
        remaining = lines.pop() || '';
        
        for (const line of lines) {
          if (line.trim()) {
            lineProcessor(line);
            lineCount++;
          }
        }
      });
      
      readStream.on('end', () => {
        // 处理最后一行
        if (remaining.trim()) {
          lineProcessor(remaining);
          lineCount++;
        }
        resolve(lineCount);
      });
      
      readStream.on('error', (err) => {
        reject(err);
      });
    });
  }

  /**
   * 流式文件拼接
   * @param {Array} sourceFiles - 源文件数组
   * @param {string} destFile - 目标文件
   * @returns {Promise<void>}
   */
  static async concatFiles(sourceFiles, destFile) {
    const writeStream = this.createWriteStream(destFile);
    
    for (const sourceFile of sourceFiles) {
      const readStream = this.createReadStream(sourceFile);
      await new Promise((resolve, reject) => {
        readStream.pipe(writeStream, { end: false });
        readStream.on('end', resolve);
        readStream.on('error', reject);
      });
    }
    
    writeStream.end();
    await new Promise((resolve) => writeStream.on('finish', resolve));
  }
}

// ============================================
// 批量文件操作
// ============================================

class BatchFileOps {
  /**
   * 批量删除文件
   * @param {Array} filePaths - 文件路径数组
   * @param {boolean} force - 是否强制删除
   * @returns {Promise<Object>} 删除结果
   */
  static async deleteMany(filePaths, force = false) {
    const results = {
      success: [],
      failed: []
    };
    
    for (const filePath of filePaths) {
      try {
        await fsPromises.unlink(filePath);
        results.success.push(filePath);
      } catch (err) {
        if (force || err.code !== 'ENOENT') {
          results.failed.push({ path: filePath, error: err.message });
        } else {
          results.success.push(filePath);
        }
      }
    }
    
    return results;
  }

  /**
   * 批量复制文件
   * @param {Array} operations - 操作数组 [{source, dest}]
   * @param {number} concurrency - 并发数
   * @returns {Promise<Object>} 复制结果
   */
  static async copyMany(operations, concurrency = 5) {
    const results = {
      success: [],
      failed: []
    };
    
    // 限制并发
    const batches = [];
    for (let i = 0; i < operations.length; i += concurrency) {
      batches.push(operations.slice(i, i + concurrency));
    }
    
    for (const batch of batches) {
      await Promise.all(batch.map(async (op) => {
        try {
          await fsPromises.copyFile(op.source, op.dest);
          results.success.push({ source: op.source, dest: op.dest });
        } catch (err) {
          results.failed.push({ source: op.source, dest: op.dest, error: err.message });
        }
      }));
    }
    
    return results;
  }

  /**
   * 批量移动文件
   * @param {Array} operations - 操作数组 [{source, dest}]
   * @returns {Promise<Object>} 移动结果
   */
  static async moveMany(operations) {
    const results = {
      success: [],
      failed: []
    };
    
    for (const op of operations) {
      try {
        await fsPromises.rename(op.source, op.dest);
        results.success.push({ source: op.source, dest: op.dest });
      } catch (err) {
        results.failed.push({ source: op.source, dest: op.dest, error: err.message });
      }
    }
    
    return results;
  }

  /**
   * 批量创建目录
   * @param {Array} dirs - 目录路径数组
   * @returns {Promise<Object>} 创建结果
   */
  static async mkdirMany(dirs, options = { recursive: true }) {
    const results = {
      success: [],
      failed: []
    };
    
    for (const dir of dirs) {
      try {
        await fsPromises.mkdir(dir, options);
        results.success.push(dir);
      } catch (err) {
        if (err.code !== 'EEXIST') {
          results.failed.push({ path: dir, error: err.message });
        } else {
          results.success.push(dir);
        }
      }
    }
    
    return results;
  }

  /**
   * 批量读取文件内容
   * @param {Array} filePaths - 文件路径数组
   * @param {Object} options - 选项
   * @returns {Promise<Object>} 文件内容映射
   */
  static async readMany(filePaths, options = { encoding: 'utf8' }) {
    const results = {};
    
    await Promise.all(filePaths.map(async (filePath) => {
      try {
        results[filePath] = await fsPromises.readFile(filePath, options);
      } catch (err) {
        console.error(`Failed to read ${filePath}:`, err.message);
      }
    }));
    
    return results;
  }
}

// ============================================
// 文件压缩
// ============================================

class FileCompressor {
  /**
   * 压缩文件（gzip）
   * @param {string} source - 源文件
   * @param {string} dest - 目标文件（.gz）
   * @param {number} level - 压缩级别 (0-9)
   * @returns {Promise<void>}
   */
  static async compress(source, dest, level = 6) {
    const gzip = zlib.createGzip({ level });
    const readStream = StreamFileOps.createReadStream(source);
    const writeStream = StreamFileOps.createWriteStream(dest);
    
    return new Promise((resolve, reject) => {
      readStream.pipe(gzip).pipe(writeStream);
      
      writeStream.on('finish', resolve);
      writeStream.on('error', reject);
      readStream.on('error', reject);
    });
  }

  /**
   * 解压缩文件（gzip）
   * @param {string} source - 源文件（.gz）
   * @param {string} dest - 目标文件
   * @returns {Promise<void>}
   */
  static async decompress(source, dest) {
    const gunzip = zlib.createGunzip();
    const readStream = StreamFileOps.createReadStream(source);
    const writeStream = StreamFileOps.createWriteStream(dest);
    
    return new Promise((resolve, reject) => {
      readStream.pipe(gunzip).pipe(writeStream);
      
      writeStream.on('finish', resolve);
      writeStream.on('error', reject);
      readStream.on('error', reject);
    });
  }

  /**
   * 压缩字符串
   * @param {string} data - 数据
   * @param {number} level - 压缩级别
   * @returns {Promise<Buffer>} 压缩后的 Buffer
   */
  static async compressString(data, level = 6) {
    return new Promise((resolve, reject) => {
      zlib.gzip(data, { level }, (err, buffer) => {
        if (err) reject(err);
        else resolve(buffer);
      });
    });
  }

  /**
   * 解压缩字符串
   * @param {Buffer} compressed - 压缩数据
   * @returns {Promise<string>} 解压后的字符串
   */
  static async decompressString(compressed) {
    return new Promise((resolve, reject) => {
      zlib.gunzip(compressed, (err, buffer) => {
        if (err) reject(err);
        else resolve(buffer.toString());
      });
    });
  }

  /**
   * 批量压缩文件
   * @param {Array} files - 文件路径数组
   * @param {string} outputDir - 输出目录
   * @returns {Promise<Object>} 压缩结果
   */
  static async compressMany(files, outputDir = './compressed') {
    await fsPromises.mkdir(outputDir, { recursive: true });
    
    const results = {
      success: [],
      failed: []
    };
    
    for (const file of files) {
      try {
        const dest = path.join(outputDir, path.basename(file) + '.gz');
        await this.compress(file, dest);
        results.success.push({ source: file, dest });
      } catch (err) {
        results.failed.push({ source: file, error: err.message });
      }
    }
    
    return results;
  }
}

// ============================================
// 文件操作优化器（整合所有优化）
// ============================================

class FileOptimizer {
  /**
   * 创建文件优化器实例
   * @param {Object} options - 配置选项
   */
  constructor(options = {}) {
    this.fileCache = new FileCache(options);
    this.stats = {
      reads: 0,
      writes: 0,
      cacheHits: 0,
      compressions: 0
    };
  }

  /**
   * 带缓存的文件读取
   */
  async read(filePath, options = {}) {
    this.stats.reads++;
    return this.fileCache.read(filePath, options);
  }

  /**
   * 带缓存的文件写入
   */
  async write(filePath, content, options = {}) {
    this.stats.writes++;
    return this.fileCache.write(filePath, content, options);
  }

  /**
   * 流式读取
   */
  createReadStream(filePath, options = {}) {
    return StreamFileOps.createReadStream(filePath, options);
  }

  /**
   * 流式写入
   */
  createWriteStream(filePath, options = {}) {
    return StreamFileOps.createWriteStream(filePath, options);
  }

  /**
   * 批量读取
   */
  async readMany(filePaths, options = {}) {
    this.stats.reads += filePaths.length;
    return this.fileCache.readMany(filePaths, options);
  }

  /**
   * 批量写入
   */
  async writeMany(files, options = {}) {
    this.stats.writes += Object.keys(files).length;
    return this.fileCache.writeMany(files, options);
  }

  /**
   * 压缩文件
   */
  async compress(source, dest, level = 6) {
    this.stats.compressions++;
    return FileCompressor.compress(source, dest, level);
  }

  /**
   * 获取统计
   */
  getStats() {
    const cacheStats = this.fileCache.getStats();
    return {
      ...this.stats,
      cache: cacheStats
    };
  }
}

// ============================================
// 导出模块
// ============================================

module.exports = {
  FileCache,
  StreamFileOps,
  BatchFileOps,
  FileCompressor,
  FileOptimizer
};

// ============================================
// 使用示例
// ============================================

/*
const { FileOptimizer, StreamFileOps, FileCompressor } = require('./file-optimized');

// 1. 初始化
const optimizer = new FileOptimizer({
  cacheDir: './.file-cache',
  maxSize: 100,  // 100MB
  defaultTTL: 3600  // 1 小时
});

// 2. 带缓存的文件读取
const content = await optimizer.read('./data/config.json');

// 3. 带缓存的文件写入
await optimizer.write('./data/output.txt', 'Hello World');

// 4. 流式处理大文件
await StreamFileOps.processLineByLine('./data/large.log', (line) => {
  console.log(line);
});

// 5. 流式复制大文件
await StreamFileOps.copyStream('./data/large-file.bin', './data/large-file-copy.bin');

// 6. 批量操作
await BatchFileOps.deleteMany(['./tmp/1.txt', './tmp/2.txt']);
await BatchFileOps.copyMany([
  { source: './src/a.txt', dest: './dest/a.txt' },
  { source: './src/b.txt', dest: './dest/b.txt' }
], 5);  // 并发数

// 7. 文件压缩
await FileCompressor.compress('./data/large-file.txt', './data/large-file.txt.gz');
await FileCompressor.decompress('./data/large-file.txt.gz', './data/large-file-decompressed.txt');

// 8. 查看统计
console.log(optimizer.getStats());
*/
