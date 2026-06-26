/**
 * Playwright 下载处理助手
 * 自动监听下载事件，用正确的原始文件名保存文件
 */

const path = require('path');
const fs = require('fs');

class DownloadHelper {
  /**
   * 创建下载助手实例
   * @param {Page} page - Playwright page 实例
   * @param {Object} options - 配置选项
   * @param {string} options.downloadDir - 下载目录，支持 ~ 符号，默认 ~/downloads
   * @param {boolean} options.debug - 是否显示调试信息，默认 false
   */
  constructor(page, options = {}) {
    this.page = page;
    this.downloadDir = options.downloadDir || '~/downloads';
    this.debug = options.debug || false;
    this.downloads = [];
    this._setupDone = false;
  }

  /**
   * 初始化下载监听器
   * 创建下载目录（如果不存在）
   * @returns {string} 下载目录的绝对路径
   */
  async setup() {
    if (this._setupDone) {
      return this._getDownloadDir();
    }

    const dir = this._getDownloadDir();

    // 确保目录存在
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
      if (this.debug) {
        console.log(`📁 创建下载目录: ${dir}`);
      }
    }

    // 监听下载事件
    this.page.on('download', async (download) => {
      await this._handleDownload(download);
    });

    this._setupDone = true;
    return dir;
  }

  /**
   * 处理单个下载事件
   * @private
   */
  async _handleDownload(download) {
    const filename = download.suggestedFilename();
    const url = download.url();
    const filePath = path.join(this._getDownloadDir(), filename);

    if (this.debug) {
      console.log('\n========================================');
      console.log('📥 检测到下载事件');
      console.log('========================================');
      console.log('📁 文件名:', filename);
      console.log('🔗 URL:', url);
      console.log('💾 保存路径:', filePath);
    }

    try {
      await download.saveAs(filePath);
      this.downloads.push(filePath);

      if (this.debug) {
        console.log('✅ 下载成功');
        console.log('========================================\n');
      }
    } catch (error) {
      if (this.debug) {
        console.log('❌ 下载失败:', error.message);
        console.log('========================================\n');
      }
      throw error;
    }
  }

  /**
   * 解析下载目录路径（支持 ~ 符号）
   * @private
   */
  _getDownloadDir() {
    return this.downloadDir.startsWith('~')
      ? path.join(process.env.HOME, this.downloadDir.slice(1))
      : this.downloadDir;
  }

  /**
   * 获取已下载的文件列表
   * @returns {Array<string>} 文件路径数组
   */
  getDownloadedFiles() {
    return [...this.downloads];
  }

  /**
   * 清空下载历史记录
   */
  clearHistory() {
    this.downloads = [];
  }

  /**
   * 移除下载监听器
   */
  dispose() {
    this.page.removeAllListeners('download');
    this._setupDone = false;
  }
}

module.exports = DownloadHelper;
