const fs = require('fs');
const path = require('path');

// 数据管理类
class DataManager {
    constructor() {
        this.dataDir = path.join(__dirname, 'data');
        this.ensureDataDir();
    }

    // 确保数据目录存在
    ensureDataDir() {
        if (!fs.existsSync(this.dataDir)) {
            fs.mkdirSync(this.dataDir, { recursive: true });
        }
    }

    // 保存用户偏好
    saveUserPreferences(preferences) {
        const filePath = path.join(this.dataDir, 'preferences.json');
        try {
            fs.writeFileSync(filePath, JSON.stringify(preferences, null, 2));
            return true;
        } catch (error) {
            console.error('保存用户偏好失败:', error);
            return false;
        }
    }

    // 获取用户偏好
    getUserPreferences() {
        const filePath = path.join(this.dataDir, 'preferences.json');
        try {
            if (fs.existsSync(filePath)) {
                const data = fs.readFileSync(filePath, 'utf8');
                return JSON.parse(data);
            }
            return this.getDefaultPreferences();
        } catch (error) {
            console.error('读取用户偏好失败:', error);
            return this.getDefaultPreferences();
        }
    }

    // 获取默认偏好
    getDefaultPreferences() {
        return {
            theme: 'light',
            language: 'zh',
            favoriteTools: [],
            searchHistory: [],
            translationSettings: {
                sourceLang: 'en',
                targetLang: 'zh'
            },
            calculatorSettings: {
                autoCalculate: false,
                showExamples: true
            }
        };
    }

    // 保存搜索历史
    saveSearchHistory(tool, query, result) {
        const preferences = this.getUserPreferences();
        const historyItem = {
            tool,
            query,
            result: typeof result === 'string' ? result : JSON.stringify(result),
            timestamp: new Date().toISOString()
        };

        preferences.searchHistory.unshift(historyItem);
        
        // 只保留最近50条记录
        if (preferences.searchHistory.length > 50) {
            preferences.searchHistory = preferences.searchHistory.slice(0, 50);
        }

        return this.saveUserPreferences(preferences);
    }

    // 获取搜索历史
    getSearchHistory(limit = 10) {
        const preferences = this.getUserPreferences();
        return preferences.searchHistory.slice(0, limit);
    }

    // 添加收藏工具
    addToFavorites(toolName) {
        const preferences = this.getUserPreferences();
        if (!preferences.favoriteTools.includes(toolName)) {
            preferences.favoriteTools.push(toolName);
            return this.saveUserPreferences(preferences);
        }
        return true;
    }

    // 移除收藏工具
    removeFromFavorites(toolName) {
        const preferences = this.getUserPreferences();
        preferences.favoriteTools = preferences.favoriteTools.filter(tool => tool !== toolName);
        return this.saveUserPreferences(preferences);
    }

    // 获取收藏工具
    getFavorites() {
        const preferences = this.getUserPreferences();
        return preferences.favoriteTools;
    }

    // 保存统计数据
    saveStatistics(stats) {
        const filePath = path.join(this.dataDir, 'statistics.json');
        try {
            fs.writeFileSync(filePath, JSON.stringify(stats, null, 2));
            return true;
        } catch (error) {
            console.error('保存统计数据失败:', error);
            return false;
        }
    }

    // 获取统计数据
    getStatistics() {
        const filePath = path.join(this.dataDir, 'statistics.json');
        try {
            if (fs.existsSync(filePath)) {
                const data = fs.readFileSync(filePath, 'utf8');
                return JSON.parse(data);
            }
            return this.getDefaultStatistics();
        } catch (error) {
            console.error('读取统计数据失败:', error);
            return this.getDefaultStatistics();
        }
    }

    // 获取默认统计数据
    getDefaultStatistics() {
        return {
            totalQueries: 0,
            toolUsage: {
                dictionary: 0,
                translate: 0,
                facts: 0,
                calculator: 0,
                history: 0
            },
            lastUsed: null,
            favoriteTools: []
        };
    }

    // 更新统计数据
    updateStatistics(toolName) {
        const stats = this.getStatistics();
        stats.totalQueries++;
        stats.toolUsage[toolName]++;
        stats.lastUsed = new Date().toISOString();
        
        this.saveStatistics(stats);
        return stats;
    }

    // 导出数据
    exportData() {
        const preferences = this.getUserPreferences();
        const statistics = this.getStatistics();
        const history = this.getSearchHistory();
        
        return {
            preferences,
            statistics,
            history,
            exportDate: new Date().toISOString(),
            version: '1.0'
        };
    }

    // 导入数据
    importData(data) {
        try {
            if (data.preferences) {
                this.saveUserPreferences(data.preferences);
            }
            if (data.statistics) {
                this.saveStatistics(data.statistics);
            }
            return true;
        } catch (error) {
            console.error('导入数据失败:', error);
            return false;
        }
    }

    // 清除所有数据
    clearAllData() {
        try {
            const files = fs.readdirSync(this.dataDir);
            files.forEach(file => {
                fs.unlinkSync(path.join(this.dataDir, file));
            });
            return true;
        } catch (error) {
            console.error('清除数据失败:', error);
            return false;
        }
    }
}

module.exports = DataManager;