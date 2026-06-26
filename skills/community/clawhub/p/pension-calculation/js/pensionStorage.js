/**
 * 养老金数据存储管理
 * 支持多种存储方式：localStorage、文件导出/导入
 */

const PensionStorage = {
  // 存储键名
  STORAGE_KEY: 'pensionData',
  
  /**
   * 从 localStorage 加载数据
   */
  loadFromLocal() {
    try {
      const saved = localStorage.getItem(this.STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        console.log('Data loaded from localStorage');
        return parsed;
      }
    } catch (error) {
      console.error('Failed to load from localStorage:', error);
    }
    return null;
  },

  /**
   * 保存数据到 localStorage
   */
  saveToLocal(data) {
    try {
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(data));
      console.log('Data saved to localStorage');
      return true;
    } catch (error) {
      console.error('Failed to save to localStorage:', error);
      return false;
    }
  },

  /**
   * 从 localStorage 删除数据
   */
  removeFromLocal() {
    try {
      localStorage.removeItem(this.STORAGE_KEY);
      console.log('Data removed from localStorage');
      return true;
    } catch (error) {
      console.error('Failed to remove from localStorage:', error);
      return false;
    }
  },

  /**
   * 导出数据为 JSON 文件
   */
  exportToFile(data, filename = 'pension-data.json') {
    try {
      const jsonStr = JSON.stringify(data, null, 2);
      const blob = new Blob([jsonStr], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      URL.revokeObjectURL(url);
      console.log('Data exported to file:', filename);
      return true;
    } catch (error) {
      console.error('Failed to export data:', error);
      return false;
    }
  },

  /**
   * 从 JSON 文件导入数据
   */
  async importFromFile(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      
      reader.onload = (event) => {
        try {
          const data = JSON.parse(event.target.result);
          console.log('Data imported from file:', file.name);
          resolve(data);
        } catch (error) {
          reject(new Error('Invalid JSON file: ' + error.message));
        }
      };
      
      reader.onerror = () => {
        reject(new Error('Failed to read file'));
      };
      
      reader.readAsText(file);
    });
  },

  /**
   * 保存数据到文件系统（Node.js 环境）
   */
  async saveToFile(data, filePath = './pension-data.json') {
    if (typeof window !== 'undefined') {
      console.warn('File system save is only available in Node.js environment');
      return false;
    }
    
    try {
      const fs = require('fs');
      const path = require('path');
      
      const fullPath = path.resolve(filePath);
      fs.writeFileSync(fullPath, JSON.stringify(data, null, 2), 'utf8');
      console.log('Data saved to file:', fullPath);
      return true;
    } catch (error) {
      console.error('Failed to save to file:', error);
      return false;
    }
  },

  /**
   * 从文件系统加载数据（Node.js 环境）
   */
  async loadFromFile(filePath = './pension-data.json') {
    if (typeof window !== 'undefined') {
      console.warn('File system load is only available in Node.js environment');
      return null;
    }
    
    try {
      const fs = require('fs');
      const path = require('path');
      
      const fullPath = path.resolve(filePath);
      if (!fs.existsSync(fullPath)) {
        console.log('File not found:', fullPath);
        return null;
      }
      
      const content = fs.readFileSync(fullPath, 'utf8');
      const data = JSON.parse(content);
      console.log('Data loaded from file:', fullPath);
      return data;
    } catch (error) {
      console.error('Failed to load from file:', error);
      return null;
    }
  },

  /**
   * 创建文件选择器用于导入
   */
  createFileInput(onFileSelected) {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json,application/json';
    input.style.display = 'none';
    
    input.addEventListener('change', async (event) => {
      const file = event.target.files[0];
      if (file) {
        try {
          const data = await this.importFromFile(file);
          onFileSelected(null, data);
        } catch (error) {
          onFileSelected(error, null);
        }
      }
      // 清除选择，允许重复选择同一文件
      input.value = '';
    });
    
    document.body.appendChild(input);
    input.click();
    
    // 清理
    setTimeout(() => {
      if (input.parentNode) {
        document.body.removeChild(input);
      }
    }, 1000);
  }
};

// 导出模块
if (typeof module !== 'undefined' && module.exports) {
  module.exports = PensionStorage;
}
