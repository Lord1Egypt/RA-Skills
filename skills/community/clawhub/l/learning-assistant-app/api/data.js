const express = require('express');
const router = express.Router();
const DataManager = require('../dataManager');

const dataManager = new DataManager();

// 获取用户偏好
router.get('/preferences', (req, res) => {
    try {
        const preferences = dataManager.getUserPreferences();
        res.json(preferences);
    } catch (error) {
        res.status(500).json({ error: '获取用户偏好失败' });
    }
});

// 保存用户偏好
router.post('/preferences', (req, res) => {
    try {
        const preferences = req.body;
        const success = dataManager.saveUserPreferences(preferences);
        
        if (success) {
            res.json({ message: '用户偏好保存成功' });
        } else {
            res.status(500).json({ error: '保存用户偏好失败' });
        }
    } catch (error) {
        res.status(500).json({ error: '保存用户偏好失败' });
    }
});

// 获取搜索历史
router.get('/history', (req, res) => {
    try {
        const limit = parseInt(req.query.limit) || 10;
        const history = dataManager.getSearchHistory(limit);
        res.json(history);
    } catch (error) {
        res.status(500).json({ error: '获取搜索历史失败' });
    }
});

// 保存搜索历史
router.post('/history', (req, res) => {
    try {
        const { tool, query, result } = req.body;
        
        if (!tool || !query) {
            return res.status(400).json({ error: '缺少必要参数' });
        }
        
        const success = dataManager.saveSearchHistory(tool, query, result);
        
        if (success) {
            res.json({ message: '搜索历史保存成功' });
        } else {
            res.status(500).json({ error: '保存搜索历史失败' });
        }
    } catch (error) {
        res.status(500).json({ error: '保存搜索历史失败' });
    }
});

// 添加收藏工具
router.post('/favorites/:tool', (req, res) => {
    try {
        const { tool } = req.params;
        const success = dataManager.addToFavorites(tool);
        
        if (success) {
            res.json({ message: '工具已添加到收藏' });
        } else {
            res.status(500).json({ error: '添加收藏失败' });
        }
    } catch (error) {
        res.status(500).json({ error: '添加收藏失败' });
    }
});

// 移除收藏工具
router.delete('/favorites/:tool', (req, res) => {
    try {
        const { tool } = req.params;
        const success = dataManager.removeFromFavorites(tool);
        
        if (success) {
            res.json({ message: '工具已从收藏中移除' });
        } else {
            res.status(500).json({ error: '移除收藏失败' });
        }
    } catch (error) {
        res.status(500).json({ error: '移除收藏失败' });
    }
});

// 获取收藏工具
router.get('/favorites', (req, res) => {
    try {
        const favorites = dataManager.getFavorites();
        res.json(favorites);
    } catch (error) {
        res.status(500).json({ error: '获取收藏失败' });
    }
});

// 获取统计数据
router.get('/statistics', (req, res) => {
    try {
        const statistics = dataManager.getStatistics();
        res.json(statistics);
    } catch (error) {
        res.status(500).json({ error: '获取统计数据失败' });
    }
});

// 更新统计数据
router.post('/statistics/:tool', (req, res) => {
    try {
        const { tool } = req.params;
        const statistics = dataManager.updateStatistics(tool);
        res.json(statistics);
    } catch (error) {
        res.status(500).json({ error: '更新统计数据失败' });
    }
});

// 导出数据
router.get('/export', (req, res) => {
    try {
        const data = dataManager.exportData();
        res.json(data);
    } catch (error) {
        res.status(500).json({ error: '导出数据失败' });
    }
});

// 导入数据
router.post('/import', (req, res) => {
    try {
        const data = req.body;
        const success = dataManager.importData(data);
        
        if (success) {
            res.json({ message: '数据导入成功' });
        } else {
            res.status(500).json({ error: '数据导入失败' });
        }
    } catch (error) {
        res.status(500).json({ error: '数据导入失败' });
    }
});

// 清除所有数据
router.delete('/clear', (req, res) => {
    try {
        const success = dataManager.clearAllData();
        
        if (success) {
            res.json({ message: '所有数据已清除' });
        } else {
            res.status(500).json({ error: '清除数据失败' });
        }
    } catch (error) {
        res.status(500).json({ error: '清除数据失败' });
    }
});

module.exports = router;